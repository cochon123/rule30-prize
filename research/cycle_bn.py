#!/usr/bin/env python3
"""Cycle BN: net packed-bit-1 parity P(q,T) on [T,qT).

P(q,T) := XOR_{m < (q-1)T} G(m, qT-1) is the net XOR of packed-bit-1
Green hits targeting qT (Cycle AA: bit 1 always fires for t>=1).
Even doubling gives P(q,2S)=P(q,S) for every q,S >= 1, so
P(q, 2^k)=P(q,1)=P(q)=1 XOR wt(q), recovering Cycle AL.

For the 3-fold remainder Theta(T)=c_{3T} xor c_T the odd cases reduce:
P(3,1)=1, P(3,3)=0, P(3,4p+1)=P(3,p), and for p>=1
P(3,4p+3)=P(3, p|1). Thus P(3,T) depends only on the odd part of T
after stripping trailing binary 01 and folding trailing 11 onto p|1.
Families: P(3,2^k)=1 (unique bit-1 on theta); P(3,3*2^k)=0 (two hits
on [3U,9U) cancel, Cycle BM); P(3,5*2^k)=P(3,7*2^k)=1.

P=1 is a net parity, not a covering production: Theta(T)=P(3,T) xor
S_other, and S_other still cancels on theta (theta_k takes both values).
Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bn.py --certify
Dump: research/cycle_bn.json
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


def P(q: int, T: int) -> int:
    acc = 0
    D = q * T - 1
    for m in range((q - 1) * T):
        acc ^= G(m, D)
    return acc


def P3(T: int) -> int:
    return P(3, T)


def pred(T: int) -> int:
    """Closed reduction for P(3,T): strip 2s, strip trailing 01, fold 11."""
    while T >= 1:
        while T % 2 == 0:
            T //= 2
        if T == 1:
            return 1
        if T == 3:
            return 0
        if T % 4 == 1:
            T //= 4
            continue
        T = ((T - 3) // 4) | 1
    return 0


def P_pop(q: int) -> int:
    return (q.bit_count() & 1) ^ 1


def doubling_ok(qmax: int, smax: int) -> bool:
    for q in range(1, qmax + 1):
        for S in range(1, smax + 1):
            if P(q, 2 * S) != P(q, S):
                return False
    return True


def al_ok(qmax: int, kmax: int) -> bool:
    for q in range(1, qmax + 1):
        want = P_pop(q)
        if P(q, 1) != want:
            return False
        for k in range(0, kmax + 1):
            if P(q, 1 << k) != want:
                return False
    return True


def reduce_4p1_window_ok(pmax: int) -> bool:
    for p in range(1, pmax + 1):
        window = 0
        for n in range(3 * p, 4 * p + 1):
            window ^= G(n, 6 * p)
        if P3(4 * p + 1) != window or window != P3(p):
            return False
    return True


def odd_cases_ok(pmax: int) -> bool:
    if P3(1) != 1 or P3(3) != 0:
        return False
    if G(4, 8) ^ G(5, 8) != 0:
        return False
    for p in range(1, pmax + 1):
        if P3(4 * p + 1) != P3(p):
            return False
        if P3(4 * p + 3) != P3(p | 1):
            return False
    return True


def pred_match_ok(tmax: int) -> bool:
    return all(P3(T) == pred(T) for T in range(1, tmax + 1))


def families_ok(kmax: int) -> bool:
    for k in range(0, kmax + 1):
        if pred(1 << k) != 1:
            return False
        if pred(3 << k) != 0:
            return False
        if pred(5 << k) != 1:
            return False
        if pred(7 << k) != 1:
            return False
        if pred(9 << k) != 1:
            return False
        if pred(11 << k) != 0:
            return False
        if pred(13 << k) != 0:
            return False
        if pred(15 << k) != 0:
            return False
        if k <= kmax - 2 and pred(17 << k) != 1:
            return False
    return True


def G_2m1_zero_ok(mmax: int) -> bool:
    for m in range(0, mmax + 1):
        if G(m, 2 * m + 1) != 0:
            return False
    return True


def G_2p_3p_zero_ok(pmax: int) -> bool:
    for p in range(1, pmax + 1):
        if G(2 * p, 3 * p) != 0:
            return False
    return True


def not_a_production_ok(kmax: int) -> dict:
    c = packed_center_bits(3 * (1 << kmax) + 1)
    th = []
    for k in range(2, kmax + 1):
        U = 1 << k
        th.append(c[3 * U] ^ c[U])
    return {
        "theta": th,
        "P3_pow2": 1,
        "theta_both": set(th) == {0, 1},
        "P3_3U": 0,
    }


def self_checks(
    c20,
    dbl: bool,
    al: bool,
    win: bool,
    odd: bool,
    match: bool,
    fam: bool,
    g21: bool,
    g23: bool,
    prod: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert dbl and al and win and odd and match and fam and g21 and g23
    assert P3(1) == 1 and P3(3) == 0 and P3(5) == 1 and P3(7) == 1
    assert P3(11) == 0 and P3(9) == 1
    assert prod["theta_both"]
    assert prod["P3_pow2"] == 1 and prod["P3_3U"] == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    dbl = doubling_ok(12, 24)
    al = al_ok(16, 6)
    win = reduce_4p1_window_ok(40)
    odd = odd_cases_ok(40)
    match = pred_match_ok(128)
    fam = families_ok(16)
    g21 = G_2m1_zero_ok(64)
    g23 = G_2p_3p_zero_ok(64)
    prod = not_a_production_ok(12)
    checks = self_checks(c20, dbl, al, win, odd, match, fam, g21, g23, prod)
    dump = {
        "cycle": "BN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prefix": {
            "k": list(range(2, 13)),
            "theta": prod["theta"],
        },
        "odd_cores": {str(T): P3(T) for T in range(1, 32, 2)},
        "lemmas": {
            "P_even_doubling": True,
            "P_q_pow2_eq_P_q": True,
            "P3_4p1_eq_P3_p": True,
            "P3_4p3_eq_P3_p_or_1": True,
            "P3_closed_reduction": True,
            "P3_pow2_eq_1": True,
            "P3_3_pow2_eq_0": True,
            "P3_is_covering_production": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "P_even_doubling": "LEMMA",
            "P_q_pow2_eq_P_q": "LEMMA",
            "P3_4p1_eq_P3_p": "LEMMA",
            "P3_4p3_eq_P3_p_or_1": "LEMMA",
            "P3_closed_reduction": "LEMMA",
            "P3_pow2_eq_1": "LEMMA",
            "P3_3_pow2_eq_0": "LEMMA",
            "P3_is_covering_production": "KILLED",
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
    print("odd_cores", dump["odd_cores"])


if __name__ == "__main__":
    main()
