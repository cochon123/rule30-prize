#!/usr/bin/env python3
"""Cycle UE: leftover plus unpaired is 2^{k+1}(F_{k+4}-3) for k>=1.

Cycle TU leftover is pal-pair minus 4U for k>=1. Cycle UD pal-pair
plus unpaired is 2^{k+1}(F_{k+4}-1). Subtract pal-center to get
leftover plus unpaired 2^{k+1}(F_{k+4}-3). Dies at k=0 because
d=2 overlaps clip-edge. Do not claim leftover alone equals that
form. Do not PREFIX leftover extra or unpaired extra separately.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ue.py --certify
Dump: research/cycle_ue.json
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
from cycle_ta import pal_split
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_ty import want_pair_from_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pal_left, want_pair_unp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UD_JSON = Path(__file__).resolve().parent / "cycle_ud.json"
TU_JSON = Path(__file__).resolve().parent / "cycle_tu.json"
TY_JSON = Path(__file__).resolve().parent / "cycle_ty.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_lo_unp(k: int) -> int:
    """Leftover plus unpaired: 2^{k+1}(F_{k+4}-3), identity for k>=1."""
    return (1 << (k + 1)) * (fib(k + 4) - 3)


def tot_form() -> dict:
    """k<=64: lo+unp = pair+unp - 4U; F identity; k=0 form is 0."""
    n_ok = 0
    if want_lo_unp(0) != 0 or want_lo_unp(1) != 8:
        return {"ok": False, "k01": True}
    if want_lo_unp(8) != 72192 or want_lo_unp(8) == 45858:
        return {"ok": False, "k8": True}
    if want_pair_unp(0) - want_pal_c(0) != 0:
        return {"ok": False, "k0a": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
        if want_lo_unp(k) != want_pair_unp(k) - want_pal_c(k):
            return {"ok": False, "sub": True, "k": k}
        if want_lo_unp(k) != (1 << (k + 1)) * (fib(k + 4) - 3):
            return {"ok": False, "F": True, "k": k}
        if want_lo_unp(k) + 2 * want_pal_c(k) != want_pal_left(k):
            return {"ok": False, "pl": True, "k": k}
        if want_pair_from_lo(want_lo_unp(k), k) != want_pair_unp(k):
            return {"ok": False, "ty": True, "k": k}
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
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def lo_unp_fold() -> dict:
    """k<=8: leftover+unp Fibonacci for k>=1; dies at k=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        ps = pal_split(k, None)
        if ps["n_pair"] + ps["n_unp"] != want_pair_unp(k):
            return {"ok": False, "pu": True, "k": k, **ps}
        if ps["n_pal"] != want_pal_c(k):
            return {"ok": False, "pc": True, "k": k, **ps}
        lo_from_pair = ps["n_pair"] - want_pal_c(k)
        if lo_from_pair + ps["n_unp"] != want_lo_unp(k):
            return {"ok": False, "alg": True, "k": k, **ps}
        if k >= 1:
            if lo_from_pair + ps["n_unp"] != want_lo_unp(k):
                return {"ok": False, "lu": True, "k": k, **ps}
            if lo_from_pair == want_lo_unp(k):
                return {"ok": False, "lo": True, "k": k, **ps}
        else:
            if ps["n_pair"] != 3 or ps["n_unp"] != 1:
                return {"ok": False, "k0": True, **ps}
            if 0 + ps["n_unp"] == want_lo_unp(0):
                return {"ok": False, "k0lu": True, **ps}
        n_ok += 1
        rows[str(k)] = {
            "n_pal": ps["n_pal"],
            "n_pair": ps["n_pair"],
            "n_unp": ps["n_unp"],
            "lo_from_pair": lo_from_pair,
            "lo_unp": lo_from_pair + ps["n_unp"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["n_pair"] == 3
        and rows["0"]["n_unp"] == 1
        and rows["0"]["lo_unp"] == 0
        and rows["0"]["n_unp"] != want_lo_unp(0)
        and rows["1"]["lo_from_pair"] == 4
        and rows["1"]["n_unp"] == 4
        and rows["1"]["lo_unp"] == 8
        and rows["8"]["n_pal"] == 1024
        and rows["8"]["n_pair"] == 46882
        and rows["8"]["n_unp"] == 26334
        and rows["8"]["lo_from_pair"] == 45858
        and rows["8"]["lo_unp"] == 72192
        and rows["8"]["lo_from_pair"] != 72192
        and rows["8"]["lo_unp"] != (1 << 10)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """Leftover alone is the F form; formula at k=0."""
    ok = (
        want_lo_unp(8) != 45858
        and want_lo_unp(0) != 1
        and want_lo_unp(1) != 4
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
    ud = json.loads(UD_JSON.read_text())
    tu = json.loads(TU_JSON.read_text())
    ty = json.loads(TY_JSON.read_text())
    ok = (
        ud["checks"]["all_ok"]
        and tu["checks"]["all_ok"]
        and ty["checks"]["all_ok"]
        and ud["verdict"]["pair_unp_eq_2km1_Fm1"] == "LEMMA"
        and ud["verdict"]["pal_c_eq_4U"] == "LEMMA"
        and tu["verdict"]["lo_count_eq_pair_minus_4U_k_ge_1"] == "LEMMA"
        and ty["verdict"]["pair_eq_lo_plus_4U_k_ge_1"] == "LEMMA"
        and ud["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ud["verdict"]["prize"] == "unsolved"
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
    cnt = lo_unp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "lo_unp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_unp_eq_2km1_Fm3_k_ge_1": True,
            "lo_eq_2km1_Fm3": False,
            "lo_unp_eq_form_k0": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_unp_eq_2km1_Fm3_k_ge_1": "LEMMA",
            "lo_eq_2km1_Fm3": "KILLED",
            "lo_unp_eq_form_k0": "KILLED",
            "G_n_n_eq_n_mod_2": "KILLED",
            "pal_c_eq_2km1": "KILLED",
            "pair_unp_eq_4U": "KILLED",
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
        "lo+unp k8",
        dump["lo_unp_fold"]["rows"]["8"]["lo_unp"],
        "lo",
        dump["lo_unp_fold"]["rows"]["8"]["lo_from_pair"],
        "unp",
        dump["lo_unp_fold"]["rows"]["8"]["n_unp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
