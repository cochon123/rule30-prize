#!/usr/bin/env python3
"""Cycle GX: at odd s, the j-th even column has Green G(n,j).

Cycle GU gives G=G(n, W/2-r/2) with n=UQ-t-1. Palindrome and
r=lo+2j send that to G(n,j), so Cycle GP's j-index holds at every
odd s, not only hits. Off-hit this is not mer_one(j). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gx.py --certify
Dump: research/cycle_gx.json
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
from cycle_gn import mer_one
from cycle_gu import odd_clock

OUT = Path(__file__).resolve().with_suffix(".json")
GW_JSON = Path(__file__).resolve().parent / "cycle_gw.json"
GU_JSON = Path(__file__).resolve().parent / "cycle_gu.json"
GP_JSON = Path(__file__).resolve().parent / "cycle_gp.json"


def odd_s_j() -> dict:
    """G(m, W-r)=G(n,j) on even r=lo+2j at every odd s. k<=6."""
    n_ok = 0
    n_s = 0
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
                n = odd_clock(t, U, Q)
                m = T - s - 1
                lo = 2 * (delta + 1)
                hi = min(2 * s - T, W)
                if hi < lo:
                    continue
                n_s += 1
                for r in range(lo, hi + 1, 2):
                    j = (r - lo) // 2
                    g = G(m, W - r)
                    if g != G(n, j):
                        return {
                            "ok": False,
                            "k": k,
                            "s": s,
                            "r": r,
                            "j": j,
                            "g": g,
                            "Gj": G(n, j),
                        }
                    n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_s": n_s}


def killed_mer_one_offhit() -> dict:
    """Off-hit G(n,j) is not mer_one(j): k=2, W=8U, delta=3, j=1."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = W // (4 * U)
    t = 1
    n = odd_clock(t, U, Q)
    j = 1
    g = G(n, j)
    mer = mer_one(j)
    ok = n == 6 and g == 0 and mer == 1
    return {"ok": ok, "k": k, "delta": 3, "j": j, "n": n, "G": g, "mer_one": mer}


def killed_reversed() -> dict:
    """Not G(n, U-1-j): k=2, W=8U, delta=3, j=0."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = W // (4 * U)
    n = odd_clock(1, U, Q)
    j = 0
    g = G(n, j)
    rev = G(n, U - 1 - j)
    ok = g == 1 and rev == 0
    return {"ok": ok, "k": k, "j": j, "G": g, "reversed": rev, "U": U}


def killed_ident_1() -> dict:
    """G(n,j) is not identically 1: same off-hit j=1."""
    k = 2
    U = 1 << k
    W = 8 * U
    n = odd_clock(1, U, W // (4 * U))
    g = G(n, 1)
    ok = g == 0
    return {"ok": ok, "k": k, "j": 1, "n": n, "G": g}


def prefixes() -> dict:
    gw = json.loads(GW_JSON.read_text())
    gu = json.loads(GU_JSON.read_text())
    gp = json.loads(GP_JSON.read_text())
    ok = (
        gw["checks"]["all_ok"]
        and gu["checks"]["all_ok"]
        and gp["checks"]["all_ok"]
        and gw["verdict"]["even_s_odd_r_G_eq_next_odd_s_r_plus_1"] == "LEMMA"
        and gu["verdict"]["odd_s_even_r_G_eq_G_odd_clock"] == "LEMMA"
        and gp["verdict"]["jth_even_r_has_palindrome_index_j"] == "LEMMA"
        and gw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, js: dict, km: dict, kr: dict, k1: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert js["ok"] and km["ok"] and kr["ok"] and k1["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    js = odd_s_j()
    km = killed_mer_one_offhit()
    kr = killed_reversed()
    k1 = killed_ident_1()
    pref = prefixes()
    checks = self_checks(c20, js, km, kr, k1, pref)
    dump = {
        "cycle": "GX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "odd_s_j": {k: js[k] for k in js if k != "ok"},
        "killed_mer_one_offhit": {k: km[k] for k in km if k != "ok"},
        "killed_reversed": {k: kr[k] for k in kr if k != "ok"},
        "killed_ident_1": {k: k1[k] for k in k1 if k != "ok"},
        "lemmas": {
            "odd_s_jth_even_r_G_eq_G_n_j": True,
            "offhit_G_eq_mer_one_j": False,
            "odd_s_G_eq_G_n_U_minus_1_minus_j": False,
            "odd_s_G_n_j_identically_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_s_jth_even_r_G_eq_G_n_j": "LEMMA",
            "offhit_G_eq_mer_one_j": "KILLED",
            "odd_s_G_eq_G_n_U_minus_1_minus_j": "KILLED",
            "odd_s_G_n_j_identically_1": "KILLED",
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
    print("odd_s_j", dump["odd_s_j"])
    print("killed_mer_one_offhit", dump["killed_mer_one_offhit"])
    print("killed_reversed", dump["killed_reversed"])
    print("killed_ident_1", dump["killed_ident_1"])


if __name__ == "__main__":
    main()
