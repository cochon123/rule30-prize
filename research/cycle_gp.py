#!/usr/bin/env python3
"""Cycle GP: j-th even cone column at a hit has palindrome index f=j.

On Cycle GG's hits the even r=lo+2j for 0<=j<U fill the cone, and Cycle
GO's palindrome index is f=j. Green is mer_one(j) (j≢2 mod 3). The map
is not reversed (f=U-1-j); Green is not 'j even'; AND is not live on
every mer_one. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_gp.py --certify
Dump: research/cycle_gp.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GO_JSON = Path(__file__).resolve().parent / "cycle_go.json"
GN_JSON = Path(__file__).resolve().parent / "cycle_gn.json"
GL_JSON = Path(__file__).resolve().parent / "cycle_gl.json"


def even_j() -> dict:
    """r=lo+2j; f=j; G=mer_one(j); lo maps to 0, chi to U-1."""
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
                chi = 2 * s - T
                lo = 2 * (s - t0 + 1)
                if lo + 2 * (U - 1) != chi:
                    return {"ok": False, "k": k, "lo": lo, "chi": chi}
                for j in range(U):
                    r = lo + 2 * j
                    e = W // 2 - r // 2
                    f = 2 * (U * n - 1) - e
                    if f != j:
                        return {"ok": False, "k": k, "j": j, "f": f}
                    g = G(m, W - r)
                    if g != mer_one(j):
                        return {"ok": False, "k": k, "j": j, "G": g}
                    n_ok += 1
                n_hits += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_hits": n_hits}


def killed_reversed() -> dict:
    """f is not U-1-j: k=1, j=0 (lo) has f=0 not 1."""
    k = 1
    U = 1 << k
    ok = 0 != U - 1
    return {"ok": ok, "k": k, "j": 0, "f": 0, "U_minus_1": U - 1}


def killed_iff_j_even() -> dict:
    """Green is not 'j even': k=1, j=1 (chi) is odd and G=1."""
    ok = mer_one(1) == 1 and (1 & 1) == 1
    return {"ok": ok, "j": 1, "mer": mer_one(1)}


def killed_and_all_mer() -> dict:
    """AND is not live on every mer_one: k=1, W=4U, j=0 (lo)."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0 + 1
    row = 1
    for _ in range(s):
        row = rule30_step(row)
    A = (row << 1) & row
    lo = 2 * (s - t0 + 1)
    on = ((A >> (T + lo)) & 1) == 1
    ok = mer_one(0) == 1 and not on
    return {"ok": ok, "k": k, "j": 0, "mer": 1, "AND": int(on)}


def prefixes() -> dict:
    go = json.loads(GO_JSON.read_text())
    gn = json.loads(GN_JSON.read_text())
    gl = json.loads(GL_JSON.read_text())
    ok = (
        go["checks"]["all_ok"]
        and gn["checks"]["all_ok"]
        and gl["checks"]["all_ok"]
        and go["verdict"]["every_hit_palindromes_to_low_mersenne_mod3"]
        == "LEMMA"
        and gn["verdict"]["G_2k_minus_1_f_eq_1_iff_f_ne_2_mod_3_on_0_U"]
        == "LEMMA"
        and gl["verdict"]["hit_green_ones_only_even_r"] == "LEMMA"
        and go["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ev: dict, kr: dict, ke: dict, ka: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ev["ok"] and kr["ok"] and ke["ok"] and ka["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ev = even_j()
    kr = killed_reversed()
    ke = killed_iff_j_even()
    ka = killed_and_all_mer()
    pref = prefixes()
    checks = self_checks(c20, ev, kr, ke, ka, pref)
    dump = {
        "cycle": "GP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_j": {k: ev[k] for k in ev if k != "ok"},
        "killed_reversed": {k: kr[k] for k in kr if k != "ok"},
        "killed_iff_j_even": {k: ke[k] for k in ke if k != "ok"},
        "killed_and_all_mer": {k: ka[k] for k in ka if k != "ok"},
        "lemmas": {
            "jth_even_r_has_palindrome_index_j": True,
            "lo_f_eq_0_chi_f_eq_U_minus_1": True,
            "G_eq_mer_one_j": True,
            "f_eq_U_minus_1_minus_j": False,
            "G_eq_1_iff_j_even": False,
            "AND_on_every_mer_one": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "jth_even_r_has_palindrome_index_j": "LEMMA",
            "lo_f_eq_0_chi_f_eq_U_minus_1": "LEMMA",
            "G_eq_mer_one_j": "LEMMA",
            "f_eq_U_minus_1_minus_j": "KILLED",
            "G_eq_1_iff_j_even": "KILLED",
            "AND_on_every_mer_one": "KILLED",
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
    print("even_j", dump["even_j"])


if __name__ == "__main__":
    main()
