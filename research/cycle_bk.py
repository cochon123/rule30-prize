#!/usr/bin/env python3
"""Cycle BK: exact pentuple-Green bits on 5-fold/9-fold.

Cycle BJ closed quad-Green bits on the covering annuli. Pentuples are
the next odd multiplicity, so they contribute to Fermat spines.
C_le=5 occurs at nine (M,r) slots on the 5-fold annulus and seven on
the 9-fold. Those match Cycle BA's even pentuple seeds on full
power-of-two windows (only r=17,37,39,79 survive the r-bound) plus
five truncated residues. For k>=4 there are exactly nine pentuple
packed bits on the 5-fold annulus and exactly seven on the 9-fold
(eight and seven at k=3, before the M=4 family appears), with times
from Green lift.

Not a prize claim: those pentuples are not identically-1 productions,
and the Fermat covering remains a prefix.

Run: python3 research/cycle_bk.py --certify
Dump: research/cycle_bk.json
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

Q5_PENT = [(1, 1), (5, 2), (7, 2), (11, 2), (17, 2), (15, 3), (37, 3), (39, 3), (79, 4)]
Q9_PENT = [(3, 1), (5, 1), (7, 1), (11, 1), (13, 1), (17, 1), (15, 2)]
BA_Q = (12, 16, 18, 20, 26, 28, 34, 50)


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


def family_p_times(q: int, k: int, r: int, M: int) -> tuple[int, list[int]] | None:
    if M > k:
        return None
    U = 1 << k
    j = k - M
    p = q * U + 1 - r * (1 << j)
    if p < 1:
        return None
    N, _W, _nc = N_ann(q, M, r)
    ts = []
    for n in range(N + 1):
        if G(n, r - 1):
            t = q * U - (1 << j) * (n + 1)
            if 1 <= p <= 2 * t and U <= t < q * U:
                ts.append(t)
    ts.sort()
    return p, ts


def expected_families(q: int, k: int) -> list[tuple[int, int]]:
    fam = Q5_PENT if q == 5 else Q9_PENT
    return [(r, M) for r, M in fam if M <= k]


def expected_pentuples(q: int, k: int) -> list[int]:
    out = []
    for r, M in expected_families(q, k):
        ft = family_p_times(q, k, r, M)
        if ft is not None:
            out.append(ft[0])
    return sorted(out)


def H(m: int) -> int:
    return sum(G(n, 2 * m) for n in range(m, 2 * m + 1))


def interval_H5_ok() -> bool:
    hits = {
        5: [5, 6, 7, 9, 10],
        9: [9, 10, 15, 17, 18],
        15: [15, 23, 27, 29, 30],
        30: [30, 46, 54, 58, 60],
    }
    for m, want in hits.items():
        got = [n for n in range(m, 2 * m + 1) if G(n, 2 * m)]
        if got != want or H(m) != 5:
            return False
    le5 = [m for m in range(1, 65) if H(m) <= 5]
    return le5 == [1, 2, 3, 4, 5, 6, 7, 9, 14, 15, 30]


def ba_even_pentuples_ok() -> bool:
    def even_S(a: int) -> list[int]:
        nmax = (1 << (a - 1)) - 1
        return [
            D
            for D in range(0, 2 * nmax + 1, 2)
            if sum(G(n, D) for n in range(nmax + 1)) == 5
        ]

    if even_S(4) != []:
        return False
    if even_S(5) != [16, 20]:
        return False
    if even_S(6) != [36, 38, 44, 46, 48, 52]:
        return False
    for a in (7, 8):
        pred = sorted((1 << a) - q for q in BA_Q)
        if even_S(a) != pred:
            return False
    # r-bound: 5-fold M>=5 and 9-fold M>=2 have no surviving BA seed
    for M in range(5, 10):
        rmin = (1 << (M + 3)) - 49
        if rmin <= 5 * (1 << M):
            return False
    for M in range(3, 8):
        rmin = (1 << (M + 4)) - 49
        if rmin <= 9 * (1 << M):
            return False
    return True


def C_le_pent_Mge0(q: int, Mmax: int) -> list[tuple[int, int]]:
    found = []
    rmax_base = {5: 5, 9: 9}[q]
    for M in range(0, Mmax + 1):
        for r in range(1, rmax_base * (1 << M) + 1, 2):
            N, _W, _nc = N_ann(q, M, r)
            if N < 0:
                continue
            if C_le(N, r - 1) == 5:
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


def negative_M_pent_ok() -> bool:
    for k in range(3, 8):
        for j in range(k + 1, k + 5):
            if r1_surviving(5, k, j) == 5:
                return False
            if r1_surviving(9, k, j) == 5:
                return False
    return True


def firing_xor_ok(kmax: int) -> dict:
    rows = evolve_rows(9 * (1 << kmax))
    xor5, xor9, phi5, phi9 = [], [], [], []
    for k in range(3, kmax + 1):
        U = 1 << k
        x5 = 0
        for r, M in expected_families(5, k):
            ft = family_p_times(5, k, r, M)
            if ft is None or len(ft[1]) != 5:
                return {"ok": False}
            p, ts = ft
            for t in ts:
                x5 ^= fires(rows[t], p)
        x9 = 0
        for r, M in expected_families(9, k):
            ft = family_p_times(9, k, r, M)
            if ft is None or len(ft[1]) != 5:
                return {"ok": False}
            p, ts = ft
            for t in ts:
                x9 ^= fires(rows[t], p)
        c = lambda t: (rows[t] >> t) & 1
        xor5.append(x5)
        xor9.append(x9)
        phi5.append(c(5 * U) ^ c(U))
        phi9.append(c(9 * U) ^ c(U))
    return {
        "ok": True,
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
    h5: bool,
    ba: bool,
    found5: list,
    found9: list,
    negM: bool,
    recs: list[dict],
    fire: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert h5 and ba and negM and fire.get("ok")
    assert found5 == [(1, 1), (2, 5), (2, 7), (2, 11), (2, 17), (3, 15), (3, 37), (3, 39), (4, 79)]
    assert found9 == [(1, 3), (1, 5), (1, 7), (1, 11), (1, 13), (1, 17), (2, 15)]
    for rec in recs:
        assert rec["pent_q5"] == rec["lift5"]
        assert rec["pent_q9"] == rec["lift9"]
        assert rec["n5"] == (8 if rec["k"] == 3 else 9)
        assert rec["n9"] == 7
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
    h5 = interval_H5_ok()
    ba = ba_even_pentuples_ok()
    found5 = C_le_pent_Mge0(5, 8)
    found9 = C_le_pent_Mge0(9, 6)
    negM = negative_M_pent_ok()
    recs = []
    for k in range(3, 8):
        by5 = census(k, 5)
        by9 = census(k, 9)
        p5 = sorted(p for p, ts in by5.items() if len(ts) == 5)
        p9 = sorted(p for p, ts in by9.items() if len(ts) == 5)
        lift5, lift9 = [], []
        times5_ok = times9_ok = True
        for r, M in expected_families(5, k):
            ft = family_p_times(5, k, r, M)
            if ft is None or len(ft[1]) != 5:
                times5_ok = False
                continue
            lift5.append(ft[0])
            if by5.get(ft[0], []) != ft[1]:
                times5_ok = False
        for r, M in expected_families(9, k):
            ft = family_p_times(9, k, r, M)
            if ft is None or len(ft[1]) != 5:
                times9_ok = False
                continue
            lift9.append(ft[0])
            if by9.get(ft[0], []) != ft[1]:
                times9_ok = False
        recs.append({
            "k": k,
            "pent_q5": p5,
            "pent_q9": p9,
            "lift5": sorted(lift5),
            "lift9": sorted(lift9),
            "n5": len(p5),
            "n9": len(p9),
            "times5_ok": times5_ok,
            "times9_ok": times9_ok,
        })
    fire = firing_xor_ok(10)
    checks = self_checks(c20, h5, ba, found5, found9, negM, recs, fire)
    dump = {
        "cycle": "BK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": recs,
        "C_le_eq5_Mge0": {"q5": found5, "q9": found9},
        "firing": {
            "xor5": fire["xor5"],
            "xor9": fire["xor9"],
            "phi5": fire["phi5"],
            "phi9": fire["phi9"],
        },
        "lemmas": {
            "H_m_eq5": True,
            "exactly_nine_pentuples_q5": True,
            "exactly_seven_pentuples_q9": True,
            "pentuples_always_fire": False,
            "pentuple_xor_is_phi": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "H_m_eq5": "LEMMA",
            "exactly_nine_pentuples_q5": "LEMMA",
            "exactly_seven_pentuples_q9": "LEMMA",
            "pentuples_always_fire": "KILLED",
            "pentuple_xor_is_phi": "KILLED",
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
    print("annulus", [{k: rec[k] for k in ("k", "n5", "n9", "times5_ok", "times9_ok")} for rec in recs])
    print("C_le==5", dump["C_le_eq5_Mge0"])


if __name__ == "__main__":
    main()
