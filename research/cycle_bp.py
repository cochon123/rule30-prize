#!/usr/bin/env python3
"""Cycle BP: 9-fold unique bit p=5U+1 fires; gamma identically 0 is killed.

Cycle BF: packed bit p=5U+1 is unique-Green on the 9-fold annulus and
fires iff gamma_k := c_{5U} and r_{5U}. That AND vanished on 3<=k<=12,
a prefix not a theorem. Direct packed samples give gamma_13=gamma_14=1
and gamma_15=0. So c_{5·2^k} and r_{5·2^k} is not identically 0, and
the 9-fold unique XOR is not identically alpha_k.

Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bp.py --certify
Dump: research/cycle_bp.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def spatial(row: int, t: int, j: int) -> int:
    if abs(j) > t:
        return 0
    return (row >> (j + t)) & 1


def samples(kmax: int) -> dict[int, tuple[int, int, int]]:
    tmax = 5 * (1 << kmax) + 2
    need = set()
    for k in range(1, kmax + 1):
        U = 1 << k
        need.update((U, 5 * U, 5 * U + 1))
    row = 1
    out: dict[int, tuple[int, int, int]] = {}
    for t in range(tmax + 1):
        if t in need:
            out[t] = ((row >> t) & 1, spatial(row, t, 1), spatial(row, t, -1))
        row = rule30_step(row)
    return out


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def self_checks(c20, gamma: list[int], alpha: list[int]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gamma[:11] == [0] * 11  # k=2..12
    assert gamma[11] == 1  # k=13
    assert gamma[12] == 1  # k=14
    assert gamma[13] == 0  # k=15
    assert set(gamma) == {0, 1}
    assert set(alpha) == {0, 1}
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    kmax = 15
    c20 = packed_center_bits(20)
    samp = samples(kmax)
    ks = list(range(2, kmax + 1))
    gamma = []
    alpha = []
    c5 = []
    r5 = []
    for k in ks:
        U = 1 << k
        cu, ru, _ = samp[U]
        c5u, r5u, _ = samp[5 * U]
        alpha.append(cu & ru)
        gamma.append(c5u & r5u)
        c5.append(c5u)
        r5.append(r5u)
    checks = self_checks(c20, gamma, alpha)
    dump = {
        "cycle": "BP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prefix": {
            "k": ks,
            "gamma": gamma,
            "alpha": alpha,
            "c5U": c5,
            "r5U": r5,
        },
        "lemmas": {
            "gamma_identically_0": False,
            "gamma_fires_k13_k14": True,
            "alpha_both_values": True,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "gamma_identically_0": "KILLED",
            "gamma_fires_k13_k14": "LEMMA",
            "alpha_both_values": "LEMMA",
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
    print("gamma", gamma)


if __name__ == "__main__":
    main()
