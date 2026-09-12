#!/usr/bin/env python3
"""Cycle EJ: every n0=2 scar has at most one odd in each annulus 2..15.

Every length-2 T0 lifts to FAM372 then even-52809 (Cycles EE/EF). Placed
at k=2, extra 22 lands in k=4 (odd), extra 372 in k=8 (odd), extra 52809
in k=15 (even). Those images skip k=3,5,6,7,9-14. Cycle EI: 87468 cannot
occupy the k=15 leftover. So through k=15 the only odds are at k=2,4,8,
one each. With the k=1 odd, pi_16=16 divides 2^15: every n0=2 scar has
the period-H seed at k=16. Kills nothing new on covering. Do not claim
at-most-one-odd for all k; do not claim the seed for all k; do not claim
k=16 odd for every n0=2 scar. Not a prize claim.

Run: python3 research/cycle_ej.py --certify
Dump: research/cycle_ej.json
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
from cycle_du import pi_from_odds, seed_from_at_most_one
from cycle_ee import image_one_annulus

OUT = Path(__file__).resolve().with_suffix(".json")
EE_JSON = Path(__file__).resolve().parent / "cycle_ee.json"
EF_JSON = Path(__file__).resolve().parent / "cycle_ef.json"
EI_JSON = Path(__file__).resolve().parent / "cycle_ei.json"
DU_JSON = Path(__file__).resolve().parent / "cycle_du.json"
EMPTY_K = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14]
ODD_K = [2, 4, 8]
# odd counts in annuli m=1..15
ODD_COUNTS_1_15 = [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]


def landings_skip() -> dict:
    """Extras 22,372,52809 skip EMPTY_K; 87468 cannot occupy k=15 leftover."""
    r22 = image_one_annulus(2, 22)
    r372 = image_one_annulus(4, 372)
    r52809 = image_one_annulus(8, 52809)
    r89 = image_one_annulus(4, 89)
    ok = (
        r22["ok"]
        and r22["k_lo"] == 4
        and r372["ok"]
        and r372["k_lo"] == 8
        and r52809["ok"]
        and r52809["k_lo"] == 15
        and r89["ok"]
        and r89["k_lo"] == 6
        and r22["k_lo"] not in EMPTY_K
        and r372["k_lo"] not in EMPTY_K
        and r52809["k_lo"] not in EMPTY_K
        and all(k not in ODD_K for k in EMPTY_K)
    )
    return {
        "ok": ok,
        "22": r22,
        "372": r372,
        "52809": r52809,
        "89_k6": r89["k_lo"],
        "empty": EMPTY_K,
        "odd_k": ODD_K,
    }


def seed_k16() -> dict:
    pi = pi_from_odds(ODD_COUNTS_1_15)
    h = 1 << 15
    ok = pi == 16 and h % pi == 0 and seed_from_at_most_one(16)
    if max(ODD_COUNTS_1_15) > 1:
        return {"ok": False, "counts": ODD_COUNTS_1_15}
    if sum(ODD_COUNTS_1_15) != 4:
        return {"ok": False, "sum": sum(ODD_COUNTS_1_15)}
    return {"ok": ok, "pi16": pi, "H16": h, "counts": ODD_COUNTS_1_15}


def prefixes() -> dict:
    ee = json.loads(EE_JSON.read_text())
    ef = json.loads(EF_JSON.read_text())
    ei = json.loads(EI_JSON.read_text())
    du = json.loads(DU_JSON.read_text())
    ok = (
        ee["checks"]["all_ok"]
        and ee["verdict"]["n0_2_lifts_to_FAM372"] == "LEMMA"
        and ee["verdict"]["FAM89_reachable_from_n0_2"] == "KILLED"
        and ee["landings"]["22_from_2"]["k_lo"] == 4
        and ee["landings"]["372_from_4"]["k_lo"] == 8
        and ee["landings"]["89_from_4"]["k_lo"] == 6
        and ef["checks"]["all_ok"]
        and ef["verdict"]["fam372_unfolds_to_52809_even"] == "LEMMA"
        and ef["verdict"]["extra52809_k8_lands_k15"] == "LEMMA"
        and ei["checks"]["all_ok"]
        and ei["gap"]["actual_fits"] is False
        and du["checks"]["all_ok"]
        and du["verdict"]["at_most_one_odd_implies_seed"] == "LEMMA"
        and du["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, land: dict, seed: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert land["ok"] and seed["ok"] and pref["ok"]
    assert land["22"]["k_lo"] == 4 and land["372"]["k_lo"] == 8
    assert land["52809"]["k_lo"] == 15 and land["89_k6"] == 6
    assert seed["pi16"] == 16 and (1 << 15) % 16 == 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    land = landings_skip()
    seed = seed_k16()
    pref = prefixes()
    checks = self_checks(c20, land, seed, pref)
    dump = {
        "cycle": "EJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "empty_k": EMPTY_K,
        "odd_k": ODD_K,
        "landings": {
            "22": {k: land["22"][k] for k in ("lo", "hi", "k_lo", "k_hi")},
            "372": {k: land["372"][k] for k in ("lo", "hi", "k_lo", "k_hi")},
            "52809": {k: land["52809"][k] for k in ("lo", "hi", "k_lo", "k_hi")},
        },
        "seed_k16": {"pi16": seed["pi16"], "H16": seed["H16"], "counts": seed["counts"]},
        "lemmas": {
            "n0_2_odds_only_at_k_2_4_8_through_15": True,
            "n0_2_skips_empty_annuli_3_5_7_9_14": True,
            "k15_even_not_odd": True,
            "at_most_one_odd_annuli_2_to_15_on_n0_2": True,
            "period_H_seed_at_k16_every_n0_2": True,
            "FAM89_would_land_k6": True,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "k16_odd_every_n0_2": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n0_2_odds_only_at_k_2_4_8_through_15": "LEMMA",
            "n0_2_skips_empty_annuli_3_5_7_9_14": "LEMMA",
            "k15_even_not_odd": "LEMMA",
            "at_most_one_odd_annuli_2_to_15_on_n0_2": "LEMMA",
            "period_H_seed_at_k16_every_n0_2": "LEMMA",
            "FAM89_would_land_k6": "LEMMA",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "k16_odd_every_n0_2": "PREFIX",
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
    print("empty_k", dump["empty_k"])
    print("seed_k16", dump["seed_k16"])


if __name__ == "__main__":
    main()
