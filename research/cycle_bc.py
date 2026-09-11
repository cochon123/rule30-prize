#!/usr/bin/env python3
"""Cycle BC: eleven octuples; ten even nonuple seeds.

For a>=10 there are no even half-window octuples, so the eleven
octuples are the odd-lift orbit of a=9's packed bits
{258,259,263,269,329,369,393,401,433,465,481}. For a>=11 the even
nonuples of G are exactly
2^a-{38,54,132,196,258,260,386,388,514,770}. Octuple XOR and nonuple
XOR are not I_k. Nested left is still not a formula for I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_bc.py --certify
Dump: research/cycle_bc.json
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
OCT_SEEDS = [258, 259, 263, 269, 329, 369, 393, 401, 433, 465, 481]
OCT_EARLY = {
    5: [24, 26, 28, 30, 31],
    6: [42, 47, 50, 51, 55, 59, 61],
    7: [68, 83, 93, 99, 101, 109, 117, 121],
    8: [130, 132, 135, 165, 185, 197, 201, 217, 233, 241],
}
OCT_EVEN_AT = {
    5: {24, 26, 28, 30},
    6: {42, 50},
    7: {68},
    8: {130, 132},
    9: {258},
}
NON_Q = (38, 54, 132, 196, 258, 260, 386, 388, 514, 770)
NON_S = {
    38: [0, 5, 6, 8, 9, 10, 16, 17, 18],
    54: [0, 1, 2, 16, 21, 22, 24, 25, 26],
    132: [0, 1, 2, 3, 5, 9, 17, 33, 65],
    196: [1, 64, 65, 66, 67, 69, 73, 81, 97],
    258: [0, 1, 2, 4, 8, 16, 32, 64, 128],
    260: [0, 2, 3, 5, 9, 17, 33, 65, 129],
    386: [0, 128, 129, 130, 132, 136, 144, 160, 192],
    388: [1, 128, 130, 131, 133, 137, 145, 161, 193],
    514: [1, 2, 4, 8, 16, 32, 64, 128, 256],
    770: [0, 257, 258, 260, 264, 272, 288, 320, 384],
}
NON_Q_AMIN = {
    38: 7, 54: 7, 132: 9, 196: 9,
    258: 10, 260: 10, 386: 10, 388: 10,
    514: 11, 770: 11,
}
NON_R_AMIN = {q - 1: amin for q, amin in NON_Q_AMIN.items()}
NON_EVEN_AT = {
    7: {38, 54},
    8: {38, 54},
    9: {38, 54, 132, 196},
    10: {38, 54, 132, 196, 258, 260, 386, 388},
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


def non_s_sets_ok(amax: int) -> bool:
    for q, amin in NON_Q_AMIN.items():
        want = NON_S[q]
        for a in range(amin, amax + 1):
            if ones_s(a, q) != want:
                return False
    return True


def even_qs(a: int, sz: int) -> set[int]:
    nmax = (1 << (a - 1)) - 1
    return {(1 << a) - D for D in range(0, 2 * nmax + 1, 2)
            if len(support(a, D)) == sz}


def even_octuples_ok(amax: int) -> bool:
    for a in range(5, amax + 1):
        got = even_qs(a, 8)
        want = OCT_EVEN_AT.get(a, set())
        if got != want:
            return False
    return True


def even_nonuples_ok(amax: int) -> bool:
    for a in range(7, amax + 1):
        got = even_qs(a, 9)
        want = set(NON_Q) if a >= 11 else NON_EVEN_AT[a]
        if got != want:
            return False
    return True


def odd_lifts_ok(amax: int, sz: int, amin: int) -> bool:
    for a in range(amin, amax + 1):
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


def mech_qs(c: int, target: int) -> set[int]:
    nmax = (1 << (c - 1)) - 1
    qs = set()
    for D in range(0, 2 * nmax + 1):
        e = D + 1
        if e > 2 * nmax:
            continue
        B = set(support(c, D))
        A = set(support(c, e))
        if even_count(B, A) == target:
            qs.add((1 << (c + 1)) - 2 * e)
    return qs


def oct_mech_ok(cmax: int) -> bool:
    want = {
        4: {30, 28, 26, 24},
        5: {50, 42},
        6: {68},
        7: {132, 130},
        8: {258},
    }
    for c in range(4, cmax + 1):
        if mech_qs(c, 8) != want.get(c, set()):
            return False
    return True


def non_mech_ok(cmax: int) -> bool:
    for c in range(6, cmax + 1):
        a = c + 1
        want = set(NON_Q) if a >= 11 else NON_EVEN_AT.get(a, set())
        if mech_qs(c, 9) != want:
            return False
    return True


def expected_oct_p(k: int) -> list[int]:
    if k in OCT_EARLY:
        return list(OCT_EARLY[k])
    j = k - 9
    if j < 0:
        return []
    return sorted((1 << j) * (s - 1) + 1 for s in OCT_SEEDS)


def expected_non_p(k: int) -> list[int]:
    out = []
    for r, amin in NON_R_AMIN.items():
        for j in range(0, max(0, k - amin + 1)):
            out.append(r * (1 << j) + 1)
    return sorted(out)


def expected_non_times(k: int, r: int, j: int) -> list[int]:
    T = 1 << (k - 1)
    return [T + s * (1 << j) for s in NON_S[r + 1]]


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
    octu = sorted(p for p, ts in by_p.items() if len(ts) == 8)
    nonu = sorted(p for p, ts in by_p.items() if len(ts) == 9)
    return {
        "T": T,
        "n8": len(octu),
        "oct": octu,
        "n9": len(nonu),
        "non": nonu,
        "times": {p: by_p[p] for p in octu + nonu},
    }


def family_times_ok(k: int, cen: dict) -> bool:
    for r, amin in NON_R_AMIN.items():
        for j in range(0, max(0, k - amin + 1)):
            p = r * (1 << j) + 1
            if cen["times"].get(p) != expected_non_times(k, r, j):
                return False
    return True


def xor_fires(rows: list[int], p: int, ts: list[int]) -> int:
    x = 0
    for t in ts:
        x ^= fires(rows[t], p)
    return x


def self_checks(
    c20, ssets, even8, even9, lift8, lift9, mech8, mech9, recs, miss8, miss9,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ssets and even8 and even9 and lift8 and lift9 and mech8 and mech9
    vals = []
    for rec in recs:
        k = rec["k"]
        assert rec["oct"] == rec["expected8"]
        assert rec["non"] == rec["expected9"]
        if k >= 9:
            assert rec["n8"] == 11
        if k >= 7:
            assert rec["family_times"]
            vals.append(rec["I"])
    assert miss8 and miss9
    assert 0 in vals and 1 in vals
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ssets = non_s_sets_ok(12)
    even8 = even_octuples_ok(12)
    even9 = even_nonuples_ok(12)
    lift8 = odd_lifts_ok(12, 8, 6)
    lift9 = odd_lifts_ok(12, 9, 8)
    mech8 = oct_mech_ok(11)
    mech9 = non_mech_ok(11)

    k_ann = 9
    rows = evolve_rows(1 << k_ann)
    recs = []
    miss8 = []
    miss9 = []
    for k in range(5, k_ann + 1):
        cen = hit_census(k)
        T = cen["T"]
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        x8 = 0
        for p in cen["oct"]:
            x8 ^= xor_fires(rows, p, cen["times"][p])
        x9 = 0
        for p in cen["non"]:
            x9 ^= xor_fires(rows, p, cen["times"][p])
        if x8 != I:
            miss8.append(k)
        if cen["non"] and x9 != I:
            miss9.append(k)
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "n8": cen["n8"],
            "n9": cen["n9"],
            "oct": cen["oct"],
            "non": cen["non"],
            "expected8": expected_oct_p(k),
            "expected9": expected_non_p(k),
            "family_times": family_times_ok(k, cen) if k >= 7 else True,
            "oct_xor": x8,
            "non_xor": x9,
        })
    checks = self_checks(
        c20, ssets, even8, even9, lift8, lift9, mech8, mech9,
        recs, miss8, miss9,
    )
    dump = {
        "cycle": "BC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "non_s_sets": ssets,
            "even_octuples": even8,
            "even_nonuples": even9,
            "odd_lifts_8": lift8,
            "odd_lifts_9": lift9,
            "oct_mechanisms": mech8,
            "non_mechanisms": mech9,
        },
        "annulus": recs,
        "oct_xor_mismatch_k": miss8,
        "non_xor_mismatch_k": miss9,
        "lemmas": {
            "no_even_octuples_a_ge_10": True,
            "exactly_eleven_octuples": True,
            "even_nonuples_exactly_ten": True,
            "nonuples_are_ten_families": True,
            "oct_xor_is_I": False,
            "non_xor_is_I": False,
            "nested_left_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "no_even_octuples_a_ge_10": "LEMMA",
            "exactly_eleven_octuples": "LEMMA",
            "even_nonuples_exactly_ten": "LEMMA",
            "nonuples_are_ten_families": "LEMMA",
            "oct_xor_is_I": "KILLED",
            "non_xor_is_I": "KILLED",
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
        {key: rec[key] for key in rec if key not in ("oct", "non")}
        for rec in recs
    ])
    print("oct_xor_mismatch_k", miss8)
    print("non_xor_mismatch_k", miss9)


if __name__ == "__main__":
    main()
