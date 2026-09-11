#!/usr/bin/env python3
"""Cycle AV: unique half-window G-supports are exactly the AS families.

On n < 2^{a-1}, |{n: G(n,D)=1}|=1 if and only if D is a 2-family or
3-family target from Cycle AS. The doubling recurrence plus the W
interval of Cycle AN make this an induction, not a prefix. Unique-Green
packed bits for I_k are therefore exactly p=2^j+1 and p=3*2^j+1
(j<=k-3). Period-4 tails e_13..e_17 make bits 13 and 17 contribute 0.
The remaining unique 3-family is not identically 0 (k=15), and the
right-half double p=3T/2+1 does not have XOR 0 (k=12).

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_av.py --certify
Dump: research/cycle_av.json
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


def family_D(a: int) -> set[int]:
    out = {(1 << a) - (1 << j) - 1 for j in range(a)}
    for j in range(max(0, a - 2)):
        if j <= a - 3:
            out.add((1 << a) - 3 * (1 << j) - 1)
    return out


def unique_even_ok(bmax: int) -> bool:
    for b in range(2, bmax + 1):
        nmax = (1 << (b - 1)) - 1
        found = []
        for E in range(0, 2 * nmax + 1, 2):
            if len(support(b, E)) == 1:
                found.append(E)
        want = [(1 << b) - 2]
        if b >= 3:
            want.append((1 << b) - 4)
        if sorted(found) != sorted(want):
            return False
    return True


def unique_D_families_ok(amax: int) -> bool:
    for a in range(2, amax + 1):
        nmax = (1 << (a - 1)) - 1
        fam = family_D(a)
        extra = []
        missing = set(fam)
        for D in range(0, 2 * nmax + 1):
            sl = support(a, D)
            if len(sl) == 1:
                if D not in fam:
                    extra.append(D)
                else:
                    missing.discard(D)
            elif D in fam:
                return False
        if extra or missing:
            return False
    return True


def odd_doubling_ok(amax: int) -> bool:
    """G(2l+1, 2d+1)=G(l,d); unique odd D=2d+1 iff d unique one level down."""
    for a in range(2, amax + 1):
        nmax = (1 << (a - 1)) - 1
        prev_max = (1 << (a - 2)) - 1
        for d in range(0, prev_max + 1):
            D = 2 * d + 1
            got = support(a, D)
            want = [2 * ell + 1 for ell in support(a - 1, d)]
            if got != want:
                return False
    return True


def even_count_ok(bmax: int) -> bool:
    """|S(b, 2e)| = |B| + 2|A\\B| with A=S(b-1,e), B=S(b-1,e-1)."""
    for b in range(2, bmax + 1):
        nmax = (1 << (b - 1)) - 1
        for e in range(0, nmax + 1):
            E = 2 * e
            A = set(support(b - 1, e))
            B = set(support(b - 1, e - 1)) if e >= 1 else set()
            sl = support(b, E)
            want = len(B) + 2 * len(A - B)
            if len(sl) != want:
                return False
    return True


def consecutive_same_support_ok(amax: int) -> bool:
    for a in range(2, amax + 1):
        nmax = (1 << (a - 1)) - 1
        uniq = []
        for D in range(0, 2 * nmax + 1):
            sl = support(a, D)
            if len(sl) == 1:
                uniq.append((D, sl[0]))
        same = [
            (uniq[i], uniq[i + 1])
            for i in range(len(uniq) - 1)
            if uniq[i + 1][0] == uniq[i][0] + 1 and uniq[i][1] == uniq[i + 1][1]
        ]
        want_pair = (((1 << a) - 3, (1 << (a - 1)) - 1),
                     ((1 << a) - 2, (1 << (a - 1)) - 1))
        if same != [want_pair]:
            return False
    return True


def w_interval_uniques_ok(amax: int) -> bool:
    """Unique D live in the Cycle AN interval [2^{a-1}-1, 2^a-2]."""
    for a in range(2, amax + 1):
        nmax = (1 << (a - 1)) - 1
        lo, hi = nmax, (1 << a) - 2
        for D in range(0, 2 * nmax + 1):
            if len(support(a, D)) == 1 and not (lo <= D <= hi):
                return False
    return True


def family_n_ok(amax: int) -> bool:
    for a in range(2, amax + 1):
        n_two = (1 << (a - 1)) - 1
        for j in range(a):
            D = (1 << a) - (1 << j) - 1
            if support(a, D) != [n_two]:
                return False
        for j in range(0, max(0, a - 2)):
            if j > a - 3:
                continue
            D = (1 << a) - 3 * (1 << j) - 1
            want = n_two - (1 << j)
            if support(a, D) != [want]:
                return False
    return True


def e13(t: int) -> int:
    return int(t % 4 != 3)


def e14(t: int) -> int:
    return int(t % 4 in (0, 1))


def e15(t: int) -> int:
    return int(t % 4 in (0, 3))


def e16(t: int) -> int:
    return int(t % 4 != 1)


def e17(t: int) -> int:
    return int(t % 4 == 3)


def tails_ok(rows: list[int], tmax: int) -> bool:
    formulas = {13: e13, 14: e14, 15: e15, 16: e16, 17: e17}
    onsets = {13: 13, 14: 14, 15: 15, 16: 16, 17: 16}
    for j, f in formulas.items():
        for t in range(onsets[j], tmax):
            if e_bit(rows[t], j) != f(t):
                return False
    # recurrences on the tail, using AU's e_11, e_12
    for t in range(16, tmax - 1):
        e11 = int((t % 4) == 2)
        e12 = int((t % 4) != 0)
        got13 = e_bit(rows[t + 1], 13)
        want13 = e11 ^ (e12 | e_bit(rows[t], 13))
        if got13 != want13:
            return False
        got14 = e_bit(rows[t + 1], 14)
        want14 = e12 ^ (e_bit(rows[t], 13) | e_bit(rows[t], 14))
        if got14 != want14:
            return False
        got15 = e_bit(rows[t + 1], 15)
        want15 = e_bit(rows[t], 13) ^ (e_bit(rows[t], 14) | e_bit(rows[t], 15))
        if got15 != want15:
            return False
        got16 = e_bit(rows[t + 1], 16)
        want16 = e_bit(rows[t], 14) ^ (e_bit(rows[t], 15) | e_bit(rows[t], 16))
        if got16 != want16:
            return False
        got17 = e_bit(rows[t + 1], 17)
        want17 = e_bit(rows[t], 15) ^ (e_bit(rows[t], 16) | e_bit(rows[t], 17))
        if got17 != want17:
            return False
    return True


def expected_unique(k: int) -> list[int]:
    twos = [(1 << j) + 1 for j in range(k)]
    threes = [3 * (1 << j) + 1 for j in range(k - 2)]
    return sorted(twos + threes)


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
    uniq = sorted(p for p, ts in by_p.items() if len(ts) == 1)
    dbl = sorted(p for p, ts in by_p.items() if len(ts) == 2)
    return {
        "T": T,
        "n1": len(uniq),
        "n2": len(dbl),
        "uniq": uniq,
        "doubles": dbl,
        "expected_uniq": expected_unique(k),
    }


def bit13_17_zero(rows: list[int], kmax: int) -> bool:
    for k in range(5, kmax + 1):
        T = 1 << (k - 1)
        if fires(rows[T + 4], 13) != 0:
            return False
        if fires(rows[T], 17) != 0:
            return False
    return True


def self_checks(
    c20,
    even_ok: bool,
    fam_ok: bool,
    odd_ok: bool,
    even_count: bool,
    consec: bool,
    w_ok: bool,
    n_ok: bool,
    tails: bool,
    bits_zero: bool,
    recs: list[dict],
    kill_3fam: dict,
    kill_double: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert even_ok and fam_ok and odd_ok and even_count
    assert consec and w_ok and n_ok and tails and bits_zero
    for rec in recs:
        assert rec["n1"] == 2 * rec["k"] - 2
        assert rec["uniq"] == rec["expected_uniq"]
    assert kill_3fam["fire"] == 1 and kill_3fam["p"] >= 13
    assert kill_double["xor"] == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    even_ok = unique_even_ok(12)
    fam_ok = unique_D_families_ok(12)
    odd_ok = odd_doubling_ok(12)
    even_count = even_count_ok(10)
    consec = consecutive_same_support_ok(12)
    w_ok = w_interval_uniques_ok(12)
    n_ok = family_n_ok(12)

    k_ann = 8
    t_kill = (1 << 14) + (1 << 12)  # k=15, t=T+2^{12}=20480
    rows = evolve_rows(max(1 << k_ann, t_kill, 256))
    tails = tails_ok(rows, min(len(rows) - 1, 256))
    bits_zero = bit13_17_zero(rows, 12)

    recs = []
    for k in range(4, k_ann + 1):
        cen = hit_census(k)
        recs.append({
            "k": k,
            "T": cen["T"],
            "n1": cen["n1"],
            "n2": cen["n2"],
            "uniq": cen["uniq"],
            "expected_uniq": cen["expected_uniq"],
            "doubles": cen["doubles"],
        })

    k15, j15 = 15, 12
    T15 = 1 << (k15 - 1)
    p15 = 3 * (1 << j15) + 1
    t15 = T15 + (1 << j15)
    kill_3fam = {
        "k": k15,
        "j": j15,
        "p": p15,
        "t": t15,
        "fire": fires(rows[t15], p15),
    }

    k12 = 12
    T12 = 1 << (k12 - 1)
    p_d = 3 * T12 // 2 + 1
    f_d = [fires(rows[T12], p_d), fires(rows[3 * T12 // 2], p_d)]
    kill_double = {
        "k": k12,
        "p": p_d,
        "fires": f_d,
        "xor": f_d[0] ^ f_d[1],
    }

    checks = self_checks(
        c20, even_ok, fam_ok, odd_ok, even_count, consec, w_ok, n_ok,
        tails, bits_zero, recs, kill_3fam, kill_double,
    )
    dump = {
        "cycle": "AV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "unique_even": even_ok,
            "unique_D_families": fam_ok,
            "odd_doubling": odd_ok,
            "even_count": even_count,
            "consecutive_same_support": consec,
            "W_interval_uniques": w_ok,
            "family_n": n_ok,
            "e13_e17_tails": tails,
            "bit13_17_zero": bits_zero,
        },
        "annulus": recs,
        "kills": {"three_family_ge13": kill_3fam, "double_3T2": kill_double},
        "lemmas": {
            "unique_even_only_2a_minus_2_4": True,
            "unique_D_are_AS_families": True,
            "unique_Green_bits_exactly_2k_minus_2": True,
            "e13_e17_period4": True,
            "bit13_contributes_0": True,
            "bit17_contributes_0": True,
            "exactly_two_doubles_all_k": None,
            "three_family_ge13_identically_0": False,
            "double_3T2_xor_0": False,
            "nested_left_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "unique_even_only_2a_minus_2_4": "LEMMA",
            "unique_D_are_AS_families": "LEMMA",
            "unique_Green_bits_exactly_2k_minus_2": "LEMMA",
            "e13_e17_period4": "LEMMA",
            "bit13_contributes_0": "LEMMA",
            "bit17_contributes_0": "LEMMA",
            "exactly_two_doubles_all_k": "PREFIX",
            "three_family_ge13_identically_0": "KILLED",
            "double_3T2_xor_0": "KILLED",
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
        {key: rec[key] for key in ("k", "T", "n1", "n2")}
        for rec in recs
    ])
    print("kills", dump["kills"])


if __name__ == "__main__":
    main()
