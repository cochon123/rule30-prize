#!/usr/bin/env python3
"""Cycle BD: period-8 tails e_29..e_33; bit 33 contributes 1.

Cycle BA closed e_20..e_27 as period 4, e_28=0, and e_30=1 for t>=33.
The recurrence then forces period-8 tails for e_29, e_31, e_32, e_33.
The AND at packed bit 33 fires iff t≡0 mod 8, and T=2^{k-1}≡0 mod 8
for k>=4, so bit 33 contributes 1 for every k>=7. This upgrades Cycle
AW's prefix. Nested left is still not a formula for I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_bd.py --certify
Dump: research/cycle_bd.json
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


def evolve_rows(tmax: int) -> list[int]:
    row = 1
    out = []
    for _ in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def fires(row: int, p: int) -> int:
    return (((row << 1) & row) >> p) & 1


def e_bit(row: int, j: int) -> int:
    return (row >> j) & 1


def e27(t: int) -> int:
    return int(t % 4 != 0)


def e29(t: int) -> int:
    return int(t % 8 in (0, 1, 3, 6))


def e31(t: int) -> int:
    return int(t % 8 in (0, 3, 5, 6))


def e32(t: int) -> int:
    return int(t % 8 in (0, 2, 5))


def e33(t: int) -> int:
    return int(t % 8 in (0, 3, 7))


def invariance_ok() -> bool:
    """Period-8 candidates are invariant given e_27 period 4, e_28=0, e_30=1."""
    for r in range(8):
        # e29(t+1) = e27(t) XOR e29(t)
        if e29((r + 1) % 8) != (e27(r) ^ e29(r)):
            return False
        # e31(t+1) = e29(t) XOR 1
        if e31((r + 1) % 8) != (e29(r) ^ 1):
            return False
        # e32(t+1) = 1 XOR (e31(t) OR e32(t))
        if e32((r + 1) % 8) != (1 ^ (e31(r) | e32(r))):
            return False
        # e33(t+1) = e31(t) XOR (e32(t) OR e33(t))
        if e33((r + 1) % 8) != (e31(r) ^ (e32(r) | e33(r))):
            return False
        # AND 33 empty except r=0
        and33 = e33(r) & e32(r)
        if and33 != int(r == 0):
            return False
    return True


def tails_ok(rows: list[int], tmax: int) -> bool:
    starts = {29: 30, 31: 34, 32: 36, 33: 36}
    fns = {29: e29, 31: e31, 32: e32, 33: e33}
    for j, fn in fns.items():
        for t in range(starts[j], tmax):
            if e_bit(rows[t], j) != fn(t):
                return False
    for t in range(31, tmax):
        if e_bit(rows[t], 28) != 0:
            return False
    for t in range(33, tmax):
        if e_bit(rows[t], 30) != 1:
            return False
    for t in range(20, tmax - 1):
        for j in (29, 31, 32, 33):
            got = e_bit(rows[t + 1], j)
            want = e_bit(rows[t], j - 2) ^ (
                e_bit(rows[t], j - 1) | e_bit(rows[t], j)
            )
            if got != want:
                return False
    return True


def and33_ok(rows: list[int], tmax: int) -> bool:
    for t in range(36, tmax):
        if fires(rows[t], 33) != int(t % 8 == 0):
            return False
        if fires(rows[t], 29):
            return False
    return True


def unique_times_k(k: int, p: int) -> list[int]:
    """Unique 2-family p=2^j+1 is Green only at t=T."""
    T = 1 << (k - 1)
    end = 1 << k
    out = []
    for t in range(T, end):
        if p > 2 * t:
            continue
        if G(end - t - 1, end - p):
            out.append(t)
    return out


def self_checks(c20, inv, tails, ands, recs) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert inv and tails and ands
    vals = []
    for rec in recs:
        assert rec["t33"] == [rec["T"]]
        assert rec["x33"] == 1
        assert rec["T"] % 8 == 0
        vals.append(rec["I"])
    assert 0 in vals and 1 in vals
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    inv = invariance_ok()
    k_ann = 12
    rows = evolve_rows(1 << k_ann)
    tmax = min(len(rows) - 1, 512)
    tails = tails_ok(rows, tmax)
    ands = and33_ok(rows, tmax)
    recs = []
    for k in range(7, k_ann + 1):
        T = 1 << (k - 1)
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        t33 = unique_times_k(k, 33)
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "t33": t33,
            "fire33": [fires(rows[t], 33) for t in t33],
            "x33": fires(rows[T], 33),
        })
    checks = self_checks(c20, inv, tails, ands, recs)
    dump = {
        "cycle": "BD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "period8_invariance": inv,
            "e29_e33_tails": tails,
            "and33_only_mod8_0": ands,
        },
        "annulus": recs,
        "lemmas": {
            "e29_e33_period8": True,
            "bit33_contributes_1": True,
            "bit29_never_fires": True,
            "nested_left_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "e29_e33_period8": "LEMMA",
            "bit33_contributes_1": "LEMMA",
            "bit29_never_fires": "LEMMA",
            "nested_left_is_I": "KILLED",
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
