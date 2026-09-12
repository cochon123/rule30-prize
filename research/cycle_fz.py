#!/usr/bin/env python3
"""Cycle FZ: unclipped hi is 1 iff (s-t0) mod 2U is 0 (a odd) or a power of 2.

Cycle FY walks r(s)=(-s-1) mod 2U backward from 2U-1. That residue is a
one-zero bit iff the offset delta=s-t0 satisfies (delta mod 2U)=0 with
a=k+1 odd, or (delta mod 2U) is a positive power of 2. The whole-window
hi Green XOR is then (U-1) mod 2 (unclipped XOR vanishes; clipped tail
length U-1 is all 1s). Offset 0 is not always 1, and delta itself being
0 or a power of 2 misses the wrap. Do not claim J6=J10=0 implies J18=1
for all k; do not push even-spine past k=18; do not bump all n0=16 past
414990. Not a prize claim.

Run: python3 research/cycle_fz.py --certify
Dump: research/cycle_fz.json
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
from cycle_fw import want_one

OUT = Path(__file__).resolve().with_suffix(".json")
FY_JSON = Path(__file__).resolve().parent / "cycle_fy.json"
FX_JSON = Path(__file__).resolve().parent / "cycle_fx.json"
FW_JSON = Path(__file__).resolve().parent / "cycle_fw.json"


def dyadic_offset(delta: int, a: int, U: int) -> int:
    """Predicted unclipped hi G=1 from (s-t0) mod 2U."""
    r = delta % (2 * U)
    if r == 0:
        return a & 1
    return int(r > 0 and (r & (r - 1)) == 0)


def dyadic_times() -> dict:
    """want_one(r(s)) == dyadic_offset(s-t0) on the unclipped window."""
    n_ok = 0
    n_one = 0
    for k in range(0, 12):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in range(t0, clip + 1):
                r = (-s - 1) % (2 * U)
                p = dyadic_offset(s - t0, a, U)
                if want_one(r, a) != p:
                    return {"ok": False, "k": k, "s": s, "r": r, "pred": p}
                n_ok += 1
                n_one += p
    return {"ok": n_ok > 0 and n_one > 0, "n_ok": n_ok, "n_one": n_one}


def g_matches() -> dict:
    """G(m,2U-2) matches the dyadic-offset predicate, k<=7."""
    n_ok = 0
    for k in range(0, 8):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in range(t0, clip + 1):
                m = T - s - 1
                g = G(m, 2 * U - 2) if U > 1 else G(m, 0)
                if g != dyadic_offset(s - t0, a, U):
                    return {"ok": False, "k": k, "s": s, "g": g}
                n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def whole_window_xor() -> dict:
    """Whole-window hi Green XOR is (U-1) mod 2."""
    n_ok = 0
    for k in range(0, 12):
        U = 1 << k
        a = k + 1
        expect = (U - 1) & 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            xor = 0
            for s in range(t0, clip + 1):
                xor ^= dyadic_offset(s - t0, a, U)
            n_clip = T - clip - 1
            if n_clip != U - 1:
                return {"ok": False, "k": k, "n_clip": n_clip}
            whole = xor ^ (n_clip & 1)
            if xor != 0 or whole != expect:
                return {
                    "ok": False,
                    "k": k,
                    "W": W,
                    "unclip": xor,
                    "whole": whole,
                    "expect": expect,
                }
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def killed_offset0_always() -> dict:
    """Offset 0 is not always 1: k=1 (a even), W=4U, s=t0."""
    k = 1
    U = 1 << k
    a = k + 1
    W, T = 4 * U, 6 * U
    t0 = T - W // 2
    r = (-t0 - 1) % (2 * U)
    w = want_one(r, a)
    p = dyadic_offset(0, a, U)
    ok = w == 0 and p == 0 and (a & 1) == 0
    return {"ok": ok, "k": k, "s": t0, "want": w, "pred": p, "a": a}


def killed_delta_pow2_no_mod() -> dict:
    """delta itself 0-or-pow2 misses the wrap: k=2, W=8U, delta=2U+1."""
    k = 2
    U = 1 << k
    a = k + 1
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    delta = 2 * U + 1
    s = t0 + delta
    r = (-s - 1) % (2 * U)
    w = want_one(r, a)
    p = dyadic_offset(delta, a, U)
    naive = int(delta == 0 or (delta > 0 and (delta & (delta - 1)) == 0))
    ok = w == 1 and p == 1 and naive == 0
    return {
        "ok": ok,
        "k": k,
        "delta": delta,
        "want": w,
        "pred": p,
        "naive": naive,
    }


def prefixes() -> dict:
    fy = json.loads(FY_JSON.read_text())
    fx = json.loads(FX_JSON.read_text())
    fw = json.loads(FW_JSON.read_text())
    ok = (
        fy["checks"]["all_ok"]
        and fx["checks"]["all_ok"]
        and fw["checks"]["all_ok"]
        and fy["verdict"]["residue_walk_2U_minus_1_to_U_minus_1"] == "LEMMA"
        and fy["verdict"]["unclipped_hi_XOR_vanishes"] == "LEMMA"
        and fx["verdict"]["unclipped_hi_eq_want_one_minus_s_minus_1"] == "LEMMA"
        and fw["verdict"]["G_r_2a_minus_2_bit_pattern"] == "LEMMA"
        and fy["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    times: dict,
    gmatch: dict,
    ww: dict,
    k0: dict,
    kn: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert times["ok"] and gmatch["ok"] and ww["ok"]
    assert k0["ok"] and kn["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    times = dyadic_times()
    gmatch = g_matches()
    ww = whole_window_xor()
    k0 = killed_offset0_always()
    kn = killed_delta_pow2_no_mod()
    pref = prefixes()
    checks = self_checks(c20, times, gmatch, ww, k0, kn, pref)
    dump = {
        "cycle": "FZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "dyadic_times": {k: times[k] for k in times if k != "ok"},
        "g_matches": {k: gmatch[k] for k in gmatch if k != "ok"},
        "whole_window_xor": {k: ww[k] for k in ww if k != "ok"},
        "killed_offset0_always": {k: k0[k] for k in k0 if k != "ok"},
        "killed_delta_pow2_no_mod": {k: kn[k] for k in kn if k != "ok"},
        "lemmas": {
            "unclipped_hi_iff_dyadic_offset": True,
            "whole_window_hi_XOR_eq_U_minus_1_mod_2": True,
            "offset0_always_1": False,
            "delta_pow2_without_mod": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "unclipped_hi_iff_dyadic_offset": "LEMMA",
            "whole_window_hi_XOR_eq_U_minus_1_mod_2": "LEMMA",
            "offset0_always_1": "KILLED",
            "delta_pow2_without_mod": "KILLED",
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
    print("dyadic_times", dump["dyadic_times"])


if __name__ == "__main__":
    main()
