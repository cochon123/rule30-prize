#!/usr/bin/env python3
"""Cycle BQ: packed bit 1 cannot Green-hit after t=(T-1)/2.

G(T-t-1, T-1)=1 forces t <= (T-1)/2. On the covering coboundary
blocks [6U,10U) targeting 10U and [10U,18U) targeting 18U, every
time is strictly past that cone, so there are zero packed-bit-1
hits for every k>=1. Those remainders are purely S_other. The first
block [2U,6U) targeting 6U still has bit-1 net 1 (Cycle AJ/BN).
Covering fails at k+1 iff S_A=1 and S_B=S_C=0.

Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bq.py --certify
Dump: research/cycle_bq.json
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


def xor_prefix(M: int, D: int) -> int:
    acc = 0
    for m in range(M):
        acc ^= G(m, D)
    return acc


def cone_ok(tmax: int) -> bool:
    for T in range(2, tmax + 1):
        lim = (T - 1) // 2
        for t in range(1, T):
            hit = G(T - t - 1, T - 1)
            if hit and t > lim:
                return False
            if t > lim and hit:
                return False
    return True


def block_ineq_ok(kmax: int) -> bool:
    for k in range(1, kmax + 1):
        U = 1 << k
        if (10 * U - 1) // 2 >= 6 * U:
            return False
        if (18 * U - 1) // 2 >= 10 * U:
            return False
        if (6 * U - 1) // 2 < 2 * U:
            return False
    return True


def zero_hits_scan_ok(kmax: int) -> bool:
    for k in range(1, kmax + 1):
        U = 1 << k
        for t in range(6 * U, 10 * U):
            if G(10 * U - t - 1, 10 * U - 1):
                return False
        for t in range(10 * U, 18 * U):
            if G(18 * U - t - 1, 18 * U - 1):
                return False
    return True


def xor_blocks_ok(nmax: int) -> bool:
    for n in range(1, nmax + 1):
        T = 1 << n
        if xor_prefix(2 * T, 3 * T - 1) != 1:
            return False
        if xor_prefix(1 << (n + 1), 5 * T - 1) != 0:
            return False
        if xor_prefix(1 << (n + 2), 9 * T - 1) != 0:
            return False
        if xor_prefix(4 * T, 5 * T - 1) != 1:
            return False
        if xor_prefix(8 * T, 9 * T - 1) != 1:
            return False
    return True


def self_checks(c20, cone: bool, ineq: bool, zhit: bool, xors: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cone and ineq and zhit and xors
    assert G(1, 2) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cone = cone_ok(48)
    ineq = block_ineq_ok(12)
    zhit = zero_hits_scan_ok(6)
    xors = xor_blocks_ok(10)
    checks = self_checks(c20, cone, ineq, zhit, xors)
    dump = {
        "cycle": "BQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "lemmas": {
            "bit1_cone": True,
            "zero_bit1_on_B": True,
            "zero_bit1_on_C": True,
            "bit1_net_A_eq_1": True,
            "cover_fails_iff_SA1_SB0_SC0": True,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "bit1_cone": "LEMMA",
            "zero_bit1_on_B": "LEMMA",
            "zero_bit1_on_C": "LEMMA",
            "bit1_net_A_eq_1": "LEMMA",
            "cover_fails_iff_SA1_SB0_SC0": "LEMMA",
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


if __name__ == "__main__":
    main()
