#!/usr/bin/env python3
"""Cycle HB: W=16U unified-band XOR is Delta16_R, not J_tail.

Cycles GZ/HA put that band in the j-index. Remainder Green to 18U
vanishes on p>18U, so J_tail is in-support; the right strip is the
16U-shift Delta toward 34U (dual of FL/FN). Delta16_R is not J_tail
(k=2: 0 vs 1) and is not Delta_R (k=2: 0 vs 1). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_hb.py --certify
Dump: research/cycle_hb.json
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
HA_JSON = Path(__file__).resolve().parent / "cycle_ha.json"
FO_JSON = Path(__file__).resolve().parent / "cycle_fo.json"
FL_JSON = Path(__file__).resolve().parent / "cycle_fl.json"
FR_JSON = Path(__file__).resolve().parent / "cycle_fr.json"


def _walk16(k: int) -> dict:
    """Delta16_R, unified-band XOR, and J_tail on [10U,18U)."""
    U = 1 << k
    W = 16 * U
    T = 2 * U + W
    t0 = T - W // 2
    T18, T34 = 18 * U, 34 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    dR = d_band = tot = Jtail = 0
    n_out = g18_right = 0
    s = t0
    while s < T:
        A = (row << 1) & row
        lo = 2 * (s - t0 + 1)
        hi = min(2 * s - T, W)
        m = T - s - 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1:
                g18 = G(T18 - s - 1, T18 - p)
                Jtail ^= g18
                if p > T18:
                    g34 = G(T34 - s - 1, T34 - p)
                    if g18:
                        g18_right += 1
                    dR ^= g34
                    r = p - T18
                    if lo <= r <= hi:
                        d_band ^= g34
                        tot ^= G(m, W - r)
                    elif g34:
                        n_out += 1
            tmp >>= 1
            p += 1
        row = rule30_step(row)
        s += 1
    return {
        "dR16": dR,
        "d_band": d_band,
        "tot": tot,
        "Jtail": Jtail,
        "n_out": n_out,
        "g18_right": g18_right,
    }


def delta16_band() -> dict:
    """Delta16_R = W=16U band XOR = unified G(m,W-r) XOR. k<=6."""
    n_ok = 0
    rows = {}
    for k in range(0, 7):
        w = _walk16(k)
        if (
            w["dR16"] != w["d_band"]
            or w["d_band"] != w["tot"]
            or w["n_out"]
            or w["g18_right"]
        ):
            return {"ok": False, "k": k, **w}
        n_ok += 1
        rows[str(k)] = {
            "dR16": w["dR16"],
            "tot": w["tot"],
            "Jtail": w["Jtail"],
        }
    return {"ok": n_ok == 7, "n_ok": n_ok, "rows": rows}


def killed_eq_Jtail() -> dict:
    """Delta16_R is not J_tail: k=2, 0 vs 1."""
    w = _walk16(2)
    ok = w["dR16"] == 0 and w["Jtail"] == 1
    return {"ok": ok, "k": 2, "dR16": w["dR16"], "Jtail": w["Jtail"]}


def killed_eq_0() -> dict:
    """Delta16_R is not identically 0: k=3."""
    w = _walk16(3)
    ok = w["dR16"] == 1
    return {"ok": ok, "k": 3, "dR16": w["dR16"]}


def killed_eq_dR8() -> dict:
    """Delta16_R is not Delta_R (W=8U): k=2, 0 vs 1."""
    w = _walk16(2)
    fr = json.loads(FR_JSON.read_text())
    dR8 = fr["split"]["rows"]["2"]["dR"]
    ok = w["dR16"] == 0 and dR8 == 1
    return {"ok": ok, "k": 2, "dR16": w["dR16"], "dR8": dR8}


def prefixes() -> dict:
    ha = json.loads(HA_JSON.read_text())
    fo = json.loads(FO_JSON.read_text())
    fl = json.loads(FL_JSON.read_text())
    fr = json.loads(FR_JSON.read_text())
    ok = (
        ha["checks"]["all_ok"]
        and fo["checks"]["all_ok"]
        and fl["checks"]["all_ok"]
        and fr["checks"]["all_ok"]
        and ha["verdict"]["even_s_band_XOR_eq_cob1_even_AND_xor_G1_odd_AND"]
        == "LEMMA"
        and fo["verdict"]["Delta16_L_eq_0"] == "LEMMA"
        and fl["verdict"]["Delta_R_eq_band_xor"] == "LEMMA"
        and fr["verdict"]["Jpost_eq_Jmid10_xor_DeltaR_xor_Jtail"] == "LEMMA"
        and ha["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, d16: dict, kj: dict, k0: dict, k8: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert d16["ok"] and kj["ok"] and k0["ok"] and k8["ok"] and pref["ok"]
    fr = json.loads(FR_JSON.read_text())
    for k in ("2", "3", "4", "5"):
        assert d16["rows"][k]["Jtail"] == fr["split"]["rows"][k]["Jtail"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    d16 = delta16_band()
    kj = killed_eq_Jtail()
    k0 = killed_eq_0()
    k8 = killed_eq_dR8()
    pref = prefixes()
    checks = self_checks(c20, d16, kj, k0, k8, pref)
    dump = {
        "cycle": "HB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "delta16_band": {k: d16[k] for k in d16 if k != "ok"},
        "killed_eq_Jtail": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_eq_dR8": {k: k8[k] for k in k8 if k != "ok"},
        "lemmas": {
            "Delta16_R_eq_W16U_band_xor": True,
            "Delta16_R_eq_Jtail": False,
            "Delta16_R_eq_0": False,
            "Delta16_R_eq_Delta_R": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "Delta16_R_eq_W16U_band_xor": "LEMMA",
            "Delta16_R_eq_Jtail": "KILLED",
            "Delta16_R_eq_0": "KILLED",
            "Delta16_R_eq_Delta_R": "KILLED",
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
    print("delta16_band n_ok", dump["delta16_band"]["n_ok"])
    print("killed_eq_Jtail", dump["killed_eq_Jtail"])
    print("killed_eq_0", dump["killed_eq_0"])
    print("killed_eq_dR8", dump["killed_eq_dR8"])


if __name__ == "__main__":
    main()
