#!/usr/bin/env python3
"""Cycle BM: leftmost 11 hits Theta(T) iff the odd part of T is 1, or
3 (mod 4) with no adjacent 0-bits.

G(2T-1, 3T-1) is the Green hit of packed bit 1 at time T on the 3-fold
remainder Theta(T)=c_{3T} xor c_T. Even doubling gives chi(2S)=chi(S),
so the value depends only on the odd part r of T. For r=4p+1>1 the
count vanishes (G(2p,3p)=0). For r=4p+3 it reduces to chi(p+1). Those
recurrences match the predicate: r=1, or r≡3 (mod 4) with no adjacent
0-bits. In particular the hit at time T is 1 for every T=2^k (Cycle AJ) and every
T=3*2^k. On [3U,9U) a second packed-bit-1 hit at t=4U cancels it, so
phi^{(9)}_k xor theta_k has net bit-1 parity 0.
It is not identically 1 (two bit-1 hits on [3U,9U) cancel), and
{theta, phi^{(9)}} is not a covering (fails at k=3).

Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bm.py --certify
Dump: research/cycle_bm.json
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


def chi(T: int) -> int:
    return G(2 * T - 1, 3 * T - 1)


def pred(T: int) -> int:
    r = T
    while r % 2 == 0:
        r //= 2
    if r == 1:
        return 1
    if r % 4 != 3:
        return 0
    return int("00" not in bin(r)[2:])


def doubling_ok(tmax: int) -> bool:
    for S in range(1, tmax + 1):
        if chi(2 * S) != chi(S):
            return False
    return True


def G_2p_3p_zero_ok(pmax: int) -> bool:
    for p in range(1, pmax + 1):
        if G(2 * p, 3 * p) != 0:
            return False
    return True


def odd_cases_ok(pmax: int) -> bool:
    if chi(1) != 1:
        return False
    for p in range(1, pmax + 1):
        if chi(4 * p + 1) != 0:
            return False
        if chi(4 * p + 3) != chi(p + 1):
            return False
        if pred(4 * p + 3) != pred(p + 1):
            return False
    return True


def pred_match_ok(tmax: int) -> bool:
    return all(chi(T) == pred(T) for T in range(1, tmax + 1))


def families_ok(kmax: int) -> bool:
    for k in range(0, kmax + 1):
        if chi(1 << k) != 1:
            return False
        if chi(3 << k) != 1:
            return False
        if chi(7 << k) != 1:
            return False
        if chi(5 << k) != 0:
            return False
        if chi(9 << k) != 0:
            return False
        if k >= 1 and chi(11 << k) != 1:
            return False
    return True


def bit1_times(T: int, q: int = 3) -> list[int]:
    end = q * T
    ts = []
    for t in range(T, end):
        if G(end - t - 1, end - 1):
            ts.append(t)
    return ts


def two_hits_3U_ok(kmax: int) -> bool:
    for k in range(2, kmax + 1):
        U = 1 << k
        ts = bit1_times(3 * U)
        if ts != [3 * U, 4 * U]:
            return False
        if len(bit1_times(U)) != 1:
            return False
    return True


def theta_prefix_ok(kmax: int) -> dict:
    c = packed_center_bits(9 * (1 << kmax) + 1)
    th, th3, both0 = [], [], []
    for k in range(2, kmax + 1):
        U = 1 << k
        a = c[3 * U] ^ c[U]
        b = c[9 * U] ^ c[3 * U]
        th.append(a)
        th3.append(b)
        both0.append(int(a == 0 and b == 0))
    return {
        "theta": th,
        "Theta3U": th3,
        "both0": both0,
        "theta_both": set(th) == {0, 1},
        "Theta3U_both": set(th3) == {0, 1},
        "k3_both0": both0[1] == 1,  # k=3 at index 1
        "kge4_both0": any(both0[k - 2] for k in range(4, kmax + 1)),
    }


def self_checks(
    c20,
    dbl: bool,
    g23: bool,
    odd: bool,
    match: bool,
    fam: bool,
    two: bool,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert dbl and g23 and odd and match and fam and two
    assert chi(1) == 1 and chi(3) == 1 and chi(5) == 0 and chi(9) == 0
    assert pref["theta_both"] and pref["Theta3U_both"]
    assert pref["k3_both0"]
    assert not pref["kge4_both0"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    dbl = doubling_ok(1024)
    g23 = G_2p_3p_zero_ok(256)
    odd = odd_cases_ok(256)
    match = pred_match_ok(4096)
    fam = families_ok(12)
    two = two_hits_3U_ok(8)
    pref = theta_prefix_ok(12)
    checks = self_checks(c20, dbl, g23, odd, match, fam, two, pref)
    dump = {
        "cycle": "BM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prefix": {
            "k": list(range(2, 13)),
            "theta": pref["theta"],
            "Theta3U": pref["Theta3U"],
            "both0": pref["both0"],
        },
        "lemmas": {
            "chi_even_doubling": True,
            "chi_closed_form": True,
            "leftmost_hits_T_pow2": True,
            "leftmost_hits_T_3_pow2": True,
            "two_bit1_hits_3U_9U": True,
            "Theta3U_identically_1": False,
            "phi3_or_phi9_all_k": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "chi_even_doubling": "LEMMA",
            "chi_closed_form": "LEMMA",
            "leftmost_hits_T_pow2": "LEMMA",
            "leftmost_hits_T_3_pow2": "LEMMA",
            "two_bit1_hits_3U_9U": "LEMMA",
            "Theta3U_identically_1": "KILLED",
            "phi3_or_phi9_all_k": "KILLED",
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
    print("prefix", dump["prefix"])


if __name__ == "__main__":
    main()
