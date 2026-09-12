#!/usr/bin/env python3
"""Cycle GU: at odd s=t0+2t+1, even-r Green is G(UQ-t-1, W/2-r/2).

Cycle GT showed off-hit times still carry AND. Cycle GM's freshman
half at hits is the t=qU slice of a clock that runs at every odd s:
m=2(UQ-t-1), G(m,W-r)=G(UQ-t-1, W/2-r/2), and odd-r Green vanishes.
The clock is not the hit Mersenne clock off-hit; naive half fails at
even s. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_gu.py --certify
Dump: research/cycle_gu.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits

OUT = Path(__file__).resolve().with_suffix(".json")
GT_JSON = Path(__file__).resolve().parent / "cycle_gt.json"
GM_JSON = Path(__file__).resolve().parent / "cycle_gm.json"
GJ_JSON = Path(__file__).resolve().parent / "cycle_gj.json"


def odd_clock(t: int, U: int, Q: int) -> int:
    """Reduced Green clock at odd s=t0+2t+1."""
    return U * Q - t - 1


def odd_s_clock() -> dict:
    """m=2(UQ-t-1) on every odd s; hits recover U(Q-q)-1. k<=11."""
    n_ok = 0
    n_hits = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for s in range(t0, T):
                if s % 2 == 0:
                    continue
                delta = s - t0
                t = delta // 2
                m = T - s - 1
                clock = odd_clock(t, U, Q)
                if m != 2 * clock or clock < 0:
                    return {"ok": False, "k": k, "s": s, "m": m, "clock": clock}
                if delta % (2 * U) == 1:
                    q = delta // (2 * U)
                    if clock != U * (Q - q) - 1:
                        return {
                            "ok": False,
                            "hit": True,
                            "k": k,
                            "q": q,
                            "clock": clock,
                        }
                    n_hits += 1
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_hits": n_hits}


def odd_s_green() -> dict:
    """G(m,W-r)=G(UQ-t-1, W/2-r/2) on even r; odd-r Green=0. k<=6."""
    n_even = 0
    n_odd = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for s in range(t0, T):
                if s % 2 == 0:
                    continue
                delta = s - t0
                t = delta // 2
                m = T - s - 1
                clock = odd_clock(t, U, Q)
                lo = 2 * (delta + 1)
                hi = min(2 * s - T, W)
                if hi < lo:
                    continue
                for r in range(lo, hi + 1):
                    g = G(m, W - r)
                    if r % 2:
                        if g != 0:
                            return {"ok": False, "odd_r": True, "k": k, "r": r}
                        n_odd += 1
                    else:
                        red = G(clock, W // 2 - r // 2)
                        if g != red:
                            return {
                                "ok": False,
                                "k": k,
                                "s": s,
                                "r": r,
                                "g": g,
                                "red": red,
                            }
                        n_even += 1
    return {"ok": n_even > 0, "n_even": n_even, "n_odd": n_odd}


def killed_even_s_half() -> dict:
    """Naive half at even s: k=0, W=4U, s=4, r=2, G=1 vs 0."""
    k = 0
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    s = 4
    r = 2
    m = T - s - 1
    g = G(m, W - r)
    half = G(m // 2, W // 2 - r // 2)
    ok = s % 2 == 0 and g == 1 and half == 0
    return {"ok": ok, "k": k, "s": s, "r": r, "G": g, "half": half}


def killed_offhit_mersenne() -> dict:
    """Off-hit clock is not a hit Mersenne clock: k=2, W=8U, delta=3."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = W // (4 * U)
    t = 1
    clock = odd_clock(t, U, Q)
    hit0 = U * (Q - 0) - 1
    hit1 = U * (Q - 1) - 1
    ok = clock == 6 and clock != hit0 and clock != hit1
    return {
        "ok": ok,
        "k": k,
        "delta": 3,
        "clock": clock,
        "hit_clocks": [hit0, hit1],
    }


def killed_red_G_1() -> dict:
    """Reduced G is not identically 1: k=2, W=8U, delta=3, r=10."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = W // (4 * U)
    t = 1
    clock = odd_clock(t, U, Q)
    r = 10
    red = G(clock, W // 2 - r // 2)
    ok = red == 0
    return {"ok": ok, "k": k, "r": r, "clock": clock, "G_red": red}


def prefixes() -> dict:
    gt = json.loads(GT_JSON.read_text())
    gm = json.loads(GM_JSON.read_text())
    gj = json.loads(GJ_JSON.read_text())
    ok = (
        gt["checks"]["all_ok"]
        and gm["checks"]["all_ok"]
        and gj["checks"]["all_ok"]
        and gt["verdict"]["k4_AND_lo_dead_on_covering_hits"] == "LEMMA"
        and gm["verdict"]["even_r_G_eq_G_Un_minus_1_W_over_2_minus_r_over_2"]
        == "LEMMA"
        and gj["verdict"]["m_eq_2U_Q_minus_q_minus_2"] == "LEMMA"
        and gt["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, cl: dict, gr: dict, ke: dict, km: dict, kr: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cl["ok"] and gr["ok"]
    assert ke["ok"] and km["ok"] and kr["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cl = odd_s_clock()
    grn = odd_s_green()
    ke = killed_even_s_half()
    km = killed_offhit_mersenne()
    kr = killed_red_G_1()
    pref = prefixes()
    checks = self_checks(c20, cl, grn, ke, km, kr, pref)
    dump = {
        "cycle": "GU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "odd_s_clock": {k: cl[k] for k in cl if k != "ok"},
        "odd_s_green": {k: grn[k] for k in grn if k != "ok"},
        "killed_even_s_half": {k: ke[k] for k in ke if k != "ok"},
        "killed_offhit_mersenne": {k: km[k] for k in km if k != "ok"},
        "killed_red_G_1": {k: kr[k] for k in kr if k != "ok"},
        "lemmas": {
            "odd_s_m_eq_2_UQ_minus_t_minus_1": True,
            "odd_s_even_r_G_eq_G_odd_clock": True,
            "odd_s_odd_r_G_eq_0": True,
            "even_s_naive_half": False,
            "offhit_clock_eq_hit_Mersenne": False,
            "odd_s_reduced_G_identically_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_s_m_eq_2_UQ_minus_t_minus_1": "LEMMA",
            "odd_s_even_r_G_eq_G_odd_clock": "LEMMA",
            "odd_s_odd_r_G_eq_0": "LEMMA",
            "even_s_naive_half": "KILLED",
            "offhit_clock_eq_hit_Mersenne": "KILLED",
            "odd_s_reduced_G_identically_1": "KILLED",
            "J6_J10_0_implies_J18_1_all_k": "PREFIX",
            "eleven_bit_gap": "PREFIX",
            "extra_414990_formula": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "I_1_infinitely_often": "OPEN",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("odd_s_clock", dump["odd_s_clock"])
    print("odd_s_green", dump["odd_s_green"])
    print("killed_even_s_half", dump["killed_even_s_half"])
    print("killed_offhit_mersenne", dump["killed_offhit_mersenne"])
    print("killed_red_G_1", dump["killed_red_G_1"])


if __name__ == "__main__":
    main()
