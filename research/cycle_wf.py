#!/usr/bin/env python3
"""Cycle WF: leftover-parent xor 4-way F/L closed forms.

plo_s is (2^{k-3}(33 F_k-21 F_{k-2}-25)+4(-1)^{k-1})/3 for k>=3.
glo_s is (2^{k-3}(33 F_k-21 F_{k-2}-50)+2(-1)^{k-1}+9)/3 for k>=3.
plo_l is (2^{k-3}(21 F_k+11 F_{k-2}-25)-10(-1)^{k-1}+2)/5 for k>=3.
glo_l is (2^{k-3}(21 F_k+11 F_{k-2}-20)-5(-1)^{k-1}-3)/5 for k>=3.
They sum to Cycle VU leftover-parent xor halves and Cycle VX
n_pg/n_gp. plo_s is 2 sm(k-1) and plo_l is 2 e_ge(k-1) for k>=3,
not at k=2 (plo_s got 1, not 2; plo_l got 1, not 0). Dies at k=3
for all four F/L forms with shift 0 (plo_s got 1, not 8; glo_s
got 3, not 2; plo_l got -2, not 4; glo_l got -2, not 5). Dies at
k=8 without plo_s 2^{k-3} (got 165, not 5332), without plo_s
4(-1)^{k-1} (got 5333, not 5332), without glo_s +9 (got 5066, not
5069), without plo_l +2 (got 3227, not 3228), without plo_l
-10(-1)^{k-1} (got 3226, not 3228), and without glo_l
-5(-1)^{k-1} (got 3257, not 3258). Dies at k=7 without glo_s
2(-1)^{k-1} (got 1464, not 1465). Do not kill glo_s sign at k=8
or glo_l -3 at k=8: floor-div masks them. Dies at k=8 for plo_s
equals tot small (got 5332, not 10401), plo_s equals tot pg (got
5332, not 8560), and plo_s equals glo_s (got 5332, not 5069).
Special plo_s=plo_l=1 at k=2. Census k=8: plo_s 5332, glo_s 5069,
plo_l 3228, glo_l 3258. Do not PREFIX pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_wf.py --certify
Dump: research/cycle_wf.json
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
from cycle_uo import named_half_split
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vu import want_lo_parent_l_fl, want_lo_parent_s_fl
from cycle_vx import want_gp_lo_fl, want_pg_lo_fl
from cycle_we import want_ege_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WE_JSON = Path(__file__).resolve().parent / "cycle_we.json"
VU_JSON = Path(__file__).resolve().parent / "cycle_vu.json"
VX_JSON = Path(__file__).resolve().parent / "cycle_vx.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_plo_s_fl(k: int) -> int:
    """leftover-parent xor n_pg on n<=5U/2: F form for k>=3; 1 at k=2."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    n = (
        (1 << (k - 3)) * (33 * fib(k) - 21 * fib(k - 2) - 25)
        + 4 * ((-1) ** (k - 1))
    )
    return n // 3


def want_glo_s_fl(k: int) -> int:
    """leftover-parent xor n_gp on n<=5U/2: F form for k>=3; 0 at k<=2."""
    if k <= 2:
        return 0
    n = (
        (1 << (k - 3)) * (33 * fib(k) - 21 * fib(k - 2) - 50)
        + 2 * ((-1) ** (k - 1))
        + 9
    )
    return n // 3


def want_plo_l_fl(k: int) -> int:
    """leftover-parent xor n_pg on n>5U/2: F form for k>=3; 1 at k=2."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    n = (
        (1 << (k - 3)) * (21 * fib(k) + 11 * fib(k - 2) - 25)
        - 10 * ((-1) ** (k - 1))
        + 2
    )
    return n // 5


def want_glo_l_fl(k: int) -> int:
    """leftover-parent xor n_gp on n>5U/2: F form for k>=3; 0 at k<=2."""
    if k <= 2:
        return 0
    n = (
        (1 << (k - 3)) * (21 * fib(k) + 11 * fib(k - 2) - 20)
        - 5 * ((-1) ** (k - 1))
        - 3
    )
    return n // 5


def tot_form() -> dict:
    """k<=64: leftover-parent xor 4-way F/L; dies at k=3 with shift 0.

    Do not call named_half_split / leftover_xor_half here.
    Census is par_4w_fold for k<=8.
    """
    n_ok = 0
    raw_ps3 = (4 * ((-1) ** 2)) // 3
    raw_gs3 = (2 * ((-1) ** 2) + 9) // 3
    raw_pl3 = (-10 * ((-1) ** 2) + 2) // 5
    raw_gl3 = (-5 * ((-1) ** 2) - 3) // 5
    miss_ps_pow = (33 * fib(8) - 21 * fib(6) - 25 + 4 * ((-1) ** 7)) // 3
    miss_ps_sign = ((1 << 5) * (33 * fib(8) - 21 * fib(6) - 25)) // 3
    miss_gs9 = (
        (1 << 5) * (33 * fib(8) - 21 * fib(6) - 50) + 2 * ((-1) ** 7)
    ) // 3
    miss_gs_sign8 = ((1 << 5) * (33 * fib(8) - 21 * fib(6) - 50) + 9) // 3
    miss_gs_sign7 = ((1 << 4) * (33 * fib(7) - 21 * fib(5) - 50) + 9) // 3
    miss_pl2 = (
        (1 << 5) * (21 * fib(8) + 11 * fib(6) - 25) - 10 * ((-1) ** 7)
    ) // 5
    miss_pl_sign = ((1 << 5) * (21 * fib(8) + 11 * fib(6) - 25) + 2) // 5
    miss_gl3 = (
        (1 << 5) * (21 * fib(8) + 11 * fib(6) - 20) - 5 * ((-1) ** 7)
    ) // 5
    miss_gl_sign = ((1 << 5) * (21 * fib(8) + 11 * fib(6) - 20) - 3) // 5
    if want_plo_s_fl(0) != 0 or want_plo_s_fl(1) != 0:
        return {"ok": False, "k01": True}
    if want_plo_s_fl(2) != 1 or want_glo_s_fl(2) != 0:
        return {"ok": False, "k2s": True}
    if want_plo_l_fl(2) != 1 or want_glo_l_fl(2) != 0:
        return {"ok": False, "k2l": True}
    if want_plo_s_fl(3) != 8 or want_glo_s_fl(3) != 2:
        return {"ok": False, "k3s": True}
    if want_plo_l_fl(3) != 4 or want_glo_l_fl(3) != 5:
        return {"ok": False, "k3l": True}
    if want_plo_s_fl(8) != 5332 or want_glo_s_fl(8) != 5069:
        return {"ok": False, "k8s": True}
    if want_plo_l_fl(8) != 3228 or want_glo_l_fl(8) != 3258:
        return {"ok": False, "k8l": True}
    if want_plo_s_fl(3) == raw_ps3:
        return {"ok": False, "rawps": True}
    if want_glo_s_fl(3) == raw_gs3:
        return {"ok": False, "rawgs": True}
    if want_plo_l_fl(3) == raw_pl3:
        return {"ok": False, "rawpl": True}
    if want_glo_l_fl(3) == raw_gl3:
        return {"ok": False, "rawgl": True}
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
        if want_plo_s_fl(k) + want_glo_s_fl(k) != want_lo_parent_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if want_plo_l_fl(k) + want_glo_l_fl(k) != want_lo_parent_l_fl(k):
            return {"ok": False, "suml": True, "k": k}
        if want_plo_s_fl(k) + want_plo_l_fl(k) != want_pg_lo_fl(k):
            return {"ok": False, "sump": True, "k": k}
        if want_glo_s_fl(k) + want_glo_l_fl(k) != want_gp_lo_fl(k):
            return {"ok": False, "sumg": True, "k": k}
        if k >= 3:
            if want_plo_s_fl(k) != 2 * want_sm(k - 1):
                return {"ok": False, "sm": True, "k": k}
            if want_plo_l_fl(k) != 2 * want_ege_fl(k - 1):
                return {"ok": False, "ege": True, "k": k}
            ns = (
                (1 << (k - 3)) * (33 * fib(k) - 21 * fib(k - 2) - 25)
                + 4 * ((-1) ** (k - 1))
            )
            ngs = (
                (1 << (k - 3)) * (33 * fib(k) - 21 * fib(k - 2) - 50)
                + 2 * ((-1) ** (k - 1))
                + 9
            )
            npl = (
                (1 << (k - 3)) * (21 * fib(k) + 11 * fib(k - 2) - 25)
                - 10 * ((-1) ** (k - 1))
                + 2
            )
            ngl = (
                (1 << (k - 3)) * (21 * fib(k) + 11 * fib(k - 2) - 20)
                - 5 * ((-1) ** (k - 1))
                - 3
            )
            if ns % 3 != 0 or ns // 3 != want_plo_s_fl(k):
                return {"ok": False, "dps": True, "k": k}
            if ngs % 3 != 0 or ngs // 3 != want_glo_s_fl(k):
                return {"ok": False, "dgs": True, "k": k}
            if npl % 5 != 0 or npl // 5 != want_plo_l_fl(k):
                return {"ok": False, "dpl": True, "k": k}
            if ngl % 5 != 0 or ngl // 5 != want_glo_l_fl(k):
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
        and want_plo_s_fl(3) != raw_ps3
        and want_glo_s_fl(3) != raw_gs3
        and want_plo_l_fl(3) != raw_pl3
        and want_glo_l_fl(3) != raw_gl3
        and want_plo_s_fl(8) != miss_ps_pow
        and want_plo_s_fl(8) != miss_ps_sign
        and want_glo_s_fl(8) != miss_gs9
        and want_glo_s_fl(8) == miss_gs_sign8
        and want_glo_s_fl(7) != miss_gs_sign7
        and want_plo_l_fl(8) != miss_pl2
        and want_plo_l_fl(8) != miss_pl_sign
        and want_glo_l_fl(8) == miss_gl3
        and want_glo_l_fl(8) != miss_gl_sign
        and want_plo_s_fl(2) != 2 * want_sm(1)
        and want_plo_l_fl(2) != 2 * want_ege_fl(1)
        and want_plo_s_fl(8) != want_lo_parent_s_fl(8)
        and want_plo_s_fl(8) != want_pg_lo_fl(8)
        and want_plo_s_fl(8) != want_glo_s_fl(8)
        and want_plo_s_fl(8) == 5332
        and want_glo_s_fl(8) == 5069
        and want_plo_l_fl(8) == 3228
        and want_glo_l_fl(8) == 3258
        and want_lo_parent_s_fl(8) == 10401
        and want_lo_parent_l_fl(8) == 6486
        and want_pg_lo_fl(8) == 8560
        and want_gp_lo_fl(8) == 8327
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
        and miss_ps_pow == 165
        and miss_ps_sign == 5333
        and miss_gs9 == 5066
        and miss_gs_sign8 == 5069
        and miss_gs_sign7 == 1464
        and miss_pl2 == 3227
        and miss_pl_sign == 3226
        and miss_gl3 == 3258
        and miss_gl_sign == 3257
        and raw_ps3 == 1
        and raw_gs3 == 3
        and raw_pl3 == -2
        and raw_gl3 == -2
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def par_4w_fold() -> dict:
    """k<=8 leftover-parent xor 4-way vs F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = named_half_split(k)
        if a["n_bad"] != 0 or a["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if a["plo_s"] != want_plo_s_fl(k):
            return {"ok": False, "ps": True, "k": k, "got": a["plo_s"]}
        if a["glo_s"] != want_glo_s_fl(k):
            return {"ok": False, "gs": True, "k": k, "got": a["glo_s"]}
        if a["plo_l"] != want_plo_l_fl(k):
            return {"ok": False, "pl": True, "k": k, "got": a["plo_l"]}
        if a["glo_l"] != want_glo_l_fl(k):
            return {"ok": False, "gl": True, "k": k, "got": a["glo_l"]}
        if a["plo_s"] + a["glo_s"] != want_lo_parent_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if a["plo_l"] + a["glo_l"] != want_lo_parent_l_fl(k):
            return {"ok": False, "suml": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "plo_s": a["plo_s"],
            "glo_s": a["glo_s"],
            "plo_l": a["plo_l"],
            "glo_l": a["glo_l"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["plo_s"] == 0
        and rows["1"]["glo_l"] == 0
        and rows["2"]["plo_s"] == 1
        and rows["2"]["plo_l"] == 1
        and rows["2"]["glo_s"] == 0
        and rows["3"]["plo_s"] == 8
        and rows["3"]["glo_s"] == 2
        and rows["3"]["plo_l"] == 4
        and rows["3"]["glo_l"] == 5
        and rows["8"]["plo_s"] == 5332
        and rows["8"]["glo_s"] == 5069
        and rows["8"]["plo_l"] == 3228
        and rows["8"]["glo_l"] == 3258
        and want_plo_s_fl(4) == 34
        and want_glo_s_fl(5) == 101
        and want_plo_l_fl(5) == 80
        and want_glo_l_fl(6) == 290
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L forms at k=3 with shift 0; plo_s power/sign, glo_s +9, large."""
    raw_ps3 = (4 * ((-1) ** 2)) // 3
    raw_gs3 = (2 * ((-1) ** 2) + 9) // 3
    raw_pl3 = (-10 * ((-1) ** 2) + 2) // 5
    raw_gl3 = (-5 * ((-1) ** 2) - 3) // 5
    miss_ps_pow = (33 * fib(8) - 21 * fib(6) - 25 + 4 * ((-1) ** 7)) // 3
    miss_ps_sign = ((1 << 5) * (33 * fib(8) - 21 * fib(6) - 25)) // 3
    miss_gs9 = (
        (1 << 5) * (33 * fib(8) - 21 * fib(6) - 50) + 2 * ((-1) ** 7)
    ) // 3
    miss_gs_sign8 = ((1 << 5) * (33 * fib(8) - 21 * fib(6) - 50) + 9) // 3
    miss_gs_sign7 = ((1 << 4) * (33 * fib(7) - 21 * fib(5) - 50) + 9) // 3
    miss_pl2 = (
        (1 << 5) * (21 * fib(8) + 11 * fib(6) - 25) - 10 * ((-1) ** 7)
    ) // 5
    miss_pl_sign = ((1 << 5) * (21 * fib(8) + 11 * fib(6) - 25) + 2) // 5
    miss_gl3 = (
        (1 << 5) * (21 * fib(8) + 11 * fib(6) - 20) - 5 * ((-1) ** 7)
    ) // 5
    miss_gl_sign = ((1 << 5) * (21 * fib(8) + 11 * fib(6) - 20) - 3) // 5
    a8 = named_half_split(8)
    ok = (
        want_plo_s_fl(3) != raw_ps3
        and want_glo_s_fl(3) != raw_gs3
        and want_plo_l_fl(3) != raw_pl3
        and want_glo_l_fl(3) != raw_gl3
        and want_plo_s_fl(8) != miss_ps_pow
        and want_plo_s_fl(8) != miss_ps_sign
        and want_glo_s_fl(8) != miss_gs9
        and want_glo_s_fl(8) == miss_gs_sign8
        and want_glo_s_fl(7) != miss_gs_sign7
        and want_plo_l_fl(8) != miss_pl2
        and want_plo_l_fl(8) != miss_pl_sign
        and want_glo_l_fl(8) == miss_gl3
        and want_glo_l_fl(8) != miss_gl_sign
        and want_plo_s_fl(2) != 2 * want_sm(1)
        and want_plo_l_fl(2) != 2 * want_ege_fl(1)
        and want_plo_s_fl(8) != want_lo_parent_s_fl(8)
        and want_plo_s_fl(8) != want_pg_lo_fl(8)
        and want_plo_s_fl(8) != want_glo_s_fl(8)
        and a8["plo_s"] == 5332
        and a8["glo_s"] == 5069
        and a8["plo_l"] == 3228
        and a8["glo_l"] == 3258
        and miss_ps_pow == 165
        and miss_ps_sign == 5333
        and miss_gs9 == 5066
        and miss_gs_sign8 == 5069
        and miss_gs_sign7 == 1464
        and miss_pl2 == 3227
        and miss_pl_sign == 3226
        and miss_gl3 == 3258
        and miss_gl_sign == 3257
        and raw_ps3 == 1
        and raw_gs3 == 3
        and raw_pl3 == -2
        and raw_gl3 == -2
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
    we = json.loads(WE_JSON.read_text())
    vu = json.loads(VU_JSON.read_text())
    vx = json.loads(VX_JSON.read_text())
    ok = (
        we["checks"]["all_ok"]
        and vu["checks"]["all_ok"]
        and vx["checks"]["all_ok"]
        and we["verdict"]["ege_eq_FL_closed_k_ge_3"] == "LEMMA"
        and vu["verdict"]["lo_parent_s_eq_FL_closed_k_ge_3"] == "LEMMA"
        and vx["verdict"]["pg_lo_eq_FL_closed_k_ge_2"] == "LEMMA"
        and we["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and we["verdict"]["prize"] == "unsolved"
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
    cnt = par_4w_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "par_4w_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "plo_s_eq_FL_closed_k_ge_3": True,
            "glo_s_eq_FL_closed_k_ge_3": True,
            "plo_l_eq_FL_closed_k_ge_3": True,
            "glo_l_eq_FL_closed_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "plo_s_eq_FL_closed_k_ge_3": "LEMMA",
            "glo_s_eq_FL_closed_k_ge_3": "LEMMA",
            "plo_l_eq_FL_closed_k_ge_3": "LEMMA",
            "glo_l_eq_FL_closed_k_ge_3": "LEMMA",
            "par_4w_FL_shift0_at_k3": "KILLED",
            "plo_s_without_pow_at_k8": "KILLED",
            "plo_s_without_sign_at_k8": "KILLED",
            "glo_s_without_plus9_at_k8": "KILLED",
            "glo_s_without_sign_at_k7": "KILLED",
            "plo_l_without_plus2_at_k8": "KILLED",
            "plo_l_without_sign_at_k8": "KILLED",
            "glo_l_without_sign_at_k8": "KILLED",
            "plo_s_eq_2sm_at_k2": "KILLED",
            "plo_l_eq_2ege_at_k2": "KILLED",
            "plo_s_eq_lo_parent_s": "KILLED",
            "plo_s_eq_pg_lo": "KILLED",
            "plo_s_eq_glo_s": "KILLED",
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
        dump["par_4w_fold"]["rows"]["8"]["plo_s"],
        dump["par_4w_fold"]["rows"]["8"]["glo_s"],
        dump["par_4w_fold"]["rows"]["8"]["plo_l"],
        dump["par_4w_fold"]["rows"]["8"]["glo_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
