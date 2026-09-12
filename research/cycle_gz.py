#!/usr/bin/env python3
"""Cycle GZ: odd-s band XOR is AND on G(n,j)=1 even columns.

Cycle GX indexes those columns. AND can fire on G=0 even columns but
contributes 0. Odd-s XOR is not Delta_R (k=4, W=8U: 0 vs 1); even-s
XOR is not identically 0. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_gz.py --certify
Dump: research/cycle_gz.json
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
from cycle_gu import odd_clock
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GY_JSON = Path(__file__).resolve().parent / "cycle_gy.json"
GX_JSON = Path(__file__).resolve().parent / "cycle_gx.json"
FL_JSON = Path(__file__).resolve().parent / "cycle_fl.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"


def _walk(k: int, W: int) -> dict:
    U = 1 << k
    T = 2 * U + W
    t0 = T - W // 2
    Q = W // (4 * U)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    s = t0
    xor_direct = xor_j = xor_even = 0
    n_g0and = 0
    odd_r_contrib = False
    while s < T:
        A = (row << 1) & row
        delta = s - t0
        t = delta // 2
        n = odd_clock(t, U, Q)
        lo = 2 * (delta + 1)
        hi = min(2 * s - T, W)
        m = T - s - 1
        if hi >= lo:
            if s % 2:
                for r in range(lo, hi + 1):
                    on = (A >> (T + r)) & 1
                    g = G(m, W - r)
                    if r % 2:
                        if on and g:
                            odd_r_contrib = True
                        continue
                    j = (r - lo) // 2
                    gj = G(n, j)
                    if on and g:
                        xor_direct ^= 1
                    if on and gj:
                        xor_j ^= 1
                    if on and not gj:
                        n_g0and += 1
            else:
                for r in range(lo, hi + 1):
                    if ((A >> (T + r)) & 1) and G(m, W - r):
                        xor_even ^= 1
        row = rule30_step(row)
        s += 1
    return {
        "xor_odd": xor_direct,
        "xor_j": xor_j,
        "xor_even": xor_even,
        "n_g0and": n_g0and,
        "odd_r_contrib": odd_r_contrib,
    }


def odd_s_and() -> dict:
    """odd-s G*AND XOR = XOR of AND on G(n,j)=1 even columns. k<=6."""
    n_ok = 0
    n_g0 = 0
    rows = {}
    for k in range(0, 7):
        U = 1 << k
        krow = {}
        for W in (4 * U, 8 * U, 16 * U):
            w = _walk(k, W)
            if w["odd_r_contrib"] or w["xor_odd"] != w["xor_j"]:
                return {"ok": False, "k": k, "W": W, **w}
            n_ok += 1
            n_g0 += w["n_g0and"]
            krow[f"{W // U}U"] = {
                "xor_odd": w["xor_odd"],
                "xor_even": w["xor_even"],
                "n_g0and": w["n_g0and"],
            }
        rows[str(k)] = krow
    return {"ok": n_ok == 21, "n_ok": n_ok, "n_g0and": n_g0, "rows": rows}


def killed_and_only_g1() -> dict:
    """AND is not only on G=1 even columns: k=1, W=8U, 4 fires on G=0."""
    w = _walk(1, 8 * 2)
    ok = w["n_g0and"] > 0
    return {"ok": ok, "k": 1, "W": "8U", "n_g0and": w["n_g0and"]}


def killed_odd_s_eq_dR() -> dict:
    """Odd-s XOR is not Delta_R: k=4, W=8U, 0 vs 1."""
    w = _walk(4, 8 * 16)
    fr = json.loads(FR_JSON.read_text())
    dR = fr["split"]["rows"]["4"]["dR"]
    ok = w["xor_odd"] == 0 and dR == 1
    return {"ok": ok, "k": 4, "W": "8U", "xor_odd": w["xor_odd"], "dR": dR}


def killed_even_s_0() -> dict:
    """Even-s G*AND XOR is not identically 0: k=4, W=8U."""
    w = _walk(4, 8 * 16)
    ok = w["xor_even"] == 1
    return {"ok": ok, "k": 4, "W": "8U", "xor_even": w["xor_even"]}


def prefixes() -> dict:
    gy = json.loads(GY_JSON.read_text())
    gx = json.loads(GX_JSON.read_text())
    fl = json.loads(FL_JSON.read_text())
    ok = (
        gy["checks"]["all_ok"]
        and gx["checks"]["all_ok"]
        and fl["checks"]["all_ok"]
        and gy["verdict"]["even_s_jth_even_r_G_eq_G_n_j_xor_G_n_j_minus_1"]
        == "LEMMA"
        and gx["verdict"]["odd_s_jth_even_r_G_eq_G_n_j"] == "LEMMA"
        and fl["verdict"]["Delta_R_eq_band_xor"] == "LEMMA"
        and gy["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, od: dict, ka: dict, kd: dict, ke: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert od["ok"] and ka["ok"] and kd["ok"] and ke["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    od = odd_s_and()
    ka = killed_and_only_g1()
    kd = killed_odd_s_eq_dR()
    ke = killed_even_s_0()
    pref = prefixes()
    checks = self_checks(c20, od, ka, kd, ke, pref)
    dump = {
        "cycle": "GZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "odd_s_and": {k: od[k] for k in od if k != "ok"},
        "killed_and_only_g1": {k: ka[k] for k in ka if k != "ok"},
        "killed_odd_s_eq_dR": {k: kd[k] for k in kd if k != "ok"},
        "killed_even_s_0": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "odd_s_band_XOR_eq_AND_on_G_n_j_eq_1": True,
            "AND_only_on_G_eq_1": False,
            "odd_s_XOR_eq_Delta_R": False,
            "even_s_XOR_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_s_band_XOR_eq_AND_on_G_n_j_eq_1": "LEMMA",
            "AND_only_on_G_eq_1": "KILLED",
            "odd_s_XOR_eq_Delta_R": "KILLED",
            "even_s_XOR_eq_0": "KILLED",
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
    print("odd_s_and n_ok", dump["odd_s_and"]["n_ok"], "n_g0and", dump["odd_s_and"]["n_g0and"])
    print("killed_and_only_g1", dump["killed_and_only_g1"])
    print("killed_odd_s_eq_dR", dump["killed_odd_s_eq_dR"])
    print("killed_even_s_0", dump["killed_even_s_0"])


if __name__ == "__main__":
    main()
