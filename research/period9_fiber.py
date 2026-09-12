#!/usr/bin/env python3
"""Cycle I ideas9 item 4: exhaustive finite-row scan for period-9 isolated zero.

The strip-graph residual for q=8 (centre word 011111111, period 9) is
still nonempty (research/period9_q8.md). Cycle I's period-2 finite-row
scan is the model: packed Rule 30 on every nonzero row of support radius
w, longest exact period-9 centre run.

This is not the strip-graph residual-SCC test, not onset SAT, and not a
prize claim. Stdlib only. Does not modify experiment.py, strip_graph.py,
strip_extend.py, period2_fiber.*, or period3_fiber.*.

Run: python3 research/period9_fiber.py
Dump: research/period9_fiber.json
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

OUT = Path(__file__).resolve().with_suffix(".json")

PERIOD = 9
ISO_WORD = "011111111"
W_MAX_DEFAULT = 7
# Eventual-in-cap: suffix covers at least two isolated-zero periods and
# the last break sits inside the light-cone transient.
MIN_EVENTUAL_SUFFIX = 18


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


def tcap_long(w: int) -> int:
    return 8 * w + 128


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


def min_period(block: str) -> int:
    n = len(block)
    for p in range(1, n + 1):
        if n % p == 0 and block == block[:p] * (n // p):
            return p
    return n


def rotations(word: str) -> list[str]:
    return [word[i:] + word[:i] for i in range(len(word))]


ISO_ROTS = tuple(rotations(ISO_WORD))
ISO_ROT_SET = frozenset(ISO_ROTS)


def _window_tables(p: int = PERIOD) -> tuple[list[int], list[int], list[str]]:
    """iso_flag[w], prim_flag[w], bits9[w] for every 9-bit window w.

    Window integer: MSB is the oldest bit (time t-8), LSB is time t,
    matching format(w, '09b') == ''.join(map(str, bits[t-8:t+1])).
    """
    n = 1 << p
    iso = [0] * n
    prim = [0] * n
    bits9 = [""] * n
    for w in range(n):
        s = format(w, f"0{p}b")
        bits9[w] = s
        if s in ISO_ROT_SET:
            iso[w] = 1
        if min_period(s) == p:
            prim[w] = 1
    return iso, prim, bits9


ISO_FLAG, PRIM_FLAG, BITS9 = _window_tables()


def brute_longest_p9(
    bits: list[int],
    allowed: frozenset[str] | None,
    require_primitive: bool,
    p: int = PERIOD,
) -> tuple[int, int, str]:
    """Longest exact period-p run. Returns (L, start, block). L=0 if none."""
    n = len(bits)
    best = 0
    best_start = 0
    best_block = ""
    if n < p:
        return 0, 0, ""
    for s in range(0, n - p + 1):
        block = "".join("1" if bits[s + i] else "0" for i in range(p))
        if allowed is not None and block not in allowed:
            continue
        if require_primitive and min_period(block) != p:
            continue
        e = s + p
        while e < n and bits[e] == bits[e - p]:
            e += 1
        L = e - s
        if L > best:
            best = L
            best_start = s
            best_block = block
    return best, best_start, best_block


def analyze_centers(bits: list[int], p: int = PERIOD) -> dict:
    """One-pass window scan for isolated-zero and any exact period-p runs.

    A run of length L >= p is a consecutive centre factor whose repeating
    p-block is (iso) a rotation of 011111111, or (any) a primitive p-bit
    word. Length p with no further match still counts: the block appears.
    """
    n = len(bits)
    empty = {
        "L_iso": 0,
        "start_iso": 0,
        "end_iso": 0,
        "block_iso": "",
        "prefix_iso": 0,
        "suffix_iso": 0,
        "L_any": 0,
        "start_any": 0,
        "end_any": 0,
        "block_any": "",
        "prefix_any": 0,
        "suffix_any": 0,
        "reaches_cap_iso": False,
        "reaches_cap_any": False,
    }
    if n < p:
        return empty

    w = 0
    run_iso = 0
    run_iso_start = 0
    best_iso = 0
    best_iso_start = 0
    run_any = 0
    run_any_start = 0
    best_any = 0
    best_any_start = 0
    prefix_iso = 0
    prefix_iso_alive = True
    prefix_any = 0
    prefix_any_alive = True

    for t, bit in enumerate(bits):
        w = ((w << 1) | (bit & 1)) & ((1 << p) - 1)
        if t < p - 1:
            continue
        iso = ISO_FLAG[w]
        prim = PRIM_FLAG[w]
        # Continuation of a length-p run is bits[t] == bits[t-p]. Consecutive
        # primitive 9-windows that do not match at lag 9 are a new block, not
        # one run (the isolated-zero necklace is the exception: consecutive
        # iso windows are automatically the unique shift).
        cont = t >= p and bit == bits[t - p]
        if iso:
            if run_iso and cont:
                run_iso += 1
                if prefix_iso_alive:
                    prefix_iso += 1
            else:
                run_iso = p
                run_iso_start = t - (p - 1)
                if t == p - 1:
                    prefix_iso = p
                else:
                    prefix_iso_alive = False
            if run_iso > best_iso:
                best_iso = run_iso
                best_iso_start = run_iso_start
        else:
            run_iso = 0
            prefix_iso_alive = False
        if prim:
            if run_any and cont:
                run_any += 1
                if prefix_any_alive:
                    prefix_any += 1
            else:
                run_any = p
                run_any_start = t - (p - 1)
                if t == p - 1:
                    prefix_any = p
                else:
                    prefix_any_alive = False
            if run_any > best_any:
                best_any = run_any
                best_any_start = run_any_start
        else:
            run_any = 0
            prefix_any_alive = False

    block_iso = ""
    if best_iso >= p:
        block_iso = "".join(
            "1" if bits[best_iso_start + i] else "0" for i in range(p)
        )
    block_any = ""
    if best_any >= p:
        block_any = "".join(
            "1" if bits[best_any_start + i] else "0" for i in range(p)
        )
    end_iso = best_iso_start + best_iso if best_iso else 0
    end_any = best_any_start + best_any if best_any else 0
    return {
        "L_iso": best_iso,
        "start_iso": best_iso_start,
        "end_iso": end_iso,
        "block_iso": block_iso,
        "prefix_iso": prefix_iso,
        "suffix_iso": run_iso,
        "L_any": best_any,
        "start_any": best_any_start,
        "end_any": end_any,
        "block_any": block_any,
        "prefix_any": prefix_any,
        "suffix_any": run_any,
        "reaches_cap_iso": best_iso >= p and end_iso == n,
        "reaches_cap_any": best_any >= p and end_any == n,
    }


def scan_mask(mask: int, w: int, tcap: int) -> dict:
    bits = evolve_centers(mask, w, tcap)
    st = analyze_centers(bits)
    st["tcap"] = tcap
    return st


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


def row_bits(mask: int, w: int) -> str:
    return "".join(str((mask >> i) & 1) for i in range(2 * w + 1))


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def prize_prefix(n: int = 16) -> str:
    return "".join(map(str, evolve_centers(1, 0, n)))


def run_checks() -> dict:
    checks: dict = {}

    prize = evolve_centers(1, 0, 32)
    naive_prize = naive_centers({0: 1}, 32)
    checks["packed_matches_naive_prize"] = prize == naive_prize
    exp = list(experiment_center_bits(64))
    packed64 = evolve_centers(1, 0, 64)
    checks["packed_matches_experiment_center_bits"] = packed64 == exp
    checks["prize_prefix16"] = "".join(map(str, prize[:16]))
    checks["prize_prefix16_ok"] = checks["prize_prefix16"] == "1101110011000101"
    checks["prize_prefix20_ok"] = prize[:20] == [
        1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    ]

    for w, mask in [(1, 5), (2, 19), (3, 73), (4, 300), (5, 1023)]:
        a = evolve_centers(mask, w, 40)
        b = naive_centers(mask_to_live(mask, w), 40)
        if a != b:
            checks["packed_matches_naive_small"] = False
            checks["naive_fail"] = {"w": w, "mask": mask}
            break
    else:
        checks["packed_matches_naive_small"] = True

    checks["iso_rotations"] = list(ISO_ROTS)
    checks["n_iso_rotations"] = len(ISO_ROT_SET)
    checks["iso_rotations_distinct"] = len(ISO_ROT_SET) == PERIOD
    checks["iso_word_primitive"] = min_period(ISO_WORD) == PERIOD
    checks["all_ones_not_primitive9"] = min_period("1" * PERIOD) != PERIOD
    checks["all_zeros_not_primitive9"] = min_period("0" * PERIOD) != PERIOD
    checks["001_rep_not_primitive9"] = min_period("001" * 3) != PERIOD
    n_prim = sum(PRIM_FLAG)
    checks["n_primitive9_words"] = n_prim
    checks["n_primitive9_words_ok"] = n_prim == (1 << PERIOD) - (1 << 3)
    checks["n_iso_windows"] = sum(ISO_FLAG)
    checks["n_iso_windows_ok"] = sum(ISO_FLAG) == PERIOD

    # Synthetic traces vs brute force.
    synth_ok = True
    synth_fail = None
    cases = [
        ([0, 1, 1, 1, 1, 1, 1, 1, 1] * 3, 27, 27),
        # Trailing 0 is the correct next isolated-zero bit, so L=10.
        ([0, 1, 1, 1, 1, 1, 1, 1, 1] + [0], 10, 10),
        # Trailing 1 breaks the necklace after one block.
        ([0, 1, 1, 1, 1, 1, 1, 1, 1] + [1], 9, 9),
        ([1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], 0, 10),
        # (01)^∞ has odd-length 9-windows of min-period 9, but lag-9 fails,
        # so L_any=9 and L_iso=0.
        ([0, 1] * 20, 0, 9),
        ([1] * 20, 0, 0),
        ([0] * 20, 0, 0),
        ([1, 1, 1, 1, 1, 1, 1, 1, 0] + [1, 1, 1, 1, 1, 1, 1, 1], 17, 17),
    ]
    for bits, expect_iso, expect_any in cases:
        st = analyze_centers(bits)
        bi, _, _ = brute_longest_p9(bits, ISO_ROT_SET, True)
        ba, _, _ = brute_longest_p9(bits, None, True)
        if st["L_iso"] != expect_iso or st["L_any"] != expect_any:
            synth_ok = False
            synth_fail = {
                "bits": "".join(map(str, bits)),
                "got_iso": st["L_iso"],
                "expect_iso": expect_iso,
                "got_any": st["L_any"],
                "expect_any": expect_any,
            }
            break
        if st["L_iso"] != bi or st["L_any"] != ba:
            synth_ok = False
            synth_fail = {
                "bits": "".join(map(str, bits)),
                "window_iso": st["L_iso"],
                "brute_iso": bi,
                "window_any": st["L_any"],
                "brute_any": ba,
            }
            break
    checks["synthetic_p9_runs"] = synth_ok
    if synth_fail is not None:
        checks["synthetic_fail"] = synth_fail

    # Window scan vs brute on the prize seed and a few packed rows.
    brute_ok = True
    for w, mask, tcap in [(0, 1, 128), (1, 5, 40), (2, 19, 48), (3, 73, 56)]:
        bits = evolve_centers(mask, w, tcap)
        st = analyze_centers(bits)
        bi, _, _ = brute_longest_p9(bits, ISO_ROT_SET, True)
        ba, _, _ = brute_longest_p9(bits, None, True)
        if st["L_iso"] != bi or st["L_any"] != ba:
            brute_ok = False
            checks["brute_fail"] = {
                "w": w,
                "mask": mask,
                "window_iso": st["L_iso"],
                "brute_iso": bi,
                "window_any": st["L_any"],
                "brute_any": ba,
            }
            break
        pref_iso_brute = 0
        block0 = "".join("1" if bits[i] else "0" for i in range(PERIOD))
        if block0 in ISO_ROT_SET:
            pref_iso_brute = PERIOD
            t = PERIOD
            while t < tcap and bits[t] == bits[t - PERIOD]:
                pref_iso_brute += 1
                t += 1
        if st["prefix_iso"] != pref_iso_brute:
            brute_ok = False
            checks["prefix_fail"] = {
                "w": w,
                "mask": mask,
                "window": st["prefix_iso"],
                "brute": pref_iso_brute,
            }
            break
    checks["window_matches_brute"] = brute_ok

    checks["all_ok"] = all(
        v is True
        for k, v in checks.items()
        if k
        not in (
            "prize_prefix16",
            "iso_rotations",
            "n_iso_rotations",
            "n_primitive9_words",
            "n_iso_windows",
        )
    )
    return checks


# ---------------------------------------------------------------------------
# Exhaustive finite radius-w rows
# ---------------------------------------------------------------------------


def eventual_iso(st: dict, w: int, tcap: int) -> bool:
    """True if the isolated-zero suffix looks like a post-transient regime."""
    suff = st["suffix_iso"]
    if suff < MIN_EVENTUAL_SUFFIX:
        return False
    last_break = tcap - suff
    transient = max(2 * w + 8, MIN_EVENTUAL_SUFFIX)
    return last_break <= transient


def cap_touch_iso(st: dict, tcap: int, Lrun: int) -> bool:
    return (
        st["end_iso"] == tcap
        and st["suffix_iso"] >= max(MIN_EVENTUAL_SUFFIX, Lrun)
        and st["L_iso"] >= MIN_EVENTUAL_SUFFIX
    )


def exhaustive_scan(w_max: int, log: list[str]) -> tuple[list[dict], list[dict]]:
    rows = []
    cap_survivors = []
    for w in range(0, w_max + 1):
        tcap = tcap_long(w)
        nstates = 1 << (2 * w + 1)
        t0 = time.perf_counter()
        Liso = 0
        Lany = 0
        Lpref_iso = 0
        Lpref_any = 0
        Lsuff_iso = 0
        Lsuff_any = 0
        best_iso = None
        best_any = None
        n_reach = 0
        n_gt_4w16 = 0
        max_end_iso = 0
        n_iso_ge9 = 0
        n_iso_ge18 = 0
        for mask in range(1, nstates):
            st = scan_mask(mask, w, tcap)
            if st["L_iso"] > Liso:
                Liso = st["L_iso"]
                best_iso = {
                    "mask": mask,
                    "row": row_bits(mask, w),
                    "L": st["L_iso"],
                    "start": st["start_iso"],
                    "end": st["end_iso"],
                    "prefix": st["prefix_iso"],
                    "suffix": st["suffix_iso"],
                    "block": st["block_iso"],
                }
            if st["L_any"] > Lany:
                Lany = st["L_any"]
                best_any = {
                    "mask": mask,
                    "row": row_bits(mask, w),
                    "L": st["L_any"],
                    "start": st["start_any"],
                    "end": st["end_any"],
                    "prefix": st["prefix_any"],
                    "suffix": st["suffix_any"],
                    "block": st["block_any"],
                }
            if st["prefix_iso"] > Lpref_iso:
                Lpref_iso = st["prefix_iso"]
            if st["prefix_any"] > Lpref_any:
                Lpref_any = st["prefix_any"]
            if st["suffix_iso"] > Lsuff_iso:
                Lsuff_iso = st["suffix_iso"]
            if st["suffix_any"] > Lsuff_any:
                Lsuff_any = st["suffix_any"]
            if st["end_iso"] > max_end_iso:
                max_end_iso = st["end_iso"]
            if st["L_iso"] >= PERIOD:
                n_iso_ge9 += 1
            if st["L_iso"] >= MIN_EVENTUAL_SUFFIX:
                n_iso_ge18 += 1
            if st["L_iso"] > 4 * w + 16:
                n_gt_4w16 += 1

            ev = eventual_iso(st, w, tcap)
            touch = cap_touch_iso(st, tcap, Liso)
            if ev or touch:
                if ev:
                    n_reach += 1
                ext = max(4 * tcap, 8 * w + 512)
                st2 = scan_mask(mask, w, ext)
                last_break = tcap - st["suffix_iso"]
                last2 = ext - st2["suffix_iso"]
                transient = max(2 * w + 8, MIN_EVENTUAL_SUFFIX)
                rec = {
                    "w": w,
                    "mask": mask,
                    "row": row_bits(mask, w),
                    "tcap": tcap,
                    "eventual_in_cap": ev,
                    "L_iso_at_tcap": st["L_iso"],
                    "suffix_iso": st["suffix_iso"],
                    "block_iso": st["block_iso"],
                    "last_break": last_break,
                    "ext": ext,
                    "L_iso_ext": st2["L_iso"],
                    "suffix_iso_ext": st2["suffix_iso"],
                    "last_break_ext": last2,
                    "reaches_ext": st2["suffix_iso"] >= ext - transient,
                }
                cap_survivors.append(rec)
                if st2["L_iso"] > Liso:
                    Liso = st2["L_iso"]
                    best_iso = {
                        "mask": mask,
                        "row": row_bits(mask, w),
                        "L": st2["L_iso"],
                        "start": st2["start_iso"],
                        "end": st2["end_iso"],
                        "prefix": st2["prefix_iso"],
                        "suffix": st2["suffix_iso"],
                        "block": st2["block_iso"],
                        "extended_tcap": ext,
                    }

        # Confirm the maximizer is not cap-limited: double its tcap.
        maximizer_ext = None
        if best_iso is not None:
            ext = max(2 * tcap, 8 * w + 256)
            st2 = scan_mask(best_iso["mask"], w, ext)
            maximizer_ext = {
                "ext": ext,
                "L_iso": st2["L_iso"],
                "start": st2["start_iso"],
                "end": st2["end_iso"],
                "suffix": st2["suffix_iso"],
                "grew": st2["L_iso"] > best_iso["L"],
            }
            if st2["L_iso"] > Liso:
                Liso = st2["L_iso"]
                best_iso = {
                    "mask": best_iso["mask"],
                    "row": best_iso["row"],
                    "L": st2["L_iso"],
                    "start": st2["start_iso"],
                    "end": st2["end_iso"],
                    "prefix": st2["prefix_iso"],
                    "suffix": st2["suffix_iso"],
                    "block": st2["block_iso"],
                    "extended_tcap": ext,
                }

        elapsed = time.perf_counter() - t0
        row = {
            "w": w,
            "n_nonzero": nstates - 1,
            "tcap": tcap,
            "L_iso": Liso,
            "L_any": Lany,
            "L_prefix_iso": Lpref_iso,
            "L_prefix_any": Lpref_any,
            "L_suffix_iso": Lsuff_iso,
            "L_suffix_any": Lsuff_any,
            "max_iso_end": max_end_iso,
            "n_cap_survivors": n_reach,
            "n_L_iso_gt_4w16": n_gt_4w16,
            "n_L_iso_ge9": n_iso_ge9,
            "n_L_iso_ge18": n_iso_ge18,
            "bound_4w16": 4 * w + 16,
            "best_iso": best_iso,
            "best_any": best_any,
            "maximizer_extended": maximizer_ext,
            "elapsed_sec": round(elapsed, 4),
        }
        rows.append(row)
        log.append(
            f"exhaustive w={w} n={nstates - 1} tcap={tcap} "
            f"L_iso={Liso} L_any={Lany} L_prefix_iso={Lpref_iso} "
            f"L_suffix_iso={Lsuff_iso} reach={n_reach} "
            f"L_iso>4w+16={n_gt_4w16} {elapsed:.3f}s"
        )
    return rows, cap_survivors


def plateau_terminal(values: list[int], min_len: int = 3) -> dict:
    """Longest terminal constant run of L(w)."""
    if not values:
        return {"plateau": False, "value": 0, "w_lo": None, "w_hi": None, "length": 0}
    last = values[-1]
    k = 1
    for v in reversed(values[:-1]):
        if v == last:
            k += 1
        else:
            break
    w_hi = len(values) - 1
    w_lo = w_hi - k + 1
    return {
        "plateau": k >= min_len,
        "value": last,
        "w_lo": w_lo,
        "w_hi": w_hi,
        "length": k,
    }


def growing(values: list[int]) -> bool:
    """Strict new maxima continue into the last few radii."""
    if len(values) < 2:
        return False
    last_new = 0
    m = values[0]
    for i, v in enumerate(values):
        if v > m:
            m = v
            last_new = i
    # A new record at w_max, or only a length-1 or length-2 terminal tie
    # after a record near the end, is "still growing".
    return last_new >= len(values) - 2


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def certify(w_max: int) -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    prize_bits = evolve_centers(1, 0, tcap_long(0))
    prize_st = analyze_centers(prize_bits)
    prize512 = evolve_centers(1, 0, 512)
    prize512_st = analyze_centers(prize512)
    log.append(
        f"prize w=0 tcap={tcap_long(0)} L_iso={prize_st['L_iso']} "
        f"L_any={prize_st['L_any']} block_iso={prize_st['block_iso']!r} "
        f"block_any={prize_st['block_any']!r} start_iso={prize_st['start_iso']}"
    )
    log.append(
        f"prize t=512 L_iso={prize512_st['L_iso']} "
        f"start_iso={prize512_st['start_iso']} "
        f"block_iso={prize512_st['block_iso']!r} "
        f"L_any={prize512_st['L_any']}"
    )

    exh, cap_surv = exhaustive_scan(w_max, log)

    xs = [r["w"] for r in exh]
    ys_iso = [r["L_iso"] for r in exh]
    ys_any = [r["L_any"] for r in exh]
    C_iso, Cp_iso = fit_linear(xs, ys_iso)
    C_any, Cp_any = fit_linear(xs, ys_any)
    res_iso = [y - (C_iso * x + Cp_iso) for x, y in zip(xs, ys_iso)]

    plat_iso = plateau_terminal(ys_iso)
    plat_any = plateau_terminal(ys_any)
    growing_iso = growing(ys_iso)
    growing_any = growing(ys_any)

    genuine = [
        s
        for s in cap_surv
        if s.get("eventual_in_cap") and s.get("reaches_ext")
    ]

    Lmax_iso = max(ys_iso) if ys_iso else 0
    tcap_max = tcap_long(w_max)
    small_vs_cap = Lmax_iso <= max(4 * PERIOD, tcap_max // 4)

    if genuine:
        verdict = "KILL"
        kill_reason = (
            "finite nonzero row whose centre stays on a rotation of "
            "011111111 through an extended cap (looks genuinely eventual)"
        )
    elif growing_iso and not plat_iso["plateau"]:
        verdict = "KILL"
        kill_reason = (
            "L_iso(w) still grows through the scanned radii with no "
            "terminal plateau; this kills the 'same as period 2' hope "
            "for q=8 (period 2 had L_run=24 on 6<=w<=10)"
        )
    elif plat_iso["plateau"] and small_vs_cap and not genuine:
        verdict = "FINITE_THEOREM"
        kill_reason = (
            "no genuine eventual isolated-zero witness; L_iso(w) plateaus "
            f"at {plat_iso['value']} on w={plat_iso['w_lo']}..{plat_iso['w_hi']} "
            f"inside tcap=8w+128; every radius-w<= {w_max} row breaks "
            "01^8 by time 8w+128, and no isolated-zero run exceeds "
            f"L_iso(w)<={Lmax_iso}"
        )
    else:
        verdict = "OPEN"
        kill_reason = (
            "no genuine eventual isolated-zero witness, but L_iso(w) is "
            f"{ys_iso} and is not a small terminal plateau of length>=3; "
            "the period-2 analog is not established at these radii"
        )

    wall = time.perf_counter() - t_all
    dump = {
        "attack": "period9_fiber",
        "ideas": "ideas9 item 4",
        "problem": (
            "no nonzero finite-support configuration has an eventually "
            "period-9 isolated-zero central trace (011111111 / q=8)"
        ),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": False,
        "kill_reason": kill_reason,
        "wall_time_sec": round(wall, 4),
        "tcap_long": "8w+128",
        "w_max": w_max,
        "period": PERIOD,
        "iso_word": ISO_WORD,
        "iso_rotations": list(ISO_ROTS),
        "min_eventual_suffix": MIN_EVENTUAL_SUFFIX,
        "checks": checks,
        "prize_seed": {
            "w": 0,
            "mask": 1,
            "tcap": tcap_long(0),
            "prefix16": checks["prize_prefix16"],
            "matches_experiment_center_bits": checks[
                "packed_matches_experiment_center_bits"
            ],
            "L_iso": prize_st["L_iso"],
            "L_any": prize_st["L_any"],
            "start_iso": prize_st["start_iso"],
            "end_iso": prize_st["end_iso"],
            "block_iso": prize_st["block_iso"],
            "start_any": prize_st["start_any"],
            "end_any": prize_st["end_any"],
            "block_any": prize_st["block_any"],
            "prefix_iso": prize_st["prefix_iso"],
            "suffix_iso": prize_st["suffix_iso"],
            "horizon_512": {
                "L_iso": prize512_st["L_iso"],
                "start_iso": prize512_st["start_iso"],
                "end_iso": prize512_st["end_iso"],
                "block_iso": prize512_st["block_iso"],
                "L_any": prize512_st["L_any"],
                "start_any": prize512_st["start_any"],
                "block_any": prize512_st["block_any"],
            },
        },
        "exhaustive": exh,
        "cap_survivors": [s for s in cap_surv if s.get("eventual_in_cap")]
        + [s for s in cap_surv if not s.get("eventual_in_cap")][:8],
        "genuine_eventual_witnesses": genuine,
        "fit_L_iso": {
            "C": C_iso,
            "Cprime": Cp_iso,
            "max_residual": max(res_iso) if res_iso else 0.0,
            "min_residual": min(res_iso) if res_iso else 0.0,
            "note": (
                "least-squares L_iso ~ C*w+C' is a summary only; the table "
                "and any plateau are the actual finite statement"
            ),
        },
        "fit_L_any": {"C": C_any, "Cprime": Cp_any},
        "plateau_iso": plat_iso,
        "plateau_any": plat_any,
        "growing_iso": growing_iso,
        "growing_any": growing_any,
        "exclusion_table": {
            "f_w": (
                "L_iso(w); an exact period-9 isolated-zero centre run of a "
                "radius-w row lasts at most L_iso(w) steps inside tcap=8w+128. "
                "L_any(w) is the same for any primitive 9-bit necklace."
            ),
            "L_iso": [{"w": r["w"], "L": r["L_iso"], "tcap": r["tcap"]} for r in exh],
            "L_any": [{"w": r["w"], "L": r["L_any"], "tcap": r["tcap"]} for r in exh],
            "L_prefix_iso": [
                {"w": r["w"], "L": r["L_prefix_iso"]} for r in exh
            ],
            "n_L_iso_gt_4w16": sum(r["n_L_iso_gt_4w16"] for r in exh),
            "n_eventual_in_cap": sum(r["n_cap_survivors"] for r in exh),
            "n_genuine_eventual": len(genuine),
        },
        "log": log,
    }
    OUT.write_text(json.dumps(dump, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"verdict={verdict} wall={wall:.3f}s")
    print(f"reason: {kill_reason}")
    print(f"L_iso by w: {[(r['w'], r['L_iso'], r['tcap']) for r in exh]}")
    print(f"L_any by w: {[(r['w'], r['L_any'], r['tcap']) for r in exh]}")
    print(f"fit L_iso ~ {C_iso:.3f}*w + {Cp_iso:.3f}")
    print(
        f"n_cap_survivors={sum(r['n_cap_survivors'] for r in exh)} "
        f"genuine={len(genuine)}"
    )
    print(
        f"prize L_iso={prize_st['L_iso']} L_any={prize_st['L_any']} "
        f"block_any={prize_st['block_any']!r}"
    )
    return dump


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--w-max", type=int, default=W_MAX_DEFAULT)
    args = p.parse_args()
    certify(args.w_max)


if __name__ == "__main__":
    main()
