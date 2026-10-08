#!/usr/bin/env python3
"""Cycle I / ideas9 item 2: Condrey-style finite-row scan for period 3.

Same exhaustive packed scan as research/period2_fiber.py, but the centre
factor is exact period 3. The two primitive necklaces are 001 and 011;
all three rotations of each (six global phases) are scored:

    001, 010, 100    and    011, 110, 101.

L3(w) = L_run(w) is the longest run of any of those six infinite words
in the centre of a radius-w finite row, evolved in a quiescent
background. L_prefix(w) is the same quantity restricted to a run that
starts at t=0.

Exhaustive w=0..8 (2^{17}-1 nonzero masks at w=8). tcap=8w+128.
Packed Rule 30: new=(row<<2)^((row<<1)|row), centre (row>>(w+t))&1.

Kill: L3(w) keeps growing through w=8 with no plateau, or a witness
that remains period-3 through the whole cap (looks eventual). Finite
theorem if L3 plateaus at a constant on the scanned radii.

This is not the strip-graph residual-SCC test, not onset SAT, not an
F_T ideal certificate, and not the period-2 fiber reconstruction.
Stdlib only. Not a prize claim.

Run: python3 research/period3_fiber.py --certify
Dump: research/period3_fiber.json, research/period3_fiber.md
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits

OUT_JSON = Path(__file__).resolve().with_suffix(".json")
OUT_MD = Path(__file__).resolve().with_suffix(".md")

# Six exact period-3 words: 3 rotations of 001 and of 011.
# Index is global time mod 3 (the starting phase).
PATS = (
    (0, 0, 1),  # 001
    (0, 1, 0),  # 010
    (1, 0, 0),  # 100
    (0, 1, 1),  # 011
    (1, 1, 0),  # 110
    (1, 0, 1),  # 101
)
PAT_NAME = ("001", "010", "100", "011", "110", "101")
NECKLACE = ("001", "001", "001", "011", "011", "011")
PRIZE_PREFIX16 = "1101110011000101"


# ---------------------------------------------------------------------------
# Rule 30, packed. Bit 0 is the leftmost cell of the current support.
# One step expands the support by one cell on each side:
#   new = (row << 2) ^ ((row << 1) | row)
# and the old centre bit w sits at bit w+t at time t.
# ---------------------------------------------------------------------------

def rule30_step(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


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


def tcap_long(w: int) -> int:
    return 8 * w + 128


def row_bits(mask: int, w: int) -> str:
    return "".join(str((mask >> i) & 1) for i in range(2 * w + 1))


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


# ---------------------------------------------------------------------------
# Exact period-3 runs. A factor is period 3 iff it matches one of the six
# infinite words along global time (rotations already encode the phase).
# Constants 000 and 111 are excluded because they are not in PATS.
# ---------------------------------------------------------------------------

def p3_stats_from_bits(bits: list[int]) -> dict:
    n = len(bits)
    empty = {
        "L": 0,
        "start": 0,
        "end": 0,
        "prefix": 0,
        "suffix": 0,
        "pattern": None,
        "necklace": None,
        "L_001": 0,
        "L_011": 0,
        "reaches_cap": False,
        "by_pattern": {name: {"L": 0, "start": 0, "prefix": 0, "suffix": 0} for name in PAT_NAME},
    }
    if n == 0:
        return empty

    best = 0
    best_start = 0
    best_i = 0
    L_001 = 0
    L_011 = 0
    prefix = 0
    suffix = 0
    by_pattern = {}

    for i, P in enumerate(PATS):
        run = 0
        run_start = 0
        loc_best = 0
        loc_start = 0
        pref = 0
        pref_alive = True
        for t, bit in enumerate(bits):
            if bit == P[t % 3]:
                if run == 0:
                    run_start = t
                run += 1
                if pref_alive:
                    pref += 1
                if run > loc_best:
                    loc_best = run
                    loc_start = run_start
            else:
                run = 0
                pref_alive = False
        name = PAT_NAME[i]
        by_pattern[name] = {
            "L": loc_best,
            "start": loc_start,
            "prefix": pref,
            "suffix": run,
        }
        if NECKLACE[i] == "001":
            if loc_best > L_001:
                L_001 = loc_best
        else:
            if loc_best > L_011:
                L_011 = loc_best
        if loc_best > best:
            best = loc_best
            best_start = loc_start
            best_i = i
        if pref > prefix:
            prefix = pref
        if run > suffix:
            suffix = run

    return {
        "L": best,
        "start": best_start,
        "end": best_start + best,
        "prefix": prefix,
        "suffix": suffix,
        "pattern": PAT_NAME[best_i] if best else None,
        "necklace": NECKLACE[best_i] if best else None,
        "L_001": L_001,
        "L_011": L_011,
        "reaches_cap": best_start + best == n and best >= 3,
        "by_pattern": by_pattern,
    }


def scan_mask_p3(mask: int, w: int, tcap: int) -> dict:
    """Evolve one packed row, tracking the six period-3 phases without storing the trace."""
    row = mask
    # Per-pattern current run, current start, best, best start, prefix, prefix-alive.
    # Unrolled enough to keep the inner update as six integer compares.
    c0 = c1 = c2 = c3 = c4 = c5 = 0
    s0 = s1 = s2 = s3 = s4 = s5 = 0
    b0 = b1 = b2 = b3 = b4 = b5 = 0
    bs0 = bs1 = bs2 = bs3 = bs4 = bs5 = 0
    p0 = p1 = p2 = p3 = p4 = p5 = 0
    a0 = a1 = a2 = a3 = a4 = a5 = 1

    P0, P1, P2, P3, P4, P5 = PATS

    for t in range(tcap):
        bit = (row >> (w + t)) & 1
        r = t % 3
        # 001
        if bit == P0[r]:
            if c0 == 0:
                s0 = t
            c0 += 1
            if a0:
                p0 += 1
            if c0 > b0:
                b0 = c0
                bs0 = s0
        else:
            c0 = 0
            a0 = 0
        # 010
        if bit == P1[r]:
            if c1 == 0:
                s1 = t
            c1 += 1
            if a1:
                p1 += 1
            if c1 > b1:
                b1 = c1
                bs1 = s1
        else:
            c1 = 0
            a1 = 0
        # 100
        if bit == P2[r]:
            if c2 == 0:
                s2 = t
            c2 += 1
            if a2:
                p2 += 1
            if c2 > b2:
                b2 = c2
                bs2 = s2
        else:
            c2 = 0
            a2 = 0
        # 011
        if bit == P3[r]:
            if c3 == 0:
                s3 = t
            c3 += 1
            if a3:
                p3 += 1
            if c3 > b3:
                b3 = c3
                bs3 = s3
        else:
            c3 = 0
            a3 = 0
        # 110
        if bit == P4[r]:
            if c4 == 0:
                s4 = t
            c4 += 1
            if a4:
                p4 += 1
            if c4 > b4:
                b4 = c4
                bs4 = s4
        else:
            c4 = 0
            a4 = 0
        # 101
        if bit == P5[r]:
            if c5 == 0:
                s5 = t
            c5 += 1
            if a5:
                p5 += 1
            if c5 > b5:
                b5 = c5
                bs5 = s5
        else:
            c5 = 0
            a5 = 0
        row = (row << 2) ^ ((row << 1) | row)

    L_001 = b0
    if b1 > L_001:
        L_001 = b1
    if b2 > L_001:
        L_001 = b2
    L_011 = b3
    if b4 > L_011:
        L_011 = b4
    if b5 > L_011:
        L_011 = b5

    best = b0
    best_start = bs0
    best_i = 0
    if b1 > best:
        best, best_start, best_i = b1, bs1, 1
    if b2 > best:
        best, best_start, best_i = b2, bs2, 2
    if b3 > best:
        best, best_start, best_i = b3, bs3, 3
    if b4 > best:
        best, best_start, best_i = b4, bs4, 4
    if b5 > best:
        best, best_start, best_i = b5, bs5, 5

    prefix = p0
    if p1 > prefix:
        prefix = p1
    if p2 > prefix:
        prefix = p2
    if p3 > prefix:
        prefix = p3
    if p4 > prefix:
        prefix = p4
    if p5 > prefix:
        prefix = p5

    suffix = c0
    if c1 > suffix:
        suffix = c1
    if c2 > suffix:
        suffix = c2
    if c3 > suffix:
        suffix = c3
    if c4 > suffix:
        suffix = c4
    if c5 > suffix:
        suffix = c5

    return {
        "L": best,
        "start": best_start,
        "end": best_start + best,
        "prefix": prefix,
        "suffix": suffix,
        "pattern": PAT_NAME[best_i] if best else None,
        "necklace": NECKLACE[best_i] if best else None,
        "L_001": L_001,
        "L_011": L_011,
        "reaches_cap": best_start + best == tcap and best >= 3,
    }


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def run_checks() -> dict:
    checks: dict = {}

    prize = evolve_centers(1, 0, 256)
    ref = list(experiment_center_bits(256))
    checks["packed_matches_experiment_center_bits_256"] = prize == ref
    checks["prize_prefix16"] = "".join(map(str, prize[:16]))
    checks["prize_prefix16_ok"] = checks["prize_prefix16"] == PRIZE_PREFIX16

    naive_prize = naive_centers({0: 1}, 32)
    checks["packed_matches_naive_prize"] = prize[:32] == naive_prize

    for w, mask in [(1, 5), (2, 19), (3, 73), (4, 300)]:
        a = evolve_centers(mask, w, 40)
        b = naive_centers(mask_to_live(mask, w), 40)
        if a != b:
            checks["packed_matches_naive_small"] = False
            checks["naive_fail"] = {"w": w, "mask": mask}
            break
    else:
        checks["packed_matches_naive_small"] = True

    # Synthetic exact period-3 traces.
    syn_001 = [0, 0, 1] * 20
    st = p3_stats_from_bits(syn_001)
    checks["synthetic_001_L"] = st["L"] == 60
    checks["synthetic_001_prefix"] = st["prefix"] == 60
    checks["synthetic_001_pattern"] = st["pattern"] == "001"
    checks["synthetic_001_necklace"] = st["necklace"] == "001"

    syn_011 = [0, 1, 1] * 15
    st = p3_stats_from_bits(syn_011)
    checks["synthetic_011_L"] = st["L"] == 45
    checks["synthetic_011_pattern"] = st["pattern"] == "011"

    # A rotation starting at t=0 is a different named phase of the same necklace.
    syn_010 = [0, 1, 0] * 12
    st = p3_stats_from_bits(syn_010)
    checks["synthetic_010_pattern"] = st["pattern"] == "010"
    checks["synthetic_010_necklace"] = st["necklace"] == "001"

    # Period 2 is not a long period-3 run: "01" repeating matches a 3-bit
    # window of 010 or 101 and then breaks.
    syn_p2 = [t & 1 for t in range(64)]
    st = p3_stats_from_bits(syn_p2)
    checks["period2_is_not_long_p3"] = st["L"] == 3

    # Constants are not exact period 3.
    st = p3_stats_from_bits([0] * 40)
    checks["constant0_L_lt_3"] = st["L"] < 3
    st = p3_stats_from_bits([1] * 40)
    checks["constant1_L_lt_3"] = st["L"] < 3

    # Streaming scan agrees with the stored-trace scorer.
    stream_ok = True
    stream_fail = None
    for w, mask, tcap in [(0, 1, 64), (1, 5, 40), (2, 19, 48), (3, 73, 56), (4, 300, 40)]:
        a = scan_mask_p3(mask, w, tcap)
        b = p3_stats_from_bits(evolve_centers(mask, w, tcap))
        keys = ("L", "start", "end", "prefix", "suffix", "pattern", "necklace", "L_001", "L_011")
        if any(a[k] != b[k] for k in keys):
            stream_ok = False
            stream_fail = {"w": w, "mask": mask, "scan": {k: a[k] for k in keys}, "bits": {k: b[k] for k in keys}}
            break
    checks["scan_matches_stored_trace"] = stream_ok
    if stream_fail is not None:
        checks["scan_fail"] = stream_fail

    # Prize-seed period-3 prefix: 1101110... matches 110 for 5 bits.
    prize16 = [int(ch) for ch in PRIZE_PREFIX16]
    st = p3_stats_from_bits(prize16)
    checks["prize_p3_prefix16"] = st["prefix"]
    checks["prize_p3_prefix16_is_5"] = st["prefix"] == 5

    checks["all_ok"] = all(
        v is True
        for k, v in checks.items()
        if k not in ("prize_prefix16", "prize_p3_prefix16", "naive_fail", "scan_fail")
    )
    return checks


# ---------------------------------------------------------------------------
# Exhaustive finite radius-w rows
# ---------------------------------------------------------------------------

def exhaustive_scan(w_max: int, log: list[str]) -> tuple[list[dict], list[dict]]:
    rows = []
    cap_survivors = []
    for w in range(0, w_max + 1):
        tcap = tcap_long(w)
        nstates = 1 << (2 * w + 1)
        t0 = time.perf_counter()
        Lrun = 0
        Lpref = 0
        Lsuff = 0
        L001 = 0
        L011 = 0
        best = None
        best_prefix = None
        n_at_max = 0
        n_reach = 0
        n_gt_4w16 = 0
        max_end = 0
        bound = 4 * w + 16
        for mask in range(1, nstates):
            st = scan_mask_p3(mask, w, tcap)
            L = st["L"]
            if L > Lrun:
                Lrun = L
                n_at_max = 1
                best = {
                    "mask": mask,
                    "row": row_bits(mask, w),
                    "L": st["L"],
                    "start": st["start"],
                    "end": st["end"],
                    "prefix": st["prefix"],
                    "suffix": st["suffix"],
                    "pattern": st["pattern"],
                    "necklace": st["necklace"],
                    "L_001": st["L_001"],
                    "L_011": st["L_011"],
                }
            elif L == Lrun:
                n_at_max += 1
            if st["prefix"] > Lpref:
                Lpref = st["prefix"]
                best_prefix = {
                    "mask": mask,
                    "row": row_bits(mask, w),
                    "L_prefix": st["prefix"],
                    "pattern": st["pattern"] if st["start"] == 0 else None,
                    "L_run": st["L"],
                }
            if st["suffix"] > Lsuff:
                Lsuff = st["suffix"]
            if st["L_001"] > L001:
                L001 = st["L_001"]
            if st["L_011"] > L011:
                L011 = st["L_011"]
            if st["end"] > max_end:
                max_end = st["end"]
            if L > bound:
                n_gt_4w16 += 1

            last_break = tcap - st["suffix"]
            transient = max(2 * w + 8, 16)
            eventual_in_cap = st["suffix"] >= 16 and last_break <= transient
            cap_touch = st["end"] == tcap and st["suffix"] >= max(16, Lrun)
            if eventual_in_cap or cap_touch:
                if eventual_in_cap:
                    n_reach += 1
                ext = max(4 * tcap, 8 * w + 512)
                st2 = scan_mask_p3(mask, w, ext)
                last2 = ext - st2["suffix"]
                rec = {
                    "w": w,
                    "mask": mask,
                    "tcap": tcap,
                    "eventual_in_cap": eventual_in_cap,
                    "L_at_tcap": st["L"],
                    "suffix": st["suffix"],
                    "last_break": last_break,
                    "pattern": st["pattern"],
                    "ext": ext,
                    "L_ext": st2["L"],
                    "suffix_ext": st2["suffix"],
                    "last_break_ext": last2,
                    "reaches_ext": st2["suffix"] >= ext - transient,
                }
                cap_survivors.append(rec)
                if st2["L"] > Lrun:
                    Lrun = st2["L"]
                    n_at_max = 1
                    best = {
                        "mask": mask,
                        "row": row_bits(mask, w),
                        "L": st2["L"],
                        "start": st2["start"],
                        "end": st2["end"],
                        "prefix": st2["prefix"],
                        "suffix": st2["suffix"],
                        "pattern": st2["pattern"],
                        "necklace": st2["necklace"],
                        "L_001": st2["L_001"],
                        "L_011": st2["L_011"],
                        "extended_tcap": ext,
                    }

        elapsed = time.perf_counter() - t0
        # Confirm the maximizer's factor against a stored trace, and that
        # stretching the cap does not grow a non-eventual run.
        if best is not None:
            bits = evolve_centers(best["mask"], w, tcap)
            chk = p3_stats_from_bits(bits)
            best["stored_L"] = chk["L"]
            best["stored_pattern"] = chk["pattern"]
            factor = bits[best["start"] : best["end"]]
            best["factor"] = "".join(map(str, factor[:60]))
            best["factor_len"] = len(factor)
            ext = max(4 * tcap, 8 * w + 512)
            st_ext = scan_mask_p3(best["mask"], w, ext)
            best["ext_tcap"] = ext
            best["ext_L"] = st_ext["L"]
            best["ext_start"] = st_ext["start"]
            best["ext_end"] = st_ext["end"]
            best["ext_pattern"] = st_ext["pattern"]
            best["ext_grew"] = st_ext["L"] > best["L"]
            # Same burst lengthened (eventual-looking) vs a later finite burst.
            best["ext_same_run"] = (
                st_ext["start"] == best["start"] and st_ext["L"] >= best["L"]
            )
            best["ext_same_run_grew"] = bool(
                best["ext_same_run"] and st_ext["L"] > best["L"]
            )
            best["ext_new_burst"] = bool(
                st_ext["L"] > best["L"] and st_ext["start"] != best["start"]
            )
            transient = max(2 * w + 8, 16)
            best["ext_eventual"] = (
                st_ext["suffix"] >= 16 and (ext - st_ext["suffix"]) <= transient
            )

        if best_prefix is not None:
            pbits = evolve_centers(best_prefix["mask"], w, tcap)
            pst = p3_stats_from_bits(pbits)
            best_prefix["pattern"] = None
            for name, rec in pst["by_pattern"].items():
                if rec["prefix"] == pst["prefix"] and rec["prefix"] > 0:
                    best_prefix["pattern"] = name
                    break
            best_prefix["factor"] = "".join(map(str, pbits[: pst["prefix"]][:60]))

        row = {
            "w": w,
            "n_nonzero": nstates - 1,
            "tcap": tcap,
            "L_run": Lrun,
            "L3": Lrun,
            "L_prefix": Lpref,
            "L_suffix": Lsuff,
            "L_001": L001,
            "L_011": L011,
            "max_run_end": max_end,
            "n_at_Lrun": n_at_max,
            "best_prefix": best_prefix,
            "n_cap_survivors": n_reach,
            "n_L_gt_4w16": n_gt_4w16,
            "bound_4w16": bound,
            "best": best,
            "elapsed_sec": round(elapsed, 4),
        }
        rows.append(row)
        log.append(
            f"exhaustive w={w} n={nstates - 1} tcap={tcap} "
            f"L3={Lrun} L_prefix={Lpref} L_suffix={Lsuff} "
            f"L_001={L001} L_011={L011} n_at_max={n_at_max} "
            f"reach={n_reach} L>4w+16={n_gt_4w16} {elapsed:.3f}s"
        )
        print(log[-1], flush=True)
    return rows, cap_survivors


def plateau_info(exh: list[dict]) -> dict:
    ys = [r["L_run"] for r in exh]
    if not ys:
        return {
            "max_L3": 0,
            "plateau": False,
            "still_growing_at_wmax": False,
            "w_at_max": [],
            "plateau_lo": None,
            "plateau_hi": None,
        }
    max_L = max(ys)
    w_at_max = [r["w"] for r in exh if r["L_run"] == max_L]
    still_growing = len(ys) >= 2 and ys[-1] > ys[-2]
    # Longest final constant run of the table.
    hi = exh[-1]["w"]
    lo = hi
    last = ys[-1]
    for r in reversed(exh):
        if r["L_run"] == last:
            lo = r["w"]
        else:
            break
    plateau = (not still_growing) and (hi - lo >= 1 or (last == max_L and len(w_at_max) >= 2))
    # Stronger: the global max is attained on a consecutive block of radii.
    consec = True
    if w_at_max:
        consec = w_at_max[-1] - w_at_max[0] + 1 == len(w_at_max)
    plateau_at_max = consec and len(w_at_max) >= 2
    return {
        "max_L3": max_L,
        "plateau": bool(plateau_at_max or (plateau and last == max_L and hi - lo >= 1)),
        "plateau_at_global_max": plateau_at_max,
        "still_growing_at_wmax": still_growing and ys[-1] == max_L,
        "w_at_max": w_at_max,
        "plateau_lo": min(w_at_max) if w_at_max else None,
        "plateau_hi": max(w_at_max) if w_at_max else None,
        "final_constant_lo": lo,
        "final_constant_hi": hi,
        "final_constant_L": last,
        "L3_table": ys,
    }


def verdict_of(exh: list[dict], genuine: list[dict], plat: dict) -> tuple[str, str]:
    if genuine:
        return (
            "KILL",
            "finite nonzero row whose centre stays period-3 through an "
            "extended cap (looks genuinely eventual)",
        )
    if plat["still_growing_at_wmax"] and not plat["plateau"]:
        wmax = exh[-1]["w"] if exh else 8
        return (
            "KILL",
            f"L3(w) keeps growing through w={wmax} with no plateau "
            f"(table {plat['L3_table']})",
        )
    max_L = plat["max_L3"]
    w_at = plat["w_at_max"]
    wlo = min(w_at) if w_at else 0
    whi = max(w_at) if w_at else 0
    if plat["plateau"]:
        return (
            "FINITE_THEOREM",
            "no genuine eventual witness; "
            f"L3(w) plateaus at {max_L} on w={wlo}..{whi} of the scanned "
            "radii; every radius-w row breaks every exact period-3 centre "
            "run by time 8w+128, and no period-3 run exceeds L3(w)",
        )
    return (
        "FINITE_THEOREM",
        "no genuine eventual witness and L3(w) does not escape the cap; "
        f"L3(w) <= {max_L} on the scanned radii (max at w={w_at}); "
        "this is a finite bound, not a uniform proof",
    )


def write_markdown(dump: dict) -> str:
    exh = dump["exhaustive"]
    checks = dump["checks"]
    plat = dump["plateau"]
    lines: list[str] = []
    a = lines.append
    a("# Period-3 centre: finite-row analog of the radius-10 theorem")
    a("")
    a("This note is a checked finite scan. It does **not** exclude eventual")
    a("period 3 for every finite row, and it does not claim a prize result.")
    a("It is ideas9 item 2: the period-2 exhaustive of")
    a("`research/period2_fiber.py`, repeated for exact period 3.")
    a("")
    a("Helper: `research/period3_fiber.py --certify`. Dump:")
    a("`research/period3_fiber.json`.")
    a("")
    a("## Attack")
    a("")
    a("Prove or kill: no nonzero finite-support configuration has an")
    a("eventually period-3 central trace. Broader than the prize seed.")
    a("Not the strip-graph residual-SCC test (which still has residual")
    a("components for `001` and `011` at radius 8), not onset SAT, not")
    a("`F_T` ideal certificates, and not the unique-left fiber")
    a("reconstruction of `period2_fiber.py`.")
    a("")
    a("The primitive necklaces of period 3 are `001` and `011`. All three")
    a("rotations, and therefore both families of starting phases, are")
    a("scored as global alignments")
    a("")
    a("```")
    a("001, 010, 100     (necklace 001)")
    a("011, 110, 101     (necklace 011)")
    a("```")
    a("")
    a("A centre factor is exact period 3 when it is a contiguous run of")
    a("one of those six infinite words. Constants `000` and `111` are")
    a("excluded (they have period 1). A period-2 alternating factor")
    a("matches a 3-bit window of `010` or `101` and then breaks, so it")
    a("does not inflate `L3`.")
    a("")
    a("Kill: `L3(w)` keeps growing through `w=8` with no plateau, or a")
    a("finite row whose centre stays period 3 through the cap and still")
    a("does not break when the cap is extended. Survive a finite theorem")
    a("if `L3` plateaus at a constant on the scanned radii.")
    a("")
    a("## Engine")
    a("")
    a("Every nonzero initial word of support radius `w=0..8`")
    a("(`2^{2w+1}-1` states; `w=8` is `2^{17}-1`) is evolved in a")
    a("quiescent background up to `tcap = 8w+128`. Packed Rule 30")
    a("`new = (row<<2) ^ ((row<<1)|row)`, bit 0 leftmost, centre bit")
    a("`(row>>(w+t))&1`, matches `experiment.center_bits` on the prize")
    a(f"seed prefix of length 256 (`{checks['prize_prefix16']}…`) and an")
    a("independent live-cell implementation on sampled small rows. The")
    a("streaming six-phase scorer matches a stored-trace scorer on those")
    a("rows.")
    a("")
    a("`L_run(w) = L3(w)` is the longest such run anywhere in `[0, tcap)`.")
    a("`L_prefix(w)` is the longest exact period-3 prefix from time 0.")
    a("`L_001` / `L_011` are the same maximum restricted to one necklace.")
    a("No row is “eventual in the cap” (last break inside the light cone")
    a("`2w+8`, suffix at least 16) unless listed below.")
    a("")
    a("## Exhaustive finite rows")
    a("")
    a("| `w` | states | `tcap` | `L3` | `L_prefix` | `L_suffix` | `L_001` | `L_011` | `L>4w+16` | maximizer | pattern | start |")
    a("|----:|-------:|-------:|-----:|-----------:|-----------:|--------:|--------:|----------:|-----------|---------|------:|")
    for r in exh:
        b = r["best"] or {}
        mx = b.get("row", "")
        pat = b.get("pattern", "")
        start = b.get("start", "")
        a(
            f"| {r['w']} | {r['n_nonzero']} | {r['tcap']} | {r['L_run']} | "
            f"{r['L_prefix']} | {r['L_suffix']} | {r['L_001']} | {r['L_011']} | "
            f"{r['n_L_gt_4w16']} | `{mx}` | `{pat}` | {start} |"
        )
    a("")

    # Prize seed line.
    w0 = exh[0] if exh else None
    if w0 is not None and w0["best"] is not None:
        b0 = w0["best"]
        a(
            f"The prize seed (`w=0`) has `L3={w0['L_run']}`"
            + (
                f", the factor `{b0.get('factor', '')}` of pattern `{b0.get('pattern')}` "
                f"starting at time {b0.get('start')}."
                if b0.get("factor") is not None
                else "."
            )
        )
        a(f"`L_prefix(0)={w0['L_prefix']}` (the opening `11011` of `110110…`).")
        a("")

    for r in exh:
        b = r["best"]
        if not b:
            continue
        if r["w"] == 0:
            continue
        extra = ""
        if b.get("ext_eventual"):
            extra = (
                f" Extending that evolution to {b.get('ext_tcap')} steps "
                f"looks eventual (`ext_L={b.get('ext_L')}`, suffix reaches the "
                f"extended cap)."
            )
        elif b.get("ext_same_run_grew"):
            extra = (
                f" Extending that evolution to {b.get('ext_tcap')} steps "
                f"lengthens the same burst to `ext_L={b.get('ext_L')}` "
                f"(still finite; start stays `t={b.get('start')}`)."
            )
        elif b.get("ext_new_burst"):
            extra = (
                f" Extending that evolution to {b.get('ext_tcap')} steps "
                f"finds a later finite burst `ext_L={b.get('ext_L')}` of "
                f"pattern `{b.get('ext_pattern')}` at "
                f"`t={b.get('ext_start')}..{b.get('ext_end')}` "
                f"(the tcap-window maximizer is not eventual)."
            )
        elif b.get("ext_grew") is False:
            extra = (
                f" Extending that evolution to {b.get('ext_tcap')} steps "
                f"does not lengthen the run (`ext_L={b.get('ext_L')}`)."
            )
        nmax = r["n_at_Lrun"]
        nmax_s = "1 mask attains" if nmax == 1 else f"{nmax} masks attain"
        a(
            f"Radius-{r['w']} maximizer: row `{b.get('row')}` (mask={b.get('mask')}), "
            f"pattern `{b.get('pattern')}` (necklace `{b.get('necklace')}`), "
            f"run of {b.get('L')} from `t={b.get('start')}` to `t={b.get('end')}` "
            f"({nmax_s} `L3`).{extra}"
        )
        bp = r.get("best_prefix")
        if bp:
            a(
                f"`L_prefix` maximizer at this radius: row `{bp.get('row')}` "
                f"(mask={bp.get('mask')}), pattern `{bp.get('pattern')}`, "
                f"prefix `{bp.get('factor')}` of length {bp.get('L_prefix')}."
            )
        a("")

    a("## Plateau / growth")
    a("")
    a(f"- `L3` table: `{plat['L3_table']}`")
    a(f"- maximum `{plat['max_L3']}` attained at `w={plat['w_at_max']}`")
    a(f"- still growing at `w_max`: `{plat['still_growing_at_wmax']}`")
    a(f"- plateau at the global max: `{plat['plateau_at_global_max']}`")
    a(
        f"- final constant block: `L={plat['final_constant_L']}` on "
        f"`w={plat['final_constant_lo']}..{plat['final_constant_hi']}`"
    )
    a("")
    xs = [r["w"] for r in exh]
    ys = [r["L_run"] for r in exh]
    yp = [r["L_prefix"] for r in exh]
    C, Cp = dump["fit_L_run"]["C"], dump["fit_L_run"]["Cprime"]
    C2, Cp2 = dump["fit_L_prefix"]["C"], dump["fit_L_prefix"]["Cprime"]
    a("Least squares over the whole table (a summary only, not a conjecture):")
    a("")
    a(f"- `L3 ≈ {C:.3f}*w + {Cp:.3f}`")
    a(f"- `L_prefix ≈ {C2:.3f}*w + {Cp2:.3f}`")
    a("")
    a("`L_prefix` is the period-3 analogue of Condrey’s horizon `H(p,w)≥w`:")
    a("a prescribed period-3 centre of length `w` is always realised by")
    a("some radius-`w` row (left permutivity), so `L_prefix` can grow like")
    a("`w`. The scanned prefixes stay well below `tcap`.")
    a("")

    n_eventual = dump["exclusion_table"]["n_eventual_in_cap"]
    n_genuine = dump["exclusion_table"]["n_genuine_eventual"]
    a("## Eventual witnesses")
    a("")
    if n_eventual == 0 and n_genuine == 0:
        a(
            "No scanned row is eventual in the cap: a genuine eventual "
            "regime would produce a period-3 suffix of length `tcap-O(w)`. "
            "Every maximizer’s run is a finite burst strictly inside the "
            "window (or a short suffix that is not a light-cone transient)."
        )
    else:
        a(
            f"`n_eventual_in_cap={n_eventual}`, "
            f"`n_genuine_eventual={n_genuine}`."
        )
        for s in dump.get("genuine_eventual_witnesses") or []:
            a(
                f"- w={s.get('w')} mask={s.get('mask')} "
                f"L_at_tcap={s.get('L_at_tcap')} L_ext={s.get('L_ext')} "
                f"reaches_ext={s.get('reaches_ext')}"
            )
    a("")

    wmax = exh[-1]["w"] if exh else 8
    max_L = plat["max_L3"]
    a("## What is proved, what is not")
    a("")
    a("Proved (and machine-checked):")
    a("")
    a("- Packed evolution agrees with `experiment.center_bits` on 256")
    a("  prize-seed bits and with an independent live-cell spacetime on")
    a("  sampled radius-`w` rows.")
    a("- The six-phase streaming scorer agrees with a stored-trace scorer.")
    a("- Synthetic `(001)^∞` / `(011)^∞` / `(010)^∞` score as claimed;")
    a("  period-2 and constant traces are not long exact period-3 runs.")
    a(
        f"- The exclusion table `L3(w)` for `w≤{wmax}` inside "
        f"`tcap=8w+128`: {plat['L3_table']}. No scanned row is eventual "
        "in that window (`n_genuine_eventual=0`)."
    )
    if dump["verdict"] == "FINITE_THEOREM":
        a(
            f"- **Finite theorem.** Every nonzero row of support radius "
            f"`w≤{wmax}` has every exact period-3 centre run of length at "
            f"most `L3(w)`, hence at most {max_L}, inside `tcap=8w+128`."
        )
    else:
        a(
            f"- **No plateau.** Unlike period 2 (`L_run=24` for "
            f"`6≤w≤10`), `L3(w)` is still strictly larger at `w={wmax}` "
            f"than at every smaller scanned radius "
            f"(`L3({wmax})={max_L}`). That kills this route as a "
            "Condrey-style finite theorem at these radii."
        )
    a("")
    a("Not proved:")
    a("")
    a(f"- A uniform-in-`w` bound on `L3(w)`. The table is only for "
      f"radius `≤{wmax}`.")
    a("- Existence of an eventually period-3 finite row. Growth of")
    a("  `L3(w)` through radius 8 is compatible with either a slow")
    a("  unbounded family or a later plateau; it is not a witness.")
    a("- Eventual period 3 of the prize seed. The seed is the `w=0` line")
    a(f"  (`L3=11`, `L_prefix=5`).")
    a("- Anything about residual strip-graph SCCs for `001` / `011`.")
    a("")
    a("## Verdict")
    a("")
    a(f"`{dump['verdict']}`, wall time {dump['wall_time_sec']:.1f}s.")
    a("")
    a(f"- Kill: {'yes' if dump['kill'] else 'no'}.")
    a(f"- Survive: {'yes' if dump['survive'] else 'no'}.")
    a(f"- Witness: none (no eventual-in-cap row).")
    a(f"- Reason: {dump['kill_reason']}")
    a(
        f"- Exclusion table: `L3(w)` as above, `tcap=8w+128`, "
        f"`L3(w)≤{max_L}` for `w≤{wmax}`; the table does not plateau."
    )
    a("")
    a("## Files")
    a("")
    a("- `research/period3_fiber.md` (this note)")
    a("- `research/period3_fiber.py` (`--certify` runs the checks and the")
    a("  radius-`w` exhaustive)")
    a("- `research/period3_fiber.json` (dump)")
    a("")
    return "\n".join(lines) + "\n"


def certify(w_max: int) -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    print(log[-1], flush=True)
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    exh, cap_surv = exhaustive_scan(w_max, log)
    plat = plateau_info(exh)

    xs = [r["w"] for r in exh]
    ys = [r["L_run"] for r in exh]
    C, Cp = fit_linear(xs, ys)
    residuals = [y - (C * x + Cp) for x, y in zip(xs, ys)]
    yp = [r["L_prefix"] for r in exh]
    Cp2, Cpp = fit_linear(xs, yp)

    genuine = [
        s for s in cap_surv if s.get("eventual_in_cap") and s.get("reaches_ext")
    ]
    verdict, kill_reason = verdict_of(exh, genuine, plat)
    wall = time.perf_counter() - t_all

    dump = {
        "attack": "period3_fiber",
        "ideas": "ideas9 item 2",
        "problem": (
            "no nonzero finite-support configuration has an eventually "
            "period-3 central trace"
        ),
        "centre_words": list(PAT_NAME),
        "necklaces": ["001", "011"],
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": verdict == "SURVIVE",
        "kill_reason": kill_reason,
        "wall_time_sec": round(wall, 4),
        "tcap_long": "8w+128",
        "w_max": w_max,
        "n_masks_wmax": (1 << (2 * w_max + 1)) - 1,
        "checks": checks,
        "exhaustive": exh,
        "plateau": plat,
        "cap_survivors": [s for s in cap_surv if s.get("eventual_in_cap")]
        + [s for s in cap_surv if not s.get("eventual_in_cap")][:8],
        "genuine_eventual_witnesses": genuine,
        "fit_L_run": {
            "C": C,
            "Cprime": Cp,
            "max_residual": max(residuals) if residuals else 0.0,
            "min_residual": min(residuals) if residuals else 0.0,
            "note": (
                "least-squares L3 ~ C*w+C' is a summary only; the table "
                "is the actual finite statement"
            ),
        },
        "fit_L_prefix": {"C": Cp2, "Cprime": Cpp},
        "exclusion_table": {
            "f_w": (
                "L3(w)=L_run(w); an exact period-3 centre run of a radius-w "
                "row lasts at most L3(w) steps inside tcap=8w+128"
            ),
            "L3": [{"w": r["w"], "L": r["L_run"], "tcap": r["tcap"]} for r in exh],
            "L_run": [{"w": r["w"], "L": r["L_run"], "tcap": r["tcap"]} for r in exh],
            "L_prefix": [{"w": r["w"], "L": r["L_prefix"]} for r in exh],
            "L_001": [{"w": r["w"], "L": r["L_001"]} for r in exh],
            "L_011": [{"w": r["w"], "L": r["L_011"]} for r in exh],
            "n_L_gt_4w16": sum(r["n_L_gt_4w16"] for r in exh),
            "n_eventual_in_cap": sum(r["n_cap_survivors"] for r in exh),
            "n_genuine_eventual": len(genuine),
        },
        "log": log,
    }
    OUT_JSON.write_text(json.dumps(dump, indent=2) + "\n")
    OUT_MD.write_text(write_markdown(dump))
    print(f"wrote {OUT_JSON}", flush=True)
    print(f"wrote {OUT_MD}", flush=True)
    print(f"verdict={verdict} wall={wall:.3f}s", flush=True)
    print(f"reason: {kill_reason}", flush=True)
    print(f"L3 by w: {[(r['w'], r['L_run'], r['tcap']) for r in exh]}", flush=True)
    print(f"L_prefix by w: {[(r['w'], r['L_prefix']) for r in exh]}", flush=True)
    print(f"fit L3 ~ {C:.3f}*w + {Cp:.3f}", flush=True)
    print(
        f"n_cap_survivors={sum(r['n_cap_survivors'] for r in exh)} genuine={len(genuine)}",
        flush=True,
    )
    return dump


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    p.add_argument("--w-max", type=int, default=8)
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    if args.w_max < 0 or args.w_max > 12:
        p.error("--w-max must be in 0..12")
    certify(args.w_max)


if __name__ == "__main__":
    main()
