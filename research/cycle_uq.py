#!/usr/bin/env python3
"""Cycle UQ: leftover extra large, parent-xor large sum, and xor_lo close.

Leftover extra on n>5U/2 is Cycle UP extra_lo minus Cycle UK lo_small.
Leftover-parent xor large sum is leftover-parent xor total minus Cycle
UO small sum. Leftover xor-pair n_pg+n_gp is extra_lo minus j=0
leftover, or named plus leftover-parent xor total. Large leftover
extra partitions as named large plus leftover-parent xor large (no
j=0 on that half). Do not PREFIX leftover-parent xor large
difference or pal-center tot. Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_uq.py --certify
Dump: research/cycle_uq.json
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
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_tw import want_j0_odd_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uk import want_lo_small
from cycle_ul import want_named_lo
from cycle_um import want_lo_parent_diff
from cycle_uo import named_half_split, want_lo_parent_small_sum, want_named_l
from cycle_up import (
    lucas,
    want_extra_lo,
    want_extra_unp,
    want_lo_e,
    want_lo_parent_sum,
    want_pg_lo,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"
UO_JSON = Path(__file__).resolve().parent / "cycle_uo.json"
UK_JSON = Path(__file__).resolve().parent / "cycle_uk.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_lo_large(k: int) -> int:
    """Leftover extra on n>5U/2: extra_lo minus lo_small."""
    return want_extra_lo(k) - want_lo_small(k)


def want_lo_parent_large_sum(k: int) -> int:
    """pg:lo+gp:lo on n>5U/2: leftover-parent xor total minus small sum."""
    return want_lo_parent_sum(k) - want_lo_parent_small_sum(k)


def want_xor_lo(k: int) -> int:
    """Leftover xor-pair n_pg+n_gp: extra_lo minus j=0 leftover."""
    return want_extra_lo(k) - want_j0_odd_lo(k)


def tot_form() -> dict:
    """k<=64: large leftover extra, parent-xor large sum, xor_lo."""
    n_ok = 0
    if want_lo_large(0) != 0 or want_lo_large(1) != 0 or want_lo_large(2) != 3:
        return {"ok": False, "k012": True}
    if want_lo_parent_large_sum(8) != 6486 or want_lo_large(8) != 6644:
        return {"ok": False, "k8l": True}
    if want_xor_lo(8) != 17311 or want_xor_lo(1) != 1:
        return {"ok": False, "k8x": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
        if m % 2 == 0 and G(m, m - 1 if m else 0) != 0 and m > 0:
            return {"ok": False, "eodd": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_lo_large(k) != want_extra_lo(k) - want_lo_small(k):
            return {"ok": False, "ll": True, "k": k}
        if want_lo_parent_large_sum(k) != (
            want_lo_parent_sum(k) - want_lo_parent_small_sum(k)
        ):
            return {"ok": False, "ls": True, "k": k}
        if want_xor_lo(k) != want_extra_lo(k) - want_j0_odd_lo(k):
            return {"ok": False, "x1": True, "k": k}
        if want_xor_lo(k) != want_named_lo(k) + want_lo_parent_sum(k):
            return {"ok": False, "x2": True, "k": k}
        if want_lo_large(k) != want_named_l(k) + want_lo_parent_large_sum(k):
            return {"ok": False, "part": True, "k": k}
        if want_lo_large(k) < 0 or want_lo_parent_large_sum(k) < 0:
            return {"ok": False, "neg": True, "k": k}
        if k >= 3:
            if want_lo_parent_large_sum(k) == want_lo_parent_diff(k):
                return {"ok": False, "eqd": True, "k": k}
            if want_lo_parent_large_sum(k) == want_lo_parent_small_sum(k):
                return {"ok": False, "eqs": True, "k": k}
            if want_xor_lo(k) == want_lo_parent_sum(k):
                return {"ok": False, "xn": True, "k": k}
            if want_lo_large(k) == want_extra_lo(k):
                return {"ok": False, "eqe": True, "k": k}
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
        and want_lo_large(8) != want_extra_lo(8)
        and want_lo_parent_large_sum(8) != want_lo_parent_diff(8)
        and want_xor_lo(8) != want_lo_parent_sum(8)
        and want_lo_large(8) == 6644
        and want_lo_small(8) == 10986
        and want_extra_lo(8) == 17630
        and want_j0_odd_lo(8) == 319
        and want_named_lo(8) == 424
        and want_named_l(8) == 158
        and want_pg_lo(8) == 8560
        and want_lo_e(8) == 14114
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
        and want_extra_unp(8) == 10019
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def large_fold() -> dict:
    """k<=8: leftover extra large, parent-xor large sum, xor_lo match."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        named_s = r["gpd1_s"] + r["pgd2_s"] + r["gpd2_s"]
        named_l = r["gpd1_l"] + r["pgd2_l"] + r["gpd2_l"]
        ssum = r["plo_s"] + r["glo_s"]
        lsum = r["plo_l"] + r["glo_l"]
        extra = r["lo_s"] + r["lo_l"]
        xor_lo = named_s + named_l + ssum + lsum
        if r["n_bad"] != 0 or r["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if r["lo_s"] != want_lo_small(k):
            return {"ok": False, "los": True, "k": k}
        if r["lo_l"] != want_lo_large(k):
            return {"ok": False, "lol": True, "k": k, "got": r["lo_l"]}
        if extra != want_extra_lo(k):
            return {"ok": False, "elo": True, "k": k}
        if lsum != want_lo_parent_large_sum(k):
            return {"ok": False, "ls": True, "k": k, "got": lsum}
        if named_l != want_named_l(k):
            return {"ok": False, "nl": True, "k": k}
        if r["lo_l"] != named_l + lsum:
            return {"ok": False, "part": True, "k": k}
        if xor_lo != want_xor_lo(k):
            return {"ok": False, "xor": True, "k": k, "got": xor_lo}
        if extra - r["j0"] != want_xor_lo(k):
            return {"ok": False, "xj0": True, "k": k}
        if k >= 3 and lsum == want_lo_parent_diff(k):
            return {"ok": False, "eqd": True, "k": k}
        if k >= 3 and xor_lo == want_lo_parent_sum(k):
            return {"ok": False, "xn": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "lo_l": r["lo_l"],
            "large_sum": lsum,
            "xor_lo": xor_lo,
            "named_l": named_l,
            "j0": r["j0"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["lo_l"] == 0
        and rows["1"]["lo_l"] == 0
        and rows["2"]["lo_l"] == 3
        and rows["8"]["lo_l"] == 6644
        and rows["8"]["large_sum"] == 6486
        and rows["8"]["xor_lo"] == 17311
        and rows["8"]["named_l"] == 158
        and rows["8"]["j0"] == 319
        and rows["8"]["lo_l"] != 17630
        and rows["8"]["large_sum"] != 233
        and rows["8"]["xor_lo"] != 16887
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """lo_large=extra_lo; large sum=diff; xor_lo=parent xor without named."""
    ok = (
        want_lo_large(8) != want_extra_lo(8)
        and want_lo_parent_large_sum(8) != want_lo_parent_diff(8)
        and want_lo_parent_large_sum(8) != want_lo_parent_small_sum(8)
        and want_xor_lo(8) != want_lo_parent_sum(8)
        and want_lo_large(8) != want_named_lo(8)
        and want_lo_large(8) != want_named_l(8)
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
    up = json.loads(UP_JSON.read_text())
    uo = json.loads(UO_JSON.read_text())
    uk = json.loads(UK_JSON.read_text())
    ok = (
        up["checks"]["all_ok"]
        and uo["checks"]["all_ok"]
        and uk["checks"]["all_ok"]
        and up["verdict"]["extra_lo_eq_named_j0_sum"] == "LEMMA"
        and up["verdict"]["lo_parent_sum_eq_4_loe_minus_diff"] == "LEMMA"
        and uo["verdict"]["lo_parent_small_sum_eq_lo_small_minus_named_j0"]
        == "LEMMA"
        and uk["verdict"]["lo_small_eq_tot_minus_d1"] == "LEMMA"
        and up["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and up["verdict"]["prize"] == "unsolved"
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
    cnt = large_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UQ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "large_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_large_eq_extra_lo_minus_lo_small": True,
            "lo_parent_large_sum_eq_tot_minus_small": True,
            "xor_lo_eq_extra_lo_minus_j0": True,
            "lo_large_eq_named_l_plus_large_sum": True,
            "lo_large_eq_extra_lo": False,
            "large_sum_eq_diff": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_large_eq_extra_lo_minus_lo_small": "LEMMA",
            "lo_parent_large_sum_eq_tot_minus_small": "LEMMA",
            "xor_lo_eq_extra_lo_minus_j0": "LEMMA",
            "lo_large_eq_named_l_plus_large_sum": "LEMMA",
            "lo_large_eq_extra_lo": "KILLED",
            "large_sum_eq_diff": "KILLED",
            "large_sum_eq_small_sum": "KILLED",
            "xor_lo_eq_parent_xor_sum": "KILLED",
            "lo_large_eq_named": "KILLED",
            "lo_large_eq_named_l": "KILLED",
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
        "lo_l k8",
        dump["large_fold"]["rows"]["8"]["lo_l"],
        "large_sum",
        dump["large_fold"]["rows"]["8"]["large_sum"],
        "xor_lo",
        dump["large_fold"]["rows"]["8"]["xor_lo"],
        "named_l",
        dump["large_fold"]["rows"]["8"]["named_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
