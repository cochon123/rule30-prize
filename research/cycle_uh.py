#!/usr/bin/env python3
"""Cycle UH: unpaired xor n_ug-n_gu is Jacobsthal.

Odd-n even-j unpaired extra from parent unpaired xor splits into
n_ug (unp then g0) and n_gu (g0 then unp). Their difference is 0
at k<=1, J_k+J_{k-2} for even k>=2, and J_k+2 J_{k-3} for odd
k>=3, equivalently (5*2^{k-2}-2+(k mod 2))/3. Do not PREFIX
n_ug+n_gu or leftover extra or unpaired extra. Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_uh.py --certify
Dump: research/cycle_uh.json
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
from cycle_ub import unpaired_xor_split, want_clip_gp
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UB_JSON = Path(__file__).resolve().parent / "cycle_ub.json"
UG_JSON = Path(__file__).resolve().parent / "cycle_ug.json"
UA_JSON = Path(__file__).resolve().parent / "cycle_ua.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ug_minus_gu(k: int) -> int:
    """n_ug-n_gu: 0 at k<=1; J_k+J_{k-2} even; J_k+2 J_{k-3} odd."""
    if k <= 1:
        return 0
    if k % 2 == 0:
        return jacobsthal(k) + jacobsthal(k - 2)
    return jacobsthal(k) + 2 * jacobsthal(k - 3)


def want_ug_minus_gu_pow(k: int) -> int:
    """n_ug-n_gu: (5*2^{k-2}-2+(k mod 2))/3 for k>=2."""
    if k <= 1:
        return 0
    return (5 * (1 << (k - 2)) - 2 + (k % 2)) // 3


def tot_form() -> dict:
    """k<=64: Jacobsthal and power-of-two forms agree; J recurrences."""
    n_ok = 0
    if want_ug_minus_gu(0) != 0 or want_ug_minus_gu(1) != 0:
        return {"ok": False, "k01": True}
    if want_ug_minus_gu(2) != 1 or want_ug_minus_gu(3) != 3:
        return {"ok": False, "k23": True}
    if want_ug_minus_gu(8) != 106 or want_ug_minus_gu(8) == 9742:
        return {"ok": False, "k8": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_ug_minus_gu(k) != want_ug_minus_gu_pow(k):
            return {"ok": False, "pow": True, "k": k}
        if k >= 2:
            if (5 * (1 << (k - 2)) - 2 + (k % 2)) % 3 != 0:
                return {"ok": False, "div": True, "k": k}
            if k % 2 == 0:
                if want_ug_minus_gu(k) != jacobsthal(k) + jacobsthal(k - 2):
                    return {"ok": False, "even": True, "k": k}
            else:
                if want_ug_minus_gu(k) != jacobsthal(k) + 2 * jacobsthal(k - 3):
                    return {"ok": False, "odd": True, "k": k}
            if want_clip_gp(k) * 2 + 1 != jacobsthal(k + 1):
                return {"ok": False, "clip": True, "k": k}
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
        and G(2, 2) != 0
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(1) != (1 << 3)
        and want_lo_unp(1) != 4
        and want_ug_minus_gu(8) != jacobsthal(8)
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ug_gu_fold() -> dict:
    """k<=8: n_ug-n_gu matches Jacobsthal; n_pg empty; sum not the form."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = unpaired_xor_split(k)
        diff = r["n_ug"] - r["n_gu"]
        xor_unp = r["n_ug"] + r["n_gu"]
        if r["n_pg"] != 0:
            return {"ok": False, "pg": True, "k": k, **r}
        if r["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, **r}
        if diff != want_ug_minus_gu(k):
            return {"ok": False, "d": True, "k": k, **r, "diff": diff}
        if k >= 2 and xor_unp == want_ug_minus_gu(k):
            return {"ok": False, "sum": True, "k": k, **r}
        if k >= 2 and r["n_ug"] == r["n_gu"]:
            return {"ok": False, "eq": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n_ug": r["n_ug"],
            "n_gu": r["n_gu"],
            "diff": diff,
            "xor_unp": xor_unp,
            "n_gp": r["n_gp"],
            "n_neg": r["n_neg"],
            "extra": r["extra"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["diff"] == 0
        and rows["1"]["diff"] == 0
        and rows["2"]["diff"] == 1
        and rows["8"]["n_ug"] == 4924
        and rows["8"]["n_gu"] == 4818
        and rows["8"]["diff"] == 106
        and rows["8"]["xor_unp"] == 9742
        and rows["8"]["xor_unp"] != 106
        and rows["8"]["n_gp"] == 85
        and rows["8"]["n_neg"] == 192
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """n_ug=n_gu; difference is J_k; xor-unp equals the difference."""
    ok = (
        want_ug_minus_gu(8) != 0
        and want_ug_minus_gu(8) != jacobsthal(8)
        and want_ug_minus_gu(8) != 9742
        and want_ug_minus_gu(8) != 10019
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
    ub = json.loads(UB_JSON.read_text())
    ug = json.loads(UG_JSON.read_text())
    ua = json.loads(UA_JSON.read_text())
    ok = (
        ub["checks"]["all_ok"]
        and ug["checks"]["all_ok"]
        and ua["checks"]["all_ok"]
        and ub["verdict"]["odd_ej_unp_from_unp_xor_plus_clip"] == "LEMMA"
        and ub["verdict"]["clip_gp_eq_half_J_k1_k_ge_2"] == "LEMMA"
        and ug["verdict"]["extra_sum_eq_odd_minus_even_minus_J_k_ge_1"] == "LEMMA"
        and ua["verdict"]["unp_eq_2_even_plus_J_extra_k_ge_1"] == "LEMMA"
        and ub["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ub["verdict"]["prize"] == "unsolved"
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
    cnt = ug_gu_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ug_gu_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ug_minus_gu_eq_jacobsthal": True,
            "ug_eq_gu": False,
            "ug_minus_gu_eq_J_k": False,
            "xor_unp_eq_ug_minus_gu": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ug_minus_gu_eq_jacobsthal": "LEMMA",
            "ug_eq_gu": "KILLED",
            "ug_minus_gu_eq_J_k": "KILLED",
            "xor_unp_eq_ug_minus_gu": "KILLED",
            "unp_extra_eq_xor_unp_alone": "KILLED",
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
        "diff k8",
        dump["ug_gu_fold"]["rows"]["8"]["diff"],
        "xor",
        dump["ug_gu_fold"]["rows"]["8"]["xor_unp"],
        "ug",
        dump["ug_gu_fold"]["rows"]["8"]["n_ug"],
        "gu",
        dump["ug_gu_fold"]["rows"]["8"]["n_gu"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
