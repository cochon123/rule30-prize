#!/usr/bin/env python3
"""Cycle AZ: five quads; e_19; bit 19 contributes 1; I_k = B^{>=20}.

For a>=6 there are no even half-window quads, so the five quads are
the odd-lift orbit of a=5's packed bits {18,19,23,27,29}. Packed bit
19 is the j=1 member of the 9-family (a triple for k>=6). With the
period-4 tail of e_19, it contributes 1, so I_k = B_k^{>=20} for
k>=6. Nested depth 19 is not a closed form. Quad XOR is not I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_az.py --certify
Dump: research/cycle_az.json
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
SEEDS = [18, 19, 23, 27, 29]


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


def no_even_quads_ok(amax: int) -> bool:
    for a in range(6, amax + 1):
        nmax = (1 << (a - 1)) - 1
        for E in range(0, 2 * nmax + 1, 2):
            if len(support(a, E)) == 4:
                return False
    return True


def odd_lifts_ok(amax: int) -> bool:
    for a in range(6, amax + 1):
        prev_max = (1 << (a - 2)) - 1
        prev = {D for D in range(0, 2 * prev_max + 1) if len(support(a - 1, D)) == 4}
        lifted = {2 * d + 1 for d in prev}
        nmax = (1 << (a - 1)) - 1
        got = {D for D in range(1, 2 * nmax + 1, 2) if len(support(a, D)) == 4}
        if got != lifted or len(got) != 5:
            return False
    return True


def a5_seeds_ok() -> bool:
    nmax = 15
    ps = sorted((1 << 5) - D for D in range(0, 2 * nmax + 1) if len(support(5, D)) == 4)
    return ps == SEEDS


def even_blockers_ok(cmax: int) -> bool:
    """Even |S|=4 mechanisms fail for a=c+1>=6."""
    for c in range(5, cmax + 1):
        # (i) e a double => B nonempty
        for e in ((1 << (c - 2)) - 1, 3 * (1 << (c - 3)) - 1):
            B = support(c, e - 1)
            if not B:
                return False
        # (ii) 5-double neighbour: |A\B| >= 2
        e = 3 * (1 << (c - 3))
        B = set(support(c, e - 1))
        A = set(support(c, e))
        if len(A - B) < 2:
            return False
        # Mersenne-double neighbour sits in the W=1 interval (odd |S|)
        e2 = 1 << (c - 2)
        D = 2 * e2  # at level c+1 this is 2^{c}
        # checked globally via no_even_quads; here G(e2,e2)=1 off the double
        B2 = set(support(c, (1 << (c - 2)) - 1))
        if G(e2, e2) != 1 or e2 in B2:
            return False
        # (iii) A not subset B for each quad at level c
        nmax = (1 << (c - 1)) - 1
        for D in range(0, 2 * nmax + 1):
            if len(support(c, D)) != 4:
                continue
            B = set(support(c, D))
            A = set(support(c, D + 1))
            if A <= B:
                return False
    return True


def expected_quad_p(k: int) -> list[int]:
    j = k - 5
    if j < 0:
        return []
    return sorted((1 << j) * (s - 1) + 1 for s in SEEDS)


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
    qd = sorted(p for p, ts in by_p.items() if len(ts) == 4)
    return {"T": T, "n4": len(qd), "quads": qd, "times": {p: by_p[p] for p in qd}}


def e19(t: int) -> int:
    return int(t % 4 in (2, 3))


def tails_ok(rows: list[int], tmax: int) -> bool:
    for t in range(20, tmax):
        if e_bit(rows[t], 19) != e19(t):
            return False
    for t in range(20, tmax - 1):
        e17 = int(t % 4 == 3)
        e18 = int(t % 4 in (1, 2))
        got = e_bit(rows[t + 1], 19)
        want = e17 ^ (e18 | e_bit(rows[t], 19))
        if got != want:
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


def self_checks(
    c20, no_even, lifts, seeds, blockers, tails, recs, mismatches,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert no_even and lifts and seeds and blockers and tails
    vals = []
    for rec in recs:
        assert rec["n4"] == 5
        assert rec["quads"] == rec["expected"]
        if rec["k"] >= 6:
            assert rec["t19"] == [rec["T"] + s for s in (2, 4, 8)]
            assert rec["fire19"] == [1, 0, 0] and rec["x19"] == 1
            assert rec["I"] == rec["B20"]
            vals.append(rec["B20"])
    assert mismatches
    assert 0 in vals and 1 in vals
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    no_even = no_even_quads_ok(12)
    lifts = odd_lifts_ok(12)
    seeds = a5_seeds_ok()
    blockers = even_blockers_ok(11)
    k_ann = 8
    rows = evolve_rows(1 << k_ann)
    tails = tails_ok(rows, min(len(rows) - 1, 256))
    recs = []
    mismatches = []
    for k in range(5, k_ann + 1):
        cen = hit_census(k)
        T = cen["T"]
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        qx = 0
        for p in cen["quads"]:
            qx ^= xor_fires(rows, p, cen["times"][p])
        if qx != I:
            mismatches.append(k)
        t19 = green_times(k, 19)
        f19 = [fires(rows[t], 19) for t in t19]
        x19 = xor_fires(rows, 19, t19)
        B20 = bulk_ge(rows, k, 20) if k >= 6 else None
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "n4": cen["n4"],
            "quads": cen["quads"],
            "expected": expected_quad_p(k),
            "quad_xor": qx,
            "t19": t19,
            "fire19": f19,
            "x19": x19,
            "B20": B20,
        })
    checks = self_checks(
        c20, no_even, lifts, seeds, blockers, tails, recs, mismatches,
    )
    dump = {
        "cycle": "AZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "no_even_quads": no_even,
            "odd_lifts": lifts,
            "a5_seeds": seeds,
            "even_blockers": blockers,
            "e19_tail": tails,
        },
        "annulus": recs,
        "quad_xor_mismatch_k": mismatches,
        "lemmas": {
            "no_even_quads_a_ge_6": True,
            "exactly_five_quads": True,
            "e19_period4": True,
            "bit19_contributes_1": True,
            "I_eq_B20": True,
            "nested19_is_I": False,
            "quad_xor_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "no_even_quads_a_ge_6": "LEMMA",
            "exactly_five_quads": "LEMMA",
            "e19_period4": "LEMMA",
            "bit19_contributes_1": "LEMMA",
            "I_eq_B20": "LEMMA",
            "nested19_is_I": "KILLED",
            "quad_xor_is_I": "KILLED",
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
        {key: rec[key] for key in rec if key not in ("t19",)}
        for rec in recs
    ])
    print("quad_xor_mismatch_k", mismatches)


if __name__ == "__main__":
    main()
