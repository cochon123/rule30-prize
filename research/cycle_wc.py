#!/usr/bin/env python3
"""Cycle WC: leftover xor 4-way F/L closed forms.

pg_s is 2^{k-3}(4 F_{k+1}+3 F_{k-1}-5) for k>=3.
gp_s is (2^{k-3}(12 F_{k+1}+9 F_{k-1}-35)-2(-1)^k+3)/3 for k>=3.
pg_l is (2^{k-3}(5 F_{k-1}+16 L_{k-1}-15)+2)/5 for k>=3.
gp_l is (2^{k-3}(5 F_{k-1}+16 L_{k-1}-5)+5(-1)^k-3)/5 for k>=3.
They sum to Cycle WA leftover xor n_pg/n_gp and Cycle VT xor_lo
halves. Dies at k=3 for gp_s/pg_l/gp_l F/L forms with shift 0
(gp_s got 1, not 5; pg_l got 0, not 8; gp_l got -2, not 8). Do
not kill pg_s shift 0 at k=3: 2^{0}=1 so it matches. Dies at k=8
without pg_s 2^{k-3} (got 170, not 5440), without gp_s +3 (got
5226, not 5227), without pg_l +2 (got 3289, not 3290), and
without gp_l 5(-1)^k (got 3353, not 3354). Do not kill without
gp_l -3 at k=8: floor-div masks it.
Dies at k=8 for pg_s equals tot small (got 5440, not 10667), pg_s
equals tot pg (got 5440, not 8730), and pg_s equals gp_s (got
5440, not 5227). Special gp_l=2 at k=2, not 0. Census k=8: pg_s
5440, gp_s 5227, pg_l 3290, gp_l 3354. Do not PREFIX pal-center
tot. Not rest=S xor T. Do not walk leftover p catalogues. Do not
walk leftover d catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wc.py --certify
Dump: research/cycle_wc.json
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
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vh import leftover_xor_half, want_gp_l, want_gp_s, want_pg_l, want_pg_s
from cycle_vt import want_xor_lo_l_fl, want_xor_lo_s_fl
from cycle_wa import want_xor_gp_fl, want_xor_pg_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WB_JSON = Path(__file__).resolve().parent / "cycle_wb.json"
WA_JSON = Path(__file__).resolve().parent / "cycle_wa.json"
VT_JSON = Path(__file__).resolve().parent / "cycle_vt.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_pg_s_fl(k: int) -> int:
    """leftover xor n_pg on n<=5U/2: F form for k>=3; 1 at k=1; 3 at k=2."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    if k == 2:
        return 3
    return (1 << (k - 3)) * (4 * fib(k + 1) + 3 * fib(k - 1) - 5)


def want_xor_gp_s_fl(k: int) -> int:
    """leftover xor n_gp on n<=5U/2: F form for k>=3; 0 at k<=2."""
    if k <= 2:
        return 0
    n = (
        (1 << (k - 3)) * (12 * fib(k + 1) + 9 * fib(k - 1) - 35)
        - 2 * ((-1) ** k)
        + 3
    )
    return n // 3


def want_xor_pg_l_fl(k: int) -> int:
    """leftover xor n_pg on n>5U/2: F/L form for k>=3; 1 at k=2; 0 at k<=1."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    n = (1 << (k - 3)) * (5 * fib(k - 1) + 16 * lucas(k - 1) - 15) + 2
    return n // 5


def want_xor_gp_l_fl(k: int) -> int:
    """leftover xor n_gp on n>5U/2: F/L form for k>=3; 2 at k=2; 0 at k<=1."""
    if k <= 1:
        return 0
    if k == 2:
        return 2
    n = (
        (1 << (k - 3)) * (5 * fib(k - 1) + 16 * lucas(k - 1) - 5)
        + 5 * ((-1) ** k)
        - 3
    )
    return n // 5


def tot_form() -> dict:
    """k<=64: leftover xor 4-way F/L; dies at k=3 with shift 0 on three.

    Do not call leftover_xor_half / leftover_xor_split here.
    Census is xor_4w_fold for k<=8. pg_s shift 0 at k=3 matches.
    """
    n_ok = 0
    raw_gps3 = (-2 * ((-1) ** 3) + 3) // 3
    raw_pgl3 = 2 // 5
    raw_gpl3 = (5 * ((-1) ** 3) - 3) // 5
    miss_pgs_pow = 4 * fib(9) + 3 * fib(7) - 5
    miss_gps3 = (
        (1 << 5) * (12 * fib(9) + 9 * fib(7) - 35) - 2 * ((-1) ** 8)
    ) // 3
    miss_pgl2 = ((1 << 5) * (5 * fib(7) + 16 * lucas(7) - 15)) // 5
    miss_gplsign = (
        (1 << 5) * (5 * fib(7) + 16 * lucas(7) - 5) - 3
    ) // 5
    miss_gplm3 = (
        (1 << 5) * (5 * fib(7) + 16 * lucas(7) - 5) + 5 * ((-1) ** 8)
    ) // 5
    if want_xor_pg_s_fl(0) != 0 or want_xor_pg_s_fl(1) != 1:
        return {"ok": False, "k01": True}
    if want_xor_pg_s_fl(2) != 3 or want_xor_gp_s_fl(2) != 0:
        return {"ok": False, "k2s": True}
    if want_xor_pg_l_fl(2) != 1 or want_xor_gp_l_fl(2) != 2:
        return {"ok": False, "k2l": True}
    if want_xor_gp_l_fl(2) == 0:
        return {"ok": False, "k2g0": True}
    if want_xor_pg_s_fl(3) != 10 or want_xor_gp_s_fl(3) != 5:
        return {"ok": False, "k3s": True}
    if want_xor_pg_l_fl(3) != 8 or want_xor_gp_l_fl(3) != 8:
        return {"ok": False, "k3l": True}
    if want_xor_pg_s_fl(8) != 5440 or want_xor_gp_s_fl(8) != 5227:
        return {"ok": False, "k8s": True}
    if want_xor_pg_l_fl(8) != 3290 or want_xor_gp_l_fl(8) != 3354:
        return {"ok": False, "k8l": True}
    if want_xor_pg_s_fl(8) == miss_pgs_pow:
        return {"ok": False, "pow": True}
    if want_xor_gp_s_fl(3) == raw_gps3:
        return {"ok": False, "rawgs": True}
    if want_xor_pg_l_fl(3) == raw_pgl3:
        return {"ok": False, "rawl": True}
    if want_xor_gp_l_fl(3) == raw_gpl3:
        return {"ok": False, "rawgl": True}
    if want_xor_gp_s_fl(8) == miss_gps3:
        return {"ok": False, "gs3": True}
    if want_xor_pg_l_fl(8) == miss_pgl2:
        return {"ok": False, "pl2": True}
    if want_xor_gp_l_fl(8) == miss_gplsign:
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
        if want_xor_pg_s_fl(k) != want_pg_s(k):
            return {"ok": False, "ps": True, "k": k}
        if want_xor_gp_s_fl(k) != want_gp_s(k):
            return {"ok": False, "gs": True, "k": k}
        if want_xor_pg_l_fl(k) != want_pg_l(k):
            return {"ok": False, "pl": True, "k": k}
        if want_xor_gp_l_fl(k) != want_gp_l(k):
            return {"ok": False, "gl": True, "k": k}
        if want_xor_pg_s_fl(k) + want_xor_gp_s_fl(k) != want_xor_lo_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if want_xor_pg_l_fl(k) + want_xor_gp_l_fl(k) != want_xor_lo_l_fl(k):
            return {"ok": False, "suml": True, "k": k}
        if want_xor_pg_s_fl(k) + want_xor_pg_l_fl(k) != want_xor_pg_fl(k):
            return {"ok": False, "sump": True, "k": k}
        if want_xor_gp_s_fl(k) + want_xor_gp_l_fl(k) != want_xor_gp_fl(k):
            return {"ok": False, "sumg": True, "k": k}
        if k >= 3:
            ns = (
                (1 << (k - 3)) * (12 * fib(k + 1) + 9 * fib(k - 1) - 35)
                - 2 * ((-1) ** k)
                + 3
            )
            np = (
                (1 << (k - 3)) * (5 * fib(k - 1) + 16 * lucas(k - 1) - 15)
                + 2
            )
            ng = (
                (1 << (k - 3)) * (5 * fib(k - 1) + 16 * lucas(k - 1) - 5)
                + 5 * ((-1) ** k)
                - 3
            )
            if ns % 3 != 0 or ns // 3 != want_xor_gp_s_fl(k):
                return {"ok": False, "dgs": True, "k": k}
            if np % 5 != 0 or np // 5 != want_xor_pg_l_fl(k):
                return {"ok": False, "dpl": True, "k": k}
            if ng % 5 != 0 or ng // 5 != want_xor_gp_l_fl(k):
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
        and want_xor_pg_s_fl(8) != miss_pgs_pow
        and want_xor_gp_s_fl(3) != raw_gps3
        and want_xor_pg_l_fl(3) != raw_pgl3
        and want_xor_gp_l_fl(3) != raw_gpl3
        and want_xor_gp_s_fl(8) != miss_gps3
        and want_xor_pg_l_fl(8) != miss_pgl2
        and want_xor_gp_l_fl(8) != miss_gplsign
        and want_xor_gp_l_fl(8) == miss_gplm3
        and want_xor_pg_s_fl(8) != want_xor_lo_s_fl(8)
        and want_xor_pg_s_fl(8) != want_xor_pg_fl(8)
        and want_xor_pg_s_fl(8) != want_xor_gp_s_fl(8)
        and want_xor_pg_s_fl(8) == 5440
        and want_xor_gp_s_fl(8) == 5227
        and want_xor_pg_l_fl(8) == 3290
        and want_xor_gp_l_fl(8) == 3354
        and want_xor_lo_s_fl(8) == 10667
        and want_xor_lo_l_fl(8) == 6644
        and want_xor_pg_fl(8) == 8730
        and want_xor_gp_fl(8) == 8581
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
        and miss_gps3 == 5226
        and miss_pgl2 == 3289
        and miss_gplsign == 3353
        and miss_gplm3 == 3354
        and miss_pgs_pow == 170
        and raw_gps3 == 1
        and raw_pgl3 == 0
        and raw_gpl3 == -2
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def xor_4w_fold() -> dict:
    """k<=8 leftover xor 4-way vs F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = leftover_xor_half(k)
        if a["bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if a["pg_s"] != want_xor_pg_s_fl(k):
            return {"ok": False, "ps": True, "k": k, "got": a["pg_s"]}
        if a["gp_s"] != want_xor_gp_s_fl(k):
            return {"ok": False, "gs": True, "k": k, "got": a["gp_s"]}
        if a["pg_l"] != want_xor_pg_l_fl(k):
            return {"ok": False, "pl": True, "k": k, "got": a["pg_l"]}
        if a["gp_l"] != want_xor_gp_l_fl(k):
            return {"ok": False, "gl": True, "k": k, "got": a["gp_l"]}
        if a["pg_s"] + a["gp_s"] != want_xor_lo_s_fl(k):
            return {"ok": False, "sums": True, "k": k}
        if a["pg_l"] + a["gp_l"] != want_xor_lo_l_fl(k):
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
        and rows["1"]["pg_s"] == 1
        and rows["1"]["gp_s"] == 0
        and rows["1"]["pg_l"] == 0
        and rows["1"]["gp_l"] == 0
        and rows["2"]["pg_s"] == 3
        and rows["2"]["gp_s"] == 0
        and rows["2"]["pg_l"] == 1
        and rows["2"]["gp_l"] == 2
        and rows["3"]["pg_s"] == 10
        and rows["3"]["gp_s"] == 5
        and rows["3"]["pg_l"] == 8
        and rows["3"]["gp_l"] == 8
        and rows["8"]["pg_s"] == 5440
        and rows["8"]["gp_s"] == 5227
        and rows["8"]["pg_l"] == 3290
        and rows["8"]["gp_l"] == 3354
        and want_xor_pg_s_fl(4) == 42
        and want_xor_gp_s_fl(5) == 119
        and want_xor_pg_l_fl(5) == 90
        and want_xor_gp_l_fl(6) == 314
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L forms at k=3 with shift 0; pg_s power, gp_s +3, pg_l +2, gp_l sign."""
    raw_gps3 = (-2 * ((-1) ** 3) + 3) // 3
    raw_pgl3 = 2 // 5
    raw_gpl3 = (5 * ((-1) ** 3) - 3) // 5
    miss_pgs_pow = 4 * fib(9) + 3 * fib(7) - 5
    miss_gps3 = (
        (1 << 5) * (12 * fib(9) + 9 * fib(7) - 35) - 2 * ((-1) ** 8)
    ) // 3
    miss_pgl2 = ((1 << 5) * (5 * fib(7) + 16 * lucas(7) - 15)) // 5
    miss_gplsign = (
        (1 << 5) * (5 * fib(7) + 16 * lucas(7) - 5) - 3
    ) // 5
    miss_gplm3 = (
        (1 << 5) * (5 * fib(7) + 16 * lucas(7) - 5) + 5 * ((-1) ** 8)
    ) // 5
    a8 = leftover_xor_half(8)
    ok = (
        want_xor_pg_s_fl(8) != miss_pgs_pow
        and want_xor_gp_s_fl(3) != raw_gps3
        and want_xor_pg_l_fl(3) != raw_pgl3
        and want_xor_gp_l_fl(3) != raw_gpl3
        and want_xor_gp_s_fl(8) != miss_gps3
        and want_xor_pg_l_fl(8) != miss_pgl2
        and want_xor_gp_l_fl(8) != miss_gplsign
        and want_xor_gp_l_fl(8) == miss_gplm3
        and want_xor_pg_s_fl(8) != want_xor_lo_s_fl(8)
        and want_xor_pg_s_fl(8) != want_xor_pg_fl(8)
        and want_xor_pg_s_fl(8) != want_xor_gp_s_fl(8)
        and a8["pg_s"] == 5440
        and a8["gp_s"] == 5227
        and a8["pg_l"] == 3290
        and a8["gp_l"] == 3354
        and miss_pgs_pow == 170
        and raw_gps3 == 1
        and raw_pgl3 == 0
        and raw_gpl3 == -2
        and miss_gps3 == 5226
        and miss_pgl2 == 3289
        and miss_gplsign == 3353
        and miss_gplm3 == 3354
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
    wb = json.loads(WB_JSON.read_text())
    wa = json.loads(WA_JSON.read_text())
    vt = json.loads(VT_JSON.read_text())
    ok = (
        wb["checks"]["all_ok"]
        and wa["checks"]["all_ok"]
        and vt["checks"]["all_ok"]
        and wb["verdict"]["ej_xor_s_eq_FL_closed_k_ge_3"] == "LEMMA"
        and wa["verdict"]["xor_pg_eq_FL_closed_k_ge_2"] == "LEMMA"
        and vt["verdict"]["xor_lo_s_eq_FL_closed_k_ge_2"] == "LEMMA"
        and wb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wb["verdict"]["prize"] == "unsolved"
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
    cnt = xor_4w_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "xor_4w_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_pg_s_eq_FL_closed_k_ge_3": True,
            "xor_gp_s_eq_FL_closed_k_ge_3": True,
            "xor_pg_l_eq_FL_closed_k_ge_3": True,
            "xor_gp_l_eq_FL_closed_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_pg_s_eq_FL_closed_k_ge_3": "LEMMA",
            "xor_gp_s_eq_FL_closed_k_ge_3": "LEMMA",
            "xor_pg_l_eq_FL_closed_k_ge_3": "LEMMA",
            "xor_gp_l_eq_FL_closed_k_ge_3": "LEMMA",
            "xor_4w_FL_shift0_at_k3": "KILLED",
            "xor_pg_s_without_pow_at_k8": "KILLED",
            "xor_gp_s_without_plus3_at_k8": "KILLED",
            "xor_pg_l_without_plus2_at_k8": "KILLED",
            "xor_gp_l_without_sign_at_k8": "KILLED",
            "xor_pg_s_eq_xor_lo_s": "KILLED",
            "xor_pg_s_eq_xor_pg": "KILLED",
            "xor_pg_s_eq_xor_gp_s": "KILLED",
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
        dump["xor_4w_fold"]["rows"]["8"]["pg_s"],
        dump["xor_4w_fold"]["rows"]["8"]["gp_s"],
        dump["xor_4w_fold"]["rows"]["8"]["pg_l"],
        dump["xor_4w_fold"]["rows"]["8"]["gp_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
