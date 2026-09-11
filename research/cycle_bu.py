#!/usr/bin/env python3
"""Cycle BU: defect chaining; small-degree Green sums vanish.

For M=2^a with 2M>t the freshman extras at +-2M and +-3M lie outside
the seed cone, so the palindrome defect chains:

    d^{(a+1)}_{t+M} = d^{(a)}_t XOR J^{-> t-M} XOR J^{-> t+3M}.

On covering block B this is 8U>6U, hence
d_C = d_B XOR J_B^{->2U} XOR J_B^{->18U}. Those three Green parities
live on disjoint packed-bit ranges. The unweighted sum
S(2^a, d) := XOR_{m<2^a} G(m,d) vanishes for every d<2^{a-1}, so in
particular the always-firing packed-bit-1 slice of J_B^{->2U} is 0.
The fire-weighted J_B^{->2U} itself vanishes on the prefix where
x(6U,-4U)=x(10U,-8U). Not a prize claim: the Fermat covering remains
a prefix.

Run: python3 research/cycle_bu.py --certify
Dump: research/cycle_bu.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
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


def packed_bit(row: int, t: int, spatial: int) -> int:
    p = spatial + t
    if p < 0 or p > 2 * t:
        return 0
    return (row >> p) & 1


def green_xor(rows: list[int], t0: int, t1: int, Tbit: int) -> tuple[int, int, int]:
    acc = 0
    pmin, pmax = 10**9, -1
    n = 0
    for t in range(t0, t1):
        tmp = (rows[t] << 1) & rows[t]
        m = t1 - t - 1
        p = 0
        while tmp:
            if tmp & 1 and G(m, Tbit - p):
                acc ^= 1
                n += 1
                pmin = min(pmin, p)
                pmax = max(pmax, p)
            tmp >>= 1
            p += 1
    if n == 0:
        return 0, 0, -1
    return acc, pmin, pmax


def S_brute(N: int, d: int) -> int:
    acc = 0
    for m in range(N):
        acc ^= G(m, d)
    return acc


def S_pow2(a: int, d: int) -> int:
    """XOR_{m<2^a} G(m,d) via the even-doubling recurrences."""
    if d < 0:
        return 0
    while a > 0:
        if d % 2 == 0:
            d = d // 2 - 1
        else:
            d = d // 2
        a -= 1
        if d < 0:
            return 0
    return int(d == 0)


def S_recurrence_ok(Mmax: int) -> bool:
    for M in range(1, Mmax + 1):
        for j in range(0, 2 * M + 1):
            if S_brute(2 * M, 2 * j) != S_brute(M, j - 1):
                return False
            if S_brute(2 * M, 2 * j + 1) != S_brute(M, j):
                return False
    return True


def S_pow2_ok(amax: int, brute_a: int) -> bool:
    for a in range(0, brute_a + 1):
        N = 1 << a
        for d in range(0, 2 * N):
            if S_pow2(a, d) != S_brute(N, d):
                return False
    for a in range(0, amax + 1):
        half = 1 << max(a - 1, 0)
        if a == 0:
            # S(1,0)=1, the range d<2^{-1} is empty; check S(1,0)=1
            if S_pow2(0, 0) != 1:
                return False
            continue
        for d in range(0, half):
            if S_pow2(a, d) != 0:
                return False
    return True


def evolve(tmax: int) -> list[int]:
    rows = []
    row = 1
    for _t in range(tmax + 1):
        rows.append(row)
        row = rule30_step(row)
    return rows


def chaining_ok(rows: list[int], tmax: int, amax: int) -> tuple[bool, int]:
    n = len(rows) - 1
    checked = 0
    for t in range(0, tmax + 1):
        for a in range(0, amax + 1):
            M = 1 << a
            if 2 * M <= t:
                continue
            t1 = t + M
            if t1 > n:
                continue
            d0 = packed_bit(rows[t], t, M) ^ packed_bit(rows[t], t, -M)
            d1 = packed_bit(rows[t1], t1, 2 * M) ^ packed_bit(
                rows[t1], t1, -2 * M
            )
            Jlo = green_xor(rows, t, t1, t - M)[0]
            Jhi = green_xor(rows, t, t1, t + 3 * M)[0]
            if d1 != d0 ^ Jlo ^ Jhi:
                return False, checked
            checked += 1
    return True, checked


def cone_split_ok(kmax: int) -> bool:
    for k in range(1, kmax + 1):
        U = 1 << k
        if 8 * U <= 6 * U:
            return False
        for s in range(0, 4 * U):
            t = 6 * U + s
            left_hi = 2 * U
            cen_lo = 2 * t - 10 * U + 2
            cen_hi = 10 * U
            right_lo = 2 * t - 2 * U + 2
            if left_hi >= cen_lo:
                return False
            if cen_hi >= right_lo:
                return False
            if cen_lo != 2 * U + 2 + 2 * s:
                return False
            if right_lo != 10 * U + 2 + 2 * s:
                return False
    return True


def covering_chain_ok(rows: list[int], kmax: int) -> dict:
    dB = []
    dC = []
    JB2 = []
    JB18 = []
    match = []
    disjoint = []
    jb2_zero = []
    for k in range(1, kmax + 1):
        U = 1 << k
        db = packed_bit(rows[6 * U], 6 * U, 4 * U) ^ packed_bit(
            rows[6 * U], 6 * U, -4 * U
        )
        dc = packed_bit(rows[10 * U], 10 * U, 8 * U) ^ packed_bit(
            rows[10 * U], 10 * U, -8 * U
        )
        j2, lo2, hi2 = green_xor(rows, 6 * U, 10 * U, 2 * U)
        j18, lo18, hi18 = green_xor(rows, 6 * U, 10 * U, 18 * U)
        jcen, loc, hic = green_xor(rows, 6 * U, 10 * U, 10 * U)
        dB.append(db)
        dC.append(dc)
        JB2.append(j2)
        JB18.append(j18)
        match.append(dc == db ^ j2 ^ j18)
        split = True
        if lo2 != 0 and hi2 >= loc and loc != 0:
            split = False
        if hic >= lo18 and lo18 != 0:
            split = False
        if hi2 > 2 * U:
            split = False
        if loc < 2 * U + 2:
            split = False
        disjoint.append(split)
        jb2_zero.append(j2 == 0)
    return {
        "dB": dB,
        "dC": dC,
        "JB2": JB2,
        "JB18": JB18,
        "match": match,
        "disjoint": disjoint,
        "jb2_zero": jb2_zero,
        "ok": all(match) and all(disjoint) and all(jb2_zero),
        "JB18_both": set(JB18) == {0, 1},
        "dC_eq_dB": dC == dB,
    }


def left_extra_frozen(kmax: int) -> dict:
    need: set[int] = set()
    for k in range(1, kmax + 1):
        U = 1 << k
        need.update((6 * U, 10 * U))
    tmax = 10 * (1 << kmax)
    row = 1
    samp: dict[int, int] = {}
    for t in range(tmax + 1):
        if t in need:
            samp[t] = row
        row = rule30_step(row)
    eq = []
    lefts = []
    for k in range(1, kmax + 1):
        U = 1 << k
        a = packed_bit(samp[6 * U], 6 * U, -4 * U)
        b = packed_bit(samp[10 * U], 10 * U, -8 * U)
        eq.append(a == b)
        lefts.append(a)
    return {"eq": eq, "left": lefts, "all_eq": all(eq)}


def self_checks(
    c20,
    rec: bool,
    sp: bool,
    cone: bool,
    chain: bool,
    nchain: int,
    cov: dict,
    frozen: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rec and sp and cone and chain and nchain > 0
    assert cov["ok"]
    assert cov["JB18_both"]
    assert not cov["dC_eq_dB"]
    assert frozen["all_eq"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rec = S_recurrence_ok(24)
    sp = S_pow2_ok(16, 8)
    cone = cone_split_ok(12)
    rows_gen = evolve(80)
    chain, nchain = chaining_ok(rows_gen, 24, 6)
    k_id = 6
    rows = evolve(18 * (1 << k_id))
    cov = covering_chain_ok(rows, k_id)
    frozen = left_extra_frozen(12)
    checks = self_checks(c20, rec, sp, cone, chain, nchain, cov, frozen)
    dump = {
        "cycle": "BU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "S_vanish_a_le": 16,
        "chaining": {"tmax": 24, "amax": 6, "n": nchain, "ok": chain},
        "covering": {
            "kmax": k_id,
            "dB": cov["dB"],
            "dC": cov["dC"],
            "JB2": cov["JB2"],
            "JB18": cov["JB18"],
        },
        "left_extra_k12": frozen,
        "lemmas": {
            "S_pow2_small_d_vanishes": True,
            "defect_chain_2M_gt_t": True,
            "dC_eq_dB_xor_JB_extras": True,
            "disjoint_supports_on_B": True,
            "JB2_identically_0": None,
            "JB18_identically_0": False,
            "dC_identically_dB": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "S_pow2_small_d_vanishes": "LEMMA",
            "defect_chain_2M_gt_t": "LEMMA",
            "dC_eq_dB_xor_JB_extras": "LEMMA",
            "disjoint_supports_on_B": "LEMMA",
            "JB2_identically_0": "PREFIX",
            "JB18_identically_0": "KILLED",
            "dC_identically_dB": "KILLED",
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
    print("nchain", nchain)
    print("JB2", cov["JB2"])
    print("left_eq", frozen["eq"])


if __name__ == "__main__":
    main()
