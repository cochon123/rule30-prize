#!/usr/bin/env python3
"""Cycle VL: leftover extra xor COUNT gap n_pg is 2 lo_e(k-1) minus
parent leftover xor n_pg.

Cycle UP pg:lo is twice even leftover. Leftover extra xor n_pg is
parent leftover xor n_pg, so the COUNT gap n_pg is 2 lo_e(k-1) minus
that parent count. COUNT gap n_gp is the same minus Cycle UM. Small
n_pg is 2 sm(k-1) minus parent leftover xor small n_pg; large n_pg
is 2 e_ge(k-1) minus parent leftover xor large n_pg. Dies at k=2 for
small gp (got 1, walk 0). Dies at k=2,3 for large gp. Census k=8:
tot 5910/5752. Do not PREFIX pal-center tot. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_vl.py --certify
Dump: research/cycle_vl.json
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
from cycle_up import lucas, want_lo_e, want_gp_lo, want_pg_lo
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uy import want_lo_parent_large_diff
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vd import want_lo_parent_small_diff
from cycle_ve import want_xor_small_gap
from cycle_vg import want_gp, want_pg
from cycle_vh import want_gp_l, want_gp_s, want_pg_l, want_pg_s
from cycle_vi import want_xor_count_gap
from cycle_vj import want_xor_count_gap_l, want_xor_count_gap_s
from cycle_vk import (
    want_xor_count_gap_gp,
    want_xor_count_gap_l_gp,
    want_xor_count_gap_l_pg,
    want_xor_count_gap_pg,
    want_xor_count_gap_s_gp,
    want_xor_count_gap_s_pg,
)
from cycle_um import want_lo_parent_diff
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VK_JSON = Path(__file__).resolve().parent / "cycle_vk.json"
VJ_JSON = Path(__file__).resolve().parent / "cycle_vj.json"
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_count_gap_pg_loe(k: int) -> int:
    """COUNT gap n_pg: 2 lo_e(k-1) minus parent leftover xor n_pg."""
    return 2 * want_lo_e(k - 1) - want_pg(k - 1)


def want_xor_count_gap_gp_loe(k: int) -> int:
    """COUNT gap n_gp: 2 lo_e(k-1) minus UM minus parent leftover xor n_gp."""
    return 2 * want_lo_e(k - 1) - want_lo_parent_diff(k) - want_gp(k - 1)


def want_xor_count_gap_s_pg_sm(k: int) -> int:
    """COUNT gap small n_pg: 2 sm(k-1) minus parent leftover xor small n_pg."""
    return 2 * want_sm(k - 1) - want_pg_s(k - 1)


def want_xor_count_gap_s_gp_sm(k: int) -> int:
    """COUNT gap small n_gp: 2 sm(k-1) minus UM_s minus parent small n_gp.

    Special-case 0 at k<=2 (the 2-sm form at k=2 is 1).
    """
    if k <= 2:
        return 0
    return (
        2 * want_sm(k - 1)
        - want_lo_parent_small_diff(k)
        - want_gp_s(k - 1)
    )


def want_xor_count_gap_l_pg_ege(k: int) -> int:
    """COUNT gap large n_pg: 2 e_ge(k-1) minus parent leftover xor large n_pg."""
    return 2 * want_ege(k - 1) - want_pg_l(k - 1)


def want_xor_count_gap_l_gp_ege(k: int) -> int:
    """COUNT gap large n_gp: 2 e_ge(k-1) minus UM_l minus parent large n_gp.

    Special-case 0 at k<=2; 3 at k=3 (the 2-ege form at k=3 is 2).
    """
    if k <= 2:
        return 0
    if k == 3:
        return 3
    return (
        2 * want_ege(k - 1)
        - want_lo_parent_large_diff(k)
        - want_gp_l(k - 1)
    )


def tot_form() -> dict:
    """k<=64: COUNT gap pg/gp from 2 lo_e; dies at k=2,3 for gp halves.

    Do not call named_half_split / leftover_extra_xor_split here.
    Census is gap_loe_fold for k<=8.
    """
    n_ok = 0
    raw_s2 = (
        2 * want_sm(1)
        - want_lo_parent_small_diff(2)
        - want_gp_s(1)
    )
    raw_l2 = (
        2 * want_ege(1)
        - want_lo_parent_large_diff(2)
        - want_gp_l(1)
    )
    raw_l3 = (
        2 * want_ege(2)
        - want_lo_parent_large_diff(3)
        - want_gp_l(2)
    )
    if want_xor_count_gap_pg_loe(0) != 0 or want_xor_count_gap_pg_loe(2) != 1:
        return {"ok": False, "k02": True}
    if want_xor_count_gap_pg_loe(8) != 5910 or want_xor_count_gap_gp_loe(8) != 5752:
        return {"ok": False, "k8": True}
    if want_xor_count_gap_s_gp_sm(2) == raw_s2:
        return {"ok": False, "k2s": True}
    if want_xor_count_gap_l_gp_ege(2) == raw_l2:
        return {"ok": False, "k2l": True}
    if want_xor_count_gap_l_gp_ege(3) == raw_l3:
        return {"ok": False, "k3l": True}
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
        if want_xor_count_gap_pg(k) != want_xor_count_gap_pg_loe(k):
            return {"ok": False, "pg": True, "k": k}
        if want_xor_count_gap_gp(k) != want_xor_count_gap_gp_loe(k):
            return {"ok": False, "gp": True, "k": k}
        if want_xor_count_gap_pg_loe(k) != 2 * want_lo_e(k - 1) - want_pg(k - 1):
            return {"ok": False, "fpg": True, "k": k}
        if want_xor_count_gap_gp_loe(k) != (
            2 * want_lo_e(k - 1) - want_lo_parent_diff(k) - want_gp(k - 1)
        ):
            return {"ok": False, "fgp": True, "k": k}
        if want_xor_count_gap_s_pg(k) != want_xor_count_gap_s_pg_sm(k):
            return {"ok": False, "sp": True, "k": k}
        if want_xor_count_gap_s_gp(k) != want_xor_count_gap_s_gp_sm(k):
            return {"ok": False, "sg": True, "k": k}
        if want_xor_count_gap_l_pg(k) != want_xor_count_gap_l_pg_ege(k):
            return {"ok": False, "lp": True, "k": k}
        if want_xor_count_gap_l_gp(k) != want_xor_count_gap_l_gp_ege(k):
            return {"ok": False, "lg": True, "k": k}
        if k >= 3:
            if want_xor_count_gap_s_gp_sm(k) != (
                2 * want_sm(k - 1)
                - want_lo_parent_small_diff(k)
                - want_gp_s(k - 1)
            ):
                return {"ok": False, "s3": True, "k": k}
        if k >= 4:
            if want_xor_count_gap_l_gp_ege(k) != (
                2 * want_ege(k - 1)
                - want_lo_parent_large_diff(k)
                - want_gp_l(k - 1)
            ):
                return {"ok": False, "l4": True, "k": k}
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
        and want_xor_count_gap_s_gp_sm(2) != raw_s2
        and want_xor_count_gap_l_gp_ege(3) != raw_l3
        and want_xor_count_gap_s_pg(8) != want_xor_count_gap_pg(8)
        and want_xor_count_gap_pg_loe(8) == 5910
        and want_xor_count_gap_gp_loe(8) == 5752
        and want_xor_count_gap(8) == 11662
        and want_xor_small_gap(8) == 158
        and want_ej_xor(8) == 5225
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
        and want_pg_lo(8) == 8560
        and want_gp_lo(8) == 8327
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
        and lucas(8) == 47
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def gap_loe_fold() -> dict:
    """k<=8 COUNT gap n_pg/n_gp vs 2 lo_e minus parent leftover xor."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        a = leftover_extra_xor_split(k)
        gpg = r["plo_s"] + r["plo_l"] - a["pg_s"] - a["pg_l"]
        ggp = r["glo_s"] + r["glo_l"] - a["gp_s"] - a["gp_l"]
        gps = r["plo_s"] - a["pg_s"]
        ggs = r["glo_s"] - a["gp_s"]
        gpl = r["plo_l"] - a["pg_l"]
        ggl = r["glo_l"] - a["gp_l"]
        if gpg != want_xor_count_gap_pg_loe(k):
            return {"ok": False, "pg": True, "k": k, "got": gpg}
        if ggp != want_xor_count_gap_gp_loe(k):
            return {"ok": False, "gp": True, "k": k, "got": ggp}
        if gps != want_xor_count_gap_s_pg_sm(k):
            return {"ok": False, "sp": True, "k": k, "got": gps}
        if ggs != want_xor_count_gap_s_gp_sm(k):
            return {"ok": False, "sg": True, "k": k, "got": ggs}
        if gpl != want_xor_count_gap_l_pg_ege(k):
            return {"ok": False, "lp": True, "k": k, "got": gpl}
        if ggl != want_xor_count_gap_l_gp_ege(k):
            return {"ok": False, "lg": True, "k": k, "got": ggl}
        n_ok += 1
        rows[str(k)] = {"pg": gpg, "gp": ggp, "pg_s": gps, "gp_s": ggs, "pg_l": gpl, "gp_l": ggl}
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["pg"] == 1
        and rows["2"]["gp"] == 0
        and rows["3"]["pg"] == 8
        and rows["3"]["gp"] == 5
        and rows["8"]["pg"] == 5910
        and rows["8"]["gp"] == 5752
        and rows["8"]["pg_s"] == 3684
        and rows["8"]["pg_l"] == 2226
        and want_xor_count_gap_pg_loe(4) == 38
        and want_xor_count_gap_s_gp_sm(4) == 16
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """small gp 2-sm at k=2; large gp 2-ege at k=2,3; small pg equals tot pg."""
    raw_s2 = (
        2 * want_sm(1)
        - want_lo_parent_small_diff(2)
        - want_gp_s(1)
    )
    raw_l2 = (
        2 * want_ege(1)
        - want_lo_parent_large_diff(2)
        - want_gp_l(1)
    )
    raw_l3 = (
        2 * want_ege(2)
        - want_lo_parent_large_diff(3)
        - want_gp_l(2)
    )
    r8 = named_half_split(8)
    a8 = leftover_extra_xor_split(8)
    gpg8 = r8["plo_s"] + r8["plo_l"] - a8["pg_s"] - a8["pg_l"]
    ok = (
        want_xor_count_gap_s_gp_sm(2) != raw_s2
        and want_xor_count_gap_l_gp_ege(2) != raw_l2
        and want_xor_count_gap_l_gp_ege(3) != raw_l3
        and want_xor_count_gap_s_pg(8) != want_xor_count_gap_pg(8)
        and gpg8 == 5910
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
    vk = json.loads(VK_JSON.read_text())
    vj = json.loads(VJ_JSON.read_text())
    up = json.loads(UP_JSON.read_text())
    ok = (
        vk["checks"]["all_ok"]
        and vj["checks"]["all_ok"]
        and up["checks"]["all_ok"]
        and vk["verdict"]["xor_count_gap_pg_gp_eq_gap_pm_xor_small_gap"] == "LEMMA"
        and vj["verdict"]["xor_count_gap_small_eq_lo_small_named_j0_k_ge_3"] == "LEMMA"
        and up["verdict"]["pg_lo_eq_2_parent_even_lo"] == "LEMMA"
        and vk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vk["verdict"]["prize"] == "unsolved"
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
    cnt = gap_loe_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "gap_loe_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_count_gap_pg_eq_2_loe_minus_parent_pg": True,
            "xor_count_gap_small_pg_eq_2_sm_minus_parent_pg_s": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_count_gap_pg_eq_2_loe_minus_parent_pg": "LEMMA",
            "xor_count_gap_small_pg_eq_2_sm_minus_parent_pg_s": "LEMMA",
            "xor_count_gap_small_gp_2sm_at_k2": "KILLED",
            "xor_count_gap_large_gp_2ege_at_k2": "KILLED",
            "xor_count_gap_large_gp_2ege_at_k3": "KILLED",
            "xor_count_gap_small_pg_eq_tot_pg": "KILLED",
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
        "gap k8 pg",
        dump["gap_loe_fold"]["rows"]["8"]["pg"],
        "gp",
        dump["gap_loe_fold"]["rows"]["8"]["gp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
