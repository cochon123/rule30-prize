#!/usr/bin/env python3
"""Cycle GE: at s=W+2^j, m=2U-1-2^j; right-edge AND live iff t odd.

On Cycle GD's times s=W+2^j the Green clock is m=2U-1-2^j, interpolating
the diagonal m=2U-2 at j=0 to the clip corner m=U-1 at j=a-1. Cone-hi
equals r* iff j=0 (the palindrome pair collapses). Packed bit 2t is the
right edge x(t,t)=1; the right-edge AND (bits 2t and 2t-1) is live iff
t is odd. Covering W is even, so s=W+1 is odd and the collapsed cell
has G=1 and live AND. Right-edge AND is not always live; collapse is
not for all j. Do not claim J6=J10=0 implies J18=1 for all k; do not
push even-spine past k=18; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_ge.py --certify
Dump: research/cycle_ge.json
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
from cycle_ca import KNOWN20, packed_center_bits
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
GD_JSON = Path(__file__).resolve().parent / "cycle_gd.json"
GB_JSON = Path(__file__).resolve().parent / "cycle_gb.json"


def m_and_collapse() -> dict:
    """m=2U-1-2^j; cone-hi=r* iff j=0."""
    n_ok = 0
    n_col = 0
    for k in range(0, 12):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            rstar = W - 2 * U + 2
            for j in range(a):
                s = W + (1 << j)
                m = T - s - 1
                if m != 2 * U - 1 - (1 << j):
                    return {"ok": False, "k": k, "j": j, "m": m}
                chi = 2 * s - T
                if (chi == rstar) != (j == 0):
                    return {"ok": False, "k": k, "j": j, "chi": chi, "rstar": rstar}
                n_ok += 1
                n_col += int(j == 0)
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_collapse": n_col}


def right_edge(tmax: int = 256) -> dict:
    """Bit 2t=1; bit 2t-1 = t mod 2; AND at 2t live iff t odd. t=1..tmax."""
    n_ok = 0
    n_odd = 0
    row = 1
    row = rule30_step(row)
    for t in range(1, tmax + 1):
        b_edge = (row >> (2 * t)) & 1
        b_prev = (row >> (2 * t - 1)) & 1
        A = (row << 1) & row
        on = ((A >> (2 * t)) & 1) == 1
        if b_edge != 1 or b_prev != (t & 1) or on != bool(t & 1):
            return {"ok": False, "t": t, "edge": b_edge, "prev": b_prev, "AND": int(on)}
        n_ok += 1
        n_odd += t & 1
        row = rule30_step(row)
    return {"ok": n_ok == tmax and n_odd == tmax // 2, "n_ok": n_ok, "n_odd": n_odd, "tmax": tmax}


def collapsed_and_live() -> dict:
    """At s=W+1 the collapsed cell AND is live (k<=6, all covering W)."""
    n_ok = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            s = W + 1
            rstar = W - 2 * U + 2
            if 2 * s - T != rstar:
                return {"ok": False, "k": k, "chi": 2 * s - T}
            if (s & 1) != 1:
                return {"ok": False, "k": k, "s": s}
            row = 1
            for _ in range(s):
                row = rule30_step(row)
            A = (row << 1) & row
            on = ((A >> (T + rstar)) & 1) == 1
            if not on or T + rstar != 2 * s:
                return {"ok": False, "k": k, "W": W, "AND": int(on)}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_and_always() -> dict:
    """Right-edge AND is not always live: t=2."""
    row = 1
    row = rule30_step(row)
    row = rule30_step(row)
    A = (row << 1) & row
    on = ((A >> 4) & 1) == 1
    return {"ok": not on, "t": 2, "AND": int(on)}


def killed_collapse_all_j() -> dict:
    """Collapse only at j=0: k=2, W=8U, j=1."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    rstar = W - 2 * U + 2
    s = W + 2
    chi = 2 * s - T
    ok = chi != rstar
    return {"ok": ok, "k": k, "j": 1, "chi": chi, "rstar": rstar}


def killed_pair_xor0() -> dict:
    """Palindrome-pair AND XOR is not 0: k=4, W=4U, j=4."""
    k = 4
    U = 1 << k
    a = k + 1
    W, T = 4 * U, 6 * U
    rstar = W - 2 * U + 2
    row = 1
    for _ in range(W + 1):
        row = rule30_step(row)
    s_cur = W + 1
    xor = 0
    hit = None
    for j in range(a):
        s = W + (1 << j)
        while s_cur < s:
            row = rule30_step(row)
            s_cur += 1
        A = (row << 1) & row
        chi = 2 * s - T
        on_hi = ((A >> (T + chi)) & 1) == 1
        on_r = ((A >> (T + rstar)) & 1) == 1
        xor ^= int(on_hi) ^ int(on_r)
        if j == 4:
            hit = (int(on_hi), int(on_r))
    ok = xor == 1 and hit == (0, 1)
    return {"ok": ok, "k": k, "xor": xor, "j4": hit}


def prefixes() -> dict:
    gd = json.loads(GD_JSON.read_text())
    gb = json.loads(GB_JSON.read_text())
    ok = (
        gd["checks"]["all_ok"]
        and gb["checks"]["all_ok"]
        and gd["verdict"]["incone_hi_eq_1_iff_s_eq_W_plus_2j"] == "LEMMA"
        and gd["verdict"]["s_eq_W_plus_1_G_mm_eq_1"] == "LEMMA"
        and gb["verdict"]["cone_hi_dual_eq_stationary_W_minus_2U_plus_2"] == "LEMMA"
        and gd["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    mc: dict,
    edge: dict,
    live: dict,
    ka: dict,
    kc: dict,
    kx: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert mc["ok"] and edge["ok"] and live["ok"]
    assert ka["ok"] and kc["ok"] and kx["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    mc = m_and_collapse()
    edge = right_edge()
    live = collapsed_and_live()
    ka = killed_and_always()
    kc = killed_collapse_all_j()
    kx = killed_pair_xor0()
    pref = prefixes()
    checks = self_checks(c20, mc, edge, live, ka, kc, kx, pref)
    dump = {
        "cycle": "GE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "m_and_collapse": {k: mc[k] for k in mc if k != "ok"},
        "right_edge": {k: edge[k] for k in edge if k != "ok"},
        "collapsed_and_live": {k: live[k] for k in live if k != "ok"},
        "killed_and_always": {k: ka[k] for k in ka if k != "ok"},
        "killed_collapse_all_j": {k: kc[k] for k in kc if k != "ok"},
        "killed_pair_xor0": {k: kx[k] for k in kx if k != "ok"},
        "lemmas": {
            "m_eq_2U_minus_1_minus_2j": True,
            "cone_hi_eq_rstar_iff_j_eq_0": True,
            "right_edge_AND_live_iff_t_odd": True,
            "collapsed_cell_AND_live": True,
            "right_edge_AND_always_live": False,
            "collapse_all_j": False,
            "pair_AND_XOR_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "m_eq_2U_minus_1_minus_2j": "LEMMA",
            "cone_hi_eq_rstar_iff_j_eq_0": "LEMMA",
            "right_edge_AND_live_iff_t_odd": "LEMMA",
            "collapsed_cell_AND_live": "LEMMA",
            "right_edge_AND_always_live": "KILLED",
            "collapse_all_j": "KILLED",
            "pair_AND_XOR_eq_0": "KILLED",
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
    print("right_edge", dump["right_edge"])


if __name__ == "__main__":
    main()
