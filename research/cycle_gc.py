#!/usr/bin/env python3
"""Cycle GC: r* is in-cone for U times; ones-count is k+1 independent of W.

Cycle GB puts r*=W-2U+2 in the cone-band iff W+1<=s<=clip. That interval
has length U, independent of covering W. On it, (s-t0) mod 2U runs
through [1,U] (never 0), so Cycle FZ's hi/r* Green is 1 iff the residue
is a positive power of 2; the ones-count is a=k+1, independent of W.
The length does depend on W if misread as scaling with the window; offset
0 is not in-cone; the AND does not fire on all k+1 times. Do not claim
J6=J10=0 implies J18=1 for all k; do not push even-spine past k=18;
do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gc.py --certify
Dump: research/cycle_gc.json
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
from cycle_fz import dyadic_offset
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GB_JSON = Path(__file__).resolve().parent / "cycle_gb.json"
GA_JSON = Path(__file__).resolve().parent / "cycle_ga.json"
FZ_JSON = Path(__file__).resolve().parent / "cycle_fz.json"


def incone_window() -> dict:
    """[W+1, clip] has length U; residues [1,U]; ones-count a=k+1."""
    n_ok = 0
    n_one = 0
    for k in range(0, 12):
        U = 1 << k
        a = k + 1
        pow2 = {1 << j for j in range(a)}
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            if W + 1 < t0 or clip >= T:
                return {"ok": False, "k": k, "W": W}
            if clip - (W + 1) + 1 != U:
                return {"ok": False, "k": k, "L": clip - (W + 1) + 1}
            got = set()
            for s in range(W + 1, clip + 1):
                r = (s - t0) % (2 * U)
                if not (1 <= r <= U):
                    return {"ok": False, "k": k, "s": s, "r": r}
                p = dyadic_offset(s - t0, a, U)
                if p:
                    if r not in pow2:
                        return {"ok": False, "k": k, "r": r}
                    got.add(r)
                n_ok += 1
                n_one += p
            if got != pow2:
                return {"ok": False, "k": k, "W": W, "got": sorted(got)}
    return {"ok": n_ok > 0 and n_one > 0, "n_ok": n_ok, "n_one": n_one}


def g_matches() -> dict:
    """G(m,2U-2) matches the in-cone dyadic prediction, k<=7."""
    n_ok = 0
    for k in range(0, 8):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in range(W + 1, clip + 1):
                m = T - s - 1
                g = G(m, 2 * U - 2) if U > 1 else G(m, 0)
                if g != dyadic_offset(s - t0, a, U):
                    return {"ok": False, "k": k, "s": s, "g": g}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_length_depends_W() -> dict:
    """In-cone length does not depend on W: always U."""
    k = 2
    U = 1 << k
    lengths = []
    for W in (4 * U, 8 * U, 16 * U):
        clip = U + W
        lengths.append(clip - (W + 1) + 1)
    ok = lengths == [U, U, U]
    return {"ok": ok, "k": k, "lengths": lengths, "U": U}


def killed_offset0_incone() -> dict:
    """Offset 0 (s=t0) is before the in-cone window."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    ok = t0 < W + 1
    return {"ok": ok, "k": k, "t0": t0, "W_plus_1": W + 1}


def killed_count_eq_N() -> dict:
    """Ones-count is a, not N=a+(a mod 2): a=3 would be N=4."""
    k = 2
    U = 1 << k
    a = k + 1
    N = a + (a & 1)
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    clip = U + W
    ones = sum(dyadic_offset(s - t0, a, U) for s in range(W + 1, clip + 1))
    ok = ones == a and ones != N
    return {"ok": ok, "k": k, "ones": ones, "a": a, "N": N}


def killed_and_all_live() -> dict:
    """AND at r* is not live on all in-cone G=1 times (k=2, W=8U)."""
    k = 2
    U = 1 << k
    a = k + 1
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    clip = U + W
    rstar = W - 2 * U + 2
    row = 1
    for _ in range(W + 1):
        row = rule30_step(row)
    live1 = dead1 = 0
    for s in range(W + 1, clip + 1):
        A = (row << 1) & row
        on = ((A >> (T + rstar)) & 1) == 1
        if dyadic_offset(s - t0, a, U):
            if on:
                live1 += 1
            else:
                dead1 += 1
        row = rule30_step(row)
    ok = live1 > 0 and dead1 > 0
    return {"ok": ok, "k": k, "live1": live1, "dead1": dead1}


def prefixes() -> dict:
    gb = json.loads(GB_JSON.read_text())
    ga = json.loads(GA_JSON.read_text())
    fz = json.loads(FZ_JSON.read_text())
    ok = (
        gb["checks"]["all_ok"]
        and ga["checks"]["all_ok"]
        and fz["checks"]["all_ok"]
        and gb["verdict"]["rstar_in_cone_iff_W_plus_1_to_clip"] == "LEMMA"
        and ga["verdict"]["unclipped_hi_times_q_param"] == "LEMMA"
        and fz["verdict"]["unclipped_hi_iff_dyadic_offset"] == "LEMMA"
        and gb["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    win: dict,
    gmatch: dict,
    kl: dict,
    k0: dict,
    kn: dict,
    ka: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert win["ok"] and gmatch["ok"]
    assert kl["ok"] and k0["ok"] and kn["ok"] and ka["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    win = incone_window()
    gmatch = g_matches()
    kl = killed_length_depends_W()
    k0 = killed_offset0_incone()
    kn = killed_count_eq_N()
    ka = killed_and_all_live()
    pref = prefixes()
    checks = self_checks(c20, win, gmatch, kl, k0, kn, ka, pref)
    dump = {
        "cycle": "GC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "incone_window": {k: win[k] for k in win if k != "ok"},
        "g_matches": {k: gmatch[k] for k in gmatch if k != "ok"},
        "killed_length_depends_W": {k: kl[k] for k in kl if k != "ok"},
        "killed_offset0_incone": {k: k0[k] for k in k0 if k != "ok"},
        "killed_count_eq_N": {k: kn[k] for k in kn if k != "ok"},
        "killed_and_all_live": {k: ka[k] for k in ka if k != "ok"},
        "lemmas": {
            "rstar_incone_length_eq_U": True,
            "incone_ones_count_eq_k_plus_1": True,
            "incone_length_depends_on_W": False,
            "offset0_in_incone_window": False,
            "incone_ones_count_eq_N": False,
            "incone_AND_all_live": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "rstar_incone_length_eq_U": "LEMMA",
            "incone_ones_count_eq_k_plus_1": "LEMMA",
            "incone_length_depends_on_W": "KILLED",
            "offset0_in_incone_window": "KILLED",
            "incone_ones_count_eq_N": "KILLED",
            "incone_AND_all_live": "KILLED",
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
    print("incone_window", dump["incone_window"])


if __name__ == "__main__":
    main()
