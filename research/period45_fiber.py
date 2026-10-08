#!/usr/bin/env python3
"""Cycle I / ideas10 item 3: Condrey-style finite-row scan for periods 4 and 5.

Same exhaustive packed scan as research/period3_fiber.py (packed step copied,
that file is not modified). The centre factor is exact period 4 or exact
period 5. Primitive necklaces only; all rotations (global phases) are scored.

Period 4: 0001, 0011, 0111 (12 phases). 0101 is period 2 and is excluded.
Period 5: the six primitive necklaces (30 phases). Length-5 has eight binary
necklaces; 00000 and 11111 are period 1 and are excluded, matching the
period-3 exclusion of 000 / 111.

    L4(w) = longest run of any of the 12 infinite period-4 words
    L5(w) = longest run of any of the 30 infinite period-5 words

in the centre of a radius-w finite row, evolved in a quiescent background.
L_prefix(w) is the same quantity restricted to a run that starts at t=0.

Exhaustive w=0..7 (2^{15}-1 nonzero masks at w=7). tcap=8w+128.
Packed Rule 30: new=(row<<2)^((row<<1)|row), centre (row>>(w+t))&1.

Kill: L_p(w) is still strictly larger at w=7 than at every smaller scanned
radius (growing, no plateau), or a witness that remains period-p through the
whole cap (looks eventual). Finite theorem if L_p plateaus at a constant on
the scanned radii, like Cycle I's period-2 L_run=24 for 6<=w<=10.

This is not the strip-graph residual-SCC test, not onset SAT, not an
F_T ideal certificate, and not the period-2 fiber reconstruction.
Stdlib only. Not a prize claim.

Run: python3 research/period45_fiber.py --certify
Dump: research/period45_fiber.json, research/period45_fiber.md
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

PRIZE_PREFIX16 = "1101110011000101"

# Explicit primitive necklaces. Period 5 has six, not eight: the other two
# length-5 necklaces are the constants 00000 and 11111.
P4_NECK = ("0001", "0011", "0111")
P5_NECK = ("00001", "00011", "00101", "00111", "01011", "01111")


# ---------------------------------------------------------------------------
# Rule 30, packed. Copied from research/period3_fiber.py; that file is not
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


CAT4 = make_catalog(P4_NECK)
CAT5 = make_catalog(P5_NECK)


# ---------------------------------------------------------------------------
# Exact period-p runs. A factor is exact period p iff it matches one of the
# infinite words along global time (rotations already encode the phase).
# Constants and proper-divisor periods are excluded because they are not in
# the catalog.
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


def scan_mask_p45(mask: int, w: int, tcap: int) -> tuple[dict, dict]:
    """One packed evolution, both catalogs. Inner update is integer compares."""
    p4 = CAT4["pats"]
    p5 = CAT5["pats"]
    n4 = CAT4["n"]
    n5 = CAT5["n"]
    c4 = [0] * n4
    s4 = [0] * n4
    b4 = [0] * n4
    bs4 = [0] * n4
    pfx4 = [0] * n4
    a4 = [1] * n4
    c5 = [0] * n5
    s5 = [0] * n5
    b5 = [0] * n5
    bs5 = [0] * n5
    pfx5 = [0] * n5
    a5 = [1] * n5
    row = mask
    for t in range(tcap):
        bit = (row >> (w + t)) & 1
        r4 = t & 3
        r5 = t % 5
        for i in range(n4):
            if bit == p4[i][r4]:
                if c4[i] == 0:
                    s4[i] = t
                c4[i] += 1
                if a4[i]:
                    pfx4[i] += 1
                if c4[i] > b4[i]:
                    b4[i] = c4[i]
                    bs4[i] = s4[i]
            else:
                c4[i] = 0
                a4[i] = 0
        for i in range(n5):
            if bit == p5[i][r5]:
                if c5[i] == 0:
                    s5[i] = t
                c5[i] += 1
                if a5[i]:
                    pfx5[i] += 1
                if c5[i] > b5[i]:
                    b5[i] = c5[i]
                    bs5[i] = s5[i]
            else:
                c5[i] = 0
                a5[i] = 0
        row = (row << 2) ^ ((row << 1) | row)
    return (
        _assemble(CAT4, b4, bs4, pfx4, c4, tcap),
        _assemble(CAT5, b5, bs5, pfx5, c5, tcap),
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

    checks["p4_necklaces"] = list(P4_NECK)
    checks["p5_necklaces"] = list(P5_NECK)
    checks["p4_necklaces_match_generator"] = list(P4_NECK) == primitive_necklaces(4)
    checks["p5_necklaces_match_generator"] = list(P5_NECK) == primitive_necklaces(5)
    checks["n_p4_necklaces"] = len(P4_NECK)
    checks["n_p4_necklaces_is_3"] = len(P4_NECK) == 3
    checks["n_p5_primitive_necklaces"] = len(P5_NECK)
    checks["n_p5_primitive_necklaces_is_6"] = len(P5_NECK) == 6
    checks["n_p5_all_length5_necklaces_is_8"] = len(primitive_necklaces(5)) + 2 == 8
    checks["n_p4_phases"] = CAT4["n"]
    checks["n_p4_phases_is_12"] = CAT4["n"] == 12
    checks["n_p5_phases"] = CAT5["n"]
    checks["n_p5_phases_is_30"] = CAT5["n"] == 30
    checks["p4_excludes_0101"] = "0101" not in CAT4["names"]
    checks["p4_excludes_1010"] = "1010" not in CAT4["names"]
    checks["p4_excludes_0000"] = "0000" not in CAT4["names"]
    checks["p4_excludes_1111"] = "1111" not in CAT4["names"]
    checks["p5_excludes_00000"] = "00000" not in CAT5["names"]
    checks["p5_excludes_11111"] = "11111" not in CAT5["names"]
    checks["each_p4_necklace_primitive"] = all(min_period(n) == 4 for n in P4_NECK)
    checks["each_p5_necklace_primitive"] = all(min_period(n) == 5 for n in P5_NECK)

    # Synthetic exact period-4 traces.
    syn_0001 = [0, 0, 0, 1] * 20
    st = stats_from_bits(syn_0001, CAT4)
    checks["synthetic_0001_L"] = st["L"] == 80
    checks["synthetic_0001_prefix"] = st["prefix"] == 80
    checks["synthetic_0001_pattern"] = st["pattern"] == "0001"
    checks["synthetic_0001_necklace"] = st["necklace"] == "0001"

    syn_0010 = [0, 0, 1, 0] * 12
    st = stats_from_bits(syn_0010, CAT4)
    checks["synthetic_0010_pattern"] = st["pattern"] == "0010"
    checks["synthetic_0010_necklace"] = st["necklace"] == "0001"
    checks["synthetic_0010_L"] = st["L"] == 48

    syn_0011 = [0, 0, 1, 1] * 15
    st = stats_from_bits(syn_0011, CAT4)
    checks["synthetic_0011_L"] = st["L"] == 60
    checks["synthetic_0011_pattern"] = st["pattern"] == "0011"
    checks["synthetic_0011_necklace"] = st["necklace"] == "0011"

    syn_0111 = [0, 1, 1, 1] * 10
    st = stats_from_bits(syn_0111, CAT4)
    checks["synthetic_0111_L"] = st["L"] == 40
    checks["synthetic_0111_necklace"] = st["necklace"] == "0111"

    # Period 2 is not a long period-4 run: "01" repeating matches a 3-bit
    # window of 0100 and then breaks. 0101 itself is excluded.
    syn_p2 = [t & 1 for t in range(64)]
    st = stats_from_bits(syn_p2, CAT4)
    checks["period2_is_not_long_p4"] = st["L"] == 3

    st = stats_from_bits([0] * 40, CAT4)
    checks["constant0_p4_L_lt_4"] = st["L"] < 4
    st = stats_from_bits([1] * 40, CAT4)
    checks["constant1_p4_L_lt_4"] = st["L"] < 4

    # Synthetic exact period-5 traces.
    syn_00001 = [0, 0, 0, 0, 1] * 16
    st = stats_from_bits(syn_00001, CAT5)
    checks["synthetic_00001_L"] = st["L"] == 80
    checks["synthetic_00001_pattern"] = st["pattern"] == "00001"
    checks["synthetic_00001_necklace"] = st["necklace"] == "00001"

    syn_01010 = [0, 1, 0, 1, 0] * 10
    st = stats_from_bits(syn_01010, CAT5)
    checks["synthetic_01010_pattern"] = st["pattern"] == "01010"
    checks["synthetic_01010_necklace"] = st["necklace"] == "00101"
    checks["synthetic_01010_L"] = st["L"] == 50

    syn_01111 = [0, 1, 1, 1, 1] * 8
    st = stats_from_bits(syn_01111, CAT5)
    checks["synthetic_01111_L"] = st["L"] == 40
    checks["synthetic_01111_necklace"] = st["necklace"] == "01111"

    # (01)^∞ matches a 5-window of 01010 / 10101 and then breaks at lag 5.
    st = stats_from_bits(syn_p2, CAT5)
    checks["period2_is_not_long_p5"] = st["L"] == 5

    # (001)^∞ matches a short window of 00101 / 00001 and then breaks.
    syn_p3 = [0, 0, 1] * 20
    st = stats_from_bits(syn_p3, CAT5)
    checks["period3_is_not_long_p5"] = st["L"] == 6
    st = stats_from_bits(syn_p3, CAT4)
    checks["period3_is_not_long_p4"] = st["L"] == 5

    st = stats_from_bits([0] * 40, CAT5)
    checks["constant0_p5_L_lt_5"] = st["L"] < 5
    st = stats_from_bits([1] * 40, CAT5)
    checks["constant1_p5_L_lt_5"] = st["L"] < 5

    # Streaming scan agrees with the stored-trace scorer, both catalogs,
    # including the combined one-evolution path.
    stream_ok = True
    stream_fail = None
    keys = ("L", "start", "end", "prefix", "suffix", "pattern", "necklace")
    for w, mask, tcap in [(0, 1, 64), (1, 5, 40), (2, 19, 48), (3, 73, 56), (4, 300, 40)]:
        a4, a5 = scan_mask_p45(mask, w, tcap)
        bits = evolve_centers(mask, w, tcap)
        b4 = stats_from_bits(bits, CAT4)
        b5 = stats_from_bits(bits, CAT5)
        s4 = scan_mask(mask, w, tcap, CAT4)
        s5 = scan_mask(mask, w, tcap, CAT5)
        if any(a4[k] != b4[k] for k in keys) or a4["L_neck"] != b4["L_neck"]:
            stream_ok = False
            stream_fail = {"which": "p4-combined", "w": w, "mask": mask}
            break
        if any(a5[k] != b5[k] for k in keys) or a5["L_neck"] != b5["L_neck"]:
            stream_ok = False
            stream_fail = {"which": "p5-combined", "w": w, "mask": mask}
            break
        if any(s4[k] != b4[k] for k in keys) or any(s5[k] != b5[k] for k in keys):
            stream_ok = False
            stream_fail = {"which": "single-catalog", "w": w, "mask": mask}
            break
    checks["scan_matches_stored_trace"] = stream_ok
    if stream_fail is not None:
        checks["scan_fail"] = stream_fail

    prize16 = [int(ch) for ch in PRIZE_PREFIX16]
    st4 = stats_from_bits(prize16, CAT4)
    st5 = stats_from_bits(prize16, CAT5)
    checks["prize_p4_prefix16"] = st4["prefix"]
    checks["prize_p5_prefix16"] = st5["prefix"]
    checks["prize_p4_L16"] = st4["L"]
    checks["prize_p5_L16"] = st5["L"]

    checks["all_ok"] = all(
        v is True
        for k, v in checks.items()
        if k
        not in (
            "prize_prefix16",
            "prize_p4_prefix16",
            "prize_p5_prefix16",
            "prize_p4_L16",
            "prize_p5_L16",
            "p4_necklaces",
            "p5_necklaces",
            "n_p4_necklaces",
            "n_p5_primitive_necklaces",
            "n_p4_phases",
            "n_p5_phases",
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

    def update(self, mask: int, st: dict) -> None:
        L = st["L"]
        if L > self.Lrun:
            self.Lrun = L
            self.n_at_max = 1
            self.best = _best_record(mask, self.w, st)
        elif L == self.Lrun:
            self.n_at_max += 1
        if st["prefix"] > self.Lpref:
            self.Lpref = st["prefix"]
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

    def finish(self, elapsed: float) -> dict:
        if self.best is not None:
            _confirm_best(self.best, self.w, self.tcap, self.cat)
        if self.best_prefix is not None:
            _confirm_prefix(self.best_prefix, self.w, self.tcap, self.cat)
        row = {
            "w": self.w,
            "n_nonzero": (1 << (2 * self.w + 1)) - 1,
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


def exhaustive_scan(w_max: int, log: list[str]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    rows4: list[dict] = []
    rows5: list[dict] = []
    cap4: list[dict] = []
    cap5: list[dict] = []
    for w in range(0, w_max + 1):
        tcap = tcap_long(w)
        nstates = 1 << (2 * w + 1)
        t0 = time.perf_counter()
        acc4 = _Acc(CAT4, w, tcap)
        acc5 = _Acc(CAT5, w, tcap)
        for mask in range(1, nstates):
            st4, st5 = scan_mask_p45(mask, w, tcap)
            acc4.update(mask, st4)
            acc5.update(mask, st5)
        elapsed = time.perf_counter() - t0
        row4 = acc4.finish(elapsed)
        row5 = acc5.finish(elapsed)
        rows4.append(row4)
        rows5.append(row5)
        cap4.extend(acc4.cap_survivors)
        cap5.extend(acc5.cap_survivors)
        log.append(
            f"exhaustive w={w} n={nstates - 1} tcap={tcap} "
            f"L4={acc4.Lrun} L5={acc5.Lrun} "
            f"L4_prefix={acc4.Lpref} L5_prefix={acc5.Lpref} "
            f"n4_at_max={acc4.n_at_max} n5_at_max={acc5.n_at_max} "
            f"reach4={acc4.n_reach} reach5={acc5.n_reach} "
            f"{elapsed:.3f}s"
        )
        print(log[-1], flush=True)
    return rows4, rows5, cap4, cap5


def plateau_info(exh: list[dict], tag: str) -> dict:
    ys = [r["L_run"] for r in exh]
    if not ys:
        return {
            f"max_{tag}": 0,
            "plateau": False,
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
    return {
        f"max_{tag}": max_L,
        "max_L": max_L,
        "plateau": bool(plateau_at_max or (plateau and last == max_L and hi - lo >= 1)),
        "plateau_at_global_max": plateau_at_max,
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
    wmax = exh[-1]["w"] if exh else 7
    if plat["strictly_larger_at_wmax"] and not plat["plateau"]:
        return (
            "KILL",
            f"{tag}(w) is still strictly larger at w={wmax} than at every "
            f"smaller scanned radius (table {table})",
        )
    if plat["still_growing_at_wmax"] and not plat["plateau"]:
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
    if plat["plateau"]:
        return (
            "FINITE_THEOREM",
            "no genuine eventual witness; "
            f"{tag}(w) plateaus at {max_L} on w={wlo}..{whi} of the scanned "
            f"radii; every radius-w row breaks every exact period-{p} centre "
            f"run by time 8w+128, and no period-{p} run exceeds {tag}(w)",
        )
    return (
        "FINITE_THEOREM",
        "no genuine eventual witness and "
        f"{tag}(w) does not escape the cap; "
        f"{tag}(w) <= {max_L} on the scanned radii (max at w={w_at}); "
        "this is a finite bound, not a uniform proof",
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
    cat = CAT4 if tag == "L4" else CAT5
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
    if period == 4:
        a("The period-2 necklace `0101` and the constants `0000` / `1111`")
        a("are excluded. A period-2 alternating factor matches a 3-bit")
        a("window of `0100` and then breaks, so it does not inflate `L4`.")
    else:
        a("Constants `00000` and `11111` are excluded (they have period 1);")
        a("those two extra length-5 necklaces are why some notes say “8")
        a("necklaces”. A period-2 alternating factor matches a 5-bit window")
        a("of `01010` or `10101` and then breaks, so it does not inflate `L5`.")
    a("")

    neck_headers = " | ".join(f"`L_{n}`" for n in cat["necklaces"])
    a(
        f"| `w` | states | `tcap` | `{tag}` | `L_prefix` | `L_suffix` | "
        f"{neck_headers} | `L>4w+16` | maximizer | pattern | start |"
    )
    dashes = "|----:|-------:|-------:|-----:|-----------:|-----------:"
    dashes += "|--------:" * len(cat["necklaces"])
    dashes += "|----------:|-----------|---------|------:|"
    a(dashes)
    for r in exh:
        b = r["best"] or {}
        mx = b.get("row", "")
        pat = b.get("pattern", "")
        start = b.get("start", "")
        neck_cols = " | ".join(str(r["L_neck"][n]) for n in cat["necklaces"])
        a(
            f"| {r['w']} | {r['n_nonzero']} | {r['tcap']} | {r['L_run']} | "
            f"{r['L_prefix']} | {r['L_suffix']} | {neck_cols} | "
            f"{r['n_L_gt_4w16']} | `{mx}` | `{pat}` | {start} |"
        )
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
    a(
        f"- final constant block: `L={plat['final_constant_L']}` on "
        f"`w={plat['final_constant_lo']}..{plat['final_constant_hi']}`"
    )
    wmax = exh[-1]["w"] if exh else None
    if (
        plat.get("plateau")
        and plat.get("plateau_hi") == wmax
        and plat.get("plateau_lo") is not None
        and plat["plateau_hi"] - plat["plateau_lo"] <= 1
    ):
        a(
            f"- caveat: this is only two radii at the scan edge, not Cycle I’s "
            f"five-radius period-2 plateau (`L_run=24` on `6≤w≤10`). Period 3 "
            f"looked the same at `w=6..7` (`L3=20`) before `L3(8)=22`."
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
    a("# Period-4 and period-5 centres: finite-row analog of the radius-10 theorem")
    a("")
    a("This note is a checked finite scan. It does **not** exclude eventual")
    a("period 4 or 5 for every finite row, and it does not claim a prize result.")
    a("It is ideas10 item 3: the period-3 exhaustive of")
    a("`research/period3_fiber.py`, repeated for exact periods 4 and 5.")
    a("")
    a("Helper: `research/period45_fiber.py --certify`. Dump:")
    a("`research/period45_fiber.json`.")
    a("")
    a("## Attack")
    a("")
    a("Prove or kill: no nonzero finite-support configuration has an")
    a("eventually period-4 or period-5 central trace. Broader than the prize")
    a("seed. Not the strip-graph residual-SCC test (residual components")
    a("remain for every primitive period-4 and period-5 word), not onset SAT,")
    a("not `F_T` ideal certificates, and not the unique-left fiber")
    a("reconstruction of `period2_fiber.py`.")
    a("")
    a("Kill: `L4(w)` or `L5(w)` is still strictly larger at `w=7` than at")
    a("every smaller scanned radius (growing, no plateau), or a finite row")
    a("whose centre stays period-p through the cap and still does not break")
    a("when the cap is extended. Survive a finite theorem if `L_p` plateaus")
    a("at a constant on the scanned radii, like Cycle I’s period-2")
    a("`L_run=24` for `6≤w≤10`.")
    a("")
    a("## Engine")
    a("")
    a("Every nonzero initial word of support radius `w=0..7`")
    a("(`2^{2w+1}-1` states; `w=7` is `2^{15}-1`) is evolved in a")
    a("quiescent background up to `tcap = 8w+128`. Packed Rule 30")
    a("`new = (row<<2) ^ ((row<<1)|row)`, bit 0 leftmost, centre bit")
    a("`(row>>(w+t))&1`, copied from `research/period3_fiber.py` and matching")
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

    _period_markdown(lines, dump, "period4", "L4", "Period 4")
    _period_markdown(lines, dump, "period5", "L5", "Period 5")

    wmax = dump["w_max"]
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
    a("  and constant traces are not long exact period-4 or period-5 runs.")
    a("- `0101` is not a period-4 necklace; `00000` / `11111` are not")
    a("  period-5 necklaces.")
    plat4 = dump["period4"]["plateau"]
    plat5 = dump["period5"]["plateau"]
    a(
        f"- The exclusion tables inside `tcap=8w+128` for `w≤{wmax}`: "
        f"`L4={plat4['L_table']}`, `L5={plat5['L_table']}`."
    )
    for key, tag in (("period4", "L4"), ("period5", "L5")):
        block = dump[key]
        plat = block["plateau"]
        max_L = plat["max_L"]
        p = tag[1:]
        if block["verdict"] == "FINITE_THEOREM":
            edge = (
                plat.get("plateau_hi") == wmax
                and plat.get("plateau_lo") is not None
                and plat["plateau_hi"] - plat["plateau_lo"] <= 1
            )
            extra = (
                " The constant block is only two radii at the scan edge, "
                "weaker than Cycle I’s period-2 plateau on `6≤w≤10`; it is a "
                f"checked bound `{tag}(w)≤{max_L}` for `w≤{wmax}`, not a "
                "uniform-in-`w` theorem."
                if edge
                else ""
            )
            a(
                f"- **Finite theorem ({tag}).** Every nonzero row of support "
                f"radius `w≤{wmax}` has every exact period-{p} centre run of "
                f"length at most `{tag}(w)`, hence at most {max_L}, inside "
                f"`tcap=8w+128`.{extra}"
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
    a(f"- A uniform-in-`w` bound on `L4(w)` or `L5(w)`. The tables are only")
    a(f"  for radius `≤{wmax}`.")
    a("- Existence of an eventually period-4 or period-5 finite row. Growth")
    a("  of `L_p(w)` is compatible with either a slow unbounded family or a")
    a("  later plateau; it is not a witness.")
    a("- Eventual period 4 or 5 of the prize seed. The seed is the `w=0`")
    a(
        f"  line (`L4={dump['period4']['exhaustive'][0]['L_run']}`, "
        f"`L5={dump['period5']['exhaustive'][0]['L_run']}`)."
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
        f"- Exclusion tables: `L4(w)` and `L5(w)` as above, `tcap=8w+128`, "
        f"radius `≤{wmax}`."
    )
    a("")
    a("## Files")
    a("")
    a("- `research/period45_fiber.md` (this note)")
    a("- `research/period45_fiber.py` (`--certify` runs the checks and the")
    a("  radius-`w` exhaustive)")
    a("- `research/period45_fiber.json` (dump)")
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


def certify(w_max: int) -> dict:
    log: list[str] = []
    t_all = time.perf_counter()

    checks = run_checks()
    log.append(f"checks all_ok={checks['all_ok']}")
    print(log[-1], flush=True)
    if not checks["all_ok"]:
        raise AssertionError(f"self-checks failed: {checks}")

    rows4, rows5, cap4, cap5 = exhaustive_scan(w_max, log)
    p4 = _period_bundle(rows4, cap4, "L4", CAT4)
    p5 = _period_bundle(rows5, cap5, "L5", CAT5)
    wall = time.perf_counter() - t_all

    if p4["verdict"] == "KILL" and p5["verdict"] == "KILL":
        verdict = "KILL"
        kill_reason = f"L4: {p4['kill_reason']}; L5: {p5['kill_reason']}"
    elif p4["verdict"] == "KILL":
        verdict = "KILL"
        kill_reason = f"L4: {p4['kill_reason']} (L5: {p5['kill_reason']})"
    elif p5["verdict"] == "KILL":
        verdict = "KILL"
        kill_reason = f"L5: {p5['kill_reason']} (L4: {p4['kill_reason']})"
    else:
        verdict = "FINITE_THEOREM"
        kill_reason = f"L4: {p4['kill_reason']}; L5: {p5['kill_reason']}"

    dump = {
        "attack": "period45_fiber",
        "ideas": "ideas10 item 3",
        "problem": (
            "no nonzero finite-support configuration has an eventually "
            "period-4 or period-5 central trace"
        ),
        "centre_words_p4": list(CAT4["names"]),
        "centre_words_p5": list(CAT5["names"]),
        "necklaces_p4": list(P4_NECK),
        "necklaces_p5": list(P5_NECK),
        "verdict": verdict,
        "kill": verdict == "KILL",
        "survive": verdict == "SURVIVE",
        "kill_reason": kill_reason,
        "wall_time_sec": round(wall, 4),
        "tcap_long": "8w+128",
        "w_max": w_max,
        "n_masks_wmax": (1 << (2 * w_max + 1)) - 1,
        "checks": checks,
        "period4": p4,
        "period5": p5,
        "log": log,
    }
    OUT_JSON.write_text(json.dumps(dump, indent=2) + "\n")
    OUT_MD.write_text(write_markdown(dump))
    print(f"wrote {OUT_JSON}", flush=True)
    print(f"wrote {OUT_MD}", flush=True)
    print(f"verdict={verdict} wall={wall:.3f}s", flush=True)
    print(f"reason: {kill_reason}", flush=True)
    print(f"L4 by w: {[(r['w'], r['L_run'], r['tcap']) for r in rows4]}", flush=True)
    print(f"L5 by w: {[(r['w'], r['L_run'], r['tcap']) for r in rows5]}", flush=True)
    print(
        f"n_cap4={sum(r['n_cap_survivors'] for r in rows4)} "
        f"genuine4={len(p4['genuine_eventual_witnesses'])} "
        f"n_cap5={sum(r['n_cap_survivors'] for r in rows5)} "
        f"genuine5={len(p5['genuine_eventual_witnesses'])}",
        flush=True,
    )
    return dump


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--certify", action="store_true")
    p.add_argument("--w-max", type=int, default=7)
    args = p.parse_args()
    if not args.certify:
        p.error("pass --certify")
    if args.w_max < 0 or args.w_max > 12:
        p.error("--w-max must be in 0..12")
    certify(args.w_max)


if __name__ == "__main__":
    main()
