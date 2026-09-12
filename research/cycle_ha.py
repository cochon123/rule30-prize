#!/usr/bin/env python3
"""Cycle HA: even-s band XOR is coboundary-1 even AND plus G=1 odd AND.

Cycle GY indexes those columns. AND can fire on coboundary-0 even
columns and on G=0 odd columns but those contribute 0. Even-s XOR
is not Delta_R (k=2, W=8U: 0 vs 1) and is not the even-r slice
alone (k=3, W=8U: odd-r XOR=1). Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ha.py --certify
Dump: research/cycle_ha.json
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
GZ_JSON = Path(__file__).resolve().parent / "cycle_gz.json"
GY_JSON = Path(__file__).resolve().parent / "cycle_gy.json"
FL_JSON = Path(__file__).resolve().parent / "cycle_fl.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"


def _walk_even(k: int, W: int) -> dict:
    U = 1 << k
    T = 2 * U + W
    t0 = T - W // 2
    Q = W // (4 * U)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    s = t0
    xor_direct = xor_j = xor_even_r = xor_odd_r = 0
    n_cob0and = n_odd_r_g1and = n_odd_r_g0and = n_lo_and = 0
    while s < T:
        A = (row << 1) & row
        if s % 2 == 0:
            delta = s - t0
            t = delta // 2
            n = odd_clock(t, U, Q)
            lo = 2 * (delta + 1)
            hi = min(2 * s - T, W)
            m = T - s - 1
            if hi >= lo:
                for r in range(lo, hi + 1):
                    on = (A >> (T + r)) & 1
                    g = G(m, W - r)
                    if on and g:
                        xor_direct ^= 1
                    if r % 2 == 0:
                        j = (r - lo) // 2
                        cob = G(n, j) ^ G(n, j - 1)
                        if on and cob:
                            xor_j ^= 1
                            xor_even_r ^= 1
                            if j == 0:
                                n_lo_and += 1
                        if on and not cob:
                            n_cob0and += 1
                    else:
                        j = (r - lo - 1) // 2
                        gj = G(n, j)
                        if on and gj:
                            xor_j ^= 1
                            xor_odd_r ^= 1
                            n_odd_r_g1and += 1
                        if on and not gj:
                            n_odd_r_g0and += 1
        row = rule30_step(row)
        s += 1
    return {
        "xor_even": xor_direct,
        "xor_j": xor_j,
        "xor_even_r": xor_even_r,
        "xor_odd_r": xor_odd_r,
        "n_cob0and": n_cob0and,
        "n_odd_r_g1and": n_odd_r_g1and,
        "n_odd_r_g0and": n_odd_r_g0and,
        "n_lo_and": n_lo_and,
    }


def even_s_and() -> dict:
    """even-s G*AND XOR = coboundary-1 even AND XOR G=1 odd AND. k<=6."""
    n_ok = 0
    n_cob0 = 0
    n_odd_g1 = 0
    rows = {}
    for k in range(0, 7):
        U = 1 << k
        krow = {}
        for W in (4 * U, 8 * U, 16 * U):
            w = _walk_even(k, W)
            if w["xor_even"] != w["xor_j"]:
                return {"ok": False, "k": k, "W": W, **w}
            n_ok += 1
            n_cob0 += w["n_cob0and"]
            n_odd_g1 += w["n_odd_r_g1and"]
            krow[f"{W // U}U"] = {
                "xor_even": w["xor_even"],
                "xor_even_r": w["xor_even_r"],
                "xor_odd_r": w["xor_odd_r"],
                "n_cob0and": w["n_cob0and"],
                "n_odd_r_g1and": w["n_odd_r_g1and"],
                "n_odd_r_g0and": w["n_odd_r_g0and"],
                "n_lo_and": w["n_lo_and"],
            }
        rows[str(k)] = krow
    return {
        "ok": n_ok == 21,
        "n_ok": n_ok,
        "n_cob0and": n_cob0,
        "n_odd_r_g1and": n_odd_g1,
        "rows": rows,
    }


def killed_and_only_cob1() -> dict:
    """AND is not only on coboundary-1 even columns: k=3, W=8U."""
    w = _walk_even(3, 8 * 8)
    ok = w["n_cob0and"] > 0
    return {"ok": ok, "k": 3, "W": "8U", "n_cob0and": w["n_cob0and"]}


def killed_even_r_only() -> dict:
    """Even-s XOR is not the even-r coboundary slice: k=3, W=8U."""
    w = _walk_even(3, 8 * 8)
    ok = w["xor_even_r"] != w["xor_even"] and w["xor_odd_r"] == 1
    return {
        "ok": ok,
        "k": 3,
        "W": "8U",
        "xor_even": w["xor_even"],
        "xor_even_r": w["xor_even_r"],
        "xor_odd_r": w["xor_odd_r"],
    }


def killed_even_s_eq_dR() -> dict:
    """Even-s XOR is not Delta_R: k=2, W=8U, 0 vs 1."""
    w = _walk_even(2, 8 * 4)
    fr = json.loads(FR_JSON.read_text())
    dR = fr["split"]["rows"]["2"]["dR"]
    ok = w["xor_even"] == 0 and dR == 1
    return {"ok": ok, "k": 2, "W": "8U", "xor_even": w["xor_even"], "dR": dR}


def prefixes() -> dict:
    gz = json.loads(GZ_JSON.read_text())
    gy = json.loads(GY_JSON.read_text())
    fl = json.loads(FL_JSON.read_text())
    ok = (
        gz["checks"]["all_ok"]
        and gy["checks"]["all_ok"]
        and fl["checks"]["all_ok"]
        and gz["verdict"]["odd_s_band_XOR_eq_AND_on_G_n_j_eq_1"] == "LEMMA"
        and gy["verdict"]["even_s_jth_even_r_G_eq_G_n_j_xor_G_n_j_minus_1"]
        == "LEMMA"
        and fl["verdict"]["Delta_R_eq_band_xor"] == "LEMMA"
        and gz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, ev: dict, ka: dict, ke: dict, kd: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ev["ok"] and ka["ok"] and ke["ok"] and kd["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    ev = even_s_and()
    ka = killed_and_only_cob1()
    ke = killed_even_r_only()
    kd = killed_even_s_eq_dR()
    pref = prefixes()
    checks = self_checks(c20, ev, ka, ke, kd, pref)
    dump = {
        "cycle": "HA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_s_and": {k: ev[k] for k in ev if k != "ok"},
        "killed_and_only_cob1": {k: ka[k] for k in ka if k != "ok"},
        "killed_even_r_only": {k: ke[k] for k in ke if k != "ok"},
        "killed_even_s_eq_dR": {k: kd[k] for k in kd if k != "ok"},
        "lemmas": {
            "even_s_band_XOR_eq_cob1_even_AND_xor_G1_odd_AND": True,
            "AND_only_on_coboundary_1": False,
            "even_s_XOR_eq_even_r_slice": False,
            "even_s_XOR_eq_Delta_R": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_s_band_XOR_eq_cob1_even_AND_xor_G1_odd_AND": "LEMMA",
            "AND_only_on_coboundary_1": "KILLED",
            "even_s_XOR_eq_even_r_slice": "KILLED",
            "even_s_XOR_eq_Delta_R": "KILLED",
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
    print(
        "even_s_and n_ok",
        dump["even_s_and"]["n_ok"],
        "n_cob0and",
        dump["even_s_and"]["n_cob0and"],
        "n_odd_r_g1and",
        dump["even_s_and"]["n_odd_r_g1and"],
    )
    print("killed_and_only_cob1", dump["killed_and_only_cob1"])
    print("killed_even_r_only", dump["killed_even_r_only"])
    print("killed_even_s_eq_dR", dump["killed_even_s_eq_dR"])


if __name__ == "__main__":
    main()
