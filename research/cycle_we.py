#!/usr/bin/env python3
"""Cycle WE: even leftover large e_ge F/L closed form.

e_ge is (2^{k-3}(21 F_{k+1}+11 F_{k-1}-25)-5(-1)^k+1)/5 for k>=3.
Special 2 at k=2; 0 at k<=1. Even leftover small is lo_e-e_ge.
Dies at k=3 for the F/L form with shift 0 (got 1, not 11). Dies at
k=8 without +1 (got 5323, not 5324) and without -5(-1)^k (got 5325,
not 5324). Do not kill without both +1 and the sign at k=8:
floor-div masks it. Dies at k=8 for e_ge equals tot lo_e (got 5324,
not 14114) and e_ge equals lo_large (got 5324, not 6644). Census
k=8: e_ge 5324, sm 8790. Do not PREFIX pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_we.py --certify
Dump: research/cycle_we.json
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
from cycle_uq import want_lo_large
from cycle_up import lucas, want_lo_e
from cycle_ur import even_lo_ph_split, parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WD_JSON = Path(__file__).resolve().parent / "cycle_wd.json"
UZ_JSON = Path(__file__).resolve().parent / "cycle_uz.json"
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ege_fl(k: int) -> int:
    """Even leftover on n>=5U/2: F/L form for k>=3; 2 at k=2; 0 at k<=1."""
    if k <= 1:
        return 0
    if k == 2:
        return 2
    n = (
        (1 << (k - 3)) * (21 * fib(k + 1) + 11 * fib(k - 1) - 25)
        - 5 * ((-1) ** k)
        + 1
    )
    return n // 5


def tot_form() -> dict:
    """k<=64: e_ge F/L; dies at k=3 with shift 0.

    Do not call even_lo_ph_split / ege_kind_split here.
    Census is ege_fold for k<=8.
    """
    n_ok = 0
    raw_k3 = (-5 * ((-1) ** 3) + 1) // 5
    miss_plus1 = (
        (1 << 5) * (21 * fib(9) + 11 * fib(7) - 25) - 5 * ((-1) ** 8)
    ) // 5
    miss_sign = ((1 << 5) * (21 * fib(9) + 11 * fib(7) - 25) + 1) // 5
    miss_both = ((1 << 5) * (21 * fib(9) + 11 * fib(7) - 25)) // 5
    if want_ege_fl(0) != 0 or want_ege_fl(1) != 0:
        return {"ok": False, "k01": True}
    if want_ege_fl(2) != 2 or want_ege_fl(3) != 11:
        return {"ok": False, "k23": True}
    if want_ege_fl(8) != 5324:
        return {"ok": False, "k8": True}
    if want_ege_fl(3) == raw_k3:
        return {"ok": False, "raw3": True}
    if want_ege_fl(8) == miss_plus1:
        return {"ok": False, "p1": True}
    if want_ege_fl(8) == miss_sign:
        return {"ok": False, "sg": True}
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
        if want_ege_fl(k) != want_ege(k):
            return {"ok": False, "ege": True, "k": k}
        if want_sm(k) != want_lo_e(k) - want_ege_fl(k):
            return {"ok": False, "sm": True, "k": k}
        if k >= 3:
            n = (
                (1 << (k - 3)) * (21 * fib(k + 1) + 11 * fib(k - 1) - 25)
                - 5 * ((-1) ** k)
                + 1
            )
            if n % 5 != 0 or n // 5 != want_ege_fl(k):
                return {"ok": False, "div": True, "k": k}
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
        and want_ege_fl(3) != raw_k3
        and want_ege_fl(8) != miss_plus1
        and want_ege_fl(8) != miss_sign
        and want_ege_fl(8) == miss_both
        and want_ege_fl(8) != want_lo_e(8)
        and want_ege_fl(8) != want_lo_large(8)
        and want_ege_fl(8) == 5324
        and want_sm(8) == 8790
        and want_lo_e(8) == 14114
        and want_lo_large(8) == 6644
        and want_ege_fl(4) == 40
        and want_ege_fl(5) == 142
        and want_ege_fl(6) == 484
        and want_ej_xor(8) == 5225
        and lucas(8) == 47
        and fib(8) == 21
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
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
        and miss_plus1 == 5323
        and miss_sign == 5325
        and miss_both == 5324
        and raw_k3 == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ege_fold() -> dict:
    """k<=8 even leftover ph-split vs e_ge F/L and sm=lo_e-e_ge."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = even_lo_ph_split(k)
        ege = a["eq"] + a["lg"]
        if ege != want_ege_fl(k):
            return {"ok": False, "ege": True, "k": k, "got": ege}
        if a["sm"] != want_sm(k):
            return {"ok": False, "sm": True, "k": k, "got": a["sm"]}
        if a["sm"] + ege != want_lo_e(k):
            return {"ok": False, "sum": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"ege": ege, "sm": a["sm"], "eq": a["eq"], "lg": a["lg"]}
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["ege"] == 0
        and rows["1"]["sm"] == 1
        and rows["2"]["ege"] == 2
        and rows["2"]["sm"] == 4
        and rows["3"]["ege"] == 11
        and rows["3"]["sm"] == 17
        and rows["8"]["ege"] == 5324
        and rows["8"]["sm"] == 8790
        and want_ege_fl(4) == 40
        and want_ege_fl(5) == 142
        and want_ege_fl(6) == 484
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L form at k=3 with shift 0; without +1 / sign at k=8; tot lo_e."""
    raw_k3 = (-5 * ((-1) ** 3) + 1) // 5
    miss_plus1 = (
        (1 << 5) * (21 * fib(9) + 11 * fib(7) - 25) - 5 * ((-1) ** 8)
    ) // 5
    miss_sign = ((1 << 5) * (21 * fib(9) + 11 * fib(7) - 25) + 1) // 5
    miss_both = ((1 << 5) * (21 * fib(9) + 11 * fib(7) - 25)) // 5
    a8 = even_lo_ph_split(8)
    ok = (
        want_ege_fl(3) != raw_k3
        and want_ege_fl(8) != miss_plus1
        and want_ege_fl(8) != miss_sign
        and want_ege_fl(8) == miss_both
        and want_ege_fl(8) != want_lo_e(8)
        and want_ege_fl(8) != want_lo_large(8)
        and a8["eq"] + a8["lg"] == 5324
        and a8["sm"] == 8790
        and miss_plus1 == 5323
        and miss_sign == 5325
        and miss_both == 5324
        and raw_k3 == 1
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
    wd = json.loads(WD_JSON.read_text())
    uz = json.loads(UZ_JSON.read_text())
    up = json.loads(UP_JSON.read_text())
    ok = (
        wd["checks"]["all_ok"]
        and uz["checks"]["all_ok"]
        and up["checks"]["all_ok"]
        and wd["verdict"]["ej_xor_pg_s_eq_FL_closed_k_ge_4"] == "LEMMA"
        and uz["verdict"]["ege_rec_2ege_2d2e_lo_large_k_ge_4"] == "LEMMA"
        and up["verdict"]["lo_e_closed_form_k_ge_1"] == "LEMMA"
        and wd["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wd["verdict"]["prize"] == "unsolved"
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
    cnt = ege_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ege_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ege_eq_FL_closed_k_ge_3": True,
            "sm_eq_loe_minus_ege_all_k": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ege_eq_FL_closed_k_ge_3": "LEMMA",
            "sm_eq_loe_minus_ege_all_k": "LEMMA",
            "ege_FL_shift0_at_k3": "KILLED",
            "ege_without_plus1_at_k8": "KILLED",
            "ege_without_sign_at_k8": "KILLED",
            "ege_eq_loe": "KILLED",
            "ege_eq_lo_large": "KILLED",
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
        "ege k8",
        dump["ege_fold"]["rows"]["8"]["ege"],
        "sm",
        dump["ege_fold"]["rows"]["8"]["sm"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
