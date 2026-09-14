#!/usr/bin/env python3
"""Cycle RC: covering leftover n%4==2 tot equals rest n%4==2 tot for every k.

UNIQUE_REST packed tot on n%4==2 is 0 (Cycle RB), so the rest/unique
partition on that residue is leftover n2 tot = rest n2 tot. Leftover
n0 tot is rest n0 xor unique n0, matching Cycle QO's lo_n0 through
k<=10. Leftover even-n tot is leftover n0 xor leftover n2, equal to
Cycle QT. Not leftover n2 tot equals ST (k=0: 1 vs 0). Not leftover
n2 tot equals leftover even-n tot (k=3: 0 vs 1). Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rc.py --certify
Dump: research/cycle_rc.json
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
from cycle_qt import want_lo_en
from cycle_rb import want_u_n0, want_u_n1, want_u_n2, want_u_n3, want_u_nmod

OUT = Path(__file__).resolve().with_suffix(".json")
QO_JSON = Path(__file__).resolve().parent / "cycle_qo.json"
RB_JSON = Path(__file__).resolve().parent / "cycle_rb.json"
QT_JSON = Path(__file__).resolve().parent / "cycle_qt.json"

N_PAL = 64
M_SLOTS = 64
K_REST = 10
K_ALG = 64


def want_lo_n0(k: int, n0: int) -> int:
    """Leftover n%4==0 tot from rest n0 and unique n0."""
    return n0 ^ want_u_n0(k)


def want_lo_n1(k: int, n1: int) -> int:
    """Leftover n%4==1 tot from rest n1 and unique n1."""
    return n1 ^ want_u_n1(k)


def want_lo_n2(k: int, n2: int) -> int:
    """Leftover n%4==2 tot equals rest n2: unique n2 is 0."""
    return n2


def want_lo_n3(k: int, n3: int) -> int:
    """Leftover n%4==3 tot from rest n3 and unique n3."""
    return n3 ^ want_u_n3(k)


def tot_form() -> dict:
    """k<=K_ALG: unique n2=0 so leftover n2 helper is identity; n0 flips on unique n0."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if want_u_n2(k) != 0:
            return {"ok": False, "u2": True, "k": k}
        if want_lo_n2(k, 0) != 0 or want_lo_n2(k, 1) != 1:
            return {"ok": False, "id": True, "k": k}
        if want_lo_n0(k, 0) != want_u_n0(k):
            return {"ok": False, "n0": True, "k": k}
        if want_lo_n1(k, 0) != want_u_n1(k):
            return {"ok": False, "n1": True, "k": k}
        if want_lo_n3(k, 0) != want_u_n3(k):
            return {"ok": False, "n3": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_u_n2(6) == 0
        and want_lo_n2(0, 1) == 1
        and want_lo_n0(3, 0) == 1
        and want_lo_n0(4, 1) == 1
        and want_u_nmod(6) == [1, 0, 0, 1]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def rest_split() -> dict:
    """k<=10: leftover n%4 from QO rest xor RB unique; n2 equals rest n2."""
    qo = json.loads(QO_JSON.read_text())
    rows_in = qo["rest_n0_walk"]["rows"]
    n_ok = 0
    rows = {}
    for k in range(0, K_REST + 1):
        tot = rows_in[str(k)]["tot"]
        lo = [
            want_lo_n0(k, tot[0]),
            want_lo_n1(k, tot[1]),
            want_lo_n2(k, tot[2]),
            want_lo_n3(k, tot[3]),
        ]
        if lo[2] != tot[2]:
            return {"ok": False, "n2": True, "k": k, "lo": lo, "tot": tot}
        if lo[0] != rows_in[str(k)]["lo_n0"]:
            return {"ok": False, "n0": True, "k": k, "lo0": lo[0]}
        if rows_in[str(k)]["u_n0"] != want_u_n0(k):
            return {"ok": False, "u0": True, "k": k}
        even_rest = tot[0] ^ tot[2]
        if (lo[0] ^ lo[2]) != want_lo_en(k, even_rest):
            return {"ok": False, "even": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"tot": tot, "lo": lo, "u": want_u_nmod(k)}
    ok = (
        n_ok == K_REST + 1
        and rows["0"]["lo"][2] == 1
        and rows["3"]["lo"][2] == 0
        and rows["6"]["lo"][2] == 0
        and rows["8"]["lo"][0] == 0
        and rows["10"]["lo"][2] == 0
        and rows["6"]["lo"] == [1, 1, 0, 1]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_REST, "rows": rows}


def killed_eq() -> dict:
    """Leftover n2 tot equals ST, and equals leftover even-n tot."""
    qo = json.loads(QO_JSON.read_text())
    r0 = qo["rest_n0_walk"]["rows"]["0"]
    r3 = qo["rest_n0_walk"]["rows"]["3"]
    r6 = qo["rest_n0_walk"]["rows"]["6"]
    lo2_0 = want_lo_n2(0, r0["tot"][2])
    lo2_3 = want_lo_n2(3, r3["tot"][2])
    lo2_6 = want_lo_n2(6, r6["tot"][2])
    even0 = r0["tot"][0] ^ r0["tot"][2]
    even3 = r3["tot"][0] ^ r3["tot"][2]
    lo_e0 = want_lo_en(0, even0)
    lo_e3 = want_lo_en(3, even3)
    ok = (
        lo2_0 == 1
        and want_rest_e0(0) == 0
        and lo2_6 == 0
        and want_rest_e0(6) == 1
        and lo2_3 == 0
        and lo_e3 == 1
        and lo_e0 == 1
        and lo2_0 == lo_e0
    )
    return {
        "ok": ok,
        "lo2_0": lo2_0,
        "st0": 0,
        "lo2_6": lo2_6,
        "st6": 1,
        "lo2_3": lo2_3,
        "lo_e3": lo_e3,
    }


def prefixes() -> dict:
    rb = json.loads(RB_JSON.read_text())
    qo = json.loads(QO_JSON.read_text())
    qt = json.loads(QT_JSON.read_text())
    ok = (
        rb["checks"]["all_ok"]
        and qo["checks"]["all_ok"]
        and qt["checks"]["all_ok"]
        and rb["verdict"]["unique_n2_0"] == "LEMMA"
        and rb["verdict"]["unique_n0_iff_k_eq_3_or_ge_5"] == "LEMMA"
        and qt["verdict"]["lo_en_eq_erest_xor_ue_even"] == "LEMMA"
        and qo["verdict"]["rest_n0_eq_ST_k_minus_2"] == "KILLED"
        and rb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rb["verdict"]["prize"] == "unsolved"
        and want_u_n2(8) == 0
        and want_lo_n2(8, 1) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, split, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and split["ok"]
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
    split = rest_split()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, split, kl, sc, pref)
    dump = {
        "cycle": "RC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "rest_split": {k: split[k] for k in split if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_n2_eq_rest_n2": True,
            "lo_nmod_eq_rest_xor_unique": True,
            "lo_n2_eq_ST": False,
            "lo_n2_eq_lo_even": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_n2_eq_rest_n2": "LEMMA",
            "lo_nmod_eq_rest_xor_unique": "LEMMA",
            "lo_n2_eq_ST": "KILLED",
            "lo_n2_eq_lo_even": "KILLED",
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
        "k0_lo",
        dump["rest_split"]["rows"]["0"]["lo"],
        "k6_lo",
        dump["rest_split"]["rows"]["6"]["lo"],
        "k10_n2",
        dump["rest_split"]["rows"]["10"]["lo"][2],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
