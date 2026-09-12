#!/usr/bin/env python3
"""Cycle FQ: G(n+2^a, d)=G(n,d) for d<2^a; unified T=2U+W right band.

Freshman (1+x+x^2)^{2^a}=1+x^{2^a}+x^{2^{a+1}} gives
G(n+2^a, d)=G(n,d) XOR G(n, d-2^a) XOR G(n, d-2^{a+1}). Both extras
vanish when 0<=d<2^a, with no bound on n. Dual of Cycle FF (which
shifts both arguments and needs n<2^{a-1}). On the left reduced
strip, d=2U-p with p>=1 so d<2U, hence Green weights repeat in every
2U-block. The right band for a W-shift comparing T vs T+W with
T=2U+W unifies Cycles FL and FN: width 2U-1 until s=U+W, then clips.
Kills: the identity for d=2^a; 2U==4U on width 2U (k>=4); period
from t=0; flat width on the whole window. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fq.py --certify
Dump: research/cycle_fq.json
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
FP_JSON = Path(__file__).resolve().parent / "cycle_fp.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
FL_JSON = Path(__file__).resolve().parent / "cycle_fl.json"
FN_JSON = Path(__file__).resolve().parent / "cycle_fn.json"


def n_shift(amax: int = 8, nmax: int = 40) -> dict:
    """G(n+2^a, d)=G(n,d) for 0<=d<2^a, all n in [0, nmax)."""
    n_ok = 0
    for a in range(0, amax + 1):
        pa = 1 << a
        for n in range(nmax):
            for d in range(pa):
                if G(n + pa, d) != G(n, d):
                    return {"ok": False, "a": a, "n": n, "d": d}
                n_ok += 1
    return {"ok": True, "n_ok": n_ok, "amax": amax, "nmax": nmax}


def left_strip_repeat() -> dict:
    """Left reduced Green G(m, 2U-p) is 2U-periodic in m for p>=1."""
    n_ok = 0
    for k in range(0, 9):
        U = 1 << k
        for m in range(0, 4 * U):
            for p in range(1, 2 * U + 1):
                d = 2 * U - p
                if G(m + 2 * U, d) != G(m, d):
                    return {"ok": False, "k": k, "m": m, "p": p}
                n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def r_band(s: int, U: int, W: int) -> tuple[int, int, int, int]:
    T = 2 * U + W
    t0 = T - W // 2
    lo = 2 * (s - t0 + 1)
    hi = min(2 * s - T, W)
    return lo, hi, T, t0


def unified_band() -> dict:
    """Width 2U-1 until s=U+W; then W-2(s-t0+1)+1, at least 1."""
    n_flat = 0
    n_clip = 0
    for k in range(0, 11):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in range(t0, T):
                lo, hi, _, _ = r_band(s, U, W)
                w = hi - lo + 1 if hi >= lo else 0
                if s <= clip:
                    if w != 2 * U - 1:
                        return {"ok": False, "k": k, "W": W, "s": s, "w": w}
                    n_flat += 1
                else:
                    want = W - 2 * (s - t0 + 1) + 1
                    if w != want or w < 1:
                        return {
                            "ok": False,
                            "clip": True,
                            "k": k,
                            "W": W,
                            "s": s,
                            "w": w,
                            "want": want,
                        }
                    n_clip += 1
    return {"ok": True, "n_flat": n_flat, "n_clip": n_clip}


def killed_d_eq_power() -> dict:
    """d=2^a is false: G(2^a, 2^a)=1 != G(0, 2^a)=0."""
    a = 3
    pa = 1 << a
    g0 = G(0, pa)
    g1 = G(pa, pa)
    ok = g0 == 0 and g1 == 1
    return {"ok": ok, "a": a, "d": pa, "G_0": g0, "G_pa": g1}


def killed_from_t0() -> dict:
    """Width-2U word at t=0 is not the frozen word at 4U; 2U!=4U for k>=4."""
    k = 4
    U = 1 << k
    W = 2 * U
    mask = (1 << (W + 1)) - 1
    row = 1
    snap = {}
    for t in range(0, 4 * U + 1):
        if t in (0, 2 * U, 3 * U, 4 * U):
            snap[t] = row & mask
        row = rule30_step(row)
    ok = (
        snap[0] != snap[4 * U]
        and snap[2 * U] != snap[4 * U]
        and snap[3 * U] == snap[4 * U]
    )
    return {
        "ok": ok,
        "k": k,
        "eq_0_4U": snap[0] == snap[4 * U],
        "eq_2U_4U": snap[2 * U] == snap[4 * U],
        "eq_3U_4U": snap[3 * U] == snap[4 * U],
    }


def killed_flat_band() -> dict:
    """Width is not 2U-1 on the whole window: s=clip+1."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    clip = U + W
    s = clip + 1
    lo, hi, _, t0 = r_band(s, U, W)
    w = hi - lo + 1
    want = W - 2 * (s - t0 + 1) + 1
    ok = t0 <= s < T and w != 2 * U - 1 and w == want
    return {"ok": ok, "k": k, "s": s, "w": w, "flat": 2 * U - 1, "want": want}


def prefixes() -> dict:
    fp = json.loads(FP_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    fl = json.loads(FL_JSON.read_text())
    fn = json.loads(FN_JSON.read_text())
    ok = (
        fp["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fl["checks"]["all_ok"]
        and fn["checks"]["all_ok"]
        and fp["verdict"]["Delta_L_eq_nblocks_mod_2"] == "LEMMA"
        and ff["verdict"]["G_shift_q_2a_n_lt_2a_minus_1"] == "LEMMA"
        and fl["verdict"]["width_2U_minus_1_on_6U_9U"] == "LEMMA"
        and fn["verdict"]["width_2U_minus_1_on_4U_5U"] == "LEMMA"
        and fp["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    green: dict,
    strip: dict,
    band: dict,
    kd: dict,
    kt: dict,
    kf: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert green["ok"] and strip["ok"] and band["ok"]
    assert kd["ok"] and kt["ok"] and kf["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    green = n_shift()
    strip = left_strip_repeat()
    band = unified_band()
    kd = killed_d_eq_power()
    kt = killed_from_t0()
    kf = killed_flat_band()
    pref = prefixes()
    checks = self_checks(c20, green, strip, band, kd, kt, kf, pref)
    dump = {
        "cycle": "FQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n_shift": {k: green[k] for k in green if k != "ok"},
        "left_strip": {k: strip[k] for k in strip if k != "ok"},
        "band": {k: band[k] for k in band if k != "ok"},
        "killed_d_eq_power": {k: kd[k] for k in kd if k != "ok"},
        "killed_from_t0": {k: kt[k] for k in kt if k != "ok"},
        "killed_flat_band": {k: kf[k] for k in kf if k != "ok"},
        "lemmas": {
            "G_n_plus_2a_d_eq_G_n_d_for_d_lt_2a": True,
            "left_strip_Green_2U_periodic_in_m": True,
            "unified_T_eq_2U_plus_W_band": True,
            "d_eq_2a": False,
            "period_from_t0": False,
            "width_2U_eq_4U": False,
            "flat_width_whole_window": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_n_plus_2a_d_eq_G_n_d_for_d_lt_2a": "LEMMA",
            "left_strip_Green_2U_periodic_in_m": "LEMMA",
            "unified_T_eq_2U_plus_W_band": "LEMMA",
            "d_eq_2a": "KILLED",
            "period_from_t0": "KILLED",
            "width_2U_eq_4U": "KILLED",
            "flat_width_whole_window": "KILLED",
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
    print("n_shift", dump["n_shift"])
    print("band", dump["band"])


if __name__ == "__main__":
    main()
