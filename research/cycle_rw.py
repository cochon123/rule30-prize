#!/usr/bin/env python3
"""Cycle RW: covering Green G=1 on n%4==0 equals parent even G=1.

Cycle QV even-n G=1 at k is the 2-fold of all clipped G=1 at k-1,
split n0 from even parent and n2 from odd parent. Cycle QX n0 G=1
is clip xor at k-2, which equals even-n G=1 at k-1. Cycle QX n2
G=1 is odd-n G=1 at k-1. So G=1 folds on even children: n0 G=1
equals parent even G=1 and n2 G=1 equals parent odd G=1 for every
k>=1 (the even-child dual of Cycle QY). Green rest is G=1 xor
forced, so Cycle RS rest xor equals Cycle RV forced xor. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rw.py --certify
Dump: research/cycle_rw.json
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
from cycle_qh import want_clip_g1
from cycle_qw import want_g1_even
from cycle_qx import want_g1_n0, want_g1_n2
from cycle_qy import want_g1_n1, want_g1_n3
from cycle_rs import want_g_n0_xor_parent_even, want_g_n2_xor_parent_odd
from cycle_rv import (
    want_f_n0,
    want_f_n1,
    want_f_n2,
    want_f_n3,
)

OUT = Path(__file__).resolve().with_suffix(".json")
QX_JSON = Path(__file__).resolve().parent / "cycle_qx.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
QV_JSON = Path(__file__).resolve().parent / "cycle_qv.json"
RS_JSON = Path(__file__).resolve().parent / "cycle_rs.json"
RV_JSON = Path(__file__).resolve().parent / "cycle_rv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_WALK = 8


def want_g1_n0_xor_parent_even(k: int) -> int:
    """n0 G=1 xor parent even G=1, all k: 0 for k>=1."""
    if k < 1:
        return 0
    return want_g1_n0(k) ^ want_g1_even(k - 1)


def want_g1_n2_xor_parent_odd(k: int) -> int:
    """n2 G=1 xor parent odd G=1, all k: 0 for k>=1."""
    if k < 1:
        return 0
    po = want_g1_even(k - 1) ^ want_clip_g1(k - 1)
    return want_g1_n2(k) ^ po


def want_f_n0_xor_parent_even(k: int) -> int:
    """Forced n0 tot xor parent even forced tot, all k: 1 iff k>=2."""
    if k < 1:
        return 0
    return want_f_n0(k) ^ want_f_n0(k - 1) ^ want_f_n2(k - 1)


def want_f_n2_xor_parent_odd(k: int) -> int:
    """Forced n2 tot xor parent odd forced tot, all k: 1 iff k>=4."""
    if k < 1:
        return 0
    return want_f_n2(k) ^ want_f_n1(k - 1) ^ want_f_n3(k - 1)


def walk_chk() -> dict:
    """k<=8: QX walk n0/n2 G=1 equals parent even/odd G=1."""
    qx = json.loads(QX_JSON.read_text())
    rows_in = qx["green_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(1, K_WALK + 1):
        g1 = rows_in[str(k)]["g1"]
        pg1 = rows_in[str(k - 1)]["g1"]
        pe = pg1[0] ^ pg1[2]
        po = pg1[1] ^ pg1[3]
        if g1[0] != pe:
            return {"ok": False, "n0": True, "k": k, "g0": g1[0], "pe": pe}
        if g1[2] != po:
            return {"ok": False, "n2": True, "k": k, "g2": g1[2], "po": po}
        if want_g1_n0_xor_parent_even(k) != 0:
            return {"ok": False, "n0xor": True, "k": k}
        if want_g1_n2_xor_parent_odd(k) != 0:
            return {"ok": False, "n2xor": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"g0": g1[0], "pe": pe, "g2": g1[2], "po": po}
    ok = (
        n_ok == K_WALK
        and rows["1"]["g0"] == 0
        and rows["2"]["g0"] == 1
        and rows["3"]["g0"] == 0
        and rows["1"]["g2"] == 1
        and rows["8"]["g0"] == 0
        and rows["8"]["g2"] == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_WALK, "rows": rows}


def tot_form() -> dict:
    """k<=K_ALG: even-child G=1 folds; RS rest xor equals RV forced xor."""
    n_ok = 0
    for k in range(1, K_ALG + 1):
        pe = want_g1_n0(k - 1) ^ want_g1_n2(k - 1)
        if pe != want_g1_even(k - 1):
            return {"ok": False, "pe": True, "k": k, "pe": pe}
        if want_g1_n0(k) != pe:
            return {"ok": False, "n0": True, "k": k}
        if want_g1_n0_xor_parent_even(k) != 0:
            return {"ok": False, "n0xor": True, "k": k}
        po = want_g1_n1(k - 1) ^ want_g1_n3(k - 1)
        po2 = want_g1_even(k - 1) ^ want_clip_g1(k - 1)
        if po != po2:
            return {"ok": False, "po": True, "k": k, "po": po, "po2": po2}
        if want_g1_n2(k) != po:
            return {"ok": False, "n2": True, "k": k}
        if want_g1_n2_xor_parent_odd(k) != 0:
            return {"ok": False, "n2xor": True, "k": k}
        r0 = want_g_n0_xor_parent_even(k)
        f0 = want_f_n0_xor_parent_even(k)
        if r0 != f0:
            return {"ok": False, "rs0": True, "k": k, "r0": r0, "f0": f0}
        if r0 != int(k >= 2):
            return {"ok": False, "n0form": True, "k": k, "r0": r0}
        r2 = want_g_n2_xor_parent_odd(k)
        f2 = want_f_n2_xor_parent_odd(k)
        if r2 != f2:
            return {"ok": False, "rs2": True, "k": k, "r2": r2, "f2": f2}
        if r2 != int(k >= 4):
            return {"ok": False, "n2form": True, "k": k, "r2": r2}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and want_g1_n0_xor_parent_even(1) == 0
        and want_g1_n0_xor_parent_even(2) == 0
        and want_g1_n0_xor_parent_even(64) == 0
        and want_g1_n2_xor_parent_odd(1) == 0
        and want_g1_n2_xor_parent_odd(64) == 0
        and want_g_n0_xor_parent_even(2) == 1
        and want_f_n0_xor_parent_even(2) == 1
        and want_g_n2_xor_parent_odd(4) == 1
        and want_f_n2_xor_parent_odd(4) == 1
        and want_g1_n0(1) != (want_g1_n1(0) ^ want_g1_n3(0))
        and want_g1_n2(1) != want_g1_even(0)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """n0 G=1 equals parent odd G=1; n2 G=1 equals parent even G=1."""
    ok = (
        want_g1_n0(1) != (want_g1_n1(0) ^ want_g1_n3(0))
        and want_g1_n2(1) != want_g1_even(0)
        and want_g1_n0_xor_parent_even(1) == 0
        and want_g1_n2_xor_parent_odd(1) == 0
        and want_g_n0_xor_parent_even(1) == 0
        and want_g_n2_xor_parent_odd(3) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    qx = json.loads(QX_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    qv = json.loads(QV_JSON.read_text())
    rs = json.loads(RS_JSON.read_text())
    rv = json.loads(RV_JSON.read_text())
    ok = (
        qx["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and qv["checks"]["all_ok"]
        and rs["checks"]["all_ok"]
        and rv["checks"]["all_ok"]
        and qv["verdict"]["g1_2fold_covering_bijection"] == "LEMMA"
        and qy["verdict"]["g1_n1_eq_parent_even"] == "LEMMA"
        and qy["verdict"]["g1_n3_eq_parent_odd"] == "LEMMA"
        and rs["verdict"]["g_n0_xor_parent_even_iff_k_ge_2"] == "LEMMA"
        and rs["verdict"]["g_n2_xor_parent_odd_iff_k_ge_4"] == "LEMMA"
        and rv["verdict"]["f_n1_eq_parent_even"] == "LEMMA"
        and qv["verdict"]["cellwise_2fold_and"] == "KILLED"
        and rs["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rs["verdict"]["prize"] == "unsolved"
        and want_g1_n0_xor_parent_even(2) == 0
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, walk, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and walk["ok"] and tot["ok"]
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
    walk = walk_chk()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, walk, tot, kl, sc, pref)
    dump = {
        "cycle": "RW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "walk_chk": {k: walk[k] for k in walk if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "g1_n0_eq_parent_even": True,
            "g1_n2_eq_parent_odd": True,
            "rs_rest_xor_eq_rv_forced_xor": True,
            "g1_n0_eq_parent_odd": False,
            "g1_n2_eq_parent_even": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "g1_n0_eq_parent_even": "LEMMA",
            "g1_n2_eq_parent_odd": "LEMMA",
            "rs_rest_xor_eq_rv_forced_xor": "LEMMA",
            "g1_n0_eq_parent_odd": "KILLED",
            "g1_n2_eq_parent_even": "KILLED",
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
        "tot_form n_ok",
        dump["tot_form"]["n_ok"],
        "walk n_ok",
        dump["walk_chk"]["n_ok"],
        "n0eq",
        int(want_g1_n0_xor_parent_even(2) == 0),
        "n2eq",
        int(want_g1_n2_xor_parent_odd(2) == 0),
        "rs2",
        want_g_n2_xor_parent_odd(4),
        "f2",
        want_f_n2_xor_parent_odd(4),
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
