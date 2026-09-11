#!/usr/bin/env python3
"""Cycle AW: exactly two double-Green bits for I_k.

For a>=4 there are no even half-window doubles. Odd doubling then
propagates the a=4 pair, so |S(a,D)|=2 iff D is 2^{a-2}-1 or
3*2^{a-3}-1. Unique-Green bits were classified in Cycle AV; the
double-Green packed bits for I_k are therefore exactly p=3T/2+1 and
p=5T/8+1. All left-diagonals eventually period 4 is killed (e_29).
Packed bit 33 firing at every T is a prefix, not a theorem.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_aw.py --certify
Dump: research/cycle_aw.json
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


def e_bit(row: int, j: int) -> int:
    return (row >> j) & 1


def support(a: int, D: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    return [n for n in range(nmax + 1) if G(n, D)]


def expected_double_D(a: int) -> list[int]:
    return sorted([(1 << (a - 2)) - 1, 3 * (1 << (a - 3)) - 1])


def no_even_doubles_ok(amax: int) -> bool:
    for a in range(4, amax + 1):
        nmax = (1 << (a - 1)) - 1
        for E in range(0, 2 * nmax + 1, 2):
            if len(support(a, E)) == 2:
                return False
    return True


def double_D_ok(amax: int) -> bool:
    for a in range(4, amax + 1):
        nmax = (1 << (a - 1)) - 1
        want = set(expected_double_D(a))
        got = {D for D in range(0, 2 * nmax + 1) if len(support(a, D)) == 2}
        if got != want:
            return False
    return True


def mersenne_double_ok(amax: int) -> bool:
    """S(a, 2^{a-2}-1) = {2^{a-2}-1, 2^{a-1}-1}."""
    for a in range(2, amax + 1):
        D = (1 << (a - 2)) - 1
        want = [(1 << (a - 2)) - 1, (1 << (a - 1)) - 1]
        if support(a, D) != want:
            return False
    return True


def five_double_ok(amax: int) -> bool:
    """S(a, 3*2^{a-3}-1) = {3*2^{a-3}-1, 2^{a-2}-1} for a>=4."""
    if support(3, 2) != [1, 2]:
        return False
    for a in range(4, amax + 1):
        D = 3 * (1 << (a - 3)) - 1
        want = sorted([3 * (1 << (a - 3)) - 1, (1 << (a - 2)) - 1])
        if support(a, D) != want:
            return False
    return True


def even_blockers_ok(amax: int) -> bool:
    """The two even-|S|=2 mechanisms fail for a>=5.

    Case (i): leftmost unique e=2^{a-2}-1 has e-1=2^{a-2}-2 nonempty
    (contains the cone G(m,2m)=1 at m=2^{a-3}-1).
    Case (ii): lifting either double, the central G(e,e)=1 lies off
    that double's support.
    """
    for a in range(5, amax + 1):
        c = a - 1
        # case (i)
        D = (1 << (c - 1)) - 2
        cone = (1 << (c - 2)) - 1
        if G(cone, 2 * cone) != 1:
            return False
        if cone not in support(c, D):
            return False
        # case (ii), Mersenne double
        e = 1 << (c - 2)
        B = set(support(c, (1 << (c - 2)) - 1))
        if G(e, e) != 1 or e in B:
            return False
        # case (ii), 5-double
        e2 = 3 * (1 << (c - 3))
        B2 = set(support(c, 3 * (1 << (c - 3)) - 1))
        if G(e2, e2) != 1 or e2 in B2:
            return False
    return True


def expected_double_p(k: int) -> list[int]:
    return sorted([3 * (1 << (k - 2)) + 1, 5 * (1 << (k - 3)) + 1])


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
    dbl = sorted(p for p, ts in by_p.items() if len(ts) == 2)
    times = {p: by_p[p] for p in dbl}
    return {"T": T, "n2": len(dbl), "doubles": dbl, "times": times}


def family_times_ok(k: int, cen: dict) -> bool:
    T = cen["T"]
    p3 = 3 * (1 << (k - 2)) + 1
    p5 = 5 * (1 << (k - 3)) + 1
    if cen["times"].get(p3) != [T, 3 * T // 2]:
        return False
    if cen["times"].get(p5) != [5 * T // 4, 3 * T // 2]:
        return False
    return True


def e29_not_period4(rows: list[int], tmax: int) -> bool:
    """e_29 fails period 4 on t>=64, and matches period 8 there."""
    start = 64
    if start + 16 >= tmax:
        return False
    seq = [e_bit(rows[t], 29) for t in range(start, start + 16)]
    if seq == seq[:4] * 4:
        return False
    if not all(e_bit(rows[t], 29) == e_bit(rows[t + 8], 29)
               for t in range(start, tmax - 8)):
        return False
    return True


def bit33_prefix(rows: list[int], kmax: int) -> list[int]:
    out = []
    for k in range(7, kmax + 1):
        T = 1 << (k - 1)
        out.append(fires(rows[T], 33))
    return out


def self_checks(
    c20,
    no_even: bool,
    dD: bool,
    mer: bool,
    five: bool,
    blockers: bool,
    recs: list[dict],
    e29: bool,
    b33: list[int],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert no_even and dD and mer and five and blockers
    for rec in recs:
        assert rec["n2"] == 2
        assert rec["doubles"] == rec["expected"]
        assert rec["family_times"]
    assert e29
    assert b33 and all(x == 1 for x in b33)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    no_even = no_even_doubles_ok(12)
    dD = double_D_ok(12)
    mer = mersenne_double_ok(12)
    five = five_double_ok(12)
    blockers = even_blockers_ok(12)

    k_ann = 8
    k33 = 12
    rows = evolve_rows(max(1 << k_ann, 1 << (k33 - 1), 512))
    recs = []
    for k in range(4, k_ann + 1):
        cen = hit_census(k)
        recs.append({
            "k": k,
            "T": cen["T"],
            "n2": cen["n2"],
            "doubles": cen["doubles"],
            "expected": expected_double_p(k),
            "family_times": family_times_ok(k, cen),
        })
    e29 = e29_not_period4(rows, min(len(rows) - 1, 512))
    b33 = bit33_prefix(rows, k33)
    checks = self_checks(
        c20, no_even, dD, mer, five, blockers, recs, e29, b33,
    )
    dump = {
        "cycle": "AW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "no_even_doubles": no_even,
            "double_D": dD,
            "mersenne_double": mer,
            "five_double": five,
            "even_blockers": blockers,
            "e29_not_period4": e29,
        },
        "annulus": recs,
        "bit33_fires_k7_to_12": b33,
        "lemmas": {
            "no_even_doubles_a_ge_4": True,
            "double_D_exactly_two": True,
            "exactly_two_double_Green_bits": True,
            "all_e_j_period4": False,
            "bit33_always_fires": None,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "no_even_doubles_a_ge_4": "LEMMA",
            "double_D_exactly_two": "LEMMA",
            "exactly_two_double_Green_bits": "LEMMA",
            "all_e_j_period4": "KILLED",
            "bit33_always_fires": "PREFIX",
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
        {key: rec[key] for key in ("k", "T", "n2", "doubles", "family_times")}
        for rec in recs
    ])
    print("bit33", b33)


if __name__ == "__main__":
    main()
