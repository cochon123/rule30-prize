#!/usr/bin/env python3
"""Cycle RD: covering silent n%4==3 tot equals leftover n%4==3 tot iff k==4 or k>=6.

Silent is Green rest xor packed rest. Leftover is packed rest xor
unique. Their xor on a residue is Green xor unique. Cycle QY Green
n%4==3 rest is 1 for every k, so silent n3 equals leftover n3 iff
unique n3 is 1, which Cycle RB says is k==4 or k>=6. Not silent n3
equals leftover n3 for all k (k=0: silent 1, leftover 0). Not rest
=S xor T. Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rd.py --certify
Dump: research/cycle_rd.json
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
from cycle_pb import want_rest_e0
from cycle_qy import want_g_n3
from cycle_rb import want_u_n3
from cycle_rc import want_lo_n3

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
QX_JSON = Path(__file__).resolve().parent / "cycle_qx.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"
RC_JSON = Path(__file__).resolve().parent / "cycle_rc.json"
RB_JSON = Path(__file__).resolve().parent / "cycle_rb.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def want_sil_n3(k: int, n3: int) -> int:
    """Silent n%4==3 tot: Green n3 xor packed rest n3."""
    return want_g_n3(k) ^ n3


def want_sil_eq_lo_n3(k: int) -> int:
    """Silent n3 equals leftover n3 iff unique n3 is 1."""
    return want_u_n3(k)


def tot_form() -> dict:
    """k<=K_ALG: Green n3 is 1; silent xor leftover is Green xor unique."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_g_n3(k) != 1:
            return {"ok": False, "g": True, "k": k}
        if (want_g_n3(k) ^ want_u_n3(k)) != (1 ^ want_sil_eq_lo_n3(k)):
            return {"ok": False, "xor": True, "k": k}
        if want_sil_eq_lo_n3(k) != int(k == 4 or k >= 6):
            return {"ok": False, "form": True, "k": k}
        for n3 in (0, 1):
            sil = want_sil_n3(k, n3)
            lo = want_lo_n3(k, n3)
            if (sil == lo) != bool(want_sil_eq_lo_n3(k)):
                return {"ok": False, "id": True, "k": k, "n3": n3}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_sil_eq_lo_n3(0) == 0
        and want_sil_eq_lo_n3(4) == 1
        and want_sil_eq_lo_n3(5) == 0
        and want_sil_eq_lo_n3(6) == 1
        and want_u_n3(4) == 1
        and want_g_n3(10) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def rest_split() -> dict:
    """k<=10: QO packed n3 vs leftover/silent from Green and unique."""
    qo = json.loads(QO_JSON.read_text())
    rc = json.loads(RC_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    lo_in = rc["rest_split"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        n3 = rows_in[str(k)]["tot"][3]
        sil = want_sil_n3(k, n3)
        lo = want_lo_n3(k, n3)
        if lo != lo_in[str(k)]["lo"][3]:
            return {"ok": False, "lo": True, "k": k, "lo": lo}
        if (sil == lo) != bool(want_sil_eq_lo_n3(k)):
            return {"ok": False, "eq": True, "k": k, "sil": sil, "lo": lo}
        n_ok += 1
        rows[str(k)] = {"n3": n3, "sil": sil, "lo": lo, "eq": int(sil == lo)}
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["sil"] == 1
        and rows["0"]["lo"] == 0
        and rows["4"]["sil"] == 0
        and rows["4"]["lo"] == 0
        and rows["5"]["sil"] == 1
        and rows["5"]["lo"] == 0
        and rows["6"]["eq"] == 1
        and rows["10"]["eq"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def qx_walk() -> dict:
    """Cycle QX Green n3 is 1 on k<=8, matching silent = 1 xor packed n3."""
    qx = json.loads(QX_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    n_ok = 0
    for k in range(0, 9):
        g = qx["green_walk"]["rows"][str(k)]["tot"][3]
        n3 = qo["rest_n0_walk"]["rows"][str(k)]["tot"][3]
        if g != 1 or want_sil_n3(k, n3) != (g ^ n3):
            return {"ok": False, "k": k, "g": g, "n3": n3}
        n_ok += 1
    ok = n_ok == 9
    return {"ok": ok, "n_ok": n_ok, "k_hi": 8}


def killed_eq() -> dict:
    """Silent n3 equals leftover n3 for all k; equals ST."""
    qo = json.loads(QO_JSON.read_text())
    n3_0 = qo["rest_n0_walk"]["rows"]["0"]["tot"][3]
    sil0 = want_sil_n3(0, n3_0)
    lo0 = want_lo_n3(0, n3_0)
    n3_7 = qo["rest_n0_walk"]["rows"]["7"]["tot"][3]
    sil7 = want_sil_n3(7, n3_7)
    ok = (
        sil0 == 1
        and lo0 == 0
        and sil0 != lo0
        and want_sil_eq_lo_n3(0) == 0
        and sil7 == want_lo_n3(7, n3_7)
        and want_rest_e0(7) == 0
        and sil7 != want_rest_e0(7)
    )
    return {"ok": ok, "sil0": sil0, "lo0": lo0, "sil7": sil7, "st7": 0}


def prefixes() -> dict:
    qy = json.loads(QY_JSON.read_text())
    rb = json.loads(RB_JSON.read_text())
    rc = json.loads(RC_JSON.read_text())
    qx = json.loads(QX_JSON.read_text())
    ok = (
        qy["checks"]["all_ok"]
        and rb["checks"]["all_ok"]
        and rc["checks"]["all_ok"]
        and qx["checks"]["all_ok"]
        and qy["verdict"]["green_n3_all_k"] == "LEMMA"
        and rb["verdict"]["unique_n3_iff_k_eq_4_or_ge_6"] == "LEMMA"
        and rc["verdict"]["lo_nmod_eq_rest_xor_unique"] == "LEMMA"
        and qx["verdict"]["green_nmod_eq_packed"] == "KILLED"
        and rb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rb["verdict"]["prize"] == "unsolved"
        and want_u_n3(6) == 1
        and want_g_n3(10) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, split, walk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and split["ok"]
    assert walk["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
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
    split = rest_split()
    walk = qx_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, split, walk, kl, sc, pref)
    dump = {
        "cycle": "RD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "rest_split": {k: split[k] for k in split if k != "ok"},
        "qx_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "sil_n3_eq_lo_n3_iff_k_eq_4_or_ge_6": True,
            "sil_n3_eq_lo_n3_all_k": False,
            "sil_n3_eq_ST": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "sil_n3_eq_lo_n3_iff_k_eq_4_or_ge_6": "LEMMA",
            "sil_n3_eq_lo_n3_all_k": "KILLED",
            "sil_n3_eq_ST": "KILLED",
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
        "rest_split n_ok",
        dump["rest_split"]["n_ok"],
        "k0",
        dump["rest_split"]["rows"]["0"],
        "k4",
        dump["rest_split"]["rows"]["4"],
        "k6_eq",
        dump["rest_split"]["rows"]["6"]["eq"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
