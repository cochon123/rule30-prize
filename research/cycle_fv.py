#!/usr/bin/env python3
"""Cycle FV: remainder palindrome p|->2s+2-p; center p=s+1 always in-support.

For a Green remainder to target T at time s<T, in-support is
p in [2s-T+2, T]. Palindrome G(m,d)=G(m,2m-d) acts by p |-> 2s+2-p
and swaps the endpoints (G(m,2m)=1 at p_lo, G(m,0)=1 at p=T). The
unique fixed point is p=s+1, with degree m, so G(m,m)=1. Unlike Cycle
FU's comparison-band center (in cone only for s>=W+1), the remainder
center is in-support for every s in the window. Kills: remainder AND
palindrome-symmetry; remainder-center AND always live. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fv.py --certify
Dump: research/cycle_fv.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FU_JSON = Path(__file__).resolve().parent / "cycle_fu.json"
FT_JSON = Path(__file__).resolve().parent / "cycle_ft.json"
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"


def remainder_pal() -> dict:
    """p|->2s+2-p swaps plo and T; center s+1 in-support with G(m,m)=1."""
    n_ok = 0
    for k in range(0, 11):
        U = 1 << k
        windows = (
            (6 * U, 2 * U, 6 * U),
            (10 * U, 6 * U, 10 * U),
            (18 * U, 10 * U, 18 * U),
        )
        for T, t0, t1 in windows:
            for s in (t0, (t0 + t1) // 2, t1 - 1):
                if not (t0 <= s < t1):
                    continue
                m = T - s - 1
                plo = 2 * s - T + 2
                ctr = s + 1
                if 2 * (s + 1) - plo != T or 2 * (s + 1) - T != plo:
                    return {"ok": False, "ends": True, "k": k, "s": s}
                if not (plo <= ctr <= T) or T - ctr != m or G(m, m) != 1:
                    return {"ok": False, "ctr": True, "k": k, "s": s}
                if T - plo != 2 * m or G(m, 2 * m) != 1 or G(m, 0) != 1:
                    return {"ok": False, "corners": True, "k": k, "s": s}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_and_sym() -> dict:
    """Remainder ANDs on [plo,T] are not palindrome-symmetric (J_tail, k=2)."""
    k = 2
    U = 1 << k
    t0, t1, T = 10 * U, 18 * U, 18 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    mm = 0
    for s in range(t0, t1):
        A = (row << 1) & row
        plo = 2 * s - T + 2
        for p in range(max(plo, 0), T + 1):
            pp = 2 * s + 2 - p
            if pp <= p:
                continue
            if ((A >> p) & 1) != ((A >> pp) & 1):
                mm += 1
        row = rule30_step(row)
    return {"ok": mm > 0, "k": k, "mismatches": mm}


def killed_center_and() -> dict:
    """Remainder-center AND p=s+1 is not always live (J_tail, k=2)."""
    k = 2
    U = 1 << k
    t0, t1, T = 10 * U, 18 * U, 18 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    live = dead = 0
    for s in range(t0, t1):
        A = (row << 1) & row
        if (A >> (s + 1)) & 1:
            live += 1
        else:
            dead += 1
        row = rule30_step(row)
    ok = live > 0 and dead > 0
    return {"ok": ok, "k": k, "live": live, "dead": dead}


def prefixes() -> dict:
    fu = json.loads(FU_JSON.read_text())
    ft = json.loads(FT_JSON.read_text())
    fs = json.loads(FS_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    ok = (
        fu["checks"]["all_ok"]
        and ft["checks"]["all_ok"]
        and fs["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fu["verdict"]["center_in_cone_iff_s_ge_W_plus_1"] == "LEMMA"
        and ft["verdict"]["green_interval_palindrome_sym"] == "LEMMA"
        and fs["verdict"]["G_m_d_eq_G_m_2m_minus_d"] == "LEMMA"
        and ff["verdict"]["G_nn_eq_1"] == "LEMMA"
        and fu["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal: dict, ka: dict, kc: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and ka["ok"] and kc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = remainder_pal()
    ka = killed_and_sym()
    kc = killed_center_and()
    pref = prefixes()
    checks = self_checks(c20, pal, ka, kc, pref)
    dump = {
        "cycle": "FV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "remainder_pal": {k: pal[k] for k in pal if k != "ok"},
        "killed_and_sym": {k: ka[k] for k in ka if k != "ok"},
        "killed_center_and": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "remainder_palindrome_p_to_2s_plus_2_minus_p": True,
            "remainder_center_s_plus_1_always_in_support": True,
            "remainder_AND_palindrome_sym": False,
            "remainder_center_AND_always_live": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "remainder_palindrome_p_to_2s_plus_2_minus_p": "LEMMA",
            "remainder_center_s_plus_1_always_in_support": "LEMMA",
            "remainder_AND_palindrome_sym": "KILLED",
            "remainder_center_AND_always_live": "KILLED",
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
    print("remainder_pal", dump["remainder_pal"])


if __name__ == "__main__":
    main()
