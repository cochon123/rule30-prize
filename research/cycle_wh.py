#!/usr/bin/env python3
"""Cycle WH: even leftover small sm F/L closed form.

sm is (2^{k-2}(33 F_{k+1}-21 F_{k-1}-25)+4(-1)^k)/6 for k>=2.
Special 1 at k=1; 0 at k<=0. Equals lo_e-e_ge. 2 sm(k) is leftover-
parent xor plo_s(k+1) for k>=2. Dies at k=2 for the F/L form with
shift 0 (got 0, not 4). Dies at k=8 without 2^{k-2} (got 138, not
8790) and without 4(-1)^k (got 8789, not 8790). Dies at k=8 for sm
equals tot lo_e (got 8790, not 14114) and sm equals e_ge (got 8790,
not 5324). Census k=8: sm 8790, e_ge 5324. Do not PREFIX pal-center
tot. Not rest=S xor T. Do not walk leftover p catalogues. Do not
walk leftover d catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wh.py --certify
Dump: research/cycle_wh.json
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
from cycle_up import lucas, want_lo_e
from cycle_ur import even_lo_ph_split, parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_we import want_ege_fl
from cycle_wf import want_plo_s_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WG_JSON = Path(__file__).resolve().parent / "cycle_wg.json"
WE_JSON = Path(__file__).resolve().parent / "cycle_we.json"
VA_JSON = Path(__file__).resolve().parent / "cycle_va.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_sm_fl(k: int) -> int:
    """Even leftover on n<5U/2: F form for k>=2; 1 at k=1; 0 at k<=0."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    n = (
        (1 << (k - 2)) * (33 * fib(k + 1) - 21 * fib(k - 1) - 25)
        + 4 * ((-1) ** k)
    )
    return n // 6


def tot_form() -> dict:
    """k<=64: sm F/L; dies at k=2 with shift 0.

    Do not call even_lo_ph_split / named_half_split here.
    Census is sm_fold for k<=8.
    """
    n_ok = 0
    raw_k2 = (4 * ((-1) ** 2)) // 6
    miss_pow = (33 * fib(9) - 21 * fib(7) - 25 + 4 * ((-1) ** 8)) // 6
    miss_sign = ((1 << 6) * (33 * fib(9) - 21 * fib(7) - 25)) // 6
    if want_sm_fl(0) != 0 or want_sm_fl(1) != 1:
        return {"ok": False, "k01": True}
    if want_sm_fl(2) != 4 or want_sm_fl(3) != 17:
        return {"ok": False, "k23": True}
    if want_sm_fl(8) != 8790:
        return {"ok": False, "k8": True}
    if want_sm_fl(2) == raw_k2:
        return {"ok": False, "raw2": True}
    if want_sm_fl(8) == miss_pow:
        return {"ok": False, "pow": True}
    if want_sm_fl(8) == miss_sign:
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
        if want_sm_fl(k) != want_sm(k):
            return {"ok": False, "sm": True, "k": k}
        if want_sm_fl(k) != want_lo_e(k) - want_ege_fl(k):
            return {"ok": False, "diff": True, "k": k}
        if k >= 2:
            n = (
                (1 << (k - 2)) * (33 * fib(k + 1) - 21 * fib(k - 1) - 25)
                + 4 * ((-1) ** k)
            )
            if n % 6 != 0 or n // 6 != want_sm_fl(k):
                return {"ok": False, "div": True, "k": k}
            if 2 * want_sm_fl(k) != want_plo_s_fl(k + 1):
                return {"ok": False, "plo": True, "k": k}
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
        and want_sm_fl(2) != raw_k2
        and want_sm_fl(8) != miss_pow
        and want_sm_fl(8) != miss_sign
        and want_sm_fl(8) != want_lo_e(8)
        and want_sm_fl(8) != want_ege_fl(8)
        and want_sm_fl(8) == 8790
        and want_ege_fl(8) == 5324
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
        and want_sm_fl(4) == 66
        and want_sm_fl(5) == 234
        and want_sm_fl(6) == 798
        and want_plo_s_fl(8) == 5332
        and 2 * want_sm_fl(7) == want_plo_s_fl(8)
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
        and miss_pow == 138
        and miss_sign == 8789
        and raw_k2 == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def sm_fold() -> dict:
    """k<=8 even leftover small vs sm F/L."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = even_lo_ph_split(k)
        ege = a["eq"] + a["lg"]
        if a["sm"] != want_sm_fl(k):
            return {"ok": False, "sm": True, "k": k, "got": a["sm"]}
        if ege != want_ege_fl(k):
            return {"ok": False, "ege": True, "k": k, "got": ege}
        if a["sm"] + ege != want_lo_e(k):
            return {"ok": False, "sum": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"sm": a["sm"], "ege": ege}
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["sm"] == 1
        and rows["1"]["ege"] == 0
        and rows["2"]["sm"] == 4
        and rows["2"]["ege"] == 2
        and rows["3"]["sm"] == 17
        and rows["8"]["sm"] == 8790
        and rows["8"]["ege"] == 5324
        and want_sm_fl(4) == 66
        and want_sm_fl(5) == 234
        and want_sm_fl(6) == 798
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L form at k=2 with shift 0; without power / sign at k=8."""
    raw_k2 = (4 * ((-1) ** 2)) // 6
    miss_pow = (33 * fib(9) - 21 * fib(7) - 25 + 4 * ((-1) ** 8)) // 6
    miss_sign = ((1 << 6) * (33 * fib(9) - 21 * fib(7) - 25)) // 6
    a8 = even_lo_ph_split(8)
    ok = (
        want_sm_fl(2) != raw_k2
        and want_sm_fl(8) != miss_pow
        and want_sm_fl(8) != miss_sign
        and want_sm_fl(8) != want_lo_e(8)
        and want_sm_fl(8) != want_ege_fl(8)
        and a8["sm"] == 8790
        and a8["eq"] + a8["lg"] == 5324
        and miss_pow == 138
        and miss_sign == 8789
        and raw_k2 == 0
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
    wg = json.loads(WG_JSON.read_text())
    we = json.loads(WE_JSON.read_text())
    va = json.loads(VA_JSON.read_text())
    ok = (
        wg["checks"]["all_ok"]
        and we["checks"]["all_ok"]
        and va["checks"]["all_ok"]
        and wg["verdict"]["named_pg_s_eq_closed_k_ge_3"] == "LEMMA"
        and we["verdict"]["sm_eq_loe_minus_ege_all_k"] == "LEMMA"
        and va["verdict"]["sm_rec_2sm_2d2e_lo_small_k_ge_4"] == "LEMMA"
        and wg["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wg["verdict"]["prize"] == "unsolved"
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
    cnt = sm_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "sm_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "sm_eq_FL_closed_k_ge_2": True,
            "two_sm_eq_plo_s_next_k_ge_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "sm_eq_FL_closed_k_ge_2": "LEMMA",
            "two_sm_eq_plo_s_next_k_ge_2": "LEMMA",
            "sm_FL_shift0_at_k2": "KILLED",
            "sm_without_pow_at_k8": "KILLED",
            "sm_without_sign_at_k8": "KILLED",
            "sm_eq_loe": "KILLED",
            "sm_eq_ege": "KILLED",
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
        "sm k8",
        dump["sm_fold"]["rows"]["8"]["sm"],
        "ege",
        dump["sm_fold"]["rows"]["8"]["ege"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
