#!/usr/bin/env python3
"""Cycle GY: at even s, j-th even column is G(n,j) XOR G(n,j-1).

Same n=UQ-t-1 as Cycles GU/GX. j=0 is the lo corner G=1. Odd-r
Green is G(n,j) with j=(r-lo-1)/2. Even-r Green is not the odd-s
single term G(n,j). Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_gy.py --certify
Dump: research/cycle_gy.json
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
GX_JSON = Path(__file__).resolve().parent / "cycle_gx.json"
GV_JSON = Path(__file__).resolve().parent / "cycle_gv.json"
GW_JSON = Path(__file__).resolve().parent / "cycle_gw.json"


def even_s_j() -> dict:
    """Even-r: G(n,j) XOR G(n,j-1); odd-r: G(n,j); j=0 even-r is 1. k<=6."""
    n_even = 0
    n_odd = 0
    n_j0 = 0
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
                n = odd_clock(t, U, Q)
                m = T - s - 1
                lo = 2 * (delta + 1)
                hi = min(2 * s - T, W)
                if hi < lo:
                    continue
                for r in range(lo, hi + 1):
                    g = G(m, W - r)
                    if r % 2 == 0:
                        j = (r - lo) // 2
                        want = G(n, j) ^ G(n, j - 1)
                        if g != want:
                            return {
                                "ok": False,
                                "k": k,
                                "s": s,
                                "r": r,
                                "j": j,
                                "g": g,
                                "want": want,
                            }
                        if j == 0:
                            if g != 1:
                                return {"ok": False, "j0": True, "k": k, "s": s}
                            n_j0 += 1
                        n_even += 1
                    else:
                        j = (r - lo - 1) // 2
                        want = G(n, j)
                        if g != want:
                            return {
                                "ok": False,
                                "odd": True,
                                "k": k,
                                "s": s,
                                "r": r,
                                "j": j,
                                "g": g,
                                "want": want,
                            }
                        n_odd += 1
    return {
        "ok": n_even > 0,
        "n_even": n_even,
        "n_odd": n_odd,
        "n_j0": n_j0,
    }


def killed_eq_odd_s_j() -> dict:
    """Even-r Green is not G(n,j): k=1, W=4U, s=8, j=1."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0
    j = 1
    n = odd_clock(0, U, W // (4 * U))
    lo = 2 * (0 + 1)
    r = lo + 2 * j
    g = G(T - s - 1, W - r)
    gj = G(n, j)
    cob = gj ^ G(n, j - 1)
    ok = g == 0 and gj == 1 and cob == 0
    return {"ok": ok, "k": k, "s": s, "j": j, "G": g, "G_n_j": gj}


def killed_mer_one() -> dict:
    """Even-s even-r Green is not mer_one(j): same witness j=1."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0
    j = 1
    lo = 2
    r = lo + 2 * j
    g = G(T - s - 1, W - r)
    mer = mer_one(j)
    ok = g == 0 and mer == 1
    return {"ok": ok, "k": k, "j": j, "G": g, "mer_one": mer}


def killed_ident_1() -> dict:
    """Even-s even-r Green is not identically 1: j=1 at k=1, W=4U."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    s = T - W // 2
    j = 1
    r = 2 + 2 * j
    g = G(T - s - 1, W - r)
    ok = g == 0
    return {"ok": ok, "k": k, "j": j, "G": g}


def prefixes() -> dict:
    gx = json.loads(GX_JSON.read_text())
    gv = json.loads(GV_JSON.read_text())
    gw = json.loads(GW_JSON.read_text())
    ok = (
        gx["checks"]["all_ok"]
        and gv["checks"]["all_ok"]
        and gw["checks"]["all_ok"]
        and gx["verdict"]["odd_s_jth_even_r_G_eq_G_n_j"] == "LEMMA"
        and gv["verdict"]["even_s_even_r_G_eq_two_term_XOR"] == "LEMMA"
        and gw["verdict"]["even_s_odd_r_G_eq_next_odd_s_r_plus_1"] == "LEMMA"
        and gx["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ev: dict, kj: dict, km: dict, k1: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ev["ok"] and kj["ok"] and km["ok"] and k1["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ev = even_s_j()
    kj = killed_eq_odd_s_j()
    km = killed_mer_one()
    k1 = killed_ident_1()
    pref = prefixes()
    checks = self_checks(c20, ev, kj, km, k1, pref)
    dump = {
        "cycle": "GY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_s_j": {k: ev[k] for k in ev if k != "ok"},
        "killed_eq_odd_s_j": {k: kj[k] for k in kj if k != "ok"},
        "killed_mer_one": {k: km[k] for k in km if k != "ok"},
        "killed_ident_1": {k: k1[k] for k in k1 if k != "ok"},
        "lemmas": {
            "even_s_jth_even_r_G_eq_G_n_j_xor_G_n_j_minus_1": True,
            "even_s_j0_G_eq_1": True,
            "even_s_odd_r_G_eq_G_n_j": True,
            "even_s_even_r_eq_odd_s_G_n_j": False,
            "even_s_even_r_eq_mer_one_j": False,
            "even_s_even_r_G_identically_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_s_jth_even_r_G_eq_G_n_j_xor_G_n_j_minus_1": "LEMMA",
            "even_s_j0_G_eq_1": "LEMMA",
            "even_s_odd_r_G_eq_G_n_j": "LEMMA",
            "even_s_even_r_eq_odd_s_G_n_j": "KILLED",
            "even_s_even_r_eq_mer_one_j": "KILLED",
            "even_s_even_r_G_identically_1": "KILLED",
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
    print("even_s_j", dump["even_s_j"])
    print("killed_eq_odd_s_j", dump["killed_eq_odd_s_j"])
    print("killed_mer_one", dump["killed_mer_one"])
    print("killed_ident_1", dump["killed_ident_1"])


if __name__ == "__main__":
    main()
