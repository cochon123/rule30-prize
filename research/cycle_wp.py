#!/usr/bin/env python3
"""Cycle WP: first ug/gu/gp is n=5U/2+5 for k>=5.

The first three odd covering n>5U/2 are 5U/2+1, +3, +5. Cycle WO
has only j=0 even-j unpaired extra at +1. At +3, G(n,2)=0 because
both parent bits at the WO parent fire, so even-j unpaired extra is
again only j=0 for k>=4. At +5, parent is even n=5U_p/2+2 with
unpaired j=0 and j=2, and even-j unpaired extra is
{0,2,4,6,8} = (neg, ug, gu, ug, gp) for k>=5. Dies at k=4 for the
five-cell (got 4, no gp) and for first gp at +5 (got +7). Dies at
k=3 for first ug at +5 (got +3). Do not kill pal_kind unpaired at
n=5U/2+5, j=0,2,4,6,8. Do not PREFIX pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_wp.py --certify
Dump: research/cycle_wp.json
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
from cycle_ub import want_clip_gp
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_we import want_ege_fl
from cycle_wh import want_sm_fl
from cycle_wk import want_gu_fl, want_ug_fl
from cycle_wm import want_j0_all_unp, want_j0_even_unp
from cycle_wn import want_clip_gp_jk, want_clip_slice
from cycle_wo import ph1_n, ph1_split, want_ph1_even_unp, want_ph1_ug
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WO_JSON = Path(__file__).resolve().parent / "cycle_wo.json"
WN_JSON = Path(__file__).resolve().parent / "cycle_wn.json"
WM_JSON = Path(__file__).resolve().parent / "cycle_wm.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph3_n(k: int) -> int:
    """Covering n=5U/2+3."""
    return parent_half(k) + 3


def ph5_n(k: int) -> int:
    """Covering n=5U/2+5."""
    return parent_half(k) + 5


def want_ph3_even_unp(k: int) -> int:
    """Even-j unpaired extra at n=5U/2+3: 1 for k>=4; 3,2 at k=2,3."""
    if k <= 1:
        return 0
    if k == 2:
        return 3
    if k == 3:
        return 2
    return 1


def want_ph3_ug(k: int) -> int:
    """n_ug at n=5U/2+3: 0 for k>=4; 1 at k=2,3."""
    if k in (2, 3):
        return 1
    return 0


def want_ph5_even_unp(k: int) -> int:
    """Even-j unpaired extra at n=5U/2+5: 5 for k>=5; 4 at k=4; 3 at k<=3."""
    if k <= 1:
        return 0
    if k <= 3:
        return 3
    if k == 4:
        return 4
    return 5


def want_ph5_ug(k: int) -> int:
    """n_ug at n=5U/2+5: 2 for k>=4; 1 at k=2,3."""
    if k <= 1:
        return 0
    if k <= 3:
        return 1
    return 2


def want_ph5_gu(k: int) -> int:
    """n_gu at n=5U/2+5: 1 for k>=4 except 0 at k=3; 1 at k=2."""
    if k <= 1 or k == 3:
        return 0
    return 1


def want_ph5_gp(k: int) -> int:
    """n_gp at n=5U/2+5: 1 for k>=5; 0 at k=4; 1 at k=3; 0 at k=2."""
    if k == 3 or k >= 5:
        return 1
    return 0


def want_first_ug_n(k: int) -> int:
    """First odd n>5U/2 with n_ug: 5U/2+3 at k<=3, else +5."""
    if k <= 3:
        return ph3_n(k)
    return ph5_n(k)


def want_first_gp_n(k: int) -> int:
    """First odd n>5U/2 with n_gp: +3,+5,+7, then +5."""
    if k == 2:
        return ph3_n(k)
    if k == 4:
        return ph5_n(k) + 2
    return ph5_n(k)


def unp_xor_at(k: int, n: int) -> dict:
    """Even-j unpaired extra kinds at one odd covering n. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    k_p = k - 1 if k >= 1 else 0
    m = (n - 1) // 2
    n_ug = n_gu = n_gp = n_neg = n_bad = extra = 0
    js = []
    for j in range(0, min(2 * n, clip) + 1, 2):
        if j >= n or G(n, j) == 0 or pal_kind(n, j, k) != "unp":
            continue
        extra += 1
        js.append(j)
        r = j // 2
        if green_odd_even(m, r) != 1:
            n_bad += 1
            continue
        if r == 0:
            n_neg += 1
            continue
        kr = pal_kind(m, r, k_p) if G(m, r) else "g0"
        km = pal_kind(m, r - 1, k_p) if G(m, r - 1) else "g0"
        if km == "unp" and kr == "g0":
            n_ug += 1
        elif km == "g0" and kr == "unp":
            n_gu += 1
        elif km == "g0" and kr == "pair" and is_clip_edge(m, r, k_p):
            n_gp += 1
        else:
            n_bad += 1
    return {
        "extra": extra,
        "n_ug": n_ug,
        "n_gu": n_gu,
        "n_gp": n_gp,
        "n_neg": n_neg,
        "n_bad": n_bad,
        "js": js,
    }


def tot_form() -> dict:
    """k<=64: n=5U/2+5 five-cell; dies at k=4 without gp.

    Do not call unp_xor_at / ph1_split here.
    Census is ph5_fold for k<=8.
    """
    n_ok = 0
    if want_ph5_even_unp(0) != 0 or want_ph3_even_unp(1) != 0:
        return {"ok": False, "k01": True}
    if want_ph5_even_unp(4) != 4 or want_ph5_gp(4) != 0:
        return {"ok": False, "k4": True}
    if want_ph5_even_unp(8) != 5 or want_ph5_gp(8) != 1:
        return {"ok": False, "k8": True}
    if want_ph3_even_unp(8) != 1 or want_ph3_ug(8) != 0:
        return {"ok": False, "p3": True}
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
        n1 = ph1_n(k)
        n3 = ph3_n(k)
        n5 = ph5_n(k)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if n3 != ph + 3 or n5 != ph + 5:
            return {"ok": False, "n": True, "k": k}
        if want_ph1_even_unp(k) != 1 or want_ph1_ug(k) != 0:
            return {"ok": False, "wo": True, "k": k}
        if k >= 2:
            if n5 >= 4 * u or n3 >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if n1 % 2 != 1 or n3 % 2 != 1 or n5 % 2 != 1:
                return {"ok": False, "odd": True, "k": k}
            if pal_kind(n5, 0, k) != "unp" or G(n5, 0) != 1:
                return {"ok": False, "j0": True, "k": k}
            if 2 * n5 - clip - 2 != 8:
                return {"ok": False, "sl": True, "k": k}
            m5 = (n5 - 1) // 2
            m3 = (n3 - 1) // 2
            if m5 != parent_half(k - 1) + 2:
                return {"ok": False, "m5": True, "k": k}
            if m3 != ph1_n(k - 1):
                return {"ok": False, "m3": True, "k": k}
        if k >= 4:
            m5 = (n5 - 1) // 2
            m3 = (n3 - 1) // 2
            if pal_kind(m5, 0, k - 1) != "unp" or G(m5, 0) != 1:
                return {"ok": False, "p0": True, "k": k}
            if pal_kind(m5, 2, k - 1) != "unp" or G(m5, 2) != 1:
                return {"ok": False, "p2": True, "k": k}
            if G(n3, 2) != 0:
                return {"ok": False, "g32": True, "k": k}
            if G(m3, 0) != 1 or G(m3, 1) != 1:
                return {"ok": False, "wo1": True, "k": k}
            if G(n3, 2) != G(m3, 1) ^ G(m3, 0):
                return {"ok": False, "xor": True, "k": k}
            for j in (0, 2, 4, 6):
                if G(n5, j) != 1 or pal_kind(n5, j, k) != "unp":
                    return {"ok": False, "c5": True, "k": k, "j": j}
            if want_ph3_even_unp(k) != 1 or want_ph3_ug(k) != 0:
                return {"ok": False, "p3w": True, "k": k}
            if want_ph5_ug(k) != 2 or want_ph5_gu(k) != 1:
                return {"ok": False, "p5w": True, "k": k}
            if want_first_ug_n(k) != n5:
                return {"ok": False, "fug": True, "k": k}
        if k >= 5:
            m5 = (n5 - 1) // 2
            if G(n5, 8) != 1 or pal_kind(n5, 8, k) != "unp":
                return {"ok": False, "j8": True, "k": k}
            if is_clip_edge(n5, 8, k):
                return {"ok": False, "c8": True, "k": k}
            if 2 * n5 - 8 != clip + 2:
                return {"ok": False, "pr8": True, "k": k}
            if not is_clip_edge(m5, 4, k - 1):
                return {"ok": False, "pc4": True, "k": k}
            if G(m5, 4) != 1 or pal_kind(m5, 4, k - 1) != "pair":
                return {"ok": False, "g4": True, "k": k}
            if G(m5, 4) != G(ph1_n(k - 2), 2):
                return {"ok": False, "dbl": True, "k": k}
            if want_ph5_even_unp(k) != 5 or want_ph5_gp(k) != 1:
                return {"ok": False, "five": True, "k": k}
            if want_first_gp_n(k) != n5:
                return {"ok": False, "fgp": True, "k": k}
        if k == 4:
            if want_ph5_even_unp(k) != 4 or want_ph5_gp(k) != 0:
                return {"ok": False, "k4b": True}
            if G(n5, 8) != 0:
                return {"ok": False, "k4g8": True}
            if want_first_gp_n(k) != n5 + 2:
                return {"ok": False, "k4gp": True}
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
        and want_ph5_even_unp(4) != 5
        and want_first_ug_n(3) != ph5_n(3)
        and want_first_gp_n(4) != ph5_n(4)
        and want_ph3_ug(3) != 0
        and want_ph5_even_unp(8) != want_clip_gp(8)
        and want_ph5_even_unp(8) != want_j0_odd_unp(8)
        and want_ph5_even_unp(8) != want_clip_slice(8)
        and G(ph5_n(4), 8) != 1
        and pal_kind(ph5_n(8), 8, 8) == "unp"
        and pal_kind(ph5_n(8), 0, 8) == "unp"
        and want_ph5_even_unp(8) == 5
        and want_ph5_ug(8) == 2
        and want_ph5_gu(8) == 1
        and want_ph5_gp(8) == 1
        and want_ph3_even_unp(8) == 1
        and want_ph3_ug(8) == 0
        and want_first_ug_n(8) == 645
        and want_first_gp_n(8) == 645
        and ph5_n(8) == 645
        and ph3_n(8) == 643
        and ph1_n(8) == 641
        and want_clip_slice(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_j0_even_unp(8) == 191
        and want_j0_all_unp(8) == 383
        and want_ug_fl(8) == 4924
        and want_gu_fl(8) == 4818
        and want_sm_fl(8) == 8790
        and want_sm(8) == 8790
        and want_ege_fl(8) == 5324
        and want_ege(8) == 5324
        and want_ej_xor(8) == 5225
        and lucas(8) == 47
        and fib(8) == 21
        and jacobsthal(8) == 85
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
        and parent_half(8) == 640
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ph5_fold() -> dict:
    """k<=8 even-j unpaired extra at n=5U/2+1,+3,+5."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a1 = ph1_split(k)
        if a1["n_ug"] != 0 or a1["n_gu"] != 0 or a1["n_gp"] != 0:
            return {"ok": False, "p1": True, "k": k, "got": a1}
        a3 = unp_xor_at(k, ph3_n(k)) if k >= 2 else {
            "extra": 0, "n_ug": 0, "n_gu": 0, "n_gp": 0, "n_neg": 0, "n_bad": 0, "js": []
        }
        a5 = unp_xor_at(k, ph5_n(k)) if k >= 2 else {
            "extra": 0, "n_ug": 0, "n_gu": 0, "n_gp": 0, "n_neg": 0, "n_bad": 0, "js": []
        }
        if a3["n_bad"] != 0 or a5["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "a3": a3, "a5": a5}
        if a3["extra"] != want_ph3_even_unp(k) or a3["n_ug"] != want_ph3_ug(k):
            return {"ok": False, "p3": True, "k": k, "got": a3}
        if a3["n_gu"] != 0:
            return {"ok": False, "p3gu": True, "k": k, "got": a3}
        if a5["extra"] != want_ph5_even_unp(k):
            return {"ok": False, "p5e": True, "k": k, "got": a5}
        if a5["n_ug"] != want_ph5_ug(k) or a5["n_gu"] != want_ph5_gu(k):
            return {"ok": False, "p5u": True, "k": k, "got": a5}
        if a5["n_gp"] != want_ph5_gp(k):
            return {"ok": False, "p5g": True, "k": k, "got": a5}
        if k >= 5 and a5["js"] != [0, 2, 4, 6, 8]:
            return {"ok": False, "js": True, "k": k, "got": a5["js"]}
        if k >= 4 and a3["js"] != [0]:
            return {"ok": False, "js3": True, "k": k, "got": a3["js"]}
        n_ok += 1
        rows[str(k)] = {
            "p3": a3["extra"],
            "p5": a5["extra"],
            "p5_ug": a5["n_ug"],
            "p5_gu": a5["n_gu"],
            "p5_gp": a5["n_gp"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["p5"] == 3
        and rows["3"]["p3"] == 2
        and rows["4"]["p5"] == 4
        and rows["4"]["p5_gp"] == 0
        and rows["5"]["p5"] == 5
        and rows["8"]["p5"] == 5
        and rows["8"]["p5_ug"] == 2
        and rows["8"]["p5_gu"] == 1
        and rows["8"]["p5_gp"] == 1
        and rows["8"]["p3"] == 1
        and want_ph5_even_unp(6) == 5
        and want_ph5_even_unp(7) == 5
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """five-cell at k=4; first ug at +5 at k=3; first gp at +5 at k=4."""
    ok = (
        want_ph5_even_unp(4) != 5
        and want_first_ug_n(3) != ph5_n(3)
        and want_first_gp_n(4) != ph5_n(4)
        and want_ph3_ug(3) != 0
        and want_ph5_even_unp(8) != want_clip_gp(8)
        and want_ph5_even_unp(8) != want_j0_odd_unp(8)
        and want_ph5_even_unp(8) != want_clip_slice(8)
        and G(ph5_n(4), 8) != 1
        and pal_kind(ph5_n(8), 8, 8) == "unp"
        and pal_kind(ph5_n(8), 2, 8) == "unp"
        and pal_kind(ph5_n(8), 4, 8) == "unp"
        and pal_kind(ph5_n(8), 6, 8) == "unp"
        and want_ph5_even_unp(4) == 4
        and want_first_ug_n(3) == ph3_n(3)
        and want_first_gp_n(4) == ph5_n(4) + 2
        and want_ph3_ug(3) == 1
        and want_ph5_even_unp(8) == 5
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and want_clip_slice(8) == 85
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and ph5_n(8) == 645
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
    wo = json.loads(WO_JSON.read_text())
    wn = json.loads(WN_JSON.read_text())
    wm = json.loads(WM_JSON.read_text())
    ok = (
        wo["checks"]["all_ok"]
        and wn["checks"]["all_ok"]
        and wm["checks"]["all_ok"]
        and wo["verdict"]["ph1_no_ug_gu_gp"] == "LEMMA"
        and wn["verdict"]["clip_gp_eq_J_k_minus_kmod2"] == "LEMMA"
        and wm["verdict"]["j0_unp_eq_window"] == "LEMMA"
        and wo["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wo["verdict"]["prize"] == "unsolved"
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
    cnt = ph5_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph5_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph3_only_j0_k_ge_4": True,
            "ph5_five_cell_k_ge_5": True,
            "first_ug_gp_eq_ph5_k_ge_5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph3_only_j0_k_ge_4": "LEMMA",
            "ph5_five_cell_k_ge_5": "LEMMA",
            "first_ug_eq_ph5_k_ge_4": "LEMMA",
            "first_gp_eq_ph5_k_ge_5": "LEMMA",
            "ph5_five_cell_at_k4": "KILLED",
            "first_ug_eq_ph5_at_k3": "KILLED",
            "first_gp_eq_ph5_at_k4": "KILLED",
            "ph3_ug_eq_0_at_k3": "KILLED",
            "ph5_eq_clip_gp_at_k8": "KILLED",
            "ph5_eq_j0_odd_at_k8": "KILLED",
            "ph5_eq_slice_at_k8": "KILLED",
            "ph5_G8_eq_1_at_k4": "KILLED",
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
    print("ph5 k8", dump["ph5_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
