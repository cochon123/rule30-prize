#!/usr/bin/env python3
"""Cycle GA: unclipped hi-1 times are t0 + q*2U + eps with q < W/(4U).

Covering W in {4U,8U,16U} is 0 mod 4U, so Q=W/(4U) is an integer.
Cycle FZ's dyadic offsets in one 2U-period, copied over q=0..Q-1, are
exactly the unclipped times with hi Green 1. The last such time is
clip, at q=Q-1 and eps=U=2^{a-1}. Whole-window hi is 1 iff s>clip or
s is one of those times. Clip hi AND is not always live, W is not 0
mod 8U, and E_a is not all of [0,U]. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all
n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_ga.py --certify
Dump: research/cycle_ga.json
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
FZ_JSON = Path(__file__).resolve().parent / "cycle_fz.json"
FY_JSON = Path(__file__).resolve().parent / "cycle_fy.json"
FX_JSON = Path(__file__).resolve().parent / "cycle_fx.json"


def dyadic_eps(a: int) -> list[int]:
    """Offsets in one 2U-period: {2^j : 0<=j<a} and 0 iff a odd."""
    eps = [1 << j for j in range(a)]
    if a & 1:
        return [0] + eps
    return eps


def w_mod_4U() -> dict:
    """W in {4U,8U,16U} is 0 mod 4U."""
    n_ok = 0
    for k in range(0, 21):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            if W % (4 * U) != 0:
                return {"ok": False, "k": k, "W": W}
            n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def q_param() -> dict:
    """s = t0 + q*2U + eps enumerates unclipped hi-1; clip is last."""
    n_ok = 0
    n_times = 0
    for k in range(0, 12):
        U = 1 << k
        a = k + 1
        eps = dyadic_eps(a)
        if len(eps) != a + (a & 1):
            return {"ok": False, "k": k, "eps": eps}
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            Q = W // (4 * U)
            last = t0 + (Q - 1) * (2 * U) + U
            if last != clip:
                return {"ok": False, "k": k, "W": W, "last": last, "clip": clip}
            got = set()
            for q in range(Q):
                for e in eps:
                    s = t0 + q * (2 * U) + e
                    if s > clip:
                        return {"ok": False, "k": k, "s": s}
                    got.add(s)
            want = {
                s
                for s in range(t0, clip + 1)
                if dyadic_offset(s - t0, a, U)
            }
            if got != want:
                return {"ok": False, "k": k, "W": W, "ngot": len(got), "nwant": len(want)}
            n_ok += 1
            n_times += len(got)
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_times": n_times}


def piecewise_hi() -> dict:
    """Whole-window hi G=1 iff s>clip or dyadic; k<=7."""
    n_ok = 0
    n_one = 0
    for k in range(0, 8):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            for s in range(t0, T):
                m = T - s - 1
                if s <= clip:
                    g = G(m, 2 * U - 2) if U > 1 else G(m, 0)
                    p = dyadic_offset(s - t0, a, U)
                else:
                    g = G(m, 0)
                    p = 1
                if g != p:
                    return {"ok": False, "k": k, "s": s, "g": g, "p": p}
                n_ok += 1
                n_one += p
    return {"ok": n_ok > 0 and n_one > 0, "n_ok": n_ok, "n_one": n_one}


def killed_w_mod_8U() -> dict:
    """W is not 0 mod 8U: W=4U at k=2."""
    k = 2
    U = 1 << k
    W = 4 * U
    ok = W % (8 * U) != 0 and W % (4 * U) == 0
    return {"ok": ok, "k": k, "W": W}


def killed_clip_and_live() -> dict:
    """Clip hi AND is not always live: k=2, W=8U."""
    k = 2
    U = 1 << k
    W, T = 8 * U, 10 * U
    t0 = T - W // 2
    clip = U + W
    row = 1
    for _ in range(clip):
        row = rule30_step(row)
    A = (row << 1) & row
    r_hi = 2 * clip - T
    on = ((A >> (T + r_hi)) & 1) == 1
    ok = r_hi == W and not on
    return {"ok": ok, "k": k, "s": clip, "r_hi": r_hi, "AND": int(on)}


def killed_eps_interval() -> dict:
    """E_a is not all of [0,U]: a=3 misses 3."""
    a = 3
    U = 1 << (a - 1)
    eps = set(dyadic_eps(a))
    interval = set(range(U + 1))
    ok = 3 not in eps and eps < interval
    return {"ok": ok, "a": a, "eps": sorted(eps), "missing": sorted(interval - eps)}


def prefixes() -> dict:
    fz = json.loads(FZ_JSON.read_text())
    fy = json.loads(FY_JSON.read_text())
    fx = json.loads(FX_JSON.read_text())
    ok = (
        fz["checks"]["all_ok"]
        and fy["checks"]["all_ok"]
        and fx["checks"]["all_ok"]
        and fz["verdict"]["unclipped_hi_iff_dyadic_offset"] == "LEMMA"
        and fy["verdict"]["unclipped_hi_ones_count"] == "LEMMA"
        and fx["verdict"]["W_eq_0_mod_2U"] == "LEMMA"
        and fz["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    wmod: dict,
    qp: dict,
    piece: dict,
    kw: dict,
    ka: dict,
    ke: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert wmod["ok"] and qp["ok"] and piece["ok"]
    assert kw["ok"] and ka["ok"] and ke["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    wmod = w_mod_4U()
    qp = q_param()
    piece = piecewise_hi()
    kw = killed_w_mod_8U()
    ka = killed_clip_and_live()
    ke = killed_eps_interval()
    pref = prefixes()
    checks = self_checks(c20, wmod, qp, piece, kw, ka, ke, pref)
    dump = {
        "cycle": "GA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "w_mod_4U": {k: wmod[k] for k in wmod if k != "ok"},
        "q_param": {k: qp[k] for k in qp if k != "ok"},
        "piecewise_hi": {k: piece[k] for k in piece if k != "ok"},
        "killed_w_mod_8U": {k: kw[k] for k in kw if k != "ok"},
        "killed_clip_and_live": {k: ka[k] for k in ka if k != "ok"},
        "killed_eps_interval": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "W_eq_0_mod_4U": True,
            "unclipped_hi_times_q_param": True,
            "clip_is_last_dyadic": True,
            "piecewise_whole_window_hi": True,
            "W_eq_0_mod_8U": False,
            "clip_hi_AND_always_live": False,
            "E_a_eq_interval_0_to_U": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "W_eq_0_mod_4U": "LEMMA",
            "unclipped_hi_times_q_param": "LEMMA",
            "clip_is_last_dyadic": "LEMMA",
            "piecewise_whole_window_hi": "LEMMA",
            "W_eq_0_mod_8U": "KILLED",
            "clip_hi_AND_always_live": "KILLED",
            "E_a_eq_interval_0_to_U": "KILLED",
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
    print("q_param", dump["q_param"])


if __name__ == "__main__":
    main()
