#!/usr/bin/env python3
"""Cycle GF: unclipped cone-hi AND is live iff s is odd.

Unclipped cone-hi sits at packed bit T+(2s-T)=2s, the right edge, so
Cycle GE's odd-t criterion applies: the AND is live iff s is odd. Covering
W is even, so among s=W+2^j only j=0 (s=W+1) is odd; the other G=1
in-cone times have dead cone-hi AND. After clip the band-hi is r=W, not
the right edge, and that AND is not iff s odd. r* AND is not iff s odd.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gf.py --certify
Dump: research/cycle_gf.json
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
GE_JSON = Path(__file__).resolve().parent / "cycle_ge.json"
GD_JSON = Path(__file__).resolve().parent / "cycle_gd.json"


def packed_is_right_edge() -> dict:
    """T+(2s-T)=2s on the unclipped window."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in (t0, (t0 + clip) // 2, clip):
                if T + (2 * s - T) != 2 * s:
                    return {"ok": False, "k": k, "s": s}
                n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def only_j0_odd() -> dict:
    """Among s=W+2^j, only j=0 is odd (W even; 2^j even for j>=1)."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            if W % 2:
                return {"ok": False, "k": k, "W": W}
            for j in range(a):
                s = W + (1 << j)
                odd = bool(s & 1)
                if odd != (j == 0):
                    return {"ok": False, "k": k, "j": j, "s": s}
                n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def cone_hi_and_odd() -> dict:
    """Unclipped cone-hi AND live iff s odd, k<=6."""
    n_ok = 0
    n_live = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            row = 1
            for _ in range(t0):
                row = rule30_step(row)
            for s in range(t0, clip + 1):
                A = (row << 1) & row
                chi = 2 * s - T
                on = ((A >> (T + chi)) & 1) == 1
                if on != bool(s & 1):
                    return {"ok": False, "k": k, "s": s, "AND": int(on)}
                n_ok += 1
                n_live += int(on)
                row = rule30_step(row)
    return {"ok": n_ok > 0 and n_live > 0, "n_ok": n_ok, "n_live": n_live}


def killed_after_clip_iff_odd() -> dict:
    """After clip, band-hi AND is not iff s odd: k=2, W=8U."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    clip = U + W
    row = 1
    for _ in range(clip + 1):
        row = rule30_step(row)
    mism = 0
    for s in range(clip + 1, T):
        A = (row << 1) & row
        on = ((A >> (T + W)) & 1) == 1
        if on != bool(s & 1):
            mism += 1
        row = rule30_step(row)
    ok = mism > 0
    return {"ok": ok, "k": k, "mism": mism}


def killed_rstar_iff_odd() -> dict:
    """r* AND is not iff s odd: k=2, W=8U, 1 live / 5 dead on odd s."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    clip = U + W
    rstar = W - 2 * U + 2
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    live_odd = dead_odd = 0
    for s in range(t0, clip + 1):
        A = (row << 1) & row
        on = ((A >> (T + rstar)) & 1) == 1
        if s & 1:
            if on:
                live_odd += 1
            else:
                dead_odd += 1
        row = rule30_step(row)
    ok = live_odd > 0 and dead_odd > 0
    return {"ok": ok, "k": k, "live_odd": live_odd, "dead_odd": dead_odd}


def killed_clip_and_live() -> dict:
    """Clip cone-hi AND is dead for k>=1: k=2, W=8U, clip even."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    clip = U + W
    row = 1
    for _ in range(clip):
        row = rule30_step(row)
    A = (row << 1) & row
    chi = 2 * clip - T
    on = ((A >> (T + chi)) & 1) == 1
    ok = chi == W and (clip & 1) == 0 and not on
    return {"ok": ok, "k": k, "s": clip, "AND": int(on)}


def prefixes() -> dict:
    ge = json.loads(GE_JSON.read_text())
    gd = json.loads(GD_JSON.read_text())
    ok = (
        ge["checks"]["all_ok"]
        and gd["checks"]["all_ok"]
        and ge["verdict"]["right_edge_AND_live_iff_t_odd"] == "LEMMA"
        and ge["verdict"]["collapsed_cell_AND_live"] == "LEMMA"
        and gd["verdict"]["incone_hi_eq_1_iff_s_eq_W_plus_2j"] == "LEMMA"
        and ge["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    pk: dict,
    j0: dict,
    odd: dict,
    ka: dict,
    kr: dict,
    kc: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pk["ok"] and j0["ok"] and odd["ok"]
    assert ka["ok"] and kr["ok"] and kc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pk = packed_is_right_edge()
    j0 = only_j0_odd()
    odd = cone_hi_and_odd()
    ka = killed_after_clip_iff_odd()
    kr = killed_rstar_iff_odd()
    kc = killed_clip_and_live()
    pref = prefixes()
    checks = self_checks(c20, pk, j0, odd, ka, kr, kc, pref)
    dump = {
        "cycle": "GF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "packed_is_right_edge": {k: pk[k] for k in pk if k != "ok"},
        "only_j0_odd": {k: j0[k] for k in j0 if k != "ok"},
        "cone_hi_and_odd": {k: odd[k] for k in odd if k != "ok"},
        "killed_after_clip_iff_odd": {k: ka[k] for k in ka if k != "ok"},
        "killed_rstar_iff_odd": {k: kr[k] for k in kr if k != "ok"},
        "killed_clip_and_live": {k: kc[k] for k in kc if k != "ok"},
        "lemmas": {
            "unclipped_cone_hi_packed_eq_2s": True,
            "unclipped_cone_hi_AND_live_iff_s_odd": True,
            "only_j0_among_W_plus_2j_has_live_cone_hi_AND": True,
            "after_clip_band_hi_AND_iff_s_odd": False,
            "rstar_AND_iff_s_odd": False,
            "clip_cone_hi_AND_live_k_ge_1": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "unclipped_cone_hi_packed_eq_2s": "LEMMA",
            "unclipped_cone_hi_AND_live_iff_s_odd": "LEMMA",
            "only_j0_among_W_plus_2j_has_live_cone_hi_AND": "LEMMA",
            "after_clip_band_hi_AND_iff_s_odd": "KILLED",
            "rstar_AND_iff_s_odd": "KILLED",
            "clip_cone_hi_AND_live_k_ge_1": "KILLED",
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
    print("cone_hi_and_odd", dump["cone_hi_and_odd"])


if __name__ == "__main__":
    main()
