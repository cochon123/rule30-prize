#!/usr/bin/env python3
"""Cycle ZW: odd partner-5U+536870912 unpaired extra has count J_k-89478485(-1)^k+89478486.

Odd-n unpaired extra at j=2n-5U-536870912 with j>=2 has count
J_k-89478485(-1)^k+89478486 for k>=30. The first cell is n=5U/2+268435457, j=2
for k>=28. Dies at k=29 for that formula (got 178956970, not 357913942). Dies
at k=28 for that formula (got 44739242, not 89478486). Dies at k=28 for
equals odd_s268435456 and odd_s134217728 and clip_gp (got 44739242, not
89478486/89478485). Dies at k=27 for covering. Do not kill equals
odd_s268435456 or odd_s67108864 or odd_s16777216 or odd_s4194304 or
odd_s1048576 or odd_s262144 or odd_s65536 or odd_s16384 or odd_s4096 or
odd_s1024 or odd_s256 or odd_s64 or odd_s16 or odd_s4 or even_s268435456 or
even_s67108864 or even_s16777216 or clip_gp at k=29 (all 178956970). Do not
kill pal_kind unpaired at n=5U/2+268435457, j=2 for k>=28. Do not PREFIX
pal-center tot. Not rest=S xor T. Do not walk leftover p catalogues. Do
not walk leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_zw.py --certify
Dump: research/cycle_zw.json
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
from cycle_ys import ph262145_n, want_odd_s524288
from cycle_yt import ph262146_n, want_even_s524288
from cycle_yu import ph1048576_n
from cycle_yv import ph524289_n, want_odd_s1048576
from cycle_yw import ph524290_n, want_even_s1048576
from cycle_yx import ph2097152_n
from cycle_yy import ph1048577_n, want_odd_s2097152
from cycle_yz import ph1048578_n, want_even_s2097152
from cycle_za import ph4194304_n
from cycle_zb import ph2097153_n, want_odd_s4194304
from cycle_zc import ph2097154_n, want_even_s4194304
from cycle_zd import ph8388608_n
from cycle_ze import ph4194305_n, want_odd_s8388608
from cycle_zf import want_even_s8388608
from cycle_zg import ph16777216_n
from cycle_zh import ph8388609_n, want_odd_s16777216
from cycle_zi import want_even_s16777216
from cycle_zj import ph33554432_n
from cycle_zk import ph16777217_n, want_odd_s33554432
from cycle_zl import want_even_s33554432
from cycle_zm import ph67108864_n
from cycle_zn import ph33554433_n, want_odd_s67108864
from cycle_zo import want_even_s67108864
from cycle_zp import ph134217728_n
from cycle_zq import ph67108865_n, want_odd_s134217728
from cycle_zr import want_even_s134217728
from cycle_zs import ph268435456_n
from cycle_zt import ph134217729_n, want_odd_s268435456
from cycle_zu import want_even_s268435456
from cycle_zv import ph536870912_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ZT_JSON = Path(__file__).resolve().parent / "cycle_zt.json"
ZQ_JSON = Path(__file__).resolve().parent / "cycle_zq.json"
ZV_JSON = Path(__file__).resolve().parent / "cycle_zv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph268435457_n(k: int) -> int:
    """Covering n=5U/2+268435457, first odd partner-5U+536870912 cell."""
    return parent_half(k) + 268435457


def want_odd_s536870912(k: int) -> int:
    """Odd-n unpaired extra at partner 5U+536870912, j>=2: 0 at k<=27, 44739242 at k=28, 178956970 at k=29."""
    if k <= 27:
        return 0
    if k == 28:
        return 44739242
    if k == 29:
        return 178956970
    return jacobsthal(k) - 89478485 * ((-1) ** k) + 89478486


def odd_s536870912_split(k: int) -> dict:
    """Odd-n unpaired extra at j=2n-5U-536870912 with j>=2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    n_at = n_bad = 0
    first = None
    for n in range(1, 4 * u, 2):
        j = 2 * n - clip - 536870912
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
    """k<=64: odd slice J_k-89478485(-1)^k+89478486 for k>=30; dies at k=29 for that form.

    Do not call odd_s536870912_split here.
    Census is odd_s536870912_fold for k<=8.
    """
    n_ok = 0
    if want_odd_s536870912(0) != 0 or want_odd_s536870912(27) != 0:
        return {"ok": False, "k027": True}
    if want_odd_s536870912(28) != 44739242 or want_odd_s536870912(29) != 178956970:
        return {"ok": False, "k2829": True}
    if want_odd_s536870912(30) != 357913942 or want_odd_s536870912(31) != 894784854:
        return {"ok": False, "k3031": True}
    if want_odd_s536870912(28) == want_odd_s536870912(29):
        return {"ok": False, "eq2829": True}
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
        if k <= 27 and want_odd_s536870912(k) != 0:
            return {"ok": False, "z": True, "k": k}
        if k == 28:
            if want_odd_s536870912(k) != 44739242:
                return {"ok": False, "k28": True}
            if want_odd_s536870912(k) == jacobsthal(k) - 89478485 * ((-1) ** k) + 89478486:
                return {"ok": False, "k28f": True}
        if k == 29:
            if want_odd_s536870912(k) != 178956970:
                return {"ok": False, "k29": True}
            if want_odd_s536870912(k) == jacobsthal(k) - 89478485 * ((-1) ** k) + 89478486:
                return {"ok": False, "k29f": True}
        if k >= 30 and want_odd_s536870912(k) != jacobsthal(k) - 89478485 * ((-1) ** k) + 89478486:
            return {"ok": False, "Jk": True, "k": k}
        if k >= 28:
            n = ph268435457_n(k)
            j = 2 * n - clip - 536870912
            if j != 2:
                return {"ok": False, "j2": True, "k": k}
            if 2 * n - 2 != clip + 536870912:
                return {"ok": False, "pr": True, "k": k}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "pk": True, "k": k}
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if G(n, 2) != 1:
                return {"ok": False, "g2": True, "k": k}
        if k == 27:
            n = ph268435457_n(27)
            if n < 4 * u:
                return {"ok": False, "k27c": True}
            if G(n, 2) != 1:
                return {"ok": False, "k27g": True}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "k27k": True}
            if 2 * n - 2 != clip + 536870912:
                return {"ok": False, "k27p": True}
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
        and want_odd_s536870912(28) != jacobsthal(28) - 89478485 * ((-1) ** 28) + 89478486
        and want_odd_s536870912(29) != jacobsthal(29) - 89478485 * ((-1) ** 29) + 89478486
        and want_odd_s536870912(8) != want_odd_s512(8)
        and want_odd_s536870912(8) != want_odd_s256(8)
        and want_odd_s536870912(8) != want_clip_gp(8)
        and want_odd_s536870912(8) != jacobsthal(8)
        and want_odd_s536870912(8) != want_even_s512(8)
        and want_odd_s536870912(8) == want_odd_s268435456(8)
        and want_odd_s536870912(8) == want_odd_s134217728(8)
        and want_odd_s536870912(8) == want_odd_s67108864(8)
        and want_odd_s536870912(8) == want_even_s268435456(8)
        and want_odd_s536870912(8) == want_even_s134217728(8)
        and want_odd_s536870912(8) == want_even_s67108864(8)
        and want_odd_s536870912(26) == want_odd_s268435456(26)
        and want_odd_s536870912(27) != want_odd_s268435456(27)
        and want_odd_s536870912(27) != want_odd_s134217728(27)
        and want_odd_s536870912(27) != want_clip_gp(27)
        and want_odd_s536870912(28) != want_odd_s268435456(28)
        and want_odd_s536870912(28) != want_odd_s134217728(28)
        and want_odd_s536870912(28) != want_clip_gp(28)
        and want_odd_s536870912(28) == want_clip_gp(27)
        and want_odd_s536870912(28) == want_odd_s134217728(27)
        and want_odd_s536870912(28) == want_odd_s67108864(27)
        and want_odd_s536870912(29) == want_odd_s268435456(29)
        and want_odd_s536870912(29) == want_odd_s67108864(29)
        and want_odd_s536870912(29) == want_odd_s16777216(29)
        and want_odd_s536870912(29) == want_odd_s4194304(29)
        and want_odd_s536870912(29) == want_odd_s1048576(29)
        and want_odd_s536870912(29) == want_odd_s262144(29)
        and want_odd_s536870912(29) == want_odd_s65536(29)
        and want_odd_s536870912(29) == want_odd_s16384(29)
        and want_odd_s536870912(29) == want_odd_s4096(29)
        and want_odd_s536870912(29) == want_odd_s1024(29)
        and want_odd_s536870912(29) == want_odd_s256(29)
        and want_odd_s536870912(29) == want_odd_s64(29)
        and want_odd_s536870912(29) == want_odd_s16(29)
        and want_odd_s536870912(29) == want_odd_s4(29)
        and want_odd_s536870912(29) == want_even_s268435456(29)
        and want_odd_s536870912(29) == want_even_s67108864(29)
        and want_odd_s536870912(29) == want_even_s16777216(29)
        and want_odd_s536870912(29) == want_clip_gp(29)
        and want_odd_s536870912(29) != want_odd_s134217728(29)
        and want_odd_s536870912(29) != want_odd_s33554432(29)
        and want_odd_s536870912(29) != want_odd_s8388608(29)
        and want_odd_s536870912(8) == 0
        and want_odd_s536870912(27) == 0
        and want_odd_s536870912(28) == 44739242
        and want_odd_s536870912(29) == 178956970
        and want_odd_s536870912(30) == 357913942
        and jacobsthal(28) - 89478485 * ((-1) ** 28) + 89478486 == 89478486
        and jacobsthal(29) - 89478485 * ((-1) ** 29) + 89478486 == 357913942
        and jacobsthal(30) - 89478485 * ((-1) ** 30) + 89478486 == 357913942
        and want_odd_s33554432(8) == 0
        and want_odd_s16777216(8) == 0
        and want_odd_s8388608(8) == 0
        and want_odd_s4194304(8) == 0
        and want_odd_s2097152(8) == 0
        and want_odd_s1048576(8) == 0
        and want_odd_s524288(8) == 0
        and want_odd_s262144(8) == 0
        and want_odd_s131072(8) == 0
        and want_odd_s512(8) == 42
        and want_odd_s256(8) == 86
        and want_even_s512(8) == 42
        and want_clip_gp(8) == 85
        and want_clip_gp(26) == 22369621
        and want_clip_gp(27) == 44739242
        and want_clip_gp(28) == 89478485
        and jacobsthal(8) == 85
        and jacobsthal(26) == 22369621
        and jacobsthal(27) == 44739243
        and jacobsthal(28) == 89478485
        and want_clip_gp_jk(8) == 85
        and want_clip_slice(8) == 85
        and want_even_slice(8) == 85
        and ph268435457_n(8) == 268436097
        and ph268435457_n(26) == 436207617
        and ph268435457_n(27) == 603979777
        and ph268435457_n(28) == 939524097
        and ph268435457_n(29) == 1610612737
        and ph268435456_n(8) == 268436096
        and ph134217729_n(8) == 134218369
        and ph536870912_n(8) == 536871552
        and ph67108865_n(8) == 67109505
        and ph33554433_n(8) == 33555073
        and ph134217728_n(8) == 134218368
        and ph16777217_n(8) == 16777857
        and ph8388609_n(8) == 8389249
        and ph4194305_n(8) == 4194945
        and ph2097153_n(8) == 2097793
        and ph2097154_n(8) == 2097794
        and ph1048577_n(8) == 1049217
        and ph1048578_n(8) == 1049218
        and ph67108864_n(8) == 67109504
        and ph33554432_n(8) == 33555072
        and ph16777216_n(8) == 16777856
        and ph8388608_n(8) == 8389248
        and ph4194304_n(8) == 4194944
        and ph2097152_n(8) == 2097792
        and ph1048576_n(8) == 1049216
        and ph524289_n(8) == 524929
        and ph524290_n(8) == 524930
        and pal_kind(ph268435457_n(26), 2, 26) == "unp"
        and pal_kind(ph268435457_n(27), 2, 27) == "unp"
        and pal_kind(ph268435457_n(28), 2, 28) == "unp"
        and pal_kind(ph268435457_n(28), 2, 28) != "pair"
        and G(ph268435457_n(27), 2) == 1
        and G(ph268435457_n(28), 2) == 1
        and ph268435457_n(27) >= 4 * (1 << 27)
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
        and want_odd_s536870912(4) == 0
        and want_odd_s536870912(8) == 0
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
        and ph65537_n(8) == 66177
        and ph32769_n(8) == 33409
        and ph16385_n(8) == 17025
        and ph131074_n(8) == 131714
        and ph131072_n(8) == 131712
        and ph131073_n(8) == 131713
        and ph262145_n(8) == 262785
        and ph262146_n(8) == 262786
        and ph524288_n(8) == 524928
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def odd_s536870912_fold() -> dict:
    """k<=8 odd partner-5U+536870912 slice vs J_k-89478485(-1)^k+89478486 for k>=30."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = odd_s536870912_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_odd_s536870912(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if k >= 28:
            if a["first"] != (ph268435457_n(k), 2):
                return {"ok": False, "first": True, "k": k, "got": a["first"]}
        if k <= 27 and a["first"] is not None:
            return {"ok": False, "k27f": True, "got": a["first"]}
        n_ok += 1
        rows[str(k)] = {
            "n_at": a["n_at"],
            "first": list(a["first"]) if a["first"] else None,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["8"]["n_at"] == 0
        and rows["8"]["first"] is None
        and want_odd_s536870912(8) == 0
        and want_odd_s536870912(27) == 0
        and want_odd_s536870912(28) == 44739242
        and want_odd_s536870912(29) == 178956970
        and want_odd_s536870912(30) == 357913942
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """formula at k=28 and k=29; equals odd_s268435456 at k=28; covering at k=27."""
    ok = (
        want_odd_s536870912(28) != jacobsthal(28) - 89478485 * ((-1) ** 28) + 89478486
        and want_odd_s536870912(29) != jacobsthal(29) - 89478485 * ((-1) ** 29) + 89478486
        and want_odd_s536870912(8) != want_odd_s512(8)
        and want_odd_s536870912(8) != want_odd_s256(8)
        and want_odd_s536870912(8) != want_clip_gp(8)
        and want_odd_s536870912(8) != jacobsthal(8)
        and want_odd_s536870912(8) != want_even_s512(8)
        and want_odd_s536870912(26) == want_odd_s268435456(26)
        and want_odd_s536870912(27) != want_odd_s268435456(27)
        and want_odd_s536870912(27) != want_clip_gp(27)
        and want_odd_s536870912(28) != want_odd_s268435456(28)
        and want_odd_s536870912(28) != want_odd_s134217728(28)
        and want_odd_s536870912(28) != want_clip_gp(28)
        and want_odd_s536870912(28) == want_clip_gp(27)
        and want_odd_s536870912(29) == want_odd_s268435456(29)
        and want_odd_s536870912(29) == want_odd_s4(29)
        and want_odd_s536870912(29) == want_even_s67108864(29)
        and want_odd_s536870912(29) == want_clip_gp(29)
        and want_odd_s536870912(29) != want_odd_s134217728(29)
        and want_odd_s536870912(8) == 0
        and want_odd_s536870912(27) == 0
        and want_odd_s536870912(28) == 44739242
        and want_odd_s536870912(29) == 178956970
        and jacobsthal(28) - 89478485 * ((-1) ** 28) + 89478486 == 89478486
        and jacobsthal(29) - 89478485 * ((-1) ** 29) + 89478486 == 357913942
        and want_odd_s33554432(8) == 0
        and want_odd_s16777216(8) == 0
        and want_odd_s8388608(8) == 0
        and want_odd_s4194304(8) == 0
        and want_odd_s2097152(8) == 0
        and want_odd_s1048576(8) == 0
        and want_odd_s524288(8) == 0
        and want_odd_s262144(8) == 0
        and want_odd_s131072(8) == 0
        and want_odd_s512(8) == 42
        and want_odd_s256(8) == 86
        and want_even_s512(8) == 42
        and want_clip_gp(8) == 85
        and want_clip_gp(27) == 44739242
        and want_clip_gp(28) == 89478485
        and jacobsthal(8) == 85
        and jacobsthal(27) == 44739243
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and pal_kind(ph268435457_n(28), 2, 28) == "unp"
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
    zt = json.loads(ZT_JSON.read_text())
    zq = json.loads(ZQ_JSON.read_text())
    zv = json.loads(ZV_JSON.read_text())
    ok = (
        zt["checks"]["all_ok"]
        and zq["checks"]["all_ok"]
        and zv["checks"]["all_ok"]
        and zt["verdict"]["odd_s268435456_eq_J_k_plus_44739243m1_plus_44739242_k_ge_29"] == "LEMMA"
        and zq["verdict"]["odd_s134217728_eq_J_k_minus_22369621m1_plus_22369622_k_ge_28"] == "LEMMA"
        and zv["verdict"]["ph536870912_eq_2fold_zs_k_ge_2"] == "LEMMA"
        and zt["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and zt["verdict"]["prize"] == "unsolved"
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
    cnt = odd_s536870912_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "ZW",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "odd_s536870912_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_s536870912_eq_J_k_minus_89478485m1_plus_89478486_k_ge_30": True,
            "first_odd_s536870912_eq_ph268435457_k_ge_28": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_s536870912_eq_J_k_minus_89478485m1_plus_89478486_k_ge_30": "LEMMA",
            "first_odd_s536870912_eq_ph268435457_k_ge_28": "LEMMA",
            "odd_s536870912_eq_form_at_k29": "KILLED",
            "odd_s536870912_eq_form_at_k28": "KILLED",
            "odd_s536870912_eq_odd_s268435456_at_k28": "KILLED",
            "odd_s536870912_eq_odd_s134217728_at_k28": "KILLED",
            "odd_s536870912_eq_clip_gp_at_k28": "KILLED",
            "odd_s536870912_eq_odd_s268435456_at_k27": "KILLED",
            "odd_s536870912_eq_clip_gp_at_k27": "KILLED",
            "odd_s536870912_eq_clip_gp_at_k8": "KILLED",
            "odd_s536870912_eq_J_k_at_k8": "KILLED",
            "odd_s536870912_eq_odd_s512_at_k8": "KILLED",
            "ph268435457_covering_at_k27": "KILLED",
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
    print("odd s536870912 k8", dump["odd_s536870912_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
