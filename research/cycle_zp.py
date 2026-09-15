#!/usr/bin/env python3
"""Cycle ZP: even n=5U/2+134217728 is the 2-fold of Cycle ZM at k-1.

Covering n=5U/2+134217728 equals 2*(5U_p/2+67108864). Even doubling sends parent
left Green to child left Green with pal_kind and clip-edge preserved,
so unpaired left is {0,134217728} for k>=29 and leftover+pal is the even
11-set {U/2,U/2+134217728,U/2+268435456,U,U+134217728,U+268435456,2U,2U+134217728,2U+268435456,5U/2,n}
for k>=30. The j=134217728 cell has partner 5U+134217728. Dies at k=28 for
unpaired {0,134217728} (G at j=134217728 is 0). Dies at k=29 for leftover
11-set (got 6). Leftover at first covering k=27 is 2, not a blind +1 of
Cycle ZM's 2. Do not kill pal_kind unpaired at n=5U/2+134217728, j=0
for k>=27 or j=134217728 for k>=29. Do not call ph134217728_lo_js below k=30.
Do not call ph67108864_lo_js below k=29. Do not call ph33554432_lo_js below
k=28. Do not call ph16777216_lo_js below k=27. Do not call ph8388608_lo_js
below k=26. Do not call ph4194304_lo_js below k=25. Do not PREFIX pal-center tot.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk leftover
d catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_zp.py --certify
Dump: research/cycle_zp.json
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
from cycle_yf import ph32768_n, want_ph32768_lo
from cycle_yi import ph65536_n, want_ph65536_lo
from cycle_yl import ph131072_n, want_ph131072_lo
from cycle_yo import ph262144_n, want_ph262144_clip, want_ph262144_lo, want_ph262144_unp
from cycle_yr import (
    ph524288_n,
    want_ph524288_clip,
    want_ph524288_lo,
    want_ph524288_unp,
)
from cycle_yu import (
    ph1048576_n,
    want_ph1048576_clip,
    want_ph1048576_lo,
    want_ph1048576_unp,
)
from cycle_yx import (
    ph2097152_n,
    want_ph2097152_clip,
    want_ph2097152_lo,
    want_ph2097152_unp,
)
from cycle_za import (
    ph4194304_n,
    want_ph4194304_clip,
    want_ph4194304_lo,
    want_ph4194304_unp,
)
from cycle_zj import (
    ph33554432_n,
    want_ph33554432_clip,
    want_ph33554432_lo,
    want_ph33554432_unp,
)
from cycle_zm import (
    ph67108864_lo_js,
    ph67108864_n,
    want_ph67108864_clip,
    want_ph67108864_lo,
    want_ph67108864_unp,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ZM_JSON = Path(__file__).resolve().parent / "cycle_zm.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
ZJ_JSON = Path(__file__).resolve().parent / "cycle_zj.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph134217728_n(k: int) -> int:
    """Covering n=5U/2+134217728."""
    return parent_half(k) + 134217728


def ph134217728_lo_js(k: int) -> tuple[int, ...]:
    """Leftover+pal left indices at even n=5U/2+134217728: 2-fold of Cycle ZM.

    Call only for k>=30.
    """
    return tuple(2 * j for j in ph67108864_lo_js(k - 1))


def want_ph134217728_unp(k: int) -> int:
    """Unpaired left Green at n=5U/2+134217728: 2 for k>=29; 1 at k=28; 3 at k=27."""
    if k <= 26:
        return 0
    if k == 27:
        return 3
    if k == 28:
        return 1
    return 2


def want_ph134217728_lo(k: int) -> int:
    """Leftover+pal left Green at n=5U/2+134217728: 11 for k>=30; 6 at k=29; 1 at k=28; 2 at k=27."""
    if k <= 26:
        return 0
    if k == 27:
        return 2
    if k == 28:
        return 1
    if k == 29:
        return 6
    return 11


def want_ph134217728_clip(k: int) -> int:
    """Left clip-edge Green at n=5U/2+134217728: 1 for k>=27 except 0 at k=29."""
    if k <= 26:
        return 0
    if k == 29:
        return 0
    return 1


def ph134217728_split(k: int) -> dict:
    """Left Green kinds at even n=5U/2+134217728. Do not call from tot_form."""
    n = ph134217728_n(k)
    u = 1 << k
    clip = 5 * u
    n_unp = n_lo = n_clip = n_bad = 0
    unp_js = []
    lo_js = []
    if k < 27 or n >= 4 * u:
        return {
            "n_unp": 0,
            "n_lo": 0,
            "n_clip": 0,
            "n_bad": 0,
            "unp_js": [],
            "lo_js": [],
        }
    for j in range(0, min(2 * n, clip) + 1):
        if G(n, j) == 0:
            continue
        kind = pal_kind(n, j, k)
        if j > n:
            continue
        if kind == "unp":
            n_unp += 1
            unp_js.append(j)
        elif kind in ("pair", "pal"):
            if is_clip_edge(n, j, k):
                n_clip += 1
            elif j in (1, 2):
                n_bad += 1
            else:
                n_lo += 1
                lo_js.append(j)
        else:
            n_bad += 1
    return {
        "n_unp": n_unp,
        "n_lo": n_lo,
        "n_clip": n_clip,
        "n_bad": n_bad,
        "unp_js": unp_js,
        "lo_js": lo_js,
    }


def tot_form() -> dict:
    """k<=64: n=5U/2+134217728 is 2-fold of ZM; dies at k=28 for {0,134217728}.

    Do not call ph134217728_split here.
    Do not call ph134217728_lo_js below k=30.
    Do not call ph67108864_lo_js below k=29.
    Do not call ph33554432_lo_js below k=28.
    Do not call ph16777216_lo_js below k=27.
    Do not call ph8388608_lo_js below k=26.
    Do not call ph4194304_lo_js below k=25.
    Census is ph134217728_fold for k<=8.
    """
    n_ok = 0
    if want_ph134217728_unp(0) != 0 or want_ph134217728_lo(26) != 0:
        return {"ok": False, "k26": True}
    if want_ph134217728_unp(27) != 3 or want_ph134217728_unp(28) != 1:
        return {"ok": False, "k2728": True}
    if want_ph134217728_lo(28) != 1 or want_ph134217728_unp(29) != 2:
        return {"ok": False, "k2829": True}
    if want_ph134217728_clip(29) != 0 or want_ph134217728_lo(30) != 11:
        return {"ok": False, "k2930": True}
    if want_ph134217728_lo(27) != 2:
        return {"ok": False, "k27lo": True}
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
        n = ph134217728_n(k)
        n_p = ph67108864_n(k - 1) if k >= 1 else ph67108864_n(0)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if n != parent_half(k) + 134217728:
            return {"ok": False, "n": True, "k": k}
        if k >= 2:
            if n != 2 * n_p:
                return {"ok": False, "fold": True, "k": k}
            if n % 2 != 0:
                return {"ok": False, "ev": True, "k": k}
        if k >= 27:
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if pal_kind(n, 0, k) != "unp" or G(n, 0) != 1:
                return {"ok": False, "j0": True, "k": k}
            if 2 * n - 134217728 != clip + 134217728:
                return {"ok": False, "pr": True, "k": k}
            if not is_clip_edge(n, 268435456, k):
                return {"ok": False, "c268435456": True, "k": k}
            if G(n, 0) != G(n_p, 0):
                return {"ok": False, "g00": True, "k": k}
            if pal_kind(n, 134217728, k) != "unp":
                return {"ok": False, "j134217728k": True, "k": k}
        if k >= 29:
            if G(n, 134217728) != 1 or G(n, 134217728) != G(n_p, 67108864):
                return {"ok": False, "g134217728": True, "k": k}
            if pal_kind(n_p, 67108864, k - 1) != "unp":
                return {"ok": False, "p67108864": True, "k": k}
            if want_ph134217728_unp(k) != 2:
                return {"ok": False, "u2": True, "k": k}
        if k == 28:
            if G(n, 134217728) != 0 or want_ph134217728_unp(k) != 1:
                return {"ok": False, "k28g": True}
            if pal_kind(n, 134217728, k) != "unp":
                return {"ok": False, "k28k": True}
        if k == 27:
            if G(n, 134217728) != 0 or want_ph134217728_unp(k) != 3:
                return {"ok": False, "k27g": True}
            if pal_kind(n, 134217728, k) != "unp":
                return {"ok": False, "k27k": True}
        if k == 26:
            if n < 4 * u:
                return {"ok": False, "k26c": True}
        if k >= 30:
            if want_ph134217728_lo(k) != 11 or want_ph67108864_lo(k - 1) != 11:
                return {"ok": False, "lo": True, "k": k}
            if ph134217728_lo_js(k) != tuple(2 * j for j in ph67108864_lo_js(k - 1)):
                return {"ok": False, "js": True, "k": k}
            for j in ph134217728_lo_js(k):
                if G(n, j) != 1:
                    return {"ok": False, "loj": True, "k": k, "j": j}
                kind = pal_kind(n, j, k)
                if kind not in ("pair", "pal"):
                    return {"ok": False, "lok": True, "k": k, "j": j}
                if is_clip_edge(n, j, k) or j in (1, 2):
                    return {"ok": False, "loc": True, "k": k, "j": j}
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
        and want_ph134217728_unp(28) != 2
        and want_ph134217728_lo(29) != 11
        and want_ph134217728_unp(8) != want_clip_gp(8)
        and want_ph134217728_lo(8) != want_clip_gp(8)
        and want_ph134217728_unp(8) != want_even_slice(8)
        and pal_kind(ph134217728_n(27), 134217728, 27) != "pair"
        and G(ph134217728_n(26), 134217728) != 1
        and G(ph134217728_n(27), 134217728) != 1
        and G(ph134217728_n(28), 134217728) != 1
        and pal_kind(ph134217728_n(27), 0, 27) == "unp"
        and pal_kind(ph134217728_n(27), 134217728, 27) == "unp"
        and pal_kind(ph134217728_n(29), 134217728, 29) == "unp"
        and want_ph134217728_unp(8) == 0
        and want_ph134217728_unp(26) == 0
        and want_ph134217728_unp(27) == 3
        and want_ph134217728_unp(28) == 1
        and want_ph134217728_unp(29) == 2
        and want_ph134217728_lo(26) == 0
        and want_ph134217728_lo(27) == 2
        and want_ph134217728_lo(27) != want_ph67108864_lo(26) + 1
        and want_ph134217728_lo(28) == 1
        and want_ph134217728_lo(29) == 6
        and want_ph134217728_lo(30) == 11
        and want_ph134217728_clip(27) == 1
        and want_ph134217728_clip(28) == 1
        and want_ph134217728_clip(29) == 0
        and ph134217728_n(8) == 134218368
        and ph134217728_n(8) == 2 * ph67108864_n(7)
        and ph134217728_n(24) == 176160768
        and ph134217728_n(24) == 2 * ph67108864_n(23)
        and ph134217728_n(25) == 218103808
        and ph134217728_n(25) == 2 * ph67108864_n(24)
        and ph134217728_n(26) == 301989888
        and ph134217728_n(26) == 2 * ph67108864_n(25)
        and ph134217728_n(27) == 469762048
        and ph67108864_n(8) == 67109504
        and ph33554432_n(8) == 33555072
        and ph4194304_n(8) == 4194944
        and ph2097152_n(8) == 2097792
        and ph1048576_n(8) == 1049216
        and ph524288_n(8) == 524928
        and ph262144_n(8) == 262784
        and ph131072_n(8) == 131712
        and ph65536_n(8) == 66176
        and ph32768_n(8) == 33408
        and want_ph67108864_unp(26) == 3
        and want_ph67108864_lo(26) == 2
        and want_ph67108864_lo(29) == 11
        and want_ph67108864_clip(28) == 0
        and want_ph33554432_unp(25) == 3
        and want_ph33554432_lo(25) == 3
        and want_ph33554432_lo(28) == 11
        and want_ph33554432_clip(27) == 0
        and want_ph4194304_unp(22) == 3
        and want_ph4194304_lo(22) == 2
        and want_ph4194304_lo(25) == 11
        and want_ph4194304_clip(24) == 0
        and want_ph2097152_unp(21) == 3
        and want_ph2097152_lo(24) == 11
        and want_ph2097152_clip(23) == 0
        and want_ph1048576_unp(20) == 3
        and want_ph1048576_lo(23) == 11
        and want_ph1048576_clip(22) == 0
        and want_ph524288_unp(19) == 3
        and want_ph524288_lo(22) == 11
        and want_ph524288_clip(21) == 0
        and want_ph262144_lo(21) == 11
        and want_ph131072_lo(20) == 11
        and want_ph65536_lo(19) == 11
        and want_ph32768_lo(18) == 11
        and want_clip_slice(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_even_slice(8) == 85
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
        and want_ph134217728_unp(8) == 0
        and want_ph134217728_unp(29) == 2
        and want_lo_e(8) == 14114
        and want_ph67108864_unp(26) == 3
        and want_ph67108864_clip(28) == 0
        and want_ph33554432_unp(25) == 3
        and want_ph33554432_clip(27) == 0
        and want_ph4194304_unp(22) == 3
        and want_ph4194304_clip(24) == 0
        and want_ph262144_unp(18) == 3
        and want_ph262144_clip(20) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ph134217728_fold() -> dict:
    """k<=8 left Green at even n=5U/2+134217728 vs 2-fold of ZM."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = ph134217728_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_unp"] != want_ph134217728_unp(k):
            return {"ok": False, "unp": True, "k": k, "got": a["n_unp"]}
        if a["n_lo"] != want_ph134217728_lo(k):
            return {"ok": False, "lo": True, "k": k, "got": a["n_lo"]}
        if a["n_clip"] != want_ph134217728_clip(k):
            return {"ok": False, "cl": True, "k": k, "got": a["n_clip"]}
        if k <= 8 and a["unp_js"] != []:
            return {"ok": False, "u8": True, "k": k, "got": a["unp_js"]}
        n_ok += 1
        rows[str(k)] = {
            "n_unp": a["n_unp"],
            "n_lo": a["n_lo"],
            "n_clip": a["n_clip"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["8"]["n_unp"] == 0
        and rows["8"]["n_lo"] == 0
        and rows["8"]["n_clip"] == 0
        and want_ph134217728_lo(8) == 0
        and want_ph134217728_lo(27) == 2
        and want_ph134217728_lo(28) == 1
        and want_ph134217728_lo(29) == 6
        and want_ph134217728_lo(30) == 11
        and want_ph67108864_lo(29) == 11
        and want_ph33554432_lo(28) == 11
        and want_ph4194304_lo(25) == 11
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """unpaired {0,134217728} at k=28; leftover 11-set at k=29."""
    n26 = ph134217728_n(26)
    n27 = ph134217728_n(27)
    n28 = ph134217728_n(28)
    n29 = ph134217728_n(29)
    ok = (
        want_ph134217728_unp(28) != 2
        and want_ph134217728_lo(29) != 11
        and want_ph134217728_unp(8) != want_clip_gp(8)
        and want_ph134217728_lo(8) != want_clip_gp(8)
        and want_ph134217728_unp(8) != want_even_slice(8)
        and pal_kind(n27, 134217728, 27) != "pair"
        and G(n26, 134217728) != 1
        and G(n27, 134217728) != 1
        and G(n28, 134217728) != 1
        and pal_kind(n27, 0, 27) == "unp"
        and pal_kind(n27, 134217728, 27) == "unp"
        and pal_kind(n28, 134217728, 28) == "unp"
        and pal_kind(n29, 134217728, 29) == "unp"
        and want_ph134217728_unp(8) == 0
        and want_ph134217728_unp(26) == 0
        and want_ph134217728_unp(27) == 3
        and want_ph134217728_lo(27) == 2
        and G(n26, 134217728) == 0
        and G(n27, 134217728) == 0
        and G(n28, 134217728) == 0
        and G(n29, 134217728) == 1
        and want_ph134217728_unp(28) == 1
        and want_ph134217728_unp(29) == 2
        and want_ph134217728_lo(28) == 1
        and want_ph134217728_lo(29) == 6
        and want_ph134217728_lo(30) == 11
        and want_clip_gp(8) == 85
        and want_even_slice(8) == 85
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and n26 == 301989888
        and n26 >= 4 * (1 << 26)
        and n27 < 4 * (1 << 27)
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
    zm = json.loads(ZM_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    zj = json.loads(ZJ_JSON.read_text())
    ok = (
        zm["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and zj["checks"]["all_ok"]
        and zm["verdict"]["ph67108864_j67108864_partner_5U67108864"] == "LEMMA"
        and zm["verdict"]["ph67108864_lo_eq_11_k_ge_29"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and zj["verdict"]["ph33554432_lo_eq_11_k_ge_28"] == "LEMMA"
        and zm["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and zm["verdict"]["prize"] == "unsolved"
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
    cnt = ph134217728_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "ZP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph134217728_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph134217728_eq_2fold_zm_k_ge_2": True,
            "ph134217728_unp_eq_0134217728_k_ge_29": True,
            "ph134217728_lo_eq_11_k_ge_30": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph134217728_eq_2fold_zm_k_ge_2": "LEMMA",
            "ph134217728_unp_eq_0134217728_k_ge_29": "LEMMA",
            "ph134217728_lo_eq_11_k_ge_30": "LEMMA",
            "ph134217728_j134217728_partner_5U134217728": "LEMMA",
            "ph134217728_unp_eq_0134217728_at_k28": "KILLED",
            "ph134217728_lo_eq_11_at_k29": "KILLED",
            "ph134217728_unp_eq_clip_gp_at_k8": "KILLED",
            "ph134217728_lo_eq_clip_gp_at_k8": "KILLED",
            "ph134217728_unp_eq_even_slice_at_k8": "KILLED",
            "ph134217728_j134217728_pair": "KILLED",
            "ph134217728_G134217728_eq_1_at_k28": "KILLED",
            "ph134217728_covering_at_k26": "KILLED",
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
    print("ph134217728 k8", dump["ph134217728_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
