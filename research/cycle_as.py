#!/usr/bin/env python3
"""Cycle AS: half-window G(n, 2^a-2) and G(n, 2^a-4); dyadic unique bits.

On n < 2^{a-1}, G(n, 2^a-2)=1 iff n=2^{a-1}-1. For a>=3, G(n, 2^a-4)=1
iff n=2^{a-1}-2. The Green lift then makes every packed bit p=2^j+1
unique-Green for I_k at time T=2^{k-1}, and every p=3*2^j+1 with
j<=k-3 unique-Green at time T+2^j. The two double-Green bits are
p=5*2^{k-3}+1 and p=3*2^{k-2}+1. Packed bit 9 always fires at T.
The XOR of unique firings is not I_k. Exhaustiveness is a prefix.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_as.py --certify
Dump: research/cycle_as.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
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


def center_bit(row: int, t: int) -> int:
    return (row >> t) & 1


def half_window_ok(amax: int) -> bool:
    """G(n, 2^a-2), G(n, 2^a-3), G(n, 2^a-4) on n < 2^{a-1}."""
    for a in range(1, amax + 1):
        nmax = (1 << (a - 1)) - 1
        d2 = (1 << a) - 2
        for n in range(0, nmax + 1):
            if G(n, d2) != int(n == nmax):
                return False
        if a >= 2:
            d3 = (1 << a) - 3
            for n in range(0, nmax + 1):
                if G(n, d3) != int(n == nmax):
                    return False
        if a >= 3:
            d4 = (1 << a) - 4
            want = nmax - 1  # 2^{a-1}-2
            for n in range(0, nmax + 1):
                if G(n, d4) != int(n == want):
                    return False
    return True


def expected_unique(k: int) -> list[int]:
    twos = [(1 << j) + 1 for j in range(k)]
    threes = [3 * (1 << j) + 1 for j in range(k - 2)]
    return sorted(twos + threes)


def expected_doubles(k: int) -> list[int]:
    return sorted([5 * (1 << (k - 3)) + 1, 3 * (1 << (k - 2)) + 1])


def green_times_dyadic(k: int, p: int) -> list[int]:
    T = 1 << (k - 1)
    end = 1 << k
    out = []
    for t in range(T, end):
        if p > 2 * t:
            continue
        m = end - t - 1
        if G(m, end - p):
            out.append(t)
    return out


def hit_census(k: int) -> dict:
    T = 1 << (k - 1)
    end = 1 << k
    by_p: dict[int, list[int]] = defaultdict(list)
    for t in range(T, end):
        m = end - t - 1
        lo = max(0, end - 2 * m)
        hi = min(end, 2 * t)
        for p in range(lo, hi + 1):
            if G(m, end - p):
                by_p[p].append(t)
    uniq = sorted(p for p, ts in by_p.items() if len(ts) == 1)
    dbl = sorted(p for p, ts in by_p.items() if len(ts) == 2)
    return {
        "T": T,
        "n1": len(uniq),
        "n2": len(dbl),
        "uniq": uniq,
        "doubles": dbl,
        "times": {p: by_p[p] for p in uniq + dbl},
        "expected_uniq": expected_unique(k),
        "expected_doubles": expected_doubles(k),
    }


def family_times_ok(k: int, cen: dict) -> bool:
    T = cen["T"]
    ts = cen["times"]
    for j in range(k):
        p = (1 << j) + 1
        if ts.get(p) != [T]:
            return False
    for j in range(k - 2):
        p = 3 * (1 << j) + 1
        if ts.get(p) != [T + (1 << j)]:
            return False
    p3 = 3 * (1 << (k - 2)) + 1
    p5 = 5 * (1 << (k - 3)) + 1
    if ts.get(p3) != [T, 3 * T // 2]:
        return False
    if ts.get(p5) != [5 * T // 4, 3 * T // 2]:
        return False
    return True


def self_checks(c20, half: bool, recs: list[dict], p9: list[int], mismatches: list[int]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert half
    for rec in recs:
        k = rec["k"]
        assert rec["n1"] == 2 * k - 2
        assert rec["n2"] == 2
        assert rec["uniq"] == rec["expected_uniq"]
        assert rec["doubles"] == rec["expected_doubles"]
        assert rec["family_times"]
        assert rec["p9_fire"] == 1
        assert rec["p9_times"] == [rec["T"]]
    assert p9 == [1] * len(p9)
    assert mismatches, "unique XOR should fail as a formula for I_k"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    half = half_window_ok(12)
    kmax = 8
    rows = evolve_rows(1 << kmax)
    recs = []
    mismatches = []
    p9_fires = []
    for k in range(4, kmax + 1):
        cen = hit_census(k)
        T = cen["T"]
        end = 1 << k
        I = center_bit(rows[end], end) ^ center_bit(rows[T], T)
        ux = 0
        ufire = []
        for p in cen["uniq"]:
            t = cen["times"][p][0]
            f = fires(rows[t], p)
            ux ^= f
            if f:
                ufire.append(p)
        p9_fire = fires(rows[T], 9)
        p9_fires.append(p9_fire)
        if ux != I:
            mismatches.append(k)
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "n1": cen["n1"],
            "n2": cen["n2"],
            "uniq": cen["uniq"],
            "doubles": cen["doubles"],
            "expected_uniq": cen["expected_uniq"],
            "expected_doubles": cen["expected_doubles"],
            "family_times": family_times_ok(k, cen),
            "uniq_xor": ux,
            "uniq_that_fire": ufire,
            "p9_fire": p9_fire,
            "p9_times": green_times_dyadic(k, 9),
        })
    checks = self_checks(c20, half, recs, p9_fires, mismatches)
    dump = {
        "cycle": "AS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {"half_window": half},
        "annulus": [
            {
                key: rec[key]
                for key in (
                    "k", "T", "I", "n1", "n2", "uniq", "doubles",
                    "uniq_xor", "uniq_that_fire", "p9_fire",
                )
            }
            for rec in recs
        ],
        "uniq_xor_mismatch_k": mismatches,
        "lemmas": {
            "G_half_2a_minus_2": True,
            "G_half_2a_minus_3": True,
            "G_half_2a_minus_4": True,
            "unique_2_family": True,
            "unique_3_family": True,
            "two_double_bits": True,
            "bit9_always_fires": True,
            "exactly_2k_minus_2_unique_all_k": None,
            "exactly_two_doubles_all_k": None,
            "unique_xor_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "G_half_2a_minus_2": "LEMMA",
            "G_half_2a_minus_3": "LEMMA",
            "G_half_2a_minus_4": "LEMMA",
            "unique_2_family": "LEMMA",
            "unique_3_family": "LEMMA",
            "two_double_bits": "LEMMA",
            "bit9_always_fires": "LEMMA",
            "exactly_2k_minus_2_unique_all_k": "PREFIX",
            "exactly_two_doubles_all_k": "PREFIX",
            "unique_xor_is_I": "KILLED",
            "I_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("annulus", dump["annulus"])
    print("uniq_xor_mismatch_k", mismatches)


if __name__ == "__main__":
    main()
