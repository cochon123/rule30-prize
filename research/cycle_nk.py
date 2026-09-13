#!/usr/bin/env python3
"""Cycle NK: on q=10 through k<=10, NI S on 2U<=n<5U/2 is 1 iff k%4 in (2, 3).

On covering J10 through k<=10, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and 2U<=n<5U/2 (p=T-2j>=0; no packed
row) is 1 iff k%4 in (2, 3). Prefix Cycle NI for k<=8; walk k=9
and k=10 via Cycle NJ's hi72 walk. Not a death at k=9 (xor=0=want);
not a death at k=10 (xor=1=want); not NH through k<=10 (dies at
k=9); not NJ through k<=10 (dies at k=9); not rest (k=10: 1 vs 0);
not NE high (k=10: 1 vs 0); not empty (k=9 n_lo=4372); not the
form on q=6; not the form for all k. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_nk.py --certify
Dump: research/cycle_nk.json
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
from cycle_ne import want_s_hi
from cycle_nh import want_s_2u3u
from cycle_ni import want_s_2u25
from cycle_nj import want_s_hi72, _walk_s_hi72

OUT = Path(__file__).resolve().with_suffix(".json")
NI_JSON = Path(__file__).resolve().parent / "cycle_ni.json"
NJ_JSON = Path(__file__).resolve().parent / "cycle_nj.json"
NH_JSON = Path(__file__).resolve().parent / "cycle_nh.json"
NE_JSON = Path(__file__).resolve().parent / "cycle_ne.json"

# Probe-checked k=9,10 q=10 hi72 walk sizes (~6-9s expected).
WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_lo": 4372,
        "n_23": 11387,
        "n_hi72": 3235,
        "n_hi72g": 1211,
        "xor_lo": 0,
        "xor_23": 1,
        "xor_hi72": 1,
        "xor_hi": 0,
        "xor_sall": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_lo": 13951,
        "n_23": 35196,
        "n_hi72": 9688,
        "n_hi72g": 4639,
        "xor_lo": 1,
        "xor_23": 1,
        "xor_hi72": 1,
        "xor_hi": 0,
        "xor_sall": 0,
    },
}


def _row_ok(k: int, w: dict) -> bool:
    """True if walk sizes match the probe and xor_lo equals want_s_2u25."""
    want = WANT_WALK[k]
    wr = want_s_2u25(k)
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_lo"] == want["n_lo"]
        and w["n_23"] == want["n_23"]
        and w["n_hi72"] == want["n_hi72"]
        and w["n_hi72g"] == want["n_hi72g"]
        and w["xor_lo"] == want["xor_lo"] == wr
        and w["xor_23"] == want["xor_23"]
        and w["xor_hi72"] == want["xor_hi72"]
        and w["xor_hi"] == want["xor_hi"] == want_s_hi(k)
        and w["xor_sall"] == want["xor_sall"]
    )


def q10_s_2u25_10() -> dict:
    """q=10 k<=10: prefix NI k<=8; walk k=9,10; xor_lo equals want_s_2u25."""
    ni = json.loads(NI_JSON.read_text())
    rows = {}
    for k in range(0, 9):
        r = ni["q10_s_2u25"]["rows"][str(k)]
        wr = want_s_2u25(k)
        if r["xor_lo"] != wr or r["xor_lo"] != r["want"]:
            return {"ok": False, "k": k, "q": 10, "xor_lo": r["xor_lo"], "wr": wr}
        rows[str(k)] = {
            "xor_lo": r["xor_lo"],
            "xor_23": r["xor_23"],
            "xor_hi": r["xor_hi"],
            "xor_sall": r["xor_sall"],
            "want": wr,
            "rest": want_rest10(k, 10),
            "n_lo": r["n_lo"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "NI",
        }
    n_ok = n_g1 = n_lo = n_23 = n_hi72 = n_hi72g = 0
    for k in (9, 10):
        w = _walk_s_hi72(k, 10)
        if not _row_ok(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_lo": w.get("xor_lo"),
                "wr": want_s_2u25(k),
                "n_ok": w.get("n_ok"),
                "n_g1": w.get("n_g1"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo += w["n_lo"]
        n_23 += w["n_23"]
        n_hi72 += w["n_hi72"]
        n_hi72g += w["n_hi72g"]
        rows[str(k)] = {
            "xor_lo": w["xor_lo"],
            "xor_23": w["xor_23"],
            "xor_hi72": w["xor_hi72"],
            "xor_hi": w["xor_hi"],
            "xor_sall": w["xor_sall"],
            "want": want_s_2u25(k),
            "rest": want_rest10(k, 10),
            "n_lo": w["n_lo"],
            "n_23": w["n_23"],
            "n_hi72": w["n_hi72"],
            "n_hi72g": w["n_hi72g"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_lo"] == want_s_2u25(k) for k in range(0, 11))
        and rows["8"]["xor_lo"] == 0
        and rows["9"]["xor_lo"] == 0
        and rows["10"]["xor_lo"] == 1
        and rows["9"]["n_lo"] == 4372
        and rows["10"]["n_lo"] == 13951
        and rows["9"]["xor_23"] == 1
        and rows["9"]["xor_hi72"] == 1
        and want_s_2u25(9) == 0
        and want_s_2u25(10) == 1
        and want_s_2u3u(9) == 0
        and want_s_hi72(9) == 0
        and want_s_hi(9) == 0
        and want_s_hi(10) == 0
        and ni["checks"]["all_ok"]
        and ni["verdict"]["s_2u25"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo": n_lo,
        "n_23": n_23,
        "n_hi72": n_hi72,
        "n_hi72g": n_hi72g,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    """NI form dies at k=9: xor_lo=0 equals want."""
    r = q10["rows"]["9"]
    ok = r["xor_lo"] == 0 and r["want"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_lo": r["xor_lo"], "want": r["want"]}


def killed_die_k10(q10: dict) -> dict:
    """NI form dies at k=10: xor_lo=1 equals want."""
    r = q10["rows"]["10"]
    ok = r["xor_lo"] == 1 and r["want"] == 1 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_lo": r["xor_lo"], "want": r["want"]}


def killed_nh_k9(q10: dict) -> dict:
    """NH 2U-3U form through k<=10: k=9 xor_23=1 want=0."""
    r = q10["rows"]["9"]
    ok = r["xor_23"] == 1 and want_s_2u3u(9) == 0 and r["n_23"] == 11387
    return {
        "ok": ok,
        "k": 9,
        "q": 10,
        "xor_23": r["xor_23"],
        "want": want_s_2u3u(9),
        "n_23": r["n_23"],
    }


def killed_nj_k9(q10: dict) -> dict:
    """NJ n>=7U/2 form through k<=10: k=9 xor_hi72=1 want=0."""
    r = q10["rows"]["9"]
    ok = r["xor_hi72"] == 1 and want_s_hi72(9) == 0 and r["n_hi72"] == 3235
    return {
        "ok": ok,
        "k": 9,
        "q": 10,
        "xor_hi72": r["xor_hi72"],
        "want": want_s_hi72(9),
        "n_hi72": r["n_hi72"],
    }


def killed_eq_rest(q10: dict) -> dict:
    """NI through k<=10 equals rest: k=10 is 1 vs 0."""
    r = q10["rows"]["10"]
    ok = r["xor_lo"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 10, "q": 10, "xor_lo": r["xor_lo"], "rest": r["rest"]}


def killed_eq_hi(q10: dict) -> dict:
    """NI through k<=10 equals NE high: k=10 is 1 vs 0."""
    r = q10["rows"]["10"]
    ok = r["xor_lo"] == 1 and r["xor_hi"] == 0
    return {"ok": ok, "k": 10, "q": 10, "xor_lo": r["xor_lo"], "xor_hi": r["xor_hi"]}


def killed_empty(q10: dict) -> dict:
    """k=9 2U-5U/2 S-slice empty: n_lo=4372."""
    r = q10["rows"]["9"]
    ok = r["n_lo"] == 4372
    return {"ok": ok, "k": 9, "q": 10, "n_lo": r["n_lo"]}


def killed_q6() -> dict:
    """NI form on q=6: prefix NI k=2 empty, xor=0 want=1."""
    ni = json.loads(NI_JSON.read_text())
    kq = ni["killed_q6"]
    ok = kq["xor_lo"] == 0 and kq["want"] == 1 and kq["n_lo"] == 0
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "xor_lo": kq["xor_lo"],
        "want": kq["want"],
        "n_lo": kq["n_lo"],
    }


def prefixes() -> dict:
    ni = json.loads(NI_JSON.read_text())
    nj = json.loads(NJ_JSON.read_text())
    nh = json.loads(NH_JSON.read_text())
    ne = json.loads(NE_JSON.read_text())
    ok = (
        ni["checks"]["all_ok"]
        and nj["checks"]["all_ok"]
        and nh["checks"]["all_ok"]
        and ne["checks"]["all_ok"]
        and ni["verdict"]["s_2u25"] == "LEMMA"
        and nj["verdict"]["s_hi72"] == "LEMMA"
        and nh["verdict"]["s_2u3u"] == "LEMMA"
        and ne["verdict"]["s_hi"] == "LEMMA"
        and ni["verdict"]["prize"] == "unsolved"
        and want_s_2u25(10) == 1
        and want_s_2u25(9) == 0
        and want_s_2u3u(9) == 0
        and want_s_hi72(9) == 0
        and want_s_hi(10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    knh: dict,
    knj: dict,
    kr: dict,
    kh: dict,
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
        and knh["ok"]
        and knj["ok"]
        and kr["ok"]
        and kh["ok"]
        and kemp["ok"]
        and kq6["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert q10["n_ok"] == WANT_WALK[9]["n_ok"] + WANT_WALK[10]["n_ok"]
    assert q10["n_g1"] == WANT_WALK[9]["n_g1"] + WANT_WALK[10]["n_g1"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_s_2u25_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    knh = killed_nh_k9(q10)
    knj = killed_nj_k9(q10)
    kr = killed_eq_rest(q10)
    kh = killed_eq_hi(q10)
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, knh, knj, kr, kh, kemp, kq6, sc, pref
    )
    dump = {
        "cycle": "NK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_2u25_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_nh_k9": {k: knh[k] for k in knh if k != "ok"},
        "killed_nj_k9": {k: knj[k] for k in knj if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_eq_hi": {k: kh[k] for k in kh if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_2u25_10": True,
            "s_2u25": True,
            "s_2u3u": True,
            "s_hi72": True,
            "s_hi": True,
            "dies_k9": False,
            "dies_k10": False,
            "nh_k10": False,
            "nj_k10": False,
            "eq_rest": False,
            "eq_hi": False,
            "nlo_empty": False,
            "q6_form": False,
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
            "s_2u25_10": "LEMMA",
            "s_2u25": "LEMMA",
            "s_2u3u": "LEMMA",
            "s_hi72": "LEMMA",
            "s_hi": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "nh_k10": "KILLED",
            "nj_k10": "KILLED",
            "eq_rest": "KILLED",
            "eq_hi": "KILLED",
            "nlo_empty": "KILLED",
            "q6_form": "KILLED",
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
        "q10_s_2u25_10 n_ok",
        dump["q10_s_2u25_10"]["n_ok"],
        "n_g1",
        dump["q10_s_2u25_10"]["n_g1"],
        "n_lo",
        dump["q10_s_2u25_10"]["n_lo"],
        "n_23",
        dump["q10_s_2u25_10"]["n_23"],
        "n_hi72",
        dump["q10_s_2u25_10"]["n_hi72"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_nh_k9", dump["killed_nh_k9"])
    print("killed_nj_k9", dump["killed_nj_k9"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
