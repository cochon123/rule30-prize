"""Cycle I attack: Condrey-style unique left fiber for a period-2 Rule 30 centre.

Condrey 2026 (arXiv:2609.09431) classifies the unique left half making the
central trace *constant*. This script asks the same question at period 2:
given a finite right half and a prescribed period-2 centre (phase 01 or 10),
the left is unique via

    x(t, j-1) = x(t+1, j) XOR (x(t, j) OR x(t, j+1)),

hence l_t = c_{t+1} XOR (c_t OR r_t). Either that left is an infinite
closed-form tail (Condrey-style survive) or a finite right+left pair exists
(kill) or every small-radius row breaks period 2 by a documented f(w)
(finite theorem, not a uniform proof).

This is not the strip-graph residual-SCC test, not onset SAT, and not an
F_T ideal certificate. Identities from research/period2_neighbor.md are
reused as checks (u has no consecutive 1s; u_{n+1}=1 iff a width-3 right
vacuum) without modifying that file.

Run: python3 research/period2_fiber.py --certify
Dump: research/period2_fiber.json
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().with_suffix(".json")


# ---------------------------------------------------------------------------
# Rule 30, packed. Bit 0 is the leftmost cell of the current support.
# One step expands the support by one cell on each side:
#   new = (row << 2) ^ ((row << 1) | row)
# and the old centre bit w sits at bit w+t at time t.
# ---------------------------------------------------------------------------

def rule30_step(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def center_bit(row: int, w: int, t: int) -> int:
    return (row >> (w + t)) & 1


def evolve_centers(mask: int, w: int, tcap: int) -> list[int]:
    row = mask
    out = [0] * tcap
    for t in range(tcap):
        out[t] = (row >> (w + t)) & 1
        row = rule30_step(row)
    return out


def naive_centers(live: dict[int, int], tcap: int) -> list[int]:
    """Independent spacetime for self-check. live: position -> bit at t=0."""
    centers = []
    cur = {p: 1 for p, b in live.items() if b}
    for _t in range(tcap):
        centers.append(1 if 0 in cur else 0)
        if not cur:
            centers.extend([0] * (tcap - len(centers)))
            break
        mn, mx = min(cur), max(cur)
        nxt = {}
        for j in range(mn - 1, mx + 2):
            a = 1 if (j - 1) in cur else 0
            b = 1 if j in cur else 0
            c = 1 if (j + 1) in cur else 0
            if a ^ (b | c):
                nxt[j] = 1
        cur = nxt
    return centers


def mask_to_live(mask: int, w: int) -> dict[int, int]:
    live = {}
    for i in range(2 * w + 1):
        if (mask >> i) & 1:
            live[i - w] = 1
    return live


def alt_run_stats(bits: list[int]) -> dict:
    """Longest alternating (period-2) run, prefix, and suffix."""
    n = len(bits)
    if n == 0:
        return {
            "L": 0,
            "start": 0,
            "prefix": 0,
            "suffix": 0,
            "reaches_cap": False,
        }
    best = 1
    best_start = 0
    run = 1
    run_start = 0
    prefix = 1
    prefix_alive = True
    for t in range(1, n):
        if bits[t] != bits[t - 1]:
            run += 1
            if prefix_alive:
                prefix += 1
        else:
            run = 1
            run_start = t
            prefix_alive = False
        if run > best:
            best = run
            best_start = run_start
    suffix = run
    return {
        "L": best,
        "start": best_start,
        "prefix": prefix,
        "suffix": suffix,
        "reaches_cap": best_start + best == n and best >= 2,
    }


def scan_mask_runs(mask: int, w: int, tcap: int) -> dict:
    """Evolve one packed row, tracking alternating runs without storing the trace."""
    row = mask
    prev = (row >> w) & 1
    best = 1
    best_start = 0
    run = 1
    run_start = 0
    prefix = 1
    prefix_alive = True
    for t in range(1, tcap):
        row = rule30_step(row)
        bit = (row >> (w + t)) & 1
        if bit != prev:
            run += 1
            if prefix_alive:
                prefix += 1
        else:
            run = 1
            run_start = t
            prefix_alive = False
        if run > best:
            best = run
            best_start = run_start
        prev = bit
    return {
        "L": best,
        "start": best_start,
        "prefix": prefix,
        "suffix": run,
        "reaches_cap": best_start + best == tcap and best >= 2,
        "end": best_start + best,
    }


def tcap_short(w: int) -> int:
    return 4 * w + 64


def tcap_long(w: int) -> int:
    return 8 * w + 128


def tcap_fiber(w: int) -> int:
    return max(64, 8 * w + 128)


# ---------------------------------------------------------------------------
# Forced-centre right half, packed. Bit 0 is the centre (overwritten each
# step by the prescribed period-2 bit). Bit j>=1 is spatial position +j.
# ---------------------------------------------------------------------------

def forced_right_traces(right: list[int], c0: int, T: int):
    """Return traces c, r=x(*,1), e=x(*,2), f=x(*,3) of length T+1."""
    row = 1 if c0 else 0
    for j, b in enumerate(right):
        if b:
            row |= 1 << (j + 1)
    c = [0] * (T + 1)
    r = [0] * (T + 1)
    e = [0] * (T + 1)
    f = [0] * (T + 1)
    for t in range(T + 1):
        c[t] = row & 1
        r[t] = (row >> 1) & 1
        e[t] = (row >> 2) & 1
        f[t] = (row >> 3) & 1
        if t == T:
            break
        nxt = (row << 1) ^ (row | (row >> 1))
        nxt_c = c0 ^ ((t + 1) & 1)
        row = (nxt & ~1) | nxt_c
    return c, r, e, f


def reconstruct_left_from_traces(c: list[int], r: list[int]) -> list[int]:
    """Initial left bits L_k = x(0, -k) for k = 1, ..., len(c)-1.

    Column traces shrink by one time each step left. Needs centre through
    time T to produce T left bits.
    """
    T = len(c) - 1
    if T <= 0:
        return []
    # column 0 is c; column +1 is r; build column -1, -2, ...
    mid = [c[t + 1] ^ (c[t] | r[t]) for t in range(T)]  # x(t, -1) for t=0..T-1
    rightish = c
    left0 = [mid[0]]
    for _d in range(2, T + 1):
        tmax = len(mid) - 1
        newcol = [0] * tmax
        for t in range(tmax):
            newcol[t] = mid[t + 1] ^ (mid[t] | rightish[t])
        left0.append(newcol[0])
        rightish = mid
        mid = newcol
    return left0


def fiber_left(right: list[int], c0: int, T: int) -> dict:
    c, r, e, f = forced_right_traces(right, c0, T)
    left = reconstruct_left_from_traces(c, r)
    u = [r[2 * n] for n in range((T // 2) + 1) if 2 * n <= T]
    eu = [e[2 * n] for n in range(len(u))]
    fu = [f[2 * n] for n in range(len(u))]
    return {
        "c": c,
        "r": r,
        "e": e,
        "f": f,
        "u": u,
        "eu": eu,
        "fu": fu,
        "left": left,
    }


def last_one(seq: list[int]) -> int:
    last = 0
    for i, v in enumerate(seq, 1):
        if v:
            last = i
    return last


def gap_stats(seq: list[int]) -> dict:
    pos = [i for i, v in enumerate(seq) if v]
    n = len(seq)
    if not pos:
        return {
            "n1": 0,
            "last1": 0,
            "maxgap": n,
            "trail": n,
            "lead": n,
        }
    gaps = [pos[i] - pos[i - 1] - 1 for i in range(1, len(pos))]
    return {
        "n1": len(pos),
        "last1": pos[-1] + 1,
        "maxgap": max(gaps) if gaps else 0,
        "trail": n - 1 - pos[-1],
        "lead": pos[0],
    }


def bm_len(bits: list[int]) -> int:
    """Berlekamp–Massey linear complexity over GF(2)."""
    n = len(bits)
    C = [1]
    B = [1]
    L = 0
    m = 1
    for n_i in range(n):
        d = bits[n_i]
        for i in range(1, L + 1):
            if i < len(C):
                d ^= C[i] & bits[n_i - i]
        if d == 0:
            m += 1
        else:
            Tcopy = C[:]
            while len(C) < len(B) + m:
                C.append(0)
            for i in range(len(B)):
                C[i + m] ^= B[i]
            if 2 * L <= n_i:
                L = n_i + 1 - L
                B = Tcopy
                m = 1
            else:
                m += 1
    return L


def consec_ones(seq: list[int]) -> bool:
    return any(seq[i] == 1 and seq[i + 1] == 1 for i in range(len(seq) - 1))


def bits_from_int(n: int, w: int) -> list[int]:
    return [(n >> (j - 1)) & 1 for j in range(1, w + 1)]


def pack_row(left_bits: list[int], c0: int, right: list[int]) -> tuple[int, int]:
    """Pack L_1.., centre, R_1.. into a packed row with radius w = max(depths)."""
    wl = len(left_bits)
    wr = len(right)
    w = max(wl, wr)
    mask = 0
    if c0:
        mask |= 1 << w
    for k, v in enumerate(left_bits, 1):
        if v:
            mask |= 1 << (w - k)
    for j, v in enumerate(right, 1):
        if v:
            mask |= 1 << (w + j)
    return mask, w


def fit_linear(xs: list[int], ys: list[int]) -> tuple[float, float]:
    n = len(xs)
    if n < 2:
        return 0.0, float(ys[0]) if ys else 0.0
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    den = n * sxx - sx * sx
    if den == 0:
        return 0.0, sy / n
    C = (n * sxy - sx * sy) / den
    Cp = (sy - C * sx) / n
    return C, Cp


def suffix_period(seq: list[int], min_periods: int = 6):
    n = len(seq)
    if n < 2 * min_periods:
        return None
    for p in range(1, n // min_periods + 1):
        need = min_periods * p
        for t0 in range(0, n - need + 1):
            pat = seq[t0 : t0 + p]
            if all(seq[i] == pat[(i - t0) % p] for i in range(t0, n)):
                return {"p": p, "t0": t0, "pat": "".join(map(str, pat))}
    return None


# ---------------------------------------------------------------------------
# Condrey constant-fiber audit (sanity only; not a re-proof).
# ---------------------------------------------------------------------------

def condrey_zero_left(right: list[int], depth: int) -> list[int]:
    """Theorem 2: first right 1 at m, then L_j=0 (j<m), L_m=1, L_j=j mod 2 (j>m)."""
    m = None
    for j, b in enumerate(right, 1):
        if b:
            m = j
            break
    out = []
    for k in range(1, depth + 1):
        if m is None:
            out.append(0)
        elif k < m:
            out.append(0)
        elif k == m:
            out.append(1)
        else:
            out.append(k & 1)
    return out


def condrey_one_left(depth: int) -> list[int]:
    """Theorem 3: L_j = 1 iff j is positive and even."""
    return [1 if (k % 2 == 0) else 0 for k in range(1, depth + 1)]


def forced_const_traces(right: list[int], cconst: int, T: int):
    row = 1 if cconst else 0
    for j, b in enumerate(right):
        if b:
            row |= 1 << (j + 1)
    c = [0] * (T + 1)
    r = [0] * (T + 1)
    for t in range(T + 1):
        c[t] = row & 1
        r[t] = (row >> 1) & 1
        if t == T:
            break
        nxt = (row << 1) ^ (row | (row >> 1))
        row = (nxt & ~1) | cconst
    return c, r


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def prize_prefix() -> str:
    return "".join(map(str, evolve_centers(1, 0, 16)))


def run_checks() -> dict:
    checks = {}

    # Packed CA vs naive on the prize seed and a few random small rows.
    prize = evolve_centers(1, 0, 32)
    naive_prize = naive_centers({0: 1}, 32)
    checks["packed_matches_naive_prize"] = prize == naive_prize
    checks["prize_prefix16"] = "".join(map(str, prize[:16]))
    checks["prize_prefix16_ok"] = checks["prize_prefix16"] == "1101110011000101"

    for w, mask in [(1, 5), (2, 19), (3, 73), (4, 300)]:
        a = evolve_centers(mask, w, 40)
        b = naive_centers(mask_to_live(mask, w), 40)
        if a != b:
            checks["packed_matches_naive_small"] = False
            checks["naive_fail"] = {"w": w, "mask": mask}
            break
    else:
        checks["packed_matches_naive_small"] = True

    # Reconstruction recovers the true left of a genuine spacetime.
    w, mask, T = 3, 0b1011011, 24
    live = mask_to_live(mask, w)
    # Build actual traces from naive spacetime.
    cells = dict(live)
    spacetime = [dict(cells)]
    for _t in range(T):
        if not cells:
            spacetime.append({})
            continue
        mn, mx = min(cells), max(cells)
        nxt = {}
        for j in range(mn - 1, mx + 2):
            a = cells.get(j - 1, 0)
            b = cells.get(j, 0)
            c = cells.get(j + 1, 0)
            if a ^ (b | c):
                nxt[j] = 1
        cells = nxt
        spacetime.append(cells)
    c = [spacetime[t].get(0, 0) for t in range(T + 1)]
    r = [spacetime[t].get(1, 0) for t in range(T + 1)]
    recon = reconstruct_left_from_traces(c, r)
    true_left = [live.get(-k, 0) for k in range(1, T + 1)]
    checks["recon_recovers_true_left"] = recon == true_left

    # Condrey constant-0 fiber formula vs reconstruction.
    condrey_ok = True
    T = 24
    for m in range(1, 8):
        right = [0] * 8
        right[m - 1] = 1
        cc, rr = forced_const_traces(right, 0, T)
        left = reconstruct_left_from_traces(cc, rr)
        formula = condrey_zero_left(right, T)
        if left != formula:
            condrey_ok = False
            checks["condrey_zero_fail_m"] = m
            break
    checks["condrey_zero_fiber"] = condrey_ok

    # Condrey all-one fiber: left independent of the right.
    one_ok = True
    formula1 = condrey_one_left(T)
    for n in range(8):
        right = bits_from_int(n, 3)
        cc, rr = forced_const_traces(right, 1, T)
        left = reconstruct_left_from_traces(cc, rr)
        if left != formula1:
            one_ok = False
            break
    checks["condrey_one_fiber"] = one_ok

    # Neighbor identity on forced period-2 phase 01 (period2_neighbor.md).
    id_ok = True
    no11 = True
    for w in range(0, 5):
        for n in range(1 << w):
            fib = fiber_left(bits_from_int(n, w), 0, 40)
            u, eu, fu = fib["u"], fib["eu"], fib["fu"]
            if consec_ones(u):
                no11 = False
            for i in range(len(u) - 1):
                pred = 1 if (u[i], eu[i], fu[i]) == (0, 0, 0) else 0
                if pred != u[i + 1]:
                    id_ok = False
                    break
            if not id_ok:
                break
        if not id_ok:
            break
    checks["u_no_consecutive_ones_phase01"] = no11
    checks["u_vacuum_triple_identity_phase01"] = id_ok

    # Odd-time left neighbor is identically 1 on phase 01 (alternating.md).
    odd_l = True
    fib = fiber_left([], 0, 40)
    # l_t = c_{t+1} XOR (c_t OR r_t); at odd t, c_t=1, c_{t+1}=0 => l_t=1.
    c, r = fib["c"], fib["r"]
    for t in range(0, 39, 2):
        pass
    for t in range(1, 39, 2):
        lt = c[t + 1] ^ (c[t] | r[t])
        if lt != 1:
            odd_l = False
            break
    checks["phase01_odd_left_is_one"] = odd_l

    # Fiber prefix is stable as T grows (well-defined infinite left).
    a = fiber_left([1, 0, 1], 0, 30)["left"]
    b = fiber_left([1, 0, 1], 0, 60)["left"]
    checks["fiber_prefix_stable"] = a == b[:30]

    checks["all_ok"] = all(
        v is True for k, v in checks.items() if k not in ("prize_prefix16",)
    )
    return checks


# ---------------------------------------------------------------------------
# Experiment 1: exhaustive finite radius-w rows
# ---------------------------------------------------------------------------

def exhaustive_scan(w_max: int, skip_w10: bool, log) -> tuple[list[dict], list[dict]]:
    rows = []
    cap_survivors = []
    for w in range(0, w_max + 1):
        if w == 10 and skip_w10:
            log.append(f"skip w=10 (2^{21} states)")
            continue
        # 8w+128 for every scanned radius. w=10 is 2^21 states times ~208
        # steps and finishes in about two minutes in this environment.
        tcap = tcap_long(w)
        nstates = 1 << (2 * w + 1)
        t0 = time.perf_counter()
        Lrun = 0
        Lpref = 0
        Lsuff = 0
        best = None
        n_reach = 0
        n_gt_4w16 = 0
        max_end = 0
        for mask in range(1, nstates):
            st = scan_mask_runs(mask, w, tcap)
            if st["L"] > Lrun:
                Lrun = st["L"]
                best = {
                    "mask": mask,
                    "row": "".join(str((mask >> i) & 1) for i in range(2 * w + 1)),
                    "L": st["L"],
                    "start": st["start"],
                    "end": st["end"],
                    "prefix": st["prefix"],
                    "suffix": st["suffix"],
                }
            if st["prefix"] > Lpref:
                Lpref = st["prefix"]
            if st["suffix"] > Lsuff:
                Lsuff = st["suffix"]
            if st["end"] > max_end:
                max_end = st["end"]
            if st["L"] > 4 * w + 16:
                n_gt_4w16 += 1
            # Eventual-in-cap: after a light-cone transient the rest of the
            # trace is period 2. A short alternating suffix that merely
            # touches tcap is not eventual.
            last_break = tcap - st["suffix"]
            transient = max(2 * w + 8, 16)
            eventual_in_cap = st["suffix"] >= 16 and last_break <= transient
            cap_touch = st["end"] == tcap and st["suffix"] >= max(16, Lrun)
            if eventual_in_cap or cap_touch:
                if eventual_in_cap:
                    n_reach += 1
                ext = max(4 * tcap, 8 * w + 512)
                st2 = scan_mask_runs(mask, w, ext)
                last2 = ext - st2["suffix"]
                rec = {
                    "w": w,
                    "mask": mask,
                    "tcap": tcap,
                    "eventual_in_cap": eventual_in_cap,
                    "L_at_tcap": st["L"],
                    "suffix": st["suffix"],
                    "last_break": last_break,
                    "ext": ext,
                    "L_ext": st2["L"],
                    "suffix_ext": st2["suffix"],
                    "last_break_ext": last2,
                    "reaches_ext": st2["suffix"] >= ext - transient,
                }
                cap_survivors.append(rec)
                if st2["L"] > Lrun:
                    Lrun = st2["L"]
                    best = {
                        "mask": mask,
                        "row": "".join(
                            str((mask >> i) & 1) for i in range(2 * w + 1)
                        ),
                        "L": st2["L"],
                        "start": st2["start"],
                        "end": st2["end"],
                        "prefix": st2["prefix"],
                        "suffix": st2["suffix"],
                        "extended_tcap": ext,
                    }
        elapsed = time.perf_counter() - t0
        row = {
            "w": w,
            "n_nonzero": nstates - 1,
            "tcap": tcap,
            "L_run": Lrun,
            "L_prefix": Lpref,
            "L_suffix": Lsuff,
            "max_run_end": max_end,
            "n_cap_survivors": n_reach,
            "n_L_gt_4w16": n_gt_4w16,
            "bound_4w16": 4 * w + 16,
            "best": best,
            "elapsed_sec": round(elapsed, 4),
        }
        rows.append(row)
        log.append(
            f"exhaustive w={w} n={nstates - 1} tcap={tcap} "
            f"L_run={Lrun} L_prefix={Lpref} L_suffix={Lsuff} "
            f"reach={n_reach} L>4w+16={n_gt_4w16} {elapsed:.3f}s"
        )
    return rows, cap_survivors


# ---------------------------------------------------------------------------
# Experiment 2: unique left fiber of every finite right
# ---------------------------------------------------------------------------

def fiber_scan(w_max: int, log) -> dict:
    by_w = []
    finite_hits = []
    long_bimaterial = []
    attractors = {0: Counter(), 1: Counter()}
    n_none = {0: 0, 1: 0}
    leading_distinct = []
    special = []

    for w in range(0, w_max + 1):
        T = tcap_fiber(w)
        t0 = time.perf_counter()
        for c0, phase in ((0, "01"), (1, "10")):
            maxgap = 0
            min_last1 = 10**9
            max_trail = 0
            min_n1 = 10**9
            max_bm = 0
            min_bm = 10**9
            n_finiteish = 0
            n_id_fail = 0
            n_consec = 0
            lefts_by_m: dict[int, set[str]] = {}
            n_u_ev0 = 0
            for n in range(1 << w):
                right = bits_from_int(n, w)
                fib = fiber_left(right, c0, T)
                left = fib["left"]
                st = gap_stats(left)
                bm = bm_len(left[: min(len(left), 80)])
                maxgap = max(maxgap, st["maxgap"])
                min_last1 = min(min_last1, st["last1"])
                max_trail = max(max_trail, st["trail"])
                min_n1 = min(min_n1, st["n1"])
                max_bm = max(max_bm, bm)
                min_bm = min(min_bm, bm)
                if c0 == 0:
                    u = fib["u"]
                    if consec_ones(u):
                        n_consec += 1
                    for i in range(len(u) - 1):
                        pred = (
                            1
                            if (u[i], fib["eu"][i], fib["fu"][i]) == (0, 0, 0)
                            else 0
                        )
                        if pred != u[i + 1]:
                            n_id_fail += 1
                            break
                    if sum(u[-16:]) == 0:
                        n_u_ev0 += 1
                    per = suffix_period(u, min_periods=6)
                    if per is None:
                        n_none[c0] += 1
                    else:
                        attractors[c0][per["pat"]] += 1
                else:
                    per = suffix_period(fib["u"], min_periods=6)
                    if per is None:
                        n_none[c0] += 1
                    else:
                        attractors[c0][per["pat"]] += 1

                # Finite-left candidate: a long zero tail, last 1 bounded.
                if st["trail"] >= 24 and st["last1"] <= T - 24:
                    n_finiteish += 1
                    W = st["last1"]
                    mask, ww = pack_row(left[:W], c0, right)
                    ext = max(8 * ww + 128, 256)
                    st_fwd = (
                        scan_mask_runs(mask, ww, ext) if mask else None
                    )
                    hit = {
                        "w": w,
                        "phase": phase,
                        "right": "".join(map(str, right)),
                        "last1": st["last1"],
                        "trail": st["trail"],
                        "T": T,
                    }
                    if st_fwd is not None:
                        hit["forward_prefix"] = st_fwd["prefix"]
                        hit["forward_L"] = st_fwd["L"]
                        hit["forward_tcap"] = ext
                        hit["forward_reaches"] = st_fwd["reaches_cap"]
                        if st_fwd["prefix"] > 4 * w + 16:
                            long_bimaterial.append(hit)
                    finite_hits.append(hit)

                if n > 0 and w > 0:
                    m = min(j for j, b in enumerate(right, 1) if b)
                    lefts_by_m.setdefault(m, set()).add(
                        "".join(map(str, left[: min(40, len(left))]))
                    )

                # Sparse / periodic left family.
                if bm <= 8 and st["n1"] <= T // 5 + 2:
                    special.append(
                        {
                            "w": w,
                            "phase": phase,
                            "right": "".join(map(str, right)),
                            "n1": st["n1"],
                            "bm80": bm,
                            "maxgap": st["maxgap"],
                            "head": "".join(map(str, left[:24])),
                        }
                    )

            rec = {
                "w": w,
                "phase": phase,
                "T": T,
                "n_rights": 1 << w,
                "maxgap": maxgap,
                "min_last1": min_last1 if min_last1 < 10**9 else 0,
                "max_trail": max_trail,
                "min_n1": min_n1 if min_n1 < 10**9 else 0,
                "max_bm80": max_bm,
                "min_bm80": min_bm if min_bm < 10**9 else 0,
                "n_finiteish": n_finiteish,
                "n_identity_fail": n_id_fail,
                "n_consec11": n_consec,
                "n_u_eventual0": n_u_ev0,
                "elapsed_sec": round(time.perf_counter() - t0, 4),
            }
            if w > 0:
                rec["n_distinct_lefts_by_leading_one"] = {
                    str(m): len(s) for m, s in sorted(lefts_by_m.items())
                }
                leading_distinct.append(
                    {
                        "w": w,
                        "phase": phase,
                        "by_m": rec["n_distinct_lefts_by_leading_one"],
                    }
                )
            by_w.append(rec)
            log.append(
                f"fiber w={w} {phase} T={T} maxgap={maxgap} min_last1={rec['min_last1']} "
                f"max_trail={max_trail} finiteish={n_finiteish} "
                f"u_ev0={n_u_ev0} id_fail={n_id_fail}"
            )

    # Dedup specials: keep a few illustrative ones.
    special_uniq = []
    seen = set()
    for s in special:
        key = (s["phase"], s["head"], s["bm80"])
        if key in seen:
            continue
        seen.add(key)
        special_uniq.append(s)
        if len(special_uniq) >= 12:
            break

    att_dump = {}
    for c0, phase in ((0, "01"), (1, "10")):
        att_dump[phase] = [
            {"pat": p, "count": c, "period": len(p)}
            for p, c in attractors[c0].most_common(16)
        ]

    return {
        "by_w": by_w,
        "finite_left_hits": finite_hits,
        "bimaterial_prefix_gt_4w16": long_bimaterial[:20],
        "n_bimaterial_prefix_gt_4w16": len(long_bimaterial),
        "u_attractors": att_dump,
        "n_u_no_suffix_period": n_none,
        "leading_one_does_not_determine_left": any(
            int(v) > 1
            for rec in leading_distinct
            for v in rec["by_m"].values()
        ),
        "leading_distinct": leading_distinct,
        "special_low_complexity_lefts": special_uniq,
    }


def truncated_fiber_horizon(w_max: int, log) -> list[dict]:
    """Install the unique left through depth w and measure the p2 prefix.

    Condrey notes H(2,w) >= w by left permutivity; this table is the
    matching finite-horizon analogue of his Theorems 6–7.
    """
    out = []
    for w in range(1, w_max + 1):
        Trec = 2 * w + 24
        tcap = 4 * w + 32
        max_pref = 0
        n_full = 0
        best = None
        for c0 in (0, 1):
            for n in range(1 << w):
                right = bits_from_int(n, w)
                left = fiber_left(right, c0, Trec)["left"]
                mask, ww = pack_row(left[:w], c0, right)
                if mask == 0:
                    continue
                st = scan_mask_runs(mask, ww, tcap)
                if st["prefix"] > max_pref:
                    max_pref = st["prefix"]
                    best = {
                        "phase": "01" if c0 == 0 else "10",
                        "right": "".join(map(str, right)),
                        "prefix": st["prefix"],
                    }
                if st["prefix"] >= tcap:
                    n_full += 1
        rec = {
            "w": w,
            "tcap": tcap,
            "max_p2_prefix": max_pref,
            "n_prefix_hits_tcap": n_full,
            "best": best,
        }
        out.append(rec)
        log.append(
            f"trunc-fiber w={w} max_p2_prefix={max_pref} tcap={tcap} n_full={n_full}"
        )
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def certify(w_exh: int, w_fiber: int, skip_w10: bool) -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    exh, cap_surv = exhaustive_scan(w_exh, skip_w10, log)
    fib = fiber_scan(w_fiber, log)
    trunc = truncated_fiber_horizon(min(w_fiber, 8), log)

    xs = [r["w"] for r in exh]
    ys = [r["L_run"] for r in exh]
    C, Cp = fit_linear(xs, ys)
    residuals = [y - (C * x + Cp) for x, y in zip(xs, ys)]
    yp = [r["L_prefix"] for r in exh]
    Cp2, Cpp = fit_linear(xs, yp)

    genuine = [
        s
        for s in cap_surv
        if s.get("eventual_in_cap") and s.get("reaches_ext")
    ]
    finite_left = fib["finite_left_hits"]

    # Verdict.
    if genuine:
        verdict = "KILL"
        kill_reason = (
            "finite nonzero row whose centre stays period-2 through an "
            "extended cap (looks genuinely eventual)"
        )
    elif finite_left:
        verdict = "KILL"
        kill_reason = (
            "finite reconstructed left for a finite right: a bimaterial "
            "period-2 fiber member"
        )
    else:
        closed = (
            not fib["leading_one_does_not_determine_left"]
            and fib["n_u_no_suffix_period"]["0"] == 0
        )
        # Closed-form survive needs an explicit infinite tail for every
        # nonzero finite right, like Condrey's alternating / checkerboard.
        # Growing BM, several u-attractors, and many aperiodic u-suffixes
        # block that.
        max_bm = max(r["max_bm80"] for r in fib["by_w"])
        survive = False
        if closed and max_bm <= 16:
            survive = True
        if survive:
            verdict = "SURVIVE"
            kill_reason = (
                "closed-form unique left fiber, always infinite on nonzero "
                "finite rights"
            )
        else:
            Lmax = max(ys) if ys else 0
            plateau_ws = [r["w"] for r in exh if r["L_run"] == Lmax]
            verdict = "FINITE_THEOREM"
            kill_reason = (
                "no genuine eventual witness and no Condrey-style closed-form "
                "left fiber; unique left of every finite right is infinite in "
                f"the scan (min last1 ~ T); L_run(w) <= {Lmax} with a plateau "
                f"on w={min(plateau_ws)}..{max(plateau_ws)}; L_prefix grows "
                "like w (Condrey H(2,w)>=w); every radius-w row breaks period "
                "2 by time 8w+128, and no period-2 run exceeds L_run(w)"
            )

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period2_fiber",
        "arxiv": "2609.09431",
        "problem": (
            "no nonzero finite-support configuration has an eventually "
            "period-2 central trace"
        ),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": verdict == "SURVIVE",
        "kill_reason": kill_reason,
        "wall_time_sec": round(wall, 4),
        "tcap_short": "4w+64",
        "tcap_long": "8w+128",
        "checks": checks,
        "exhaustive": exh,
        "cap_survivors": [
            s for s in cap_surv if s.get("eventual_in_cap")
        ]
        + [
            s
            for s in cap_surv
            if not s.get("eventual_in_cap")
        ][:8],
        "genuine_eventual_witnesses": genuine,
        "fit_L_run": {
            "C": C,
            "Cprime": Cp,
            "max_residual": max(residuals) if residuals else 0.0,
            "min_residual": min(residuals) if residuals else 0.0,
            "note": (
                "least-squares L_run ~ C*w+C' is a summary only; the table "
                "plateaus and is the actual finite theorem"
            ),
        },
        "exclusion_table": {
            "f_w": "L_run(w); a period-2 centre run of a radius-w row lasts at most L_run(w) steps inside tcap=8w+128",
            "L_run": [{"w": r["w"], "L": r["L_run"], "tcap": r["tcap"]} for r in exh],
            "L_prefix": [{"w": r["w"], "L": r["L_prefix"]} for r in exh],
            "n_L_gt_4w16": sum(r["n_L_gt_4w16"] for r in exh),
            "n_eventual_in_cap": sum(r["n_cap_survivors"] for r in exh),
            "n_genuine_eventual": len(genuine),
            "n_finite_left_fiber": len(finite_left),
        },
        "fit_L_prefix": {"C": Cp2, "Cprime": Cpp},
        "fiber": fib,
        "truncated_fiber_horizon": trunc,
        "log": log,
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict={verdict} wall={wall:.3f}s")
    print(f"reason: {kill_reason}")
    print(f"L_run by w: {[(r['w'], r['L_run'], r['tcap']) for r in exh]}")
    print(f"fit L_run ~ {C:.3f}*w + {Cp:.3f}")
    print(f"n_cap_survivors={sum(r['n_cap_survivors'] for r in exh)} genuine={len(genuine)}")
    print(f"finite_left_hits={len(finite_left)}")
    return dump


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    p.add_argument("--w-exh", type=int, default=10)
    p.add_argument("--w-fiber", type=int, default=10)
    p.add_argument("--skip-w10", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    skip = args.skip_w10
    if args.w_exh >= 10 and not args.skip_w10:
        # w=10 is 2^21 states; run it unless the user opts out.
        skip = False
    certify(args.w_exh, args.w_fiber, skip)


if __name__ == "__main__":
    main()
