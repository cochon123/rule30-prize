#!/usr/bin/env python3
"""Cycle WG: named leftover extra 4-way closed forms.

pg_s is (5*2^{k-2}-4(-1)^{k-1})/3 for k>=3.
gp_s is 5*2^{k-3}-2 for k>=3.
pg_l is 2^{k-2}+2(-1)^{k-1} for k>=3.
gp_l is 3*2^{k-3} for k>=3.
They sum to Cycle VY named halves and equal leftover xor 4-way
minus leftover-parent xor 4-way. pg_s+pg_l is 2 J_k for k>=2.
Dies at k=3 for pg_s/pg_l with shift 0 (pg_s got -2, not 2; pg_l
got 2, not 4). Do not kill gp_s or gp_l shift 0 at k=3: 2^{0}=1
so they match. Dies at k=2 for pg_s/pg_l forms (pg_s got 3, not 2;
pg_l got -1, not 0). Dies at k=8 without pg_s 5*2^{k-2} (got 1,
not 108), without pg_s sign (got 106, not 108), without gp_s -2
(got 160, not 158), without gp_s 5*2^{k-3} (got -2, not 158),
without pg_l 2^{k-2} (got -2, not 62), without pg_l sign (got 64,
not 62), without gp_l 3 (got 32, not 96), and without gp_l
2^{k-3} (got 3, not 96). Dies at k=8 for pg_s equals tot small
(got 108, not 266), pg_s equals tot pg (got 108, not 170), and
pg_s equals gp_s (got 108, not 158). Special pg_s=1 at k=1 and
2 at k=2; gp_l=2 at k=2. Census k=8: pg_s 108, gp_s 158, pg_l
62, gp_l 96. Do not PREFIX pal-center tot. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_wg.py --certify
Dump: research/cycle_wg.json
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
from cycle_ul import want_named_lo
from cycle_uo import named_half_split
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vy import want_named_l_fl, want_named_s_fl
from cycle_wc import (
    want_xor_gp_l_fl,
    want_xor_gp_s_fl,
    want_xor_pg_l_fl,
    want_xor_pg_s_fl,
)
from cycle_we import want_ege_fl
from cycle_wf import (
    want_glo_l_fl,
    want_glo_s_fl,
    want_plo_l_fl,
    want_plo_s_fl,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WF_JSON = Path(__file__).resolve().parent / "cycle_wf.json"
WC_JSON = Path(__file__).resolve().parent / "cycle_wc.json"
VY_JSON = Path(__file__).resolve().parent / "cycle_vy.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_named_pg_s_fl(k: int) -> int:
    """named leftover extra n_pg on n<=5U/2: (5*2^{k-2}-4(-1)^{k-1})/3 for k>=3."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    if k == 2:
        return 2
    n = 5 * (1 << (k - 2)) - 4 * ((-1) ** (k - 1))
    return n // 3


def want_named_gp_s_fl(k: int) -> int:
    """named leftover extra n_gp on n<=5U/2: 5*2^{k-3}-2 for k>=3."""
    if k <= 2:
        return 0
    return 5 * (1 << (k - 3)) - 2


def want_named_pg_l_fl(k: int) -> int:
    """named leftover extra n_pg on n>5U/2: 2^{k-2}+2(-1)^{k-1} for k>=3."""
    if k <= 2:
        return 0
    return (1 << (k - 2)) + 2 * ((-1) ** (k - 1))


def want_named_gp_l_fl(k: int) -> int:
    """named leftover extra n_gp on n>5U/2: 3*2^{k-3} for k>=3; 2 at k=2."""
    if k <= 1:
        return 0
    if k == 2:
        return 2
    return 3 * (1 << (k - 3))


def tot_form() -> dict:
    """k<=64: named leftover extra 4-way; dies at k=3 with shift 0 on pg.

    Do not call named_half_split / leftover_xor_half here.
    Census is named_4w_fold for k<=8. gp_s/gp_l shift 0 at k=3 matches.
    """
    n_ok = 0
    raw_pgs3 = (-4 * ((-1) ** 2)) // 3
    raw_pgl3 = 2 * ((-1) ** 2)
    miss_pgs_pow = (-4 * ((-1) ** 7)) // 3
    miss_pgs_sign = (5 * (1 << 6)) // 3
    miss_gps2 = 5 * (1 << 5)
    miss_gps5 = -2
    miss_pgl_pow = 2 * ((-1) ** 7)
    miss_pgl_sign = 1 << 6
    miss_gpl3 = 1 << 5
    miss_gpl_pow = 3
    form_pgs2 = (5 * (1 << 0) - 4 * ((-1) ** 1)) // 3
    form_pgl2 = (1 << 0) + 2 * ((-1) ** 1)
    if want_named_pg_s_fl(0) != 0 or want_named_pg_s_fl(1) != 1:
        return {"ok": False, "k01": True}
    if want_named_pg_s_fl(2) != 2 or want_named_gp_s_fl(2) != 0:
        return {"ok": False, "k2s": True}
    if want_named_pg_l_fl(2) != 0 or want_named_gp_l_fl(2) != 2:
        return {"ok": False, "k2l": True}
    if want_named_pg_s_fl(3) != 2 or want_named_gp_s_fl(3) != 3:
        return {"ok": False, "k3s": True}
    if want_named_pg_l_fl(3) != 4 or want_named_gp_l_fl(3) != 3:
        return {"ok": False, "k3l": True}
    if want_named_pg_s_fl(8) != 108 or want_named_gp_s_fl(8) != 158:
        return {"ok": False, "k8s": True}
    if want_named_pg_l_fl(8) != 62 or want_named_gp_l_fl(8) != 96:
        return {"ok": False, "k8l": True}
    if want_named_pg_s_fl(3) == raw_pgs3:
        return {"ok": False, "rawps": True}
    if want_named_pg_l_fl(3) == raw_pgl3:
        return {"ok": False, "rawpl": True}
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
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if want_named_pg_s_fl(k) != want_xor_pg_s_fl(k) - want_plo_s_fl(k):
            return {"ok": False, "ps": True, "k": k}
        if want_named_gp_s_fl(k) != want_xor_gp_s_fl(k) - want_glo_s_fl(k):
            return {"ok": False, "gs": True, "k": k}
        if want_named_pg_l_fl(k) != want_xor_pg_l_fl(k) - want_plo_l_fl(k):
            return {"ok": False, "pl": True, "k": k}
        if want_named_gp_l_fl(k) != want_xor_gp_l_fl(k) - want_glo_l_fl(k):
            return {"ok": False, "gl": True, "k": k}
        if want_named_pg_s_fl(k) + want_named_gp_s_fl(k) != want_named_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if want_named_pg_l_fl(k) + want_named_gp_l_fl(k) != want_named_l_fl(k):
            return {"ok": False, "suml": True, "k": k}
        if (
            want_named_pg_s_fl(k)
            + want_named_gp_s_fl(k)
            + want_named_pg_l_fl(k)
            + want_named_gp_l_fl(k)
            != want_named_lo(k)
        ):
            return {"ok": False, "tot": True, "k": k}
        if k >= 2 and want_named_pg_s_fl(k) + want_named_pg_l_fl(k) != 2 * jacobsthal(k):
            return {"ok": False, "Jpg": True, "k": k}
        if k >= 3:
            ns = 5 * (1 << (k - 2)) - 4 * ((-1) ** (k - 1))
            if ns % 3 != 0 or ns // 3 != want_named_pg_s_fl(k):
                return {"ok": False, "dps": True, "k": k}
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
        and want_named_pg_s_fl(3) != raw_pgs3
        and want_named_pg_l_fl(3) != raw_pgl3
        and want_named_gp_s_fl(3) == 5 * (1 << 0) - 2
        and want_named_gp_l_fl(3) == 3 * (1 << 0)
        and want_named_pg_s_fl(8) != miss_pgs_pow
        and want_named_pg_s_fl(8) != miss_pgs_sign
        and want_named_gp_s_fl(8) != miss_gps2
        and want_named_gp_s_fl(8) != miss_gps5
        and want_named_pg_l_fl(8) != miss_pgl_pow
        and want_named_pg_l_fl(8) != miss_pgl_sign
        and want_named_gp_l_fl(8) != miss_gpl3
        and want_named_gp_l_fl(8) != miss_gpl_pow
        and want_named_pg_s_fl(2) != form_pgs2
        and want_named_pg_l_fl(2) != form_pgl2
        and want_named_pg_s_fl(8) != want_named_s_fl(8)
        and want_named_pg_s_fl(8) != 2 * jacobsthal(8)
        and want_named_pg_s_fl(8) != want_named_gp_s_fl(8)
        and want_named_pg_s_fl(8) == 108
        and want_named_gp_s_fl(8) == 158
        and want_named_pg_l_fl(8) == 62
        and want_named_gp_l_fl(8) == 96
        and want_named_s_fl(8) == 266
        and want_named_l_fl(8) == 158
        and want_named_lo(8) == 424
        and 2 * jacobsthal(8) == 170
        and want_named_gp_s_fl(8) + want_named_gp_l_fl(8)
        == jacobsthal(9) + jacobsthal(8) - 2
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
        and miss_pgs_pow == 1
        and miss_pgs_sign == 106
        and miss_gps2 == 160
        and miss_gps5 == -2
        and miss_pgl_pow == -2
        and miss_pgl_sign == 64
        and miss_gpl3 == 32
        and miss_gpl_pow == 3
        and raw_pgs3 == -2
        and raw_pgl3 == 2
        and form_pgs2 == 3
        and form_pgl2 == -1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def named_4w_fold() -> dict:
    """k<=8 named leftover extra 4-way vs closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = named_half_split(k)
        if a["n_bad"] != 0 or a["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        gps = a["gpd1_s"] + a["gpd2_s"]
        gpl = a["gpd1_l"] + a["gpd2_l"]
        if a["pgd2_s"] != want_named_pg_s_fl(k):
            return {"ok": False, "ps": True, "k": k, "got": a["pgd2_s"]}
        if gps != want_named_gp_s_fl(k):
            return {"ok": False, "gs": True, "k": k, "got": gps}
        if a["pgd2_l"] != want_named_pg_l_fl(k):
            return {"ok": False, "pl": True, "k": k, "got": a["pgd2_l"]}
        if gpl != want_named_gp_l_fl(k):
            return {"ok": False, "gl": True, "k": k, "got": gpl}
        if a["pgd2_s"] + gps != want_named_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if a["pgd2_l"] + gpl != want_named_l_fl(k):
            return {"ok": False, "suml": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "pg_s": a["pgd2_s"],
            "gp_s": gps,
            "pg_l": a["pgd2_l"],
            "gp_l": gpl,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["pg_s"] == 1
        and rows["1"]["gp_l"] == 0
        and rows["2"]["pg_s"] == 2
        and rows["2"]["pg_l"] == 0
        and rows["2"]["gp_l"] == 2
        and rows["3"]["pg_s"] == 2
        and rows["3"]["gp_s"] == 3
        and rows["3"]["pg_l"] == 4
        and rows["3"]["gp_l"] == 3
        and rows["8"]["pg_s"] == 108
        and rows["8"]["gp_s"] == 158
        and rows["8"]["pg_l"] == 62
        and rows["8"]["gp_l"] == 96
        and want_named_pg_s_fl(4) == 8
        and want_named_gp_s_fl(5) == 18
        and want_named_pg_l_fl(5) == 10
        and want_named_gp_l_fl(6) == 24
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """pg_s/pg_l shift 0 at k=3; k=2 forms; k=8 missing powers/signs."""
    raw_pgs3 = (-4 * ((-1) ** 2)) // 3
    raw_pgl3 = 2 * ((-1) ** 2)
    miss_pgs_pow = (-4 * ((-1) ** 7)) // 3
    miss_pgs_sign = (5 * (1 << 6)) // 3
    miss_gps2 = 5 * (1 << 5)
    miss_gps5 = -2
    miss_pgl_pow = 2 * ((-1) ** 7)
    miss_pgl_sign = 1 << 6
    miss_gpl3 = 1 << 5
    miss_gpl_pow = 3
    form_pgs2 = (5 * (1 << 0) - 4 * ((-1) ** 1)) // 3
    form_pgl2 = (1 << 0) + 2 * ((-1) ** 1)
    a8 = named_half_split(8)
    gps8 = a8["gpd1_s"] + a8["gpd2_s"]
    gpl8 = a8["gpd1_l"] + a8["gpd2_l"]
    ok = (
        want_named_pg_s_fl(3) != raw_pgs3
        and want_named_pg_l_fl(3) != raw_pgl3
        and want_named_gp_s_fl(3) == 5 * (1 << 0) - 2
        and want_named_gp_l_fl(3) == 3 * (1 << 0)
        and want_named_pg_s_fl(8) != miss_pgs_pow
        and want_named_pg_s_fl(8) != miss_pgs_sign
        and want_named_gp_s_fl(8) != miss_gps2
        and want_named_gp_s_fl(8) != miss_gps5
        and want_named_pg_l_fl(8) != miss_pgl_pow
        and want_named_pg_l_fl(8) != miss_pgl_sign
        and want_named_gp_l_fl(8) != miss_gpl3
        and want_named_gp_l_fl(8) != miss_gpl_pow
        and want_named_pg_s_fl(2) != form_pgs2
        and want_named_pg_l_fl(2) != form_pgl2
        and want_named_pg_s_fl(8) != want_named_s_fl(8)
        and want_named_pg_s_fl(8) != 2 * jacobsthal(8)
        and want_named_pg_s_fl(8) != want_named_gp_s_fl(8)
        and a8["pgd2_s"] == 108
        and gps8 == 158
        and a8["pgd2_l"] == 62
        and gpl8 == 96
        and miss_pgs_pow == 1
        and miss_pgs_sign == 106
        and miss_gps2 == 160
        and miss_gps5 == -2
        and miss_pgl_pow == -2
        and miss_pgl_sign == 64
        and miss_gpl3 == 32
        and miss_gpl_pow == 3
        and raw_pgs3 == -2
        and raw_pgl3 == 2
        and form_pgs2 == 3
        and form_pgl2 == -1
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
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
    wf = json.loads(WF_JSON.read_text())
    wc = json.loads(WC_JSON.read_text())
    vy = json.loads(VY_JSON.read_text())
    ok = (
        wf["checks"]["all_ok"]
        and wc["checks"]["all_ok"]
        and vy["checks"]["all_ok"]
        and wf["verdict"]["plo_s_eq_FL_closed_k_ge_3"] == "LEMMA"
        and wc["verdict"]["xor_pg_s_eq_FL_closed_k_ge_3"] == "LEMMA"
        and vy["verdict"]["named_s_eq_closed_k_ge_3"] == "LEMMA"
        and wf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wf["verdict"]["prize"] == "unsolved"
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
    cnt = named_4w_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "named_4w_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "named_pg_s_eq_closed_k_ge_3": True,
            "named_gp_s_eq_closed_k_ge_3": True,
            "named_pg_l_eq_closed_k_ge_3": True,
            "named_gp_l_eq_closed_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "named_pg_s_eq_closed_k_ge_3": "LEMMA",
            "named_gp_s_eq_closed_k_ge_3": "LEMMA",
            "named_pg_l_eq_closed_k_ge_3": "LEMMA",
            "named_gp_l_eq_closed_k_ge_3": "LEMMA",
            "named_pg_s_shift0_at_k3": "KILLED",
            "named_pg_l_shift0_at_k3": "KILLED",
            "named_pg_s_form_at_k2": "KILLED",
            "named_pg_l_form_at_k2": "KILLED",
            "named_pg_s_without_pow_at_k8": "KILLED",
            "named_pg_s_without_sign_at_k8": "KILLED",
            "named_gp_s_without_minus2_at_k8": "KILLED",
            "named_gp_s_without_5pow_at_k8": "KILLED",
            "named_pg_l_without_pow_at_k8": "KILLED",
            "named_pg_l_without_sign_at_k8": "KILLED",
            "named_gp_l_without_3_at_k8": "KILLED",
            "named_gp_l_without_pow_at_k8": "KILLED",
            "named_pg_s_eq_named_s": "KILLED",
            "named_pg_s_eq_2J": "KILLED",
            "named_pg_s_eq_named_gp_s": "KILLED",
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
        dump["named_4w_fold"]["rows"]["8"]["pg_s"],
        dump["named_4w_fold"]["rows"]["8"]["gp_s"],
        dump["named_4w_fold"]["rows"]["8"]["pg_l"],
        dump["named_4w_fold"]["rows"]["8"]["gp_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
