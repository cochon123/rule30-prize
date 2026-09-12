#!/usr/bin/env python3
"""Cycle FL: Delta_R lives on a sliding r-band of width 2U-1 until 9U.

Cycle FK reduced Delta_R to G(10U-s-1, 8U-r) on AND p=10U+r.
Green support is 2(s-6U+1) <= r <= 8U; the light cone further
restricts r <= 2s-10U. On s in [6U,9U] that intersection has
length 2U-1; after 9U the r<=8U cap shrinks it to 20U-2s-1,
ending at width 1. For r < 2(s-6U+1) the reduced Green vanishes
even when the AND fires (r=2 after s=6U).
Kills: width 2U-1 on all of [6U,10U) (s=9U+1 clips); last AND at
p=18U always live (dead at k=2). Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fl.py --certify
Dump: research/cycle_fl.json
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
FK_JSON = Path(__file__).resolve().parent / "cycle_fk.json"
FJ_JSON = Path(__file__).resolve().parent / "cycle_fj.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"


def r_band(s: int, U: int) -> tuple[int, int]:
    lo = 2 * (s - 6 * U + 1)
    hi = min(2 * s - 10 * U, 8 * U)
    return lo, hi


def algebraic_width() -> dict:
    """Width 2U-1 on [6U,9U]; 20U-2s-1 after 9U, at least 1."""
    n_flat = 0
    n_clip = 0
    for k in range(0, 13):
        U = 1 << k
        for s in range(6 * U, 10 * U):
            lo, hi = r_band(s, U)
            w = hi - lo + 1 if hi >= lo else 0
            if s <= 9 * U:
                if w != 2 * U - 1:
                    return {"ok": False, "k": k, "s": s, "w": w}
                n_flat += 1
            else:
                want = 20 * U - 2 * s - 1
                if w != want or w < 1:
                    return {"ok": False, "clip": True, "k": k, "s": s, "w": w, "want": want}
                n_clip += 1
    return {"ok": True, "n_flat": n_flat, "n_clip": n_clip}


def killed_width_all() -> dict:
    """Width is not 2U-1 on the whole [6U,10U): s=9U+1 clips."""
    k = 2
    U = 1 << k
    s = 9 * U + 1
    lo, hi = r_band(s, U)
    w = hi - lo + 1
    ok = w != 2 * U - 1 and w == 20 * U - 2 * s - 1
    return {"ok": ok, "k": k, "s": s, "w": w, "flat": 2 * U - 1}


def green_outside() -> dict:
    """G(m, 8U-r)=0 for r < lo or r > 8U (Green support, not light-cone)."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        for s in (t0, t0 + U, 9 * U, t1 - 1):
            if not (t0 <= s < t1):
                continue
            m = 10 * U - s - 1
            lo, _hi = r_band(s, U)
            samples = {1, max(lo - 1, 0), 8 * U + 1, 9 * U}
            for r in samples:
                g = G(m, 8 * U - r)
                inside = lo <= r <= 8 * U
                if (not inside) and g != 0:
                    return {"ok": False, "k": k, "s": s, "r": r, "g": g}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def packed_band(kmax: int = 6) -> dict:
    """Delta_R equals the band XOR; outside ANDs contribute 0; r=2 fires late."""
    rows = {}
    n_ok = 0
    n_r2_late = 0
    n_last_dead = 0
    n_last_live = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        T18 = 18 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        dR = d_band = 0
        n_out_nz = 0
        late = 0
        last = 0
        for s in range(t0, t1):
            A = (row << 1) & row
            m = 10 * U - s - 1
            lo, hi = r_band(s, U)
            tmp, p = A, 0
            while tmp:
                if tmp & 1 and p > 10 * U:
                    r = p - 10 * U
                    g18 = G(T18 - s - 1, T18 - p)
                    dR ^= g18
                    if lo <= r <= hi:
                        d_band ^= g18
                    else:
                        if g18:
                            n_out_nz += 1
                        if r == 2 and s > t0:
                            late += 1
                    if s == t1 - 1 and p == 18 * U:
                        last = 1
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if dR != d_band or n_out_nz:
            return {"ok": False, "k": k, "dR": dR, "band": d_band, "out": n_out_nz}
        n_ok += 1
        if late:
            n_r2_late += 1
        if last:
            n_last_live += 1
        else:
            n_last_dead += 1
        rows[str(k)] = {"dR": dR, "late_r2": late, "last_p18": last}
    return {
        "ok": n_ok == kmax - 1 and n_r2_late > 0 and n_last_dead > 0,
        "n_ok": n_ok,
        "n_r2_late": n_r2_late,
        "n_last_dead": n_last_dead,
        "n_last_live": n_last_live,
        "rows": rows,
    }


def prefixes() -> dict:
    fk = json.loads(FK_JSON.read_text())
    fj = json.loads(FJ_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    ok = (
        fk["checks"]["all_ok"]
        and fj["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fk["verdict"]["freshman_right_reduces_to_G_m_8U_r"] == "LEMMA"
        and fj["verdict"]["Delta_eq_Delta_R"] == "LEMMA"
        and fk["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, width: dict, killed_w: dict, green: dict, band: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert width["ok"] and killed_w["ok"] and green["ok"] and band["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    width = algebraic_width()
    killed_w = killed_width_all()
    green = green_outside()
    band = packed_band()
    pref = prefixes()
    checks = self_checks(c20, width, killed_w, green, band, pref)
    dump = {
        "cycle": "FL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "width": {k: width[k] for k in width if k != "ok"},
        "killed_width": {k: killed_w[k] for k in killed_w if k != "ok"},
        "green": {k: green[k] for k in green if k != "ok"},
        "band": {k: band[k] for k in band if k != "ok"},
        "lemmas": {
            "width_2U_minus_1_on_6U_9U": True,
            "clip_width_after_9U": True,
            "Delta_R_eq_band_xor": True,
            "width_2U_minus_1_on_all_6U_10U": False,
            "last_AND_p18U_always_live": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "width_2U_minus_1_on_6U_9U": "LEMMA",
            "clip_width_after_9U": "LEMMA",
            "Delta_R_eq_band_xor": "LEMMA",
            "width_2U_minus_1_on_all_6U_10U": "KILLED",
            "last_AND_p18U_always_live": "KILLED",
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
    print("width", dump["width"])
    print("band", dump["band"])


if __name__ == "__main__":
    main()
