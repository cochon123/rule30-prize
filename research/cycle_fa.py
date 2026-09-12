#!/usr/bin/env python3
"""Cycle FA: even-n0 n5 consecutive 11 via O-type xor at empty n4-pair.

n3 is O-type, so n3[i] XOR n3[i+n0]=1. An empty n4-pair has n5=11
(Cycle EX). Consecutive 11 iff U=1 on a 0 of A (Cycle EZ), here
A=n3 and U=n5, so the 0 of that n3-pair is a meet. That proves
consecutive 11 in n5. Kills: n5 always has 00 (124 of 1364 lack it);
n7 always type N (440 O-type). Do not claim n7 consecutive 11 as a
production; do not claim an 11-bit gap; do not claim a formula for
extra 414990; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fa.py --certify
Dump: research/cycle_fa.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_cb import twocopy_type
from cycle_dv import mask_bits, odd_copy
from cycle_er import U32
from cycle_ev import has00, has11
from cycle_ew import scar_n3_to_n6
from cycle_ex import empty_slots

OUT = Path(__file__).resolve().with_suffix(".json")
EZ_JSON = Path(__file__).resolve().parent / "cycle_ez.json"
EX_JSON = Path(__file__).resolve().parent / "cycle_ex.json"


def n5_meet_at_empty() -> dict:
    """O-type xor at empty n4-pair hits n5=1 on a 0 of n3."""
    n_ok = 0
    n_n5_00 = 0
    n_n5_no00 = 0
    n7_O = 0
    n7_N = 0
    n7_11 = 0
    for n0 in range(2, 11, 2):
        L = 2 * n0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            n3, n4, n5, n6 = scar_n3_to_n6(t)
            if twocopy_type(n3) != "O":
                return {"ok": False, "n0": n0, "n3": True}
            slots = empty_slots(n4, n0)
            if not slots:
                return {"ok": False, "n0": n0, "empty": True}
            hit = False
            for i in slots:
                if n3[i] == n3[i + n0]:
                    return {"ok": False, "n0": n0, "xor": True}
                if n5[i] != 1 or n5[i + n0] != 1:
                    return {"ok": False, "n0": n0, "n5": True}
                if (n5[i] == 1 and n3[i] == 0) or (
                    n5[i + n0] == 1 and n3[i + n0] == 0
                ):
                    hit = True
            if not hit:
                return {"ok": False, "n0": n0, "hit": True}
            if not has11(n5):
                return {"ok": False, "n0": n0, "cons": True}
            if has00(n5):
                n_n5_00 += 1
            else:
                n_n5_no00 += 1
            n7 = reconstruct(n5, n6)
            if n7 is None:
                return {"ok": False, "n0": n0, "n7": True}
            ty = twocopy_type(n7)
            if ty == "O":
                n7_O += 1
            elif ty == "N":
                n7_N += 1
            else:
                return {"ok": False, "n0": n0, "n7ty": ty}
            if has11(n7):
                n7_11 += 1
            n_ok += 1
    if n_n5_no00 == 0:
        return {"ok": False, "n5_always_00": True}
    if n7_O == 0:
        return {"ok": False, "n7_always_N": True}
    return {
        "ok": n_ok == 1364 and n_n5_no00 == 124 and n7_O == 440,
        "n_ok": n_ok,
        "n_n5_00": n_n5_00,
        "n_n5_no00": n_n5_no00,
        "n7_O": n7_O,
        "n7_N": n7_N,
        "n7_11": n7_11,
    }


def tstar() -> dict:
    t = [int(c) for c in U32]
    n3, n4, n5, n6 = scar_n3_to_n6(t)
    n0 = 16
    slots = empty_slots(n4, n0)
    hit = False
    for i in slots:
        if n3[i] == n3[i + n0] or n5[i] != 1 or n5[i + n0] != 1:
            return {"ok": False}
        if (n5[i] == 1 and n3[i] == 0) or (
            n5[i + n0] == 1 and n3[i + n0] == 0
        ):
            hit = True
    n7 = reconstruct(n5, n6)
    ok = (
        hit
        and has11(n5)
        and has00(n5)
        and n7 is not None
        and twocopy_type(n7) == "N"
        and has11(n7)
    )
    return {
        "ok": ok,
        "z": len(slots),
        "n5_has11": has11(n5),
        "n5_has00": has00(n5),
        "n7_type": twocopy_type(n7) if n7 is not None else None,
        "wt5": sum(n5),
        "wt7": sum(n7) if n7 is not None else None,
    }


def prefixes() -> dict:
    ez = json.loads(EZ_JSON.read_text())
    ex = json.loads(EX_JSON.read_text())
    ok = (
        ez["checks"]["all_ok"]
        and ex["checks"]["all_ok"]
        and ez["verdict"]["cons11_iff_U_meets_zero_of_A"] == "LEMMA"
        and ex["verdict"]["empty_n4_pair_next_n6_11"] == "LEMMA"
        and ex["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, scar: dict, ts: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert scar["ok"] and ts["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    scar = n5_meet_at_empty()
    ts = tstar()
    pref = prefixes()
    checks = self_checks(c20, scar, ts, pref)
    dump = {
        "cycle": "FA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "scar": {k: scar[k] for k in scar if k != "ok"},
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "lemmas": {
            "even_n0_n5_consecutive_11_proved": True,
            "n5_always_has_00": False,
            "n7_always_type_N": False,
            "n7_consecutive_11": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_n0_n5_consecutive_11_proved": "LEMMA",
            "n5_always_has_00": "KILLED",
            "n7_always_type_N": "KILLED",
            "n7_consecutive_11": "PREFIX",
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
    print("scar", dump["scar"])
    print("tstar", dump["tstar"])


if __name__ == "__main__":
    main()
