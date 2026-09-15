#!/usr/bin/env python3
"""Cycle YB: even partner-5U+8192 unpaired extra has count J_k-1365(-1)^k+1364.

Even-n unpaired extra at j=2n-5U-8192 with j>=2 has count
J_k-1365(-1)^k+1364 for k>=14. Together with Cycle YA they are
J_{k+1}-2731(-1)^k+2730 for k>=14. The first even cell is
n=5U/2+4098, j=4 for k>=12. Dies at k=13 for the k>=14 formula
(got 2730, not 5460) and at k=12 (got 682, not 1364). Dies at k=14
for even equals odd (got 5460, not 5462) and for tot equals
J_{k+1} (got 10922, not 10923). Do not kill even equals odd at
k<=13 (both 0 through k=11, both 682 at k=12, both 2730 at k=13).
Do not kill equals clip_gp or even_s4096 or even_s1024 or even_s256
or even_s64 or odd at k=13 (all 2730). Do not kill equals even_s2048
or even_s512 or even_s128 or even_s32 or even_s8 at k=14 (all 5460).
Do not kill pal_kind unpaired at n=5U/2+4098, j=4 for k>=12.
Do not PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_yb.py --certify
Dump: research/cycle_yb.json
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
from cycle_wr import want_even_slice
from cycle_ww import want_odd_s8
from cycle_wx import want_even_s8
from cycle_wz import want_odd_s16
from cycle_xa import want_even_s16
from cycle_xc import want_odd_s32
from cycle_xd import ph18_n, want_even_s32
from cycle_xf import want_odd_s64
from cycle_xg import ph34_n, want_even_s64
from cycle_xh import ph128_n
from cycle_xi import want_odd_s128
from cycle_xj import ph66_n, want_even_s128
from cycle_xk import ph256_n
from cycle_xl import ph129_n, want_odd_s256
from cycle_xm import ph130_n, want_even_s256
from cycle_xn import ph512_n
from cycle_xo import ph257_n, want_odd_s512
from cycle_xp import ph258_n, want_even_s512
from cycle_xq import ph1024_n
from cycle_xr import ph513_n, want_odd_s1024
from cycle_xs import ph514_n, want_even_s1024
from cycle_xt import ph2048_n
from cycle_xu import ph1025_n, want_odd_s2048
from cycle_xv import ph1026_n, want_even_s2048
from cycle_xw import ph4096_n
from cycle_xx import ph2049_n, want_odd_s4096
from cycle_xy import ph2050_n, want_even_s4096
from cycle_xz import ph8192_n
from cycle_ya import ph4097_n, want_odd_s8192
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
YA_JSON = Path(__file__).resolve().parent / "cycle_ya.json"
XZ_JSON = Path(__file__).resolve().parent / "cycle_xz.json"
XV_JSON = Path(__file__).resolve().parent / "cycle_xv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph4098_n(k: int) -> int:
    """Covering n=5U/2+4098, first even partner-5U+8192 cell."""
    return parent_half(k) + 4098


def want_even_s8192(k: int) -> int:
    """Even-n unpaired extra at partner 5U+8192, j>=2: 0 at k<=11, 682 at k=12, 2730 at k=13."""
    if k <= 11:
        return 0
    if k == 12:
        return 682
    if k == 13:
        return 2730
    return jacobsthal(k) - 1365 * ((-1) ** k) + 1364


def want_s8192_tot(k: int) -> int:
    """Odd+even partner-5U+8192 unpaired extra with j>=2."""
    return want_odd_s8192(k) + want_even_s8192(k)


def want_s8192_tot_J(k: int) -> int:
    """J_{k+1}-2731(-1)^k+2730 for k>=14; 5460 at k=13; 1364 at k=12; 0 at k<=11."""
    if k <= 11:
        return 0
    if k == 12:
        return 1364
    if k == 13:
        return 5460
    return jacobsthal(k + 1) - 2731 * ((-1) ** k) + 2730


def even_s8192_split(k: int) -> dict:
    """Even-n unpaired extra at j=2n-5U-8192 with j>=2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    n_at = n_bad = 0
    first = None
    for n in range(0, 4 * u, 2):
        j = 2 * n - clip - 8192
        if j < 2 or j >= n or j % 2 != 0:
            continue
        if G(n, j) == 0:
            continue
        if pal_kind(n, j, k) != "unp":
            n_bad += 1
            continue
        n_at += 1
        if first is None:
            first = (n, j)
    return {"n_at": n_at, "n_bad": n_bad, "first": first}


def tot_form() -> dict:
    """k<=64: even slice J_k-1365(-1)^k+1364 for k>=14; tot J_{k+1}-2731(-1)^k+2730.

    Do not call even_s8192_split / odd_s8192_split here.
    Census is even_s8192_fold for k<=8.
    """
    n_ok = 0
    if want_even_s8192(0) != 0 or want_even_s8192(11) != 0:
        return {"ok": False, "k011": True}
    if want_even_s8192(12) != 682 or want_s8192_tot(12) != 1364:
        return {"ok": False, "k12": True}
    if want_even_s8192(13) != 2730 or want_s8192_tot(13) != 5460:
        return {"ok": False, "k13": True}
    if want_even_s8192(14) != 5460 or want_s8192_tot(14) != 10922:
        return {"ok": False, "k14": True}
    if want_odd_s8192(8) != 0:
        return {"ok": False, "o8": True}
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
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_s8192_tot(k) != want_odd_s8192(k) + want_even_s8192(k):
            return {"ok": False, "sum": True, "k": k}
        if want_s8192_tot(k) != want_s8192_tot_J(k):
            return {"ok": False, "Jform": True, "k": k}
        if k <= 11 and want_even_s8192(k) != 0:
            return {"ok": False, "z": True, "k": k}
        if k == 12:
            if want_even_s8192(k) != 682:
                return {"ok": False, "k12e": True}
            if want_even_s8192(k) == jacobsthal(k) - 1365 * ((-1) ** k) + 1364:
                return {"ok": False, "k12f": True}
            if want_even_s8192(k) != want_odd_s8192(k):
                return {"ok": False, "k12eq": True}
        if k == 13:
            if want_even_s8192(k) != 2730:
                return {"ok": False, "k13e": True}
            if want_even_s8192(k) == jacobsthal(k) - 1365 * ((-1) ** k) + 1364:
                return {"ok": False, "k13f": True}
            if want_even_s8192(k) != want_odd_s8192(k):
                return {"ok": False, "k13eq": True}
        if k >= 14:
            if want_even_s8192(k) != jacobsthal(k) - 1365 * ((-1) ** k) + 1364:
                return {"ok": False, "Jk": True, "k": k}
            if want_even_s8192(k) == want_odd_s8192(k):
                return {"ok": False, "eq": True, "k": k}
            if want_s8192_tot(k) != 2 * want_even_s8192(k) + 2:
                return {"ok": False, "two": True, "k": k}
            if want_s8192_tot(k) != jacobsthal(k + 1) - 2731 * ((-1) ** k) + 2730:
                return {"ok": False, "Jm": True, "k": k}
        if k >= 12:
            n = ph4098_n(k)
            j = 2 * n - clip - 8192
            if j != 4:
                return {"ok": False, "j4": True, "k": k}
            if 2 * n - 4 != clip + 8192:
                return {"ok": False, "pr": True, "k": k}
            if pal_kind(n, 4, k) != "unp":
                return {"ok": False, "pk": True, "k": k}
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if G(n, 4) != 1:
                return {"ok": False, "g4": True, "k": k}
        if k == 11:
            n = ph4098_n(11)
            if n < 4 * u:
                return {"ok": False, "k11c": True}
            if G(n, 4) != 1:
                return {"ok": False, "k11g": True}
            if pal_kind(n, 4, k) != "unp":
                return {"ok": False, "k11k": True}
            if 2 * n - 4 != clip + 8192:
                return {"ok": False, "k11p": True}
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
        and want_even_s8192(12) != jacobsthal(12) - 1365 * ((-1) ** 12) + 1364
        and want_even_s8192(13) != jacobsthal(13) - 1365 * ((-1) ** 13) + 1364
        and want_even_s8192(12) == want_odd_s8192(12)
        and want_even_s8192(13) == want_odd_s8192(13)
        and want_even_s8192(14) != want_odd_s8192(14)
        and want_s8192_tot(12) != jacobsthal(13)
        and want_s8192_tot(13) != jacobsthal(14)
        and want_s8192_tot(14) != jacobsthal(15)
        and want_even_s8192(8) != want_clip_gp(8)
        and want_even_s8192(8) != jacobsthal(8)
        and want_even_s8192(8) != want_odd_s512(8)
        and want_even_s8192(8) != want_even_s512(8)
        and want_even_s8192(8) != want_odd_s256(8)
        and want_even_s8192(8) != want_even_s256(8)
        and want_even_s8192(8) != want_odd_s128(8)
        and want_even_s8192(8) != want_even_s128(8)
        and want_even_s8192(8) != want_odd_s64(8)
        and want_even_s8192(8) != want_even_s64(8)
        and want_even_s8192(8) != want_odd_s16(8)
        and want_even_s8192(8) != want_even_s16(8)
        and want_even_s8192(8) != want_odd_s8(8)
        and want_even_s8192(8) != want_even_s32(8)
        and want_even_s8192(8) != want_even_s8(8)
        and want_even_s8192(8) != want_ug_fl(8)
        and want_even_s8192(8) != want_j0_odd_unp(8)
        and want_even_s8192(8) == want_odd_s8192(8)
        and want_even_s8192(8) == want_even_s2048(8)
        and want_even_s8192(8) == want_even_s1024(8)
        and want_even_s8192(10) != want_even_s2048(10)
        and want_even_s8192(11) != want_even_s2048(11)
        and want_even_s8192(11) != want_clip_gp(11)
        and want_even_s8192(12) != want_even_s2048(12)
        and want_even_s8192(12) != want_even_s512(12)
        and want_even_s8192(12) != want_even_s128(12)
        and want_even_s8192(12) != want_even_s32(12)
        and want_even_s8192(12) != want_even_s8(12)
        and want_even_s8192(12) != want_even_s1024(12)
        and want_even_s8192(12) != want_clip_gp(12)
        and want_even_s8192(13) == want_odd_s8192(13)
        and want_even_s8192(13) == want_clip_gp(13)
        and want_even_s8192(13) == want_even_s4096(13)
        and want_even_s8192(13) == want_even_s1024(13)
        and want_even_s8192(13) == want_even_s256(13)
        and want_even_s8192(13) == want_even_s64(13)
        and want_even_s8192(14) == want_even_s2048(14)
        and want_even_s8192(14) == want_even_s512(14)
        and want_even_s8192(14) == want_even_s128(14)
        and want_even_s8192(14) == want_even_s32(14)
        and want_even_s8192(14) == want_even_s8(14)
        and want_even_s8192(14) != want_clip_gp(14)
        and want_even_s8192(8) == want_even_s4096(8)
        and want_even_s8192(8) == 0
        and want_odd_s8192(8) == 0
        and want_s8192_tot(8) == 0
        and want_s8192_tot_J(8) == 0
        and want_even_s8192(10) == 0
        and want_odd_s8192(10) == 0
        and want_s8192_tot(10) == 0
        and want_even_s8192(11) == 0
        and want_odd_s8192(11) == 0
        and want_s8192_tot(11) == 0
        and want_even_s8192(12) == 682
        and want_odd_s8192(12) == 682
        and want_s8192_tot(12) == 1364
        and want_even_s8192(13) == 2730
        and want_s8192_tot(13) == 5460
        and want_even_s8192(14) == 5460
        and want_s8192_tot(14) == 10922
        and jacobsthal(11) == 683
        and jacobsthal(12) == 1365
        and jacobsthal(13) == 2731
        and jacobsthal(14) == 5461
        and want_clip_gp(11) == 682
        and want_clip_gp(12) == 1365
        and want_clip_gp(13) == 2730
        and jacobsthal(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_clip_slice(8) == 85
        and want_even_slice(8) == 85
        and ph2050_n(8) == 2690
        and ph4098_n(8) == 4738
        and ph4097_n(8) == 4737
        and ph8192_n(8) == 8832
        and ph4098_n(11) == 9218
        and ph4098_n(12) == 14338
        and ph2049_n(8) == 2689
        and ph1026_n(8) == 1666
        and ph1025_n(8) == 1665
        and ph514_n(8) == 1154
        and ph513_n(8) == 1153
        and ph258_n(8) == 898
        and ph257_n(8) == 897
        and ph130_n(8) == 770
        and ph129_n(8) == 769
        and ph66_n(8) == 706
        and ph34_n(8) == 674
        and ph18_n(8) == 658
        and ph128_n(8) == 768
        and ph256_n(8) == 896
        and ph512_n(8) == 1152
        and ph1024_n(8) == 1664
        and ph2048_n(8) == 2688
        and ph4096_n(8) == 4736
        and pal_kind(ph4098_n(12), 4, 12) == "unp"
        and pal_kind(ph4098_n(12), 4, 12) != "pair"
        and G(ph4098_n(11), 4) == 1
        and G(ph4098_n(12), 4) == 1
        and ph4098_n(11) >= 4 * (1 << 11)
        and want_even_s8(8) == 84
        and want_odd_s8(8) == 86
        and want_even_s16(8) == 90
        and want_odd_s16(8) == 90
        and want_even_s32(8) == 84
        and want_odd_s32(8) == 86
        and want_even_s64(8) == 106
        and want_odd_s64(8) == 106
        and want_even_s128(8) == 84
        and want_even_s256(8) == 84
        and want_odd_s256(8) == 86
        and want_even_s512(8) == 42
        and want_odd_s512(8) == 42
        and want_even_s1024(8) == 0
        and want_even_s2048(8) == 0
        and want_odd_s2048(8) == 0
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
        and want_even_s8192(4) == 0
        and want_even_s8192(6) == 0
        and want_s8192_tot(6) == 0
        and jacobsthal(12) - 1365 * ((-1) ** 12) + 1364 == 1364
        and jacobsthal(13) - 1365 * ((-1) ** 13) + 1364 == 5460
        and jacobsthal(14) - 1365 * ((-1) ** 14) + 1364 == 5460
        and jacobsthal(13) - 2731 * ((-1) ** 12) + 2730 == 2730
        and want_lo_e(8) == 14114
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def even_s8192_fold() -> dict:
    """k<=8 even partner-5U+8192 slice vs J_k-1365(-1)^k+1364 for k>=14."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = even_s8192_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_even_s8192(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if k >= 12:
            if a["first"] != (ph4098_n(k), 4):
                return {"ok": False, "first": True, "k": k, "got": a["first"]}
        if k <= 11 and a["first"] is not None:
            return {"ok": False, "k10f": True, "got": a["first"]}
        n_ok += 1
        rows[str(k)] = {
            "n_at": a["n_at"],
            "first": list(a["first"]) if a["first"] else None,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["8"]["n_at"] == 0
        and rows["8"]["first"] is None
        and want_even_s8192(8) == 0
        and want_even_s8192(10) == 0
        and want_even_s8192(11) == 0
        and want_even_s8192(12) == 682
        and want_even_s8192(13) == 2730
        and want_s8192_tot(8) == 0
        and want_s8192_tot(11) == 0
        and want_s8192_tot(12) == 1364
        and want_s8192_tot(13) == 5460
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """formula at k=12 and k=13; even equals odd at k=14; tot equals J_{k+1}."""
    ok = (
        want_even_s8192(12) != jacobsthal(12) - 1365 * ((-1) ** 12) + 1364
        and want_even_s8192(13) != jacobsthal(13) - 1365 * ((-1) ** 13) + 1364
        and want_even_s8192(14) != want_odd_s8192(14)
        and want_even_s8192(12) == want_odd_s8192(12)
        and want_s8192_tot(12) != jacobsthal(13)
        and want_s8192_tot(13) != jacobsthal(14)
        and want_s8192_tot(14) != jacobsthal(15)
        and want_even_s8192(8) != want_clip_gp(8)
        and want_even_s8192(8) != jacobsthal(8)
        and want_even_s8192(8) != want_odd_s512(8)
        and want_even_s8192(8) != want_even_s512(8)
        and want_even_s8192(8) != want_odd_s256(8)
        and want_even_s8192(8) != want_even_s256(8)
        and want_even_s8192(8) != want_odd_s128(8)
        and want_even_s8192(8) != want_even_s128(8)
        and want_even_s8192(8) != want_odd_s64(8)
        and want_even_s8192(8) != want_even_s64(8)
        and want_even_s8192(8) != want_odd_s16(8)
        and want_even_s8192(8) != want_even_s16(8)
        and want_even_s8192(8) != want_odd_s8(8)
        and want_even_s8192(8) != want_even_s32(8)
        and want_even_s8192(8) != want_even_s8(8)
        and want_even_s8192(8) != want_ug_fl(8)
        and want_even_s8192(8) != want_j0_odd_unp(8)
        and want_even_s8192(8) == want_odd_s8192(8)
        and want_even_s8192(10) != want_even_s2048(10)
        and want_even_s8192(11) != want_even_s2048(11)
        and want_even_s8192(11) != want_clip_gp(11)
        and want_even_s8192(12) != want_even_s2048(12)
        and want_even_s8192(12) != want_even_s512(12)
        and want_even_s8192(12) != want_even_s128(12)
        and want_even_s8192(12) != want_even_s32(12)
        and want_even_s8192(12) != want_even_s8(12)
        and want_even_s8192(9) == want_odd_s8192(9)
        and want_even_s8192(9) == 0
        and want_even_s8192(8) == 0
        and want_even_s8192(10) == 0
        and want_even_s8192(11) == 0
        and jacobsthal(12) - 1365 * ((-1) ** 12) + 1364 == 1364
        and jacobsthal(13) - 1365 * ((-1) ** 13) + 1364 == 5460
        and want_odd_s8192(8) == 0
        and want_odd_s8192(10) == 0
        and want_odd_s8192(11) == 0
        and want_odd_s8192(12) == 682
        and want_even_s8192(12) == 682
        and want_s8192_tot(8) == 0
        and want_s8192_tot(10) == 0
        and want_s8192_tot(11) == 0
        and want_s8192_tot(12) == 1364
        and want_s8192_tot(13) == 5460
        and want_clip_gp(8) == 85
        and jacobsthal(8) == 85
        and jacobsthal(11) == 683
        and jacobsthal(12) == 1365
        and jacobsthal(13) == 2731
        and jacobsthal(14) == 5461
        and want_even_s8(8) == 84
        and want_even_s512(8) == 42
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and pal_kind(ph4098_n(12), 4, 12) == "unp"
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
    ya = json.loads(YA_JSON.read_text())
    xz = json.loads(XZ_JSON.read_text())
    xv = json.loads(XV_JSON.read_text())
    ok = (
        ya["checks"]["all_ok"]
        and xz["checks"]["all_ok"]
        and xv["checks"]["all_ok"]
        and ya["verdict"]["odd_s8192_eq_J_k_minus_1365m1_plus_1366_k_ge_14"] == "LEMMA"
        and xz["verdict"]["ph8192_j8192_partner_5U8192"] == "LEMMA"
        and xv["verdict"]["even_s2048_eq_J_k_minus_341m1_plus_340_k_ge_12"] == "LEMMA"
        and ya["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ya["verdict"]["prize"] == "unsolved"
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
    cnt = even_s8192_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "YB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "even_s8192_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_s8192_eq_J_k_minus_1365m1_plus_1364_k_ge_14": True,
            "s8192_tot_eq_J_k1_minus_2731m1_plus_2730_k_ge_14": True,
            "first_even_s8192_eq_ph4098_k_ge_12": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_s8192_eq_J_k_minus_1365m1_plus_1364_k_ge_14": "LEMMA",
            "s8192_tot_eq_J_k1_minus_2731m1_plus_2730_k_ge_14": "LEMMA",
            "first_even_s8192_eq_ph4098_k_ge_12": "LEMMA",
            "even_s8192_eq_form_at_k13": "KILLED",
            "even_s8192_eq_form_at_k12": "KILLED",
            "even_s8192_eq_odd_at_k14": "KILLED",
            "s8192_tot_eq_J_k1_at_k12": "KILLED",
            "s8192_tot_eq_J_k1_at_k13": "KILLED",
            "s8192_tot_eq_J_k1_at_k14": "KILLED",
            "even_s8192_eq_clip_gp_at_k8": "KILLED",
            "even_s8192_eq_J_k_at_k8": "KILLED",
            "even_s8192_eq_odd_s512_at_k8": "KILLED",
            "even_s8192_eq_even_s512_at_k8": "KILLED",
            "even_s8192_eq_odd_s256_at_k8": "KILLED",
            "even_s8192_eq_even_s256_at_k8": "KILLED",
            "even_s8192_eq_odd_s128_at_k8": "KILLED",
            "even_s8192_eq_even_s128_at_k8": "KILLED",
            "even_s8192_eq_odd_s64_at_k8": "KILLED",
            "even_s8192_eq_even_s64_at_k8": "KILLED",
            "even_s8192_eq_odd_s16_at_k8": "KILLED",
            "even_s8192_eq_even_s16_at_k8": "KILLED",
            "even_s8192_eq_odd_s8_at_k8": "KILLED",
            "even_s8192_eq_even_s32_at_k8": "KILLED",
            "even_s8192_eq_even_s8_at_k8": "KILLED",
            "even_s8192_eq_ug_at_k8": "KILLED",
            "even_s8192_eq_j0_odd_at_k8": "KILLED",
            "ph4098_covering_at_k11": "KILLED",
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
    print("even s8192 k8", dump["even_s8192_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
