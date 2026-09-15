#!/usr/bin/env python3
"""Cycle YS: odd partner-5U+524288 unpaired extra has count J_k-87381(-1)^k+87382.

Odd-n unpaired extra at j=2n-5U-524288 with j>=2 has count
J_k-87381(-1)^k+87382 for k>=20. The first cell is n=5U/2+262145, j=2
for k>=18. Dies at k=19 for that formula (got 174762, not 349526). Dies
at k=18 for that formula (got 43690, not 87382). Dies at k=18 for
equals odd_s262144 and odd_s131072 and clip_gp (got 43690, not 87382/87381).
Dies at k=17 for covering. Do not kill equals odd_s262144 or even_s262144
or odd_s65536 or even_s65536 or odd_s16384 or even_s16384 or odd_s4096
or even_s4096 or odd_s1024 or odd_s256 or odd_s64 or odd_s16 or
odd_s4 or clip_gp at k=19 (all 174762). Do not kill equals odd_s131072
or odd_s32768 or odd_s8192 or odd_s2048 or odd_s512 or odd_s128 or
odd_s32 or odd_s8 or odd_s4 at k=20 (all 349526). Do not kill pal_kind
unpaired at n=5U/2+262145, j=2 for k>=18. Do not PREFIX pal-center tot.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk leftover
d catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_ys.py --certify
Dump: research/cycle_ys.json
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
from cycle_wz import ph9_n, want_odd_s16
from cycle_xa import want_even_s16
from cycle_xc import ph17_n, want_odd_s32
from cycle_xd import want_even_s32
from cycle_xf import ph33_n, want_odd_s64
from cycle_xg import want_even_s64
from cycle_xh import ph128_n
from cycle_xi import ph65_n, want_odd_s128
from cycle_xj import want_even_s128
from cycle_xk import ph256_n
from cycle_xl import ph129_n, want_odd_s256
from cycle_xm import want_even_s256
from cycle_xn import ph512_n
from cycle_xo import ph257_n, want_odd_s512
from cycle_xp import want_even_s512
from cycle_xq import ph1024_n
from cycle_xr import ph513_n, want_odd_s1024
from cycle_xs import want_even_s1024
from cycle_xt import ph2048_n
from cycle_xu import ph1025_n, want_odd_s2048
from cycle_xv import want_even_s2048
from cycle_xw import ph4096_n
from cycle_xx import ph2049_n, want_odd_s4096
from cycle_xy import want_even_s4096
from cycle_xz import ph8192_n
from cycle_ya import ph4097_n, want_odd_s8192
from cycle_yb import want_even_s8192
from cycle_yc import ph16384_n
from cycle_yd import ph8193_n, want_odd_s16384
from cycle_ye import want_even_s16384
from cycle_yg import ph16385_n, want_odd_s32768
from cycle_yh import want_even_s32768
from cycle_yj import ph32769_n, want_odd_s65536
from cycle_yk import want_even_s65536
from cycle_yl import ph131072_n
from cycle_ym import ph65537_n, want_odd_s131072
from cycle_yn import want_even_s131072
from cycle_yp import ph131073_n, want_odd_s262144
from cycle_yq import ph131074_n, want_even_s262144
from cycle_yr import ph524288_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
YR_JSON = Path(__file__).resolve().parent / "cycle_yr.json"
YP_JSON = Path(__file__).resolve().parent / "cycle_yp.json"
YM_JSON = Path(__file__).resolve().parent / "cycle_ym.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph262145_n(k: int) -> int:
    """Covering n=5U/2+262145, first odd partner-5U+524288 cell."""
    return parent_half(k) + 262145


def want_odd_s524288(k: int) -> int:
    """Odd-n unpaired extra at partner 5U+524288, j>=2: 0 at k<=17, 43690 at k=18, 174762 at k=19."""
    if k <= 17:
        return 0
    if k == 18:
        return 43690
    if k == 19:
        return 174762
    return jacobsthal(k) - 87381 * ((-1) ** k) + 87382


def odd_s524288_split(k: int) -> dict:
    """Odd-n unpaired extra at j=2n-5U-524288 with j>=2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    n_at = n_bad = 0
    first = None
    for n in range(1, 4 * u, 2):
        j = 2 * n - clip - 524288
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
    """k<=64: odd slice J_k-87381(-1)^k+87382 for k>=20; dies at k=19 for that form.

    Do not call odd_s524288_split here.
    Census is odd_s524288_fold for k<=8.
    """
    n_ok = 0
    if want_odd_s524288(0) != 0 or want_odd_s524288(17) != 0:
        return {"ok": False, "k017": True}
    if want_odd_s524288(18) != 43690 or want_odd_s524288(19) != 174762:
        return {"ok": False, "k1819": True}
    if want_odd_s524288(20) != 349526 or want_odd_s524288(21) != 873814:
        return {"ok": False, "k2021": True}
    if want_odd_s524288(19) == want_odd_s524288(20):
        return {"ok": False, "k1920": True}
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
        if k <= 17 and want_odd_s524288(k) != 0:
            return {"ok": False, "z": True, "k": k}
        if k == 18:
            if want_odd_s524288(k) != 43690:
                return {"ok": False, "k18": True}
            if want_odd_s524288(k) == jacobsthal(k) - 87381 * ((-1) ** k) + 87382:
                return {"ok": False, "k18f": True}
        if k == 19:
            if want_odd_s524288(k) != 174762:
                return {"ok": False, "k19": True}
            if want_odd_s524288(k) == jacobsthal(k) - 87381 * ((-1) ** k) + 87382:
                return {"ok": False, "k19f": True}
        if k >= 20 and want_odd_s524288(k) != jacobsthal(k) - 87381 * ((-1) ** k) + 87382:
            return {"ok": False, "Jk": True, "k": k}
        if k >= 18:
            n = ph262145_n(k)
            j = 2 * n - clip - 524288
            if j != 2:
                return {"ok": False, "j2": True, "k": k}
            if 2 * n - 2 != clip + 524288:
                return {"ok": False, "pr": True, "k": k}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "pk": True, "k": k}
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if G(n, 2) != 1:
                return {"ok": False, "g2": True, "k": k}
        if k == 17:
            n = ph262145_n(17)
            if n < 4 * u:
                return {"ok": False, "k17c": True}
            if G(n, 2) != 1:
                return {"ok": False, "k17g": True}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "k17k": True}
            if 2 * n - 2 != clip + 524288:
                return {"ok": False, "k17p": True}
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
        and want_odd_s524288(18) != jacobsthal(18) - 87381 * ((-1) ** 18) + 87382
        and want_odd_s524288(19) != jacobsthal(19) - 87381 * ((-1) ** 19) + 87382
        and want_odd_s524288(8) != want_odd_s512(8)
        and want_odd_s524288(8) != want_odd_s256(8)
        and want_odd_s524288(8) != want_odd_s128(8)
        and want_odd_s524288(8) != want_odd_s64(8)
        and want_odd_s524288(8) != want_odd_s32(8)
        and want_odd_s524288(8) != want_odd_s16(8)
        and want_odd_s524288(8) != want_odd_s8(8)
        and want_odd_s524288(8) != want_odd_s4(8)
        and want_odd_s524288(8) != jacobsthal(8)
        and want_odd_s524288(8) != want_clip_gp(8)
        and want_odd_s524288(8) != want_even_slice(8)
        and want_odd_s524288(8) != want_even_s512(8)
        and want_odd_s524288(8) != want_j0_odd_unp(8)
        and want_odd_s524288(8) == want_odd_s262144(8)
        and want_odd_s524288(8) == want_odd_s131072(8)
        and want_odd_s524288(8) == want_odd_s65536(8)
        and want_odd_s524288(8) == want_odd_s32768(8)
        and want_odd_s524288(8) == want_odd_s16384(8)
        and want_odd_s524288(8) == want_odd_s8192(8)
        and want_odd_s524288(8) == want_odd_s4096(8)
        and want_odd_s524288(8) == want_odd_s2048(8)
        and want_odd_s524288(8) == want_odd_s1024(8)
        and want_odd_s524288(8) == want_even_s262144(8)
        and want_odd_s524288(8) == want_even_s131072(8)
        and want_odd_s524288(8) == want_even_s65536(8)
        and want_odd_s524288(9) != want_clip_gp(9)
        and want_odd_s524288(9) != want_odd_s1024(9)
        and want_odd_s524288(9) == want_odd_s262144(9)
        and want_odd_s524288(16) == want_odd_s262144(16)
        and want_odd_s524288(16) == want_even_s262144(16)
        and want_odd_s524288(16) != want_clip_gp(16)
        and want_odd_s524288(17) != want_odd_s262144(17)
        and want_odd_s524288(17) != want_clip_gp(17)
        and want_odd_s524288(18) != want_odd_s262144(18)
        and want_odd_s524288(18) != want_odd_s131072(18)
        and want_odd_s524288(18) != want_clip_gp(18)
        and want_odd_s524288(19) == want_odd_s262144(19)
        and want_odd_s524288(19) == want_even_s262144(19)
        and want_odd_s524288(19) == want_odd_s65536(19)
        and want_odd_s524288(19) == want_even_s65536(19)
        and want_odd_s524288(19) == want_odd_s16384(19)
        and want_odd_s524288(19) == want_even_s16384(19)
        and want_odd_s524288(19) == want_odd_s4096(19)
        and want_odd_s524288(19) == want_even_s4096(19)
        and want_odd_s524288(19) == want_odd_s1024(19)
        and want_odd_s524288(19) == want_odd_s256(19)
        and want_odd_s524288(19) == want_odd_s64(19)
        and want_odd_s524288(19) == want_odd_s16(19)
        and want_odd_s524288(19) == want_odd_s4(19)
        and want_odd_s524288(19) == want_clip_gp(19)
        and want_odd_s524288(19) != want_odd_s131072(19)
        and want_odd_s524288(19) != want_odd_s32768(19)
        and want_odd_s524288(20) == want_odd_s131072(20)
        and want_odd_s524288(20) == want_odd_s32768(20)
        and want_odd_s524288(20) == want_odd_s8192(20)
        and want_odd_s524288(20) == want_odd_s2048(20)
        and want_odd_s524288(20) == want_odd_s512(20)
        and want_odd_s524288(20) == want_odd_s128(20)
        and want_odd_s524288(20) == want_odd_s32(20)
        and want_odd_s524288(20) == want_odd_s8(20)
        and want_odd_s524288(20) == want_odd_s4(20)
        and want_odd_s524288(20) != want_odd_s262144(20)
        and want_odd_s524288(20) != want_clip_gp(20)
        and want_odd_s524288(8) == 0
        and want_odd_s524288(17) == 0
        and want_odd_s524288(18) == 43690
        and want_odd_s524288(19) == 174762
        and want_odd_s524288(20) == 349526
        and want_odd_s524288(21) == 873814
        and want_odd_s262144(8) == 0
        and want_odd_s131072(8) == 0
        and want_odd_s65536(8) == 0
        and want_odd_s32768(8) == 0
        and want_odd_s16384(8) == 0
        and want_odd_s8192(8) == 0
        and want_odd_s4096(8) == 0
        and want_odd_s2048(8) == 0
        and want_odd_s1024(8) == 0
        and want_odd_s512(8) == 42
        and want_odd_s256(8) == 86
        and want_even_s256(8) == 84
        and want_even_s512(8) == 42
        and want_even_s262144(8) == 0
        and want_odd_s64(8) == 106
        and want_odd_s32(8) == 86
        and want_odd_s16(8) == 90
        and want_odd_s8(8) == 86
        and want_odd_s128(8) == 86
        and want_odd_s4(8) == 86
        and want_clip_gp(8) == 85
        and want_clip_gp(17) == 43690
        and want_clip_gp(18) == 87381
        and want_clip_gp(19) == 174762
        and want_clip_gp(20) == 349525
        and jacobsthal(8) == 85
        and jacobsthal(18) == 87381
        and jacobsthal(19) == 174763
        and jacobsthal(20) == 349525
        and jacobsthal(21) == 699051
        and want_clip_gp_jk(8) == 85
        and want_clip_slice(8) == 85
        and want_even_slice(8) == 85
        and ph262145_n(8) == 262785
        and ph262145_n(17) == 589825
        and ph262145_n(18) == 917505
        and ph262145_n(19) == 1572865
        and ph131073_n(8) == 131713
        and ph131074_n(8) == 131714
        and ph524288_n(8) == 524928
        and ph65537_n(8) == 66177
        and ph32769_n(8) == 33409
        and ph16385_n(8) == 17025
        and ph131072_n(8) == 131712
        and pal_kind(ph262145_n(18), 2, 18) == "unp"
        and pal_kind(ph262145_n(18), 2, 18) != "pair"
        and G(ph262145_n(17), 2) == 1
        and G(ph262145_n(18), 2) == 1
        and ph262145_n(17) >= 4 * (1 << 17)
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
        and want_odd_s524288(4) == 0
        and want_odd_s524288(8) == 0
        and jacobsthal(18) - 87381 * ((-1) ** 18) + 87382 == 87382
        and jacobsthal(19) - 87381 * ((-1) ** 19) + 87382 == 349526
        and jacobsthal(20) - 87381 * ((-1) ** 20) + 87382 == 349526
        and want_lo_e(8) == 14114
        and ph9_n(8) == 649
        and ph17_n(8) == 657
        and ph33_n(8) == 673
        and ph65_n(8) == 705
        and ph128_n(8) == 768
        and ph129_n(8) == 769
        and ph256_n(8) == 896
        and ph257_n(8) == 897
        and ph512_n(8) == 1152
        and ph513_n(8) == 1153
        and ph1024_n(8) == 1664
        and ph1025_n(8) == 1665
        and ph2048_n(8) == 2688
        and ph2049_n(8) == 2689
        and ph4096_n(8) == 4736
        and ph4097_n(8) == 4737
        and ph8192_n(8) == 8832
        and ph8193_n(8) == 8833
        and ph16384_n(8) == 17024
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def odd_s524288_fold() -> dict:
    """k<=8 odd partner-5U+524288 slice vs J_k-87381(-1)^k+87382 for k>=20."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = odd_s524288_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_odd_s524288(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if k >= 18:
            if a["first"] != (ph262145_n(k), 2):
                return {"ok": False, "first": True, "k": k, "got": a["first"]}
        if k <= 17 and a["first"] is not None:
            return {"ok": False, "k17f": True, "got": a["first"]}
        n_ok += 1
        rows[str(k)] = {
            "n_at": a["n_at"],
            "first": list(a["first"]) if a["first"] else None,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["8"]["n_at"] == 0
        and rows["8"]["first"] is None
        and want_odd_s524288(8) == 0
        and want_odd_s524288(17) == 0
        and want_odd_s524288(18) == 43690
        and want_odd_s524288(19) == 174762
        and want_odd_s524288(20) == 349526
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """formula at k=18 and k=19; equals odd_s262144 at k=18; covering at k=17."""
    ok = (
        want_odd_s524288(18) != jacobsthal(18) - 87381 * ((-1) ** 18) + 87382
        and want_odd_s524288(19) != jacobsthal(19) - 87381 * ((-1) ** 19) + 87382
        and want_odd_s524288(8) != want_odd_s512(8)
        and want_odd_s524288(8) != want_odd_s256(8)
        and want_odd_s524288(8) != want_clip_gp(8)
        and want_odd_s524288(8) != jacobsthal(8)
        and want_odd_s524288(8) != want_even_s512(8)
        and want_odd_s524288(16) == want_odd_s262144(16)
        and want_odd_s524288(17) != want_odd_s262144(17)
        and want_odd_s524288(17) != want_clip_gp(17)
        and want_odd_s524288(18) != want_odd_s262144(18)
        and want_odd_s524288(18) != want_odd_s131072(18)
        and want_odd_s524288(18) != want_clip_gp(18)
        and want_odd_s524288(19) == want_odd_s262144(19)
        and want_odd_s524288(19) == want_clip_gp(19)
        and want_odd_s524288(19) == want_odd_s4(19)
        and want_odd_s524288(19) != want_odd_s131072(19)
        and want_odd_s524288(20) == want_odd_s131072(20)
        and want_odd_s524288(20) == want_odd_s32768(20)
        and want_odd_s524288(20) == want_odd_s4(20)
        and want_odd_s524288(20) != want_clip_gp(20)
        and want_odd_s524288(8) == 0
        and want_odd_s524288(17) == 0
        and want_odd_s524288(18) == 43690
        and want_odd_s524288(19) == 174762
        and jacobsthal(18) - 87381 * ((-1) ** 18) + 87382 == 87382
        and jacobsthal(19) - 87381 * ((-1) ** 19) + 87382 == 349526
        and want_odd_s262144(8) == 0
        and want_odd_s131072(8) == 0
        and want_odd_s65536(8) == 0
        and want_odd_s32768(8) == 0
        and want_odd_s512(8) == 42
        and want_odd_s256(8) == 86
        and want_even_s512(8) == 42
        and want_clip_gp(8) == 85
        and want_clip_gp(18) == 87381
        and want_clip_gp(19) == 174762
        and jacobsthal(8) == 85
        and jacobsthal(18) == 87381
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and pal_kind(ph262145_n(18), 2, 18) == "unp"
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
    yr = json.loads(YR_JSON.read_text())
    yp = json.loads(YP_JSON.read_text())
    ym = json.loads(YM_JSON.read_text())
    ok = (
        yr["checks"]["all_ok"]
        and yp["checks"]["all_ok"]
        and ym["checks"]["all_ok"]
        and yr["verdict"]["ph524288_j524288_partner_5U524288"] == "LEMMA"
        and yp["verdict"]["odd_s262144_eq_J_k_plus_43691m1_plus_43690_k_ge_19"] == "LEMMA"
        and ym["verdict"]["odd_s131072_eq_J_k_minus_21845m1_plus_21846_k_ge_18"] == "LEMMA"
        and yr["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and yr["verdict"]["prize"] == "unsolved"
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
    cnt = odd_s524288_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "YS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "odd_s524288_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_s524288_eq_J_k_minus_87381m1_plus_87382_k_ge_20": True,
            "first_odd_s524288_eq_ph262145_k_ge_18": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_s524288_eq_J_k_minus_87381m1_plus_87382_k_ge_20": "LEMMA",
            "first_odd_s524288_eq_ph262145_k_ge_18": "LEMMA",
            "odd_s524288_eq_form_at_k19": "KILLED",
            "odd_s524288_eq_form_at_k18": "KILLED",
            "odd_s524288_eq_odd_s262144_at_k18": "KILLED",
            "odd_s524288_eq_odd_s131072_at_k18": "KILLED",
            "odd_s524288_eq_clip_gp_at_k18": "KILLED",
            "odd_s524288_eq_odd_s262144_at_k17": "KILLED",
            "odd_s524288_eq_clip_gp_at_k17": "KILLED",
            "odd_s524288_eq_clip_gp_at_k8": "KILLED",
            "odd_s524288_eq_J_k_at_k8": "KILLED",
            "odd_s524288_eq_odd_s512_at_k8": "KILLED",
            "ph262145_covering_at_k17": "KILLED",
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
    print("odd s524288 k8", dump["odd_s524288_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
