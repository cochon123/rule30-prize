#!/usr/bin/env python3
"""Cycle EE: every n0=2 scar lifts to FAM372; 89-orbit unreachable after k=2.

Every length-2 T0 odd-ident-0s at extra 22 with predecessor a a rotation of
0111 (Cycle DI). unfold(a) is 0010, 0100, 0101, or 0110, all in the n0=4
extra-372 family. So a left-machine n0=2 doubling never produces the extra-89
orbit. Extra 22 sends annulus k=2 into k=4; extra 372 sends k=4 into k=8;
extra 89 would send k=4 into k=6, but that family is unreachable from n0=2.
Prize T0=0010 is unfold(0111). Kills: 89-orbit reachable from n0=2; every
n0=4 waits for a 2-power (89 still hits k=6, but not on the left machine
after k=2). Do not claim an n0=8 lift closed form; do not claim k=8 maps
to k=16. Not a prize claim.

Run: python3 research/cycle_ee.py --certify
Dump: research/cycle_ee.json
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
from cycle_df import unfold
from cycle_di import FAM372, FAM89, PRIZE4, ROTS_0111, first_odd, mask_bits
from cycle_ed import threshold

OUT = Path(__file__).resolve().with_suffix(".json")
ED_JSON = Path(__file__).resolve().parent / "cycle_ed.json"
DI_JSON = Path(__file__).resolve().parent / "cycle_di.json"
LIFT372 = {"0010", "0100", "0101", "0110"}


def annulus(p: int) -> int:
    """k such that 2^k < p <= 2^{k+1}."""
    k = p.bit_length() - 1
    if p == (1 << k):
        return k - 1
    return k


def next_image(k: int, extra: int) -> tuple[int, int]:
    """Image of packed (2^k, 2^{k+1}] under p |-> p+extra-1."""
    w = 1 << k
    return w + extra, 2 * w + extra - 1


def image_one_annulus(k: int, extra: int) -> dict:
    lo, hi = next_image(k, extra)
    ak, ah = annulus(lo), annulus(hi)
    return {"ok": ak == ah, "lo": lo, "hi": hi, "k_lo": ak, "k_hi": ah}


def unfold_rots_0111() -> dict:
    """unfold of every rotation of 0111 is a FAM372 word starting with 0."""
    got: dict[str, str] = {}
    for rot in sorted(ROTS_0111):
        u = "".join(map(str, unfold([int(c) for c in rot])))
        got[rot] = u
        if u not in FAM372 or u[0] != "0" or u not in LIFT372:
            return {"ok": False, "rot": rot, "u": u}
    if set(got.values()) != LIFT372:
        return {"ok": False, "got": got}
    if got["0111"] != PRIZE4:
        return {"ok": False, "prize": got["0111"]}
    return {"ok": True, "map": got}


def n0_2_lifts_372() -> dict:
    """Every length-2 T0 lifts through extra 22 to a FAM372 T0."""
    rows: dict[str, str] = {}
    for mask in range(4):
        t0 = mask_bits(mask, 2)
        key = "".join(map(str, t0))
        cur, a = first_odd(t0, 40)
        if cur != 22 or a is None or a not in ROTS_0111:
            return {"ok": False, "T0": key, "cur": cur, "a": a}
        u = "".join(map(str, unfold([int(c) for c in a])))
        if u not in LIFT372:
            return {"ok": False, "T0": key, "u": u}
        extra_u, _ = first_odd([int(c) for c in u], 400)
        if extra_u != 372:
            return {"ok": False, "T0": key, "next": extra_u}
        rows[key] = u
    if set(rows.values()) != LIFT372:
        return {"ok": False, "rows": rows}
    return {"ok": True, "rows": rows}


def fam_extras() -> dict:
    """FAM372 all extra 372; FAM89 all extra 89; no n0=2 lift in FAM89."""
    n372 = 0
    n89 = 0
    for mask in range(16):
        t0 = mask_bits(mask, 4)
        key = "".join(map(str, t0))
        cur, _ = first_odd(t0, 400)
        if key in FAM372:
            if cur != 372:
                return {"ok": False, "372": key, "cur": cur}
            n372 += 1
        elif key in FAM89:
            if cur != 89:
                return {"ok": False, "89": key, "cur": cur}
            n89 += 1
        else:
            return {"ok": False, "key": key}
    if n372 != 8 or n89 != 8:
        return {"ok": False, "n": (n372, n89)}
    if LIFT372 & FAM89:
        return {"ok": False, "overlap": True}
    if not LIFT372 <= FAM372:
        return {"ok": False, "subset": True}
    return {"ok": True, "n372": 8, "n89": 8}


def landings() -> dict:
    """k=2 extra 22 -> k=4; k=4 extra 372 -> k=8; k=4 extra 89 -> k=6."""
    rows = {
        "22_from_2": image_one_annulus(2, 22),
        "372_from_4": image_one_annulus(4, 372),
        "89_from_4": image_one_annulus(4, 89),
    }
    ok = (
        rows["22_from_2"]["ok"]
        and rows["22_from_2"]["k_lo"] == 4
        and rows["372_from_4"]["ok"]
        and rows["372_from_4"]["k_lo"] == 8
        and rows["89_from_4"]["ok"]
        and rows["89_from_4"]["k_lo"] == 6
    )
    prize_next = (8 + 22 - 1, 29 + 372 - 1)
    if prize_next != (29, 400):
        return {"ok": False, "prize_next": prize_next}
    if annulus(29) != 4 or annulus(400) != 8 or annulus(8) != 2:
        return {"ok": False, "ann": True}
    return {"ok": ok, "rows": rows, "prize_next": {"8": 29, "29": 400}}


def ed_prefix() -> dict:
    ed = json.loads(ED_JSON.read_text())
    di = json.loads(DI_JSON.read_text())
    ok = (
        ed["checks"]["all_ok"]
        and ed["threshold_v"]["4"] == 7
        and ed["threshold_v"]["8"] == 15
        and di["checks"]["all_ok"]
        and di["len2"]["extra"] == 22
        and di["len4"]["prize_extra"] == 372
        and threshold(89) == 7
        and threshold(372) == 9
    )
    return {"ok": ok, "v4": 7, "v372": threshold(372)}


def self_checks(
    c20, unf: dict, lift: dict, fam: dict, land: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert unf["ok"] and lift["ok"] and fam["ok"] and land["ok"] and pref["ok"]
    assert unf["map"]["0111"] == PRIZE4
    assert lift["rows"]["11"] == PRIZE4
    assert fam["n372"] == 8 and "0010" in FAM372 and "0001" in FAM89
    assert land["prize_next"]["8"] == 29
    assert land["rows"]["89_from_4"]["k_lo"] == 6
    assert pref["v372"] == 9
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    unf = unfold_rots_0111()
    lift = n0_2_lifts_372()
    fam = fam_extras()
    land = landings()
    pref = ed_prefix()
    checks = self_checks(c20, unf, lift, fam, land, pref)
    dump = {
        "cycle": "EE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "unfold_0111": unf["map"],
        "n0_2_lift": lift["rows"],
        "landings": {k: {kk: vv for kk, vv in row.items() if kk != "ok"} for k, row in land["rows"].items()},
        "prize_next": land["prize_next"],
        "lemmas": {
            "unfold_rots_0111_in_FAM372": True,
            "n0_2_lifts_to_FAM372": True,
            "FAM372_all_extra_372": True,
            "extra22_k2_lands_k4": True,
            "extra372_k4_lands_k8": True,
            "extra89_k4_lands_k6": True,
            "FAM89_reachable_from_n0_2": False,
            "every_n0_4_waits_for_pow2": False,
            "n0_8_lift_closed_form": None,
            "k8_lands_k16": None,
            "at_most_one_odd_all_k": None,
            "pi_formula_all_k": None,
            "period_H_seed_all_k": None,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "unfold_rots_0111_in_FAM372": "LEMMA",
            "n0_2_lifts_to_FAM372": "LEMMA",
            "FAM372_all_extra_372": "LEMMA",
            "extra22_k2_lands_k4": "LEMMA",
            "extra372_k4_lands_k8": "LEMMA",
            "extra89_k4_lands_k6": "LEMMA",
            "FAM89_reachable_from_n0_2": "KILLED",
            "every_n0_4_waits_for_pow2": "KILLED",
            "n0_8_lift_closed_form": "PREFIX",
            "k8_lands_k16": "PREFIX",
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
    print("n0_2_lift", dump["n0_2_lift"])
    print("landings", dump["landings"])


if __name__ == "__main__":
    main()
