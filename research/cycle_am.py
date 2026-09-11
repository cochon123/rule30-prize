#!/usr/bin/env python3
"""Cycle AM: nested-left ANDs for I_k; e_8 and e_10 closed forms.

Packed-bit-4 ANDs fire on every odd t>=4 and contribute 1 to every I_k
(k>=3): the Green prefix XOR W(2^{k-2}, 2^{k-1}-2) equals 1 by doubling.
Packed-bit-6 ANDs contribute 1 for k>=4 and cancel that 1. e_8(t)=1 iff
t mod 4 in {0,1} (t>=8); e_10(t)=1 iff t mod 4 in {0,3} (t>=10). Packed
bit 9 then contributes 1 for k>=5, so the net nested-left remainder
through p=9 is 1 and I_k = 1 XOR B_k with B_k the hits of packed bit
>=10. Packed bit 10 itself contributes 1 and cancels again.

Not a prize claim: B_k (or the further bulk) is not proved 0 infinitely
often, so I_k is still not proved 1 infinitely often.

Run: python3 research/cycle_am.py --certify
Dump: research/cycle_am.json
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


def W(n: int, D: int) -> int:
    acc = 0
    for m in range(n):
        acc ^= G(m, D)
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


def ej(rows: list[int], t: int, j: int) -> int:
    if t < 0 or t >= len(rows):
        return 0
    return (rows[t] >> j) & 1


def W_identities(amax: int) -> dict:
    """W(2^a, 2^{a+1}-2)=1; W(2^a, 2^{a+1}-3)=1 for a>=1."""
    w2_ok = W(1, 0) == 1
    w3_ok = True
    for a in range(1, amax + 1):
        if W(1 << a, (1 << (a + 1)) - 2) != 1:
            w2_ok = False
        if W(1 << a, (1 << (a + 1)) - 3) != 1:
            w3_ok = False
    return {"W_2a_2a1_minus2": w2_ok, "W_2a_2a1_minus3": w3_ok}


def left_diagonal_forms(rows: list[int], tmax: int) -> dict:
    fail = {
        "e3": 0, "e4": 0, "e5": 0, "e6": 0, "e7": 0,
        "e8": 0, "e9": 0, "e10": 0, "rec8": 0, "rec10": 0,
    }
    if ej(rows, 8, 8) != 1 or ej(rows, 10, 10) != 0 or ej(rows, 9, 9) != 1:
        fail["e8"] += 1
    for t in range(tmax):
        if t >= 3 and ej(rows, t, 3) != (t % 2):
            fail["e3"] += 1
        if t >= 4 and ej(rows, t, 4) != 1:
            fail["e4"] += 1
        if t >= 5 and ej(rows, t, 5) != (t % 2):
            fail["e5"] += 1
        if t >= 6 and ej(rows, t, 6) != (t % 2):
            fail["e6"] += 1
        if t >= 7 and ej(rows, t, 7) != 0:
            fail["e7"] += 1
        if t >= 8 and ej(rows, t, 8) != int((t % 4) in (0, 1)):
            fail["e8"] += 1
        if t >= 9 and ej(rows, t, 9) != 1:
            fail["e9"] += 1
        if t >= 10 and ej(rows, t, 10) != int((t % 4) in (0, 3)):
            fail["e10"] += 1
        if t >= 7 and ej(rows, t + 1, 8) != ((t % 2) ^ ej(rows, t, 8)):
            fail["rec8"] += 1
        if t >= 9 and ej(rows, t + 1, 10) != (1 ^ ej(rows, t, 8)):
            fail["rec10"] += 1
    return fail


def annulus_hits(rows: list[int], k: int) -> dict:
    T = 1 << (k - 1)
    by_p: dict[int, int] = defaultdict(int)
    n_p: dict[int, int] = defaultdict(int)
    fire_odd4 = fire_miss4 = 0
    tot = 0
    for t in range(T, 2 * T):
        A = (rows[t] << 1) & rows[t]
        m = 2 * T - t - 1
        bit4 = (A >> 4) & 1
        if t % 2 == 1:
            if bit4:
                fire_odd4 += 1
            else:
                fire_miss4 += 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1 and G(m, 2 * T - p):
                by_p[p] ^= 1
                n_p[p] += 1
                tot ^= 1
            tmp >>= 1
            p += 1
    nest9 = 0
    bulk10 = 0
    for p, v in by_p.items():
        if p <= 9:
            nest9 ^= v
        else:
            bulk10 ^= v
    return {
        "I": tot,
        "by_p": {str(p): by_p[p] for p in sorted(by_p) if p <= 12},
        "n4": n_p.get(4, 0),
        "n5": n_p.get(5, 0),
        "n6": n_p.get(6, 0),
        "n8": n_p.get(8, 0),
        "p4": by_p.get(4, 0),
        "p5": by_p.get(5, 0),
        "p6": by_p.get(6, 0),
        "p9": by_p.get(9, 0),
        "p10": by_p.get(10, 0),
        "p12": by_p.get(12, 0),
        "nest9": nest9,
        "bulk10": bulk10,
        "fire_odd4": fire_odd4,
        "fire_miss4": fire_miss4,
        "odd_slots": T // 2,
    }


def self_checks(
    c20,
    wlem: dict,
    diag_fail: dict,
    recs: list[dict],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert wlem["W_2a_2a1_minus2"] and wlem["W_2a_2a1_minus3"]
    assert all(v == 0 for v in diag_fail.values())
    for rec in recs:
        k = rec["k"]
        assert rec["fire_miss4"] == 0
        assert rec["p5"] == 0 and rec["n8"] == 0
        if k >= 3:
            assert rec["p4"] == 1 and rec["n4"] == 1
        if k >= 4:
            assert rec["p6"] == 1 and rec["n6"] == 1
        if k >= 5:
            assert rec["p9"] == 1
            assert rec["nest9"] == 1
            assert rec["I"] == (1 ^ rec["bulk10"])
            assert rec["p10"] == 1
    # I takes both values on the prefix, so neither remainder is identically 0/1
    i_vals = {rec["I"] for rec in recs if rec["k"] >= 5}
    assert i_vals == {0, 1}
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    wlem = W_identities(12)
    kmax = 11
    rows = evolve_rows(1 << kmax)
    diag_fail = left_diagonal_forms(rows, min(len(rows) - 2, 512))
    recs = []
    for k in range(3, kmax + 1):
        h = annulus_hits(rows, k)
        h["k"] = k
        recs.append(h)
    checks = self_checks(c20, wlem, diag_fail, recs)
    dump = {
        "cycle": "AM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "W_identities": wlem,
        "diag_fail": diag_fail,
        "annulus": [
            {key: rec[key] for key in (
                "k", "I", "p4", "p5", "p6", "p9", "p10", "p12",
                "nest9", "bulk10", "n4", "n5", "n6", "fire_miss4",
            )}
            for rec in recs
        ],
        "lemmas": {
            "W_2a_2a1_minus2": True,
            "p4_contributes_1": True,
            "p6_cancels_p4": True,
            "e8_period4": True,
            "e10_period4": True,
            "I_eq_1_xor_bulk_p_ge_10": True,
            "I_k_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "W_2a_2a1_minus2": "LEMMA",
            "p4_contributes_1": "LEMMA",
            "p6_cancels_p4": "LEMMA",
            "e8_period4": "LEMMA",
            "e10_period4": "LEMMA",
            "I_eq_1_xor_bulk_p_ge_10": "LEMMA",
            "p4_closed_form_for_I": "KILLED",
            "nested_le9_closed_form_for_I": "KILLED",
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
