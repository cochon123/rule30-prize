#!/usr/bin/env python3
"""Cycle BG: exactly three/two unique-Green bits on 5-fold/9-fold.

Cycle BF listed Mersenne centre-right unique bits and left exhaustiveness
as a prefix. The even-target identity G(m,2m)=1, vanishing for n<m, and a
second hit n in (m, 3m/2+1] (mod-4 cases, with 2^a-2 and 2^a-1 exceptions)
force 6m >= 4N-2 whenever C_le(N, 2m)=1. On the 5-fold and 9-fold annuli
that inequality contradicts uniqueness for every even d when M=k-j >= 1.
Together with the r=1 count (unique iff j in {k+a-1, k+a}) this upgrades
exhaustiveness to a lemma: exactly three unique-Green bits on the 5-fold
annulus and exactly two on the 9-fold, for every k>=3.

Not a prize claim: extra unique bits are still not identically-1, and the
Fermat covering remains a prefix.

Run: python3 research/cycle_bg.py --certify
Dump: research/cycle_bg.json
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


def unique_census(k: int, q: int) -> dict[int, list[int]]:
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
    """Canonical second n>m with G(n, 2m)=1, by the mod-4 lemma."""
    if m % 4 in (0, 1):
        return m + 1
    if m % 4 == 2:
        return m + (1 << (v2(m + 2) - 1))
    return m + (1 << (v2(m + 1) - 1))


def second_hit_ok(mmax: int) -> bool:
    for m in range(1, mmax + 1):
        n = second_hit(m)
        cap = 3 * m // 2 + 1
        if not (m < n <= cap):
            return False
        if G(n, 2 * m) != 1:
            return False
        if any(G(t, 2 * m) for t in range(m + 1, n)):
            return False
        if any(G(t, 2 * m) for t in range(0, m)):
            return False
        if G(m, 2 * m) != 1:
            return False
    return True


def merse_mod4_identities(mmax: int) -> bool:
    for m in range(1, mmax + 1):
        if m % 4 in (0, 1) and G(m + 1, 2 * m) != 1:
            return False
        if m % 4 == 0:
            # even m=2p, p even => G(p, 2p-1)=0
            p = m // 2
            if G(p, 2 * p - 1) != 0:
                return False
        if m % 4 == 1:
            k = (m - 1) // 4
            if G(k, 2 * k) != 1:
                return False
        if m % 4 == 2:
            n = m + (1 << (v2(m + 2) - 1))
            if G(n, 2 * m) != 1:
                return False
        if m % 4 == 3:
            n = m + (1 << (v2(m + 1) - 1))
            if G(n, 2 * m) != 1:
                return False
    return True


def C_unique_even(a: int) -> list[int]:
    if a < 2:
        return []
    return [((1 << (a + 1)) - 4), ((1 << (a + 1)) - 2)]


def C_unique_set(a: int) -> set[int]:
    if a == 0:
        return {0}
    if a == 1:
        return {1, 2}
    odd = {2 * s + 1 for s in C_unique_set(a - 1)}
    return odd | set(C_unique_even(a))


def C_unique_ok(amax: int) -> bool:
    for a in range(0, amax + 1):
        pred = C_unique_set(a)
        brute = set()
        N = 1 << a
        mx = 2 * (N - 1)
        for d in range(0, mx + 1):
            cnt = sum(G(n, d) for n in range(N))
            if cnt == 1:
                brute.add(d)
        if pred != brute:
            return False
    return True


def r1_surviving(q: int, k: int, j: int) -> int:
    """Surviving n-count for r=1 (G(n,0)=1 for all n)."""
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
    # n+1 <= nmax, n <= min(W, nmax-1)
    last = min(W, nmax - 1)
    return max(0, last + 1)


def algebra_contradiction_ok() -> bool:
    """3d <= 4N-4 on 5-fold and 9-fold for M>=1, even d."""
    for M in range(1, 12):
        for q, alen in ((5, M + 2), (9, M + 3)):
            W = (1 << alen) - 1
            for r in range(1, q * (1 << M) + 1, 2):
                d = r - 1
                ncone = (q * (1 << M) + r - 3) // 2
                N = min(W, ncone)
                if N <= 0:
                    continue
                if 3 * d >= 4 * N - 2:
                    # r=1 has d=0; skip even-d lemma
                    if d >= 2:
                        return False
    return True


def self_checks(
    c20,
    second: bool,
    merse: bool,
    cuniq: bool,
    alg: bool,
    recs: list[dict],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert second and merse and cuniq and alg
    for rec in recs:
        k = rec["k"]
        U = 1 << k
        assert rec["uniq_q5"] == [1, U + 1, 3 * U + 1]
        assert rec["uniq_q9"] == [U + 1, 5 * U + 1]
        assert rec["r1_unique_q5"] == [k + 1, k + 2]
        assert rec["r1_unique_q9"] == [k + 2, k + 3]
        assert rec["n_p1_q9"] == 3
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    second = second_hit_ok(256)
    merse = merse_mod4_identities(256)
    cuniq = C_unique_ok(8)
    alg = algebra_contradiction_ok()
    recs = []
    for k in range(3, 8):
        U = 1 << k
        by5 = unique_census(k, 5)
        by9 = unique_census(k, 9)
        uniq5 = sorted(p for p, ts in by5.items() if len(ts) == 1)
        uniq9 = sorted(p for p, ts in by9.items() if len(ts) == 1)
        r1_5 = [j for j in range(0, k + 3) if r1_surviving(5, k, j) == 1]
        r1_9 = [j for j in range(0, k + 4) if r1_surviving(9, k, j) == 1]
        recs.append({
            "k": k,
            "uniq_q5": uniq5,
            "uniq_q9": uniq9,
            "n_p1_q9": len(by9.get(1, [])),
            "r1_unique_q5": r1_5,
            "r1_unique_q9": r1_9,
        })
    checks = self_checks(c20, second, merse, cuniq, alg, recs)
    dump = {
        "cycle": "BG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": recs,
        "lemmas": {
            "C_unique_even": True,
            "second_hit_2m": True,
            "r1_unique_js": True,
            "unique_exactly_q5_q9": True,
            "extra_unique_always_fire": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "C_unique_even": "LEMMA",
            "second_hit_2m": "LEMMA",
            "r1_unique_js": "LEMMA",
            "unique_exactly_q5_q9": "LEMMA",
            "extra_unique_always_fire": "KILLED",
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


if __name__ == "__main__":
    main()
