#!/usr/bin/env python3
"""Cycle NM: on q=10 through k<=10, NL S on 2U<=n<9U/4 vanishes.

On covering J10 through k<=10, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0 and 2U<=n<9U/4 (p=T-2j>=0; no packed
row) is 0. Prefix Cycle NL for k<=8; walk k=9 and k=10. Not a
death at k=9 (xor=0); not a death at k=10 (xor=0); not NI through
k<=10 (k=10: 0 vs 1); not rest (k=2: 0 vs 1); not empty (k=9
n_lo9=1389); not pointwise 0 (k=9 n_lo9g=560); not the form on
q=6; not the form for all k. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_nm.py --certify
Dump: research/cycle_nm.json
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
from cycle_ni import want_s_2u25
from cycle_nl import _walk_s_2u94

OUT = Path(__file__).resolve().with_suffix(".json")
NL_JSON = Path(__file__).resolve().parent / "cycle_nl.json"
NK_JSON = Path(__file__).resolve().parent / "cycle_nk.json"
NI_JSON = Path(__file__).resolve().parent / "cycle_ni.json"

# Probe-checked k=9,10 q=10 lo9 walk sizes (~8.9s expected).
WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_lo9": 1389,
        "n_lo9g": 560,
        "n_lo": 4372,
        "n_up": 2983,
        "xor_lo9": 0,
        "xor_up": 0,
        "xor_lo": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_lo9": 4203,
        "n_lo9g": 2032,
        "n_lo": 13951,
        "n_up": 9748,
        "xor_lo9": 0,
        "xor_up": 1,
        "xor_lo": 1,
    },
}


def _row_ok(k: int, w: dict) -> bool:
    """True if walk sizes match the probe and xor_lo9 vanishes."""
    want = WANT_WALK[k]
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_lo9"] == want["n_lo9"]
        and w["n_lo9g"] == want["n_lo9g"]
        and w["n_lo"] == want["n_lo"]
        and w["n_up"] == want["n_up"]
        and w["xor_lo9"] == want["xor_lo9"] == 0
        and w["xor_up"] == want["xor_up"]
        and w["xor_lo"] == want["xor_lo"] == want_s_2u25(k)
        and w["xor_lo9"] ^ w["xor_up"] == w["xor_lo"]
    )


def q10_s_2u94_10() -> dict:
    """q=10 k<=10: prefix NL k<=8; walk k=9,10; xor_lo9 vanishes."""
    nl = json.loads(NL_JSON.read_text())
    rows = {}
    for k in range(0, 9):
        r = nl["q10_s_2u94"]["rows"][str(k)]
        if r["xor_lo9"] != 0 or r["xor_lo"] != want_s_2u25(k):
            return {"ok": False, "k": k, "q": 10, "xor_lo9": r["xor_lo9"]}
        rows[str(k)] = {
            "xor_lo9": r["xor_lo9"],
            "xor_up": r["xor_up"],
            "xor_lo": r["xor_lo"],
            "rest": want_rest10(k, 10),
            "n_lo9": r["n_lo9"],
            "n_lo9g": r["n_lo9g"],
            "n_lo": r["n_lo"],
            "n_up": r["n_up"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "NL",
        }
    n_ok = n_g1 = n_lo9 = n_lo9g = 0
    for k in (9, 10):
        w = _walk_s_2u94(k, 10)
        if not _row_ok(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_lo9": w.get("xor_lo9"),
                "n_ok": w.get("n_ok"),
                "n_g1": w.get("n_g1"),
                "n_lo9": w.get("n_lo9"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_lo9 += w["n_lo9"]
        n_lo9g += w["n_lo9g"]
        rows[str(k)] = {
            "xor_lo9": w["xor_lo9"],
            "xor_up": w["xor_up"],
            "xor_lo": w["xor_lo"],
            "rest": want_rest10(k, 10),
            "n_lo9": w["n_lo9"],
            "n_lo9g": w["n_lo9g"],
            "n_lo": w["n_lo"],
            "n_up": w["n_up"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor_lo9"] == 0 for k in range(0, 11))
        and rows["8"]["n_lo9"] == 389
        and rows["9"]["n_lo9"] == 1389
        and rows["9"]["n_lo9g"] == 560
        and rows["10"]["n_lo9"] == 4203
        and rows["10"]["n_lo9g"] == 2032
        and rows["10"]["xor_lo"] == 1
        and rows["10"]["xor_up"] == 1
        and want_s_2u25(10) == 1
        and want_rest10(10, 10) == 0
        and nl["checks"]["all_ok"]
        and nl["verdict"]["s_2u94"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_lo9": n_lo9,
        "n_lo9g": n_lo9g,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    """NL vanish dies at k=9: xor_lo9=0."""
    r = q10["rows"]["9"]
    ok = r["xor_lo9"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor_lo9": r["xor_lo9"]}


def killed_die_k10(q10: dict) -> dict:
    """NL vanish dies at k=10: xor_lo9=0."""
    r = q10["rows"]["10"]
    ok = r["xor_lo9"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor_lo9": r["xor_lo9"]}


def killed_eq_ni(q10: dict) -> dict:
    """NL vanish through k<=10 equals NI: k=10 is 0 vs 1."""
    r = q10["rows"]["10"]
    ok = r["xor_lo9"] == 0 and r["xor_lo"] == 1
    return {"ok": ok, "k": 10, "q": 10, "xor_lo9": r["xor_lo9"], "xor_lo": r["xor_lo"]}


def killed_eq_rest(q10: dict) -> dict:
    """NL vanish through k<=10 equals rest: k=2 is 0 vs 1."""
    r = q10["rows"]["2"]
    ok = r["xor_lo9"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_lo9": r["xor_lo9"], "rest": r["rest"]}


def killed_empty(q10: dict) -> dict:
    """k=9 2U-9U/4 S-slice empty: n_lo9=1389."""
    r = q10["rows"]["9"]
    ok = r["n_lo9"] == 1389
    return {"ok": ok, "k": 9, "q": 10, "n_lo9": r["n_lo9"]}


def killed_pointwise(q10: dict) -> dict:
    """k=9 2U-9U/4 S pointwise 0: n_lo9g=560."""
    r = q10["rows"]["9"]
    ok = r["n_lo9g"] == 560 and r["n_lo9"] == 1389
    return {"ok": ok, "k": 9, "q": 10, "n_lo9g": r["n_lo9g"], "n_lo9": r["n_lo9"]}


def killed_q6() -> dict:
    """NL vanish on q=6 as a non-empty census: prefix NL k=4 empty."""
    nl = json.loads(NL_JSON.read_text())
    kq = nl["killed_q6"]
    ok = kq["xor_lo9"] == 0 and kq["n_lo9"] == 0
    return {
        "ok": ok,
        "k": 4,
        "q": 6,
        "xor_lo9": kq["xor_lo9"],
        "n_lo9": kq["n_lo9"],
    }


def prefixes() -> dict:
    nl = json.loads(NL_JSON.read_text())
    nk = json.loads(NK_JSON.read_text())
    ni = json.loads(NI_JSON.read_text())
    ok = (
        nl["checks"]["all_ok"]
        and nk["checks"]["all_ok"]
        and ni["checks"]["all_ok"]
        and nl["verdict"]["s_2u94"] == "LEMMA"
        and nk["verdict"]["s_2u25_10"] == "LEMMA"
        and ni["verdict"]["s_2u25"] == "LEMMA"
        and nl["verdict"]["prize"] == "unsolved"
        and want_s_2u25(10) == 1
        and want_rest10(2, 10) == 1
        and want_rest10(10, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    kni: dict,
    kr: dict,
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
        and kni["ok"]
        and kr["ok"]
        and kemp["ok"]
        and kpw["ok"]
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
    q10 = q10_s_2u94_10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    kni = killed_eq_ni(q10)
    kr = killed_eq_rest(q10)
    kemp = killed_empty(q10)
    kpw = killed_pointwise(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(
        c20, q10, kd9, kd10, kni, kr, kemp, kpw, kq6, sc, pref
    )
    dump = {
        "cycle": "NM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_s_2u94_10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_eq_ni": {k: kni[k] for k in kni if k != "ok"},
        "killed_eq_rest": {k: kr[k] for k in kr if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_pointwise": {k: kpw[k] for k in kpw if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "s_2u94_10": True,
            "s_2u94": True,
            "s_2u25_10": True,
            "dies_k9": False,
            "dies_k10": False,
            "eq_ni": False,
            "eq_rest": False,
            "nlo9_empty": False,
            "nlo9_pointwise": False,
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
            "s_2u94_10": "LEMMA",
            "s_2u94": "LEMMA",
            "s_2u25_10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "eq_ni": "KILLED",
            "eq_rest": "KILLED",
            "nlo9_empty": "KILLED",
            "nlo9_pointwise": "KILLED",
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
        "q10_s_2u94_10 n_ok",
        dump["q10_s_2u94_10"]["n_ok"],
        "n_g1",
        dump["q10_s_2u94_10"]["n_g1"],
        "n_lo9",
        dump["q10_s_2u94_10"]["n_lo9"],
        "n_lo9g",
        dump["q10_s_2u94_10"]["n_lo9g"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_eq_ni", dump["killed_eq_ni"])
    print("killed_eq_rest", dump["killed_eq_rest"])
    print("killed_empty", dump["killed_empty"])
    print("killed_pointwise", dump["killed_pointwise"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
