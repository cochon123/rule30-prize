#!/usr/bin/env python3
"""Cycle NR: on q=10 through k<=10, MW outer pal-right G(j+1) is identically 1.

On covering J10 through k<=10, XOR of G(n,j+1) over covering G=1
cells with j>n+n//2 (p=T-2j>=0; no packed row) is 1. Prefix Cycle
MW for k<=8; walk k=9 and k=10. Not a death at k=9 (xor=1=want);
not a death at k=10 (xor=1=want); not rest (k=0: 1 vs 0); not NN
T-cell jp1 (k=0: 1 vs 0); not NO outer T jp1 (k=0: 1 vs 0); not
MV inner even vanish (k=9: 1 vs 0); not 0; not empty (k=9
n_out=73657); not pointwise 0 (k=9 n_gjp1=28139); not identically
1 on q=6; not the form for all k. Do not claim T is 1 iff k=2;
do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_nr.py --certify
Dump: research/cycle_nr.json
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
from cycle_md import want_rest10
from cycle_nn import want_t_jp1
from cycle_no import want_t_jp1_out
from cycle_mw import _walk_outer_jp1, killed_q6_one, want_outer_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
MW_JSON = Path(__file__).resolve().parent / "cycle_mw.json"
MV_JSON = Path(__file__).resolve().parent / "cycle_mv.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_out": 73657,
        "n_gjp1": 28139,
        "n_in": 78271,
        "n_ine": 47906,
        "xor_out": 1,
        "xor_ine": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_out": 237830,
        "n_gjp1": 90857,
        "n_in": 254236,
        "n_ine": 156201,
        "xor_out": 1,
        "xor_ine": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_out"] == want["n_out"]
        and w["n_gjp1"] == want["n_gjp1"]
        and w["n_in"] == want["n_in"]
        and w["n_ine"] == want["n_ine"]
        and w["xor_out"] == want["xor_out"] == want_outer_jp1(k)
        and w["xor_ine"] == want["xor_ine"] == 0
    )


def q10_outer_jp1_10() -> dict:
    """q=10 k<=10: prefix MW k<=8; walk k=9,10; xor_out identically 1."""
    mw = json.loads(MW_JSON.read_text())
    rows = {}
    for k in range(0, 9):
        r = mw["q10_outer_jp1"]["rows"][str(k)]
        if r["xor_out"] != 1 or r["xor_ine"] != 0:
            return {"ok": False, "k": k, "q": 10, "xor_out": r["xor_out"]}
        rows[str(k)] = {
            "xor_out": r["xor_out"],
            "xor_ine": r["xor_ine"],
            "want": 1,
            "rest": want_rest10(k, 10),
            "n_out": r["n_out"],
            "n_gjp1": r["n_gjp1"],
            "n_ine": r["n_ine"],
            "n_in": r["n_in"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "MW",
        }
    n_ok = mw["q10_outer_jp1"]["n_ok"]
    n_g1 = mw["q10_outer_jp1"]["n_g1"]
    n_out = mw["q10_outer_jp1"]["n_out"]
    n_gjp1 = mw["q10_outer_jp1"]["n_gjp1"]
    for k in (9, 10):
        w = _walk_outer_jp1(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_out": w.get("xor_out"),
                "n_ok": w.get("n_ok"),
                "n_out": w.get("n_out"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_out += w["n_out"]
        n_gjp1 += w["n_gjp1"]
        rows[str(k)] = {
            "xor_out": w["xor_out"],
            "xor_ine": w["xor_ine"],
            "want": 1,
            "rest": want_rest10(k, 10),
            "n_out": w["n_out"],
            "n_gjp1": w["n_gjp1"],
            "n_ine": w["n_ine"],
            "n_in": w["n_in"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_out"] == 1 for k in range(0, 11))
        and all(rows[str(k)]["xor_ine"] == 0 for k in range(0, 11))
        and rows["0"]["n_out"] == 3
        and rows["0"]["n_gjp1"] == 1
        and rows["8"]["n_out"] == 22844
        and rows["9"]["xor_out"] == 1
        and rows["9"]["n_out"] == 73657
        and rows["9"]["n_gjp1"] == 28139
        and rows["10"]["xor_out"] == 1
        and rows["10"]["n_out"] == 237830
        and rows["10"]["n_gjp1"] == 90857
        and want_outer_jp1(10) == 1
        and want_t_jp1(0) == 0
        and want_t_jp1_out(0) == 0
        and mw["checks"]["all_ok"]
        and mw["verdict"]["outer_jp1"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_out": n_out,
        "n_gjp1": n_gjp1,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_out"] == 1 and r["want"] == 1 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_out": r["xor_out"], "want": r["want"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_out"] == 1 and r["want"] == 1 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_out": r["xor_out"], "want": r["want"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["0"]
    ok = r["xor_out"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_out": r["xor_out"], "rest": r["rest"]}


def killed_eq_jp1(q10: dict) -> dict:
    r = q10["rows"]["0"]
    ok = r["xor_out"] == 1 and want_t_jp1(0) == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_out": r["xor_out"]}


def killed_eq_out_t(q10: dict) -> dict:
    r = q10["rows"]["0"]
    ok = r["xor_out"] == 1 and want_t_jp1_out(0) == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_out": r["xor_out"]}


def killed_eq_mv(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_out"] == 1 and r["xor_ine"] == 0
    return {"ok": ok, "k": 9, "q": 10, "xor_out": r["xor_out"], "xor_ine": r["xor_ine"]}


def killed_zero(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_out"] == 1
    return {"ok": ok, "k": 9, "q": 10, "xor_out": r["xor_out"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_out"] == 73657
    return {"ok": ok, "k": 9, "q": 10, "n_out": r["n_out"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_gjp1"] == 28139 and r["n_out"] == 73657
    return {"ok": ok, "k": 9, "q": 10, "n_gjp1": r["n_gjp1"], "n_out": r["n_out"]}


def prefixes() -> dict:
    mw = json.loads(MW_JSON.read_text())
    mv = json.loads(MV_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mw["checks"]["all_ok"]
        and mv["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mw["verdict"]["outer_jp1"] == "LEMMA"
        and mv["verdict"]["inner_even_jp1"] == "LEMMA"
        and mw["verdict"]["prize"] == "unsolved"
        and want_outer_jp1(9) == 1
        and want_outer_jp1(10) == 1
        and want_t_jp1(10) == 1
        and want_t_jp1_out(0) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    kj: dict,
    kt: dict,
    kmv: dict,
    kz: dict,
    kemp: dict,
    kpw: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and kd9["ok"]
        and kd10["ok"]
        and kr["ok"]
        and kj["ok"]
        and kt["ok"]
        and kmv["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mw = json.loads(MW_JSON.read_text())
    assert q10["n_ok"] == mw["q10_outer_jp1"]["n_ok"] + WANT_WALK[9]["n_ok"] + WANT_WALK[10]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_outer_jp1_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    kj = killed_eq_jp1(q10)
    kt = killed_eq_out_t(q10)
    kmv = killed_eq_mv(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    kq6 = killed_q6_one()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kr, kj, kt, kmv, kz, kemp, kpw, kq6, sc, pref
    )
    dump = {
        "cycle": "NR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_outer_jp1_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_jp1": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_out_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_eq_mv": {k: kmv[k] for k in kmv if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_q6_one": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "outer_jp1_10": True,
            "outer_jp1": True,
            "inner_even_jp1": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_jp1": False,
            "eq_out_t": False,
            "eq_mv": False,
            "outer_jp1_zero": False,
            "outer_empty": False,
            "outer_pointwise": False,
            "q6_one": False,
            "all_k": False,
            "u_vs_j": False,
            "unique0": False,
            "left_eq": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "outer_jp1_10": "LEMMA",
            "outer_jp1": "LEMMA",
            "inner_even_jp1": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_jp1": "KILLED",
            "eq_out_t": "KILLED",
            "eq_mv": "KILLED",
            "outer_jp1_zero": "KILLED",
            "outer_empty": "KILLED",
            "outer_pointwise": "KILLED",
            "q6_one": "KILLED",
            "all_k": "KILLED",
            "u_vs_j": "KILLED",
            "unique0": "KILLED",
            "left_eq": "KILLED",
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
        "q10_outer_jp1_10 n_ok",
        dump["q10_outer_jp1_10"]["n_ok"],
        "n_g1",
        dump["q10_outer_jp1_10"]["n_g1"],
        "n_out",
        dump["q10_outer_jp1_10"]["n_out"],
        "n_gjp1",
        dump["q10_outer_jp1_10"]["n_gjp1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_jp1", dump["killed_eq_jp1"])
    print("killed_eq_out_t", dump["killed_eq_out_t"])
    print("killed_eq_mv", dump["killed_eq_mv"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_q6_one", dump["killed_q6_one"])


if __name__ == "__main__":
    main()
