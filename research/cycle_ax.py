#!/usr/bin/env python3
"""Cycle AX: triple-Green bits are the 5,7,9,13 families.

For a>=5 the even half-window triples are exactly 2^a-{6,8,10,14}.
Odd triples are 2d+1 with d a triple one level down. Packed bits are
p=q*2^j+1 for q in {5,7,9,13} with j bounded by the unique/double
cutoffs. G(n, 2^a-14)=1 iff s in {0,5,6}. Bits 14 and 15 contribute
0. Exactly five quads is a prefix. Triple XOR is not I_k.

Not a prize claim: I_k=1 infinitely often remains open.

Run: python3 research/cycle_ax.py --certify
Dump: research/cycle_ax.json
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
SEED_Q = (6, 8, 10, 14)
SEED_S = {6: [0, 1, 2], 8: [0, 2, 3], 10: [1, 2, 4], 14: [0, 5, 6]}
FAM_Q = (5, 7, 9, 13)
FAM_JMAX_OFF = {5: 4, 7: 4, 9: 5, 13: 5}  # j <= k - offset


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


def support(a: int, D: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    return [n for n in range(nmax + 1) if G(n, D)]


def ones_s(a: int, q: int) -> list[int]:
    nmax = (1 << (a - 1)) - 1
    D = (1 << a) - q
    return sorted(nmax - n for n in range(nmax + 1) if G(n, D))


def g14_ok(amax: int) -> bool:
    for a in range(5, amax + 1):
        if ones_s(a, 14) != [0, 5, 6]:
            return False
    return True


def even_triples_ok(amax: int) -> bool:
    for a in range(5, amax + 1):
        nmax = (1 << (a - 1)) - 1
        want = {(1 << a) - q for q in SEED_Q}
        got = {D for D in range(0, 2 * nmax + 1, 2) if len(support(a, D)) == 3}
        if got != want:
            return False
    return True


def odd_lifts_ok(amax: int) -> bool:
    for a in range(5, amax + 1):
        nmax = (1 << (a - 1)) - 1
        prev = {D for D in range(0, 2 * ((1 << (a - 2)) - 1) + 1)
                if len(support(a - 1, D)) == 3}
        lifted = {2 * d + 1 for d in prev}
        got = {D for D in range(1, 2 * nmax + 1, 2) if len(support(a, D)) == 3}
        if got != lifted:
            return False
    return True


def even_mech_ok(cmax: int) -> bool:
    """Mechanism (i): only consecutive uniques with distinct supports.
    Mechanism (ii): even-seed predecessors give 2^a-10,14 not 18,26.
    """
    for c in range(5, cmax + 1):
        nmax = (1 << (c - 1)) - 1
        # (i) unique D, D+1 also unique, A != B
        uniq = []
        for D in range(0, 2 * nmax + 1):
            sl = support(c, D)
            if len(sl) == 1:
                uniq.append((D, sl[0]))
        pairs = []
        for i in range(len(uniq) - 1):
            if uniq[i + 1][0] == uniq[i][0] + 1 and uniq[i][1] != uniq[i + 1][1]:
                pairs.append((uniq[i][0], uniq[i + 1][0]))
        want_pairs = [((1 << c) - 5, (1 << c) - 4), ((1 << c) - 4, (1 << c) - 3)]
        if pairs != want_pairs:
            return False
        # (ii) A subset B for q=6,8; not for 10,14
        for q, good in ((6, True), (8, True), (10, False), (14, False)):
            B = set(support(c, (1 << c) - q))
            A = set(support(c, (1 << c) - q + 1))
            if (A <= B) != good:
                return False
    return True


def expected_triple_p(k: int) -> list[int]:
    out = []
    for q, off in FAM_JMAX_OFF.items():
        for j in range(0, max(0, k - off + 1)):
            out.append(q * (1 << j) + 1)
    return sorted(out)


def expected_times(k: int, q: int, j: int) -> list[int]:
    T = 1 << (k - 1)
    seed = {5: 6, 7: 8, 9: 10, 13: 14}[q]
    return [T + s * (1 << j) for s in SEED_S[seed]]


def hit_census(k: int) -> dict:
    T = 1 << (k - 1)
    end = 1 << k
    by_p: dict[int, list[int]] = defaultdict(list)
    for t in range(T, end):
        m = end - t - 1
        lo = max(0, end - 2 * m)
        hi = min(end, 2 * t)
        for p in range(lo, hi + 1):
            if G(m, end - p):
                by_p[p].append(t)
    tr = sorted(p for p, ts in by_p.items() if len(ts) == 3)
    qd = sorted(p for p, ts in by_p.items() if len(ts) == 4)
    return {"T": T, "n3": len(tr), "triples": tr, "n4": len(qd), "quads": qd,
            "times": {p: by_p[p] for p in tr}}


def family_times_ok(k: int, cen: dict) -> bool:
    for q, off in FAM_JMAX_OFF.items():
        for j in range(0, max(0, k - off + 1)):
            p = q * (1 << j) + 1
            if cen["times"].get(p) != expected_times(k, q, j):
                return False
    return True


def quad_prefix_ok(amax: int) -> bool:
    prev = None
    for a in range(5, amax + 1):
        nmax = (1 << (a - 1)) - 1
        ps = sorted((1 << a) - D for D in range(0, 2 * nmax + 1)
                    if len(support(a, D)) == 4)
        if len(ps) != 5:
            return False
        if a == 5:
            if ps != [18, 19, 23, 27, 29]:
                return False
        else:
            want = sorted(2 * p - 1 for p in prev)
            if ps != want:
                return False
        prev = ps
    return True


def xor_fires(rows: list[int], p: int, ts: list[int]) -> int:
    x = 0
    for t in ts:
        x ^= fires(rows[t], p)
    return x


def self_checks(
    c20, g14, even_tr, odd_lift, mech, recs, qpref, b14, b15, mismatches,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert g14 and even_tr and odd_lift and mech and qpref
    for rec in recs:
        k = rec["k"]
        assert rec["n3"] == 4 * k - 14
        assert rec["triples"] == rec["expected"]
        assert rec["family_times"]
        if k >= 5:
            assert rec["x14"] == 0
            assert rec["x15"] == 0
    assert b14 and b15
    assert mismatches, "triple XOR should fail as a formula for I_k"
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    g14 = g14_ok(12)
    even_tr = even_triples_ok(12)
    odd_lift = odd_lifts_ok(12)
    mech = even_mech_ok(11)
    qpref = quad_prefix_ok(10)

    k_ann = 8
    rows = evolve_rows(1 << k_ann)
    recs = []
    mismatches = []
    for k in range(4, k_ann + 1):
        cen = hit_census(k)
        T = cen["T"]
        end = 1 << k
        I = ((rows[end] >> end) & 1) ^ ((rows[T] >> T) & 1)
        tx = 0
        for p in cen["triples"]:
            tx ^= xor_fires(rows, p, cen["times"][p])
        if tx != I:
            mismatches.append(k)
        t14 = cen["times"].get(14, expected_times(k, 13, 0) if k >= 5 else [])
        t15 = cen["times"].get(15, expected_times(k, 7, 1) if k >= 5 else [])
        recs.append({
            "k": k,
            "T": T,
            "I": I,
            "n3": cen["n3"],
            "n4": cen["n4"],
            "triples": cen["triples"],
            "expected": expected_triple_p(k),
            "family_times": family_times_ok(k, cen),
            "triple_xor": tx,
            "x14": xor_fires(rows, 14, t14) if t14 else None,
            "x15": xor_fires(rows, 15, t15) if t15 else None,
            "t14": t14,
            "t15": t15,
        })
    b14 = all(rec["x14"] == 0 for rec in recs if rec["k"] >= 5)
    b15 = all(rec["x15"] == 0 for rec in recs if rec["k"] >= 5)
    checks = self_checks(
        c20, g14, even_tr, odd_lift, mech, recs, qpref, b14, b15, mismatches,
    )
    dump = {
        "cycle": "AX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "algebra": {
            "G_2a_minus_14": g14,
            "even_triples": even_tr,
            "odd_lifts": odd_lift,
            "even_mechanisms": mech,
            "quad_prefix": qpref,
        },
        "annulus": [
            {key: rec[key] for key in (
                "k", "T", "I", "n3", "n4", "triples", "triple_xor", "x14", "x15",
            )}
            for rec in recs
        ],
        "triple_xor_mismatch_k": mismatches,
        "lemmas": {
            "G_2a_minus_14": True,
            "even_triples_exactly_four": True,
            "triples_are_5_7_9_13_families": True,
            "bit14_contributes_0": True,
            "bit15_contributes_0": True,
            "exactly_five_quads_all_k": None,
            "triple_xor_is_I": False,
            "I_1_infinitely_often": None,
            "prize": False,
        },
        "verdict": {
            "G_2a_minus_14": "LEMMA",
            "even_triples_exactly_four": "LEMMA",
            "triples_are_5_7_9_13_families": "LEMMA",
            "bit14_contributes_0": "LEMMA",
            "bit15_contributes_0": "LEMMA",
            "exactly_five_quads_all_k": "PREFIX",
            "triple_xor_is_I": "KILLED",
            "I_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("annulus", dump["annulus"])
    print("triple_xor_mismatch_k", mismatches)


if __name__ == "__main__":
    main()
