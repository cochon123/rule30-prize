#!/usr/bin/env python3
"""Cycle DQ: n0=16 scars are ident-0-free in 65536 extras; k=16 at most one.

Bit-sliced unique continuation shows all 65536 length-16 T0 have no ident-0
in the next 65536 extras after (0, T0||not T0, 1). That window is 2^16, so
even an odd at the start of the k=16 high half leaves too little room for a
second ident-0. Combined with Cycle DP, at most one ident-0 after an odd
fits in (W,2W] for every 2<=k<=16 and every matching T0. Do not claim a
closed form for a later extra. Not a prize claim.

Run: python3 research/cycle_dq.py --certify
Dump: research/cycle_dq.json
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
from cycle_de import pi_formula
from cycle_dj import leftover
from cycle_dk import PRIZE_U16
from cycle_dn import N_WORDS, census, prize_mask

OUT = Path(__file__).resolve().with_suffix(".json")
DP_JSON = Path(__file__).resolve().parent / "cycle_dp.json"
W16 = 1 << 16
N_EXTRA = W16  # 65536


def dp_prefix() -> dict:
    dp = json.loads(DP_JSON.read_text())
    ok = (
        dp["checks"]["all_ok"]
        and dp["E"]["2"] == 22
        and dp["E"]["8"] == 6344
        and dp["verdict"]["at_most_one_ident0_after_odd_k_2_to_15"] == "LEMMA"
    )
    return {"ok": ok, "E15": dp["E"]}


def high_half_k16(n16: dict) -> dict:
    """Remaining <= W=65536 < min extra, so a second ident-0 cannot fit."""
    e16 = N_EXTRA + 1 if n16["n_hit"] == 0 else n16["min_extra"]
    return {
        "ok": n16["n_hit"] == 0 and n16["n_none"] == N_WORDS and e16 > W16,
        "E16": e16,
        "W": W16,
        "leftover": leftover(16),
        "second_fits_rmax": not (e16 > W16),
        "second_fits_prize_leftover": not (e16 > leftover(16)),
    }


def at_most_one_through_16(E: dict[int, int]) -> bool:
    for k in range(2, 17):
        n0 = pi_formula(k)
        if E[n0] <= (1 << k):
            return False
    return True


def self_checks(c20, dp: dict, n16: dict, k16: dict, all16: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert dp["ok"] and n16["n_hit"] == 0 and k16["ok"] and all16
    pz = prize_mask(PRIZE_U16)
    assert 0 <= pz < N_WORDS and pz not in n16["first"]
    assert leftover(16) == 43205 and k16["E16"] == 65537
    assert not k16["second_fits_rmax"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    dp = dp_prefix()
    n16 = census(16, N_EXTRA)
    k16 = high_half_k16(n16)
    E = {int(k): v for k, v in dp["E15"].items()}
    E[16] = k16["E16"]
    all16 = at_most_one_through_16(E)
    checks = self_checks(c20, dp, n16, k16, all16)
    dump = {
        "cycle": "DQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "n16": {
            "n_extra": N_EXTRA,
            "n_hit": n16["n_hit"],
            "n_none": n16["n_none"],
            "prize_u16": PRIZE_U16,
            "E16": k16["E16"],
        },
        "k16": {
            "W": k16["W"],
            "leftover": k16["leftover"],
            "second_fits_rmax": k16["second_fits_rmax"],
        },
        "lemmas": {
            "n0_16_no_ident0_in_65536": True,
            "k16_all_T0_early_odd_leftover_too_short": True,
            "at_most_one_ident0_after_odd_k_2_to_16": True,
            "n0_16_extras_closed_form": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "n0_16_no_ident0_in_65536": "LEMMA",
            "k16_all_T0_early_odd_leftover_too_short": "LEMMA",
            "at_most_one_ident0_after_odd_k_2_to_16": "LEMMA",
            "n0_16_extras_closed_form": "KILLED",
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
    print("n16", dump["n16"])
    print("k16", dump["k16"])


if __name__ == "__main__":
    main()
