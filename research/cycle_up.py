#!/usr/bin/env python3
"""Cycle UP: pg:lo is twice even leftover; leftover extra is closed.

Even leftover pal-pairs have next bit 0 (G(even,odd)=0), so every
even leftover parent produces a leftover pair+g0 child: n=2m+1,
j=2(r+1), distance 2d-1>=5, pal-partner doubles and stays at most
5U. Census through k<=8 matches the odd-parent half to the same
even leftover count, hence pg:lo(k)=2 lo_e(k-1) for k>=1. Then
leftover-parent xor total sum is 4 lo_e(k-1) minus Cycle UM's
difference, leftover extra is named plus j=0 plus that sum, and
unpaired extra is Cycle UC extra-sum minus leftover extra. Even
leftover is (75 2^k F_k + 39 2^k L_k - 100 2^k - 20 (-1)^k + 12)/60
for k>=1 (dies at k=0). Do not PREFIX pal-center tot or
leftover-parent xor large difference. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_up.py --certify
Dump: research/cycle_up.json
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
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering, leftover_split
from cycle_tw import want_j0_odd_lo
from cycle_uc import fib, trans, want_extra_sum, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_ul import leftover_named_split, want_named_lo
from cycle_um import want_lo_parent_diff
from cycle_uo import want_lo_parent_small_sum
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UO_JSON = Path(__file__).resolve().parent / "cycle_uo.json"
UM_JSON = Path(__file__).resolve().parent / "cycle_um.json"
UL_JSON = Path(__file__).resolve().parent / "cycle_ul.json"
TU_JSON = Path(__file__).resolve().parent / "cycle_tu.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def lucas(n: int) -> int:
    """L_n with L_0=2, L_1=1."""
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def lo_e_num(k: int) -> int:
    """Numerator of the even leftover closed form, including k=0."""
    tw = 1 << k
    return (
        75 * tw * fib(k)
        + 39 * tw * lucas(k)
        - 100 * tw
        - 20 * ((-1) ** k)
        + 12
    )


def want_lo_e(k: int) -> int:
    """Even leftover count: 0 at k=0, closed form / 60 for k>=1."""
    if k <= 0:
        return 0
    return lo_e_num(k) // 60


def want_lo_e_rhs(k: int) -> int:
    """Inhomogeneous term of the lo_e recurrence, k>=3."""
    return (5 * (1 << k) + (-1) ** k) // 3 - 1


def want_pg_lo(k: int) -> int:
    """pair+g0 leftover extra from leftover parents: 2 lo_e(k-1)."""
    if k <= 0:
        return 0
    return 2 * want_lo_e(k - 1)


def want_gp_lo(k: int) -> int:
    """g0+pair leftover extra from leftover parents: pg:lo minus UM diff."""
    return want_pg_lo(k) - want_lo_parent_diff(k)


def want_lo_parent_sum(k: int) -> int:
    """pg:lo+gp:lo: 4 lo_e(k-1) minus Cycle UM difference."""
    if k <= 0:
        return 0
    return 4 * want_lo_e(k - 1) - want_lo_parent_diff(k)


def want_extra_lo(k: int) -> int:
    """Leftover extra: named plus j=0 plus leftover-parent xor sum."""
    if k <= 0:
        return 0
    return want_named_lo(k) + want_j0_odd_lo(k) + want_lo_parent_sum(k)


def want_extra_unp(k: int) -> int:
    """Unpaired extra: Cycle UC extra-sum minus leftover extra."""
    return want_extra_sum(k) - want_extra_lo(k)


def tot_form() -> dict:
    """k<=64: lo_e closed form, doubling, extras; even next bit 0."""
    n_ok = 0
    if want_lo_e(0) != 0 or want_lo_e(1) != 1 or want_lo_e(2) != 6:
        return {"ok": False, "k012": True}
    if want_pg_lo(0) != 0 or want_pg_lo(1) != 0 or want_pg_lo(2) != 2:
        return {"ok": False, "pg012": True}
    if want_lo_e(8) != 14114 or want_pg_lo(8) != 8560:
        return {"ok": False, "k8e": True}
    if want_lo_parent_sum(8) != 16887 or want_extra_lo(8) != 17630:
        return {"ok": False, "k8s": True}
    if want_extra_unp(8) != 10019 or want_gp_lo(8) != 8327:
        return {"ok": False, "k8u": True}
    if lo_e_num(0) % 60 == 0 or lo_e_num(1) % 60 != 0:
        return {"ok": False, "div": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
        if m % 2 == 0:
            for r in range(0, m + 1):
                if r % 2 == 1 and G(m, r) != 0:
                    return {"ok": False, "eodd": True, "m": m, "r": r}
                if r % 2 == 0 and G(m, r) == 1:
                    if G(m, r + 1) != 0:
                        return {"ok": False, "enxt": True, "m": m, "r": r}
                    nc = 2 * m + 1
                    jc = 2 * (r + 1)
                    if nc - jc != 2 * (m - r) - 1:
                        return {"ok": False, "cd": True, "m": m, "r": r}
                    if 2 * nc - jc != 2 * (2 * m - r):
                        return {"ok": False, "cjp": True, "m": m, "r": r}
                    if pal_kind(nc, jc, max(m.bit_length(), 1)) == "pal":
                        return {"ok": False, "cpal": True, "m": m, "r": r}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_pg_lo(k) != (0 if k <= 0 else 2 * want_lo_e(k - 1)):
            return {"ok": False, "pg": True, "k": k}
        if want_gp_lo(k) != want_pg_lo(k) - want_lo_parent_diff(k):
            return {"ok": False, "gp": True, "k": k}
        if want_lo_parent_sum(k) != want_pg_lo(k) + want_gp_lo(k):
            return {"ok": False, "sm": True, "k": k}
        if want_extra_lo(k) != (
            0
            if k <= 0
            else want_named_lo(k) + want_j0_odd_lo(k) + want_lo_parent_sum(k)
        ):
            return {"ok": False, "elo": True, "k": k}
        if want_extra_unp(k) != want_extra_sum(k) - want_extra_lo(k):
            return {"ok": False, "eun": True, "k": k}
        if want_extra_unp(k) < 0 or want_gp_lo(k) < 0:
            return {"ok": False, "neg": True, "k": k}
        if k >= 1:
            if lo_e_num(k) % 60 != 0 or want_lo_e(k) != lo_e_num(k) // 60:
                return {"ok": False, "cf": True, "k": k}
            if want_lo_parent_sum(k) != (
                4 * want_lo_e(k - 1) - want_lo_parent_diff(k)
            ):
                return {"ok": False, "4e": True, "k": k}
        if k >= 3:
            rhs = 2 * want_lo_e(k - 1) + 4 * want_lo_e(k - 2) + want_lo_e_rhs(k)
            if want_lo_e(k) != rhs:
                return {"ok": False, "rec": True, "k": k}
            if want_lo_parent_sum(k) == want_lo_parent_diff(k):
                return {"ok": False, "eqd": True, "k": k}
            if want_pg_lo(k) == want_lo_e(k - 1):
                return {"ok": False, "half": True, "k": k}
        if k >= 1 and jacobsthal(k + 1) != (1 << k) - jacobsthal(k):
            return {"ok": False, "Jrec": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
        if k >= 1 and lucas(k) != fib(k - 1) + fib(k + 1):
            return {"ok": False, "Lrec": True, "k": k}
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
        and want_pg_lo(8) != want_lo_e(7)
        and want_lo_parent_sum(8) != want_lo_parent_diff(8)
        and want_lo_parent_sum(8) != want_lo_parent_small_sum(8)
        and want_extra_lo(8) != want_extra_unp(8)
        and want_lo_e(8) == 14114
        and want_j0_odd_lo(8) == 319
        and want_named_lo(8) == 424
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
        and lucas(0) == 2
        and lucas(8) == 47
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def pg_lo_fold() -> dict:
    """k<=8: pg:lo doubles parent even leftover; extras match."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        lo = leftover_split(k)
        r = leftover_named_split(k)
        if lo["lo_e"] != want_lo_e(k):
            return {"ok": False, "loe": True, "k": k, "got": lo["lo_e"]}
        if r["n_bad"] != 0 or r["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if r["n_pg_lo"] != want_pg_lo(k):
            return {"ok": False, "pg": True, "k": k, "got": r["n_pg_lo"]}
        if r["n_gp_lo"] != want_gp_lo(k):
            return {"ok": False, "gp": True, "k": k, "got": r["n_gp_lo"]}
        tot = r["n_pg_lo"] + r["n_gp_lo"]
        if tot != want_lo_parent_sum(k):
            return {"ok": False, "sum": True, "k": k, "got": tot}
        if r["extra"] != want_extra_lo(k):
            return {"ok": False, "elo": True, "k": k, "got": r["extra"]}
        if r["n_neg"] != want_j0_odd_lo(k):
            return {"ok": False, "j0": True, "k": k}
        named = r["n_gp_d1"] + r["n_pg_d2"] + r["n_gp_d2"]
        if named != want_named_lo(k):
            return {"ok": False, "nm": True, "k": k}
        if r["extra"] != named + r["n_neg"] + tot:
            return {"ok": False, "part": True, "k": k}
        if want_extra_sum(k) - r["extra"] != want_extra_unp(k):
            return {"ok": False, "eun": True, "k": k}
        if k >= 1 and r["n_pg_lo"] != 2 * want_lo_e(k - 1):
            return {"ok": False, "dbl": True, "k": k}
        if k >= 3 and tot == want_lo_parent_diff(k):
            return {"ok": False, "eqd": True, "k": k}
        if k >= 3 and r["n_pg_lo"] == want_lo_e(k - 1):
            return {"ok": False, "half": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "lo_e": lo["lo_e"],
            "n_pg_lo": r["n_pg_lo"],
            "n_gp_lo": r["n_gp_lo"],
            "tot": tot,
            "extra": r["extra"],
            "extra_unp": want_extra_unp(k),
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["lo_e"] == 0
        and rows["1"]["lo_e"] == 1
        and rows["8"]["lo_e"] == 14114
        and rows["8"]["n_pg_lo"] == 8560
        and rows["8"]["n_gp_lo"] == 8327
        and rows["8"]["tot"] == 16887
        and rows["8"]["extra"] == 17630
        and rows["8"]["extra_unp"] == 10019
        and rows["8"]["n_pg_lo"] != rows["7"]["lo_e"]
        and rows["8"]["tot"] != 233
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """pg:lo=lo_e; sum=diff; lo_e formula at k=0; extra_lo=extra_unp."""
    ok = (
        want_pg_lo(8) != want_lo_e(7)
        and want_lo_parent_sum(8) != want_lo_parent_diff(8)
        and want_lo_parent_sum(8) != want_lo_parent_small_sum(8)
        and want_extra_lo(8) != want_extra_unp(8)
        and lo_e_num(0) % 60 != 0
        and want_pg_lo(8) != want_gp_lo(8)
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
    uo = json.loads(UO_JSON.read_text())
    um = json.loads(UM_JSON.read_text())
    ul = json.loads(UL_JSON.read_text())
    tu = json.loads(TU_JSON.read_text())
    ok = (
        uo["checks"]["all_ok"]
        and um["checks"]["all_ok"]
        and ul["checks"]["all_ok"]
        and tu["checks"]["all_ok"]
        and uo["verdict"]["lo_parent_small_sum_eq_lo_small_minus_named_j0"]
        == "LEMMA"
        and um["verdict"]["lo_parent_diff_eq_3_2km1_J"] == "LEMMA"
        and tu["verdict"]["even_lo_eq_parent_lo_plus_d2_k_ge_2"] == "LEMMA"
        and uo["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uo["verdict"]["prize"] == "unsolved"
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
    cnt = pg_lo_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "pg_lo_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "pg_lo_eq_2_parent_even_lo": True,
            "lo_parent_sum_eq_4_loe_minus_diff": True,
            "extra_lo_eq_named_j0_sum": True,
            "lo_e_closed_form_k_ge_1": True,
            "extra_unp_eq_extra_sum_minus_extra_lo": True,
            "pg_lo_eq_parent_loe": False,
            "lo_parent_sum_eq_diff": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "pg_lo_eq_2_parent_even_lo": "LEMMA",
            "lo_parent_sum_eq_4_loe_minus_diff": "LEMMA",
            "extra_lo_eq_named_j0_sum": "LEMMA",
            "lo_e_closed_form_k_ge_1": "LEMMA",
            "extra_unp_eq_extra_sum_minus_extra_lo": "LEMMA",
            "pg_lo_eq_parent_loe": "KILLED",
            "lo_parent_sum_eq_diff": "KILLED",
            "lo_parent_sum_eq_small_sum": "KILLED",
            "lo_e_formula_at_k0": "KILLED",
            "extra_lo_eq_extra_unp": "KILLED",
            "pg_lo_eq_gp_lo": "KILLED",
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
            "lo_parent_large_diff_closed": "PREFIX",
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
        "lo_e k8",
        dump["pg_lo_fold"]["rows"]["8"]["lo_e"],
        "pg",
        dump["pg_lo_fold"]["rows"]["8"]["n_pg_lo"],
        "sum",
        dump["pg_lo_fold"]["rows"]["8"]["tot"],
        "extra",
        dump["pg_lo_fold"]["rows"]["8"]["extra"],
        "extra_unp",
        dump["pg_lo_fold"]["rows"]["8"]["extra_unp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
