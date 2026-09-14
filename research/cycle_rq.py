#!/usr/bin/env python3
"""Cycle RQ: UNIQUE_EVEN Green n%4 equals Green rest n%4 for every k>=6.

Cycle QX/QY Green rest n%4 is (0,1,1,1) for k>=3. Cycle RP UNIQUE_EVEN
Green n%4 is (0,1,1,1) for k>=6. Hence they agree for k>=6: Green rest
on each residue is UNIQUE_EVEN's profile. Dual: leftover Green n%4
equals UNIQUE_ODD Green n%4, both (0,0,0,1), so leftover and UNIQUE_ODD
cancel on n%4==3. Not equal for all k (k=3: Green (0,1,1,1), UNIQUE_EVEN
(1,1,0,1)). Not leftover Green equals UNIQUE_ODD Green for all k.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_rq.py --certify
Dump: research/cycle_rq.json
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
from cycle_rm import want_lo_g_nmod
from cycle_ro import want_ue_g_nmod, want_uo_g_nmod

OUT = Path(__file__).resolve().with_suffix(".json")
RP_JSON = Path(__file__).resolve().parent / "cycle_rp.json"
RO_JSON = Path(__file__).resolve().parent / "cycle_ro.json"
RM_JSON = Path(__file__).resolve().parent / "cycle_rm.json"
QY_JSON = Path(__file__).resolve().parent / "cycle_qy.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64


def want_g_nmod(k: int) -> list[int]:
    return [want_g_n0(k), want_g_n1(k), want_g_n2(k), want_g_n3(k)]


def tot_form() -> dict:
    """k<=K_ALG: UNIQUE_EVEN Green equals Green rest iff k>=6; leftover equals UO."""
    n_ok = 0
    n_eq = 0
    n_lo = 0
    for k in range(0, K_ALG + 1):
        g = want_g_nmod(k)
        ue = want_ue_g_nmod(k)
        lo = want_lo_g_nmod(k)
        uo = want_uo_g_nmod(k)
        xor = [g[i] ^ ue[i] for i in range(4)]
        if xor != [lo[i] ^ uo[i] for i in range(4)]:
            return {"ok": False, "cancel": True, "k": k, "xor": xor}
        eq = ue == g
        if eq != (k >= 6):
            return {"ok": False, "eq": True, "k": k, "g": g, "ue": ue}
        if (lo == uo) != (k >= 6):
            return {"ok": False, "lo": True, "k": k, "lo": lo, "uo": uo}
        if k >= 6:
            if g != [0, 1, 1, 1] or ue != [0, 1, 1, 1]:
                return {"ok": False, "ge6": True, "k": k, "g": g, "ue": ue}
            if lo != [0, 0, 0, 1] or uo != [0, 0, 0, 1]:
                return {"ok": False, "lo_uo": True, "k": k}
            n_eq += 1
            n_lo += 1
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and n_eq == K_ALG - 5
        and n_lo == K_ALG - 5
        and want_g_nmod(3) == [0, 1, 1, 1]
        and want_ue_g_nmod(3) == [1, 1, 0, 1]
        and want_g_nmod(3) != want_ue_g_nmod(3)
        and want_g_nmod(6) == want_ue_g_nmod(6)
        and want_lo_g_nmod(0) != want_uo_g_nmod(0)
        and want_lo_g_nmod(6) == want_uo_g_nmod(6)
    )
    return {"ok": ok, "n_ok": n_ok, "n_eq": n_eq, "n_lo": n_lo, "k_hi": K_ALG}


def prefix_walk() -> dict:
    """Prefix RP/RO/RM walks: UNIQUE_EVEN Green equals Green rest at k=6,8."""
    rp = json.loads(RP_JSON.read_text())
    ro = json.loads(RO_JSON.read_text())
    rm = json.loads(RM_JSON.read_text())
    ue6 = rp["ue_walk"]["rows"]["6"]
    ue8 = rp["ue_walk"]["rows"]["8"]
    ue3 = rp["ue_walk"]["rows"]["3"]
    uo6 = ro["uo_walk"]["rows"]["6"]
    lo6 = rm["green_walk"]["rows"]["6"]["lo"]
    lo0 = rm["green_walk"]["rows"]["0"]["lo"]
    ok = (
        rp["checks"]["all_ok"]
        and ro["checks"]["all_ok"]
        and rm["checks"]["all_ok"]
        and ue6 == [0, 1, 1, 1]
        and ue8 == [0, 1, 1, 1]
        and ue3 == [1, 1, 0, 1]
        and ue6 == want_g_nmod(6)
        and ue8 == want_g_nmod(8)
        and ue3 != want_g_nmod(3)
        and uo6 == [0, 0, 0, 1]
        and lo6 == [0, 0, 0, 1]
        and lo6 == uo6
        and lo0 != want_uo_g_nmod(0)
    )
    return {
        "ok": ok,
        "ue6": ue6,
        "ue8": ue8,
        "ue3": ue3,
        "uo6": uo6,
        "lo6": lo6,
        "lo0": lo0,
    }


def killed_eq() -> dict:
    """UNIQUE_EVEN Green equals Green rest all k; leftover equals UNIQUE_ODD all k."""
    ok = (
        want_g_nmod(0) == [1, 0, 0, 1]
        and want_ue_g_nmod(0) == [0, 0, 0, 0]
        and want_g_nmod(0) != want_ue_g_nmod(0)
        and want_g_nmod(3) != want_ue_g_nmod(3)
        and want_g_nmod(4) == [0, 1, 1, 1]
        and want_ue_g_nmod(4) == [0, 0, 0, 0]
        and want_lo_g_nmod(0) != want_uo_g_nmod(0)
        and want_lo_g_nmod(4) != want_uo_g_nmod(4)
        and want_g_nmod(6) == want_ue_g_nmod(6)
        and want_lo_g_nmod(6) == want_uo_g_nmod(6)
    )
    return {
        "ok": ok,
        "g3": want_g_nmod(3),
        "ue3": want_ue_g_nmod(3),
        "lo4": want_lo_g_nmod(4),
        "uo4": want_uo_g_nmod(4),
    }


def prefixes() -> dict:
    rp = json.loads(RP_JSON.read_text())
    ro = json.loads(RO_JSON.read_text())
    qy = json.loads(QY_JSON.read_text())
    ok = (
        rp["checks"]["all_ok"]
        and ro["checks"]["all_ok"]
        and qy["checks"]["all_ok"]
        and rp["verdict"]["ue_g_nmod_0111_k_ge_6"] == "LEMMA"
        and ro["verdict"]["uo_g_nmod_0001_k_ge_6"] == "LEMMA"
        and qy["verdict"]["green_nmod_0111_k_ge_3"] == "LEMMA"
        and rp["verdict"]["ue_g_nmod_0111_all_k"] == "KILLED"
        and rp["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and rp["verdict"]["prize"] == "unsolved"
        and want_ue_g_nmod(6) == want_g_nmod(6)
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
        "cycle": "RQ",
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
            "ue_g_eq_green_nmod_k_ge_6": True,
            "lo_g_eq_uo_g_nmod_k_ge_6": True,
            "ue_g_eq_green_nmod_all_k": False,
            "lo_g_eq_uo_g_nmod_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ue_g_eq_green_nmod_k_ge_6": "LEMMA",
            "lo_g_eq_uo_g_nmod_k_ge_6": "LEMMA",
            "ue_g_eq_green_nmod_all_k": "KILLED",
            "lo_g_eq_uo_g_nmod_all_k": "KILLED",
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
        "prefix_walk ue6",
        dump["prefix_walk"]["ue6"],
        "g6",
        want_g_nmod(6),
        "lo6",
        dump["prefix_walk"]["lo6"],
        "uo6",
        dump["prefix_walk"]["uo6"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
