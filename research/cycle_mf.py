#!/usr/bin/env python3
"""Cycle MF: unique-rest XOR vanishes at k=9 for both covering q.

On covering J6,J10 at k=9, XOR of the LC-LU unique packed AND
slots off {4,6,14} is 0, so leftover XOR equals rest=0. Cycle ME
therefore holds at k=9 on q=10; q=6 unique xor is also 0 (unlike
k=2 q=6). Not ME for all k; not unique=0 on all q=6; not unique
xor vs J; not leftover=rest on q=6. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_mf.py --certify
Dump: research/cycle_mf.json
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
from cycle_md import _walk_split, want_rest10

OUT = Path(__file__).resolve().with_suffix(".json")
ME_JSON = Path(__file__).resolve().parent / "cycle_me.json"
MB_JSON = Path(__file__).resolve().parent / "cycle_mb.json"

# Probe-checked k=9 split sizes (q=6 ~1.38s, q=10 ~4.98s).
WANT_WALK = {
    (9, 6): {
        "n_ok": 983296,
        "n_g1": 135032,
        "xor_rest": 0,
        "xor_u": 0,
        "xor_lo": 0,
    },
    (9, 10): {
        "n_ok": 3605248,
        "n_g1": 391544,
        "xor_rest": 0,
        "xor_u": 0,
        "xor_lo": 0,
    },
}


def _row_ok(k: int, q: int, w: dict) -> bool:
    """True if split sizes match the probe and unique xor vanishes."""
    want = WANT_WALK[(k, q)]
    wr = want_rest10(k, q)
    return (
        w.get("ok")
        and w["n_ok"] == want["n_ok"]
        and w["n_g1"] == want["n_g1"]
        and w["xor_rest"] == want["xor_rest"] == wr
        and w["xor_u"] == want["xor_u"] == 0
        and w["xor_lo"] == want["xor_lo"] == w["xor_rest"]
        and w["xor_rest"] == w["xor_u"] ^ w["xor_lo"]
    )


def k9_u0() -> dict:
    """k=9 both q: unique-rest xor=0 and leftover xor=rest=0."""
    rows = {}
    n_ok = n_g1 = 0
    for q, name in ((6, "j6"), (10, "j10")):
        w = _walk_split(9, q)
        if not _row_ok(9, q, w):
            return {
                "ok": False,
                "k": 9,
                "q": q,
                "xor_u": w.get("xor_u"),
                "xor_lo": w.get("xor_lo"),
                "xor_rest": w.get("xor_rest"),
                "n_ok": w.get("n_ok"),
                "n_g1": w.get("n_g1"),
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        rows[name] = {
            "xor_rest": w["xor_rest"],
            "xor_u": w["xor_u"],
            "xor_lo": w["xor_lo"],
        }
    ok = (
        rows["j6"]["xor_u"] == 0
        and rows["j10"]["xor_u"] == 0
        and rows["j6"]["xor_rest"] == 0
        and rows["j10"]["xor_rest"] == 0
        and want_rest10(9, 6) == 0
        and want_rest10(9, 10) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_me9(k9: dict) -> dict:
    """ME dies at k=9 q=10: unique xor is 0, leftover=rest=0."""
    r = k9["rows"]["j10"]
    ok = r["xor_u"] == 0 and r["xor_lo"] == 0 and r["xor_rest"] == 0
    return {"ok": ok, "k": 9, "q": 10, "xor_u": r["xor_u"], "xor_rest": r["xor_rest"]}


def killed_q6_u1(k9: dict) -> dict:
    """q=6 unique xor always 1: k=9 q=6 is 0."""
    r = k9["rows"]["j6"]
    ok = r["xor_u"] == 0
    return {"ok": ok, "k": 9, "q": 6, "xor_u": r["xor_u"]}


def killed_u_vs_j(k9: dict) -> dict:
    """unique-rest xor equals J at k=9: unique=0, J=1 (Cycle MB)."""
    mb = json.loads(MB_JSON.read_text())
    j10 = mb["k9_holds"]["rows"]["j10"]["xor_j"]
    ok = k9["rows"]["j10"]["xor_u"] == 0 and j10 == 1
    return {"ok": ok, "k": 9, "q": 10, "xor_u": 0, "J": j10}


def prefixes() -> dict:
    me = json.loads(ME_JSON.read_text())
    mb = json.loads(MB_JSON.read_text())
    ok = (
        me["checks"]["all_ok"]
        and me["verdict"]["q10_left"] == "LEMMA"
        and mb["checks"]["all_ok"]
        and mb["verdict"]["k9_holds"] == "LEMMA"
        and me["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    k9: dict,
    kme: dict,
    kq6: dict,
    kuj: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert k9["ok"] and kme["ok"] and kq6["ok"] and kuj["ok"] and sc["ok"] and pref["ok"]
    assert want_rest10(9, 10) == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    k9 = k9_u0()
    kme = killed_me9(k9)
    kq6 = killed_q6_u1(k9)
    kuj = killed_u_vs_j(k9)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, k9, kme, kq6, kuj, sc, pref)
    dump = {
        "cycle": "MF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "k9_u0": {k: k9[k] for k in k9 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_me9": {k: kme[k] for k in kme if k != "ok"},
        "killed_q6_u1": {k: kq6[k] for k in kq6 if k != "ok"},
        "killed_u_vs_j": {k: kuj[k] for k in kuj if k != "ok"},
        "lemmas": {
            "k9_u0": True,
            "q10_left": True,
            "rest10": True,
            "k10_kill": True,
            "forced10": True,
            "q6_rest0": True,
            "rest8": True,
            "k9_holds": True,
            "forced9": True,
            "k7_holds": True,
            "forced8": True,
            "j_form": True,
            "rest_q10": True,
            "p14_except": True,
            "only_p4_p6": True,
            "p6_g1_and": True,
            "p4_g1_and": True,
            "me9_die": False,
            "q6_u1": False,
            "u_vs_j": False,
            "q6_u0": False,
            "unique0": False,
            "left_eq": False,
            "rest8_all": False,
            "all_k": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "k9_u0": "LEMMA",
            "q10_left": "LEMMA",
            "rest10": "LEMMA",
            "k10_kill": "KILLED",
            "forced10": "LEMMA",
            "q6_rest0": "LEMMA",
            "rest8": "LEMMA",
            "k9_holds": "LEMMA",
            "forced9": "LEMMA",
            "k7_holds": "LEMMA",
            "forced8": "LEMMA",
            "j_form": "LEMMA",
            "rest_q10": "LEMMA",
            "p14_except": "LEMMA",
            "only_p4_p6": "LEMMA",
            "p6_g1_and": "LEMMA",
            "p4_g1_and": "LEMMA",
            "me9_die": "KILLED",
            "q6_u1": "KILLED",
            "u_vs_j": "KILLED",
            "q6_u0": "KILLED",
            "unique0": "KILLED",
            "left_eq": "KILLED",
            "rest8_all": "KILLED",
            "all_k": "KILLED",
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
    print("k9_u0 n_ok", dump["k9_u0"]["n_ok"], "n_g1", dump["k9_u0"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_me9", dump["killed_me9"])
    print("killed_q6_u1", dump["killed_q6_u1"])
    print("killed_u_vs_j", dump["killed_u_vs_j"])


if __name__ == "__main__":
    main()
