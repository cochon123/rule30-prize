#!/usr/bin/env python3
"""Cycle FI: on [6U,10U) FF matches in-support; 10U vs 18U remainders need not.

For s in [6U,10U) the Green degree m=10U-s-1 satisfies m<4U=2^{k+2},
so Cycle FF's q=1, a=k+3 translation gives G(m+8U, d+8U)=G(m,d)
whenever 0<=d<=2m. Freshman extras of the 8U-shift therefore leave
the support on that slice. The remainders themselves need not agree:
off-support ANDs (d not in [0,2m]) can still reach 18U.

The injection at packed p=1 is live for every t>=1 (bit0 stays 1,
bit1=bit0 OR bit1). At s=6U it contributes G(12U-1,18U-1)=1 to the
18U remainder and G(4U-1,10U-1)=0 to the 10U remainder. That single
bit does not force the window XOR to 1 (k=5 cancels). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fi.py --certify
Dump: research/cycle_fi.json
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
FH_JSON = Path(__file__).resolve().parent / "cycle_fh.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"
FG_JSON = Path(__file__).resolve().parent / "cycle_fg.json"


def m_lt_4U() -> dict:
    """m=10U-s-1 < 4U on s in [6U,10U)."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for s in (6 * U, 8 * U, 10 * U - 1):
            m = 10 * U - s - 1
            if not (0 <= m < 4 * U):
                return {"ok": False, "k": k, "s": s, "m": m}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def cone_on_support() -> dict:
    """8U Freshman extras leave [0,2m] whenever d is in support."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        samples = [t0, t0 + U, 8 * U, t1 - 1]
        for s in samples:
            if not (t0 <= s < t1):
                continue
            m = 10 * U - s - 1
            two_m = 2 * m
            for p in (0, s, 2 * s):
                d = 10 * U - p
                if 0 <= d <= two_m:
                    for e in (d + 8 * U, d - 8 * U):
                        if 0 <= e <= two_m:
                            return {"ok": False, "k": k, "s": s, "p": p, "e": e}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def green_start() -> dict:
    """G(12U-1,18U-1)=1; G(4U-1,10U-1)=0; peels to G(5,8) for k>=1."""
    if G(5, 8) != 1:
        return {"ok": False, "G58": G(5, 8)}
    if G(11, 17) != 1:
        return {"ok": False, "G11_17": G(11, 17)}
    n_ok = 0
    for k in range(0, 17):
        U = 1 << k
        g18 = G(12 * U - 1, 18 * U - 1)
        g10 = G(4 * U - 1, 10 * U - 1)
        if g18 != 1 or g10 != 0:
            return {"ok": False, "k": k, "g18": g18, "g10": g10}
        if k >= 1 and g18 != G(5, 8):
            return {"ok": False, "peel": k}
        n_ok += 1
    return {"ok": True, "n_ok": n_ok, "G58": 1}


def left_and_p1() -> dict:
    """Packed bits 0,1 are 11 for t>=1, so AND bit 1 is live."""
    row = 1
    n_ok = 0
    for t in range(0, 65):
        b0 = row & 1
        b1 = (row >> 1) & 1
        if t == 0:
            if not (b0 == 1 and b1 == 0):
                return {"ok": False, "t": 0}
        else:
            if not (b0 == 1 and b1 == 1):
                return {"ok": False, "t": t, "b0": b0, "b1": b1}
            if ((row << 1) & row) & 2 == 0:
                return {"ok": False, "and": t}
            n_ok += 1
        row = rule30_step(row)
    return {"ok": n_ok == 64, "n_ok": n_ok}


def packed_window(kmax: int = 6) -> dict:
    """Remainders on [6U,10U) to 10U vs 18U: not always equal; Delta not always 1."""
    rows = {}
    n_neq = 0
    n_delta0 = 0
    live_p1 = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        T10, T18 = 10 * U, 18 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        j10 = j18 = 0
        p1_live = False
        for s in range(t0, t1):
            A = (row << 1) & row
            if s == t0 and (A & 2):
                p1_live = True
            tmp, p = A, 0
            while tmp:
                if tmp & 1:
                    g10 = G(T10 - s - 1, T10 - p)
                    g18 = G(T18 - s - 1, T18 - p)
                    j10 ^= g10
                    j18 ^= g18
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if not p1_live:
            return {"ok": False, "k": k, "p1": False}
        live_p1 += 1
        delta = j10 ^ j18
        rows[str(k)] = {"J10": j10, "J18": j18, "Delta": delta}
        if j10 != j18:
            n_neq += 1
        if delta == 0:
            n_delta0 += 1
    return {
        "ok": n_neq > 0 and n_delta0 > 0 and live_p1 == kmax - 1,
        "n_neq": n_neq,
        "n_delta0": n_delta0,
        "live_p1": live_p1,
        "rows": rows,
    }


def prefixes() -> dict:
    fh = json.loads(FH_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    fg = json.loads(FG_JSON.read_text())
    ok = (
        fh["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fg["checks"]["all_ok"]
        and fh["verdict"]["J18_eq_J6_xor_Jpost"] == "LEMMA"
        and ff["verdict"]["G_shift_q_2a_n_lt_2a_minus_1"] == "LEMMA"
        and fh["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, mlt: dict, cone: dict, green: dict, left: dict, win: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mlt["ok"] and cone["ok"] and green["ok"]
    assert left["ok"] and win["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mlt = m_lt_4U()
    cone = cone_on_support()
    green = green_start()
    left = left_and_p1()
    win = packed_window()
    pref = prefixes()
    checks = self_checks(c20, mlt, cone, green, left, win, pref)
    dump = {
        "cycle": "FI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "m_lt_4U": {k: mlt[k] for k in mlt if k != "ok"},
        "cone": {k: cone[k] for k in cone if k != "ok"},
        "green": {k: green[k] for k in green if k != "ok"},
        "left": {k: left[k] for k in left if k != "ok"},
        "window": {k: win[k] for k in win if k != "ok"},
        "lemmas": {
            "m_lt_4U_on_6U_10U": True,
            "FF_on_support_8U_shift": True,
            "G_12U_minus_1_18U_minus_1_eq_1": True,
            "AND_p1_live_t_ge_1": True,
            "J_6U_10U_to_10U_eq_to_18U": False,
            "Delta_off_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "m_lt_4U_on_6U_10U": "LEMMA",
            "FF_on_support_8U_shift": "LEMMA",
            "G_12U_minus_1_18U_minus_1_eq_1": "LEMMA",
            "AND_p1_live_t_ge_1": "LEMMA",
            "J_6U_10U_to_10U_eq_to_18U": "KILLED",
            "Delta_off_eq_1": "KILLED",
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
    print("green", dump["green"])
    print("window", dump["window"])


if __name__ == "__main__":
    main()
