#!/usr/bin/env python3
"""Cycle EK: every n0=2 scar has at most one odd in k=16; seed at k=17.

Cycle EJ: n0=2 scars have at most one odd in each annulus 2..15 and the
period-H seed at k=16. Extra 87468 from k=8 lands entirely in k=16
(6 of 16 even-52809 words); the other ten, including prize T0, have no
odd in 131000 extras, which covers that k=16 window. After 87468, n0=16
has no ident-0 in 262144 extras (Cycle DR), and leftover after the
87468 image is 43093<262145, so those six words have no second ident-0
in k=16 leftover. Hence at most one odd in k=16 on every n0=2 scar, and
pi_17 in {16,32} divides 2^16. Do not claim a k=16 odd for every n0=2
scar; do not claim the seed for all k; do not bump n0=16 extras. Not a
prize claim.

Run: python3 research/cycle_ek.py --certify
Dump: research/cycle_ek.json
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
from cycle_ef import EXTRA87468, MAX_ODD, PRIZE8

OUT = Path(__file__).resolve().with_suffix(".json")
EJ_JSON = Path(__file__).resolve().parent / "cycle_ej.json"
EH_JSON = Path(__file__).resolve().parent / "cycle_eh.json"
DR_JSON = Path(__file__).resolve().parent / "cycle_dr.json"
K17 = 1 << 17
E16 = 262145
ODD_COUNTS_1_15 = [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]


def k16_window() -> dict:
    land = image_one_annulus(8, EXTRA87468)
    left = K17 - land["hi"]
    k16_need = K17 - ((1 << 9) - 1)  # 130561: extra so image hi=512+E-1 stays <= 2^17
    ok = (
        land["ok"]
        and land["k_lo"] == 16
        and land["k_hi"] == 16
        and land["lo"] == 87724
        and land["hi"] == 87979
        and left == 43093
        and left < E16
        and MAX_ODD > k16_need
    )
    return {
        "ok": ok,
        "land": {k: land[k] for k in ("lo", "hi", "k_lo", "k_hi")},
        "leftover": left,
        "k16_need": k16_need,
        "max_odd": MAX_ODD,
    }


def seed_k17() -> dict:
    pi0 = pi_from_odds(ODD_COUNTS_1_15 + [0])
    pi1 = pi_from_odds(ODD_COUNTS_1_15 + [1])
    h = 1 << 16
    ok = (
        pi0 == 16
        and pi1 == 32
        and h % pi0 == 0
        and h % pi1 == 0
        and seed_from_at_most_one(17)
    )
    return {"ok": ok, "pi_no_k16_odd": pi0, "pi_one_k16_odd": pi1, "H17": h}


def prefixes() -> dict:
    ej = json.loads(EJ_JSON.read_text())
    eh = json.loads(EH_JSON.read_text())
    dr = json.loads(DR_JSON.read_text())
    ok = (
        ej["checks"]["all_ok"]
        and ej["verdict"]["at_most_one_odd_annuli_2_to_15_on_n0_2"] == "LEMMA"
        and ej["verdict"]["period_H_seed_at_k16_every_n0_2"] == "LEMMA"
        and eh["checks"]["all_ok"]
        and eh["family"]["n87468"] == 6
        and eh["family"]["n57888"] == 12
        and PRIZE8 not in eh["family"]["g72177"]
        and eh["family"]["prize_e2"] == 57888
        and dr["checks"]["all_ok"]
        and dr["n16"]["n_hit"] == 0
        and dr["n16"]["E16"] == E16
    )
    return {"ok": ok, "n87468": eh["family"]["n87468"], "n_none": 10}


def self_checks(c20, win: dict, seed: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert win["ok"] and seed["ok"] and pref["ok"]
    assert win["land"]["k_lo"] == 16 and win["leftover"] < E16
    assert win["max_odd"] > win["k16_need"]
    assert seed["pi_no_k16_odd"] == 16 and seed["pi_one_k16_odd"] == 32
    assert pref["n87468"] == 6
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    win = k16_window()
    seed = seed_k17()
    pref = prefixes()
    checks = self_checks(c20, win, seed, pref)
    dump = {
        "cycle": "EK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "k16": win,
        "seed_k17": {
            "pi_no_k16_odd": seed["pi_no_k16_odd"],
            "pi_one_k16_odd": seed["pi_one_k16_odd"],
            "H17": seed["H17"],
        },
        "n87468": pref["n87468"],
        "n_none": pref["n_none"],
        "lemmas": {
            "extra87468_k8_lands_k16": True,
            "k16_leftover_after_87468_lt_E16": True,
            "max_odd_covers_k16_window_from_k8": True,
            "at_most_one_odd_k16_on_n0_2": True,
            "period_H_seed_at_k17_every_n0_2": True,
            "k16_odd_every_n0_2": False,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "extra87468_k8_lands_k16": "LEMMA",
            "k16_leftover_after_87468_lt_E16": "LEMMA",
            "max_odd_covers_k16_window_from_k8": "LEMMA",
            "at_most_one_odd_k16_on_n0_2": "LEMMA",
            "period_H_seed_at_k17_every_n0_2": "LEMMA",
            "k16_odd_every_n0_2": "KILLED",
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
    print("k16", {k: win[k] for k in ("land", "leftover", "k16_need")})
    print("seed_k17", dump["seed_k17"])


if __name__ == "__main__":
    main()
