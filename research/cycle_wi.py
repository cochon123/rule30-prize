#!/usr/bin/env python3
"""Cycle WI: named leftover extra gpd1/gpd2 closed forms.

gpd1_s is (5*2^{k-2}-2(-1)^k-3)/3 for k>=2.
gpd1_l is 2^{k-2}+(-1)^k for k>=2.
gpd2_s is (5*2^{k-3}+2(-1)^k-3)/3 for k>=3.
gpd2_l is 2^{k-3}-(-1)^k for k>=3.
They sum to Cycle UL gp:d1 / gp:d2 and Cycle WG named gp halves.
Dies at k=3 for gpd1_s/gpd1_l with shift 0 (gpd1_s got 1, not 3;
gpd1_l got 0, not 1). Dies at k=4 for gpd2_s/gpd2_l with shift 0
(gpd2_s got 1, not 3; gpd2_l got 0, not 1). Do not kill gpd1 shift 0
at k=2 or gpd2 shift 0 at k=3: they match. Do not kill gpd1_s sign
at k=8: floor-div masks (105=105); kill that sign at k=7 (52 vs 53).
Dies at k=8 without gpd1_s 5*2^{k-2} (got -2, not 105), without
gpd1_s -3 (got 106, not 105), without gpd1_l 2^{k-2} (got 1, not
65), without gpd1_l sign (got 64, not 65), without gpd2_s 5*2^{k-3}
(got -1, not 53), without gpd2_s sign (got 52, not 53), without
gpd2_s -3 (got 54, not 53), without gpd2_l 2^{k-3} (got -1, not 31),
and without gpd2_l sign (got 32, not 31). Dies at k=8 for gpd1_s
equals tot gp_s (got 105, not 158), gpd1_s equals gpd2_s (got 105,
not 53), gpd1_s equals tot small (got 105, not 266), and gpd1_s
equals gpd1_l (got 105, not 65). Census k=8: gpd1_s 105, gpd1_l 65,
gpd2_s 53, gpd2_l 31. Do not PREFIX pal-center tot. Not rest=S xor
T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_wi.py --certify
Dump: research/cycle_wi.json
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
from cycle_ul import want_gp_d1, want_gp_d2, want_named_lo
from cycle_uo import (
    named_half_split,
    want_gp_d1_large,
    want_gp_d1_small,
    want_gp_d2_large,
    want_gp_d2_small,
)
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vy import want_named_l_fl, want_named_s_fl
from cycle_we import want_ege_fl
from cycle_wg import want_named_gp_l_fl, want_named_gp_s_fl
from cycle_wh import want_sm_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WH_JSON = Path(__file__).resolve().parent / "cycle_wh.json"
UO_JSON = Path(__file__).resolve().parent / "cycle_uo.json"
WG_JSON = Path(__file__).resolve().parent / "cycle_wg.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_gpd1_s_fl(k: int) -> int:
    """named leftover extra g0+pair d=1 on n<=5U/2: (5*2^{k-2}-2(-1)^k-3)/3 for k>=2."""
    if k <= 1:
        return 0
    n = 5 * (1 << (k - 2)) - 2 * ((-1) ** k) - 3
    return n // 3


def want_gpd1_l_fl(k: int) -> int:
    """named leftover extra g0+pair d=1 on n>5U/2: 2^{k-2}+(-1)^k for k>=2."""
    if k <= 1:
        return 0
    return (1 << (k - 2)) + ((-1) ** k)


def want_gpd2_s_fl(k: int) -> int:
    """named leftover extra g0+pair d=2 on n<=5U/2: (5*2^{k-3}+2(-1)^k-3)/3 for k>=3."""
    if k <= 2:
        return 0
    n = 5 * (1 << (k - 3)) + 2 * ((-1) ** k) - 3
    return n // 3


def want_gpd2_l_fl(k: int) -> int:
    """named leftover extra g0+pair d=2 on n>5U/2: 2^{k-3}-(-1)^k for k>=3."""
    if k <= 2:
        return 0
    return (1 << (k - 3)) - ((-1) ** k)


def tot_form() -> dict:
    """k<=64: named leftover extra gpd1/gpd2; dies at k=3/k=4 with shift 0.

    Do not call named_half_split / even_lo_ph_split here.
    Census is named_gpd12_fold for k<=8.
    """
    n_ok = 0
    raw_d1s3 = (5 * 1 - 2 * ((-1) ** 3) - 3) // 3
    raw_d1l3 = 1 + ((-1) ** 3)
    raw_d2s4 = (5 * 1 + 2 * ((-1) ** 4) - 3) // 3
    raw_d2l4 = 1 - ((-1) ** 4)
    miss_d1s_pow = (-2 * ((-1) ** 8) - 3) // 3
    miss_d1s_m3 = (5 * (1 << 6) - 2 * ((-1) ** 8)) // 3
    miss_d1s_sign7 = (5 * (1 << 5) - 3) // 3
    miss_d1l_pow = ((-1) ** 8)
    miss_d1l_sign = 1 << 6
    miss_d2s_pow = (2 * ((-1) ** 8) - 3) // 3
    miss_d2s_sign = (5 * (1 << 5) - 3) // 3
    miss_d2s_m3 = (5 * (1 << 5) + 2 * ((-1) ** 8)) // 3
    miss_d2l_pow = -((-1) ** 8)
    miss_d2l_sign = 1 << 5
    mask_d1s_sign8 = (5 * (1 << 6) - 3) // 3
    if want_gpd1_s_fl(0) != 0 or want_gpd1_s_fl(1) != 0:
        return {"ok": False, "k01": True}
    if want_gpd1_l_fl(2) != 2 or want_gpd2_l_fl(2) != 0:
        return {"ok": False, "k2": True}
    if want_gpd1_s_fl(3) != 3 or want_gpd2_s_fl(3) != 0:
        return {"ok": False, "k3": True}
    if want_gpd1_s_fl(8) != 105 or want_gpd2_s_fl(8) != 53:
        return {"ok": False, "k8": True}
    if want_gpd1_s_fl(3) == raw_d1s3:
        return {"ok": False, "raws": True}
    if want_gpd1_l_fl(3) == raw_d1l3:
        return {"ok": False, "rawl": True}
    if want_gpd2_s_fl(4) == raw_d2s4:
        return {"ok": False, "raw2s": True}
    if want_gpd2_l_fl(4) == raw_d2l4:
        return {"ok": False, "raw2l": True}
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
        if want_gpd1_s_fl(k) != want_gp_d1_small(k):
            return {"ok": False, "d1s": True, "k": k}
        if want_gpd1_l_fl(k) != want_gp_d1_large(k):
            return {"ok": False, "d1l": True, "k": k}
        if want_gpd2_s_fl(k) != want_gp_d2_small(k):
            return {"ok": False, "d2s": True, "k": k}
        if want_gpd2_l_fl(k) != want_gp_d2_large(k):
            return {"ok": False, "d2l": True, "k": k}
        if want_gpd1_s_fl(k) + want_gpd1_l_fl(k) != want_gp_d1(k):
            return {"ok": False, "d1t": True, "k": k}
        if want_gpd2_s_fl(k) + want_gpd2_l_fl(k) != want_gp_d2(k):
            return {"ok": False, "d2t": True, "k": k}
        if want_gpd1_s_fl(k) + want_gpd2_s_fl(k) != want_named_gp_s_fl(k):
            return {"ok": False, "gps": True, "k": k}
        if want_gpd1_l_fl(k) + want_gpd2_l_fl(k) != want_named_gp_l_fl(k):
            return {"ok": False, "gpl": True, "k": k}
        if k >= 2:
            n = 5 * (1 << (k - 2)) - 2 * ((-1) ** k) - 3
            if n % 3 != 0 or n // 3 != want_gpd1_s_fl(k):
                return {"ok": False, "div1": True, "k": k}
        if k >= 3:
            n = 5 * (1 << (k - 3)) + 2 * ((-1) ** k) - 3
            if n % 3 != 0 or n // 3 != want_gpd2_s_fl(k):
                return {"ok": False, "div2": True, "k": k}
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
        and want_gpd1_s_fl(3) != raw_d1s3
        and want_gpd1_l_fl(3) != raw_d1l3
        and want_gpd2_s_fl(4) != raw_d2s4
        and want_gpd2_l_fl(4) != raw_d2l4
        and want_gpd1_s_fl(2) == (5 * 1 - 2 * ((-1) ** 2) - 3) // 3
        and want_gpd1_l_fl(2) == 1 + ((-1) ** 2)
        and want_gpd2_s_fl(3) == (5 * 1 + 2 * ((-1) ** 3) - 3) // 3
        and want_gpd2_l_fl(3) == 1 - ((-1) ** 3)
        and want_gpd1_s_fl(8) != miss_d1s_pow
        and want_gpd1_s_fl(8) != miss_d1s_m3
        and want_gpd1_s_fl(7) != miss_d1s_sign7
        and want_gpd1_s_fl(8) == mask_d1s_sign8
        and want_gpd1_l_fl(8) != miss_d1l_pow
        and want_gpd1_l_fl(8) != miss_d1l_sign
        and want_gpd2_s_fl(8) != miss_d2s_pow
        and want_gpd2_s_fl(8) != miss_d2s_sign
        and want_gpd2_s_fl(8) != miss_d2s_m3
        and want_gpd2_l_fl(8) != miss_d2l_pow
        and want_gpd2_l_fl(8) != miss_d2l_sign
        and want_gpd1_s_fl(8) != want_named_gp_s_fl(8)
        and want_gpd1_s_fl(8) != want_gpd2_s_fl(8)
        and want_gpd1_s_fl(8) != want_named_s_fl(8)
        and want_gpd1_s_fl(8) != want_gpd1_l_fl(8)
        and want_gpd1_s_fl(8) == 105
        and want_gpd1_l_fl(8) == 65
        and want_gpd2_s_fl(8) == 53
        and want_gpd2_l_fl(8) == 31
        and want_named_gp_s_fl(8) == 158
        and want_named_gp_l_fl(8) == 96
        and want_named_s_fl(8) == 266
        and want_named_l_fl(8) == 158
        and want_named_lo(8) == 424
        and want_gp_d1(8) == jacobsthal(9) - 1
        and want_gp_d2(8) == jacobsthal(8) - 1
        and want_sm_fl(8) == 8790
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
        and miss_d1s_pow == -2
        and miss_d1s_m3 == 106
        and miss_d1s_sign7 == 52
        and mask_d1s_sign8 == 105
        and miss_d1l_pow == 1
        and miss_d1l_sign == 64
        and miss_d2s_pow == -1
        and miss_d2s_sign == 52
        and miss_d2s_m3 == 54
        and miss_d2l_pow == -1
        and miss_d2l_sign == 32
        and raw_d1s3 == 1
        and raw_d1l3 == 0
        and raw_d2s4 == 1
        and raw_d2l4 == 0
        and want_gpd1_s_fl(4) == 5
        and want_gpd1_s_fl(5) == 13
        and want_gpd1_l_fl(6) == 17
        and want_gpd2_s_fl(6) == 13
        and want_gpd2_l_fl(7) == 17
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def named_gpd12_fold() -> dict:
    """k<=8 named leftover extra gpd1/gpd2 vs closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = named_half_split(k)
        if a["n_bad"] != 0 or a["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if a["gpd1_s"] != want_gpd1_s_fl(k):
            return {"ok": False, "d1s": True, "k": k, "got": a["gpd1_s"]}
        if a["gpd1_l"] != want_gpd1_l_fl(k):
            return {"ok": False, "d1l": True, "k": k, "got": a["gpd1_l"]}
        if a["gpd2_s"] != want_gpd2_s_fl(k):
            return {"ok": False, "d2s": True, "k": k, "got": a["gpd2_s"]}
        if a["gpd2_l"] != want_gpd2_l_fl(k):
            return {"ok": False, "d2l": True, "k": k, "got": a["gpd2_l"]}
        if a["gpd1_s"] + a["gpd2_s"] != want_named_gp_s_fl(k):
            return {"ok": False, "gps": True, "k": k}
        if a["gpd1_l"] + a["gpd2_l"] != want_named_gp_l_fl(k):
            return {"ok": False, "gpl": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "gpd1_s": a["gpd1_s"],
            "gpd1_l": a["gpd1_l"],
            "gpd2_s": a["gpd2_s"],
            "gpd2_l": a["gpd2_l"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["gpd1_l"] == 2
        and rows["2"]["gpd1_s"] == 0
        and rows["3"]["gpd1_s"] == 3
        and rows["3"]["gpd1_l"] == 1
        and rows["3"]["gpd2_s"] == 0
        and rows["3"]["gpd2_l"] == 2
        and rows["8"]["gpd1_s"] == 105
        and rows["8"]["gpd1_l"] == 65
        and rows["8"]["gpd2_s"] == 53
        and rows["8"]["gpd2_l"] == 31
        and want_gpd1_s_fl(4) == 5
        and want_gpd1_s_fl(5) == 13
        and want_gpd1_l_fl(6) == 17
        and want_gpd2_s_fl(6) == 13
        and want_gpd2_l_fl(7) == 17
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """gpd1 shift 0 at k=3; gpd2 shift 0 at k=4; k=8 missing powers/signs."""
    raw_d1s3 = (5 * 1 - 2 * ((-1) ** 3) - 3) // 3
    raw_d1l3 = 1 + ((-1) ** 3)
    raw_d2s4 = (5 * 1 + 2 * ((-1) ** 4) - 3) // 3
    raw_d2l4 = 1 - ((-1) ** 4)
    miss_d1s_pow = (-2 * ((-1) ** 8) - 3) // 3
    miss_d1s_m3 = (5 * (1 << 6) - 2 * ((-1) ** 8)) // 3
    miss_d1s_sign7 = (5 * (1 << 5) - 3) // 3
    miss_d1l_pow = ((-1) ** 8)
    miss_d1l_sign = 1 << 6
    miss_d2s_pow = (2 * ((-1) ** 8) - 3) // 3
    miss_d2s_sign = (5 * (1 << 5) - 3) // 3
    miss_d2s_m3 = (5 * (1 << 5) + 2 * ((-1) ** 8)) // 3
    miss_d2l_pow = -((-1) ** 8)
    miss_d2l_sign = 1 << 5
    mask_d1s_sign8 = (5 * (1 << 6) - 3) // 3
    a8 = named_half_split(8)
    ok = (
        want_gpd1_s_fl(3) != raw_d1s3
        and want_gpd1_l_fl(3) != raw_d1l3
        and want_gpd2_s_fl(4) != raw_d2s4
        and want_gpd2_l_fl(4) != raw_d2l4
        and want_gpd1_s_fl(2) == (5 * 1 - 2 * ((-1) ** 2) - 3) // 3
        and want_gpd1_l_fl(2) == 1 + ((-1) ** 2)
        and want_gpd2_s_fl(3) == (5 * 1 + 2 * ((-1) ** 3) - 3) // 3
        and want_gpd2_l_fl(3) == 1 - ((-1) ** 3)
        and want_gpd1_s_fl(8) != miss_d1s_pow
        and want_gpd1_s_fl(8) != miss_d1s_m3
        and want_gpd1_s_fl(7) != miss_d1s_sign7
        and want_gpd1_s_fl(8) == mask_d1s_sign8
        and want_gpd1_l_fl(8) != miss_d1l_pow
        and want_gpd1_l_fl(8) != miss_d1l_sign
        and want_gpd2_s_fl(8) != miss_d2s_pow
        and want_gpd2_s_fl(8) != miss_d2s_sign
        and want_gpd2_s_fl(8) != miss_d2s_m3
        and want_gpd2_l_fl(8) != miss_d2l_pow
        and want_gpd2_l_fl(8) != miss_d2l_sign
        and want_gpd1_s_fl(8) != want_named_gp_s_fl(8)
        and want_gpd1_s_fl(8) != want_gpd2_s_fl(8)
        and want_gpd1_s_fl(8) != want_named_s_fl(8)
        and want_gpd1_s_fl(8) != want_gpd1_l_fl(8)
        and a8["gpd1_s"] == 105
        and a8["gpd1_l"] == 65
        and a8["gpd2_s"] == 53
        and a8["gpd2_l"] == 31
        and miss_d1s_pow == -2
        and miss_d1s_m3 == 106
        and miss_d1s_sign7 == 52
        and mask_d1s_sign8 == 105
        and miss_d1l_pow == 1
        and miss_d1l_sign == 64
        and miss_d2s_pow == -1
        and miss_d2s_sign == 52
        and miss_d2s_m3 == 54
        and miss_d2l_pow == -1
        and miss_d2l_sign == 32
        and raw_d1s3 == 1
        and raw_d1l3 == 0
        and raw_d2s4 == 1
        and raw_d2l4 == 0
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
    wh = json.loads(WH_JSON.read_text())
    uo = json.loads(UO_JSON.read_text())
    wg = json.loads(WG_JSON.read_text())
    ok = (
        wh["checks"]["all_ok"]
        and uo["checks"]["all_ok"]
        and wg["checks"]["all_ok"]
        and wh["verdict"]["sm_eq_FL_closed_k_ge_2"] == "LEMMA"
        and uo["verdict"]["gp_d1_half_eq_parent_d1"] == "LEMMA"
        and wg["verdict"]["named_gp_s_eq_closed_k_ge_3"] == "LEMMA"
        and wh["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wh["verdict"]["prize"] == "unsolved"
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
    cnt = named_gpd12_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "named_gpd12_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "gpd1_s_eq_closed_k_ge_2": True,
            "gpd1_l_eq_closed_k_ge_2": True,
            "gpd2_s_eq_closed_k_ge_3": True,
            "gpd2_l_eq_closed_k_ge_3": True,
            "gpd1_halves_eq_gp_d1": True,
            "gpd2_halves_eq_gp_d2": True,
            "gpd12_s_eq_gp_s": True,
            "gpd12_l_eq_gp_l": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "gpd1_s_eq_closed_k_ge_2": "LEMMA",
            "gpd1_l_eq_closed_k_ge_2": "LEMMA",
            "gpd2_s_eq_closed_k_ge_3": "LEMMA",
            "gpd2_l_eq_closed_k_ge_3": "LEMMA",
            "gpd1_halves_eq_gp_d1": "LEMMA",
            "gpd2_halves_eq_gp_d2": "LEMMA",
            "gpd12_s_eq_gp_s": "LEMMA",
            "gpd12_l_eq_gp_l": "LEMMA",
            "gpd1_shift0_at_k3": "KILLED",
            "gpd2_shift0_at_k4": "KILLED",
            "gpd1_s_without_pow_at_k8": "KILLED",
            "gpd1_s_without_m3_at_k8": "KILLED",
            "gpd1_s_without_sign_at_k7": "KILLED",
            "gpd1_l_without_pow_at_k8": "KILLED",
            "gpd1_l_without_sign_at_k8": "KILLED",
            "gpd2_s_without_pow_at_k8": "KILLED",
            "gpd2_s_without_sign_at_k8": "KILLED",
            "gpd2_s_without_m3_at_k8": "KILLED",
            "gpd2_l_without_pow_at_k8": "KILLED",
            "gpd2_l_without_sign_at_k8": "KILLED",
            "gpd1_s_eq_gp_s": "KILLED",
            "gpd1_s_eq_gpd2_s": "KILLED",
            "gpd1_s_eq_named_s": "KILLED",
            "gpd1_s_eq_gpd1_l": "KILLED",
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
        "gpd12 k8",
        dump["named_gpd12_fold"]["rows"]["8"]["gpd1_s"],
        dump["named_gpd12_fold"]["rows"]["8"]["gpd1_l"],
        dump["named_gpd12_fold"]["rows"]["8"]["gpd2_s"],
        dump["named_gpd12_fold"]["rows"]["8"]["gpd2_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
