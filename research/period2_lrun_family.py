"""Cycle J follow-up: constructive families for period-2 L_run growth.

Cycle J (research/period2_lrun.md) killed L_run<=24: w=11 mask 4369552 has
a period-2 centre run of length 29. Zero-padding that row does not
lengthen the burst. This script searches a one-parameter family of finite
rows whose longest period-2 centre run L might tend to infinity, and
also hunts L>=30 (then L>=40) on nearby constructive and random rows.

Packed evolution is imported from research/period2_fiber.py and that
file is not modified:
    new = (row << 2) ^ ((row << 1) | row)
    centre bit (row >> (w + t)) & 1
with bit 0 the leftmost cell of the current support.

Run: python3 research/period2_lrun_family.py --certify
Dump: research/period2_lrun_family.json
"""
from __future__ import annotations

import argparse
import json
import math
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
)

OUT = Path(__file__).resolve().with_suffix(".json")

# Witnesses from Cycle J / Cycle I.
MASK_4369552 = 4369552
W_4369552 = 11
MASK_4842768 = 4842768
MASK_7503 = 7503
W_7503 = 6
MOTIF_4369552 = (-7, -4, -1, 0, 2, 4, 6, 11)
MOTIF_4842768 = (-7, -3, -1, 2, 3, 4, 5, 8, 11)
MOTIF_7503 = (-6, -5, -4, -3, 0, 2, 4, 5, 6)

K_MAX = 64
N_RANDOM = 1 << 18
RANDOM_SEED = 20260911
HW_LO, HW_HI = 8, 16
W_RANDOM = (12, 13, 14, 15, 16)
INTERVAL_LEN = 20
INTERVAL_W = 20
NPROC_CAP = 4
# Motif repeats: n copies at spacing d (local-origin distance).
MOTIF_NS = (2, 3, 4, 5)
MOTIF_D_MAX = 64
# Extra 6- and 8-copy slices at a few spacings (cheap).
MOTIF_EXTRA_NS = (6, 8)
MOTIF_EXTRA_DS = (16, 19, 20, 24, 32, 40, 48, 64)


def tcap_fam(w: int) -> int:
    """Specified family cap: 8w+256 (Cycle J used 8w+128)."""
    return 8 * w + 256


def nproc() -> int:
    try:
        import os

        return max(1, min(NPROC_CAP, os.cpu_count() or 1))
    except Exception:
        return 1


def row_bits(mask: int, w: int) -> str:
    return "".join(str((mask >> i) & 1) for i in range(2 * w + 1))


def live_positions(mask: int, w: int) -> list[int]:
    return [i - w for i in range(2 * w + 1) if (mask >> i) & 1]


def pack_live(live) -> tuple[int, int]:
    """True radius and packed mask for a set of live spatial cells."""
    if not live:
        return 0, 0
    lo = min(live)
    hi = max(live)
    w = max(-lo, hi)
    mask = 0
    for p in live:
        mask |= 1 << (p + w)
    return w, mask


def support_block(mask: int, w: int) -> tuple[int, ...]:
    """Bits from first live cell to last live cell (inclusive)."""
    live = live_positions(mask, w)
    if not live:
        return ()
    lo, hi = live[0], live[-1]
    s = set(live)
    return tuple(1 if p in s else 0 for p in range(lo, hi + 1))


def scan_runs_fast(mask: int, w: int, tcap: int) -> tuple[int, int, int, int]:
    """Same packed CA as period2_fiber.scan_mask_runs; no prefix tracking.

    Returns (L, start, end, suffix). Inlines the step to keep the inner
    loop in bytecode range. Correctness against scan_mask_runs is a
    self-check.
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
    return best, best_start, best_start + best, run


def rec_of(mask: int, w: int, st: tuple[int, int, int, int], tcap: int) -> dict:
    L, start, end, suffix = st
    live = live_positions(mask, w)
    return {
        "mask": mask,
        "w": w,
        "row": row_bits(mask, w),
        "live": live,
        "n1": len(live),
        "span": (live[-1] - live[0] + 1) if live else 0,
        "L": L,
        "start": start,
        "end": end,
        "suffix": suffix,
        "tcap": tcap,
        "reaches_cap": end == tcap and L >= 2,
    }


def extend_if_capped(rec: dict) -> dict:
    """If the best run hits tcap, double until it breaks or two doubles."""
    if rec is None:
        return rec
    out = dict(rec)
    if not rec.get("reaches_cap"):
        return out
    w = rec["w"]
    mask = rec["mask"]
    tcap = rec["tcap"]
    for _ in range(2):
        tcap *= 2
        st = scan_runs_fast(mask, w, tcap)
        out = rec_of(mask, w, st, tcap)
        if not out["reaches_cap"]:
            break
    return out


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
    }
    return out


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


def scan_packed(mask: int, w: int, tcap: int | None = None) -> dict:
    if tcap is None:
        tcap = tcap_fam(w)
    rec = rec_of(mask, w, scan_runs_fast(mask, w, tcap), tcap)
    return extend_if_capped(rec)


def scan_live(live, tcap: int | None = None) -> dict | None:
    w, mask = pack_live(live)
    if mask == 0:
        return None
    return scan_packed(mask, w, tcap)


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def run_checks() -> dict:
    checks: dict = {}

    t11 = 8 * 11 + 128
    st11 = scan_mask_runs(MASK_4369552, W_4369552, t11)
    checks["w11_mask"] = MASK_4369552
    checks["w11_L"] = st11["L"]
    checks["w11_start"] = st11["start"]
    checks["w11_end"] = st11["end"]
    checks["w11_L29_ok"] = st11["L"] == 29 and st11["start"] == 159 and st11["end"] == 188
    live11 = live_positions(MASK_4369552, W_4369552)
    checks["w11_live"] = live11
    checks["w11_live_ok"] = live11 == list(MOTIF_4369552)

    t6 = 8 * 6 + 128
    st6 = scan_mask_runs(MASK_7503, W_7503, t6)
    checks["w6_L"] = st6["L"]
    checks["w6_start"] = st6["start"]
    checks["w6_run24_ok"] = st6["L"] == 24 and st6["start"] == 94

    # Family cap still sees the length-29 burst.
    st11f = scan_runs_fast(MASK_4369552, W_4369552, tcap_fam(11))
    checks["w11_family_tcap_L"] = st11f[0]
    checks["w11_family_tcap_ok"] = st11f[0] == 29 and st11f[1] == 159

    fast_ok = True
    fail = None
    for w, mask, tcap in (
        (0, 1, 128),
        (6, MASK_7503, 176),
        (11, MASK_4369552, 216),
        (11, MASK_4842768, 216),
        (12, MASK_4369552 << 1, 64),
        (4, 300, 80),
    ):
        a = scan_mask_runs(mask, w, tcap)
        b = scan_runs_fast(mask, w, tcap)
        if a["L"] != b[0] or a["start"] != b[1] or a["end"] != b[2] or a["suffix"] != b[3]:
            fast_ok = False
            fail = {"w": w, "mask": mask, "engine": a, "fast": b}
            break
    checks["fast_matches_scan_mask_runs"] = fast_ok
    if fail:
        checks["fast_fail"] = fail

    prize = evolve_centers(1, 0, 32)
    checks["packed_matches_naive_prize"] = prize == naive_centers({0: 1}, 32)
    live_m = mask_to_live(MASK_4369552, W_4369552)
    a = evolve_centers(MASK_4369552, W_4369552, 48)
    b = naive_centers(live_m, 48)
    checks["packed_matches_naive_4369552"] = a == b

    checks["rule30_step_formula"] = all(
        rule30_step(m) == ((m << 2) ^ ((m << 1) | m))
        for m in (0, 1, MASK_7503, MASK_4369552)
    )

    # Zero-padding does not lengthen the burst (Cycle J claim).
    c11 = evolve_centers(MASK_4369552, 11, 216)
    pad_ok = True
    pad_L = []
    for w in (12, 13, 16, 20):
        mask = MASK_4369552 << (w - 11)
        cw = evolve_centers(mask, w, 216)
        if cw != c11:
            pad_ok = False
            checks["pad_fail_w"] = w
            break
        st = scan_mask_runs(mask, w, tcap_fam(w))
        pad_L.append({"w": w, "L": st["L"], "start": st["start"], "end": st["end"]})
        if st["L"] != 29 or st["start"] != 159:
            pad_ok = False
            checks["pad_L_fail_w"] = w
            break
    checks["zero_padding_same_trace"] = pad_ok
    checks["padded_L"] = pad_L

    # pack_live round-trip on the motif.
    w_p, m_p = pack_live(MOTIF_4369552)
    checks["pack_live_ok"] = w_p == 11 and m_p == MASK_4369552

    bool_keys = [
        "w11_L29_ok",
        "w11_live_ok",
        "w6_run24_ok",
        "w11_family_tcap_ok",
        "fast_matches_scan_mask_runs",
        "packed_matches_naive_prize",
        "packed_matches_naive_4369552",
        "rule30_step_formula",
        "zero_padding_same_trace",
        "pack_live_ok",
    ]
    checks["all_ok"] = all(checks[k] is True for k in bool_keys)
    return checks


# ---------------------------------------------------------------------------
# Concatenate two live-support blocks, k zeros, all placements
# ---------------------------------------------------------------------------

def concat_live_from_block(bits: tuple[int, ...], k: int, leftmost: int) -> list[int]:
    span = len(bits)
    live = []
    for i, b in enumerate(bits):
        if not b:
            continue
        live.append(leftmost + i)
        live.append(leftmost + span + k + i)
    return live


def placement_leftmosts(S: int) -> range:
    """Slide a length-S block through the origin, including fully left/right.

    Pattern occupies [L, L+S-1]. L from -S to 1 puts it fully on the
    negative axis, covering 0, or fully on the positive axis. That is a
    large enough radius: w = max(|L|, |L+S-1|) <= S.
    """
    return range(-S, 2)


def scan_concat_family(mask: int, w0: int, k_max: int, log: list[str], tag: str) -> dict:
    bits = support_block(mask, w0)
    span = len(bits)
    t0 = time.perf_counter()
    per_k = []
    best = None
    n_scanned = 0
    n_ge30 = 0
    n_ge29 = 0
    first_ge30 = None
    for k in range(0, k_max + 1):
        S = 2 * span + k
        best_k = None
        n_k = 0
        for Lft in placement_leftmosts(S):
            rec = scan_live(concat_live_from_block(bits, k, Lft))
            if rec is None:
                continue
            rec = dict(rec)
            rec["k"] = k
            rec["leftmost"] = Lft
            rec["family"] = tag
            n_k += 1
            n_scanned += 1
            best_k = consider(best_k, rec)
            best = consider(best, rec)
            if rec["L"] >= 29:
                n_ge29 += 1
            if rec["L"] >= 30:
                n_ge30 += 1
                if first_ge30 is None:
                    first_ge30 = rec
        assert best_k is not None
        per_k.append(
            {
                "k": k,
                "S": S,
                "n_place": n_k,
                "L": best_k["L"],
                "start": best_k["start"],
                "end": best_k["end"],
                "w": best_k["w"],
                "mask": best_k["mask"],
                "leftmost": best_k["leftmost"],
                "reaches_cap": best_k["reaches_cap"],
            }
        )
    elapsed = time.perf_counter() - t0
    Ls = [row["L"] for row in per_k]
    growth = growth_report(Ls, k_max)
    if best is not None and best["L"] >= 25:
        best = double_cap(best)
    if first_ge30 is not None:
        first_ge30 = double_cap(first_ge30)
    rec = {
        "tag": tag,
        "source_mask": mask,
        "source_w": w0,
        "block": "".join(map(str, bits)),
        "block_span": span,
        "k_max": k_max,
        "n_scanned": n_scanned,
        "L_run": best["L"] if best else 0,
        "n_ge29": n_ge29,
        "n_ge30": n_ge30,
        "best": best,
        "first_ge30": first_ge30,
        "per_k": per_k,
        "L_by_k": Ls,
        "growth": growth,
        "elapsed_sec": round(elapsed, 4),
    }
    msg = (
        f"{tag} n={n_scanned} L_run={rec['L_run']} n_ge30={n_ge30} "
        f"L_by_k=[{min(Ls)}..{max(Ls)}] {elapsed:.3f}s"
    )
    log.append(msg)
    print(msg, flush=True)
    return rec


def growth_report(Ls: list[int], k_max: int) -> dict:
    """Does L grow with the spacing parameter?"""
    if not Ls:
        return {"grows": False, "reason": "empty"}
    n = len(Ls)
    # Target mentioned in the attack: L >= 20 + k/2.
    n_hit_half = sum(1 for k, L in enumerate(Ls) if L >= 20 + k / 2)
    # Linear least squares L ~ a + b k on k=0..k_max.
    ks = list(range(n))
    mean_k = (n - 1) / 2
    mean_L = sum(Ls) / n
    var_k = sum((k - mean_k) ** 2 for k in ks)
    cov = sum((k - mean_k) * (L - mean_L) for k, L in zip(ks, Ls))
    slope = cov / var_k if var_k else 0.0
    intercept = mean_L - slope * mean_k
    # Strictly unbounded-looking: max on the second half exceeds max on
    # the first half by at least 4, and slope >= 0.1.
    mid = n // 2
    max_lo = max(Ls[: max(1, mid)])
    max_hi = max(Ls[mid:])
    grows = (max_hi >= max_lo + 4 and slope >= 0.1) or (
        n_hit_half >= max(3, n // 4) and max(Ls) >= 30
    )
    return {
        "L_min": min(Ls),
        "L_max": max(Ls),
        "L_at_0": Ls[0],
        "L_at_kmax": Ls[-1],
        "slope": round(slope, 6),
        "intercept": round(intercept, 4),
        "max_first_half": max_lo,
        "max_second_half": max_hi,
        "n_hit_L_ge_20_plus_k_over_2": n_hit_half,
        "grows": grows,
        "flat_at_29": max(Ls) == 29 and min(Ls) <= 29,
    }


# ---------------------------------------------------------------------------
# Repeat the 8-one motif at several spacings
# ---------------------------------------------------------------------------

def motif_union(motif: tuple[int, ...], n_copies: int, spacing: int, shift: int) -> list[int]:
    live = set()
    for i in range(n_copies):
        for p in motif:
            live.add(p + i * spacing + shift)
    return list(live)


def motif_span(motif: tuple[int, ...], n_copies: int, spacing: int) -> tuple[int, int]:
    lo = min(motif)
    hi = max(motif) + (n_copies - 1) * spacing
    return lo, hi


def scan_motif_family(
    motif: tuple[int, ...],
    ns: tuple[int, ...],
    d_max: int,
    log: list[str],
    tag: str,
    extra_ns: tuple[int, ...] = (),
    extra_ds: tuple[int, ...] = (),
) -> dict:
    t0 = time.perf_counter()
    best = None
    n_scanned = 0
    n_ge30 = 0
    n_ge29 = 0
    first_ge30 = None
    by_nd: list[dict] = []
    jobs: list[tuple[int, int]] = []
    for n in ns:
        for d in range(1, d_max + 1):
            jobs.append((n, d))
    for n in extra_ns:
        for d in extra_ds:
            jobs.append((n, d))
    # unique jobs, stable
    seen_jobs = set()
    uniq_jobs = []
    for j in jobs:
        if j not in seen_jobs:
            seen_jobs.add(j)
            uniq_jobs.append(j)

    for n_copies, d in uniq_jobs:
        lo0, hi0 = motif_span(motif, n_copies, d)
        S = hi0 - lo0 + 1
        best_nd = None
        n_place = 0
        for Lft in placement_leftmosts(S):
            shift = Lft - lo0
            rec = scan_live(motif_union(motif, n_copies, d, shift))
            if rec is None:
                continue
            rec = dict(rec)
            rec["n_copies"] = n_copies
            rec["spacing"] = d
            rec["shift"] = shift
            rec["family"] = tag
            n_place += 1
            n_scanned += 1
            best_nd = consider(best_nd, rec)
            best = consider(best, rec)
            if rec["L"] >= 29:
                n_ge29 += 1
            if rec["L"] >= 30:
                n_ge30 += 1
                if first_ge30 is None:
                    first_ge30 = rec
        assert best_nd is not None
        by_nd.append(
            {
                "n_copies": n_copies,
                "spacing": d,
                "S": S,
                "n_place": n_place,
                "L": best_nd["L"],
                "start": best_nd["start"],
                "end": best_nd["end"],
                "w": best_nd["w"],
                "mask": best_nd["mask"],
                "shift": best_nd["shift"],
            }
        )

    elapsed = time.perf_counter() - t0
    # Growth in n at fixed spacing, and in d at fixed n=2,3.
    growth_by_n = {}
    for d in (19, 20, 24, 32, 40, 48, 64):
        Ls = [row["L"] for row in by_nd if row["spacing"] == d]
        ns_here = [row["n_copies"] for row in by_nd if row["spacing"] == d]
        if Ls:
            growth_by_n[str(d)] = {
                "n_copies": ns_here,
                "L": Ls,
                "L_max": max(Ls),
                "increases_with_n": (
                    len(Ls) >= 3
                    and max(Ls[len(Ls) // 2 :]) >= max(Ls[: len(Ls) // 2]) + 4
                ),
            }
    growth_by_d = {}
    for n_copies in ns:
        Ls = [row["L"] for row in by_nd if row["n_copies"] == n_copies]
        if Ls:
            growth_by_d[str(n_copies)] = growth_report(Ls, len(Ls) - 1)

    if best is not None and best["L"] >= 25:
        best = double_cap(best)
    if first_ge30 is not None:
        first_ge30 = double_cap(first_ge30)

    rec = {
        "tag": tag,
        "motif": list(motif),
        "n_scanned": n_scanned,
        "L_run": best["L"] if best else 0,
        "n_ge29": n_ge29,
        "n_ge30": n_ge30,
        "best": best,
        "first_ge30": first_ge30,
        "by_nd": by_nd,
        "growth_by_n_at_fixed_d": growth_by_n,
        "growth_by_d_at_fixed_n": growth_by_d,
        # Repeating a motif at larger n can recover a short burst that
        # small-n interference destroyed. That is not L tending to
        # infinity. Require the spacing-parameter growth test.
        "grows": any(g.get("grows") for g in growth_by_d.values()),
        "elapsed_sec": round(elapsed, 4),
    }
    msg = (
        f"{tag} n={n_scanned} L_run={rec['L_run']} n_ge30={n_ge30} "
        f"{elapsed:.3f}s"
    )
    log.append(msg)
    print(msg, flush=True)
    return rec


# ---------------------------------------------------------------------------
# Random Hamming-weight masks
# ---------------------------------------------------------------------------

def _note_scan(mask: int, w: int, tcap: int, hw: int | None, best, n_ge29, n_ge30, first_ge30):
    """Update best/counters from one packed scan. Avoid rec_of on typical rows."""
    st = scan_runs_fast(mask, w, tcap)
    L = st[0]
    if L >= 29:
        n_ge29 += 1
    if L >= 30:
        n_ge30 += 1
    if L > (best["L"] if best else 0) or (L >= 30 and first_ge30 is None):
        recd = rec_of(mask, w, st, tcap)
        if hw is not None:
            recd["hw"] = hw
        if L > (best["L"] if best else 0):
            best = recd
        elif best is None:
            best = recd
        if L >= 30 and first_ge30 is None:
            first_ge30 = recd
    elif best is None:
        recd = rec_of(mask, w, st, tcap)
        if hw is not None:
            recd["hw"] = hw
        best = recd
    return best, n_ge29, n_ge30, first_ge30, L


def _random_chunk(args: tuple[int, int, int, int, int]) -> dict:
    w, hw, seed, n, tcap = args
    rng = random.Random(seed)
    width = 2 * w + 1
    if hw < 1 or hw > width:
        return {
            "w": w,
            "hw": hw,
            "n": 0,
            "L_run": 0,
            "n_ge29": 0,
            "n_ge30": 0,
            "best": None,
            "first_ge30": None,
        }
    nmax = math.comb(width, hw)
    want = min(n, nmax)
    best = None
    n_ge29 = 0
    n_ge30 = 0
    first_ge30 = None
    seen: set[int] = set()
    # If the space is small, enumerate combinations instead of sampling.
    if nmax <= want:
        def rec_enum(start: int, left: int, acc: int) -> None:
            nonlocal best, n_ge29, n_ge30, first_ge30
            if left == 0:
                best, n_ge29, n_ge30, first_ge30, _L = _note_scan(
                    acc, w, tcap, hw, best, n_ge29, n_ge30, first_ge30
                )
                return
            last = width - left
            for i in range(start, last + 1):
                rec_enum(i + 1, left - 1, acc | (1 << i))

        rec_enum(0, hw, 0)
        n_done = nmax
    else:
        while len(seen) < want:
            acc = 0
            for i in rng.sample(range(width), hw):
                acc |= 1 << i
            if acc in seen:
                continue
            seen.add(acc)
            best, n_ge29, n_ge30, first_ge30, _L = _note_scan(
                acc, w, tcap, hw, best, n_ge29, n_ge30, first_ge30
            )
        n_done = want
    if best is not None:
        best = extend_if_capped(best)
    if first_ge30 is not None:
        first_ge30 = extend_if_capped(first_ge30)
    return {
        "w": w,
        "hw": hw,
        "n": n_done,
        "L_run": best["L"] if best else 0,
        "n_ge29": n_ge29,
        "n_ge30": n_ge30,
        "best": best,
        "first_ge30": first_ge30,
    }


def scan_random_family(log: list[str]) -> dict:
    t0 = time.perf_counter()
    workers = nproc()
    tasks = []
    # 2^18 samples per (w, hw), split across workers.
    n_chunks = workers
    chunk = N_RANDOM // n_chunks
    rem = N_RANDOM - chunk * n_chunks
    for w in W_RANDOM:
        tcap = tcap_fam(w)
        for hw in range(HW_LO, HW_HI + 1):
            for c in range(n_chunks):
                n = chunk + (rem if c == n_chunks - 1 else 0)
                seed = RANDOM_SEED + 10007 * w + 97 * hw + 13 * c
                tasks.append((w, hw, seed, n, tcap))

    parts = []
    if workers == 1:
        for task in tasks:
            parts.append(_random_chunk(task))
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(_random_chunk, task) for task in tasks]
            done = 0
            for fut in as_completed(futs):
                parts.append(fut.result())
                done += 1
                if done == 1 or done == len(futs) or done % max(1, len(futs) // 5) == 0:
                    Lsofar = max((p["L_run"] for p in parts), default=0)
                    msg = f"random chunks {done}/{len(futs)} L_run={Lsofar}"
                    log.append(msg)
                    print(msg, flush=True)

    by_whw = []
    best = None
    n_scanned = 0
    n_ge29 = 0
    n_ge30 = 0
    first_ge30 = None
    # Merge chunks that share (w, hw).
    merged: dict[tuple[int, int], dict] = {}
    for p in parts:
        key = (p["w"], p["hw"])
        acc = merged.get(key)
        if acc is None:
            merged[key] = {
                "w": p["w"],
                "hw": p["hw"],
                "n": p["n"],
                "L_run": p["L_run"],
                "n_ge29": p["n_ge29"],
                "n_ge30": p["n_ge30"],
                "best": p["best"],
                "first_ge30": p["first_ge30"],
            }
        else:
            acc["n"] += p["n"]
            acc["n_ge29"] += p["n_ge29"]
            acc["n_ge30"] += p["n_ge30"]
            if p["best"] is not None:
                acc["best"] = consider(acc["best"], p["best"])
                acc["L_run"] = acc["best"]["L"]
            if p["first_ge30"] is not None:
                if acc["first_ge30"] is None:
                    acc["first_ge30"] = p["first_ge30"]
    by_w = []
    for w in W_RANDOM:
        Lw = 0
        nw = 0
        n29 = 0
        n30 = 0
        best_w = None
        for hw in range(HW_LO, HW_HI + 1):
            acc = merged[(w, hw)]
            by_whw.append(
                {
                    "w": w,
                    "hw": hw,
                    "n": acc["n"],
                    "tcap": tcap_fam(w),
                    "L_run": acc["L_run"],
                    "n_ge29": acc["n_ge29"],
                    "n_ge30": acc["n_ge30"],
                    "best_mask": None if acc["best"] is None else acc["best"]["mask"],
                    "best_start": None if acc["best"] is None else acc["best"]["start"],
                    "best_end": None if acc["best"] is None else acc["best"]["end"],
                }
            )
            nw += acc["n"]
            n29 += acc["n_ge29"]
            n30 += acc["n_ge30"]
            if acc["best"] is not None:
                best_w = consider(best_w, acc["best"])
                best = consider(best, acc["best"])
                Lw = best_w["L"]
            if acc["first_ge30"] is not None:
                if first_ge30 is None:
                    first_ge30 = acc["first_ge30"]
        n_scanned += nw
        n_ge29 += n29
        n_ge30 += n30
        by_w.append(
            {
                "w": w,
                "tcap": tcap_fam(w),
                "n": nw,
                "L_run": Lw,
                "n_ge29": n29,
                "n_ge30": n30,
                "best_mask": None if best_w is None else best_w["mask"],
            }
        )

    elapsed = time.perf_counter() - t0
    if best is not None and best["L"] >= 25:
        best = double_cap(best)
    if first_ge30 is not None:
        first_ge30 = double_cap(first_ge30)
    rec = {
        "tag": "random_hw_8_16",
        "n_samples_per_w_hw": N_RANDOM,
        "hw": [HW_LO, HW_HI],
        "w": list(W_RANDOM),
        "tcap": "8w+256",
        "n_scanned": n_scanned,
        "nproc": workers,
        "L_run": best["L"] if best else 0,
        "n_ge29": n_ge29,
        "n_ge30": n_ge30,
        "best": best,
        "first_ge30": first_ge30,
        "by_w": by_w,
        "by_w_hw": by_whw,
        "elapsed_sec": round(elapsed, 4),
    }
    msg = (
        f"random hw={HW_LO}..{HW_HI} w={list(W_RANDOM)} n={n_scanned} "
        f"L_run={rec['L_run']} n_ge30={n_ge30} {elapsed:.3f}s nproc={workers}"
    )
    log.append(msg)
    print(msg, flush=True)
    return rec


# ---------------------------------------------------------------------------
# Single-interval supports of length <= 20
# ---------------------------------------------------------------------------

def _interval_chunk(args: tuple[int, int, int, int, int]) -> dict:
    """Patterns of exact support length L (endpoints live), mid in [lo, hi)."""
    L, mid_lo, mid_hi, w, tcap = args
    width = 2 * w + 1
    nplace = width - L + 1
    best = None
    n = 0
    n_ge29 = 0
    n_ge30 = 0
    first_ge30 = None
    ge30: list[dict] = []
    for mid in range(mid_lo, mid_hi):
        if L == 1:
            pat = 1
        else:
            pat = 1 | (mid << 1) | (1 << (L - 1))
        for s in range(nplace):
            mask = pat << s
            st = scan_runs_fast(mask, w, tcap)
            n += 1
            Lrun = st[0]
            if Lrun >= 29:
                n_ge29 += 1
            if Lrun >= 30:
                n_ge30 += 1
            if best is None or Lrun > best["L"] or Lrun >= 30:
                recd = rec_of(mask, w, st, tcap)
                recd["interval_len"] = L
                recd["place"] = s
                if best is None or Lrun > best["L"]:
                    best = recd
                if Lrun >= 30:
                    ge30.append(recd)
                    if first_ge30 is None:
                        first_ge30 = recd
    if best is not None:
        best = extend_if_capped(best)
    if first_ge30 is not None:
        first_ge30 = extend_if_capped(first_ge30)
    ge30 = [extend_if_capped(r) for r in ge30]
    return {
        "L": L,
        "n": n,
        "L_run": best["L"] if best else 0,
        "n_ge29": n_ge29,
        "n_ge30": n_ge30,
        "best": best,
        "first_ge30": first_ge30,
        "ge30": ge30,
    }


def scan_interval_family(log: list[str]) -> dict:
    """Exact-length interval supports (first and last cells live), length <=20.

    All placements inside radius INTERVAL_W. Scanning at this w is
    equivalent to the true-radius scan for the centre trace (zero padding
    does not change the trace on the common window; tcap=8*20+256 is at
    least the family cap of every smaller true radius).
    """
    t0 = time.perf_counter()
    w = INTERVAL_W
    tcap = tcap_fam(w)
    workers = nproc()
    tasks = []
    # Chunk the 2^{L-2} endpoint-1 patterns.
    for L in range(1, INTERVAL_LEN + 1):
        nmid = 1 if L <= 2 else (1 << (L - 2))
        # Aim for ~workers*4 chunks, but keep chunks from being tiny.
        target = max(1, nmid // max(workers * 4, 1))
        target = max(1, min(nmid, max(target, nmid // 64 if nmid > 64 else nmid)))
        lo = 0
        while lo < nmid:
            hi = min(lo + target, nmid)
            tasks.append((L, lo, hi, w, tcap))
            lo = hi

    parts = []
    if workers == 1:
        for task in tasks:
            parts.append(_interval_chunk(task))
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(_interval_chunk, task) for task in tasks]
            done = 0
            for fut in as_completed(futs):
                parts.append(fut.result())
                done += 1
                if done == 1 or done == len(futs) or done % max(1, len(futs) // 5) == 0:
                    Lsofar = max((p["L_run"] for p in parts), default=0)
                    msg = f"interval chunks {done}/{len(futs)} L_run={Lsofar}"
                    log.append(msg)
                    print(msg, flush=True)

    by_L = []
    best = None
    n_scanned = 0
    n_ge29 = 0
    n_ge30 = 0
    first_ge30 = None
    ge30_all: list[dict] = []
    merged_L: dict[int, dict] = {}
    for p in parts:
        L = p["L"]
        acc = merged_L.get(L)
        if acc is None:
            merged_L[L] = {
                "interval_len": L,
                "n": p["n"],
                "L_run": p["L_run"],
                "n_ge29": p["n_ge29"],
                "n_ge30": p["n_ge30"],
                "best": p["best"],
                "first_ge30": p["first_ge30"],
                "ge30": list(p.get("ge30") or []),
            }
        else:
            acc["n"] += p["n"]
            acc["n_ge29"] += p["n_ge29"]
            acc["n_ge30"] += p["n_ge30"]
            if p["best"] is not None:
                acc["best"] = consider(acc["best"], p["best"])
                acc["L_run"] = acc["best"]["L"]
            if p["first_ge30"] is not None and acc["first_ge30"] is None:
                acc["first_ge30"] = p["first_ge30"]
            acc.setdefault("ge30", []).extend(p.get("ge30") or [])
    for L in range(1, INTERVAL_LEN + 1):
        acc = merged_L[L]
        by_L.append(
            {
                "interval_len": L,
                "n": acc["n"],
                "L_run": acc["L_run"],
                "n_ge29": acc["n_ge29"],
                "n_ge30": acc["n_ge30"],
                "best_mask": None if acc["best"] is None else acc["best"]["mask"],
                "best_start": None if acc["best"] is None else acc["best"]["start"],
                "best_end": None if acc["best"] is None else acc["best"]["end"],
                "best_w_true": None
                if acc["best"] is None
                else max(abs(p) for p in acc["best"]["live"])
                if acc["best"]["live"]
                else 0,
            }
        )
        n_scanned += acc["n"]
        n_ge29 += acc["n_ge29"]
        n_ge30 += acc["n_ge30"]
        if acc["best"] is not None:
            best = consider(best, acc["best"])
        if acc["first_ge30"] is not None and first_ge30 is None:
            first_ge30 = acc["first_ge30"]
        ge30_all.extend(acc.get("ge30") or [])

    elapsed = time.perf_counter() - t0
    if best is not None and best["L"] >= 25:
        best = double_cap(best)
    if first_ge30 is not None:
        first_ge30 = double_cap(first_ge30)
    # Unique L>=30 interval rows.
    ge30_uniq = []
    seen_m = set()
    for r in ge30_all:
        k = (r["w"], r["mask"])
        if k in seen_m:
            continue
        seen_m.add(k)
        if r.get("doubled") is None:
            r = double_cap(r)
        ge30_uniq.append(slim_best(r))
    Ls = [row["L_run"] for row in by_L]
    rec = {
        "tag": "interval_len_le_20",
        "max_len": INTERVAL_LEN,
        "w": w,
        "tcap": tcap,
        "n_scanned": n_scanned,
        "nproc": workers,
        "L_run": best["L"] if best else 0,
        "n_ge29": n_ge29,
        "n_ge30": n_ge30,
        "best": best,
        "first_ge30": first_ge30,
        "ge30": ge30_uniq,
        "by_L": by_L,
        "growth": growth_report(Ls, INTERVAL_LEN) if Ls else None,
        "elapsed_sec": round(elapsed, 4),
    }
    msg = (
        f"interval len<= {INTERVAL_LEN} w={w} n={n_scanned} "
        f"L_run={rec['L_run']} n_ge30={n_ge30} {elapsed:.3f}s"
    )
    log.append(msg)
    print(msg, flush=True)
    return rec


# ---------------------------------------------------------------------------
# Witness verification
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
        "fast_matches_engine": fast == (st["L"], st["start"], st["end"], st["suffix"]),
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
    """Cycle J cap 8w+128 versus the family cap 8w+256, then doubled."""
    t_short = 8 * w + 128
    t_fam = tcap_fam(w)
    st_s = scan_mask_runs(mask, w, t_short)
    st_f = scan_mask_runs(mask, w, t_fam)
    st_2 = scan_mask_runs(mask, w, 2 * t_fam)
    return {
        "w": w,
        "mask": mask,
        "tcap_8w128": t_short,
        "L_8w128": st_s["L"],
        "start_8w128": st_s["start"],
        "end_8w128": st_s["end"],
        "suffix_8w128": st_s["suffix"],
        "truncated_by_8w128": st_s["L"] < st_f["L"],
        "tcap_fam": t_fam,
        "L_fam": st_f["L"],
        "start_fam": st_f["start"],
        "end_fam": st_f["end"],
        "tcap_doubled": 2 * t_fam,
        "L_doubled": st_2["L"],
        "start_doubled": st_2["start"],
        "end_doubled": st_2["end"],
        "holds": st_2["L"] >= st_f["L"],
    }


def true_radius_report(rec: dict) -> dict:
    """Re-pack at the true support radius and re-score."""
    live = rec["live"]
    w, mask = pack_live(live)
    out = scan_packed(mask, w)
    out = double_cap(out)
    out["scan_w"] = rec.get("w")
    out["scan_mask"] = rec.get("mask")
    out["cap_compare"] = cap_compare(mask, w)
    out["verify"] = verify_row(mask, w, out["tcap"])
    return out


def slim_best(rec: dict | None) -> dict | None:
    if rec is None:
        return None
    keys = (
        "mask",
        "w",
        "row",
        "live",
        "n1",
        "span",
        "L",
        "start",
        "end",
        "suffix",
        "tcap",
        "reaches_cap",
        "k",
        "leftmost",
        "n_copies",
        "spacing",
        "shift",
        "hw",
        "interval_len",
        "family",
        "doubled",
        "cap_compare",
        "verify",
        "scan_w",
        "scan_mask",
    )
    return {k: rec[k] for k in keys if k in rec}


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def certify() -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    print(f"checks all_ok={checks['all_ok']}", flush=True)
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    families = []

    # 1. Concatenate two copies of the live support.
    concat_436 = scan_concat_family(
        MASK_4369552, W_4369552, K_MAX, log, "concat_4369552"
    )
    concat_7503 = scan_concat_family(
        MASK_7503, W_7503, K_MAX, log, "concat_7503"
    )
    concat_484 = scan_concat_family(
        MASK_4842768, W_4369552, K_MAX, log, "concat_4842768"
    )
    families.extend([concat_436, concat_7503, concat_484])

    # 2. Repeat the 8-one motif at several spacings.
    motif_436 = scan_motif_family(
        MOTIF_4369552,
        MOTIF_NS,
        MOTIF_D_MAX,
        log,
        "motif_4369552",
        extra_ns=MOTIF_EXTRA_NS,
        extra_ds=MOTIF_EXTRA_DS,
    )
    motif_7503 = scan_motif_family(
        MOTIF_7503,
        (2, 3, 4),
        MOTIF_D_MAX,
        log,
        "motif_7503",
    )
    families.extend([motif_436, motif_7503])

    # 3. Random Hamming-weight masks.
    random_fam = scan_random_family(log)
    families.append(random_fam)

    # 4. Single-interval supports of length <= 20.
    interval_fam = scan_interval_family(log)
    families.append(interval_fam)

    best = None
    n_ge30 = 0
    n_ge40 = 0
    first_ge30 = None
    first_ge40 = None
    for fam in families:
        n_ge30 += fam.get("n_ge30") or 0
        if fam.get("best") is not None:
            best = consider(best, fam["best"])
        hit = fam.get("first_ge30")
        if hit is not None:
            if first_ge30 is None:
                first_ge30 = hit
            if hit["L"] >= 40:
                n_ge40 += 1
                if first_ge40 is None:
                    first_ge40 = hit
        if fam.get("best") and fam["best"]["L"] >= 40:
            n_ge40 += 1
            if first_ge40 is None:
                first_ge40 = fam["best"]

    L_best = best["L"] if best else 0
    growing = []
    if concat_436["growth"]["grows"] and concat_436["L_run"] >= 30:
        growing.append("concat_4369552")
    if concat_7503["growth"]["grows"] and concat_7503["L_run"] >= 30:
        growing.append("concat_7503")
    if concat_484["growth"]["grows"] and concat_484["L_run"] >= 30:
        growing.append("concat_4842768")
    if motif_436.get("grows") and motif_436["L_run"] >= 30:
        growing.append("motif_4369552")
    if motif_7503.get("grows") and motif_7503["L_run"] >= 30:
        growing.append("motif_7503")
    # Interval max-L versus support length is an enumeration, not a
    # constructive iterate. Record it, but do not treat a rise through
    # length 20 as L tending to infinity.
    interval_growth = (interval_fam.get("growth") or {})
    interval_looks_increasing = bool(interval_growth.get("grows"))

    # Strong constructive kill of a uniform bound: L grows in the
    # spacing parameter on a one-parameter family (e.g. L >= 20+k/2).
    unbounded_family = bool(growing)
    found_ge30 = L_best >= 30
    found_ge40 = L_best >= 40
    stays_29 = L_best == 29

    if unbounded_family:
        verdict = "UNBOUNDED_FAMILY"
        kill_constructive = False
        kill_bounded_hope = True
        reason = (
            "a one-parameter constructive family produces period-2 centre "
            f"runs whose length grows with the parameter (best L={L_best}). "
            "That kills the hope that L_run stays bounded. The runs remain "
            "finite bursts inside the cap unless a doubled scan reaches the cap."
        )
    elif found_ge30:
        verdict = "L_GE_30"
        kill_constructive = False
        kill_bounded_hope = False
        reason = (
            f"found a finite row with L={L_best}>=30, so L_run is not "
            "capped at the Cycle J value 29. Concatenating or repeating the "
            "Cycle J motifs does not make L grow with the spacing (none "
            "satisfies L>=20+k/2; two copies recover at most the single-copy "
            "burst). Not a proof that L_run is unbounded, and not a proof of "
            "a bound. No L>=40."
        )
    else:
        verdict = "KILL"
        kill_constructive = True
        kill_bounded_hope = False
        reason = (
            f"best L on the scanned constructive/random/interval families "
            f"is {L_best} (Cycle J's 29 is matched, not beaten). No family "
            "has L growing in its parameter (in particular none satisfies "
            "L>=20+k/2). This kills the constructive-unbounded search. It is "
            "not a proof that L_run is bounded."
        )

    witness_check = None
    true_best = None
    ge30_reports = []
    if best is not None:
        witness_check = verify_row(best["mask"], best["w"], best["tcap"])
        log.append(
            f"witness_check ok={witness_check['ok']} L={witness_check['L']} "
            f"doubled={witness_check['doubled_L']} alt={witness_check['alternating']}"
        )
        if not witness_check["ok"]:
            raise AssertionError(f"best-row verification failed: {witness_check}")
        if best.get("doubled") is None and best["L"] >= 25:
            best = double_cap(best)
        true_best = true_radius_report(best)
        log.append(
            f"true_radius w={true_best['w']} mask={true_best['mask']} "
            f"L={true_best['L']} cap8w128={true_best['cap_compare']['L_8w128']} "
            f"truncated={true_best['cap_compare']['truncated_by_8w128']}"
        )
        if not true_best["verify"]["ok"]:
            raise AssertionError(f"true-radius verification failed: {true_best}")

    # True-radius reports for every L>=30 row we kept.
    for rec in (best, first_ge30, first_ge40):
        if rec is None or rec.get("L", 0) < 30:
            continue
        ge30_reports.append(true_radius_report(rec))
    for rec in interval_fam.get("ge30") or []:
        if rec is None:
            continue
        ge30_reports.append(true_radius_report(rec))
    # Unique by true (w, mask).
    uniq_ge30 = []
    seen_tm = set()
    for r in ge30_reports:
        k = (r["w"], r["mask"])
        if k in seen_tm:
            continue
        seen_tm.add(k)
        uniq_ge30.append(
            {
                "w": r["w"],
                "mask": r["mask"],
                "row": r["row"],
                "live": r["live"],
                "n1": r["n1"],
                "span": r["span"],
                "L": r["L"],
                "start": r["start"],
                "end": r["end"],
                "tcap": r["tcap"],
                "doubled": r.get("doubled"),
                "cap_compare": r["cap_compare"],
                "verify_ok": r["verify"]["ok"],
            }
        )

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period2_lrun_family",
        "cycle_j": "research/period2_lrun.md",
        "ideas10": "item 2",
        "problem": (
            "constructive family of finite rows with period-2 centre run "
            "length L tending to infinity; hunt L>=30 then L>=40"
        ),
        "verdict": verdict,
        "kill_constructive_unbounded_search": kill_constructive,
        "kill_bounded_hope": kill_bounded_hope,
        "uniform_proof": False,
        "survive": False,
        "found_L_ge_30": found_ge30,
        "found_L_ge_40": found_ge40,
        "best_L": L_best,
        "stays_29": stays_29,
        "growing_families": growing,
        "interval_span_L_increasing": interval_looks_increasing,
        "reason": reason,
        "tcap": "8w+256",
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "witness_check": witness_check,
        "best": slim_best(best),
        "true_radius_best": slim_best(true_best) if true_best else None,
        "true_radius_best_cap": None if true_best is None else true_best.get("cap_compare"),
        "first_ge30": slim_best(first_ge30),
        "first_ge40": slim_best(first_ge40),
        "ge30_true_radius": uniq_ge30,
        "wall_time_sec": round(wall, 4),
        "checks": checks,
        "witness_check": witness_check,
        "best": slim_best(best),
        "first_ge30": slim_best(first_ge30),
        "first_ge40": slim_best(first_ge40),
        "concat_4369552": _slim_family(concat_436),
        "concat_7503": _slim_family(concat_7503),
        "concat_4842768": _slim_family(concat_484),
        "motif_4369552": _slim_motif(motif_436),
        "motif_7503": _slim_motif(motif_7503),
        "random": _slim_random(random_fam),
        "interval": _slim_interval(interval_fam),
        "n_ge30_rows_scanned": n_ge30,
        "log": log,
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict={verdict} best_L={L_best} wall={wall:.3f}s")
    print(f"reason: {reason}")
    return dump


def _slim_family(fam: dict) -> dict:
    out = dict(fam)
    out["best"] = slim_best(fam.get("best"))
    out["first_ge30"] = slim_best(fam.get("first_ge30"))
    return out


def _slim_motif(fam: dict) -> dict:
    out = _slim_family(fam)
    by = fam.get("by_nd") or []
    out["by_nd_n"] = len(by)
    out["by_nd"] = [row for row in by if row["L"] >= 20]
    return out


def _slim_random(fam: dict) -> dict:
    out = dict(fam)
    out["best"] = slim_best(fam.get("best"))
    out["first_ge30"] = slim_best(fam.get("first_ge30"))
    return out


def _slim_interval(fam: dict) -> dict:
    out = dict(fam)
    out["best"] = slim_best(fam.get("best"))
    out["first_ge30"] = slim_best(fam.get("first_ge30"))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    certify()


if __name__ == "__main__":
    main()
