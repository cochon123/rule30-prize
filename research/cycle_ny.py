#!/usr/bin/env python3
"""Cycle NY: on q=10 through k<=10, NE high S is 1 iff k%8 in (4, 6).

On covering J10 through k<=10, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and n>=3U/2 (p=T-2j>=0; no packed
row) is 1 iff k%8 in (4, 6). Prefix Cycle NE for k<=8; walk k=9
and k=10. Companion NC n<U and ND mid still hold at those k.
Not a death at k=9 (xor=0=want); not a death at k=10 (xor=0=want);
not rest (k=4: 1 vs 0); not NC n<U (k=6: 1 vs 0); not NA S (k=4:
1 vs 0); not ND mid (k=4: 1 vs 0); not 0 (k=4: 1); not empty
(k=9 n_hi=21245); not pointwise 0 (k=9 n_hig=8898); not the form
on q=6; not the form for all k. Do not claim T is 1 iff k=2;
do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_ny.py --certify
Dump: research/cycle_ny.json
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
from cycle_nc import want_s_nltu
from cycle_nd import _walk_s_mid
from cycle_ne import want_s_hi

OUT = Path(__file__).resolve().with_suffix(".json")
NE_JSON = Path(__file__).resolve().parent / "cycle_ne.json"
NX_JSON = Path(__file__).resolve().parent / "cycle_nx.json"
ND_JSON = Path(__file__).resolve().parent / "cycle_nd.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_hi": 21245,
        "n_hig": 8898,
        "xor_hi": 0,
        "xor_mid": 0,
        "xor_nltu": 0,
        "xor_sall": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_hi": 68524,
        "n_hig": 30400,
        "xor_hi": 0,
        "xor_mid": 0,
        "xor_nltu": 0,
        "xor_sall": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_hi"] == want["n_hi"]
        and w["n_hig"] == want["n_hig"]
        and w["xor_hi"] == want["xor_hi"] == want_s_hi(k)
        and w["xor_mid"] == want["xor_mid"] == 0
        and w["xor_nltu"] == want["xor_nltu"] == want_s_nltu(k)
        and w["xor_sall"] == want["xor_sall"] == w["xor_nltu"] ^ w["xor_hi"]
    )


def q10_s_hi_10() -> dict:
    """q=10 k<=10: prefix NE k<=8; walk k=9,10; xor_hi = want_s_hi."""
    ne = json.loads(NE_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_hi = n_hig = 0
    for k in range(0, 9):
        r = ne["q10_s_hi"]["rows"][str(k)]
        wh = want_s_hi(k)
        if r["xor_hi"] != wh or r["xor_mid"] != 0:
            return {"ok": False, "k": k, "q": 10, "xor_hi": r["xor_hi"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_hi += r["n_hi"]
        n_hig += r["n_hig"]
        rows[str(k)] = {
            "xor_hi": r["xor_hi"],
            "xor_nltu": r["xor_nltu"],
            "xor_sall": r["xor_sall"],
            "xor_mid": r["xor_mid"],
            "want": wh,
            "rest": want_rest10(k, 10),
            "n_hi": r["n_hi"],
            "n_hig": r["n_hig"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "NE",
        }
    for k in (9, 10):
        w = _walk_s_mid(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_hi": w.get("xor_hi"),
                "n_ok": w.get("n_ok"),
                "n_hi": w.get("n_hi"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_hi += w["n_hi"]
        n_hig += w["n_hig"]
        rows[str(k)] = {
            "xor_hi": w["xor_hi"],
            "xor_nltu": w["xor_nltu"],
            "xor_sall": w["xor_sall"],
            "xor_mid": w["xor_mid"],
            "want": want_s_hi(k),
            "rest": want_rest10(k, 10),
            "n_hi": w["n_hi"],
            "n_hig": w["n_hig"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_hi"] == want_s_hi(k) for k in range(0, 11))
        and rows["2"]["n_hi"] == 4
        and rows["2"]["n_hig"] == 2
        and rows["4"]["xor_hi"] == 1
        and rows["4"]["n_hi"] == 48
        and rows["6"]["xor_hi"] == 1
        and rows["8"]["n_hi"] == 6284
        and rows["8"]["xor_hi"] == 0
        and rows["9"]["xor_hi"] == 0
        and rows["9"]["n_hi"] == 21245
        and rows["9"]["n_hig"] == 8898
        and rows["9"]["xor_mid"] == 0
        and rows["10"]["xor_hi"] == 0
        and rows["10"]["n_hi"] == 68524
        and rows["10"]["n_hig"] == 30400
        and want_s_hi(9) == 0
        and want_s_hi(10) == 0
        and want_s_nltu(9) == 0
        and ne["checks"]["all_ok"]
        and ne["verdict"]["s_hi"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_hi": n_hi,
        "n_hig": n_hig,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_hi"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_hi": r["xor_hi"]}


def killed_die_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_hi"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_hi": r["xor_hi"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"], "rest": r["rest"]}


def killed_eq_nltu(q10: dict) -> dict:
    r = q10["rows"]["6"]
    ok = r["xor_hi"] == 1 and r["xor_nltu"] == 0
    return {"ok": ok, "k": 6, "q": 10, "xor_hi": r["xor_hi"], "xor_nltu": r["xor_nltu"]}


def killed_eq_s(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1 and r["xor_sall"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"], "xor_sall": r["xor_sall"]}


def killed_eq_mid(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1 and r["xor_mid"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"], "xor_mid": r["xor_mid"]}


def killed_zero(q10: dict) -> dict:
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_hi"] == 21245
    return {"ok": ok, "k": 9, "q": 10, "n_hi": r["n_hi"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_hig"] == 8898 and r["xor_hi"] == 0
    return {"ok": ok, "k": 9, "q": 10, "n_hig": r["n_hig"]}


def killed_q6() -> dict:
    w = _walk_s_mid(3, 6)
    ok = w.get("ok") and w["xor_hi"] == 1 and want_s_hi(3) == 0 and w["n_hi"] == 1
    return {
        "ok": ok,
        "k": 3,
        "q": 6,
        "xor_hi": w.get("xor_hi"),
        "want": want_s_hi(3),
        "n_hi": w.get("n_hi"),
    }


def prefixes() -> dict:
    ne = json.loads(NE_JSON.read_text())
    nx = json.loads(NX_JSON.read_text())
    nd = json.loads(ND_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        ne["checks"]["all_ok"]
        and nx["checks"]["all_ok"]
        and nd["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and ne["verdict"]["s_hi"] == "LEMMA"
        and nx["verdict"]["inner_par_10"] == "LEMMA"
        and nd["verdict"]["s_mid"] == "LEMMA"
        and ne["verdict"]["prize"] == "unsolved"
        and want_s_hi(10) == 0
        and want_s_nltu(4) == 1
        and want_rest10(4, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kr: dict,
    kn: dict,
    ks: dict,
    km: dict,
    kz: dict,
    kemp: dict,
    kpw: dict,
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
        and kn["ok"]
        and ks["ok"]
        and km["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kpw["ok"]
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
    q10 = q10_s_hi_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kr = killed_eq_rest(q10)
    kn = killed_eq_nltu(q10)
    ks = killed_eq_s(q10)
    km = killed_eq_mid(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kr, kn, ks, km, kz, kemp, kpw, kq6, sc, pref
    )
    dump = {
        "cycle": "NY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_hi_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_nltu": {k: kn[k] for k in kn if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_mid": {k: km[k] for k in km if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_hi_10": True,
            "s_hi": True,
            "s_mid": True,
            "inner_par_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_rest": False,
            "eq_nltu": False,
            "eq_s": False,
            "eq_mid": False,
            "s_hi_zero": False,
            "nhi_empty": False,
            "nhi_pointwise": False,
            "q6_hi": False,
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
            "s_hi_10": "LEMMA",
            "s_hi": "LEMMA",
            "s_mid": "LEMMA",
            "inner_par_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_nltu": "KILLED",
            "eq_s": "KILLED",
            "eq_mid": "KILLED",
            "s_hi_zero": "KILLED",
            "nhi_empty": "KILLED",
            "nhi_pointwise": "KILLED",
            "q6_hi": "KILLED",
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
        "q10_s_hi_10 n_ok",
        dump["q10_s_hi_10"]["n_ok"],
        "n_g1",
        dump["q10_s_hi_10"]["n_g1"],
        "n_hi",
        dump["q10_s_hi_10"]["n_hi"],
        "n_hig",
        dump["q10_s_hi_10"]["n_hig"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_nltu", dump["killed_eq_nltu"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_mid", dump["killed_eq_mid"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
