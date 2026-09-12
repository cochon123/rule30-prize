#!/usr/bin/env python3
"""Cycle EM: every n0=2 scar has at most one odd in k=18; seed at k=19.

Cycle EL: n0=2 scars have at most one odd in k=17 and the period-H seed
at k=18. The last n0=8 holdout 00001101 (72177 group, no odd in 261633)
first-odds at extra 271197, which lands in k=18. Leftover after that
image is 252580<E16, so no second ident-0 in k=18 leftover. The nine
words that already odd-doubled at k=16 or k=17 are n0=16; Cycle DR has
no ident-0 in 262144 extras, and extra 262145 from k=16 or k=17 lands
in k=18, with a second such extra past k=18. Hence at most one odd in
k=18 on every n0=2 scar, and pi_19 in {16,32,64} divides 2^18. Kills:
00001101 never odd-doubles; every n0=2 scar skips k=18. Do not claim a
closed form for 271197; do not bump n0=8 past 523777 or n0=16 past
2^18; do not claim the seed for all k. Not a prize claim.

Run: python3 research/cycle_em.py --certify
Dump: research/cycle_em.json
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
from cycle_ef import first_odd_continue
from cycle_eh import ident0_events
from cycle_ek import E16, ODD_COUNTS_1_15

OUT = Path(__file__).resolve().with_suffix(".json")
EL_JSON = Path(__file__).resolve().parent / "cycle_el.json"
DR_JSON = Path(__file__).resolve().parent / "cycle_dr.json"
EH_JSON = Path(__file__).resolve().parent / "cycle_eh.json"
K19 = 1 << 19
MAX_K18 = K19 - ((1 << 9) - 1)  # 523777: image hi=511+E stays <= 2^19
EXTRA271197 = 271197
HOLD = "00001101"
EVEN_K17 = (165350, 174051, 179001)


def holdout_odd() -> dict:
    """00001101 first-odds at 271197 after only even ident-0s."""
    t0 = [int(c) for c in HOLD]
    cur = first_odd_continue(t0, MAX_K18)
    ev = ident0_events(t0, MAX_K18)
    kinds = [(e, k) for e, k, _ in ev]
    ok = (
        cur == EXTRA271197
        and kinds[-1] == (EXTRA271197, "odd")
        and all(k == "even" for _, k in kinds[:-1])
        and kinds[0] == (52809, "even")
        and kinds[1] == (72177, "even")
        and tuple(e for e, k in kinds[2:-1] if k == "even") == EVEN_K17
        and not any(k == "wrap" for _, k in kinds)
    )
    return {
        "ok": ok,
        "odd": cur,
        "events": kinds,
        "n_even": sum(1 for _, k in kinds if k == "even"),
    }


def k18_window() -> dict:
    land = image_one_annulus(8, EXTRA271197)
    left = K19 - land["hi"]
    e16_16 = image_one_annulus(16, E16)
    e16_17 = image_one_annulus(17, E16)
    second_from_18_lo = e16_16["lo"] + E16 - 1
    second_from_17_lo = e16_17["lo"] + E16 - 1
    ok = (
        land["ok"]
        and land["k_lo"] == 18
        and land["k_hi"] == 18
        and land["lo"] == 271453
        and land["hi"] == 271708
        and left == 252580
        and left < E16
        and MAX_K18 == 523777
        and EXTRA271197 <= MAX_K18
        and e16_16["ok"]
        and e16_16["k_lo"] == 18
        and e16_16["k_hi"] == 18
        and e16_16["lo"] == 327681
        and e16_16["hi"] == 393216
        and e16_17["ok"]
        and e16_17["k_lo"] == 18
        and e16_17["k_hi"] == 18
        and e16_17["lo"] == 393217
        and e16_17["hi"] == 524288
        and second_from_18_lo > K19
        and second_from_17_lo > K19
    )
    return {
        "ok": ok,
        "land": {k: land[k] for k in ("lo", "hi", "k_lo", "k_hi")},
        "leftover": left,
        "k18_need": MAX_K18,
        "e16_from_k16": {k: e16_16[k] for k in ("lo", "hi", "k_lo", "k_hi")},
        "e16_from_k17": {k: e16_17[k] for k in ("lo", "hi", "k_lo", "k_hi")},
        "second_packed_after_k16_e16": second_from_18_lo,
        "second_packed_after_k17_e16": second_from_17_lo,
    }


def seed_k19() -> dict:
    pis = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                pis.append(pi_from_odds(ODD_COUNTS_1_15 + [a, b, c]))
    h = 1 << 18
    ok = (
        set(pis) == {16, 32, 64}
        and all(h % p == 0 for p in pis)
        and seed_from_at_most_one(19)
        and max(ODD_COUNTS_1_15) <= 1
    )
    return {
        "ok": ok,
        "pi_min": min(pis),
        "pi_max": max(pis),
        "H19": h,
        "pis": sorted(set(pis)),
    }


def prefixes() -> dict:
    el = json.loads(EL_JSON.read_text())
    dr = json.loads(DR_JSON.read_text())
    eh = json.loads(EH_JSON.read_text())
    ok = (
        el["checks"]["all_ok"]
        and el["verdict"]["at_most_one_odd_k17_on_n0_2"] == "LEMMA"
        and el["verdict"]["period_H_seed_at_k18_every_n0_2"] == "LEMMA"
        and el["family"]["none"] == [HOLD]
        and el["family"]["n228939"] == 6
        and el["family"]["n87468"] == 6
        and dr["checks"]["all_ok"]
        and dr["n16"]["n_hit"] == 0
        and dr["n16"]["E16"] == E16
        and dr["verdict"]["n0_16_odd_at_k_9_to_16_skips_k17"] == "LEMMA"
        and eh["checks"]["all_ok"]
        and HOLD in eh["family"]["g72177"]
    )
    return {"ok": ok}


def self_checks(c20, hold: dict, win: dict, seed: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert hold["ok"] and win["ok"] and seed["ok"] and pref["ok"]
    assert hold["odd"] == EXTRA271197
    assert win["land"]["k_lo"] == 18 and win["leftover"] < E16
    assert win["e16_from_k16"]["k_lo"] == 18
    assert win["e16_from_k17"]["k_lo"] == 18
    assert seed["pi_max"] == 64 and seed["H19"] == 1 << 18
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    hold = holdout_odd()
    win = k18_window()
    seed = seed_k19()
    pref = prefixes()
    checks = self_checks(c20, hold, win, seed, pref)
    dump = {
        "cycle": "EM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "holdout": {
            "T0": HOLD,
            "odd": hold.get("odd"),
            "events": hold.get("events"),
            "n_even": hold.get("n_even"),
        },
        "k18": {
            "ok": win["ok"],
            "land": win["land"],
            "leftover": win["leftover"],
            "k18_need": win["k18_need"],
            "e16_from_k16": win["e16_from_k16"],
            "e16_from_k17": win["e16_from_k17"],
        },
        "seed_k19": {
            "pi_min": seed["pi_min"],
            "pi_max": seed["pi_max"],
            "H19": seed["H19"],
            "pis": seed["pis"],
        },
        "lemmas": {
            "extra271197_k8_lands_k18": True,
            "k18_leftover_after_271197_lt_E16": True,
            "max_k18_covers_window_from_k8": True,
            "holdout_00001101_odd_271197": True,
            "e16_from_k16_or_k17_lands_k18": True,
            "at_most_one_odd_k18_on_n0_2": True,
            "period_H_seed_at_k19_every_n0_2": True,
            "word_00001101_never_odd": False,
            "every_n0_2_skips_k18": False,
            "n271197_closed_form": None,
            "leftover_after_271197_empty_later_k": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "pi_formula_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "extra271197_k8_lands_k18": "LEMMA",
            "k18_leftover_after_271197_lt_E16": "LEMMA",
            "max_k18_covers_window_from_k8": "LEMMA",
            "holdout_00001101_odd_271197": "LEMMA",
            "e16_from_k16_or_k17_lands_k18": "LEMMA",
            "at_most_one_odd_k18_on_n0_2": "LEMMA",
            "period_H_seed_at_k19_every_n0_2": "LEMMA",
            "word_00001101_never_odd": "KILLED",
            "every_n0_2_skips_k18": "KILLED",
            "n271197_closed_form": "PREFIX",
            "leftover_after_271197_empty_later_k": "PREFIX",
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
    print("holdout", dump["holdout"])
    print("k18", {k: win[k] for k in ("land", "leftover", "k18_need")})
    print("seed_k19", dump["seed_k19"])


if __name__ == "__main__":
    main()
