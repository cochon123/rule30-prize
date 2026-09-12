#!/usr/bin/env python3
"""Cycle GI: at cone-hi hit q, cone-hi sits 4U(Q-1-q) left of r*.

Cycle GG's hits s=t0+1+q*2U have cone-hi chi=2U+2+4U*q. The dual column
is r*=W-2U+2, so r*-chi=4U(Q-1-q). Gap 0 iff q=Q-1 (the in-cone
collapse at s=W+1). Gap is not 0 on pre-cone hits and is not independent
of q. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_gi.py --certify
Dump: research/cycle_gi.json
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
from cycle_ca import KNOWN20, packed_center_bits

OUT = Path(__file__).resolve().with_suffix(".json")
GH_JSON = Path(__file__).resolve().parent / "cycle_gh.json"
GG_JSON = Path(__file__).resolve().parent / "cycle_gg.json"
GB_JSON = Path(__file__).resolve().parent / "cycle_gb.json"


def chi_gap() -> dict:
    """chi=2U+2+4U*q; r*-chi=4U(Q-1-q); zero iff q=Q-1."""
    n_ok = 0
    n_zero = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            rstar = W - 2 * U + 2
            for q in range(Q):
                s = t0 + 1 + q * (2 * U)
                chi = 2 * s - T
                if chi != 2 * U + 2 + 4 * U * q:
                    return {"ok": False, "k": k, "q": q, "chi": chi}
                gap = rstar - chi
                if gap != 4 * U * (Q - 1 - q):
                    return {"ok": False, "k": k, "q": q, "gap": gap}
                if (gap == 0) != (q == Q - 1):
                    return {"ok": False, "k": k, "q": q}
                n_ok += 1
                n_zero += int(gap == 0)
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_zero": n_zero}


def killed_gap0_pre() -> dict:
    """Gap is not 0 on a pre-cone hit: k=2, W=8U, q=0."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = 2
    rstar = W - 2 * U + 2
    chi = 2 * U + 2
    gap = rstar - chi
    ok = gap == 4 * U and gap != 0
    return {"ok": ok, "k": k, "gap": gap, "rstar": rstar, "chi": chi}


def killed_gap_indep_q() -> dict:
    """Gap depends on q: k=2, W=8U, q=0 vs q=1."""
    k = 2
    U = 1 << k
    g0 = 4 * U * (2 - 1 - 0)
    g1 = 4 * U * (2 - 1 - 1)
    ok = g0 != g1 and g1 == 0
    return {"ok": ok, "g0": g0, "g1": g1}


def killed_chi_eq_rstar_at_t0() -> dict:
    """chi != r* at t0+1 for W=8U."""
    k = 2
    U = 1 << k
    W = 8 * U
    ok = (2 * U + 2) != (W - 2 * U + 2)
    return {"ok": ok, "chi": 2 * U + 2, "rstar": W - 2 * U + 2}


def prefixes() -> dict:
    gh = json.loads(GH_JSON.read_text())
    gg = json.loads(GG_JSON.read_text())
    gb = json.loads(GB_JSON.read_text())
    ok = (
        gh["checks"]["all_ok"]
        and gg["checks"]["all_ok"]
        and gb["checks"]["all_ok"]
        and gh["verdict"]["exactly_one_incone_cone_hi_hit"] == "LEMMA"
        and gg["verdict"]["unclipped_cone_hi_contrib_t0_plus_1_plus_q_2U"]
        == "LEMMA"
        and gb["verdict"]["cone_hi_dual_eq_stationary_W_minus_2U_plus_2"]
        == "LEMMA"
        and gh["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gap: dict, k0: dict, ki: dict, kc: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gap["ok"] and k0["ok"] and ki["ok"] and kc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gap = chi_gap()
    k0 = killed_gap0_pre()
    ki = killed_gap_indep_q()
    kc = killed_chi_eq_rstar_at_t0()
    pref = prefixes()
    checks = self_checks(c20, gap, k0, ki, kc, pref)
    dump = {
        "cycle": "GI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "chi_gap": {k: gap[k] for k in gap if k != "ok"},
        "killed_gap0_pre": {k: k0[k] for k in k0 if k != "ok"},
        "killed_gap_indep_q": {k: ki[k] for k in ki if k != "ok"},
        "killed_chi_eq_rstar_at_t0": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "chi_eq_2U_plus_2_plus_4U_q": True,
            "rstar_minus_chi_eq_4U_Q_minus_1_minus_q": True,
            "gap_zero_iff_q_eq_Q_minus_1": True,
            "gap_zero_on_precone": False,
            "gap_independent_of_q": False,
            "chi_eq_rstar_at_t0_plus_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "chi_eq_2U_plus_2_plus_4U_q": "LEMMA",
            "rstar_minus_chi_eq_4U_Q_minus_1_minus_q": "LEMMA",
            "gap_zero_iff_q_eq_Q_minus_1": "LEMMA",
            "gap_zero_on_precone": "KILLED",
            "gap_independent_of_q": "KILLED",
            "chi_eq_rstar_at_t0_plus_1": "KILLED",
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
    print("chi_gap", dump["chi_gap"])


if __name__ == "__main__":
    main()
