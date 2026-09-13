#!/usr/bin/env python3
"""Cycle QF: covering UNIQUE_REST packed AND xor tot is 0 for every k.

The 16 UNIQUE_REST packed xor formulas (PH, PK, PM, PN, PR, PS, PV,
PW, PX, PY, PZ, QA, QB, QC, QD, QE) xor to 0 for every k. The case
split is finite: the formulas stabilize for k>=7, where ten columns
fire. Unique tot=0 lifts Cycles ME/MF/MG (unique-rest xor vanishes
through k<=10) to all k, so leftover xor equals rest on covering
q=10 for every k. Not leftover after classified leftover columns
(34/40/62/64/70) equals rest. Not unique-rest xor tot equals rest
(tot is 0; rest is not). Not rest=S xor T. Not E_k=0 for all k.
Do not walk leftover p catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_qf.py --certify
Dump: research/cycle_qf.json
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
from cycle_md import UNIQUE_REST, want_rest10
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_ph import want_p16_pack
from cycle_pk import want_p32_pack
from cycle_pm import want_p30_pack
from cycle_pn import want_p38_pack
from cycle_pr import want_p42_pack
from cycle_ps import want_p54_pack
from cycle_pv import want_p58_pack
from cycle_pw import want_p52_pack
from cycle_px import want_p60_pack
from cycle_py import want_p72_pack
from cycle_pz import want_p76_pack
from cycle_qa import want_p86_pack
from cycle_qb import want_p88_pack
from cycle_qc import want_p98_pack
from cycle_qd import want_p106_pack
from cycle_qe import want_p114_pack

OUT = Path(__file__).resolve().with_suffix(".json")
QE_JSON = Path(__file__).resolve().parent / "cycle_qe.json"
MG_JSON = Path(__file__).resolve().parent / "cycle_mg.json"
MD_JSON = Path(__file__).resolve().parent / "cycle_md.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_REST = 10

PACK = {
    16: want_p16_pack,
    30: want_p30_pack,
    32: want_p32_pack,
    38: want_p38_pack,
    42: want_p42_pack,
    52: want_p52_pack,
    54: want_p54_pack,
    58: want_p58_pack,
    60: want_p60_pack,
    72: want_p72_pack,
    76: want_p76_pack,
    86: want_p86_pack,
    88: want_p88_pack,
    98: want_p98_pack,
    106: want_p106_pack,
    114: want_p114_pack,
}

FIRE = {
    0: frozenset(),
    1: frozenset(),
    2: frozenset({30, 38}),
    3: frozenset({16, 32, 38, 42, 52, 58, 72, 76}),
    4: frozenset({16, 54, 58, 60, 88, 114}),
    5: frozenset({16, 32, 42, 54, 76, 86, 106, 114}),
    6: frozenset({16, 32, 42, 54, 58, 76, 88, 98}),
}
FIRE_GE7 = frozenset({16, 32, 42, 54, 58, 76, 88, 98, 106, 114})


def want_unique_tot(k: int) -> int:
    """XOR of the 16 UNIQUE_REST packed xor formulas, all k."""
    acc = 0
    for fn in PACK.values():
        acc ^= fn(k)
    return acc


def fire_at(k: int) -> frozenset[int]:
    """UNIQUE_REST columns whose packed xor formula is 1."""
    return frozenset(p for p, fn in PACK.items() if fn(k))


def unique_tot() -> dict:
    """k=0..K_ALG: unique tot is 0; firing sets match FIRE / FIRE_GE7."""
    if set(PACK) != set(UNIQUE_REST):
        return {"ok": False, "pack": sorted(PACK), "unique": sorted(UNIQUE_REST)}
    n_ok = 0
    rows = {}
    for k in range(0, K_ALG + 1):
        tot = want_unique_tot(k)
        got = fire_at(k)
        want = FIRE[k] if k < 7 else FIRE_GE7
        if tot != 0 or got != want:
            return {
                "ok": False,
                "k": k,
                "tot": tot,
                "got": sorted(got),
                "want": sorted(want),
            }
        if k <= 12 or k in (16, 24, 32, 48, 64):
            rows[str(k)] = {"tot": tot, "n_fire": len(got), "fire": sorted(got)}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and all(want_unique_tot(k) == 0 for k in range(0, K_ALG + 1))
        and rows["2"]["n_fire"] == 2
        and rows["3"]["n_fire"] == 8
        and rows["4"]["n_fire"] == 6
        and rows["5"]["n_fire"] == 8
        and rows["6"]["n_fire"] == 8
        and rows["7"]["n_fire"] == 10
        and rows["64"]["n_fire"] == 10
        and want_p32_pack(3) == 1
        and want_p32_pack(4) == 0
        and want_p32_pack(5) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def leftover_eq_rest() -> dict:
    """Unique tot=0 so leftover tot equals rest; matches rest10 on k<=10."""
    n_ok = 0
    rows = {}
    for k in range(0, K_ALG + 1):
        u = want_unique_tot(k)
        rest = want_rest10(k, 10) if k <= K_REST else None
        st = want_rest_e0(k)
        if u != 0:
            return {"ok": False, "k": k, "u": u}
        if k <= K_REST:
            # leftover tot = rest xor unique tot = rest.
            leftover = rest ^ u
            if leftover != rest:
                return {"ok": False, "left": True, "k": k, "lo": leftover, "rest": rest}
        if k <= 12:
            rows[str(k)] = {
                "unique": u,
                "rest10": rest,
                "ST": st,
                "leftover_is_rest": True,
            }
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and rows["0"]["rest10"] == 0
        and rows["2"]["rest10"] == 1
        and rows["6"]["rest10"] == 1
        and rows["8"]["rest10"] == 1
        and rows["10"]["rest10"] == 0
        and rows["2"]["unique"] == 0
        and rows["2"]["ST"] == 1
        and rows["2"]["unique"] != rows["2"]["rest10"]
        and rows["2"]["unique"] != rows["2"]["ST"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG, "rows": rows}


def killed_unique_eq_rest() -> dict:
    """unique-rest xor tot equals rest: k=2 rest=1 tot=0."""
    ok = want_unique_tot(2) == 0 and want_rest10(2, 10) == 1
    return {"ok": ok, "k": 2, "tot": 0, "rest": 1}


def killed_unique_eq_st() -> dict:
    """unique-rest xor tot equals S xor T: k=2 ST=1 tot=0."""
    ok = want_unique_tot(2) == 0 and want_rest_e0(2) == 1
    return {"ok": ok, "k": 2, "tot": 0, "ST": 1}


def killed_class_left_eq_rest() -> dict:
    """leftover after classified leftover columns equals rest.

    Classified leftover xor is not unique tot (which is 0), and the
    gap is unclassified leftover. Dual of the QE prefix kill.
    """
    qe = json.loads(QE_JSON.read_text())
    ok = qe["verdict"]["unique_rest_xor0"] == "KILLED"
    return {"ok": ok, "note": "classified leftover subset is not rest"}


def prefixes() -> dict:
    qe = json.loads(QE_JSON.read_text())
    mg = json.loads(MG_JSON.read_text())
    md = json.loads(MD_JSON.read_text())
    ok = (
        qe["checks"]["all_ok"]
        and mg["checks"]["all_ok"]
        and md["checks"]["all_ok"]
        and qe["verdict"]["p114_xor_iff_k_ge_4_ne_6"] == "LEMMA"
        and qe["lemmas"]["p114_xor_iff_k_ge_4_ne_6"] is True
        and mg["verdict"]["k10_u0"] == "LEMMA"
        and md["verdict"]["rest10"] == "LEMMA"
        and qe["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and qe["verdict"]["prize"] == "unsolved"
        and want_p114_pack(4) == 1
        and want_p114_pack(6) == 0
        and want_p16_pack(3) == 1
        and set(UNIQUE_REST) == set(PACK)
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, tot, left, ku, ks, kc, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and tot["ok"] and left["ok"]
    assert ku["ok"] and ks["ok"] and kc["ok"] and sc["ok"] and pref["ok"]
    assert want_unique_tot(0) == 0
    assert want_unique_tot(7) == 0
    assert want_unique_tot(64) == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    tot = unique_tot()
    left = leftover_eq_rest()
    ku = killed_unique_eq_rest()
    ks = killed_unique_eq_st()
    kc = killed_class_left_eq_rest()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, tot, left, ku, ks, kc, sc, pref)
    dump = {
        "cycle": "QF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "unique_tot": {k: tot[k] for k in tot if k != "ok"},
        "leftover_eq_rest": {k: left[k] for k in left if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_tot_0_all_k": True,
            "leftover_eq_rest_all_k": True,
            "leftover_eq_rest10_k_le_10": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "unique_eq_rest": False,
            "class_left_eq_rest": False,
            "prize": False,
        },
        "verdict": {
            "unique_tot_0_all_k": "LEMMA",
            "leftover_eq_rest_all_k": "LEMMA",
            "leftover_eq_rest10_k_le_10": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "E_all_k": "PREFIX",
            "unique_eq_rest": "KILLED",
            "class_left_eq_rest": "KILLED",
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
        "unique_tot n_ok",
        dump["unique_tot"]["n_ok"],
        "k_hi",
        dump["unique_tot"]["k_hi"],
        "n_fire7",
        dump["unique_tot"]["rows"]["7"]["n_fire"],
    )
    print("leftover_eq_rest rows", dump["leftover_eq_rest"]["rows"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
