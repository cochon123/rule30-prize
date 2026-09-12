#!/usr/bin/env python3
"""Cycle GG: unclipped cone-hi contributes iff s=t0+1+q*2U; XOR is 1 iff W=4U.

Unclipped cone-hi G*AND is 1 iff s is odd and dyadic (Cycles FZ+GF). t0 is
even, so that is delta=1 (mod 2U): s=t0+1+q*2U for 0<=q<Q=W/(4U). Those
Q times XOR to Q mod 2, which is 1 iff W=4U. The XOR is not always 1 or
always 0, and not every W+2^j contributes. Do not claim J6=J10=0 implies
J18=1 for all k; do not push even-spine past k=18; do not bump all n0=16
past 414990. Not a prize claim.

Run: python3 research/cycle_gg.py --certify
Dump: research/cycle_gg.json
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
GF_JSON = Path(__file__).resolve().parent / "cycle_gf.json"
GE_JSON = Path(__file__).resolve().parent / "cycle_ge.json"
GD_JSON = Path(__file__).resolve().parent / "cycle_gd.json"


def contrib_times() -> dict:
    """s=t0+1+q*2U lies in the unclipped window; last is W+1."""
    n_ok = 0
    for k in range(0, 12):
        U = 1 << k
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            Q = W // (4 * U)
            if t0 % 2:
                return {"ok": False, "k": k, "t0": t0}
            times = []
            for q in range(Q):
                s = t0 + 1 + q * (2 * U)
                if not (t0 <= s <= clip):
                    return {"ok": False, "k": k, "s": s}
                if (s - t0) % (2 * U) != 1:
                    return {"ok": False, "k": k, "s": s}
                if dyadic_offset(s - t0, k + 1, U) != 1:
                    return {"ok": False, "k": k, "s": s}
                times.append(s)
            if times[-1] != W + 1:
                return {"ok": False, "k": k, "last": times[-1]}
            n_ok += 1
    return {"ok": n_ok > 0, "n_ok": n_ok}


def packed_contrib() -> dict:
    """G*AND=1 exactly on those times; XOR is Q mod 2. k<=6."""
    n_ok = 0
    n_one = 0
    for k in range(0, 7):
        U = 1 << k
        a = k + 1
        for W in (4 * U, 8 * U, 16 * U):
            T = 2 * U + W
            t0 = T - W // 2
            clip = U + W
            Q = W // (4 * U)
            want = {t0 + 1 + q * (2 * U) for q in range(Q)}
            row = 1
            for _ in range(t0):
                row = rule30_step(row)
            got = set()
            xor = 0
            for s in range(t0, clip + 1):
                A = (row << 1) & row
                chi = 2 * s - T
                on = ((A >> (T + chi)) & 1) == 1
                g = G(T - s - 1, 2 * U - 2) if U > 1 else G(T - s - 1, 0)
                if on and g:
                    got.add(s)
                    xor ^= 1
                n_ok += 1
                row = rule30_step(row)
            if got != want or xor != (Q & 1):
                return {
                    "ok": False,
                    "k": k,
                    "W": W,
                    "ngot": len(got),
                    "xor": xor,
                    "Q": Q,
                }
            n_one += len(got)
    return {"ok": n_ok > 0, "n_ok": n_ok, "n_one": n_one}


def killed_xor_always_1() -> dict:
    """Unclipped cone-hi XOR is 0 for W=8U."""
    k = 2
    U = 1 << k
    W = 8 * U
    Q = W // (4 * U)
    ok = (Q & 1) == 0
    return {"ok": ok, "k": k, "Q": Q}


def killed_xor_always_0() -> dict:
    """Unclipped cone-hi XOR is 1 for W=4U."""
    k = 2
    U = 1 << k
    W = 4 * U
    Q = W // (4 * U)
    ok = (Q & 1) == 1
    return {"ok": ok, "k": k, "Q": Q}


def killed_all_w_plus_2j() -> dict:
    """s=W+2 (j=1) does not contribute: even, AND dead."""
    k = 2
    U = 1 << k
    W = 8 * U
    s = W + 2
    ok = (s & 1) == 0
    return {"ok": ok, "k": k, "s": s}


def prefixes() -> dict:
    gf = json.loads(GF_JSON.read_text())
    ge = json.loads(GE_JSON.read_text())
    gd = json.loads(GD_JSON.read_text())
    ok = (
        gf["checks"]["all_ok"]
        and ge["checks"]["all_ok"]
        and gd["checks"]["all_ok"]
        and gf["verdict"]["unclipped_cone_hi_AND_live_iff_s_odd"] == "LEMMA"
        and gf["verdict"]["only_j0_among_W_plus_2j_has_live_cone_hi_AND"] == "LEMMA"
        and gd["verdict"]["incone_hi_eq_1_iff_s_eq_W_plus_2j"] == "LEMMA"
        and gf["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20,
    times: dict,
    packed: dict,
    k1: dict,
    k0: dict,
    kj: dict,
    pref: dict,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert times["ok"] and packed["ok"]
    assert k1["ok"] and k0["ok"] and kj["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    times = contrib_times()
    packed = packed_contrib()
    k1 = killed_xor_always_1()
    k0 = killed_xor_always_0()
    kj = killed_all_w_plus_2j()
    pref = prefixes()
    checks = self_checks(c20, times, packed, k1, k0, kj, pref)
    dump = {
        "cycle": "GG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "contrib_times": {k: times[k] for k in times if k != "ok"},
        "packed_contrib": {k: packed[k] for k in packed if k != "ok"},
        "killed_xor_always_1": {k: k1[k] for k in k1 if k != "ok"},
        "killed_xor_always_0": {k: k0[k] for k in k0 if k != "ok"},
        "killed_all_w_plus_2j": {k: kj[k] for k in kj if k != "ok"},
        "lemmas": {
            "unclipped_cone_hi_contrib_t0_plus_1_plus_q_2U": True,
            "unclipped_cone_hi_XOR_eq_1_iff_W_eq_4U": True,
            "unclipped_cone_hi_XOR_always_1": False,
            "unclipped_cone_hi_XOR_always_0": False,
            "all_W_plus_2j_contribute": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "unclipped_cone_hi_contrib_t0_plus_1_plus_q_2U": "LEMMA",
            "unclipped_cone_hi_XOR_eq_1_iff_W_eq_4U": "LEMMA",
            "unclipped_cone_hi_XOR_always_1": "KILLED",
            "unclipped_cone_hi_XOR_always_0": "KILLED",
            "all_W_plus_2j_contribute": "KILLED",
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
    print("packed_contrib", dump["packed_contrib"])


if __name__ == "__main__":
    main()
