#!/usr/bin/env python3
"""Cycle DE: π_k=2^{ceil(log2 k)} through 18; odd high toggle iff k is a 2-power.

The left-word period at t=2W equals 2^{ceil(log2 k)} for 1<=k<=18, so the
period-H seed holds through k=18 (the formula divides 2^{k-1} for every
k>=1). In the high half (W,2W], an odd ident-0 occurs iff k is a 2-power,
for every 1<=k<=16, at packed bits 3,8,29,400,87867. Non-powers may have
even ident-0s (k=15 has two). Not a prize claim: the formula is a prefix.

Run: python3 research/cycle_de.py --certify
Dump: research/cycle_de.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_ca import (
    KNOWN20,
    apply_n,
    left_at_2W,
    min_period,
    packed_center_bits,
    prize_cycle,
    reconstruct,
    xorcat,
)
from cycle_cb import ext

OUT = Path(__file__).resolve().with_suffix(".json")
EXPECTED_ODD_P = {1: 3, 2: 8, 4: 29, 8: 400, 16: 87867}


def pi_formula(k: int) -> int:
    return 1 if k <= 1 else 1 << math.ceil(math.log2(k))


def formula_divides_H(kmax: int = 64) -> bool:
    """2^{ceil(log2 k)} divides 2^{k-1} for every k>=1."""
    for k in range(1, kmax + 1):
        pi = pi_formula(k)
        H = 1 << (k - 1)
        if H % pi:
            return False
    return True


def seed_through_18() -> dict:
    pis: list[int] = []
    for k in range(1, 19):
        W = 1 << k
        H = W >> 1
        w = left_at_2W(k)
        pi = min_period(w, W)
        if pi != pi_formula(k) or apply_n(w, W, H) != w or H % pi:
            return {"ok": False, "k": k, "pi": pi, "pis": pis}
        pis.append(pi)
    return {"ok": True, "pis": pis}


def high_odd_toggles(kmax: int = 16) -> dict:
    """Odd ident-0 in (W, 2W] iff k is a 2-power, through kmax."""
    odd_p: dict[int, int] = {}
    even_n: dict[int, int] = {}
    for k in range(1, kmax + 1):
        pi, cyc = prize_cycle(k)
        W = 1 << k
        seqs = {p: [(w >> p) & 1 for w in cyc] for p in range(W + 1)}
        cur_pi = pi
        n_odd = 0
        n_even = 0
        last_odd = None
        p = W + 1
        while p <= 2 * W:
            a = ext(seqs[p - 2], cur_pi)
            b = ext(seqs[p - 1], cur_pi)
            if all(x == 0 for x in b):
                sm = xorcat(a)
                u = [0] * cur_pi
                for t in range(cur_pi - 1):
                    u[t + 1] = a[t] ^ u[t]
                if sm == 1:
                    n_odd += 1
                    last_odd = p
                    u = u + [x ^ 1 for x in u]
                    cur_pi *= 2
                else:
                    n_even += 1
                seqs[p] = u
            else:
                seqs[p] = reconstruct(a, b)
            p += 1
        pow2 = k > 0 and (k & (k - 1)) == 0
        if n_odd != (1 if pow2 else 0):
            return {"ok": False, "k": k, "n_odd": n_odd, "pow2": pow2}
        if pow2:
            if last_odd != EXPECTED_ODD_P[k] or not (W < last_odd <= 2 * W):
                return {"ok": False, "k": k, "p": last_odd}
            odd_p[k] = last_odd
        even_n[k] = n_even
    return {"ok": True, "odd_p": odd_p, "even_n": even_n}


def self_checks(c20, loc: bool, seed: dict, high: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert loc
    assert seed["ok"] and seed["pis"] == [pi_formula(k) for k in range(1, 19)]
    assert seed["pis"][-1] == 32
    assert high["ok"]
    assert high["odd_p"] == EXPECTED_ODD_P
    assert high["even_n"][15] == 2
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    loc = formula_divides_H()
    seed = seed_through_18()
    high = high_odd_toggles(16)
    checks = self_checks(c20, loc, seed, high)
    dump = {
        "cycle": "DE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "pis": seed["pis"],
        "odd_high_p": high["odd_p"],
        "even_high_n15": high["even_n"][15],
        "lemmas": {
            "formula_divides_H": True,
            "pi_formula_k_le_18": True,
            "period_H_seed_k_le_18": True,
            "odd_high_toggle_iff_k_pow2_le_16": True,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "formula_divides_H": "LEMMA",
            "pi_formula_k_le_18": "LEMMA",
            "period_H_seed_k_le_18": "LEMMA",
            "odd_high_toggle_iff_k_pow2_le_16": "LEMMA",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("pis", dump["pis"])
    print("odd_high_p", dump["odd_high_p"])
    print("even_high_n15", dump["even_high_n15"])


if __name__ == "__main__":
    main()
