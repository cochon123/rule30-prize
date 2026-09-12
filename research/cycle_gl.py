#!/usr/bin/env python3
"""Cycle GL: at a cone-hi hit, Green ones lie only on even r.

Cycle GJ's clock m=2U(Q-q)-2 is even, so freshman G(m, odd)=0. Then
G(m, W-r)=1 forces W-r even, hence r even (W is even). All even r in
the cone have G=1 iff k<=1 (then the Cycle GK count equals U). Odd r
in the cone are Green-silent; not every even r is a one for k>=2; AND
does not fire on every Green one. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_gl.py --certify
Dump: research/cycle_gl.json
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
from cycle_gk import want_ones
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GK_JSON = Path(__file__).resolve().parent / "cycle_gk.json"
GJ_JSON = Path(__file__).resolve().parent / "cycle_gj.json"
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"


def even_r() -> dict:
    """G=1 only on even r; all even r iff k<=1; odd r exist and are 0."""
    n_ok = 0
    n_all_even = 0
    n_even_gap = 0
    for k in range(0, 12):
        U = 1 << k
        want = want_ones(k)
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            for q in range(Q):
                s = t0 + 1 + q * (2 * U)
                m = T - s - 1
                if m != 2 * U * (Q - q) - 2 or m % 2:
                    return {"ok": False, "k": k, "m": m}
                chi = 2 * s - T
                lo = 2 * (s - t0 + 1)
                n_even = n_odd_g = n_even_zero = n_odd = 0
                for r in range(lo, chi + 1):
                    g = G(m, W - r)
                    if r & 1:
                        n_odd += 1
                        n_odd_g += g
                    elif g:
                        n_even += 1
                    else:
                        n_even_zero += 1
                if n_odd_g or n_even != want:
                    return {"ok": False, "k": k, "q": q, "odd_g": n_odd_g, "n_even": n_even}
                if n_odd == 0 and U > 1:
                    return {"ok": False, "k": k, "no_odd": True}
                all_even = n_even_zero == 0
                if all_even != (k <= 1):
                    return {"ok": False, "k": k, "all_even": all_even}
                n_ok += 1
                n_all_even += int(all_even)
                n_even_gap += int(n_even_zero > 0)
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_all_even": n_all_even,
        "n_even_gap": n_even_gap,
    }


def killed_odd_r_ones() -> dict:
    """Odd r in the cone is Green-silent: k=2, W=4U, r=5."""
    k = 2
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0 + 1
    m = T - s - 1
    g = G(m, W - 5)
    ok = (5 & 1) == 1 and g == 0
    return {"ok": ok, "k": k, "r": 5, "G": g}


def killed_all_even_r() -> dict:
    """Not all even r are ones: k=2, W=4U, r=8."""
    k = 2
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s = t0 + 1
    m = T - s - 1
    g = G(m, W - 8)
    ok = (8 & 1) == 0 and g == 0
    return {"ok": ok, "k": k, "r": 8, "G": g}


def killed_and_all_green() -> dict:
    """AND does not fire on every Green one: k=1, W=4U, lo has G=1 AND=0."""
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
    m = T - s - 1
    lo = 2 * (s - t0 + 1)
    chi = 2 * s - T
    g_lo = G(m, W - lo)
    on_lo = ((A >> (T + lo)) & 1) == 1
    g_hi = G(m, W - chi)
    on_hi = ((A >> (T + chi)) & 1) == 1
    ok = g_lo == 1 and not on_lo and g_hi == 1 and on_hi
    return {"ok": ok, "k": k, "lo": lo, "AND_lo": int(on_lo), "AND_hi": int(on_hi)}


def prefixes() -> dict:
    gk = json.loads(GK_JSON.read_text())
    gj = json.loads(GJ_JSON.read_text())
    fs = json.loads(FS_JSON.read_text())
    ok = (
        gk["checks"]["all_ok"]
        and gj["checks"]["all_ok"]
        and fs["checks"]["all_ok"]
        and gk["verdict"]["hit_cone_ones_eq_2U_plus_1_plus_k_mod_2_over_3"]
        == "LEMMA"
        and gj["verdict"]["m_eq_2U_Q_minus_q_minus_2"] == "LEMMA"
        and fs["verdict"]["unclipped_cone_hi_eq_G_m_2U_minus_2"] == "LEMMA"
        and gk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ev: dict, ko: dict, ka: dict, kn: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ev["ok"] and ko["ok"] and ka["ok"] and kn["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ev = even_r()
    ko = killed_odd_r_ones()
    ka = killed_all_even_r()
    kn = killed_and_all_green()
    pref = prefixes()
    checks = self_checks(c20, ev, ko, ka, kn, pref)
    dump = {
        "cycle": "GL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_r": {k: ev[k] for k in ev if k != "ok"},
        "killed_odd_r_ones": {k: ko[k] for k in ko if k != "ok"},
        "killed_all_even_r": {k: ka[k] for k in ka if k != "ok"},
        "killed_and_all_green": {k: kn[k] for k in kn if k != "ok"},
        "lemmas": {
            "hit_green_ones_only_even_r": True,
            "all_even_r_are_ones_iff_k_le_1": True,
            "odd_r_green_ones": False,
            "all_even_r_are_ones": False,
            "AND_on_all_green_ones": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "hit_green_ones_only_even_r": "LEMMA",
            "all_even_r_are_ones_iff_k_le_1": "LEMMA",
            "odd_r_green_ones": "KILLED",
            "all_even_r_are_ones": "KILLED",
            "AND_on_all_green_ones": "KILLED",
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
    print("even_r", dump["even_r"])


if __name__ == "__main__":
    main()
