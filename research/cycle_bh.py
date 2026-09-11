#!/usr/bin/env python3
"""Cycle BH: exactly two/three double-Green bits on 5-fold/9-fold.

Cycle BG closed unique-Green bits on the covering annuli. The same
Green-lift count C_le(N, r-1), the diagonal G(m,2m)=1, a third hit
n3<=2m for m>=3, Cycle AW's absence of even half-window doubles, and
the cone inequality d<=ncone, force the even-multiplicity remainder
to have no C_le=2 slots for M=k-j>=1. The surviving doubles are
exactly two packed bits on the 5-fold annulus and three on the
9-fold, for every k>=3, with closed times.

Not a prize claim: those doubles are not identically-1 productions,
and the Fermat covering remains a prefix.

Run: python3 research/cycle_bh.py --certify
Dump: research/cycle_bh.json
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


def factor(q: int, k: int, p: int) -> tuple[int, int]:
    x = q * (1 << k) + 1 - p
    j = (x & -x).bit_length() - 1
    return x >> j, j


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


def expected_doubles(q: int, k: int) -> list[int]:
    U = 1 << k
    if q == 5:
        return sorted([2 * U + 1, 4 * U + 1])
    return sorted([3 * U + 1, 6 * U + 1, 7 * U + 1])


def expected_times(q: int, k: int, p: int) -> list[int]:
    U = 1 << k
    if q == 5:
        if p == 2 * U + 1:
            return [2 * U, 3 * U]
        if p == 4 * U + 1:
            return [3 * U, 4 * U]
    else:
        if p == 3 * U + 1:
            return [3 * U, 5 * U]
        if p == 6 * U + 1:
            return [6 * U, 7 * U]
        if p == 7 * U + 1:
            return [5 * U, 7 * U]
    raise KeyError((q, k, p))


def G_diag_ok(nmax: int) -> bool:
    return all(G(n, n) == 1 for n in range(nmax + 1))


def third_hit_ok(mmax: int) -> bool:
    """For m>=3, n2 < 2m, hence n3 <= 2m because G(2m,2m)=1."""
    for m in range(3, mmax + 1):
        n2 = second_hit(m)
        if not (m < n2 < 2 * m):
            return False
        if G(n2, 2 * m) != 1:
            return False
        if G(2 * m, 2 * m) != 1:
            return False
        if any(G(t, 2 * m) for t in range(n2 + 1, 2 * m)):
            # n3 < 2m is allowed; just must not skip past 2m
            pass
        # first hit is n=m
        if G(m, 2 * m) != 1:
            return False
        if any(G(t, 2 * m) for t in range(0, m)):
            return False
    return True


def ncone_dominates_d_ok() -> bool:
    """For M>=1, d=r-1 never exceeds ncone on 5-fold or 9-fold."""
    for q in (5, 9):
        for M in range(1, 12):
            rmax = q * (1 << M)
            for r in range(1, rmax + 1, 2):
                _N, _W, ncone = N_ann(q, M, r)
                if r - 1 > ncone:
                    return False
    return True


def C_le_doubles_Mge0(q: int, Mmax: int) -> list[tuple[int, int]]:
    found = []
    rmax_base = {5: 5, 9: 9}[q]
    for M in range(0, Mmax + 1):
        for r in range(1, rmax_base * (1 << M) + 1, 2):
            N, _W, _nc = N_ann(q, M, r)
            if N < 0:
                continue
            if C_le(N, r - 1) == 2:
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
    """Hit count for r odd, j>=1, via Green lift and the cone."""
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


def negative_M_doubles_ok() -> bool:
    """j>k: only the two 9-fold M=-1 doubles, none on 5-fold."""
    for k in range(3, 8):
        # 5-fold: r * 2^{j-k} <= 5, j-k>=1 => only r=1
        for j in range(k + 1, k + 4):
            if r1_surviving(5, k, j) == 2:
                return False
        # 9-fold r=1
        r1_dbl = [j for j in range(k + 1, k + 5) if r1_surviving(9, k, j) == 2]
        if r1_dbl != [k + 1]:
            return False
        # 9-fold r=3, j=k+1 is a double; j>k+1 is off-range
        if lift_count(9, k, 3, k + 1) != 2:
            return False
        if lift_count(9, k, 3, k + 2) != 0:
            return False
        # no r>=5 with j>k
        if lift_count(9, k, 5, k + 1) != 0:
            return False
        if lift_count(5, k, 3, k + 1) != 0:
            return False
    return True


def firing_xor_ok(kmax: int) -> dict:
    """XOR of covering-annulus doubles takes both values; not phi."""
    rows = evolve_rows(9 * (1 << kmax))
    xor5, xor9, phi5, phi9 = [], [], [], []
    bits5, bits9 = [], []
    for k in range(3, kmax + 1):
        U = 1 << k
        d1 = fires(rows[2 * U], 2 * U + 1) ^ fires(rows[3 * U], 2 * U + 1)
        d2 = fires(rows[3 * U], 4 * U + 1) ^ fires(rows[4 * U], 4 * U + 1)
        e1 = fires(rows[3 * U], 3 * U + 1) ^ fires(rows[5 * U], 3 * U + 1)
        e2 = fires(rows[6 * U], 6 * U + 1) ^ fires(rows[7 * U], 6 * U + 1)
        e3 = fires(rows[5 * U], 7 * U + 1) ^ fires(rows[7 * U], 7 * U + 1)
        c = lambda t: (rows[t] >> t) & 1
        xor5.append(d1 ^ d2)
        xor9.append(e1 ^ e2 ^ e3)
        phi5.append(c(5 * U) ^ c(U))
        phi9.append(c(9 * U) ^ c(U))
        bits5.append((d1, d2))
        bits9.append((e1, e2, e3))
    return {
        "xor5": xor5,
        "xor9": xor9,
        "phi5": phi5,
        "phi9": phi9,
        "bits5": bits5,
        "bits9": bits9,
        "xor5_both": set(xor5) == {0, 1},
        "xor9_both": set(xor9) == {0, 1},
        "xor5_is_phi": xor5 == phi5,
        "xor9_is_phi": xor9 == phi9,
    }


def self_checks(
    c20,
    diag: bool,
    third: bool,
    ncone: bool,
    found5: list,
    found9: list,
    negM: bool,
    recs: list[dict],
    fire: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert diag and third and ncone and negM
    assert found5 == [(0, 1), (0, 3)]
    assert found9 == [(0, 3)]
    assert G(0, 2) == 0 and G(1, 2) == 1 and G(2, 2) == 1
    for rec in recs:
        k = rec["k"]
        assert rec["dbl_q5"] == expected_doubles(5, k)
        assert rec["dbl_q9"] == expected_doubles(9, k)
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
    diag = G_diag_ok(128)
    third = third_hit_ok(128)
    ncone = ncone_dominates_d_ok()
    found5 = C_le_doubles_Mge0(5, 8)
    found9 = C_le_doubles_Mge0(9, 7)
    negM = negative_M_doubles_ok()
    recs = []
    for k in range(3, 8):
        by5 = census(k, 5)
        by9 = census(k, 9)
        dbl5 = sorted(p for p, ts in by5.items() if len(ts) == 2)
        dbl9 = sorted(p for p, ts in by9.items() if len(ts) == 2)
        times5_ok = all(
            by5[p] == expected_times(5, k, p) for p in dbl5
        )
        times9_ok = all(
            by9[p] == expected_times(9, k, p) for p in dbl9
        )
        recs.append({
            "k": k,
            "dbl_q5": dbl5,
            "dbl_q9": dbl9,
            "rj5": [factor(5, k, p) + (k - factor(5, k, p)[1],) for p in dbl5],
            "rj9": [factor(9, k, p) + (k - factor(9, k, p)[1],) for p in dbl9],
            "times5_ok": times5_ok,
            "times9_ok": times9_ok,
        })
    fire = firing_xor_ok(8)
    checks = self_checks(
        c20, diag, third, ncone, found5, found9, negM, recs, fire
    )
    dump = {
        "cycle": "BH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": recs,
        "C_le_eq2_Mge0": {"q5": found5, "q9": found9},
        "firing": {
            "xor5": fire["xor5"],
            "xor9": fire["xor9"],
            "phi5": fire["phi5"],
            "phi9": fire["phi9"],
        },
        "lemmas": {
            "G_nn_one": True,
            "third_hit_le_2m": True,
            "ncone_ge_d_Mge1": True,
            "exactly_two_doubles_q5": True,
            "exactly_three_doubles_q9": True,
            "doubles_always_fire": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_nn_one": "LEMMA",
            "third_hit_le_2m": "LEMMA",
            "ncone_ge_d_Mge1": "LEMMA",
            "exactly_two_doubles_q5": "LEMMA",
            "exactly_three_doubles_q9": "LEMMA",
            "doubles_always_fire": "KILLED",
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
    print("C_le==2", dump["C_le_eq2_Mge0"])


if __name__ == "__main__":
    main()
