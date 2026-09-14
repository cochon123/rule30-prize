#!/usr/bin/env python3
"""Cycle RN: unique Green n%4 is (0,1,1,0) for every k>=6.

Cycle QX/QY Green rest n%4 is (0,1,1,1) for k>=3. Cycle RM leftover
Green n%4 is (0,0,0,1) for k>=6. Unique Green is Green xor leftover,
so the tuple is (0,1,1,0): unique Green lives on n%4 in {1,2}. Dual
of RM. Not that tuple for all k (k=0 is (0,0,0,0); k=5 is (1,0,1,1)).
Not unique Green n%4 equals packed unique n%4 (packed k>=6 is
(1,0,0,1)). Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_rn.py --certify
Dump: research/cycle_rn.json
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
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qx import want_g_n0, want_g_n1, want_g_n2, want_g_n3
from cycle_rb import want_u_nmod
from cycle_rm import (
    want_lo_g_nmod,
    want_u_g_n0,
    want_u_g_n1,
    want_u_g_n2,
    want_u_g_n3,
    want_u_g_nmod,
)

OUT = Path(__file__).resolve().with_suffix(".json")
RM_JSON = Path(__file__).resolve().parent / "cycle_rm.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
RB_JSON = Path(__file__).resolve().parent / "cycle_rb.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64


def want_g_nmod(k: int) -> list[int]:
    return [want_g_n0(k), want_g_n1(k), want_g_n2(k), want_g_n3(k)]


def tot_form() -> dict:
    """k<=K_ALG: unique Green n%4 is Green xor leftover; k>=6 is (0,1,1,0)."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        g = want_g_nmod(k)
        lo = want_lo_g_nmod(k)
        u = want_u_g_nmod(k)
        xor = [g[i] ^ lo[i] for i in range(4)]
        if u != xor:
            return {"ok": False, "xor": True, "k": k, "u": u, "xor": xor}
        if u != [want_u_g_n0(k), want_u_g_n1(k), want_u_g_n2(k), want_u_g_n3(k)]:
            return {"ok": False, "parts": True, "k": k, "u": u}
        if k >= 6 and u != [0, 1, 1, 0]:
            return {"ok": False, "ge6": True, "k": k, "u": u}
        if k >= 6 and lo != [0, 0, 0, 1]:
            return {"ok": False, "lo": True, "k": k, "lo": lo}
        if k >= 3 and g != [0, 1, 1, 1]:
            return {"ok": False, "g": True, "k": k, "g": g}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_u_g_nmod(0) == [0, 0, 0, 0]
        and want_u_g_nmod(5) == [1, 0, 1, 1]
        and want_u_g_nmod(6) == [0, 1, 1, 0]
        and want_u_g_nmod(8) == [0, 1, 1, 0]
        and want_g_nmod(6) == [0, 1, 1, 1]
        and want_lo_g_nmod(6) == [0, 0, 0, 1]
        and want_u_g_n1(6) == 1
        and want_u_g_n3(6) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def prefix_walk() -> dict:
    """Prefix Cycle RM green_walk: unique Green n%4 at k=0,5,6,8."""
    rm = json.loads(RM_JSON.read_text())
    rows_in = rm["green_walk"]["rows"]
    rows = {}
    for key in ("0", "5", "6", "8"):
        u = rows_in[key]["u"]
        lo = rows_in[key]["lo"]
        k = int(key)
        if u != want_u_g_nmod(k):
            return {"ok": False, "u": True, "k": k, "u": u}
        if lo != want_lo_g_nmod(k):
            return {"ok": False, "lo": True, "k": k, "lo": lo}
        rows[key] = {"u": u, "lo": lo}
    ok = (
        rm["checks"]["all_ok"]
        and rm["green_walk"]["n_ok"] == 9
        and rows["0"]["u"] == [0, 0, 0, 0]
        and rows["5"]["u"] == [1, 0, 1, 1]
        and rows["6"]["u"] == [0, 1, 1, 0]
        and rows["8"]["u"] == [0, 1, 1, 0]
        and rows["6"]["lo"] == [0, 0, 0, 1]
        and rows["8"]["lo"] == [0, 0, 0, 1]
    )
    return {
        "ok": ok,
        "n_ok": rm["green_walk"]["n_ok"],
        "k_hi": rm["green_walk"]["k_hi"],
        "rows": rows,
    }


def killed_eq() -> dict:
    """Unique Green n%4==(0,1,1,0) all k; unique Green n%4 equals packed unique."""
    u0 = want_u_g_nmod(0)
    u5 = want_u_g_nmod(5)
    u6 = want_u_g_nmod(6)
    p6 = want_u_nmod(6)
    p8 = want_u_nmod(8)
    ok = (
        u0 == [0, 0, 0, 0]
        and u0 != [0, 1, 1, 0]
        and u5 == [1, 0, 1, 1]
        and u5 != [0, 1, 1, 0]
        and u6 == [0, 1, 1, 0]
        and p6 == [1, 0, 0, 1]
        and u6 != p6
        and want_u_g_nmod(8) == [0, 1, 1, 0]
        and p8 == [1, 0, 0, 1]
        and want_u_g_nmod(8) != p8
    )
    return {"ok": ok, "u0": u0, "u5": u5, "u6": u6, "p6": p6}


def prefixes() -> dict:
    rm = json.loads(RM_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    rb = json.loads(RB_JSON.read_text())
    ok = (
        rm["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and rb["checks"]["all_ok"]
        and rm["verdict"]["lo_g_nmod_0001_k_ge_6"] == "LEMMA"
        and qy["verdict"]["green_nmod_0111_k_ge_3"] == "LEMMA"
        and rb["verdict"]["unique_n2_0"] == "LEMMA"
        and rm["verdict"]["lo_g_nmod_0001_all_k"] == "KILLED"
        and qy["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and rm["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rm["verdict"]["prize"] == "unsolved"
        and want_u_g_nmod(6) == [0, 1, 1, 0]
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, walk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and walk["ok"]
    assert kl["ok"] and sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    tot = tot_form()
    walk = prefix_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, walk, kl, sc, pref)
    dump = {
        "cycle": "RN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "prefix_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "u_g_nmod_0110_k_ge_6": True,
            "u_g_nmod_0110_all_k": False,
            "u_g_nmod_eq_packed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "u_g_nmod_0110_k_ge_6": "LEMMA",
            "u_g_nmod_0110_all_k": "KILLED",
            "u_g_nmod_eq_packed": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "even_rest_eq_parent_odd_all_k": "PREFIX",
            "E_all_k": "PREFIX",
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
        "prefix_walk n_ok",
        dump["prefix_walk"]["n_ok"],
        "u6",
        dump["prefix_walk"]["rows"]["6"]["u"],
        "u0",
        dump["prefix_walk"]["rows"]["0"]["u"],
        "u5",
        dump["prefix_walk"]["rows"]["5"]["u"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
