#!/usr/bin/env python3
"""Cycle AT: Jacobsthal half-window G(n, 2^a-2^b); Mersenne-odd families.

For 1<=b<a and n<2^{a-1}, G(n, 2^a-2^b)=1 iff 2^{a-1}-1-n lies in the
Jacobsthal set S_b, defined by S_0={}, S_1={0},
S_b = S_{b-2} union {2^{b-2},...,2^{b-1}-1}, with |S_b|=(2^b-(-1)^b)/3.
Packed bits p=(2^c-1)2^j+1 on the dyadic annulus therefore Green-hit
at times T+s*2^j for s in S_c (when k-j>c). Recovers Cycle AS at c=1,2.
The c=3 (7-family) bits are triples. None of these families is an
identically-1 production for I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_at.py --certify
Dump: research/cycle_at.json
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


@lru_cache(maxsize=None)
def S(b: int) -> frozenset:
    if b <= 0:
        return frozenset()
    if b == 1:
        return frozenset({0})
    return S(b - 2) | frozenset(range(1 << (b - 2), 1 << (b - 1)))


def jacobsthal(b: int) -> int:
    return ((1 << b) - ((-1) ** b)) // 3


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


def S_axioms_ok(bmax: int) -> bool:
    for b in range(1, bmax + 1):
        if len(S(b)) != jacobsthal(b):
            return False
        if b >= 2:
            high = set(range(1 << (b - 2), 1 << (b - 1)))
            if set(S(b)) != set(S(b - 2)) | high:
                return False
            cap = 1 << (b - 2)
            for sp in range(cap):
                if ((2 * sp + 1) in S(b)) != (sp in S(b - 1)):
                    return False
            for sp in range(1, cap):
                if ((2 * sp) in S(b)) != (sp in S(b - 1)):
                    return False
            if (0 in S(b)) != (b % 2 == 1):
                return False
    return True


def half_window_ok(amax: int) -> bool:
    for a in range(1, amax + 1):
        nmax = (1 << (a - 1)) - 1
        for b in range(1, a):
            D = (1 << a) - (1 << b)
            Sb = S(b)
            for n in range(0, nmax + 1):
                if G(n, D) != int((nmax - n) in Sb):
                    return False
    return True


def green_times(k: int, p: int) -> list[int]:
    T = 1 << (k - 1)
    end = 1 << k
    out = []
    for t in range(T, end):
        if p > 2 * t:
            continue
        m = end - t - 1
        if G(m, end - p):
            out.append(t)
    return out


def predicted_times(k: int, c: int, j: int) -> list[int]:
    T = 1 << (k - 1)
    a = k - j
    if a <= c:
        return []
    p = ((1 << c) - 1) * (1 << j) + 1
    ts = []
    for s in S(c):
        t = T + s * (1 << j)
        if T <= t < (1 << k) and p <= 2 * t:
            ts.append(t)
    return sorted(ts)


def family_times_ok(kmax: int) -> bool:
    for k in range(4, kmax + 1):
        for c in range(1, k):
            for j in range(0, k):
                if k - j <= c:
                    continue
                p = ((1 << c) - 1) * (1 << j) + 1
                if green_times(k, p) != predicted_times(k, c, j):
                    return False
    return True


def xor_fires(rows: list[int], p: int, ts: list[int]) -> int:
    x = 0
    for t in ts:
        x ^= fires(rows[t], p)
    return x


def self_checks(
    c20,
    axioms: bool,
    half: bool,
    fam: bool,
    seven_xors: list[int],
    merse_vs_I: list[tuple[int, int, int]],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert axioms and half and fam
    assert 0 in seven_xors and 1 in seven_xors
    assert any(mx != I for I, mx, _ in merse_vs_I)
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    axioms = S_axioms_ok(12)
    half = half_window_ok(12)
    fam = family_times_ok(8)
    kmax = 8
    rows = evolve_rows(1 << kmax)
    seven_xors = []
    seven_recs = []
    merse_vs_I = []
    for k in range(4, kmax + 1):
        T = 1 << (k - 1)
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        mx = 0
        n_bits = 0
        for c in range(1, k):
            for j in range(0, k):
                if k - j <= c:
                    continue
                p = ((1 << c) - 1) * (1 << j) + 1
                ts = predicted_times(k, c, j)
                if not ts:
                    continue
                n_bits += 1
                mx ^= xor_fires(rows, p, ts)
        merse_vs_I.append((I, mx, n_bits))
        recs_k = []
        for j in range(0, k - 3):
            p = 7 * (1 << j) + 1
            ts = predicted_times(k, 3, j)
            x = xor_fires(rows, p, ts)
            seven_xors.append(x)
            recs_k.append({"j": j, "p": p, "n": len(ts), "times": ts, "xor": x})
        seven_recs.append({"k": k, "bits": recs_k})
    checks = self_checks(c20, axioms, half, fam, seven_xors, merse_vs_I)
    dump = {
        "cycle": "AT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "S_axioms": axioms,
            "half_window": half,
            "family_times": fam,
        },
        "jacobsthal": [jacobsthal(b) for b in range(1, 12)],
        "seven_family": seven_recs,
        "merse_vs_I": [
            {"k": k, "I": I, "merse_xor": mx, "n_bits": n}
            for k, (I, mx, n) in zip(range(4, kmax + 1), merse_vs_I)
        ],
        "lemmas": {
            "S_jacobsthal": True,
            "G_half_2a_minus_2b": True,
            "mersenne_odd_times": True,
            "recovers_AS": True,
            "seven_family_triples": True,
            "seven_always_xor_1": False,
            "merse_odd_xor_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "S_jacobsthal": "LEMMA",
            "G_half_2a_minus_2b": "LEMMA",
            "mersenne_odd_times": "LEMMA",
            "recovers_AS": "LEMMA",
            "seven_family_triples": "LEMMA",
            "seven_always_xor_1": "KILLED",
            "merse_odd_xor_is_I": "KILLED",
            "I_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("merse_vs_I", dump["merse_vs_I"])
    print("seven_family", dump["seven_family"])


if __name__ == "__main__":
    main()
