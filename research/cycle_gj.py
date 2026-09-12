#!/usr/bin/env python3
"""Cycle GJ: at cone-hi hit q, Green clock m=2U(Q-q)-2.

Cycle GG's hits s=t0+1+q*2U have m=T-s-1=2U(Q-q)-2, which is also
2U-2+gap/2 for Cycle GI's gap r*-chi. Residue m ≡ 2U-2 (mod 2U), so
G(m,2U-2)=G(2U-2,2U-2)=1. The clock is not 2U-2 on pre-cone hits and
is not independent of q. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_gj.py --certify
Dump: research/cycle_gj.json
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
GI_JSON = Path(__file__).resolve().parent / "cycle_gi.json"
GG_JSON = Path(__file__).resolve().parent / "cycle_gg.json"
FW_JSON = Path(__file__).resolve().parent / "cycle_fw.json"


def hit_m() -> dict:
    """m=2U(Q-q)-2 = 2U-2+gap/2; residue 2U-2; G=1."""
    n_ok = 0
    n_g = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            rstar = W - 2 * U + 2
            for q in range(Q):
                s = t0 + 1 + q * (2 * U)
                m = T - s - 1
                chi = 2 * s - T
                gap = rstar - chi
                if m != 2 * U * (Q - q) - 2:
                    return {"ok": False, "k": k, "q": q, "m": m}
                if gap % 2 or m != (2 * U - 2) + gap // 2:
                    return {"ok": False, "k": k, "q": q, "gap": gap}
                if m % (2 * U) != (2 * U - 2) % (2 * U):
                    return {"ok": False, "k": k, "q": q, "res": m % (2 * U)}
                d = 2 * U - 2 if U > 1 else 0
                if G(m, d) != 1:
                    return {"ok": False, "k": k, "q": q, "G": 0}
                n_ok += 1
                n_g += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_g": n_g}


def killed_m_eq_2U_minus_2_pre() -> dict:
    """m is not 2U-2 on a pre-cone hit: k=2, W=8U, q=0."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = 2
    m0 = 2 * U * (Q - 0) - 2
    ok = m0 == 4 * U - 2 and m0 != 2 * U - 2
    return {"ok": ok, "k": k, "m0": m0, "two_U_minus_2": 2 * U - 2}


def killed_m_indep_q() -> dict:
    """m depends on q: k=2, W=8U, q=0 vs q=1."""
    k = 2
    U = 1 << k
    m0 = 2 * U * (2 - 0) - 2
    m1 = 2 * U * (2 - 1) - 2
    ok = m0 != m1 and m1 == 2 * U - 2
    return {"ok": ok, "m0": m0, "m1": m1}


def killed_last_m_eq_half_W() -> dict:
    """Last-hit m is not W/2-2 when Q>1."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = 2
    m_last = 2 * U * (Q - (Q - 1)) - 2
    ok = m_last == 2 * U - 2 and m_last != W // 2 - 2
    return {"ok": ok, "m_last": m_last, "half_W_minus_2": W // 2 - 2}


def prefixes() -> dict:
    gi = json.loads(GI_JSON.read_text())
    gg = json.loads(GG_JSON.read_text())
    fw = json.loads(FW_JSON.read_text())
    ok = (
        gi["checks"]["all_ok"]
        and gg["checks"]["all_ok"]
        and fw["checks"]["all_ok"]
        and gi["verdict"]["rstar_minus_chi_eq_4U_Q_minus_1_minus_q"] == "LEMMA"
        and gg["verdict"]["unclipped_cone_hi_contrib_t0_plus_1_plus_q_2U"]
        == "LEMMA"
        and fw["verdict"]["G_m_2a_minus_2_eq_G_m_mod_2a"] == "LEMMA"
        and gi["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, clock: dict, k0: dict, ki: dict, kl: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert clock["ok"] and k0["ok"] and ki["ok"] and kl["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    clock = hit_m()
    k0 = killed_m_eq_2U_minus_2_pre()
    ki = killed_m_indep_q()
    kl = killed_last_m_eq_half_W()
    pref = prefixes()
    checks = self_checks(c20, clock, k0, ki, kl, pref)
    dump = {
        "cycle": "GJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "hit_m": {k: clock[k] for k in clock if k != "ok"},
        "killed_m_eq_2U_minus_2_pre": {k: k0[k] for k in k0 if k != "ok"},
        "killed_m_indep_q": {k: ki[k] for k in ki if k != "ok"},
        "killed_last_m_eq_half_W": {k: kl[k] for k in kl if k != "ok"},
        "lemmas": {
            "m_eq_2U_Q_minus_q_minus_2": True,
            "m_eq_2U_minus_2_plus_gap_over_2": True,
            "G_m_2U_minus_2_eq_1_at_hits": True,
            "m_eq_2U_minus_2_on_precone": False,
            "m_independent_of_q": False,
            "last_m_eq_W_over_2_minus_2": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "m_eq_2U_Q_minus_q_minus_2": "LEMMA",
            "m_eq_2U_minus_2_plus_gap_over_2": "LEMMA",
            "G_m_2U_minus_2_eq_1_at_hits": "LEMMA",
            "m_eq_2U_minus_2_on_precone": "KILLED",
            "m_independent_of_q": "KILLED",
            "last_m_eq_W_over_2_minus_2": "KILLED",
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
    print("hit_m", dump["hit_m"])


if __name__ == "__main__":
    main()
