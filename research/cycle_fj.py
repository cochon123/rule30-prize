#!/usr/bin/env python3
"""Cycle FJ: left off-support XOR on [6U,10U) vanishes; Delta is the right strip.

Cycle FI's mismatch Delta = J_[6U,10U)->10U XOR J_[6U,10U)->18U is the
XOR of 18U-Green on 10U-off-support ANDs. Split those into the left
strip p < 2s-10U+2 (d>2m) and the right strip p>10U (d<0). Freshman
of the 8U-shift on the left reduces G(m+8U, d+8U) to G(m, d-8U) =
G(10U-s-1, 2U-p), which vanishes for p>2U. The whole left 2U-bit
strip sits in the left region (2s-10U+2 >= 2U+2). Packed XOR of that
strip is 0, so Delta_L=0 and Delta = Delta_R. Kills: Delta_R=1
(k=5 has 0); J_[10U,18U)->18U=1 (k=3 has 0). Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fj.py --certify
Dump: research/cycle_fj.json
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
FI_JSON = Path(__file__).resolve().parent / "cycle_fi.json"
FH_JSON = Path(__file__).resolve().parent / "cycle_fh.json"
FF_JSON = Path(__file__).resolve().parent / "cycle_ff.json"


def left_region() -> dict:
    """p<=2U sits in the left off-support strip on [6U,10U)."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for s in (6 * U, 8 * U, 10 * U - 1):
            lo = 2 * s - 10 * U + 2
            if lo < 2 * U + 2:
                return {"ok": False, "k": k, "s": s, "lo": lo}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def freshman_left() -> dict:
    """On the left strip, G(m+8U, d+8U)=G(m, d-8U) and extras G(m,d)=G(m,d+8U)=0."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        for s in (t0, t0 + U, 8 * U, t1 - 1):
            if not (t0 <= s < t1):
                continue
            m = 10 * U - s - 1
            lo = 2 * s - 10 * U + 2
            for p in (1, min(U, lo - 1) if lo > 1 else 1, 2 * U if 2 * U < lo else 1):
                if not (0 < p < lo):
                    continue
                d = 10 * U - p
                if G(m, d) != 0 or G(m, d + 8 * U) != 0:
                    return {"ok": False, "live": True, "k": k, "s": s, "p": p}
                got = G(m + 8 * U, d + 8 * U)
                want = G(m, d - 8 * U)
                if got != want:
                    return {"ok": False, "k": k, "s": s, "p": p, "got": got, "want": want}
                if p > 2 * U and want != 0:
                    return {"ok": False, "pgt2U": True, "k": k, "p": p}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def packed_split(kmax: int = 6) -> dict:
    """Delta_L=0; Delta=Delta_R; in-support 10U equals 18U."""
    rows = {}
    n_dl0 = 0
    n_dr1 = 0
    n_dr0 = 0
    for k in range(2, kmax + 1):
        U = 1 << k
        t0, t1 = 6 * U, 10 * U
        T10, T18 = 10 * U, 18 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        j10 = j18 = dL = dR = d_in = 0
        for s in range(t0, t1):
            A = (row << 1) & row
            lo = 2 * s - 10 * U + 2
            tmp, p = A, 0
            while tmp:
                if tmp & 1:
                    g10 = G(T10 - s - 1, T10 - p)
                    g18 = G(T18 - s - 1, T18 - p)
                    j10 ^= g10
                    j18 ^= g18
                    if p > 10 * U:
                        dR ^= g18
                        if g10:
                            return {"ok": False, "k": k, "s": s, "p": p, "right10": True}
                    elif p < lo:
                        dL ^= g18
                        red = G(T10 - s - 1, 2 * U - p)
                        if g18 != red:
                            return {"ok": False, "k": k, "s": s, "p": p, "red": (g18, red)}
                        if g10:
                            return {"ok": False, "k": k, "left10": True}
                    else:
                        d_in ^= g10
                        if g10 != g18:
                            return {"ok": False, "k": k, "s": s, "p": p, "ins": True}
                tmp >>= 1
                p += 1
            row = rule30_step(row)
        if dL != 0:
            return {"ok": False, "k": k, "dL": dL}
        if j10 != d_in or j18 != (d_in ^ dR) or (j10 ^ j18) != dR:
            return {"ok": False, "k": k, "split": (j10, j18, d_in, dR)}
        n_dl0 += 1
        if dR == 1:
            n_dr1 += 1
        else:
            n_dr0 += 1
        rows[str(k)] = {"J10": j10, "J18": j18, "dL": dL, "dR": dR}
    return {
        "ok": n_dl0 == kmax - 1 and n_dr0 > 0 and n_dr1 > 0,
        "n_dl0": n_dl0,
        "n_dr0": n_dr0,
        "n_dr1": n_dr1,
        "rows": rows,
    }


def killed_tail() -> dict:
    """J_[10U,18U)->18U is not identically 1: k=3 vanishes."""
    k = 3
    U = 1 << k
    t0, t1, T = 10 * U, 18 * U, 18 * U
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    j = 0
    n_p1 = 0
    for s in range(t0, t1):
        A = (row << 1) & row
        if A & 2:
            n_p1 += 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1:
                j ^= G(T - s - 1, T - p)
            tmp >>= 1
            p += 1
        row = rule30_step(row)
    ok = j == 0 and n_p1 == 8 * U
    return {"ok": ok, "k": 3, "Jtail": j, "n_p1": n_p1, "window": 8 * U}


def prefixes() -> dict:
    fi = json.loads(FI_JSON.read_text())
    fh = json.loads(FH_JSON.read_text())
    ff = json.loads(FF_JSON.read_text())
    ok = (
        fi["checks"]["all_ok"]
        and fh["checks"]["all_ok"]
        and ff["checks"]["all_ok"]
        and fi["verdict"]["FF_on_support_8U_shift"] == "LEMMA"
        and fi["verdict"]["J_6U_10U_to_10U_eq_to_18U"] == "KILLED"
        and fh["verdict"]["J18_eq_J6_xor_Jpost"] == "LEMMA"
        and fi["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, left: dict, fresh: dict, split: dict, tail: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert left["ok"] and fresh["ok"] and split["ok"] and tail["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    left = left_region()
    fresh = freshman_left()
    split = packed_split()
    tail = killed_tail()
    pref = prefixes()
    checks = self_checks(c20, left, fresh, split, tail, pref)
    dump = {
        "cycle": "FJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "left_region": {k: left[k] for k in left if k != "ok"},
        "freshman": {k: fresh[k] for k in fresh if k != "ok"},
        "split": {k: split[k] for k in split if k != "ok"},
        "killed_tail": {k: tail[k] for k in tail if k != "ok"},
        "lemmas": {
            "left_2U_in_offsupport": True,
            "freshman_left_reduces_to_G_m_2U_p": True,
            "Delta_L_eq_0": True,
            "Delta_eq_Delta_R": True,
            "Delta_R_eq_1": False,
            "J_10U_18U_to_18U_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "left_2U_in_offsupport": "LEMMA",
            "freshman_left_reduces_to_G_m_2U_p": "LEMMA",
            "Delta_L_eq_0": "LEMMA",
            "Delta_eq_Delta_R": "LEMMA",
            "Delta_R_eq_1": "KILLED",
            "J_10U_18U_to_18U_eq_1": "KILLED",
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
    print("split", dump["split"])
    print("killed_tail", dump["killed_tail"])


if __name__ == "__main__":
    main()
