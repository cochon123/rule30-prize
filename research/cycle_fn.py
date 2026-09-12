#!/usr/bin/env python3
"""Cycle FN: 4U right-band of width 2U-1 until 5U; [2U,4U) 6U vs 10U fails.

Dual of Cycle FL for the 4U-shift on [4U,6U). Green support is
2(s-4U+1) <= r <= 4U with r=p-6U; the light cone restricts r <= 2s-6U.
On [4U,5U] that intersection has length 2U-1; after 5U it clips to
12U-2s-1. Delta4_R equals the band XOR. The earlier window [2U,4U)
still matches 6U vs 18U (FH) but not 6U vs 10U. Kills: flat width on
all of [4U,6U); last AND at p=10U always live. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not bump
all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fn.py --certify
Dump: research/cycle_fn.json
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
FM_JSON = Path(__file__).resolve().parent / "cycle_fm.json"
FL_JSON = Path(__file__).resolve().parent / "cycle_fl.json"
FH_JSON = Path(__file__).resolve().parent / "cycle_fh.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"


def r_band(s: int, U: int) -> tuple[int, int]:
    lo = 2 * (s - 4 * U + 1)
    hi = min(2 * s - 6 * U, 4 * U)
    return lo, hi


def algebraic_width() -> dict:
    """Width 2U-1 on [4U,5U]; 12U-2s-1 after 5U."""
    n_flat = 0
    n_clip = 0
    for k in range(0, 13):
        U = 1 << k
        for s in range(4 * U, 6 * U):
            lo, hi = r_band(s, U)
            w = hi - lo + 1 if hi >= lo else 0
            if s <= 5 * U:
                if w != 2 * U - 1:
                    return {"ok": False, "k": k, "s": s, "w": w}
                n_flat += 1
            else:
                want = 12 * U - 2 * s - 1
                if w != want or w < 1:
                    return {"ok": False, "clip": True, "k": k, "s": s, "w": w}
                n_clip += 1
    return {"ok": True, "n_flat": n_flat, "n_clip": n_clip}


def killed_width_all() -> dict:
    """Width is not 2U-1 on the whole [4U,6U): s=5U+1 clips."""
    k = 2
    U = 1 << k
    s = 5 * U + 1
    lo, hi = r_band(s, U)
    w = hi - lo + 1
    ok = w != 2 * U - 1 and w == 12 * U - 2 * s - 1
    return {"ok": ok, "k": k, "s": s, "w": w, "flat": 2 * U - 1}


def freshman_right() -> dict:
    """On p>6U, G(m+4U,d+4U)=G(m,d+4U) and G(m,d)=G(m,d-4U)=0."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        t0, t1 = 4 * U, 6 * U
        for s in (t0, t0 + U // 2 if U > 1 else t0, 5 * U, t1 - 1):
            if not (t0 <= s < t1):
                continue
            m = 6 * U - s - 1
            for p in (6 * U + 1, 6 * U + 2, min(2 * s, 8 * U)):
                if p <= 6 * U or p > 2 * s:
                    continue
                d = 6 * U - p
                if G(m, d) != 0 or G(m, d - 4 * U) != 0:
                    return {"ok": False, "live": True, "k": k, "s": s, "p": p}
                if G(m + 4 * U, d + 4 * U) != G(m, d + 4 * U):
                    return {"ok": False, "k": k, "s": s, "p": p}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def packed_band(kmax: int = 6) -> dict:
    """Delta4_R equals the band XOR; [2U,4U) matches 18U not 10U."""
    rows = {}
    n_ok = 0
    n_neq24 = 0
    n_last_dead = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        row = 1
        t24, t46, t6 = 2 * U, 4 * U, 6 * U
        T6, T10, T18 = 6 * U, 10 * U, 18 * U
        for _ in range(t24):
            row = rule30_step(row)
        j6 = j10 = j18 = 0
        for s in range(t24, t46):
            A = (row << 1) & row
            tmp, p = A, 0
            while tmp:
                if tmp & 1:
                    g6 = G(T6 - s - 1, T6 - p)
                    j6 ^= g6
                    j10 ^= G(T10 - s - 1, T10 - p)
                    g18 = G(T18 - s - 1, T18 - p)
                    j18 ^= g18
                    if g6 != g18:
                        return {"ok": False, "k": k, "fh": True, "s": s, "p": p}
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        dR = d_band = 0
        n_out_nz = 0
        last = 0
        for s in range(t46, t6):
            A = (row << 1) & row
            lo, hi = r_band(s, U)
            tmp, p = A, 0
            while tmp:
                if tmp & 1 and p > 6 * U:
                    r = p - 6 * U
                    g10 = G(T10 - s - 1, T10 - p)
                    dR ^= g10
                    if lo <= r <= hi:
                        d_band ^= g10
                    elif g10:
                        n_out_nz += 1
                    if s == t6 - 1 and p == 10 * U:
                        last = 1
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if dR != d_band or n_out_nz:
            return {"ok": False, "k": k, "dR": dR, "band": d_band, "out": n_out_nz}
        n_ok += 1
        if j6 != j10:
            n_neq24 += 1
        if not last:
            n_last_dead += 1
        rows[str(k)] = {
            "dR": dR,
            "j24_6": j6,
            "j24_10": j10,
            "j24_18": j18,
            "last_p10": last,
        }
    return {
        "ok": n_ok == kmax - 1 and n_neq24 > 0 and n_last_dead > 0,
        "n_ok": n_ok,
        "n_neq24": n_neq24,
        "n_last_dead": n_last_dead,
        "rows": rows,
    }


def prefixes() -> dict:
    fm = json.loads(FM_JSON.read_text())
    fl = json.loads(FL_JSON.read_text())
    fh = json.loads(FH_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    ok = (
        fm["checks"]["all_ok"]
        and fl["checks"]["all_ok"]
        and fh["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fm["verdict"]["Delta4_L_eq_1"] == "LEMMA"
        and fl["verdict"]["Delta_R_eq_band_xor"] == "LEMMA"
        and fh["verdict"]["J6_eq_J_2U_6U_to_18U"] == "LEMMA"
        and fm["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, width: dict, killed_w: dict, fresh: dict, pack: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert width["ok"] and killed_w["ok"] and fresh["ok"] and pack["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    width = algebraic_width()
    killed_w = killed_width_all()
    fresh = freshman_right()
    pack = packed_band()
    pref = prefixes()
    checks = self_checks(c20, width, killed_w, fresh, pack, pref)
    dump = {
        "cycle": "FN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "width": {k: width[k] for k in width if k != "ok"},
        "killed_width": {k: killed_w[k] for k in killed_w if k != "ok"},
        "freshman": {k: fresh[k] for k in fresh if k != "ok"},
        "packed": {k: pack[k] for k in pack if k != "ok"},
        "lemmas": {
            "width_2U_minus_1_on_4U_5U": True,
            "clip_width_after_5U": True,
            "Delta4_R_eq_band_xor": True,
            "J_2U_4U_to_6U_eq_to_18U": True,
            "J_2U_4U_to_6U_eq_to_10U": False,
            "width_2U_minus_1_on_all_4U_6U": False,
            "last_AND_p10U_always_live": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "width_2U_minus_1_on_4U_5U": "LEMMA",
            "clip_width_after_5U": "LEMMA",
            "Delta4_R_eq_band_xor": "LEMMA",
            "J_2U_4U_to_6U_eq_to_18U": "LEMMA",
            "J_2U_4U_to_6U_eq_to_10U": "KILLED",
            "width_2U_minus_1_on_all_4U_6U": "KILLED",
            "last_AND_p10U_always_live": "KILLED",
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
    print("packed", dump["packed"])


if __name__ == "__main__":
    main()
