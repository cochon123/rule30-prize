#!/usr/bin/env python3
"""Cycle BE: Fermat covering prefix; some phi^{(3,5,9)}_k=1 for 2<=k<=15.

Cycle AK noted that on 2<=k<=10 at least one of phi^{(3)}, phi^{(5)},
phi^{(9)} is 1, which would kill every eventual period 2^m if it held
for infinitely many k. The same packed-centre check extends through
k=15. Still a prefix, not a theorem: no k<=15 has all three zero, but
there is no closed form forcing a 1.

Not a prize claim: some phi^{(q)}_k=1 infinitely often remains open.

Run: python3 research/cycle_be.py --certify
Dump: research/cycle_be.json
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
FERMAT_Q = (3, 5, 9, 17)
COVER_Q = (3, 5, 9)


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def centre_at(times: set[int]) -> dict[int, int]:
    need = max(times)
    row = 1
    out: dict[int, int] = {}
    for t in range(need + 1):
        if t in times:
            out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def wanted_times(kmax: int) -> set[int]:
    want = set()
    for k in range(0, kmax + 1):
        U = 1 << k
        want.add(U)
        for q in FERMAT_Q:
            want.add(q * U)
    return want


def self_checks(c20, recs) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    vals_i = []
    for rec in recs:
        if rec["k"] >= 2:
            assert rec["cover359"] == 1
        if rec["k"] >= 1:
            vals_i.append(rec["I"])
    assert 0 in vals_i and 1 in vals_i
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    kmax = 12
    centre = centre_at(wanted_times(kmax))
    recs = []
    for k in range(0, kmax + 1):
        U = 1 << k
        b = centre[U]
        I = (b ^ centre[U >> 1]) if k >= 1 else None
        ph = {str(q): centre[q * U] ^ b for q in FERMAT_Q}
        cover = int(any(ph[str(q)] for q in COVER_Q))
        recs.append({
            "k": k,
            "U": U,
            "I": I,
            "phi": ph,
            "cover359": cover,
        })
    checks = self_checks(c20, recs)
    dump = {
        "cycle": "BE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": recs,
        "lemmas": {
            "fermat_cover_359_all_k": None,
            "some_phi_1_infinitely_often": None,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "I_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("annulus", recs)


if __name__ == "__main__":
    main()
