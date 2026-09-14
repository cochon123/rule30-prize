#!/usr/bin/env python3
"""Cycle VC: leftover extra xor small is lo_small minus j=0; diff is j0-d2e.

Leftover extra except j=0 each produce one leftover-parent xor child.
On n<=5U/2 that count is lo_small(k-1)-j0(k-1) for k>=3, the
complement of Cycle UV's lo_large(k-1) on n>5U/2. The signed
difference is j0(k-1)-d2e_small(k-1) for k>=4: leftover extra small
(n=1 minus n=3) at the parent plus j=0 leftover extra, since n=1
extra small is sign-balanced (Cycle VB) and j=0 is excluded from
the xor. Dies at k=2 for the count (got 0, not 1). Dies at k=3 for
the difference (got 3, not 2). Do not PREFIX pal-center tot. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_vc.py --certify
Dump: research/cycle_vc.json
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
from cycle_uk import want_lo_small
from cycle_un import want_d2e_small
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor, want_ej_xor_large
from cycle_uw import want_3u, want_miss_n
from cycle_uy import want_lo_parent_large_diff
from cycle_uz import want_ege
from cycle_va import want_n1_extra_sm, want_n3_extra_sm, want_sm
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VB_JSON = Path(__file__).resolve().parent / "cycle_vb.json"
VA_JSON = Path(__file__).resolve().parent / "cycle_va.json"
UV_JSON = Path(__file__).resolve().parent / "cycle_uv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ej_xor_small(k: int) -> int:
    """Leftover extra xor on n<=5U/2: 0 at k<=2, lo_small-j0 at parent."""
    if k <= 2:
        return 0
    return want_lo_small(k - 1) - want_j0_odd_lo(k - 1)


def want_ej_xor_small_diff(k: int) -> int:
    """That xor difference: 0 at k<=2, 3 at k=3, then j0-d2e_small."""
    if k <= 2:
        return 0
    if k == 3:
        return 3
    return want_j0_odd_lo(k - 1) - want_d2e_small(k - 1)


def tot_form() -> dict:
    """k<=64: xor small count and difference; dies at k=2 and k=3.

    Do not call leftover_extra_xor_split here.
    Census is xor_sm_fold for k<=8.
    """
    n_ok = 0
    if want_ej_xor_small(0) != 0 or want_ej_xor_small(2) != 0:
        return {"ok": False, "k02": True}
    if want_ej_xor_small(3) != 3 or want_ej_xor_small(8) != 3191:
        return {"ok": False, "k38": True}
    if want_ej_xor_small_diff(3) != 3 or want_ej_xor_small_diff(8) != 105:
        return {"ok": False, "d38": True}
    raw2 = want_lo_small(1) - want_j0_odd_lo(1)
    if want_ej_xor_small(2) == raw2:
        return {"ok": False, "k2f": True}
    raw3 = want_j0_odd_lo(2) - want_d2e_small(2)
    if want_ej_xor_small_diff(3) == raw3:
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
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if k >= 3:
            if want_ej_xor_small(k) != want_ej_xor(k) - want_ej_xor_large(k):
                return {"ok": False, "cmp": True, "k": k}
            if want_ej_xor_small(k) != (
                want_lo_small(k - 1) - want_j0_odd_lo(k - 1)
            ):
                return {"ok": False, "cnt": True, "k": k}
        if k >= 4:
            if want_ej_xor_small_diff(k) != (
                want_j0_odd_lo(k - 1) - want_d2e_small(k - 1)
            ):
                return {"ok": False, "drec": True, "k": k}
            if want_ej_xor_small_diff(k) != (
                5 * (1 << (k - 3)) - 1 - want_d2e_small(k - 1)
            ):
                return {"ok": False, "df": True, "k": k}
            if want_n3_extra_sm(k - 1) - want_n1_extra_sm(k - 1) != (
                want_d2e_small(k - 1)
            ):
                return {"ok": False, "ex": True, "k": k}
            if want_ej_xor_small_diff(k) != (
                want_j0_odd_lo(k - 1)
                + want_n1_extra_sm(k - 1)
                - want_n3_extra_sm(k - 1)
            ):
                return {"ok": False, "n13": True, "k": k}
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
        and want_ej_xor_small(2) != raw2
        and want_ej_xor_small_diff(3) != raw3
        and want_ej_xor_small(8) == 3191
        and want_ej_xor_small_diff(8) == 105
        and want_ej_xor_large(8) == 2034
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
        and want_lo_parent_large_diff(8) == -30
        and want_n1_extra_sm(8) == 5440
        and want_n3_extra_sm(8) == 5546
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
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def xor_sm_fold() -> dict:
    """k<=8 leftover extra xor small count and difference."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = leftover_extra_xor_split(k)
        ssum = a["pg_s"] + a["gp_s"]
        sdiff = a["pg_s"] - a["gp_s"]
        lsum = a["pg_l"] + a["gp_l"]
        ldiff = a["pg_l"] - a["gp_l"]
        if ssum != want_ej_xor_small(k):
            return {"ok": False, "sm": True, "k": k, "got": ssum}
        if sdiff != want_ej_xor_small_diff(k):
            return {"ok": False, "sd": True, "k": k, "got": sdiff}
        if ssum + lsum != want_ej_xor(k):
            return {"ok": False, "tot": True, "k": k}
        if lsum != want_ej_xor_large(k):
            return {"ok": False, "lg": True, "k": k, "got": lsum}
        if k >= 4:
            if ldiff != want_lo_parent_large_diff(k):
                return {"ok": False, "ld": True, "k": k, "got": ldiff}
            if sdiff != (
                want_j0_odd_lo(k - 1)
                + want_n1_extra_sm(k - 1)
                - want_n3_extra_sm(k - 1)
            ):
                return {"ok": False, "n13": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "ssum": ssum,
            "sdiff": sdiff,
            "lsum": lsum,
            "ldiff": ldiff,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["ssum"] == 0
        and rows["2"]["ssum"] != want_lo_small(1) - want_j0_odd_lo(1)
        and rows["3"]["sdiff"] == 3
        and rows["3"]["sdiff"]
        != want_j0_odd_lo(2) - want_d2e_small(2)
        and rows["8"]["ssum"] == 3191
        and rows["8"]["sdiff"] == 105
        and rows["8"]["lsum"] == 2034
        and rows["8"]["ldiff"] == -30
        and want_ej_xor_small(4) == 15
        and want_ej_xor_small_diff(4) == 5
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """xor small count at k=2; difference at k=3."""
    a2 = leftover_extra_xor_split(2)
    a8 = leftover_extra_xor_split(8)
    ok = (
        want_ej_xor_small(2) != want_lo_small(1) - want_j0_odd_lo(1)
        and want_ej_xor_small_diff(3)
        != want_j0_odd_lo(2) - want_d2e_small(2)
        and a2["pg_s"] + a2["gp_s"] == 0
        and a8["pg_s"] + a8["gp_s"] == 3191
        and a8["pg_s"] - a8["gp_s"] == 105
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and G(2, 1) == 0
        and G(4, 2) == G(2, 1)
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
    vb = json.loads(VB_JSON.read_text())
    va = json.loads(VA_JSON.read_text())
    uv = json.loads(UV_JSON.read_text())
    ok = (
        vb["checks"]["all_ok"]
        and va["checks"]["all_ok"]
        and uv["checks"]["all_ok"]
        and vb["verdict"]["n1_extra_sm_2fold_k_ge_4"] == "LEMMA"
        and vb["verdict"]["n3_extra_sm_2step_k_ge_4"] == "LEMMA"
        and vb["verdict"]["extra_sm_g0_equal_k_ge_3"] == "LEMMA"
        and uv["verdict"]["ej_xor_large_eq_lo_large_parent_k_ge_3"] == "LEMMA"
        and vb["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vb["verdict"]["prize"] == "unsolved"
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
    cnt = xor_sm_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "xor_sm_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ej_xor_small_eq_lo_small_minus_j0_k_ge_3": True,
            "ej_xor_small_diff_eq_j0_minus_d2e_k_ge_4": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ej_xor_small_eq_lo_small_minus_j0_k_ge_3": "LEMMA",
            "ej_xor_small_diff_eq_j0_minus_d2e_k_ge_4": "LEMMA",
            "ej_xor_small_cnt_at_k2": "KILLED",
            "ej_xor_small_diff_at_k3": "KILLED",
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
        "ssum/sdiff k8",
        dump["xor_sm_fold"]["rows"]["8"]["ssum"],
        dump["xor_sm_fold"]["rows"]["8"]["sdiff"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
