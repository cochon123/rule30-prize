#!/usr/bin/env python3
"""Cycle KP: G(2^a-1) is a prefix of G(3*2^a-1).

For 0<=d<=2^{a+1}-2, G(2^a-1, d)=G(3*2^a-1, d). That is the full
Mersenne row, not only d<2^a. The rows are not equal; the prefix is
not G(2^{a+1}-1) or G(2^a+1); the middle of 3*2^a-1 is not Mersenne.
This is Green-only, not J. Do not claim J6=J10=0 implies J18=1 for
all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_kp.py --certify
Dump: research/cycle_kp.json
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
from cycle_kh import g4_xor_cover
from cycle_ko import g_tri_piece

OUT = Path(__file__).resolve().with_suffix(".json")
KO_JSON = Path(__file__).resolve().parent / "cycle_ko.json"

A_MAX = 8


def mer_n(a: int) -> int:
    return (1 << a) - 1


def tri_n(a: int) -> int:
    return 3 * (1 << a) - 1


def prefix_table() -> dict:
    """a<=8: G(2^a-1,d)=G(3*2^a-1,d)=g_tri_piece(a,d) for d<=2^{a+1}-2."""
    n_a = n_ok = 0
    ns = []
    for a in range(0, A_MAX + 1):
        nm, nt = mer_n(a), tri_n(a)
        ns.append((nm, nt))
        for d in range(0, 2 * nm + 1):
            gm, gt, gp = G(nm, d), G(nt, d), g_tri_piece(a, d)
            if gm != gt or gt != gp:
                return {
                    "ok": False,
                    "g": True,
                    "a": a,
                    "d": d,
                    "mer": gm,
                    "tri": gt,
                    "piece": gp,
                }
            n_ok += 1
        n_a += 1
    ok = (
        n_a == A_MAX + 1
        and ns[0] == (0, 2)
        and ns[1] == (1, 5)
        and ns[8] == (255, 767)
        and G(1, 0) == G(5, 0) == 1
        and G(1, 2) == G(5, 2) == 1
        and G(3, 4) == G(11, 4) == 0
        and G(7, 14) == G(23, 14) == 1
    )
    return {"ok": ok, "n_a": n_a, "n_ok": n_ok, "n": ns}


def killed_full_row() -> dict:
    """The two rows are equal: n=5 d=4 is 1, G(1,4)=0."""
    ok = G(5, 4) == 1 and G(1, 4) == 0
    return {"ok": ok, "d": 4, "tri": G(5, 4), "mer": G(1, 4)}


def killed_next_mer() -> dict:
    """Prefix is G(2^{a+1}-1): a=1 d=2 is G(5,2)=1 vs G(3,2)=0."""
    ok = G(5, 2) == 1 and G(3, 2) == 0
    return {"ok": ok, "d": 2, "tri": G(5, 2), "next_mer": G(3, 2)}


def killed_fermat() -> dict:
    """Prefix is Fermat G(2^a+1): a=2 d=2 is G(11,2)=0 vs G(5,2)=1."""
    ok = G(11, 2) == 0 and G(5, 2) == 1
    return {"ok": ok, "d": 2, "tri": G(11, 2), "fermat": G(5, 2)}


def killed_middle() -> dict:
    """Middle of 3*2^a-1 is Mersenne: a=1 d=3 is G(5,3)=0 vs G(1,0)=1."""
    ok = G(5, 3) == 0 and G(1, 0) == 1
    return {"ok": ok, "d": 3, "tri": G(5, 3), "mer": G(1, 0)}


def prefixes() -> dict:
    ko = json.loads(KO_JSON.read_text())
    ok = (
        ko["checks"]["all_ok"]
        and ko["verdict"]["g_tri_piece"] == "LEMMA"
        and ko["verdict"]["g_tri_closed"] == "LEMMA"
        and ko["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, rt: dict, sc: dict, k0: dict, k1: dict, k2: dict, k3: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rt["ok"] and sc["ok"] and k0["ok"] and k1["ok"] and k2["ok"] and k3["ok"] and pref["ok"]
    assert G(0, 0) == G(2, 0) == 1
    assert mer_n(3) == 7 and tri_n(3) == 23
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rt = prefix_table()
    sc = g4_xor_cover()
    k0 = killed_full_row()
    k1 = killed_next_mer()
    k2 = killed_fermat()
    k3 = killed_middle()
    pref = prefixes()
    checks = self_checks(c20, rt, sc, k0, k1, k2, k3, pref)
    dump = {
        "cycle": "KP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prefix_table": {k: rt[k] for k in rt if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_full_row": {k: k0[k] for k in k0 if k != "ok"},
        "killed_next_mer": {k: k1[k] for k in k1 if k != "ok"},
        "killed_fermat": {k: k2[k] for k in k2 if k != "ok"},
        "killed_middle": {k: k3[k] for k in k3 if k != "ok"},
        "lemmas": {
            "mer_prefix_tri": True,
            "g_tri_piece": True,
            "g_tri_closed": True,
            "mer_eq_tri_row": False,
            "mer_prefix_next": False,
            "mer_prefix_fermat": False,
            "mer_eq_tri_mid": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "mer_prefix_tri": "LEMMA",
            "g_tri_piece": "LEMMA",
            "g_tri_closed": "LEMMA",
            "mer_eq_tri_row": "KILLED",
            "mer_prefix_next": "KILLED",
            "mer_prefix_fermat": "KILLED",
            "mer_eq_tri_mid": "KILLED",
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
    print("prefix_table", dump["prefix_table"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_full_row", dump["killed_full_row"])
    print("killed_next_mer", dump["killed_next_mer"])
    print("killed_fermat", dump["killed_fermat"])
    print("killed_middle", dump["killed_middle"])


if __name__ == "__main__":
    main()
