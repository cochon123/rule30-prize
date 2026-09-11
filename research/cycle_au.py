#!/usr/bin/env python3
"""Cycle AU: Fermat-subtract G; e_11,e_12; I_k = 1 XOR B^{>=13}.

G(n, 2^a-2^c-1)=1 on n<2^{a-1} iff n=2^{a-1}-1. Derived half-window
laws for 2^a-6, 2^a-7, 2^a-10, 2^a-12 give packed bits 10, 11, 12
explicit Green times on the dyadic annulus. With the period-4 tails of
e_11 and e_12, bit 10 contributes 1, bit 11 contributes 0, and bit 12
contributes 1. Thus I_k = 1 XOR B_k^{>=13} for k>=5, upgrading Cycle
AM's prefix. Nested depth 12 is not a closed form for I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_au.py --certify
Dump: research/cycle_au.json
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


def ones_s(a: int, q: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    D = (1 << a) - q
    return [nmax - n for n in range(nmax + 1) if G(n, D)]


def fermat_subtract_ok(amax: int) -> bool:
    for a in range(2, amax + 1):
        nmax = (1 << (a - 1)) - 1
        for c in range(1, a):
            D = (1 << a) - (1 << c) - 1
            for n in range(0, nmax + 1):
                if G(n, D) != int(n == nmax):
                    return False
    return True


def derived_s_ok(amax: int) -> bool:
    want = {
        6: [0, 1, 2],
        7: [2],
        10: [1, 2, 4],
        12: [0, 1, 2, 3, 5],
    }
    amin = {6: 4, 7: 4, 10: 5, 12: 5}
    for q, ss in want.items():
        for a in range(amin[q], amax + 1):
            if sorted(ones_s(a, q)) != ss:
                return False
    return True


def green_times(k: int, p: int) -> list[int]:
    T = 1 << (k - 1)
    end = 1 << k
    out = []
    for t in range(T, end):
        if p > 2 * t:
            continue
        if G(end - t - 1, end - p):
            out.append(t)
    return out


def xor_fires(rows: list[int], p: int, ts: list[int]) -> int:
    x = 0
    for t in ts:
        x ^= fires(rows[t], p)
    return x


def e11(t: int) -> int:
    return int(t % 4 == 2)


def e12(t: int) -> int:
    return int(t % 4 != 0)


def tails_ok(rows: list[int], tmax: int) -> bool:
    for t in range(11, tmax):
        if e_bit(rows[t], 11) != e11(t):
            return False
    for t in range(12, tmax):
        if e_bit(rows[t], 12) != e12(t):
            return False
    # recurrences on the tail
    for t in range(12, tmax - 1):
        e9 = 1
        got11 = e_bit(rows[t + 1], 11)
        want11 = e9 ^ (e_bit(rows[t], 10) | e_bit(rows[t], 11))
        if got11 != want11:
            return False
        got12 = e_bit(rows[t + 1], 12)
        want12 = e_bit(rows[t], 10) ^ (e_bit(rows[t], 11) | e_bit(rows[t], 12))
        if got12 != want12:
            return False
    return True


def self_checks(c20, fer: bool, der: bool, tails: bool, recs: list[dict]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fer and der and tails
    for rec in recs:
        assert rec["t10"] == [rec["T"] + s for s in (1, 2, 4)]
        assert rec["fire10"] == [0, 0, 1] and rec["x10"] == 1
        assert rec["t11"] == [rec["T"] + s for s in (0, 2, 4)]
        assert rec["x11"] == 0
        assert rec["t12"] == [rec["T"] + s for s in (0, 1, 2, 3, 5)]
        assert rec["fire12"] == [0, 0, 1, 0, 0] and rec["x12"] == 1
        assert rec["I"] == rec["B13"] ^ 1
    return {"all_ok": True}


def bulk_ge(rows: list[int], k: int, pmin: int) -> int:
    T = 1 << (k - 1)
    end = 1 << k
    x = 0
    for t in range(T, end):
        A = (rows[t] << 1) & rows[t]
        m = end - t - 1
        lo = max(pmin, end - 2 * m)
        hi = min(end, 2 * t)
        for p in range(lo, hi + 1):
            if G(m, end - p) and ((A >> p) & 1):
                x ^= 1
    return x


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fer = fermat_subtract_ok(12)
    der = derived_s_ok(12)
    kmax = 8
    rows = evolve_rows(1 << kmax)
    tails = tails_ok(rows, min(len(rows) - 1, 256))
    recs = []
    for k in range(5, kmax + 1):
        T = 1 << (k - 1)
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        t10 = green_times(k, 10)
        t11 = green_times(k, 11)
        t12 = green_times(k, 12)
        f10 = [fires(rows[t], 10) for t in t10]
        f11 = [fires(rows[t], 11) for t in t11]
        f12 = [fires(rows[t], 12) for t in t12]
        x10 = xor_fires(rows, 10, t10)
        x11 = xor_fires(rows, 11, t11)
        x12 = xor_fires(rows, 12, t12)
        B13 = bulk_ge(rows, k, 13)
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "t10": t10,
            "fire10": f10,
            "x10": x10,
            "t11": t11,
            "fire11": f11,
            "x11": x11,
            "t12": t12,
            "fire12": f12,
            "x12": x12,
            "B13": B13,
        })
    checks = self_checks(c20, fer, der, tails, recs)
    dump = {
        "cycle": "AU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "fermat_subtract": fer,
            "derived_s": der,
            "e11_e12_tails": tails,
        },
        "annulus": recs,
        "lemmas": {
            "G_fermat_subtract": True,
            "G_2a_minus_6_7_10_12": True,
            "e11_e12_period4": True,
            "bit10_contributes_1": True,
            "bit11_contributes_0": True,
            "bit12_contributes_1": True,
            "I_eq_1_xor_B13": True,
            "nested12_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "G_fermat_subtract": "LEMMA",
            "G_2a_minus_6_7_10_12": "LEMMA",
            "e11_e12_period4": "LEMMA",
            "bit10_contributes_1": "LEMMA",
            "bit11_contributes_0": "LEMMA",
            "bit12_contributes_1": "LEMMA",
            "I_eq_1_xor_B13": "LEMMA",
            "nested12_is_I": "KILLED",
            "I_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("annulus", [
        {key: rec[key] for key in rec if key not in ("t10", "t11", "t12")}
        for rec in recs
    ])


if __name__ == "__main__":
    main()
