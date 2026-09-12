#!/usr/bin/env python3
"""Cycle FC: even-n0 n7 consecutive 11 by n5-00 / no-00 case split.

If n5 has a 00, some 00 starts at n6=1. Then n7[s+1]=NOT n5[s]=1 and
n5[s+1]=0, so n7 meets a 0 of n5 (Cycle EZ). If n5 has no 00, n7 is
O-type (Cycle FB) and even-n0 O-type has a 11 (Cycle EV). Together
every even-n0 scar has consecutive 11 in n7. Kills: n7 always type N
(already FA); n5-00 aligned with n6=0 at every start. Do not claim an
11-bit gap; do not claim n7 type N; do not claim a formula for extra
414990; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fc.py --certify
Dump: research/cycle_fc.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
FB_JSON = Path(__file__).resolve().parent / "cycle_fb.json"
EV_JSON = Path(__file__).resolve().parent / "cycle_ev.json"
EZ_JSON = Path(__file__).resolve().parent / "cycle_ez.json"


def n7_11_cases() -> dict:
    """has00: n6=1 at some n5-00 start; no00: n7 O-type has 11."""
    n_has = 0
    n_no = 0
    n_align0 = 0
    for n0 in range(2, 11, 2):
        L = 2 * n0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            _n3, _n4, n5, n6 = scar_n3_to_n6(t)
            n7 = reconstruct(n5, n6)
            if n7 is None:
                return {"ok": False, "n0": n0, "n7": True}
            if has00(n5):
                starts = [
                    s
                    for s in range(L)
                    if n5[s] == 0 and n5[(s + 1) % L] == 0
                ]
                if not starts:
                    return {"ok": False, "n0": n0, "starts": True}
                if all(n6[s] == 0 for s in starts):
                    n_align0 += 1
                    return {"ok": False, "n0": n0, "align0": True}
                if not any(n6[s] == 1 for s in starts):
                    return {"ok": False, "n0": n0, "n6": True}
                s = next(s for s in starts if n6[s] == 1)
                if n7[(s + 1) % L] != 1 or n5[(s + 1) % L] != 0:
                    return {"ok": False, "n0": n0, "meet": True}
                n_has += 1
            else:
                if twocopy_type(n7) != "O":
                    return {"ok": False, "n0": n0, "O": True}
                if not has11(n7):
                    return {"ok": False, "n0": n0, "11": True}
                n_no += 1
            if not has11(n7):
                return {"ok": False, "n0": n0, "cons": True}
    if n_align0:
        return {"ok": False, "align0": n_align0}
    return {
        "ok": n_has == 1240 and n_no == 124,
        "n_has00": n_has,
        "n_no00": n_no,
        "n_align0": n_align0,
    }


def tstar() -> dict:
    t = [int(c) for c in U32]
    _n3, _n4, n5, n6 = scar_n3_to_n6(t)
    n7 = reconstruct(n5, n6)
    L = 32
    starts = [s for s in range(L) if n5[s] == 0 and n5[(s + 1) % L] == 0]
    hit = any(n6[s] == 1 for s in starts)
    ok = (
        has00(n5)
        and hit
        and n7 is not None
        and has11(n7)
        and twocopy_type(n7) == "N"
    )
    return {
        "ok": ok,
        "n5_has00": has00(n5),
        "n6_at_00_start": hit,
        "n7_has11": has11(n7) if n7 is not None else False,
        "n7_type": twocopy_type(n7) if n7 is not None else None,
    }


def prefixes() -> dict:
    fb = json.loads(FB_JSON.read_text())
    ev = json.loads(EV_JSON.read_text())
    ez = json.loads(EZ_JSON.read_text())
    ok = (
        fb["checks"]["all_ok"]
        and ev["checks"]["all_ok"]
        and ez["checks"]["all_ok"]
        and fb["verdict"]["n5_00_iff_n6_00"] == "LEMMA"
        and fb["verdict"]["no00_n7_O_type"] == "LEMMA"
        and ev["verdict"]["otype_00_iff_11"] == "LEMMA"
        and ez["verdict"]["cons11_iff_U_meets_zero_of_A"] == "LEMMA"
        and fb["verdict"]["prize"] == "unsolved"
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
    scar = n7_11_cases()
    ts = tstar()
    pref = prefixes()
    checks = self_checks(c20, scar, ts, pref)
    dump = {
        "cycle": "FC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "scar": {k: scar[k] for k in scar if k != "ok"},
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "lemmas": {
            "n5_00_n6_one_at_start": True,
            "has00_n7_consecutive_11": True,
            "no00_n7_O_has_11": True,
            "even_n0_n7_consecutive_11_proved": True,
            "n5_00_all_n6_zero_at_start": False,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n5_00_n6_one_at_start": "LEMMA",
            "has00_n7_consecutive_11": "LEMMA",
            "no00_n7_O_has_11": "LEMMA",
            "even_n0_n7_consecutive_11_proved": "LEMMA",
            "n5_00_all_n6_zero_at_start": "KILLED",
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
