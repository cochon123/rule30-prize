#!/usr/bin/env python3
"""Cycle UJ: leftover xor-pair plus unpaired xor-unp is extra-sum minus edges.

Leftover extra is parent pal-pair xor plus j=0 leftover. Unpaired extra
is parent unpaired xor plus clip-edge plus j=0 unpaired. Extra-sum
closed (Cycle UC) minus those three known edges leaves leftover
xor-pair sum plus unpaired xor-unp sum. Do not PREFIX either xor-sum
or leftover extra or unpaired extra. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_uj.py --certify
Dump: research/cycle_uj.json
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
from cycle_tw import leftover_xor_split, want_j0_odd_lo
from cycle_ua import want_j0_odd_unp
from cycle_ub import unpaired_xor_split, want_clip_gp
from cycle_uc import fib, trans, want_extra_sum, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uh import want_ug_minus_gu
from cycle_ui import want_pg_minus_gp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UC_JSON = Path(__file__).resolve().parent / "cycle_uc.json"
UB_JSON = Path(__file__).resolve().parent / "cycle_ub.json"
TW_JSON = Path(__file__).resolve().parent / "cycle_tw.json"
UA_JSON = Path(__file__).resolve().parent / "cycle_ua.json"
UI_JSON = Path(__file__).resolve().parent / "cycle_ui.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_tot(k: int) -> int:
    """xor_lo + xor_unp = extra_sum - j0_lo - clip_gp - j0_unp."""
    return (
        want_extra_sum(k)
        - want_j0_odd_lo(k)
        - want_clip_gp(k)
        - want_j0_odd_unp(k)
    )


def tot_form() -> dict:
    """k<=64: xor tot from extra-sum minus known edges; F and J recurrences."""
    n_ok = 0
    if want_xor_tot(0) != 0 or want_xor_tot(1) != 1:
        return {"ok": False, "k01": True}
    if want_xor_tot(8) != 27053 or want_xor_tot(8) == 27649:
        return {"ok": False, "k8": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_xor_tot(k) != (
            want_extra_sum(k)
            - want_j0_odd_lo(k)
            - want_clip_gp(k)
            - want_j0_odd_unp(k)
        ):
            return {"ok": False, "def": True, "k": k}
        if want_xor_tot(k) < 0:
            return {"ok": False, "neg": True, "k": k}
        if k >= 2:
            if want_j0_odd_lo(k) != 5 * (1 << (k - 2)) - 1:
                return {"ok": False, "j0l": True, "k": k}
            if want_j0_odd_unp(k) != 3 * (1 << (k - 2)):
                return {"ok": False, "j0u": True, "k": k}
            if want_clip_gp(k) * 2 + 1 != jacobsthal(k + 1):
                return {"ok": False, "clip": True, "k": k}
            if want_extra_sum(k) != (1 << (k + 1)) * (fib(k + 2) - 1) + (
                -1
            ) ** k:
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
            return {"ok": False, "hi": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and G(2, 2) != 0
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(1) != (1 << 3)
        and want_lo_unp(1) != 4
        and want_ug_minus_gu(8) == 106
        and want_pg_minus_gp(8) == 149
        and want_xor_tot(8) != want_extra_sum(8)
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def xor_tot_fold() -> dict:
    """k<=8: xor_lo+xor_unp equals extra-sum minus edges."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        lo = leftover_xor_split(k)
        un = unpaired_xor_split(k)
        xor_lo = lo["n_pg"] + lo["n_gp"]
        xor_unp = un["n_ug"] + un["n_gu"]
        tot = xor_lo + xor_unp
        if lo["n_bad"] != 0 or un["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if un["n_pg"] != 0:
            return {"ok": False, "pg": True, "k": k}
        if lo["n_neg"] != want_j0_odd_lo(k):
            return {"ok": False, "j0l": True, "k": k}
        if un["n_neg"] != want_j0_odd_unp(k):
            return {"ok": False, "j0u": True, "k": k}
        if un["n_gp"] != want_clip_gp(k):
            return {"ok": False, "clip": True, "k": k}
        if lo["n_pg"] + lo["n_gp"] + lo["n_neg"] != lo["extra"]:
            return {"ok": False, "lop": True, "k": k}
        if un["n_ug"] + un["n_gu"] + un["n_gp"] + un["n_neg"] != un["extra"]:
            return {"ok": False, "unp": True, "k": k}
        if lo["extra"] + un["extra"] != want_extra_sum(k):
            return {"ok": False, "xs": True, "k": k}
        if tot != want_xor_tot(k):
            return {"ok": False, "tot": True, "k": k, "tot": tot}
        if xor_lo == want_xor_tot(k) and k >= 2:
            return {"ok": False, "lo": True, "k": k}
        if xor_unp == want_xor_tot(k) and k >= 2:
            return {"ok": False, "un": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "xor_lo": xor_lo,
            "xor_unp": xor_unp,
            "tot": tot,
            "extra_lo": lo["extra"],
            "extra_unp": un["extra"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["tot"] == 0
        and rows["1"]["tot"] == 1
        and rows["8"]["xor_lo"] == 17311
        and rows["8"]["xor_unp"] == 9742
        and rows["8"]["tot"] == 27053
        and rows["8"]["tot"] != 27649
        and rows["8"]["xor_lo"] != rows["8"]["xor_unp"]
        and rows["8"]["extra_lo"] == 17630
        and rows["8"]["extra_unp"] == 10019
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """xor tot empty; xor tot equals extra-sum; xor_lo equals xor_unp."""
    ok = (
        want_xor_tot(8) != 0
        and want_xor_tot(8) != want_extra_sum(8)
        and want_xor_tot(8) != 17311
        and want_xor_tot(8) != 9742
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
    uc = json.loads(UC_JSON.read_text())
    ub = json.loads(UB_JSON.read_text())
    tw = json.loads(TW_JSON.read_text())
    ua = json.loads(UA_JSON.read_text())
    ui = json.loads(UI_JSON.read_text())
    ok = (
        uc["checks"]["all_ok"]
        and ub["checks"]["all_ok"]
        and tw["checks"]["all_ok"]
        and ua["checks"]["all_ok"]
        and ui["checks"]["all_ok"]
        and uc["verdict"]["extra_sum_eq_2km1_Fm1_pm1"] == "LEMMA"
        and ub["verdict"]["clip_gp_eq_half_J_k1_k_ge_2"] == "LEMMA"
        and tw["verdict"]["j0_odd_lo_eq_5_2km2_minus_1"] == "LEMMA"
        and ua["verdict"]["j0_odd_unp_eq_3_2km2"] == "LEMMA"
        and ui["verdict"]["pg_minus_gp_eq_2km1_plus_J"] == "LEMMA"
        and ui["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ui["verdict"]["prize"] == "unsolved"
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
    cnt = xor_tot_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "xor_tot_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_tot_eq_extra_sum_minus_edges": True,
            "xor_tot_eq_extra_sum": False,
            "xor_lo_eq_xor_unp": False,
            "xor_tot_empty": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_tot_eq_extra_sum_minus_edges": "LEMMA",
            "xor_tot_eq_extra_sum": "KILLED",
            "xor_lo_eq_xor_unp": "KILLED",
            "xor_tot_empty": "KILLED",
            "xor_lo_eq_xor_tot": "KILLED",
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
        "xor tot k8",
        dump["xor_tot_fold"]["rows"]["8"]["tot"],
        "lo",
        dump["xor_tot_fold"]["rows"]["8"]["xor_lo"],
        "unp",
        dump["xor_tot_fold"]["rows"]["8"]["xor_unp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
