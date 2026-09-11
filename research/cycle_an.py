#!/usr/bin/env python3
"""Cycle AN: dyadic W closed form; Mersenne and Fermat G; I_k cone split.

Over GF(2), x(1+x) sum_{m<n} (1+x+x^2)^m = 1+(1+x+x^2)^n. Freshman at
n=2^a gives W(2^a, D)=1 iff D is in [2^a-1, 2^{a+1}-2]. Mersenne
G(2^a-1, d) is the mod-3 window f(d) XOR f(d-2^a) XOR f(d-2^{a+1})
with f(n)=1 iff n>=0 and n not 2 mod 3. Fermat G(2^a+1, d) is the
3-sparse trinomial product. The same generating function gives
W(3*2^a, D)=1 on two intervals.

The W-support splits I_k = I_left XOR I_right, with left packed bits
p in [2, T+1] (T=2^{k-1}) and right p >= T+2. Packed bits 0 and 1
never contribute (bit 0 never fires; bit 1 never Green-hits, Cycle AA).
I_left vanishes on 7<=k<=12; that is not proved for all k, and the
time-T slice is not a formula for I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_an.py --certify
Dump: research/cycle_an.json
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


def W_spectrum(n: int) -> list[int]:
    """W(n, D) for D = 0, ..., 2n-2; empty list if n = 0."""
    if n <= 0:
        return []
    spec = [0] * (2 * n - 1)
    for m in range(n):
        for d in range(2 * m + 1):
            if G(m, d):
                spec[d] ^= 1
    return spec


def f_mod3(n: int) -> int:
    return int(n >= 0 and n % 3 != 2)


def G_mersenne(a: int, d: int) -> int:
    return f_mod3(d) ^ f_mod3(d - (1 << a)) ^ f_mod3(d - (1 << (a + 1)))


def G_mersenne_piecewise(a: int, d: int) -> int:
    m = (1 << a) - 1
    if d < 0 or d > 2 * m:
        return 0
    if d < (1 << a):
        return int(d % 3 != 2)
    if a % 2 == 0:
        return int(d % 3 != 1)
    return int(d % 3 != 0)


def G_fermat(a: int, d: int) -> int:
    acc = 0
    for shift in (0, 1 << a, 1 << (a + 1)):
        j = d - shift
        if 0 <= j <= 2:
            acc ^= 1
    return acc


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


def dyadic_W_ok(amax: int) -> bool:
    for a in range(0, amax + 1):
        n = 1 << a
        spec = W_spectrum(n)
        L, R = n - 1, 2 * n - 2
        for D, got in enumerate(spec):
            want = int(L <= D <= R)
            if got != want:
                return False
    return True


def gw_relation_ok(nmax: int) -> bool:
    for n in range(0, nmax + 1):
        spec = W_spectrum(n)

        def W(D: int) -> int:
            if D < 0 or D >= len(spec):
                return 0
            return spec[D]

        for D in range(1, 2 * n + 3):
            if (W(D - 1) ^ W(D - 2)) != G(n, D):
                return False
    return True


def mersenne_ok(amax: int) -> bool:
    for a in range(0, amax + 1):
        m = (1 << a) - 1
        for d in range(-1, 2 * m + 2):
            got = G(m, d)
            if got != G_mersenne(a, d) or got != G_mersenne_piecewise(a, d):
                return False
            # palindrome vs p-2 at the dyadic row
            T = 1 << a
            if 0 <= d <= 2 * m:
                p = d + 2
                if G(m, 2 * T - p) != G(m, p - 2):
                    return False
    return True


def fermat_ok(amax: int) -> bool:
    for a in range(0, amax + 1):
        m = (1 << a) + 1
        for d in range(-1, 2 * m + 2):
            if G(m, d) != G_fermat(a, d):
                return False
    return True


def W3_ok(amax: int) -> bool:
    for a in range(0, amax + 1):
        U = 1 << a
        n = 3 * U
        spec = W_spectrum(n)
        for D, got in enumerate(spec):
            want = int(
                (U - 1 <= D <= 3 * U - 2) or (5 * U - 1 <= D <= 6 * U - 2)
            )
            if got != want:
                return False
    return True


def annulus_split(rows: list[int], k: int) -> dict:
    T = 1 << (k - 1)
    left = right = n01 = 0
    parts = {"T": 0, "T1": 0, "rest": 0}
    nL = nR = 0
    hits_T1: list[int] = []
    t_form = 0
    t_dis = 0
    a = k - 1
    A_T = (rows[T] << 1) & rows[T]
    tmp, p = A_T, 0
    while tmp:
        if tmp & 1:
            g = G(T - 1, 2 * T - p)
            g2 = G_mersenne(a, p - 2)
            if g != g2:
                t_dis += 1
            if g2:
                t_form ^= 1
        tmp >>= 1
        p += 1
    tot = 0
    for t in range(T, 2 * T):
        A = (rows[t] << 1) & rows[t]
        m = 2 * T - t - 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1 and G(m, 2 * T - p):
                tot ^= 1
                if t == T:
                    parts["T"] ^= 1
                elif t == T + 1:
                    parts["T1"] ^= 1
                    hits_T1.append(p)
                else:
                    parts["rest"] ^= 1
                if p <= 1:
                    n01 += 1
                elif p <= T + 1:
                    left ^= 1
                    nL += 1
                else:
                    right ^= 1
                    nR += 1
            tmp >>= 1
            p += 1
    return {
        "I": tot,
        "left": left,
        "right": right,
        "T_slice": parts["T"],
        "T1_slice": parts["T1"],
        "rest": parts["rest"],
        "nL": nL,
        "nR": nR,
        "n01": n01,
        "T_form": t_form,
        "T_Gdis": t_dis,
        "T1_has_4_6": int(4 in hits_T1 and 6 in hits_T1),
        "I_eq_left_right": int(tot == (left ^ right)),
        "T_eq_I": int(parts["T"] == tot),
        "T_eq_form": int(parts["T"] == t_form),
    }


def self_checks(
    c20,
    flags: dict,
    recs: list[dict],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert flags["dyadic_W"]
    assert flags["gw_relation"]
    assert flags["mersenne"]
    assert flags["fermat"]
    assert flags["W3"]
    left_small = []
    left_large = []
    t_eq_i = []
    for rec in recs:
        k = rec["k"]
        assert rec["n01"] == 0
        assert rec["I_eq_left_right"] == 1
        assert rec["T_Gdis"] == 0
        assert rec["T_eq_form"] == 1
        if k >= 3:
            assert rec["T1_has_4_6"] == 1
        if 3 <= k <= 6:
            left_small.append(rec["left"])
        if k >= 7:
            left_large.append(rec["left"])
        t_eq_i.append(rec["T_eq_I"])
    assert any(v == 1 for v in left_small), "onset of I_left should be nontrivial"
    assert left_large and all(v == 0 for v in left_large)
    assert 0 in t_eq_i, "time-T slice must fail as a formula for I_k"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    flags = {
        "dyadic_W": dyadic_W_ok(10),
        "gw_relation": gw_relation_ok(48),
        "mersenne": mersenne_ok(10),
        "fermat": fermat_ok(8),
        "W3": W3_ok(8),
    }
    kmax = 12
    rows = evolve_rows(1 << kmax)
    recs = []
    for k in range(3, kmax + 1):
        h = annulus_split(rows, k)
        h["k"] = k
        recs.append(h)
    checks = self_checks(c20, flags, recs)
    dump = {
        "cycle": "AN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": flags,
        "annulus": [
            {
                key: rec[key]
                for key in (
                    "k",
                    "I",
                    "left",
                    "right",
                    "T_slice",
                    "T1_slice",
                    "rest",
                    "nL",
                    "nR",
                    "n01",
                    "T_eq_I",
                    "T1_has_4_6",
                )
            }
            for rec in recs
        ],
        "lemmas": {
            "dyadic_W_interval": True,
            "gw_relation": True,
            "mersenne_G_mod3": True,
            "fermat_G_sparse": True,
            "W_3_2a_two_intervals": True,
            "I_eq_left_xor_right": True,
            "I_left_vanishes_all_k": None,
            "T_slice_formula_for_I": False,
            "I_k_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "dyadic_W_interval": "LEMMA",
            "gw_relation": "LEMMA",
            "mersenne_G_mod3": "LEMMA",
            "fermat_G_sparse": "LEMMA",
            "W_3_2a_two_intervals": "LEMMA",
            "I_eq_left_xor_right": "LEMMA",
            "I_left_vanishes_k_ge_7": "PREFIX",
            "T_slice_formula_for_I": "KILLED",
            "I_k_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("annulus", dump["annulus"])


if __name__ == "__main__":
    main()
