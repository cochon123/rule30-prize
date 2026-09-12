#!/usr/bin/env python3
"""Cycle GV: at even s=t0+2t, m=2n+1 with n=UQ-t-1 (same clock as GU).

Even-r Green is G(n, d/2) XOR G(n, d/2-1); odd-r Green is
G(n, (d-1)/2). That is not the odd-s single term G(n, d/2); odd-r
Green is not identically 0. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_gv.py --certify
Dump: research/cycle_gv.json
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
from cycle_gu import odd_clock

OUT = Path(__file__).resolve().with_suffix(".json")
GU_JSON = Path(__file__).resolve().parent / "cycle_gu.json"
GM_JSON = Path(__file__).resolve().parent / "cycle_gm.json"
GT_JSON = Path(__file__).resolve().parent / "cycle_gt.json"


def even_s_clock() -> dict:
    """m=2n+1 with n=UQ-t-1 on every even s. k<=11."""
    n_ok = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for s in range(t0, T):
                if s % 2:
                    continue
                t = (s - t0) // 2
                m = T - s - 1
                n = odd_clock(t, U, Q)
                if m != 2 * n + 1 or n < 0:
                    return {"ok": False, "k": k, "s": s, "m": m, "n": n}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def even_s_green() -> dict:
    """Even-r: G(n,d/2) XOR G(n,d/2-1); odd-r: G(n,(d-1)/2). k<=6."""
    n_even = 0
    n_odd = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for s in range(t0, T):
                if s % 2:
                    continue
                delta = s - t0
                t = delta // 2
                m = T - s - 1
                n = odd_clock(t, U, Q)
                lo = 2 * (delta + 1)
                hi = min(2 * s - T, W)
                if hi < lo:
                    continue
                for r in range(lo, hi + 1):
                    g = G(m, W - r)
                    d = W - r
                    if r % 2 == 0:
                        want = G(n, d // 2) ^ G(n, d // 2 - 1)
                        if g != want:
                            return {
                                "ok": False,
                                "k": k,
                                "s": s,
                                "r": r,
                                "g": g,
                                "want": want,
                            }
                        n_even += 1
                    else:
                        want = G(n, (d - 1) // 2)
                        if g != want:
                            return {
                                "ok": False,
                                "odd": True,
                                "k": k,
                                "s": s,
                                "r": r,
                                "g": g,
                                "want": want,
                            }
                        n_odd += 1
    return {"ok": n_even > 0, "n_even": n_even, "n_odd": n_odd}


def killed_eq_odd_s_term() -> dict:
    """Even-s even-r Green is not G(n, d/2): k=0, W=4U, s=4, r=2."""
    k = 0
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    s, r = 4, 2
    t = (s - (T - W // 2)) // 2
    n = odd_clock(t, U, W // (4 * U))
    g = G(T - s - 1, W - r)
    naive = G(n, (W - r) // 2)
    ok = g == 1 and naive == 0
    return {"ok": ok, "k": k, "s": s, "r": r, "G": g, "naive": naive}


def killed_odd_r_0() -> dict:
    """Odd-r Green is not 0 at even s: k=1, W=4U, s=8, r=3."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s, r = 8, 3
    g = G(T - s - 1, W - r)
    ok = s == t0 and s % 2 == 0 and r % 2 == 1 and g == 1
    return {"ok": ok, "k": k, "s": s, "r": r, "G": g}


def killed_even_r_0() -> dict:
    """Even-r Green is not 0 at even s: same k=0 witness as naive half."""
    k = 0
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    s, r = 4, 2
    g = G(T - s - 1, W - r)
    ok = s % 2 == 0 and r % 2 == 0 and g == 1
    return {"ok": ok, "k": k, "s": s, "r": r, "G": g}


def prefixes() -> dict:
    gu = json.loads(GU_JSON.read_text())
    gm = json.loads(GM_JSON.read_text())
    gt = json.loads(GT_JSON.read_text())
    ok = (
        gu["checks"]["all_ok"]
        and gm["checks"]["all_ok"]
        and gt["checks"]["all_ok"]
        and gu["verdict"]["odd_s_m_eq_2_UQ_minus_t_minus_1"] == "LEMMA"
        and gm["verdict"]["even_r_G_eq_G_Un_minus_1_W_over_2_minus_r_over_2"]
        == "LEMMA"
        and gt["verdict"]["k4_AND_lo_dead_on_covering_hits"] == "LEMMA"
        and gu["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, cl: dict, gr: dict, kn: dict, ko: dict, ke: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cl["ok"] and gr["ok"]
    assert kn["ok"] and ko["ok"] and ke["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cl = even_s_clock()
    grn = even_s_green()
    kn = killed_eq_odd_s_term()
    ko = killed_odd_r_0()
    ke = killed_even_r_0()
    pref = prefixes()
    checks = self_checks(c20, cl, grn, kn, ko, ke, pref)
    dump = {
        "cycle": "GV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_s_clock": {k: cl[k] for k in cl if k != "ok"},
        "even_s_green": {k: grn[k] for k in grn if k != "ok"},
        "killed_eq_odd_s_term": {k: kn[k] for k in kn if k != "ok"},
        "killed_odd_r_0": {k: ko[k] for k in ko if k != "ok"},
        "killed_even_r_0": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "even_s_m_eq_2n_plus_1_n_odd_clock": True,
            "even_s_even_r_G_eq_two_term_XOR": True,
            "even_s_odd_r_G_eq_G_n_d_minus_1_over_2": True,
            "even_s_eq_odd_s_single_term": False,
            "even_s_odd_r_G_eq_0": False,
            "even_s_even_r_G_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_s_m_eq_2n_plus_1_n_odd_clock": "LEMMA",
            "even_s_even_r_G_eq_two_term_XOR": "LEMMA",
            "even_s_odd_r_G_eq_G_n_d_minus_1_over_2": "LEMMA",
            "even_s_eq_odd_s_single_term": "KILLED",
            "even_s_odd_r_G_eq_0": "KILLED",
            "even_s_even_r_G_eq_0": "KILLED",
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
    print("even_s_clock", dump["even_s_clock"])
    print("even_s_green", dump["even_s_green"])
    print("killed_eq_odd_s_term", dump["killed_eq_odd_s_term"])
    print("killed_odd_r_0", dump["killed_odd_r_0"])
    print("killed_even_r_0", dump["killed_even_r_0"])


if __name__ == "__main__":
    main()
