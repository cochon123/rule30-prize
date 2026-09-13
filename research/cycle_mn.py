#!/usr/bin/env python3
"""Cycle MN: on q=10 for k<=8, j>n xor d%3==1 Green proxy equals rest except k=8.

On covering J10 for k<=8, XOR of Cycle MJ's j>n G(n,j-1) xor with
Cycle MM's palindrome-right d%3==1 xor equals packed rest except
at k=8 (proxy=0, rest=1). Prefix MJ/MM/MD dumps; no k=8 re-walk.
Not Green-only rest; not proxy=rest; not the proxy on q=6 (k=1
proxy=1, rest=0); not the form for all k. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mn.py --certify
Dump: research/cycle_mn.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"
MM_JSON = Path(__file__).resolve().parent / "cycle_mm.json"


def want_proxy(k: int) -> int:
    """jgtn xor d31 on q=10 k<=8: want_jgtn xor want_d31."""
    return want_jgtn(k) ^ want_d31(k)


def q10_proxy() -> dict:
    """k<=8 q=10: dumped jgtn xor d31 equals rest except k=8."""
    mj = json.loads(MJ_JSON.read_text())
    mm = json.loads(MM_JSON.read_text())
    rows = {}
    for k in range(0, 9):
        jgtn = mj["bothq_jgtn"]["rows"][str(k)]["j10"]["xor_jgtn"]
        d31 = mm["q10_d31"]["rows"][str(k)]["xor_d31"]
        rest = want_rest10(k, 10)
        proxy = jgtn ^ d31
        wp = want_proxy(k)
        wr_except = rest if k != 8 else rest ^ 1
        if (
            jgtn != want_jgtn(k)
            or d31 != want_d31(k)
            or proxy != wp
            or proxy != wr_except
            or (proxy == rest) == (k == 8)
        ):
            return {
                "ok": False,
                "k": k,
                "jgtn": jgtn,
                "d31": d31,
                "proxy": proxy,
                "rest": rest,
            }
        rows[str(k)] = {
            "jgtn": jgtn,
            "d31": d31,
            "proxy": proxy,
            "rest": rest,
        }
    ok = (
        rows["8"]["proxy"] == 0
        and rows["8"]["rest"] == 1
        and rows["2"]["proxy"] == 1
        and rows["6"]["proxy"] == 1
        and rows["0"]["proxy"] == 0
        and rows["4"]["proxy"] == 0
        and all(rows[str(k)]["proxy"] == rows[str(k)]["rest"] for k in range(0, 8))
    )
    return {"ok": ok, "rows": rows}


def killed_eq_rest(q10: dict) -> dict:
    """proxy equals rest on q=10 k<=8: k=8 is 0 vs 1."""
    r = q10["rows"]["8"]
    ok = r["proxy"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 8, "q": 10, "proxy": r["proxy"], "rest": r["rest"]}


def killed_q6_proxy() -> dict:
    """proxy equals rest on q=6: k=1 jgtn=0 d31=1 proxy=1 rest=0."""
    mj = json.loads(MJ_JSON.read_text())
    mm = json.loads(MM_JSON.read_text())
    jgtn = mj["bothq_jgtn"]["rows"]["1"]["j6"]["xor_jgtn"]
    d31 = mm["killed_q6_mod4"]["xor_d31"]
    rest = want_rest10(1, 6)
    proxy = jgtn ^ d31
    ok = jgtn == 0 and d31 == 1 and proxy == 1 and rest == 0
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "jgtn": jgtn,
        "d31": d31,
        "proxy": proxy,
        "rest": rest,
    }


def prefixes() -> dict:
    mj = json.loads(MJ_JSON.read_text())
    mm = json.loads(MM_JSON.read_text())
    ok = (
        mj["checks"]["all_ok"]
        and mm["checks"]["all_ok"]
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mm["verdict"]["d31_mod4"] == "LEMMA"
        and mj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert q10["ok"] and keq["ok"] and kq6["ok"] and sc["ok"] and pref["ok"]
    assert want_proxy(8) == 0 and want_rest10(8, 10) == 1
    assert want_proxy(2) == 1 and want_proxy(0) == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_proxy()
    keq = killed_eq_rest(q10)
    kq6 = killed_q6_proxy()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kq6, sc, pref)
    dump = {
        "cycle": "MN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_proxy": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_q6_proxy": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "proxy_k8": True,
            "d31_mod4": True,
            "jgtn_even": True,
            "d2_zero": True,
            "inner0": True,
            "q10_jm1": True,
            "rest10": True,
            "eq_rest": False,
            "q6_proxy": False,
            "green_only_rest": False,
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
            "proxy_k8": "LEMMA",
            "d31_mod4": "LEMMA",
            "jgtn_even": "LEMMA",
            "d2_zero": "LEMMA",
            "inner0": "LEMMA",
            "q10_jm1": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "q6_proxy": "KILLED",
            "green_only_rest": "KILLED",
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
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_q6_proxy", dump["killed_q6_proxy"])


if __name__ == "__main__":
    main()
