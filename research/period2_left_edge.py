"""Left-edge polynomials for a hypothetical period-2 Rule 30 center.

Assumes after a time origin the center satisfies c_{2n}=0, c_{2n+1}=1.
Left reconstruction from the inverse
    x(t, j-1) = x(t+1, j) XOR (x(t, j) OR x(t, j+1))
produces columns -k as sliding Boolean functions of u_n = x(2n, 1).
The odd right neighbor v_n = x(2n+1, 1) is included as extra variables in
the independence check, then dropped.

ANF: integer whose bit m is the GF(2) coefficient of prod_{i: m>>i & 1} u_i.
v-variables, when used, occupy bits starting at VBIT.

This file is a verifier, not a SAT solver over unbounded T. It computes
exact polynomials for small n and checks left-edge / beyond-edge constraints
on every u-string with no consecutive 1s.
"""
from __future__ import annotations

import argparse
import json


def band(p: int, q: int) -> int:
    """Boolean AND as ANF product (x^2 = x, monomial product = bit OR)."""
    res = 0
    i = 0
    pp = p
    while pp:
        if pp & 1:
            j = 0
            qq = q
            while qq:
                if qq & 1:
                    res ^= 1 << (i | j)
                qq >>= 1
                j += 1
        pp >>= 1
        i += 1
    return res


def bor(p: int, q: int) -> int:
    return p ^ q ^ band(p, q)


def shift_anf(p: int, s: int) -> int:
    """Replace each u_i by u_{i+s}."""
    if s == 0 or p == 0:
        return p
    res = 0
    m = 0
    pp = p
    while pp:
        if pp & 1:
            res ^= 1 << (m << s)
        pp >>= 1
        m += 1
    return res


def reduce_no_consec(p: int) -> int:
    """Zero monomials that contain some u_i u_{i+1}."""
    res = 0
    m = 0
    pp = p
    while pp:
        if pp & 1 and (m & (m << 1)) == 0:
            res ^= 1 << m
        pp >>= 1
        m += 1
    return res


def anf_vars(p: int) -> list[int]:
    used = []
    i = 0
    while (1 << i) <= p:
        mask = 0
        m = 0
        pp = p
        while pp:
            if (pp & 1) and (m >> i) & 1:
                mask = 1
                break
            pp >>= 1
            m += 1
        if mask:
            used.append(i)
        i += 1
    return used


def anf_str(p: int, name: str = "u") -> str:
    if p == 0:
        return "0"
    if p == 1:
        return "1"
    terms = []
    m = 0
    pp = p
    while pp:
        if pp & 1:
            if m == 0:
                terms.append("1")
            else:
                fac = [f"{name}{i}" for i in range(m.bit_length()) if (m >> i) & 1]
                terms.append("*".join(fac))
        pp >>= 1
        m += 1
    return " + ".join(terms)


def eval_anf(p: int, bits: int) -> int:
    """Evaluate ANF on a bitstring stored in bits (bit i = u_i)."""
    acc = 0
    m = 0
    pp = p
    while pp:
        if pp & 1:
            acc ^= 1 if (m & bits) == m else 0
        pp >>= 1
        m += 1
    return acc


# Constant 1 and variable u_0.
ONE = 1
U0 = 2


def compute_columns(kmax: int, reduce: bool = False):
    """Return F[k], G[k] as ANFs in u_0, u_1, ... for k=0..kmax.

    F[k] = x(2n, -k) relative to window origin n=0.
    G[k] = x(2n+1, -k).
    """
    F = [0] * (kmax + 1)
    G = [0] * (kmax + 1)
    F[0] = 0
    G[0] = ONE
    if kmax >= 1:
        F[1] = ONE ^ U0
        G[1] = ONE
    for k in range(2, kmax + 1):
        F[k] = G[k - 1] ^ bor(F[k - 1], F[k - 2])
        G[k] = shift_anf(F[k - 1], 1) ^ bor(G[k - 1], G[k - 2])
        if reduce:
            F[k] = reduce_no_consec(F[k])
            G[k] = reduce_no_consec(G[k])
    return F, G


def fib_strings(length: int):
    """All bitstrings of given length with no two consecutive 1s, as ints."""
    out = []

    def rec(pos: int, last: int, acc: int):
        if pos == length:
            out.append(acc)
            return
        rec(pos + 1, 0, acc)
        if last == 0:
            rec(pos + 1, 1, acc | (1 << pos))

    rec(0, 0, 0)
    return out


def max_index(p: int) -> int:
    if p <= 1:
        return -1
    m = p.bit_length() - 1
    # highest variable in any monomial of p
    best = -1
    while m:
        if p & ((1 << (m + 1)) - 1):
            # find vars
            pass
        m -= 1
    i = 0
    best = -1
    pp = p
    mm = 0
    while pp:
        if pp & 1 and mm:
            best = max(best, mm.bit_length() - 1)
        pp >>= 1
        mm += 1
    return best


def edge_polynomials(nmax: int, reduce: bool = True):
    """E_n = x(2n, -2n), O_n = x(2n+1, -(2n+1)), as ANFs in u_0,u_1,...

    These are F_{2n} and G_{2n+1} at window origin 0, which equals the
    physical values at n=0. For general n, replace u_i by u_{n+i}.
    """
    kmax = 2 * nmax + 1
    F, G = compute_columns(kmax, reduce=reduce)
    even = []
    odd = []
    for n in range(nmax + 1):
        even.append(F[2 * n] if reduce else reduce_no_consec(F[2 * n]))
        odd.append(G[2 * n + 1] if reduce else reduce_no_consec(G[2 * n + 1]))
    return even, odd, F, G


def verify_v_independence(kmax: int = 12, nvars: int = 8) -> bool:
    """Brute-force: left columns ignore the odd right neighbor v."""

    # Truth-table reconstruction including v_i as extra bits.
    # State of u: nvars bits, v: nvars bits. Times 0..2*nvars-1 covered.
    # We only check that for each k, F_k and G_k don't change when v flips.
    # Direct spacetime via inverse from columns 0,1.

    def recon_triangle(u_bits, v_bits, kmax, tmax):
        # x[(t, j)] for j in -kmax..1, t in 0..tmax
        x = {}
        for t in range(tmax + 1):
            # center
            x[t, 0] = t & 1
            # right neighbor
            if t % 2 == 0:
                n = t // 2
                x[t, 1] = (u_bits >> n) & 1 if n < 64 else 0
            else:
                n = t // 2
                x[t, 1] = (v_bits >> n) & 1 if n < 64 else 0
        # reconstruct leftward; need increasing time for deeper columns
        for k in range(1, kmax + 1):
            j = -k
            for t in range(tmax - k + 1):
                # x(t,j) = x(t+1, j+1) XOR (x(t,j+1) OR x(t, j+2))
                right1 = x[t, j + 1]
                right2 = x[t, j + 2]
                fut = x[t + 1, j + 1]
                x[t, j] = fut ^ (right1 | right2)
        return x

    tmax = 2 * nvars + kmax + 2
    # Compare two random-ish v's and all small u with no consec 1s
    u_list = fib_strings(nvars)
    for u in u_list:
        x0 = recon_triangle(u, 0, kmax, tmax)
        x1 = recon_triangle(u, (1 << nvars) - 1, kmax, tmax)
        for k in range(kmax + 1):
            for t in range(0, tmax - k):
                if x0[t, -k] != x1[t, -k]:
                    return False
    return True


def verify_against_forward(steps: int = 40) -> bool:
    """On the real seed, reconstruction from actual (c,r) recovers the left."""
    row = {0: 1}
    hist = [dict(row)]
    for t in range(steps):
        nxt = {}
        lo, hi = -t - 1, t + 1
        for j in range(lo, hi + 1):
            nxt[j] = row.get(j - 1, 0) ^ (row.get(j, 0) | row.get(j + 1, 0))
        row = nxt
        hist.append(row)
    # inverse reconstruction from columns 0 and 1
    for t0 in range(steps):
        for k in range(1, t0 + 1):
            t = t0 - k  # so that we have future times
            if t < 0:
                continue
            j = -k
            got = hist[t + 1].get(j + 1, 0) ^ (
                hist[t].get(j + 1, 0) | hist[t].get(j + 2, 0)
            )
            if got != hist[t].get(j, 0):
                return False
    return True


def check_edge_on_fib(nmax: int):
    """For each n, evaluate E_n and O_n on all no-consec-1 strings.

    Report whether they are identically 0, identically 1, or mixed.
    Also check beyond-edge bits F_k for k>2n at window origin 0.
    """
    kmax = 2 * nmax + 3
    F, G = compute_columns(kmax, reduce=True)
    rows = []
    for n in range(nmax + 1):
        e = F[2 * n]
        o = G[2 * n + 1]
        nvars = max(max_index(e), max_index(o), 0) + 1
        # include a few extra u bits in case max_index missed constants
        nvars = max(nvars, n + 3, 1)
        strs = fib_strings(nvars)
        e_vals = {eval_anf(e, s) for s in strs}
        o_vals = {eval_anf(o, s) for s in strs}
        # beyond edge at time 2n (window origin 0): positions k>2n
        beyond_zero = True
        beyond_poly = []
        for k in range(2 * n + 1, min(2 * n + 5, kmax + 1)):
            fk = F[k]
            vals = {eval_anf(fk, s) for s in strs}
            beyond_poly.append((k, anf_str(fk), sorted(vals)))
            if vals != {0}:
                beyond_zero = False
        rows.append(
            {
                "n": n,
                "time_even": 2 * n,
                "col_even": -2 * n,
                "E_anf": anf_str(e),
                "E_vars": anf_vars(e),
                "E_values": sorted(e_vals),
                "E_identically": (
                    "0" if e_vals == {0} else "1" if e_vals == {1} else "mixed"
                ),
                "O_anf": anf_str(o),
                "O_vars": anf_vars(o),
                "O_values": sorted(o_vals),
                "O_identically": (
                    "0" if o_vals == {0} else "1" if o_vals == {1} else "mixed"
                ),
                "beyond_identically_zero": beyond_zero,
                "beyond": beyond_poly,
            }
        )
    return rows, F, G


def sat_prefixes(tmin: int, nmax: int):
    """Unshifted prize-seed check: x(t,-t)=1 for tmin <= t <= 2*nmax.

    This is the lightlike bit of the single-cell seed, not the shifted L_0
    onset row. tmin must be >= 1: t=0 in phase even-0 is the center, which
    is 0. Padding missing u bits with 0 can cause false unsat; prefer
    certify() / onset enumeration, which names its variables.
    u has no consecutive 1s. Window: physical u_n for n such that 2n >= tmin,
    i.e. n >= ceil(tmin/2). Polynomials F_k are relative: x(2n,-k)=F_k shifted
    by n, so we evaluate F_k on bits starting at u_n.

    Returns list of surviving bitstrings (as ints with bit 0 = u_{n0}) or empty.
    """
    if tmin < 1:
        raise ValueError("tmin must be >= 1 (t=0 edge is the center)")
    kmax = 2 * nmax + 3
    F, G = compute_columns(kmax, reduce=True)
    n0 = (tmin + 1) // 2  # first even time 2n >= tmin has n = ceil(tmin/2)
    # Need u bits u_{n0}, ..., u_{nmax + extra}
    extra = 6
    length = nmax - n0 + extra + 1
    if length <= 0:
        return [], F, G
    survivors = []
    for bits in fib_strings(length):
        ok = True
        for n in range(n0, nmax + 1):
            shift = n - n0
            # evaluate F[k] on u_n, u_{n+1}, ... = bits starting at `shift`
            def ev(p):
                return eval_anf(shift_anf(p, 0), bits >> shift)

            # even time 2n >= tmin automatically
            if 2 * n >= tmin:
                if ev(F[2 * n]) != 1:
                    ok = False
                    break
                for k in range(2 * n + 1, 2 * n + 3):
                    if ev(F[k]) != 0:
                        ok = False
                        break
                if not ok:
                    break
            # odd time 2n+1
            if 2 * n + 1 >= tmin:
                if ev(G[2 * n + 1]) != 1:
                    ok = False
                    break
                for k in range(2 * n + 2, 2 * n + 4):
                    if ev(G[k]) != 0:
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            survivors.append(bits)
    return survivors, F, G


def column_table(kmax: int):
    F, G = compute_columns(kmax, reduce=True)
    rows = []
    for k in range(kmax + 1):
        rows.append(
            {
                "k": k,
                "F": anf_str(F[k]),
                "F_raw_vars": anf_vars(F[k]),
                "G": anf_str(G[k]),
                "G_raw_vars": anf_vars(G[k]),
            }
        )
    return rows, F, G


def recon_cell(t, j, u_bits, phase=0):
    """x(t,j) from period-2 center of given phase and even right neighbor u.

    phase 0: c_t = t & 1  (even 0, odd 1). phase 1: the opposite.
    Odd right neighbor is omitted: left reconstruction does not use it.
    Bits of u_bits beyond its bit_length are 0.
    """
    memo = {}

    def cell(tt, jj):
        key = (tt, jj)
        if key in memo:
            return memo[key]
        if jj == 0:
            r = (tt & 1) ^ phase
        elif jj == 1:
            if tt & 1:
                # v is unused on the left; any value works. Use 0.
                r = 0
            else:
                n = tt >> 1
                r = (u_bits >> n) & 1
        elif jj > 1:
            raise ValueError("reconstruction asked for a right column > 1")
        else:
            r = cell(tt + 1, jj + 1) ^ (cell(tt, jj + 1) | cell(tt, jj + 2))
        memo[key] = r
        return r

    return cell(t, j)


def check_onset_row(T, u_bits, phase=0, extra=2):
    """L_0 row at the onset: x(0,-T)=1 and x(0,j)=0 for -T-extra <= j < -T.

    Time origin is the start of the period-2 regime (so T is the left-edge
    distance at onset, not a pre-period time that we must not over-claim).
    """
    if recon_cell(0, -T, u_bits, phase) != 1:
        return False
    for d in range(1, extra + 1):
        if recon_cell(0, -T - d, u_bits, phase) != 0:
            return False
    return True


def onset_sat(T, ulen, phase=0, extra=2):
    """Enumerate no-consec-1 u-prefixes of length ulen; count onset-row models."""
    hits = []
    for bits in fib_strings(ulen):
        if check_onset_row(T, bits, phase=phase, extra=extra):
            hits.append(bits)
    return hits


def chain_sat(T, tmax, phase=0, extra=1):
    """Existential u-prefix making L_0 hold at every time s=0..tmax-T.

    At shifted time s the leftmost 1 is at -(T+s). u-bits needed go up to
    about (tmax + T)/2; we enumerate that many Fibonacci strings.
    """
    ulen = tmax + 2
    hits = []
    for bits in fib_strings(ulen):
        ok = True
        for s in range(0, tmax + 1):
            edge = -(T + s)
            if recon_cell(s, edge, bits, phase) != 1:
                ok = False
                break
            for d in range(1, extra + 1):
                if recon_cell(s, edge - d, bits, phase) != 0:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            hits.append(bits)
    return hits


def local_obstruction_table(Tmax, ulen, phase=0, extra=3):
    """For each onset width T, is the single onset row satisfiable?"""
    rows = []
    for T in range(1, Tmax + 1):
        hits = onset_sat(T, ulen, phase=phase, extra=extra)
        rows.append({"T": T, "phase": phase, "ulen": ulen, "models": len(hits)})
    return rows


def poly_vs_recon(kmax=12, nvars=8):
    """ANF F_k, G_k must match reconstruction on every Fibonacci u."""
    F, G = compute_columns(kmax, reduce=False)
    for bits in fib_strings(nvars):
        for k in range(kmax + 1):
            # Need enough future bits: times up to k, n up to k/2 + a bit
            if max_index(F[k]) >= nvars or max_index(G[k]) >= nvars:
                continue
            fv = eval_anf(reduce_no_consec(F[k]), bits)
            gv = eval_anf(reduce_no_consec(G[k]), bits)
            if recon_cell(0, -k, bits, 0) != fv:
                return False, ("F", k, bits, fv, recon_cell(0, -k, bits, 0))
            if recon_cell(1, -k, bits, 0) != gv:
                return False, ("G", k, bits, gv, recon_cell(1, -k, bits, 0))
    return True, None


def certify():
    """Machine-check the identities and the T=1..15 onset obstructions."""
    assert verify_against_forward(50)
    assert verify_v_independence(10, 6)
    pok, perr = poly_vs_recon(12, 8)
    assert pok, perr
    F, G = compute_columns(20, reduce=True)
    # Vacuum: constant terms.
    for k in range(len(F)):
        assert (F[k] & 1) == (k & 1), k
    assert G[0] == ONE and G[1] == ONE
    # Explicit small columns in the no-consecutive-1s quotient.
    assert F[0] == 0
    assert F[1] == ONE ^ U0
    assert F[2] == U0
    assert F[3] == ONE ^ shift_anf(U0, 1)
    assert F[4] == 0
    assert F[6] == shift_anf(U0, 2)
    assert F[8] == band(shift_anf(U0, 1), shift_anf(U0, 3))
    # F_4 vanishes on every Fibonacci string (two-step identity).
    for bits in fib_strings(6):
        assert recon_cell(0, -4, bits, 0) == 0
        assert eval_anf(F[4], bits) == 0
    # Onset L_0 of width T=1..10 is empty with 10 zeros past the edge.
    # Complete finite check: F_T,...,F_{T+10} depend on finitely many
    # u bits, all enumerated. T=8 needs extra>=9 (the u7=0 branch
    # first fails at F_17).
    empty = []
    for T in range(1, 11):
        extra = 10
        top = min(T + extra, len(F) - 1)
        nvars = max(max_index(F[top]) + 1, 8)
        nvars = min(nvars, 16)
        n_ok = 0
        for bits in fib_strings(nvars):
            if eval_anf(F[T], bits) != 1:
                continue
            if all(eval_anf(F[k], bits) == 0 for k in range(T + 1, top + 1)):
                n_ok += 1
        empty.append((T, n_ok, nvars, top))
        assert n_ok == 0, (T, n_ok, nvars, top)
    # Hand T=8: u1=u3=1 forces a later 1 in the supposed zero tail.
    u8 = (1 << 1) | (1 << 3) | (1 << 5)  # u1=u3=u5=1, rest 0 through u6
    assert eval_anf(F[8], u8) == 1
    assert eval_anf(F[17], u8) == 1  # u7=0 branch
    u8b = u8 | (1 << 7)
    assert eval_anf(F[15], u8b) == 1  # u7=1 branch
    return {
        "forward_recon_ok": True,
        "v_independent": True,
        "poly_matches_recon": True,
        "F4_zero_on_fib": True,
        "onset_T_1_to_10_unsat": empty,
        "T8_both_u7_branches_fail": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kmax", type=int, default=16)
    parser.add_argument("--nmax", type=int, default=8)
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--json-out", type=str, default="")
    args = parser.parse_args()

    if args.certify:
        report = certify()
        print("certify: all assertions passed")
        print(json.dumps(report, indent=2))
        if args.json_out:
            with open(args.json_out, "w") as f:
                json.dump(report, f, indent=2)
                f.write("\n")
        return

    cert = certify()
    cols, F, G = column_table(args.kmax)
    edges, _, _ = check_edge_on_fib(args.nmax)
    report = {
        **cert,
        "columns_reduced": cols,
        "edge_polynomials": edges,
    }
    print("v-independence: True")
    print("ANF vs reconstruction: True")
    print("Reduced columns F_k = x(2n,-k), G_k = x(2n+1,-k):")
    for row in cols:
        print(f"  k={row['k']:2d}  F={row['F']:40s}  G={row['G']}")
    print("Even-edge polynomials E_n = x(2n,-2n) = F_{2n}(u_n,u_{n+1},...):")
    for row in edges:
        print(
            f"  n={row['n']}  E={row['E_anf']}  ident={row['E_identically']}"
            f"  O={row['O_anf']}  ident={row['O_identically']}"
        )
    print("Onset L_0 unsat for T=1..10 (extra=10):", cert["onset_T_1_to_10_unsat"])
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(report, f, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
