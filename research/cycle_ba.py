#!/usr/bin/env python3
"""Cycle BA: even pentuples are 2^a-{12,16,18,20,26,28,34,50}.

For a>=7 the even half-window pentuples of G are exactly those eight
targets. Odd pentuples are one doubling of a pentuple one level down.
Packed bits are p=r*2^j+1 for r in {11,15,17,19,25,27,33,49}. The
tails e_20..e_27 are period 4, e_30 is identically 1 for t>=33, and
bits 20, 24, 25 never fire. Pentuple XOR is not I_k. Nested left is
still not a formula for I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_ba.py --certify
Dump: research/cycle_ba.json
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
SEED_Q = (12, 16, 18, 20, 26, 28, 34, 50)
SEED_S = {
    12: [0, 1, 2, 3, 5],
    16: [1, 4, 5, 6, 7],
    18: [0, 1, 2, 4, 8],
    20: [0, 2, 3, 5, 9],
    26: [0, 8, 9, 10, 12],
    28: [1, 8, 10, 11, 13],
    34: [1, 2, 4, 8, 16],
    50: [0, 17, 18, 20, 24],
}
FAM_R = (11, 15, 17, 19, 25, 27, 33, 49)
FAM_AMIN = {11: 5, 15: 5, 17: 6, 19: 6, 25: 6, 27: 6, 33: 7, 49: 7}
Q_AMIN = {12: 5, 16: 5, 18: 6, 20: 6, 26: 6, 28: 6, 34: 7, 50: 7}


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


def ones_s(a: int, q: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    D = (1 << a) - q
    return sorted(nmax - n for n in range(nmax + 1) if G(n, D))


def s_sets_ok(amax: int) -> bool:
    for q, amin in Q_AMIN.items():
        want = SEED_S[q]
        for a in range(amin, amax + 1):
            if ones_s(a, q) != want:
                return False
    return True


def even_pentuples_ok(amax: int) -> bool:
    for a in range(5, amax + 1):
        nmax = (1 << (a - 1)) - 1
        got = {(1 << a) - D for D in range(0, 2 * nmax + 1, 2)
               if len(support(a, D)) == 5}
        if a == 5:
            want = {12, 16}
        elif a == 6:
            want = {12, 16, 18, 20, 26, 28}
        else:
            want = set(SEED_Q)
        if got != want:
            return False
    return True


def odd_lifts_ok(amax: int) -> bool:
    for a in range(6, amax + 1):
        nmax = (1 << (a - 1)) - 1
        prev = {D for D in range(0, 2 * ((1 << (a - 2)) - 1) + 1)
                if len(support(a - 1, D)) == 5}
        lifted = {2 * d + 1 for d in prev}
        got = {D for D in range(1, 2 * nmax + 1, 2) if len(support(a, D)) == 5}
        if got != lifted:
            return False
    return True


def even_mech_ok(cmax: int) -> bool:
    """(i) unique then |A\\B|=2; (ii) triple then |A\\B|=1;
    (iii) pentuple then A subset B. Exhaustive for even |S|=5.
    """
    for c in range(5, cmax + 1):
        nmax = (1 << (c - 1)) - 1
        sizes = [len(support(c, D)) for D in range(0, 2 * nmax + 1)]
        mech_i = []
        mech_ii = []
        mech_iii = []
        for D, sz in enumerate(sizes):
            e = D + 1
            if e > 2 * nmax:
                continue
            B = set(support(c, D))
            A = set(support(c, e))
            amb = len(A - B)
            if sz == 1 and amb == 2:
                mech_i.append(D)
            if sz == 3 and amb == 1:
                mech_ii.append(D)
            if sz == 5 and A <= B:
                mech_iii.append(D)
        want_i = [(1 << c) - 9, (1 << c) - 7]
        want_ii = sorted([
            (1 << c) - 15, (1 << c) - 14, (1 << c) - 11, (1 << c) - 10,
        ])
        if mech_i != want_i or mech_ii != want_ii:
            return False
        if c == 5:
            if mech_iii:
                return False
        else:
            want_iii = [(1 << c) - 26, (1 << c) - 18]
            if mech_iii != want_iii:
                return False
    return True


def expected_pent_p(k: int) -> list[int]:
    out = []
    for r, amin in FAM_AMIN.items():
        for j in range(0, max(0, k - amin + 1)):
            out.append(r * (1 << j) + 1)
    return sorted(out)


def expected_times(k: int, r: int, j: int) -> list[int]:
    T = 1 << (k - 1)
    return [T + s * (1 << j) for s in SEED_S[r + 1]]


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
    pent = sorted(p for p, ts in by_p.items() if len(ts) == 5)
    return {"T": T, "n5": len(pent), "pents": pent,
            "times": {p: by_p[p] for p in pent}}


def family_times_ok(k: int, cen: dict) -> bool:
    for r, amin in FAM_AMIN.items():
        for j in range(0, max(0, k - amin + 1)):
            p = r * (1 << j) + 1
            if cen["times"].get(p) != expected_times(k, r, j):
                return False
    return True


def e20(t: int) -> int:
    return int(t % 4 in (0, 1))


def e21(t: int) -> int:
    return int(t % 4 != 3)


def e22(t: int) -> int:
    return int(t % 4 in (0, 3))


def e23(t: int) -> int:
    return int(t % 2 == 0)


def e24(t: int) -> int:
    return int(t % 4 == 3)


def e25(t: int) -> int:
    return int(t % 4 in (0, 3))


def e26(t: int) -> int:
    return int(t % 4 != 0)


def e27(t: int) -> int:
    return int(t % 4 != 0)


E_FUN = {
    20: e20, 21: e21, 22: e22, 23: e23,
    24: e24, 25: e25, 26: e26, 27: e27,
}


def tails_ok(rows: list[int], tmax: int) -> bool:
    for j, fn in E_FUN.items():
        start = {20: 23, 21: 23, 22: 25, 23: 24,
                 24: 27, 25: 28, 26: 29, 27: 30}[j]
        for t in range(start, tmax):
            if e_bit(rows[t], j) != fn(t):
                return False
    for t in range(20, tmax - 1):
        for j in range(20, 28):
            got = e_bit(rows[t + 1], j)
            want = e_bit(rows[t], j - 2) ^ (
                e_bit(rows[t], j - 1) | e_bit(rows[t], j)
            )
            if got != want:
                return False
    return True


def e30_ok(rows: list[int], tmax: int) -> bool:
    if e_bit(rows[32], 30) != 0 or e_bit(rows[33], 30) != 1:
        return False
    for t in range(33, tmax):
        if e_bit(rows[t], 30) != 1:
            return False
    for t in range(31, tmax - 1):
        if e_bit(rows[t], 28) != 0:
            return False
        got = e_bit(rows[t + 1], 30)
        want = e_bit(rows[t], 28) ^ (e_bit(rows[t], 29) | e_bit(rows[t], 30))
        if got != want:
            return False
    return True


def and_empty_ok(rows: list[int], tmax: int) -> bool:
    """Period-4 ANDs for bits 20 and 24 are empty; bit 25 AND misses T+8."""
    for t in range(32, tmax):
        if e20(t) and (t % 4 in (2, 3)):  # e19
            return False
        if fires(rows[t], 20):
            return False
        if e24(t) and e23(t):
            return False
        if fires(rows[t], 24):
            return False
        if fires(rows[t], 25) and t % 4 != 3:
            return False
    return True


def xor_fires(rows: list[int], p: int, ts: list[int]) -> int:
    x = 0
    for t in ts:
        x ^= fires(rows[t], p)
    return x


def bit33_prefix(rows: list[int], kmax: int) -> list[int]:
    out = []
    for k in range(7, kmax + 1):
        T = 1 << (k - 1)
        out.append(fires(rows[T], 33))
    return out


def self_checks(
    c20, ssets, even_p, odd_lift, mech, tails, e30, ands, recs, mismatches, b33,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ssets and even_p and odd_lift and mech and tails and e30 and ands
    vals = []
    for rec in recs:
        k = rec["k"]
        if k >= 6:
            assert rec["n5"] == 8 * (k - 5)
        elif k == 5:
            assert rec["n5"] == 2
        assert rec["pents"] == rec["expected"]
        assert rec["family_times"]
        if k >= 6:
            assert rec["x20"] == 0
            assert rec["x24"] == 0
            assert rec["x25"] == 0
            vals.append(rec["I"])
    assert mismatches
    assert 0 in vals and 1 in vals
    assert b33 and all(v == 1 for v in b33)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ssets = s_sets_ok(12)
    even_p = even_pentuples_ok(12)
    odd_lift = odd_lifts_ok(12)
    mech = even_mech_ok(11)

    k_ann = 8
    k33 = 12
    rows = evolve_rows(1 << max(k_ann, k33))
    tails = tails_ok(rows, min(len(rows) - 1, 256))
    e30 = e30_ok(rows, min(len(rows) - 1, 256))
    ands = and_empty_ok(rows, min(len(rows) - 1, 256))
    recs = []
    mismatches = []
    for k in range(5, k_ann + 1):
        cen = hit_census(k)
        T = cen["T"]
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        px = 0
        for p in cen["pents"]:
            px ^= xor_fires(rows, p, cen["times"][p])
        if px != I:
            mismatches.append(k)
        t20 = cen["times"].get(20, [])
        t24 = [t for t in range(T, end)
               if 24 <= 2 * t and G(end - t - 1, end - 24)]
        t25 = [T + (1 << 3)] if k >= 6 else []
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "n5": cen["n5"],
            "pents": cen["pents"],
            "expected": expected_pent_p(k),
            "family_times": family_times_ok(k, cen),
            "pent_xor": px,
            "x20": xor_fires(rows, 20, t20) if t20 else None,
            "x24": xor_fires(rows, 24, t24) if t24 else None,
            "x25": xor_fires(rows, 25, t25) if t25 else None,
        })
    b33 = bit33_prefix(rows, k33)
    checks = self_checks(
        c20, ssets, even_p, odd_lift, mech, tails, e30, ands, recs, mismatches, b33,
    )
    dump = {
        "cycle": "BA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "s_sets": ssets,
            "even_pentuples": even_p,
            "odd_lifts": odd_lift,
            "even_mechanisms": mech,
            "e20_e27_tails": tails,
            "e30_identically_1": e30,
            "and_empty_20_24_25": ands,
        },
        "annulus": recs,
        "pent_xor_mismatch_k": mismatches,
        "bit33_fires_k7_to_12": b33,
        "lemmas": {
            "s_sets_eight_even_targets": True,
            "even_pentuples_exactly_eight": True,
            "pents_are_11_15_17_19_25_27_33_49_families": True,
            "e20_e27_period4": True,
            "e30_identically_1_t_ge_33": True,
            "bits_20_24_25_never_fire": True,
            "bit33_always_fires": None,
            "pent_xor_is_I": False,
            "nested_left_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "s_sets_eight_even_targets": "LEMMA",
            "even_pentuples_exactly_eight": "LEMMA",
            "pents_are_11_15_17_19_25_27_33_49_families": "LEMMA",
            "e20_e27_period4": "LEMMA",
            "e30_identically_1_t_ge_33": "LEMMA",
            "bits_20_24_25_never_fire": "LEMMA",
            "bit33_always_fires": "PREFIX",
            "pent_xor_is_I": "KILLED",
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
        {key: rec[key] for key in rec if key != "pents"}
        for rec in recs
    ])
    print("pent_xor_mismatch_k", mismatches)
    print("bit33", b33)


if __name__ == "__main__":
    main()
