#!/usr/bin/env python3
"""Cycle TC: clip-edge pal-pair packed AND is 0 on both sides.

Clip-edge pal-right is j=5U, packed p=0. Packed AND at p=0 is bits
0 and -1; bit -1 is 0, and the 4-tuple 0001 is not an AND-one.
Clip-edge distance d=5U-n satisfies 2d=t+1 at covering time
t=10U-2n-1, so spat(d) reads packed bits 2t+1 and 2t+2, past the
support 0..2t. Both sides vanish, so clip-edge pal-pair raw is 0
cellwise and does not contribute to pal-pair raw tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tc.py --certify
Dump: research/cycle_tc.json
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
from cycle_hh import AND_ONES, and_from_tuple, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s, packed_p
from cycle_su import covering_and_spat
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_tb import want_edge_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"
SS_JSON = Path(__file__).resolve().parent / "cycle_ss.json"
SU_JSON = Path(__file__).resolve().parent / "cycle_su.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_CELL = 8
T_AND = 256
Q = 10
PAT0011 = (0, 0, 1, 1)
PAT0001 = (0, 0, 0, 1)


def clip_j(n: int, k: int) -> int:
    """Pal-left j of the clip-edge pair: partner is 5U."""
    return 2 * n - 5 * (1 << k)


def clip_d(n: int, k: int) -> int:
    """Clip-edge pal-pair distance d=5U-n."""
    return 5 * (1 << k) - n


def tot_form() -> dict:
    """k<=64: packed p(5U)=0; clip 2d=t+1; t+2d=2t+1 past 2t."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        u = 1 << k
        clip = 5 * u
        if packed_p(clip, k) != 0:
            return {"ok": False, "p0": True, "k": k}
        samples = {0, 1, u, 3 * u, (5 * u) // 2 + 1, 4 * u - 1}
        for n in samples:
            if n < 0 or n >= 4 * u:
                continue
            j = clip_j(n, k)
            t = covering_t(k, n)
            d = clip_d(n, k)
            if 2 * d != t + 1:
                return {"ok": False, "d": True, "k": k, "n": n}
            if t + 2 * d != 2 * t + 1:
                return {"ok": False, "past": True, "k": k, "n": n}
            if packed_p(j, k) != 4 * (clip - n) and 0 <= j:
                return {"ok": False, "pl": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and packed_p(5, 0) == 0
        and clip_d(3, 0) == 2
        and covering_t(0, 3) == 3
        and want_edge_n(0) == 1
        and want_even(0) == 1
        and PAT0001 not in AND_ONES
        and PAT0011 in AND_ONES
        and and_from_tuple(*PAT0001) == 0
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def and_p0() -> dict:
    """t>=1: bits -3..0 are 0001; AND at p=0 is 0."""
    n_ok = 0
    row = 1
    for t in range(0, T_AND):
        if t >= 1:
            four = tuple(bit_at(row, i) for i in range(-3, 1))
            if four != PAT0001 or and_from_tuple(*four) != 0:
                return {"ok": False, "t": t, "four": four}
            if (bit_at(row, 0) & bit_at(row, -1)) != 0:
                return {"ok": False, "hh": True, "t": t}
            if t >= 1 and bit_at(row, 2 * t) != 1:
                return {"ok": False, "edge": True, "t": t}
            if bit_at(row, 2 * t + 1) != 0:
                return {"ok": False, "past": True, "t": t}
        n_ok += 1
        row = rule30_step(row)
    ok = n_ok == T_AND and PAT0001 not in AND_ONES
    return {"ok": ok, "n_ok": n_ok, "t_hi": T_AND - 1}


def edge_and() -> dict:
    """k<=8 clip-edge pal-pairs: both spat sides 0, raw 0, count J_{k+2}."""
    t_hi = Q * (1 << K_CELL)
    packed = []
    row = 1
    for _t in range(0, t_hi):
        packed.append(row)
        row = rule30_step(row)
    n_ok = 0
    n_cell = 0
    rows = {}
    for k in range(0, K_CELL + 1):
        u = 1 << k
        clip = 5 * u
        n_edge = n_fire = 0
        for n in range(0, 4 * u):
            j = clip_j(n, k)
            if j < 0 or j >= n or G(n, j) == 0:
                continue
            t = covering_t(k, n)
            s = even_s(n, k)
            d = clip_d(n, k)
            left = covering_and_spat(packed[t], s, d)
            right = covering_and_spat(packed[t], s, -d)
            if left != 0 or right != 0:
                return {
                    "ok": False,
                    "and": True,
                    "k": k,
                    "n": n,
                    "left": left,
                    "right": right,
                }
            if t + 2 * d != 2 * t + 1:
                return {"ok": False, "past": True, "k": k, "n": n}
            n_edge += 1
            n_fire += left ^ right
        if n_edge != want_edge_n(k) or n_fire != 0:
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_edge": n_edge,
                "want": want_edge_n(k),
                "n_fire": n_fire,
            }
        n_cell += n_edge
        n_ok += 1
        rows[str(k)] = {"n_edge": n_edge, "n_fire": n_fire}
    ok = (
        n_ok == K_CELL + 1
        and n_cell == sum(want_edge_n(k) for k in range(0, K_CELL + 1))
        and rows["0"]["n_edge"] == 1
        and rows["7"]["n_edge"] == 171
        and rows["8"]["n_edge"] == 341
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_cell": n_cell,
        "k_hi": K_CELL,
        "rows": rows,
    }


def killed_eq() -> dict:
    """clip-edge raw tot 1; pal_c_e period 8; odd pairs 2-fold all parent."""
    ok = (
        want_edge_n(0) == 1
        and packed_p(5, 0) == 0
        and PAT0001 not in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    tb = json.loads(TB_JSON.read_text())
    ss = json.loads(SS_JSON.read_text())
    su = json.loads(SU_JSON.read_text())
    ok = (
        tb["checks"]["all_ok"]
        and ss["checks"]["all_ok"]
        and su["checks"]["all_ok"]
        and tb["verdict"]["clip_edge_eq_jacobsthal"] == "LEMMA"
        and tb["verdict"]["oddj_pairs_drop_clip_edge"] == "LEMMA"
        and ss["verdict"]["packed_support_0_to_2s"] == "LEMMA"
        and ss["verdict"]["unpaired_packed_and_0_all_k"] == "LEMMA"
        and su["verdict"]["covering_and_eq_spat_2d"] == "LEMMA"
        and su["verdict"]["pair_raw_eq_spat_d_xor_minus_d"] == "LEMMA"
        and tb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tb["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, p0, edge, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and p0["ok"] and edge["ok"] and kl["ok"]
    assert sc["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    ev = even_slots(M_SLOTS)
    tot = tot_form()
    p0 = and_p0()
    edge = edge_and()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, p0, edge, kl, sc, pref)
    dump = {
        "cycle": "TC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "and_p0": {k: p0[k] for k in p0 if k != "ok"},
        "edge_and": {k: edge[k] for k in edge if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "clip_right_p_eq_0": True,
            "p0_and_eq_0": True,
            "clip_pair_and_0_both_sides": True,
            "clip_edge_raw_tot_1": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "clip_right_p_eq_0": "LEMMA",
            "p0_and_eq_0": "LEMMA",
            "clip_pair_and_0_both_sides": "LEMMA",
            "clip_edge_raw_tot_0": "LEMMA",
            "clip_edge_raw_tot_1": "KILLED",
            "odd_pairs_2fold_all_parent": "KILLED",
            "pal_c_e_period8": "KILLED",
            "pal_c_eq_ST": "KILLED",
            "E_q10_10": "CERTIFIED",
            "packed_R_eq_ST": "PREFIX",
            "even_rest_eq_parent_odd_all_k": "PREFIX",
            "E_all_k": "PREFIX",
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
    print(
        "edge k8",
        dump["edge_and"]["rows"]["8"]["n_edge"],
        "n_cell",
        dump["edge_and"]["n_cell"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
