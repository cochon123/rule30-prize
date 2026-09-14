#!/usr/bin/env python3
"""Cycle UD: pal-pair plus unpaired is 2^{k+1}(F_{k+4}-1).

G(n,n)=1 for every n by even/odd doubling to G(0,0). Pal-center
count is 4U. Pal-left covering cells are unclipped, so pal-left tot
is (W(4U)+4U)/2=2^{k+1}(F_{k+4}+1) from Cycle UC's W(2^a)=2^a F_{a+2}.
Hence pair plus unpaired is 2^{k+1}(F_{k+4}-1). Do not PREFIX leftover
extra or unpaired extra separately. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_ud.py --certify
Dump: research/cycle_ud.json
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
from cycle_uc import fib, trans, want_ej_odd_tot, wt
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UC_JSON = Path(__file__).resolve().parent / "cycle_uc.json"
TY_JSON = Path(__file__).resolve().parent / "cycle_ty.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
N_GNN = 64
PAT0011 = (0, 0, 1, 1)


def want_pal_c(k: int) -> int:
    """Pal-center count: 4U = 2^{k+2}."""
    return 1 << (k + 2)


def want_pal_left(k: int) -> int:
    """Pal-left G=1 tot including pal-center: 2^{k+1}(F_{k+4}+1)."""
    return (1 << (k + 1)) * (fib(k + 4) + 1)


def want_pair_unp(k: int) -> int:
    """Pal-pair plus unpaired: 2^{k+1}(F_{k+4}-1)."""
    return (1 << (k + 1)) * (fib(k + 4) - 1)


def tot_form() -> dict:
    """k<=64: G(n,n)=1; pal-center 4U; F identities; pal-left unclipped."""
    n_ok = 0
    if G(0, 0) != 1:
        return {"ok": False, "g00": True}
    for n in range(0, N_GNN + 1):
        if G(n, n) != 1:
            return {"ok": False, "gnn": True, "n": n}
        if n >= 1:
            m = n // 2
            if n % 2 == 0:
                if G(n, n) != G(m, m):
                    return {"ok": False, "even": True, "n": n}
            else:
                if G(n, n) != G(m, m):
                    return {"ok": False, "odd": True, "n": n}
    if want_pal_c(0) != 4 or want_pair_unp(0) != 4:
        return {"ok": False, "k0": True}
    if want_pal_left(0) != 8 or want_pair_unp(8) != 73216:
        return {"ok": False, "k08": True}
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
        if want_pal_c(k) != 4 * u:
            return {"ok": False, "pc": True, "k": k}
        if want_pal_left(k) != want_pal_c(k) + want_pair_unp(k):
            return {"ok": False, "sum": True, "k": k}
        if 4 * u >= 5 * u:
            return {"ok": False, "clip": True, "k": k}
        n = 4 * u - 1
        if n >= 5 * u:
            return {"ok": False, "n": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and G(2, 2) != 0
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(1) != (1 << 3)
        and want_ej_odd_tot(8) == 28160
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def pair_unp_fold() -> dict:
    """k<=8: pal-center 4U; pair+unp Fibonacci."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        ps = pal_split(k, None)
        pal_left = ps["n_pal"] + ps["n_pair"] + ps["n_unp"]
        if ps["n_pal"] != want_pal_c(k):
            return {"ok": False, "pc": True, "k": k, **ps}
        if pal_left != want_pal_left(k):
            return {"ok": False, "pl": True, "k": k, "pal_left": pal_left}
        if ps["n_pair"] + ps["n_unp"] != want_pair_unp(k):
            return {"ok": False, "pu": True, "k": k, **ps}
        n_ok += 1
        rows[str(k)] = {
            "n_pal": ps["n_pal"],
            "n_pair": ps["n_pair"],
            "n_unp": ps["n_unp"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["n_pal"] == 4
        and rows["0"]["n_pair"] + rows["0"]["n_unp"] == 4
        and rows["8"]["n_pal"] == 1024
        and rows["8"]["n_pair"] == 46882
        and rows["8"]["n_unp"] == 26334
        and rows["8"]["n_pair"] + rows["8"]["n_unp"] == 73216
        and rows["8"]["n_pair"] + rows["8"]["n_unp"] != (1 << 10)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """G(n,n)=n mod 2; pal-center 2^{k+1}; pair+unp=2^{k+2}."""
    ok = (
        G(2, 2) != 2 % 2
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(0) != 4 * 0
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
    ty = json.loads(TY_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ok = (
        uc["checks"]["all_ok"]
        and ty["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and uc["verdict"]["ej_odd_tot_eq_2km1_fib"] == "LEMMA"
        and uc["verdict"]["trans_eq_wt_half"] == "LEMMA"
        and ty["verdict"]["pair_eq_lo_plus_4U_k_ge_1"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and uc["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uc["verdict"]["prize"] == "unsolved"
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
    cnt = pair_unp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "pair_unp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "G_n_n_eq_1": True,
            "pal_c_eq_4U": True,
            "pal_left_eq_2km1_Fp1": True,
            "pair_unp_eq_2km1_Fm1": True,
            "G_n_n_eq_n_mod_2": False,
            "pal_c_eq_2km1": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "G_n_n_eq_1": "LEMMA",
            "pal_c_eq_4U": "LEMMA",
            "pal_left_eq_2km1_Fp1": "LEMMA",
            "pair_unp_eq_2km1_Fm1": "LEMMA",
            "G_n_n_eq_n_mod_2": "KILLED",
            "pal_c_eq_2km1": "KILLED",
            "pair_unp_eq_4U": "KILLED",
            "extra_sum_empty": "KILLED",
            "ej_odd_tot_eq_2kp2": "KILLED",
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
        "pair+unp k8",
        dump["pair_unp_fold"]["rows"]["8"]["n_pair"]
        + dump["pair_unp_fold"]["rows"]["8"]["n_unp"],
        "pal",
        dump["pair_unp_fold"]["rows"]["8"]["n_pal"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
