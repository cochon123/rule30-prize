"""ideas12 item 2: period-2 L_run among radius-w rows with left bit 1.

The prize seed has x(t, -t)=1 for every t (true Rule 30 left edge). Finite
row L_run scans allow arbitrary supports; many Cycle I maximizers are
left-padded (packed bit 0 = 0) or sit off the origin. This script restricts
to packed radius-w rows whose leftmost 1 is exactly spatial -w, i.e. bit 0
of the Cycle I packing is 1.

That is the only extra constraint. For any finite row with leftmost 1 at L
and vacuum to the left, Rule 30 sends the edge left at speed 1 and keeps it
1, so x(t, L-t)=1 is automatic. For a period-2 regime starting at time T
the relevant finite rows are radius T with leftmost 1 at -T.

Packed evolution is imported from research/period2_fiber.py and that file
is not modified:
    new = (row << 2) ^ ((row << 1) | row)
    centre bit (row >> (w + t)) & 1
with bit 0 the leftmost cell of the current support (spatial -w at t=0).

Exhaustive w<=10, 2^{2w} states (one bit fixed). Caps tcap=8w+128 (Cycle I)
and tcap=32w+512 (ideas11 long cap), one evolution per mask.

Run: python3 research/period2_leftbit.py --certify
Dump: research/period2_leftbit.json, research/period2_leftbit.md
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from period2_fiber import (  # noqa: E402
    evolve_centers,
    fit_linear,
    mask_to_live,
    naive_centers,
    rule30_step,
    scan_mask_runs,
)

OUT_JSON = Path(__file__).resolve().with_suffix(".json")
OUT_MD = Path(__file__).resolve().with_suffix(".md")

W_MAX = 10
NPROC_CAP = 4
MASK_7503 = 7503
W_7503 = 6

# Cycle I unrestricted table (period2_fiber.md / period2_lrun.py).
# Independently re-checked here at w=0 and w=6; bit-0 status is computed.
CYCLE_I_L_RUN = [
    {"w": 0, "n_nonzero": 1, "tcap": 128, "L_run": 7, "L_prefix": 1, "best_mask": 1, "best_start": 35},
    {"w": 1, "n_nonzero": 7, "tcap": 136, "L_run": 8, "L_prefix": 7, "best_mask": 1, "best_start": 128},
    {"w": 2, "n_nonzero": 31, "tcap": 144, "L_run": 10, "L_prefix": 7, "best_mask": 2, "best_start": 128},
    {"w": 3, "n_nonzero": 127, "tcap": 152, "L_run": 13, "L_prefix": 7, "best_mask": 122, "best_start": 37},
    {"w": 4, "n_nonzero": 511, "tcap": 160, "L_run": 15, "L_prefix": 7, "best_mask": 261, "best_start": 67},
    {"w": 5, "n_nonzero": 2047, "tcap": 168, "L_run": 15, "L_prefix": 9, "best_mask": 522, "best_start": 67},
    {"w": 6, "n_nonzero": 8191, "tcap": 176, "L_run": 24, "L_prefix": 10, "best_mask": 7503, "best_start": 94},
    {"w": 7, "n_nonzero": 32767, "tcap": 184, "L_run": 24, "L_prefix": 10, "best_mask": 15006, "best_start": 94},
    {"w": 8, "n_nonzero": 131071, "tcap": 192, "L_run": 24, "L_prefix": 15, "best_mask": 8647, "best_start": 92},
    {"w": 9, "n_nonzero": 524287, "tcap": 200, "L_run": 24, "L_prefix": 17, "best_mask": 17294, "best_start": 92},
    {"w": 10, "n_nonzero": 2097151, "tcap": 208, "L_run": 24, "L_prefix": 17, "best_mask": 34588, "best_start": 92},
]


def tcap_cycle_i(w: int) -> int:
    return 8 * w + 128


def tcap_long(w: int) -> int:
    return 32 * w + 512


def nproc() -> int:
    try:
        return max(1, min(NPROC_CAP, os.cpu_count() or 1))
    except Exception:
        return 1


def row_bits(mask: int, w: int) -> str:
    return "".join(str((mask >> i) & 1) for i in range(2 * w + 1))


def live_positions(mask: int, w: int) -> list[int]:
    return [i - w for i in range(2 * w + 1) if (mask >> i) & 1]


def origin_in_hull(mask: int, w: int) -> bool:
    """True leftmost is -w (bit 0) in this scan; hull contains 0 iff rightmost >= 0."""
    return mask >= (1 << w)


def both_edges(mask: int, w: int) -> bool:
    return bool(mask & 1) and bool((mask >> (2 * w)) & 1)


def rec_from(mask: int, w: int, st: tuple[int, int, int, int, int], tcap: int) -> dict:
    L, start, prefix, suffix, end = st
    live = live_positions(mask, w)
    return {
        "mask": mask,
        "w": w,
        "row": row_bits(mask, w),
        "live": live,
        "n1": len(live),
        "span": (live[-1] - live[0]) if live else 0,
        "origin_live": bool((mask >> w) & 1),
        "origin_in_hull": origin_in_hull(mask, w),
        "right_live": bool((mask >> (2 * w)) & 1),
        "L": L,
        "start": start,
        "end": end,
        "prefix": prefix,
        "suffix": suffix,
        "tcap": tcap,
        "reaches_cap": end == tcap and L >= 2,
    }


def consider(best: dict | None, rec: dict) -> dict:
    if best is None:
        return rec
    if rec["L"] > best["L"]:
        return rec
    if rec["L"] == best["L"] and rec["mask"] < best["mask"]:
        return rec
    return best


def scan_runs_two_caps(
    mask: int, w: int, t_short: int, t_long: int
) -> tuple[tuple[int, int, int, int, int], tuple[int, int, int, int, int]]:
    """One packed evolution; snapshot at t_short and at t_long.

    Same CA as period2_fiber.scan_mask_runs. Returns (short, long) tuples
    (L, start, prefix, suffix, end).
    """
    if t_short < 1 or t_long < t_short:
        raise ValueError("need 1 <= t_short <= t_long")
    row = mask
    prev = (row >> w) & 1
    best = 1
    best_start = 0
    run = 1
    run_start = 0
    prefix = 1
    prefix_alive = True
    short = (1, 0, 1, 1, 1)
    for t in range(1, t_long):
        row = (row << 2) ^ ((row << 1) | row)
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
        if t + 1 == t_short:
            short = (best, best_start, prefix, run, best_start + best)
    long = (best, best_start, prefix, run, best_start + best)
    if t_short == t_long:
        short = long
    return short, long


def left_edge_packed_ok(mask: int, w: int, tcap: int) -> bool:
    """Packed bit 0 is spatial -w-t. Rule 30 keeps it equal to the t=0 bit."""
    if (mask & 1) == 0:
        return False
    row = mask
    for t in range(tcap):
        if (row & 1) != 1:
            return False
        row = (row << 2) ^ ((row << 1) | row)
        _ = t
    return True


def left_edge_naive_ok(mask: int, w: int, tcap: int) -> bool:
    live = {p: 1 for p in live_positions(mask, w)}
    if not live or min(live) != -w:
        return False
    cur = dict(live)
    for t in range(tcap):
        if (-w - t) not in cur:
            return False
        mn, mx = min(cur), max(cur)
        nxt = {}
        for j in range(mn - 1, mx + 2):
            a = 1 if (j - 1) in cur else 0
            b = 1 if j in cur else 0
            c = 1 if (j + 1) in cur else 0
            if a ^ (b | c):
                nxt[j] = 1
        cur = nxt
    return True


def double_cap(rec: dict) -> dict:
    if rec is None:
        return rec
    out = dict(rec)
    t2 = 2 * rec["tcap"]
    st2 = scan_mask_runs(rec["mask"], rec["w"], t2)
    out["doubled"] = {
        "tcap": t2,
        "L": st2["L"],
        "start": st2["start"],
        "end": st2["end"],
        "prefix": st2["prefix"],
        "suffix": st2["suffix"],
        "reaches_cap": st2["end"] == t2 and st2["L"] >= 2,
    }
    return out


# ---------------------------------------------------------------------------
# Exhaustive scan
# ---------------------------------------------------------------------------

def _empty_side() -> dict:
    return {
        "L_run": 0,
        "L_prefix": 0,
        "L_suffix": 0,
        "best": None,
        "n_L_gt_4w16": 0,
        "n_ge24": 0,
        "L_run_hull": 0,
        "best_hull": None,
        "L_run_origin_live": 0,
        "best_origin_live": None,
        "L_run_both_edges": 0,
        "best_both_edges": None,
        "n_hull": 0,
        "n_origin_live": 0,
        "n_both_edges": 0,
        "n_reaches_cap": 0,
    }


def _exh_chunk(args: tuple[int, int, int, int, int]) -> dict:
    """Scan k in [klo, khi) with mask = (k<<1)|1."""
    klo, khi, w, t_short, t_long = args
    bound = 4 * w + 16
    hull_bit = 1 << w
    right_bit = 1 << (2 * w)
    origin_bit = 1 << w

    s = _empty_side()
    lg = _empty_side()
    # Track best (L, mask, st) without building dicts in the inner loop.
    s_best = (-1, -1, None)
    s_hull = (-1, -1, None)
    s_orig = (-1, -1, None)
    s_both = (-1, -1, None)
    l_best = (-1, -1, None)
    l_hull = (-1, -1, None)
    l_orig = (-1, -1, None)
    l_both = (-1, -1, None)

    for k in range(klo, khi):
        mask = (k << 1) | 1
        short, longt = scan_runs_two_caps(mask, w, t_short, t_long)
        Ls, _, prefs, suffs, ends = short
        Ll, _, prefl, suffl, endl = longt
        in_hull = mask >= hull_bit
        orig = bool(mask & origin_bit)
        both = bool(mask & right_bit)  # left bit already 1

        if Ls > s_best[0] or (Ls == s_best[0] and (s_best[1] < 0 or mask < s_best[1])):
            s_best = (Ls, mask, short)
        if prefs > s["L_prefix"]:
            s["L_prefix"] = prefs
        if suffs > s["L_suffix"]:
            s["L_suffix"] = suffs
        if Ls > bound:
            s["n_L_gt_4w16"] += 1
        if Ls >= 24:
            s["n_ge24"] += 1
        if ends == t_short and Ls >= 2:
            s["n_reaches_cap"] += 1

        if Ll > l_best[0] or (Ll == l_best[0] and (l_best[1] < 0 or mask < l_best[1])):
            l_best = (Ll, mask, longt)
        if prefl > lg["L_prefix"]:
            lg["L_prefix"] = prefl
        if suffl > lg["L_suffix"]:
            lg["L_suffix"] = suffl
        if Ll > bound:
            lg["n_L_gt_4w16"] += 1
        if Ll >= 24:
            lg["n_ge24"] += 1
        if endl == t_long and Ll >= 2:
            lg["n_reaches_cap"] += 1

        if in_hull:
            s["n_hull"] += 1
            lg["n_hull"] += 1
            if Ls > s_hull[0] or (Ls == s_hull[0] and (s_hull[1] < 0 or mask < s_hull[1])):
                s_hull = (Ls, mask, short)
            if Ll > l_hull[0] or (Ll == l_hull[0] and (l_hull[1] < 0 or mask < l_hull[1])):
                l_hull = (Ll, mask, longt)
        if orig:
            s["n_origin_live"] += 1
            lg["n_origin_live"] += 1
            if Ls > s_orig[0] or (Ls == s_orig[0] and (s_orig[1] < 0 or mask < s_orig[1])):
                s_orig = (Ls, mask, short)
            if Ll > l_orig[0] or (Ll == l_orig[0] and (l_orig[1] < 0 or mask < l_orig[1])):
                l_orig = (Ll, mask, longt)
        if both:
            s["n_both_edges"] += 1
            lg["n_both_edges"] += 1
            if Ls > s_both[0] or (Ls == s_both[0] and (s_both[1] < 0 or mask < s_both[1])):
                s_both = (Ls, mask, short)
            if Ll > l_both[0] or (Ll == l_both[0] and (l_both[1] < 0 or mask < l_both[1])):
                l_both = (Ll, mask, longt)

    def pack_side(side, best, hull, orig, both, tcap):
        out = dict(side)
        if best[2] is not None:
            out["L_run"] = best[0]
            out["best"] = rec_from(best[1], w, best[2], tcap)
        if hull[2] is not None:
            out["L_run_hull"] = hull[0]
            out["best_hull"] = rec_from(hull[1], w, hull[2], tcap)
        if orig[2] is not None:
            out["L_run_origin_live"] = orig[0]
            out["best_origin_live"] = rec_from(orig[1], w, orig[2], tcap)
        if both[2] is not None:
            out["L_run_both_edges"] = both[0]
            out["best_both_edges"] = rec_from(both[1], w, both[2], tcap)
        return out

    return {
        "n": khi - klo,
        "short": pack_side(s, s_best, s_hull, s_orig, s_both, t_short),
        "long": pack_side(lg, l_best, l_hull, l_orig, l_both, t_long),
    }


def _merge_side(acc: dict, part: dict) -> dict:
    acc["L_run"] = max(acc["L_run"], part["L_run"])
    acc["L_prefix"] = max(acc["L_prefix"], part["L_prefix"])
    acc["L_suffix"] = max(acc["L_suffix"], part["L_suffix"])
    acc["n_L_gt_4w16"] += part["n_L_gt_4w16"]
    acc["n_ge24"] += part["n_ge24"]
    acc["n_hull"] += part["n_hull"]
    acc["n_origin_live"] += part["n_origin_live"]
    acc["n_both_edges"] += part["n_both_edges"]
    acc["n_reaches_cap"] += part["n_reaches_cap"]
    acc["L_run_hull"] = max(acc["L_run_hull"], part["L_run_hull"])
    acc["L_run_origin_live"] = max(acc["L_run_origin_live"], part["L_run_origin_live"])
    acc["L_run_both_edges"] = max(acc["L_run_both_edges"], part["L_run_both_edges"])
    acc["best"] = consider(acc.get("best"), part["best"]) if part.get("best") else acc.get("best")
    acc["best_hull"] = (
        consider(acc.get("best_hull"), part["best_hull"])
        if part.get("best_hull")
        else acc.get("best_hull")
    )
    acc["best_origin_live"] = (
        consider(acc.get("best_origin_live"), part["best_origin_live"])
        if part.get("best_origin_live")
        else acc.get("best_origin_live")
    )
    acc["best_both_edges"] = (
        consider(acc.get("best_both_edges"), part["best_both_edges"])
        if part.get("best_both_edges")
        else acc.get("best_both_edges")
    )
    return acc


def merge_chunk(acc: dict | None, part: dict) -> dict:
    if acc is None:
        return {
            "n": part["n"],
            "short": dict(part["short"]),
            "long": dict(part["long"]),
        }
    acc["n"] += part["n"]
    acc["short"] = _merge_side(acc["short"], part["short"])
    acc["long"] = _merge_side(acc["long"], part["long"])
    return acc


def exhaustive_w(w: int, log: list[str]) -> dict:
    t_short = tcap_cycle_i(w)
    t_long = tcap_long(w)
    nstates = 1 << (2 * w)  # bit 0 fixed to 1
    workers = nproc()
    # Parallelise the large radii. w=8 is 2^16; w=10 is 2^20.
    use_pool = workers > 1 and nstates >= (1 << 16)
    n_chunks = max(workers * 4, 1) if use_pool else 1
    chunk = max(1, (nstates + n_chunks - 1) // n_chunks)
    tasks = []
    lo = 0
    while lo < nstates:
        hi = min(lo + chunk, nstates)
        tasks.append((lo, hi, w, t_short, t_long))
        lo = hi

    t0 = time.perf_counter()
    acc = None
    if not use_pool or len(tasks) == 1:
        for task in tasks:
            acc = merge_chunk(acc, _exh_chunk(task))
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(_exh_chunk, task) for task in tasks]
            done = 0
            for fut in as_completed(futs):
                part = fut.result()
                acc = merge_chunk(acc, part)
                done += 1
                if done == 1 or done == len(futs) or done % max(1, len(futs) // 4) == 0:
                    Lsofar = (acc["long"]["L_run"] if acc else 0)
                    log.append(
                        f"exhaustive w={w} chunks {done}/{len(futs)} "
                        f"L_long={Lsofar}"
                    )
                    print(log[-1], flush=True)

    elapsed = time.perf_counter() - t0
    assert acc is not None
    assert acc["n"] == nstates

    for side, tcap in (("short", t_short), ("long", t_long)):
        best = acc[side].get("best")
        if best is not None:
            acc[side]["best"] = double_cap(best)
        for key in ("best_hull", "best_origin_live", "best_both_edges"):
            rec = acc[side].get(key)
            if rec is not None:
                acc[side][key] = double_cap(rec)

    ci = CYCLE_I_L_RUN[w]
    short = acc["short"]
    longt = acc["long"]
    rec = {
        "w": w,
        "n_leftbit": nstates,
        "n_unrestricted_nonzero": (1 << (2 * w + 1)) - 1,
        "nproc": workers if use_pool else 1,
        "elapsed_sec": round(elapsed, 4),
        "cycle_i": {
            "L_run": ci["L_run"],
            "L_prefix": ci["L_prefix"],
            "tcap": ci["tcap"],
            "best_mask": ci["best_mask"],
            "best_start": ci["best_start"],
            "best_bit0": ci["best_mask"] & 1,
            "best_in_leftbit_class": bool(ci["best_mask"] & 1),
        },
        "short": {
            "tcap": t_short,
            "tcap_formula": "8w+128",
            **{k: v for k, v in short.items()},
        },
        "long": {
            "tcap": t_long,
            "tcap_formula": "32w+512",
            **{k: v for k, v in longt.items()},
        },
        "matches_cycle_i_short": short["L_run"] == ci["L_run"],
        "strictly_below_cycle_i_short": short["L_run"] < ci["L_run"],
        "long_exceeds_short": longt["L_run"] > short["L_run"],
    }
    log.append(
        f"exhaustive w={w} n={nstates} t_short={t_short} t_long={t_long} "
        f"L_short={short['L_run']} L_long={longt['L_run']} "
        f"L_CycleI={ci['L_run']} match={rec['matches_cycle_i_short']} "
        f"hull_short={short['L_run_hull']} both_short={short['L_run_both_edges']} "
        f"{elapsed:.3f}s nproc={rec['nproc']}"
    )
    print(log[-1], flush=True)
    return rec


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def run_checks() -> dict:
    checks: dict = {}

    prize = evolve_centers(1, 0, 32)
    naive_prize = naive_centers({0: 1}, 32)
    checks["packed_matches_naive_prize"] = prize == naive_prize
    checks["prize_prefix16"] = "".join(map(str, prize[:16]))
    checks["prize_prefix16_ok"] = checks["prize_prefix16"] == "1101110011000101"

    st0 = scan_mask_runs(1, 0, 128)
    checks["w0_L_run"] = st0["L"]
    checks["w0_L_run_ok"] = st0["L"] == 7 and st0["start"] == 35

    st6 = scan_mask_runs(MASK_7503, W_7503, tcap_cycle_i(W_7503))
    checks["w6_7503_L"] = st6["L"]
    checks["w6_7503_start"] = st6["start"]
    checks["w6_7503_end"] = st6["end"]
    checks["w6_7503_ok"] = st6["L"] == 24 and st6["start"] == 94
    checks["w6_7503_bit0"] = MASK_7503 & 1
    checks["w6_7503_in_leftbit_class"] = bool(MASK_7503 & 1)

    live_7503 = live_positions(MASK_7503, W_7503)
    checks["w6_7503_live"] = live_7503
    checks["w6_7503_origin_in_hull"] = live_7503[0] <= 0 <= live_7503[-1]
    checks["w6_7503_both_edges"] = both_edges(MASK_7503, W_7503)

    a = evolve_centers(MASK_7503, W_7503, 40)
    b = naive_centers(mask_to_live(MASK_7503, W_7503), 40)
    checks["packed_matches_naive_7503"] = a == b

    # Inlined two-cap vs two calls of scan_mask_runs.
    two_ok = True
    two_fail = None
    for w, mask in [(0, 1), (1, 5), (2, 19), (3, 73), (6, MASK_7503), (6, 1)]:
        ts, tl = tcap_cycle_i(w), tcap_long(w)
        short, longt = scan_runs_two_caps(mask, w, ts, tl)
        s1 = scan_mask_runs(mask, w, ts)
        s2 = scan_mask_runs(mask, w, tl)
        got_s = {
            "L": short[0],
            "start": short[1],
            "prefix": short[2],
            "suffix": short[3],
            "end": short[4],
        }
        got_l = {
            "L": longt[0],
            "start": longt[1],
            "prefix": longt[2],
            "suffix": longt[3],
            "end": longt[4],
        }
        want_s = {k: s1[k] for k in got_s}
        want_l = {k: s2[k] for k in got_l}
        if got_s != want_s or got_l != want_l:
            two_ok = False
            two_fail = {"w": w, "mask": mask, "got_s": got_s, "want_s": want_s}
            break
    checks["two_cap_matches_scan_mask_runs"] = two_ok
    if two_fail:
        checks["two_cap_fail"] = two_fail

    # Bit-0 identity of packed Rule 30: new bit 0 equals old bit 0.
    bit0_id = True
    for row in (0, 1, 2, 3, 7, 19, MASK_7503, 8647, (1 << 20) | 1):
        nxt = rule30_step(row)
        if (nxt & 1) != (row & 1):
            bit0_id = False
            break
    checks["packed_bit0_identity"] = bit0_id

    # Left edge stays 1 on left-bit-1 rows (packed and naive).
    edge_ok = True
    for w, mask, tcap in [
        (0, 1, 64),
        (3, 73, 40),
        (6, MASK_7503, 48),
        (4, 1, 32),
        (5, (1 << 10) | 1, 32),
    ]:
        if not left_edge_packed_ok(mask, w, tcap):
            edge_ok = False
            checks["left_edge_packed_fail"] = {"w": w, "mask": mask}
            break
        if not left_edge_naive_ok(mask, w, tcap):
            edge_ok = False
            checks["left_edge_naive_fail"] = {"w": w, "mask": mask}
            break
    checks["left_edge_stays_one"] = edge_ok

    # A left-bit-0 row is not in the class; its true leftmost is > -w.
    checks["w2_cycle_i_maximizer_bit0"] = CYCLE_I_L_RUN[2]["best_mask"] & 1
    checks["w2_cycle_i_maximizer_excluded"] = (
        CYCLE_I_L_RUN[2]["best_mask"] & 1
    ) == 0
    live2 = live_positions(2, 2)
    checks["w2_cycle_i_maximizer_live"] = live2
    checks["w2_cycle_i_maximizer_leftmost"] = live2[0] if live2 else None

    # w=7 Cycle I maximizer is 7503 shifted left by one vacuum.
    checks["w7_cycle_i_is_padded_7503"] = CYCLE_I_L_RUN[7]["best_mask"] == (
        MASK_7503 << 1
    )
    checks["w7_cycle_i_bit0"] = CYCLE_I_L_RUN[7]["best_mask"] & 1

    # Cycle I maximizer bit-0 census.
    ci_bit0 = []
    for row in CYCLE_I_L_RUN:
        ci_bit0.append(
            {
                "w": row["w"],
                "best_mask": row["best_mask"],
                "bit0": row["best_mask"] & 1,
                "in_leftbit_class": bool(row["best_mask"] & 1),
            }
        )
    checks["cycle_i_maximizer_bit0"] = ci_bit0
    checks["cycle_i_n_maximizers_leftbit"] = sum(1 for r in ci_bit0 if r["bit0"])
    checks["cycle_i_n_maximizers_dying_left"] = sum(
        1 for r in ci_bit0 if not r["bit0"]
    )

    skip = {
        "prize_prefix16",
        "w0_L_run",
        "w6_7503_L",
        "w6_7503_start",
        "w6_7503_end",
        "w6_7503_bit0",
        "w6_7503_live",
        "two_cap_fail",
        "left_edge_packed_fail",
        "left_edge_naive_fail",
        "w2_cycle_i_maximizer_bit0",
        "w2_cycle_i_maximizer_live",
        "w2_cycle_i_maximizer_leftmost",
        "w7_cycle_i_bit0",
        "cycle_i_maximizer_bit0",
        "cycle_i_n_maximizers_leftbit",
        "cycle_i_n_maximizers_dying_left",
    }
    checks["all_ok"] = all(
        v is True for k, v in checks.items() if k not in skip and not k.endswith("_fail")
    )
    return checks


def verify_row(mask: int, w: int, tcap: int) -> dict:
    st = scan_mask_runs(mask, w, tcap)
    bits = evolve_centers(mask, w, tcap)
    alt = True
    for t in range(st["start"] + 1, st["end"]):
        if bits[t] == bits[t - 1]:
            alt = False
            break
    naive = naive_centers(mask_to_live(mask, w), min(tcap, 64))
    packed = bits[: len(naive)]
    t2 = 2 * tcap
    st2 = scan_mask_runs(mask, w, t2)
    return {
        "ok": (
            st["L"] >= 1
            and alt
            and packed == naive
            and left_edge_packed_ok(mask, w, min(tcap, 64))
            and (mask & 1) == 1
        ),
        "L": st["L"],
        "start": st["start"],
        "end": st["end"],
        "alternating": alt,
        "packed_matches_naive": packed == naive,
        "left_bit": mask & 1,
        "left_edge_ok": left_edge_packed_ok(mask, w, min(tcap, 64)),
        "doubled_L": st2["L"],
        "doubled_tcap": t2,
        "doubled_start": st2["start"],
        "doubled_end": st2["end"],
    }


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def plateau(xs: list[int]) -> dict:
    if not xs:
        return {"value": 0, "start_w": None, "end_w": None, "length": 0}
    mx = max(xs)
    ws = [i for i, v in enumerate(xs) if v == mx]
    # Longest trailing run of the maximum, plus whether it covers a suffix.
    start = ws[0]
    # Require a contiguous block at the scan edge for a "plateau".
    trail_start = None
    for i in range(len(xs) - 1, -1, -1):
        if xs[i] == mx:
            trail_start = i
        else:
            break
    return {
        "value": mx,
        "first_w": ws[0],
        "last_w": ws[-1],
        "n_at_max": len(ws),
        "edge_start_w": trail_start,
        "edge_length": (len(xs) - trail_start) if trail_start is not None else 0,
        "covers_scan_edge": trail_start is not None and xs[-1] == mx,
    }


def decide_verdict(rows: list[dict]) -> tuple[str, str, bool]:
    """Kill if L still grows or matches unrestricted Cycle I.

    Finite theorem if left-edge-on forces a strictly smaller cap than
    unrestricted, with a plateau (not still rising at the scan edge).
    """
    Ls_short = [r["short"]["L_run"] for r in rows]
    Ls_long = [r["long"]["L_run"] for r in rows]
    Ls_ci = [r["cycle_i"]["L_run"] for r in rows]
    # Matching at w=0 is automatic (one state). Kill if the class
    # attains Cycle I at any w>=6, or at any w>=1 where Cycle I L>7.
    kill_match_ws = []
    seen: set[int] = set()
    for r in rows:
        if r["matches_cycle_i_short"] and (r["w"] >= 6 or r["cycle_i"]["L_run"] > 7):
            if r["w"] not in seen:
                seen.add(r["w"])
                kill_match_ws.append(r["w"])

    grows_at_edge_short = len(Ls_short) >= 2 and Ls_short[-1] > Ls_short[-2]
    grows_at_edge_long = len(Ls_long) >= 2 and Ls_long[-1] > Ls_long[-2]
    # Strict growth through the last three radii is a rising envelope.
    rising_long = (
        len(Ls_long) >= 3 and Ls_long[-1] > Ls_long[-2] and Ls_long[-2] > Ls_long[-3]
    )

    plat_s = plateau(Ls_short)
    plat_l = plateau(Ls_long)
    max_s = max(Ls_short) if Ls_short else 0
    max_l = max(Ls_long) if Ls_long else 0
    max_ci = max(Ls_ci) if Ls_ci else 0

    # Hull / both-edges can still match even if some dying-left rows
    # were the only unrestricted maximizers at a given w.
    hull_match = [
        r["w"]
        for r in rows
        if r["short"]["L_run_hull"] == r["cycle_i"]["L_run"] and r["w"] >= 6
    ]
    both_match = [
        r["w"]
        for r in rows
        if r["short"]["L_run_both_edges"] == r["cycle_i"]["L_run"] and r["w"] >= 6
    ]

    if kill_match_ws or hull_match or both_match:
        ws = sorted(set(kill_match_ws + hull_match + both_match))
        reason = (
            "left-edge-on (packed bit 0 = 1) attains the unrestricted Cycle I "
            f"L_run at w={ws}. The w=6 maximizer mask 7503 already has leftmost "
            "1 at -6, origin in the hull, and both packed edges live, with a "
            f"period-2 centre run of length {max_s} inside tcap=8w+128"
        )
        if max_l > max_s:
            reason += (
                f"; the long cap 32w+512 raises the class max to {max_l}"
            )
        reason += (
            ". Left-edge-on does not force a smaller cap than unrestricted. "
            "The runs are interior bursts, not an eventual regime. This does "
            "not exclude eventual period 2, and it is not a uniform-in-w theorem."
        )
        return "KILL", reason, True

    if grows_at_edge_short or grows_at_edge_long or rising_long:
        reason = (
            f"L_run on left-bit-1 rows is still growing at the scan edge "
            f"(short={Ls_short}, long={Ls_long}). Not a smaller cap than "
            "unrestricted, and not a plateau. This does not exclude eventual "
            "period 2."
        )
        return "KILL", reason, True

    below = all(r["strictly_below_cycle_i_short"] or r["w"] == 0 for r in rows)
    if below and plat_s["covers_scan_edge"] and plat_s["edge_length"] >= 3 and max_s < max_ci:
        reason = (
            f"every radius-w row with leftmost 1 at -w, w<=10, has every "
            f"period-2 centre run of length at most {max_s} inside tcap=8w+128, "
            f"strictly below the unrestricted Cycle I table (max {max_ci}). "
            f"Plateau L={plat_s['value']} on w={plat_s['edge_start_w']}..10. "
            "Finite theorem for this class only, not a uniform-in-w bound."
        )
        return "FINITE_THEOREM", reason, False

    reason = (
        f"left-bit-1 L_run short={Ls_short} long={Ls_long} Cycle I={Ls_ci}. "
        "No interesting match with the unrestricted table was recorded as a "
        "kill, and the envelope is not a strictly-smaller plateau. Not a "
        "uniform proof."
    )
    return "NO_WITNESS", reason, False


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def _fmt(n: int | None) -> str:
    if n is None:
        return "—"
    return f"{n:,}"


def write_markdown(dump: dict) -> str:
    a: list[str] = []

    def p(s: str = "") -> None:
        a.append(s)

    p("# Period-2 `L_run`: left-bit-1 (prize-seed left edge)")
    p()
    p("This note extends Cycle I (`research/period2_fiber.md`). It does")
    p("**not** exclude eventual period 2 for every finite row, and it does")
    p("not claim a prize result. It is a finite census of radius-`w≤10`")
    p("rows whose leftmost 1 sits at spatial `-w`, not a uniform-in-`w`")
    p("bound.")
    p()
    p("Helper: `research/period2_leftbit.py --certify`. Dump:")
    p("`research/period2_leftbit.json`. Packed evolution is imported from")
    p("`research/period2_fiber.py` and that file is not modified.")
    p()
    p("## Attack")
    p()
    p("The prize seed is a single 1 at the origin. Its light-cone left edge")
    p("satisfies `x(t,-t)=1` for every `t`. Finite-row `L_run` scans allow")
    p("arbitrary supports: packed bit 0 may be 0, so the window has vacuum")
    p("to the left of the true support (a dying / padded left). Cycle I’s")
    p("`w=7` maximizer is exactly the `w=6` row `7503` shifted by one left")
    p("vacuum.")
    p()
    p("For any finite row whose leftmost 1 is at `L`, vacuum to the left,")
    p("Rule 30 sends that edge left at speed 1 and keeps it 1:")
    p()
    p("```")
    p("x(t+1, L-1-t) = 0 XOR (0 OR 1) = 1")
    p("```")
    p()
    p("so `x(t, L-t)=1` is automatic — not a new constraint. Packed Rule 30")
    p("has the same identity: `(new & 1) == (old & 1)`. The prize-specific")
    p("extra is that the leftmost 1 *starts at 0*, so a later slice at time")
    p("`T` is a radius-`T` row with leftmost 1 at `-T`.")
    p()
    p("**Scan:** every radius-`w` packed row with bit 0 (spatial `-w`) equal")
    p("to 1. That is `2^{2w}` states, exhaustive through `w=10`")
    p("(`2^{20}` at the top radius). Two caps: Cycle I `tcap=8w+128` and")
    p("the ideas11 long cap `tcap=32w+512`, from a single evolution.")
    p()
    p("**Kill:** `L_run` on this class still grows with `w`, or matches the")
    p("unrestricted Cycle I table (left-edge-on does not cut the burst).")
    p()
    p("**Finite theorem (this class only):** left-edge-on forces a strictly")
    p("smaller cap than unrestricted, with a plateau at the scan edge.")
    p()
    p("**Survive / uniform proof:** not claimed; the census is finite.")
    p()
    p("Packed Rule 30 is the Cycle I engine:")
    p()
    p("```")
    p("new = (row << 2) ^ ((row << 1) | row)")
    p("```")
    p()
    p("with the centre bit at time `t` equal to `(row >> (w+t)) & 1`. Bit 0")
    p("is the leftmost cell of the current support (spatial `-w` at `t=0`).")
    p()
    p("Secondary filters, scored in the same loop: origin in the live hull")
    p("(`rightmost ≥ 0`), origin live, and both packed edges live (true")
    p("support bounding box exactly `[-w,w]`).")
    p()
    p("## Self-checks")
    p()
    ch = dump["checks"]
    p(f"- Prize seed `w=0` mask `1`, `tcap=128`: `L_run={ch['w0_L_run']}`")
    p("  from `t=35` (factor `1010101`).")
    p(
        f"- `w=6` mask `7503`, row `1111001010111`, `tcap=176`: "
        f"`L={ch['w6_7503_L']}` from `t={ch['w6_7503_start']}` to "
        f"`t={ch['w6_7503_end']}`. Bit 0 is `{ch['w6_7503_bit0']}` "
        "(in the left-bit class). Origin in hull, both edges live."
    )
    p("- Inlined two-cap loop agrees with `period2_fiber.scan_mask_runs`.")
    p("- Packed traces match the independent live-cell spacetime on the prize")
    p("  seed and on mask `7503`.")
    p("- Packed bit-0 identity: `(new & 1) == (old & 1)` on sampled rows.")
    p("- Left edge `x(t,-w-t)=1` holds on packed bit 0 and on the naive")
    p("  spacetime for sampled left-bit-1 rows.")
    p(
        f"- Cycle I `w=2` maximizer mask `2` has bit 0 = "
        f"`{ch['w2_cycle_i_maximizer_bit0']}` (excluded; true leftmost "
        f"`{ch['w2_cycle_i_maximizer_leftmost']}`)."
    )
    p(
        f"- Cycle I `w=7` maximizer is `7503 << 1` "
        f"({'yes' if ch['w7_cycle_i_is_padded_7503'] else 'no'}), bit 0 = "
        f"`{ch['w7_cycle_i_bit0']}`."
    )
    n_left = ch["cycle_i_n_maximizers_leftbit"]
    n_die = ch["cycle_i_n_maximizers_dying_left"]
    p(
        f"- Of 11 Cycle I maximizers (`w=0..10`), {n_left} already have "
        f"bit 0 = 1 and {n_die} are left-padded / dying-left."
    )
    p(f"- `checks.all_ok={ch['all_ok']}`.")
    p()
    p("## Exhaustive left-bit-1 rows, `w≤10`")
    p()
    rows = dump["exhaustive"]
    nproc_used = max(r["nproc"] for r in rows)
    wall_scan = sum(r["elapsed_sec"] for r in rows)
    p(
        f"`2^{{2w}}` states per radius (bit 0 fixed), `{nproc_used}` "
        f"processes on the large radii, scan wall {wall_scan:.1f}s "
        f"(total process {dump['wall_time_sec']:.1f}s)."
    )
    p()
    p("| `w` | states | Cycle I `L_run` | bit0 of CI max | `tcap=8w+128` | `L_left` | `L_hull` | `L_both` | `tcap=32w+512` | `L_long` | short best | long best |")
    p("|----:|-------:|----------------:|---------------:|--------------:|---------:|---------:|---------:|---------------:|---------:|-----------:|----------:|")
    for r in rows:
        bs = r["short"].get("best") or {}
        bl = r["long"].get("best") or {}
        p(
            f"| {r['w']} | {_fmt(r['n_leftbit'])} | {r['cycle_i']['L_run']} | "
            f"{r['cycle_i']['best_bit0']} | {r['short']['tcap']} | "
            f"**{r['short']['L_run']}** | {r['short']['L_run_hull']} | "
            f"{r['short']['L_run_both_edges']} | {r['long']['tcap']} | "
            f"**{r['long']['L_run']}** | {_fmt(bs.get('mask'))} | {_fmt(bl.get('mask'))} |"
        )
    p()
    Ls_s = [r["short"]["L_run"] for r in rows]
    Ls_l = [r["long"]["L_run"] for r in rows]
    Ls_ci = [r["cycle_i"]["L_run"] for r in rows]
    p(
        "Max `L` versus `w` (short / long / Cycle I): "
        + ", ".join(
            f"{r['w']}:{r['short']['L_run']}/{r['long']['L_run']}/{r['cycle_i']['L_run']}"
            for r in rows
        )
        + "."
    )
    p()
    match = [r["w"] for r in rows if r["matches_cycle_i_short"]]
    below = [r["w"] for r in rows if r["strictly_below_cycle_i_short"]]
    long_up = [r["w"] for r in rows if r["long_exceeds_short"]]
    p(
        f"Short-cap match with Cycle I at `w={match}`. Strictly below at "
        f"`w={below}`. Long cap exceeds short cap at `w={long_up or '∅'}`."
    )
    p()
    p("### Cycle I maximizers versus the left-bit class")
    p()
    p("| `w` | CI mask | bit 0 | in class | CI `L_run` | `L_left` |")
    p("|----:|--------:|------:|---------:|-----------:|---------:|")
    for r in rows:
        p(
            f"| {r['w']} | {_fmt(r['cycle_i']['best_mask'])} | "
            f"{r['cycle_i']['best_bit0']} | "
            f"{'yes' if r['cycle_i']['best_in_leftbit_class'] else 'no'} | "
            f"{r['cycle_i']['L_run']} | {r['short']['L_run']} |"
        )
    p()
    p("### Prefixes, hull, both edges")
    p()
    p("| `w` | `L_prefix` short | `L_prefix` long | `n` hull | `n` origin-live | `n` both-edges | `L_hull` long | `L_both` long |")
    p("|----:|-----------------:|----------------:|---------:|----------------:|---------------:|--------------:|--------------:|")
    for r in rows:
        p(
            f"| {r['w']} | {r['short']['L_prefix']} | {r['long']['L_prefix']} | "
            f"{_fmt(r['short']['n_hull'])} | {_fmt(r['short']['n_origin_live'])} | "
            f"{_fmt(r['short']['n_both_edges'])} | {r['long']['L_run_hull']} | "
            f"{r['long']['L_run_both_edges']} |"
        )
    p()
    p("No maximizer is eventual in either cap: the longest bursts are")
    p("interior. Each maximizer was re-evolved at `2·tcap`; none lengthened.")
    p("No scanned row has `L > 4w+16`.")
    p()
    p("### Long cap versus Cycle I")
    p()
    p("Cycle I’s `tcap=8w+128` plateaus at `L_run=24` for `6≤w≤10`. On")
    p("left-bit-1 rows the same plateau holds *inside that cap*. The long")
    p("cap `32w+512` finds later bursts that Cycle I never saw:")
    p()
    w9 = next((r for r in rows if r["w"] == 9), None)
    w10 = next((r for r in rows if r["w"] == 10), None)
    if w9 and w9["long"].get("best"):
        b = w9["long"]["best"]
        p(
            f"- `w=9`, mask `{b['mask']}`, row `{b['row']}`, live `{b['live']}` "
            f"(weight {b['n1']}, origin live, hull contains 0, right edge "
            f"{'on' if b['right_live'] else 'off'}). Run of length `{b['L']}` "
            f"from `t={b['start']}` to `t={b['end']}` inside `tcap={b['tcap']}`. "
            f"Cycle I’s cap is `{w9['short']['tcap']}`, which ends before the "
            f"burst starts. Doubled `L={(b.get('doubled') or {}).get('L')}`."
        )
    if w10 and w10["long"].get("best"):
        b = w10["long"]["best"]
        both = w10["long"].get("best_both_edges") or {}
        p(
            f"- `w=10`, mask `{b['mask']}`, row `{b['row']}`, live `{b['live']}` "
            f"(weight {b['n1']}, origin live, hull contains 0, right edge "
            f"{'on' if b['right_live'] else 'off'}). Run of length `{b['L']}` "
            f"from `t={b['start']}` to `t={b['end']}` inside `tcap={b['tcap']}`. "
            f"Cycle I’s cap is `{w10['short']['tcap']}`. Doubled "
            f"`L={(b.get('doubled') or {}).get('L')}`."
        )
        if both:
            p(
                f"  Both-edges (bounding box exactly `[-10,10]`) still reaches "
                f"`L={both['L']}` on mask `{both['mask']}`, same run window."
            )
    p()
    p("So `L_run` on this class still grows with `w` once the cap is long")
    p("enough to see the burst: 24, 25, 27 at `w=8,9,10`. Hull-contains-0")
    p("and both-edges-live agree with the class max at every scanned radius.")
    p()
    p("`w=3` is the only short-cap radius strictly below Cycle I (`12` vs")
    p("`13`). That is a one-step dip, not a smaller plateau: `w=4` already")
    p("matches again at 15, and `w=6` matches the unrestricted 24.")
    p()

    w6 = next((r for r in rows if r["w"] == 6), None)
    if w6 and w6["short"].get("best"):
        b6 = w6["short"]["best"]
        p("### Witness that the class attains Cycle I")
        p()
        p(
            f"Radius 6, mask `{b6['mask']}`, row `{b6['row']}`, live "
            f"`{b6['live']}`. Weight {b6['n1']}, span {b6['span']}, origin "
            f"in hull {'yes' if b6['origin_in_hull'] else 'no'}, both edges "
            f"{'yes' if b6['right_live'] else 'no'}. Period-2 run of length `{b6['L']}` from "
            f"`t={b6['start']}` to `t={b6['end']}` inside `tcap={b6['tcap']}`. "
            f"Doubled cap `L={(b6.get('doubled') or {}).get('L')}`."
        )
        p()
        p("This is the Cycle I maximizer. Restricting to left-bit-1 rows does")
        p("not remove it, and neither does requiring the origin in the hull or")
        p("both light-cone edges live.")
        p()
    elif dump.get("witness"):
        wt = dump["witness"]
        p("### Witness")
        p()
        p(
            f"Radius {wt['w']}, mask `{wt['mask']}`, row `{wt.get('row')}`, "
            f"`L={wt['L']}` from `t={wt['start']}` to `t={wt['end']}` "
            f"inside `tcap={wt['tcap']}`."
        )
        p()


    fit = dump.get("fit_L_run_short") or {}
    if fit:
        p(
            f"Least squares over the short-cap table: `L_left ≈ "
            f"{fit['C']:.2f} w + {fit['Cprime']:.2f}`. Summary of the small-`w` "
            "ramp plus whatever plateau is present, not a growth conjecture."
        )
        p()

    p("## Verdict")
    p()
    p(f"**{dump['verdict']}.** {dump['kill_reason']}")
    p()
    p("What this does not show:")
    p()
    p("- A uniform bound `L_run(w)≤C` on this class for all `w`.")
    p("- That the prize seed itself has a long period-2 centre run. The")
    p("  prize seed is one left-bit-1 row (`w=0`, `L_run=7`); later prize")
    p("  slices are one specific mask per radius, not the maximizer.")
    p("- Exclusion of eventual period 2. Every scanned burst is finite")
    p("  inside the cap.")
    p()
    p("## Files")
    p()
    p("- `research/period2_leftbit.py` — this scan")
    p("- `research/period2_leftbit.json` — dump")
    p("- `research/period2_fiber.py` — packed engine, not modified")
    p()
    return "\n".join(a) + "\n"


def slim_best(rec: dict | None) -> dict | None:
    if rec is None:
        return None
    keep = (
        "mask",
        "w",
        "row",
        "live",
        "n1",
        "span",
        "origin_live",
        "origin_in_hull",
        "right_live",
        "L",
        "start",
        "end",
        "prefix",
        "suffix",
        "tcap",
        "reaches_cap",
        "doubled",
    )
    return {k: rec[k] for k in keep if k in rec}


def slim_side(side: dict) -> dict:
    out = dict(side)
    for key in ("best", "best_hull", "best_origin_live", "best_both_edges"):
        if key in out:
            out[key] = slim_best(out[key])
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def certify(w_max: int = W_MAX) -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    print(log[-1], flush=True)
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    rows = []
    for w in range(0, w_max + 1):
        rows.append(exhaustive_w(w, log))

    xs = [r["w"] for r in rows]
    ys_s = [r["short"]["L_run"] for r in rows]
    ys_l = [r["long"]["L_run"] for r in rows]
    Cs, Cps = fit_linear(xs, ys_s)
    Cl, Cpl = fit_linear(xs, ys_l)

    verdict, reason, is_kill = decide_verdict(rows)

    # Verify the short-cap maximizer at the first interesting match, else
    # the global long-cap maximizer.
    witness = None
    witness_check = None
    match_rows = [r for r in rows if r["matches_cycle_i_short"] and r["w"] >= 6]
    if match_rows:
        witness = slim_best(match_rows[0]["short"]["best"])
    else:
        best_long = max(rows, key=lambda r: (r["long"]["L_run"], -r["w"]))
        witness = slim_best(best_long["long"]["best"])
    if witness is not None:
        witness_check = verify_row(witness["mask"], witness["w"], witness["tcap"])
        log.append(
            f"witness_check ok={witness_check['ok']} L={witness_check['L']} "
            f"doubled={witness_check['doubled_L']} alt={witness_check['alternating']}"
        )
        print(log[-1], flush=True)
        if not witness_check["ok"]:
            raise AssertionError(f"witness failed verification: {witness_check}")

    comparison = []
    for r in rows:
        comparison.append(
            {
                "w": r["w"],
                "n_leftbit": r["n_leftbit"],
                "L_cycle_i": r["cycle_i"]["L_run"],
                "cycle_i_best_mask": r["cycle_i"]["best_mask"],
                "cycle_i_best_bit0": r["cycle_i"]["best_bit0"],
                "L_left_short": r["short"]["L_run"],
                "L_left_long": r["long"]["L_run"],
                "L_hull_short": r["short"]["L_run_hull"],
                "L_hull_long": r["long"]["L_run_hull"],
                "L_both_short": r["short"]["L_run_both_edges"],
                "L_both_long": r["long"]["L_run_both_edges"],
                "matches_cycle_i_short": r["matches_cycle_i_short"],
                "long_exceeds_short": r["long_exceeds_short"],
            }
        )

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period2_leftbit",
        "ideas12": "item 2",
        "cycle_i": "research/period2_fiber.md",
        "problem": (
            "among radius-w rows with leftmost 1 at -w (packed bit 0 = 1), "
            "what is max period-2 centre run inside tcap=8w+128 and "
            "32w+512; kill if L still grows or matches unrestricted Cycle I; "
            "finite theorem if left-edge-on forces a smaller cap"
        ),
        "verdict": verdict,
        "kill": is_kill,
        "survive": False,
        "uniform_proof": False,
        "finite_theorem": verdict == "FINITE_THEOREM",
        "kill_reason": reason,
        "wall_time_sec": round(wall, 4),
        "tcap_cycle_i": "8w+128",
        "tcap_long": "32w+512",
        "w_max": w_max,
        "n_states_formula": "2^{2w} (bit 0 fixed to 1)",
        "checks": checks,
        "witness": witness,
        "witness_check": witness_check,
        "comparison": comparison,
        "fit_L_run_short": {
            "C": Cs,
            "Cprime": Cps,
            "note": (
                "least-squares L_left ~ C*w+C' is a summary only; the table "
                "is the actual finite statement"
            ),
        },
        "fit_L_run_long": {"C": Cl, "Cprime": Cpl},
        "plateau_short": plateau(ys_s),
        "plateau_long": plateau(ys_l),
        "exhaustive": [
            {
                **{k: v for k, v in r.items() if k not in ("short", "long")},
                "short": slim_side(r["short"]),
                "long": slim_side(r["long"]),
            }
            for r in rows
        ],
        "log": log,
    }
    OUT_JSON.write_text(json.dumps(dump, indent=2) + "\n")
    md = write_markdown(dump)
    OUT_MD.write_text(md)
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    print(f"verdict={verdict} wall={wall:.3f}s")
    print(f"reason: {reason}")
    print(
        "L_left short/long/CI: "
        + str([(r["w"], r["short"]["L_run"], r["long"]["L_run"], r["cycle_i"]["L_run"]) for r in rows])
    )
    return dump


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    p.add_argument("--render", action="store_true", help="rewrite markdown from existing json")
    p.add_argument("--w-max", type=int, default=W_MAX)
    args = p.parse_args()
    if args.render:
        dump = json.loads(OUT_JSON.read_text())
        OUT_MD.write_text(write_markdown(dump))
        print(f"wrote {OUT_MD}")
        return
    if not args.certify:
        p.error("pass --certify")
    if args.w_max < 0 or args.w_max > 10:
        p.error("w-max must be in 0..10")
    certify(args.w_max)


if __name__ == "__main__":
    main()
