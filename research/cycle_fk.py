#!/usr/bin/env python3
"""Cycle FK: right-strip Freshman; Delta_R = G(m, 8U-r) on p=10U+r.

Dual of Cycle FJ. On the right off-support strip p>10U one has d=10U-p<0
and therefore d-8U<0, so Freshman of the 8U-shift leaves only
G(m, d+8U)=G(10U-s-1, 8U-r) with r=p-10U. In particular r=1 is always
off the reduced support (8U-1>2m for s>=6U) even though the AND at
p=10U+1 does fire. Corners G(n,0)=G(n,2n)=1 (with FF's G(n,n)=1).
Kills: Delta_R equals the r=2 XOR (that XOR vanishes while Delta_R
need not). Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_fk.py --certify
Dump: research/cycle_fk.json
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
FJ_JSON = Path(__file__).resolve().parent / "cycle_fj.json"
FI_JSON = Path(__file__).resolve().parent / "cycle_fi.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"


def corners(nmax: int = 256) -> dict:
    """G(n,0)=G(n,2n)=1 (and G(n,n)=1 from Cycle FF)."""
    n_ok = 0
    for n in range(nmax):
        if G(n, 0) != 1 or G(n, 2 * n) != 1 or G(n, n) != 1:
            return {"ok": False, "n": n}
        n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def r1_offsupport() -> dict:
    """8U-1 > 2m on s in [6U,10U), so r=1 is off reduced support."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for s in (6 * U, 8 * U, 10 * U - 1):
            m = 10 * U - s - 1
            if 8 * U - 1 <= 2 * m:
                return {"ok": False, "k": k, "s": s, "m": m}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def freshman_right() -> dict:
    """On p>10U, G(m+8U,d+8U)=G(m,d+8U) and G(m,d)=G(m,d-8U)=0."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        for s in (t0, t0 + U, 8 * U, t1 - 1):
            if not (t0 <= s < t1):
                continue
            m = 10 * U - s - 1
            for p in (10 * U + 1, 10 * U + 2, min(2 * s, 12 * U)):
                if p <= 10 * U or p > 2 * s:
                    continue
                d = 10 * U - p
                if G(m, d) != 0 or G(m, d - 8 * U) != 0:
                    return {"ok": False, "live": True, "k": k, "s": s, "p": p}
                got = G(m + 8 * U, d + 8 * U)
                want = G(m, d + 8 * U)
                if got != want:
                    return {"ok": False, "k": k, "s": s, "p": p, "got": got, "want": want}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def packed_right(kmax: int = 6) -> dict:
    """Delta_R equals reduced G(m,8U-r); r=1 live but contributes 0; r=2 XOR is 0."""
    rows = {}
    n_ok = 0
    n_r1_live = 0
    n_r2_zero = 0
    n_dr_ne_r2 = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        T10, T18 = 10 * U, 18 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        dR = dR_red = r2 = 0
        n_r1 = 0
        for s in range(t0, t1):
            A = (row << 1) & row
            m = T10 - s - 1
            tmp, p = A, 0
            while tmp:
                if tmp & 1 and p > 10 * U:
                    g18 = G(T18 - s - 1, T18 - p)
                    red = G(m, T18 - p)
                    if g18 != red:
                        return {"ok": False, "k": k, "s": s, "p": p}
                    dR ^= g18
                    dR_red ^= red
                    r = p - 10 * U
                    if r == 1:
                        n_r1 += 1
                        if g18:
                            return {"ok": False, "r1_contrib": True, "k": k}
                    if r == 2:
                        r2 ^= g18
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if dR != dR_red:
            return {"ok": False, "k": k, "dR": dR, "red": dR_red}
        if n_r1 == 0:
            return {"ok": False, "k": k, "r1_dead": True}
        n_ok += 1
        n_r1_live += 1
        if r2 == 0:
            n_r2_zero += 1
        if dR != r2:
            n_dr_ne_r2 += 1
        rows[str(k)] = {"dR": dR, "r2": r2, "n_r1": n_r1}
    return {
        "ok": n_ok == kmax - 1 and n_r1_live == n_ok and n_r2_zero == n_ok and n_dr_ne_r2 > 0,
        "n_ok": n_ok,
        "n_r1_live": n_r1_live,
        "n_r2_zero": n_r2_zero,
        "n_dr_ne_r2": n_dr_ne_r2,
        "rows": rows,
    }


def prefixes() -> dict:
    fj = json.loads(FJ_JSON.read_text())
    fi = json.loads(FI_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    ok = (
        fj["checks"]["all_ok"]
        and fi["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fj["verdict"]["Delta_L_eq_0"] == "LEMMA"
        and fj["verdict"]["Delta_eq_Delta_R"] == "LEMMA"
        and ff["verdict"]["G_nn_eq_1"] == "LEMMA"
        and fj["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, corn: dict, r1: dict, fresh: dict, right: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert corn["ok"] and r1["ok"] and fresh["ok"] and right["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    corn = corners()
    r1 = r1_offsupport()
    fresh = freshman_right()
    right = packed_right()
    pref = prefixes()
    checks = self_checks(c20, corn, r1, fresh, right, pref)
    dump = {
        "cycle": "FK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "corners": {k: corn[k] for k in corn if k != "ok"},
        "r1": {k: r1[k] for k in r1 if k != "ok"},
        "freshman": {k: fresh[k] for k in fresh if k != "ok"},
        "right": {k: right[k] for k in right if k != "ok"},
        "lemmas": {
            "G_n0_eq_G_n2n_eq_1": True,
            "freshman_right_reduces_to_G_m_8U_r": True,
            "r1_off_reduced_support": True,
            "Delta_R_eq_r2_xor": False,
            "r1_AND_never_live": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "G_n0_eq_G_n2n_eq_1": "LEMMA",
            "freshman_right_reduces_to_G_m_8U_r": "LEMMA",
            "r1_off_reduced_support": "LEMMA",
            "Delta_R_eq_r2_xor": "KILLED",
            "r1_AND_never_live": "KILLED",
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
    print("right", dump["right"])


if __name__ == "__main__":
    main()
