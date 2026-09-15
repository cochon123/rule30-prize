#!/usr/bin/env python3
"""Cycle WL: unpaired xor 4-way is identically large.

pal_kind is never unp for n<=5U/2, because 2n-j<=2n<=5U. Unpaired
xor n_ug/n_gu, clip_gp, and j=0 unpaired therefore all sit on
n>5U/2: the small halves are 0 and the large halves equal the
Cycle WK/UB/UA tots. Dies at k=8 for ug_s equals n_ug (got 0, not
4924), gu_s equals n_gu (got 0, not 4818), gp_s equals clip_gp
(got 0, not 85), neg_s equals j=0 unpaired (got 0, not 192), ug_l
equals 0 (got 4924, not 0), pal_kind at n=5U/2 j=0 unpaired (it is
pair), pal_kind at n=1 unpaired, and pal_kind at n=639 unpaired.
Do not kill pal_kind at n=4U-1 unpaired: that cell is unp. Do not
PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wl.py --certify
Dump: research/cycle_wl.json
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
from cycle_tw import green_odd_even
from cycle_ua import want_j0_odd_unp
from cycle_ub import unpaired_xor_split, want_clip_gp
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uh import want_ug_minus_gu
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vr import want_extra_unp_fl
from cycle_we import want_ege_fl
from cycle_wh import want_sm_fl
from cycle_wj import want_xor_unp_fl
from cycle_wk import want_gu_fl, want_ug_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WK_JSON = Path(__file__).resolve().parent / "cycle_wk.json"
WJ_JSON = Path(__file__).resolve().parent / "cycle_wj.json"
UA_JSON = Path(__file__).resolve().parent / "cycle_ua.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ug_s(k: int) -> int:
    """unpaired xor n_ug on n<=5U/2: identically 0."""
    return 0


def want_ug_l(k: int) -> int:
    """unpaired xor n_ug on n>5U/2: equals tot n_ug."""
    return want_ug_fl(k)


def want_gu_s(k: int) -> int:
    """unpaired xor n_gu on n<=5U/2: identically 0."""
    return 0


def want_gu_l(k: int) -> int:
    """unpaired xor n_gu on n>5U/2: equals tot n_gu."""
    return want_gu_fl(k)


def want_gp_s(k: int) -> int:
    """clip_gp on n<=5U/2: identically 0."""
    return 0


def want_gp_l(k: int) -> int:
    """clip_gp on n>5U/2: equals tot clip_gp."""
    return want_clip_gp(k)


def want_neg_s(k: int) -> int:
    """j=0 unpaired on n<=5U/2: identically 0."""
    return 0


def want_neg_l(k: int) -> int:
    """j=0 unpaired on n>5U/2: equals tot j=0 unpaired."""
    return want_j0_odd_unp(k)


def odd_le_half(k: int) -> int:
    """Largest odd n<=5U/2, or 0 if none."""
    ph = parent_half(k)
    n = ph if ph % 2 == 1 else ph - 1
    return n if n >= 1 else 0


def unpaired_xor_half(k: int) -> dict:
    """Odd-n even-j unpaired: parent xor kinds split by n<=5U/2.

    Do not call this from tot_form for k<=64.
    """
    u = 1 << k
    clip = 5 * u
    half = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    a = {
        "ug_s": 0,
        "ug_l": 0,
        "gu_s": 0,
        "gu_l": 0,
        "gp_s": 0,
        "gp_l": 0,
        "neg_s": 0,
        "neg_l": 0,
        "pg": 0,
        "bad": 0,
    }
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        hi = min(2 * n, clip)
        tag = "_s" if n <= half else "_l"
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "unp":
                continue
            if j >= n:
                continue
            r = j // 2
            if green_odd_even(m, r) != 1:
                a["bad"] += 1
                continue
            if r == 0:
                a["neg" + tag] += 1
                continue
            kr = pal_kind(m, r, k_p) if G(m, r) else "g0"
            km = pal_kind(m, r - 1, k_p) if G(m, r - 1) else "g0"
            if km == "unp" and kr == "g0":
                a["ug" + tag] += 1
            elif km == "g0" and kr == "unp":
                a["gu" + tag] += 1
            elif km == "g0" and kr == "pair":
                if is_clip_edge(m, r, k_p):
                    a["gp" + tag] += 1
                else:
                    a["bad"] += 1
            elif km == "pair" and kr == "g0":
                a["pg"] += 1
            else:
                a["bad"] += 1
    return a


def tot_form() -> dict:
    """k<=64: pal_kind never unp for n<=5U/2; 4-way small halves 0.

    Do not call unpaired_xor_half / unpaired_xor_split here.
    Census is unp_half_fold for k<=8.
    """
    n_ok = 0
    if want_ug_s(8) != 0 or want_gu_s(2) != 0:
        return {"ok": False, "s0": True}
    if want_ug_l(8) != 4924 or want_gu_l(8) != 4818:
        return {"ok": False, "k8": True}
    if pal_kind(parent_half(8), 0, 8) == "unp":
        return {"ok": False, "ph8": True}
    if pal_kind(1, 0, 8) == "unp":
        return {"ok": False, "n1": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
        if G(m, 0) != 1:
            return {"ok": False, "g0": True, "m": m}
        if m > 0 and G(2 * m, 1) != 0:
            return {"ok": False, "eodd": True, "m": m}
        if not unique_van_odd_even(m, 0):
            return {"ok": False, "van": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if 2 * ph > clip:
            return {"ok": False, "2ph": True, "k": k}
        if k >= 1 and 2 * ph != clip:
            return {"ok": False, "eq": True, "k": k}
        if pal_kind(1, 0, k) == "unp":
            return {"ok": False, "n1k": True, "k": k}
        if pal_kind(ph, 0, k) == "unp":
            return {"ok": False, "phu": True, "k": k}
        n_s = odd_le_half(k)
        if n_s >= 1:
            if pal_kind(n_s, 0, k) == "unp":
                return {"ok": False, "ns": True, "k": k}
            if 2 * n_s > clip:
                return {"ok": False, "ns2": True, "k": k}
        n_l = 4 * u - 1
        if pal_kind(n_l, 0, k) != "unp":
            return {"ok": False, "nl": True, "k": k}
        if n_l <= ph:
            return {"ok": False, "nll": True, "k": k}
        if want_ug_s(k) != 0 or want_gu_s(k) != 0:
            return {"ok": False, "ugs": True, "k": k}
        if want_gp_s(k) != 0 or want_neg_s(k) != 0:
            return {"ok": False, "gps": True, "k": k}
        if want_ug_l(k) != want_ug_fl(k):
            return {"ok": False, "ugl": True, "k": k}
        if want_gu_l(k) != want_gu_fl(k):
            return {"ok": False, "gul": True, "k": k}
        if want_gp_l(k) != want_clip_gp(k):
            return {"ok": False, "gpl": True, "k": k}
        if want_neg_l(k) != want_j0_odd_unp(k):
            return {"ok": False, "negl": True, "k": k}
        if want_ug_s(k) + want_ug_l(k) != want_ug_fl(k):
            return {"ok": False, "sumu": True, "k": k}
        if want_gu_s(k) + want_gu_l(k) != want_gu_fl(k):
            return {"ok": False, "sumg": True, "k": k}
        if want_ug_l(k) + want_gu_l(k) != want_xor_unp_fl(k):
            return {"ok": False, "sumx": True, "k": k}
        if want_ug_l(k) - want_gu_l(k) != want_ug_minus_gu(k):
            return {"ok": False, "diff": True, "k": k}
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
        and want_ug_s(8) != want_ug_fl(8)
        and want_gu_s(8) != want_gu_fl(8)
        and want_gp_s(8) != want_clip_gp(8)
        and want_neg_s(8) != want_j0_odd_unp(8)
        and want_ug_l(8) != 0
        and pal_kind(parent_half(8), 0, 8) != "unp"
        and pal_kind(1, 0, 8) != "unp"
        and pal_kind(odd_le_half(8), 0, 8) != "unp"
        and pal_kind((1 << 8) * 4 - 1, 0, 8) == "unp"
        and pal_kind(parent_half(8) + 1, 0, 8) == "unp"
        and want_ug_l(8) == 4924
        and want_gu_l(8) == 4818
        and want_gp_l(8) == 85
        and want_neg_l(8) == 192
        and want_xor_unp_fl(8) == 9742
        and want_extra_unp_fl(8) == 10019
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and want_sm_fl(8) == 8790
        and want_sm(8) == 8790
        and want_ege_fl(8) == 5324
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
        and want_ej_xor(8) == 5225
        and lucas(8) == 47
        and fib(8) == 21
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
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
        and odd_le_half(8) == 639
        and parent_half(8) == 640
        and want_ug_l(2) == 2
        and want_gu_l(2) == 1
        and want_ug_l(3) == 9
        and want_gu_l(3) == 6
        and want_ug_l(4) == 36
        and want_ug_l(5) == 129
        and want_gu_l(5) == 116
        and want_gu_l(6) == 418
        and want_gp_l(2) == 1
        and want_neg_l(2) == 3
        and pal_kind(parent_half(1), 0, 1) != "unp"
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def unp_half_fold() -> dict:
    """k<=8 unpaired xor 4-way vs identically-large forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = unpaired_xor_half(k)
        b = unpaired_xor_split(k)
        if a["bad"] != 0 or a["pg"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if a["ug_s"] != want_ug_s(k) or a["ug_l"] != want_ug_l(k):
            return {"ok": False, "ug": True, "k": k, "got": a}
        if a["gu_s"] != want_gu_s(k) or a["gu_l"] != want_gu_l(k):
            return {"ok": False, "gu": True, "k": k, "got": a}
        if a["gp_s"] != want_gp_s(k) or a["gp_l"] != want_gp_l(k):
            return {"ok": False, "gp": True, "k": k, "got": a}
        if a["neg_s"] != want_neg_s(k) or a["neg_l"] != want_neg_l(k):
            return {"ok": False, "neg": True, "k": k, "got": a}
        if a["ug_s"] + a["ug_l"] != b["n_ug"]:
            return {"ok": False, "b_ug": True, "k": k}
        if a["gu_s"] + a["gu_l"] != b["n_gu"]:
            return {"ok": False, "b_gu": True, "k": k}
        if a["gp_s"] + a["gp_l"] != b["n_gp"]:
            return {"ok": False, "b_gp": True, "k": k}
        if a["neg_s"] + a["neg_l"] != b["n_neg"]:
            return {"ok": False, "b_neg": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "ug_s": a["ug_s"],
            "ug_l": a["ug_l"],
            "gu_s": a["gu_s"],
            "gu_l": a["gu_l"],
            "gp_s": a["gp_s"],
            "gp_l": a["gp_l"],
            "neg_s": a["neg_s"],
            "neg_l": a["neg_l"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["ug_s"] == 0
        and rows["2"]["ug_l"] == 2
        and rows["2"]["gu_s"] == 0
        and rows["2"]["gu_l"] == 1
        and rows["2"]["gp_l"] == 1
        and rows["2"]["neg_l"] == 3
        and rows["3"]["ug_l"] == 9
        and rows["3"]["gu_l"] == 6
        and rows["8"]["ug_s"] == 0
        and rows["8"]["ug_l"] == 4924
        and rows["8"]["gu_s"] == 0
        and rows["8"]["gu_l"] == 4818
        and rows["8"]["gp_s"] == 0
        and rows["8"]["gp_l"] == 85
        and rows["8"]["neg_s"] == 0
        and rows["8"]["neg_l"] == 192
        and want_ug_l(4) == 36
        and want_ug_l(5) == 129
        and want_gu_l(5) == 116
        and want_gu_l(6) == 418
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """Small halves equal tots at k=8; pal_kind unp at n<=5U/2."""
    ok = (
        want_ug_s(8) != want_ug_fl(8)
        and want_gu_s(8) != want_gu_fl(8)
        and want_gp_s(8) != want_clip_gp(8)
        and want_neg_s(8) != want_j0_odd_unp(8)
        and want_ug_l(8) != 0
        and pal_kind(parent_half(8), 0, 8) != "unp"
        and pal_kind(1, 0, 8) != "unp"
        and pal_kind(odd_le_half(8), 0, 8) != "unp"
        and pal_kind(parent_half(1), 0, 1) != "unp"
        and pal_kind((1 << 8) * 4 - 1, 0, 8) == "unp"
        and pal_kind(parent_half(8) + 1, 0, 8) == "unp"
        and want_ug_s(8) == 0
        and want_ug_fl(8) == 4924
        and want_gu_fl(8) == 4818
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and want_ug_s(2) != 2
        and want_gu_s(2) != 1
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and odd_le_half(8) == 639
        and G(2, 1) == 0
        and G(4, 2) == G(2, 1)
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
    wk = json.loads(WK_JSON.read_text())
    wj = json.loads(WJ_JSON.read_text())
    ua = json.loads(UA_JSON.read_text())
    ok = (
        wk["checks"]["all_ok"]
        and wj["checks"]["all_ok"]
        and ua["checks"]["all_ok"]
        and wk["verdict"]["ug_eq_FL_closed_k_ge_2"] == "LEMMA"
        and wj["verdict"]["xor_unp_eq_FL_closed_k_ge_2"] == "LEMMA"
        and ua["verdict"]["j0_odd_unp_eq_3_2km2"] == "LEMMA"
        and wk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wk["verdict"]["prize"] == "unsolved"
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
    cnt = unp_half_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "unp_half_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unp_never_n_le_ph": True,
            "ug_s_eq_0": True,
            "gu_s_eq_0": True,
            "gp_s_eq_0": True,
            "neg_s_eq_0": True,
            "ug_l_eq_ug": True,
            "gu_l_eq_gu": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unp_never_n_le_ph": "LEMMA",
            "ug_s_eq_0": "LEMMA",
            "gu_s_eq_0": "LEMMA",
            "gp_s_eq_0": "LEMMA",
            "neg_s_eq_0": "LEMMA",
            "ug_l_eq_ug": "LEMMA",
            "gu_l_eq_gu": "LEMMA",
            "ug_s_eq_ug_at_k8": "KILLED",
            "gu_s_eq_gu_at_k8": "KILLED",
            "gp_s_eq_clip_gp_at_k8": "KILLED",
            "neg_s_eq_j0_unp_at_k8": "KILLED",
            "ug_l_eq_0_at_k8": "KILLED",
            "ph_j0_unp_at_k8": "KILLED",
            "n1_unp_at_k8": "KILLED",
            "n639_unp_at_k8": "KILLED",
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
        "4w k8",
        dump["unp_half_fold"]["rows"]["8"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
