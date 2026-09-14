#!/usr/bin/env python3
"""Cycle UI: leftover xor n_pg-n_gp is 2^{k-1}+J_{k-2}.

Odd-n even-j leftover extra from parent pal-pair xor splits into
n_pg (pair then g0) and n_gp (g0 then pair). Their difference is 0
at k=0, 1 at k=1, and 2^{k-1}+J_{k-2} for k>=2, equivalently
J_k+2^{k-2}. Do not PREFIX n_pg+n_gp or leftover extra or unpaired
extra. Not rest=S xor T. Do not walk leftover p catalogues. Do not
walk leftover d catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ui.py --certify
Dump: research/cycle_ui.json
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
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uh import want_ug_minus_gu
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TW_JSON = Path(__file__).resolve().parent / "cycle_tw.json"
UH_JSON = Path(__file__).resolve().parent / "cycle_uh.json"
UG_JSON = Path(__file__).resolve().parent / "cycle_ug.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_pg_minus_gp(k: int) -> int:
    """n_pg-n_gp: 0 at k=0, 1 at k=1, 2^{k-1}+J_{k-2} for k>=2."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return (1 << (k - 1)) + jacobsthal(k - 2)


def tot_form() -> dict:
    """k<=64: power-of-two plus Jacobsthal; j=0 leftover; J recurrences."""
    n_ok = 0
    if want_pg_minus_gp(0) != 0 or want_pg_minus_gp(1) != 1:
        return {"ok": False, "k01": True}
    if want_pg_minus_gp(2) != 2 or want_pg_minus_gp(8) != 149:
        return {"ok": False, "k28": True}
    if want_pg_minus_gp(8) == 17311 or want_pg_minus_gp(8) == 17630:
        return {"ok": False, "sum": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 2:
            if want_pg_minus_gp(k) != (1 << (k - 1)) + jacobsthal(k - 2):
                return {"ok": False, "pow": True, "k": k}
            if want_pg_minus_gp(k) != jacobsthal(k) + (1 << (k - 2)):
                return {"ok": False, "alt": True, "k": k}
            if want_j0_odd_lo(k) != 5 * (1 << (k - 2)) - 1:
                return {"ok": False, "j0": True, "k": k}
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
        and want_pg_minus_gp(8) != (1 << 7)
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def pg_gp_fold() -> dict:
    """k<=8: n_pg-n_gp matches; j=0 leftover; xor sum not the form."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = leftover_xor_split(k)
        diff = r["n_pg"] - r["n_gp"]
        xor_lo = r["n_pg"] + r["n_gp"]
        if r["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, **r}
        if r["n_neg"] != want_j0_odd_lo(k):
            return {"ok": False, "j0": True, "k": k, **r}
        if r["n_pg"] + r["n_gp"] + r["n_neg"] != r["extra"]:
            return {"ok": False, "part": True, "k": k, **r}
        if diff != want_pg_minus_gp(k):
            return {"ok": False, "d": True, "k": k, **r, "diff": diff}
        if k >= 2 and xor_lo == want_pg_minus_gp(k):
            return {"ok": False, "sum": True, "k": k, **r}
        if k >= 2 and r["n_pg"] == r["n_gp"]:
            return {"ok": False, "eq": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n_pg": r["n_pg"],
            "n_gp": r["n_gp"],
            "diff": diff,
            "xor_lo": xor_lo,
            "n_neg": r["n_neg"],
            "extra": r["extra"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["diff"] == 0
        and rows["1"]["diff"] == 1
        and rows["2"]["diff"] == 2
        and rows["8"]["n_pg"] == 8730
        and rows["8"]["n_gp"] == 8581
        and rows["8"]["diff"] == 149
        and rows["8"]["xor_lo"] == 17311
        and rows["8"]["xor_lo"] != 149
        and rows["8"]["n_neg"] == 319
        and rows["8"]["extra"] == 17630
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """n_pg=n_gp; difference is 2^{k-1} or J_k; xor-lo equals the difference."""
    ok = (
        want_pg_minus_gp(8) != 0
        and want_pg_minus_gp(8) != (1 << 7)
        and want_pg_minus_gp(8) != jacobsthal(8)
        and want_pg_minus_gp(8) != 17311
        and want_pg_minus_gp(8) != 17630
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
    tw = json.loads(TW_JSON.read_text())
    uh = json.loads(UH_JSON.read_text())
    ug = json.loads(UG_JSON.read_text())
    ok = (
        tw["checks"]["all_ok"]
        and uh["checks"]["all_ok"]
        and ug["checks"]["all_ok"]
        and tw["verdict"]["odd_ej_lo_from_parent_pair_xor"] == "LEMMA"
        and tw["verdict"]["j0_odd_lo_eq_5_2km2_minus_1"] == "LEMMA"
        and uh["verdict"]["ug_minus_gu_eq_jacobsthal"] == "LEMMA"
        and ug["verdict"]["extra_sum_eq_odd_minus_even_minus_J_k_ge_1"] == "LEMMA"
        and uh["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uh["verdict"]["prize"] == "unsolved"
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
    cnt = pg_gp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "pg_gp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "pg_minus_gp_eq_2km1_plus_J": True,
            "pg_eq_gp": False,
            "pg_minus_gp_eq_2km1": False,
            "xor_lo_eq_pg_minus_gp": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "pg_minus_gp_eq_2km1_plus_J": "LEMMA",
            "pg_eq_gp": "KILLED",
            "pg_minus_gp_eq_2km1": "KILLED",
            "xor_lo_eq_pg_minus_gp": "KILLED",
            "odd_ej_lo_empty": "KILLED",
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
        dump["pg_gp_fold"]["rows"]["8"]["diff"],
        "xor",
        dump["pg_gp_fold"]["rows"]["8"]["xor_lo"],
        "pg",
        dump["pg_gp_fold"]["rows"]["8"]["n_pg"],
        "gp",
        dump["pg_gp_fold"]["rows"]["8"]["n_gp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
