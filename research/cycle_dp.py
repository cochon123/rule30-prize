#!/usr/bin/env python3
"""Cycle DP: at most one ident-0 after an odd in each high half for k<=15.

After an odd doubling at period pi=π_k the post-toggle scar is a length-pi
T0||not T0 drive. Next ident-0 extras are at least 22 (n0=2), 89 (n0=4),
6344 (n0=8), and >43205 (n0=16). Remaining high-half length is at most
2^k. For every 2<=k<=15 that bound is strictly smaller than the matching
min extra, so a second ident-0 cannot fit in the same (W,2W]. At k=16,
2^k=65536>43205, so an early odd could in principle leave room; the prize
toggle at 87867 has leftover 43205, already empty by Cycle DN. Do not claim
at most one for every T0 at k=16. Not a prize claim.

Run: python3 research/cycle_dp.py --certify
Dump: research/cycle_dp.json
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
from cycle_de import EXPECTED_ODD_P, pi_formula
from cycle_dj import leftover

OUT = Path(__file__).resolve().with_suffix(".json")
DI_JSON = Path(__file__).resolve().parent / "cycle_di.json"
DM_JSON = Path(__file__).resolve().parent / "cycle_dm.json"
DN_JSON = Path(__file__).resolve().parent / "cycle_dn.json"
DO_JSON = Path(__file__).resolve().parent / "cycle_do.json"


def min_extras() -> dict:
    di = json.loads(DI_JSON.read_text())
    dm = json.loads(DM_JSON.read_text())
    dn = json.loads(DN_JSON.read_text())
    e2 = di["len2"]["extra"]
    e4 = 89
    e8 = dm["n8"]["min_nonconst"]
    e16 = dn["n16"]["n_extra"] + 1  # no hit in 43205 extras
    ok = (
        di["checks"]["all_ok"]
        and dm["checks"]["all_ok"]
        and dn["checks"]["all_ok"]
        and e2 == 22
        and di["len4"]["n89"] == 8
        and e8 == 6344
        and dn["n16"]["n_hit"] == 0
        and dn["n16"]["n_extra"] == 43205
        and leftover(2) == 0
        and leftover(4) == 3
        and leftover(8) == 112
        and leftover(16) == 43205
    )
    return {"ok": ok, "E": {2: e2, 4: e4, 8: e8, 16: e16}}


def high_half_fits(E: dict[int, int]) -> dict:
    """Second ident-0 cannot fit in (W,2W] for 2<=k<=15."""
    rows: dict[int, dict] = {}
    for k in range(2, 17):
        n0 = pi_formula(k)
        W = 1 << k
        e = E[n0]
        rmax = W
        r_prize = leftover(k) if k in EXPECTED_ODD_P else None
        fits_rmax = e > rmax
        fits_prize = r_prize is None or e > r_prize or (
            k == 16 and r_prize == 43205 and e == 43206
        )
        rows[k] = {
            "pi": n0,
            "W": W,
            "E": e,
            "rmax": rmax,
            "leftover": r_prize,
            "second_fits_rmax": not fits_rmax,
            "second_fits_prize_leftover": not fits_prize,
        }
    ok15 = all(not rows[k]["second_fits_rmax"] for k in range(2, 16))
    ok16_rmax = rows[16]["second_fits_rmax"]  # True: 65536 >= 43206
    ok16_prize = not rows[16]["second_fits_prize_leftover"]
    return {
        "ok": ok15 and ok16_rmax and ok16_prize,
        "rows": rows,
        "at_most_one_k_2_to_15": ok15,
        "k16_rmax_too_long": ok16_rmax,
        "k16_prize_leftover_short": ok16_prize,
    }


def do_prefix() -> bool:
    do = json.loads(DO_JSON.read_text())
    return (
        do["checks"]["all_ok"]
        and do["pi_19"] == 32
        and do["high"]["17"]["n_odd"] == 0
        and do["high"]["19"]["n_odd"] == 0
    )


def self_checks(c20, mins: dict, fit: dict, do_ok: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mins["ok"] and fit["ok"] and do_ok
    assert mins["E"] == {2: 22, 4: 89, 8: 6344, 16: 43206}
    assert fit["at_most_one_k_2_to_15"] and fit["k16_rmax_too_long"]
    assert fit["k16_prize_leftover_short"]
    assert not fit["rows"][15]["second_fits_rmax"]
    assert fit["rows"][16]["second_fits_rmax"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mins = min_extras()
    fit = high_half_fits(mins["E"])
    do_ok = do_prefix()
    checks = self_checks(c20, mins, fit, do_ok)
    dump = {
        "cycle": "DP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "E": mins["E"],
        "k16_W": 1 << 16,
        "k16_leftover": leftover(16),
        "lemmas": {
            "at_most_one_ident0_after_odd_k_2_to_15": True,
            "k16_prize_leftover_too_short": True,
            "k16_all_T0_early_odd_leftover_too_short": False,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "at_most_one_ident0_after_odd_k_2_to_15": "LEMMA",
            "k16_prize_leftover_too_short": "LEMMA",
            "k16_all_T0_early_odd_leftover_too_short": "KILLED",
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
    print("E", dump["E"])
    print("k16", dump["k16_W"], dump["k16_leftover"])


if __name__ == "__main__":
    main()
