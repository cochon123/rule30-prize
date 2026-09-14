#!/usr/bin/env python3
"""Cycle VR: unpaired extra tot is 2^{k+1} F_{k+2}-2^{k+2}-4 lo_e(k-1)+2(-1)^k+1.

extra_sum minus leftover extra. F/L form is
(2^{k-2}(42 L_{k-1}+90 F_{k-1}-40)+10(-1)^k+3)/15 for k>=2.
Dies at k=1 for the lo_e form without the special case (got -1,
not 1). Dies at k=8 without the F/L +3 (got 10018, not 10019).
Dies at k=2 for the F/L form with shift 0 (got 0, not 7). Dies
at k=0 for tot 0 (got 0, not 1). Census k=8: extra_unp 10019.
Do not PREFIX pal-center tot. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_vr.py --certify
Dump: research/cycle_vr.json
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
from cycle_uc import fib, trans, want_extra_sum, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uo import named_half_split
from cycle_up import lucas, want_extra_unp, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vq import want_extra_lo_loe
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VQ_JSON = Path(__file__).resolve().parent / "cycle_vq.json"
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"
UC_JSON = Path(__file__).resolve().parent / "cycle_uc.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_extra_unp_loe(k: int) -> int:
    """extra_unp: 2^{k+1} F_{k+2}-2^{k+2}-4 lo_e(k-1)+2(-1)^k+1 for k>=2."""
    if k <= 1:
        return 1
    return (
        (1 << (k + 1)) * fib(k + 2)
        - (1 << (k + 2))
        - 4 * want_lo_e(k - 1)
        + 2 * ((-1) ** k)
        + 1
    )


def want_extra_unp_fl(k: int) -> int:
    """extra_unp F/L form for k>=2; special 1 at k<=1."""
    if k <= 1:
        return 1
    n = (
        (1 << (k - 2)) * (42 * lucas(k - 1) + 90 * fib(k - 1) - 40)
        + 10 * ((-1) ** k)
        + 3
    )
    return n // 15


def tot_form() -> dict:
    """k<=64: extra_unp lo_e and F/L forms; dies at k=1 without special.

    Do not call named_half_split / leftover_xor_split here.
    Census is extra_unp_fold for k<=8.
    """
    n_ok = 0
    raw_k1 = (
        (1 << 2) * fib(3)
        - (1 << 3)
        - 4 * want_lo_e(0)
        + 2 * ((-1) ** 1)
        + 1
    )
    raw_fl2 = (10 * ((-1) ** 2) + 3) // 15
    miss_p3 = (
        (1 << 6) * (42 * lucas(7) + 90 * fib(7) - 40)
        + 10 * ((-1) ** 8)
    ) // 15
    if want_extra_unp_loe(0) != 1 or want_extra_unp_loe(1) != 1:
        return {"ok": False, "k01": True}
    if want_extra_unp_loe(2) != 7 or want_extra_unp_fl(2) != 7:
        return {"ok": False, "k2": True}
    if want_extra_unp_loe(8) != 10019 or want_extra_unp_fl(8) != 10019:
        return {"ok": False, "k8": True}
    if want_extra_unp_loe(1) == raw_k1:
        return {"ok": False, "k1r": True}
    if want_extra_unp_fl(2) == raw_fl2:
        return {"ok": False, "k2fl": True}
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
        if want_extra_unp_loe(k) != want_extra_unp(k):
            return {"ok": False, "loe": True, "k": k}
        if want_extra_unp_fl(k) != want_extra_unp(k):
            return {"ok": False, "fl": True, "k": k}
        if want_extra_lo_loe(k) + want_extra_unp_loe(k) != want_extra_sum(k):
            return {"ok": False, "sum": True, "k": k}
        if k >= 2:
            n = (
                (1 << (k - 2))
                * (42 * lucas(k - 1) + 90 * fib(k - 1) - 40)
                + 10 * ((-1) ** k)
                + 3
            )
            if n % 15 != 0 or n // 15 != want_extra_unp_fl(k):
                return {"ok": False, "div": True, "k": k}
            if want_extra_unp_loe(k) != (
                (1 << (k + 1)) * fib(k + 2)
                - (1 << (k + 2))
                - 4 * want_lo_e(k - 1)
                + 2 * ((-1) ** k)
                + 1
            ):
                return {"ok": False, "lf": True, "k": k}
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
        and want_extra_unp_loe(1) != raw_k1
        and want_extra_unp_fl(2) != raw_fl2
        and want_extra_unp_fl(8) != miss_p3
        and want_extra_unp_loe(0) != 0
        and want_extra_unp_loe(8) == 10019
        and want_extra_unp_fl(8) == 10019
        and want_extra_lo_loe(8) == 17630
        and want_extra_sum(8) == 27649
        and want_ej_xor(8) == 5225
        and want_lo_e(7) == 4280
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def extra_unp_fold() -> dict:
    """k<=8 unpaired extra tot vs lo_e and F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        extra = r["lo_s"] + r["lo_l"]
        unp = want_extra_sum(k) - extra
        if r["n_bad"] != 0 or r["n_pg_d1"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if extra != want_extra_lo_loe(k):
            return {"ok": False, "elo": True, "k": k, "got": extra}
        if unp != want_extra_unp_loe(k):
            return {"ok": False, "loe": True, "k": k, "got": unp}
        if unp != want_extra_unp_fl(k):
            return {"ok": False, "fl": True, "k": k, "got": unp}
        n_ok += 1
        rows[str(k)] = {"extra_unp": unp, "extra_lo": extra}
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["extra_unp"] == 1
        and rows["1"]["extra_unp"] == 1
        and rows["2"]["extra_unp"] == 7
        and rows["8"]["extra_unp"] == 10019
        and rows["8"]["extra_lo"] == 17630
        and want_extra_unp_loe(4) == 83
        and want_extra_unp_fl(7) == 3063
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """lo_e form at k=1; F/L without +3 at k=8; F/L shift 0 at k=2; tot 0 at k=0."""
    raw_k1 = (
        (1 << 2) * fib(3)
        - (1 << 3)
        - 4 * want_lo_e(0)
        + 2 * ((-1) ** 1)
        + 1
    )
    raw_fl2 = (10 * ((-1) ** 2) + 3) // 15
    miss_p3 = (
        (1 << 6) * (42 * lucas(7) + 90 * fib(7) - 40)
        + 10 * ((-1) ** 8)
    ) // 15
    r8 = named_half_split(8)
    unp8 = want_extra_sum(8) - (r8["lo_s"] + r8["lo_l"])
    ok = (
        want_extra_unp_loe(1) != raw_k1
        and want_extra_unp_fl(2) != raw_fl2
        and want_extra_unp_fl(8) != miss_p3
        and want_extra_unp_loe(0) != 0
        and unp8 == 10019
        and raw_k1 == -1
        and miss_p3 == 10018
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
    vq = json.loads(VQ_JSON.read_text())
    up = json.loads(UP_JSON.read_text())
    uc = json.loads(UC_JSON.read_text())
    ok = (
        vq["checks"]["all_ok"]
        and up["checks"]["all_ok"]
        and uc["checks"]["all_ok"]
        and vq["verdict"]["extra_lo_eq_4_loe_plus_2kp1_k_ge_2"] == "LEMMA"
        and up["verdict"]["extra_unp_eq_extra_sum_minus_extra_lo"] == "LEMMA"
        and uc["verdict"]["extra_sum_eq_2km1_Fm1_pm1"] == "LEMMA"
        and vq["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vq["verdict"]["prize"] == "unsolved"
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
    cnt = extra_unp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "extra_unp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "extra_unp_eq_2kp1_F_minus_4_loe_k_ge_2": True,
            "extra_unp_eq_FL_closed_k_ge_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "extra_unp_eq_2kp1_F_minus_4_loe_k_ge_2": "LEMMA",
            "extra_unp_eq_FL_closed_k_ge_2": "LEMMA",
            "extra_unp_loe_at_k1": "KILLED",
            "extra_unp_FL_shift0_at_k2": "KILLED",
            "extra_unp_FL_without_p3_at_k8": "KILLED",
            "extra_unp_eq_0_at_k0": "KILLED",
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
    print("extra_unp k8", dump["extra_unp_fold"]["rows"]["8"]["extra_unp"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
