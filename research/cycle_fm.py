#!/usr/bin/env python3
"""Cycle FM: 4U-shift on [4U,6U); left Delta is 1 from the (4U,1) AND.

Dual of Cycles FI–FJ for the 4U-shift comparing targets 6U and 10U.
On s in [4U,6U) one has m=6U-s-1<2U, so FF matches in-support.
The left off-support strip p<2s-6U+2 contains p<=2U; Freshman reduces
it to G(6U-s-1, 2U-p). The AND at (s,p)=(4U,1) is live and contributes
G(2U-1,2U-1)=1; the rest of the left strip XOR-cancels, so Delta4_L=1.
Kills: the naive dual Delta4_L=0; Delta4_R=0 (k=5,6); Delta4=Delta4_R.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fm.py --certify
Dump: research/cycle_fm.json
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
FL_JSON = Path(__file__).resolve().parent / "cycle_fl.json"
FJ_JSON = Path(__file__).resolve().parent / "cycle_fj.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
FI_JSON = Path(__file__).resolve().parent / "cycle_fi.json"


def m_lt_2U() -> dict:
    """m=6U-s-1 < 2U on s in [4U,6U)."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for s in (4 * U, 5 * U, 6 * U - 1):
            m = 6 * U - s - 1
            if not (0 <= m < 2 * U):
                return {"ok": False, "k": k, "s": s, "m": m}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def left_region() -> dict:
    """p<=2U sits in the left off-support strip on [4U,6U)."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for s in (4 * U, 5 * U, 6 * U - 1):
            lo = 2 * s - 6 * U + 2
            if lo < 2 * U + 2:
                return {"ok": False, "k": k, "s": s, "lo": lo}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def green_start() -> dict:
    """G(2U-1,2U-1)=1; G(4U-1,2U-1)=1."""
    n_ok = 0
    for k in range(0, 17):
        U = 1 << k
        if G(2 * U - 1, 2 * U - 1) != 1 or G(4 * U - 1, 2 * U - 1) != 1:
            return {"ok": False, "k": k}
        n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def packed_left(kmax: int = 6) -> dict:
    """Delta4_L=1 from (4U,1); rest=0; in-support match; r=1 live with 0."""
    rows = {}
    n_ok = 0
    n_dl1 = 0
    n_dr_nz = 0
    n_r1 = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        t0, t1 = 4 * U, 6 * U
        T6, T10 = 6 * U, 10 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        j6 = j10 = dL = dR = d_in = start = rest = 0
        n_p1 = n_r1k = 0
        for s in range(t0, t1):
            A = (row << 1) & row
            m = T6 - s - 1
            lo = 2 * s - 6 * U + 2
            tmp, p = A, 0
            while tmp:
                if tmp & 1:
                    g6 = G(T6 - s - 1, T6 - p)
                    g10 = G(T10 - s - 1, T10 - p)
                    j6 ^= g6
                    j10 ^= g10
                    if p > 6 * U:
                        dR ^= g10
                        if g6:
                            return {"ok": False, "k": k, "right6": True}
                        r = p - 6 * U
                        if r == 1:
                            n_r1k += 1
                            if g10:
                                return {"ok": False, "r1_contrib": True, "k": k}
                    elif p < lo:
                        red = G(m, 2 * U - p)
                        if g10 != red:
                            return {"ok": False, "k": k, "s": s, "p": p, "red": True}
                        dL ^= g10
                        if s == t0 and p == 1:
                            start ^= g10
                            n_p1 += 1
                        else:
                            rest ^= g10
                        if g6:
                            return {"ok": False, "k": k, "left6": True}
                    else:
                        d_in ^= g6
                        if g6 != g10:
                            return {"ok": False, "k": k, "ins": True}
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if n_p1 != 1 or start != 1 or rest != 0 or dL != 1:
            return {"ok": False, "k": k, "start": start, "rest": rest, "dL": dL, "n_p1": n_p1}
        if n_r1k == 0:
            return {"ok": False, "k": k, "r1_dead": True}
        if j6 != d_in or j10 != (d_in ^ dL ^ dR):
            return {"ok": False, "k": k, "split": True}
        n_ok += 1
        n_dl1 += 1
        n_r1 += 1
        if dR:
            n_dr_nz += 1
        rows[str(k)] = {"j6": j6, "j10": j10, "dL": dL, "dR": dR, "rest": rest}
    return {
        "ok": n_ok == kmax - 1 and n_dl1 == n_ok and n_r1 == n_ok and n_dr_nz > 0,
        "n_ok": n_ok,
        "n_dl1": n_dl1,
        "n_dr_nz": n_dr_nz,
        "rows": rows,
    }


def prefixes() -> dict:
    fl = json.loads(FL_JSON.read_text())
    fj = json.loads(FJ_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    fi = json.loads(FI_JSON.read_text())
    ok = (
        fl["checks"]["all_ok"]
        and fj["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fi["checks"]["all_ok"]
        and fj["verdict"]["Delta_L_eq_0"] == "LEMMA"
        and fi["verdict"]["AND_p1_live_t_ge_1"] == "LEMMA"
        and ff["verdict"]["G_nn_eq_1"] == "LEMMA"
        and fl["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, mlt: dict, left: dict, green: dict, pack: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mlt["ok"] and left["ok"] and green["ok"] and pack["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mlt = m_lt_2U()
    left = left_region()
    green = green_start()
    pack = packed_left()
    pref = prefixes()
    checks = self_checks(c20, mlt, left, green, pack, pref)
    dump = {
        "cycle": "FM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "m_lt_2U": {k: mlt[k] for k in mlt if k != "ok"},
        "left_region": {k: left[k] for k in left if k != "ok"},
        "green": {k: green[k] for k in green if k != "ok"},
        "packed": {k: pack[k] for k in pack if k != "ok"},
        "lemmas": {
            "m_lt_2U_on_4U_6U": True,
            "FF_on_support_4U_shift": True,
            "Delta4_L_eq_1": True,
            "Delta4_L_eq_start_p1": True,
            "Delta4_L_eq_0": False,
            "Delta4_R_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "m_lt_2U_on_4U_6U": "LEMMA",
            "FF_on_support_4U_shift": "LEMMA",
            "Delta4_L_eq_1": "LEMMA",
            "Delta4_L_eq_start_p1": "LEMMA",
            "Delta4_L_eq_0": "KILLED",
            "Delta4_R_eq_0": "KILLED",
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
