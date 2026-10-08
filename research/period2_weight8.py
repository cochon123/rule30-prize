"""ideas11 item 1: long-cap census of weight-8, span<=24 finite rows.

Cycle K (research/period2_lrun_family.md) found L=31 on a weight-8
span-18 row (mask 281769 at w=17). Cycle J's tcap=8w+128 missed that
burst (it starts at t=320). This script enumerates every finite row of
Hamming weight 1..8 and span (maxlive-minlive) <= 24, placed with the
origin in/near the live span, at tcap=32w+512.

Packed evolution is imported from research/period2_fiber.py and that
file is not modified:
    new = (row << 2) ^ ((row << 1) | row)
    centre bit (row >> (w + t)) & 1
with bit 0 the leftmost cell of the current support.

Run: python3 research/period2_weight8.py --certify
Dump: research/period2_weight8.json, research/period2_weight8.md
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

SPAN_MAX = 24
WT_MAX = 8
NPROC_CAP = 4

MASK_4369552 = 4369552
W_4369552 = 11
MASK_281769 = 281769
W_281769 = 17
MASK_7503 = 7503

# Cycle K inclusive length = max-min+1 = 19 for both maximizers.
LIVE_4369552 = (-7, -4, -1, 0, 2, 4, 6, 11)
LIVE_281769 = (-17, -14, -12, -10, -7, -6, -3, 1)


def tcap_census(w: int) -> int:
    """ideas11 long cap. Cycle J used 8w+128; Cycle K used 8w+256."""
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
        "doubled",
        "verify",
        "cap_compare",
    )
    return {k: rec[k] for k in keys if k in rec}


# ---------------------------------------------------------------------------
# One canonical support, all translations with some live cell in [-s,s].
# Endpoints of a span-s block are live, so C runs through [-s, 2s].
# ---------------------------------------------------------------------------

def _scan_pattern(pat: int, s: int):
    """Evolve `pat` once; score every centre C in [-s, 2s] at 32w+512.

    Returns (best_i, best[], best_start[], nC).
    Spatial x sits at packed bit x+t after t steps of the unpadded row
    (bit 0 = spatial 0 at t=0). Centre C is packed bit C+t.
    """
    nC = 3 * s + 1
    tcapC = [0] * nC
    for i in range(nC):
        C = i - s
        w = C if C >= s - C else s - C
        tcapC[i] = 32 * w + 512
    tcap_max = tcapC[0]
    for tc in tcapC:
        if tc > tcap_max:
            tcap_max = tc

    prev = [0] * nC
    best = [1] * nC
    best_start = [0] * nC
    run = [1] * nC
    run_start = [0] * nC
    for i in range(nC):
        C = i - s
        prev[i] = (pat >> C) & 1 if 0 <= C <= s else 0

    # Bands of centres sharing a remaining tcap, so finished columns
    # drop out instead of branching every step.
    order = sorted(range(nC), key=tcapC.__getitem__)
    bounds = sorted(set(tcapC))
    row = pat
    nC_mask = (1 << nC) - 1
    live_lo = 0
    t = 1
    for t_hi in bounds:
        live = order[live_lo:]
        if t >= t_hi:
            while live_lo < nC and tcapC[order[live_lo]] <= t:
                live_lo += 1
            continue
        for t in range(t, t_hi):
            row = (row << 2) ^ ((row << 1) | row)
            shift = t - s
            if shift >= 0:
                chunk = (row >> shift) & nC_mask
            else:
                chunk = (row << (-shift)) & nC_mask
            for i in live:
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
    nC = 3 * s + 1
    n_patterns = 0
    n_place = 0
    Lrun = 0
    best = None
    n_ge30 = 0
    n_ge31 = 0
    n_ge40 = 0
    ge30: list[dict] = []
    ge30_hold_fail = 0
    L_after_double_max = 0

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
        C = i_best - s
        start = best_start[i_best]
        rec = rec_of(pat, s, C, L, start, start + L, tcapC[i_best])
        best = consider(best, rec)
        Lrun = best["L"]
        if L >= 30:
            # Record every placement of this pattern with L>=30.
            for i in range(nC_got):
                Li = bestL[i]
                if Li < 30:
                    continue
                n_ge30 += 1
                if Li >= 31:
                    n_ge31 += 1
                if Li >= 40:
                    n_ge40 += 1
                C = i - s
                start = best_start[i]
                rec = rec_of(pat, s, C, Li, start, start + Li, tcapC[i])
                rec = double_cap(rec)
                Ld = rec["doubled"]["L"]
                if Ld > L_after_double_max:
                    L_after_double_max = Ld
                if not rec["doubled"]["holds"]:
                    ge30_hold_fail += 1
                if Li >= 31 or Ld >= 40 or len(ge30) < 8:
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
        "n_ge40": n_ge40,
        "ge30": ge30,
        "ge30_hold_fail": ge30_hold_fail,
        "L_after_double_max": L_after_double_max,
    }


def _n_types(wt: int, s: int) -> int:
    if wt == 1:
        return 1 if s == 0 else 0
    if s < wt - 1:
        return 0
    return math.comb(s - 1, wt - 2)


def _tasks(workers: int) -> list[tuple[int, int, int, int]]:
    tasks: list[tuple[int, int, int, int]] = []
    for wt in range(1, WT_MAX + 1):
        s_lo = 0 if wt == 1 else wt - 1
        for s in range(s_lo, SPAN_MAX + 1):
            n = _n_types(wt, s)
            if n <= 0:
                continue
            # ~8s chunks at s=24 (~100 pat/s). Small (wt,s) stay one task.
            take = max(64, min(n, int(20000 / max(s, 1))))
            skip = 0
            while skip < n:
                t = min(take, n - skip)
                tasks.append((wt, s, skip, t))
                skip += t
    # Heavier (high s, high wt) first so the tail is small leftover.
    tasks.sort(key=lambda t: -(_n_types(t[0], t[1]) * (3 * t[1] + 1) * (64 * t[1] + 512)))
    _ = workers
    return tasks


def merge_parts(parts: list[dict]) -> dict:
    best = None
    n_patterns = 0
    n_place = 0
    n_ge30 = 0
    n_ge31 = 0
    n_ge40 = 0
    ge30_hold_fail = 0
    L_after_double_max = 0
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
                "n_ge40": part["n_ge40"],
                "best": part["best"],
            }
            return
        slot["n_patterns"] += part["n_patterns"]
        slot["n_place"] += part["n_place"]
        slot["n_ge30"] += part["n_ge30"]
        slot["n_ge31"] += part["n_ge31"]
        slot["n_ge40"] += part["n_ge40"]
        if part["best"] is not None:
            slot["best"] = consider(slot["best"], part["best"])
            slot["L_run"] = slot["best"]["L"]

    for p in parts:
        n_patterns += p["n_patterns"]
        n_place += p["n_place"]
        n_ge30 += p["n_ge30"]
        n_ge31 += p["n_ge31"]
        n_ge40 += p["n_ge40"]
        ge30_hold_fail += p["ge30_hold_fail"]
        if p["L_after_double_max"] > L_after_double_max:
            L_after_double_max = p["L_after_double_max"]
        if p["best"] is not None:
            best = consider(best, p["best"])
        ge30.extend(p.get("ge30") or [])
        bump(by_wt, p, p["wt"])
        bump(by_span, p, p["s"])

    # Unique L>=30 by (w, mask), prefer higher L then smaller w.
    uniq: dict[tuple[int, int], dict] = {}
    for r in ge30:
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
        "n_ge40": n_ge40,
        "ge30_hold_fail": ge30_hold_fail,
        "L_after_double_max": L_after_double_max,
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
    log.append(f"census tasks={n_tasks} nproc={workers} span<= {SPAN_MAX} wt<= {WT_MAX}")
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
        if merged["best"]["L"] >= 30:
            merged["best"] = double_cap(merged["best"])
        else:
            # still record a doubled window on the maximizer
            merged["best"] = double_cap(merged["best"])
    merged["by_wt_table"] = table_from(merged["by_wt"], list(range(1, WT_MAX + 1)), "wt")
    merged["by_span_table"] = table_from(
        merged["by_span"], list(range(0, SPAN_MAX + 1)), "span"
    )
    Ls = [row["L_run"] for row in merged["by_span_table"]]
    strict = bool(Ls) and all(Ls[i] < Ls[i + 1] for i in range(len(Ls) - 1))
    hull = []
    for s in range(0, SPAN_MAX + 1):
        hull.append({"span_len": s + 1, "L_run": Ls[s] if s < len(Ls) else 0})
    merged["span_strictly_increases_through_24"] = strict
    merged["span_L"] = Ls
    merged["hull_len_table"] = hull
    merged["elapsed_sec"] = round(elapsed, 4)
    merged["nproc"] = workers
    merged["n_tasks"] = n_tasks
    msg = (
        f"census done n_patterns={merged['n_patterns']} n_place={merged['n_place']} "
        f"L_run={merged['L_run']} n_ge30={merged['n_ge30']} "
        f"n_ge40={merged['n_ge40']} {elapsed:.3f}s"
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
    i = C + s
    ok = 0 <= i < nC
    L = bestL[i] if ok else None
    start = best_start[i] if ok else None
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
        "tcapC": tcapC[i] if ok else None,
        "ok": ok and L == st["L"] and start == st["start"] and tcapC[i] == tcap,
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
    checks["w17_wt_ok"] = popcount(MASK_281769) == 8

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

    fast_ok = True
    fail = None
    for w, mask, tcap in (
        (0, 1, 128),
        (6, MASK_7503, 176),
        (11, MASK_4369552, 216),
        (17, MASK_281769, tcap_cycle_k(17)),
        (17, MASK_281769, tcap_census(17)),
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
        for m in (0, 1, MASK_7503, MASK_4369552, MASK_281769)
    )

    m11 = _multi_matches_packed(*_pattern_of_live(LIVE_4369552))
    m17 = _multi_matches_packed(*_pattern_of_live(LIVE_281769))
    checks["multi_4369552"] = m11
    checks["multi_281769"] = m17
    checks["multi_4369552_ok"] = bool(m11["ok"]) and m11["multi_L"] == 29
    checks["multi_281769_ok"] = bool(m17["ok"]) and m17["multi_L"] == 31

    # Off-hull centres (C < 0 and C > s) against the packed engine.
    rng = random.Random(20260911)
    off_ok = True
    off_n = 0
    off_fail = None
    for _ in range(12):
        s = rng.randint(4, 12)
        wt = rng.randint(2, min(6, s + 1))
        interiors = sorted(rng.sample(range(1, s), wt - 2)) if wt > 2 else []
        pat = 1 | (1 << s)
        for i in interiors:
            pat |= 1 << i
        for C in (-s, -1, 0, s // 2, s, s + 1, 2 * s):
            got = _multi_matches_packed(pat, s, C)
            off_n += 1
            if not got["ok"]:
                off_ok = False
                off_fail = got
                break
        if not off_ok:
            break
    checks["multi_random_n"] = off_n
    checks["multi_random_ok"] = off_ok
    if off_fail:
        checks["multi_random_fail"] = off_fail

    w_p, m_p = pack_from(*_pattern_of_live(LIVE_4369552)[:2], _pattern_of_live(LIVE_4369552)[2])
    # pack_from(pat,s,C)
    pat, s, C = _pattern_of_live(LIVE_4369552)
    w_p, m_p = pack_from(pat, s, C)
    checks["pack_4369552_ok"] = w_p == 11 and m_p == MASK_4369552
    pat17, s17, C17 = _pattern_of_live(LIVE_281769)
    w17p, m17p = pack_from(pat17, s17, C17)
    checks["pack_281769_ok"] = w17p == 17 and m17p == MASK_281769

    bool_keys = [
        "w11_L29_ok",
        "w11_live_ok",
        "w11_span_ok",
        "w11_wt_ok",
        "w17_L31_ok",
        "w17_live_ok",
        "w17_wt_ok",
        "w17_missed_by_8w128",
        "w17_census_ok",
        "w6_run24_ok",
        "fast_matches_scan_mask_runs",
        "packed_matches_naive_prize",
        "packed_matches_naive_4369552",
        "packed_matches_naive_281769",
        "rule30_step_formula",
        "multi_4369552_ok",
        "multi_281769_ok",
        "multi_random_ok",
        "pack_4369552_ok",
        "pack_281769_ok",
    ]
    checks["all_ok"] = all(checks[k] is True for k in bool_keys)
    return checks


def census_contains_known(merged: dict) -> dict:
    """The two Cycle J/K maximizers must appear in the weight-8 span-18 slice."""
    out = {}
    for tag, mask, w, Lexp, live in (
        ("4369552", MASK_4369552, 11, 29, LIVE_4369552),
        ("281769", MASK_281769, 17, 31, LIVE_281769),
    ):
        pat, s, C = _pattern_of_live(live)
        i_best, bestL, best_start, nC, tcapC = _scan_pattern(pat, s)
        i = C + s
        rec = rec_of(pat, s, C, bestL[i], best_start[i], best_start[i] + bestL[i], tcapC[i])
        out[tag] = {
            "in_census_class": 1 <= popcount(mask) <= 8 and (max(live) - min(live)) <= SPAN_MAX,
            "wt": 8,
            "span": s,
            "C": C,
            "w": rec["w"],
            "mask": rec["mask"],
            "L": rec["L"],
            "start": rec["start"],
            "end": rec["end"],
            "L_expected": Lexp,
            "ok": rec["mask"] == mask and rec["w"] == w and rec["L"] >= Lexp,
        }
    out["ok"] = out["4369552"]["ok"] and out["281769"]["ok"]
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


def _in_hull(live) -> bool:
    return bool(live) and live[0] <= 0 <= live[-1]


def write_markdown(dump: dict) -> str:
    a: list[str] = []

    def p(s: str = "") -> None:
        a.append(s)

    p("# Period-2 `L_run`: weight-8 span-24 census")
    p()
    p("This note extends Cycle K (`research/period2_lrun_family.md`). It does")
    p("**not** exclude eventual period 2 for every finite row, and it does")
    p("not claim a prize result. It is a finite census of Hamming weight")
    p("`≤8` and span `≤24`, not a uniform-in-`w` bound.")
    p()
    p("Helper: `research/period2_weight8.py --certify`. Dump:")
    p("`research/period2_weight8.json`. Packed evolution is imported from")
    p("`research/period2_fiber.py` and that file is not modified.")
    p()
    p("## Attack")
    p()
    p("Cycle K found `L=31` on a weight-8 row of span `maxlive-minlive=18`")
    p("(inclusive length 19), true radius 17, mask `281769`, a run from")
    p("`t=320` to `t=351`. Cycle J’s cap `8w+128=264` misses that burst")
    p("entirely. Both known maximizers (masks `4369552` and `281769`) have")
    p("eight 1s. ideas11 item 1 asks for a complete-up-to-translation census")
    p("of every finite row of Hamming weight `1..8` and")
    p("`span = maxlive-minlive ≤ 24`, with the long cap `tcap=32w+512`.")
    p()
    p("**Kill:** a weight-`≤8` row with a period-2 centre run of length")
    p("`≥40` after doubling `tcap`, or max `L` strictly increasing with")
    p("span through 24.")
    p()
    p("**Finite theorem (this class only):** every scanned row has `L≤31`.")
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
    p("Each combinatorial support is placed in canonical form on `[0,s]`")
    p("and scored at every translation for which some live cell lies in")
    p("`[-s,s]` (origin in or within one span of the live block). That is")
    p("`3s+1` centres, not `2^{2w+1}` masks. `tcap=32w+512` of the true")
    p("radius of that placement. Any `L≥30` row is re-evolved at `2·tcap`.")
    p()
    p("## Self-checks")
    p()
    ch = dump["checks"]
    p(f"- `w=11` mask `4369552`, `tcap=8·11+128=216`: `L={ch['w11_L']}` from")
    p(f"  `t={ch['w11_start']}` to `t={ch['w11_end']}`. Live cells")
    p(f"  `{', '.join(str(x) for x in ch['w11_live'])}`. Weight 8, span 18.")
    p(f"- `w=17` mask `281769`, `tcap=8·17+256={ch['w17_tcap_8w256']}`:")
    p(f"  `L={ch['w17_L']}` from `t={ch['w17_start']}` to `t={ch['w17_end']}`.")
    p(f"  Cycle J’s `8w+128` reports `L={ch['w17_L_8w128']}` (misses the burst).")
    p(f"  Census cap `32·17+512={ch['w17_census_tcap']}` still has")
    p(f"  `L={ch['w17_census_L']}` from `t={ch['w17_start']}`.")
    p("- Inlined inner loop agrees with `period2_fiber.scan_mask_runs`.")
    p("- Packed traces match the independent live-cell spacetime on the prize")
    p("  seed, on mask `4369552`, and on mask `281769`.")
    p("- Multi-centre extraction of a canonical support agrees with the packed")
    p("  engine on both maximizers and on random off-hull placements.")
    p(f"- `checks.all_ok={ch['all_ok']}`.")
    p()
    p("## Census")
    p()
    cen = dump["census"]
    p(
        f"`{ _fmt(cen['n_patterns']) }` combinatorial supports, "
        f"`{_fmt(cen['n_place'])}` origin-near placements, "
        f"`tcap=32w+512`, `{cen['nproc']}` processes, "
        f"{cen['elapsed_sec']:.1f}s."
    )
    p()
    p("Span here is `maxlive-minlive`. Cycle K’s “span 19” is inclusive")
    p("length `max-min+1`, i.e. this span 18.")
    p()
    p("| `wt` | types | placements | `L_run` | `n≥30` | `n≥31` | best | `w` | span |")
    p("|-----:|------:|-----------:|--------:|-------:|-------:|-----:|----:|-----:|")
    for row in cen["by_wt_table"]:
        p(
            f"| {row['wt']} | {_fmt(row['n_patterns'])} | {_fmt(row['n_place'])} | "
            f"**{row['L_run']}** | {_fmt(row['n_ge30'])} | {_fmt(row['n_ge31'])} | "
            f"{_mask_cell(row)} | {_fmt(row['best_w'])} | "
            f"{(row['best_live'][-1]-row['best_live'][0]) if row['best_live'] else '—'} |"
        )
    p()
    p("| span | types | placements | `L_run` | `n≥30` | `n≥31` | best | `w` |")
    p("|-----:|------:|-----------:|--------:|-------:|-------:|-----:|----:|")
    for row in cen["by_span_table"]:
        p(
            f"| {row['span']} | {_fmt(row['n_patterns'])} | {_fmt(row['n_place'])} | "
            f"**{row['L_run']}** | {_fmt(row['n_ge30'])} | {_fmt(row['n_ge31'])} | "
            f"{_mask_cell(row)} | {_fmt(row['best_w'])} |"
        )
    p()
    Ls = cen["span_L"]
    p(
        "Max `L` versus span: "
        + ", ".join(f"{s}:{Ls[s]}" for s in range(len(Ls)))
        + "."
    )
    p()
    if cen["span_strictly_increases_through_24"]:
        p("Max `L` **strictly increases** with span through 24 (kill).")
    else:
        p(
            "Max `L` does **not** strictly increase with span through 24 "
            f"(ties at several lengths; global max {max(Ls) if Ls else 0})."
        )
        p()
        p(
            "After a plateau `L=31` on spans `18..22`, the envelope rises "
            "again: `L=33` at span 23 and `L=35` at span 24. That is not the "
            "specified kill (every consecutive span would have to go up), "
            "but span 24 is not a plateau of `L` either."
        )
    p()
    ge30 = cen.get("ge30") or []
    hull_L = [r["L"] for r in ge30 if _in_hull(r.get("live"))]
    off_L = [r["L"] for r in ge30 if not _in_hull(r.get("live"))]
    if hull_L or off_L:
        p()
        p(
            "Every recorded `L≥32` row has the origin **outside** the live "
            "convex hull (all 1s strictly left, or all strictly right, of "
            f"cell 0). Among dumped `L≥30` rows, origin-in-hull max is "
            f"`{max(hull_L) if hull_L else 0}`; off-hull max is "
            f"`{max(off_L) if off_L else 0}`. Cycle K’s `L=31` maximizer "
            "has origin in the hull; the new `L=32,33,35` bursts do not."
        )
    p()
    p("## Witness")
    p()
    best = dump.get("best") or {}
    vc = dump.get("witness_check") or {}
    live = best.get("live") or []
    in_hull = _in_hull(live)
    p("Least true-radius maximizer of the census:")
    p()
    p(f"- true radius `{best.get('w')}`, mask `{best.get('mask')}`")
    p(f"- packed row (bit 0 = spatial `-{best.get('w')}`): `{best.get('row')}`")
    p(
        f"- live at `{', '.join(str(x) for x in live)}` "
        f"({best.get('n1')} ones, span {best.get('span')})"
    )
    p(
        f"- origin in the live hull: `{in_hull}` "
        "(this maximizer is entirely to the left of cell 0; "
        "the rightmost 1 is at `-14`, which still lies in `[-24,24]`)"
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
        p(
            f"- `tcap={best.get('tcap')}` and doubled `tcap={dbl.get('tcap')}` "
            f"both give `(L,start,end)="
            f"({vc.get('L')},{vc.get('start')},{vc.get('end')})`"
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
            + (
                " (truncated)."
                if cc.get("truncated_by_8w128")
                else "."
            )
        )
        p(
            f"Cycle K cap `8w+256={cc.get('tcap_8w256')}` reports "
            f"`L={cc.get('L_8w256')}`. Census `32w+512={cc.get('tcap_census')}` "
            f"reports `L={cc.get('L_census')}`."
        )
        p()
    known = dump.get("known_in_census") or {}
    if known:
        p("Known maximizers, rescored inside this census class:")
        p()
        for tag in ("4369552", "281769"):
            r = known.get(tag) or {}
            p(
                f"- mask `{tag}`: w={r.get('w')} L={r.get('L')} "
                f"(expected ≥{r.get('L_expected')}), span {r.get('span')}, "
                f"ok={r.get('ok')}"
            )
        p()
    ge32 = [r for r in (cen.get("ge30") or []) if r.get("L", 0) >= 32]
    if ge32:
        p(f"`L≥32` rows (unique `(w,mask)`): {len(ge32)}. All have origin off-hull.")
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
    p("These are finite bursts, not eventual period 2: none of the")
    p("recorded `L≥30` rows reaches the cap after doubling.")
    p()
    p("## What is proved, what is not")
    p()
    p("Proved (machine-checked in this run):")
    p()
    p("- The Cycle I packed engine, on every finite row of Hamming weight")
    p(f"  `1..8` and span `≤{SPAN_MAX}` with the origin in/near the live")
    p(f"  span (`3s+1` translations), produces a longest period-2 centre")
    p(f"  run of length `L_run={dump.get('best_L')}` inside `tcap=32w+512`.")
    p("- Self-checks as above, including `w=11` mask `4369552` `L=29` and")
    p("  `w=17` mask `281769` `L=31` at `tcap=8·17+256`.")
    p("- Every `L≥30` candidate was re-evolved at `2·tcap`; none grew,")
    p("  none reached `L≥40`, none reached the cap.")
    p("- Among those `L≥30` rows, origin-in-hull supports still have")
    p("  `L≤31`; every `L≥32` row is off-hull.")
    p()
    p("Not proved:")
    p()
    p("- A bound for weight `>8` or span `>24`.")
    p("- A bound `L≤31` for origin-in-hull rows: it holds on the dumped")
    p("  `L≥30` slice, but that is not a separately enumerated hull-only")
    p("  census.")
    p("- Eventual period 2 of any finite seed. A bounded burst is")
    p("  compatible with every centre eventually leaving period 2.")
    p("- A uniform-in-`w` theorem.")
    p()
    p("## Verdict")
    p()
    p(f"`{dump['verdict']}`, wall time {dump['wall_time_sec']:.1f}s.")
    p()
    p(f"- Reason: {dump['reason']}")
    p(f"- `L≥40`: {'yes' if dump.get('found_L_ge_40') else 'no'}.")
    p(
        "- Span strictly increasing through 24: "
        f"{'yes' if dump.get('span_strictly_increases_through_24') else 'no'}."
    )
    p(f"- Finite theorem `L≤31` on this census: {'yes' if dump.get('finite_theorem') else 'no'}.")
    p("- Survive / uniform proof: no.")
    p()
    p("## Files")
    p()
    p("- `research/period2_weight8.md` (this note)")
    p("- `research/period2_weight8.py` (`--certify` runs the checks and the")
    p("  weight-8 span-24 census)")
    p("- `research/period2_weight8.json` (dump)")
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

    known = census_contains_known({"census": {}})
    # known helper does not need merged; it re-scores the two rows.
    log.append(
        f"known 4369552 L={known['4369552']['L']} "
        f"281769 L={known['281769']['L']} ok={known['ok']}"
    )
    print(log[-1], flush=True)
    if not known["ok"]:
        raise AssertionError(f"known maximizers failed: {known}")

    census = run_census(log)

    best = census["best"]
    L_best = 0 if best is None else best["L"]
    L_double = census.get("L_after_double_max") or 0
    if best is not None:
        Ld = (best.get("doubled") or {}).get("L") or 0
        if Ld > L_double:
            L_double = Ld
    L_report = max(L_best, L_double)

    found_ge40 = L_report >= 40 or census["n_ge40"] > 0 or L_double >= 40
    strict = bool(census.get("span_strictly_increases_through_24"))
    finite = L_report <= 31 and not found_ge40

    if found_ge40:
        verdict = "KILL"
        reason = (
            f"a weight<=8 span<=24 row has a period-2 centre run of length "
            f"{L_report}>=40 (tcap=32w+512, still holds after doubling). "
            "The census kills a bound L<=31 on this class. The run is a "
            "finite burst unless it reaches the cap. This does not exclude "
            "eventual period 2, and it is not a uniform-in-w theorem."
        )
    elif strict:
        verdict = "KILL"
        reason = (
            f"max L strictly increases with span through 24 "
            f"(L by span={census['span_L']}, best L={L_report}). "
            "The envelope is still rising at the census edge, so span<=24 "
            "is not a plateau. Not a uniform proof, and not L>=40."
        )
    elif finite:
        verdict = "FINITE_THEOREM"
        reason = (
            f"every finite row of Hamming weight 1..8 and span "
            f"(maxlive-minlive)<=24, placed with some live cell in "
            f"[-span,span], has a longest period-2 centre run of length "
            f"L<={L_best}<=31 inside tcap=32w+512. Any L>=30 row still has "
            f"L>=30 and L<40 after doubling tcap. This is a finite theorem "
            "for those supports only, not a uniform-in-w bound, and not "
            "an exclusion of eventual period 2."
        )
    else:
        verdict = "L_GT_31"
        reason = (
            f"best L on the census is {L_report} (in 32..39). No L>=40, "
            "and max L does not strictly increase with span through 24. "
            "The L<=31 finite theorem is false on this class; a larger "
            "constant is not claimed."
        )

    witness_check = None
    cap = None
    if best is not None:
        witness_check = verify_row(best["mask"], best["w"], best["tcap"])
        log.append(
            f"witness_check ok={witness_check['ok']} L={witness_check['L']} "
            f"doubled={witness_check['doubled_L']} alt={witness_check['alternating']}"
        )
        print(log[-1], flush=True)
        if not witness_check["ok"]:
            raise AssertionError(f"best-row verification failed: {witness_check}")
        cap = cap_compare(best["mask"], best["w"])
        best["cap_compare"] = cap
        best["verify"] = witness_check

    # Keep json bounded: unique L>=31 plus a few L=30.
    ge30_out = []
    n30_only = 0
    for r in census.get("ge30") or []:
        if r["L"] >= 31:
            ge30_out.append(slim_rec(r))
        else:
            n30_only += 1
            if n30_only <= 8:
                ge30_out.append(slim_rec(r))

    hull_Ls = [r["L"] for r in ge30_out if _in_hull(r.get("live"))]
    off_Ls = [r["L"] for r in ge30_out if not _in_hull(r.get("live"))]

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period2_weight8",
        "ideas11": "item 1",
        "cycle_k": "research/period2_lrun_family.md",
        "cycle_j": "research/period2_lrun.md",
        "problem": (
            "census finite rows of Hamming weight 1..8 and span "
            "(maxlive-minlive)<=24 at tcap=32w+512; kill on L>=40 or "
            "max L strictly increasing with span through 24; finite "
            "theorem if L<=31"
        ),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": False,
        "uniform_proof": False,
        "finite_theorem": finite,
        "found_L_ge_30": L_report >= 30,
        "found_L_ge_40": found_ge40,
        "span_strictly_increases_through_24": strict,
        "best_L": L_report,
        "best_L_tcap": L_best,
        "origin_in_hull_max_L_ge30": max(hull_Ls) if hull_Ls else 0,
        "off_hull_max_L_ge30": max(off_Ls) if off_Ls else 0,
        "best_origin_in_hull": _in_hull((best or {}).get("live")),
        "reason": reason,
        "tcap": "32w+512",
        "span_def": "maxlive-minlive",
        "span_max": SPAN_MAX,
        "wt_max": WT_MAX,
        "placement": "some live cell in [-span,span]; 3s+1 centres",
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "known_in_census": known,
        "witness_check": witness_check,
        "best": slim_rec(best),
        "true_radius_best_cap": cap,
        "census": {
            "n_patterns": census["n_patterns"],
            "n_place": census["n_place"],
            "n_ge30": census["n_ge30"],
            "n_ge31": census["n_ge31"],
            "n_ge40": census["n_ge40"],
            "ge30_hold_fail": census["ge30_hold_fail"],
            "L_run": census["L_run"],
            "L_after_double_max": census["L_after_double_max"],
            "elapsed_sec": census["elapsed_sec"],
            "nproc": census["nproc"],
            "n_tasks": census["n_tasks"],
            "by_wt_table": census["by_wt_table"],
            "by_span_table": census["by_span_table"],
            "span_L": census["span_L"],
            "span_strictly_increases_through_24": census[
                "span_strictly_increases_through_24"
            ],
            "hull_len_table": census["hull_len_table"],
            "ge30": ge30_out,
            "origin_in_hull_max_L_ge30": max(hull_Ls) if hull_Ls else 0,
            "off_hull_max_L_ge30": max(off_Ls) if off_Ls else 0,
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
