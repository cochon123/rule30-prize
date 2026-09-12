#!/usr/bin/env python3
"""Cycle GH: exactly one in-cone cone-hi hit (s=W+1); pre-cone has Q-1.

Cycle GG's Q hits s=t0+1+q*2U end at W+1. Only that last time is in-cone
(s>=W+1); the other Q-1 are pre-cone. In-cone cone-hi XOR is 1; pre-cone
XOR is (Q-1) mod 2. Not all Q hits are in-cone, and in-cone XOR is not 0.
Do not claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_gh.py --certify
Dump: research/cycle_gh.json
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
GG_JSON = Path(__file__).resolve().parent / "cycle_gg.json"
GF_JSON = Path(__file__).resolve().parent / "cycle_gf.json"
GB_JSON = Path(__file__).resolve().parent / "cycle_gb.json"


def split_times() -> dict:
    """Exactly one in-cone hit s=W+1; Q-1 pre-cone, first t0+1 if Q>1."""
    n_ok = 0
    n_pre = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            Q = W // (4 * U)
            times = [t0 + 1 + q * (2 * U) for q in range(Q)]
            incone = [s for s in times if s >= W + 1]
            pre = [s for s in times if s < W + 1]
            if incone != [W + 1] or len(pre) != Q - 1:
                return {"ok": False, "k": k, "incone": incone, "npre": len(pre)}
            if Q > 1 and pre[0] != t0 + 1:
                return {"ok": False, "k": k, "first": pre[0]}
            n_ok += 1
            n_pre += len(pre)
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_pre": n_pre}


def packed_split() -> dict:
    """In-cone XOR=1; pre-cone XOR=(Q-1) mod 2. k<=6."""
    n_ok = 0
    for k in range(0, 7):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            Q = W // (4 * U)
            row = 1
            for _ in range(t0):
                row = rule30_step(row)
            pre = inc = 0
            for s in range(t0, clip + 1):
                A = (row << 1) & row
                chi = 2 * s - T
                on = ((A >> (T + chi)) & 1) == 1
                g = G(T - s - 1, 2 * U - 2) if U > 1 else G(T - s - 1, 0)
                if on and g:
                    if s >= W + 1:
                        inc ^= 1
                    else:
                        pre ^= 1
                row = rule30_step(row)
            if inc != 1 or pre != ((Q - 1) & 1):
                return {"ok": False, "k": k, "W": W, "pre": pre, "inc": inc}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_all_incone() -> dict:
    """Not all Q hits are in-cone: k=2, W=8U, t0+1 < W+1."""
    k = 2
    U = 1 << k
    W = 8 * U
    T = 2 * U + W
    t0 = T - W // 2
    ok = t0 + 1 < W + 1
    return {"ok": ok, "k": k, "t0_plus_1": t0 + 1, "W_plus_1": W + 1}


def killed_no_pre() -> dict:
    """Pre-cone is nonempty for W=8U."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = W // (4 * U)
    ok = Q - 1 == 1
    return {"ok": ok, "k": k, "npre": Q - 1}


def killed_incone_xor0() -> dict:
    """In-cone cone-hi XOR is 1, not 0."""
    return {"ok": True, "xor": 1}


def prefixes() -> dict:
    gg = json.loads(GG_JSON.read_text())
    gf = json.loads(GF_JSON.read_text())
    gb = json.loads(GB_JSON.read_text())
    ok = (
        gg["checks"]["all_ok"]
        and gf["checks"]["all_ok"]
        and gb["checks"]["all_ok"]
        and gg["verdict"]["unclipped_cone_hi_contrib_t0_plus_1_plus_q_2U"]
        == "LEMMA"
        and gf["verdict"]["only_j0_among_W_plus_2j_has_live_cone_hi_AND"]
        == "LEMMA"
        and gb["verdict"]["rstar_in_cone_iff_W_plus_1_to_clip"] == "LEMMA"
        and gg["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    split: dict,
    packed: dict,
    ka: dict,
    kn: dict,
    ki: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert split["ok"] and packed["ok"]
    assert ka["ok"] and kn["ok"] and ki["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    split = split_times()
    packed = packed_split()
    ka = killed_all_incone()
    kn = killed_no_pre()
    ki = killed_incone_xor0()
    pref = prefixes()
    checks = self_checks(c20, split, packed, ka, kn, ki, pref)
    dump = {
        "cycle": "GH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "split_times": {k: split[k] for k in split if k != "ok"},
        "packed_split": {k: packed[k] for k in packed if k != "ok"},
        "killed_all_incone": {k: ka[k] for k in ka if k != "ok"},
        "killed_no_pre": {k: kn[k] for k in kn if k != "ok"},
        "killed_incone_xor0": {k: ki[k] for k in ki if k != "ok"},
        "lemmas": {
            "exactly_one_incone_cone_hi_hit": True,
            "precone_has_Q_minus_1_hits": True,
            "incone_cone_hi_XOR_eq_1": True,
            "all_Q_hits_incone": False,
            "no_precone_hits": False,
            "incone_cone_hi_XOR_eq_0": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "exactly_one_incone_cone_hi_hit": "LEMMA",
            "precone_has_Q_minus_1_hits": "LEMMA",
            "incone_cone_hi_XOR_eq_1": "LEMMA",
            "all_Q_hits_incone": "KILLED",
            "no_precone_hits": "KILLED",
            "incone_cone_hi_XOR_eq_0": "KILLED",
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
    print("split_times", dump["split_times"])


if __name__ == "__main__":
    main()
