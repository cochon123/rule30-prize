#!/usr/bin/env python3
"""Cycle SX: odd pal-right p=14 AND at dyadic covering times.

Covering times of Cycle SW's odd pal-right p=14 n are 2U+5, 4U+1,
4U+5 if k odd, and 4U+5+2^{i+1} for i=1..k-1. Packed AND at p=14
is bits 13 and 14. Those bits are 1 at t=2^m+1 (m>=4), t=2^m+5
(m>=3), and t=2^a+2^b+5 (a>b>=2) through the certified walk, so
listed cells all fire and odd pal-right p=14 tot is 1. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_sx.py --certify
Dump: research/cycle_sx.json
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
from cycle_lf import want_p14_n
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s
from cycle_sv import forced_right_j, pal_left_never_forced
from cycle_sw import odd_p14_ns, want_odd_p6_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SW_JSON = Path(__file__).resolve().parent / "cycle_sw.json"
SV_JSON = Path(__file__).resolve().parent / "cycle_sv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_GREEN = 12
M_PLUS1 = 16
M_PLUS5 = 16
A_HI = 14
T_WALK = (1 << M_PLUS1) + 5
TUPLE_0011 = (0, 0, 1, 1)
Q = 10


def covering_t(k: int, n: int) -> int:
    """Odd covering time t=s+1=10U-2n-1."""
    return Q * (1 << k) - 2 * n - 1


def odd_p14_times(k: int) -> list[int]:
    """Covering times of Cycle SW's odd pal-right p=14 n, k>=3."""
    u = 1 << k
    times = [2 * u + 5, 4 * u + 1]
    if k % 2 == 1:
        times.append(4 * u + 5)
    for i in range(1, k):
        times.append(4 * u + 5 + (1 << (i + 1)))
    return times


def and_p14(row: int) -> int:
    """Packed AND at p=14: odd-row bits 13 and 14."""
    return bit_at(row, 13) & bit_at(row, 14)


def tot_form() -> dict:
    """k<=64: covering times match the dyadic family; listed count odd."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        if k >= 3:
            u = 1 << k
            ns = odd_p14_ns(k)
            ts = odd_p14_times(k)
            if sorted(covering_t(k, n) for n in ns) != sorted(ts):
                return {"ok": False, "times": True, "k": k}
            if len(ts) != want_p14_n(k, 10) or len(ts) % 2 != 1:
                return {"ok": False, "cnt": True, "k": k, "n": len(ts)}
            if 2 * u + 5 not in ts or 4 * u + 1 not in ts:
                return {"ok": False, "core": True, "k": k}
            if (k % 2 == 1) != (4 * u + 5 in ts):
                return {"ok": False, "odd5": True, "k": k}
            for n in ns:
                t = covering_t(k, n)
                if even_s(n, k) + 1 != t:
                    return {"ok": False, "s": True, "k": k, "n": n}
                if t % 2 == 0 or t < 2 * u + 5:
                    return {"ok": False, "odd_t": True, "k": k, "t": t}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and covering_t(3, 4 * 8 - 3) == 2 * 8 + 5
        and covering_t(3, 3 * 8 - 1) == 4 * 8 + 1
        and sorted(odd_p14_times(3)) == [21, 33, 37, 41, 45]
        and max(odd_p14_times(K_GREEN)) <= T_WALK
        and pal_left_never_forced(3)
        and want_odd_p6_n(2) == 3
        and want_even(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def dyadic_and() -> dict:
    """One packed walk: bits 13 and 14 fire on the dyadic family."""
    need_p1 = {(1 << m) + 1 for m in range(4, M_PLUS1 + 1)}
    need_p5 = {(1 << m) + 5 for m in range(3, M_PLUS5 + 1)}
    need_ab: set[int] = set()
    for a in range(3, A_HI + 1):
        for b in range(2, a):
            need_ab.add((1 << a) + (1 << b) + 5)
    need_p7 = {(1 << m) + 7 for m in range(4, M_PLUS1 + 1)}
    fam: dict[int, int] = {}
    for k in range(3, K_GREEN + 1):
        for t in odd_p14_times(k):
            fam[t] = fam.get(t, 0) + 1
    row = 1
    prev = None
    n_p1 = n_p5 = n_ab = n_p7 = 0
    n_fam = n_0011 = n_clause = 0
    for t in range(0, T_WALK + 1):
        if t % 2 == 1:
            fired = and_p14(row)
            if t in need_p1:
                if fired != 1:
                    return {"ok": False, "p1": True, "t": t}
                n_p1 += 1
            if t in need_p5:
                if fired != 1:
                    return {"ok": False, "p5": True, "t": t}
                n_p5 += 1
            if t in need_ab:
                if fired != 1:
                    return {"ok": False, "ab": True, "t": t}
                n_ab += 1
            if t in need_p7:
                if fired != 0:
                    return {"ok": False, "p7": True, "t": t}
                n_p7 += 1
            if t in fam:
                if fired != 1:
                    return {"ok": False, "fam": True, "t": t}
                n_fam += fam[t]
                tup = tuple(bit_at(prev, 11 + i) for i in range(4))
                packed = and_clause(*tup)
                if packed != 1 or packed != and_from_tuple(*tup):
                    return {"ok": False, "clause": True, "t": t, "tup": tup}
                n_clause += fam[t]
                if tup == TUPLE_0011:
                    n_0011 += fam[t]
        else:
            prev = row
        row = rule30_step(row)
    want_fam = sum(want_p14_n(k, 10) for k in range(3, K_GREEN + 1))
    ok = (
        n_p1 == len(need_p1)
        and n_p5 == len(need_p5)
        and n_ab == len(need_ab)
        and n_p7 == len(need_p7)
        and n_fam == want_fam
        and n_clause == want_fam
        and n_0011 == want_fam
        and (0, 0, 0, 0) not in AND_ONES
        and TUPLE_0011 in AND_ONES
    )
    return {
        "ok": ok,
        "n_p1": n_p1,
        "n_p5": n_p5,
        "n_ab": n_ab,
        "n_p7": n_p7,
        "n_fam": n_fam,
        "n_0011": n_0011,
        "t_hi": T_WALK,
        "m_p1": M_PLUS1,
        "m_p5": M_PLUS5,
        "a_hi": A_HI,
        "k_hi": K_GREEN,
    }


def killed_eq() -> dict:
    """p=14 AND on all odd t; bits 13,14 freeze; plus7 fires."""
    row = 1
    for _ in range(9):
        row = rule30_step(row)
    t9 = and_p14(row)
    row = 1
    for _ in range(3):
        row = rule30_step(row)
    t3_13 = bit_at(row, 13)
    t3_14 = bit_at(row, 14)
    ok = (
        t9 == 0
        and not (t3_13 == 1 and t3_14 == 1)
        and (t3_13 != 3 % 2 or t3_14 != 3 % 2)
        and want_rest_e0(1) == 0
        and forced_right_j(14, 3) == 5 * 8 - 7
        and pal_left_never_forced(3)
    )
    return {"ok": ok}


def prefixes() -> dict:
    sw = json.loads(SW_JSON.read_text())
    sv = json.loads(SV_JSON.read_text())
    ok = (
        sw["checks"]["all_ok"]
        and sv["checks"]["all_ok"]
        and sw["verdict"]["p6_and_1_on_odd_t_ge_3"] == "LEMMA"
        and sw["verdict"]["odd_p14_green_set_exact"] == "CERTIFIED"
        and sw["verdict"]["odd_corr_0_k_ge_3"] == "CERTIFIED"
        and sw["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sw["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and G(4 * 8 - 3, 5 * 8 - 7) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, dy, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and dy["ok"] and kl["ok"] and sc["ok"] and pref["ok"]
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
    dy = dyadic_and()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, dy, kl, sc, pref)
    dump = {
        "cycle": "SX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "dyadic_and": {k: dy[k] for k in dy if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_p14_covering_times": True,
            "p14_and_eq_bits_13_14": True,
            "listed_p14_and_1_if_dyadic": True,
            "dyadic_13_and_14_all_m": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_p14_covering_times": "LEMMA",
            "p14_and_eq_bits_13_14": "LEMMA",
            "dyadic_13_and_14": "CERTIFIED",
            "listed_p14_and_1": "CERTIFIED",
            "listed_p14_0011": "CERTIFIED",
            "odd_p14_and_tot_1_k_ge_3": "CERTIFIED",
            "odd_corr_0_k_ge_3": "CERTIFIED",
            "p14_and_all_odd_t": "KILLED",
            "bits_13_14_freeze": "KILLED",
            "p14_and_plus7": "KILLED",
            "pal_c_eq_ST": "KILLED",
            "E_q10_10": "CERTIFIED",
            "dyadic_13_and_14_all_m": "PREFIX",
            "odd_p14_green_set_all_k": "PREFIX",
            "odd_p14_and_tot_1_all_k": "PREFIX",
            "odd_corr_0_all_k": "PREFIX",
            "odd_pair_rest_eq_raw_all_k": "PREFIX",
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
        "dyadic n_p1",
        dump["dyadic_and"]["n_p1"],
        "n_p5",
        dump["dyadic_and"]["n_p5"],
        "n_ab",
        dump["dyadic_and"]["n_ab"],
        "n_fam",
        dump["dyadic_and"]["n_fam"],
        "n_0011",
        dump["dyadic_and"]["n_0011"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
