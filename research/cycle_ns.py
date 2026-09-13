#!/usr/bin/env python3
"""Cycle NS: on q=10 through k<=10, MV inner even-d G(j+1) vanishes.

On covering J10 through k<=10, XOR of G(n,j+1) over covering G=1
cells with n<j<=n+n//2 and (j-n) even (p=T-2j>=0; no packed row)
is 0. Prefix Cycle MV j10 for k<=8; walk k=9 and k=10. Not a
death at k=9 (xor=0); not a death at k=10 (xor=0); not rest (k=2:
0 vs 1); not NR outer identically 1 (k=9: 0 vs 1); not MU even-d
(k=3 q=6: 0 vs 1, already MV); not MK inner G(j-1); not empty
(k=9 n_ine=47906); not pointwise 0 (k=9 n_gjp1=14872); not the
form for all k. Do not claim T is 1 iff k=2; do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ns.py --certify
Dump: research/cycle_ns.json
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
from cycle_mw import want_outer_jp1
from cycle_mv import _walk_inner_even_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
MV_JSON = Path(__file__).resolve().parent / "cycle_mv.json"
NR_JSON = Path(__file__).resolve().parent / "cycle_nr.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_ine": 47906,
        "n_gjp1": 14872,
        "n_in": 78271,
        "xor_ine": 0,
        "xor_in_jm1": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_ine": 156201,
        "n_gjp1": 48418,
        "n_in": 254236,
        "xor_ine": 0,
        "xor_in_jm1": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_ine"] == want["n_ine"]
        and w["n_gjp1"] == want["n_gjp1"]
        and w["n_in"] == want["n_in"]
        and w["xor_ine"] == want["xor_ine"] == 0
        and w["xor_in_jm1"] == want["xor_in_jm1"] == 0
    )


def q10_inner_even_10() -> dict:
    """q=10 k<=10: prefix MV j10 k<=8; walk k=9,10; xor_ine vanishes."""
    mv = json.loads(MV_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_ine = n_gjp1 = 0
    for k in range(0, 9):
        r = mv["bothq_inner_even"]["rows"][str(k)]["j10"]
        if r["xor_ine"] != 0:
            return {"ok": False, "k": k, "q": 10, "xor_ine": r["xor_ine"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_ine += r["n_ine"]
        n_gjp1 += r["n_gjp1"]
        rows[str(k)] = {
            "xor_ine": r["xor_ine"],
            "xor_in_jm1": r["xor_in_jm1"],
            "rest": want_rest10(k, 10),
            "n_ine": r["n_ine"],
            "n_gjp1": r["n_gjp1"],
            "n_in": r["n_in"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "MV",
        }
    for k in (9, 10):
        w = _walk_inner_even_jp1(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_ine": w.get("xor_ine"),
                "n_ok": w.get("n_ok"),
                "n_ine": w.get("n_ine"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_ine += w["n_ine"]
        n_gjp1 += w["n_gjp1"]
        rows[str(k)] = {
            "xor_ine": w["xor_ine"],
            "xor_in_jm1": w["xor_in_jm1"],
            "rest": want_rest10(k, 10),
            "n_ine": w["n_ine"],
            "n_gjp1": w["n_gjp1"],
            "n_in": w["n_in"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_ine"] == 0 for k in range(0, 11))
        and rows["2"]["n_ine"] == 5
        and rows["2"]["n_gjp1"] == 2
        and rows["8"]["n_ine"] == 14617
        and rows["9"]["xor_ine"] == 0
        and rows["9"]["n_ine"] == 47906
        and rows["9"]["n_gjp1"] == 14872
        and rows["10"]["xor_ine"] == 0
        and rows["10"]["n_ine"] == 156201
        and rows["10"]["n_gjp1"] == 48418
        and rows["9"]["xor_in_jm1"] == 0
        and rows["10"]["xor_in_jm1"] == 0
        and want_outer_jp1(9) == 1
        and mv["checks"]["all_ok"]
        and mv["verdict"]["inner_even_jp1"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_ine": n_ine,
        "n_gjp1": n_gjp1,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_ine"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_ine": r["xor_ine"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_ine"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_ine": r["xor_ine"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["2"]
    ok = r["xor_ine"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_ine": r["xor_ine"], "rest": r["rest"]}


def killed_eq_nr(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_ine"] == 0 and want_outer_jp1(9) == 1
    return {"ok": ok, "k": 9, "q": 10, "xor_ine": r["xor_ine"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_ine"] == 47906
    return {"ok": ok, "k": 9, "q": 10, "n_ine": r["n_ine"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_gjp1"] == 14872 and r["n_ine"] == 47906
    return {"ok": ok, "k": 9, "q": 10, "n_gjp1": r["n_gjp1"], "n_ine": r["n_ine"]}


def prefixes() -> dict:
    mv = json.loads(MV_JSON.read_text())
    nr = json.loads(NR_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mv["checks"]["all_ok"]
        and nr["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mv["verdict"]["inner_even_jp1"] == "LEMMA"
        and nr["verdict"]["outer_jp1_10"] == "LEMMA"
        and mv["verdict"]["prize"] == "unsolved"
        and want_outer_jp1(10) == 1
        and want_rest10(2, 10) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    knr: dict,
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
        and knr["ok"]
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
    q10 = q10_inner_even_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    knr = killed_eq_nr(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kd9, kd10, kr, knr, kemp, kpw, sc, pref)
    dump = {
        "cycle": "NS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_inner_even_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_nr": {k: knr[k] for k in knr if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "lemmas": {
            "inner_even_jp1_10": True,
            "inner_even_jp1": True,
            "outer_jp1_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_nr": False,
            "ine_empty": False,
            "ine_pointwise": False,
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
            "inner_even_jp1_10": "LEMMA",
            "inner_even_jp1": "LEMMA",
            "outer_jp1_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_nr": "KILLED",
            "ine_empty": "KILLED",
            "ine_pointwise": "KILLED",
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
        "q10_inner_even_10 n_ok",
        dump["q10_inner_even_10"]["n_ok"],
        "n_g1",
        dump["q10_inner_even_10"]["n_g1"],
        "n_ine",
        dump["q10_inner_even_10"]["n_ine"],
        "n_gjp1",
        dump["q10_inner_even_10"]["n_gjp1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_nr", dump["killed_eq_nr"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])


if __name__ == "__main__":
    main()
