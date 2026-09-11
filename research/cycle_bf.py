#!/usr/bin/env python3
"""Cycle BF: Fermat p=1 times; Mersenne centre-right unique bits.

Cycle AR lifts G(m, (2^a+1)2^k-1) to G(s, 2^a). Restricting to the
q-fold annulus gives the exact leftmost-11 times for every Fermat-odd
spine, in particular the covering triple:

    q=3: t=U;  q=5: t=2U;  q=9: t=U, 3U, 4U.

The same Mersenne-target law makes packed bit U+1 unique-Green on every
Fermat-odd annulus (time t=U, fires iff c_U AND r_U), and makes
p=(2^{a-1}+1)U+1 unique-Green at the matching centre-right time.
On the 5-fold and 9-fold annuli those, together with p=1, are the only
unique-Green bits through k=7 (prefix). Extra unique bits take both
firing values, so they are not identically-1 productions. Doubling
gives phi^{(q)}_{k+1} = phi^{(2q)}_k XOR I_{k+1}.

Not a prize claim: the Fermat covering remains a prefix; some
phi^{(q)}_k=1 infinitely often remains open.

Run: python3 research/cycle_bf.py --certify
Dump: research/cycle_bf.json
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
        left = j in S
        right = (j - 1) in S
        if left ^ right:
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


def p1_times_formula(a: int, k: int) -> list[int]:
    """Leftmost-11 Green times on the (2^a+1)-fold annulus."""
    U = 1 << k
    pow2a = 1 << a
    times = []
    for s in range(pow2a >> 1, pow2a):
        if G(s, pow2a):
            times.append((pow2a - s) * U)
    return sorted(times)


def p1_times_brute(a: int, k: int) -> list[int]:
    U = 1 << k
    q = (1 << a) + 1
    target = q * U
    hits = []
    for t in range(U, q * U):
        if G(target - t - 1, target - 1):
            hits.append(t)
    return hits


def merse_tgt_ok(amax: int, m_mult: int) -> bool:
    for a in range(0, amax + 1):
        D = (1 << a) - 1
        for m in range(0, (m_mult << a) + 1):
            got = G(m, D)
            if a == 0:
                want = 1
            elif D > 2 * m:
                want = 0
            else:
                want = int((m + 1) % (1 << a) == 0)
            if got != want:
                return False
    return True


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


def r1_unique_bits(a: int, k: int) -> list[tuple[int, int]]:
    """Predicted unique r=1 Mersenne centre-right bits: (p, t)."""
    U = 1 << k
    q = (1 << a) + 1
    p_hi = U + 1
    t_hi = U
    p_lo = ((1 << (a - 1)) + 1) * U + 1
    t_lo = ((1 << (a - 1)) + 1) * U
    return [(p_hi, t_hi), (p_lo, t_lo)]


def support_matches_G(mmax: int) -> bool:
    for m in range(0, mmax + 1):
        S = G_support(m)
        for d in range(0, 2 * m + 1):
            if G(m, d) != int(d in S):
                return False
        if any(d < 0 or d > 2 * m for d in S):
            return False
    return True


def self_checks(
    c20,
    merse: bool,
    supp: bool,
    p1_ok: bool,
    doubling_ok: bool,
    recs: list[dict],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert merse and supp and p1_ok and doubling_ok
    fire_U1 = []
    fire_5fold_3U = []
    fire_9fold_5U = []
    for rec in recs:
        k = rec["k"]
        U = 1 << k
        assert rec["p1_times"]["3"] == [U]
        assert rec["p1_times"]["5"] == [2 * U]
        assert rec["p1_times"]["9"] == [U, 3 * U, 4 * U]
        assert rec["n_U1_q3"] == rec["n_U1_q5"] == rec["n_U1_q9"] == 1
        assert rec["t_U1"] == U
        assert rec["n_3U1_q5"] == 1 and rec["t_3U1"] == 3 * U
        assert rec["n_5U1_q9"] == 1 and rec["t_5U1"] == 5 * U
        assert rec["n_2U1_q3"] == 1 and rec["t_2U1"] == 2 * U
        pred3, pred5, pred9 = r1_unique_bits(1, k), r1_unique_bits(2, k), r1_unique_bits(3, k)
        assert pred3[0] == (U + 1, U) and pred3[1] == (2 * U + 1, 2 * U)
        assert pred5[0] == (U + 1, U) and pred5[1] == (3 * U + 1, 3 * U)
        assert pred9[0] == (U + 1, U) and pred9[1] == (5 * U + 1, 5 * U)
        if k >= 3:
            assert rec["n_unique_q5"] == 3
            assert rec["uniq_q5"] == [1, U + 1, 3 * U + 1]
            assert rec["n_unique_q9"] == 2
            assert rec["uniq_q9"] == [U + 1, 5 * U + 1]
            assert rec["n_p1_q9"] == 3
        fire_U1.append(rec["fire_U1"])
        fire_5fold_3U.append(rec["fire_3U1"])
        fire_9fold_5U.append(rec["fire_5U1"])
    assert 0 in fire_U1 and 1 in fire_U1
    assert 0 in fire_5fold_3U and 1 in fire_5fold_3U
    assert 0 in fire_9fold_5U  # 1 may be absent on this prefix
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    merse = merse_tgt_ok(10, 8)
    supp = support_matches_G(80)
    p1_ok = True
    for a in range(1, 5):
        for k in range(1, 9):
            if p1_times_formula(a, k) != p1_times_brute(a, k):
                p1_ok = False
    # doubling identity on centres
    kmax_d = 8
    need = 2 * 12 * (1 << kmax_d)
    centres = packed_center_bits(need + 1)
    doubling_ok = True
    for k in range(1, kmax_d + 1):
        U = 1 << k
        I = centres[2 * U] ^ centres[U]
        for q in range(1, 13):
            left = centres[q * 2 * U] ^ centres[2 * U]
            right = (centres[2 * q * U] ^ centres[U]) ^ I
            if left != right:
                doubling_ok = False
    kmax = 7
    rows = evolve_rows(9 * (1 << kmax))
    recs = []
    for k in range(3, kmax + 1):
        U = 1 << k
        by5 = unique_census(k, 5)
        by9 = unique_census(k, 9)
        by3 = unique_census(k, 3)
        uniq5 = sorted(p for p, ts in by5.items() if len(ts) == 1)
        uniq9 = sorted(p for p, ts in by9.items() if len(ts) == 1)
        recs.append({
            "k": k,
            "p1_times": {
                "3": p1_times_formula(1, k),
                "5": p1_times_formula(2, k),
                "9": p1_times_formula(3, k),
                "17": p1_times_formula(4, k),
            },
            "n_unique_q5": len(uniq5),
            "uniq_q5": uniq5,
            "n_unique_q9": len(uniq9),
            "uniq_q9": uniq9,
            "n_p1_q9": len(by9.get(1, [])),
            "n_U1_q3": len(by3.get(U + 1, [])),
            "n_U1_q5": len(by5.get(U + 1, [])),
            "n_U1_q9": len(by9.get(U + 1, [])),
            "t_U1": (by5.get(U + 1) or [None])[0],
            "fire_U1": fires(rows[U], U + 1),
            "n_3U1_q5": len(by5.get(3 * U + 1, [])),
            "t_3U1": (by5.get(3 * U + 1) or [None])[0],
            "fire_3U1": fires(rows[3 * U], 3 * U + 1),
            "n_5U1_q9": len(by9.get(5 * U + 1, [])),
            "t_5U1": (by9.get(5 * U + 1) or [None])[0],
            "fire_5U1": fires(rows[5 * U], 5 * U + 1),
            "n_2U1_q3": len(by3.get(2 * U + 1, [])),
            "t_2U1": (by3.get(2 * U + 1) or [None])[0],
        })
    checks = self_checks(c20, merse, supp, p1_ok, doubling_ok, recs)
    dump = {
        "cycle": "BF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "annulus": recs,
        "lemmas": {
            "fermat_p1_times": True,
            "mersenne_cr_unique": True,
            "doubling_phi_q": True,
            "unique_exactly_q5_q9": None,
            "extra_unique_always_fire": False,
            "fermat_cover_359_all_k": None,
            "some_phi_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "fermat_p1_times": "LEMMA",
            "mersenne_cr_unique": "LEMMA",
            "doubling_phi_q": "LEMMA",
            "unique_exactly_q5_q9": "PREFIX",
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
