#!/usr/bin/env python3
"""Cycle GM: at a cone-hi hit, even-r Green is G(U(Q-q)-1, W/2 - r/2).

Cycle GL's even r have even degree W-r. Cycle GJ's m=2U(Q-q)-2 is even,
so freshman gives G(m, W-r)=G(U(Q-q)-1, W/2 - r/2). The half-index
rho=r/2 runs through an interval of length U. The reduced clock is
not U-1 on pre-cone hits; naive half-index on odd r can be 1 while
G=0; reduced G is not identically 1. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gm.py --certify
Dump: research/cycle_gm.json
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
GL_JSON = Path(__file__).resolve().parent / "cycle_gl.json"
GJ_JSON = Path(__file__).resolve().parent / "cycle_gj.json"
GK_JSON = Path(__file__).resolve().parent / "cycle_gk.json"


def half_r() -> dict:
    """G(m, W-r)=G(U(Q-q)-1, W/2 - r/2) on even r; rho-interval length U."""
    n_ok = 0
    n_hits = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for q in range(Q):
                s = t0 + 1 + q * (2 * U)
                m = T - s - 1
                n = Q - q
                if m != 2 * (U * n - 1):
                    return {"ok": False, "k": k, "m": m}
                chi = 2 * s - T
                lo = 2 * (s - t0 + 1)
                if (chi // 2) - (lo // 2) + 1 != U:
                    return {"ok": False, "k": k, "nrho": (chi // 2) - (lo // 2) + 1}
                for r in range(lo, chi + 1, 2):
                    g = G(m, W - r)
                    red = G(U * n - 1, W // 2 - r // 2)
                    if g != red:
                        return {"ok": False, "k": k, "q": q, "r": r, "g": g, "red": red}
                    n_ok += 1
                n_hits += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_hits": n_hits}


def killed_odd_naive_half() -> dict:
    """Naive G(m/2, (W-r)//2) on odd r can be 1 while G=0."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = 2
    m = 2 * U * (Q - 0) - 2
    r = 5
    g = G(m, W - r)
    naive = G(m // 2, (W - r) // 2)
    ok = (r & 1) == 1 and g == 0 and naive == 1
    return {"ok": ok, "k": k, "r": r, "G": g, "naive": naive}


def killed_red_deg_U_minus_1() -> dict:
    """Reduced clock is not U-1 on a pre-cone hit."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = 2
    n0 = Q - 0
    red = U * n0 - 1
    ok = red == 7 and red != U - 1
    return {"ok": ok, "k": k, "red": red, "U_minus_1": U - 1}


def killed_red_identically_1() -> dict:
    """Reduced G is not identically 1: k=2, W=4U, r=8."""
    k = 2
    U = 1 << k
    W = 4 * U
    n = 1
    r = 8
    red = G(U * n - 1, W // 2 - r // 2)
    ok = red == 0
    return {"ok": ok, "k": k, "r": r, "G_red": red}


def prefixes() -> dict:
    gl = json.loads(GL_JSON.read_text())
    gj = json.loads(GJ_JSON.read_text())
    gk = json.loads(GK_JSON.read_text())
    ok = (
        gl["checks"]["all_ok"]
        and gj["checks"]["all_ok"]
        and gk["checks"]["all_ok"]
        and gl["verdict"]["hit_green_ones_only_even_r"] == "LEMMA"
        and gj["verdict"]["m_eq_2U_Q_minus_q_minus_2"] == "LEMMA"
        and gk["verdict"]["hit_cone_ones_eq_2U_plus_1_plus_k_mod_2_over_3"]
        == "LEMMA"
        and gl["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, half: dict, ko: dict, kd: dict, ki: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert half["ok"] and ko["ok"] and kd["ok"] and ki["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    half = half_r()
    ko = killed_odd_naive_half()
    kd = killed_red_deg_U_minus_1()
    ki = killed_red_identically_1()
    pref = prefixes()
    checks = self_checks(c20, half, ko, kd, ki, pref)
    dump = {
        "cycle": "GM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "half_r": {k: half[k] for k in half if k != "ok"},
        "killed_odd_naive_half": {k: ko[k] for k in ko if k != "ok"},
        "killed_red_deg_U_minus_1": {k: kd[k] for k in kd if k != "ok"},
        "killed_red_identically_1": {k: ki[k] for k in ki if k != "ok"},
        "lemmas": {
            "even_r_G_eq_G_Un_minus_1_W_over_2_minus_r_over_2": True,
            "rho_interval_length_eq_U": True,
            "odd_r_naive_half": False,
            "reduced_clock_eq_U_minus_1_on_precone": False,
            "reduced_G_identically_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_r_G_eq_G_Un_minus_1_W_over_2_minus_r_over_2": "LEMMA",
            "rho_interval_length_eq_U": "LEMMA",
            "odd_r_naive_half": "KILLED",
            "reduced_clock_eq_U_minus_1_on_precone": "KILLED",
            "reduced_G_identically_1": "KILLED",
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
    print("half_r", dump["half_r"])


if __name__ == "__main__":
    main()
