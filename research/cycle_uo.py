#!/usr/bin/env python3
"""Cycle UO: leftover-parent xor small sum is lo_small minus named_s minus j0.

Named leftover extra on n<=5U/2 follows parent d=1/d=2 halves: gp:d1
small is parent d=1 small minus 1 for k>=3, pg:d2 and gp:d2 follow
parent d=2 halves for k>=4 (k=3 dies: parent_half is d=2). Then
leftover-parent xor small sum is Cycle UK lo_small minus named small
minus j=0 leftover. Do not PREFIX leftover-parent xor total sum or
leftover extra or unpaired extra. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_uo.py --certify
Dump: research/cycle_uo.json
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
from cycle_uk import want_d1_large, want_d1_small, want_lo_small
from cycle_ul import (
    leftover_named_split,
    parent_pair_type,
    want_gp_d1,
    want_gp_d2,
    want_named_lo,
    want_pg_d2,
)
from cycle_um import want_lo_parent_diff
from cycle_un import want_d2_large, want_d2_small, want_d2e_large, want_d2e_small
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UN_JSON = Path(__file__).resolve().parent / "cycle_un.json"
UL_JSON = Path(__file__).resolve().parent / "cycle_ul.json"
UK_JSON = Path(__file__).resolve().parent / "cycle_uk.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_gp_d1_small(k: int) -> int:
    """g0+pair leftover extra from d=1 on n<=5U/2: 0,0,0, then parent d=1 small-1."""
    if k <= 2:
        return 0
    return want_d1_small(k - 1) - 1


def want_gp_d1_large(k: int) -> int:
    """g0+pair leftover extra from d=1 on n>5U/2: 0,0,2, then parent d=1 large."""
    if k <= 1:
        return 0
    if k == 2:
        return 2
    return want_d1_large(k - 1)


def want_pg_d2_small(k: int) -> int:
    """pair+g0 leftover extra from d=2 on n<=5U/2: 0,1,2,2, then parent d=2 small."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    if k <= 3:
        return 2
    return want_d2_small(k - 1)


def want_pg_d2_large(k: int) -> int:
    """pair+g0 leftover extra from d=2 on n>5U/2: 0,0,0,4, then parent d=2 large."""
    if k <= 2:
        return 0
    if k == 3:
        return 4
    return want_d2_large(k - 1)


def want_gp_d2_small(k: int) -> int:
    """g0+pair leftover extra from even d=2 on n<=5U/2: 0 through k=3, then even parent-1."""
    if k <= 3:
        return 0
    return want_d2e_small(k - 1) - 1


def want_gp_d2_large(k: int) -> int:
    """g0+pair leftover extra from even d=2 on n>5U/2: 0,0,0,2, then even parent large."""
    if k <= 2:
        return 0
    if k == 3:
        return 2
    return want_d2e_large(k - 1)


def want_named_s(k: int) -> int:
    """Named leftover extra on n<=5U/2."""
    return want_gp_d1_small(k) + want_pg_d2_small(k) + want_gp_d2_small(k)


def want_named_l(k: int) -> int:
    """Named leftover extra on n>5U/2."""
    return want_gp_d1_large(k) + want_pg_d2_large(k) + want_gp_d2_large(k)


def want_lo_parent_small_sum(k: int) -> int:
    """pg:lo+gp:lo on n<=5U/2: lo_small minus named small minus j=0 leftover."""
    return want_lo_small(k) - want_named_s(k) - want_j0_odd_lo(k)


def named_half_split(k: int) -> dict:
    """Odd-n even-j leftover extra: named and leftover-parent xor by n<=5U/2."""
    u = 1 << k
    clip = 5 * u
    half = (5 * u) // 2
    k_p = k - 1 if k >= 1 else 0
    a = {
        "gpd1_s": 0,
        "gpd1_l": 0,
        "pgd2_s": 0,
        "pgd2_l": 0,
        "gpd2_s": 0,
        "gpd2_l": 0,
        "plo_s": 0,
        "plo_l": 0,
        "glo_s": 0,
        "glo_l": 0,
        "j0": 0,
        "lo_s": 0,
        "lo_l": 0,
        "n_bad": 0,
        "n_pg_d1": 0,
    }
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        hi = min(2 * n, clip)
        tag = "_s" if n <= half else "_l"
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            a["lo" + tag] += 1
            r = j // 2
            if r == 0:
                a["j0"] += 1
                continue
            kr = parent_pair_type(m, r, k_p)
            km = parent_pair_type(m, r - 1, k_p)
            if km == "d1" and kr == "g0":
                a["n_pg_d1"] += 1
            elif km == "d2" and kr == "g0":
                a["pgd2" + tag] += 1
            elif km == "lo" and kr == "g0":
                a["plo" + tag] += 1
            elif km == "clip" and kr == "g0":
                a["n_bad"] += 1
            elif km == "g0" and kr == "d1":
                a["gpd1" + tag] += 1
            elif km == "g0" and kr == "d2":
                a["gpd2" + tag] += 1
            elif km == "g0" and kr == "lo":
                a["glo" + tag] += 1
            elif km == "g0" and kr == "clip":
                a["n_bad"] += 1
            else:
                a["n_bad"] += 1
    return a


def tot_form() -> dict:
    """k<=64: named halves partition UL named; parent-half not d=2 for k>=4."""
    n_ok = 0
    if want_named_s(0) != 0 or want_named_s(1) != 1:
        return {"ok": False, "k01": True}
    if want_named_s(8) != 266 or want_named_l(8) != 158:
        return {"ok": False, "k8n": True}
    if want_lo_parent_small_sum(8) != 10401:
        return {"ok": False, "k8s": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if G(2 * m, 2 * m - 2) != G(m, m - 1):
            return {"ok": False, "ge": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_named_s(k) + want_named_l(k) != want_named_lo(k):
            return {"ok": False, "nm": True, "k": k}
        if want_gp_d1_small(k) + want_gp_d1_large(k) != want_gp_d1(k):
            return {"ok": False, "g1": True, "k": k}
        if want_pg_d2_small(k) + want_pg_d2_large(k) != want_pg_d2(k):
            return {"ok": False, "p2": True, "k": k}
        if want_gp_d2_small(k) + want_gp_d2_large(k) != want_gp_d2(k):
            return {"ok": False, "g2": True, "k": k}
        if want_lo_parent_small_sum(k) != (
            want_lo_small(k) - want_named_s(k) - want_j0_odd_lo(k)
        ):
            return {"ok": False, "ss": True, "k": k}
        if want_lo_parent_small_sum(k) < 0:
            return {"ok": False, "neg": True, "k": k}
        if k >= 3:
            if want_gp_d1_small(k) != want_d1_small(k - 1) - 1:
                return {"ok": False, "g1s": True, "k": k}
            if want_gp_d1_large(k) != want_d1_large(k - 1):
                return {"ok": False, "g1l": True, "k": k}
        if k >= 4:
            if want_pg_d2_small(k) != want_d2_small(k - 1):
                return {"ok": False, "p2s": True, "k": k}
            if want_pg_d2_large(k) != want_d2_large(k - 1):
                return {"ok": False, "p2l": True, "k": k}
            if want_gp_d2_small(k) != want_d2e_small(k - 1) - 1:
                return {"ok": False, "g2s": True, "k": k}
            if want_gp_d2_large(k) != want_d2e_large(k - 1):
                return {"ok": False, "g2l": True, "k": k}
            ph = 5 * (1 << (k - 2))
            if ph % 2 != 0:
                return {"ok": False, "ph": True, "k": k}
            if G(ph // 2, ph // 2 - 1) != 0:
                return {"ok": False, "d2ph": True, "k": k}
        if k == 3:
            if want_pg_d2_small(k) == want_d2_small(k - 1):
                return {"ok": False, "k3p": True}
            if want_gp_d2_small(k) == want_d2e_small(k - 1) - 1:
                return {"ok": False, "k3g": True}
            if G(5, 4) != 1:
                return {"ok": False, "k3g5": True}
        if k >= 3 and want_lo_parent_small_sum(k) == want_lo_parent_diff(k):
            return {"ok": False, "eqd": True, "k": k}
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
        and want_named_s(8) != want_named_lo(8)
        and want_named_s(8) != want_named_l(8)
        and want_lo_parent_small_sum(8) != want_lo_parent_diff(8)
        and want_lo_parent_small_sum(8) != 16887
        and want_lo_small(8) == 10986
        and want_j0_odd_lo(8) == 319
        and want_gp_d1(8) == 170
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
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def named_half_fold() -> dict:
    """k<=8: named halves and leftover-parent xor small sum match."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        tot = leftover_named_split(k)
        if r["n_bad"] != 0 or r["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if r["j0"] != want_j0_odd_lo(k):
            return {"ok": False, "j0": True, "k": k}
        if r["gpd1_s"] != want_gp_d1_small(k) or r["gpd1_l"] != want_gp_d1_large(k):
            return {"ok": False, "g1": True, "k": k, "got": r}
        if r["pgd2_s"] != want_pg_d2_small(k) or r["pgd2_l"] != want_pg_d2_large(k):
            return {"ok": False, "p2": True, "k": k, "got": r}
        if r["gpd2_s"] != want_gp_d2_small(k) or r["gpd2_l"] != want_gp_d2_large(k):
            return {"ok": False, "g2": True, "k": k, "got": r}
        named_s = r["gpd1_s"] + r["pgd2_s"] + r["gpd2_s"]
        named_l = r["gpd1_l"] + r["pgd2_l"] + r["gpd2_l"]
        if named_s != want_named_s(k) or named_l != want_named_l(k):
            return {"ok": False, "nm": True, "k": k}
        if named_s + named_l != tot["n_gp_d1"] + tot["n_pg_d2"] + tot["n_gp_d2"]:
            return {"ok": False, "ul": True, "k": k}
        if r["lo_s"] != want_lo_small(k):
            return {"ok": False, "lo": True, "k": k}
        ssum = r["plo_s"] + r["glo_s"]
        if ssum != want_lo_parent_small_sum(k):
            return {"ok": False, "ss": True, "k": k, "got": ssum}
        if r["lo_s"] != named_s + ssum + r["j0"]:
            return {"ok": False, "part": True, "k": k}
        if k >= 3 and ssum == want_lo_parent_diff(k):
            return {"ok": False, "eqd": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "gpd1_s": r["gpd1_s"],
            "pgd2_s": r["pgd2_s"],
            "gpd2_s": r["gpd2_s"],
            "named_s": named_s,
            "named_l": named_l,
            "small_sum": ssum,
            "j0": r["j0"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["named_s"] == 0
        and rows["1"]["named_s"] == 1
        and rows["8"]["gpd1_s"] == 105
        and rows["8"]["pgd2_s"] == 108
        and rows["8"]["gpd2_s"] == 53
        and rows["8"]["named_s"] == 266
        and rows["8"]["named_l"] == 158
        and rows["8"]["small_sum"] == 10401
        and rows["8"]["j0"] == 319
        and rows["8"]["named_s"] != 424
        and rows["8"]["small_sum"] != 233
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """named_s equals named; small sum equals UM diff; pg:d2 at k=3."""
    ok = (
        want_named_s(8) != want_named_lo(8)
        and want_named_s(8) != want_named_l(8)
        and want_lo_parent_small_sum(8) != want_lo_parent_diff(8)
        and want_lo_parent_small_sum(8) != 16887
        and want_pg_d2_small(3) != want_d2_small(2)
        and want_gp_d2_small(3) != want_d2e_small(2) - 1
        and G(2, 2) != 2 % 2
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
    un = json.loads(UN_JSON.read_text())
    ul = json.loads(UL_JSON.read_text())
    uk = json.loads(UK_JSON.read_text())
    ok = (
        un["checks"]["all_ok"]
        and ul["checks"]["all_ok"]
        and uk["checks"]["all_ok"]
        and un["verdict"]["d2e_half_eq_parent_d1"] == "LEMMA"
        and ul["verdict"]["named_lo_eq_2k_plus_2J_minus_2"] == "LEMMA"
        and uk["verdict"]["lo_small_eq_tot_minus_d1"] == "LEMMA"
        and un["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and un["verdict"]["prize"] == "unsolved"
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
    cnt = named_half_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UO",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "named_half_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "gp_d1_half_eq_parent_d1": True,
            "pg_d2_half_eq_parent_d2_kge4": True,
            "lo_parent_small_sum_eq_lo_small_minus_named_j0": True,
            "named_s_eq_named": False,
            "small_sum_eq_um_diff": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "gp_d1_half_eq_parent_d1": "LEMMA",
            "pg_d2_half_eq_parent_d2_kge4": "LEMMA",
            "lo_parent_small_sum_eq_lo_small_minus_named_j0": "LEMMA",
            "named_s_eq_named": "KILLED",
            "named_s_eq_named_l": "KILLED",
            "small_sum_eq_um_diff": "KILLED",
            "small_sum_eq_lo_parent_tot": "KILLED",
            "pg_d2_half_at_k3": "KILLED",
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
        "named_s k8",
        dump["named_half_fold"]["rows"]["8"]["named_s"],
        "small_sum",
        dump["named_half_fold"]["rows"]["8"]["small_sum"],
        "named_l",
        dump["named_half_fold"]["rows"]["8"]["named_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
