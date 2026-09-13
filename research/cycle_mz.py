#!/usr/bin/env python3
"""Cycle MZ: on q=10 for k<=8, inner palindrome-right G=1 count is odd iff k odd.

On covering J10 for k<=8, the number of covering G=1 cells with
n<j<=n+n//2 (p=T-2j>=0; no packed row) is odd iff k is odd.
Companion of Cycle MK's inner G(j-1) xor vanish: the inner xor
vanishes while the inner count carries k-odd parity. Not rest
(k=1: par=1, rest=0); not empty (k=1 n_in=3); not MK inner xor
(k=1 par=1, xor_in=0); not jgtn (k=1 par=1, jgtn=0); not k-odd
on q=6 (k=1 n_in=0); not Green-only rest; not the form for all k.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_mz.py --certify
Dump: research/cycle_mz.json
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
MY_JSON = Path(__file__).resolve().parent / "cycle_my.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_inner_par(k: int) -> int:
    """inner palindrome-right G=1 count parity on q=10 k<=8: 1 iff k odd."""
    return int(k % 2 == 1)


def q10_inner_par() -> dict:
    """k<=8 q=10: n_in parity is k odd; prefixes MK inner xor=0 and jgtn."""
    n_ok = n_g1 = n_in = 0
    rows = {}
    mk = json.loads(MK_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_inner(k, 10)
        wp = want_inner_par(k)
        mk_row = mk["q10_inner0"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        par = w["n_in"] % 2
        if (
            not w.get("ok")
            or par != wp
            or w["xor_in"] != 0
            or w["xor_in"] != mk_row["xor_in"]
            or w["xor_jgtn"] != want_jgtn(k)
            or w["xor_jgtn"] != mk_row["xor_jgtn"]
            or w["n_in"] != mk_row["n_in"]
            or w["n_out"] != mk_row["n_out"]
            or w["n_ok"] != mj_row["n_ok"]
            or w["n_g1"] != mj_row["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "par": par,
                "wp": wp,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_in += w["n_in"]
        rows[str(k)] = {
            "par": par,
            "xor_in": w["xor_in"],
            "xor_jgtn": w["xor_jgtn"],
            "n_in": w["n_in"],
            "n_out": w["n_out"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["par"] == want_inner_par(k) for k in range(0, 9))
        and rows["1"]["n_in"] == 3
        and rows["1"]["par"] == 1
        and rows["0"]["n_in"] == 0
        and rows["0"]["par"] == 0
        and rows["8"]["n_in"] == 24038
        and rows["8"]["par"] == 0
        and rows["1"]["xor_in"] == 0
        and rows["1"]["xor_jgtn"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "n_in": n_in, "rows": rows}


def killed_eq_rest(q10: dict) -> dict:
    """inner count parity equals rest: k=1 q=10 is 1 vs 0."""
    r = q10["rows"]["1"]
    wr = want_rest10(1, 10)
    ok = r["par"] == 1 and wr == 0
    return {"ok": ok, "k": 1, "q": 10, "par": r["par"], "rest": wr}


def killed_empty(q10: dict) -> dict:
    """inner G=1 empty on q=10: k=1 has n_in=3."""
    r = q10["rows"]["1"]
    ok = r["n_in"] == 3 and r["par"] == 1
    return {"ok": ok, "k": 1, "q": 10, "n_in": r["n_in"]}


def killed_eq_mk(q10: dict) -> dict:
    """inner count parity equals MK inner G(j-1) xor: k=1 par=1 xor_in=0."""
    r = q10["rows"]["1"]
    ok = r["par"] == 1 and r["xor_in"] == 0
    return {"ok": ok, "k": 1, "q": 10, "par": r["par"], "xor_in": r["xor_in"]}


def killed_eq_jgtn(q10: dict) -> dict:
    """inner count parity equals jgtn: k=1 par=1 jgtn=0."""
    r = q10["rows"]["1"]
    ok = r["par"] == 1 and r["xor_jgtn"] == 0
    return {"ok": ok, "k": 1, "q": 10, "par": r["par"], "xor_jgtn": r["xor_jgtn"]}


def killed_q6() -> dict:
    """k-odd inner count on q=6: k=1 has n_in=0."""
    w = _walk_inner(1, 6)
    ok = w.get("ok") and w["n_in"] == 0 and want_inner_par(1) == 1
    return {
        "ok": ok,
        "k": 1,
        "q": 6,
        "n_in": w.get("n_in"),
        "par": (w.get("n_in") or 0) % 2,
        "n_ok": w.get("n_ok"),
        "n_g1": w.get("n_g1"),
    }


def prefixes() -> dict:
    mk = json.loads(MK_JSON.read_text())
    my = json.loads(MY_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mk["checks"]["all_ok"]
        and my["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mk["verdict"]["inner0"] == "LEMMA"
        and my["verdict"]["lo_odd_jp1"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and my["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kemp: dict,
    kmk: dict,
    kj: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and keq["ok"]
        and kemp["ok"]
        and kmk["ok"]
        and kj["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert want_inner_par(1) == 1 and want_inner_par(0) == 0 and want_inner_par(8) == 0
    mk = json.loads(MK_JSON.read_text())
    assert q10["n_ok"] == mk["q10_inner0"]["n_ok"]
    assert q10["n_g1"] == mk["q10_inner0"]["n_g1"]
    assert q10["n_in"] == mk["q10_inner0"]["n_in"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_inner_par()
    keq = killed_eq_rest(q10)
    kemp = killed_empty(q10)
    kmk = killed_eq_mk(q10)
    kj = killed_eq_jgtn(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kemp, kmk, kj, kq6, sc, pref)
    dump = {
        "cycle": "MZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_inner_par": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_eq_mk": {k: kmk[k] for k in kmk if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "inner_par": True,
            "inner0": True,
            "lo_odd_jp1": True,
            "jgtn_even": True,
            "rest10": True,
            "eq_rest": False,
            "inner_empty": False,
            "eq_mk": False,
            "eq_jgtn": False,
            "q6_odd": False,
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
            "inner_par": "LEMMA",
            "inner0": "LEMMA",
            "lo_odd_jp1": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "inner_empty": "KILLED",
            "eq_mk": "KILLED",
            "eq_jgtn": "KILLED",
            "q6_odd": "KILLED",
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
    print(
        "q10_inner_par n_ok",
        dump["q10_inner_par"]["n_ok"],
        "n_g1",
        dump["q10_inner_par"]["n_g1"],
        "n_in",
        dump["q10_inner_par"]["n_in"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_eq_mk", dump["killed_eq_mk"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
