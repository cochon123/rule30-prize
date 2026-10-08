"""ideas13 item 1: origin-in-hull weight-9/10 span-20 census.

Cycle M (research/period2_hull.md) proved L<=31 for in-hull weight<=8
span<=24. The prize seed's later rows have larger weight. This script
repeats that census for Hamming weights 9 and 10, span<=20, keeping
only placements with

    min(live) <= 0 <= max(live)

i.e. the origin lies in the live convex hull. Combinatorial supports
still sit on [0,s] with live endpoints; in-hull is then C in [0,s]
(s+1 centres), not the Cycle L window C in [-s, 2s] (3s+1 centres).

Packed evolution is imported from research/period2_fiber.py and that
file is not modified:
    new = (row << 2) ^ ((row << 1) | row)
    centre bit (row >> (w + t)) & 1
with bit 0 the leftmost cell of the current support.

tcap=32w+512. Any L>=30 row is re-evolved at 2*tcap.

Self-check: wt=8 span=18 mask 281769 is NOT in this census (wt=8);
the packed engine still gives L=31 for it.

Kill: an in-hull wt=9 or 10 span<=20 row with L>=32 after doubling.
Finite theorem: L<=31 on this class too.

Run: python3 research/period2_hull910.py --certify
Dump: research/period2_hull910.json, research/period2_hull910.md

This file does not modify period2_hull.py, period2_weight8.py, or
period2_fiber.py.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations, islice
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from period2_fiber import (  # noqa: E402
    evolve_centers,
    mask_to_live,
    naive_centers,
    rule30_step,
    scan_mask_runs,
)

OUT_JSON = Path(__file__).resolve().with_suffix(".json")
OUT_MD = Path(__file__).resolve().with_suffix(".md")

SPAN_MAX = 20
WT_MIN = 9
WT_MAX = 10
NPROC_CAP = 4

MASK_4369552 = 4369552
W_4369552 = 11
MASK_281769 = 281769
W_281769 = 17
MASK_7503 = 7503
MASK_17057305 = 17057305
W_17057305 = 38

LIVE_4369552 = (-7, -4, -1, 0, 2, 4, 6, 11)
LIVE_281769 = (-17, -14, -12, -10, -7, -6, -3, 1)
LIVE_17057305 = (-38, -35, -34, -29, -28, -24, -20, -14)


def tcap_census(w: int) -> int:
    return 32 * w + 512


def tcap_cycle_j(w: int) -> int:
    return 8 * w + 128


def tcap_cycle_k(w: int) -> int:
    return 8 * w + 256


def nproc() -> int:
    try:
        return max(1, min(NPROC_CAP, os.cpu_count() or 1))
    except Exception:
        return 1


def popcount(n: int) -> int:
    return n.bit_count()


def span_of_live(live: list[int]) -> int:
    if not live:
        return 0
    return live[-1] - live[0]


def in_hull(live) -> bool:
    """Origin in the live convex hull: min(live) <= 0 <= max(live)."""
    if not live:
        return False
    return live[0] <= 0 <= live[-1]


def pack_from(pat: int, s: int, C: int) -> tuple[int, int]:
    """Pack support bits of [0,s] with the origin at canonical cell C.

    Spatial live cell p (0<=p<=s) sits at p-C. True radius
    w = max(C, s-C); mask bit 0 is spatial -w.
    """
    w = C if C >= s - C else s - C
    return w, pat << (w - C)


def live_from(pat: int, s: int, C: int) -> list[int]:
    return [p - C for p in range(s + 1) if (pat >> p) & 1]


def row_bits(mask: int, w: int) -> str:
    return "".join(str((mask >> i) & 1) for i in range(2 * w + 1))


def rec_of(pat: int, s: int, C: int, L: int, start: int, end: int, tcap: int) -> dict:
    w, mask = pack_from(pat, s, C)
    live = live_from(pat, s, C)
    return {
        "mask": mask,
        "w": w,
        "row": row_bits(mask, w),
        "live": live,
        "n1": len(live),
        "span": s,
        "span_len": s + 1,
        "C": C,
        "pat": pat,
        "L": L,
        "start": start,
        "end": end,
        "tcap": tcap,
        "reaches_cap": end == tcap and L >= 2,
        "in_hull": in_hull(live),
    }


def consider(best: dict | None, rec: dict) -> dict:
    if best is None:
        return rec
    if rec["L"] > best["L"]:
        return rec
    if rec["L"] == best["L"] and rec.get("w", 0) < best.get("w", 0):
        return rec
    if (
        rec["L"] == best["L"]
        and rec.get("w") == best.get("w")
        and rec["mask"] < best["mask"]
    ):
        return rec
    return best


def scan_runs_fast(mask: int, w: int, tcap: int) -> tuple[int, int, int]:
    """Same packed CA as period2_fiber.scan_mask_runs; no prefix tracking.

    Returns (L, start, end). Self-checked against scan_mask_runs.
    """
    row = mask
    prev = (row >> w) & 1
    best = 1
    best_start = 0
    run = 1
    run_start = 0
    for t in range(1, tcap):
        row = (row << 2) ^ ((row << 1) | row)
        bit = (row >> (w + t)) & 1
        if bit != prev:
            run += 1
        else:
            run = 1
            run_start = t
        if run > best:
            best = run
            best_start = run_start
        prev = bit
    return best, best_start, best_start + best


def double_cap(rec: dict) -> dict:
    """Re-evolve at 2*tcap. Required for any L>=30 candidate."""
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
        "suffix": st2["suffix"],
        "holds": st2["L"] >= rec["L"],
        "holds_ge30": st2["L"] >= 30,
        "holds_ge32": st2["L"] >= 32,
        "holds_ge40": st2["L"] >= 40,
    }
    return out


def slim_rec(rec: dict | None) -> dict | None:
    if rec is None:
        return None
    keys = (
        "mask",
        "w",
        "row",
        "live",
        "n1",
        "span",
        "span_len",
        "C",
        "pat",
        "L",
        "start",
        "end",
        "tcap",
        "reaches_cap",
        "in_hull",
        "doubled",
        "verify",
        "cap_compare",
    )
    return {k: rec[k] for k in keys if k in rec}


# ---------------------------------------------------------------------------
# One canonical support, in-hull translations only: C in [0, s].
# Endpoints of a span-s block are live, so min live = -C, max live = s-C,
# and min<=0<=max iff 0<=C<=s.
# ---------------------------------------------------------------------------

def _scan_pattern(pat: int, s: int):
    """Evolve `pat` once; score every in-hull centre C in [0, s] at 32w+512.

    Returns (best_i, best[], best_start[], nC, tcapC). Index i is C.
    Spatial x sits at packed bit x+t after t steps of the unpadded row
    (bit 0 = spatial 0 at t=0). Centre C is packed bit C+t.
    """
    nC = s + 1
    tcapC = [0] * nC
    for C in range(nC):
        w = C if C >= s - C else s - C
        tcapC[C] = 32 * w + 512

    prev = [0] * nC
    best = [1] * nC
    best_start = [0] * nC
    run = [1] * nC
    run_start = [0] * nC
    for C in range(nC):
        prev[C] = (pat >> C) & 1

    # Bands of centres sharing a remaining tcap, so finished columns
    # drop out instead of branching every step.
    order = sorted(range(nC), key=tcapC.__getitem__)
    bounds = sorted(set(tcapC))
    row = pat
    nC_mask = (1 << nC) - 1
    live_lo = 0
    t = 1
    for t_hi in bounds:
        active = order[live_lo:]
        if t >= t_hi:
            while live_lo < nC and tcapC[order[live_lo]] <= t:
                live_lo += 1
            continue
        for t in range(t, t_hi):
            row = (row << 2) ^ ((row << 1) | row)
            chunk = (row >> t) & nC_mask
            for i in active:
                bit = (chunk >> i) & 1
                if bit != prev[i]:
                    run[i] += 1
                else:
                    run[i] = 1
                    run_start[i] = t
                if run[i] > best[i]:
                    best[i] = run[i]
                    best_start[i] = run_start[i]
                prev[i] = bit
        while live_lo < nC and tcapC[order[live_lo]] <= t_hi:
            live_lo += 1
        t = t_hi

    i_best = 0
    Lmax = best[0]
    for i in range(1, nC):
        if best[i] > Lmax:
            Lmax = best[i]
            i_best = i
    return i_best, best, best_start, nC, tcapC


def _chunk(args: tuple[int, int, int, int]) -> dict:
    wt, s, skip, take = args
    nC = s + 1
    n_patterns = 0
    n_place = 0
    Lrun = 0
    best = None
    n_ge30 = 0
    n_ge31 = 0
    n_ge32 = 0
    n_ge40 = 0
    ge30: list[dict] = []
    ge30_hold_fail = 0
    L_after_double_max = 0
    n_off_hull = 0

    if wt == 1:
        it = [()] if s == 0 else []
    elif wt == 2:
        it = [()] if s >= 1 else []
    else:
        it = combinations(range(1, s), wt - 2)
    it = islice(it, skip, skip + take)

    for idxs in it:
        pat = 1 | (1 << s) if s > 0 else 1
        for i in idxs:
            pat |= 1 << i
        n_patterns += 1
        n_place += nC
        i_best, bestL, best_start, nC_got, tcapC = _scan_pattern(pat, s)
        L = bestL[i_best]
        C = i_best
        start = best_start[i_best]
        rec = rec_of(pat, s, C, L, start, start + L, tcapC[i_best])
        if not rec["in_hull"]:
            n_off_hull += 1
        else:
            best = consider(best, rec)
            Lrun = best["L"]
        if L >= 30:
            for i in range(nC_got):
                Li = bestL[i]
                if Li < 30:
                    continue
                n_ge30 += 1
                if Li >= 31:
                    n_ge31 += 1
                if Li >= 32:
                    n_ge32 += 1
                if Li >= 40:
                    n_ge40 += 1
                C = i
                start = best_start[i]
                rec = rec_of(pat, s, C, Li, start, start + Li, tcapC[i])
                if not rec["in_hull"]:
                    n_off_hull += 1
                    continue
                rec = double_cap(rec)
                Ld = rec["doubled"]["L"]
                if Ld > L_after_double_max:
                    L_after_double_max = Ld
                if not rec["doubled"]["holds"]:
                    ge30_hold_fail += 1
                if Li >= 31 or Ld >= 32 or len(ge30) < 8:
                    ge30.append(rec)

    return {
        "wt": wt,
        "s": s,
        "n_patterns": n_patterns,
        "n_place": n_place,
        "L_run": Lrun,
        "best": best,
        "n_ge30": n_ge30,
        "n_ge31": n_ge31,
        "n_ge32": n_ge32,
        "n_ge40": n_ge40,
        "ge30": ge30,
        "ge30_hold_fail": ge30_hold_fail,
        "L_after_double_max": L_after_double_max,
        "n_off_hull": n_off_hull,
    }


def _n_types(wt: int, s: int) -> int:
    if wt == 1:
        return 1 if s == 0 else 0
    if s < wt - 1:
        return 0
    return math.comb(s - 1, wt - 2)


def _tasks(workers: int) -> list[tuple[int, int, int, int]]:
    tasks: list[tuple[int, int, int, int]] = []
    for wt in range(WT_MIN, WT_MAX + 1):
        s_lo = wt - 1
        for s in range(s_lo, SPAN_MAX + 1):
            n = _n_types(wt, s)
            if n <= 0:
                continue
            take = max(64, min(n, int(20000 / max(s, 1))))
            skip = 0
            while skip < n:
                t = min(take, n - skip)
                tasks.append((wt, s, skip, t))
                skip += t
    # Heavier (high s, high wt) first so the tail is small leftover.
    tasks.sort(key=lambda t: -(_n_types(t[0], t[1]) * (t[1] + 1) * (32 * t[1] + 512)))
    _ = workers
    return tasks


def merge_parts(parts: list[dict]) -> dict:
    best = None
    n_patterns = 0
    n_place = 0
    n_ge30 = 0
    n_ge31 = 0
    n_ge32 = 0
    n_ge40 = 0
    ge30_hold_fail = 0
    L_after_double_max = 0
    n_off_hull = 0
    ge30: list[dict] = []
    by_wt: dict[int, dict] = {}
    by_span: dict[int, dict] = {}

    def bump(acc: dict, part: dict, key: int) -> None:
        slot = acc.get(key)
        if slot is None:
            acc[key] = {
                "n_patterns": part["n_patterns"],
                "n_place": part["n_place"],
                "L_run": part["L_run"],
                "n_ge30": part["n_ge30"],
                "n_ge31": part["n_ge31"],
                "n_ge32": part["n_ge32"],
                "n_ge40": part["n_ge40"],
                "best": part["best"],
            }
            return
        slot["n_patterns"] += part["n_patterns"]
        slot["n_place"] += part["n_place"]
        slot["n_ge30"] += part["n_ge30"]
        slot["n_ge31"] += part["n_ge31"]
        slot["n_ge32"] += part["n_ge32"]
        slot["n_ge40"] += part["n_ge40"]
        if part["best"] is not None:
            slot["best"] = consider(slot["best"], part["best"])
            slot["L_run"] = slot["best"]["L"]

    for p in parts:
        n_patterns += p["n_patterns"]
        n_place += p["n_place"]
        n_ge30 += p["n_ge30"]
        n_ge31 += p["n_ge31"]
        n_ge32 += p["n_ge32"]
        n_ge40 += p["n_ge40"]
        ge30_hold_fail += p["ge30_hold_fail"]
        n_off_hull += p["n_off_hull"]
        if p["L_after_double_max"] > L_after_double_max:
            L_after_double_max = p["L_after_double_max"]
        if p["best"] is not None:
            best = consider(best, p["best"])
        ge30.extend(p.get("ge30") or [])
        bump(by_wt, p, p["wt"])
        bump(by_span, p, p["s"])

    uniq: dict[tuple[int, int], dict] = {}
    for r in ge30:
        if not in_hull(r.get("live") or []):
            n_off_hull += 1
            continue
        k = (r["w"], r["mask"])
        prev = uniq.get(k)
        if prev is None or r["L"] > prev["L"]:
            uniq[k] = r
    ge30_u = sorted(uniq.values(), key=lambda r: (-r["L"], r["w"], r["mask"]))
    return {
        "best": best,
        "n_patterns": n_patterns,
        "n_place": n_place,
        "n_ge30": n_ge30,
        "n_ge31": n_ge31,
        "n_ge32": n_ge32,
        "n_ge40": n_ge40,
        "ge30_hold_fail": ge30_hold_fail,
        "L_after_double_max": L_after_double_max,
        "n_off_hull": n_off_hull,
        "ge30": ge30_u,
        "by_wt": by_wt,
        "by_span": by_span,
        "L_run": 0 if best is None else best["L"],
    }


def table_from(acc: dict, keys: list[int], kind: str) -> list[dict]:
    out = []
    for k in keys:
        slot = acc.get(k)
        if slot is None:
            out.append(
                {
                    kind: k,
                    "n_patterns": 0,
                    "n_place": 0,
                    "L_run": 0,
                    "n_ge30": 0,
                    "n_ge31": 0,
                    "n_ge32": 0,
                    "n_ge40": 0,
                    "best_mask": None,
                    "best_w": None,
                    "best_start": None,
                    "best_end": None,
                    "best_live": None,
                }
            )
            continue
        b = slot["best"]
        out.append(
            {
                kind: k,
                "n_patterns": slot["n_patterns"],
                "n_place": slot["n_place"],
                "L_run": slot["L_run"],
                "n_ge30": slot["n_ge30"],
                "n_ge31": slot["n_ge31"],
                "n_ge32": slot["n_ge32"],
                "n_ge40": slot["n_ge40"],
                "best_mask": None if b is None else b["mask"],
                "best_w": None if b is None else b["w"],
                "best_start": None if b is None else b["start"],
                "best_end": None if b is None else b["end"],
                "best_live": None if b is None else b["live"],
            }
        )
    return out


def run_census(log: list[str]) -> dict:
    workers = nproc()
    tasks = _tasks(workers)
    n_tasks = len(tasks)
    log.append(
        f"census tasks={n_tasks} nproc={workers} span<= {SPAN_MAX} "
        f"wt={WT_MIN}..{WT_MAX} placement=in-hull C in [0,s]"
    )
    print(log[-1], flush=True)
    t0 = time.perf_counter()
    parts: list[dict] = []
    if workers == 1:
        for i, task in enumerate(tasks, 1):
            parts.append(_chunk(task))
            if i == 1 or i == n_tasks or i % max(1, n_tasks // 8) == 0:
                sofar = max((p["L_run"] for p in parts), default=0)
                msg = f"census {i}/{n_tasks} L_run={sofar}"
                log.append(msg)
                print(msg, flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_chunk, task): task for task in tasks}
            done = 0
            for fut in as_completed(futs):
                parts.append(fut.result())
                done += 1
                if done == 1 or done == n_tasks or done % max(1, n_tasks // 10) == 0:
                    sofar = max((p["L_run"] for p in parts), default=0)
                    npat = sum(p["n_patterns"] for p in parts)
                    msg = (
                        f"census {done}/{n_tasks} n_patterns={npat} "
                        f"L_run={sofar}"
                    )
                    log.append(msg)
                    print(msg, flush=True)
    elapsed = time.perf_counter() - t0
    merged = merge_parts(parts)
    if merged["best"] is not None and merged["best"].get("doubled") is None:
        merged["best"] = double_cap(merged["best"])
    merged["by_wt_table"] = table_from(
        merged["by_wt"], list(range(WT_MIN, WT_MAX + 1)), "wt"
    )
    merged["by_span_table"] = table_from(
        merged["by_span"], list(range(0, SPAN_MAX + 1)), "span"
    )
    Ls = [row["L_run"] for row in merged["by_span_table"]]
    hull = []
    for s in range(0, SPAN_MAX + 1):
        hull.append({"span_len": s + 1, "L_run": Ls[s] if s < len(Ls) else 0})
    merged["span_L"] = Ls
    merged["hull_len_table"] = hull
    merged["elapsed_sec"] = round(elapsed, 4)
    merged["nproc"] = workers
    merged["n_tasks"] = n_tasks
    expected = sum(
        _n_types(wt, s)
        for wt in range(WT_MIN, WT_MAX + 1)
        for s in range(wt - 1, SPAN_MAX + 1)
    )
    merged["n_patterns_expected"] = expected
    if merged["n_patterns"] != expected:
        raise AssertionError(
            f"n_patterns {merged['n_patterns']} != expected {expected}"
        )
    msg = (
        f"census done n_patterns={merged['n_patterns']} n_place={merged['n_place']} "
        f"L_run={merged['L_run']} n_ge30={merged['n_ge30']} n_ge32={merged['n_ge32']} "
        f"n_off_hull={merged['n_off_hull']} {elapsed:.3f}s"
    )
    log.append(msg)
    print(msg, flush=True)
    return merged


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def verify_row(mask: int, w: int, tcap: int) -> dict:
    st = scan_mask_runs(mask, w, tcap)
    fast = scan_runs_fast(mask, w, tcap)
    bits = evolve_centers(mask, w, tcap)
    naive = naive_centers(mask_to_live(mask, w), tcap)
    run = bits[st["start"] : st["end"]]
    alt = len(run) >= 2 and all(run[i] != run[i - 1] for i in range(1, len(run)))
    before = bits[st["start"] - 1] if st["start"] else None
    after = bits[st["end"]] if st["end"] < len(bits) else None
    st2 = scan_mask_runs(mask, w, 2 * tcap)
    live = sorted(p for p, b in mask_to_live(mask, w).items() if b)
    return {
        "packed_matches_naive": bits == naive,
        "fast_matches_engine": fast == (st["L"], st["start"], st["end"]),
        "L": st["L"],
        "start": st["start"],
        "end": st["end"],
        "run_bits": "".join(map(str, run[:64])) + ("..." if len(run) > 64 else ""),
        "run_len": len(run),
        "alternating": alt,
        "break_before": before,
        "break_after": after,
        "interior": st["end"] < tcap and st["start"] > 0,
        "doubled_L": st2["L"],
        "doubled_start": st2["start"],
        "doubled_end": st2["end"],
        "in_hull": in_hull(live),
        "live": live,
        "ok": bits == naive and fast[0] == st["L"] and alt,
    }


def cap_compare(mask: int, w: int) -> dict:
    t_j = tcap_cycle_j(w)
    t_k = tcap_cycle_k(w)
    t_c = tcap_census(w)
    st_j = scan_mask_runs(mask, w, t_j)
    st_k = scan_mask_runs(mask, w, t_k)
    st_c = scan_mask_runs(mask, w, t_c)
    st_2 = scan_mask_runs(mask, w, 2 * t_c)
    return {
        "w": w,
        "mask": mask,
        "tcap_8w128": t_j,
        "L_8w128": st_j["L"],
        "start_8w128": st_j["start"],
        "end_8w128": st_j["end"],
        "truncated_by_8w128": st_j["L"] < st_c["L"],
        "tcap_8w256": t_k,
        "L_8w256": st_k["L"],
        "start_8w256": st_k["start"],
        "end_8w256": st_k["end"],
        "tcap_census": t_c,
        "L_census": st_c["L"],
        "start_census": st_c["start"],
        "end_census": st_c["end"],
        "tcap_doubled": 2 * t_c,
        "L_doubled": st_2["L"],
        "start_doubled": st_2["start"],
        "end_doubled": st_2["end"],
        "holds": st_2["L"] >= st_c["L"],
        "holds_ge32": st_2["L"] >= 32,
    }


def _pattern_of_live(live) -> tuple[int, int, int]:
    live = list(live)
    mn, mx = min(live), max(live)
    s = mx - mn
    C = -mn
    pat = 0
    for p in live:
        pat |= 1 << (p - mn)
    return pat, s, C


def _multi_matches_packed(pat: int, s: int, C: int) -> dict:
    w, mask = pack_from(pat, s, C)
    tcap = tcap_census(w)
    st = scan_mask_runs(mask, w, tcap)
    i_best, bestL, best_start, nC, tcapC = _scan_pattern(pat, s)
    in_range = 0 <= C < nC
    L = bestL[C] if in_range else None
    start = best_start[C] if in_range else None
    return {
        "w": w,
        "mask": mask,
        "engine_L": st["L"],
        "engine_start": st["start"],
        "engine_end": st["end"],
        "multi_L": L,
        "multi_start": start,
        "multi_end": None if start is None else start + L,
        "tcap": tcap,
        "tcapC": tcapC[C] if in_range else None,
        "nC": nC,
        "C": C,
        "in_hull_range": in_range,
        "ok": in_range and L == st["L"] and start == st["start"] and tcapC[C] == tcap,
    }


def run_checks() -> dict:
    checks: dict = {}
    st11 = scan_mask_runs(MASK_4369552, W_4369552, tcap_cycle_j(11))
    checks["w11_mask"] = MASK_4369552
    checks["w11_L"] = st11["L"]
    checks["w11_start"] = st11["start"]
    checks["w11_end"] = st11["end"]
    checks["w11_L29_ok"] = st11["L"] == 29 and st11["start"] == 159
    live11 = sorted(p for p, b in mask_to_live(MASK_4369552, W_4369552).items() if b)
    checks["w11_live"] = live11
    checks["w11_live_ok"] = tuple(live11) == LIVE_4369552
    checks["w11_span"] = span_of_live(live11)
    checks["w11_span_ok"] = checks["w11_span"] == 18
    checks["w11_wt_ok"] = popcount(MASK_4369552) == 8
    checks["w11_in_hull"] = in_hull(live11)
    checks["w11_in_hull_ok"] = in_hull(live11) is True

    st17 = scan_mask_runs(MASK_281769, W_281769, tcap_cycle_k(17))
    checks["w17_mask"] = MASK_281769
    checks["w17_tcap_8w256"] = tcap_cycle_k(17)
    checks["w17_L"] = st17["L"]
    checks["w17_start"] = st17["start"]
    checks["w17_end"] = st17["end"]
    checks["w17_L31_ok"] = st17["L"] == 31 and st17["start"] == 320
    live17 = sorted(p for p, b in mask_to_live(MASK_281769, W_281769).items() if b)
    checks["w17_live"] = live17
    checks["w17_live_ok"] = tuple(live17) == LIVE_281769
    checks["w17_span"] = span_of_live(live17)
    checks["w17_span_ok"] = checks["w17_span"] == 18
    checks["w17_wt_ok"] = popcount(MASK_281769) == 8
    checks["w17_not_in_wt910_ok"] = popcount(MASK_281769) not in range(
        WT_MIN, WT_MAX + 1
    )
    checks["w17_in_hull"] = in_hull(live17)
    checks["w17_in_hull_ok"] = (
        in_hull(live17) is True and live17[0] <= 0 <= live17[-1]
    )

    st17j = scan_mask_runs(MASK_281769, W_281769, tcap_cycle_j(17))
    checks["w17_L_8w128"] = st17j["L"]
    checks["w17_missed_by_8w128"] = st17j["L"] < 31 and st17["start"] > tcap_cycle_j(17)

    st17c = scan_mask_runs(MASK_281769, W_281769, tcap_census(17))
    checks["w17_census_tcap"] = tcap_census(17)
    checks["w17_census_L"] = st17c["L"]
    checks["w17_census_ok"] = st17c["L"] == 31 and st17c["start"] == 320

    st6 = scan_mask_runs(MASK_7503, 6, tcap_cycle_j(6))
    checks["w6_L"] = st6["L"]
    checks["w6_start"] = st6["start"]
    checks["w6_run24_ok"] = st6["L"] == 24 and st6["start"] == 94

    live38 = sorted(
        p for p, b in mask_to_live(MASK_17057305, W_17057305).items() if b
    )
    checks["offhull_mask"] = MASK_17057305
    checks["offhull_w"] = W_17057305
    checks["offhull_live"] = live38
    checks["offhull_live_ok"] = tuple(live38) == LIVE_17057305
    checks["offhull_wt_ok"] = popcount(MASK_17057305) == 8
    checks["offhull_span"] = span_of_live(live38)
    checks["offhull_span_ok"] = checks["offhull_span"] == 24
    checks["offhull_all_live_lt_0"] = bool(live38) and all(x < 0 for x in live38)
    checks["offhull_in_hull"] = in_hull(live38)
    checks["offhull_in_hull_ok"] = in_hull(live38) is False
    pat38, s38, C38 = _pattern_of_live(LIVE_17057305)
    w38, m38 = pack_from(pat38, s38, C38)
    checks["offhull_C"] = C38
    checks["offhull_s"] = s38
    checks["offhull_pack_ok"] = w38 == W_17057305 and m38 == MASK_17057305
    checks["offhull_C_outside_hull"] = not (0 <= C38 <= s38)
    st38 = scan_mask_runs(MASK_17057305, W_17057305, tcap_census(W_17057305))
    checks["offhull_L"] = st38["L"]
    checks["offhull_L35_ok"] = st38["L"] == 35
    checks["offhull_excluded_ok"] = (
        checks["offhull_in_hull_ok"]
        and checks["offhull_all_live_lt_0"]
        and checks["offhull_C_outside_hull"]
        and checks["offhull_pack_ok"]
        and checks["offhull_L35_ok"]
    )

    fast_ok = True
    fail = None
    for w, mask, tcap in (
        (0, 1, 128),
        (6, MASK_7503, 176),
        (11, MASK_4369552, 216),
        (17, MASK_281769, tcap_cycle_k(17)),
        (17, MASK_281769, tcap_census(17)),
        (38, MASK_17057305, tcap_census(38)),
        (4, 300, 80),
    ):
        a = scan_mask_runs(mask, w, tcap)
        b = scan_runs_fast(mask, w, tcap)
        if a["L"] != b[0] or a["start"] != b[1] or a["end"] != b[2]:
            fast_ok = False
            fail = {"w": w, "mask": mask, "engine": a, "fast": b}
            break
    checks["fast_matches_scan_mask_runs"] = fast_ok
    if fail:
        checks["fast_fail"] = fail

    prize = evolve_centers(1, 0, 32)
    checks["packed_matches_naive_prize"] = prize == naive_centers({0: 1}, 32)
    a = evolve_centers(MASK_4369552, W_4369552, 48)
    b = naive_centers(mask_to_live(MASK_4369552, W_4369552), 48)
    checks["packed_matches_naive_4369552"] = a == b
    a17 = evolve_centers(MASK_281769, W_281769, 64)
    b17 = naive_centers(mask_to_live(MASK_281769, W_281769), 64)
    checks["packed_matches_naive_281769"] = a17 == b17

    checks["rule30_step_formula"] = all(
        rule30_step(m) == ((m << 2) ^ ((m << 1) | m))
        for m in (0, 1, MASK_7503, MASK_4369552, MASK_281769, MASK_17057305)
    )

    m11 = _multi_matches_packed(*_pattern_of_live(LIVE_4369552))
    m17 = _multi_matches_packed(*_pattern_of_live(LIVE_281769))
    checks["multi_4369552"] = m11
    checks["multi_281769"] = m17
    checks["multi_4369552_ok"] = bool(m11["ok"]) and m11["multi_L"] == 29
    checks["multi_281769_ok"] = bool(m17["ok"]) and m17["multi_L"] == 31

    m38 = _multi_matches_packed(*_pattern_of_live(LIVE_17057305))
    checks["multi_17057305"] = {
        "nC": m38["nC"],
        "C": m38["C"],
        "in_hull_range": m38["in_hull_range"],
        "engine_L": m38["engine_L"],
    }
    checks["multi_17057305_excluded_ok"] = (
        m38["in_hull_range"] is False
        and m38["nC"] == LIVE_17057305[-1] - LIVE_17057305[0] + 1
        and m38["C"] > m38["nC"] - 1
        and m38["engine_L"] == 35
    )

    pat9 = (1 << 9) - 1
    s9, C9 = 8, 4
    m9 = _multi_matches_packed(pat9, s9, C9)
    live9 = live_from(pat9, s9, C9)
    checks["multi_wt9_full"] = m9
    checks["multi_wt9_full_ok"] = bool(m9["ok"])
    checks["wt9_full_wt_ok"] = popcount(pat9) == 9
    checks["wt9_full_in_hull_ok"] = in_hull(live9) is True
    checks["wt9_full_span_ok"] = span_of_live(live9) == 8

    pat10 = (1 << 10) - 1
    s10, C10 = 9, 5
    m10 = _multi_matches_packed(pat10, s10, C10)
    live10 = live_from(pat10, s10, C10)
    checks["multi_wt10_full"] = m10
    checks["multi_wt10_full_ok"] = bool(m10["ok"])
    checks["wt10_full_wt_ok"] = popcount(pat10) == 10
    checks["wt10_full_in_hull_ok"] = in_hull(live10) is True
    checks["wt10_full_span_ok"] = span_of_live(live10) == 9

    rng = random.Random(20260911)
    hull_ok = True
    hull_n = 0
    hull_fail = None
    off_ok = True
    off_n = 0
    for _ in range(12):
        wt = rng.choice([WT_MIN, WT_MAX])
        s = rng.randint(wt - 1, min(SPAN_MAX, 16))
        interiors = sorted(rng.sample(range(1, s), wt - 2)) if s > 1 else []
        pat = 1 | (1 << s)
        for i in interiors:
            pat |= 1 << i
        i_best, bestL, best_start, nC, tcapC = _scan_pattern(pat, s)
        if nC != s + 1:
            hull_ok = False
            hull_fail = {"nC": nC, "s": s}
            break
        for C in range(s + 1):
            live = live_from(pat, s, C)
            hull_n += 1
            if not in_hull(live):
                hull_ok = False
                hull_fail = {"C": C, "s": s, "live": live, "expected": "in_hull"}
                break
            got = _multi_matches_packed(pat, s, C)
            if not got["ok"]:
                hull_ok = False
                hull_fail = got
                break
        if not hull_ok:
            break
        for C in (-s, -1, s + 1, 2 * s):
            live = live_from(pat, s, C)
            off_n += 1
            if in_hull(live):
                off_ok = False
                hull_fail = {"C": C, "s": s, "live": live, "expected": "off_hull"}
                break
            if 0 <= C < nC:
                off_ok = False
                break
        if not off_ok:
            break
    checks["hull_random_n"] = hull_n
    checks["hull_random_ok"] = hull_ok
    checks["offhull_random_n"] = off_n
    checks["offhull_random_ok"] = off_ok
    if hull_fail:
        checks["hull_random_fail"] = hull_fail

    pat, s, C = _pattern_of_live(LIVE_4369552)
    w_p, m_p = pack_from(pat, s, C)
    checks["pack_4369552_ok"] = w_p == 11 and m_p == MASK_4369552
    pat17, s17, C17 = _pattern_of_live(LIVE_281769)
    w17p, m17p = pack_from(pat17, s17, C17)
    checks["pack_281769_ok"] = w17p == 17 and m17p == MASK_281769
    checks["hull_C_range_281769_ok"] = 0 <= C17 <= s17
    checks["nC_equals_s_plus_1"] = _scan_pattern(pat17, s17)[3] == s17 + 1

    bool_keys = [
        "w11_L29_ok",
        "w11_live_ok",
        "w11_span_ok",
        "w11_wt_ok",
        "w11_in_hull_ok",
        "w17_L31_ok",
        "w17_live_ok",
        "w17_span_ok",
        "w17_wt_ok",
        "w17_not_in_wt910_ok",
        "w17_in_hull_ok",
        "w17_missed_by_8w128",
        "w17_census_ok",
        "w6_run24_ok",
        "offhull_live_ok",
        "offhull_wt_ok",
        "offhull_span_ok",
        "offhull_all_live_lt_0",
        "offhull_in_hull_ok",
        "offhull_pack_ok",
        "offhull_C_outside_hull",
        "offhull_L35_ok",
        "offhull_excluded_ok",
        "fast_matches_scan_mask_runs",
        "packed_matches_naive_prize",
        "packed_matches_naive_4369552",
        "packed_matches_naive_281769",
        "rule30_step_formula",
        "multi_4369552_ok",
        "multi_281769_ok",
        "multi_17057305_excluded_ok",
        "multi_wt9_full_ok",
        "wt9_full_wt_ok",
        "wt9_full_in_hull_ok",
        "wt9_full_span_ok",
        "multi_wt10_full_ok",
        "wt10_full_wt_ok",
        "wt10_full_in_hull_ok",
        "wt10_full_span_ok",
        "hull_random_ok",
        "offhull_random_ok",
        "pack_4369552_ok",
        "pack_281769_ok",
        "hull_C_range_281769_ok",
        "nC_equals_s_plus_1",
    ]
    checks["all_ok"] = all(checks[k] is True for k in bool_keys)
    return checks


def census_membership(merged: dict | None = None) -> dict:
    """281769 is in-hull L=31 but wt=8, so this wt=9/10 census excludes it."""
    out: dict = {}
    ge30 = (merged or {}).get("ge30") or []
    ge_keys = {(r["w"], r["mask"]) for r in ge30}
    best = (merged or {}).get("best")

    def listed(w: int, mask: int) -> bool:
        return (w, mask) in ge_keys or (
            best is not None and best.get("mask") == mask and best.get("w") == w
        )

    for tag, live, mask, w, Lexp, expect_hull in (
        ("4369552", LIVE_4369552, MASK_4369552, 11, 29, True),
        ("281769", LIVE_281769, MASK_281769, 17, 31, True),
        ("17057305", LIVE_17057305, MASK_17057305, 38, 35, False),
    ):
        pat, s, C = _pattern_of_live(live)
        hull = in_hull(list(live))
        in_range = 0 <= C <= s
        rec = None
        if in_range:
            _i, bestL, best_start, _nC, tcapC = _scan_pattern(pat, s)
            rec = rec_of(
                pat, s, C, bestL[C], best_start[C], best_start[C] + bestL[C], tcapC[C]
            )
        wt = popcount(mask)
        slot = {
            "in_hull": hull,
            "C_in_0_s": in_range,
            "wt": wt,
            "span": s,
            "C": C,
            "w": None if rec is None else rec["w"],
            "mask": None if rec is None else rec["mask"],
            "L": None if rec is None else rec["L"],
            "start": None if rec is None else rec["start"],
            "end": None if rec is None else rec["end"],
            "L_expected": Lexp,
            "must_include": False,
            "excluded_because_wt8": wt == 8,
            "in_ge30": (w, mask) in ge_keys if merged is not None else None,
            "is_best": (
                best is not None and best.get("mask") == mask and best.get("w") == w
                if merged is not None
                else None
            ),
        }
        if expect_hull:
            slot["ok"] = (
                hull
                and in_range
                and rec is not None
                and rec["mask"] == mask
                and rec["w"] == w
                and rec["L"] >= Lexp
                and rec["in_hull"] is True
                and wt == 8
            )
        else:
            slot["ok"] = (
                (not hull)
                and (not in_range)
                and rec is None
                and all(x < 0 for x in live)
                and wt == 8
            )
        out[tag] = slot
    out["ok"] = out["4369552"]["ok"] and out["281769"]["ok"] and out["17057305"]["ok"]
    if merged is not None:
        out["census_excludes_281769"] = not listed(17, MASK_281769)
        out["census_excludes_4369552"] = not listed(11, MASK_4369552)
        out["census_excludes_17057305"] = not listed(38, MASK_17057305)
        best_wt = None if best is None else best.get("n1")
        out["census_wt_in_9_10"] = True if best is None else best_wt in (9, 10)
        out["ok"] = (
            out["ok"]
            and out["census_excludes_281769"]
            and out["census_excludes_4369552"]
            and out["census_excludes_17057305"]
            and out["census_wt_in_9_10"]
        )
    return out


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def _fmt(n: int | None) -> str:
    if n is None:
        return "—"
    return f"{n:,}"


def _mask_cell(row: dict) -> str:
    m = row.get("best_mask")
    if m is None:
        return "—"
    if int(m).bit_length() > 40:
        live = row.get("best_live")
        if live:
            return "`" + ",".join(str(x) for x in live) + "`"
    return _fmt(m)


def write_markdown(dump: dict) -> str:
    a: list[str] = []

    def p(s: str = "") -> None:
        a.append(s)

    p("# Period-2 `L_run`: origin-in-hull weight-9/10 span-20 census")
    p()
    p("This note extends Cycle M (`research/period2_hull.md`). It does")
    p("**not** exclude eventual period 2 for every finite row, and it does")
    p("not claim a prize result. It is a finite census of Hamming weights")
    p("`9` and `10` and span `≤20` with the origin in the live convex hull,")
    p("not a uniform-in-`w` bound.")
    p()
    p("Helper: `research/period2_hull910.py --certify`. Dump:")
    p("`research/period2_hull910.json`. Packed evolution is imported from")
    p("`research/period2_fiber.py` and that file is not modified.")
    p("`research/period2_hull.py` is not modified.")
    p()
    p("## Attack")
    p()
    p("Cycle M proved `L≤31` for every in-hull weight-`≤8` span-`≤24` row")
    p("at `tcap=32w+512`. The prize seed’s later rows have larger weight.")
    p("ideas13 item 1 asks for the same origin-in-hull census at weights")
    p("`9` and `10`, span `≤20` (state space comparable to Cycle M), with")
    p()
    p("```")
    p("min(live) <= 0 <= max(live)")
    p("```")
    p()
    p("Each combinatorial support still sits on `[0,s]` with live endpoints.")
    p("In-hull is then `C ∈ [0,s]` (`s+1` centres), not Cycle L’s window")
    p("`C ∈ [-s, 2s]` (`3s+1` centres). Cap `tcap=32w+512` of the true")
    p("radius of that placement. Any `L≥30` row is re-evolved at `2·tcap`.")
    p()
    p("**Kill:** an in-hull weight-`9` or `10` span-`≤20` row with a")
    p("period-2 centre run of length `≥32` after doubling `tcap`.")
    p()
    p("**Finite theorem (this class only):** every in-hull weight-`9` or")
    p("`10` span-`≤20` row has `L≤31`.")
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
    p("## Self-checks")
    p()
    ch = dump["checks"]
    p(f"- `w=11` mask `4369552`, `tcap=8·11+128=216`: `L={ch['w11_L']}` from")
    p(f"  `t={ch['w11_start']}` to `t={ch['w11_end']}`. Live cells")
    p(f"  `{', '.join(str(x) for x in ch['w11_live'])}`. Weight 8, span 18,")
    p(f"  origin in hull (`min={ch['w11_live'][0]}`, `max={ch['w11_live'][-1]}`).")
    p("  Not in this census (weight 8).")
    p(f"- `w=17` mask `281769`, `tcap=8·17+256={ch['w17_tcap_8w256']}`:")
    p(f"  `L={ch['w17_L']}` from `t={ch['w17_start']}` to `t={ch['w17_end']}`.")
    p(f"  Live `{', '.join(str(x) for x in ch['w17_live'])}`. In-hull")
    p(f"  (`min={ch['w17_live'][0]} ≤ 0 ≤ {ch['w17_live'][-1]}`). Census cap")
    p(f"  `32·17+512={ch['w17_census_tcap']}` still has `L={ch['w17_census_L']}`.")
    p("  Weight 8, span 18: **not** in this wt=9/10 census. The packed")
    p("  engine is unchanged.")
    p(f"- `w=38` mask `17057305`: live")
    p(f"  `{', '.join(str(x) for x in ch['offhull_live'])}`. All live `< 0`,")
    p(f"  origin off-hull, `C={ch['offhull_C']}` not in `[0, {ch['offhull_s']}]`.")
    p(f"  Packed engine still gives `L={ch['offhull_L']}` at `tcap=32·38+512`;")
    p("  excluded here by weight 8 and by the hull filter.")
    p("- Full-ones weight-9 span-8 and weight-10 span-9 supports match the")
    p("  packed engine at an in-hull centre.")
    p("- Inlined inner loop agrees with `period2_fiber.scan_mask_runs`.")
    p("- Packed traces match the independent live-cell spacetime on the prize")
    p("  seed, on mask `4369552`, and on mask `281769`.")
    p("- Multi-centre extraction of a canonical support agrees with the packed")
    p("  engine on the Cycle M in-hull maximizers. Hull scan `nC=s+1` does")
    p("  not contain the off-hull centre of mask `17057305`.")
    p("- Random in-hull centres of weight 9/10 (`C in [0,s]`) satisfy")
    p("  `min≤0≤max` and match the packed engine; random `C` outside `[0,s]`")
    p("  are off-hull.")
    p(f"- `checks.all_ok={ch['all_ok']}`.")
    p()
    p("## Census")
    p()
    cen = dump["census"]
    p(
        f"`{_fmt(cen['n_patterns'])}` combinatorial supports, "
        f"`{_fmt(cen['n_place'])}` in-hull placements (`C in [0,s]`), "
        f"`tcap=32w+512`, `{cen['nproc']}` processes, "
        f"{cen['elapsed_sec']:.1f}s."
    )
    p()
    p("Span here is `maxlive-minlive`. Cycle L’s off-hull window used")
    p("`3s+1` translations; this census uses `s+1`.")
    p()
    p("| `wt` | types | placements | `L_run` | `n≥30` | `n≥31` | `n≥32` | best | `w` | span |")
    p("|-----:|------:|-----------:|--------:|-------:|-------:|-------:|-----:|----:|-----:|")
    for row in cen["by_wt_table"]:
        span_b = "—"
        if row["best_live"]:
            span_b = str(row["best_live"][-1] - row["best_live"][0])
        p(
            f"| {row['wt']} | {_fmt(row['n_patterns'])} | {_fmt(row['n_place'])} | "
            f"**{row['L_run']}** | {_fmt(row['n_ge30'])} | {_fmt(row['n_ge31'])} | "
            f"{_fmt(row['n_ge32'])} | {_mask_cell(row)} | {_fmt(row['best_w'])} | "
            f"{span_b} |"
        )
    p()
    p("| span | types | placements | `L_run` | `n≥30` | `n≥31` | `n≥32` | best | `w` |")
    p("|-----:|------:|-----------:|--------:|-------:|-------:|-------:|-----:|----:|")
    for row in cen["by_span_table"]:
        p(
            f"| {row['span']} | {_fmt(row['n_patterns'])} | {_fmt(row['n_place'])} | "
            f"**{row['L_run']}** | {_fmt(row['n_ge30'])} | {_fmt(row['n_ge31'])} | "
            f"{_fmt(row['n_ge32'])} | {_mask_cell(row)} | {_fmt(row['best_w'])} |"
        )
    p()
    Ls = cen["span_L"]
    p(
        "Max `L` versus span: "
        + ", ".join(f"{s}:{Ls[s]}" for s in range(len(Ls)))
        + "."
    )
    p()
    p(
        f"Off-hull placements scored: `{cen.get('n_off_hull', 0)}` "
        "(must be 0; every scanned centre is `C in [0,s]`)."
    )
    p()
    p("## Witness")
    p()
    best = dump.get("best") or {}
    vc = dump.get("witness_check") or {}
    live = best.get("live") or []
    p("Least true-radius maximizer of the in-hull census:")
    p()
    p(f"- true radius `{best.get('w')}`, mask `{best.get('mask')}`")
    p(f"- packed row (bit 0 = spatial `-{best.get('w')}`): `{best.get('row')}`")
    p(
        f"- live at `{', '.join(str(x) for x in live)}` "
        f"({best.get('n1')} ones, span {best.get('span')})"
    )
    p(
        f"- origin in the live hull: `{in_hull(live)}` "
        f"(min={live[0] if live else '—'}, max={live[-1] if live else '—'})"
    )
    p(
        f"- run of {best.get('L')} from `t={best.get('start')}` to "
        f"`t={best.get('end')}` (exclusive end)"
    )
    if vc:
        dbl = best.get("doubled") or {}
        p(f"- run bits `{vc.get('run_bits')}`")
        p(
            f"- bits immediately before and after: `{vc.get('break_before')}`, "
            f"`{vc.get('break_after')}`"
        )
        same = (
            vc.get("L") == dbl.get("L") and vc.get("start") == dbl.get("start")
        )
        if same:
            p(
                f"- `tcap={best.get('tcap')}` and doubled `tcap={dbl.get('tcap')}` "
                f"both give `(L,start,end)="
                f"({vc.get('L')},{vc.get('start')},{vc.get('end')})`"
            )
        else:
            p(
                f"- `tcap={best.get('tcap')}` gives "
                f"(L,start,end)=({vc.get('L')},{vc.get('start')},{vc.get('end')}); "
                f"doubled `tcap={dbl.get('tcap')}` gives "
                f"(L,start,end)=({dbl.get('L')},{dbl.get('start')},{dbl.get('end')})"
            )
        p(
            f"- packed, fast loop, and naive spacetime agree "
            f"(`witness_check.ok={vc.get('ok')}`)"
        )
    p()
    cc = dump.get("true_radius_best_cap") or {}
    if cc:
        p(
            f"Cycle J cap `8w+128={cc.get('tcap_8w128')}` reports "
            f"`L={cc.get('L_8w128')}`"
            + (" (truncated)." if cc.get("truncated_by_8w128") else ".")
        )
        p(
            f"Cycle K cap `8w+256={cc.get('tcap_8w256')}` reports "
            f"`L={cc.get('L_8w256')}`. Census `32w+512={cc.get('tcap_census')}` "
            f"reports `L={cc.get('L_census')}`; doubled "
            f"`{cc.get('tcap_doubled')}` reports `L={cc.get('L_doubled')}`."
        )
        p()
    known = dump.get("known_in_census") or {}
    if known:
        p("Known Cycle M rows. All have weight 8, so none enter this census:")
        p()
        for tag in ("4369552", "281769", "17057305"):
            r = known.get(tag) or {}
            if tag == "281769":
                p(
                    f"- mask `{tag}`: w={r.get('w')} L={r.get('L')} "
                    f"(engine expected 31), span {r.get('span')}, wt="
                    f"{r.get('wt')}, in-hull={r.get('in_hull')}, excluded "
                    f"from this census, ok={r.get('ok')}"
                )
            elif tag == "17057305":
                p(
                    f"- mask `{tag}`: in-hull={r.get('in_hull')}, "
                    f"`C={r.get('C')}` not in `[0,s]`, wt={r.get('wt')}, "
                    f"excluded, ok={r.get('ok')}"
                )
            else:
                p(
                    f"- mask `{tag}`: w={r.get('w')} L={r.get('L')} "
                    f"(expected ≥{r.get('L_expected')}), span {r.get('span')}, "
                    f"wt={r.get('wt')}, in-hull={r.get('in_hull')}, excluded, "
                    f"ok={r.get('ok')}"
                )
        if known.get("census_excludes_281769") is not None:
            p(
                f"- census_excludes_281769="
                f"{known.get('census_excludes_281769')}"
            )
        p()
    ge32 = [r for r in (cen.get("ge30") or []) if r.get("L", 0) >= 32]
    ge31 = [r for r in (cen.get("ge30") or []) if r.get("L", 0) >= 31]
    if ge32:
        p(f"`L≥32` in-hull rows (unique `(w,mask)`): {len(ge32)}.")
        p()
        p("| `L` | `w` | mask | span | live min..max | start | end | doubled L |")
        p("|----:|----:|-----:|-----:|--------------:|------:|----:|----------:|")
        for r in ge32:
            live_r = r.get("live") or [0]
            p(
                f"| {r['L']} | {r['w']} | {r['mask']} | {r['span']} | "
                f"{live_r[0]}..{live_r[-1]} | {r['start']} | {r['end']} | "
                f"{(r.get('doubled') or {}).get('L')} |"
            )
        p()
    elif ge31:
        p(
            f"`L≥31` in-hull rows (unique `(w,mask)`): {len(ge31)}. "
            "None reach `L≥32`."
        )
        p()
        p("| `L` | `w` | mask | span | live min..max | start | end | doubled L |")
        p("|----:|----:|-----:|-----:|--------------:|------:|----:|----------:|")
        for r in ge31:
            live_r = r.get("live") or [0]
            p(
                f"| {r['L']} | {r['w']} | {r['mask']} | {r['span']} | "
                f"{live_r[0]}..{live_r[-1]} | {r['start']} | {r['end']} | "
                f"{(r.get('doubled') or {}).get('L')} |"
            )
        p()
    p("These are finite bursts, not eventual period 2: none of the")
    p("recorded `L≥30` rows reaches the cap after doubling.")
    p()
    p("## What is proved, what is not")
    p()
    p("Proved (machine-checked in this run):")
    p()
    p("- The Cycle I packed engine, on every finite row of Hamming weight")
    p(f"  `9` or `10` and span `≤{SPAN_MAX}` with the origin in the live")
    p("  convex hull (`min(live)≤0≤max(live)`, `s+1` translations),")
    p("  produces a longest period-2 centre run of length")
    p(f"  `L_run={dump.get('best_L')}` inside `tcap=32w+512`.")
    p("- Self-checks as above, including engine `L=31` on in-hull `w=17`")
    p("  mask `281769` (weight 8, **not** in this census), and exclusion")
    p("  of off-hull `w=38` mask `17057305` (`L=35`, all live `< 0`).")
    p("- Every `L≥30` candidate was re-evolved at `2·tcap`.")
    if dump.get("finite_theorem"):
        p("- Every such in-hull row has `L≤31` at `tcap` and after doubling.")
    else:
        p("- An in-hull row with `L≥32` after doubling is a kill for `L≤31`.")
    p()
    p("Not proved:")
    p()
    p("- A bound for weight `>10` or span `>20`.")
    p("- A bound for off-hull placements (Cycle L already found `L=35`).")
    p("- Eventual period 2 of any finite seed. A bounded burst is")
    p("  compatible with every centre eventually leaving period 2.")
    p("- A uniform-in-`w` theorem.")
    p()
    p("## Verdict")
    p()
    p(f"`{dump['verdict']}`, wall time {dump['wall_time_sec']:.1f}s.")
    p()
    p(f"- Reason: {dump['reason']}")
    p(f"- `L≥32` after doubling: {'yes' if dump.get('found_L_ge_32') else 'no'}.")
    p(
        f"- Finite theorem `L≤31` on in-hull weight 9–10 span≤20: "
        f"{'yes' if dump.get('finite_theorem') else 'no'}."
    )
    p("- Survive / uniform proof: no.")
    p()
    p("## Files")
    p()
    p("- `research/period2_hull910.md` (this note)")
    p("- `research/period2_hull910.py` (`--certify` runs the checks and the")
    p("  in-hull weight-9/10 span-20 census)")
    p("- `research/period2_hull910.json` (dump)")
    p()
    return "\n".join(a) + "\n"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def certify() -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    print(log[-1], flush=True)
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    known = census_membership(None)
    log.append(
        f"known 4369552 L={known['4369552']['L']} wt={known['4369552']['wt']} "
        f"281769 L={known['281769']['L']} wt={known['281769']['wt']} "
        f"17057305 excluded={known['17057305']['ok']} ok={known['ok']}"
    )
    print(log[-1], flush=True)
    if not known["ok"]:
        raise AssertionError(f"known rows failed: {known}")

    census = run_census(log)

    known = census_membership(census)
    log.append(
        f"census membership excludes_281769={known.get('census_excludes_281769')} "
        f"excludes_17057305={known.get('census_excludes_17057305')} "
        f"ok={known['ok']}"
    )
    print(log[-1], flush=True)
    if not known["ok"]:
        raise AssertionError(f"census membership failed: {known}")

    if census.get("n_off_hull", 0) != 0:
        raise AssertionError(f"off-hull placements scored: {census['n_off_hull']}")
    if census.get("best") is not None and not in_hull(census["best"].get("live") or []):
        raise AssertionError(f"best row is off-hull: {census['best']}")
    if census.get("best") is not None:
        bn1 = census["best"].get("n1")
        bspan = census["best"].get("span")
        if bn1 not in (WT_MIN, WT_MAX):
            raise AssertionError(f"best row weight {bn1} not in {WT_MIN, WT_MAX}")
        if bspan is None or bspan > SPAN_MAX:
            raise AssertionError(f"best row span {bspan} exceeds {SPAN_MAX}")

    best = census["best"]
    L_best = 0 if best is None else best["L"]
    L_double = census.get("L_after_double_max") or 0
    if best is not None:
        Ld = (best.get("doubled") or {}).get("L") or 0
        if Ld > L_double:
            L_double = Ld
    L_report = max(L_best, L_double)

    found_ge32 = L_report >= 32 or census.get("n_ge32", 0) > 0 or L_double >= 32
    finite = L_report <= 31 and not found_ge32

    if found_ge32:
        verdict = "KILL"
        reason = (
            f"an in-hull weight-9 or 10 span<=20 row has a period-2 centre "
            f"run of length {L_report}>=32 (tcap=32w+512, still holds after "
            "doubling). The census kills a bound L<=31 on origin-in-hull "
            "supports of this class. The run is a finite burst unless it "
            "reaches the cap. This does not exclude eventual period 2, and "
            "it is not a uniform-in-w theorem."
        )
    elif finite:
        verdict = "FINITE_THEOREM"
        reason = (
            f"every finite row of Hamming weight 9 or 10 and span "
            f"(maxlive-minlive)<=20 with the origin in the live convex hull "
            f"(min(live)<=0<=max(live); C in [0,s]), has a longest period-2 "
            f"centre run of length L<={L_best} inside tcap=32w+512. Any "
            f"L>=30 row still has L>=30 and L<32 after doubling tcap. Mask "
            f"281769 (w=17, wt=8, span=18) is in-hull with engine L=31 but "
            f"is not in this census. This is a finite theorem for those "
            f"supports only, not a uniform-in-w bound, and not an exclusion "
            f"of eventual period 2."
        )
    else:
        verdict = "L_GT_31"
        reason = (
            f"best L on the in-hull census is {L_report}. No consistent "
            f"L>=32 kill after doubling; finite theorem L<=31 is false."
        )

    witness_check = None
    cap = None
    if best is not None:
        witness_check = verify_row(best["mask"], best["w"], best["tcap"])
        log.append(
            f"witness_check ok={witness_check['ok']} L={witness_check['L']} "
            f"doubled={witness_check['doubled_L']} alt={witness_check['alternating']} "
            f"in_hull={witness_check['in_hull']}"
        )
        print(log[-1], flush=True)
        if not witness_check["ok"] or not witness_check["in_hull"]:
            raise AssertionError(f"best-row verification failed: {witness_check}")
        cap = cap_compare(best["mask"], best["w"])
        best["cap_compare"] = cap
        best["verify"] = witness_check

    ge30_out = []
    n30_only = 0
    for r in census.get("ge30") or []:
        if not in_hull(r.get("live") or []):
            continue
        if r["L"] >= 31:
            ge30_out.append(slim_rec(r))
        else:
            n30_only += 1
            if n30_only <= 8:
                ge30_out.append(slim_rec(r))

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period2_hull910",
        "ideas13": "item 1",
        "cycle_m": "research/period2_hull.md",
        "cycle_l": "research/period2_weight8.md",
        "cycle_k": "research/period2_lrun_family.md",
        "cycle_j": "research/period2_lrun.md",
        "problem": (
            "census finite rows of Hamming weight 9 and 10 and span "
            "(maxlive-minlive)<=20 with origin in the live convex hull "
            "(min(live)<=0<=max(live)) at tcap=32w+512; kill on in-hull "
            "L>=32 after doubling tcap; finite theorem if every such row "
            "has L<=31. Mask 281769 (wt=8) is not in this census; engine "
            "still gives L=31 for it."
        ),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": False,
        "uniform_proof": False,
        "finite_theorem": finite,
        "found_L_ge_30": L_report >= 30,
        "found_L_ge_32": found_ge32,
        "found_L_ge_40": L_report >= 40,
        "best_L": L_report,
        "best_L_tcap": L_best,
        "best_origin_in_hull": in_hull((best or {}).get("live") or []),
        "reason": reason,
        "tcap": "32w+512",
        "span_def": "maxlive-minlive",
        "span_max": SPAN_MAX,
        "wt_min": WT_MIN,
        "wt_max": WT_MAX,
        "placement": "min(live)<=0<=max(live); C in [0,s]; s+1 centres",
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "known_in_census": known,
        "witness_check": witness_check,
        "best": slim_rec(best),
        "true_radius_best_cap": cap,
        "census": {
            "n_patterns": census["n_patterns"],
            "n_patterns_expected": census.get("n_patterns_expected"),
            "n_place": census["n_place"],
            "n_ge30": census["n_ge30"],
            "n_ge31": census["n_ge31"],
            "n_ge32": census["n_ge32"],
            "n_ge40": census["n_ge40"],
            "ge30_hold_fail": census["ge30_hold_fail"],
            "n_off_hull": census["n_off_hull"],
            "L_run": census["L_run"],
            "L_after_double_max": census["L_after_double_max"],
            "elapsed_sec": census["elapsed_sec"],
            "nproc": census["nproc"],
            "n_tasks": census["n_tasks"],
            "by_wt_table": census["by_wt_table"],
            "by_span_table": census["by_span_table"],
            "span_L": census["span_L"],
            "hull_len_table": census["hull_len_table"],
            "ge30": ge30_out,
        },
        "not_a_prize_claim": True,
        "log": log,
    }
    OUT_JSON.write_text(json.dumps(dump, indent=2) + "\n")
    OUT_MD.write_text(write_markdown(dump))
    print(f"wrote {OUT_JSON}", flush=True)
    print(f"wrote {OUT_MD}", flush=True)
    print(f"verdict={verdict} best_L={L_report} wall={wall:.3f}s", flush=True)
    print(f"reason: {reason}", flush=True)
    print(f"L vs wt: {[(r['wt'], r['L_run']) for r in census['by_wt_table']]}", flush=True)
    print(f"L vs span: {census['span_L']}", flush=True)
    return dump


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--certify", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    certify()


if __name__ == "__main__":
    main()
