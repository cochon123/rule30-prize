#!/usr/bin/env python3
"""Cycle MW: on q=10 for k<=8, outer palindrome-right xor of G(n,j+1) on G=1 is identically 1.

On covering J10 for k<=8, XOR of G(n,j+1) over covering G=1 cells
with j > n + n//2 (p=T-2j>=0; no packed row) is 1. Companion of
Cycle MV's inner even-d G(j+1) vanish and Cycle MK's inner G(j-1)
vanish. Not rest (k=0: out=1, rest=0); not 0; not empty (k=0
n_out=3); not pointwise 0 (k=0 n_gjp1=1); not identically 1 on
q=6 (k=4 xor=0); not jgtn; not MV inner even vanish; not
Green-only rest; not the form for all k. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do
not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mw.py --certify
Dump: research/cycle_mw.json
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
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_kh import g4_xor_cover
from cycle_md import want_rest10
from cycle_mj import want_jgtn

OUT = Path(__file__).resolve().with_suffix(".json")
MV_JSON = Path(__file__).resolve().parent / "cycle_mv.json"
MK_JSON = Path(__file__).resolve().parent / "cycle_mk.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_outer_jp1(_k: int) -> int:
    """outer palindrome-right xor of G(n,j+1) on q=10 k<=8: identically 1."""
    return 1


def _walk_outer_jp1(k: int, q: int) -> dict:
    """Covering G=1 xor of G(n,j+1) on outer palindrome-right; also inner even."""
    U = 1 << k
    T, t0, Q = q * U, 2 * U, covering_Q(q)
    n_ok = n_g1 = n_out = n_gjp1 = n_in = n_ine = 0
    xor_out = xor_ine = xor_jgtn = 0
    t = 0
    s = t0 + 1
    while s < T:
        n = odd_clock(t, U, Q)
        for j in range(0, 2 * n + 1):
            p = T - 2 * j
            if p < 0:
                continue
            n_ok += 1
            if G(n, j) == 0:
                continue
            n_g1 += 1
            if j <= n:
                continue
            xor_jgtn ^= G(n, j - 1)
            d = j - n
            if d <= n // 2:
                n_in += 1
                if d % 2 == 0:
                    n_ine += 1
                    xor_ine ^= G(n, j + 1)
            else:
                n_out += 1
                xor_out ^= G(n, j + 1)
                n_gjp1 += G(n, j + 1)
        t += 1
        s += 2
    return {
        "ok": n_ok > 0,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_out": n_out,
        "n_gjp1": n_gjp1,
        "n_in": n_in,
        "n_ine": n_ine,
        "xor_out": xor_out,
        "xor_ine": xor_ine,
        "xor_jgtn": xor_jgtn,
    }


def q10_outer_jp1() -> dict:
    """k<=8 q=10: outer G(j+1) xor is 1; inner even jp1=0; n_out matches MK."""
    n_ok = n_g1 = n_out = n_gjp1 = 0
    rows = {}
    mv = json.loads(MV_JSON.read_text())
    mk = json.loads(MK_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_outer_jp1(k, 10)
        mv_row = mv["bothq_inner_even"]["rows"][str(k)]["j10"]
        mk_row = mk["q10_inner0"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        if (
            not w.get("ok")
            or w["xor_out"] != 1
            or w["xor_ine"] != 0
            or w["xor_ine"] != mv_row["xor_ine"]
            or w["n_ine"] != mv_row["n_ine"]
            or w["n_in"] != mk_row["n_in"]
            or w["n_out"] != mk_row["n_out"]
            or w["xor_jgtn"] != want_jgtn(k)
            or w["xor_jgtn"] != mk_row["xor_jgtn"]
            or w["n_ok"] != mj_row["n_ok"]
            or w["n_g1"] != mj_row["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_out": w.get("xor_out"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_out += w["n_out"]
        n_gjp1 += w["n_gjp1"]
        rows[str(k)] = {
            "xor_out": w["xor_out"],
            "xor_ine": w["xor_ine"],
            "xor_jgtn": w["xor_jgtn"],
            "n_out": w["n_out"],
            "n_gjp1": w["n_gjp1"],
            "n_ine": w["n_ine"],
            "n_in": w["n_in"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_out"] == 1 for k in range(0, 9))
        and all(rows[str(k)]["xor_ine"] == 0 for k in range(0, 9))
        and rows["0"]["n_out"] == 3
        and rows["0"]["n_gjp1"] == 1
        and rows["8"]["n_out"] == 22844
        and rows["1"]["xor_jgtn"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_out": n_out,
        "n_gjp1": n_gjp1,
        "rows": rows,
    }


def killed_eq_rest(q10: dict) -> dict:
    """outer G(j+1) xor equals rest: k=0 q=10 is 1 vs 0."""
    r = q10["rows"]["0"]
    wr = want_rest10(0, 10)
    ok = r["xor_out"] == 1 and wr == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_out": r["xor_out"], "rest": wr}


def killed_zero(q10: dict) -> dict:
    """outer G(j+1) xor vanishes on q=10: k=0 is 1."""
    r = q10["rows"]["0"]
    ok = r["xor_out"] == 1
    return {"ok": ok, "k": 0, "q": 10, "xor_out": r["xor_out"]}


def killed_empty(q10: dict) -> dict:
    """outer G=1 empty on q=10: k=0 has n_out=3."""
    r = q10["rows"]["0"]
    ok = r["n_out"] == 3 and r["xor_out"] == 1
    return {"ok": ok, "k": 0, "q": 10, "n_out": r["n_out"]}


def killed_pointwise(q10: dict) -> dict:
    """outer G(j+1) pointwise 0: k=0 q=10 has n_gjp1=1."""
    r = q10["rows"]["0"]
    ok = r["n_gjp1"] == 1 and r["xor_out"] == 1
    return {"ok": ok, "k": 0, "q": 10, "n_gjp1": r["n_gjp1"]}


def killed_eq_jgtn(q10: dict) -> dict:
    """outer G(j+1) equals jgtn: k=1 q=10 is 1 vs 0."""
    r = q10["rows"]["1"]
    ok = r["xor_out"] == 1 and r["xor_jgtn"] == 0
    return {"ok": ok, "k": 1, "q": 10, "xor_out": r["xor_out"], "xor_jgtn": r["xor_jgtn"]}


def killed_eq_mv(q10: dict) -> dict:
    """outer G(j+1) equals MV inner even vanish: k=0 is 1 vs 0."""
    r = q10["rows"]["0"]
    ok = r["xor_out"] == 1 and r["xor_ine"] == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_out": r["xor_out"], "xor_ine": r["xor_ine"]}


def killed_q6_one() -> dict:
    """identically 1 on q=6: k=4 xor=0 with n_out=100."""
    w = _walk_outer_jp1(4, 6)
    ok = w.get("ok") and w["xor_out"] == 0 and w["n_out"] == 100 and w["n_gjp1"] == 36
    return {
        "ok": ok,
        "k": 4,
        "q": 6,
        "xor_out": w.get("xor_out"),
        "n_out": w.get("n_out"),
        "n_gjp1": w.get("n_gjp1"),
        "n_ok": w.get("n_ok"),
    }


def prefixes() -> dict:
    mv = json.loads(MV_JSON.read_text())
    mk = json.loads(MK_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mv["checks"]["all_ok"]
        and mk["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mv["verdict"]["inner_even_jp1"] == "LEMMA"
        and mk["verdict"]["inner0"] == "LEMMA"
        and mj["verdict"]["jgtn_even"] == "LEMMA"
        and mv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    keq: dict,
    kz: dict,
    kemp: dict,
    kpw: dict,
    kj: dict,
    kmv: dict,
    kq6: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and keq["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kpw["ok"]
        and kj["ok"]
        and kmv["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mk = json.loads(MK_JSON.read_text())
    assert q10["n_ok"] == mk["q10_inner0"]["n_ok"]
    assert q10["n_g1"] == mk["q10_inner0"]["n_g1"]
    assert want_outer_jp1(0) == 1 and want_outer_jp1(8) == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_outer_jp1()
    keq = killed_eq_rest(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    kj = killed_eq_jgtn(q10)
    kmv = killed_eq_mv(q10)
    kq6 = killed_q6_one()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, keq, kz, kemp, kpw, kj, kmv, kq6, sc, pref)
    dump = {
        "cycle": "MW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_outer_jp1": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: keq[k] for k in keq if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "killed_eq_mv": {k: kmv[k] for k in kmv if k != "ok"},
        "killed_q6_one": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "outer_jp1": True,
            "inner_even_jp1": True,
            "inner0": True,
            "jgtn_even": True,
            "rest10": True,
            "eq_rest": False,
            "outer_jp1_zero": False,
            "outer_empty": False,
            "outer_pointwise": False,
            "eq_jgtn": False,
            "eq_mv": False,
            "q6_one": False,
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
            "outer_jp1": "LEMMA",
            "inner_even_jp1": "LEMMA",
            "inner0": "LEMMA",
            "jgtn_even": "LEMMA",
            "rest10": "LEMMA",
            "eq_rest": "KILLED",
            "outer_jp1_zero": "KILLED",
            "outer_empty": "KILLED",
            "outer_pointwise": "KILLED",
            "eq_jgtn": "KILLED",
            "eq_mv": "KILLED",
            "q6_one": "KILLED",
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
        "q10_outer_jp1 n_ok",
        dump["q10_outer_jp1"]["n_ok"],
        "n_g1",
        dump["q10_outer_jp1"]["n_g1"],
        "n_out",
        dump["q10_outer_jp1"]["n_out"],
        "n_gjp1",
        dump["q10_outer_jp1"]["n_gjp1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_eq_mv", dump["killed_eq_mv"])
    print("killed_q6_one", dump["killed_q6_one"])


if __name__ == "__main__":
    main()
