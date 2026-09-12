#!/usr/bin/env python3
"""Cycle FH: J18 = J6 XOR J_{[6U,18U)->18U}; cone match on all of [2U,6U).

Cycle FG's cone bounds never used s>=4U except as the window. The same
d+8U>2m and d-8U<0 hold for every light-cone AND on s in [2U,6U), so
G(m+12U, d+12U)=G(m,d) there too. Thus J_{[2U,6U)->6U}=J_{[2U,6U)->18U}
which is J6, and splitting Cycle FE's J18 gives

    J18 = J6 XOR J_{[6U,18U)->18U}.

In particular J6=0 implies J18 equals the post-6U remainder (not
identically 1: k=2 has J6=J18=0). Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fh.py --certify
Dump: research/cycle_fh.json
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
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FG_JSON = Path(__file__).resolve().parent / "cycle_fg.json"
FE_JSON = Path(__file__).resolve().parent / "cycle_fe.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
DS_JSON = Path(__file__).resolve().parent / "cycle_ds.json"


def cone_bounds() -> dict:
    """Freshman extras leave [0,2m] for light-cone ANDs on [2U,6U)."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        t0, t1 = 2 * U, 6 * U
        samples = [t0, t0 + U, 4 * U, t1 - 1]
        for s in samples:
            if not (t0 <= s < t1):
                continue
            m = 6 * U - s - 1
            if m < 0:
                return {"ok": False, "k": k, "m": m}
            two_m = 2 * m
            for p in (0, s, 2 * s):
                d = 6 * U - p
                extras = (d + 12 * U, d + 8 * U, d - 8 * U, d - 12 * U)
                for e in extras:
                    if 0 <= e <= two_m:
                        return {"ok": False, "k": k, "s": s, "p": p, "e": e}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def remainder(k: int, t0: int, t1: int, T: int) -> int:
    U = 1 << k
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    acc = 0
    for s in range(t0, t1):
        A = (row << 1) & row
        tmp, p = A, 0
        while tmp:
            if tmp & 1:
                acc ^= G(T - s - 1, T - p)
            tmp >>= 1
            p += 1
        row = rule30_step(row)
    return acc


def packed_split(kmax: int = 6) -> dict:
    """J6 window equals J18 window on [2U,6U); J18 = J6 XOR Jpost."""
    rows = {}
    n_ok = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        j6 = remainder(k, 2 * U, 6 * U, 6 * U)
        j18_pre = remainder(k, 2 * U, 6 * U, 18 * U)
        jpost = remainder(k, 6 * U, 18 * U, 18 * U)
        j18 = j18_pre ^ jpost
        if j6 != j18_pre:
            return {"ok": False, "k": k, "pre": True}
        if j18 != (j6 ^ jpost):
            return {"ok": False, "k": k, "split": True}
        n_ok += 1
        rows[str(k)] = {"J6": j6, "J18": j18, "Jpost": jpost}
    return {"ok": n_ok == kmax - 1, "n_ok": n_ok, "rows": rows}


def killed_j6_zero() -> dict:
    """J6=0 does not force J18=1: Cycle FE k=2 has J6=J18=0."""
    ds = json.loads(DS_JSON.read_text())
    pref = ds["prefix"]
    i = pref["k"].index(2)
    I = pref["phi2"][i]
    j6 = pref["phi6"][i] ^ I
    j18 = pref["phi18"][i] ^ I
    ok = j6 == 0 and j18 == 0
    return {"ok": ok, "k": 2, "J6": j6, "J18": j18}


def prefixes() -> dict:
    fg = json.loads(FG_JSON.read_text())
    fe = json.loads(FE_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    ok = (
        fg["checks"]["all_ok"]
        and fe["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fg["verdict"]["J_4U_6U_to_6U_eq_to_18U"] == "LEMMA"
        and fe["verdict"]["cover_fails_iff_J6_J10_J18_vanish"] == "LEMMA"
        and fg["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, cone: dict, split: dict, killed: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cone["ok"] and split["ok"] and killed["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cone = cone_bounds()
    split = packed_split()
    killed = killed_j6_zero()
    pref = prefixes()
    checks = self_checks(c20, cone, split, killed, pref)
    dump = {
        "cycle": "FH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "cone": {k: cone[k] for k in cone if k != "ok"},
        "split": {k: split[k] for k in split if k != "ok"},
        "killed": {k: killed[k] for k in killed if k != "ok"},
        "lemmas": {
            "cone_on_2U_6U": True,
            "J6_eq_J_2U_6U_to_18U": True,
            "J18_eq_J6_xor_Jpost": True,
            "J6_0_implies_J18_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cone_on_2U_6U": "LEMMA",
            "J6_eq_J_2U_6U_to_18U": "LEMMA",
            "J18_eq_J6_xor_Jpost": "LEMMA",
            "J6_0_implies_J18_1": "KILLED",
            "J6_J10_0_implies_J18_1_all_k": "PREFIX",
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
    print("cone", dump["cone"])
    print("split", dump["split"])
    print("killed", dump["killed"])


if __name__ == "__main__":
    main()
