#!/usr/bin/env python3
"""Cycle GB: palindrome dual of cone-hi is the stationary column r=W-2U+2.

Cycle FT's involution r |-> 2*mu-r with mu=s-2U+1 sends the moving
cone-hi 2s-T to the fixed index r*=W-2U+2, whose degree is constantly
2U-2 (Cycle FS). That column lies in Green support [lo,W] iff s<=clip,
equals the lo-edge at clip, lies in the cone-band iff W+1<=s<=clip, and
equals the palindrome center at s=W+1. It is not in-support after clip,
not equal to lo except at clip, and not in-cone from t0. The AND there
does not fire whenever G=1. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_gb.py --certify
Dump: research/cycle_gb.json
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
GA_JSON = Path(__file__).resolve().parent / "cycle_ga.json"
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"
FT_JSON = Path(__file__).resolve().parent / "cycle_ft.json"
FU_JSON = Path(__file__).resolve().parent / "cycle_fu.json"


def dual_column() -> dict:
    """2*mu-(2s-T)=W-2U+2; in-support iff s<=clip; in-cone iff W+1<=s<=clip."""
    n_ok = 0
    n_meet = 0
    n_clip_lo = 0
    for k in range(0, 11):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            rstar = W - 2 * U + 2
            if W - rstar != 2 * U - 2:
                return {"ok": False, "k": k, "deg": W - rstar}
            for s in range(t0, T):
                lo = 2 * (s - t0 + 1)
                chi = 2 * s - T
                hi = min(chi, W)
                mu = s - 2 * U + 1
                if 2 * mu - chi != rstar:
                    return {"ok": False, "k": k, "s": s, "dual": 2 * mu - chi}
                in_green = lo <= rstar <= W
                if in_green != (s <= clip):
                    return {"ok": False, "k": k, "s": s, "lo": lo, "rstar": rstar}
                in_cone = lo <= rstar <= hi
                if in_cone != (s >= W + 1 and s <= clip):
                    return {"ok": False, "k": k, "s": s, "in_cone": in_cone}
                if s == clip:
                    if lo != rstar:
                        return {"ok": False, "k": k, "clip_lo": lo}
                    n_clip_lo += 1
                if s == W + 1:
                    if mu != rstar:
                        return {"ok": False, "k": k, "mu": mu}
                    n_meet += 1
                n_ok += 1
    return {
        "ok": n_ok > 0 and n_meet > 0 and n_clip_lo > 0,
        "n_ok": n_ok,
        "n_meet": n_meet,
        "n_clip_lo": n_clip_lo,
    }


def killed_after_clip() -> dict:
    """r* is out of Green support after clip: k=2, W=8U, s=clip+1."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    clip = U + W
    s = clip + 1
    lo = 2 * (s - t0 + 1)
    rstar = W - 2 * U + 2
    ok = lo > rstar and s > clip
    return {"ok": ok, "k": k, "s": s, "lo": lo, "rstar": rstar}


def killed_eq_lo() -> dict:
    """r* equals lo only at clip, not at t0."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    rstar = W - 2 * U + 2
    lo = 2 * (t0 - t0 + 1)
    ok = lo == 2 and rstar != lo
    return {"ok": ok, "k": k, "s": t0, "lo": lo, "rstar": rstar}


def killed_in_cone_from_t0() -> dict:
    """r* is not in-cone at t0: k=2, W=8U."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    rstar = W - 2 * U + 2
    lo = 2
    hi = min(2 * t0 - T, W)
    ok = t0 < W + 1 and not (lo <= rstar <= hi)
    return {"ok": ok, "k": k, "s": t0, "hi": hi, "rstar": rstar}


def killed_and_when_g1() -> dict:
    """AND at r* does not fire whenever G=1 (k=2, W=8U, unclipped)."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    clip = U + W
    rstar = W - 2 * U + 2
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    live1 = dead1 = 0
    for s in range(t0, clip + 1):
        A = (row << 1) & row
        g = G(T - s - 1, 2 * U - 2)
        on = ((A >> (T + rstar)) & 1) == 1
        if g:
            if on:
                live1 += 1
            else:
                dead1 += 1
        row = rule30_step(row)
    ok = live1 > 0 and dead1 > 0
    return {"ok": ok, "k": k, "live1": live1, "dead1": dead1, "rstar": rstar}


def prefixes() -> dict:
    ga = json.loads(GA_JSON.read_text())
    fs = json.loads(FS_JSON.read_text())
    ft = json.loads(FT_JSON.read_text())
    fu = json.loads(FU_JSON.read_text())
    ok = (
        ga["checks"]["all_ok"]
        and fs["checks"]["all_ok"]
        and ft["checks"]["all_ok"]
        and fu["checks"]["all_ok"]
        and ga["verdict"]["unclipped_hi_times_q_param"] == "LEMMA"
        and fs["verdict"]["unclipped_cone_hi_eq_G_m_2U_minus_2"] == "LEMMA"
        and ft["verdict"]["green_interval_palindrome_sym"] == "LEMMA"
        and fu["verdict"]["center_in_cone_iff_s_ge_W_plus_1"] == "LEMMA"
        and ga["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    dual: dict,
    ka: dict,
    kl: dict,
    kc: dict,
    kand: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert dual["ok"] and ka["ok"] and kl["ok"] and kc["ok"] and kand["ok"]
    assert pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    dual = dual_column()
    ka = killed_after_clip()
    kl = killed_eq_lo()
    kc = killed_in_cone_from_t0()
    kand = killed_and_when_g1()
    pref = prefixes()
    checks = self_checks(c20, dual, ka, kl, kc, kand, pref)
    dump = {
        "cycle": "GB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "dual_column": {k: dual[k] for k in dual if k != "ok"},
        "killed_after_clip": {k: ka[k] for k in ka if k != "ok"},
        "killed_eq_lo": {k: kl[k] for k in kl if k != "ok"},
        "killed_in_cone_from_t0": {k: kc[k] for k in kc if k != "ok"},
        "killed_and_when_g1": {k: kand[k] for k in kand if k != "ok"},
        "lemmas": {
            "cone_hi_dual_eq_stationary_W_minus_2U_plus_2": True,
            "rstar_in_support_iff_s_le_clip": True,
            "rstar_in_cone_iff_W_plus_1_to_clip": True,
            "rstar_in_support_after_clip": False,
            "rstar_eq_lo_always": False,
            "rstar_in_cone_from_t0": False,
            "rstar_AND_whenever_G_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cone_hi_dual_eq_stationary_W_minus_2U_plus_2": "LEMMA",
            "rstar_in_support_iff_s_le_clip": "LEMMA",
            "rstar_in_cone_iff_W_plus_1_to_clip": "LEMMA",
            "rstar_in_support_after_clip": "KILLED",
            "rstar_eq_lo_always": "KILLED",
            "rstar_in_cone_from_t0": "KILLED",
            "rstar_AND_whenever_G_eq_1": "KILLED",
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
    print("dual_column", dump["dual_column"])


if __name__ == "__main__":
    main()
