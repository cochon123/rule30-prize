#!/usr/bin/env python3
"""Cycle BJ: exactly two/two quad-Green bits on 5-fold/9-fold.

Cycle BI closed triple-Green bits on the covering annuli. The
interval count H(m) equals 4 only for m in {4,7,14}; for m>=8 except
m=14 a hit strictly before the complementary pair {2m-2,2m-1} forces
H(m)>=5. Truncated covering windows then have C_le>=5 except the
9-fold M=0 r=1 slot (N+1=4). Full power-of-two windows have no even
quads for a>=6 by Cycle AZ; the a=4 and a=5 seeds give only 5-fold
(M,r)=(1,7),(2,15) and 9-fold (1,15). The surviving quads are exactly
two packed bits on each covering annulus, for every k>=3, with closed
times.

Not a prize claim: those quads are not identically-1 productions, and
the Fermat covering remains a prefix.

Run: python3 research/cycle_bj.py --certify
Dump: research/cycle_bj.json
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


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def second_hit(m: int) -> int:
    if m % 4 in (0, 1):
        return m + 1
    if m % 4 == 2:
        return m + (1 << (v2(m + 2) - 1))
    return m + (1 << (v2(m + 1) - 1))


def N_ann(q: int, M: int, r: int) -> tuple[int, int, int]:
    a_off = {5: 2, 9: 3}[q]
    W = (1 << (M + a_off)) - 1
    ncone = (q * (1 << M) + r - 3) // 2
    return min(W, ncone), W, ncone


def C_le(N: int, d: int) -> int:
    if N < 0:
        return 0
    return sum(G(n, d) for n in range(N + 1))


def expected_quads(q: int, k: int) -> list[int]:
    U = 1 << k
    if q == 5:
        return sorted([5 * (U >> 2) + 1, 3 * (U >> 1) + 1])
    return sorted([3 * (U >> 1) + 1, 8 * U + 1])


def expected_times(q: int, k: int, p: int) -> list[int]:
    U = 1 << k
    if q == 5:
        table = {
            5 * (U >> 2) + 1: [(5 * U) // 4, (3 * U) // 2, 2 * U, 3 * U],
            3 * (U >> 1) + 1: [U, (3 * U) // 2, 2 * U, 3 * U],
        }
        return table[p]
    table = {
        3 * (U >> 1) + 1: [(3 * U) // 2, 2 * U, 3 * U, 5 * U],
        8 * U + 1: [5 * U, 6 * U, 7 * U, 8 * U],
    }
    return table[p]


def H(m: int) -> int:
    return sum(G(n, 2 * m) for n in range(m, 2 * m + 1))


def n3_strict(m: int) -> int:
    n2 = second_hit(m)
    for n in range(n2 + 1, 2 * m):
        if G(n, 2 * m):
            return n
    return 2 * m


def interval_H4_ok() -> bool:
    if [n for n in range(4, 9) if G(n, 8)] != [4, 5, 7, 8]:
        return False
    if [n for n in range(7, 15) if G(n, 14)] != [7, 11, 13, 14]:
        return False
    if [n for n in range(14, 29) if G(n, 28)] != [14, 22, 26, 28]:
        return False
    if H(4) != 4 or H(7) != 4 or H(14) != 4:
        return False
    for m in range(1, 8):
        if m in (4, 7):
            continue
        if H(m) >= 4 and m not in (1, 2, 3, 6):
            # 1,2 H=2; 3,6 H=3; 5 H=5
            if m == 5 and H(5) < 5:
                return False
    return H(5) >= 5 and H(8) >= 5


def n3_before_comp_ok(mmax: int) -> bool:
    """For 8<=m<=mmax, n3 equals the complementary hit iff m=14."""
    for m in range(8, mmax + 1):
        n3 = n3_strict(m)
        comp = 2 * m - 2 if G(2 * m - 2, 2 * m) else 2 * m - 1
        if m == 14:
            if n3 != comp or H(m) != 4:
                return False
            continue
        if n3 >= comp or H(m) < 5:
            return False
    return True


def az_even_quad_seeds_ok() -> bool:
    """a=4,5 even |S|=4 seeds; a=6,7 empty as Cycle AZ predicts."""
    def even_S(a: int) -> list[int]:
        nmax = (1 << (a - 1)) - 1
        return [
            D
            for D in range(0, 2 * nmax + 1, 2)
            if sum(G(n, D) for n in range(nmax + 1)) == 4
        ]

    if even_S(4) != [2, 4, 6]:
        return False
    if even_S(5) != [14]:
        return False
    if even_S(6) or even_S(7):
        return False
    # r-bound: 5-fold M>=3 and 9-fold M>=2 have a>=6, so no even N=W quads
    for M in range(3, 10):
        a = M + 3
        nmax = (1 << (a - 1)) - 1
        rmax = 5 * (1 << M)
        for D in range(0, min(2 * nmax, rmax) + 1, 2):
            if sum(G(n, D) for n in range(nmax + 1)) == 4:
                if D + 1 <= rmax:
                    return False
        if M >= 3:
            break  # a=6 check is the first AZ window; a=7 already empty
    return True


def C_le_quads_Mge0(q: int, Mmax: int) -> list[tuple[int, int]]:
    found = []
    rmax_base = {5: 5, 9: 9}[q]
    for M in range(0, Mmax + 1):
        for r in range(1, rmax_base * (1 << M) + 1, 2):
            N, _W, _nc = N_ann(q, M, r)
            if N < 0:
                continue
            if C_le(N, r - 1) == 4:
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


def negative_M_quads_ok() -> bool:
    for k in range(3, 8):
        for j in range(k + 1, k + 5):
            if r1_surviving(5, k, j) == 4:
                return False
            if r1_surviving(9, k, j) == 4:
                return False
        if lift_count(5, k, 7, k + 1) != 0:
            return False
        if lift_count(9, k, 15, k + 1) != 0:
            return False
        if r1_surviving(9, k, k) != 4:
            return False
    return True


def firing_xor_ok(kmax: int) -> dict:
    rows = evolve_rows(9 * (1 << kmax))
    xor5, xor9, phi5, phi9 = [], [], [], []
    for k in range(3, kmax + 1):
        U = 1 << k
        x5 = 0
        for p in expected_quads(5, k):
            for t in expected_times(5, k, p):
                x5 ^= fires(rows[t], p)
        x9 = 0
        for p in expected_quads(9, k):
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
    h4: bool,
    n3c: bool,
    azs: bool,
    found5: list,
    found9: list,
    negM: bool,
    recs: list[dict],
    fire: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert h4 and n3c and azs and negM
    assert found5 == [(1, 7), (2, 15)]
    assert found9 == [(0, 1), (1, 15)]
    for rec in recs:
        k = rec["k"]
        assert rec["quad_q5"] == expected_quads(5, k)
        assert rec["quad_q9"] == expected_quads(9, k)
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
    h4 = interval_H4_ok()
    n3c = n3_before_comp_ok(64)
    azs = az_even_quad_seeds_ok()
    found5 = C_le_quads_Mge0(5, 8)
    found9 = C_le_quads_Mge0(9, 7)
    negM = negative_M_quads_ok()
    recs = []
    for k in range(3, 8):
        by5 = census(k, 5)
        by9 = census(k, 9)
        q5 = sorted(p for p, ts in by5.items() if len(ts) == 4)
        q9 = sorted(p for p, ts in by9.items() if len(ts) == 4)
        recs.append({
            "k": k,
            "quad_q5": q5,
            "quad_q9": q9,
            "times5_ok": all(by5[p] == expected_times(5, k, p) for p in q5),
            "times9_ok": all(by9[p] == expected_times(9, k, p) for p in q9),
        })
    fire = firing_xor_ok(8)
    checks = self_checks(
        c20, h4, n3c, azs, found5, found9, negM, recs, fire
    )
    dump = {
        "cycle": "BJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": recs,
        "C_le_eq4_Mge0": {"q5": found5, "q9": found9},
        "firing": {
            "xor5": fire["xor5"],
            "xor9": fire["xor9"],
            "phi5": fire["phi5"],
            "phi9": fire["phi9"],
        },
        "lemmas": {
            "H_m_eq4": True,
            "n3_before_comp": True,
            "exactly_two_quads_q5": True,
            "exactly_two_quads_q9": True,
            "quads_always_fire": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "H_m_eq4": "LEMMA",
            "n3_before_comp": "LEMMA",
            "exactly_two_quads_q5": "LEMMA",
            "exactly_two_quads_q9": "LEMMA",
            "quads_always_fire": "KILLED",
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
    print("C_le==4", dump["C_le_eq4_Mge0"])


if __name__ == "__main__":
    main()
