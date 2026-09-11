#!/usr/bin/env python3
"""Cycle BB: five sextuples; ten even septuple seeds; bit 22 contributes 1.

For a>=8 there are no even half-window sextuples, so the five sextuples
are the odd-lift orbit of a=7's packed bits {66,67,71,77,85}. For a>=9
the even septuples of G are exactly 2^a-{22,30,36,52,66,68,98,100,130,194}.
Packed bit 22 is the j=0 member of the 21-family (a septuple for k>=6)
and contributes 1 via Cycle BA's period-4 tails. Sextuple XOR and
septuple XOR are not I_k. Nested left is still not a formula for I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_bb.py --certify
Dump: research/cycle_bb.json
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
SEX_SEEDS = [66, 67, 71, 77, 85]
SEX_EVEN_AT = {5: {20, 22}, 6: {34, 36}, 7: {66}}
SEP_Q = (22, 30, 36, 52, 66, 68, 98, 100, 130, 194)
SEP_S = {
    22: [1, 2, 5, 6, 8, 9, 10],
    30: [0, 1, 2, 9, 10, 13, 14],
    36: [0, 1, 2, 3, 5, 9, 17],
    52: [1, 16, 17, 18, 19, 21, 25],
    66: [0, 1, 2, 4, 8, 16, 32],
    68: [0, 2, 3, 5, 9, 17, 33],
    98: [0, 32, 33, 34, 36, 40, 48],
    100: [1, 32, 34, 35, 37, 41, 49],
    130: [1, 2, 4, 8, 16, 32, 64],
    194: [0, 65, 66, 68, 72, 80, 96],
}
SEP_Q_AMIN = {
    22: 6, 30: 6, 36: 7, 52: 7,
    66: 8, 68: 8, 98: 8, 100: 8,
    130: 9, 194: 9,
}
SEP_R_AMIN = {q - 1: amin for q, amin in SEP_Q_AMIN.items()}
SEP_EVEN_AT = {
    6: {22, 30},
    7: {22, 30, 36, 52},
    8: {22, 30, 36, 52, 66, 68, 98, 100},
}


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


def support(a: int, D: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    return [n for n in range(nmax + 1) if G(n, D)]


def ones_s(a: int, q: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    D = (1 << a) - q
    return sorted(nmax - n for n in range(nmax + 1) if G(n, D))


def sep_s_sets_ok(amax: int) -> bool:
    for q, amin in SEP_Q_AMIN.items():
        want = SEP_S[q]
        for a in range(amin, amax + 1):
            if ones_s(a, q) != want:
                return False
    return True


def even_qs(a: int, sz: int) -> set[int]:
    nmax = (1 << (a - 1)) - 1
    return {(1 << a) - D for D in range(0, 2 * nmax + 1, 2)
            if len(support(a, D)) == sz}


def even_sextuples_ok(amax: int) -> bool:
    for a in range(5, amax + 1):
        got = even_qs(a, 6)
        want = SEX_EVEN_AT.get(a, set())
        if got != want:
            return False
    return True


def even_septuples_ok(amax: int) -> bool:
    for a in range(6, amax + 1):
        got = even_qs(a, 7)
        want = set(SEP_Q) if a >= 9 else SEP_EVEN_AT[a]
        if got != want:
            return False
    return True


def odd_lifts_ok(amax: int, sz: int) -> bool:
    for a in range(6, amax + 1):
        nmax = (1 << (a - 1)) - 1
        prev = {D for D in range(0, 2 * ((1 << (a - 2)) - 1) + 1)
                if len(support(a - 1, D)) == sz}
        lifted = {2 * d + 1 for d in prev}
        got = {D for D in range(1, 2 * nmax + 1, 2) if len(support(a, D)) == sz}
        if got != lifted:
            return False
    return True


def even_count(B: set[int], A: set[int]) -> int:
    return len(B) + 2 * len(A - B)


def sex_mech_ok(cmax: int) -> bool:
    """Even |S|=6 mechanisms: none for c>=7."""
    want = {
        4: {22, 20},
        5: {36, 34},
        6: {66},
    }
    for c in range(4, cmax + 1):
        nmax = (1 << (c - 1)) - 1
        qs = set()
        for D in range(0, 2 * nmax + 1):
            e = D + 1
            if e > 2 * nmax:
                continue
            B = set(support(c, D))
            A = set(support(c, e))
            if even_count(B, A) == 6:
                qs.add((1 << (c + 1)) - 2 * e)
        if qs != want.get(c, set()):
            return False
    return True


def sep_mech_ok(cmax: int) -> bool:
    """Even |S|=7 mechanisms produce the seed q-list and no extras."""
    for c in range(5, cmax + 1):
        nmax = (1 << (c - 1)) - 1
        qs = set()
        for D in range(0, 2 * nmax + 1):
            e = D + 1
            if e > 2 * nmax:
                continue
            B = set(support(c, D))
            A = set(support(c, e))
            if even_count(B, A) == 7:
                qs.add((1 << (c + 1)) - 2 * e)
        a = c + 1
        want = set(SEP_Q) if a >= 9 else SEP_EVEN_AT[a]
        if qs != want:
            return False
    return True


def expected_sex_p(k: int) -> list[int]:
    if k == 5:
        return [20, 22]
    if k == 6:
        return [34, 36, 39, 43]
    j = k - 7
    if j < 0:
        return []
    return sorted((1 << j) * (s - 1) + 1 for s in SEX_SEEDS)


def expected_sep_p(k: int) -> list[int]:
    out = []
    for r, amin in SEP_R_AMIN.items():
        for j in range(0, max(0, k - amin + 1)):
            out.append(r * (1 << j) + 1)
    return sorted(out)


def expected_sep_times(k: int, r: int, j: int) -> list[int]:
    T = 1 << (k - 1)
    return [T + s * (1 << j) for s in SEP_S[r + 1]]


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
    sex = sorted(p for p, ts in by_p.items() if len(ts) == 6)
    sep = sorted(p for p, ts in by_p.items() if len(ts) == 7)
    return {
        "T": T,
        "n6": len(sex),
        "sex": sex,
        "n7": len(sep),
        "sep": sep,
        "times": {p: by_p[p] for p in sex + sep},
        "t22": by_p.get(22, []),
    }


def family_times_ok(k: int, cen: dict) -> bool:
    for r, amin in SEP_R_AMIN.items():
        for j in range(0, max(0, k - amin + 1)):
            p = r * (1 << j) + 1
            if cen["times"].get(p) != expected_sep_times(k, r, j):
                return False
    return True


def xor_fires(rows: list[int], p: int, ts: list[int]) -> int:
    x = 0
    for t in ts:
        x ^= fires(rows[t], p)
    return x


def self_checks(
    c20, ssets, even6, even7, lift6, lift7, mech6, mech7, recs, miss6, miss7,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ssets and even6 and even7 and lift6 and lift7 and mech6 and mech7
    vals = []
    for rec in recs:
        k = rec["k"]
        assert rec["sex"] == rec["expected6"]
        assert rec["sep"] == rec["expected7"]
        if k >= 7:
            assert rec["n6"] == 5
        if k >= 6:
            assert rec["x22"] == 1
            assert rec["fire22"] == [0, 0, 0, 0, 1, 0, 0]
            vals.append(rec["I"])
        if k >= 6:
            assert rec["family_times"]
    assert miss6 and miss7
    assert 0 in vals and 1 in vals
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ssets = sep_s_sets_ok(12)
    even6 = even_sextuples_ok(12)
    even7 = even_septuples_ok(12)
    lift6 = odd_lifts_ok(12, 6)
    lift7 = odd_lifts_ok(12, 7)
    mech6 = sex_mech_ok(11)
    mech7 = sep_mech_ok(11)

    k_ann = 8
    rows = evolve_rows(1 << k_ann)
    recs = []
    miss6 = []
    miss7 = []
    for k in range(5, k_ann + 1):
        cen = hit_census(k)
        T = cen["T"]
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        x6 = 0
        for p in cen["sex"]:
            x6 ^= xor_fires(rows, p, cen["times"][p])
        x7 = 0
        for p in cen["sep"]:
            x7 ^= xor_fires(rows, p, cen["times"][p])
        if x6 != I:
            miss6.append(k)
        if cen["sep"] and x7 != I:
            miss7.append(k)
        f22 = [fires(rows[t], 22) for t in cen["t22"]]
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "n6": cen["n6"],
            "n7": cen["n7"],
            "sex": cen["sex"],
            "sep": cen["sep"],
            "expected6": expected_sex_p(k),
            "expected7": expected_sep_p(k),
            "family_times": family_times_ok(k, cen) if k >= 6 else True,
            "sex_xor": x6,
            "sep_xor": x7,
            "t22": cen["t22"],
            "fire22": f22,
            "x22": xor_fires(rows, 22, cen["t22"]) if cen["t22"] else None,
        })
    checks = self_checks(
        c20, ssets, even6, even7, lift6, lift7, mech6, mech7,
        recs, miss6, miss7,
    )
    dump = {
        "cycle": "BB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "sep_s_sets": ssets,
            "even_sextuples": even6,
            "even_septuples": even7,
            "odd_lifts_6": lift6,
            "odd_lifts_7": lift7,
            "sex_mechanisms": mech6,
            "sep_mechanisms": mech7,
        },
        "annulus": recs,
        "sex_xor_mismatch_k": miss6,
        "sep_xor_mismatch_k": miss7,
        "lemmas": {
            "no_even_sextuples_a_ge_8": True,
            "exactly_five_sextuples": True,
            "even_septuples_exactly_ten": True,
            "septuples_are_ten_families": True,
            "bit22_contributes_1": True,
            "sex_xor_is_I": False,
            "sep_xor_is_I": False,
            "nested_left_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "no_even_sextuples_a_ge_8": "LEMMA",
            "exactly_five_sextuples": "LEMMA",
            "even_septuples_exactly_ten": "LEMMA",
            "septuples_are_ten_families": "LEMMA",
            "bit22_contributes_1": "LEMMA",
            "sex_xor_is_I": "KILLED",
            "sep_xor_is_I": "KILLED",
            "nested_left_is_I": "KILLED",
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
        {key: rec[key] for key in rec if key not in ("sex", "sep", "t22")}
        for rec in recs
    ])
    print("sex_xor_mismatch_k", miss6)
    print("sep_xor_mismatch_k", miss7)


if __name__ == "__main__":
    main()
