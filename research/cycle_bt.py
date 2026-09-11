#!/usr/bin/env python3
"""Cycle BT: freshman extras on non-dyadic covering blocks.

For every t>=0 and a>=0 the packed Rule-150 step of length M=2^a is
Freshman: (1+x+x^2)^M = 1 + x^M + x^{2M} over GF(2). Hence

    c_{t+M} XOR c_t = x(t,M) XOR x(t,-M) XOR J_{[t,t+M)->t+M},

with x(t,j)=0 outside the seed cone |j|>t. Cycle AL is the case
t=2^k and M>=2t, where both extras vanish. On the covering blocks
the start times are not dyadic: at t=6U one has M=4U<6U, and at
t=10U one has M=8U<10U, so the palindrome defects survive.

Thus phi5_{k+1} XOR phi3_{k+1} equals the Green AND-parity J_B on
[6U,10U)->10U if and only if d_B:=x(6U,-4U) XOR x(6U,4U) vanishes,
which it does not identically. Covering fails at k+1 iff J_A=0 and
J_B=d_B and J_C=d_C. Not a prize claim: the Fermat covering remains
a prefix.

Run: python3 research/cycle_bt.py --certify
Dump: research/cycle_bt.json
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


def green_xor(rows: list[int], t0: int, t1: int, Tbit: int) -> int:
    acc = 0
    for t in range(t0, t1):
        tmp = (rows[t] << 1) & rows[t]
        m = t1 - t - 1
        p = 0
        while tmp:
            if tmp & 1 and G(m, Tbit - p):
                acc ^= 1
            tmp >>= 1
            p += 1
    return acc


def freshman_ok(amax: int) -> bool:
    """G(2^a, d)=1 iff d in {0, 2^a, 2^{a+1}}."""
    for a in range(0, amax + 1):
        M = 1 << a
        for d in range(0, 2 * M + 1):
            want = int(d in (0, M, 2 * M))
            if G(M, d) != want:
                return False
    return True


def evolve(tmax: int) -> list[int]:
    rows = []
    row = 1
    for _t in range(tmax + 1):
        rows.append(row)
        row = rule30_step(row)
    return rows


def general_identity_ok(rows: list[int], tmax: int, amax: int) -> bool:
    n = len(rows) - 1
    for t in range(0, tmax + 1):
        for a in range(0, amax + 1):
            M = 1 << a
            t1 = t + M
            if t1 > n:
                continue
            c0 = packed_bit(rows[t], t, 0)
            c1 = packed_bit(rows[t1], t1, 0)
            defect = packed_bit(rows[t], t, M) ^ packed_bit(rows[t], t, -M)
            J = green_xor(rows, t, t1, t1)
            if c0 ^ c1 != defect ^ J:
                return False
    return True


def covering_identity_ok(rows: list[int], kmax: int) -> dict:
    extra_A = []
    extra_B = []
    extra_C = []
    match = []
    ja_eq_phi3 = []
    jb_eq_centre = []
    jc_eq_centre = []
    fail_iff = []
    for k in range(1, kmax + 1):
        U = 1 << k
        c2 = packed_bit(rows[2 * U], 2 * U, 0)
        c6 = packed_bit(rows[6 * U], 6 * U, 0)
        c10 = packed_bit(rows[10 * U], 10 * U, 0)
        c18 = packed_bit(rows[18 * U], 18 * U, 0)
        dA = packed_bit(rows[2 * U], 2 * U, 4 * U) ^ packed_bit(
            rows[2 * U], 2 * U, -4 * U
        )
        dB = packed_bit(rows[6 * U], 6 * U, 4 * U) ^ packed_bit(
            rows[6 * U], 6 * U, -4 * U
        )
        dC = packed_bit(rows[10 * U], 10 * U, 8 * U) ^ packed_bit(
            rows[10 * U], 10 * U, -8 * U
        )
        JA = green_xor(rows, 2 * U, 6 * U, 6 * U)
        JB = green_xor(rows, 6 * U, 10 * U, 10 * U)
        JC = green_xor(rows, 10 * U, 18 * U, 18 * U)
        extra_A.append(dA)
        extra_B.append(dB)
        extra_C.append(dC)
        match.append(
            (c6 ^ c2 == JA ^ dA)
            and (c10 ^ c6 == JB ^ dB)
            and (c18 ^ c10 == JC ^ dC)
        )
        ja_eq_phi3.append(JA == (c6 ^ c2) and dA == 0)
        jb_eq_centre.append(JB == (c10 ^ c6))
        jc_eq_centre.append(JC == (c18 ^ c10))
        phi3 = c6 ^ c2
        phi5 = c10 ^ c2
        phi9 = c18 ^ c2
        fail = (phi3 | phi5 | phi9) == 0
        fail_green = JA == 0 and JB == dB and JC == dC
        fail_iff.append(fail == fail_green)
    return {
        "extra_A": extra_A,
        "extra_B": extra_B,
        "extra_C": extra_C,
        "match": match,
        "ja_eq_phi3": ja_eq_phi3,
        "jb_eq_centre": jb_eq_centre,
        "jc_eq_centre": jc_eq_centre,
        "fail_iff": fail_iff,
        "A_extras_vanish": extra_A == [0] * kmax,
        "B_both": set(extra_B) == {0, 1},
        "C_both": set(extra_C) == {0, 1},
        "identities": all(match),
        "fail_criterion": all(fail_iff),
        "BQ_JB_is_centre": all(jb_eq_centre),
        "BQ_JC_is_centre": all(jc_eq_centre),
    }


def defect_values(kmax: int) -> dict:
    need: set[int] = set()
    for k in range(1, kmax + 1):
        U = 1 << k
        need.update((2 * U, 6 * U, 10 * U))
    tmax = 10 * (1 << kmax)
    row = 1
    samp: dict[int, int] = {}
    for t in range(tmax + 1):
        if t in need:
            samp[t] = row
        row = rule30_step(row)
    dB = []
    dC = []
    dA = []
    for k in range(1, kmax + 1):
        U = 1 << k
        dA.append(
            packed_bit(samp[2 * U], 2 * U, 4 * U)
            ^ packed_bit(samp[2 * U], 2 * U, -4 * U)
        )
        dB.append(
            packed_bit(samp[6 * U], 6 * U, 4 * U)
            ^ packed_bit(samp[6 * U], 6 * U, -4 * U)
        )
        dC.append(
            packed_bit(samp[10 * U], 10 * U, 8 * U)
            ^ packed_bit(samp[10 * U], 10 * U, -8 * U)
        )
    return {
        "dA": dA,
        "dB": dB,
        "dC": dC,
        "A_zero": dA == [0] * kmax,
        "B_both": set(dB) == {0, 1},
        "C_both": set(dC) == {0, 1},
    }


def a_to_extras_ok(rows: list[int], kmax: int) -> bool:
    """d_B = J_A targeting packed 2U XOR J_A targeting packed 10U."""
    for k in range(1, kmax + 1):
        U = 1 << k
        JA2 = green_xor(rows, 2 * U, 6 * U, 2 * U)
        JA10 = green_xor(rows, 2 * U, 6 * U, 10 * U)
        dB = packed_bit(rows[6 * U], 6 * U, 4 * U) ^ packed_bit(
            rows[6 * U], 6 * U, -4 * U
        )
        if (JA2 ^ JA10) != dB:
            return False
        c2 = packed_bit(rows[2 * U], 2 * U, 0)
        left = packed_bit(rows[6 * U], 6 * U, -4 * U)
        right = packed_bit(rows[6 * U], 6 * U, 4 * U)
        if left != (c2 ^ JA2) or right != (c2 ^ JA10):
            return False
    return True


def cone_ineq_ok(kmax: int) -> bool:
    for k in range(1, kmax + 1):
        U = 1 << k
        if 4 * U <= 2 * U:
            return False
        if 4 * U >= 6 * U:
            return False
        if 8 * U >= 10 * U:
            return False
    return True


def self_checks(
    c20,
    fresh: bool,
    gen: bool,
    ineq: bool,
    cov: dict,
    defs: dict,
    extras: bool,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fresh and gen and ineq and extras
    assert cov["identities"] and cov["fail_criterion"]
    assert cov["A_extras_vanish"] and cov["B_both"] and cov["C_both"]
    assert not cov["BQ_JB_is_centre"]
    assert not cov["BQ_JC_is_centre"]
    assert defs["A_zero"] and defs["B_both"] and defs["C_both"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fresh = freshman_ok(12)
    ineq = cone_ineq_ok(12)
    rows_gen = evolve(80)
    gen = general_identity_ok(rows_gen, 24, 6)
    k_id = 6
    rows = evolve(18 * (1 << k_id))
    cov = covering_identity_ok(rows, k_id)
    extras = a_to_extras_ok(rows, k_id)
    defs = defect_values(8)
    checks = self_checks(c20, fresh, gen, ineq, cov, defs, extras)
    dump = {
        "cycle": "BT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "freshman_a_le": 12,
        "general_identity": {"tmax": 24, "amax": 6, "ok": gen},
        "covering": {
            "kmax": k_id,
            "dA": cov["extra_A"],
            "dB": cov["extra_B"],
            "dC": cov["extra_C"],
            "jb_equals_centre_coboundary": cov["jb_eq_centre"],
            "jc_equals_centre_coboundary": cov["jc_eq_centre"],
        },
        "defects_k8": defs,
        "lemmas": {
            "freshman_power2": True,
            "general_freshman_defect": True,
            "A_extras_vanish": True,
            "B_C_extras_survive": True,
            "dB_eq_JA_extras": True,
            "cover_fails_iff_JA0_JB_eq_dB_JC_eq_dC": True,
            "dB_identically_0": False,
            "dC_identically_0": False,
            "centre_coboundary_equals_JB": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "freshman_power2": "LEMMA",
            "general_freshman_defect": "LEMMA",
            "A_extras_vanish": "LEMMA",
            "B_C_extras_survive": "LEMMA",
            "dB_eq_JA_extras": "LEMMA",
            "cover_fails_iff_JA0_JB_eq_dB_JC_eq_dC": "LEMMA",
            "dB_identically_0": "KILLED",
            "dC_identically_0": "KILLED",
            "centre_coboundary_equals_JB": "KILLED",
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
    print("dB", defs["dB"])
    print("dC", defs["dC"])


if __name__ == "__main__":
    main()
