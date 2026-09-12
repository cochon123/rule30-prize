#!/usr/bin/env python3
"""Cycle EZ: reconstruct consecutive 11 iff U meets a 0 of A; even-n0 n6 11.

For U=reconstruct(A,B), U_{t+1}=A_t XOR (B_t OR U_t). If U_t=1 then
U_{t+1}=NOT A_t, so consecutive 11 iff some t has U_t=1 and A_t=0.
On an even-n0 scar, an empty n4-pair i has n6[i+1]=n6[i+1+n0]=1
(Cycle EX). Complementary support forbids n4[i+1]=n4[i+1+n0]=1, so at
least one successor is a 0 of n4 with n6=1. That proves consecutive 11
in n6 (Cycle EX certified it exhaustively). Kills: n4=0 implies n6=1.
Do not claim an 11-bit gap; do not claim n6 type N for odd n0; do not
claim a formula for extra 414990; do not bump all n0=16 past 414990.
Not a prize claim.

Run: python3 research/cycle_ez.py --certify
Dump: research/cycle_ez.json
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
from cycle_dv import mask_bits, odd_copy
from cycle_er import U32
from cycle_ev import has11
from cycle_ew import scar_n3_to_n6
from cycle_ex import empty_slots

OUT = Path(__file__).resolve().with_suffix(".json")
EX_JSON = Path(__file__).resolve().parent / "cycle_ex.json"
EY_JSON = Path(__file__).resolve().parent / "cycle_ey.json"


def cons11_iff_meet_zero() -> dict:
    """U consecutive 11 iff some t has U_t=1 and A_t=0. Length 2..8."""
    n_ok = 0
    n_cons = 0
    for n in range(2, 9):
        for ma in range(1 << n):
            a = [(ma >> t) & 1 for t in range(n)]
            for mb in range(1, 1 << n):
                b = [(mb >> t) & 1 for t in range(n)]
                u = reconstruct(a, b)
                if u is None:
                    continue
                cons = any(u[t] == 1 and u[(t + 1) % n] == 1 for t in range(n))
                meet = any(u[t] == 1 and a[t] == 0 for t in range(n))
                if cons != meet:
                    return {"ok": False, "n": n, "ma": ma, "mb": mb}
                n_ok += 1
                if cons:
                    n_cons += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_cons": n_cons}


def scar_successor_hit() -> dict:
    """Empty-pair successors: complementary pigeonhole hits n6=1 on n4=0."""
    n_left = 0
    n_right = 0
    n_both = 0
    n_ok = 0
    n_n4_implies_n6 = 0
    for n0 in range(2, 11, 2):
        L = 2 * n0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            _n3, n4, _n5, n6 = scar_n3_to_n6(t)
            slots = empty_slots(n4, n0)
            if not slots:
                return {"ok": False, "n0": n0, "empty": True}
            hit = False
            left = right = False
            for i in slots:
                u = (i + 1) % L
                up = (i + 1 + n0) % L
                if n6[u] != 1 or n6[up] != 1:
                    return {"ok": False, "n0": n0, "n6": True}
                if n4[u] == 1 and n4[up] == 1:
                    return {"ok": False, "n0": n0, "comp": True}
                if n4[u] == 0:
                    left = True
                    hit = True
                if n4[up] == 0:
                    right = True
                    hit = True
            if not hit:
                return {"ok": False, "n0": n0, "hit": True}
            if not has11(n6):
                return {"ok": False, "n0": n0, "cons": True}
            if left and right:
                n_both += 1
            elif left:
                n_left += 1
            else:
                n_right += 1
            if all(n6[j] == 1 for j in range(L) if n4[j] == 0):
                n_n4_implies_n6 += 1
            n_ok += 1
    if n_n4_implies_n6:
        return {"ok": False, "implies": n_n4_implies_n6}
    return {
        "ok": n_ok == 1364,
        "n_ok": n_ok,
        "n_left": n_left,
        "n_right": n_right,
        "n_both": n_both,
        "n_n4_implies_n6": n_n4_implies_n6,
    }


def tstar() -> dict:
    t = [int(c) for c in U32]
    _n3, n4, _n5, n6 = scar_n3_to_n6(t)
    n0 = 16
    L = 32
    slots = empty_slots(n4, n0)
    hit = False
    for i in slots:
        u = (i + 1) % L
        up = (i + 1 + n0) % L
        if n6[u] != 1 or n6[up] != 1:
            return {"ok": False, "n6": True}
        if n4[u] == 1 and n4[up] == 1:
            return {"ok": False, "comp": True}
        if n4[u] == 0 or n4[up] == 0:
            hit = True
    ok = hit and has11(n6) and not all(
        n6[j] == 1 for j in range(L) if n4[j] == 0
    )
    return {"ok": ok, "z": len(slots), "n6_has11": has11(n6)}


def prefixes() -> dict:
    ex = json.loads(EX_JSON.read_text())
    ey = json.loads(EY_JSON.read_text())
    ok = (
        ex["checks"]["all_ok"]
        and ey["checks"]["all_ok"]
        and ex["verdict"]["empty_n4_pair_next_n6_11"] == "LEMMA"
        and ex["verdict"]["n4_complementary_support"] == "LEMMA"
        and ey["verdict"]["even_n0_n4_has_00"] == "LEMMA"
        and ex["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gen: dict, scar: dict, ts: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gen["ok"] and scar["ok"] and ts["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gen = cons11_iff_meet_zero()
    scar = scar_successor_hit()
    ts = tstar()
    pref = prefixes()
    checks = self_checks(c20, gen, scar, ts, pref)
    dump = {
        "cycle": "EZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "general": {k: gen[k] for k in gen if k != "ok"},
        "scar": {k: scar[k] for k in scar if k != "ok"},
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "lemmas": {
            "cons11_iff_U_meets_zero_of_A": True,
            "empty_successor_complementary_hits": True,
            "even_n0_n6_consecutive_11_proved": True,
            "n4_zero_implies_n6_one": False,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cons11_iff_U_meets_zero_of_A": "LEMMA",
            "empty_successor_complementary_hits": "LEMMA",
            "even_n0_n6_consecutive_11_proved": "LEMMA",
            "n4_zero_implies_n6_one": "KILLED",
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
    print("general", dump["general"])
    print("scar", dump["scar"])
    print("tstar", dump["tstar"])


if __name__ == "__main__":
    main()
