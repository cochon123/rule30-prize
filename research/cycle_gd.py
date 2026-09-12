#!/usr/bin/env python3
"""Cycle GD: in-cone hi/r* is 1 iff s = W + 2^j for 0<=j<a.

Cycle GC's in-cone residues [1,U] are the offsets 2^j from W: s=W+2^j
lies in [W+1, clip] and is exactly the G=1 set. In particular s=W+1
(j=0) always has G=1: m=2U-2 and G(m,m)=1. The range is not j<=a
(s=W+2U is after clip), and the base is W not t0. The AND at those
times is not always live. Do not claim J6=J10=0 implies J18=1 for all
k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_gd.py --certify
Dump: research/cycle_gd.json
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
GC_JSON = Path(__file__).resolve().parent / "cycle_gc.json"
GB_JSON = Path(__file__).resolve().parent / "cycle_gb.json"
FZ_JSON = Path(__file__).resolve().parent / "cycle_fz.json"


def w_plus_pow2() -> dict:
    """In-cone G=1 iff s=W+2^j; s=W+1 has m=2U-2 and G(m,m)=1."""
    n_ok = 0
    n_first = 0
    for k in range(0, 12):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            times = set()
            for j in range(a):
                s = W + (1 << j)
                if not (W + 1 <= s <= clip):
                    return {"ok": False, "k": k, "s": s}
                if dyadic_offset(s - t0, a, U) != 1:
                    return {"ok": False, "k": k, "s": s}
                times.add(s)
            got = {
                s
                for s in range(W + 1, clip + 1)
                if dyadic_offset(s - t0, a, U)
            }
            if got != times:
                return {"ok": False, "k": k, "W": W}
            s0 = W + 1
            m = T - s0 - 1
            if m != 2 * U - 2:
                return {"ok": False, "k": k, "m": m}
            gmm = G(m, m)
            if gmm != 1:
                return {"ok": False, "k": k, "Gmm": gmm}
            n_ok += 1
            n_first += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_first": n_first}


def g_matches() -> dict:
    """G(m,2U-2)=1 at s=W+2^j, k<=7."""
    n_ok = 0
    for k in range(0, 8):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            for j in range(a):
                s = W + (1 << j)
                m = T - s - 1
                g = G(m, 2 * U - 2) if U > 1 else G(m, 0)
                if g != 1:
                    return {"ok": False, "k": k, "s": s, "g": g}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_j_eq_a() -> dict:
    """j=a gives s=W+2U after clip."""
    k = 2
    U = 1 << k
    W = 8 * U
    clip = U + W
    s = W + 2 * U
    ok = s > clip and s == W + (1 << (k + 1))
    return {"ok": ok, "k": k, "s": s, "clip": clip}


def killed_t0_base() -> dict:
    """The in-cone ones are W+2^j, not t0+2^j."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    ok = t0 + 1 != W + 1
    return {"ok": ok, "k": k, "t0_plus_1": t0 + 1, "W_plus_1": W + 1}


def killed_and_all_live() -> dict:
    """AND at s=W+2^j is not all live (k=2, W=8U)."""
    k = 2
    U = 1 << k
    a = k + 1
    W, T = 8 * U, 10 * U
    clip = U + W
    rstar = W - 2 * U + 2
    targets = {W + (1 << j) for j in range(a)}
    row = 1
    for _ in range(W + 1):
        row = rule30_step(row)
    live1 = dead1 = 0
    for s in range(W + 1, clip + 1):
        A = (row << 1) & row
        if s in targets:
            on = ((A >> (T + rstar)) & 1) == 1
            if on:
                live1 += 1
            else:
                dead1 += 1
        row = rule30_step(row)
    ok = live1 > 0 and dead1 > 0
    return {"ok": ok, "k": k, "live1": live1, "dead1": dead1}


def prefixes() -> dict:
    gc = json.loads(GC_JSON.read_text())
    gb = json.loads(GB_JSON.read_text())
    fz = json.loads(FZ_JSON.read_text())
    ok = (
        gc["checks"]["all_ok"]
        and gb["checks"]["all_ok"]
        and fz["checks"]["all_ok"]
        and gc["verdict"]["incone_ones_count_eq_k_plus_1"] == "LEMMA"
        and gb["verdict"]["rstar_in_cone_iff_W_plus_1_to_clip"] == "LEMMA"
        and fz["verdict"]["unclipped_hi_iff_dyadic_offset"] == "LEMMA"
        and gc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    times: dict,
    gmatch: dict,
    kj: dict,
    kt: dict,
    ka: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert times["ok"] and gmatch["ok"]
    assert kj["ok"] and kt["ok"] and ka["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    times = w_plus_pow2()
    gmatch = g_matches()
    kj = killed_j_eq_a()
    kt = killed_t0_base()
    ka = killed_and_all_live()
    pref = prefixes()
    checks = self_checks(c20, times, gmatch, kj, kt, ka, pref)
    dump = {
        "cycle": "GD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "w_plus_pow2": {k: times[k] for k in times if k != "ok"},
        "g_matches": {k: gmatch[k] for k in gmatch if k != "ok"},
        "killed_j_eq_a": {k: kj[k] for k in kj if k != "ok"},
        "killed_t0_base": {k: kt[k] for k in kt if k != "ok"},
        "killed_and_all_live": {k: ka[k] for k in ka if k != "ok"},
        "lemmas": {
            "incone_hi_eq_1_iff_s_eq_W_plus_2j": True,
            "s_eq_W_plus_1_G_mm_eq_1": True,
            "j_up_to_a": False,
            "incone_ones_from_t0": False,
            "AND_at_W_plus_2j_all_live": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "incone_hi_eq_1_iff_s_eq_W_plus_2j": "LEMMA",
            "s_eq_W_plus_1_G_mm_eq_1": "LEMMA",
            "j_up_to_a": "KILLED",
            "incone_ones_from_t0": "KILLED",
            "AND_at_W_plus_2j_all_live": "KILLED",
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
    print("w_plus_pow2", dump["w_plus_pow2"])


if __name__ == "__main__":
    main()
