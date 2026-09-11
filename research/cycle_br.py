#!/usr/bin/env python3
"""Cycle BR: packed bits p<=2U+1 are silent on covering blocks B and C.

The Green cone is t <= (T+p-2)/2. On B=[6U,10U)->10U and
C=[10U,18U)->18U this forces p<=2U+1 to have zero hits for every
k>=1, strengthening Cycle BQ (the p=1 case). Packed bit p=2U+2 is
unique-Green on each block: at t=6U on B and at t=10U on C, both
G(m,2m)=1. That unique AND takes both firing values, so it is not
a 1-production for S_B or S_C.

Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_br.py --certify
Dump: research/cycle_br.json
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


def t_max(T: int, p: int) -> int:
    return (T + p - 2) // 2


def cone_ok(tmax: int, pmax: int) -> bool:
    for T in range(2, tmax + 1):
        for p in range(1, min(pmax, 2 * T) + 1):
            lim = t_max(T, p)
            for t in range(1, T):
                if G(T - t - 1, T - p) and t > lim:
                    return False
    return True


def silence_ineq_ok(kmax: int) -> bool:
    for k in range(1, kmax + 1):
        U = 1 << k
        if t_max(10 * U, 2 * U + 1) >= 6 * U:
            return False
        if t_max(18 * U, 2 * U + 1) >= 10 * U:
            return False
        if t_max(10 * U, 2 * U + 2) < 6 * U:
            return False
        if t_max(18 * U, 2 * U + 2) < 10 * U:
            return False
    return True


def unique_2U2_ok(kmax: int) -> bool:
    for k in range(1, kmax + 1):
        U = 1 << k
        p = 2 * U + 2
        if G(4 * U - 1, 8 * U - 2) != 1:
            return False
        if G(8 * U - 1, 16 * U - 2) != 1:
            return False
        hits_b = [t for t in range(6 * U, 10 * U) if G(10 * U - t - 1, 10 * U - p)]
        hits_c = [t for t in range(10 * U, 18 * U) if G(18 * U - t - 1, 18 * U - p)]
        if hits_b != [6 * U] or hits_c != [10 * U]:
            return False
    return True


def fires(row: int, p: int) -> int:
    return ((row >> p) & 1) & ((row >> (p - 1)) & 1)


def firing_samples(kmax: int) -> dict:
    tmax = 10 * (1 << kmax) + 2
    need = set()
    for k in range(1, kmax + 1):
        U = 1 << k
        need.add(6 * U)
        need.add(10 * U)
    row = 1
    samp: dict[int, int] = {}
    for t in range(tmax + 1):
        if t in need:
            samp[t] = row
        row = rule30_step(row)
    f6, f10, eq = [], [], []
    for k in range(1, kmax + 1):
        U = 1 << k
        p = 2 * U + 2
        a = fires(samp[6 * U], p)
        b = fires(samp[10 * U], p)
        f6.append(a)
        f10.append(b)
        eq.append(int(a == b))
    return {"f6": f6, "f10": f10, "eq": eq, "both": set(f6) == {0, 1}}


def self_checks(c20, cone: bool, sil: bool, uniq: bool, fir: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cone and sil and uniq
    assert fir["both"]
    assert 0 in fir["f6"] and 1 in fir["f6"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cone = cone_ok(24, 8)
    sil = silence_ineq_ok(12)
    uniq = unique_2U2_ok(6)
    fir = firing_samples(8)
    checks = self_checks(c20, cone, sil, uniq, fir)
    dump = {
        "cycle": "BR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "firing": fir,
        "lemmas": {
            "general_cone": True,
            "low_bits_silent_B_C": True,
            "p_2U2_unique_on_B": True,
            "p_2U2_unique_on_C": True,
            "p_2U2_identically_fires": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "general_cone": "LEMMA",
            "low_bits_silent_B_C": "LEMMA",
            "p_2U2_unique_on_B": "LEMMA",
            "p_2U2_unique_on_C": "LEMMA",
            "p_2U2_identically_fires": "KILLED",
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
    print("firing", fir)


if __name__ == "__main__":
    main()
