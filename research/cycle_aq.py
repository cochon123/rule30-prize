#!/usr/bin/env python3
"""Cycle AQ: closed form for G(m, 2^a); unique double-hit bit on theta.

G(m, 2^a) = bit_a(m) XOR (L mod 2), where L is the run of 1s starting
at bit a-1 and going downward. Equivalently the sequence is periodic
of period 2^{a+1}, and G(m XOR 2^a, 2^a) = G(m, 2^a) XOR 1. On the
3-fold annulus the unique double-Green packed bit is the Cycle AO
two-point member p=3*2^{k-1}+1 at times 3U/2 and 2U; it does not
always fire. Five triple-Green bits follow a scaling pattern on
k=4..8 (prefix).

Not a prize claim: theta_k=1 infinitely often remains open.

Run: python3 research/cycle_aq.py --certify
Dump: research/cycle_aq.json
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


def run_len(m: int, a: int) -> int:
    """Length of the 1-run from bit a-1 downward, at most a."""
    if a <= 0:
        return 0
    L = 0
    bit = a - 1
    while L < a and (m >> bit) & 1:
        L += 1
        bit -= 1
    return L


def G_pow2_formula(m: int, a: int) -> int:
    if a == 0:
        return m & 1
    D = 1 << a
    if D > 2 * m:
        return 0
    return ((m >> a) & 1) ^ (run_len(m, a) & 1)


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


def pow2_form_ok(amax: int, m_mult: int) -> bool:
    for a in range(0, amax + 1):
        D = 1 << a
        for m in range(0, (m_mult << a) + 1):
            if G(m, D) != G_pow2_formula(m, a):
                return False
    return True


def pairing_ok(amax: int) -> bool:
    """chi(m XOR 2^a) = chi(m) XOR 1 ignoring the degree cut."""
    for a in range(0, amax + 1):
        D = 1 << a
        per = 1 << (a + 1)
        for m in range(per):
            chi = ((m >> a) & 1) ^ (run_len(m, a) & 1) if a else (m & 1)
            m2 = m ^ D
            chi2 = ((m2 >> a) & 1) ^ (run_len(m2, a) & 1) if a else (m2 & 1)
            if chi2 != (chi ^ 1):
                return False
    return True


def period_ok(amax: int) -> bool:
    for a in range(0, amax + 1):
        D = 1 << a
        per = 1 << (a + 1)
        rs = {m % per for m in range(0, 4 * per) if G(m, D)}
        for m in range(0, 4 * per):
            want = int(m % per in rs)
            if D > 2 * m:
                want = 0
            if G(m, D) != want:
                return False
        if len(rs) != (1 << a):
            return False
    return True


def hit_multiplicities(rows: list[int], k: int) -> dict:
    U = 1 << k
    end = 3 * U
    by_p: dict[int, list[int]] = defaultdict(list)
    for t in range(U, end):
        m = end - t - 1
        lo = max(0, end - 2 * m)
        hi = min(end, 2 * t)
        for p in range(lo, hi + 1):
            if G(m, end - p):
                by_p[p].append(t)
    doubles = sorted(p for p, ts in by_p.items() if len(ts) == 2)
    triples = sorted(p for p, ts in by_p.items() if len(ts) == 3)
    p_d = 3 * (U >> 1) + 1
    ts = by_p.get(p_d, [])
    fire = []
    for t in ts:
        A = (rows[t] << 1) & rows[t]
        fire.append((A >> p_d) & 1)
    xor = 0
    for f in fire:
        xor ^= f
    expected_triples = [
        (1 << (k - 3)) + 1,
        (1 << (k - 2)) + 1,
        5 * (1 << (k - 3)) + 1,
        3 * (1 << (k - 2)) + 1,
        5 * (1 << (k - 1)) + 1,
    ]
    return {
        "n1": sum(1 for ts in by_p.values() if len(ts) == 1),
        "n2": len(doubles),
        "n3": len(triples),
        "doubles": doubles,
        "p_double": p_d,
        "t_double": ts,
        "fire_double": fire,
        "xor_double": xor,
        "triples": triples,
        "expected_triples": expected_triples,
    }


def self_checks(c20, form: bool, pair: bool, per: bool, recs: list[dict]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert form and pair and per
    xors = []
    for rec in recs:
        k = rec["k"]
        U = 1 << k
        assert rec["n2"] == 1
        assert rec["doubles"] == [3 * (U >> 1) + 1]
        assert rec["t_double"] == [3 * (U >> 1), 2 * U]
        if k >= 4:
            assert rec["n1"] == 4
            assert rec["n3"] == 5
            assert rec["triples"] == rec["expected_triples"]
        xors.append(rec["xor_double"])
    assert 0 in xors and 1 in xors
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    form = pow2_form_ok(10, 8)
    pair = pairing_ok(10)
    per = period_ok(8)
    kmax = 8
    rows = evolve_rows(3 * (1 << kmax))
    recs = []
    for k in range(3, kmax + 1):
        h = hit_multiplicities(rows, k)
        h["k"] = k
        recs.append(h)
    checks = self_checks(c20, form, pair, per, recs)
    dump = {
        "cycle": "AQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {"pow2_formula": form, "pairing": pair, "period": per},
        "annulus": [
            {
                key: rec[key]
                for key in (
                    "k", "n1", "n2", "n3", "p_double", "t_double",
                    "fire_double", "xor_double", "triples",
                )
            }
            for rec in recs
        ],
        "lemmas": {
            "G_pow2_run_form": True,
            "G_pow2_period_pairing": True,
            "unique_double_hit_bit": True,
            "exactly_one_double_all_k": None,
            "five_triples_all_k": None,
            "double_always_xor_1": False,
            "theta_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "G_pow2_run_form": "LEMMA",
            "G_pow2_period_pairing": "LEMMA",
            "unique_double_hit_bit": "LEMMA",
            "exactly_one_double_all_k": "PREFIX",
            "five_triples_all_k": "PREFIX",
            "double_always_xor_1": "KILLED",
            "theta_1_infinitely_often": "OPEN",
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
