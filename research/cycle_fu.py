#!/usr/bin/env python3
"""Cycle FU: palindrome center r=s-2U+1 has G(m,m)=1; in cone iff s>=W+1.

Cycle FT's involution r |-> 2mu-r has unique fixed point mu=s-2U+1.
The reduced degree there is W-mu=m, so G(m,m)=1 (Cycle FF diagonal).
Together with Cycle FR's endpoints G(m,2m)=1 at lo and G(m,0)=1 at r=W,
the three palindrome-special indices are the three Green corners.
The center lies in the cone-band iff s>=W+1. Live ANDs on [lo,W] are
not palindrome-symmetric; the center AND is not always live. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fu.py --certify
Dump: research/cycle_fu.json
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
FT_JSON = Path(__file__).resolve().parent / "cycle_ft.json"
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"


def center_degree() -> dict:
    """W-mu=m, G(m,m)=1; in cone iff s>=W+1."""
    n_ok = 0
    n_in = 0
    n_out = 0
    for k in range(0, 11):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            for s in (t0, W, W + 1, U + W, T - 1):
                if not (t0 <= s < T):
                    continue
                m = T - s - 1
                mu = s - 2 * U + 1
                lo = 2 * (s - t0 + 1)
                hi = min(2 * s - T, W)
                if W - mu != m or G(m, m) != 1:
                    return {"ok": False, "k": k, "W": W, "s": s, "m": m, "W_mu": W - mu}
                in_cone = lo <= mu <= hi
                if in_cone != (s >= W + 1):
                    return {
                        "ok": False,
                        "cone": True,
                        "k": k,
                        "s": s,
                        "in_cone": in_cone,
                    }
                n_ok += 1
                if in_cone:
                    n_in += 1
                else:
                    n_out += 1
    return {"ok": n_ok > 0 and n_out > 0 and n_in > 0, "n_ok": n_ok, "n_in": n_in, "n_out": n_out}


def killed_and_sym() -> dict:
    """Live ANDs on Green [lo,W] are not palindrome-symmetric."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    mismatches = 0
    for s in range(t0, T):
        A = (row << 1) & row
        mu = s - 2 * U + 1
        lo = 2 * (s - t0 + 1)
        for r in range(lo, W + 1):
            rp = 2 * mu - r
            if rp <= r:
                continue
            live = (A >> (T + r)) & 1
            livep = (A >> (T + rp)) & 1
            if live != livep:
                mismatches += 1
        row = rule30_step(row)
    return {"ok": mismatches > 0, "k": k, "mismatches": mismatches}


def killed_center_and() -> dict:
    """Center AND is not always live, even in the cone."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    live_in = dead_in = 0
    for s in range(t0, T):
        A = (row << 1) & row
        mu = s - 2 * U + 1
        lo = 2 * (s - t0 + 1)
        hi = min(2 * s - T, W)
        on = ((A >> (T + mu)) & 1) == 1
        if lo <= mu <= hi:
            if on:
                live_in += 1
            else:
                dead_in += 1
        row = rule30_step(row)
    ok = live_in > 0 and dead_in > 0
    return {"ok": ok, "k": k, "live_in": live_in, "dead_in": dead_in}


def prefixes() -> dict:
    ft = json.loads(FT_JSON.read_text())
    fs = json.loads(FS_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    ok = (
        ft["checks"]["all_ok"]
        and fs["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and ft["verdict"]["green_interval_palindrome_sym"] == "LEMMA"
        and fs["verdict"]["G_m_d_eq_G_m_2m_minus_d"] == "LEMMA"
        and ff["verdict"]["G_nn_eq_1"] == "LEMMA"
        and fr["verdict"]["band_lo_edge_eq_G_m_2m"] == "LEMMA"
        and ft["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, ctr: dict, ka: dict, kc: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ctr["ok"] and ka["ok"] and kc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ctr = center_degree()
    ka = killed_and_sym()
    kc = killed_center_and()
    pref = prefixes()
    checks = self_checks(c20, ctr, ka, kc, pref)
    dump = {
        "cycle": "FU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "center": {k: ctr[k] for k in ctr if k != "ok"},
        "killed_and_sym": {k: ka[k] for k in ka if k != "ok"},
        "killed_center_and": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "center_degree_eq_m_G_mm_eq_1": True,
            "center_in_cone_iff_s_ge_W_plus_1": True,
            "AND_palindrome_sym_on_lo_W": False,
            "center_AND_always_live": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "center_degree_eq_m_G_mm_eq_1": "LEMMA",
            "center_in_cone_iff_s_ge_W_plus_1": "LEMMA",
            "AND_palindrome_sym_on_lo_W": "KILLED",
            "center_AND_always_live": "KILLED",
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
    print("center", dump["center"])


if __name__ == "__main__":
    main()
