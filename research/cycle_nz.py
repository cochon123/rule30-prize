#!/usr/bin/env python3
"""Cycle NZ: on q=10 through k<=10, ND mid S vanishes.

On covering J10 through k<=10, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and U<=n<3U/2 (p=T-2j>=0; no packed
row) is 0. Prefix Cycle ND for k<=8; walk k=9 and k=10. Companion
NC n<U and NY high S still hold at those k. Not a death at k=9
(xor=0); not a death at k=10 (xor=0); not rest (k=2: 0 vs 1); not
NC n<U (k=4: 0 vs 1); not NA S (k=6: 0 vs 1); not NY high S (k=4:
0 vs 1); not empty (k=9 n_mid=4203); not pointwise 0 (k=9
n_midg=2032); not the form for all k. Do not claim T is 1 iff
k=2; do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_nz.py --certify
Dump: research/cycle_nz.json
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
from cycle_nc import want_s_nltu
from cycle_nd import _walk_s_mid
from cycle_ne import want_s_hi

OUT = Path(__file__).resolve().with_suffix(".json")
ND_JSON = Path(__file__).resolve().parent / "cycle_nd.json"
NY_JSON = Path(__file__).resolve().parent / "cycle_ny.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_mid": 4203,
        "n_midg": 2032,
        "xor_mid": 0,
        "xor_hi": 0,
        "xor_nltu": 0,
        "xor_sall": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_mid": 14359,
        "n_midg": 6062,
        "xor_mid": 0,
        "xor_hi": 0,
        "xor_nltu": 0,
        "xor_sall": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_mid"] == want["n_mid"]
        and w["n_midg"] == want["n_midg"]
        and w["xor_mid"] == want["xor_mid"] == 0
        and w["xor_hi"] == want["xor_hi"] == want_s_hi(k)
        and w["xor_nltu"] == want["xor_nltu"] == want_s_nltu(k)
        and w["xor_sall"] == want["xor_sall"] == w["xor_nltu"] ^ w["xor_hi"]
    )


def q10_s_mid_10() -> dict:
    """q=10 k<=10: prefix ND k<=8; walk k=9,10; xor_mid = 0."""
    nd = json.loads(ND_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_mid = n_midg = 0
    for k in range(0, 9):
        r = nd["bothq_s_mid"]["rows"][str(k)]["j10"]
        if r["xor_mid"] != 0:
            return {"ok": False, "k": k, "q": 10, "xor_mid": r["xor_mid"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_mid += r["n_mid"]
        n_midg += r["n_midg"]
        rows[str(k)] = {
            "xor_mid": r["xor_mid"],
            "xor_hi": r["xor_hi"],
            "xor_nltu": r["xor_nltu"],
            "xor_sall": r["xor_sall"],
            "want_hi": want_s_hi(k),
            "rest": want_rest10(k, 10),
            "n_mid": r["n_mid"],
            "n_midg": r["n_midg"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "ND",
        }
    for k in (9, 10):
        w = _walk_s_mid(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_mid": w.get("xor_mid"),
                "n_ok": w.get("n_ok"),
                "n_mid": w.get("n_mid"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_mid += w["n_mid"]
        n_midg += w["n_midg"]
        rows[str(k)] = {
            "xor_mid": w["xor_mid"],
            "xor_hi": w["xor_hi"],
            "xor_nltu": w["xor_nltu"],
            "xor_sall": w["xor_sall"],
            "want_hi": want_s_hi(k),
            "rest": want_rest10(k, 10),
            "n_mid": w["n_mid"],
            "n_midg": w["n_midg"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_mid"] == 0 for k in range(0, 11))
        and rows["2"]["n_mid"] == 1
        and rows["2"]["n_midg"] == 0
        and rows["2"]["rest"] == 1
        and rows["4"]["n_mid"] == 13
        and rows["4"]["n_midg"] == 4
        and rows["4"]["xor_hi"] == 1
        and rows["4"]["xor_nltu"] == 1
        and rows["6"]["xor_sall"] == 1
        and rows["8"]["n_mid"] == 1389
        and rows["8"]["xor_mid"] == 0
        and rows["9"]["xor_mid"] == 0
        and rows["9"]["n_mid"] == 4203
        and rows["9"]["n_midg"] == 2032
        and rows["10"]["xor_mid"] == 0
        and rows["10"]["n_mid"] == 14359
        and rows["10"]["n_midg"] == 6062
        and want_s_nltu(9) == 0
        and want_s_hi(4) == 1
        and nd["checks"]["all_ok"]
        and nd["verdict"]["s_mid"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_mid": n_mid,
        "n_midg": n_midg,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_mid"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_mid": r["xor_mid"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_mid"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_mid": r["xor_mid"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["2"]
    ok = r["xor_mid"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_mid": r["xor_mid"], "rest": r["rest"]}


def killed_eq_nltu(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor_mid"] == 0 and r["xor_nltu"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_mid": r["xor_mid"], "xor_nltu": r["xor_nltu"]}


def killed_eq_s(q10: dict) -> dict:
    r = q10["rows"]["6"]
    ok = r["xor_mid"] == 0 and r["xor_sall"] == 1
    return {"ok": ok, "k": 6, "q": 10, "xor_mid": r["xor_mid"], "xor_sall": r["xor_sall"]}


def killed_eq_hi(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor_mid"] == 0 and r["xor_hi"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_mid": r["xor_mid"], "xor_hi": r["xor_hi"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_mid"] == 4203
    return {"ok": ok, "k": 9, "q": 10, "n_mid": r["n_mid"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_midg"] == 2032 and r["xor_mid"] == 0
    return {"ok": ok, "k": 9, "q": 10, "n_midg": r["n_midg"]}


def prefixes() -> dict:
    nd = json.loads(ND_JSON.read_text())
    ny = json.loads(NY_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nd["checks"]["all_ok"]
        and ny["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nd["verdict"]["s_mid"] == "LEMMA"
        and ny["verdict"]["s_hi_10"] == "LEMMA"
        and nd["verdict"]["prize"] == "unsolved"
        and want_s_nltu(4) == 1
        and want_s_hi(4) == 1
        and want_rest10(2, 10) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    kn: dict,
    ks: dict,
    kh: dict,
    kemp: dict,
    kpw: dict,
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
        and kn["ok"]
        and ks["ok"]
        and kh["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    q10_8 = sum(mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    assert q10["n_ok"] == q10_8 + WANT_WALK[9]["n_ok"] + WANT_WALK[10]["n_ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_s_mid_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    kn = killed_eq_nltu(q10)
    ks = killed_eq_s(q10)
    kh = killed_eq_hi(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kr, kn, ks, kh, kemp, kpw, sc, pref
    )
    dump = {
        "cycle": "NZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_mid_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_nltu": {k: kn[k] for k in kn if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "lemmas": {
            "s_mid_10": True,
            "s_mid": True,
            "s_hi_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_nltu": False,
            "eq_s": False,
            "eq_hi": False,
            "nmid_empty": False,
            "nmid_pointwise": False,
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
            "s_mid_10": "LEMMA",
            "s_mid": "LEMMA",
            "s_hi_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_nltu": "KILLED",
            "eq_s": "KILLED",
            "eq_hi": "KILLED",
            "nmid_empty": "KILLED",
            "nmid_pointwise": "KILLED",
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
        "q10_s_mid_10 n_ok",
        dump["q10_s_mid_10"]["n_ok"],
        "n_g1",
        dump["q10_s_mid_10"]["n_g1"],
        "n_mid",
        dump["q10_s_mid_10"]["n_mid"],
        "n_midg",
        dump["q10_s_mid_10"]["n_midg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_nltu", dump["killed_eq_nltu"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])


if __name__ == "__main__":
    main()
