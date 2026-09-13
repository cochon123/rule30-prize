#!/usr/bin/env python3
"""Cycle OE: on q=10, NJ n>=7U/2 S form dies at k=9.

On covering J10, Cycle NJ's XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and n>=7U/2 (p=T-2j>=0; no packed
row) is 1 iff k%8 in (5, 6) for k<=8, but at k=9 xor=1 while
want=0. Also dies at k=10 (xor=1, want=0). Prefix NJ for k<=8;
walk k=9 and k=10. Companion NY high S and OD 2U-3U death still
hold at those k. Not empty (k=9 n_hi72=3235); not pointwise 0
(k=9 n_hi72g=1211); not NY high (k=5: 1 vs 0); not NH 2U-3U
(k=6: 1 vs 0); not NI 2U-5U/2 (k=5: 1 vs 0); not rest (k=5:
1 vs 0); not NA S (k=5: 1 vs 0); not the form through k<=10;
not the form for all k. Do not claim T is 1 iff k=2; do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_oe.py --certify
Dump: research/cycle_oe.json
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
from cycle_nj import _walk_s_hi72, want_s_hi72

OUT = Path(__file__).resolve().with_suffix(".json")
NJ_JSON = Path(__file__).resolve().parent / "cycle_nj.json"
OD_JSON = Path(__file__).resolve().parent / "cycle_od.json"
MJ_JSON = Path(__file__).resolve().parent / "cycle_mj.json"

WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_hi72": 3235,
        "n_hi72g": 1211,
        "n_23": 11387,
        "xor_hi72": 1,
        "xor_hi": 0,
        "xor_23": 1,
        "xor_lo": 0,
        "xor_sall": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_hi72": 9688,
        "n_hi72g": 4639,
        "n_23": 35196,
        "xor_hi72": 1,
        "xor_hi": 0,
        "xor_23": 1,
        "xor_lo": 1,
        "xor_sall": 0,
    },
}


def _row_ok10(k: int, w: dict) -> bool:
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_hi72"] == want["n_hi72"]
        and w["n_hi72g"] == want["n_hi72g"]
        and w["n_23"] == want["n_23"]
        and w["xor_hi72"] == want["xor_hi72"] == 1
        and w["xor_hi72"] != want_s_hi72(k)
        and w["xor_hi"] == want["xor_hi"] == want_s_hi(k)
        and w["xor_23"] == want["xor_23"] != want_s_2u3u(k)
        and w["xor_lo"] == want["xor_lo"] == want_s_2u25(k)
        and w["xor_sall"] == want["xor_sall"]
    )


def q10_s_hi72_die() -> dict:
    """q=10: prefix NJ k<=8 holds; k=9,10 xor_hi72=1 != want."""
    nj = json.loads(NJ_JSON.read_text())
    rows = {}
    n_ok = n_g1 = n_hi72 = n_hi72g = 0
    for k in range(0, 9):
        r = nj["q10_s_hi72"]["rows"][str(k)]
        wh = want_s_hi72(k)
        if r["xor_hi72"] != wh:
            return {"ok": False, "k": k, "q": 10, "xor_hi72": r["xor_hi72"]}
        n_ok += r["n_ok"]
        n_g1 += r["n_g1"]
        n_hi72 += r["n_hi72"]
        n_hi72g += r["n_hi72g"]
        rows[str(k)] = {
            "xor_hi72": r["xor_hi72"],
            "xor_hi": r["xor_hi"],
            "xor_23": r["xor_23"],
            "xor_lo": r["xor_lo"],
            "xor_sall": r["xor_sall"],
            "want": wh,
            "rest": want_rest10(k, 10),
            "n_hi72": r["n_hi72"],
            "n_hi72g": r["n_hi72g"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "NJ",
        }
    for k in (9, 10):
        w = _walk_s_hi72(k, 10)
        if not _row_ok10(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_hi72": w.get("xor_hi72"),
                "n_ok": w.get("n_ok"),
                "n_hi72": w.get("n_hi72"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_hi72 += w["n_hi72"]
        n_hi72g += w["n_hi72g"]
        rows[str(k)] = {
            "xor_hi72": w["xor_hi72"],
            "xor_hi": w["xor_hi"],
            "xor_23": w["xor_23"],
            "xor_lo": w["xor_lo"],
            "xor_sall": w["xor_sall"],
            "want": want_s_hi72(k),
            "rest": want_rest10(k, 10),
            "n_hi72": w["n_hi72"],
            "n_hi72g": w["n_hi72g"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_hi72"] == want_s_hi72(k) for k in range(0, 9))
        and rows["3"]["n_hi72"] == 3
        and rows["5"]["xor_hi72"] == 1
        and rows["5"]["xor_hi"] == 0
        and rows["5"]["rest"] == 0
        and rows["6"]["xor_hi72"] == 1
        and rows["6"]["xor_23"] == 0
        and rows["8"]["n_hi72"] == 874
        and rows["8"]["xor_hi72"] == 0
        and rows["9"]["xor_hi72"] == 1
        and rows["9"]["want"] == 0
        and rows["9"]["n_hi72"] == 3235
        and rows["9"]["n_hi72g"] == 1211
        and rows["9"]["xor_23"] == 1
        and rows["10"]["xor_hi72"] == 1
        and rows["10"]["want"] == 0
        and rows["10"]["n_hi72"] == 9688
        and rows["10"]["n_hi72g"] == 4639
        and want_s_hi72(9) == 0
        and want_s_hi72(10) == 0
        and want_s_hi72(5) == 1
        and want_s_hi72(8) == 0
        and nj["checks"]["all_ok"]
        and nj["verdict"]["s_hi72"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_hi72": n_hi72,
        "n_hi72g": n_hi72g,
        "rows": rows,
    }


def killed_holds_k9(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["xor_hi72"] == 1 and r["want"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_hi72": r["xor_hi72"], "want": r["want"]}


def killed_holds_k10(q10: dict) -> dict:
    r = q10["rows"]["10"]
    ok = r["xor_hi72"] == 1 and r["want"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_hi72": r["xor_hi72"], "want": r["want"]}


def killed_eq_hi(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["xor_hi"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "xor_hi": r["xor_hi"]}


def killed_eq_23(q10: dict) -> dict:
    r = q10["rows"]["6"]
    ok = r["xor_hi72"] == 1 and r["xor_23"] == 0
    return {"ok": ok, "k": 6, "q": 10, "xor_hi72": r["xor_hi72"], "xor_23": r["xor_23"]}


def killed_eq_lo(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["xor_lo"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "xor_lo": r["xor_lo"]}


def killed_eq_s(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["xor_sall"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "xor_sall": r["xor_sall"]}


def killed_eq_rest(q10: dict) -> dict:
    r = q10["rows"]["5"]
    ok = r["xor_hi72"] == 1 and r["rest"] == 0
    return {"ok": ok, "k": 5, "q": 10, "xor_hi72": r["xor_hi72"], "rest": r["rest"]}


def killed_empty(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_hi72"] == 3235
    return {"ok": ok, "k": 9, "q": 10, "n_hi72": r["n_hi72"]}


def killed_pointwise(q10: dict) -> dict:
    r = q10["rows"]["9"]
    ok = r["n_hi72g"] == 1211 and r["xor_hi72"] == 1
    return {"ok": ok, "k": 9, "q": 10, "n_hi72g": r["n_hi72g"]}


def prefixes() -> dict:
    nj = json.loads(NJ_JSON.read_text())
    od = json.loads(OD_JSON.read_text())
    mj = json.loads(MJ_JSON.read_text())
    ok = (
        nj["checks"]["all_ok"]
        and od["checks"]["all_ok"]
        and mj["checks"]["all_ok"]
        and nj["verdict"]["s_hi72"] == "LEMMA"
        and od["verdict"]["s_2u3u_dies_k9"] == "LEMMA"
        and nj["verdict"]["prize"] == "unsolved"
        and want_s_hi72(5) == 1
        and want_s_hi72(9) == 0
        and want_s_hi(5) == 0
        and want_s_2u3u(6) == 0
        and want_rest10(5, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kh9: dict,
    kh10: dict,
    khi: dict,
    k23: dict,
    klo: dict,
    ks: dict,
    kr: dict,
    kemp: dict,
    kpw: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        q10["ok"]
        and kh9["ok"]
        and kh10["ok"]
        and khi["ok"]
        and k23["ok"]
        and klo["ok"]
        and ks["ok"]
        and kr["ok"]
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
    q10 = q10_s_hi72_die()
    kh9 = killed_holds_k9(q10)
    kh10 = killed_holds_k10(q10)
    khi = killed_eq_hi(q10)
    k23 = killed_eq_23(q10)
    klo = killed_eq_lo(q10)
    ks = killed_eq_s(q10)
    kr = killed_eq_rest(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kh9, kh10, khi, k23, klo, ks, kr, kemp, kpw, sc, pref
    )
    dump = {
        "cycle": "OE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_hi72_die": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_holds_k9": {k: kh9[k] for k in kh9 if k != "ok"},
        "killed_holds_k10": {k: kh10[k] for k in kh10 if k != "ok"},
        "killed_eq_hi": {k: khi[k] for k in khi if k != "ok"},
        "killed_eq_23": {k: k23[k] for k in k23 if k != "ok"},
        "killed_eq_lo": {k: klo[k] for k in klo if k != "ok"},
        "killed_eq_s": {k: ks[k] for k in ks if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "lemmas": {
            "s_hi72_dies_k9": True,
            "s_hi72_dies_k10": True,
            "s_hi72": True,
            "s_2u3u_dies_k9": True,
            "s_hi72_10": False,
            "holds_k9": False,
            "holds_k10": False,
            "eq_hi": False,
            "eq_23": False,
            "eq_lo": False,
            "eq_s": False,
            "eq_rest": False,
            "nhi72_empty": False,
            "nhi72_pointwise": False,
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
            "s_hi72_dies_k9": "LEMMA",
            "s_hi72_dies_k10": "LEMMA",
            "s_hi72": "LEMMA",
            "s_2u3u_dies_k9": "LEMMA",
            "s_hi72_10": "KILLED",
            "holds_k9": "KILLED",
            "holds_k10": "KILLED",
            "eq_hi": "KILLED",
            "eq_23": "KILLED",
            "eq_lo": "KILLED",
            "eq_s": "KILLED",
            "eq_rest": "KILLED",
            "nhi72_empty": "KILLED",
            "nhi72_pointwise": "KILLED",
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
        "q10_s_hi72_die n_ok",
        dump["q10_s_hi72_die"]["n_ok"],
        "n_g1",
        dump["q10_s_hi72_die"]["n_g1"],
        "n_hi72",
        dump["q10_s_hi72_die"]["n_hi72"],
        "n_hi72g",
        dump["q10_s_hi72_die"]["n_hi72g"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_holds_k9", dump["killed_holds_k9"])
    print("killed_holds_k10", dump["killed_holds_k10"])
    print("killed_eq_hi", dump["killed_eq_hi"])
    print("killed_eq_23", dump["killed_eq_23"])
    print("killed_eq_lo", dump["killed_eq_lo"])
    print("killed_eq_s", dump["killed_eq_s"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])


if __name__ == "__main__":
    main()
