#!/usr/bin/env python3
"""Cycle NB: on q=10 for k<=10, NA Green-only two-piece xor equals rest.

On covering J10 through k<=10, XOR of G(n,j+1) over palindrome-right
d%3==1 cells with G(n,j-1)=0, xor XOR of G(n,j-1) over
palindrome-right cells with n<U/2 (p=T-2j>=0; no packed row)
equals rest. Prefix Cycle NA for k<=8; walk k=9 and k=10.
Not a death at k=9 (xor=0=rest); not a death at k=10; not S
alone; not T alone; not the form on q=6; not the form for all k.
Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_nb.py --certify
Dump: research/cycle_nb.json
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
from cycle_na import _walk_green_rest

OUT = Path(__file__).resolve().with_suffix(".json")
NA_JSON = Path(__file__).resolve().parent / "cycle_na.json"
MD_JSON = Path(__file__).resolve().parent / "cycle_md.json"

# Probe-checked k=9,10 q=10 Green-only rest walk sizes (~1.78s, ~7.05s).
WANT_WALK = {
    9: {
        "n_ok": 3605248,
        "n_g1": 391544,
        "n_s": 29820,
        "n_t": 6912,
        "xor": 0,
        "xor_s": 0,
        "xor_t": 0,
    },
    10: {
        "n_ok": 14419456,
        "n_g1": 1266210,
        "n_s": 96773,
        "n_t": 22528,
        "xor": 0,
        "xor_s": 0,
        "xor_t": 0,
    },
}


def _row_ok(k: int, w: dict) -> bool:
    """True if walk sizes match the probe and xor equals rest."""
    want = WANT_WALK[k]
    wr = want_rest10(k, 10)
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["n_s"] == want["n_s"]
        and w["n_t"] == want["n_t"]
        and w["xor"] == want["xor"] == wr
        and w["xor_s"] == want["xor_s"]
        and w["xor_t"] == want["xor_t"]
        and w["xor"] == w["xor_s"] ^ w["xor_t"]
    )


def q10_rest10() -> dict:
    """q=10 k<=10: prefix NA k<=8; walk k=9,10; xor equals rest."""
    na = json.loads(NA_JSON.read_text())
    rows = {}
    for k in range(0, 9):
        r = na["q10_green_rest"]["rows"][str(k)]
        wr = want_rest10(k, 10)
        if r["xor"] != wr or r["xor"] != r["xor_s"] ^ r["xor_t"]:
            return {"ok": False, "k": k, "q": 10, "xor": r["xor"], "wr": wr}
        rows[str(k)] = {
            "xor": r["xor"],
            "xor_s": r["xor_s"],
            "xor_t": r["xor_t"],
            "rest": wr,
            "n_s": r["n_s"],
            "n_t": r["n_t"],
            "n_ok": r["n_ok"],
            "n_g1": r["n_g1"],
            "src": "NA",
        }
    n_ok = n_g1 = n_s = n_t = 0
    for k in (9, 10):
        w = _walk_green_rest(k, 10)
        if not _row_ok(k, w):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor": w.get("xor"),
                "wr": want_rest10(k, 10),
                "n_ok": w.get("n_ok"),
                "n_g1": w.get("n_g1"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        n_s += w["n_s"]
        n_t += w["n_t"]
        rows[str(k)] = {
            "xor": w["xor"],
            "xor_s": w["xor_s"],
            "xor_t": w["xor_t"],
            "rest": want_rest10(k, 10),
            "n_s": w["n_s"],
            "n_t": w["n_t"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
            "src": "walk",
        }
    ok = (
        all(rows[str(k)]["xor"] == want_rest10(k, 10) for k in range(0, 11))
        and rows["8"]["xor"] == 1
        and rows["9"]["xor"] == 0
        and rows["10"]["xor"] == 0
        and rows["9"]["n_s"] == 29820
        and rows["10"]["n_s"] == 96773
        and want_rest10(9, 10) == 0
        and want_rest10(10, 10) == 0
        and na["checks"]["all_ok"]
        and na["verdict"]["green_rest"] == "LEMMA"
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_g1": n_g1,
        "n_s": n_s,
        "n_t": n_t,
        "rows": rows,
    }


def killed_die_k9(q10: dict) -> dict:
    """NA form dies at k=9: xor=0 equals rest."""
    r = q10["rows"]["9"]
    ok = r["xor"] == 0 and r["rest"] == 0 and r["n_ok"] == 3605248
    return {"ok": ok, "k": 9, "q": 10, "xor": r["xor"], "rest": r["rest"]}


def killed_die_k10(q10: dict) -> dict:
    """NA form dies at k=10: xor=0 equals rest."""
    r = q10["rows"]["10"]
    ok = r["xor"] == 0 and r["rest"] == 0 and r["n_ok"] == 14419456
    return {"ok": ok, "k": 10, "q": 10, "xor": r["xor"], "rest": r["rest"]}


def killed_s_alone() -> dict:
    """S alone equals rest through k<=10: k=2 S=0 rest=1."""
    na = json.loads(NA_JSON.read_text())
    r = na["q10_green_rest"]["rows"]["2"]
    ok = r["xor_s"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 2, "q": 10, "xor_s": r["xor_s"], "rest": r["rest"]}


def killed_t_alone() -> dict:
    """T alone equals rest through k<=10: k=8 T=0 rest=1."""
    na = json.loads(NA_JSON.read_text())
    r = na["q10_green_rest"]["rows"]["8"]
    ok = r["xor_t"] == 0 and r["rest"] == 1
    return {"ok": ok, "k": 8, "q": 10, "xor_t": r["xor_t"], "rest": r["rest"]}


def killed_empty(q10: dict) -> dict:
    """k=9 S-slice empty: n_s=29820."""
    r = q10["rows"]["9"]
    ok = r["n_s"] == 29820 and r["n_t"] == 6912
    return {"ok": ok, "k": 9, "q": 10, "n_s": r["n_s"], "n_t": r["n_t"]}


def killed_q6() -> dict:
    """green rest form on q=6: prefix NA k=2 xor=1 rest=0."""
    na = json.loads(NA_JSON.read_text())
    kq = na["killed_q6"]
    ok = kq["xor"] == 1 and kq["rest"] == 0 and kq["n_t"] == 1
    return {
        "ok": ok,
        "k": 2,
        "q": 6,
        "xor": kq["xor"],
        "rest": kq["rest"],
        "n_t": kq["n_t"],
    }


def prefixes() -> dict:
    na = json.loads(NA_JSON.read_text())
    md = json.loads(MD_JSON.read_text())
    ok = (
        na["checks"]["all_ok"]
        and md["checks"]["all_ok"]
        and na["verdict"]["green_rest"] == "LEMMA"
        and md["verdict"]["rest10"] == "LEMMA"
        and na["verdict"]["prize"] == "unsolved"
        and want_rest10(8, 10) == 1
        and want_rest10(9, 10) == 0
        and want_rest10(10, 10) == 0
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kd9: dict,
    kd10: dict,
    ks: dict,
    kt: dict,
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
        and ks["ok"]
        and kt["ok"]
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
    q10 = q10_rest10()
    kd9 = killed_die_k9(q10)
    kd10 = killed_die_k10(q10)
    ks = killed_s_alone()
    kt = killed_t_alone()
    kemp = killed_empty(q10)
    kq6 = killed_q6()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kd9, kd10, ks, kt, kemp, kq6, sc, pref)
    dump = {
        "cycle": "NB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_rest10": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_die_k9": {k: kd9[k] for k in kd9 if k != "ok"},
        "killed_die_k10": {k: kd10[k] for k in kd10 if k != "ok"},
        "killed_s_alone": {k: ks[k] for k in ks if k != "ok"},
        "killed_t_alone": {k: kt[k] for k in kt if k != "ok"},
        "killed_empty": {k: kemp[k] for k in kemp if k != "ok"},
        "killed_q6": {k: kq6[k] for k in kq6 if k != "ok"},
        "lemmas": {
            "green_rest10": True,
            "green_rest": True,
            "rest10": True,
            "dies_k9": False,
            "dies_k10": False,
            "s_alone": False,
            "t_alone": False,
            "nlt_empty": False,
            "q6_rest": False,
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
            "green_rest10": "LEMMA",
            "green_rest": "LEMMA",
            "rest10": "LEMMA",
            "dies_k9": "KILLED",
            "dies_k10": "KILLED",
            "s_alone": "KILLED",
            "t_alone": "KILLED",
            "nlt_empty": "KILLED",
            "q6_rest": "KILLED",
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
        "q10_rest10 n_ok",
        dump["q10_rest10"]["n_ok"],
        "n_g1",
        dump["q10_rest10"]["n_g1"],
        "n_s",
        dump["q10_rest10"]["n_s"],
        "n_t",
        dump["q10_rest10"]["n_t"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_die_k9", dump["killed_die_k9"])
    print("killed_die_k10", dump["killed_die_k10"])
    print("killed_s_alone", dump["killed_s_alone"])
    print("killed_t_alone", dump["killed_t_alone"])
    print("killed_empty", dump["killed_empty"])
    print("killed_q6", dump["killed_q6"])


if __name__ == "__main__":
    main()
