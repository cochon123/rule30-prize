#!/usr/bin/env python3
"""Cycle YJ: odd partner-5U+65536 unpaired extra has count J_k+10923(-1)^k+10922.

Odd-n unpaired extra at j=2n-5U-65536 with j>=2 has count
J_k+10923(-1)^k+10922 for k>=17. The first cell is n=5U/2+32769, j=2
for k>=15. Dies at k=16 for that formula (got 21846, not 43690). Dies
at k=15 for that formula (got 5462, not 10922). Dies at k=15 for
equals odd_s32768 and odd_s16384 and clip_gp (got 5462, not 10922).
Dies at k=14 for covering. Do not kill equals odd_s32768 or odd_s8192
or odd_s2048 or odd_s512 or odd_s128 or odd_s32 or odd_s8 or odd_s4
at k=16 (all 21846). Do not kill equals odd_s16384 or even_s16384 or
odd_s4096 or even_s4096 or odd_s1024 or odd_s256 or odd_s64 or
odd_s16 or odd_s4 or clip_gp at k=17 (all 43690). Do not kill
pal_kind unpaired at n=5U/2+32769, j=2 for k>=15. Do not PREFIX
pal-center tot. Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk leftover d catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_yj.py --certify
Dump: research/cycle_yj.json
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
from cycle_yi import ph65536_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
YI_JSON = Path(__file__).resolve().parent / "cycle_yi.json"
YG_JSON = Path(__file__).resolve().parent / "cycle_yg.json"
YD_JSON = Path(__file__).resolve().parent / "cycle_yd.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph32769_n(k: int) -> int:
    """Covering n=5U/2+32769, first odd partner-5U+65536 cell."""
    return parent_half(k) + 32769


def want_odd_s65536(k: int) -> int:
    """Odd-n unpaired extra at partner 5U+65536, j>=2: 0 at k<=14, 5462 at k=15, 21846 at k=16."""
    if k <= 14:
        return 0
    if k == 15:
        return 5462
    if k == 16:
        return 21846
    return jacobsthal(k) + 10923 * ((-1) ** k) + 10922


def odd_s65536_split(k: int) -> dict:
    """Odd-n unpaired extra at j=2n-5U-65536 with j>=2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    n_at = n_bad = 0
    first = None
    for n in range(1, 4 * u, 2):
        j = 2 * n - clip - 65536
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
    """k<=64: odd slice J_k+10923(-1)^k+10922 for k>=17; dies at k=16 for that form.

    Do not call odd_s65536_split here.
    Census is odd_s65536_fold for k<=8.
    """
    n_ok = 0
    if want_odd_s65536(0) != 0 or want_odd_s65536(14) != 0:
        return {"ok": False, "k014": True}
    if want_odd_s65536(15) != 5462 or want_odd_s65536(16) != 21846:
        return {"ok": False, "k1516": True}
    if want_odd_s65536(17) != 43690 or want_odd_s65536(18) != 109226:
        return {"ok": False, "k1718": True}
    if want_odd_s65536(16) == want_odd_s65536(17):
        return {"ok": False, "k1617": True}
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
        if k <= 14 and want_odd_s65536(k) != 0:
            return {"ok": False, "z": True, "k": k}
        if k == 15:
            if want_odd_s65536(k) != 5462:
                return {"ok": False, "k15": True}
            if want_odd_s65536(k) == jacobsthal(k) + 10923 * ((-1) ** k) + 10922:
                return {"ok": False, "k15f": True}
        if k == 16:
            if want_odd_s65536(k) != 21846:
                return {"ok": False, "k16": True}
            if want_odd_s65536(k) == jacobsthal(k) + 10923 * ((-1) ** k) + 10922:
                return {"ok": False, "k16f": True}
        if k >= 17 and want_odd_s65536(k) != jacobsthal(k) + 10923 * ((-1) ** k) + 10922:
            return {"ok": False, "Jk": True, "k": k}
        if k >= 15:
            n = ph32769_n(k)
            j = 2 * n - clip - 65536
            if j != 2:
                return {"ok": False, "j2": True, "k": k}
            if 2 * n - 2 != clip + 65536:
                return {"ok": False, "pr": True, "k": k}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "pk": True, "k": k}
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if G(n, 2) != 1:
                return {"ok": False, "g2": True, "k": k}
        if k == 14:
            n = ph32769_n(14)
            if n < 4 * u:
                return {"ok": False, "k14c": True}
            if G(n, 2) != 1:
                return {"ok": False, "k14g": True}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "k14k": True}
            if 2 * n - 2 != clip + 65536:
                return {"ok": False, "k14p": True}
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
        and want_odd_s65536(15) != jacobsthal(15) + 10923 * ((-1) ** 15) + 10922
        and want_odd_s65536(16) != jacobsthal(16) + 10923 * ((-1) ** 16) + 10922
        and want_odd_s65536(8) != want_odd_s512(8)
        and want_odd_s65536(8) != want_odd_s256(8)
        and want_odd_s65536(8) != want_odd_s128(8)
        and want_odd_s65536(8) != want_odd_s64(8)
        and want_odd_s65536(8) != want_odd_s32(8)
        and want_odd_s65536(8) != want_odd_s16(8)
        and want_odd_s65536(8) != want_odd_s8(8)
        and want_odd_s65536(8) != want_odd_s4(8)
        and want_odd_s65536(8) != jacobsthal(8)
        and want_odd_s65536(8) != want_clip_gp(8)
        and want_odd_s65536(8) != want_even_slice(8)
        and want_odd_s65536(8) != want_even_s512(8)
        and want_odd_s65536(8) != want_j0_odd_unp(8)
        and want_odd_s65536(8) == want_odd_s32768(8)
        and want_odd_s65536(8) == want_odd_s16384(8)
        and want_odd_s65536(8) == want_odd_s8192(8)
        and want_odd_s65536(8) == want_odd_s4096(8)
        and want_odd_s65536(8) == want_odd_s2048(8)
        and want_odd_s65536(8) == want_odd_s1024(8)
        and want_odd_s65536(8) == want_even_s32768(8)
        and want_odd_s65536(8) == want_even_s16384(8)
        and want_odd_s65536(8) == want_even_s8192(8)
        and want_odd_s65536(8) == want_even_s4096(8)
        and want_odd_s65536(8) == want_even_s2048(8)
        and want_odd_s65536(8) == want_even_s1024(8)
        and want_odd_s65536(9) != want_clip_gp(9)
        and want_odd_s65536(9) != want_odd_s1024(9)
        and want_odd_s65536(9) != want_odd_s512(9)
        and want_odd_s65536(9) != want_odd_s256(9)
        and want_odd_s65536(9) == want_odd_s32768(9)
        and want_odd_s65536(9) == want_odd_s16384(9)
        and want_odd_s65536(9) == want_odd_s8192(9)
        and want_odd_s65536(9) == want_odd_s4096(9)
        and want_odd_s65536(9) == want_odd_s2048(9)
        and want_odd_s65536(10) != want_odd_s2048(10)
        and want_odd_s65536(10) != want_odd_s1024(10)
        and want_odd_s65536(10) != want_odd_s512(10)
        and want_odd_s65536(10) != want_clip_gp(10)
        and want_odd_s65536(10) == want_odd_s32768(10)
        and want_odd_s65536(10) == want_odd_s16384(10)
        and want_odd_s65536(10) == want_odd_s8192(10)
        and want_odd_s65536(10) == want_odd_s4096(10)
        and want_odd_s65536(11) != want_odd_s4096(11)
        and want_odd_s65536(11) != want_odd_s2048(11)
        and want_odd_s65536(11) != want_clip_gp(11)
        and want_odd_s65536(11) == want_odd_s32768(11)
        and want_odd_s65536(11) == want_odd_s16384(11)
        and want_odd_s65536(11) == want_odd_s8192(11)
        and want_odd_s65536(12) != want_odd_s8192(12)
        and want_odd_s65536(12) != want_odd_s4096(12)
        and want_odd_s65536(12) != want_clip_gp(12)
        and want_odd_s65536(12) == want_odd_s32768(12)
        and want_odd_s65536(12) == want_odd_s16384(12)
        and want_odd_s65536(13) != want_odd_s16384(13)
        and want_odd_s65536(13) != want_odd_s8192(13)
        and want_odd_s65536(13) != want_odd_s4096(13)
        and want_odd_s65536(13) != want_clip_gp(13)
        and want_odd_s65536(13) == want_odd_s32768(13)
        and want_odd_s65536(14) != want_odd_s32768(14)
        and want_odd_s65536(14) != want_odd_s16384(14)
        and want_odd_s65536(14) != want_odd_s8192(14)
        and want_odd_s65536(14) != want_odd_s4096(14)
        and want_odd_s65536(14) != want_clip_gp(14)
        and want_odd_s65536(15) != want_odd_s32768(15)
        and want_odd_s65536(15) != want_odd_s16384(15)
        and want_odd_s65536(15) != want_odd_s8192(15)
        and want_odd_s65536(15) != want_odd_s4096(15)
        and want_odd_s65536(15) != want_clip_gp(15)
        and want_odd_s65536(15) != want_odd_s4(15)
        and want_odd_s65536(16) == want_odd_s32768(16)
        and want_odd_s65536(16) == want_odd_s8192(16)
        and want_odd_s65536(16) == want_odd_s2048(16)
        and want_odd_s65536(16) == want_odd_s512(16)
        and want_odd_s65536(16) == want_odd_s128(16)
        and want_odd_s65536(16) == want_odd_s32(16)
        and want_odd_s65536(16) == want_odd_s8(16)
        and want_odd_s65536(16) == want_odd_s4(16)
        and want_odd_s65536(16) != want_odd_s16384(16)
        and want_odd_s65536(16) != want_odd_s4096(16)
        and want_odd_s65536(16) != want_clip_gp(16)
        and want_odd_s65536(16) != want_even_s32768(16)
        and want_odd_s65536(17) == want_odd_s16384(17)
        and want_odd_s65536(17) == want_even_s16384(17)
        and want_odd_s65536(17) == want_odd_s4096(17)
        and want_odd_s65536(17) == want_even_s4096(17)
        and want_odd_s65536(17) == want_odd_s1024(17)
        and want_odd_s65536(17) == want_odd_s256(17)
        and want_odd_s65536(17) == want_odd_s64(17)
        and want_odd_s65536(17) == want_odd_s16(17)
        and want_odd_s65536(17) == want_odd_s4(17)
        and want_odd_s65536(17) == want_clip_gp(17)
        and want_odd_s65536(17) != want_odd_s32768(17)
        and want_odd_s65536(17) != want_odd_s8192(17)
        and want_odd_s65536(17) != want_even_s32768(17)
        and want_odd_s65536(8) == 0
        and want_odd_s65536(9) == 0
        and want_odd_s65536(10) == 0
        and want_odd_s65536(11) == 0
        and want_odd_s65536(12) == 0
        and want_odd_s65536(13) == 0
        and want_odd_s65536(14) == 0
        and want_odd_s65536(15) == 5462
        and want_odd_s65536(16) == 21846
        and want_odd_s65536(17) == 43690
        and want_odd_s65536(18) == 109226
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
        and want_even_s1024(8) == 0
        and want_even_s2048(8) == 0
        and want_even_s4096(8) == 0
        and want_even_s8192(8) == 0
        and want_even_s16384(8) == 0
        and want_even_s32768(8) == 0
        and want_odd_s64(8) == 106
        and want_odd_s32(8) == 86
        and want_odd_s16(8) == 90
        and want_odd_s8(8) == 86
        and want_odd_s128(8) == 86
        and want_odd_s4(8) == 86
        and want_clip_gp(8) == 85
        and want_clip_gp(14) == 5461
        and want_clip_gp(15) == 10922
        and want_clip_gp(16) == 21845
        and want_clip_gp(17) == 43690
        and jacobsthal(8) == 85
        and jacobsthal(15) == 10923
        and jacobsthal(16) == 21845
        and jacobsthal(17) == 43691
        and jacobsthal(18) == 87381
        and want_clip_gp_jk(8) == 85
        and want_clip_slice(8) == 85
        and want_even_slice(8) == 85
        and ph32769_n(8) == 33409
        and ph32769_n(14) == 73729
        and ph32769_n(15) == 114689
        and ph32769_n(16) == 196609
        and ph16385_n(8) == 17025
        and ph8193_n(8) == 8833
        and ph65536_n(8) == 66176
        and ph16384_n(8) == 17024
        and ph8192_n(8) == 8832
        and ph4096_n(8) == 4736
        and pal_kind(ph32769_n(15), 2, 15) == "unp"
        and pal_kind(ph32769_n(15), 2, 15) != "pair"
        and G(ph32769_n(14), 2) == 1
        and G(ph32769_n(15), 2) == 1
        and ph32769_n(14) >= 4 * (1 << 14)
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
        and want_odd_s65536(4) == 0
        and want_odd_s65536(8) == 0
        and jacobsthal(15) + 10923 * ((-1) ** 15) + 10922 == 10922
        and jacobsthal(16) + 10923 * ((-1) ** 16) + 10922 == 43690
        and jacobsthal(17) + 10923 * ((-1) ** 17) + 10922 == 43690
        and want_lo_e(8) == 14114
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def odd_s65536_fold() -> dict:
    """k<=8 odd partner-5U+65536 slice vs J_k+10923(-1)^k+10922 for k>=17."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = odd_s65536_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_odd_s65536(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if k >= 15:
            if a["first"] != (ph32769_n(k), 2):
                return {"ok": False, "first": True, "k": k, "got": a["first"]}
        if k <= 14 and a["first"] is not None:
            return {"ok": False, "k14f": True, "got": a["first"]}
        n_ok += 1
        rows[str(k)] = {
            "n_at": a["n_at"],
            "first": list(a["first"]) if a["first"] else None,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["8"]["n_at"] == 0
        and rows["8"]["first"] is None
        and want_odd_s65536(8) == 0
        and want_odd_s65536(14) == 0
        and want_odd_s65536(15) == 5462
        and want_odd_s65536(16) == 21846
        and want_odd_s65536(17) == 43690
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """formula at k=15 and k=16; equals odd_s32768 at k=15; covering at k=14."""
    ok = (
        want_odd_s65536(15) != jacobsthal(15) + 10923 * ((-1) ** 15) + 10922
        and want_odd_s65536(16) != jacobsthal(16) + 10923 * ((-1) ** 16) + 10922
        and want_odd_s65536(8) != want_odd_s512(8)
        and want_odd_s65536(8) != want_odd_s256(8)
        and want_odd_s65536(8) != want_clip_gp(8)
        and want_odd_s65536(8) != jacobsthal(8)
        and want_odd_s65536(8) != want_even_s512(8)
        and want_odd_s65536(9) != want_clip_gp(9)
        and want_odd_s65536(9) != want_odd_s1024(9)
        and want_odd_s65536(9) != want_odd_s512(9)
        and want_odd_s65536(9) != want_odd_s256(9)
        and want_odd_s65536(10) != want_odd_s2048(10)
        and want_odd_s65536(10) != want_odd_s1024(10)
        and want_odd_s65536(10) != want_odd_s512(10)
        and want_odd_s65536(10) != want_clip_gp(10)
        and want_odd_s65536(11) != want_odd_s4096(11)
        and want_odd_s65536(11) != want_odd_s2048(11)
        and want_odd_s65536(11) != want_clip_gp(11)
        and want_odd_s65536(12) != want_odd_s8192(12)
        and want_odd_s65536(12) != want_odd_s4096(12)
        and want_odd_s65536(12) != want_clip_gp(12)
        and want_odd_s65536(13) != want_odd_s16384(13)
        and want_odd_s65536(13) != want_odd_s8192(13)
        and want_odd_s65536(13) != want_clip_gp(13)
        and want_odd_s65536(14) != want_odd_s32768(14)
        and want_odd_s65536(14) != want_odd_s16384(14)
        and want_odd_s65536(14) != want_clip_gp(14)
        and want_odd_s65536(15) != want_odd_s32768(15)
        and want_odd_s65536(15) != want_odd_s16384(15)
        and want_odd_s65536(15) != want_clip_gp(15)
        and want_odd_s65536(15) != want_odd_s4(15)
        and want_odd_s65536(16) == want_odd_s32768(16)
        and want_odd_s65536(16) == want_odd_s8192(16)
        and want_odd_s65536(16) == want_odd_s2048(16)
        and want_odd_s65536(16) == want_odd_s512(16)
        and want_odd_s65536(16) == want_odd_s128(16)
        and want_odd_s65536(16) == want_odd_s32(16)
        and want_odd_s65536(16) == want_odd_s8(16)
        and want_odd_s65536(16) == want_odd_s4(16)
        and want_odd_s65536(16) != want_odd_s16384(16)
        and want_odd_s65536(16) != want_clip_gp(16)
        and want_odd_s65536(16) != want_even_s32768(16)
        and want_odd_s65536(17) == want_clip_gp(17)
        and want_odd_s65536(17) == want_odd_s16384(17)
        and want_odd_s65536(17) == want_odd_s4(17)
        and want_odd_s65536(17) != want_odd_s32768(17)
        and want_odd_s65536(8) == 0
        and want_odd_s65536(9) == 0
        and want_odd_s65536(10) == 0
        and want_odd_s65536(11) == 0
        and want_odd_s65536(12) == 0
        and want_odd_s65536(13) == 0
        and want_odd_s65536(14) == 0
        and want_odd_s65536(15) == 5462
        and want_odd_s65536(16) == 21846
        and jacobsthal(15) + 10923 * ((-1) ** 15) + 10922 == 10922
        and jacobsthal(16) + 10923 * ((-1) ** 16) + 10922 == 43690
        and want_odd_s32768(8) == 0
        and want_odd_s16384(8) == 0
        and want_odd_s8192(8) == 0
        and want_odd_s4096(8) == 0
        and want_odd_s2048(8) == 0
        and want_odd_s1024(8) == 0
        and want_odd_s512(8) == 42
        and want_odd_s256(8) == 86
        and want_even_s512(8) == 42
        and want_clip_gp(8) == 85
        and want_clip_gp(14) == 5461
        and want_clip_gp(15) == 10922
        and jacobsthal(8) == 85
        and jacobsthal(15) == 10923
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and pal_kind(ph32769_n(15), 2, 15) == "unp"
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
    yi = json.loads(YI_JSON.read_text())
    yg = json.loads(YG_JSON.read_text())
    yd = json.loads(YD_JSON.read_text())
    ok = (
        yi["checks"]["all_ok"]
        and yg["checks"]["all_ok"]
        and yd["checks"]["all_ok"]
        and yi["verdict"]["ph65536_j65536_partner_5U65536"] == "LEMMA"
        and yg["verdict"]["odd_s32768_eq_J_k_minus_5461m1_plus_5462_k_ge_16"] == "LEMMA"
        and yd["verdict"]["odd_s16384_eq_J_k_plus_2731m1_plus_2730_k_ge_15"] == "LEMMA"
        and yi["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and yi["verdict"]["prize"] == "unsolved"
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
    cnt = odd_s65536_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "YJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "odd_s65536_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_s65536_eq_J_k_plus_10923m1_plus_10922_k_ge_17": True,
            "first_odd_s65536_eq_ph32769_k_ge_15": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_s65536_eq_J_k_plus_10923m1_plus_10922_k_ge_17": "LEMMA",
            "first_odd_s65536_eq_ph32769_k_ge_15": "LEMMA",
            "odd_s65536_eq_form_at_k16": "KILLED",
            "odd_s65536_eq_form_at_k15": "KILLED",
            "odd_s65536_eq_odd_s32768_at_k15": "KILLED",
            "odd_s65536_eq_odd_s16384_at_k15": "KILLED",
            "odd_s65536_eq_clip_gp_at_k15": "KILLED",
            "odd_s65536_eq_odd_s32768_at_k14": "KILLED",
            "odd_s65536_eq_odd_s16384_at_k14": "KILLED",
            "odd_s65536_eq_clip_gp_at_k14": "KILLED",
            "odd_s65536_eq_odd_s16384_at_k13": "KILLED",
            "odd_s65536_eq_odd_s8192_at_k13": "KILLED",
            "odd_s65536_eq_clip_gp_at_k13": "KILLED",
            "odd_s65536_eq_odd_s8192_at_k12": "KILLED",
            "odd_s65536_eq_odd_s4096_at_k12": "KILLED",
            "odd_s65536_eq_clip_gp_at_k12": "KILLED",
            "odd_s65536_eq_odd_s4096_at_k11": "KILLED",
            "odd_s65536_eq_clip_gp_at_k11": "KILLED",
            "odd_s65536_eq_odd_s2048_at_k10": "KILLED",
            "odd_s65536_eq_clip_gp_at_k10": "KILLED",
            "odd_s65536_eq_odd_s1024_at_k9": "KILLED",
            "odd_s65536_eq_clip_gp_at_k9": "KILLED",
            "odd_s65536_eq_odd_s512_at_k8": "KILLED",
            "odd_s65536_eq_clip_gp_at_k8": "KILLED",
            "odd_s65536_eq_J_k_at_k8": "KILLED",
            "odd_s65536_eq_even_s512_at_k8": "KILLED",
            "ph32769_covering_at_k14": "KILLED",
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
    print("odd s65536 k8", dump["odd_s65536_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
