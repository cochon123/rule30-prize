#!/usr/bin/env python3
"""Cycle NW: on q=10 through k<=10, MR pal-right d%3==0 G(j-1) is 1 iff k%4 in (1, 2).

On covering J10 through k<=10, XOR of G(n,j-1) over covering G=1
cells with j>n and (j-n)%3==0 (p=T-2j>=0; no packed row) is 1 iff
k%4 in (1, 2). Prefix Cycle MR q=10 for k<=8; walk k=9 and k=10.
On q=10 this xor equals Cycle NU's d31 G(j+1) (same want; different
cells). Not a death at k=9 (xor=1=want); not a death at k=10
(xor=1=want); not rest (k=1: 1 vs 0); not NV Green d31 (k=9: 1 vs
0); not NT inner vanish (k=9: 1 vs 0); not NU as the same cells
(k=9 n_d30=52103 vs n_d31=50742); not MQ on q=6 (k=1 d30=1,
jp1=0); not 0; not empty (k=9 n_d30=52103); not the form for all
k. Do not claim T is 1 iff k=2; do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_nw.py --certify
Dump: research/cycle_nw.json
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
from cycle_mj import want_jgtn
from cycle_mm import want_d31
from cycle_mq import _walk_d31_jp1, want_d31_jp1
from cycle_mr import _walk_d30, want_d30

OUT = Path(__file__).resolve().with_suffix(".json")
MR_JSON = Path(__file__).resolve().parent / "cycle_mr.json"
NV_JSON = Path(__file__).resolve().parent / "cycle_nv.json"
NU_JSON = Path(__file__).resolve().parent / "cycle_nu.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_d30": 52103,
        "n_d31": 50742,
        "xor_d30": 1,
        "xor_d31": 0,
        "xor_jgtn": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_d30": 167835,
        "n_d31": 160761,
        "xor_d30": 1,
        "xor_d31": 0,
        "xor_jgtn": 1,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_d30"] == want["n_d30"]
        and w["n_d31"] == want["n_d31"]
        and w["xor_d30"] == want["xor_d30"] == want_d30(k) == want_d31_jp1(k)
        and w["xor_d31"] == want["xor_d31"] == want_d31(k)
        and w["xor_jgtn"] == want["xor_jgtn"] == want_jgtn(k)
    )


def q10_d30_10() -> dict:
    """q=10 k<=10: prefix MR j10 k<=8; walk k=9,10; xor_d30 = want_d30."""
    mr = json.loads(MR_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_d30 = 0
    for k in range(0, 9):
        r = mr["bothq_d30"]["rows"][str(k)]["j10"]
        wd = want_d30(k)
        if (
            r["xor_d30"] != wd
            or r["xor_d30"] != want_d31_jp1(k)
            or r["xor_d31"] != want_d31(k)
        ):
            return {"ok": False, "k": k, "q": 10, "xor_d30": r["xor_d30"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_d30 += r["n_d30"]
        rows[str(k)] = {
            "xor_d30": r["xor_d30"],
            "xor_d31": r["xor_d31"],
            "want": wd,
            "rest": want_rest10(k, 10),
            "n_d30": r["n_d30"],
            "n_d31": r["n_d31"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "MR",
        }
    for k in (9, 10):
        w = _walk_d30(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_d30": w.get("xor_d30"),
                "n_ok": w.get("n_ok"),
                "n_d30": w.get("n_d30"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_d30 += w["n_d30"]
        rows[str(k)] = {
            "xor_d30": w["xor_d30"],
            "xor_d31": w["xor_d31"],
            "want": want_d30(k),
            "rest": want_rest10(k, 10),
            "n_d30": w["n_d30"],
            "n_d31": w["n_d31"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_d30"] == want_d30(k) for k in range(0, 11))
        and all(rows[str(k)]["xor_d30"] == want_d31_jp1(k) for k in range(0, 11))
        and all(rows[str(k)]["xor_d31"] == want_d31(k) for k in range(0, 11))
        and rows["0"]["n_d30"] == 0
        and rows["1"]["n_d30"] == 3
        and rows["1"]["xor_d30"] == 1
        and rows["8"]["n_d30"] == 16173
        and rows["8"]["xor_d30"] == 0
        and rows["9"]["xor_d30"] == 1
        and rows["9"]["n_d30"] == 52103
        and rows["9"]["n_d31"] == 50742
        and rows["9"]["xor_d31"] == 0
        and rows["10"]["xor_d30"] == 1
        and rows["10"]["n_d30"] == 167835
        and rows["10"]["n_d31"] == 160761
        and want_d30(9) == 1
        and want_d30(10) == 1
        and want_d31(9) == 0
        and mr["checks"]["all_ok"]
        and mr["verdict"]["d30_both"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_d30": n_d30,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_d30"] == 1 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_d30": r["xor_d30"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_d30"] == 1 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_d30": r["xor_d30"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["1"]
    ok = r["xor_d30"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 1, "q": 10, "xor_d30": r["xor_d30"], "rest": r["rest"]}


def killed_eq_nv(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_d30"] == 1 and r["xor_d31"] == 0
    return {
        "ok": ok,
        "k": 9,
        "q": 10,
        "xor_d30": r["xor_d30"],
        "xor_d31": r["xor_d31"],
    }


def killed_eq_nu_cells(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_d30"] == 52103 and r["n_d31"] == 50742 and r["n_d30"] != r["n_d31"]
    return {
        "ok": ok,
        "k": 9,
        "q": 10,
        "n_d30": r["n_d30"],
        "n_d31": r["n_d31"],
    }


def killed_eq_mq() -> dict:
    w = _walk_d30(1, 6)
    wj = _walk_d31_jp1(1, 6)
    ok = (
        w.get("ok")
        and wj.get("ok")
        and w["xor_d30"] == 1
        and wj["xor_jp1"] == 0
        and want_d31_jp1(1) == 1
    )
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "xor_d30": w.get("xor_d30"),
        "xor_jp1": wj.get("xor_jp1"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
        "n_d30": w.get("n_d30"),
    }


def killed_zero(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_d30"] == 1
    return {"ok": ok, "k": 9, "q": 10, "xor_d30": r["xor_d30"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_d30"] == 52103
    return {"ok": ok, "k": 9, "q": 10, "n_d30": r["n_d30"]}


def prefixes() -> dict:
    mr = json.loads(MR_JSON.read_text())
    nv = json.loads(NV_JSON.read_text())
    nu = json.loads(NU_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mr["checks"]["all_ok"]
        and nv["checks"]["all_ok"]
        and nu["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mr["verdict"]["d30_both"] == "LEMMA"
        and nv["verdict"]["d31_mod4_10"] == "LEMMA"
        and nu["verdict"]["d31_jp1_10"] == "LEMMA"
        and mr["verdict"]["prize"] == "unsolved"
        and want_d30(10) == 1
        and want_d31(10) == 0
        and want_rest10(1, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    knv: dict,
    knu: dict,
    kmq: dict,
    kz: dict,
    kemp: dict,
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
        and knv["ok"]
        and knu["ok"]
        and kmq["ok"]
        and kz["ok"]
        and kemp["ok"]
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
    q10 = q10_d30_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    knv = killed_eq_nv(q10)
    knu = killed_eq_nu_cells(q10)
    kmq = killed_eq_mq()
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kr, knv, knu, kmq, kz, kemp, sc, pref
    )
    dump = {
        "cycle": "NW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_d30_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_nv": {k: knv[k] for k in knv if k != "ok"},
        "killed_eq_nu_cells": {k: knu[k] for k in knu if k != "ok"},
        "killed_eq_mq": {k: kmq[k] for k in kmq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "lemmas": {
            "d30_10": True,
            "d30_both": True,
            "d31_jp1_10": True,
            "d31_mod4_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_nv": False,
            "eq_nu_cells": False,
            "eq_mq": False,
            "d30_zero": False,
            "d30_empty": False,
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
            "d30_10": "LEMMA",
            "d30_both": "LEMMA",
            "d31_jp1_10": "LEMMA",
            "d31_mod4_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_nv": "KILLED",
            "eq_nu_cells": "KILLED",
            "eq_mq": "KILLED",
            "d30_zero": "KILLED",
            "d30_empty": "KILLED",
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
        "q10_d30_10 n_ok",
        dump["q10_d30_10"]["n_ok"],
        "n_g1",
        dump["q10_d30_10"]["n_g1"],
        "n_d30",
        dump["q10_d30_10"]["n_d30"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_nv", dump["killed_eq_nv"])
    print("killed_eq_nu_cells", dump["killed_eq_nu_cells"])
    print("killed_eq_mq", dump["killed_eq_mq"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])


if __name__ == "__main__":
    main()
