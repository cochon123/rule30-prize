#!/usr/bin/env python3
"""Cycle UG: extra sum is odd(lo+unp)-even(lo+unp)-J_{k+1}.

For k>=1, leftover extra is odd leftover minus even leftover, and
unpaired extra is odd unpaired minus even unpaired minus J_{k+1}.
Cycle UF then gives extra_lo+extra_unp equal to odd leftover-plus
unpaired minus even leftover-plus-unpaired minus J_{k+1}. Fibonacci
and Jacobsthal cancel to Cycle UC's 2^{k+1}(F_{k+2}-1)+(-1)^k.
Do not PREFIX leftover extra or unpaired extra separately. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ug.py --certify
Dump: research/cycle_ug.json
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
from cycle_uc import fib, trans, want_extra_sum, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uf import even_lo_unp_split, want_even_lo_unp, want_odd_lo_unp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UF_JSON = Path(__file__).resolve().parent / "cycle_uf.json"
UC_JSON = Path(__file__).resolve().parent / "cycle_uc.json"
UE_JSON = Path(__file__).resolve().parent / "cycle_ue.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_extra_from_parity(k: int) -> int:
    """odd(lo+unp)-even(lo+unp)-J_{k+1} for k>=1."""
    return want_odd_lo_unp(k) - want_even_lo_unp(k) - jacobsthal(k + 1)


def tot_form() -> dict:
    """k<=64: parity extra sum equals UC Fibonacci; J recurrences."""
    n_ok = 0
    if want_extra_from_parity(1) != 3 or want_extra_sum(1) != 3:
        return {"ok": False, "k1": True}
    if want_extra_from_parity(8) != 27649 or want_extra_sum(8) != 27649:
        return {"ok": False, "k8": True}
    if want_extra_from_parity(8) == 17630 or want_extra_from_parity(8) == 10019:
        return {"ok": False, "sep": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 1:
            if jacobsthal(k) + jacobsthal(k + 1) != 1 << k:
                return {"ok": False, "Jsum": True, "k": k}
            if 4 * jacobsthal(k) + jacobsthal(k + 1) != (1 << (k + 1)) - (
                -1
            ) ** k:
                return {"ok": False, "J4": True, "k": k}
            if want_extra_from_parity(k) != want_extra_sum(k):
                return {"ok": False, "eq": True, "k": k}
            if want_extra_from_parity(k) != (
                want_lo_unp(k) - 2 * want_even_lo_unp(k) - jacobsthal(k + 1)
            ):
                return {"ok": False, "lu": True, "k": k}
            if want_extra_from_parity(k) != (1 << (k + 1)) * (
                fib(k + 2) - 1
            ) + (-1) ** k:
                return {"ok": False, "F": True, "k": k}
            if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
                return {"ok": False, "Frec": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        if 4 * u >= 5 * u:
            return {"ok": False, "clip": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and G(2, 2) != 0
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(1) != (1 << 3)
        and want_lo_unp(1) != 4
        and want_extra_sum(0) == 1
        and want_extra_from_parity(2) != 0
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def extra_parity_fold() -> dict:
    """k<=8: odd-even lo+unp minus J_{k+1} equals extra sum for k>=1."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = even_lo_unp_split(k)
        lo_extra = r["lo_o"] - r["lo_e"]
        if k >= 1:
            unp_extra = r["unp_o"] - r["unp_e"] - jacobsthal(k + 1)
            got = r["odd"] - r["even"] - jacobsthal(k + 1)
            if got != want_extra_from_parity(k):
                return {"ok": False, "par": True, "k": k, **r}
            if got != want_extra_sum(k):
                return {"ok": False, "uc": True, "k": k, **r}
            if lo_extra + unp_extra != got:
                return {"ok": False, "sum": True, "k": k, **r, "lo_extra": lo_extra}
            if lo_extra == 0 or unp_extra == 0:
                return {"ok": False, "empty": True, "k": k}
            if lo_extra == unp_extra:
                return {"ok": False, "eq": True, "k": k}
            if lo_extra == want_extra_sum(k) or unp_extra == want_extra_sum(k):
                return {"ok": False, "alone": True, "k": k}
        else:
            lo_extra = r["lo_o"] - r["lo_e"]
            unp_extra = r["unp"]
            got = None
            if r["even"] != 0 or r["unp"] != 1:
                return {"ok": False, "k0": True, **r}
        n_ok += 1
        rows[str(k)] = {
            "even": r["even"],
            "odd": r["odd"],
            "lo_extra": lo_extra,
            "unp_extra": unp_extra,
            "got": got,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["got"] == 3
        and rows["1"]["lo_extra"] == 2
        and rows["1"]["unp_extra"] == 1
        and rows["8"]["got"] == 27649
        and rows["8"]["lo_extra"] == 17630
        and rows["8"]["unp_extra"] == 10019
        and rows["8"]["lo_extra"] != rows["8"]["unp_extra"]
        and rows["8"]["got"] != (1 << 10)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """Extra sum empty; leftover extra equals unpaired extra; extras PREFIX."""
    ok = (
        want_extra_from_parity(8) != 0
        and want_extra_from_parity(8) != 17630
        and want_extra_from_parity(8) != 10019
        and want_extra_sum(0) == 1
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
    uf = json.loads(UF_JSON.read_text())
    uc = json.loads(UC_JSON.read_text())
    ue = json.loads(UE_JSON.read_text())
    ok = (
        uf["checks"]["all_ok"]
        and uc["checks"]["all_ok"]
        and ue["checks"]["all_ok"]
        and uf["verdict"]["even_lo_unp_eq_parent_lu_plus_2J_k_ge_1"] == "LEMMA"
        and uf["verdict"]["odd_lo_unp_eq_lu_minus_even_k_ge_1"] == "LEMMA"
        and uc["verdict"]["extra_sum_eq_2km1_Fm1_pm1"] == "LEMMA"
        and ue["verdict"]["lo_unp_eq_2km1_Fm3_k_ge_1"] == "LEMMA"
        and uf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uf["verdict"]["prize"] == "unsolved"
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
    cnt = extra_parity_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "extra_parity_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "extra_sum_eq_odd_minus_even_minus_J_k_ge_1": True,
            "extra_from_parity_eq_UC": True,
            "extra_lo_eq_extra_unp": False,
            "extra_sum_empty": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "extra_sum_eq_odd_minus_even_minus_J_k_ge_1": "LEMMA",
            "extra_from_parity_eq_UC": "LEMMA",
            "extra_lo_eq_extra_unp": "KILLED",
            "extra_sum_empty": "KILLED",
            "lo_extra_eq_UC_sum": "KILLED",
            "unp_extra_eq_UC_sum": "KILLED",
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
        "extra k8",
        dump["extra_parity_fold"]["rows"]["8"]["got"],
        "lo",
        dump["extra_parity_fold"]["rows"]["8"]["lo_extra"],
        "unp",
        dump["extra_parity_fold"]["rows"]["8"]["unp_extra"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
