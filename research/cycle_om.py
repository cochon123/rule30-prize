#!/usr/bin/env python3
"""Cycle OM: pal-right S on n=8t+7 equals S(2t+1).

n=8t+7 is 4s+3 with s=2t+1 odd. Pal-right S(4s+3)=S(s) through
t<128 (n<=1023). Combined with Cycle OL, every odd n<1024 reduces
to even-parent residue xor or n=8u+3 off-residue 0. Not the
recurrence for all t. Not a closed S for n%8==7 without the fold.
Not E_k=0 for all k. Do not catalogue further S/T subregions
unless the experiment answers why E_k=0. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_om.py --certify
Dump: research/cycle_om.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_ok import pal_right_s

OUT = Path(__file__).resolve().with_suffix(".json")
OL_JSON = Path(__file__).resolve().parent / "cycle_ol.json"
OK_JSON = Path(__file__).resolve().parent / "cycle_ok.json"
OJ_JSON = Path(__file__).resolve().parent / "cycle_oj.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

T_HI = 128


def want_n7(t: int) -> int:
    """S(8t+7) equals S(2t+1), t<128."""
    return pal_right_s(2 * t + 1)[0]


def n7_fold() -> dict:
    """t<128: pal_right_s(8t+7) == pal_right_s(2t+1)."""
    n_ok = n_one = 0
    sample = {}
    for t in range(0, T_HI):
        n = 8 * t + 7
        xor_s, n_s, n_fire = pal_right_s(n)
        want = want_n7(t)
        if xor_s != want:
            return {"ok": False, "t": t, "n": n, "xor": xor_s, "want": want}
        n_ok += 1
        n_one += xor_s
        if t <= 8 or t == 127:
            sample[str(t)] = {
                "n": n,
                "xor": xor_s,
                "want": want,
                "s": 2 * t + 1,
                "n_s": n_s,
                "n_fire": n_fire,
            }
    ok = (
        n_ok == T_HI
        and sample["0"]["xor"] == 0
        and sample["0"]["s"] == 1
        and sample["1"]["xor"] == 0
        and sample["4"]["xor"] == 1
        and sample["4"]["s"] == 9
        and sample["127"]["xor"] == pal_right_s(255)[0]
        and n_one > 0
        and n_one < T_HI
        and want_n7(0) == 0
        and want_n7(4) == 1
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_one": n_one,
        "t_hi": T_HI,
        "sample": sample,
    }


def killed_n7_zero(fold: dict) -> dict:
    ok = fold["sample"]["4"]["xor"] == 1
    return {"ok": ok, "t": 4, "n": 39, "xor": 1}


def killed_eq_n3(fold: dict) -> dict:
    """S(23)=0 while S(19)=1: not equal to the n=8t+3 class."""
    s23 = pal_right_s(23)[0]
    s19 = pal_right_s(19)[0]
    ok = s23 == 0 and s19 == 1 and fold["sample"]["2"]["xor"] == 0
    return {"ok": ok, "n23": s23, "n19": s19}


def prefixes() -> dict:
    ol = json.loads(OL_JSON.read_text())
    okj = json.loads(OK_JSON.read_text())
    oj = json.loads(OJ_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        ol["checks"]["all_ok"]
        and okj["checks"]["all_ok"]
        and oj["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and ol["verdict"]["n3_off0"] == "LEMMA"
        and ol["verdict"]["even_m_s"] == "LEMMA"
        and oj["verdict"]["T_iff_k2_all_k"] == "LEMMA"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and ol["verdict"]["prize"] == "unsolved"
        and ol["verdict"]["odd_s_closed"] == "PREFIX"
    )
    return {"ok": ok}


def self_checks(c20, fold, kz, k3, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert fold["ok"] and kz["ok"] and k3["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    fold = n7_fold()
    kz = killed_n7_zero(fold)
    k3 = killed_eq_n3(fold)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, fold, kz, k3, sc, pref)
    dump = {
        "cycle": "OM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n7_fold": {k: fold[k] for k in fold if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_n7_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_eq_n3": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "n7_fold": True,
            "n3_off0": True,
            "even_m_s": True,
            "T_iff_k2_all_k": True,
            "E_q10_10": True,
            "n7_zero": False,
            "eq_n3": False,
            "n7_all_t": False,
            "odd_s_closed": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n7_fold": "CERTIFIED",
            "n3_off0": "LEMMA",
            "even_m_s": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "n7_zero": "KILLED",
            "eq_n3": "KILLED",
            "n7_all_t": "PREFIX",
            "odd_s_closed": "PREFIX",
            "E_all_k": "PREFIX",
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
    print("n7_fold n_ok", dump["n7_fold"]["n_ok"], "n_one", dump["n7_fold"]["n_one"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_n7_zero", dump["killed_n7_zero"])
    print("killed_eq_n3", dump["killed_eq_n3"])


if __name__ == "__main__":
    main()
