#!/usr/bin/env python3
"""Cycle BS: four leftmost unique-Green bits on covering blocks B and C.

On B=[6U,10U)->10U (and C=[10U,18U)->18U) the cone allows s<(p-2U-2)/2
steps after the block start. For p=2U+2..2U+5 that forces uniqueness
after a one-line G evaluation: times 6U, 6U, 6U+1, 6U on B (and
10U, 10U, 10U+1, 10U on C). The XOR of those four firings takes both
values, so it is not a 1-production for S_B or S_C.

Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bs.py --certify
Dump: research/cycle_bs.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


@lru_cache(maxsize=None)
def G(m: int, d: int) -> int:
    if d < 0 or d > 2 * m:
        return 0
    if m == 0:
        return int(d == 0)
    if m % 2 == 0:
        if d % 2:
            return 0
        return G(m // 2, d // 2)
    n = m // 2
    if d % 2 == 0:
        return G(n, d // 2) ^ G(n, d // 2 - 1)
    return G(n, (d - 1) // 2)


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def G_m1_ok(mmax: int) -> bool:
    if G(0, 0) != 1:
        return False
    for m in range(0, mmax + 1):
        if G(m, 1) != (m & 1):
            return False
        if m >= 1 and G(m, 2 * m) != 1:
            return False
        if m >= 1 and G(m, 2 * m - 1) != (m & 1):
            return False
    return True


def vanish_2U4_ok(kmax: int) -> bool:
    for k in range(1, kmax + 1):
        U = 1 << k
        if G(4 * U - 1, 8 * U - 4) != 0:
            return False
        if G(4 * U - 2, 8 * U - 4) != 1:
            return False
        if G(8 * U - 1, 16 * U - 4) != 0:
            return False
        if G(8 * U - 2, 16 * U - 4) != 1:
            return False
    return True


def unique_scan_ok(kmax: int) -> bool:
    want_b = {2: 0, 3: 0, 4: 1, 5: 0}  # offset -> s
    want_c = {2: 0, 3: 0, 4: 1, 5: 0}
    for k in range(1, kmax + 1):
        U = 1 << k
        for dp, s in want_b.items():
            p = 2 * U + dp
            hits = [t for t in range(6 * U, 10 * U) if G(10 * U - t - 1, 10 * U - p)]
            if hits != [6 * U + s]:
                return False
        for dp, s in want_c.items():
            p = 2 * U + dp
            hits = [t for t in range(10 * U, 18 * U) if G(18 * U - t - 1, 18 * U - p)]
            if hits != [10 * U + s]:
                return False
    return True


def fires(row: int, p: int) -> int:
    return ((row >> p) & 1) & ((row >> (p - 1)) & 1)


def firing_xor(kmax: int) -> dict:
    tmax = 6 * (1 << kmax) + 4
    need: set[int] = set()
    for k in range(1, kmax + 1):
        U = 1 << k
        need.update((6 * U, 6 * U + 1))
    row = 1
    samp: dict[int, int] = {}
    for t in range(tmax + 1):
        if t in need:
            samp[t] = row
        row = rule30_step(row)
    xs = []
    rows = []
    for k in range(1, kmax + 1):
        U = 1 << k
        f2 = fires(samp[6 * U], 2 * U + 2)
        f3 = fires(samp[6 * U], 2 * U + 3)
        f5 = fires(samp[6 * U], 2 * U + 5)
        f4 = fires(samp[6 * U + 1], 2 * U + 4)
        x = f2 ^ f3 ^ f4 ^ f5
        xs.append(x)
        rows.append({"k": k, "f": [f2, f3, f4, f5], "xor": x})
    return {"xor": xs, "rows": rows, "both": set(xs) == {0, 1}}


def self_checks(c20, g1: bool, van: bool, uniq: bool, fir: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert g1 and van and uniq
    assert fir["both"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    g1 = G_m1_ok(64)
    van = vanish_2U4_ok(8)
    uniq = unique_scan_ok(5)
    fir = firing_xor(8)
    checks = self_checks(c20, g1, van, uniq, fir)
    dump = {
        "cycle": "BS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "firing": {"xor": fir["xor"], "rows": fir["rows"]},
        "lemmas": {
            "G_m_1_eq_m_mod_2": True,
            "four_left_unique_on_B": True,
            "four_left_unique_on_C": True,
            "unique4_xor_identically_1": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_m_1_eq_m_mod_2": "LEMMA",
            "four_left_unique_on_B": "LEMMA",
            "four_left_unique_on_C": "LEMMA",
            "unique4_xor_identically_1": "KILLED",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("xor", fir["xor"])


if __name__ == "__main__":
    main()
