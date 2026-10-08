#!/usr/bin/env python3
"""Cycle I / ideas11 item 3: Condrey-style finite-row scan for periods 6 and 7.

Same packed engine as research/period45_fiber.py (step copied, that file is
not modified). The centre factor is exact period 6 or exact period 7.
Primitive necklaces only; all rotations (global phases) are scored.

Period 6: nine primitive necklaces (54 phases). The five non-primitive
    length-6 necklaces are 000000, 111111 (period 1), 010101 (period 2),
    001001 and 011011 (period 3).
Period 7: eighteen primitive necklaces (126 phases). Length 7 is prime, so
    the only excluded necklaces are the constants 0000000 and 1111111
    (20 binary necklaces minus those two).

    L6(w) = longest run of any of the 54 infinite period-6 words
    L7(w) = longest run of any of the 126 infinite period-7 words

in the centre of a radius-w finite row, evolved in a quiescent background.
L_prefix(w) is the same quantity restricted to a run that starts at t=0.

Exhaustive w=0..6 (2^{13}-1 nonzero masks at w=6). If w=6 is slow, finish
w<=5 fully and sample w=6. tcap=8w+128.
Packed Rule 30: new=(row<<2)^((row<<1)|row), centre (row>>(w+t))&1.

Kill: L_p(w) is still strictly larger at the max scanned w than at every
smaller scanned radius (growing, no plateau), or a witness that remains
period-p through the whole cap (looks eventual). Finite theorem if L_p
plateaus at a constant on the scanned radii for at least three radii, not
merely the last two (period 3 looked the same at w=6..7 before L3(8)=22).

This is not the strip-graph residual-SCC test, not onset SAT, not an
F_T ideal certificate, and not the period-2 fiber reconstruction.
Stdlib only. Not a prize claim.

Run: python3 research/period67_fiber.py --certify
Dump: research/period67_fiber.json, research/period67_fiber.md
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits

OUT_JSON = Path(__file__).resolve().with_suffix(".json")
OUT_MD = Path(__file__).resolve().with_suffix(".md")

PRIZE_PREFIX16 = "1101110011000101"

# Explicit primitive necklaces. Period 6 has nine, not fourteen: the other
# five length-6 necklaces are the constants, 010101, 001001, and 011011.
# Period 7 has eighteen, not twenty: the other two are the constants.
P6_NECK = (
    "000001",
    "000011",
    "000101",
    "000111",
    "001011",
    "001101",
    "001111",
    "010111",
    "011111",
)
P7_NECK = (
    "0000001",
    "0000011",
    "0000101",
    "0000111",
    "0001001",
    "0001011",
    "0001101",
    "0001111",
    "0010011",
    "0010101",
    "0010111",
    "0011011",
    "0011101",
    "0011111",
    "0101011",
    "0101111",
    "0110111",
    "0111111",
)

NPROC_CAP = 4
SAMPLE_SEED = 20260911


# ---------------------------------------------------------------------------
# Rule 30, packed. Copied from research/period45_fiber.py; that file is not
# modified. Bit 0 is the leftmost cell of the current support.
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


def primitive_necklaces(n: int) -> list[str]:
    out = []
    for x in range(1 << n):
        w = "".join(str((x >> (n - 1 - i)) & 1) for i in range(n))
        if any(n % d == 0 and w == w[:d] * (n // d) for d in range(1, n)):
            continue
        if w != min(w[i:] + w[:i] for i in range(n)):
            continue
        out.append(w)
    return out


def all_necklaces(n: int) -> list[str]:
    out = []
    for x in range(1 << n):
        w = "".join(str((x >> (n - 1 - i)) & 1) for i in range(n))
        if w != min(w[i:] + w[:i] for i in range(n)):
            continue
        out.append(w)
    return out


def min_period(block: str) -> int:
    n = len(block)
    for p in range(1, n + 1):
        if n % p == 0 and block == block[:p] * (n // p):
            return p
    return n


def make_catalog(necklaces: tuple[str, ...]) -> dict:
    period = len(necklaces[0])
    pats: list[tuple[int, ...]] = []
    names: list[str] = []
    necks: list[str] = []
    for neck in necklaces:
        if len(neck) != period:
            raise ValueError(f"necklace length {len(neck)} != {period}")
        if min_period(neck) != period:
            raise ValueError(f"non-primitive necklace {neck}")
        for i in range(period):
            rot = neck[i:] + neck[:i]
            pats.append(tuple(int(ch) for ch in rot))
            names.append(rot)
            necks.append(neck)
    return {
        "period": period,
        "necklaces": necklaces,
        "pats": tuple(pats),
        "names": tuple(names),
        "necks": tuple(necks),
        "n": len(pats),
    }


CAT6 = make_catalog(P6_NECK)
CAT7 = make_catalog(P7_NECK)
P6_PATS = CAT6["pats"]
P7_PATS = CAT7["pats"]
N6 = CAT6["n"]
N7 = CAT7["n"]


# ---------------------------------------------------------------------------
# Exact period-p runs. A factor is exact period p iff it matches one of the
# infinite words along global time (rotations already encode the phase).
# Constants and proper-divisor periods are excluded because they are not in
# the catalog (except that a length-7 window of (01)^∞ is primitive, and
# then breaks at lag 7 because 7 is odd).
# ---------------------------------------------------------------------------

def stats_from_bits(bits: list[int], cat: dict) -> dict:
    n = len(bits)
    period = cat["period"]
    names = cat["names"]
    necks = cat["necks"]
    pats = cat["pats"]
    empty_pat = {"L": 0, "start": 0, "prefix": 0, "suffix": 0}
    empty = {
        "L": 0,
        "start": 0,
        "end": 0,
        "prefix": 0,
        "suffix": 0,
        "pattern": None,
        "necklace": None,
        "L_neck": {name: 0 for name in cat["necklaces"]},
        "reaches_cap": False,
        "by_pattern": {name: dict(empty_pat) for name in names},
    }
    if n == 0:
        return empty

    best = 0
    best_start = 0
    best_i = 0
    prefix = 0
    suffix = 0
    L_neck = {name: 0 for name in cat["necklaces"]}
    by_pattern = {}

    for i, P in enumerate(pats):
        run = 0
        run_start = 0
        loc_best = 0
        loc_start = 0
        pref = 0
        pref_alive = True
        for t, bit in enumerate(bits):
            if bit == P[t % period]:
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
        name = names[i]
        by_pattern[name] = {
            "L": loc_best,
            "start": loc_start,
            "prefix": pref,
            "suffix": run,
        }
        neck = necks[i]
        if loc_best > L_neck[neck]:
            L_neck[neck] = loc_best
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
        "pattern": names[best_i] if best else None,
        "necklace": necks[best_i] if best else None,
        "L_neck": L_neck,
        "reaches_cap": best_start + best == n and best >= period,
        "by_pattern": by_pattern,
    }


def _assemble(cat: dict, b: list[int], bs: list[int], pfx: list[int], sfx: list[int], tcap: int) -> dict:
    n = cat["n"]
    names = cat["names"]
    necks = cat["necks"]
    period = cat["period"]
    best = b[0]
    best_i = 0
    best_start = bs[0]
    for i in range(1, n):
        if b[i] > best:
            best = b[i]
            best_i = i
            best_start = bs[i]
    prefix = pfx[0]
    suffix = sfx[0]
    for i in range(1, n):
        if pfx[i] > prefix:
            prefix = pfx[i]
        if sfx[i] > suffix:
            suffix = sfx[i]
    L_neck = {name: 0 for name in cat["necklaces"]}
    for i in range(n):
        neck = necks[i]
        if b[i] > L_neck[neck]:
            L_neck[neck] = b[i]
    return {
        "L": best,
        "start": best_start,
        "end": best_start + best,
        "prefix": prefix,
        "suffix": suffix,
        "pattern": names[best_i] if best else None,
        "necklace": necks[best_i] if best else None,
        "L_neck": L_neck,
        "reaches_cap": best_start + best == tcap and best >= period,
    }


def scan_mask(mask: int, w: int, tcap: int, cat: dict) -> dict:
    """Evolve one packed row, tracking every phase of one period catalog."""
    pats = cat["pats"]
    n = cat["n"]
    period = cat["period"]
    cur = [0] * n
    st = [0] * n
    b = [0] * n
    bs = [0] * n
    pfx = [0] * n
    alive = [1] * n
    row = mask
    for t in range(tcap):
        bit = (row >> (w + t)) & 1
        r = t % period
        for i in range(n):
            if bit == pats[i][r]:
                if cur[i] == 0:
                    st[i] = t
                cur[i] += 1
                if alive[i]:
                    pfx[i] += 1
                if cur[i] > b[i]:
                    b[i] = cur[i]
                    bs[i] = st[i]
            else:
                cur[i] = 0
                alive[i] = 0
        row = (row << 2) ^ ((row << 1) | row)
    return _assemble(cat, b, bs, pfx, cur, tcap)


def scan_mask_p67(mask: int, w: int, tcap: int) -> tuple[dict, dict]:
    """One packed evolution, both catalogs. Inner update is integer compares."""
    p6 = P6_PATS
    p7 = P7_PATS
    n6 = N6
    n7 = N7
    c6 = [0] * n6
    s6 = [0] * n6
    b6 = [0] * n6
    bs6 = [0] * n6
    pfx6 = [0] * n6
    a6 = [1] * n6
    c7 = [0] * n7
    s7 = [0] * n7
    b7 = [0] * n7
    bs7 = [0] * n7
    pfx7 = [0] * n7
    a7 = [1] * n7
    row = mask
    r6 = 0
    r7 = 0
    for t in range(tcap):
        bit = (row >> (w + t)) & 1
        for i in range(n6):
            if bit == p6[i][r6]:
                if c6[i] == 0:
                    s6[i] = t
                c6[i] += 1
                if a6[i]:
                    pfx6[i] += 1
                if c6[i] > b6[i]:
                    b6[i] = c6[i]
                    bs6[i] = s6[i]
            else:
                c6[i] = 0
                a6[i] = 0
        for i in range(n7):
            if bit == p7[i][r7]:
                if c7[i] == 0:
                    s7[i] = t
                c7[i] += 1
                if a7[i]:
                    pfx7[i] += 1
                if c7[i] > b7[i]:
                    b7[i] = c7[i]
                    bs7[i] = s7[i]
            else:
                c7[i] = 0
                a7[i] = 0
        r6 += 1
        if r6 == 6:
            r6 = 0
        r7 += 1
        if r7 == 7:
            r7 = 0
        row = (row << 2) ^ ((row << 1) | row)
    return (
        _assemble(CAT6, b6, bs6, pfx6, c6, tcap),
        _assemble(CAT7, b7, bs7, pfx7, c7, tcap),
    )


def _best_record(mask: int, w: int, st: dict) -> dict:
    rec = {
        "mask": mask,
        "row": row_bits(mask, w),
        "L": st["L"],
        "start": st["start"],
        "end": st["end"],
        "prefix": st["prefix"],
        "suffix": st["suffix"],
        "pattern": st["pattern"],
        "necklace": st["necklace"],
        "L_neck": dict(st["L_neck"]),
    }
    if "extended_tcap" in st:
        rec["extended_tcap"] = st["extended_tcap"]
    return rec


def _prefix_record(mask: int, w: int, st: dict) -> dict:
    return {
        "mask": mask,
        "row": row_bits(mask, w),
        "L_prefix": st["prefix"],
        "pattern": st["pattern"] if st["start"] == 0 else None,
        "L_run": st["L"],
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

    checks["p6_necklaces"] = list(P6_NECK)
    checks["p7_necklaces"] = list(P7_NECK)
    checks["p6_necklaces_match_generator"] = list(P6_NECK) == primitive_necklaces(6)
    checks["p7_necklaces_match_generator"] = list(P7_NECK) == primitive_necklaces(7)
    checks["n_p6_necklaces"] = len(P6_NECK)
    checks["n_p6_necklaces_is_9"] = len(P6_NECK) == 9
    checks["n_p7_primitive_necklaces"] = len(P7_NECK)
    checks["n_p7_primitive_necklaces_is_18"] = len(P7_NECK) == 18
    checks["n_p6_all_length6_necklaces_is_14"] = len(all_necklaces(6)) == 14
    checks["n_p7_all_length7_necklaces_is_20"] = len(all_necklaces(7)) == 20
    checks["n_p6_phases"] = CAT6["n"]
    checks["n_p6_phases_is_54"] = CAT6["n"] == 54
    checks["n_p7_phases"] = CAT7["n"]
    checks["n_p7_phases_is_126"] = CAT7["n"] == 126
    checks["p6_excludes_000000"] = "000000" not in CAT6["names"]
    checks["p6_excludes_111111"] = "111111" not in CAT6["names"]
    checks["p6_excludes_010101"] = "010101" not in CAT6["names"]
    checks["p6_excludes_101010"] = "101010" not in CAT6["names"]
    checks["p6_excludes_001001"] = "001001" not in CAT6["names"]
    checks["p6_excludes_011011"] = "011011" not in CAT6["names"]
    checks["p7_excludes_0000000"] = "0000000" not in CAT7["names"]
    checks["p7_excludes_1111111"] = "1111111" not in CAT7["names"]
    checks["each_p6_necklace_primitive"] = all(min_period(n) == 6 for n in P6_NECK)
    checks["each_p7_necklace_primitive"] = all(min_period(n) == 7 for n in P7_NECK)

    syn_000001 = [0, 0, 0, 0, 0, 1] * 16
    st = stats_from_bits(syn_000001, CAT6)
    checks["synthetic_000001_L"] = st["L"] == 96
    checks["synthetic_000001_prefix"] = st["prefix"] == 96
    checks["synthetic_000001_pattern"] = st["pattern"] == "000001"
    checks["synthetic_000001_necklace"] = st["necklace"] == "000001"

    syn_100000 = [1, 0, 0, 0, 0, 0] * 10
    st = stats_from_bits(syn_100000, CAT6)
    checks["synthetic_100000_pattern"] = st["pattern"] == "100000"
    checks["synthetic_100000_necklace"] = st["necklace"] == "000001"
    checks["synthetic_100000_L"] = st["L"] == 60

    syn_000011 = [0, 0, 0, 0, 1, 1] * 12
    st = stats_from_bits(syn_000011, CAT6)
    checks["synthetic_000011_L"] = st["L"] == 72
    checks["synthetic_000011_necklace"] = st["necklace"] == "000011"

    syn_011111 = [0, 1, 1, 1, 1, 1] * 10
    st = stats_from_bits(syn_011111, CAT6)
    checks["synthetic_011111_L"] = st["L"] == 60
    checks["synthetic_011111_necklace"] = st["necklace"] == "011111"

    syn_p2 = [t & 1 for t in range(64)]
    st = stats_from_bits(syn_p2, CAT6)
    checks["period2_is_not_long_p6"] = st["L"] == 5

    st = stats_from_bits([0] * 40, CAT6)
    checks["constant0_p6_L_lt_6"] = st["L"] < 6
    st = stats_from_bits([1] * 40, CAT6)
    checks["constant1_p6_L_lt_6"] = st["L"] < 6

    syn_0000001 = [0, 0, 0, 0, 0, 0, 1] * 12
    st = stats_from_bits(syn_0000001, CAT7)
    checks["synthetic_0000001_L"] = st["L"] == 84
    checks["synthetic_0000001_pattern"] = st["pattern"] == "0000001"
    checks["synthetic_0000001_necklace"] = st["necklace"] == "0000001"

    syn_0010101 = [0, 0, 1, 0, 1, 0, 1] * 8
    st = stats_from_bits(syn_0010101, CAT7)
    checks["synthetic_0010101_pattern"] = st["pattern"] == "0010101"
    checks["synthetic_0010101_necklace"] = st["necklace"] == "0010101"
    checks["synthetic_0010101_L"] = st["L"] == 56

    syn_0111111 = [0, 1, 1, 1, 1, 1, 1] * 8
    st = stats_from_bits(syn_0111111, CAT7)
    checks["synthetic_0111111_L"] = st["L"] == 56
    checks["synthetic_0111111_necklace"] = st["necklace"] == "0111111"

    # (01)^∞ matches a 7-window of a primitive length-7 necklace (7 is odd)
    # and then breaks, so it does not inflate L7.
    st = stats_from_bits(syn_p2, CAT7)
    checks["period2_is_not_long_p7"] = st["L"] == 7

    syn_p3 = [0, 0, 1] * 20
    st = stats_from_bits(syn_p3, CAT6)
    checks["period3_is_not_long_p6"] = st["L"] == 5
    st = stats_from_bits(syn_p3, CAT7)
    checks["period3_is_not_long_p7"] = st["L"] == 8

    syn_p4 = [0, 0, 0, 1] * 16
    st = stats_from_bits(syn_p4, CAT6)
    checks["period4_is_not_long_p6"] = st["L"] == 7
    syn_p5 = [0, 0, 0, 0, 1] * 13
    st = stats_from_bits(syn_p5, CAT6)
    checks["period5_is_not_long_p6"] = st["L"] == 9
    st = stats_from_bits(syn_p5, CAT7)
    checks["period5_is_not_long_p7"] = st["L"] == 9

    st = stats_from_bits([0] * 40, CAT7)
    checks["constant0_p7_L_lt_7"] = st["L"] < 7
    st = stats_from_bits([1] * 40, CAT7)
    checks["constant1_p7_L_lt_7"] = st["L"] < 7

    stream_ok = True
    stream_fail = None
    keys = ("L", "start", "end", "prefix", "suffix", "pattern", "necklace")
    for w, mask, tcap in [(0, 1, 64), (1, 5, 40), (2, 19, 48), (3, 73, 56), (4, 300, 40)]:
        a6, a7 = scan_mask_p67(mask, w, tcap)
        bits = evolve_centers(mask, w, tcap)
        b6 = stats_from_bits(bits, CAT6)
        b7 = stats_from_bits(bits, CAT7)
        s6 = scan_mask(mask, w, tcap, CAT6)
        s7 = scan_mask(mask, w, tcap, CAT7)
        if any(a6[k] != b6[k] for k in keys) or a6["L_neck"] != b6["L_neck"]:
            stream_ok = False
            stream_fail = {"which": "p6-combined", "w": w, "mask": mask}
            break
        if any(a7[k] != b7[k] for k in keys) or a7["L_neck"] != b7["L_neck"]:
            stream_ok = False
            stream_fail = {"which": "p7-combined", "w": w, "mask": mask}
            break
        if any(s6[k] != b6[k] for k in keys) or any(s7[k] != b7[k] for k in keys):
            stream_ok = False
            stream_fail = {"which": "single-catalog", "w": w, "mask": mask}
            break
    checks["scan_matches_stored_trace"] = stream_ok
    if stream_fail is not None:
        checks["scan_fail"] = stream_fail

    prize16 = [int(ch) for ch in PRIZE_PREFIX16]
    st6 = stats_from_bits(prize16, CAT6)
    st7 = stats_from_bits(prize16, CAT7)
    checks["prize_p6_prefix16"] = st6["prefix"]
    checks["prize_p7_prefix16"] = st7["prefix"]
    checks["prize_p6_L16"] = st6["L"]
    checks["prize_p7_L16"] = st7["L"]

    checks["all_ok"] = all(
        v is True
        for k, v in checks.items()
        if k
        not in (
            "prize_prefix16",
            "prize_p6_prefix16",
            "prize_p7_prefix16",
            "prize_p6_L16",
            "prize_p7_L16",
            "p6_necklaces",
            "p7_necklaces",
            "n_p6_necklaces",
            "n_p7_primitive_necklaces",
            "n_p6_phases",
            "n_p7_phases",
            "naive_fail",
            "scan_fail",
        )
    )
    return checks


# ---------------------------------------------------------------------------
# Exhaustive finite radius-w rows
# ---------------------------------------------------------------------------

def _confirm_best(best: dict, w: int, tcap: int, cat: dict) -> None:
    bits = evolve_centers(best["mask"], w, tcap)
    chk = stats_from_bits(bits, cat)
    best["stored_L"] = chk["L"]
    best["stored_pattern"] = chk["pattern"]
    factor = bits[best["start"] : best["end"]]
    best["factor"] = "".join(map(str, factor[:60]))
    best["factor_len"] = len(factor)
    ext = max(4 * tcap, 8 * w + 512)
    st_ext = scan_mask(best["mask"], w, ext, cat)
    best["ext_tcap"] = ext
    best["ext_L"] = st_ext["L"]
    best["ext_start"] = st_ext["start"]
    best["ext_end"] = st_ext["end"]
    best["ext_pattern"] = st_ext["pattern"]
    best["ext_grew"] = st_ext["L"] > best["L"]
    best["ext_same_run"] = st_ext["start"] == best["start"] and st_ext["L"] >= best["L"]
    best["ext_same_run_grew"] = bool(best["ext_same_run"] and st_ext["L"] > best["L"])
    best["ext_new_burst"] = bool(st_ext["L"] > best["L"] and st_ext["start"] != best["start"])
    transient = max(2 * w + 8, 16)
    best["ext_eventual"] = (
        st_ext["suffix"] >= 16 and (ext - st_ext["suffix"]) <= transient
    )


def _confirm_prefix(best_prefix: dict, w: int, tcap: int, cat: dict) -> None:
    pbits = evolve_centers(best_prefix["mask"], w, tcap)
    pst = stats_from_bits(pbits, cat)
    best_prefix["pattern"] = None
    for name, rec in pst["by_pattern"].items():
        if rec["prefix"] == pst["prefix"] and rec["prefix"] > 0:
            best_prefix["pattern"] = name
            break
    best_prefix["factor"] = "".join(map(str, pbits[: pst["prefix"]][:60]))


class _Acc:
    def __init__(self, cat: dict, w: int, tcap: int):
        self.cat = cat
        self.period = cat["period"]
        self.tag = f"L{self.period}"
        self.w = w
        self.tcap = tcap
        self.Lrun = 0
        self.Lpref = 0
        self.Lsuff = 0
        self.L_neck = {name: 0 for name in cat["necklaces"]}
        self.best: dict | None = None
        self.best_prefix: dict | None = None
        self.n_at_max = 0
        self.n_reach = 0
        self.n_gt_4w16 = 0
        self.max_end = 0
        self.bound = 4 * w + 16
        self.cap_survivors: list[dict] = []
        self.n_scanned = 0

    def update(self, mask: int, st: dict) -> None:
        self.n_scanned += 1
        L = st["L"]
        if L > self.Lrun:
            self.Lrun = L
            self.n_at_max = 1
            self.best = _best_record(mask, self.w, st)
        elif L == self.Lrun:
            self.n_at_max += 1
            if self.best is None or mask < self.best["mask"]:
                self.best = _best_record(mask, self.w, st)
        if st["prefix"] > self.Lpref:
            self.Lpref = st["prefix"]
            self.best_prefix = _prefix_record(mask, self.w, st)
        elif st["prefix"] == self.Lpref and st["prefix"] > 0:
            if self.best_prefix is None or mask < self.best_prefix["mask"]:
                self.best_prefix = _prefix_record(mask, self.w, st)
        if st["suffix"] > self.Lsuff:
            self.Lsuff = st["suffix"]
        for name, val in st["L_neck"].items():
            if val > self.L_neck[name]:
                self.L_neck[name] = val
        if st["end"] > self.max_end:
            self.max_end = st["end"]
        if L > self.bound:
            self.n_gt_4w16 += 1

        last_break = self.tcap - st["suffix"]
        transient = max(2 * self.w + 8, 16)
        eventual_in_cap = st["suffix"] >= 16 and last_break <= transient
        cap_touch = st["end"] == self.tcap and st["suffix"] >= max(16, self.Lrun)
        if eventual_in_cap or cap_touch:
            if eventual_in_cap:
                self.n_reach += 1
            ext = max(4 * self.tcap, 8 * self.w + 512)
            st2 = scan_mask(mask, self.w, ext, self.cat)
            last2 = ext - st2["suffix"]
            rec = {
                "period": self.period,
                "w": self.w,
                "mask": mask,
                "tcap": self.tcap,
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
            self.cap_survivors.append(rec)
            if st2["L"] > self.Lrun:
                self.Lrun = st2["L"]
                self.n_at_max = 1
                rec_best = _best_record(mask, self.w, st2)
                rec_best["extended_tcap"] = ext
                self.best = rec_best

    def snapshot(self) -> dict:
        return {
            "Lrun": self.Lrun,
            "Lpref": self.Lpref,
            "Lsuff": self.Lsuff,
            "L_neck": dict(self.L_neck),
            "best": self.best,
            "best_prefix": self.best_prefix,
            "n_at_max": self.n_at_max,
            "n_reach": self.n_reach,
            "n_gt_4w16": self.n_gt_4w16,
            "max_end": self.max_end,
            "cap_survivors": list(self.cap_survivors),
            "n_scanned": self.n_scanned,
        }

    def merge_snapshot(self, snap: dict) -> None:
        if snap["Lrun"] > self.Lrun:
            self.Lrun = snap["Lrun"]
            self.n_at_max = snap["n_at_max"]
            self.best = snap["best"]
        elif snap["Lrun"] == self.Lrun and snap["Lrun"] > 0:
            self.n_at_max += snap["n_at_max"]
            if self.best is None:
                self.best = snap["best"]
            elif snap["best"] is not None and snap["best"]["mask"] < self.best["mask"]:
                self.best = snap["best"]
        if snap["Lpref"] > self.Lpref:
            self.Lpref = snap["Lpref"]
            self.best_prefix = snap["best_prefix"]
        elif snap["Lpref"] == self.Lpref and snap["Lpref"] > 0:
            if self.best_prefix is None:
                self.best_prefix = snap["best_prefix"]
            elif (
                snap["best_prefix"] is not None
                and snap["best_prefix"]["mask"] < self.best_prefix["mask"]
            ):
                self.best_prefix = snap["best_prefix"]
        if snap["Lsuff"] > self.Lsuff:
            self.Lsuff = snap["Lsuff"]
        for name, val in snap["L_neck"].items():
            if val > self.L_neck[name]:
                self.L_neck[name] = val
        if snap["max_end"] > self.max_end:
            self.max_end = snap["max_end"]
        self.n_gt_4w16 += snap["n_gt_4w16"]
        self.n_reach += snap["n_reach"]
        self.n_scanned += snap["n_scanned"]
        self.cap_survivors.extend(snap["cap_survivors"])

    def finish(self, elapsed: float, mode: str = "exhaustive") -> dict:
        if self.best is not None:
            _confirm_best(self.best, self.w, self.tcap, self.cat)
        if self.best_prefix is not None:
            _confirm_prefix(self.best_prefix, self.w, self.tcap, self.cat)
        n_nonzero = (1 << (2 * self.w + 1)) - 1
        row = {
            "w": self.w,
            "n_nonzero": n_nonzero,
            "n_scanned": self.n_scanned,
            "mode": mode,
            "tcap": self.tcap,
            "L_run": self.Lrun,
            self.tag: self.Lrun,
            "L_prefix": self.Lpref,
            "L_suffix": self.Lsuff,
            "L_neck": dict(self.L_neck),
            "max_run_end": self.max_end,
            "n_at_Lrun": self.n_at_max,
            "best_prefix": self.best_prefix,
            "n_cap_survivors": self.n_reach,
            "n_L_gt_4w16": self.n_gt_4w16,
            "bound_4w16": self.bound,
            "best": self.best,
            "elapsed_sec": round(elapsed, 4),
        }
        for name, val in self.L_neck.items():
            row[f"L_{name}"] = val
        return row


def nproc() -> int:
    try:
        return max(1, min(NPROC_CAP, os.cpu_count() or 1))
    except Exception:
        return 1


def _scan_chunk(args: tuple[int, int, int, int]) -> tuple[dict, dict]:
    w, tcap, lo, hi = args
    acc6 = _Acc(CAT6, w, tcap)
    acc7 = _Acc(CAT7, w, tcap)
    for mask in range(lo, hi):
        st6, st7 = scan_mask_p67(mask, w, tcap)
        acc6.update(mask, st6)
        acc7.update(mask, st7)
    return acc6.snapshot(), acc7.snapshot()


def _scan_mask_list(args: tuple[int, int, list[int]]) -> tuple[dict, dict]:
    w, tcap, masks = args
    acc6 = _Acc(CAT6, w, tcap)
    acc7 = _Acc(CAT7, w, tcap)
    for mask in masks:
        st6, st7 = scan_mask_p67(mask, w, tcap)
        acc6.update(mask, st6)
        acc7.update(mask, st7)
    return acc6.snapshot(), acc7.snapshot()


def _run_chunks(w: int, tcap: int, chunks: list, workers: int, listed: bool) -> tuple[_Acc, _Acc]:
    acc6 = _Acc(CAT6, w, tcap)
    acc7 = _Acc(CAT7, w, tcap)
    fn = _scan_mask_list if listed else _scan_chunk
    if workers <= 1 or len(chunks) == 1:
        for ch in chunks:
            s6, s7 = fn(ch)
            acc6.merge_snapshot(s6)
            acc7.merge_snapshot(s7)
        return acc6, acc7
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for s6, s7 in ex.map(fn, chunks):
            acc6.merge_snapshot(s6)
            acc7.merge_snapshot(s7)
    return acc6, acc7


def _hw_masks(width: int, max_hw: int) -> list[int]:
    """All nonzero masks of Hamming weight <= max_hw on `width` bits."""
    out: list[int] = []

    def rec(start: int, left: int, acc: int) -> None:
        if left == 0:
            if acc:
                out.append(acc)
            return
        last = width - left
        for i in range(start, last + 1):
            rec(i + 1, left - 1, acc | (1 << i))

    for hw in range(1, max_hw + 1):
        rec(0, hw, 0)
    return out


def sample_masks(w: int, n_sample: int, extra: list[int]) -> list[int]:
    """Deterministic sample: low Hamming weight, extras, then random fill."""
    width = 2 * w + 1
    nstates = 1 << width
    chosen: set[int] = set()
    for m in extra:
        if 1 <= m < nstates:
            chosen.add(m)
    for m in _hw_masks(width, 4):
        chosen.add(m)
    rng = random.Random(SAMPLE_SEED + 1009 * w)
    target = min(nstates - 1, max(n_sample, len(chosen)))
    while len(chosen) < target:
        chosen.add(rng.randrange(1, nstates))
    return sorted(chosen)


def scan_radius(
    w: int,
    mode: str,
    n_sample: int,
    extra_masks: list[int],
    log: list[str],
) -> tuple[dict, dict, list[dict], list[dict]]:
    tcap = tcap_long(w)
    nstates = 1 << (2 * w + 1)
    workers = nproc() if w >= 5 else 1
    t0 = time.perf_counter()
    if mode == "sampled":
        masks = sample_masks(w, n_sample, extra_masks)
        if workers <= 1 or len(masks) < 256:
            chunks = [(w, tcap, masks)]
            workers = 1
        else:
            size = (len(masks) + workers - 1) // workers
            chunks = [
                (w, tcap, masks[i : i + size])
                for i in range(0, len(masks), size)
            ]
        acc6, acc7 = _run_chunks(w, tcap, chunks, workers, listed=True)
    else:
        total = nstates - 1
        if workers <= 1 or total < 256:
            chunks = [(w, tcap, 1, nstates)]
            workers = 1
        else:
            size = (total + workers - 1) // workers
            chunks = []
            lo = 1
            while lo < nstates:
                hi = min(nstates, lo + size)
                chunks.append((w, tcap, lo, hi))
                lo = hi
        acc6, acc7 = _run_chunks(w, tcap, chunks, workers, listed=False)
    elapsed = time.perf_counter() - t0
    row6 = acc6.finish(elapsed, mode)
    row7 = acc7.finish(elapsed, mode)
    log.append(
        f"{mode} w={w} n_scanned={acc6.n_scanned}/{nstates - 1} tcap={tcap} "
        f"L6={acc6.Lrun} L7={acc7.Lrun} "
        f"L6_prefix={acc6.Lpref} L7_prefix={acc7.Lpref} "
        f"n6_at_max={acc6.n_at_max} n7_at_max={acc7.n_at_max} "
        f"reach6={acc6.n_reach} reach7={acc7.n_reach} "
        f"nproc={workers} {elapsed:.3f}s"
    )
    print(log[-1], flush=True)
    return row6, row7, acc6.cap_survivors, acc7.cap_survivors


def exhaustive_scan(
    w_max: int,
    sample_w6: int,
    log: list[str],
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    rows6: list[dict] = []
    rows7: list[dict] = []
    cap6: list[dict] = []
    cap7: list[dict] = []
    for w in range(0, w_max + 1):
        sample_this = bool(sample_w6 and w == 6)
        mode = "sampled" if sample_this else "exhaustive"
        n_sample = sample_w6 if sample_this else 0
        # Zero-pad smaller-radius maximizers into radius w (sample seed).
        padded_masks = []
        for src in rows6 + rows7:
            b = src.get("best") or {}
            src_w = src["w"]
            if b.get("mask") is None or src_w >= w:
                continue
            padded_masks.append(b["mask"] << (w - src_w))
        row6, row7, c6, c7 = scan_radius(
            w, mode, n_sample, padded_masks, log
        )
        rows6.append(row6)
        rows7.append(row7)
        cap6.extend(c6)
        cap7.extend(c7)
    return rows6, rows7, cap6, cap7


def plateau_info(exh: list[dict], tag: str) -> dict:
    ys = [r["L_run"] for r in exh]
    if not ys:
        return {
            f"max_{tag}": 0,
            "plateau": False,
            "real_plateau": False,
            "still_growing_at_wmax": False,
            "strictly_larger_at_wmax": False,
            "w_at_max": [],
            "plateau_lo": None,
            "plateau_hi": None,
        }
    max_L = max(ys)
    w_at_max = [r["w"] for r in exh if r["L_run"] == max_L]
    still_growing = len(ys) >= 2 and ys[-1] > ys[-2]
    strictly_larger = len(ys) >= 2 and all(ys[-1] > y for y in ys[:-1])
    hi = exh[-1]["w"]
    lo = hi
    last = ys[-1]
    for r in reversed(exh):
        if r["L_run"] == last:
            lo = r["w"]
        else:
            break
    plateau = (not still_growing) and (hi - lo >= 1 or (last == max_L and len(w_at_max) >= 2))
    consec = True
    if w_at_max:
        consec = w_at_max[-1] - w_at_max[0] + 1 == len(w_at_max)
    plateau_at_max = consec and len(w_at_max) >= 2
    # Real plateau: global max on at least three consecutive scanned radii,
    # not merely the last two at the scan edge.
    real_plateau = bool(
        plateau_at_max and w_at_max and (w_at_max[-1] - w_at_max[0] >= 2)
    )
    two_radius_edge = bool(
        plateau_at_max
        and w_at_max
        and w_at_max[-1] == hi
        and w_at_max[-1] - w_at_max[0] <= 1
    )
    return {
        f"max_{tag}": max_L,
        "max_L": max_L,
        "plateau": bool(plateau_at_max or (plateau and last == max_L and hi - lo >= 1)),
        "plateau_at_global_max": plateau_at_max,
        "real_plateau": real_plateau,
        "two_radius_edge": two_radius_edge,
        "still_growing_at_wmax": still_growing and ys[-1] == max_L,
        "strictly_larger_at_wmax": strictly_larger and ys[-1] == max_L,
        "w_at_max": w_at_max,
        "plateau_lo": min(w_at_max) if w_at_max else None,
        "plateau_hi": max(w_at_max) if w_at_max else None,
        "final_constant_lo": lo,
        "final_constant_hi": hi,
        "final_constant_L": last,
        f"{tag}_table": ys,
        "L_table": ys,
    }


def verdict_of(exh: list[dict], genuine: list[dict], plat: dict, tag: str) -> tuple[str, str]:
    if genuine:
        return (
            "KILL",
            f"finite nonzero row whose centre stays period-{tag[1:]} through an "
            "extended cap (looks genuinely eventual)",
        )
    table = plat["L_table"]
    wmax = exh[-1]["w"] if exh else 6
    sampled = bool(exh and exh[-1].get("mode") == "sampled")
    if plat["strictly_larger_at_wmax"] and not plat["real_plateau"]:
        extra = " (sampled w_max is a lower bound, already a kill)" if sampled else ""
        return (
            "KILL",
            f"{tag}(w) is still strictly larger at w={wmax} than at every "
            f"smaller scanned radius (table {table}){extra}",
        )
    if plat["still_growing_at_wmax"] and not plat["real_plateau"]:
        return (
            "KILL",
            f"{tag}(w) keeps growing through w={wmax} with no plateau "
            f"(table {table})",
        )
    max_L = plat["max_L"]
    w_at = plat["w_at_max"]
    wlo = min(w_at) if w_at else 0
    whi = max(w_at) if w_at else 0
    p = tag[1:]
    if sampled:
        return (
            "FINITE_BOUND",
            "no genuine eventual witness; "
            f"{tag}(w) is not strictly larger at sampled w={wmax} than at all "
            f"smaller w (table {table}), but w={wmax} is a sample so this is "
            "not an exhaustive finite theorem",
        )
    if plat["real_plateau"]:
        return (
            "FINITE_THEOREM",
            "no genuine eventual witness; "
            f"{tag}(w) plateaus at {max_L} on w={wlo}..{whi} of the scanned "
            f"radii (≥3 radii, not just the last two); every radius-w row "
            f"breaks every exact period-{p} centre run by time 8w+128, and "
            f"no period-{p} run exceeds {tag}(w)",
        )
    if plat.get("two_radius_edge"):
        return (
            "FINITE_BOUND",
            "no genuine eventual witness; "
            f"{tag}(w) is constant on only the last two scanned radii "
            f"(table {table}), which is not a real plateau (period 3 looked "
            "the same at w=6..7 before L3(8)=22)",
        )
    return (
        "FINITE_BOUND",
        "no genuine eventual witness and "
        f"{tag}(w) does not escape the cap; "
        f"{tag}(w) <= {max_L} on the scanned radii (max at w={w_at}); "
        "this is a finite bound, not a uniform proof, and not a real plateau",
    )


def _ext_note(b: dict) -> str:
    if b.get("ext_eventual"):
        return (
            f" Extending that evolution to {b.get('ext_tcap')} steps "
            f"looks eventual (`ext_L={b.get('ext_L')}`, suffix reaches the "
            f"extended cap)."
        )
    if b.get("ext_same_run_grew"):
        return (
            f" Extending that evolution to {b.get('ext_tcap')} steps "
            f"lengthens the same burst to `ext_L={b.get('ext_L')}` "
            f"(still finite; start stays `t={b.get('start')}`)."
        )
    if b.get("ext_new_burst"):
        return (
            f" Extending that evolution to {b.get('ext_tcap')} steps "
            f"finds a later finite burst `ext_L={b.get('ext_L')}` of "
            f"pattern `{b.get('ext_pattern')}` at "
            f"`t={b.get('ext_start')}..{b.get('ext_end')}` "
            f"(the tcap-window maximizer is not eventual)."
        )
    if b.get("ext_grew") is False:
        return (
            f" Extending that evolution to {b.get('ext_tcap')} steps "
            f"does not lengthen the run (`ext_L={b.get('ext_L')}`)."
        )
    return ""


def _period_markdown(lines: list, dump: dict, key: str, tag: str, title: str) -> None:
    a = lines.append
    block = dump[key]
    exh = block["exhaustive"]
    plat = block["plateau"]
    cat = CAT6 if tag == "L6" else CAT7
    period = cat["period"]
    necks = ", ".join(f"`{n}`" for n in cat["necklaces"])
    phases = ", ".join(cat["names"])

    a(f"## {title}")
    a("")
    a(f"The primitive necklaces of period {period} are {necks}. All")
    a(f"{cat['n']} rotations, and therefore every starting phase, are scored")
    a("as global alignments")
    a("")
    a("```")
    a(phases)
    a("```")
    a("")
    a(
        f"A centre factor is exact period {period} when it is a contiguous "
        f"run of one of those {cat['n']} infinite words."
    )
    if period == 6:
        a("The five non-primitive length-6 necklaces `000000`, `111111`,")
        a("`010101`, `001001`, and `011011` are excluded (periods 1, 2, 3).")
        a("A period-2 alternating factor matches a 5-bit window of `000101`")
        a("and then breaks, so it does not inflate `L6`.")
    else:
        a("Length 7 is prime, so the only excluded necklaces are the")
        a("constants `0000000` and `1111111` (20 binary necklaces minus")
        a("those two). A period-2 alternating factor matches a 7-bit window")
        a("of a primitive necklace (7 is odd) and then breaks, so it does")
        a("not inflate `L7`.")
    a("")

    a(
        f"| `w` | mode | scanned | states | `tcap` | `{tag}` | `L_prefix` | "
        f"`L_suffix` | `L>4w+16` | maximizer | pattern | start |"
    )
    a(
        "|----:|------|--------:|-------:|-------:|-----:|-----------:"
        "|-----------:|----------:|-----------|---------|------:|"
    )
    for r in exh:
        b = r["best"] or {}
        mx = b.get("row", "")
        pat = b.get("pattern", "")
        start = b.get("start", "")
        a(
            f"| {r['w']} | {r.get('mode', 'exhaustive')} | {r.get('n_scanned', r['n_nonzero'])} | "
            f"{r['n_nonzero']} | {r['tcap']} | {r['L_run']} | "
            f"{r['L_prefix']} | {r['L_suffix']} | "
            f"{r['n_L_gt_4w16']} | `{mx}` | `{pat}` | {start} |"
        )
    a("")

    a("Per-necklace maxima `L_neck(w)`:")
    a("")
    header = "| necklace | " + " | ".join(f"w={r['w']}" for r in exh) + " |"
    a(header)
    dash = "|----------|" + "|".join("----:" for _ in exh) + "|"
    a(dash)
    for name in cat["necklaces"]:
        cols = " | ".join(str(r["L_neck"][name]) for r in exh)
        a(f"| `{name}` | {cols} |")
    a("")

    w0 = exh[0] if exh else None
    if w0 is not None and w0["best"] is not None:
        b0 = w0["best"]
        extra = ""
        if b0.get("factor") is not None:
            extra = (
                f", the factor `{b0.get('factor', '')}` of pattern "
                f"`{b0.get('pattern')}` starting at time {b0.get('start')}."
            )
        else:
            extra = "."
        a(f"The prize seed (`w=0`) has `{tag}={w0['L_run']}`{extra}")
        a(f"`L_prefix(0)={w0['L_prefix']}`.")
        a("")

    for r in exh:
        b = r["best"]
        if not b or r["w"] == 0:
            continue
        extra = _ext_note(b)
        nmax = r["n_at_Lrun"]
        nmax_s = "1 mask attains" if nmax == 1 else f"{nmax} masks attain"
        a(
            f"Radius-{r['w']} maximizer: row `{b.get('row')}` (mask={b.get('mask')}), "
            f"pattern `{b.get('pattern')}` (necklace `{b.get('necklace')}`), "
            f"run of {b.get('L')} from `t={b.get('start')}` to `t={b.get('end')}` "
            f"({nmax_s} `{tag}`).{extra}"
        )
        bp = r.get("best_prefix")
        if bp:
            a(
                f"`L_prefix` maximizer at this radius: row `{bp.get('row')}` "
                f"(mask={bp.get('mask')}), pattern `{bp.get('pattern')}`, "
                f"prefix `{bp.get('factor')}` of length {bp.get('L_prefix')}."
            )
        a("")

    a("### Plateau / growth")
    a("")
    a(f"- `{tag}` table: `{plat['L_table']}`")
    a(f"- maximum `{plat['max_L']}` attained at `w={plat['w_at_max']}`")
    a(f"- still growing at `w_max`: `{plat['still_growing_at_wmax']}`")
    a(f"- strictly larger at `w_max` than every smaller `w`: `{plat['strictly_larger_at_wmax']}`")
    a(f"- plateau at the global max: `{plat['plateau_at_global_max']}`")
    a(f"- real plateau (≥3 consecutive radii): `{plat['real_plateau']}`")
    a(f"- two-radius edge only: `{plat['two_radius_edge']}`")
    a(
        f"- final constant block: `L={plat['final_constant_L']}` on "
        f"`w={plat['final_constant_lo']}..{plat['final_constant_hi']}`"
    )
    if plat.get("two_radius_edge"):
        a(
            "- caveat: this is only two radii at the scan edge, not Cycle I’s "
            "five-radius period-2 plateau (`L_run=24` on `6≤w≤10`). Period 3 "
            "looked the same at `w=6..7` (`L3=20`) before `L3(8)=22`. That is "
            "not a finite theorem."
        )
    a("")
    fit = block["fit_L_run"]
    fitp = block["fit_L_prefix"]
    a("Least squares over the whole table (a summary only, not a conjecture):")
    a("")
    a(f"- `{tag} ≈ {fit['C']:.3f}*w + {fit['Cprime']:.3f}`")
    a(f"- `L_prefix ≈ {fitp['C']:.3f}*w + {fitp['Cprime']:.3f}`")
    a("")

    n_eventual = block["exclusion_table"]["n_eventual_in_cap"]
    n_genuine = block["exclusion_table"]["n_genuine_eventual"]
    a("### Eventual witnesses")
    a("")
    if n_eventual == 0 and n_genuine == 0:
        a(
            f"No scanned row is eventual in the cap: a genuine eventual "
            f"regime would produce a period-{period} suffix of length "
            f"`tcap-O(w)`. Every maximizer’s run is a finite burst strictly "
            f"inside the window (or a short suffix that is not a light-cone "
            f"transient)."
        )
    else:
        a(
            f"`n_eventual_in_cap={n_eventual}`, "
            f"`n_genuine_eventual={n_genuine}`."
        )
        for s in block.get("genuine_eventual_witnesses") or []:
            a(
                f"- w={s.get('w')} mask={s.get('mask')} "
                f"L_at_tcap={s.get('L_at_tcap')} L_ext={s.get('L_ext')} "
                f"reaches_ext={s.get('reaches_ext')}"
            )
    cap_touch = [
        s for s in block.get("cap_survivors") or [] if not s.get("eventual_in_cap")
    ]
    if cap_touch:
        a("")
        a(
            "Some rows have a period-p burst that happens to end at `tcap` "
            "(window-edge, not light-cone eventual). Extending those evolutions "
            "does not produce an eventual regime:"
        )
        for s in cap_touch[:6]:
            a(
                f"- w={s.get('w')} mask={s.get('mask')} "
                f"L_at_tcap={s.get('L_at_tcap')} suffix={s.get('suffix')} "
                f"last_break={s.get('last_break')}; extended to {s.get('ext')}: "
                f"L_ext={s.get('L_ext')}, suffix_ext={s.get('suffix_ext')}, "
                f"reaches_ext={s.get('reaches_ext')}"
            )
    a("")
    a(f"### Verdict ({tag})")
    a("")
    a(f"`{block['verdict']}`.")
    a("")
    a(f"- Kill: {'yes' if block['kill'] else 'no'}.")
    a(f"- Reason: {block['kill_reason']}")
    a("")


def write_markdown(dump: dict) -> str:
    checks = dump["checks"]
    lines: list[str] = []
    a = lines.append
    a("# Period-6 and period-7 centres: finite-row analog of the radius-10 theorem")
    a("")
    a("This note is a checked finite scan. It does **not** exclude eventual")
    a("period 6 or 7 for every finite row, and it does not claim a prize result.")
    a("It is ideas11 item 3: the period-4/5 exhaustive of")
    a("`research/period45_fiber.py`, repeated for exact periods 6 and 7.")
    a("")
    a("Helper: `research/period67_fiber.py --certify`. Dump:")
    a("`research/period67_fiber.json`.")
    a("")
    a("## Attack")
    a("")
    a("Prove or kill: no nonzero finite-support configuration has an")
    a("eventually period-6 or period-7 central trace. Broader than the prize")
    a("seed. Not the strip-graph residual-SCC test (residual components")
    a("remain for every primitive period-6 and period-7 word; see")
    a("`period_scan_6.json` / `period_scan_7.json`), not onset SAT,")
    a("not `F_T` ideal certificates, and not the unique-left fiber")
    a("reconstruction of `period2_fiber.py`.")
    a("")
    a("Kill: `L6(w)` or `L7(w)` is still strictly larger at the max scanned")
    a("`w` than at every smaller scanned radius (growing, no plateau), or a")
    a("finite row whose centre stays period-p through the cap and still does")
    a("not break when the cap is extended. Survive a finite theorem if `L_p`")
    a("plateaus at a constant on at least three scanned radii, like Cycle I’s")
    a("period-2 `L_run=24` for `6≤w≤10`. A two-radius edge plateau is not a")
    a("finite theorem (period 3 looked the same at `w=6..7` before `L3(8)=22`).")
    a("")
    a("## Engine")
    a("")
    wmax = dump["w_max"]
    nmax = dump["n_masks_wmax"]
    sampled = dump.get("w6_sampled", False)
    if sampled:
        a(f"Every nonzero initial word of support radius `w=0..5` is evolved")
        a("exhaustively; radius `w=6` is sampled (see the table). Packed Rule 30")
    else:
        a(f"Every nonzero initial word of support radius `w=0..{wmax}`")
        a(f"(`2^{{2w+1}}-1` states; `w={wmax}` is `{nmax}`) is evolved in a")
    a("quiescent background up to `tcap = 8w+128`. Packed Rule 30")
    a("`new = (row<<2) ^ ((row<<1)|row)`, bit 0 leftmost, centre bit")
    a("`(row>>(w+t))&1`, copied from `research/period45_fiber.py` and matching")
    a("`experiment.center_bits` on the prize seed prefix of length 256")
    a(f"(`{checks['prize_prefix16']}…`) and an independent live-cell")
    a("implementation on sampled small rows. The streaming scorer matches a")
    a("stored-trace scorer on those rows. One packed evolution scores both")
    a("periods.")
    a("")
    a("`L_run(w) = L_p(w)` is the longest such run anywhere in `[0, tcap)`.")
    a("`L_prefix(w)` is the longest exact period-p prefix from time 0.")
    a("Per-necklace maxima are recorded. No row is “eventual in the cap”")
    a("(last break inside the light cone `2w+8`, suffix at least 16) unless")
    a("listed below.")
    a("")

    _period_markdown(lines, dump, "period6", "L6", "Period 6")
    _period_markdown(lines, dump, "period7", "L7", "Period 7")

    a("## What is proved, what is not")
    a("")
    a("Proved (and machine-checked):")
    a("")
    a("- Packed evolution agrees with `experiment.center_bits` on 256")
    a("  prize-seed bits and with an independent live-cell spacetime on")
    a("  sampled radius-`w` rows.")
    a("- The streaming scorer agrees with a stored-trace scorer for both")
    a("  catalogs, including the combined one-evolution path.")
    a("- Synthetic primitive words score as claimed; period-2, period-3,")
    a("  period-4, period-5, and constant traces are not long exact")
    a("  period-6 or period-7 runs.")
    a("- `010101` / `001001` / `011011` are not period-6 necklaces;")
    a("  `0000000` / `1111111` are not period-7 necklaces.")
    plat6 = dump["period6"]["plateau"]
    plat7 = dump["period7"]["plateau"]
    a(
        f"- The exclusion tables inside `tcap=8w+128` for `w≤{wmax}`: "
        f"`L6={plat6['L_table']}`, `L7={plat7['L_table']}`."
    )
    for key, tag in (("period6", "L6"), ("period7", "L7")):
        block = dump[key]
        plat = block["plateau"]
        max_L = plat["max_L"]
        p = tag[1:]
        if block["verdict"] == "FINITE_THEOREM":
            a(
                f"- **Finite theorem ({tag}).** Every nonzero row of support "
                f"radius `w≤{wmax}` has every exact period-{p} centre run of "
                f"length at most `{tag}(w)`, hence at most {max_L}, inside "
                f"`tcap=8w+128`. The constant block covers "
                f"`w={plat['plateau_lo']}..{plat['plateau_hi']}` (≥3 radii)."
            )
        elif block["verdict"] == "FINITE_BOUND":
            a(
                f"- **Finite bound, not a theorem ({tag}).** `{tag}(w)≤{max_L}` "
                f"on the scanned radii, but this is not a real plateau "
                f"(table `{plat['L_table']}`)."
            )
        else:
            a(
                f"- **No plateau ({tag}).** Unlike period 2 (`L_run=24` for "
                f"`6≤w≤10`), `{tag}(w)` is still strictly larger at `w={wmax}` "
                f"than at every smaller scanned radius "
                f"(`{tag}({wmax})={max_L}`). That kills this route as a "
                "Condrey-style finite theorem at these radii."
            )
    a("")
    a("Not proved:")
    a("")
    a(f"- A uniform-in-`w` bound on `L6(w)` or `L7(w)`. The tables are only")
    a(f"  for radius `≤{wmax}`.")
    a("- Existence of an eventually period-6 or period-7 finite row. Growth")
    a("  of `L_p(w)` is compatible with either a slow unbounded family or a")
    a("  later plateau; it is not a witness.")
    a("- Eventual period 6 or 7 of the prize seed. The seed is the `w=0`")
    a(
        f"  line (`L6={dump['period6']['exhaustive'][0]['L_run']}`, "
        f"`L7={dump['period7']['exhaustive'][0]['L_run']}`)."
    )
    a("- Anything about residual strip-graph SCCs for these necklaces.")
    a("")
    a("## Verdict")
    a("")
    a(f"`{dump['verdict']}`, wall time {dump['wall_time_sec']:.1f}s.")
    a("")
    a(f"- Kill: {'yes' if dump['kill'] else 'no'}.")
    a(f"- Survive: {'yes' if dump['survive'] else 'no'}.")
    a("- Witness: none (no eventual-in-cap row) unless listed above.")
    a(f"- Reason: {dump['kill_reason']}")
    a(
        f"- Exclusion tables: `L6(w)` and `L7(w)` as above, `tcap=8w+128`, "
        f"radius `≤{wmax}`."
    )
    a("")
    a("## Files")
    a("")
    a("- `research/period67_fiber.md` (this note)")
    a("- `research/period67_fiber.py` (`--certify` runs the checks and the")
    a("  radius-`w` exhaustive)")
    a("- `research/period67_fiber.json` (dump)")
    a("")
    return "\n".join(lines) + "\n"


def _period_bundle(exh: list[dict], cap_surv: list[dict], tag: str, cat: dict) -> dict:
    plat = plateau_info(exh, tag)
    xs = [r["w"] for r in exh]
    ys = [r["L_run"] for r in exh]
    C, Cp = fit_linear(xs, ys)
    residuals = [y - (C * x + Cp) for x, y in zip(xs, ys)]
    yp = [r["L_prefix"] for r in exh]
    Cp2, Cpp = fit_linear(xs, yp)
    genuine = [
        s for s in cap_surv if s.get("eventual_in_cap") and s.get("reaches_ext")
    ]
    verdict, kill_reason = verdict_of(exh, genuine, plat, tag)
    neck_tables = {
        name: [{"w": r["w"], "L": r["L_neck"][name]} for r in exh]
        for name in cat["necklaces"]
    }
    return {
        "period": cat["period"],
        "centre_words": list(cat["names"]),
        "necklaces": list(cat["necklaces"]),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": verdict == "SURVIVE",
        "kill_reason": kill_reason,
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
                f"least-squares {tag} ~ C*w+C' is a summary only; the table "
                "is the actual finite statement"
            ),
        },
        "fit_L_prefix": {"C": Cp2, "Cprime": Cpp},
        "exclusion_table": {
            "f_w": (
                f"{tag}(w)=L_run(w); an exact period-{cat['period']} centre "
                f"run of a radius-w row lasts at most {tag}(w) steps inside "
                "tcap=8w+128"
            ),
            tag: [{"w": r["w"], "L": r["L_run"], "tcap": r["tcap"]} for r in exh],
            "L_run": [{"w": r["w"], "L": r["L_run"], "tcap": r["tcap"]} for r in exh],
            "L_prefix": [{"w": r["w"], "L": r["L_prefix"]} for r in exh],
            "L_neck": neck_tables,
            "n_L_gt_4w16": sum(r["n_L_gt_4w16"] for r in exh),
            "n_eventual_in_cap": sum(r["n_cap_survivors"] for r in exh),
            "n_genuine_eventual": len(genuine),
        },
    }


def _combine_verdict(p6: dict, p7: dict) -> tuple[str, str]:
    if p6["verdict"] == "KILL" and p7["verdict"] == "KILL":
        return "KILL", f"L6: {p6['kill_reason']}; L7: {p7['kill_reason']}"
    if p6["verdict"] == "KILL":
        return "KILL", f"L6: {p6['kill_reason']} (L7: {p7['kill_reason']})"
    if p7["verdict"] == "KILL":
        return "KILL", f"L7: {p7['kill_reason']} (L6: {p6['kill_reason']})"
    if p6["verdict"] == "FINITE_THEOREM" and p7["verdict"] == "FINITE_THEOREM":
        return "FINITE_THEOREM", f"L6: {p6['kill_reason']}; L7: {p7['kill_reason']}"
    return "FINITE_BOUND", f"L6: {p6['kill_reason']}; L7: {p7['kill_reason']}"


def certify(w_max: int, sample_w6: int) -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    print(log[-1], flush=True)
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    rows6, rows7, cap6, cap7 = exhaustive_scan(w_max, sample_w6, log)
    p6 = _period_bundle(rows6, cap6, "L6", CAT6)
    p7 = _period_bundle(rows7, cap7, "L7", CAT7)
    wall = time.perf_counter() - t_all
    verdict, kill_reason = _combine_verdict(p6, p7)
    w6_sampled = bool(w_max >= 6 and sample_w6)

    dump = {
        "attack": "period67_fiber",
        "ideas": "ideas11 item 3",
        "problem": (
            "no nonzero finite-support configuration has an eventually "
            "period-6 or period-7 central trace"
        ),
        "centre_words_p6": list(CAT6["names"]),
        "centre_words_p7": list(CAT7["names"]),
        "necklaces_p6": list(P6_NECK),
        "necklaces_p7": list(P7_NECK),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": verdict == "SURVIVE",
        "kill_reason": kill_reason,
        "wall_time_sec": round(wall, 4),
        "tcap_long": "8w+128",
        "w_max": w_max,
        "n_masks_wmax": (1 << (2 * w_max + 1)) - 1,
        "w6_sampled": w6_sampled,
        "sample_w6": sample_w6,
        "checks": checks,
        "period6": p6,
        "period7": p7,
        "log": log,
    }
    OUT_JSON.write_text(json.dumps(dump, indent=2) + "\n")
    OUT_MD.write_text(write_markdown(dump))
    print(f"wrote {OUT_JSON}", flush=True)
    print(f"wrote {OUT_MD}", flush=True)
    print(f"verdict={verdict} wall={wall:.3f}s", flush=True)
    print(f"reason: {kill_reason}", flush=True)
    print(f"L6 by w: {[(r['w'], r['L_run'], r['tcap'], r.get('mode')) for r in rows6]}", flush=True)
    print(f"L7 by w: {[(r['w'], r['L_run'], r['tcap'], r.get('mode')) for r in rows7]}", flush=True)
    print(
        f"n_cap6={sum(r['n_cap_survivors'] for r in rows6)} "
        f"genuine6={len(p6['genuine_eventual_witnesses'])} "
        f"n_cap7={sum(r['n_cap_survivors'] for r in rows7)} "
        f"genuine7={len(p7['genuine_eventual_witnesses'])}",
        flush=True,
    )
    return dump


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    p.add_argument("--w-max", type=int, default=6)
    p.add_argument(
        "--sample-w6",
        type=int,
        default=0,
        help="if >0, exhaustive w<=5 and sample this many masks at w=6",
    )
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    if args.w_max < 0 or args.w_max > 12:
        p.error("--w-max must be in 0..12")
    if args.sample_w6 < 0:
        p.error("--sample-w6 must be >= 0")
    certify(args.w_max, args.sample_w6)


if __name__ == "__main__":
    main()
