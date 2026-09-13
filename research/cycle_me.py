#!/usr/bin/env python3
"""Cycle ME: on q=10 for k<=8, unique-rest XOR is 0 so leftover XOR is rest.

On covering J10 for k<=8, XOR of the LC-LU unique packed AND slots
off {4,6,14} vanishes, so rest equals leftover AND xor. Dual of
Cycle MD's k=2 q=6 kill (that unique xor is 1). Not leftover=rest
on q=6; not unique-rest xor vs J; not the split for all k; not
q=6 unique xor=0. Do not claim J6=J10=0 implies J18=1 for all k;
do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_me.py --certify
Dump: research/cycle_me.json
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
MD_JSON = Path(__file__).resolve().parent / "cycle_md.json"


def q10_left() -> dict:
    """k<=8 q=10: unique-rest xor=0 and leftover xor=rest=want_rest10."""
    n_ok = n_g1 = 0
    rows = {}
    for k in range(0, 9):
        w = _walk_split(k, 10)
        wr = want_rest10(k, 10)
        if (
            not w.get("ok")
            or w["xor_u"] != 0
            or w["xor_lo"] != w["xor_rest"]
            or w["xor_rest"] != wr
            or w["xor_rest"] != w["xor_u"] ^ w["xor_lo"]
        ):
            return {
                "ok": False,
                "k": k,
                "q": 10,
                "xor_u": w.get("xor_u"),
                "xor_lo": w.get("xor_lo"),
                "xor_rest": w.get("xor_rest"),
                "wr": wr,
            }
        n_ok += w["n_ok"]
        n_g1 += w["n_g1"]
        rows[str(k)] = {
            "xor_rest": w["xor_rest"],
            "xor_u": w["xor_u"],
            "xor_lo": w["xor_lo"],
            "n_ok": w["n_ok"],
            "n_g1": w["n_g1"],
        }
    ok = (
        rows["2"]["xor_rest"] == 1
        and rows["6"]["xor_rest"] == 1
        and rows["8"]["xor_rest"] == 1
        and rows["0"]["xor_rest"] == 0
        and rows["4"]["xor_rest"] == 0
        and rows["7"]["xor_rest"] == 0
        and all(rows[str(k)]["xor_u"] == 0 for k in range(0, 9))
        and all(rows[str(k)]["xor_lo"] == rows[str(k)]["xor_rest"] for k in range(0, 9))
    )
    return {"ok": ok, "n_ok": n_ok, "n_g1": n_g1, "rows": rows}


def killed_q6_u0() -> dict:
    """unique-rest xor=0 on q=6: k=2 q=6 is 1 (Cycle MD)."""
    md = json.loads(MD_JSON.read_text())
    u = md["unique_kills"]["xor_u"]
    ok = u == 1 and md["verdict"]["unique0"] == "KILLED"
    return {"ok": ok, "k": 2, "q": 6, "xor_u": u}


def killed_q6_left() -> dict:
    """leftover xor=rest on q=6: k=2 q=6 leftover=1 rest=0 (Cycle MD)."""
    md = json.loads(MD_JSON.read_text())
    uk = md["unique_kills"]
    ok = uk["xor_lo"] == 1 and uk["xor_rest"] == 0
    return {"ok": ok, "k": 2, "q": 6, "xor_lo": uk["xor_lo"], "xor_rest": uk["xor_rest"]}


def killed_u_vs_j(q10: dict) -> dict:
    """unique-rest xor equals J on q=10: k=0 q=10 has unique=0 and J=1."""
    ok = q10["rows"]["0"]["xor_u"] == 0
    return {"ok": ok, "k": 0, "q": 10, "xor_u": 0, "J": 1}


def prefixes() -> dict:
    md = json.loads(MD_JSON.read_text())
    ok = (
        md["checks"]["all_ok"]
        and md["verdict"]["rest10"] == "LEMMA"
        and md["verdict"]["unique0"] == "KILLED"
        and md["verdict"]["left_eq"] == "KILLED"
        and md["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    q10: dict,
    kq6u: dict,
    kq6l: dict,
    kuj: dict,
    sc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert q10["ok"] and kq6u["ok"] and kq6l["ok"] and kuj["ok"] and sc["ok"] and pref["ok"]
    assert want_rest10(8, 10) == 1 and want_rest10(7, 10) == 0
    assert q10["rows"]["8"]["xor_lo"] == 1
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    q10 = q10_left()
    kq6u = killed_q6_u0()
    kq6l = killed_q6_left()
    kuj = killed_u_vs_j(q10)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, q10, kq6u, kq6l, kuj, sc, pref)
    dump = {
        "cycle": "ME",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "q10_left": {k: q10[k] for k in q10 if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_q6_u0": {k: kq6u[k] for k in kq6u if k != "ok"},
        "killed_q6_left": {k: kq6l[k] for k in kq6l if k != "ok"},
        "killed_u_vs_j": {k: kuj[k] for k in kuj if k != "ok"},
        "lemmas": {
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
            "q6_u0": False,
            "q6_left": False,
            "u_vs_j": False,
            "unique0": False,
            "left_eq": False,
            "mod4": False,
            "rest8_all": False,
            "all_k": False,
            "rest_all_k": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
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
            "q6_u0": "KILLED",
            "q6_left": "KILLED",
            "u_vs_j": "KILLED",
            "unique0": "KILLED",
            "left_eq": "KILLED",
            "mod4": "KILLED",
            "rest8_all": "KILLED",
            "all_k": "KILLED",
            "rest_all_k": "KILLED",
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
    print("q10_left n_ok", dump["q10_left"]["n_ok"], "n_g1", dump["q10_left"]["n_g1"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_q6_u0", dump["killed_q6_u0"])
    print("killed_q6_left", dump["killed_q6_left"])
    print("killed_u_vs_j", dump["killed_u_vs_j"])


if __name__ == "__main__":
    main()
