#!/usr/bin/env python3
"""Cycle EI: leftover after extra 57888 cannot hold odd 87468.

The 57888 second-even group lands from k=8 entirely in annulus k=15 at
packed (58144,58399]. Remaining extra to 87468 is 29580. That is
strictly less than worst-case leftover 2^15=32768, so threshold(29580)=15
equals the landing k and a later odd can fit in the worst case. Actual
leftover after the image is at most 65536-58144=7392<29580, so 87468
cannot sit in the same k=15 high half on this path. Kills: remaining
after 57888 exceeds 2^15. Do not claim leftover empty at k=16; do not
claim packed 58287; do not claim a closed form for 29580/87468. Not a
prize claim.

Run: python3 research/cycle_ei.py --certify
Dump: research/cycle_ei.json
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
from cycle_ed import threshold
from cycle_ee import image_one_annulus
from cycle_ef import EXTRA87468, PRIZE8
from cycle_eh import EXTRA57888

OUT = Path(__file__).resolve().with_suffix(".json")
EH_JSON = Path(__file__).resolve().parent / "cycle_eh.json"
REM = EXTRA87468 - EXTRA57888  # 29580
K15 = 1 << 15
K16 = 1 << 16


def second_even_gap() -> dict:
    land = image_one_annulus(8, EXTRA57888)
    v = threshold(REM)
    left_lo = K16 - land["lo"]
    left_hi = K16 - land["hi"]
    left_max = max(left_lo, left_hi)
    ok = (
        land["ok"]
        and land["k_lo"] == 15
        and land["k_hi"] == 15
        and REM == 29580
        and v == 15
        and (1 << 14) < REM <= K15
        and REM < K15
        and left_max < REM
        and land["lo"] == 58144
        and land["hi"] == 58399
        and left_hi == 7137
        and left_lo == 7392
    )
    return {
        "ok": ok,
        "land": {k: land[k] for k in ("lo", "hi", "k_lo", "k_hi")},
        "rem": REM,
        "v_rem": v,
        "k15_worst": K15,
        "left_lo": left_lo,
        "left_hi": left_hi,
        "worst_fits": K15 >= REM,
        "actual_fits": left_max >= REM,
    }


def eh_prefix() -> dict:
    eh = json.loads(EH_JSON.read_text())
    ok = (
        eh["checks"]["all_ok"]
        and eh["family"]["n57888"] == 12
        and eh["family"]["n87468"] == 6
        and eh["family"]["prize_e2"] == EXTRA57888
        and eh["verdict"]["extra57888_k8_lands_k15"] == "LEMMA"
        and eh["verdict"]["prize_hits_72177_or_rowland_72577"] == "KILLED"
        and PRIZE8 not in eh["family"]["g72177"]
    )
    return {"ok": ok}


def self_checks(c20, gap: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gap["ok"] and pref["ok"]
    assert gap["rem"] == 29580 < K15
    assert gap["v_rem"] == 15 == gap["land"]["k_lo"]
    assert gap["worst_fits"] is True
    assert gap["actual_fits"] is False
    assert gap["left_hi"] == 7137 < gap["rem"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gap = second_even_gap()
    pref = eh_prefix()
    checks = self_checks(c20, gap, pref)
    dump = {
        "cycle": "EI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "gap": {
            "rem": gap["rem"],
            "v_rem": gap["v_rem"],
            "k15_worst": gap["k15_worst"],
            "left_lo": gap["left_lo"],
            "left_hi": gap["left_hi"],
            "worst_fits": gap["worst_fits"],
            "actual_fits": gap["actual_fits"],
            "land": gap["land"],
        },
        "lemmas": {
            "rem87468_after_57888_is_29580": True,
            "threshold_29580_is_15": True,
            "worst_k15_leftover_can_fit_29580": True,
            "actual_57888_image_leftover_cannot_fit_87468": True,
            "remaining_after_57888_exceeds_2_15": False,
            "leftover_empty_at_k16": None,
            "packed_second_k15_even_is_58287": None,
            "n29580_closed_form": None,
            "at_most_one_odd_all_k": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "rem87468_after_57888_is_29580": "LEMMA",
            "threshold_29580_is_15": "LEMMA",
            "worst_k15_leftover_can_fit_29580": "LEMMA",
            "actual_57888_image_leftover_cannot_fit_87468": "LEMMA",
            "remaining_after_57888_exceeds_2_15": "KILLED",
            "leftover_empty_at_k16": "PREFIX",
            "packed_second_k15_even_is_58287": "PREFIX",
            "n29580_closed_form": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
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
    print("gap", dump["gap"])


if __name__ == "__main__":
    main()
