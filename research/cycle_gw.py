#!/usr/bin/env python3
"""Cycle GW: even-s Green is the coboundary of the next odd-s row.

Odd-r: G(s,r)=G(s+1,r+1), and r+1 is always in the odd-s band.
Even-r: G(s,r)=G(s+1,r) XOR G(s+1,r+2) whenever r+2 is in-band;
that fails at the clipped right edge r=W. Do not claim J6=J10=0
implies J18=1 for all k; do not push even-spine past k=18; do not
bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gw.py --certify
Dump: research/cycle_gw.json
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

OUT = Path(__file__).resolve().with_suffix(".json")
GV_JSON = Path(__file__).resolve().parent / "cycle_gv.json"
GU_JSON = Path(__file__).resolve().parent / "cycle_gu.json"
GT_JSON = Path(__file__).resolve().parent / "cycle_gt.json"


def _band(s: int, t0: int, T: int, W: int) -> tuple[int, int]:
    lo = 2 * (s - t0 + 1)
    hi = min(2 * s - T, W)
    return lo, hi


def copy_odd_r() -> dict:
    """G(s, odd r)=G(s+1, r+1); r+1 always in the odd-s band. k<=6."""
    n_ok = 0
    n_r1 = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            for s in range(t0, T - 1):
                if s % 2:
                    continue
                lo, hi = _band(s, t0, T, W)
                lo1, hi1 = _band(s + 1, t0, T, W)
                if hi < lo:
                    continue
                m = T - s - 1
                m1 = T - (s + 1) - 1
                for r in range(lo, hi + 1):
                    if r % 2 == 0:
                        continue
                    r1 = r + 1
                    if not (lo1 <= r1 <= hi1):
                        return {"ok": False, "r1_out": True, "k": k, "s": s, "r": r}
                    n_r1 += 1
                    g = G(m, W - r)
                    g1 = G(m1, W - r1)
                    if g != g1:
                        return {"ok": False, "k": k, "s": s, "r": r, "g": g, "g1": g1}
                    n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_r1_in_band": n_r1}


def coboundary_even_r() -> dict:
    """G(s, even r)=G(s+1,r) XOR G(s+1,r+2) when r+2 in-band. k<=6."""
    n_ok = 0
    n_edge = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in range(t0, T - 1):
                if s % 2:
                    continue
                lo, hi = _band(s, t0, T, W)
                lo1, hi1 = _band(s + 1, t0, T, W)
                if hi < lo:
                    continue
                m = T - s - 1
                m1 = T - (s + 1) - 1
                for r in range(lo, hi + 1, 2):
                    in2 = lo1 <= r + 2 <= hi1
                    g = G(m, W - r)
                    if in2:
                        g0 = G(m1, W - r)
                        g2 = G(m1, W - (r + 2))
                        if g != (g0 ^ g2):
                            return {
                                "ok": False,
                                "k": k,
                                "s": s,
                                "r": r,
                                "g": g,
                                "want": g0 ^ g2,
                            }
                        n_ok += 1
                    else:
                        if not (s >= clip and r == W):
                            return {
                                "ok": False,
                                "unexpected_out": True,
                                "k": k,
                                "s": s,
                                "r": r,
                            }
                        n_edge += 1
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_clip_edge": n_edge}


def killed_cobound_clip() -> dict:
    """Coboundary fails at clipped r=W: k=1, W=4U, s=10, r=8."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    clip = U + W
    s, r = 10, W
    lo1, hi1 = _band(s + 1, t0, T, W)
    g = G(T - s - 1, W - r)
    g0 = G(T - (s + 1) - 1, W - r)
    ok = (
        s >= clip
        and r == W
        and not (lo1 <= r + 2 <= hi1)
        and g == 1
        and g0 == 1
    )
    return {"ok": ok, "k": k, "s": s, "r": r, "G": g, "G_odd_r": g0}


def killed_copy_even_r() -> dict:
    """Copy G(s,r)=G(s+1,r+1) is not for even r: k=0, W=4U, s=4, r=2."""
    k = 0
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    s, r = 4, 2
    g = G(T - s - 1, W - r)
    g1 = G(T - (s + 1) - 1, W - (r + 1))
    ok = r % 2 == 0 and g == 1 and g1 == 0
    return {"ok": ok, "k": k, "s": s, "r": r, "G": g, "G_next": g1}


def killed_independent() -> dict:
    """Even-s Green is not independent of the next odd-s row."""
    k = 1
    U = 1 << k
    W = 4 * U
    T = 2 * U + W
    t0 = T - W // 2
    s, r = t0, 3
    g = G(T - s - 1, W - r)
    g1 = G(T - (s + 1) - 1, W - (r + 1))
    ok = r % 2 == 1 and g == g1 == 1
    return {"ok": ok, "k": k, "s": s, "r": r, "G": g, "G_next": g1}


def prefixes() -> dict:
    gv = json.loads(GV_JSON.read_text())
    gu = json.loads(GU_JSON.read_text())
    gt = json.loads(GT_JSON.read_text())
    ok = (
        gv["checks"]["all_ok"]
        and gu["checks"]["all_ok"]
        and gt["checks"]["all_ok"]
        and gv["verdict"]["even_s_m_eq_2n_plus_1_n_odd_clock"] == "LEMMA"
        and gu["verdict"]["odd_s_even_r_G_eq_G_odd_clock"] == "LEMMA"
        and gt["verdict"]["k4_AND_lo_dead_on_covering_hits"] == "LEMMA"
        and gv["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, cp: dict, cb: dict, kc: dict, ke: dict, ki: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert cp["ok"] and cb["ok"]
    assert kc["ok"] and ke["ok"] and ki["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    cp = copy_odd_r()
    cb = coboundary_even_r()
    kc = killed_cobound_clip()
    ke = killed_copy_even_r()
    ki = killed_independent()
    pref = prefixes()
    checks = self_checks(c20, cp, cb, kc, ke, ki, pref)
    dump = {
        "cycle": "GW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "copy_odd_r": {k: cp[k] for k in cp if k != "ok"},
        "coboundary_even_r": {k: cb[k] for k in cb if k != "ok"},
        "killed_cobound_clip": {k: kc[k] for k in kc if k != "ok"},
        "killed_copy_even_r": {k: ke[k] for k in ke if k != "ok"},
        "killed_independent": {k: ki[k] for k in ki if k != "ok"},
        "lemmas": {
            "even_s_odd_r_G_eq_next_odd_s_r_plus_1": True,
            "even_s_even_r_coboundary_when_r_plus_2_in_band": True,
            "r_plus_1_always_in_odd_s_band": True,
            "coboundary_at_clipped_r_W": False,
            "copy_on_even_r": False,
            "even_s_G_independent_of_odd_s": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "even_s_odd_r_G_eq_next_odd_s_r_plus_1": "LEMMA",
            "even_s_even_r_coboundary_when_r_plus_2_in_band": "LEMMA",
            "r_plus_1_always_in_odd_s_band": "LEMMA",
            "coboundary_at_clipped_r_W": "KILLED",
            "copy_on_even_r": "KILLED",
            "even_s_G_independent_of_odd_s": "KILLED",
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
    print("copy_odd_r", dump["copy_odd_r"])
    print("coboundary_even_r", dump["coboundary_even_r"])
    print("killed_cobound_clip", dump["killed_cobound_clip"])
    print("killed_copy_even_r", dump["killed_copy_even_r"])
    print("killed_independent", dump["killed_independent"])


if __name__ == "__main__":
    main()
