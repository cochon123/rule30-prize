#!/usr/bin/env python3
"""Cycle OA: on q=10 through k<=10, NC n<U S is 1 iff k>0 and k%4==0.

On covering J10 through k<=10, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and n<U (p=T-2j>=0; no packed row)
is 1 iff k>0 and k%4==0. Prefix Cycle NC for k<=8; walk k=9 and
k=10. Companion NZ mid vanish and NY high S still hold at those
k. Not a death at k=9 (xor=0=want); not a death at k=10
(xor=0=want); not rest (k=4: 1 vs 0); not NY high S (k=6: 0 vs
1); not NZ mid (k=4: 1 vs 0); not NA S (k=6: 0 vs 1); not empty
(k=9 n_s=4372); not pointwise 0 (k=9 n_sg=1728); not 0 (k=4: 1);
not the form for all k. Do not claim T is 1 iff k=2; do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_oa.py --certify
Dump: research/cycle_oa.json
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
from cycle_mq import want_d31_jp1
from cycle_nc import _walk_s_nltu, want_s_nltu
from cycle_ne import want_s_hi

OUT = Path(__file__).resolve().with_suffix(".json")
NC_JSON = Path(__file__).resolve().parent / "cycle_nc.json"
NZ_JSON = Path(__file__).resolve().parent / "cycle_nz.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_s": 4372,
        "n_sg": 1728,
        "xor": 0,
        "xor_sall": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_s": 13890,
        "n_sg": 6282,
        "xor": 0,
        "xor_sall": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_s"] == want["n_s"]
        and w["n_sg"] == want["n_sg"]
        and w["xor"] == want["xor"] == want_s_nltu(k)
        and w["xor_sall"] == want["xor_sall"] == w["xor"] ^ want_s_hi(k)
        and w["xor_jgtn"] == want_jgtn(k)
    )


def q10_s_nltu_10() -> dict:
    """q=10 k<=10: prefix NC k<=8; walk k=9,10; xor = want_s_nltu."""
    nc = json.loads(NC_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_s = n_sg = 0
    for k in range(0, 9):
        r = nc["bothq_s_nltu"]["rows"][str(k)]["j10"]
        wh = want_s_nltu(k)
        if r["xor"] != wh:
            return {"ok": False, "k": k, "q": 10, "xor": r["xor"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_s += r["n_s"]
        n_sg += r["n_sg"]
        rows[str(k)] = {
            "xor": r["xor"],
            "xor_sall": r["xor_sall"],
            "xor_jgtn": r["xor_jgtn"],
            "want": wh,
            "want_hi": want_s_hi(k),
            "rest": want_rest10(k, 10),
            "n_s": r["n_s"],
            "n_sg": r["n_sg"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "NC",
        }
    for k in (9, 10):
        w = _walk_s_nltu(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor": w.get("xor"),
                "n_ok": w.get("n_ok"),
                "n_s": w.get("n_s"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_s += w["n_s"]
        n_sg += w["n_sg"]
        rows[str(k)] = {
            "xor": w["xor"],
            "xor_sall": w["xor_sall"],
            "xor_jgtn": w["xor_jgtn"],
            "want": want_s_nltu(k),
            "want_hi": want_s_hi(k),
            "rest": want_rest10(k, 10),
            "n_s": w["n_s"],
            "n_sg": w["n_sg"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor"] == want_s_nltu(k) for k in range(0, 11))
        and rows["0"]["n_s"] == 0
        and rows["3"]["n_s"] == 2
        and rows["3"]["n_sg"] == 0
        and rows["4"]["n_s"] == 6
        and rows["4"]["n_sg"] == 3
        and rows["4"]["xor"] == 1
        and rows["6"]["xor"] == 0
        and rows["6"]["xor_sall"] == 1
        and rows["8"]["n_s"] == 1222
        and rows["8"]["xor"] == 1
        and rows["9"]["xor"] == 0
        and rows["9"]["n_s"] == 4372
        and rows["9"]["n_sg"] == 1728
        and rows["10"]["xor"] == 0
        and rows["10"]["n_s"] == 13890
        and rows["10"]["n_sg"] == 6282
        and want_s_nltu(9) == 0
        and want_s_nltu(10) == 0
        and want_s_nltu(8) == 1
        and nc["checks"]["all_ok"]
        and nc["verdict"]["s_nltu"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_s": n_s,
        "n_sg": n_sg,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor": r["xor"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor": r["xor"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor": r["xor"], "rest": r["rest"]}


def killed_eq_hi(q10: dict) -> dict:
    r = q10["rows"]["6"]
    ok = r["xor"] == 0 and r["want_hi"] == 1
    return {"ok": ok, "k": 6, "q": 10, "xor": r["xor"], "want_hi": r["want_hi"]}


def killed_eq_mid(q10: dict) -> dict:
    r = q10["rows"]["4"]
    nz = json.loads(NZ_JSON.read_text())
    mid = nz["q10_s_mid_10"]["rows"]["4"]["xor_mid"]
    ok = r["xor"] == 1 and mid == 0
    return {"ok": ok, "k": 4, "q": 10, "xor": r["xor"], "xor_mid": mid}


def killed_eq_s(q10: dict) -> dict:
    r = q10["rows"]["6"]
    ok = r["xor"] == 0 and r["xor_sall"] == 1
    return {"ok": ok, "k": 6, "q": 10, "xor": r["xor"], "xor_sall": r["xor_sall"]}


def killed_eq_d31(q10: dict) -> dict:
    r = q10["rows"]["0"]
    ok = r["xor"] == 0 and want_d31(0) == 1
    return {"ok": ok, "k": 0, "q": 10, "xor": r["xor"], "d31": 1}


def killed_eq_jp1(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor"] == 1 and want_d31_jp1(4) == 0
    return {"ok": ok, "k": 4, "q": 10, "xor": r["xor"], "d31_jp1": 0}


def killed_eq_jgtn(q10: dict) -> dict:
    r = q10["rows"]["2"]
    ok = r["xor"] == 0 and r["xor_jgtn"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor": r["xor"], "xor_jgtn": r["xor_jgtn"]}


def killed_zero(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor": r["xor"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_s"] == 4372
    return {"ok": ok, "k": 9, "q": 10, "n_s": r["n_s"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_sg"] == 1728 and r["xor"] == 0
    return {"ok": ok, "k": 9, "q": 10, "n_sg": r["n_sg"]}


def prefixes() -> dict:
    nc = json.loads(NC_JSON.read_text())
    nz = json.loads(NZ_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nc["checks"]["all_ok"]
        and nz["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nc["verdict"]["s_nltu"] == "LEMMA"
        and nz["verdict"]["s_mid_10"] == "LEMMA"
        and nc["verdict"]["prize"] == "unsolved"
        and want_s_nltu(4) == 1
        and want_s_hi(6) == 1
        and want_rest10(4, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    kh: dict,
    km: dict,
    ks: dict,
    kd31: dict,
    kjp1: dict,
    kj: dict,
    kz: dict,
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
        and kh["ok"]
        and km["ok"]
        and ks["ok"]
        and kd31["ok"]
        and kjp1["ok"]
        and kj["ok"]
        and kz["ok"]
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
    q10 = q10_s_nltu_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    kh = killed_eq_hi(q10)
    km = killed_eq_mid(q10)
    ks = killed_eq_s(q10)
    kd31 = killed_eq_d31(q10)
    kjp1 = killed_eq_jp1(q10)
    kj = killed_eq_jgtn(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20,
        q10,
        kd9,
        kd10,
        kr,
        kh,
        km,
        ks,
        kd31,
        kjp1,
        kj,
        kz,
        kemp,
        kpw,
        sc,
        pref,
    )
    dump = {
        "cycle": "OA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_nltu_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_eq_mid": {k: km[k] for k in km if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_d31": {k: kd31[k] for k in kd31 if k != "ok"},
        "killed_eq_jp1": {k: kjp1[k] for k in kjp1 if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "lemmas": {
            "s_nltu_10": True,
            "s_nltu": True,
            "s_mid_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_hi": False,
            "eq_mid": False,
            "eq_s": False,
            "eq_d31": False,
            "eq_jp1": False,
            "eq_jgtn": False,
            "s_nltu_zero": False,
            "ns_empty": False,
            "ns_pointwise": False,
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
            "s_nltu_10": "LEMMA",
            "s_nltu": "LEMMA",
            "s_mid_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_hi": "KILLED",
            "eq_mid": "KILLED",
            "eq_s": "KILLED",
            "eq_d31": "KILLED",
            "eq_jp1": "KILLED",
            "eq_jgtn": "KILLED",
            "s_nltu_zero": "KILLED",
            "ns_empty": "KILLED",
            "ns_pointwise": "KILLED",
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
        "q10_s_nltu_10 n_ok",
        dump["q10_s_nltu_10"]["n_ok"],
        "n_g1",
        dump["q10_s_nltu_10"]["n_g1"],
        "n_s",
        dump["q10_s_nltu_10"]["n_s"],
        "n_sg",
        dump["q10_s_nltu_10"]["n_sg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_eq_mid", dump["killed_eq_mid"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_d31", dump["killed_eq_d31"])
    print("killed_eq_jp1", dump["killed_eq_jp1"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])


if __name__ == "__main__":
    main()
