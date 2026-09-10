"""Algebraic / automata attack on period-2 L_0 certificates.

Does not overwrite strip_graph.py or strip_extend.py.
Does not claim a prize result.

Goal: for each onset T, find R(T) and multipliers A_{T,j} in
B = F2[u_i] / <u_i^2+u_i, u_i u_{i+1}> such that
    F_T = sum_j A_{T,j} F_{T+j}
in B. Equivalent, on Fibonacci strings, to: no u with F_T=1 and
R further zeros. Compactness gives existence once unsat is known;
this file looks for a T-uniform construction.

Run: python3 research/period2_certificate.py --certify
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_left_edge import (
    ONE,
    U0,
    anf_str,
    anf_vars,
    band,
    bor,
    compute_columns,
    eval_anf,
    max_index,
    reduce_no_consec,
    shift_anf,
)
from period2_vacuum import F_of_u, fib_strings, nvars, vacuum_F


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------


def bits_from_list(u):
    acc = 0
    for i, b in enumerate(u):
        if b:
            acc |= 1 << i
    return acc


def list_from_bits(bits, length):
    return [(bits >> i) & 1 for i in range(length)]


def eval_F_list(u, kmax):
    F, G = F_of_u(u, kmax)
    return F, G


def survivors(T, R, extra_u=0):
    """Fibonacci u of length nvars(T+R)+extra_u with F_T=1 and R zeros after."""
    top = T + R
    L = max(nvars(top), 1) + extra_u
    kmax = max(top, 2 * L + 2)
    out = []
    for u in fib_strings(L):
        F, _ = F_of_u(u, kmax)
        if F[T] != 1:
            continue
        if all(F[T + d] == 0 for d in range(1, R + 1)):
            out.append(u)
    return out


def forced_bits(models):
    """For each index, None if mixed, else the forced 0/1."""
    if not models:
        return []
    L = max(len(m) for m in models)
    forced = []
    for i in range(L):
        vals = {(m[i] if i < len(m) else 0) for m in models}
        if len(vals) == 1:
            forced.append(next(iter(vals)))
        else:
            forced.append(None)
    return forced


def fmt_forced(forced):
    chars = []
    for b in forced:
        chars.append("." if b is None else str(b))
    return "".join(chars)


def onset_table(Tmax, Rmax=24):
    rows = []
    cache = {}
    for T in range(1, Tmax + 1):
        maxR = -1
        nmax = 0
        last_models = []
        killed = None
        for R in range(0, Rmax + 1):
            top = T + R
            L = max(nvars(top), 1)
            K = top
            if L not in cache or cache[L][0] < K:
                strs = fib_strings(L)
                kneed = max(K, 2 * L + 2)
                cache[L] = (kneed, strs, [F_of_u(u, kneed)[0] for u in strs])
            strs = cache[L][1]
            rowsF = cache[L][2]
            models = []
            for u, F in zip(strs, rowsF):
                if F[T] != 1:
                    continue
                if all(F[T + d] == 0 for d in range(1, R + 1)):
                    models.append(u)
            n = len(models)
            if n:
                maxR = R
                nmax = n
                last_models = models
            else:
                killed = top
                break
        fb = forced_bits(last_models)
        # support of last-sat models (positions of 1s)
        supports = [tuple(i for i, b in enumerate(u) if b) for u in last_models]
        rows.append(
            {
                "T": T,
                "max_sat_R": maxR,
                "n_at_max": nmax,
                "killed_by": killed,
                "nvars_kill": nvars(killed) if killed is not None else None,
                "forced_prefix": fmt_forced(fb),
                "supports": supports[:12],
                "n_supports_shown": min(12, len(supports)),
            }
        )
        assert killed is not None, T
    return rows


# ---------------------------------------------------------------------------
# Sparse ANF structure
# ---------------------------------------------------------------------------


def column_anfs(kmax, reduce=True):
    F, G = compute_columns(kmax, reduce=reduce)
    rows = []
    for k in range(kmax + 1):
        rows.append(
            {
                "k": k,
                "F": anf_str(F[k]),
                "F_vars": anf_vars(F[k]),
                "F_deg": max((bin(m).count("1") for m in monomials_of(F[k])), default=0),
                "n_terms": bin(F[k]).count("1") if F[k] else 0,
                "G": anf_str(G[k]),
                "G_vars": anf_vars(G[k]),
            }
        )
    return rows, F, G


def monomials_of(p):
    out = []
    m = 0
    pp = p
    while pp:
        if pp & 1:
            out.append(m)
        pp >>= 1
        m += 1
    return out


def F_minus_shift(F, k, s):
    """F_k + S^s F_{k-s} as a reduced ANF (0 if they coincide)."""
    if k - s < 0:
        return None
    return reduce_no_consec(F[k] ^ shift_anf(F[k - s], s))


# ---------------------------------------------------------------------------
# Value-level shift identities on a zero run after a 1
# ---------------------------------------------------------------------------


def spatial_G_from_F(F, k):
    """G_k = F_{k+1} XOR (F_k OR F_{k-1}) as a value, k>=1."""
    if k < 1:
        raise ValueError("spatial identity starts at k=1")
    return F[k + 1] ^ (F[k] | F[k - 1])


def check_zero_run_shift(T, R, models=None, kmax_extra=8):
    """On L_0 survivors, compare F_*(u) with F_*(Su) and test derived identities.

    Derived (values, using spatial G and the fold G-recurrence):
      If F_T=1 and F_{T+1}=F_{T+2}=0 then
          F_{T+3} = 1 XOR F_{T+1}(Su).
    """
    if models is None:
        models = survivors(T, R)
    kmax = T + R + kmax_extra
    rows = []
    for u in models:
        F, G = F_of_u(u, kmax)
        Su = u[1:] + [0]
        FS, GS = F_of_u(Su, kmax)
        rec = {
            "u": u,
            "F_T": F[T],
            "zeros_ok": all(F[T + d] == 0 for d in range(1, R + 1)),
        }
        if R >= 2 and T + 3 <= kmax:
            # predicted F_{T+3}
            pred = 1 ^ FS[T + 1]
            rec["F_Tplus3"] = F[T + 3] if T + 3 < len(F) else None
            rec["pred_F_Tplus3"] = pred
            rec["id_T3"] = F[T + 3] == pred if T + 3 < len(F) else None
        # Does Su look like an onset at some T'?
        last1 = max((k for k in range(kmax + 1) if FS[k] == 1), default=-1)
        first1 = min((k for k in range(1, kmax + 1) if FS[k] == 1), default=-1)
        rec["Su_first1"] = first1
        rec["Su_last1"] = last1
        rec["Su_F_T"] = FS[T]
        rec["Su_F_Tplus1"] = FS[T + 1] if T + 1 <= kmax else None
        rec["Su_F_Tminus1"] = FS[T - 1] if T >= 1 else None
        rec["Su_F_Tplus2"] = FS[T + 2] if T + 2 <= kmax else None
        rows.append(rec)
    return rows


def derived_identity_T3_poly(T, kmax=None):
    """Check as polynomials: on the variety F_T=1, F_{T+1}=F_{T+2}=0,
    whether F_{T+3} + 1 + S F_{T+1} vanishes.

    Done by enumeration of Fibonacci strings of length nvars(T+3)+1
    (S F_{T+1} needs one extra bit).
    """
    if kmax is None:
        kmax = T + 6
    L = max(nvars(kmax), nvars(T + 1) + 1, 2)
    n_on_var = 0
    n_fail = 0
    for u in fib_strings(L):
        F, _ = F_of_u(u, kmax)
        if F[T] != 1 or F[T + 1] != 0 or F[T + 2] != 0:
            continue
        n_on_var += 1
        Su = u[1:] + [0]
        FS, _ = F_of_u(Su, kmax)
        if F[T + 3] != (1 ^ FS[T + 1]):
            n_fail += 1
    return {"T": T, "n_on_variety": n_on_var, "n_fail": n_fail, "L": L}


def propagate_zero_run(T, R, u):
    """From F_T=1 and R zeros, compute predicted later F via G spatial/fold.

    Returns a dict of implied constraints on F_*(Su).
    """
    kmax = T + R + 4
    F, G = F_of_u(u, kmax)
    Su = u[1:] + [0]
    FS, GS = F_of_u(Su, kmax)
    # Rebuild g from spatial
    g = [None] * (kmax + 1)
    g[0] = 1
    for k in range(1, kmax):
        g[k] = F[k + 1] ^ (F[k] | F[k - 1])
        if g[k] != G[k]:
            return {"spatial_fail": k}
    implied = []
    # For k>=2: G_k = F_{k-1}(Su) XOR (G_{k-1} OR G_{k-2})
    for k in range(2, min(T + R, kmax) + 1):
        rhs = FS[k - 1] ^ (G[k - 1] | G[k - 2])
        implied.append(
            {
                "k": k,
                "G_k": G[k],
                "fold_rhs": rhs,
                "implies_FSu": FS[k - 1],
                "match": rhs == G[k],
            }
        )
    return {
        "F": F[: kmax + 1],
        "G": G[: kmax + 1],
        "FS": FS[: kmax + 1],
        "implied_ok": all(x["match"] for x in implied),
    }


# ---------------------------------------------------------------------------
# T |-> T+2 and shift S on certificates
# ---------------------------------------------------------------------------


def test_shift_closure(table, T_list=None):
    """Does a last-sat model of T, shifted, become a last-sat model of T+2?

    Also: does S (drop u0) map the T-variety into a (T-delta)-variety?
    """
    rows = []
    byT = {r["T"]: r for r in table}
    if T_list is None:
        T_list = [r["T"] for r in table if r["T"] + 2 in byT]
    for T in T_list:
        if T not in byT or T + 2 not in byT:
            continue
        rT = byT[T]
        r2 = byT[T + 2]
        if rT["max_sat_R"] < 0 or r2["max_sat_R"] < 0:
            rows.append({"T": T, "note": "one side identically unsat at R=0"})
            continue
        mods = survivors(T, rT["max_sat_R"])
        mods2 = survivors(T + 2, r2["max_sat_R"])
        set2 = {tuple(m) for m in mods2}
        # pad/truncate to compare prefixes
        n_shift_in = 0
        n_S_in = 0
        n_drop_u0_u1_in = 0
        Su_onsets = Counter()
        for u in mods:
            # interpret u as starting at index 0; shifted model for T+2
            # would be [0,0]+u or u with two extra leading zeros? or drop?
            # Physical S: next window uses (u1,u2,...).
            Su = u[1:]
            # pad
            L2 = max(nvars((T + 2) + r2["max_sat_R"]), 1)
            Su_pad = (Su + [0] * L2)[:L2]
            if tuple(Su_pad) in set2 or any(
                tuple((Su + [0] * 8)[: len(m)]) == tuple(m)[: len(Su) + 0]
                for m in mods2
            ):
                n_S_in += 1
            uu = ([0, 0] + u)[:L2]
            if tuple(uu) in set2:
                n_shift_in += 1
            if len(u) >= 2:
                drop = (u[2:] + [0] * L2)[:L2]
                if tuple(drop) in set2:
                    n_drop_u0_u1_in += 1
            # onset of Su
            FS, _ = F_of_u(u[1:] + [0], T + rT["max_sat_R"] + 6)
            ones = [k for k in range(1, len(FS)) if FS[k] == 1]
            Su_onsets[ones[0] if ones else None] += 1
        rows.append(
            {
                "T": T,
                "n_T": len(mods),
                "n_T2": len(mods2),
                "leading00_in_T2": n_shift_in,
                "Su_in_T2": n_S_in,
                "drop2_in_T2": n_drop_u0_u1_in,
                "Su_first1": dict(Su_onsets),
                "forced_T": rT["forced_prefix"],
                "forced_T2": r2["forced_prefix"],
            }
        )
    return rows


def test_S_on_polynomials(kmax=16):
    """When is F_k = S^s F_t as polynomials in B?"""
    F, G = compute_columns(kmax, reduce=True)
    hits = []
    for t in range(0, kmax + 1):
        for s in (1, 2, 3, 4):
            for k in range(t + 1, kmax + 1):
                diff = reduce_no_consec(F[k] ^ shift_anf(F[t], s))
                if diff == 0 and F[k] != 0:
                    hits.append(
                        {
                            "s": s,
                            "t": t,
                            "k": k,
                            "kind": f"F_{k} = S^{s} F_{t}",
                            "poly": anf_str(F[k]),
                        }
                    )
    diffs = []
    for k in range(2, min(kmax, 12) + 1):
        d1 = reduce_no_consec(F[k] ^ shift_anf(F[k - 1], 1)) if k >= 1 else None
        d2 = reduce_no_consec(F[k] ^ shift_anf(F[k - 2], 2)) if k >= 2 else None
        d_skip = (
            reduce_no_consec(F[k] ^ shift_anf(F[k - 2], 1)) if k >= 2 else None
        )
        diffs.append(
            {
                "k": k,
                "F_k": anf_str(F[k]),
                "F_k + S F_{k-1}": anf_str(d1) if d1 is not None else None,
                "F_k + S^2 F_{k-2}": anf_str(d2) if d2 is not None else None,
                "F_k + S F_{k-2}": anf_str(d_skip) if d_skip is not None else None,
            }
        )
    return {"equalities": hits, "small_diffs": diffs}


# ---------------------------------------------------------------------------
# Linear algebra for low-degree multipliers
# ---------------------------------------------------------------------------


def fib_monomials(nvars_):
    """Bitmasks of square-free no-consecutive-1 monomials on n variables, plus 1."""
    out = []

    def rec(pos, last, acc):
        if pos == nvars_:
            out.append(acc)
            return
        rec(pos + 1, 0, acc)
        if last == 0:
            rec(pos + 1, 1, acc | (1 << pos))

    rec(0, 0, 0)
    return out


def eval_mask(mask, bits):
    return 1 if (mask & bits) == mask else 0


def gf2_rref(A, b):
    """Solve A x = b over GF(2). A is list of row lists, b list.
    Returns (ok, particular x or None, nullity).
    """
    n = len(A)
    if n == 0:
        return True, [], 0
    m = len(A[0])
    M = [A[i][:] + [b[i]] for i in range(n)]
    rank = 0
    pivots = [-1] * m
    row = 0
    for col in range(m):
        piv = None
        for r in range(row, n):
            if M[r][col]:
                piv = r
                break
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        for r in range(n):
            if r != row and M[r][col]:
                for c in range(col, m + 1):
                    M[r][c] ^= M[row][c]
        pivots[col] = row
        rank += 1
        row += 1
        if row == n:
            break
    for r in range(n):
        if all(M[r][c] == 0 for c in range(m)) and M[r][m]:
            return False, None, 0
    x = [0] * m
    for col, pr in enumerate(pivots):
        if pr != -1:
            x[col] = M[pr][m]
    nullity = m - rank
    return True, x, nullity


def try_multipliers(T, R, deg_vars=None, degree=1):
    """Seek A_j in span of monomials of given degree (or first deg_vars bits)
    such that F_T = sum_{j=1}^R A_j F_{T+j} on all Fibonacci strings
    of length nvars(T+R).
    """
    top = T + R
    L = max(nvars(top), 1)
    if deg_vars is None:
        deg_vars = min(L, 6 if degree >= 2 else L)
    mons = [m for m in fib_monomials(deg_vars) if bin(m).count("1") <= degree]
    strs = fib_strings(L)
    kmax = max(top, 2)
    Fs = [F_of_u(u, kmax)[0] for u in strs]
    # unknowns: A_j coeff of monomial m, j=1..R, indexed (j-1)*nmon + mi
    nmon = len(mons)
    ncols = R * nmon
    if ncols == 0:
        return {"ok": False, "reason": "no columns"}
    A = []
    b = []
    for u, F in zip(strs, Fs):
        bits = bits_from_list(u)
        row = [0] * ncols
        for j in range(1, R + 1):
            fj = F[T + j]
            if fj == 0:
                continue
            for mi, m in enumerate(mons):
                if eval_mask(m, bits):
                    row[(j - 1) * nmon + mi] ^= 1
        A.append(row)
        b.append(F[T])
    ok, x, nul = gf2_rref(A, b)
    used = []
    if ok and x is not None:
        for j in range(1, R + 1):
            terms = []
            for mi, m in enumerate(mons):
                if x[(j - 1) * nmon + mi]:
                    terms.append(anf_str(1 << m) if m else "1")
            if terms:
                used.append({"j": j, "A": " + ".join(terms)})
    return {
        "T": T,
        "R": R,
        "degree": degree,
        "deg_vars": deg_vars,
        "n_mons": nmon,
        "n_eq": len(A),
        "ok": ok,
        "nullity": nul if ok else None,
        "A_support": used[:40],
        "n_A_nonzero_j": len(used),
    }


def tautological_multipliers_check(T, R):
    """Boolean Nullstellensatz particular solution, checked by evaluation:

        P := prod_{j=1}^R (1 + F_{T+j})
        F_T * P = 0     (unsat)
        P = 1 + sum_j C_j F_{T+j}
        F_T = F_T (P + 1) = sum_j (F_T C_j) F_{T+j}

    The identity holds on the whole Boolean cube of Fibonacci strings of
    length nvars(T+R) iff the variety is empty. We check F_T * P == 0.
    """
    top = T + R
    L = max(nvars(top), 1)
    kmax = top
    n_bad = 0
    n_all = 0
    for u in fib_strings(L):
        n_all += 1
        F, _ = F_of_u(u, kmax)
        P = 1
        for j in range(1, R + 1):
            P &= 1 ^ F[T + j]
        if (F[T] & P) != 0:
            n_bad += 1
    return {"T": T, "R": R, "n": n_all, "n_fail": n_bad, "ok": n_bad == 0}


# ---------------------------------------------------------------------------
# Residual automata after a legal u-prefix (right-fold state)
# ---------------------------------------------------------------------------


def fold_one(F, G, un, kmax):
    Fn = [0] * (kmax + 1)
    Gn = [0] * (kmax + 1)
    Fn[0] = 0
    Gn[0] = 1
    if kmax >= 1:
        Fn[1] = 1 ^ un
        Gn[1] = 1
    for k in range(2, kmax + 1):
        Fn[k] = Gn[k - 1] ^ (Fn[k - 1] | Fn[k - 2])
        Gn[k] = F[k - 1] ^ (Gn[k - 1] | Gn[k - 2])
    return Fn, Gn


def residual_window_stats(T, R, prefix_lens=None):
    """Fold from the right (true causality). After reading a Fibonacci
    suffix of length p, look at the window W = (F_T, ..., F_{T+R}).

    If the set of reachable windows after p bits grows like Fib(p) without
    collapsing, residual memory is unbounded in the prefix.
    """
    kmax = T + R
    if prefix_lens is None:
        prefix_lens = list(range(0, min(nvars(kmax), 12) + 1))
    rows = []
    for p in prefix_lens:
        windows = set()
        last1s = Counter()
        for u in fib_strings(p) if p else [[]]:
            F, G = F_of_u(u, kmax)  # suffix then vacuum: correct fold-from-right
            W = tuple(F[T : T + R + 1])
            windows.add(W)
            ones = [T + i for i, b in enumerate(W) if b]
            last1s[ones[-1] if ones else None] += 1
        rows.append(
            {
                "p": p,
                "n_fib": len(fib_strings(p)) if p else 1,
                "n_windows": len(windows),
                "last1_hist": {str(k): v for k, v in last1s.items()},
            }
        )
    return rows


def rank_candidate(T, Rmax=12):
    """Is there a well-founded rank on residual windows that every legal
    0/1 fold strictly decreases while preserving a 'still-open L_0' bit?

    We try rank = last index of a 1 in F_T..F_{T+R}, and also Hamming
    weight of that window. Report whether a 1-fold can increase it.
    """
    kmax = T + Rmax
    inc_last = 0
    inc_wt = 0
    n = 0
    examples = []
    # start from all short suffixes
    for p in range(0, min(8, nvars(kmax)) + 1):
        for u in fib_strings(p) if p else [[]]:
            F, G = F_of_u(u, kmax)
            last = max((k for k in range(T, kmax + 1) if F[k]), default=T - 1)
            wt = sum(F[T : kmax + 1])
            for b in (0, 1):
                if u and u[0] == 1 and b == 1:
                    continue  # would put consecutive 1s at the fold-left
                # folding a NEW leftmost bit: F_of_u([b]+u)
                Fn, Gn = F_of_u([b] + u, kmax)
                lastn = max((k for k in range(T, kmax + 1) if Fn[k]), default=T - 1)
                wtn = sum(Fn[T : kmax + 1])
                n += 1
                if lastn > last:
                    inc_last += 1
                    if len(examples) < 6:
                        examples.append(
                            {
                                "u": u,
                                "b": b,
                                "last": last,
                                "lastn": lastn,
                                "wt": wt,
                                "wtn": wtn,
                            }
                        )
                if wtn > wt:
                    inc_wt += 1
    return {
        "T": T,
        "Rmax": Rmax,
        "n_folds": n,
        "n_increase_last1": inc_last,
        "n_increase_weight": inc_wt,
        "examples": examples,
    }


# ---------------------------------------------------------------------------
# Explicit small-T identities (hand-checkable ANF)
# ---------------------------------------------------------------------------


def explicit_small_identities():
    """Machine-check polynomial identities used as base cases.

    F_4 = 0 in B.
    F_2 = u0, F_3 = 1+u1, so F_2 F_3 = u0(1+u1) and F_2=1, F_3=0 forces u0=1,u1=1
    which is illegal; equivalently F_2 (1+F_3) = 0 after reduction? Check.
    F_8 = u1 u3.
    """
    F, G = compute_columns(20, reduce=True)
    checks = {}
    checks["F4_zero"] = F[4] == 0
    checks["F2"] = anf_str(F[2])
    checks["F3"] = anf_str(F[3])
    checks["F8"] = anf_str(F[8])
    checks["F6"] = anf_str(F[6])
    checks["F12"] = anf_str(F[12]) if 12 < len(F) else None
    checks["F16"] = anf_str(F[16]) if 16 < len(F) else None
    # T=2: F_2 (1+F_3) should be 0 in B? F_2=u0, F_3=1+u1, product u0(1+u1)=u0+u0 u1
    # reduced: u0 u1 = 0 so product = u0 = F_2, not 0. Need F_2 and F_3 together:
    # F_2=1, F_3=0 => u0=1, u1=1 illegal. The ideal membership is
    # F_2 = A F_3  ?  u0 = A (1+u1). No A in B: evaluate at u0=1,u1=0: lhs=1, rhs=0.
    # So R=1 fails for T=2. With R=1 killed by F_3? onset says maxR=0, killed by F_3.
    # Identity: F_2 = F_3 * 0 + F_2, need F_3. F_2 * (1+F_3) * (something).
    # Variety F_2=1, F_3=0 empty, so F_2 (1+F_3)=0 in B?
    prod = reduce_no_consec(band(F[2], ONE ^ F[3]))
    checks["T2_F2_times_1plusF3"] = anf_str(prod)
    checks["T2_empty_R1"] = prod == 0
    # T=4: F_4=0, so F_4 is in every ideal; R=-1 / killed by itself.
    # T=8: F_8 = u1 u3. Check tautological at killing R.
    return checks, F, G


def try_F8_compact():
    """T=8 killed by F_18 with maxR=9. Look for a compact identity with smaller
    generator list, e.g. F_8 in <F_15, F_17, F_18> or similar sparse support.
    """
    results = []
    # first: which single F_{8+j} already kills F_8=1? none if maxR=9
    F, G = compute_columns(20, reduce=True)
    # F_8 = u1 u3. On {u1=u3=1} (hence u0=u2=u4=0), F_k become functions of u5+
    L = nvars(18)
    models_F8 = []
    for u in fib_strings(L):
        Fu, _ = F_of_u(u, 18)
        if Fu[8] == 1:
            models_F8.append((u, Fu))
    # among F_8=1, when is the first later 1?
    first_later = Counter()
    for u, Fu in models_F8:
        later = [k for k in range(9, 19) if Fu[k] == 1]
        first_later[later[0] if later else None] += 1
    results.append({"first_1_after_F8": dict(first_later), "n_F8": len(models_F8)})
    # restrict to u1=u3=1
    forced = []
    for u, Fu in models_F8:
        forced.append((tuple(u[:8]), tuple(k for k in range(9, 19) if Fu[k])))
    results.append(
        {
            "prefix8_to_later_ones": [
                {"pre": p, "later": later} for p, later in forced[:20]
            ]
        }
    )
    # linear algebra degree 0 (constants): F_8 = sum a_j F_{8+j}
    results.append(try_multipliers(8, 10, deg_vars=0, degree=0))
    results.append(try_multipliers(8, 10, deg_vars=8, degree=1))
    results.append(try_multipliers(8, 10, deg_vars=6, degree=2))
    return results


def try_T20_structure():
    rmax = 16
    mods = survivors(20, rmax)
    fb = forced_bits(mods)
    supports = [tuple(i for i, b in enumerate(u) if b) for u in mods]
    # first later 1 at R=17 (the killer)
    kill_pos = Counter()
    extras = []
    L = nvars(37)
    for u in fib_strings(L):
        F, _ = F_of_u(u, 37)
        if F[20] != 1:
            continue
        if any(F[20 + d] for d in range(1, 17)):
            continue
        # last-sat on first 18 bits; bit 19 = u_{18} determines F_37
        kill_pos[F[37]] += 1
        extras.append({"u": u, "F37": F[37], "ones": [i for i, b in enumerate(u) if b]})
    return {
        "n_last_sat": len(mods),
        "forced": fmt_forced(fb),
        "supports": supports,
        "kill_F37_on_extended": dict(kill_pos),
        "extended": extras[:8],
    }


# ---------------------------------------------------------------------------
# Descent: L_0(T) for u  =?=>  L_0(T') for Su
# ---------------------------------------------------------------------------


def descent_scan(Tmax=20, R=10):
    """For last-sat models of each T, where is the first 1 of F(Su)?
    If it were always at some T'<T, we would have a rank.
    """
    rows = []
    table = onset_table(Tmax, Rmax=20)
    for rec in table:
        T = rec["T"]
        maxR = rec["max_sat_R"]
        if maxR < 0:
            rows.append({"T": T, "note": "identically zero"})
            continue
        mods = survivors(T, maxR)
        c_first = Counter()
        c_last = Counter()
        still_L0 = 0
        for u in mods:
            FS, _ = F_of_u(u[1:] + [0] * 4, T + maxR + 8)
            ones = [k for k in range(len(FS)) if FS[k] == 1]
            first = ones[0] if ones else None
            last = ones[-1] if ones else None
            c_first[first] += 1
            c_last[last] += 1
            # Su has a 1 at T' <= T and zeros after T+maxR-2? rough L0
            if first is not None and first <= T:
                tail = FS[first + 1 : T + maxR]
                if tail and all(b == 0 for b in tail):
                    still_L0 += 1
        rows.append(
            {
                "T": T,
                "maxR": maxR,
                "n": len(mods),
                "Su_first1": dict(c_first),
                "Su_last1": {str(k): v for k, v in list(c_last.items())[:8]},
                "n_Su_L0_smaller": still_L0,
            }
        )
    return rows, table


# ---------------------------------------------------------------------------
# Compact ANF certificates F_T = sum_j A_j F_{T+j} in B
# ---------------------------------------------------------------------------


def U_anf(i: int) -> int:
    return 1 << (1 << i)


def parse_A(s: str) -> int:
    """Parse '1 + u4 + u1*u3' into a reduced ANF integer."""
    p = 0
    for term in s.replace(" ", "").split("+"):
        if not term:
            continue
        if term == "1":
            p ^= 1
            continue
        fac = 1
        for f in term.split("*"):
            if not f.startswith("u"):
                raise ValueError(s)
            fac = band(fac, U_anf(int(f[1:])))
        p ^= fac
    return reduce_no_consec(p)


# Linear (or quadratic for T=12) identities, machine-checked in certify().
# A maps j -> polynomial so F_T = sum_j A[j] F_{T+j}.
ANF_CERTS = [
    {"T": 1, "A": {1: "1", 2: "u2 + u3", 6: "1", 7: "1"}},
    {"T": 2, "A": {1: "u0"}},
    {"T": 3, "A": {2: "1", 3: "1"}},
    {"T": 5, "A": {1: "u4", 2: "u4 + u1", 4: "1"}},
    {"T": 6, "A": {1: "u4", 4: "1"}},
    {"T": 7, "A": {2: "1 + u3", 3: "u4"}},
    {
        "T": 8,
        "A": {
            1: "u6 + u4",
            2: "u6 + u4",
            3: "u6",
            4: "u7 + u6",
            5: "u7",
            6: "u7",
            7: "1 + u4",
            8: "u8",
            9: "1 + u6 + u5 + u4",
            10: "1 + u6",
        },
    },
    {
        "T": 9,
        "A": {
            1: "1 + u4",
            2: "u6 + u5",
            3: "u7",
            4: "u7",
            6: "1 + u7 + u4",
            7: "1",
        },
    },
    {
        "T": 10,
        "A": {1: "1 + u6 + u2", 2: "u7", 3: "1 + u6", 4: "u7", 6: "u4"},
    },
    {"T": 11, "A": {1: "u6 + u3", 2: "1 + u4", 3: "1"}},
    {"T": 12, "A": {1: "u5 + u3 + u1*u3", 2: "u3"}},
]


def check_anf_cert(cert, F=None):
    T = cert["T"]
    need = T + max(cert["A"])
    if F is None:
        F, _ = compute_columns(need, reduce=True)
    rhs = 0
    for j, s in cert["A"].items():
        rhs ^= band(parse_A(s), F[T + j])
    rhs = reduce_no_consec(rhs)
    return F[T] == rhs, anf_str(reduce_no_consec(F[T] ^ rhs))


def certify_t20_explicit():
    """The T=20 last-sat variety is six length-18 Fibonacci words, all
    sharing the tail 00010010010001 from index 4. Each has F_37=1, and
    the only legal 19th bit is 0 (u17=1). So F_20 * prod_{j=1}^{16}(1+F_{20+j})
    vanishes, and F_37=1 on that support.
    """
    mods = survivors(20, 16)
    assert len(mods) == 6
    tail = [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
    for u in mods:
        assert u[4:18] == tail, u
        F, _ = F_of_u(u, 37)
        assert F[20] == 1
        assert all(F[20 + d] == 0 for d in range(1, 17))
        ext = u + [0]
        Fe, _ = F_of_u(ext, 37)
        assert Fe[37] == 1
        # u17=1 forbids u18=1
        assert u[17] == 1
    # tautological identity at the killing R
    tau = tautological_multipliers_check(20, 17)
    assert tau["ok"]
    return {"n": 6, "tail_from_4": "00010010010001", "F37_forced": 1, "tautological": tau}


# ---------------------------------------------------------------------------
# Certify
# ---------------------------------------------------------------------------


def certify(Tmax=16):
    checks, F, G = explicit_small_identities()
    assert checks["F4_zero"]
    assert checks["F8"] == "u1*u3"
    Fbig, _ = compute_columns(22, reduce=True)
    anf_ok = []
    for cert in ANF_CERTS:
        ok, diff = check_anf_cert(cert, Fbig)
        assert ok, (cert["T"], diff)
        anf_ok.append({"T": cert["T"], "R": max(cert["A"]), "ok": True})
    # T=2,1,8 tautological (Boolean Nullstellensatz particular solution)
    t2 = tautological_multipliers_check(2, 1)
    assert t2["ok"]
    t1 = tautological_multipliers_check(1, 7)
    assert t1["ok"]
    t8 = tautological_multipliers_check(8, 10)
    assert t8["ok"]
    # value identity F_{T+3}=1+F_{T+1}(Su) on {F_T=1, F_{T+1}=F_{T+2}=0}
    id3 = []
    for T in range(1, 13):
        if T == 4:
            continue
        rec = derived_identity_T3_poly(T)
        assert rec["n_fail"] == 0, rec
        id3.append(rec)
    sh = test_S_on_polynomials(16)
    assert any(h["s"] == 1 and h["t"] == 1 and h["k"] == 3 for h in sh["equalities"])
    assert any(h["s"] == 2 and h["t"] == 2 and h["k"] == 6 for h in sh["equalities"])
    assert any(h["s"] == 1 and h["t"] == 5 and h["k"] == 7 for h in sh["equalities"])
    # linear multipliers fail at T=16 and T=20 (no T-uniform linear template)
    m16 = try_multipliers(16, 10, degree=1)
    m20 = try_multipliers(20, 17, degree=1)
    assert m16["ok"] is False
    assert m20["ok"] is False
    t20 = certify_t20_explicit()
    table = onset_table(Tmax, Rmax=20)
    return {
        "small_identities": checks,
        "anf_certs": anf_ok,
        "tautological_T1_T2_T8": [t1, t2, t8],
        "zero_run_id_T3": id3,
        "shift_poly_equalities": sh["equalities"],
        "linear_fails_T16_T20": True,
        "T20_explicit": t20,
        "onset": table,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--tmax", type=int, default=16)
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--json-out", type=str, default="")
    args = parser.parse_args()

    report = {}
    if args.certify:
        report["certify"] = certify(args.tmax)
        print("certify: assertions passed")
        print("ANF certificates T=1,2,3,5,6,7,8,9,10,11,12")
        print("F_4=0, F_8=u1 u3; linear multipliers fail at T=16 and T=20")
        print("value identity F_{T+3}=1+F_{T+1}(Su) on {F_T=1, F_{T+1}=F_{T+2}=0}")
        print("T=20: 6 last-sat words, tail 00010010010001, F_37=1")
        for row in report["certify"]["onset"]:
            print(
                f"  T={row['T']:2d} maxR={row['max_sat_R']:2d} n={row['n_at_max']:3d} "
                f"killed_by_F[{row['killed_by']}] forced={row['forced_prefix']}"
            )

    if args.scan:
        print("=== onset table with forced bits ===")
        table = onset_table(args.tmax, Rmax=24)
        report["onset"] = table
        for row in table:
            print(
                f"  T={row['T']:2d} maxR={row['max_sat_R']:2d} n={row['n_at_max']:3d} "
                f"kill F_{row['killed_by']} nv={row['nvars_kill']} "
                f"forced={row['forced_prefix']} supp={row['supports'][:4]}"
            )
        print("=== T=8 compact multipliers ===")
        t8 = try_F8_compact()
        report["T8"] = t8
        print(json.dumps(t8, indent=2, default=str)[:4000])
        print("=== T=20 structure ===")
        t20 = try_T20_structure()
        report["T20"] = t20
        print(json.dumps(t20, indent=2, default=str)[:4000])
        print("=== shift closure ===")
        sc = test_shift_closure(table)
        report["shift_closure"] = sc
        print(json.dumps(sc, indent=2, default=str)[:4000])
        print("=== descent Su first-1 ===")
        desc, _ = descent_scan(min(args.tmax, 20), R=10)
        report["descent"] = desc
        print(json.dumps(desc, indent=2, default=str)[:5000])
        print("=== degree-0/1 multipliers for selected T ===")
        muls = []
        for T, R in [(2, 1), (3, 3), (5, 4), (8, 10), (16, 8), (20, 17)]:
            if T > args.tmax and T not in (8, 20):
                continue
            for deg in (0, 1):
                rec = try_multipliers(T, R, degree=deg)
                muls.append(rec)
                print(
                    f"  T={T} R={R} deg={deg} ok={rec['ok']} "
                    f"nA={rec.get('n_A_nonzero_j')} nul={rec.get('nullity')}"
                )
                if rec["ok"] and rec["A_support"]:
                    print("    ", rec["A_support"][:8])
        report["multipliers"] = muls
        print("=== residual windows T=8,20 ===")
        report["residual_T8"] = residual_window_stats(8, 10)
        report["residual_T20"] = residual_window_stats(20, 16, prefix_lens=list(range(0, 13)))
        print("T8", report["residual_T8"])
        print("T20", report["residual_T20"])
        print("=== rank candidates ===")
        report["rank_T8"] = rank_candidate(8, 12)
        report["rank_T20"] = rank_candidate(20, 16)
        print(report["rank_T8"])
        print(report["rank_T20"])
        print("=== S on polynomials ===")
        report["shift_poly"] = test_S_on_polynomials(18)
        print(report["shift_poly"])

    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(report, f, indent=2, default=str)
            f.write("\n")


if __name__ == "__main__":
    main()
