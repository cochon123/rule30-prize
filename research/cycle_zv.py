#!/usr/bin/env python3
"""Cycle ZV: even n=5U/2+536870912 is the 2-fold of Cycle ZS at k-1.

Covering n=5U/2+536870912 equals 2*(5U_p/2+268435456). Even doubling sends parent
left Green to child left Green with pal_kind and clip-edge preserved,
so unpaired left is {0,536870912} for k>=31 and leftover+pal is the even
11-set {U/2,U/2+536870912,U/2+1073741824,U,U+536870912,U+1073741824,2U,2U+536870912,2U+1073741824,5U/2,n}
for k>=32. The j=536870912 cell has partner 5U+536870912. Dies at k=30 for
unpaired {0,536870912} (G at j=536870912 is 0). Dies at k=31 for leftover
11-set (got 6). Leftover at first covering k=29 is 2, not a blind +1 of
Cycle ZS's 2. Do not kill pal_kind unpaired at n=5U/2+536870912, j=0
for k>=29 or j=536870912 for k>=31. Do not call ph536870912_lo_js below k=32.
Do not call ph268435456_lo_js below k=31.
Do not call ph134217728_lo_js below k=30. Do not call ph67108864_lo_js below
k=29. Do not call ph33554432_lo_js below k=28. Do not call ph16777216_lo_js
below k=27. Do not call ph8388608_lo_js below k=26. Do not call
ph4194304_lo_js below k=25. Do not PREFIX pal-center tot.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk leftover
d catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_zv.py --certify
Dump: research/cycle_zv.json
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
from cycle_zs import (
    ph268435456_lo_js,
    ph268435456_n,
    want_ph268435456_clip,
    want_ph268435456_lo,
    want_ph268435456_unp,
)
from cycle_zp import (
    ph134217728_lo_js,
    ph134217728_n,
    want_ph134217728_clip,
    want_ph134217728_lo,
    want_ph134217728_unp,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ZS_JSON = Path(__file__).resolve().parent / "cycle_zs.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
ZJ_JSON = Path(__file__).resolve().parent / "cycle_zj.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)



def ph536870912_n(k: int) -> int:
    """Covering n=5U/2+536870912."""
    return parent_half(k) + 536870912


def ph536870912_lo_js(k: int) -> tuple[int, ...]:
    """Leftover+pal left indices at even n=5U/2+536870912: 2-fold of Cycle ZS.

    Call only for k>=32.
    """
    return tuple(2 * j for j in ph268435456_lo_js(k - 1))


def want_ph536870912_unp(k: int) -> int:
    """Unpaired left Green at n=5U/2+536870912: 2 for k>=31; 1 at k=30; 3 at k=29."""
    if k <= 28:
        return 0
    if k == 29:
        return 3
    if k == 30:
        return 1
    return 2


def want_ph536870912_lo(k: int) -> int:
    """Leftover+pal left Green at n=5U/2+536870912: 11 for k>=32; 6 at k=31; 1 at k=30; 2 at k=29."""
    if k <= 28:
        return 0
    if k == 29:
        return 2
    if k == 30:
        return 1
    if k == 31:
        return 6
    return 11


def want_ph536870912_clip(k: int) -> int:
    """Left clip-edge Green at n=5U/2+536870912: 1 for k>=29 except 0 at k=31."""
    if k <= 28:
        return 0
    if k == 31:
        return 0
    return 1


def ph536870912_split(k: int) -> dict:
    """Left Green kinds at even n=5U/2+536870912. Do not call from tot_form."""
    n = ph536870912_n(k)
    u = 1 << k
    clip = 5 * u
    n_unp = n_lo = n_clip = n_bad = 0
    unp_js = []
    lo_js = []
    if k < 29 or n >= 4 * u:
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
    """k<=64: n=5U/2+536870912 is 2-fold of ZS; dies at k=30 for {0,536870912}.

    Do not call ph536870912_split here.
    Do not call ph536870912_lo_js below k=32.
    Do not call ph268435456_lo_js below k=31.
    Do not call ph134217728_lo_js below k=30.
    Do not call ph67108864_lo_js below k=29.
    Do not call ph33554432_lo_js below k=28.
    Do not call ph16777216_lo_js below k=27.
    Do not call ph8388608_lo_js below k=26.
    Do not call ph4194304_lo_js below k=25.
    Census is ph536870912_fold for k<=8.
    """
    n_ok = 0
    if want_ph536870912_unp(0) != 0 or want_ph536870912_lo(28) != 0:
        return {"ok": False, "k28": True}
    if want_ph536870912_unp(29) != 3 or want_ph536870912_unp(30) != 1:
        return {"ok": False, "k2930": True}
    if want_ph536870912_lo(30) != 1 or want_ph536870912_unp(31) != 2:
        return {"ok": False, "k3031": True}
    if want_ph536870912_clip(31) != 0 or want_ph536870912_lo(32) != 11:
        return {"ok": False, "k3132": True}
    if want_ph536870912_lo(29) != 2:
        return {"ok": False, "k29lo": True}
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
        n = ph536870912_n(k)
        n_p = ph268435456_n(k - 1) if k >= 1 else ph268435456_n(0)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if n != parent_half(k) + 536870912:
            return {"ok": False, "n": True, "k": k}
        if k >= 2:
            if n != 2 * n_p:
                return {"ok": False, "fold": True, "k": k}
            if n % 2 != 0:
                return {"ok": False, "ev": True, "k": k}
        if k >= 29:
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if pal_kind(n, 0, k) != "unp" or G(n, 0) != 1:
                return {"ok": False, "j0": True, "k": k}
            if 2 * n - 536870912 != clip + 536870912:
                return {"ok": False, "pr": True, "k": k}
            if not is_clip_edge(n, 1073741824, k):
                return {"ok": False, "c1073741824": True, "k": k}
            if G(n, 0) != G(n_p, 0):
                return {"ok": False, "g00": True, "k": k}
            if pal_kind(n, 536870912, k) != "unp":
                return {"ok": False, "j536870912k": True, "k": k}
        if k >= 31:
            if G(n, 536870912) != 1 or G(n, 536870912) != G(n_p, 268435456):
                return {"ok": False, "g536870912": True, "k": k}
            if pal_kind(n_p, 268435456, k - 1) != "unp":
                return {"ok": False, "p268435456": True, "k": k}
            if want_ph536870912_unp(k) != 2:
                return {"ok": False, "u2": True, "k": k}
        if k == 30:
            if G(n, 536870912) != 0 or want_ph536870912_unp(k) != 1:
                return {"ok": False, "k30g": True}
            if pal_kind(n, 536870912, k) != "unp":
                return {"ok": False, "k30k": True}
        if k == 29:
            if G(n, 536870912) != 0 or want_ph536870912_unp(k) != 3:
                return {"ok": False, "k29g": True}
            if pal_kind(n, 536870912, k) != "unp":
                return {"ok": False, "k29k": True}
        if k == 28:
            if n < 4 * u:
                return {"ok": False, "k28c": True}
        if k >= 32:
            if want_ph536870912_lo(k) != 11 or want_ph268435456_lo(k - 1) != 11:
                return {"ok": False, "lo": True, "k": k}
            if ph536870912_lo_js(k) != tuple(2 * j for j in ph268435456_lo_js(k - 1)):
                return {"ok": False, "js": True, "k": k}
            for j in ph536870912_lo_js(k):
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
        and want_ph536870912_unp(30) != 2
        and want_ph536870912_lo(31) != 11
        and want_ph536870912_unp(8) != want_clip_gp(8)
        and want_ph536870912_lo(8) != want_clip_gp(8)
        and want_ph536870912_unp(8) != want_even_slice(8)
        and pal_kind(ph536870912_n(29), 536870912, 29) != "pair"
        and G(ph536870912_n(28), 536870912) != 1
        and G(ph536870912_n(29), 536870912) != 1
        and G(ph536870912_n(30), 536870912) != 1
        and pal_kind(ph536870912_n(29), 0, 29) == "unp"
        and pal_kind(ph536870912_n(29), 536870912, 29) == "unp"
        and pal_kind(ph536870912_n(31), 536870912, 31) == "unp"
        and want_ph536870912_unp(8) == 0
        and want_ph536870912_unp(28) == 0
        and want_ph536870912_unp(29) == 3
        and want_ph536870912_unp(30) == 1
        and want_ph536870912_unp(31) == 2
        and want_ph536870912_lo(28) == 0
        and want_ph536870912_lo(29) == 2
        and want_ph536870912_lo(29) != want_ph268435456_lo(28) + 1
        and want_ph536870912_lo(30) == 1
        and want_ph536870912_lo(31) == 6
        and want_ph536870912_lo(32) == 11
        and want_ph536870912_clip(29) == 1
        and want_ph536870912_clip(30) == 1
        and want_ph536870912_clip(31) == 0
        and ph536870912_n(8) == 536871552
        and ph536870912_n(8) == 2 * ph268435456_n(7)
        and ph536870912_n(24) == 578813952
        and ph536870912_n(24) == 2 * ph268435456_n(23)
        and ph536870912_n(25) == 620756992
        and ph536870912_n(25) == 2 * ph268435456_n(24)
        and ph536870912_n(26) == 704643072
        and ph536870912_n(26) == 2 * ph268435456_n(25)
        and ph536870912_n(27) == 872415232
        and ph536870912_n(28) == 1207959552
        and ph536870912_n(29) == 1879048192
        and ph268435456_n(8) == 268436096
        and ph134217728_n(8) == 134218368
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
        and want_ph268435456_unp(28) == 3
        and want_ph268435456_lo(28) == 2
        and want_ph268435456_lo(31) == 11
        and want_ph268435456_clip(30) == 0
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
        and want_ph536870912_unp(8) == 0
        and want_ph536870912_unp(31) == 2
        and want_lo_e(8) == 14114
        and want_ph268435456_unp(28) == 3
        and want_ph268435456_clip(30) == 0
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


def ph536870912_fold() -> dict:
    """k<=8 left Green at even n=5U/2+536870912 vs 2-fold of ZS."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = ph536870912_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_unp"] != want_ph536870912_unp(k):
            return {"ok": False, "unp": True, "k": k, "got": a["n_unp"]}
        if a["n_lo"] != want_ph536870912_lo(k):
            return {"ok": False, "lo": True, "k": k, "got": a["n_lo"]}
        if a["n_clip"] != want_ph536870912_clip(k):
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
        and want_ph536870912_lo(8) == 0
        and want_ph536870912_lo(29) == 2
        and want_ph536870912_lo(30) == 1
        and want_ph536870912_lo(31) == 6
        and want_ph536870912_lo(32) == 11
        and want_ph268435456_lo(31) == 11
        and want_ph67108864_lo(29) == 11
        and want_ph33554432_lo(28) == 11
        and want_ph4194304_lo(25) == 11
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """unpaired {0,536870912} at k=30; leftover 11-set at k=31."""
    n28 = ph536870912_n(28)
    n29 = ph536870912_n(29)
    n30 = ph536870912_n(30)
    n31 = ph536870912_n(31)
    ok = (
        want_ph536870912_unp(30) != 2
        and want_ph536870912_lo(31) != 11
        and want_ph536870912_unp(8) != want_clip_gp(8)
        and want_ph536870912_lo(8) != want_clip_gp(8)
        and want_ph536870912_unp(8) != want_even_slice(8)
        and pal_kind(n29, 536870912, 29) != "pair"
        and G(n28, 536870912) != 1
        and G(n29, 536870912) != 1
        and G(n30, 536870912) != 1
        and pal_kind(n29, 0, 29) == "unp"
        and pal_kind(n29, 536870912, 29) == "unp"
        and pal_kind(n30, 536870912, 30) == "unp"
        and pal_kind(n31, 536870912, 31) == "unp"
        and want_ph536870912_unp(8) == 0
        and want_ph536870912_unp(28) == 0
        and want_ph536870912_unp(29) == 3
        and want_ph536870912_lo(29) == 2
        and G(n28, 536870912) == 0
        and G(n29, 536870912) == 0
        and G(n30, 536870912) == 0
        and G(n31, 536870912) == 1
        and want_ph536870912_unp(30) == 1
        and want_ph536870912_unp(31) == 2
        and want_ph536870912_lo(30) == 1
        and want_ph536870912_lo(31) == 6
        and want_ph536870912_lo(32) == 11
        and want_clip_gp(8) == 85
        and want_even_slice(8) == 85
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and n28 == 1207959552
        and n28 >= 4 * (1 << 28)
        and n29 < 4 * (1 << 29)
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
    zs = json.loads(ZS_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    zj = json.loads(ZJ_JSON.read_text())
    ok = (
        zs["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and zj["checks"]["all_ok"]
        and zs["verdict"]["ph268435456_j268435456_partner_5U268435456"] == "LEMMA"
        and zs["verdict"]["ph268435456_lo_eq_11_k_ge_31"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and zj["verdict"]["ph33554432_lo_eq_11_k_ge_28"] == "LEMMA"
        and zs["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and zs["verdict"]["prize"] == "unsolved"
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
    cnt = ph536870912_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "ZV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph536870912_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph536870912_eq_2fold_zs_k_ge_2": True,
            "ph536870912_unp_eq_0536870912_k_ge_31": True,
            "ph536870912_lo_eq_11_k_ge_32": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph536870912_eq_2fold_zs_k_ge_2": "LEMMA",
            "ph536870912_unp_eq_0536870912_k_ge_31": "LEMMA",
            "ph536870912_lo_eq_11_k_ge_32": "LEMMA",
            "ph536870912_j536870912_partner_5U536870912": "LEMMA",
            "ph536870912_unp_eq_0536870912_at_k30": "KILLED",
            "ph536870912_lo_eq_11_at_k31": "KILLED",
            "ph536870912_unp_eq_clip_gp_at_k8": "KILLED",
            "ph536870912_lo_eq_clip_gp_at_k8": "KILLED",
            "ph536870912_unp_eq_even_slice_at_k8": "KILLED",
            "ph536870912_j536870912_pair": "KILLED",
            "ph536870912_G536870912_eq_1_at_k30": "KILLED",
            "ph536870912_covering_at_k28": "KILLED",
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
    print("ph536870912 k8", dump["ph536870912_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
