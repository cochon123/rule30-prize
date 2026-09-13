#!/usr/bin/env python3
"""Cycle OB: on q=10 through k<=10, NF outer T is 1 iff k%3==2.

On covering J10 through k<=10, XOR of G(n,j-1) over palindrome-right
G=1 cells with n<U/2 and j>n+n//2 (p=T-2j>=0; no packed row) is 1
iff k%3==2. Prefix Cycle NF for k<=8; walk k=9 and k=10. Companion
NG inner still holds at those k. Not a death at k=9 (xor=0=want);
not a death at k=10 (xor=0=want); not T (k=5: 1 vs 0); not rest
(k=5: 1 vs 0); not inner T (k=2: 1 vs 0); not NN T-cell G(j+1)
(k=9: 0 vs 1); not empty (k=9 n_out=4296); not pointwise 0 (k=9
n_outg=1650); not 0 (k=5: 1); not the form for all k. Do not
claim T is 1 iff k=2; do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_ob.py --certify
Dump: research/cycle_ob.json
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
from cycle_nf import _walk_t_outer, want_t_outer
from cycle_ng import want_t_inner
from cycle_nn import want_t_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
NF_JSON = Path(__file__).resolve().parent / "cycle_nf.json"
OA_JSON = Path(__file__).resolve().parent / "cycle_oa.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_out": 4296,
        "n_outg": 1650,
        "n_t": 6912,
        "xor_out": 0,
        "xor_in": 0,
        "xor_t": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_out": 13873,
        "n_outg": 5314,
        "n_t": 22528,
        "xor_out": 0,
        "xor_in": 0,
        "xor_t": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_out"] == want["n_out"]
        and w["n_outg"] == want["n_outg"]
        and w["n_t"] == want["n_t"]
        and w["xor_out"] == want["xor_out"] == want_t_outer(k)
        and w["xor_in"] == want["xor_in"] == want_t_inner(k)
        and w["xor_t"] == want["xor_t"] == w["xor_in"] ^ w["xor_out"]
    )


def q10_t_outer_10() -> dict:
    """q=10 k<=10: prefix NF k<=8; walk k=9,10; xor_out = want_t_outer."""
    nf = json.loads(NF_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_out = n_outg = 0
    for k in range(0, 9):
        r = nf["bothq_t_outer"]["rows"][str(k)]["j10"]
        wh = want_t_outer(k)
        if r["xor_out"] != wh:
            return {"ok": False, "k": k, "q": 10, "xor_out": r["xor_out"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_out += r["n_out"]
        n_outg += r["n_outg"]
        rows[str(k)] = {
            "xor_out": r["xor_out"],
            "xor_in": r["xor_in"],
            "xor_t": r["xor_t"],
            "want": wh,
            "want_in": want_t_inner(k),
            "want_jp1": want_t_jp1(k),
            "rest": want_rest10(k, 10),
            "n_out": r["n_out"],
            "n_outg": r["n_outg"],
            "n_t": r["n_t"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "NF",
        }
    for k in (9, 10):
        w = _walk_t_outer(k, 10)
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
        n_outg += w["n_outg"]
        rows[str(k)] = {
            "xor_out": w["xor_out"],
            "xor_in": w["xor_in"],
            "xor_t": w["xor_t"],
            "want": want_t_outer(k),
            "want_in": want_t_inner(k),
            "want_jp1": want_t_jp1(k),
            "rest": want_rest10(k, 10),
            "n_out": w["n_out"],
            "n_outg": w["n_outg"],
            "n_t": w["n_t"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_out"] == want_t_outer(k) for k in range(0, 11))
        and rows["2"]["n_out"] == 1
        and rows["2"]["xor_out"] == 1
        and rows["2"]["xor_in"] == 0
        and rows["5"]["xor_out"] == 1
        and rows["5"]["xor_t"] == 0
        and rows["8"]["n_out"] == 1333
        and rows["8"]["xor_out"] == 1
        and rows["9"]["xor_out"] == 0
        and rows["9"]["n_out"] == 4296
        and rows["9"]["n_outg"] == 1650
        and rows["10"]["xor_out"] == 0
        and rows["10"]["n_out"] == 13873
        and rows["10"]["n_outg"] == 5314
        and want_t_outer(9) == 0
        and want_t_outer(10) == 0
        and want_t_outer(8) == 1
        and want_t_inner(9) == 0
        and nf["checks"]["all_ok"]
        and nf["verdict"]["t_outer"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_out": n_out,
        "n_outg": n_outg,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_out"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_out": r["xor_out"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_out"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_out": r["xor_out"]}


def killed_eq_t(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_out"] == 1 and r["xor_t"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_out": r["xor_out"], "xor_t": r["xor_t"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_out"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_out": r["xor_out"], "rest": r["rest"]}


def killed_eq_inner(q10: dict) -> dict:
    r = q10["rows"]["2"]
    ok = r["xor_out"] == 1 and r["xor_in"] == 0
    return {"ok": ok, "k": 2, "q": 10, "xor_out": r["xor_out"], "xor_in": r["xor_in"]}


def killed_eq_jp1(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_out"] == 0 and r["want_jp1"] == 1
    return {"ok": ok, "k": 9, "q": 10, "xor_out": r["xor_out"], "want_jp1": r["want_jp1"]}


def killed_zero(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_out"] == 1
    return {"ok": ok, "k": 5, "q": 10, "xor_out": r["xor_out"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_out"] == 4296
    return {"ok": ok, "k": 9, "q": 10, "n_out": r["n_out"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_outg"] == 1650 and r["xor_out"] == 0
    return {"ok": ok, "k": 9, "q": 10, "n_outg": r["n_outg"]}


def prefixes() -> dict:
    nf = json.loads(NF_JSON.read_text())
    oa = json.loads(OA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nf["checks"]["all_ok"]
        and oa["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nf["verdict"]["t_outer"] == "LEMMA"
        and oa["verdict"]["s_nltu_10"] == "LEMMA"
        and nf["verdict"]["prize"] == "unsolved"
        and want_t_outer(8) == 1
        and want_t_inner(2) == 0
        and want_t_jp1(9) == 1
        and want_rest10(5, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kt: dict,
    kr: dict,
    kin: dict,
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
        and kt["ok"]
        and kr["ok"]
        and kin["ok"]
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
    q10 = q10_t_outer_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kt = killed_eq_t(q10)
    kr = killed_eq_rest(q10)
    kin = killed_eq_inner(q10)
    kj = killed_eq_jp1(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kt, kr, kin, kj, kz, kemp, kpw, sc, pref
    )
    dump = {
        "cycle": "OB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_t_outer_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_t": {k: kt[k] for k in kt if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_inner": {k: kin[k] for k in kin if k != "ok"},
        "killed_eq_jp1": {k: kj[k] for k in kj if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "lemmas": {
            "t_outer_10": True,
            "t_outer": True,
            "s_nltu_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_t": False,
            "eq_rest": False,
            "eq_inner": False,
            "eq_jp1": False,
            "t_outer_zero": False,
            "nout_empty": False,
            "nout_pointwise": False,
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
            "t_outer_10": "LEMMA",
            "t_outer": "LEMMA",
            "s_nltu_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_t": "KILLED",
            "eq_rest": "KILLED",
            "eq_inner": "KILLED",
            "eq_jp1": "KILLED",
            "t_outer_zero": "KILLED",
            "nout_empty": "KILLED",
            "nout_pointwise": "KILLED",
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
        "q10_t_outer_10 n_ok",
        dump["q10_t_outer_10"]["n_ok"],
        "n_g1",
        dump["q10_t_outer_10"]["n_g1"],
        "n_out",
        dump["q10_t_outer_10"]["n_out"],
        "n_outg",
        dump["q10_t_outer_10"]["n_outg"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_t", dump["killed_eq_t"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_inner", dump["killed_eq_inner"])
    print("killed_eq_jp1", dump["killed_eq_jp1"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])


if __name__ == "__main__":
    main()
