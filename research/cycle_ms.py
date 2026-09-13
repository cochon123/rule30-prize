#!/usr/bin/env python3
"""Cycle MS: on q=6 for k<=8, palindrome-right d%3==1 xor of G(n,j-1) is 1 iff k%4 in (0, 1, 2).

On covering J6 for k<=8, XOR of G(n,j-1) over covering G=1 cells
with j>n and (j-n)%3==1 (p=T-2j>=0; no packed row) is 1 iff
k%4 in (0, 1, 2). Companion of Cycle MM's q=10 d31 = k%4==0.
Not rest (q=6 rest=0, k=0 xor=1); not MM form (k=1 xor=1,
want_d31=0); not Cycle MR d30 (k=0 d31=1 d30=0); not jgtn
(k=1 d31=1 jgtn=0); not the {0,1,2} form on q=10 (k=1 d31=0);
not Green-only rest; not the form for all k. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ms.py --certify
Dump: research/cycle_ms.json
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
from cycle_mm import _walk_d31, want_d31
from cycle_mr import want_d30

OUT = Path(__file__).resolve().with_suffix(".json")
MM_JSON = Path(__file__).resolve().parent / "cycle_mm.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"
MR_JSON = Path(__file__).resolve().parent / "cycle_mr.json"


def want_d31_q6(k: int) -> int:
    """palindrome-right d%3==1 xor of G(n,j-1) on q=6 k<=8: 1 iff k%4 in (0, 1, 2)."""
    return int(k % 4 in (0, 1, 2))


def q6_d31() -> dict:
    """k<=8 q=6: d%3==1 G(j-1) xor is 1 iff k%4 in (0, 1, 2)."""
    n_ok = n_g1 = n_d31 = 0
    rows = {}
    mr = json.loads(MR_JSON.read_text())
    for k in range(0, 9):
        w = _walk_d31(k, 6)
        wd = want_d31_q6(k)
        mr_row = mr["bothq_d30"]["rows"][str(k)]["j6"]
        if (
            not w.get("ok")
            or w["xor_d31"] != wd
            or w["xor_d31"] != mr_row["xor_d31"]
            or w["n_ok"] != mr_row["n_ok"]
            or w["n_g1"] != mr_row["n_g1"]
            or w["n_d31"] != mr_row["n_d31"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 6,
                "xor_d31": w.get("xor_d31"),
                "wd": wd,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_d31 += w["n_d31"]
        rows[str(k)] = {
            "xor_d31": w["xor_d31"],
            "xor_jgtn": w["xor_jgtn"],
            "n_d31": w["n_d31"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_d31"] == want_d31_q6(k) for k in range(0, 9))
        and rows["0"]["xor_d31"] == 1
        and rows["1"]["xor_d31"] == 1
        and rows["2"]["xor_d31"] == 1
        and rows["3"]["xor_d31"] == 0
        and rows["7"]["xor_d31"] == 0
        and rows["8"]["xor_d31"] == 1
        and want_d31(1) == 0
        and rows["0"]["n_d31"] > 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_d31": n_d31, "rows": rows}


def killed_eq_rest(q6: dict) -> dict:
    """q=6 d31 xor equals rest: k=0 is 1 vs 0."""
    r = q6["rows"]["0"]
    wr = want_rest10(0, 6)
    ok = r["xor_d31"] == 1 and wr == 0
    return {"ok": ok, "k": 0, "q": 6, "xor_d31": r["xor_d31"], "rest": wr}


def killed_eq_mm(q6: dict) -> dict:
    """q=6 d31 xor equals MM k%4==0: k=1 is 1 vs 0."""
    r = q6["rows"]["1"]
    ok = r["xor_d31"] == 1 and want_d31(1) == 0
    return {"ok": ok, "k": 1, "q": 6, "xor_d31": r["xor_d31"], "want_d31": 0}


def killed_eq_d30(q6: dict) -> dict:
    """q=6 d31 xor equals MR d30: k=0 d31=1 d30=0."""
    r = q6["rows"]["0"]
    ok = r["xor_d31"] == 1 and want_d30(0) == 0
    return {"ok": ok, "k": 0, "q": 6, "xor_d31": r["xor_d31"], "want_d30": 0}


def killed_eq_jgtn(q6: dict) -> dict:
    """q=6 d31 xor equals jgtn: k=1 d31=1 jgtn=0."""
    r = q6["rows"]["1"]
    ok = r["xor_d31"] == 1 and r["xor_jgtn"] == 0 and want_jgtn(1) == 0
    return {"ok": ok, "k": 1, "q": 6, "xor_d31": r["xor_d31"], "xor_jgtn": r["xor_jgtn"]}


def killed_q10_mod() -> dict:
    """{0,1,2} form on q=10: k=1 d31=0 but 1%4 in {0,1,2}."""
    mm = json.loads(MM_JSON.read_text())
    r = mm["q10_d31"]["rows"]["1"]
    ok = r["xor_d31"] == 0 and want_d31_q6(1) == 1
    return {"ok": ok, "k": 1, "q": 10, "xor_d31": r["xor_d31"], "n_d31": r["n_d31"]}


def prefixes() -> dict:
    mm = json.loads(MM_JSON.read_text())
    mr = json.loads(MR_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mm["checks"]["all_ok"]
        and mr["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mm["verdict"]["d31_mod4"] == "LEMMA"
        and mr["verdict"]["d30_both"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mm["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q6: dict,
    keq: dict,
    kmm: dict,
    kd30: dict,
    kj: dict,
    kq10: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q6["ok"]
        and keq["ok"]
        and kmm["ok"]
        and kd30["ok"]
        and kj["ok"]
        and kq10["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_d31_q6(0) == 1 and want_d31_q6(3) == 0 and want_d31_q6(1) == 1
    mr = json.loads(MR_JSON.read_text())
    n6 = sum(mr["bothq_d30"]["rows"][str(k)]["j6"]["n_ok"] for k in range(0, 9))
    assert q6["n_ok"] == n6
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q6 = q6_d31()
    keq = killed_eq_rest(q6)
    kmm = killed_eq_mm(q6)
    kd30 = killed_eq_d30(q6)
    kj = killed_eq_jgtn(q6)
    kq10 = killed_q10_mod()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q6, keq, kmm, kd30, kj, kq10, sc, pref)
    dump = {
        "cycle": "MS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q6_d31": {k: q6[k] for k in q6 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_eq_mm": {k: kmm[k] for k in kmm if k != "ok"},
        "killed_eq_d30": {k: kd30[k] for k in kd30 if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "killed_q10_mod": {k: kq10[k] for k in kq10 if k != "ok"},
        "lemmas": {
            "d31_q6": True,
            "d30_both": True,
            "d31_mod4": True,
            "jgtn_even": True,
            "rest10": True,
            "eq_rest": False,
            "eq_mm": False,
            "eq_d30": False,
            "eq_jgtn": False,
            "q10_mod": False,
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
            "d31_q6": "LEMMA",
            "d30_both": "LEMMA",
            "d31_mod4": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "eq_mm": "KILLED",
            "eq_d30": "KILLED",
            "eq_jgtn": "KILLED",
            "q10_mod": "KILLED",
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
    print("q6_d31 n_ok", dump["q6_d31"]["n_ok"], "n_g1", dump["q6_d31"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_mm", dump["killed_eq_mm"])
    print("killed_eq_d30", dump["killed_eq_d30"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_q10_mod", dump["killed_q10_mod"])


if __name__ == "__main__":
    main()
