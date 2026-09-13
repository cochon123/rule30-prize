#!/usr/bin/env python3
"""Cycle NT: on q=10 through k<=10, MK inner pal-right G(j-1) vanishes.

On covering J10 through k<=10, XOR of G(n,j-1) over covering G=1
cells with n<j<=n+n//2 (p=T-2j>=0; no packed row) is 0, so Cycle
MJ's even-k j>n xor is still the outer slice. Prefix Cycle MK for
k<=8; walk k=9 and k=10. Not a death at k=9 (xor=0); not a death
at k=10 (xor=0); not rest (k=2: 0 vs 1); not NS inner even G(j+1)
(k=3 q=6: 1 vs 0); not MX inner odd-d as a q=10 lift (tautology
of this vanish on q=10); not empty (k=9 n_in=78271); not
pointwise 0 (k=1 n_gjm1=2); not inner vanish on q=6 (k=3 q=6
xor=1); not the form for all k. Do not claim T is 1 iff k=2;
do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_nt.py --certify
Dump: research/cycle_nt.json
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
from cycle_mk import _walk_inner

OUT = Path(__file__).resolve().with_suffix(".json")
MK_JSON = Path(__file__).resolve().parent / "cycle_mk.json"
MX_JSON = Path(__file__).resolve().parent / "cycle_mx.json"
NS_JSON = Path(__file__).resolve().parent / "cycle_ns.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_in": 78271,
        "n_out": 73657,
        "xor_in": 0,
        "xor_out": 0,
        "xor_jgtn": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_in": 254236,
        "n_out": 237830,
        "xor_in": 0,
        "xor_out": 1,
        "xor_jgtn": 1,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    wj = want_jgtn(k)
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_in"] == want["n_in"]
        and w["n_out"] == want["n_out"]
        and w["xor_in"] == want["xor_in"] == 0
        and w["xor_out"] == want["xor_out"] == wj
        and w["xor_jgtn"] == want["xor_jgtn"] == wj
        and w["xor_jgtn"] == w["xor_in"] ^ w["xor_out"]
    )


def q10_inner0_10() -> dict:
    """q=10 k<=10: prefix MK k<=8; walk k=9,10; xor_in vanishes."""
    mk = json.loads(MK_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_in = 0
    for k in range(0, 9):
        r = mk["q10_inner0"]["rows"][str(k)]
        wj = want_jgtn(k)
        if r["xor_in"] != 0 or r["xor_out"] != wj or r["xor_jgtn"] != wj:
            return {"ok": False, "k": k, "q": 10, "xor_in": r["xor_in"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_in += r["n_in"]
        rows[str(k)] = {
            "xor_in": r["xor_in"],
            "xor_out": r["xor_out"],
            "xor_jgtn": r["xor_jgtn"],
            "want": wj,
            "rest": want_rest10(k, 10),
            "n_in": r["n_in"],
            "n_out": r["n_out"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "MK",
        }
    for k in (9, 10):
        w = _walk_inner(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_in": w.get("xor_in"),
                "n_ok": w.get("n_ok"),
                "n_in": w.get("n_in"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_in += w["n_in"]
        rows[str(k)] = {
            "xor_in": w["xor_in"],
            "xor_out": w["xor_out"],
            "xor_jgtn": w["xor_jgtn"],
            "want": want_jgtn(k),
            "rest": want_rest10(k, 10),
            "n_in": w["n_in"],
            "n_out": w["n_out"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    mx = json.loads(MX_JSON.read_text())
    n_gjm1_k1 = mx["bothq_inner_odd"]["rows"]["1"]["j10"]["n_gjm1"]
    ok = (
        all(rows[str(k)]["xor_in"] == 0 for k in range(0, 11))
        and all(rows[str(k)]["xor_out"] == want_jgtn(k) for k in range(0, 11))
        and rows["1"]["n_in"] == 3
        and rows["8"]["n_in"] == 24038
        and rows["9"]["xor_in"] == 0
        and rows["9"]["n_in"] == 78271
        and rows["9"]["n_out"] == 73657
        and rows["9"]["xor_out"] == 0
        and rows["10"]["xor_in"] == 0
        and rows["10"]["n_in"] == 254236
        and rows["10"]["n_out"] == 237830
        and rows["10"]["xor_out"] == 1
        and n_gjm1_k1 == 2
        and want_jgtn(9) == 0
        and want_jgtn(10) == 1
        and mk["checks"]["all_ok"]
        and mk["verdict"]["inner0"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_in": n_in,
        "n_gjm1_k1": n_gjm1_k1,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_in"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_in": r["xor_in"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_in"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_in": r["xor_in"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["2"]
    ok = r["xor_in"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_in": r["xor_in"], "rest": r["rest"]}


def killed_eq_ns(q10: dict) -> dict:
    """inner G(j-1) is not NS inner even-d G(j+1): q=6 k=3 xor_in=1."""
    w = _walk_inner(3, 6)
    ok = w.get("ok") and w["xor_in"] == 1 and q10["rows"]["9"]["xor_in"] == 0
    return {
        "ok": ok,
        "k": 3,
        "q": 6,
        "xor_in": w.get("xor_in"),
        "n_in": w.get("n_in"),
    }


def killed_q6_inner(q10: dict) -> dict:
    w = _walk_inner(3, 6)
    ok = w.get("ok") and w["xor_in"] == 1 and w["n_in"] > 0
    return {
        "ok": ok,
        "k": 3,
        "q": 6,
        "xor_in": w.get("xor_in"),
        "n_in": w.get("n_in"),
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
    }


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_in"] == 78271
    return {"ok": ok, "k": 9, "q": 10, "n_in": r["n_in"]}


def killed_pointwise(q10: dict) -> dict:
    ok = q10["n_gjm1_k1"] == 2 and q10["rows"]["1"]["n_in"] == 3
    return {
        "ok": ok,
        "k": 1,
        "q": 10,
        "n_gjm1": q10["n_gjm1_k1"],
        "n_in": q10["rows"]["1"]["n_in"],
    }


def prefixes() -> dict:
    mk = json.loads(MK_JSON.read_text())
    mx = json.loads(MX_JSON.read_text())
    ns = json.loads(NS_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mk["checks"]["all_ok"]
        and mx["checks"]["all_ok"]
        and ns["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mk["verdict"]["inner0"] == "LEMMA"
        and ns["verdict"]["inner_even_jp1_10"] == "LEMMA"
        and mx["verdict"]["inner_odd_jm1"] == "LEMMA"
        and mk["verdict"]["prize"] == "unsolved"
        and want_jgtn(10) == 1
        and want_rest10(2, 10) == 1
        and mx["bothq_inner_odd"]["rows"]["1"]["j10"]["n_gjm1"] == 2
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    kns: dict,
    kq6: dict,
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
        and kns["ok"]
        and kq6["ok"]
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
    q10 = q10_inner0_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    kns = killed_eq_ns(q10)
    kq6 = killed_q6_inner(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kd9, kd10, kr, kns, kq6, kemp, kpw, sc, pref)
    dump = {
        "cycle": "NT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_inner0_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_ns": {k: kns[k] for k in kns if k != "ok"},
        "killed_q6_inner": {k: kq6[k] for k in kq6 if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "lemmas": {
            "inner0_10": True,
            "inner0": True,
            "outer_even": True,
            "jgtn_even": True,
            "inner_even_jp1_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_ns": False,
            "q6_inner0": False,
            "inner_empty": False,
            "inner_pointwise": False,
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
            "inner0_10": "LEMMA",
            "inner0": "LEMMA",
            "outer_even": "LEMMA",
            "jgtn_even": "LEMMA",
            "inner_even_jp1_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_ns": "KILLED",
            "q6_inner0": "KILLED",
            "inner_empty": "KILLED",
            "inner_pointwise": "KILLED",
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
        "q10_inner0_10 n_ok",
        dump["q10_inner0_10"]["n_ok"],
        "n_g1",
        dump["q10_inner0_10"]["n_g1"],
        "n_in",
        dump["q10_inner0_10"]["n_in"],
        "n_gjm1_k1",
        dump["q10_inner0_10"]["n_gjm1_k1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_ns", dump["killed_eq_ns"])
    print("killed_q6_inner", dump["killed_q6_inner"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])


if __name__ == "__main__":
    main()
