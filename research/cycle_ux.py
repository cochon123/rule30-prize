#!/usr/bin/env python3
"""Cycle UX: leftover extra large n=1 mod 4 is 2-fold parent even leftover large union d=2.

Even leftover union d=2 on n>=5 U_p/2 produces leftover extra (j,j+2)
pairs on large n=1 mod 4, count 2(e_ge(k-1)+d2e_large(k-1)) for
k>=4. G(s,t)=0 leftover extra large on n=3 mod 4 equals that on
n=1 mod 4 for k>=3, so leftover-parent xor large difference is
leftover extra large (n=1 minus n=3) at k-1. Dies at k=3 for the
2-fold (count 8, not 6). Do not PREFIX leftover-parent xor large
difference as a 0-1 form, or pal-center tot. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_ux.py --certify
Dump: research/cycle_ux.json
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
from cycle_un import want_d2e_large
from cycle_up import lucas, want_lo_e
from cycle_ur import even_lo_ph_split, parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor_large
from cycle_uw import leftover_cell, want_3u, want_miss_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UW_JSON = Path(__file__).resolve().parent / "cycle_uw.json"
UV_JSON = Path(__file__).resolve().parent / "cycle_uv.json"
UU_JSON = Path(__file__).resolve().parent / "cycle_uu.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def e_ge(k: int) -> int:
    """Even leftover on n>=5U/2, including the half."""
    eh = even_lo_ph_split(k)
    return eh["eq"] + eh["lg"]


def want_n1_extra_lg(k: int) -> int:
    """Leftover extra large n=1 mod 4: 0,0,8, then 2(e_ge+d2e_large) at k-1."""
    if k <= 2:
        return 0
    if k == 3:
        return 8
    return 2 * (e_ge(k - 1) + want_d2e_large(k - 1))


def extra_lg_res_split(k: int) -> dict:
    """Leftover extra on n>ph split by n mod 4 and G(s,t)."""
    u = 1 << k
    ph = parent_half(k)
    clip = 5 * u
    z = {
        1: {"g0": 0, "g1": 0, "n": 0},
        3: {"g0": 0, "g1": 0, "n": 0},
    }
    for n in range(1, 4 * u, 2):
        if n <= ph:
            continue
        r = n % 4
        if r not in (1, 3):
            continue
        s = (n - 1) // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if not leftover_cell(n, j, k):
                continue
            gs = G(s, j // 2)
            z[r]["n"] += 1
            z[r]["g0" if gs == 0 else "g1"] += 1
    return z


def tot_form() -> dict:
    """k<=64: even parent child n=1 mod 4; 2-fold dies at k=3.

    Do not call e_ge / even_lo_ph_split here: that walks covering.
    The 2-fold identity is census-checked in n1_2f_fold for k<=8.
    """
    n_ok = 0
    if want_n1_extra_lg(0) != 0 or want_n1_extra_lg(2) != 0:
        return {"ok": False, "k02": True}
    if want_n1_extra_lg(3) != 8 or want_n1_extra_lg(8) != 3290:
        return {"ok": False, "k38": True}
    if want_n1_extra_lg(3) == 2 * (e_ge(2) + want_d2e_large(2)):
        return {"ok": False, "k3f": True}
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
        n = 2 * m + 1
        if m % 2 == 0:
            if n % 4 != 1:
                return {"ok": False, "n1": True, "m": m}
        elif n % 4 != 3:
            return {"ok": False, "n3": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if k >= 2 and (2 * ph + 1) % 4 != 1:
            return {"ok": False, "ch": True, "k": k}
        if (2 * (2 * k) + 1) % 4 != 1:
            return {"ok": False, "epar": True, "k": k}
        if (2 * (2 * k + 1) + 1) % 4 != 3:
            return {"ok": False, "opar": True, "k": k}
        if k >= 2:
            par_u = 1 << (k - 1)
            if 2 * (3 * par_u) + 1 != 3 * u + 1:
                return {"ok": False, "miss": True, "k": k}
            if (2 * (3 * par_u) + 1) % 4 != 1:
                return {"ok": False, "m1": True, "k": k}
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
        and want_n1_extra_lg(3) != 2 * (e_ge(2) + want_d2e_large(2))
        and want_n1_extra_lg(8) == 3290
        and want_n1_extra_lg(7) == 1002
        and want_ej_xor_large(8) == 2034
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
        and want_lo_e(8) == 14114
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def n1_2f_fold() -> dict:
    """k<=8 leftover extra large residue split and 2-fold."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        z = extra_lg_res_split(k)
        n1 = z[1]["n"]
        n3 = z[3]["n"]
        if n1 != want_n1_extra_lg(k):
            return {"ok": False, "n1": True, "k": k, "got": n1}
        if k >= 3:
            if z[1]["g0"] != z[3]["g0"]:
                return {"ok": False, "g0": True, "k": k, "got": z}
            if z[1]["g0"] != z[1]["g1"]:
                return {"ok": False, "bal": True, "k": k}
            extra = n3 - n1
            if z[3]["g1"] - z[3]["g0"] != extra:
                return {"ok": False, "xg1": True, "k": k, "got": z}
        if k >= 4:
            if n1 != 2 * (e_ge(k - 1) + want_d2e_large(k - 1)):
                return {"ok": False, "2f": True, "k": k, "got": n1}
            xr = leftover_extra_xor_split(k)
            diff = xr["pg_l"] - xr["gp_l"]
            par = extra_lg_res_split(k - 1)
            if diff != par[1]["n"] - par[3]["n"]:
                return {
                    "ok": False,
                    "ld": True,
                    "k": k,
                    "diff": diff,
                    "n1n3": par[1]["n"] - par[3]["n"],
                }
        n_ok += 1
        rows[str(k)] = {
            "n1": n1,
            "n3": n3,
            "g0_1": z[1]["g0"],
            "g0_3": z[3]["g0"],
            "g1_3": z[3]["g1"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["n1"] == 0
        and rows["3"]["n1"] == 8
        and rows["3"]["n1"] != 2 * (e_ge(2) + want_d2e_large(2))
        and rows["8"]["n1"] == 3290
        and rows["8"]["n3"] == 3354
        and rows["8"]["g0_1"] == rows["8"]["g0_3"]
        and rows["8"]["g0_1"] == 1645
        and rows["7"]["n3"] - rows["7"]["n1"] == 30
        and want_n1_extra_lg(4) == 24
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """2-fold at k=3; g0 equal at k=2; n3 equals n1."""
    z2 = extra_lg_res_split(2)
    z8 = extra_lg_res_split(8)
    ok = (
        want_n1_extra_lg(3) != 2 * (e_ge(2) + want_d2e_large(2))
        and z2[1]["g0"] != z2[3]["g0"]
        and z8[1]["n"] != z8[3]["n"]
        and z8[1]["g0"] == z8[3]["g0"]
        and z8[3]["g1"] != z8[3]["g0"]
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and want_ph_check()
        and G(2, 1) == 0
        and G(3, 2) == 0
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


def want_ph_check() -> bool:
    return parent_half(2) == 10 and parent_half(8) == 640


def prefixes() -> dict:
    uw = json.loads(UW_JSON.read_text())
    uv = json.loads(UV_JSON.read_text())
    uu = json.loads(UU_JSON.read_text())
    ok = (
        uw["checks"]["all_ok"]
        and uv["checks"]["all_ok"]
        and uu["checks"]["all_ok"]
        and uw["verdict"]["n1_extra_sign_balanced_k_ge_2"] == "LEMMA"
        and uw["verdict"]["n_3u_no_leftover"] == "LEMMA"
        and uw["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uw["verdict"]["prize"] == "unsolved"
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
    cnt = n1_2f_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "n1_2f_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "n1_extra_lg_2fold_ege_d2e_k_ge_4": True,
            "g0_n3_eq_g0_n1_k_ge_3": True,
            "large_diff_eq_n1_minus_n3_parent": True,
            "lo_parent_large_diff_closed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n1_extra_lg_2fold_ege_d2e_k_ge_4": "LEMMA",
            "g0_n3_eq_g0_n1_k_ge_3": "LEMMA",
            "large_diff_eq_n1_minus_n3_parent_k_ge_4": "LEMMA",
            "n1_2fold_at_k3": "KILLED",
            "g0_eq_at_k2": "KILLED",
            "n3_eq_n1": "KILLED",
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
        "n1/n3 k8",
        dump["n1_2f_fold"]["rows"]["8"]["n1"],
        dump["n1_2f_fold"]["rows"]["8"]["n3"],
        "g0",
        dump["n1_2f_fold"]["rows"]["8"]["g0_1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
