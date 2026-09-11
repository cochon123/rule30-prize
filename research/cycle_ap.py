#!/usr/bin/env python3
"""Cycle AP: Mersenne-target G; 4-point 5-fold; unique-Green bits on theta.

G(m, 2^a-1)=1 iff 2^a divides (m+1). G(m, 5*2^k-1)=1 on four residue
classes modulo 2^{k+3}. Together with Cycle AO's two-point law these
identify four unique-Green packed bits on the 3-fold annulus for k>=3:
p=1 at t=2^k (always fires), p=2^{k-1}+1 at t=3*2^{k-1}, p=2^k+1 at
t=2^k (centre-right), and p=2^{k+1}+1 at t=2^{k+1} (centre-right at
2U; the other Mersenne time is outside the cone). The three extra bits
do not always fire. Exhaustiveness of the four is a certified prefix.

Not a prize claim: theta_k=1 infinitely often remains open.

Run: python3 research/cycle_ap.py --certify
Dump: research/cycle_ap.json
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


def merse_tgt_ok(amax: int, m_mult: int) -> bool:
    for a in range(0, amax + 1):
        D = (1 << a) - 1
        for m in range(0, (m_mult << a) + 1):
            got = G(m, D)
            if a == 0:
                want = 1
            elif D > 2 * m:
                want = 0
            else:
                want = int((m + 1) % (1 << a) == 0)
            if got != want:
                return False
    return True


def pred5(m: int, k: int) -> int:
    mod = 1 << (k + 3)
    rs = {
        (3 * (1 << k) - 1) % mod,
        (5 * (1 << k) - 1) % mod,
        (3 * (1 << (k + 1)) - 1) % mod,
        ((1 << (k + 3)) - 1) % mod,
    }
    return int(m % mod in rs)


def four_point_ok(kmax: int, m_mult: int) -> bool:
    for k in range(0, kmax + 1):
        D = 5 * (1 << k) - 1
        for m in range(0, (m_mult << k) + 1):
            if G(m, D) != pred5(m, k):
                return False
    return True


def green_times(U: int, q: int, p: int) -> list[int]:
    end = q * U
    out = []
    for t in range(U, end):
        if p > 2 * t:
            continue
        m = end - t - 1
        if G(m, end - p):
            out.append(t)
    return out


def fires(rows: list[int], t: int, p: int) -> int:
    A = (rows[t] << 1) & rows[t]
    return (A >> p) & 1


def unique_census(rows: list[int], k: int) -> dict:
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
    uniq = sorted(p for p, ts in by_p.items() if len(ts) == 1)
    expected = [1, (U >> 1) + 1, U + 1, (U << 1) + 1]
    fire = {}
    times = {}
    for p in expected:
        ts = by_p.get(p, [])
        times[p] = ts[0] if len(ts) == 1 else None
        fire[p] = fires(rows, ts[0], p) if len(ts) == 1 else 0
    return {
        "uniq": uniq,
        "n_unique": len(uniq),
        "expected": expected,
        "times": times,
        "fire": fire,
        "theta": ((rows[end] >> end) & 1) ^ ((rows[U] >> U) & 1),
    }


def self_checks(c20, merse: bool, four: bool, recs: list[dict]) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert merse and four
    fires_half = []
    fires_U1 = []
    fires_2U1 = []
    for rec in recs:
        k = rec["k"]
        U = 1 << k
        assert rec["t_p1"] == U and rec["fire_p1"] == 1
        assert rec["n_p1"] == rec["n_half"] == rec["n_U1"] == rec["n_2U1"] == 1
        assert rec["t_half"] == 3 * (U >> 1)
        assert rec["t_U1"] == U
        assert rec["t_2U1"] == 2 * U
        if k >= 3:
            assert rec["n_unique"] == 4
            assert rec["uniq"] == [1, (U >> 1) + 1, U + 1, 2 * U + 1]
        fires_half.append(rec["fire_half"])
        fires_U1.append(rec["fire_U1"])
        fires_2U1.append(rec["fire_2U1"])
    assert 0 in fires_half and 1 in fires_half
    assert 0 in fires_U1 and 1 in fires_U1
    assert 0 in fires_2U1 and 1 in fires_2U1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    merse = merse_tgt_ok(10, 8)
    four = four_point_ok(7, 16)
    kmax = 8
    rows = evolve_rows(3 * (1 << kmax))
    recs = []
    for k in range(3, kmax + 1):
        U = 1 << k
        cen = unique_census(rows, k)
        recs.append({
            "k": k,
            "n_unique": cen["n_unique"],
            "uniq": cen["uniq"],
            "t_p1": green_times(U, 3, 1)[0],
            "t_half": green_times(U, 3, (U >> 1) + 1)[0],
            "t_U1": green_times(U, 3, U + 1)[0],
            "t_2U1": green_times(U, 3, 2 * U + 1)[0],
            "n_p1": len(green_times(U, 3, 1)),
            "n_half": len(green_times(U, 3, (U >> 1) + 1)),
            "n_U1": len(green_times(U, 3, U + 1)),
            "n_2U1": len(green_times(U, 3, 2 * U + 1)),
            "fire_p1": cen["fire"][1],
            "fire_half": cen["fire"][(U >> 1) + 1],
            "fire_U1": cen["fire"][U + 1],
            "fire_2U1": cen["fire"][2 * U + 1],
            "theta": cen["theta"],
        })
    checks = self_checks(c20, merse, four, recs)
    dump = {
        "cycle": "AP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {"mersenne_target": merse, "four_point_5": four},
        "annulus": recs,
        "lemmas": {
            "mersenne_target": True,
            "four_point_5fold": True,
            "four_unique_green_bits": True,
            "exactly_four_all_k": None,
            "extra_unique_always_fire": False,
            "theta_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "mersenne_target": "LEMMA",
            "four_point_5fold": "LEMMA",
            "four_unique_green_bits": "LEMMA",
            "exactly_four_all_k": "PREFIX",
            "extra_unique_always_fire": "KILLED",
            "theta_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("annulus", [
        {key: rec[key] for key in rec if key != "uniq"}
        for rec in recs
    ])


if __name__ == "__main__":
    main()
