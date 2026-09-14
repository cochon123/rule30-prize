#!/usr/bin/env python3
"""Cycle TH: d=1 origin is odd children; n=1 mod 4 times are an 8-AP.

At k>=1, d=1 pal-pairs on n=1 mod 4 are the odd children of every
even covering n at k-1 (count 2^k). d=1 pal-pairs on n=3 mod 4 are
the odd children of odd d=2 pal-pairs at k-1 (count J_k). Covering
times of n=1 mod 4 are the arithmetic progression 2U+5, 2U+13, ...,
10U-3 (difference 8). Pal-center AND on that AP is not identically
0. Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_th.py --certify
Dump: research/cycle_th.json
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
from cycle_hh import AND_ONES
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s
from cycle_st import pal_center_and
from cycle_su import covering_and_spat
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_sz import odd_child_t
from cycle_ta import pal_kind
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tf import want_d1_r1_n, want_d1_r3_n, want_d2_r3_n
from cycle_tg import d1_children
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TG_JSON = Path(__file__).resolve().parent / "cycle_tg.json"
TF_JSON = Path(__file__).resolve().parent / "cycle_tf.json"
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
K_CELL = 8
Q = 10
PAT0011 = (0, 0, 1, 1)


def n1_times(k: int) -> list[int]:
    """Covering times of n=1 mod 4: AP 2U+5 .. 10U-3 step 8."""
    u = 1 << k
    return list(range(2 * u + 5, 10 * u - 3 + 1, 8))


def tot_form() -> dict:
    """k<=64: AP endpoints; odd child of even n is n=1 mod 4 d=1."""
    n_ok = 0
    if n1_times(0) != [7] or covering_t(0, 1) != 7:
        return {"ok": False, "k0": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ap = n1_times(k)
        if len(ap) != u or ap[0] != 2 * u + 5 or ap[-1] != 10 * u - 3:
            return {"ok": False, "ap": True, "k": k}
        if k >= 1 and (ap[1] - ap[0] != 8):
            return {"ok": False, "step": True, "k": k}
        if want_d1_r1_n(k) != 1 << k:
            return {"ok": False, "r1": True, "k": k}
        if k >= 1 and want_d1_r3_n(k) != want_d2_r3_n(k - 1):
            return {"ok": False, "r3": True, "k": k}
        samples = {0, 2, u, 3 * u, 4 * u - 4, 4 * u - 2}
        if k >= 1:
            up = 1 << (k - 1)
            for m in samples:
                if m < 0 or m >= 4 * up or m % 2:
                    continue
                n = 2 * m + 1
                if n % 4 != 1:
                    return {"ok": False, "mod": True, "k": k, "m": m}
                if G(n, n - 1) != 1 or pal_kind(n, n - 1, k) != "pair":
                    return {"ok": False, "d1": True, "k": k, "m": m}
                if odd_child_t(m, k) != covering_t(k, n):
                    return {"ok": False, "t": True, "k": k, "m": m}
                if covering_t(k, n) != 10 * u - 2 * n - 1:
                    return {"ok": False, "t2": True, "k": k, "n": n}
            d2_samples = {3, 4 * up - 1}
            for m in d2_samples:
                if m < 2 or m >= 4 * up or m % 2 == 0:
                    continue
                if G(m, m - 2) != 1:
                    continue
                n = 2 * m + 1
                if n % 4 != 3:
                    return {"ok": False, "mod3": True, "k": k, "m": m}
                if G(n, n - 1) != 1 or pal_kind(n, n - 1, k) != "pair":
                    return {"ok": False, "d13": True, "k": k, "m": m}
                if odd_child_t(m, k) != covering_t(k, n):
                    return {"ok": False, "t3": True, "k": k, "m": m}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d1_r1_n(7) == 128
        and want_d1_r3_n(7) == 43
        and d1_children(1) == (2, 3)
        and G(1, 0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def origin_count() -> dict:
    """k<=12: d=1 r1 = odd children of even covering; r3 = odd children of odd d=2."""
    n_ok = 0
    rows = {}
    for k in range(1, K_COUNT + 1):
        u = 1 << k
        up = 1 << (k - 1)
        child = []
        from_even = []
        from_d2 = []
        for n in range(1, 4 * u):
            if G(n, n - 1) == 1 and pal_kind(n, n - 1, k) == "pair":
                child.append(n)
        for m in range(0, 4 * up, 2):
            n = 2 * m + 1
            if pal_kind(n, n - 1, k) != "pair" or G(n, n - 1) != 1:
                return {"ok": False, "even": True, "k": k, "m": m}
            if odd_child_t(m, k) != covering_t(k, n):
                return {"ok": False, "te": True, "k": k, "m": m}
            from_even.append(n)
        for m in range(1, 4 * up, 2):
            if m < 2 or G(m, m - 2) == 0:
                continue
            if pal_kind(m, m - 2, k - 1) != "pair":
                return {"ok": False, "pkind": True, "k": k, "m": m}
            n = 2 * m + 1
            if G(n, n - 1) != 1 or pal_kind(n, n - 1, k) != "pair":
                return {"ok": False, "d2": True, "k": k, "m": m}
            from_d2.append(n)
        if sorted(child) != sorted(from_even + from_d2):
            return {"ok": False, "set": True, "k": k}
        if len(from_even) != want_d1_r1_n(k) or len(from_d2) != want_d1_r3_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_even": len(from_even),
                "n_d2": len(from_d2),
            }
        n_ok += 1
        rows[str(k)] = {
            "n_d1": len(child),
            "n_r1": len(from_even),
            "n_r3": len(from_d2),
        }
    ok = (
        n_ok == K_COUNT
        and rows["1"]["n_d1"] == 3
        and rows["7"]["n_r1"] == 128
        and rows["7"]["n_r3"] == 43
        and rows["12"]["n_d1"] == 5461
        and rows["12"]["n_r3"] == 1365
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def ap_times() -> dict:
    """k<=12: covering times of n=1 mod 4 equal n1_times AP."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        got = sorted(covering_t(k, n) for n in range(1, 4 * u, 4))
        want = n1_times(k)
        if got != want:
            return {"ok": False, "ap": True, "k": k, "got": got[:4], "want": want[:4]}
        n_ok += 1
        rows[str(k)] = {"n": len(got), "lo": got[0], "hi": got[-1]}
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["lo"] == 7
        and rows["2"]["lo"] == 13
        and rows["7"]["n"] == 128
        and rows["12"]["n"] == 4096
        and rows["12"]["lo"] == 2 * 4096 + 5
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def pal_r1() -> dict:
    """k<=8 pal-center tot on n=1 mod 4: not identically 0."""
    t_hi = Q * (1 << K_CELL)
    packed = []
    row = 1
    for _t in range(0, t_hi):
        packed.append(row)
        row = rule30_step(row)
    n_ok = 0
    rows = {}
    for k in range(0, K_CELL + 1):
        u = 1 << k
        tot = spat = 0
        n_cell = 0
        for n in range(1, 4 * u, 4):
            t = covering_t(k, n)
            s = even_s(n, k)
            tot ^= pal_center_and(packed[t], s)
            spat ^= covering_and_spat(packed[t], s, 1) ^ covering_and_spat(
                packed[t], s, -1
            )
            n_cell += 1
        if n_cell != want_d1_r1_n(k):
            return {"ok": False, "count": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"tot": tot, "spat": spat, "n": n_cell}
    fired = any(rows[str(k)]["tot"] for k in range(0, K_CELL + 1))
    spat_fired = any(rows[str(k)]["spat"] for k in range(0, K_CELL + 1))
    ok = (
        n_ok == K_CELL + 1
        and fired
        and spat_fired
        and rows["2"]["tot"] == 1
        and rows["7"]["tot"] == 1
        and rows["0"]["tot"] == 0
        and rows["1"]["spat"] == 1
        and rows["0"]["spat"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "k_hi": K_CELL,
        "rows": rows,
        "ident0": False,
    }


def killed_eq() -> dict:
    """pal-center on n=1 mod 4 identically 0; d=1 spat on r1 identically 0."""
    ok = (
        n1_times(0) == [7]
        and want_d1_r1_n(1) == 2
        and want_d1_n(1) == 3
        and want_d2_n(0) == 2
        and G(5, 4) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tg = json.loads(TG_JSON.read_text())
    tf = json.loads(TF_JSON.read_text())
    te = json.loads(TE_JSON.read_text())
    ok = (
        tg["checks"]["all_ok"]
        and tf["checks"]["all_ok"]
        and te["checks"]["all_ok"]
        and tg["verdict"]["d2_eq_both_children_of_d1"] == "LEMMA"
        and tf["verdict"]["d1_all_n1_mod4"] == "LEMMA"
        and te["verdict"]["odd_n_d1_xor_d2"] == "LEMMA"
        and tg["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tg["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, orig, ap, pr1, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and orig["ok"] and ap["ok"] and pr1["ok"] and kl["ok"]
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
    orig = origin_count()
    ap = ap_times()
    pr1 = pal_r1()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, orig, ap, pr1, kl, sc, pref)
    dump = {
        "cycle": "TH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "origin_count": {k: orig[k] for k in orig if k != "ok"},
        "ap_times": {k: ap[k] for k in ap if k != "ok"},
        "pal_r1": {k: pr1[k] for k in pr1 if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d1_r1_odd_children_even_covering": True,
            "d1_r3_odd_children_odd_d2": True,
            "n1_times_eq_8_ap": True,
            "pal_r1_identically_0": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d1_r1_odd_children_even_covering": "LEMMA",
            "d1_r3_odd_children_odd_d2": "LEMMA",
            "n1_times_eq_8_ap": "LEMMA",
            "pal_r1_identically_0": "KILLED",
            "d1_spat_r1_identically_0": "KILLED",
            "d2_spat_eq_parent_d1_spat": "KILLED",
            "d1_all_odd_n": "KILLED",
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
        "d1 k12",
        dump["origin_count"]["rows"]["12"]["n_d1"],
        "ap lo",
        dump["ap_times"]["rows"]["12"]["lo"],
        "pal_r1 k7",
        dump["pal_r1"]["rows"]["7"]["tot"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
