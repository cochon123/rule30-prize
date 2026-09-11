#!/usr/bin/env python3
"""Cycle ED: second-odd leftover threshold for 2-power n0.

After an odd ident-0 with half-length n0, a second odd fits in the same
high half of annulus k only if leftover can exceed the first odd extra.
Worst-case leftover is 2^k (odd at packed 2^k+1). Extra depends on T0,
not on k, so if n0 persists then 2^k eventually catches extra. The
threshold v(n0) is the least k with 2^k >= min odd extra of that n0:
v(1)=3, v(2)=5, v(4)=7, v(8)=15, v(16)=19, using extras 6, 22, 89,
26357, >262144. Prize 2-power odds sit at k=1,2,4,8,16, all strictly
before v. Kills leftover-always-empty for 2-power n0 at every k (n0=2
at k=5 has 32>=22). Do not claim the next odd is forced before v; do
not claim a formula for v; do not bump n0=16 extras past 2^18. Not a
prize claim.

Run: python3 research/cycle_ed.py --certify
Dump: research/cycle_ed.json
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
from cycle_di import first_odd, mask_bits
from cycle_dj import leftover
from cycle_dm import ODD_EXTRAS, first_ident0_int
EXPECTED_ODD_P = {1: 3, 2: 8, 4: 29, 8: 400, 16: 87867}

OUT = Path(__file__).resolve().with_suffix(".json")
EC_JSON = Path(__file__).resolve().parent / "cycle_ec.json"
DM_JSON = Path(__file__).resolve().parent / "cycle_dm.json"
DR_JSON = Path(__file__).resolve().parent / "cycle_dr.json"
DI_JSON = Path(__file__).resolve().parent / "cycle_di.json"
DE_JSON = Path(__file__).resolve().parent / "cycle_de.json"

MIN_ODD = {1: 6, 2: 22, 4: 89, 8: 26357, 16: 262145}
PRIZE_ODD_K = {1: 1, 2: 2, 4: 4, 8: 8, 16: 16}
EXPECTED_V = {1: 3, 2: 5, 4: 7, 8: 15, 16: 19}


def threshold(extra: int) -> int:
    """Least k with 2^k >= extra."""
    k = 0
    while (1 << k) < extra:
        k += 1
    return k


def min_odd_extras() -> dict:
    """Min first-odd extra for 2-power n0, from DI/DM/DR plus n0=1."""
    for mask in range(2):
        cur, sm = first_ident0_int(mask_bits(mask, 1), 20)
        if cur != 6 or sm != 1:
            return {"ok": False, "n0": 1, "cur": cur, "sm": sm}
    for mask in range(4):
        cur, a = first_odd(mask_bits(mask, 2), 40)
        if cur != 22 or a is None:
            return {"ok": False, "n0": 2, "cur": cur}
    di = json.loads(DI_JSON.read_text())
    dm = json.loads(DM_JSON.read_text())
    dr = json.loads(DR_JSON.read_text())
    if di["len4"]["n89"] != 8 or di["len2"]["extra"] != 22:
        return {"ok": False, "di": True}
    if min(int(x) for x in dm["n8"]["odd_extras"]) != MIN_ODD[8]:
        return {"ok": False, "dm_odd": dm["n8"]["odd_extras"]}
    if dm["n8"]["min_nonconst"] != 6344:
        return {"ok": False, "dm_min": dm["n8"]["min_nonconst"]}
    if dr["n16"]["E16"] != MIN_ODD[16] or dr["n16"]["n_hit"] != 0:
        return {"ok": False, "dr": dr["n16"]}
    if ODD_EXTRAS != (26357, 44842):
        return {"ok": False, "ODD_EXTRAS": ODD_EXTRAS}
    return {"ok": True, "E": dict(MIN_ODD)}


def thresholds_of(E: dict) -> dict:
    v = {int(n0): threshold(extra) for n0, extra in E.items()}
    if v != EXPECTED_V:
        return {"ok": False, "v": v}
    for n0, extra in MIN_ODD.items():
        vv = v[n0]
        if (1 << (vv - 1)) >= extra or (1 << vv) < extra:
            return {"ok": False, "n0": n0, "v": vv}
    return {"ok": True, "v": v}


def prize_before_threshold(v: dict) -> dict:
    de = json.loads(DE_JSON.read_text())
    odds = {int(k): p for k, p in de["odd_high_p"].items()}
    if odds != EXPECTED_ODD_P:
        return {"ok": False, "odds": odds}
    rows: dict[int, dict] = {}
    for n0, k_odd in PRIZE_ODD_K.items():
        if k_odd >= v[n0]:
            return {"ok": False, "n0": n0, "k": k_odd, "v": v[n0]}
        rmax = 1 << k_odd
        extra = MIN_ODD[n0]
        r_prize = leftover(n0) if n0 in (2, 4, 8, 16) else None
        if rmax >= extra:
            return {"ok": False, "n0": n0, "rmax": rmax, "E": extra}
        if r_prize is not None and r_prize >= extra:
            return {"ok": False, "n0": n0, "R": r_prize}
        rows[n0] = {
            "k_odd": k_odd,
            "v": v[n0],
            "rmax": rmax,
            "R_prize": r_prize,
            "E_odd": extra,
        }
    return {"ok": True, "rows": rows}


def skip_becomes_dangerous(v: dict) -> dict:
    """If n0 persists to k=v, worst-case leftover can fit a second odd."""
    rows: dict[int, dict] = {}
    for n0, vv in v.items():
        extra = MIN_ODD[n0]
        rmax = 1 << vv
        rows[n0] = {
            "v": vv,
            "rmax": rmax,
            "E_odd": extra,
            "second_fits": rmax >= extra,
        }
        if rmax < extra:
            return {"ok": False, "n0": n0}
    n2_k5 = (1 << 5) >= MIN_ODD[2]
    return {"ok": True, "rows": rows, "n0_2_k5_fits": n2_k5}


def ec_prefix() -> dict:
    ec = json.loads(EC_JSON.read_text())
    ok = (
        ec["checks"]["all_ok"]
        and ec["verdict"]["pow2_n0_fold_primitive"] == "LEMMA"
        and ec["verdict"]["left_machine_pi_always_pow2"] == "LEMMA"
        and ec["verdict"]["extra6_and_extra22_folds_unreachable_after_k2"] == "LEMMA"
        and ec["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok, "odd_n0": ec["odd_n0_left_machine"]}


def self_checks(
    c20, extras: dict, th: dict, prize: dict, skip: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert extras["ok"] and th["ok"] and prize["ok"] and skip["ok"] and pref["ok"]
    assert extras["E"][8] == 26357 and extras["E"][16] == 262145
    assert th["v"] == EXPECTED_V
    assert prize["rows"][16]["k_odd"] == 16 < 19
    assert prize["rows"][8]["R_prize"] == 112
    assert skip["n0_2_k5_fits"] is True
    assert leftover(2) == 0 and leftover(4) == 3
    assert leftover(8) == 112 and leftover(16) == 43205
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    extras = min_odd_extras()
    th = thresholds_of(extras["E"] if extras["ok"] else MIN_ODD)
    prize = prize_before_threshold(th["v"] if th["ok"] else EXPECTED_V)
    skip = skip_becomes_dangerous(th["v"] if th["ok"] else EXPECTED_V)
    pref = ec_prefix()
    checks = self_checks(c20, extras, th, prize, skip, pref)
    dump = {
        "cycle": "ED",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "min_odd_extra": extras["E"],
        "threshold_v": th["v"],
        "prize_before_v": prize["rows"],
        "skip_dangerous": skip["rows"],
        "lemmas": {
            "min_odd_extra_pow2_n0_le_16": True,
            "threshold_v_of_min_odd_extra": True,
            "prize_odd_k_before_v": True,
            "prize_leftover_and_rmax_below_E": True,
            "skip_n0_hits_v_then_second_odd_fits": True,
            "leftover_always_empty_pow2_n0_every_k": False,
            "next_odd_forced_before_v": None,
            "v_closed_form_all_pow2_n0": None,
            "at_most_one_odd_all_k": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "min_odd_extra_pow2_n0_le_16": "LEMMA",
            "threshold_v_of_min_odd_extra": "LEMMA",
            "prize_odd_k_before_v": "LEMMA",
            "prize_leftover_and_rmax_below_E": "LEMMA",
            "skip_n0_hits_v_then_second_odd_fits": "LEMMA",
            "leftover_always_empty_pow2_n0_every_k": "KILLED",
            "next_odd_forced_before_v": "PREFIX",
            "v_closed_form_all_pow2_n0": "PREFIX",
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
    print("threshold_v", dump["threshold_v"])
    print("prize_before_v", dump["prize_before_v"])


if __name__ == "__main__":
    main()
