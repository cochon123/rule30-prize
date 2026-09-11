#!/usr/bin/env python3
"""Cycle AR: Green lift G(m, q*2^j-1); five triples and four quadruples.

For j>=1, G(m, q*2^j-1)=1 iff 2^j divides (m+1) and
G((m+1)/2^j-1, q-1)=1. Fermat-odd q=2^a+1 reduces the second factor
to Cycle AQ's G(n, 2^a), recovering Cycle AO (a=1) and Cycle AP (a=2).
On the 3-fold annulus the five triple-Green bits and four
quadruple-Green bits of Cycle AQ's histogram have closed times, because
the lift window n <= 2^{1+j_off}-1 is independent of k. None of those
nine bits is an identically-1 production. Exhaustiveness of the nine
is a prefix. Bit B's firing XOR is not k mod 2 (dies at k=9).

Not a prize claim: theta_k=1 infinitely often remains open.

Run: python3 research/cycle_ar.py --certify
Dump: research/cycle_ar.json
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


def lift_want(m: int, q: int, j: int) -> int:
    if (m + 1) % (1 << j):
        return 0
    n = (m + 1) // (1 << j) - 1
    return G(n, q - 1)


def lift_ok(qmax: int, jmax: int, m_mult: int) -> bool:
    for q in range(1, qmax + 1):
        for j in range(1, jmax + 1):
            D = q * (1 << j) - 1
            for m in range(0, m_mult * q * (1 << j) + 1):
                if G(m, D) != lift_want(m, q, j):
                    return False
    return True


def ao_pred(m: int, j: int) -> int:
    mod = 1 << (j + 2)
    return int(m % mod in ((1 << (j + 1)) - 1, 3 * (1 << j) - 1))


def ap_pred(m: int, j: int) -> int:
    mod = 1 << (j + 3)
    rs = {
        (3 * (1 << j) - 1) % mod,
        (5 * (1 << j) - 1) % mod,
        (3 * (1 << (j + 1)) - 1) % mod,
        ((1 << (j + 3)) - 1) % mod,
    }
    return int(m % mod in rs)


def fermat_recover_ok(jmax: int, m_mult: int) -> bool:
    """Lift of G(n, 2^a) recovers AO (a=1) and AP (a=2)."""
    for a, pred in ((1, ao_pred), (2, ap_pred)):
        q = (1 << a) + 1
        for j in range(1, jmax + 1):
            D = q * (1 << j) - 1
            for m in range(0, m_mult * (1 << j) + 1):
                got = G(m, D)
                want = lift_want(m, q, j)
                if got != want:
                    return False
                periodic = pred(m, j)
                if D <= 2 * m and got != periodic:
                    return False
    return True


def ones_upto(d: int, nmax: int) -> list[int]:
    return [n for n in range(nmax + 1) if G(n, d)]


def green_times(U: int, p: int) -> list[int]:
    end = 3 * U
    out = []
    for t in range(U, end):
        if p > 2 * t:
            continue
        m = end - t - 1
        if G(m, end - p):
            out.append(t)
    return out


def lift_times(U: int, p: int, q: int, j: int, nmax: int) -> list[int]:
    ts = []
    for n in ones_upto(q - 1, nmax):
        m = (1 << j) * (n + 1) - 1
        t = 3 * U - 1 - m
        if U <= t < 3 * U and p <= 2 * t:
            ts.append(t)
    return sorted(ts)


def fires(row: int, p: int) -> int:
    return (((row << 1) & row) >> p) & 1


def xor_fires(rows: list[int], p: int, ts: list[int]) -> tuple[list[int], int]:
    fs = [fires(rows[t], p) for t in ts]
    x = 0
    for f in fs:
        x ^= f
    return fs, x


def triple_specs(k: int) -> list[dict]:
    U = 1 << k
    return [
        {
            "name": "A",
            "p": (1 << (k - 3)) + 1,
            "q": 23,
            "j": k - 3,
            "nmax": 15,
            "times": [9 * U // 8, 5 * U // 4, 3 * U // 2],
        },
        {
            "name": "B",
            "p": (1 << (k - 2)) + 1,
            "q": 11,
            "j": k - 2,
            "nmax": 7,
            "times": [U, 5 * U // 4, 3 * U // 2],
        },
        {
            "name": "C",
            "p": 5 * (1 << (k - 3)) + 1,
            "q": 19,
            "j": k - 3,
            "nmax": 15,
            "times": [U, 13 * U // 8, 7 * U // 4],
        },
        {
            "name": "D",
            "p": 3 * (1 << (k - 2)) + 1,
            "q": 9,
            "j": k - 2,
            "nmax": 7,
            "times": [U, 3 * U // 2, 7 * U // 4],
        },
        {
            "name": "E",
            "p": 5 * (1 << (k - 1)) + 1,
            "q": 1,
            "j": k - 1,
            "nmax": 3,
            "times": [3 * U // 2, 2 * U, 5 * U // 2],
        },
    ]


def quad_specs(k: int) -> list[dict]:
    U = 1 << k
    return [
        {
            "name": "Q1",
            "p": 9 * (1 << (k - 3)) + 1,
            "q": 15,
            "j": k - 3,
            "nmax": 15,
            "times": [9 * U // 8, 5 * U // 4, 3 * U // 2, 2 * U],
        },
        {
            "name": "Q2",
            "p": 5 * (1 << (k - 2)) + 1,
            "q": 7,
            "j": k - 2,
            "nmax": 7,
            "times": [U, 5 * U // 4, 3 * U // 2, 2 * U],
        },
        {
            "name": "Q3",
            "p": 7 * (1 << (k - 2)) + 1,
            "q": 5,
            "j": k - 2,
            "nmax": 7,
            "times": [U, 3 * U // 2, 7 * U // 4, 9 * U // 4],
        },
        {
            "name": "Q4",
            "p": 9 * (1 << (k - 2)) + 1,
            "q": 3,
            "j": k - 2,
            "nmax": 7,
            "times": [5 * U // 4, 3 * U // 2, 9 * U // 4, 5 * U // 2],
        },
    ]


def window_ones_ok() -> bool:
    """Finite n-windows that make the 3-fold counts independent of k."""
    want = {
        (22, 15): [11, 13, 14],
        (10, 7): [5, 6, 7],
        (18, 15): [9, 10, 15],
        (8, 7): [4, 5, 7],
        (0, 3): [0, 1, 2, 3],
        (14, 15): [7, 11, 13, 14],
        (6, 7): [3, 5, 6, 7],
        (4, 7): [2, 4, 5, 7],
        (2, 7): [1, 2, 5, 6],
    }
    for (d, nmax), ns in want.items():
        if ones_upto(d, nmax) != ns:
            return False
    return True


def hit_census(k: int) -> dict:
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
    triples = sorted(p for p, ts in by_p.items() if len(ts) == 3)
    quads = sorted(p for p, ts in by_p.items() if len(ts) == 4)
    return {
        "n1": sum(1 for ts in by_p.values() if len(ts) == 1),
        "n2": sum(1 for ts in by_p.values() if len(ts) == 2),
        "n3": len(triples),
        "n4": len(quads),
        "triples": triples,
        "quads": quads,
        "expected_triples": [sp["p"] for sp in triple_specs(k)],
        "expected_quads": [sp["p"] for sp in quad_specs(k)],
    }


def bit_record(rows: list[int], k: int, sp: dict) -> dict:
    U = 1 << k
    p, q, j, nmax = sp["p"], sp["q"], sp["j"], sp["nmax"]
    got = green_times(U, p)
    pred = lift_times(U, p, q, j, nmax)
    fs, xor = xor_fires(rows, p, got)
    return {
        "name": sp["name"],
        "p": p,
        "times": got,
        "lift_times": pred,
        "formula_times": sp["times"],
        "n": len(got),
        "fire": fs,
        "xor": xor,
        "match": got == pred == sp["times"],
    }


def self_checks(
    c20,
    lift: bool,
    fermat: bool,
    windows: bool,
    recs: list[dict],
    b9_fire: list[int],
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert lift and fermat and windows
    xor_tri: dict[str, list[int]] = defaultdict(list)
    xor_quad: dict[str, list[int]] = defaultdict(list)
    for rec in recs:
        k = rec["k"]
        assert rec["n3"] == 5
        assert rec["n4"] == 4
        assert rec["triples"] == rec["expected_triples"]
        assert rec["quads"] == rec["expected_quads"]
        for tr in rec["triple_bits"]:
            assert tr["match"] and tr["n"] == 3
            xor_tri[tr["name"]].append(tr["xor"])
        for qd in rec["quad_bits"]:
            assert qd["match"] and qd["n"] == 4
            xor_quad[qd["name"]].append(qd["xor"])
    for name, xs in xor_tri.items():
        assert 0 in xs, name
    for name, xs in xor_quad.items():
        assert 0 in xs and 1 in xs, name
    # AQ prefix "B xor = k mod 2 on k=4..8" dies at odd k=9 (all zeros).
    assert b9_fire == [0, 0, 0]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    lift = lift_ok(16, 6, 4)
    fermat = fermat_recover_ok(8, 16)
    windows = window_ones_ok()
    kmax = 8
    rows = evolve_rows(3 * (1 << kmax))
    recs = []
    for k in range(4, kmax + 1):
        cen = hit_census(k)
        recs.append({
            "k": k,
            **cen,
            "triple_bits": [bit_record(rows, k, sp) for sp in triple_specs(k)],
            "quad_bits": [bit_record(rows, k, sp) for sp in quad_specs(k)],
        })
    rows9 = evolve_rows(3 * (1 << 9) // 2 + 2)
    b9 = triple_specs(9)[1]
    b9_fire = [fires(rows9[t], b9["p"]) for t in b9["times"]]
    checks = self_checks(c20, lift, fermat, windows, recs, b9_fire)
    dump = {
        "cycle": "AR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "lift": lift,
            "fermat_recovers_AO_AP": fermat,
            "window_ones": windows,
        },
        "annulus": [
            {
                "k": rec["k"],
                "n1": rec["n1"],
                "n2": rec["n2"],
                "n3": rec["n3"],
                "n4": rec["n4"],
                "triples": rec["triples"],
                "quads": rec["quads"],
                "triple_xor": {tr["name"]: tr["xor"] for tr in rec["triple_bits"]},
                "triple_fire": {tr["name"]: tr["fire"] for tr in rec["triple_bits"]},
                "quad_xor": {qd["name"]: qd["xor"] for qd in rec["quad_bits"]},
            }
            for rec in recs
        ],
        "bit_B_k9_fire": b9_fire,
        "lemmas": {
            "green_lift": True,
            "fermat_odd_reduces_to_pow2": True,
            "recovers_AO_AP": True,
            "five_triples_times": True,
            "four_quadruples_times": True,
            "exactly_five_triples_all_k": None,
            "exactly_four_quadruples_all_k": None,
            "triple_always_xor_1": False,
            "quadruple_always_xor_1": False,
            "bit_B_xor_k_mod_2": False,
            "bit_D_never_fires": None,
            "theta_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "green_lift": "LEMMA",
            "fermat_odd_reduces_to_pow2": "LEMMA",
            "recovers_AO_AP": "LEMMA",
            "five_triples_times": "LEMMA",
            "four_quadruples_times": "LEMMA",
            "exactly_five_triples_all_k": "PREFIX",
            "exactly_four_quadruples_all_k": "PREFIX",
            "triple_always_xor_1": "KILLED",
            "quadruple_always_xor_1": "KILLED",
            "bit_B_xor_k_mod_2": "KILLED",
            "bit_D_never_fires": "PREFIX",
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
    print("bit_B_k9_fire", b9_fire)


if __name__ == "__main__":
    main()
