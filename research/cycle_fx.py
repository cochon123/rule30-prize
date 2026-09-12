#!/usr/bin/env python3
"""Cycle FX: unclipped cone-hi is 1 iff ((-s-1) mod 2U) is a one-zero residue.

On the unified T=2U+W band, W is 0 mod 2U for W in {4U,8U,16U}, so
m=T-s-1 ≡ -s-1 (mod 2U). Cycle FS says the unclipped cone-hi Green is
G(m,2U-2); Cycle FW evaluates that by the one-zero pattern at scale
k+1 on r=m mod 2U. Hence G=1 iff want_one((-s-1) mod 2U, k+1)=1.
The hi AND does not fire whenever G=1, and G is not identically 1.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_fx.py --certify
Dump: research/cycle_fx.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
FW_JSON = Path(__file__).resolve().parent / "cycle_fw.json"
FS_JSON = Path(__file__).resolve().parent / "cycle_fs.json"
FQ_JSON = Path(__file__).resolve().parent / "cycle_fq.json"


def w_mod_2U() -> dict:
    """W in {4U,8U,16U} is 0 mod 2U."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            if W % (2 * U) != 0:
                return {"ok": False, "k": k, "W": W}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def hi_vs_s() -> dict:
    """Unclipped G(m,2U-2)=want_one((-s-1) mod 2U, k+1)."""
    n_ok = 0
    n_one = 0
    for k in range(0, 8):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in (t0, t0 + max(U, 1), clip - 1, clip):
                if not (t0 <= s <= clip and s < T):
                    continue
                m = T - s - 1
                g = G(m, 2 * U - 2) if U > 1 else G(m, 0)
                r = (-s - 1) % (2 * U)
                if g != want_one(r, a):
                    return {"ok": False, "k": k, "W": W, "s": s, "g": g, "r": r}
                n_ok += 1
                n_one += g
    return {"ok": n_ok > 0 and n_one > 0, "n_ok": n_ok, "n_one": n_one}


def killed_g_always_one() -> dict:
    """Unclipped hi Green is not identically 1: k=2, W=8U, s=9U-1."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    s = U + W - 1  # clip-1 = 9U-1
    m = T - s - 1
    g = G(m, 2 * U - 2)
    r = (-s - 1) % (2 * U)
    ok = g == 0 and want_one(r, k + 1) == 0
    return {"ok": ok, "k": k, "s": s, "G": g, "r": r}


def killed_and_when_g1() -> dict:
    """Hi AND does not fire whenever G=1 (k=2, W=8U unclipped)."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    clip = U + W
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    live1 = dead1 = 0
    for s in range(t0, min(clip, T)):
        A = (row << 1) & row
        r_hi = 2 * s - T
        g = G(T - s - 1, 2 * U - 2)
        on = ((A >> (T + r_hi)) & 1) == 1
        if g:
            if on:
                live1 += 1
            else:
                dead1 += 1
        row = rule30_step(row)
    ok = live1 > 0 and dead1 > 0
    return {"ok": ok, "k": k, "live1": live1, "dead1": dead1}


def prefixes() -> dict:
    fw = json.loads(FW_JSON.read_text())
    fs = json.loads(FS_JSON.read_text())
    fq = json.loads(FQ_JSON.read_text())
    ok = (
        fw["checks"]["all_ok"]
        and fs["checks"]["all_ok"]
        and fq["checks"]["all_ok"]
        and fw["verdict"]["G_r_2a_minus_2_bit_pattern"] == "LEMMA"
        and fs["verdict"]["unclipped_cone_hi_eq_G_m_2U_minus_2"] == "LEMMA"
        and fq["verdict"]["G_n_plus_2a_d_eq_G_n_d_for_d_lt_2a"] == "LEMMA"
        and fw["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, wmod: dict, hi: dict, kg: dict, ka: dict, pref: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert wmod["ok"] and hi["ok"] and kg["ok"] and ka["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    wmod = w_mod_2U()
    hi = hi_vs_s()
    kg = killed_g_always_one()
    ka = killed_and_when_g1()
    pref = prefixes()
    checks = self_checks(c20, wmod, hi, kg, ka, pref)
    dump = {
        "cycle": "FX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "w_mod": {k: wmod[k] for k in wmod if k != "ok"},
        "hi_vs_s": {k: hi[k] for k in hi if k != "ok"},
        "killed_g_always_one": {k: kg[k] for k in kg if k != "ok"},
        "killed_and_when_g1": {k: ka[k] for k in ka if k != "ok"},
        "lemmas": {
            "W_eq_0_mod_2U": True,
            "unclipped_hi_eq_want_one_minus_s_minus_1": True,
            "unclipped_hi_always_1": False,
            "hi_AND_whenever_G_eq_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "W_eq_0_mod_2U": "LEMMA",
            "unclipped_hi_eq_want_one_minus_s_minus_1": "LEMMA",
            "unclipped_hi_always_1": "KILLED",
            "hi_AND_whenever_G_eq_1": "KILLED",
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
    print("hi_vs_s", dump["hi_vs_s"])


if __name__ == "__main__":
    main()
