#!/usr/bin/env python3
"""Cycle NU: on q=10 through k<=10, MQ pal-right d%3==1 G(j+1) is 1 iff k%4 in (1, 2).

On covering J10 through k<=10, XOR of G(n,j+1) over covering G=1
cells with j>n and (j-n)%3==1 (p=T-2j>=0; no packed row) is 1 iff
k%4 in (1, 2). Prefix Cycle MQ for k<=8; walk k=9 and k=10. Dual
of Cycle MM's G(n,j-1) d31 = k%4==0, which still holds as a
companion at k=9,10 (xor_jm1=0). Not a death at k=9 (xor=1=want);
not a death at k=10 (xor=1=want); not rest (k=1: 1 vs 0); not NQ
T-cell d31 G(j+1) (k=9: 1 vs 0); not MM Green d31 (k=9: 1 vs 0);
not NT inner G(j-1) vanish (k=9: 1 vs 0); not 0; not empty (k=9
n_d31=50742); not the form on q=6; not the form for all k. Do
not claim T is 1 iff k=2; do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_nu.py --certify
Dump: research/cycle_nu.json
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
from cycle_mm import want_d31
from cycle_mq import _walk_d31_jp1, want_d31_jp1
from cycle_nq import want_t_d31_jp1

OUT = Path(__file__).resolve().with_suffix(".json")
MQ_JSON = Path(__file__).resolve().parent / "cycle_mq.json"
NT_JSON = Path(__file__).resolve().parent / "cycle_nt.json"
MM_JSON = Path(__file__).resolve().parent / "cycle_mm.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_d31": 50742,
        "xor_jp1": 1,
        "xor_jm1": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_d31": 160761,
        "xor_jp1": 1,
        "xor_jm1": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_d31"] == want["n_d31"]
        and w["xor_jp1"] == want["xor_jp1"] == want_d31_jp1(k)
        and w["xor_jm1"] == want["xor_jm1"] == want_d31(k)
    )


def q10_d31_jp1_10() -> dict:
    """q=10 k<=10: prefix MQ k<=8; walk k=9,10; xor_jp1 = want_d31_jp1."""
    mq = json.loads(MQ_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_d31 = 0
    for k in range(0, 9):
        r = mq["q10_d31_jp1"]["rows"][str(k)]
        wj = want_d31_jp1(k)
        if r["xor_jp1"] != wj or r["xor_jm1"] != want_d31(k):
            return {"ok": False, "k": k, "q": 10, "xor_jp1": r["xor_jp1"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_d31 += r["n_d31"]
        rows[str(k)] = {
            "xor_jp1": r["xor_jp1"],
            "xor_jm1": r["xor_jm1"],
            "want": wj,
            "rest": want_rest10(k, 10),
            "n_d31": r["n_d31"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "MQ",
        }
    for k in (9, 10):
        w = _walk_d31_jp1(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_jp1": w.get("xor_jp1"),
                "n_ok": w.get("n_ok"),
                "n_d31": w.get("n_d31"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_d31 += w["n_d31"]
        rows[str(k)] = {
            "xor_jp1": w["xor_jp1"],
            "xor_jm1": w["xor_jm1"],
            "want": want_d31_jp1(k),
            "rest": want_rest10(k, 10),
            "n_d31": w["n_d31"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_jp1"] == want_d31_jp1(k) for k in range(0, 11))
        and all(rows[str(k)]["xor_jm1"] == want_d31(k) for k in range(0, 11))
        and rows["0"]["n_d31"] == 1
        and rows["1"]["n_d31"] == 6
        and rows["1"]["xor_jp1"] == 1
        and rows["8"]["n_d31"] == 15146
        and rows["8"]["xor_jp1"] == 0
        and rows["9"]["xor_jp1"] == 1
        and rows["9"]["n_d31"] == 50742
        and rows["9"]["xor_jm1"] == 0
        and rows["10"]["xor_jp1"] == 1
        and rows["10"]["n_d31"] == 160761
        and rows["10"]["xor_jm1"] == 0
        and want_d31_jp1(9) == 1
        and want_d31_jp1(10) == 1
        and want_t_d31_jp1(9) == 0
        and want_d31(9) == 0
        and mq["checks"]["all_ok"]
        and mq["verdict"]["d31_jp1"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_d31": n_d31,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_jp1"] == 1 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_jp1": r["xor_jp1"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_jp1"] == 1 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_jp1": r["xor_jp1"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["1"]
    ok = r["xor_jp1"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 1, "q": 10, "xor_jp1": r["xor_jp1"], "rest": r["rest"]}


def killed_eq_nq(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_jp1"] == 1 and want_t_d31_jp1(9) == 0
    return {"ok": ok, "k": 9, "q": 10, "xor_jp1": r["xor_jp1"]}


def killed_eq_mm(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_jp1"] == 1 and r["xor_jm1"] == 0
    return {
        "ok": ok,
        "k": 9,
        "q": 10,
        "xor_jp1": r["xor_jp1"],
        "xor_jm1": r["xor_jm1"],
    }


def killed_eq_nt(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_jp1"] == 1
    return {"ok": ok, "k": 9, "q": 10, "xor_jp1": r["xor_jp1"]}


def killed_zero(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_jp1"] == 1
    return {"ok": ok, "k": 9, "q": 10, "xor_jp1": r["xor_jp1"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_d31"] == 50742
    return {"ok": ok, "k": 9, "q": 10, "n_d31": r["n_d31"]}


def killed_q6_mod() -> dict:
    w = _walk_d31_jp1(1, 6)
    ok = w.get("ok") and w["xor_jp1"] == 0 and want_d31_jp1(1) == 1
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "xor_jp1": w.get("xor_jp1"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
        "n_d31": w.get("n_d31"),
    }


def prefixes() -> dict:
    mq = json.loads(MQ_JSON.read_text())
    nt = json.loads(NT_JSON.read_text())
    mm = json.loads(MM_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mq["checks"]["all_ok"]
        and nt["checks"]["all_ok"]
        and mm["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mq["verdict"]["d31_jp1"] == "LEMMA"
        and nt["verdict"]["inner0_10"] == "LEMMA"
        and mm["verdict"]["d31_mod4"] == "LEMMA"
        and mq["verdict"]["prize"] == "unsolved"
        and want_d31_jp1(10) == 1
        and want_rest10(1, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    knq: dict,
    kmm: dict,
    knt: dict,
    kz: dict,
    kemp: dict,
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
        and knq["ok"]
        and kmm["ok"]
        and knt["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kq6["ok"]
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
    q10 = q10_d31_jp1_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    knq = killed_eq_nq(q10)
    kmm = killed_eq_mm(q10)
    knt = killed_eq_nt(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6_mod()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kr, knq, kmm, knt, kz, kemp, kq6, sc, pref
    )
    dump = {
        "cycle": "NU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_d31_jp1_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_nq": {k: knq[k] for k in knq if k != "ok"},
        "killed_eq_mm": {k: kmm[k] for k in kmm if k != "ok"},
        "killed_eq_nt": {k: knt[k] for k in knt if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6_mod": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "d31_jp1_10": True,
            "d31_jp1": True,
            "d31_mod4": True,
            "inner0_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_nq": False,
            "eq_mm": False,
            "eq_nt": False,
            "d31_jp1_zero": False,
            "d31_empty": False,
            "q6_mod": False,
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
            "d31_jp1_10": "LEMMA",
            "d31_jp1": "LEMMA",
            "d31_mod4": "LEMMA",
            "inner0_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_nq": "KILLED",
            "eq_mm": "KILLED",
            "eq_nt": "KILLED",
            "d31_jp1_zero": "KILLED",
            "d31_empty": "KILLED",
            "q6_mod": "KILLED",
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
        "q10_d31_jp1_10 n_ok",
        dump["q10_d31_jp1_10"]["n_ok"],
        "n_g1",
        dump["q10_d31_jp1_10"]["n_g1"],
        "n_d31",
        dump["q10_d31_jp1_10"]["n_d31"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_nq", dump["killed_eq_nq"])
    print("killed_eq_mm", dump["killed_eq_mm"])
    print("killed_eq_nt", dump["killed_eq_nt"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6_mod", dump["killed_q6_mod"])


if __name__ == "__main__":
    main()
