#!/usr/bin/env python3
"""Cycle BI: exactly four/three triple-Green bits on 5-fold/9-fold.

Cycle BH closed double-Green bits on the covering annuli. The same
C_le count, the diagonal pair {m, 2m}, and a complementary hit at
2m-2 or 2m-1 for every m>=8, force at least four Green hits in
[m, 2m] except m in {1,2,3,6}. Truncated windows then have C_le>=4
except two 5-fold M=1 slots and the three 9-fold M=0 Fermat-odd
targets. Full power-of-two windows have no extra even triples by
Cycle AX (only r=19 at 5-fold M=2 survives the r-bound). The
surviving triples are exactly four packed bits on the 5-fold annulus
and three on the 9-fold, for every k>=3, with closed times.

Not a prize claim: those triples are not identically-1 productions,
and the Fermat covering remains a prefix.

Run: python3 research/cycle_bi.py --certify
Dump: research/cycle_bi.json
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


@lru_cache(maxsize=None)
def G_support(m: int) -> frozenset[int]:
    if m == 0:
        return frozenset({0})
    if m % 2 == 0:
        return frozenset(2 * e for e in G_support(m // 2))
    S = G_support(m // 2)
    out = {2 * j + 1 for j in S}
    cands = S | {x + 1 for x in S}
    for j in cands:
        if j < 0:
            continue
        if (j in S) ^ ((j - 1) in S):
            d = 2 * j
            if 0 <= d <= 2 * m:
                out.add(d)
    return frozenset(out)


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


def census(k: int, q: int) -> dict[int, list[int]]:
    U = 1 << k
    target = q * U
    by_p: dict[int, list[int]] = defaultdict(list)
    for t in range(U, q * U):
        m = target - t - 1
        for d in G_support(m):
            p = target - d
            if 1 <= p <= 2 * t:
                by_p[p].append(t)
    return by_p


def N_ann(q: int, M: int, r: int) -> tuple[int, int, int]:
    a_off = {5: 2, 9: 3}[q]
    W = (1 << (M + a_off)) - 1
    ncone = (q * (1 << M) + r - 3) // 2
    return min(W, ncone), W, ncone


def C_le(N: int, d: int) -> int:
    if N < 0:
        return 0
    return sum(G(n, d) for n in range(N + 1))


def expected_triples(q: int, k: int) -> list[int]:
    U = 1 << k
    if q == 5:
        return sorted([(U >> 2) + 1, (U >> 1) + 1, 5 * (U >> 1) + 1, 7 * (U >> 1) + 1])
    return sorted([1, 2 * U + 1, 4 * U + 1])


def expected_times(q: int, k: int, p: int) -> list[int]:
    U = 1 << k
    if q == 5:
        table = {
            (U >> 2) + 1: [U, (9 * U) // 4, (5 * U) // 2],
            (U >> 1) + 1: [U, 2 * U, (5 * U) // 2],
            5 * (U >> 1) + 1: [2 * U, (5 * U) // 2, (7 * U) // 2],
            7 * (U >> 1) + 1: [2 * U, (7 * U) // 2, 4 * U],
        }
        return table[p]
    table = {
        1: [U, 3 * U, 4 * U],
        2 * U + 1: [2 * U, 3 * U, 5 * U],
        4 * U + 1: [3 * U, 4 * U, 6 * U],
    }
    return table[p]


def H(m: int) -> int:
    """# of G(.,2m)=1 hits in [m, 2m]."""
    return sum(G(n, 2 * m) for n in range(m, 2 * m + 1))


def interval_count_ok() -> bool:
    if H(1) != 2 or H(2) != 2:
        return False
    if H(3) != 3 or H(6) != 3:
        return False
    if [n for n in range(3, 7) if G(n, 6)] != [3, 5, 6]:
        return False
    if [n for n in range(6, 13) if G(n, 12)] != [6, 10, 12]:
        return False
    for m in (4, 5, 7):
        if H(m) < 4:
            return False
    return True


def complementary_ok(mmax: int) -> bool:
    """For m>=8, exactly one of 2m-2, 2m-1 is a hit, and n2 <= 2m-3."""
    for m in range(8, mmax + 1):
        a = G(2 * m - 1, 2 * m)
        b = G(2 * m - 2, 2 * m)
        if a + b != 1 or a == b:
            return False
        if G(m - 1, m - 1) != 1:
            return False
        if G(2 * m - 2, 2 * m) != G(m - 1, m):
            return False
        if G(2 * m - 1, 2 * m) != (G(m - 1, m) ^ 1):
            return False
        cap = 3 * m // 2 + 1
        if cap > 2 * m - 3 and m % 2 == 0:
            return False
        if m % 2 and (3 * m + 1) // 2 > 2 * m - 3:
            return False
        if H(m) < 4:
            return False
    return True


def ax_r_bound_ok() -> bool:
    """Even AX triples have r too large except 5-fold M=2, r=19."""
    # 5-fold N=W level a=M+3; even triples r = 2^a - {5,7,9,13}
    for M in range(2, 12):
        a = M + 3
        rs = [(1 << a) - q for q in (5, 7, 9, 13)]
        rmax = 5 * (1 << M)
        survivors = [r for r in rs if r <= rmax]
        if M == 2 and survivors != [19]:
            return False
        if M >= 3 and survivors:
            return False
    # 9-fold level a=M+4
    for M in range(1, 10):
        a = M + 4
        rs = [(1 << a) - q for q in (5, 7, 9, 13)]
        rmax = 9 * (1 << M)
        if any(r <= rmax for r in rs):
            return False
    return True


def C_le_triples_Mge0(q: int, Mmax: int) -> list[tuple[int, int]]:
    found = []
    rmax_base = {5: 5, 9: 9}[q]
    for M in range(0, Mmax + 1):
        for r in range(1, rmax_base * (1 << M) + 1, 2):
            N, _W, _nc = N_ann(q, M, r)
            if N < 0:
                continue
            if C_le(N, r - 1) == 3:
                found.append((M, r))
    return found


def r1_surviving(q: int, k: int, j: int) -> int:
    U = 1 << k
    if j < 0:
        return 0
    p = q * U + 1 - (1 << j)
    if p < 1:
        return 0
    W = ((q - 1) << k) // (1 << j) - 1
    if W < 0:
        return 0
    nmax = (q * U + (1 << j) - 1) // (1 << (j + 1))
    last = min(W, nmax - 1)
    return max(0, last + 1)


def lift_count(q: int, k: int, r: int, j: int) -> int:
    U = 1 << k
    p = q * U + 1 - r * (1 << j)
    if p < 1:
        return 0
    W = ((q - 1) << k) // (1 << j) - 1
    if W < 0:
        return 0
    nmax = (q * U + r * (1 << j) - 1) // (1 << (j + 1))
    N = min(W, nmax - 1)
    return C_le(N, r - 1)


def negative_M_triples_ok() -> bool:
    for k in range(3, 8):
        for j in range(k + 1, k + 5):
            if r1_surviving(5, k, j) == 3:
                return False
            if r1_surviving(9, k, j) == 3:
                return False
        if lift_count(5, k, 3, k + 1) != 0:
            return False
        if lift_count(9, k, 3, k + 1) != 2:
            return False
        if lift_count(9, k, 5, k + 1) != 0:
            return False
    return True


def a4_even_triples_ok() -> bool:
    """S(4, even D) has |S|=3 iff D in {8,10}; only D=8 meets 5-fold M=1 r<=10."""
    found = []
    for D in range(0, 15, 2):
        if sum(G(n, D) for n in range(8)) == 3:
            found.append(D)
    return found == [8, 10]


def firing_xor_ok(kmax: int) -> dict:
    rows = evolve_rows(9 * (1 << kmax))
    xor5, xor9, phi5, phi9 = [], [], [], []
    for k in range(3, kmax + 1):
        U = 1 << k
        x5 = 0
        for p in expected_triples(5, k):
            for t in expected_times(5, k, p):
                x5 ^= fires(rows[t], p)
        x9 = 0
        for p in expected_triples(9, k):
            for t in expected_times(9, k, p):
                x9 ^= fires(rows[t], p)
        c = lambda t: (rows[t] >> t) & 1
        xor5.append(x5)
        xor9.append(x9)
        phi5.append(c(5 * U) ^ c(U))
        phi9.append(c(9 * U) ^ c(U))
    return {
        "xor5": xor5,
        "xor9": xor9,
        "phi5": phi5,
        "phi9": phi9,
        "xor5_both": set(xor5) == {0, 1},
        "xor9_both": set(xor9) == {0, 1},
        "xor5_is_phi": xor5 == phi5,
        "xor9_is_phi": xor9 == phi9,
    }


def self_checks(
    c20,
    interval: bool,
    comp: bool,
    axr: bool,
    a4: bool,
    found5: list,
    found9: list,
    negM: bool,
    recs: list[dict],
    fire: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert interval and comp and axr and a4 and negM
    assert found5 == [(1, 3), (1, 5), (1, 9), (2, 19)]
    assert found9 == [(0, 5), (0, 7), (0, 9)]
    for rec in recs:
        k = rec["k"]
        assert rec["tri_q5"] == expected_triples(5, k)
        assert rec["tri_q9"] == expected_triples(9, k)
        assert rec["times5_ok"] and rec["times9_ok"]
    assert fire["xor5_both"] and fire["xor9_both"]
    assert not fire["xor5_is_phi"] and not fire["xor9_is_phi"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    interval = interval_count_ok()
    comp = complementary_ok(64)
    axr = ax_r_bound_ok()
    a4 = a4_even_triples_ok()
    found5 = C_le_triples_Mge0(5, 8)
    found9 = C_le_triples_Mge0(9, 7)
    negM = negative_M_triples_ok()
    recs = []
    for k in range(3, 8):
        by5 = census(k, 5)
        by9 = census(k, 9)
        tri5 = sorted(p for p, ts in by5.items() if len(ts) == 3)
        tri9 = sorted(p for p, ts in by9.items() if len(ts) == 3)
        times5_ok = all(by5[p] == expected_times(5, k, p) for p in tri5)
        times9_ok = all(by9[p] == expected_times(9, k, p) for p in tri9)
        recs.append({
            "k": k,
            "tri_q5": tri5,
            "tri_q9": tri9,
            "times5_ok": times5_ok,
            "times9_ok": times9_ok,
        })
    fire = firing_xor_ok(8)
    checks = self_checks(
        c20, interval, comp, axr, a4, found5, found9, negM, recs, fire
    )
    dump = {
        "cycle": "BI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": recs,
        "C_le_eq3_Mge0": {"q5": found5, "q9": found9},
        "firing": {
            "xor5": fire["xor5"],
            "xor9": fire["xor9"],
            "phi5": fire["phi5"],
            "phi9": fire["phi9"],
        },
        "lemmas": {
            "interval_H_m": True,
            "complementary_2m": True,
            "exactly_four_triples_q5": True,
            "exactly_three_triples_q9": True,
            "triples_always_fire": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "interval_H_m": "LEMMA",
            "complementary_2m": "LEMMA",
            "exactly_four_triples_q5": "LEMMA",
            "exactly_three_triples_q9": "LEMMA",
            "triples_always_fire": "KILLED",
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
    print("annulus", recs)
    print("C_le==3", dump["C_le_eq3_Mge0"])


if __name__ == "__main__":
    main()
