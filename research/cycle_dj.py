#!/usr/bin/env python3
"""Cycle DJ: leftover dyadic high half is shorter than the next odd extra.

After the toggle at packed bits 8,29,400 the leftover in that same high
half is 0, 3, 112 bits. Every length-2 scar waits 22 extras; every
length-4 scar waits 89 or 372; Cycle CG gives 130 ident-0-free extras
for every nonconstant length-8 T0. So 22>0, 89>3, and 112<130: no
second odd ident-0 can fit in the leftover at k=2,4,8, for any matching
T0. Do not claim the next odd lands in a 2-power high half (the n0=4
89-orbit would hit k=6). k=16 leftover 43205 is untouched. Not a prize
claim.

Run: python3 research/cycle_dj.py --certify
Dump: research/cycle_dj.json
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
from cycle_di import len2_at_22, len4_89_or_372

OUT = Path(__file__).resolve().with_suffix(".json")
CG_JSON = Path(__file__).resolve().parent / "cycle_cg.json"
P = {2: 8, 4: 29, 8: 400, 16: 87867}


def leftover(k: int) -> int:
    """Packed bits after the dyadic toggle still inside (W,2W]."""
    return (1 << (k + 1)) - P[k]


def leftovers() -> dict:
    got = {k: leftover(k) for k in P}
    if got != {2: 0, 4: 3, 8: 112, 16: 43205}:
        return {"ok": False, "got": got}
    return {"ok": True, "R": got}


def leftover_too_short(len2: dict, len4: dict) -> dict:
    """Next odd extra does not fit in the leftover at k=2,4,8."""
    cg = json.loads(CG_JSON.read_text())
    e8 = cg["e8"]
    if e8["n0"] != 8 or e8["n_extra"] != 130 or e8["n_none"] != 0 or e8["n_ok"] != 254:
        return {"ok": False, "why": "cg8"}
    e4 = cg["e4"]
    if e4["n0"] != 4 or e4["n_extra"] != 80 or e4["n_none"] != 0:
        return {"ok": False, "why": "cg4"}
    r = {k: leftover(k) for k in (2, 4, 8)}
    if not len2["ok"] or len2["packed"] != 29:
        return {"ok": False, "why": "len2"}
    if not len4["ok"] or len4["packed"] != 400:
        return {"ok": False, "why": "len4"}
    if not (22 > r[2] and 89 > r[4] and 372 > r[4] and r[4] < 80 and r[8] < 130):
        return {"ok": False, "R": r}
    return {
        "ok": True,
        "R": r,
        "E2": 22,
        "E4": (89, 372),
        "cg8_extra": 130,
        "k16_leftover": leftover(16),
    }


def self_checks(c20, R: dict, gap: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert R["ok"] and gap["ok"] and gap["R"][8] == 112 and gap["k16_leftover"] == 43205
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    len2 = len2_at_22()
    len4 = len4_89_or_372()
    R = leftovers()
    gap = leftover_too_short(len2, len4)
    checks = self_checks(c20, R, gap)
    dump = {
        "cycle": "DJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "leftover": R["R"],
        "gap": {
            "E2": gap["E2"],
            "E4": list(gap["E4"]),
            "cg8_extra": gap["cg8_extra"],
            "k16_leftover": gap["k16_leftover"],
        },
        "lemmas": {
            "leftover_2_4_8_16": True,
            "no_second_odd_in_leftover_k_2_4_8": True,
            "next_odd_always_in_pow2_high_half": False,
            "k16_leftover_too_short": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "leftover_2_4_8_16": "LEMMA",
            "no_second_odd_in_leftover_k_2_4_8": "LEMMA",
            "next_odd_always_in_pow2_high_half": "KILLED",
            "k16_leftover_too_short": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("leftover", dump["leftover"])
    print("gap", dump["gap"])


if __name__ == "__main__":
    main()
