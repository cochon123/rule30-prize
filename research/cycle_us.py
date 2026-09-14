#!/usr/bin/env python3
"""Cycle US: odd-j leftover halves match even leftover for k>=2.

Odd-j leftover and even leftover both 2-fold parent leftover union
d=2 (Cycles TU/TV). Restricting the parent to n<5 U_p/2 versus
n>=5 U_p/2, even doubling lands on n<5U/2 versus n>=5U/2, while
odd-j doubling lands on n<5U/2 versus n>5U/2 (parent-half is even,
so odd n never equals it). Hence odd-j leftover on n<5U/2 equals
even leftover on n<5U/2, and odd-j leftover on n>5U/2 equals even
leftover on n>=5U/2, for k>=2. Dies at k=1 (parent-half odd). Do
not PREFIX leftover-parent xor large difference or pal-center tot.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_us.py --certify
Dump: research/cycle_us.json
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
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import is_clip_edge, unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_up import lucas, want_lo_e
from cycle_ur import even_lo_ph_split, parent_half, want_ph_lo
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UR_JSON = Path(__file__).resolve().parent / "cycle_ur.json"
UQ_JSON = Path(__file__).resolve().parent / "cycle_uq.json"
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def odd_j_ph_split(k: int) -> dict:
    """Odd-j leftover pal-pairs split by n<ph, n==ph, n>ph."""
    u = 1 << k
    clip = 5 * u
    ph = parent_half(k)
    sm = eq = lg = 0
    for n in range(0, 4 * u):
        hi = min(2 * n, clip)
        for j in range(1, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            if n < ph:
                sm += 1
            elif n == ph:
                eq += 1
            else:
                lg += 1
    return {"sm": sm, "eq": eq, "lg": lg, "ph": ph}


def parent_lo_d2_ph_split(k: int) -> dict:
    """Leftover union d=2 pal-pairs split by n<ph versus n>=ph."""
    u = 1 << k
    clip = 5 * u
    ph = parent_half(k)
    sm = ge = 0
    for n in range(0, 4 * u):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d == 1 or is_clip_edge(n, j, k):
                continue
            # leftover or d=2
            if n < ph:
                sm += 1
            else:
                ge += 1
    return {"sm": sm, "ge": ge, "ph": ph}


def tot_form() -> dict:
    """k<=64: half doubling; odd-j never on even ph; G folds."""
    n_ok = 0
    if parent_half(0) != 2 or parent_half(1) != 5 or parent_half(2) != 10:
        return {"ok": False, "k012": True}
    if want_ph_lo(0) != 0 or want_ph_lo(1) != 2 or want_ph_lo(2) != 2:
        return {"ok": False, "ph012": True}
    if want_ph_lo(3) != 3 or G(5, 1) != 1 or G(5, 3) != 0:
        return {"ok": False, "g5": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
        if G(2 * m, 2 * m) != G(m, m):
            return {"ok": False, "ee": True, "m": m}
        if G(2 * m + 1, 2 * m + 1) != G(m, m):
            return {"ok": False, "oo": True, "m": m}
        if m > 0 and G(2 * m, 1) != 0:
            return {"ok": False, "eodd": True, "m": m}
        if G(2 * m + 1, 1) != G(m, 0):
            return {"ok": False, "oj": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if (ph % 2 == 0) != (k != 1):
            return {"ok": False, "pev": True, "k": k}
        if k >= 2:
            php = parent_half(k - 1)
            if 2 * php != ph:
                return {"ok": False, "2ph": True, "k": k}
            # even doubling: 2m >= ph iff m >= php
            if 2 * php < ph:
                return {"ok": False, "ed": True, "k": k}
            # odd doubling: 2m+1 > ph iff m >= php
            if 2 * php + 1 <= ph:
                return {"ok": False, "od": True, "k": k}
            if G(ph, 1) != 0:
                return {"ok": False, "phodd": True, "k": k}
        if k == 1 and ph % 2 == 0:
            return {"ok": False, "k1": True}
        if k >= 1 and jacobsthal(k + 1) != (1 << k) - jacobsthal(k):
            return {"ok": False, "Jrec": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        if 4 * u >= 5 * u:
            return {"ok": False, "hi": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_ph_lo(2) != 3
        and want_ph_lo(8) == 3
        and want_lo_e(8) == 14114
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(1) != (1 << 3)
        and want_lo_unp(1) != 4
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
        and G(2, 2) != 0
        and lucas(8) == 47
        and parent_half(8) == 640
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def oj_ph_fold() -> dict:
    """k<=8: odd-j leftover halves equal even leftover split for k>=2."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        eh = even_lo_ph_split(k)
        oj = odd_j_ph_split(k)
        e_ge = eh["eq"] + eh["lg"]
        if k >= 2:
            if oj["eq"] != 0:
                return {"ok": False, "eq": True, "k": k, "got": oj}
            if oj["sm"] != eh["sm"]:
                return {"ok": False, "sm": True, "k": k, "got": oj, "e": eh}
            if oj["lg"] != e_ge:
                return {"ok": False, "lg": True, "k": k, "got": oj, "e_ge": e_ge}
            pf = parent_lo_d2_ph_split(k - 1)
            if pf["sm"] != eh["sm"] or pf["ge"] != e_ge:
                return {"ok": False, "fold": True, "k": k, "got": pf}
            if oj["sm"] + oj["lg"] != want_lo_e(k):
                return {"ok": False, "tot": True, "k": k}
        if k == 1:
            if oj["sm"] == eh["sm"] and eh["sm"] == 1:
                return {"ok": False, "k1s": True}
            if oj["eq"] == 0:
                return {"ok": False, "k1e": True}
        n_ok += 1
        rows[str(k)] = {
            "oj_sm": oj["sm"],
            "oj_eq": oj["eq"],
            "oj_lg": oj["lg"],
            "e_sm": eh["sm"],
            "e_ge": e_ge,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["oj_sm"] == 0
        and rows["0"]["oj_lg"] == 0
        and rows["1"]["oj_sm"] == 0
        and rows["1"]["oj_eq"] == 1
        and rows["2"]["oj_sm"] == 4
        and rows["2"]["oj_lg"] == 2
        and rows["2"]["e_ge"] == 2
        and rows["8"]["oj_sm"] == 8790
        and rows["8"]["oj_lg"] == 5324
        and rows["8"]["e_sm"] == 8790
        and rows["8"]["e_ge"] == 5324
        and rows["8"]["oj_eq"] == 0
        and rows["1"]["oj_sm"] != rows["1"]["e_sm"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """oj halves at k=1; oj on even ph; oj_lg empty / equals lo_e."""
    oj1 = odd_j_ph_split(1)
    eh1 = even_lo_ph_split(1)
    oj8 = odd_j_ph_split(8)
    ok = (
        oj1["sm"] != eh1["sm"]
        and oj1["eq"] != 0
        and oj8["eq"] == 0
        and oj8["lg"] != 0
        and oj8["lg"] != want_lo_e(8)
        and oj8["lg"] != 3
        and oj8["sm"] != oj8["lg"]
        and want_ph_lo(2) != 3
        and parent_half(2) == 10
        and G(2, 1) == 0
        and G(2, 2) != 2 % 2
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(8) != (1 << 10)
        and G(0, 0) == 1
        and d2_clip_covering(0)
        and not d2_clip_covering(1)
        and unique_even_leftover(1)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_odd(0) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    ur = json.loads(UR_JSON.read_text())
    uq = json.loads(UQ_JSON.read_text())
    up = json.loads(UP_JSON.read_text())
    ok = (
        ur["checks"]["all_ok"]
        and uq["checks"]["all_ok"]
        and up["checks"]["all_ok"]
        and ur["verdict"]["ph_lo_eq_3_k_ge_3"] == "LEMMA"
        and ur["verdict"]["pg_lo_half_eq_2_even_lo_ph_k_ge_3"] == "LEMMA"
        and ur["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ur["verdict"]["prize"] == "unsolved"
        and want_d2_n(0) == 2
        and jacobsthal(2) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and cnt["ok"] and kl["ok"]
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
    cnt = oj_ph_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "US",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "oj_ph_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "oj_lg_eq_even_lo_ge_k_ge_2": True,
            "oj_sm_eq_even_lo_sm_k_ge_2": True,
            "oj_half_at_k1": False,
            "oj_on_even_ph": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "oj_lg_eq_even_lo_ge_k_ge_2": "LEMMA",
            "oj_sm_eq_even_lo_sm_k_ge_2": "LEMMA",
            "oj_half_at_k1": "KILLED",
            "oj_on_even_ph": "KILLED",
            "oj_lg_empty": "KILLED",
            "oj_lg_eq_lo_e": "KILLED",
            "oj_lg_eq_3": "KILLED",
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
            "lo_parent_large_diff_closed": "PREFIX",
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
        "oj_sm k8",
        dump["oj_ph_fold"]["rows"]["8"]["oj_sm"],
        "oj_lg k8",
        dump["oj_ph_fold"]["rows"]["8"]["oj_lg"],
        "e_ge k8",
        dump["oj_ph_fold"]["rows"]["8"]["e_ge"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
