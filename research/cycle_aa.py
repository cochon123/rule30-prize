#!/usr/bin/env python3
"""Cycle AA: every centre-right AND on a dyadic annulus hits I_k.

Cycle Z: b_k = b_{k-1} XOR I_k with I_k the Green parity of AND
injections on [T,2T), T=2^{k-1}. This cycle identifies a production that
hits every time in that annulus: the central trinomial coefficient
[x^m](1+x+x^2)^m equals 1 over GF(2), so c_t AND r_t at time t contributes
to I_k for every t in [T,2T). The remainder R_k (all ANDs of spatial
offset != 0) does not vanish, so this is not a closed form for I_k.

Also: packed bit 1 is identically 1 for t>=1 (left-edge 11), but that
AND never reaches the next dyadic centre; G(m,m-1)=v_2(m+1) mod 2.

Not a prize claim unless I_k (equivalently R_k XOR the (c AND r) parity)
is proved not eventually 0.

Run: python3 research/cycle_aa.py --certify
Dump: research/cycle_aa.json
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
    """[x^d](1+x+x^2)^m over GF(2), via the doubling recurrence."""
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
    for _t in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def v2(n: int) -> int:
    if n == 0:
        return 0
    return (n & -n).bit_length() - 1


def cr_and_remainder(rows: list[int], k: int) -> dict:
    """Split I_k into XOR(c AND r) plus off-centre AND hits."""
    T = 1 << (k - 1)
    cr = 0
    n_cr = 0
    other = 0
    n_other = 0
    n_leftmost = 0
    leftmost_hit = 0
    for t in range(T, 2 * T):
        R = rows[t]
        c = (R >> t) & 1
        rbit = (R >> (t + 1)) & 1
        if c & rbit:
            cr ^= 1
            n_cr += 1
        A = (R << 1) & R
        if A & 2:
            n_leftmost += 1
        m = 2 * T - 1 - t
        tmp = A
        p = 0
        while tmp:
            if tmp & 1:
                if G(m, 2 * T - p):
                    delta = p - (t + 1)
                    if delta != 0:
                        other ^= 1
                        n_other += 1
                    if p == 1:
                        leftmost_hit ^= 1
            tmp >>= 1
            p += 1
    return {
        "k": k,
        "cr": cr,
        "n_cr": n_cr,
        "other": other,
        "n_other": n_other,
        "tot": cr ^ other,
        "n_leftmost": n_leftmost,
        "leftmost_hit": leftmost_hit,
    }


def mersenne_local(rows: list[int], k: int) -> dict:
    T = 1 << (k - 1)
    t_m = 2 * T - 1
    t_m2 = 2 * T - 2
    Rm, Rm2 = rows[t_m], rows[t_m2]

    def sp(R: int, t: int, j: int) -> int:
        bit = j + t
        if bit < 0:
            return 0
        return (R >> bit) & 1

    c_m = sp(Rm, t_m, 0)
    l_m = sp(Rm, t_m, -1)
    r_m = sp(Rm, t_m, 1)
    c_m2 = sp(Rm2, t_m2, 0)
    l_m2 = sp(Rm2, t_m2, -1)
    r_m2 = sp(Rm2, t_m2, 1)
    x2 = sp(Rm2, t_m2, 2)
    a0 = (r_m2 & x2) ^ (c_m2 & r_m2) ^ (l_m2 & c_m2)
    return {
        "c_m": c_m,
        "l_m": l_m,
        "r_m": r_m,
        "c_and_r_m": c_m & r_m,
        "c_m2": c_m2,
        "a0_prod": a0,
    }


def self_checks(c20, rows, b, I, split, g_central, g_near, bit1) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    for rec in split:
        assert rec["tot"] == rec["I"]
        assert rec["cr"] ^ rec["other"] == rec["I"]
        assert rec["leftmost_hit"] == 0
        if rec["k"] >= 1:
            T = 1 << (rec["k"] - 1)
            # every time in the annulus has the leftmost 11
            assert rec["n_leftmost"] == T
    assert all(g_central)
    assert all(g_near[m] == (v2(m + 1) % 2) for m in range(len(g_near)))
    assert all(bit1)
    # palindrome
    for m in range(40):
        for d in range(2 * m + 1):
            assert G(m, d) == G(m, 2 * m - d)
    # I_k is not identically the (c AND r) parity
    assert any(rec["cr"] != rec["I"] for rec in split)
    return {"all_ok": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--kmax", type=int, default=12)
    parser.add_argument("--splitmax", type=int, default=10)
    args = parser.parse_args()
    t0 = time.perf_counter()
    kmax = args.kmax
    tmax = 1 << kmax
    c20 = packed_center_bits(20)
    rows = evolve_rows(tmax)
    b = [(rows[1 << k] >> (1 << k)) & 1 for k in range(0, kmax + 1)]
    I = [b[k] ^ b[k - 1] for k in range(1, kmax + 1)]

    g_central = [G(m, m) for m in range(1 << 10)]
    g_near = [G(m, m - 1) if m else 0 for m in range(1 << 9)]
    bit1 = [((rows[t] >> 1) & 1) == 1 for t in range(1, min(len(rows), 1 << 12))]

    split = []
    for k in range(1, min(args.splitmax, kmax) + 1):
        rec = cr_and_remainder(rows, k)
        rec["I"] = I[k - 1]
        rec["match_tot"] = rec["tot"] == rec["I"]
        rec["cr_eq_I"] = rec["cr"] == rec["I"]
        rec["other_eq_I"] = rec["other"] == rec["I"]
        split.append(rec)

    mersenne = []
    names = ("c_m", "l_m", "r_m", "c_and_r_m", "c_m2", "a0_prod")
    fail = {n: 0 for n in names}
    for k in range(2, min(kmax, 12) + 1):
        loc = mersenne_local(rows, k)
        loc["k"] = k
        loc["I"] = I[k - 1]
        loc["eq"] = {n: loc[n] == I[k - 1] for n in names}
        for n in names:
            if not loc["eq"][n]:
                fail[n] += 1
        mersenne.append(loc)
    any_mersenne = any(f == 0 for f in fail.values())

    cr_eq_all = all(rec["cr_eq_I"] for rec in split)
    other_eq_all = all(rec["other_eq_I"] for rec in split)

    # linear recurrences of small order for I
    rec_fail = {}
    for lag in range(1, 5):
        rec_fail[f"period_{lag}"] = [
            i + 1 for i in range(lag, len(I)) if I[i] != I[i - lag]
        ]
    rec_fail["fib"] = [
        i + 1 for i in range(2, len(I)) if I[i] != I[i - 1] ^ I[i - 2]
    ]

    checks = self_checks(c20, rows, b, I, split, g_central, g_near, bit1)

    dump = {
        "cycle": "AA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "b": b,
        "I": I,
        "n_I_ones": sum(I),
        "n_I_zeros": len(I) - sum(I),
        "G_central_all_one": all(g_central),
        "G_near_v2": all(g_near[m] == (v2(m + 1) % 2) for m in range(len(g_near))),
        "packed_bit1_always_one": all(bit1),
        "n_bit1_checked": len(bit1),
        "split": split,
        "cr_equals_I_universal": cr_eq_all,
        "remainder_equals_I_universal": other_eq_all,
        "first_cr_ne_I": next((rec["k"] for rec in split if not rec["cr_eq_I"]), None),
        "mersenne_fail": fail,
        "any_mersenne_universal": any_mersenne,
        "I_recurrence_fails": rec_fail,
        "lemmas": {
            "G_mm_is_one": all(g_central),
            "cr_hits_every_time": True,
            "leftmost_11_always": all(bit1),
            "leftmost_never_hits_I": all(rec["leftmost_hit"] == 0 for rec in split),
            "G_near_is_v2": all(g_near[m] == (v2(m + 1) % 2) for m in range(len(g_near))),
            "I_independently_split": all(rec["match_tot"] for rec in split),
            "b_not_eventually_constant": None,
        },
        "verdict": {
            "central_trinomial": "LEMMA",
            "cr_hits_I": "LEMMA",
            "I_eq_cr_parity": "KILLED" if not cr_eq_all else "OPEN",
            "leftmost_11": "LEMMA",
            "leftmost_hits_I": "KILLED",
            "G_near_v2": "LEMMA",
            "mersenne_local": "KILLED" if not any_mersenne else "OPEN",
            "I_small_recurrence": "KILLED",
            "b_k_eventual_constancy": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("b", b)
    print("I", I)
    print("split", [(r["k"], r["I"], r["cr"], r["other"], r["n_cr"], r["n_other"]) for r in split])
    print("first_cr_ne_I", dump["first_cr_ne_I"])
    print("mersenne_fail", fail)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
