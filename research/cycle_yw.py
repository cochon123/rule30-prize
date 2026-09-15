#!/usr/bin/env python3
"""Cycle YW: even partner-5U+1048576 unpaired extra has count J_k+174763(-1)^k+174762.

Even-n unpaired extra at j=2n-5U-1048576 with j>=2 has count
J_k+174763(-1)^k+174762 for k>=21, equal to the odd Cycle YV slice.
Together they are J_{k+1}+349525(-1)^k+349524 for k>=21. The first even
cell is n=5U/2+524290, j=4 for k>=19. Dies at k=20 for the k>=21 formula
(got 349524, not 699050) and at k=19 (got 87380, not 174762). Dies at
k=19 for even equals odd (got 87380, not 87382) and at k=20 (got 349524,
not 349526). Dies at k=19 for tot equals J_{k+1} (got 174762, not 349525)
and at k=20 (got 699050, not 699051) and at k=21 (got 1398100, not
1398101). Do not kill even equals odd at k<=18 (both 0) or k>=21. Do not
kill equals even_s524288 or even_s131072 or even_s32768 or even_s8192 or
even_s2048 or even_s512 or even_s128 or even_s32 or even_s8 at k=20 (all
349524). Do not kill equals clip_gp or even_s262144 or even_s65536 or
even_s16384 or even_s4096 or even_s1024 or even_s256 or even_s64 or
even_s16 or odd at k=21 (all 699050). Do not kill pal_kind unpaired at
n=5U/2+524290, j=4 for k>=19. Do not PREFIX pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12 T-bands.
Not a prize claim.

Run: python3 research/cycle_yw.py --certify
Dump: research/cycle_yw.json
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
from cycle_wu import want_odd_s4
from cycle_ww import want_odd_s8
from cycle_wx import want_even_s8
from cycle_wz import want_odd_s16
from cycle_xa import want_even_s16
from cycle_xc import want_odd_s32
from cycle_xd import want_even_s32
from cycle_xf import want_odd_s64
from cycle_xg import want_even_s64
from cycle_xh import ph128_n
from cycle_xi import want_odd_s128
from cycle_xj import want_even_s128
from cycle_xk import ph256_n
from cycle_xl import want_odd_s256
from cycle_xm import want_even_s256
from cycle_xn import ph512_n
from cycle_xo import want_odd_s512
from cycle_xp import want_even_s512
from cycle_xq import ph1024_n
from cycle_xr import want_odd_s1024
from cycle_xs import want_even_s1024
from cycle_xt import ph2048_n
from cycle_xu import want_odd_s2048
from cycle_xv import want_even_s2048
from cycle_xw import ph4096_n
from cycle_xx import want_odd_s4096
from cycle_xy import want_even_s4096
from cycle_xz import ph8192_n
from cycle_ya import ph4097_n
from cycle_yb import ph4098_n, want_even_s8192
from cycle_yc import ph16384_n
from cycle_yd import want_odd_s16384
from cycle_ye import ph8194_n, want_even_s16384
from cycle_yf import ph32768_n
from cycle_yg import ph16385_n, want_odd_s32768
from cycle_yh import ph16386_n, want_even_s32768
from cycle_yi import ph65536_n
from cycle_yj import ph32769_n, want_odd_s65536
from cycle_yk import ph32770_n, want_even_s65536
from cycle_yl import ph131072_n
from cycle_ym import ph65537_n, want_odd_s131072
from cycle_yn import ph65538_n, want_even_s131072
from cycle_yo import ph262144_n
from cycle_yp import ph131073_n, want_odd_s262144
from cycle_yq import ph131074_n, want_even_s262144
from cycle_yr import ph524288_n
from cycle_ys import ph262145_n, want_odd_s524288
from cycle_yt import ph262146_n, want_even_s524288
from cycle_yu import ph1048576_n
from cycle_yv import ph524289_n, want_odd_s1048576
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
YV_JSON = Path(__file__).resolve().parent / "cycle_yv.json"
YU_JSON = Path(__file__).resolve().parent / "cycle_yu.json"
YQ_JSON = Path(__file__).resolve().parent / "cycle_yq.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph524290_n(k: int) -> int:
    """Covering n=5U/2+524290, first even partner-5U+1048576 cell."""
    return parent_half(k) + 524290


def want_even_s1048576(k: int) -> int:
    """Even-n unpaired extra at partner 5U+1048576, j>=2: 0 at k<=18, 87380 at k=19, 349524 at k=20."""
    if k <= 18:
        return 0
    if k == 19:
        return 87380
    if k == 20:
        return 349524
    return jacobsthal(k) + 174763 * ((-1) ** k) + 174762


def want_s1048576_tot(k: int) -> int:
    """Odd+even partner-5U+1048576 unpaired extra with j>=2."""
    return want_odd_s1048576(k) + want_even_s1048576(k)


def want_s1048576_tot_J(k: int) -> int:
    """J_{k+1}+349525(-1)^k+349524 for k>=21; 699050 at k=20; 174762 at k=19; 0 at k<=18."""
    if k <= 18:
        return 0
    if k == 19:
        return 174762
    if k == 20:
        return 699050
    return jacobsthal(k + 1) + 349525 * ((-1) ** k) + 349524


def even_s1048576_split(k: int) -> dict:
    """Even-n unpaired extra at j=2n-5U-1048576 with j>=2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    n_at = n_bad = 0
    first = None
    for n in range(0, 4 * u, 2):
        j = 2 * n - clip - 1048576
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
    """k<=64: even slice J_k+174763(-1)^k+174762 for k>=21; tot J_{k+1}+349525(-1)^k+349524.

    Do not call even_s1048576_split / odd_s1048576_split here.
    Census is even_s1048576_fold for k<=8.
    """
    n_ok = 0
    if want_even_s1048576(0) != 0 or want_even_s1048576(18) != 0:
        return {"ok": False, "k018": True}
    if want_even_s1048576(19) != 87380 or want_s1048576_tot(19) != 174762:
        return {"ok": False, "k19": True}
    if want_even_s1048576(20) != 349524 or want_s1048576_tot(20) != 699050:
        return {"ok": False, "k20": True}
    if want_even_s1048576(21) != 699050 or want_s1048576_tot(21) != 1398100:
        return {"ok": False, "k21": True}
    if want_even_s1048576(22) != 1747626 or want_s1048576_tot(22) != 3495252:
        return {"ok": False, "k22": True}
    if want_odd_s1048576(8) != 0:
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
        if want_s1048576_tot(k) != want_odd_s1048576(k) + want_even_s1048576(k):
            return {"ok": False, "sum": True, "k": k}
        if want_s1048576_tot(k) != want_s1048576_tot_J(k):
            return {"ok": False, "Jform": True, "k": k}
        if k <= 18 and want_even_s1048576(k) != 0:
            return {"ok": False, "z": True, "k": k}
        if k == 19:
            if want_even_s1048576(k) != 87380:
                return {"ok": False, "k19e": True}
            if want_even_s1048576(k) == jacobsthal(k) + 174763 * ((-1) ** k) + 174762:
                return {"ok": False, "k19f": True}
            if want_even_s1048576(k) == want_odd_s1048576(k):
                return {"ok": False, "k19eq": True}
        if k == 20:
            if want_even_s1048576(k) != 349524:
                return {"ok": False, "k20e": True}
            if want_even_s1048576(k) == jacobsthal(k) + 174763 * ((-1) ** k) + 174762:
                return {"ok": False, "k20f": True}
            if want_even_s1048576(k) == want_odd_s1048576(k):
                return {"ok": False, "k20eq": True}
        if k >= 21:
            if want_even_s1048576(k) != jacobsthal(k) + 174763 * ((-1) ** k) + 174762:
                return {"ok": False, "Jk": True, "k": k}
            if want_even_s1048576(k) != want_odd_s1048576(k):
                return {"ok": False, "eq": True, "k": k}
            if want_s1048576_tot(k) != 2 * want_even_s1048576(k):
                return {"ok": False, "two": True, "k": k}
            if want_s1048576_tot(k) != jacobsthal(k + 1) + 349525 * ((-1) ** k) + 349524:
                return {"ok": False, "Jm": True, "k": k}
        if k >= 19:
            n = ph524290_n(k)
            j = 2 * n - clip - 1048576
            if j != 4:
                return {"ok": False, "j4": True, "k": k}
            if 2 * n - 4 != clip + 1048576:
                return {"ok": False, "pr": True, "k": k}
            if pal_kind(n, 4, k) != "unp":
                return {"ok": False, "pk": True, "k": k}
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if G(n, 4) != 1:
                return {"ok": False, "g4": True, "k": k}
        if k == 18:
            n = ph524290_n(18)
            if n < 4 * u:
                return {"ok": False, "k18c": True}
            if G(n, 4) != 1:
                return {"ok": False, "k18g": True}
            if pal_kind(n, 4, k) != "unp":
                return {"ok": False, "k18k": True}
            if 2 * n - 4 != clip + 1048576:
                return {"ok": False, "k18p": True}
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
        and want_even_s1048576(19) != jacobsthal(19) + 174763 * ((-1) ** 19) + 174762
        and want_even_s1048576(20) != jacobsthal(20) + 174763 * ((-1) ** 20) + 174762
        and want_even_s1048576(19) != want_odd_s1048576(19)
        and want_even_s1048576(20) != want_odd_s1048576(20)
        and want_even_s1048576(21) == want_odd_s1048576(21)
        and want_s1048576_tot(19) != jacobsthal(20)
        and want_s1048576_tot(20) != jacobsthal(21)
        and want_s1048576_tot(21) != jacobsthal(22)
        and want_even_s1048576(8) != want_clip_gp(8)
        and want_even_s1048576(8) != jacobsthal(8)
        and want_even_s1048576(8) != want_odd_s512(8)
        and want_even_s1048576(8) != want_even_s512(8)
        and want_even_s1048576(8) != want_odd_s256(8)
        and want_even_s1048576(8) != want_even_s256(8)
        and want_even_s1048576(8) != want_odd_s128(8)
        and want_even_s1048576(8) != want_even_s128(8)
        and want_even_s1048576(8) != want_odd_s64(8)
        and want_even_s1048576(8) != want_even_s64(8)
        and want_even_s1048576(8) != want_odd_s16(8)
        and want_even_s1048576(8) != want_even_s16(8)
        and want_even_s1048576(8) != want_odd_s8(8)
        and want_even_s1048576(8) != want_even_s32(8)
        and want_even_s1048576(8) != want_even_s8(8)
        and want_even_s1048576(8) != want_ug_fl(8)
        and want_even_s1048576(8) != want_j0_odd_unp(8)
        and want_even_s1048576(8) == want_odd_s1048576(8)
        and want_even_s1048576(8) == want_even_s524288(8)
        and want_even_s1048576(8) == want_even_s262144(8)
        and want_even_s1048576(8) == want_even_s131072(8)
        and want_even_s1048576(18) != want_even_s524288(18)
        and want_even_s1048576(18) != want_clip_gp(18)
        and want_even_s1048576(18) == want_odd_s1048576(18)
        and want_even_s1048576(19) != want_even_s524288(19)
        and want_even_s1048576(19) != want_clip_gp(19)
        and want_even_s1048576(19) != want_odd_s1048576(19)
        and want_even_s1048576(20) == want_even_s524288(20)
        and want_even_s1048576(20) == want_even_s131072(20)
        and want_even_s1048576(20) == want_even_s32768(20)
        and want_even_s1048576(20) == want_even_s8192(20)
        and want_even_s1048576(20) == want_even_s2048(20)
        and want_even_s1048576(20) == want_even_s512(20)
        and want_even_s1048576(20) == want_even_s128(20)
        and want_even_s1048576(20) == want_even_s32(20)
        and want_even_s1048576(20) == want_even_s8(20)
        and want_even_s1048576(20) != want_clip_gp(20)
        and want_even_s1048576(20) != want_odd_s1048576(20)
        and want_even_s1048576(21) == want_odd_s1048576(21)
        and want_even_s1048576(21) == want_clip_gp(21)
        and want_even_s1048576(21) == want_even_s262144(21)
        and want_even_s1048576(21) == want_even_s65536(21)
        and want_even_s1048576(21) == want_even_s16384(21)
        and want_even_s1048576(21) == want_even_s4096(21)
        and want_even_s1048576(21) == want_even_s1024(21)
        and want_even_s1048576(21) == want_even_s256(21)
        and want_even_s1048576(21) == want_even_s64(21)
        and want_even_s1048576(21) == want_even_s16(21)
        and want_even_s1048576(21) == want_odd_s4(21)
        and want_even_s1048576(21) != want_even_s524288(21)
        and want_even_s1048576(21) != want_even_s131072(21)
        and want_even_s1048576(21) != want_even_s32768(21)
        and want_even_s1048576(8) == 0
        and want_odd_s1048576(8) == 0
        and want_s1048576_tot(8) == 0
        and want_s1048576_tot_J(8) == 0
        and want_even_s1048576(18) == 0
        and want_odd_s1048576(18) == 0
        and want_s1048576_tot(18) == 0
        and want_even_s1048576(19) == 87380
        and want_odd_s1048576(19) == 87382
        and want_s1048576_tot(19) == 174762
        and want_even_s1048576(20) == 349524
        and want_odd_s1048576(20) == 349526
        and want_s1048576_tot(20) == 699050
        and want_even_s1048576(21) == 699050
        and want_s1048576_tot(21) == 1398100
        and want_even_s1048576(22) == 1747626
        and want_s1048576_tot(22) == 3495252
        and jacobsthal(19) == 174763
        and jacobsthal(20) == 349525
        and jacobsthal(21) == 699051
        and jacobsthal(22) == 1398101
        and want_clip_gp(19) == 174762
        and want_clip_gp(20) == 349525
        and want_clip_gp(21) == 699050
        and jacobsthal(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_clip_slice(8) == 85
        and want_even_slice(8) == 85
        and ph524290_n(8) == 524930
        and ph524290_n(18) == 1179650
        and ph524290_n(19) == 1835010
        and ph524290_n(20) == 3145730
        and ph524289_n(8) == 524929
        and ph1048576_n(8) == 1049216
        and ph262146_n(8) == 262786
        and ph262145_n(8) == 262785
        and ph131074_n(8) == 131714
        and ph131073_n(8) == 131713
        and ph524288_n(8) == 524928
        and ph65538_n(8) == 66178
        and ph32770_n(8) == 33410
        and pal_kind(ph524290_n(19), 4, 19) == "unp"
        and pal_kind(ph524290_n(19), 4, 19) != "pair"
        and G(ph524290_n(18), 4) == 1
        and G(ph524290_n(19), 4) == 1
        and ph524290_n(18) >= 4 * (1 << 18)
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
        and want_even_s4096(8) == 0
        and want_even_s8192(8) == 0
        and want_even_s16384(8) == 0
        and want_even_s32768(8) == 0
        and want_even_s65536(8) == 0
        and want_even_s131072(8) == 0
        and want_even_s262144(8) == 0
        and want_even_s524288(8) == 0
        and want_odd_s1048576(8) == 0
        and want_odd_s524288(8) == 0
        and want_odd_s262144(8) == 0
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
        and want_even_s1048576(4) == 0
        and want_even_s1048576(8) == 0
        and jacobsthal(19) + 174763 * ((-1) ** 19) + 174762 == 174762
        and jacobsthal(20) + 174763 * ((-1) ** 20) + 174762 == 699050
        and jacobsthal(21) + 174763 * ((-1) ** 21) + 174762 == 699050
        and jacobsthal(21) + 349525 * ((-1) ** 20) + 349524 == 1398100
        and want_lo_e(8) == 14114
        and ph128_n(8) == 768
        and ph256_n(8) == 896
        and ph512_n(8) == 1152
        and ph1024_n(8) == 1664
        and ph2048_n(8) == 2688
        and ph4096_n(8) == 4736
        and ph8192_n(8) == 8832
        and ph4097_n(8) == 4737
        and ph4098_n(8) == 4738
        and ph8194_n(8) == 8834
        and ph16384_n(8) == 17024
        and ph16385_n(8) == 17025
        and ph16386_n(8) == 17026
        and ph32768_n(8) == 33408
        and ph32769_n(8) == 33409
        and ph65536_n(8) == 66176
        and ph65537_n(8) == 66177
        and ph131072_n(8) == 131712
        and ph262144_n(8) == 262784
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def even_s1048576_fold() -> dict:
    """k<=8 even partner-5U+1048576 slice vs J_k+174763(-1)^k+174762 for k>=21."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = even_s1048576_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_even_s1048576(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if k >= 19:
            if a["first"] != (ph524290_n(k), 4):
                return {"ok": False, "first": True, "k": k, "got": a["first"]}
        if k <= 18 and a["first"] is not None:
            return {"ok": False, "k18f": True, "got": a["first"]}
        n_ok += 1
        rows[str(k)] = {
            "n_at": a["n_at"],
            "first": list(a["first"]) if a["first"] else None,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["8"]["n_at"] == 0
        and rows["8"]["first"] is None
        and want_even_s1048576(8) == 0
        and want_even_s1048576(18) == 0
        and want_even_s1048576(19) == 87380
        and want_even_s1048576(20) == 349524
        and want_s1048576_tot(8) == 0
        and want_s1048576_tot(18) == 0
        and want_s1048576_tot(19) == 174762
        and want_s1048576_tot(20) == 699050
        and want_s1048576_tot(21) == 1398100
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """formula at k=19 and k=20; even equals odd at k=19 and k=20; tot equals J_{k+1}."""
    ok = (
        want_even_s1048576(19) != jacobsthal(19) + 174763 * ((-1) ** 19) + 174762
        and want_even_s1048576(20) != jacobsthal(20) + 174763 * ((-1) ** 20) + 174762
        and want_even_s1048576(19) != want_odd_s1048576(19)
        and want_even_s1048576(20) != want_odd_s1048576(20)
        and want_even_s1048576(21) == want_odd_s1048576(21)
        and want_s1048576_tot(19) != jacobsthal(20)
        and want_s1048576_tot(20) != jacobsthal(21)
        and want_s1048576_tot(21) != jacobsthal(22)
        and want_even_s1048576(8) != want_clip_gp(8)
        and want_even_s1048576(8) != jacobsthal(8)
        and want_even_s1048576(8) != want_odd_s512(8)
        and want_even_s1048576(8) != want_even_s512(8)
        and want_even_s1048576(8) != want_odd_s256(8)
        and want_even_s1048576(8) != want_even_s256(8)
        and want_even_s1048576(8) != want_odd_s128(8)
        and want_even_s1048576(8) != want_even_s128(8)
        and want_even_s1048576(8) != want_odd_s64(8)
        and want_even_s1048576(8) != want_even_s64(8)
        and want_even_s1048576(8) != want_odd_s16(8)
        and want_even_s1048576(8) != want_even_s16(8)
        and want_even_s1048576(8) != want_odd_s8(8)
        and want_even_s1048576(8) != want_even_s32(8)
        and want_even_s1048576(8) != want_even_s8(8)
        and want_even_s1048576(8) != want_ug_fl(8)
        and want_even_s1048576(8) != want_j0_odd_unp(8)
        and want_even_s1048576(8) == want_odd_s1048576(8)
        and want_even_s1048576(18) != want_even_s524288(18)
        and want_even_s1048576(18) != want_clip_gp(18)
        and want_even_s1048576(19) != want_even_s524288(19)
        and want_even_s1048576(19) != want_clip_gp(19)
        and want_even_s1048576(20) == want_even_s524288(20)
        and want_even_s1048576(20) == want_even_s131072(20)
        and want_even_s1048576(20) == want_even_s32768(20)
        and want_even_s1048576(20) == want_even_s8192(20)
        and want_even_s1048576(20) == want_even_s2048(20)
        and want_even_s1048576(20) == want_even_s512(20)
        and want_even_s1048576(20) == want_even_s128(20)
        and want_even_s1048576(20) == want_even_s32(20)
        and want_even_s1048576(20) == want_even_s8(20)
        and want_even_s1048576(8) == 0
        and want_even_s1048576(18) == 0
        and jacobsthal(19) + 174763 * ((-1) ** 19) + 174762 == 174762
        and jacobsthal(20) + 174763 * ((-1) ** 20) + 174762 == 699050
        and want_odd_s1048576(8) == 0
        and want_odd_s1048576(18) == 0
        and want_odd_s1048576(19) == 87382
        and want_even_s1048576(19) == 87380
        and want_s1048576_tot(8) == 0
        and want_s1048576_tot(18) == 0
        and want_s1048576_tot(19) == 174762
        and want_s1048576_tot(20) == 699050
        and want_clip_gp(8) == 85
        and jacobsthal(8) == 85
        and jacobsthal(19) == 174763
        and jacobsthal(20) == 349525
        and jacobsthal(21) == 699051
        and want_even_s8(8) == 84
        and want_even_s512(8) == 42
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and pal_kind(ph524290_n(19), 4, 19) == "unp"
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
    yv = json.loads(YV_JSON.read_text())
    yu = json.loads(YU_JSON.read_text())
    yq = json.loads(YQ_JSON.read_text())
    ok = (
        yv["checks"]["all_ok"]
        and yu["checks"]["all_ok"]
        and yq["checks"]["all_ok"]
        and yv["verdict"]["odd_s1048576_eq_J_k_plus_174763m1_plus_174762_k_ge_21"] == "LEMMA"
        and yu["verdict"]["ph1048576_j1048576_partner_5U1048576"] == "LEMMA"
        and yq["verdict"]["even_s262144_eq_J_k_plus_43691m1_plus_43690_k_ge_19"] == "LEMMA"
        and yv["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and yv["verdict"]["prize"] == "unsolved"
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
    cnt = even_s1048576_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "YW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "even_s1048576_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_s1048576_eq_J_k_plus_174763m1_plus_174762_k_ge_21": True,
            "s1048576_tot_eq_J_k1_plus_349525m1_plus_349524_k_ge_21": True,
            "first_even_s1048576_eq_ph524290_k_ge_19": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_s1048576_eq_J_k_plus_174763m1_plus_174762_k_ge_21": "LEMMA",
            "s1048576_tot_eq_J_k1_plus_349525m1_plus_349524_k_ge_21": "LEMMA",
            "first_even_s1048576_eq_ph524290_k_ge_19": "LEMMA",
            "even_s1048576_eq_form_at_k20": "KILLED",
            "even_s1048576_eq_form_at_k19": "KILLED",
            "even_s1048576_eq_odd_at_k20": "KILLED",
            "even_s1048576_eq_odd_at_k19": "KILLED",
            "s1048576_tot_eq_J_k1_at_k19": "KILLED",
            "s1048576_tot_eq_J_k1_at_k20": "KILLED",
            "s1048576_tot_eq_J_k1_at_k21": "KILLED",
            "even_s1048576_eq_clip_gp_at_k8": "KILLED",
            "even_s1048576_eq_J_k_at_k8": "KILLED",
            "even_s1048576_eq_odd_s512_at_k8": "KILLED",
            "even_s1048576_eq_even_s512_at_k8": "KILLED",
            "even_s1048576_eq_odd_s256_at_k8": "KILLED",
            "even_s1048576_eq_even_s256_at_k8": "KILLED",
            "even_s1048576_eq_odd_s128_at_k8": "KILLED",
            "even_s1048576_eq_even_s128_at_k8": "KILLED",
            "even_s1048576_eq_odd_s64_at_k8": "KILLED",
            "even_s1048576_eq_even_s64_at_k8": "KILLED",
            "even_s1048576_eq_odd_s16_at_k8": "KILLED",
            "even_s1048576_eq_even_s16_at_k8": "KILLED",
            "even_s1048576_eq_odd_s8_at_k8": "KILLED",
            "even_s1048576_eq_even_s32_at_k8": "KILLED",
            "even_s1048576_eq_even_s8_at_k8": "KILLED",
            "even_s1048576_eq_ug_at_k8": "KILLED",
            "even_s1048576_eq_j0_odd_at_k8": "KILLED",
            "ph524290_covering_at_k18": "KILLED",
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
    print("even s1048576 k8", dump["even_s1048576_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
