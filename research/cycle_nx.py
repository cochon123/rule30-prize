#!/usr/bin/env python3
"""Cycle NX: on q=10 through k<=10, MZ inner G=1 count is odd iff k odd.

On covering J10 through k<=10, the number of covering G=1 cells
with n<j<=n+n//2 (p=T-2j>=0; no packed row) is odd iff k is odd.
Prefix Cycle MZ for k<=8; walk k=9 and k=10. Companion of Cycle
NT's inner G(j-1) xor vanish. Not a death at k=9 (par=1=want);
not a death at k=10 (par=0=want); not rest (k=1: 1 vs 0); not NT
inner xor (k=9: par=1, xor_in=0); not jgtn (k=9: par=1, jgtn=0);
not k-odd on q=6 (k=1 n_in=0); not empty (k=9 n_in=78271); not
the form for all k. Do not claim T is 1 iff k=2; do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past
k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_nx.py --certify
Dump: research/cycle_nx.json
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
from cycle_mz import want_inner_par

OUT = Path(__file__).resolve().with_suffix(".json")
MZ_JSON = Path(__file__).resolve().parent / "cycle_mz.json"
NT_JSON = Path(__file__).resolve().parent / "cycle_nt.json"
NW_JSON = Path(__file__).resolve().parent / "cycle_nw.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_in": 78271,
        "n_out": 73657,
        "xor_in": 0,
        "xor_jgtn": 0,
        "par": 1,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_in": 254236,
        "n_out": 237830,
        "xor_in": 0,
        "xor_jgtn": 1,
        "par": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    par = w["n_in"] % 2
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_in"] == want["n_in"]
        and w["n_out"] == want["n_out"]
        and w["xor_in"] == want["xor_in"] == 0
        and w["xor_jgtn"] == want["xor_jgtn"] == want_jgtn(k)
        and par == want["par"] == want_inner_par(k)
    )


def q10_inner_par_10() -> dict:
    """q=10 k<=10: prefix MZ k<=8; walk k=9,10; n_in parity is k odd."""
    mz = json.loads(MZ_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_in = 0
    for k in range(0, 9):
        r = mz["q10_inner_par"]["rows"][str(k)]
        wp = want_inner_par(k)
        if r["par"] != wp or r["xor_in"] != 0 or r["xor_jgtn"] != want_jgtn(k):
            return {"ok": False, "k": k, "q": 10, "par": r["par"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_in += r["n_in"]
        rows[str(k)] = {
            "par": r["par"],
            "xor_in": r["xor_in"],
            "xor_jgtn": r["xor_jgtn"],
            "want": wp,
            "rest": want_rest10(k, 10),
            "n_in": r["n_in"],
            "n_out": r["n_out"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "MZ",
        }
    for k in (9, 10):
        w = _walk_inner(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "par": (w.get("n_in") or 0) % 2,
                "n_ok": w.get("n_ok"),
                "n_in": w.get("n_in"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_in += w["n_in"]
        rows[str(k)] = {
            "par": w["n_in"] % 2,
            "xor_in": w["xor_in"],
            "xor_jgtn": w["xor_jgtn"],
            "want": want_inner_par(k),
            "rest": want_rest10(k, 10),
            "n_in": w["n_in"],
            "n_out": w["n_out"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["par"] == want_inner_par(k) for k in range(0, 11))
        and all(rows[str(k)]["xor_in"] == 0 for k in range(0, 11))
        and rows["0"]["n_in"] == 0
        and rows["1"]["n_in"] == 3
        and rows["1"]["par"] == 1
        and rows["8"]["n_in"] == 24038
        and rows["8"]["par"] == 0
        and rows["9"]["par"] == 1
        and rows["9"]["n_in"] == 78271
        and rows["9"]["xor_in"] == 0
        and rows["9"]["xor_jgtn"] == 0
        and rows["10"]["par"] == 0
        and rows["10"]["n_in"] == 254236
        and rows["10"]["xor_jgtn"] == 1
        and want_inner_par(9) == 1
        and want_inner_par(10) == 0
        and mz["checks"]["all_ok"]
        and mz["verdict"]["inner_par"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_in": n_in,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["par"] == 1 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "par": r["par"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["par"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "par": r["par"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["1"]
    ok = r["par"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 1, "q": 10, "par": r["par"], "rest": r["rest"]}


def killed_eq_nt(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["par"] == 1 and r["xor_in"] == 0
    return {"ok": ok, "k": 9, "q": 10, "par": r["par"], "xor_in": r["xor_in"]}


def killed_eq_jgtn(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["par"] == 1 and r["xor_jgtn"] == 0
    return {"ok": ok, "k": 9, "q": 10, "par": r["par"], "xor_jgtn": r["xor_jgtn"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_in"] == 78271
    return {"ok": ok, "k": 9, "q": 10, "n_in": r["n_in"]}


def killed_q6() -> dict:
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
    mz = json.loads(MZ_JSON.read_text())
    nt = json.loads(NT_JSON.read_text())
    nw = json.loads(NW_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        mz["checks"]["all_ok"]
        and nt["checks"]["all_ok"]
        and nw["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and mz["verdict"]["inner_par"] == "LEMMA"
        and nt["verdict"]["inner0_10"] == "LEMMA"
        and nw["verdict"]["d30_10"] == "LEMMA"
        and mz["verdict"]["prize"] == "unsolved"
        and want_inner_par(9) == 1
        and want_rest10(1, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    knt: dict,
    kj: dict,
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
        and knt["ok"]
        and kj["ok"]
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
    q10 = q10_inner_par_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    knt = killed_eq_nt(q10)
    kj = killed_eq_jgtn(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kr, knt, kj, kemp, kq6, sc, pref
    )
    dump = {
        "cycle": "NX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_inner_par_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_nt": {k: knt[k] for k in knt if k != "ok"},
        "killed_eq_jgtn": {k: kj[k] for k in kj if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "inner_par_10": True,
            "inner_par": True,
            "inner0_10": True,
            "d30_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_nt": False,
            "eq_jgtn": False,
            "inner_empty": False,
            "q6_odd": False,
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
            "inner_par_10": "LEMMA",
            "inner_par": "LEMMA",
            "inner0_10": "LEMMA",
            "d30_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_nt": "KILLED",
            "eq_jgtn": "KILLED",
            "inner_empty": "KILLED",
            "q6_odd": "KILLED",
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
        "q10_inner_par_10 n_ok",
        dump["q10_inner_par_10"]["n_ok"],
        "n_g1",
        dump["q10_inner_par_10"]["n_g1"],
        "n_in",
        dump["q10_inner_par_10"]["n_in"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_nt", dump["killed_eq_nt"])
    print("killed_eq_jgtn", dump["killed_eq_jgtn"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
