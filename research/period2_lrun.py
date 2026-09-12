"""Cycle I follow-up: extend or kill the L_run <= 24 finite theorem.

Cycle I (research/period2_fiber.md) proved that every nonzero finite row
of support radius w<=10 has every period-2 centre run of length at most
24, inside tcap=8w+128. Packed evolution
    new = (row << 2) ^ ((row << 1) | row)
with the centre bit at time t equal to (row >> (w+t)) & 1. The maximizer
at w=6 is mask=7503, a run of 24 from t=94.

This script does not modify period2_fiber.py. It imports that packed
engine and asks whether L_run<=24 survives at larger radii, or dies on a
witness of length >=25 that still holds after doubling tcap.

Run: python3 research/period2_lrun.py --certify
Dump: research/period2_lrun.json
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
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
    tcap_long,
)

OUT = Path(__file__).resolve().with_suffix(".json")

# Exhaustive w=11 is 2^{23}-1 states. Cycle I w=10 (2^{21}-1) took ~69s
# on the same packed loop; a short probe below decides whether to run
# the full scan or fall back. 15 minutes is well above the 4-core
# estimate of a couple of minutes.
EXH_W = 11
EXH_TIMEOUT_SEC = 900.0
PROBE_MASKS = 1 << 16
N_RANDOM = 1 << 20
RANDOM_SEED = 20260910
INTERVAL_LEN = 10
W6_MAXIMIZER = 7503
NPROC_CAP = 4

# Cycle I table, copied for the combined L_run(w) dump. Independently
# re-checked here at w=0 and w=6; not re-enumerated at w=9,10.
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


def row_bits(mask: int, w: int) -> str:
    return "".join(str((mask >> i) & 1) for i in range(2 * w + 1))


def scan_runs_fast(mask: int, w: int, tcap: int) -> tuple[int, int, int, int, int]:
    """Same packed CA as period2_fiber.scan_mask_runs; tuple return.

    Inlines rule30_step to keep the 2^{23} inner loop in bytecode range.
    Correctness against scan_mask_runs is a self-check.
    """
    row = mask
    prev = (row >> w) & 1
    best = 1
    best_start = 0
    run = 1
    run_start = 0
    prefix = 1
    prefix_alive = True
    for t in range(1, tcap):
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
    return best, best_start, prefix, run, best_start + best


def rec_from_tuple(mask: int, w: int, st: tuple[int, int, int, int, int]) -> dict:
    L, start, prefix, suffix, end = st
    return {
        "mask": mask,
        "row": row_bits(mask, w),
        "L": L,
        "start": start,
        "end": end,
        "prefix": prefix,
        "suffix": suffix,
    }


def consider(best: dict | None, rec: dict) -> dict:
    if best is None or rec["L"] > best["L"]:
        return rec
    return best


def scan_one(mask: int, w: int, tcap: int) -> dict:
    return rec_from_tuple(mask, w, scan_runs_fast(mask, w, tcap))


def double_cap_if_long(rec: dict, w: int, tcap: int) -> dict:
    """Re-evolve at 2*tcap. Required for any L>=25 witness; cheap on a maximizer."""
    if rec is None:
        return rec
    out = dict(rec)
    out["tcap"] = tcap
    if "doubled" in out:
        return out
    t2 = 2 * tcap
    st2 = scan_mask_runs(rec["mask"], w, t2)
    out["doubled"] = {
        "tcap": t2,
        "L": st2["L"],
        "start": st2["start"],
        "end": st2["end"],
        "prefix": st2["prefix"],
        "suffix": st2["suffix"],
        "holds_ge25": st2["L"] >= 25,
    }
    return out


def _exh_chunk(args: tuple[int, int, int, int]) -> dict:
    lo, hi, w, tcap = args
    Lrun = 0
    Lpref = 0
    Lsuff = 0
    best = None
    n_gt = 0
    n_ge25 = 0
    first_ge25 = None
    ge25: list[dict] = []
    bound = 4 * w + 16
    for mask in range(lo, hi):
        st = scan_runs_fast(mask, w, tcap)
        L, start, prefix, suffix, end = st
        if L > Lrun:
            Lrun = L
            best = rec_from_tuple(mask, w, st)
        if prefix > Lpref:
            Lpref = prefix
        if suffix > Lsuff:
            Lsuff = suffix
        if L > bound:
            n_gt += 1
        if L >= 25:
            n_ge25 += 1
            rec = rec_from_tuple(mask, w, st)
            if first_ge25 is None:
                first_ge25 = rec
            ge25.append(rec)
    return {
        "L_run": Lrun,
        "L_prefix": Lpref,
        "L_suffix": Lsuff,
        "best": best,
        "n_L_gt_4w16": n_gt,
        "n_ge25": n_ge25,
        "first_ge25": first_ge25,
        "ge25": ge25,
        "n": hi - lo,
    }


def merge_chunk_stats(acc: dict | None, part: dict) -> dict:
    if acc is None:
        return dict(part)
    acc["L_run"] = max(acc["L_run"], part["L_run"])
    acc["L_prefix"] = max(acc["L_prefix"], part["L_prefix"])
    acc["L_suffix"] = max(acc["L_suffix"], part["L_suffix"])
    acc["n_L_gt_4w16"] += part["n_L_gt_4w16"]
    acc["n_ge25"] += part["n_ge25"]
    acc["n"] += part["n"]
    if part["best"] is not None:
        acc["best"] = consider(acc.get("best"), part["best"])
    if acc.get("first_ge25") is None:
        acc["first_ge25"] = part["first_ge25"]
    acc.setdefault("ge25", [])
    acc["ge25"].extend(part.get("ge25") or [])
    return acc


def nproc() -> int:
    try:
        import os

        return max(1, min(NPROC_CAP, os.cpu_count() or 1))
    except Exception:
        return 1


def probe_rate(w: int, tcap: int, n: int = PROBE_MASKS) -> float:
    nstates = (1 << (2 * w + 1)) - 1
    n = min(n, nstates)
    t0 = time.perf_counter()
    s = 0
    for mask in range(1, n + 1):
        s += scan_runs_fast(mask, w, tcap)[0]
    elapsed = time.perf_counter() - t0
    rate = n / elapsed if elapsed > 0 else float("inf")
    # silence unused
    _ = s
    return rate


def exhaustive_scan(w: int, tcap: int, timeout_sec: float, log: list[str]) -> dict:
    nstates = 1 << (2 * w + 1)
    n_nonzero = nstates - 1
    workers = nproc()
    t_probe = time.perf_counter()
    rate = probe_rate(w, tcap)
    probe_elapsed = time.perf_counter() - t_probe
    est_serial = n_nonzero / rate if rate else float("inf")
    est_par = est_serial / workers
    log.append(
        f"probe w={w} tcap={tcap} rate={rate:.0f} masks/s "
        f"est_serial={est_serial:.1f}s est_{workers}proc={est_par:.1f}s "
        f"probe={probe_elapsed:.3f}s"
    )
    timed_out = est_par > timeout_sec
    if timed_out:
        log.append(
            f"TIMEOUT skip exhaustive w={w}: estimated {est_par:.1f}s "
            f"> {timeout_sec:.0f}s"
        )
        return {
            "w": w,
            "tcap": tcap,
            "n_nonzero": n_nonzero,
            "mode": "timeout",
            "timed_out": True,
            "timeout_sec": timeout_sec,
            "est_serial_sec": round(est_serial, 3),
            "est_parallel_sec": round(est_par, 3),
            "probe_rate_per_sec": round(rate, 1),
            "nproc": workers,
            "L_run": None,
            "best": None,
            "elapsed_sec": round(probe_elapsed, 4),
        }

    t0 = time.perf_counter()
    # Equal mask ranges. Probe already scanned 1..PROBE; we still scan
    # the full 1..nstates-1 so the maximizer is exact.
    n_chunks = max(workers * 4, workers)
    chunk = (n_nonzero + n_chunks - 1) // n_chunks
    tasks = []
    lo = 1
    while lo <= n_nonzero:
        hi = min(lo + chunk, nstates)
        tasks.append((lo, hi, w, tcap))
        lo = hi

    acc = None
    if workers == 1 or len(tasks) == 1:
        for task in tasks:
            acc = merge_chunk_stats(acc, _exh_chunk(task))
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(_exh_chunk, task) for task in tasks]
            done = 0
            for fut in as_completed(futs):
                part = fut.result()
                acc = merge_chunk_stats(acc, part)
                done += 1
                if done == 1 or done == len(futs) or done % max(1, len(futs) // 4) == 0:
                    log.append(
                        f"exhaustive w={w} chunks {done}/{len(futs)} "
                        f"L_run={acc['L_run']}"
                    )

    elapsed = time.perf_counter() - t0
    assert acc is not None
    best = acc["best"]
    ge25 = sorted(acc.get("ge25") or [], key=lambda r: (-r["L"], r["mask"]))
    if best is not None:
        best = double_cap_if_long(best, w, tcap)
        ge25_out = []
        for rec in ge25:
            if rec["mask"] == best["mask"]:
                ge25_out.append(best)
            else:
                ge25_out.append(double_cap_if_long(rec, w, tcap))
        ge25 = ge25_out
        first = None
        for rec in ge25:
            if first is None or rec["mask"] < first["mask"]:
                first = rec
        acc["first_ge25"] = first
        acc["ge25"] = ge25

    rec = {
        "w": w,
        "tcap": tcap,
        "n_nonzero": n_nonzero,
        "mode": "exhaustive",
        "timed_out": False,
        "timeout_sec": timeout_sec,
        "est_serial_sec": round(est_serial, 3),
        "est_parallel_sec": round(est_par, 3),
        "probe_rate_per_sec": round(rate, 1),
        "nproc": workers,
        "L_run": acc["L_run"],
        "L_prefix": acc["L_prefix"],
        "L_suffix": acc["L_suffix"],
        "n_L_gt_4w16": acc["n_L_gt_4w16"],
        "n_ge25": acc["n_ge25"],
        "best": best,
        "first_ge25": acc.get("first_ge25"),
        "ge25": acc.get("ge25") or [],
        "elapsed_sec": round(elapsed, 4),
    }
    log.append(
        f"exhaustive w={w} n={n_nonzero} tcap={tcap} L_run={rec['L_run']} "
        f"L_prefix={rec['L_prefix']} L_suffix={rec['L_suffix']} "
        f"n_ge25={rec['n_ge25']} {elapsed:.3f}s nproc={workers}"
    )
    return rec


def random_masks(w: int, n: int, seed: int) -> list[int]:
    nstates = 1 << (2 * w + 1)
    rng = random.Random(seed + w)
    # Distinct nonzero masks. For n << 2^{2w+1} collisions are rare;
    # the set keeps the sample honest.
    out = set()
    # Hard cap: if the space is smaller than n, take everything.
    want = min(n, nstates - 1)
    while len(out) < want:
        out.add(rng.randrange(1, nstates))
    return list(out)


def interval_masks(w: int, max_len: int) -> list[int]:
    """Masks whose live bits lie in a single interval of length <= max_len,
    placed at every position that stays inside [-w, w]."""
    width = 2 * w + 1
    seen: set[int] = set()
    for L in range(1, max_len + 1):
        npat = 1 << L
        nplace = width - L + 1
        for pat in range(1, npat):
            for s in range(nplace):
                seen.add(pat << s)
    return sorted(seen)


def padded_maximizer_mask(w: int) -> int:
    """w=6 maximizer 7503 occupying [-6,6], zeros on [-w,-7] U [7,w]."""
    if w < 6:
        raise ValueError("padding target must have w>=6")
    return W6_MAXIMIZER << (w - 6)


def scan_mask_list(masks: list[int], w: int, tcap: int, log: list[str], tag: str) -> dict:
    t0 = time.perf_counter()
    Lrun = 0
    Lpref = 0
    Lsuff = 0
    best = None
    n_ge25 = 0
    first_ge25 = None
    n_gt = 0
    bound = 4 * w + 16
    for mask in masks:
        if mask == 0:
            continue
        st = scan_runs_fast(mask, w, tcap)
        rec = rec_from_tuple(mask, w, st)
        if rec["L"] > Lrun:
            Lrun = rec["L"]
            best = rec
        if rec["prefix"] > Lpref:
            Lpref = rec["prefix"]
        if rec["suffix"] > Lsuff:
            Lsuff = rec["suffix"]
        if rec["L"] > bound:
            n_gt += 1
        if rec["L"] >= 25:
            n_ge25 += 1
            if first_ge25 is None:
                first_ge25 = rec
    elapsed = time.perf_counter() - t0
    if best is not None:
        best = double_cap_if_long(best, w, tcap)
        # Always double-cap a kill candidate even if it is not the max.
        if first_ge25 is not None:
            if first_ge25["mask"] == best["mask"]:
                first_ge25 = best
            else:
                first_ge25 = double_cap_if_long(first_ge25, w, tcap)
    rec = {
        "tag": tag,
        "w": w,
        "tcap": tcap,
        "n_scanned": len(masks),
        "L_run": Lrun,
        "L_prefix": Lpref,
        "L_suffix": Lsuff,
        "n_L_gt_4w16": n_gt,
        "n_ge25": n_ge25,
        "best": best,
        "first_ge25": first_ge25,
        "elapsed_sec": round(elapsed, 4),
    }
    log.append(
        f"{tag} w={w} n={len(masks)} tcap={tcap} L_run={Lrun} "
        f"n_ge25={n_ge25} {elapsed:.3f}s"
    )
    return rec


def run_checks() -> dict:
    checks: dict = {}

    # Required self-checks.
    t0 = tcap_long(0)
    st0 = scan_mask_runs(1, 0, t0)
    checks["w0_L_run"] = st0["L"]
    checks["w0_L_run_ok"] = st0["L"] == 7
    checks["w0_tcap"] = t0

    t6 = tcap_long(6)
    st6 = scan_mask_runs(W6_MAXIMIZER, 6, t6)
    checks["w6_mask"] = W6_MAXIMIZER
    checks["w6_row"] = row_bits(W6_MAXIMIZER, 6)
    checks["w6_L"] = st6["L"]
    checks["w6_start"] = st6["start"]
    checks["w6_end"] = st6["end"]
    checks["w6_run24_ok"] = st6["L"] == 24 and st6["start"] == 94
    checks["w6_tcap"] = t6

    # Fast loop agrees with the imported engine.
    fast_ok = True
    fail = None
    for w, mask, tcap in (
        (0, 1, 128),
        (6, W6_MAXIMIZER, 176),
        (3, 73, 80),
        (4, 300, 80),
        (11, 7503 << 5, 64),
        (11, 1, 64),
        (12, 4095, 64),
    ):
        a = scan_mask_runs(mask, w, tcap)
        b = scan_runs_fast(mask, w, tcap)
        if (
            a["L"] != b[0]
            or a["start"] != b[1]
            or a["prefix"] != b[2]
            or a["suffix"] != b[3]
            or a["end"] != b[4]
        ):
            fast_ok = False
            fail = {"w": w, "mask": mask, "engine": a, "fast": b}
            break
    checks["fast_matches_scan_mask_runs"] = fast_ok
    if fail:
        checks["fast_fail"] = fail

    # Packed formula vs independent live-cell spacetime.
    prize = evolve_centers(1, 0, 32)
    checks["packed_matches_naive_prize"] = prize == naive_centers({0: 1}, 32)
    checks["prize_prefix16"] = "".join(map(str, prize[:16]))
    checks["prize_prefix16_ok"] = checks["prize_prefix16"] == "1101110011000101"
    live6 = mask_to_live(W6_MAXIMIZER, 6)
    a = evolve_centers(W6_MAXIMIZER, 6, 48)
    b = naive_centers(live6, 48)
    checks["packed_matches_naive_7503"] = a == b

    # rule30_step is the same packed engine.
    checks["rule30_step_formula"] = all(
        rule30_step(m) == ((m << 2) ^ ((m << 1) | m)) for m in (0, 1, 7503, 123456)
    )

    # Padding the w=6 maximizer to larger w is the same physical row:
    # centre traces must agree on the common time window.
    c6 = evolve_centers(W6_MAXIMIZER, 6, 176)
    pad_ok = True
    for w in (7, 8, 11, 12):
        cw = evolve_centers(padded_maximizer_mask(w), w, 176)
        if cw != c6:
            pad_ok = False
            checks["pad_fail_w"] = w
            break
    checks["padded_maximizer_same_trace"] = pad_ok

    bool_keys = [
        "w0_L_run_ok",
        "w6_run24_ok",
        "fast_matches_scan_mask_runs",
        "packed_matches_naive_prize",
        "prize_prefix16_ok",
        "packed_matches_naive_7503",
        "rule30_step_formula",
        "padded_maximizer_same_trace",
    ]
    checks["all_ok"] = all(checks[k] is True for k in bool_keys)
    return checks


def pad_mask(mask: int, w_from: int, w_to: int) -> int:
    """Same physical row: extra quiescent cells on both sides."""
    if w_to < w_from:
        raise ValueError("w_to must be >= w_from")
    return mask << (w_to - w_from)


def verify_kill_row(mask: int, w: int, tcap: int) -> dict:
    """Packed engine, fast loop, and naive live-cell spacetime agree on the run."""
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
        "fast_matches_engine": fast == (st["L"], st["start"], st["prefix"], st["suffix"], st["end"]),
        "L": st["L"],
        "start": st["start"],
        "end": st["end"],
        "run_bits": "".join(map(str, run)),
        "alternating": alt,
        "break_before": before,
        "break_after": after,
        "interior": st["end"] < tcap and st["start"] > 0,
        "doubled_L": st2["L"],
        "doubled_start": st2["start"],
        "doubled_end": st2["end"],
        "holds_ge25": st2["L"] >= 25,
        "ok": (
            bits == naive
            and fast[0] == st["L"]
            and st["L"] >= 25
            and alt
            and st2["L"] >= 25
        ),
    }


def collect_witnesses(scans: list[dict]) -> list[dict]:
    hits = []
    for rec in scans:
        if rec is None or not isinstance(rec, dict):
            continue
        objs = []
        for key in ("best", "first_ge25"):
            if rec.get(key):
                objs.append(rec[key])
        objs.extend(rec.get("ge25") or [])
        src = rec.get("tag") or rec.get("mode") or rec.get("w")
        for obj in objs:
            if not obj or obj.get("L", 0) < 25:
                continue
            dbl = obj.get("doubled") or {}
            hits.append(
                {
                    "source": src,
                    "w": rec.get("w"),
                    "mask": obj["mask"],
                    "row": obj.get("row"),
                    "L_tcap": obj["L"],
                    "start": obj.get("start"),
                    "end": obj.get("end"),
                    "tcap": rec.get("tcap") or obj.get("tcap"),
                    "L_doubled": dbl.get("L"),
                    "doubled_tcap": dbl.get("tcap"),
                    "holds_ge25": dbl.get("holds_ge25"),
                }
            )
    uniq = []
    seen = set()
    for h in hits:
        k = (h["w"], h["mask"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(h)
    uniq.sort(key=lambda h: (-h["L_tcap"], h["w"], h["mask"]))
    return uniq


def live_positions(mask: int, w: int) -> list[int]:
    return [i - w for i in range(2 * w + 1) if (mask >> i) & 1]


def shrink_to_support(mask: int, w: int) -> tuple[int, int, list[int]]:
    """Minimal radius containing the live cells, and the packed mask there."""
    live = live_positions(mask, w)
    if not live:
        return 0, 0, live
    r = max(abs(p) for p in live)
    shift = w - r
    mask_r = (mask >> shift) & ((1 << (2 * r + 1)) - 1)
    return r, mask_r, live


def cap_truncation_report(ge25: list[dict], w_scan: int, log: list[str]) -> list[dict]:
    """Rescan each long run at its true support radius with Cycle I's tcap.

    A run that starts near 8w+128 can look shorter than 25 in Cycle I and
    finish past that cap. Doubling at the true radius catches it.
    """
    out = []
    for rec in ge25:
        r, mask_r, live = shrink_to_support(rec["mask"], w_scan)
        tcap_r = tcap_long(r)
        st_r = scan_mask_runs(mask_r, r, tcap_r)
        st_hi = scan_mask_runs(mask_r, r, max(2 * tcap_r, rec.get("end", 0) + 32))
        item = {
            "w_scan": w_scan,
            "mask_scan": rec["mask"],
            "L_scan": rec["L"],
            "true_radius": r,
            "mask_true": mask_r,
            "row_true": row_bits(mask_r, r),
            "live": live,
            "n1": len(live),
            "span": (live[-1] - live[0] + 1) if live else 0,
            "tcap_true": tcap_r,
            "L_at_cycle_i_tcap": st_r["L"],
            "start_at_cycle_i_tcap": st_r["start"],
            "end_at_cycle_i_tcap": st_r["end"],
            "suffix_at_cycle_i_tcap": st_r["suffix"],
            "reaches_cycle_i_tcap": st_r["end"] == tcap_r,
            "tcap_extended": max(2 * tcap_r, rec.get("end", 0) + 32),
            "L_extended": st_hi["L"],
            "start_extended": st_hi["start"],
            "end_extended": st_hi["end"],
            "holds_ge25_at_true_radius": st_hi["L"] >= 25,
            "truncated_by_cycle_i_tcap": st_r["L"] < st_hi["L"] and st_hi["L"] >= 25,
        }
        out.append(item)
        if item["truncated_by_cycle_i_tcap"]:
            log.append(
                f"cap-truncation true_w={r} mask={mask_r} "
                f"L({tcap_r})={st_r['L']} -> L({item['tcap_extended']})={st_hi['L']} "
                f"start={st_hi['start']} end={st_hi['end']}"
            )
    return out


def certify() -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    scans: list[dict] = []

    # --- exhaustive w=11, or timeout + documented fallback ---
    tcap11 = tcap_long(EXH_W)
    exh11 = exhaustive_scan(EXH_W, tcap11, EXH_TIMEOUT_SEC, log)
    scans.append(exh11)

    fallback_ws = [12]
    if exh11.get("timed_out"):
        fallback_ws = [11, 12]
        log.append("fallback: random + interval + padded maximizer at w=11 and w=12")
    else:
        log.append("exhaustive w=11 finished; fallback families run at w=12")

    sampled = []
    interval = []
    padded = []

    for w in fallback_ws:
        tcap = tcap_long(w)
        rng_masks = random_masks(w, N_RANDOM, RANDOM_SEED)
        sampled.append(
            scan_mask_list(rng_masks, w, tcap, log, f"random_2^{20}")
        )
        iv = interval_masks(w, INTERVAL_LEN)
        interval.append(
            scan_mask_list(iv, w, tcap, log, f"interval_len<={INTERVAL_LEN}")
        )

    # Padded w=6 maximizer at every w>=6 we touch, plus a few larger
    # radii (same physical row; tcap grows). Doubled if L>=25.
    pad_ws = sorted(set([11, 12] + fallback_ws + [16, 20]))
    for w in pad_ws:
        tcap = tcap_long(w)
        mask = padded_maximizer_mask(w)
        rec = scan_mask_list([mask], w, tcap, log, "padded_w6_maximizer")
        padded.append(rec)

    scans.extend(sampled)
    scans.extend(interval)
    scans.extend(padded)

    # If exhaustive w=11 produced a long run, embed that same physical row
    # at larger radii (zeros on both sides) so L_run(w) for w>11 is not
    # under-reported by the w=12 sample, which can miss a 19-bit support.
    embedded = []
    if (not exh11.get("timed_out")) and exh11.get("best") and exh11["best"]["L"] >= 25:
        w0 = exh11["w"]
        m0 = exh11["best"]["mask"]
        for w in (12, 13, 16, 20):
            tcap = tcap_long(w)
            rec = scan_mask_list(
                [pad_mask(m0, w0, w)], w, tcap, log, "embedded_w11_maximizer"
            )
            embedded.append(rec)
        scans.extend(embedded)

    witnesses = collect_witnesses(scans)
    kill_hits = [h for h in witnesses if h.get("holds_ge25")]

    witness_check = None
    if kill_hits:
        h = next(
            (x for x in kill_hits if x.get("w") == 11 and x.get("source") == "exhaustive"),
            kill_hits[0],
        )
        witness_check = verify_kill_row(h["mask"], h["w"], h["tcap"])
        log.append(
            f"witness_check ok={witness_check['ok']} L={witness_check['L']} "
            f"doubled={witness_check['doubled_L']} alt={witness_check['alternating']} "
            f"naive={witness_check['packed_matches_naive']}"
        )
        if not witness_check["ok"]:
            raise AssertionError(f"kill witness failed verification: {witness_check}")

    cap_trunc = []
    if exh11.get("ge25"):
        cap_trunc = cap_truncation_report(exh11["ge25"], exh11["w"], log)

    # Combined L_run table.
    table = []
    for row in CYCLE_I_L_RUN:
        src = "cycle_i_exhaustive"
        if row["w"] == 0:
            src = "this_run_selfcheck"
            assert checks["w0_L_run"] == row["L_run"]
        elif row["w"] == 6:
            src = "this_run_selfcheck"
            assert checks["w6_L"] == row["L_run"]
        table.append(
            {
                "w": row["w"],
                "n_nonzero": row["n_nonzero"],
                "tcap": row["tcap"],
                "L_run": row["L_run"],
                "L_prefix": row["L_prefix"],
                "mode": src,
                "best_mask": row["best_mask"],
                "best_start": row["best_start"],
            }
        )

    if not exh11.get("timed_out"):
        table.append(
            {
                "w": 11,
                "n_nonzero": exh11["n_nonzero"],
                "tcap": exh11["tcap"],
                "L_run": exh11["L_run"],
                "L_prefix": exh11.get("L_prefix"),
                "mode": "this_run_exhaustive",
                "best_mask": (exh11.get("best") or {}).get("mask"),
                "best_start": (exh11.get("best") or {}).get("start"),
                "elapsed_sec": exh11.get("elapsed_sec"),
            }
        )
    else:
        # Fallback L_run(11) is a sampled lower bound.
        parts = [r for r in sampled + interval + padded if r.get("w") == 11]
        L11 = max((r["L_run"] for r in parts), default=None)
        table.append(
            {
                "w": 11,
                "n_nonzero": (1 << 23) - 1,
                "tcap": tcap11,
                "L_run": L11,
                "L_run_is_lower_bound": True,
                "mode": "timeout_then_sampled",
                "elapsed_sec": exh11.get("elapsed_sec"),
            }
        )

    parts12 = [r for r in sampled + interval + padded + embedded if r.get("w") == 12]
    if parts12:
        best12 = max(parts12, key=lambda r: r["L_run"])
        sampled_only = [r for r in sampled + interval + padded if r.get("w") == 12]
        sampled_L = max((r["L_run"] for r in sampled_only), default=None)
        table.append(
            {
                "w": 12,
                "n_nonzero": (1 << 25) - 1,
                "tcap": tcap_long(12),
                "L_run": best12["L_run"],
                "L_run_is_lower_bound": True,
                "L_run_sampled_only": sampled_L,
                "mode": (
                    "embedded_w11_witness"
                    if best12.get("tag") == "embedded_w11_maximizer"
                    else "sampled_random_interval_padded"
                ),
                "best_mask": (best12.get("best") or {}).get("mask"),
                "best_start": (best12.get("best") or {}).get("start"),
                "n_scanned_sample_families": sum(r["n_scanned"] for r in sampled_only),
            }
        )
    for rec in embedded:
        if rec.get("w") == 12:
            continue
        table.append(
            {
                "w": rec["w"],
                "tcap": rec["tcap"],
                "L_run": rec["L_run"],
                "L_run_is_lower_bound": True,
                "mode": "embedded_w11_witness",
                "best_mask": (rec.get("best") or {}).get("mask"),
                "best_start": (rec.get("best") or {}).get("start"),
            }
        )

    exh11_le24 = (not exh11.get("timed_out")) and (exh11.get("L_run") or 0) <= 24
    sampled_max = max((r["L_run"] for r in sampled + interval + padded), default=0)

    if kill_hits:
        verdict = "KILL"
        wtn = next(
            (x for x in kill_hits if x.get("w") == 11 and x.get("source") == "exhaustive"),
            kill_hits[0],
        )
        kill_reason = (
            f"finite nonzero row w={wtn['w']} mask={wtn['mask']} has a period-2 "
            f"centre run of length {wtn['L_tcap']} >=25 (t={wtn['start']}..{wtn['end']}) "
            f"that still holds after doubling tcap ({wtn['tcap']} -> {wtn['doubled_tcap']}, "
            f"L={wtn['L_doubled']}). The Cycle I bound L_run<=24 is false at radius 11. "
            "The run is an interior burst, not an eventual regime. This does not "
            "exclude eventual period 2, and it is not a uniform-in-w theorem."
        )
        witness = wtn
    else:
        witness = None
        if exh11_le24:
            verdict = "FINITE_THEOREM"
            extra = ""
            if sampled_max <= 24:
                extra = (
                    " Sampled w=12 (2^20 random, interval supports of length "
                    "<=10, padded w=6 maximizer) also has L_run<=24; that is "
                    "a lower-bound scan, not an exhaustive theorem at w=12."
                )
            kill_reason = (
                "exhaustive radius 11 (2^{23}-1 nonzero rows, tcap=8*11+128=216) "
                f"has L_run={exh11['L_run']}<=24. Finite theorem extends from "
                "w<=10 to w<=11. Not a uniform-in-w proof: a radius-12 row "
                "with a length-25 burst is not excluded by enumeration."
                + extra
            )
        elif exh11.get("timed_out"):
            verdict = "NO_WITNESS"
            kill_reason = (
                f"exhaustive w=11 timed out (budget {EXH_TIMEOUT_SEC:.0f}s); "
                "fallback random/interval/padded scans found no length>=25 "
                "run that survives doubling tcap. Not a finite theorem at "
                "radius 11."
            )
        else:
            # Exhaustive found L>=25 that failed to hold after doubling,
            # or some other non-kill long run.
            verdict = "NO_WITNESS"
            kill_reason = (
                f"longest scanned run is {exh11.get('L_run')}; no witness "
                "of length >=25 held after doubling tcap"
            )

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period2_lrun",
        "cycle_i": "research/period2_fiber.md",
        "problem": (
            "upgrade L_run<=24 to more radii, or kill with a finite nonzero "
            "row whose period-2 centre run has length >=25 after doubling tcap"
        ),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": False,
        "uniform_proof": False,
        "kill_reason": kill_reason,
        "witness": witness,
        "n_kill_witnesses": len(kill_hits),
        "kill_witnesses": kill_hits,
        "wall_time_sec": round(wall, 4),
        "tcap": "8w+128",
        "tcap_w11": tcap11,
        "tcap_w12": tcap_long(12),
        "checks": checks,
        "witness_check": witness_check,
        "L_run": table,
        "finite_theorem_w_le_11": bool(exh11_le24),
        "exhaustive_w11": exh11,
        "sampled": sampled,
        "interval": interval,
        "padded_maximizer": padded,
        "embedded_w11_maximizer": embedded,
        "true_radius_rescans": cap_trunc,
        "n_truncated_by_cycle_i_tcap": sum(
            1 for x in cap_trunc if x.get("truncated_by_cycle_i_tcap")
        ),
        "fallback_radii": fallback_ws,
        "log": log,
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict={verdict} wall={wall:.3f}s")
    print(f"reason: {kill_reason}")
    print(f"L_run: {[(r['w'], r['L_run'], r['mode']) for r in table]}")
    print(f"witness: {witness}")
    return dump


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    certify()


if __name__ == "__main__":
    main()
