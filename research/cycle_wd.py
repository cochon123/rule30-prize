#!/usr/bin/env python3
"""Cycle WD: leftover extra xor 4-way F/L closed forms.

pg_s is 2^{k-4}(4 F_k+3 F_{k-2}-5) for k>=4.
gp_s is (2^{k-4}(12 F_k+9 F_{k-2}-35)-2(-1)^{k-1}+3)/3 for k>=4.
pg_l is (2^{k-4}(5 F_{k-2}+16 L_{k-2}-15)+2)/5 for k>=4.
gp_l is (2^{k-4}(5 F_{k-2}+16 L_{k-2}-5)+5(-1)^{k-1}-3)/5 for k>=4.
They sum to Cycle WB leftover extra xor halves and Cycle VZ
n_pg/n_gp. Equal Cycle WC leftover xor 4-way at k-1 for k>=3, not
at k=2. Dies at k=4 for gp_s/pg_l/gp_l F/L forms with shift 0
(gp_s got 1, not 5; pg_l got 0, not 8; gp_l got -2, not 8). Do
not kill pg_s shift 0 at k=4: 2^{0}=1 so it matches. Dies at k=8
without pg_s 2^{k-4} (got 103, not 1648), without gp_s +3 (got
1542, not 1543), without pg_l +2 (got 1001, not 1002), and
without gp_l 5(-1)^{k-1} (got 1033, not 1032). Do not kill without
gp_l -3 at k=8: floor-div masks it. Dies at k=2 for parent leftover
xor 4-way (pg_s got 0, not 1; pg_l got 1, not 0). Dies at k=8 for
pg_s equals tot small (got 1648, not 3191), pg_s equals tot pg
(got 1648, not 2650), and pg_s equals gp_s (got 1648, not 1543).
Special pg_s=3 at k=3; gp_l=2 at k=3; pg_l=1 at k=2 and k=3.
Census k=8: pg_s 1648, gp_s 1543, pg_l 1002, gp_l 1032. Do not
PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wd.py --certify
Dump: research/cycle_wd.json
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
from cycle_tw import want_j0_odd_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vh import want_ej_xor_gp_l, want_ej_xor_gp_s, want_ej_xor_pg_l, want_ej_xor_pg_s
from cycle_vz import want_ej_xor_gp_fl, want_ej_xor_pg_fl
from cycle_wb import want_ej_xor_l_fl, want_ej_xor_s_fl
from cycle_wc import (
    want_xor_gp_l_fl,
    want_xor_gp_s_fl,
    want_xor_pg_l_fl,
    want_xor_pg_s_fl,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WC_JSON = Path(__file__).resolve().parent / "cycle_wc.json"
WB_JSON = Path(__file__).resolve().parent / "cycle_wb.json"
VZ_JSON = Path(__file__).resolve().parent / "cycle_vz.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ej_xor_pg_s_fl(k: int) -> int:
    """leftover extra xor n_pg on n<=5U/2: F form for k>=4; 3 at k=3."""
    if k <= 2:
        return 0
    if k == 3:
        return 3
    return (1 << (k - 4)) * (4 * fib(k) + 3 * fib(k - 2) - 5)


def want_ej_xor_gp_s_fl(k: int) -> int:
    """leftover extra xor n_gp on n<=5U/2: F form for k>=4; 0 at k<=3."""
    if k <= 3:
        return 0
    n = (
        (1 << (k - 4)) * (12 * fib(k) + 9 * fib(k - 2) - 35)
        - 2 * ((-1) ** (k - 1))
        + 3
    )
    return n // 3


def want_ej_xor_pg_l_fl(k: int) -> int:
    """leftover extra xor n_pg on n>5U/2: F/L form for k>=4; 1 at k=2,3."""
    if k <= 1:
        return 0
    if k <= 3:
        return 1
    n = (1 << (k - 4)) * (5 * fib(k - 2) + 16 * lucas(k - 2) - 15) + 2
    return n // 5


def want_ej_xor_gp_l_fl(k: int) -> int:
    """leftover extra xor n_gp on n>5U/2: F/L form for k>=4; 2 at k=3."""
    if k <= 2:
        return 0
    if k == 3:
        return 2
    n = (
        (1 << (k - 4)) * (5 * fib(k - 2) + 16 * lucas(k - 2) - 5)
        + 5 * ((-1) ** (k - 1))
        - 3
    )
    return n // 5


def tot_form() -> dict:
    """k<=64: leftover extra xor 4-way F/L; dies at k=4 with shift 0.

    Do not call leftover_extra_xor_split / leftover_xor_half here.
    Census is ej_4w_fold for k<=8. pg_s shift 0 at k=4 matches.
    """
    n_ok = 0
    raw_gps4 = (-2 * ((-1) ** 3) + 3) // 3
    raw_pgl4 = 2 // 5
    raw_gpl4 = (5 * ((-1) ** 3) - 3) // 5
    miss_pgs_pow = 4 * fib(8) + 3 * fib(6) - 5
    miss_gps3 = (
        (1 << 4) * (12 * fib(8) + 9 * fib(6) - 35) - 2 * ((-1) ** 7)
    ) // 3
    miss_pgl2 = ((1 << 4) * (5 * fib(6) + 16 * lucas(6) - 15)) // 5
    miss_gplsign = (
        (1 << 4) * (5 * fib(6) + 16 * lucas(6) - 5) - 3
    ) // 5
    miss_gplm3 = (
        (1 << 4) * (5 * fib(6) + 16 * lucas(6) - 5) + 5 * ((-1) ** 7)
    ) // 5
    if want_ej_xor_pg_s_fl(0) != 0 or want_ej_xor_pg_s_fl(1) != 0:
        return {"ok": False, "k01": True}
    if want_ej_xor_pg_s_fl(2) != 0 or want_ej_xor_gp_s_fl(2) != 0:
        return {"ok": False, "k2s": True}
    if want_ej_xor_pg_l_fl(2) != 1 or want_ej_xor_gp_l_fl(2) != 0:
        return {"ok": False, "k2l": True}
    if want_ej_xor_pg_s_fl(3) != 3 or want_ej_xor_gp_s_fl(3) != 0:
        return {"ok": False, "k3s": True}
    if want_ej_xor_pg_l_fl(3) != 1 or want_ej_xor_gp_l_fl(3) != 2:
        return {"ok": False, "k3l": True}
    if want_ej_xor_pg_s_fl(4) != 10 or want_ej_xor_gp_s_fl(4) != 5:
        return {"ok": False, "k4s": True}
    if want_ej_xor_pg_l_fl(4) != 8 or want_ej_xor_gp_l_fl(4) != 8:
        return {"ok": False, "k4l": True}
    if want_ej_xor_pg_s_fl(8) != 1648 or want_ej_xor_gp_s_fl(8) != 1543:
        return {"ok": False, "k8s": True}
    if want_ej_xor_pg_l_fl(8) != 1002 or want_ej_xor_gp_l_fl(8) != 1032:
        return {"ok": False, "k8l": True}
    if want_ej_xor_pg_s_fl(8) == miss_pgs_pow:
        return {"ok": False, "pow": True}
    if want_ej_xor_gp_s_fl(4) == raw_gps4:
        return {"ok": False, "rawgs": True}
    if want_ej_xor_pg_l_fl(4) == raw_pgl4:
        return {"ok": False, "rawl": True}
    if want_ej_xor_gp_l_fl(4) == raw_gpl4:
        return {"ok": False, "rawgl": True}
    if want_ej_xor_gp_s_fl(8) == miss_gps3:
        return {"ok": False, "gs3": True}
    if want_ej_xor_pg_l_fl(8) == miss_pgl2:
        return {"ok": False, "pl2": True}
    if want_ej_xor_gp_l_fl(8) == miss_gplsign:
        return {"ok": False, "gls": True}
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
        if want_ej_xor_pg_s_fl(k) != want_ej_xor_pg_s(k):
            return {"ok": False, "ps": True, "k": k}
        if want_ej_xor_gp_s_fl(k) != want_ej_xor_gp_s(k):
            return {"ok": False, "gs": True, "k": k}
        if want_ej_xor_pg_l_fl(k) != want_ej_xor_pg_l(k):
            return {"ok": False, "pl": True, "k": k}
        if want_ej_xor_gp_l_fl(k) != want_ej_xor_gp_l(k):
            return {"ok": False, "gl": True, "k": k}
        if want_ej_xor_pg_s_fl(k) + want_ej_xor_gp_s_fl(k) != want_ej_xor_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if want_ej_xor_pg_l_fl(k) + want_ej_xor_gp_l_fl(k) != want_ej_xor_l_fl(k):
            return {"ok": False, "suml": True, "k": k}
        if want_ej_xor_pg_s_fl(k) + want_ej_xor_pg_l_fl(k) != want_ej_xor_pg_fl(k):
            return {"ok": False, "sump": True, "k": k}
        if want_ej_xor_gp_s_fl(k) + want_ej_xor_gp_l_fl(k) != want_ej_xor_gp_fl(k):
            return {"ok": False, "sumg": True, "k": k}
        if k >= 3:
            if want_ej_xor_pg_s_fl(k) != want_xor_pg_s_fl(k - 1):
                return {"ok": False, "vs": True, "k": k}
            if want_ej_xor_gp_s_fl(k) != want_xor_gp_s_fl(k - 1):
                return {"ok": False, "vg": True, "k": k}
            if want_ej_xor_pg_l_fl(k) != want_xor_pg_l_fl(k - 1):
                return {"ok": False, "vl": True, "k": k}
            if want_ej_xor_gp_l_fl(k) != want_xor_gp_l_fl(k - 1):
                return {"ok": False, "vgl": True, "k": k}
        if k >= 4:
            ns = (
                (1 << (k - 4)) * (12 * fib(k) + 9 * fib(k - 2) - 35)
                - 2 * ((-1) ** (k - 1))
                + 3
            )
            np = (
                (1 << (k - 4)) * (5 * fib(k - 2) + 16 * lucas(k - 2) - 15)
                + 2
            )
            ng = (
                (1 << (k - 4)) * (5 * fib(k - 2) + 16 * lucas(k - 2) - 5)
                + 5 * ((-1) ** (k - 1))
                - 3
            )
            if ns % 3 != 0 or ns // 3 != want_ej_xor_gp_s_fl(k):
                return {"ok": False, "dgs": True, "k": k}
            if np % 5 != 0 or np // 5 != want_ej_xor_pg_l_fl(k):
                return {"ok": False, "dpl": True, "k": k}
            if ng % 5 != 0 or ng // 5 != want_ej_xor_gp_l_fl(k):
                return {"ok": False, "dgl": True, "k": k}
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
        and want_ej_xor_pg_s_fl(8) != miss_pgs_pow
        and want_ej_xor_gp_s_fl(4) != raw_gps4
        and want_ej_xor_pg_l_fl(4) != raw_pgl4
        and want_ej_xor_gp_l_fl(4) != raw_gpl4
        and want_ej_xor_gp_s_fl(8) != miss_gps3
        and want_ej_xor_pg_l_fl(8) != miss_pgl2
        and want_ej_xor_gp_l_fl(8) != miss_gplsign
        and want_ej_xor_gp_l_fl(8) == miss_gplm3
        and want_ej_xor_pg_s_fl(2) != want_xor_pg_s_fl(1)
        and want_ej_xor_pg_l_fl(2) != want_xor_pg_l_fl(1)
        and want_ej_xor_pg_s_fl(8) != want_ej_xor_s_fl(8)
        and want_ej_xor_pg_s_fl(8) != want_ej_xor_pg_fl(8)
        and want_ej_xor_pg_s_fl(8) != want_ej_xor_gp_s_fl(8)
        and want_ej_xor_pg_s_fl(8) == 1648
        and want_ej_xor_gp_s_fl(8) == 1543
        and want_ej_xor_pg_l_fl(8) == 1002
        and want_ej_xor_gp_l_fl(8) == 1032
        and want_ej_xor_s_fl(8) == 3191
        and want_ej_xor_l_fl(8) == 2034
        and want_ej_xor_pg_fl(8) == 2650
        and want_ej_xor_gp_fl(8) == 2575
        and want_ej_xor(8) == 5225
        and want_j0_odd_lo(8) == 319
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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
        and miss_gps3 == 1542
        and miss_pgl2 == 1001
        and miss_gplsign == 1033
        and miss_gplm3 == 1032
        and miss_pgs_pow == 103
        and raw_gps4 == 1
        and raw_pgl4 == 0
        and raw_gpl4 == -2
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ej_4w_fold() -> dict:
    """k<=8 leftover extra xor 4-way vs F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = leftover_extra_xor_split(k)
        if a["sign_bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if a["pg_s"] != want_ej_xor_pg_s_fl(k):
            return {"ok": False, "ps": True, "k": k, "got": a["pg_s"]}
        if a["gp_s"] != want_ej_xor_gp_s_fl(k):
            return {"ok": False, "gs": True, "k": k, "got": a["gp_s"]}
        if a["pg_l"] != want_ej_xor_pg_l_fl(k):
            return {"ok": False, "pl": True, "k": k, "got": a["pg_l"]}
        if a["gp_l"] != want_ej_xor_gp_l_fl(k):
            return {"ok": False, "gl": True, "k": k, "got": a["gp_l"]}
        if a["pg_s"] + a["gp_s"] != want_ej_xor_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if a["pg_l"] + a["gp_l"] != want_ej_xor_l_fl(k):
            return {"ok": False, "suml": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "pg_s": a["pg_s"],
            "gp_s": a["gp_s"],
            "pg_l": a["pg_l"],
            "gp_l": a["gp_l"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["pg_s"] == 0
        and rows["1"]["gp_l"] == 0
        and rows["2"]["pg_s"] == 0
        and rows["2"]["pg_l"] == 1
        and rows["2"]["gp_l"] == 0
        and rows["3"]["pg_s"] == 3
        and rows["3"]["gp_s"] == 0
        and rows["3"]["pg_l"] == 1
        and rows["3"]["gp_l"] == 2
        and rows["8"]["pg_s"] == 1648
        and rows["8"]["gp_s"] == 1543
        and rows["8"]["pg_l"] == 1002
        and rows["8"]["gp_l"] == 1032
        and want_ej_xor_pg_s_fl(4) == 10
        and want_ej_xor_gp_s_fl(5) == 29
        and want_ej_xor_pg_l_fl(5) == 24
        and want_ej_xor_gp_l_fl(6) == 96
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L forms at k=4 with shift 0; pg_s power, gp_s +3, pg_l +2, gp_l sign."""
    raw_gps4 = (-2 * ((-1) ** 3) + 3) // 3
    raw_pgl4 = 2 // 5
    raw_gpl4 = (5 * ((-1) ** 3) - 3) // 5
    miss_pgs_pow = 4 * fib(8) + 3 * fib(6) - 5
    miss_gps3 = (
        (1 << 4) * (12 * fib(8) + 9 * fib(6) - 35) - 2 * ((-1) ** 7)
    ) // 3
    miss_pgl2 = ((1 << 4) * (5 * fib(6) + 16 * lucas(6) - 15)) // 5
    miss_gplsign = (
        (1 << 4) * (5 * fib(6) + 16 * lucas(6) - 5) - 3
    ) // 5
    miss_gplm3 = (
        (1 << 4) * (5 * fib(6) + 16 * lucas(6) - 5) + 5 * ((-1) ** 7)
    ) // 5
    a8 = leftover_extra_xor_split(8)
    ok = (
        want_ej_xor_pg_s_fl(8) != miss_pgs_pow
        and want_ej_xor_gp_s_fl(4) != raw_gps4
        and want_ej_xor_pg_l_fl(4) != raw_pgl4
        and want_ej_xor_gp_l_fl(4) != raw_gpl4
        and want_ej_xor_gp_s_fl(8) != miss_gps3
        and want_ej_xor_pg_l_fl(8) != miss_pgl2
        and want_ej_xor_gp_l_fl(8) != miss_gplsign
        and want_ej_xor_gp_l_fl(8) == miss_gplm3
        and want_ej_xor_pg_s_fl(2) != want_xor_pg_s_fl(1)
        and want_ej_xor_pg_l_fl(2) != want_xor_pg_l_fl(1)
        and want_ej_xor_pg_s_fl(8) != want_ej_xor_s_fl(8)
        and want_ej_xor_pg_s_fl(8) != want_ej_xor_pg_fl(8)
        and want_ej_xor_pg_s_fl(8) != want_ej_xor_gp_s_fl(8)
        and a8["pg_s"] == 1648
        and a8["gp_s"] == 1543
        and a8["pg_l"] == 1002
        and a8["gp_l"] == 1032
        and miss_pgs_pow == 103
        and raw_gps4 == 1
        and raw_pgl4 == 0
        and raw_gpl4 == -2
        and miss_gps3 == 1542
        and miss_pgl2 == 1001
        and miss_gplsign == 1033
        and miss_gplm3 == 1032
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
    wc = json.loads(WC_JSON.read_text())
    wb = json.loads(WB_JSON.read_text())
    vz = json.loads(VZ_JSON.read_text())
    ok = (
        wc["checks"]["all_ok"]
        and wb["checks"]["all_ok"]
        and vz["checks"]["all_ok"]
        and wc["verdict"]["xor_pg_s_eq_FL_closed_k_ge_3"] == "LEMMA"
        and wb["verdict"]["ej_xor_s_eq_FL_closed_k_ge_3"] == "LEMMA"
        and vz["verdict"]["ej_xor_pg_eq_FL_closed_k_ge_3"] == "LEMMA"
        and wc["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wc["verdict"]["prize"] == "unsolved"
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
    cnt = ej_4w_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ej_4w_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ej_xor_pg_s_eq_FL_closed_k_ge_4": True,
            "ej_xor_gp_s_eq_FL_closed_k_ge_4": True,
            "ej_xor_pg_l_eq_FL_closed_k_ge_4": True,
            "ej_xor_gp_l_eq_FL_closed_k_ge_4": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ej_xor_pg_s_eq_FL_closed_k_ge_4": "LEMMA",
            "ej_xor_gp_s_eq_FL_closed_k_ge_4": "LEMMA",
            "ej_xor_pg_l_eq_FL_closed_k_ge_4": "LEMMA",
            "ej_xor_gp_l_eq_FL_closed_k_ge_4": "LEMMA",
            "ej_xor_4w_FL_shift0_at_k4": "KILLED",
            "ej_xor_pg_s_without_pow_at_k8": "KILLED",
            "ej_xor_gp_s_without_plus3_at_k8": "KILLED",
            "ej_xor_pg_l_without_plus2_at_k8": "KILLED",
            "ej_xor_gp_l_without_sign_at_k8": "KILLED",
            "ej_xor_4w_eq_parent_xor_4w_at_k2": "KILLED",
            "ej_xor_pg_s_eq_ej_xor_s": "KILLED",
            "ej_xor_pg_s_eq_ej_xor_pg": "KILLED",
            "ej_xor_pg_s_eq_ej_xor_gp_s": "KILLED",
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
        dump["ej_4w_fold"]["rows"]["8"]["pg_s"],
        dump["ej_4w_fold"]["rows"]["8"]["gp_s"],
        dump["ej_4w_fold"]["rows"]["8"]["pg_l"],
        dump["ej_4w_fold"]["rows"]["8"]["gp_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
