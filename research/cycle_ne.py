#!/usr/bin/env python3
"""Cycle NE: on q=10 for k<=8, NA's S on n>=3U/2 is 1 iff k%8 in (4, 6).

On covering J10 for k<=8, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and n>=3U/2 (p=T-2j>=0; no packed
row) is 1 iff k%8 in (4, 6). Companion of Cycle NC's n<U form:
Cycle ND's mid-band vanish leaves this high slice. Not rest (k=4:
xor=1, rest=0); not NC n<U (k=6: 1 vs 0); not NA S (k=4: 1 vs 0);
not ND mid (k=4: 1 vs 0); not 0; not empty (k=2 n_hi=4); not the
form on q=6 (k=3 xor=1, want=0); not Green-only rest; not the form
for all k. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_ne.py --certify
Dump: research/cycle_ne.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
ND_JSON = Path(__file__).resolve().parent / "cycle_nd.json"
NC_JSON = Path(__file__).resolve().parent / "cycle_nc.json"
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"


def want_s_hi(k: int) -> int:
    """S on n>=3U/2 on q=10 k<=8: 1 iff k%8 in (4, 6)."""
    return int(k % 8 in (4, 6))


def q10_s_hi() -> dict:
    """k<=8 q=10: S on n>=3U/2 is 1 iff k%8 in (4, 6)."""
    n_ok = n_g1 = n_hi = n_hig = 0
    rows = {}
    nd = json.loads(ND_JSON.read_text())
    nc = json.loads(NC_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    for k in range(0, 9):
        w = _walk_s_mid(k, 10)
        wh = want_s_hi(k)
        nd_row = nd["bothq_s_mid"]["rows"][str(k)]["j10"]
        nc_row = nc["bothq_s_nltu"]["rows"][str(k)]["j10"]
        na_row = na["q10_green_rest"]["rows"][str(k)]
        mj_row = mj["bothq_jgtn"]["rows"][str(k)]["j10"]
        if (
            not w.get("ok")
            or w["xor_hi"] != wh
            or w["xor_mid"] != 0
            or w["xor_nltu"] != want_s_nltu(k)
            or w["xor_nltu"] != nc_row["xor"]
            or w["xor_sall"] != na_row["xor_s"]
            or w["xor_sall"] != w["xor_nltu"] ^ w["xor_hi"]
            or w["xor_hi"] != nd_row["xor_hi"]
            or w["n_hi"] != nd_row["n_hi"]
            or w["n_ok"] != mj_row["n_ok"]
            or w["n_g1"] != mj_row["n_g1"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_hi": w.get("xor_hi"),
                "want": wh,
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
            "want": wh,
            "rest": want_rest10(k, 10),
            "n_hi": w["n_hi"],
            "n_hig": w["n_hig"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        all(rows[str(k)]["xor_hi"] == want_s_hi(k) for k in range(0, 9))
        and rows["4"]["xor_hi"] == 1
        and rows["6"]["xor_hi"] == 1
        and rows["8"]["xor_hi"] == 0
        and rows["4"]["n_hi"] == 48
        and rows["4"]["n_hig"] == 21
        and rows["6"]["n_hi"] == 560
        and rows["2"]["n_hi"] == 4
        and want_s_hi(4) == 1
        and want_s_nltu(4) == 1
        and want_s_hi(8) == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_hi": n_hi,
        "n_hig": n_hig,
        "rows": rows,
    }


def killed_eq_rest(q10: dict) -> dict:
    """high S equals rest: k=4 is 1 vs 0."""
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"], "rest": r["rest"]}


def killed_eq_nltu(q10: dict) -> dict:
    """high S equals NC n<U: k=6 is 1 vs 0."""
    r = q10["rows"]["6"]
    ok = r["xor_hi"] == 1 and r["xor_nltu"] == 0
    return {"ok": ok, "k": 6, "q": 10, "xor_hi": r["xor_hi"], "xor_nltu": r["xor_nltu"]}


def killed_eq_s(q10: dict) -> dict:
    """high S equals NA S: k=4 is 1 vs 0."""
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1 and r["xor_sall"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"], "xor_sall": r["xor_sall"]}


def killed_eq_mid(q10: dict) -> dict:
    """high S equals ND mid: k=4 is 1 vs 0."""
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1 and r["xor_mid"] == 0
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"], "xor_mid": r["xor_mid"]}


def killed_zero(q10: dict) -> dict:
    """high S vanishes: k=4 is 1."""
    r = q10["rows"]["4"]
    ok = r["xor_hi"] == 1
    return {"ok": ok, "k": 4, "q": 10, "xor_hi": r["xor_hi"]}


def killed_empty(q10: dict) -> dict:
    """high S empty: k=2 has n_hi=4."""
    r = q10["rows"]["2"]
    ok = r["n_hi"] == 4 and r["n_hig"] == 2
    return {"ok": ok, "k": 2, "q": 10, "n_hi": r["n_hi"]}


def killed_q6() -> dict:
    """high S form on q=6: k=3 xor=1 but want=0."""
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
    nd = json.loads(ND_JSON.read_text())
    nc = json.loads(NC_JSON.read_text())
    na = json.loads(NA_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nd["checks"]["all_ok"]
        and nc["checks"]["all_ok"]
        and na["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nd["verdict"]["s_mid"] == "LEMMA"
        and nc["verdict"]["s_nltu"] == "LEMMA"
        and na["verdict"]["green_rest"] == "LEMMA"
        and nd["verdict"]["prize"] == "unsolved"
        and want_s_hi(4) == 1
        and want_s_hi(6) == 1
        and want_s_hi(8) == 0
        and want_s_nltu(4) == 1
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kr: dict,
    kn: dict,
    ks: dict,
    km: dict,
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
        and kr["ok"]
        and kn["ok"]
        and ks["ok"]
        and km["ok"]
        and kz["ok"]
        and kemp["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    mj = json.loads(MJ_JSON.read_text())
    j10_ok = sum(mj["bothq_jgtn"]["rows"][str(k)]["j10"]["n_ok"] for k in range(0, 9))
    assert q10["n_ok"] == j10_ok
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_s_hi()
    kr = killed_eq_rest(q10)
    kn = killed_eq_nltu(q10)
    ks = killed_eq_s(q10)
    km = killed_eq_mid(q10)
    kz = killed_zero(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kr, kn, ks, km, kz, kemp, kq6, sc, pref)
    dump = {
        "cycle": "NE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_hi": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_nltu": {k: kn[k] for k in kn if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_mid": {k: km[k] for k in km if k != "ok"},
        "killed_zero": {k: kz[k] for k in kz if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_hi": True,
            "s_mid": True,
            "s_nltu": True,
            "green_rest": True,
            "eq_rest": False,
            "eq_nltu": False,
            "eq_s": False,
            "eq_mid": False,
            "s_hi_zero": False,
            "nhi_empty": False,
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
            "s_hi": "LEMMA",
            "s_mid": "LEMMA",
            "s_nltu": "LEMMA",
            "green_rest": "LEMMA",
            "eq_rest": "KILLED",
            "eq_nltu": "KILLED",
            "eq_s": "KILLED",
            "eq_mid": "KILLED",
            "s_hi_zero": "KILLED",
            "nhi_empty": "KILLED",
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
        "q10_s_hi n_ok",
        dump["q10_s_hi"]["n_ok"],
        "n_g1",
        dump["q10_s_hi"]["n_g1"],
        "n_hi",
        dump["q10_s_hi"]["n_hi"],
        "n_hig",
        dump["q10_s_hi"]["n_hig"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_nltu", dump["killed_eq_nltu"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_mid", dump["killed_eq_mid"])
    print("killed_zero", dump["killed_zero"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
