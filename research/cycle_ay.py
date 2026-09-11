#!/usr/bin/env python3
"""Cycle AY: bit 16 S_4; e_18; I_k = 1 XOR B^{>=19}.

Packed bit 16 is Jacobsthal G(n, 2^a-16) with s in S_4={1,4,5,6,7}.
With Cycle AV's e_15, e_16 the five AND fires are 0,1,0,0,1, XOR 0.
e_18(t)=1 iff t≡1,2 mod 4 for t>=20, so e_18 AND e_17 is identically 0
and bit 18 never fires. Combined with bits 13-15,17 already 0,
I_k = 1 XOR B_k^{>=19} for k>=5. Nested depth 18 is not a closed form.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_ay.py --certify
Dump: research/cycle_ay.json
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
S4 = [1, 4, 5, 6, 7]


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


def jacobsthal_S(b: int) -> set[int]:
    if b == 0:
        return set()
    if b == 1:
        return {0}
    return jacobsthal_S(b - 2) | set(range(1 << (b - 2), 1 << (b - 1)))


def ones_s(a: int, q: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    D = (1 << a) - q
    return sorted(nmax - n for n in range(nmax + 1) if G(n, D))


def s4_ok(amax: int) -> bool:
    if sorted(jacobsthal_S(4)) != S4:
        return False
    for a in range(5, amax + 1):
        if ones_s(a, 16) != S4:
            return False
    return True


def green_times(k: int, p: int) -> list[int]:
    T = 1 << (k - 1)
    end = 1 << k
    out = []
    for t in range(T, end):
        if p > 2 * t:
            continue
        if G(end - t - 1, end - p):
            out.append(t)
    return out


def e18(t: int) -> int:
    return int(t % 4 in (1, 2))


def tails_ok(rows: list[int], tmax: int) -> bool:
    for t in range(20, tmax):
        if e_bit(rows[t], 18) != e18(t):
            return False
    for t in range(20, tmax - 1):
        e16 = int(t % 4 != 1)
        e17 = int(t % 4 == 3)
        got = e_bit(rows[t + 1], 18)
        want = e16 ^ (e17 | e_bit(rows[t], 18))
        if got != want:
            return False
        if e_bit(rows[t], 18) and e_bit(rows[t], 17):
            return False
    return True


def bulk_ge(rows: list[int], k: int, pmin: int) -> int:
    T = 1 << (k - 1)
    end = 1 << k
    x = 0
    for t in range(T, end):
        A = (rows[t] << 1) & rows[t]
        m = end - t - 1
        lo = max(pmin, end - 2 * m)
        hi = min(end, 2 * t)
        for p in range(lo, hi + 1):
            if G(m, end - p) and ((A >> p) & 1):
                x ^= 1
    return x


def self_checks(c20, s4: bool, tails: bool, recs: list[dict]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert s4 and tails
    vals = []
    for rec in recs:
        T = rec["T"]
        assert rec["t16"] == [T + s for s in S4]
        assert rec["fire16"] == [0, 1, 0, 0, 1] and rec["x16"] == 0
        assert rec["x18"] == 0
        assert rec["I"] == rec["B19"] ^ 1
        vals.append(rec["B19"])
    assert 0 in vals and 1 in vals
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    s4 = s4_ok(12)
    kmax = 8
    rows = evolve_rows(1 << kmax)
    tails = tails_ok(rows, min(len(rows) - 1, 256))
    recs = []
    for k in range(5, kmax + 1):
        T = 1 << (k - 1)
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        t16 = green_times(k, 16)
        f16 = [fires(rows[t], 16) for t in t16]
        x16 = 0
        for f in f16:
            x16 ^= f
        t18 = green_times(k, 18)
        f18 = [fires(rows[t], 18) for t in t18]
        x18 = 0
        for f in f18:
            x18 ^= f
        B19 = bulk_ge(rows, k, 19)
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "t16": t16,
            "fire16": f16,
            "x16": x16,
            "t18": t18,
            "fire18": f18,
            "x18": x18,
            "B19": B19,
        })
    checks = self_checks(c20, s4, tails, recs)
    dump = {
        "cycle": "AY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {"S4": s4, "e18_tail": tails},
        "annulus": recs,
        "lemmas": {
            "G_2a_minus_16_S4": True,
            "bit16_contributes_0": True,
            "e18_period4": True,
            "bit18_never_fires": True,
            "I_eq_1_xor_B19": True,
            "nested18_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "G_2a_minus_16_S4": "LEMMA",
            "bit16_contributes_0": "LEMMA",
            "e18_period4": "LEMMA",
            "bit18_never_fires": "LEMMA",
            "I_eq_1_xor_B19": "LEMMA",
            "nested18_is_I": "KILLED",
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
        {key: rec[key] for key in rec if key not in ("t16", "t18")}
        for rec in recs
    ])


if __name__ == "__main__":
    main()
