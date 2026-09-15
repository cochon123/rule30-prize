#!/usr/bin/env python3
"""Cycle WJ: unpaired xor tot xor_unp F/L closed form.

xor_unp is (2^{k-2}(28 L_{k-1}+60 F_{k-1}-70)+5(-1)^k+7)/10 for k>=2.
Special 0 at k<=1. Equals extra_unp minus clip_gp minus j=0 unpaired.
Equals xor tot minus leftover xor tot. n_ug/n_gu are (xor_unp plus
or minus ug-gu)/2. Dies at k=2 for the F/L form with shift 0 (got
1, not 3). Dies at k=8 without 2^{k-2} (got 1, not 9742), without
5(-1)^k (got 9741, not 9742), and without +7 (got 9741, not 9742).
Do not kill the sign at k=7: floor-div masks (2925=2925). Dies at
k=8 for xor_unp equals extra_unp (got 9742, not 10019), equals
xor_lo (got 9742, not 17311), and equals xor tot (got 9742, not
27053). Census k=8: xor_unp 9742, n_ug 4924, n_gu 4818. Do not
PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wj.py --certify
Dump: research/cycle_wj.json
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
from cycle_ua import want_j0_odd_unp
from cycle_ub import unpaired_xor_split, want_clip_gp
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uh import want_ug_minus_gu
from cycle_uj import want_xor_tot
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vp import want_xor_lo_fl
from cycle_vr import want_extra_unp_fl, want_extra_unp_loe
from cycle_we import want_ege_fl
from cycle_wh import want_sm_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WI_JSON = Path(__file__).resolve().parent / "cycle_wi.json"
VR_JSON = Path(__file__).resolve().parent / "cycle_vr.json"
UH_JSON = Path(__file__).resolve().parent / "cycle_uh.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_unp_fl(k: int) -> int:
    """unpaired xor tot: F/L form for k>=2; 0 at k<=1."""
    if k <= 1:
        return 0
    n = (
        (1 << (k - 2)) * (28 * lucas(k - 1) + 60 * fib(k - 1) - 70)
        + 5 * ((-1) ** k)
        + 7
    )
    return n // 10


def want_xor_unp_loe(k: int) -> int:
    """unpaired xor tot: extra_unp minus clip_gp minus j=0 unpaired."""
    return want_extra_unp_loe(k) - want_clip_gp(k) - want_j0_odd_unp(k)


def want_ug_fl(k: int) -> int:
    """n_ug is (xor_unp + ug-gu)/2."""
    return (want_xor_unp_fl(k) + want_ug_minus_gu(k)) // 2


def want_gu_fl(k: int) -> int:
    """n_gu is (xor_unp - ug-gu)/2."""
    return (want_xor_unp_fl(k) - want_ug_minus_gu(k)) // 2


def tot_form() -> dict:
    """k<=64: xor_unp F/L; dies at k=2 with shift 0.

    Do not call unpaired_xor_split / named_half_split here.
    Census is xor_unp_fold for k<=8.
    """
    n_ok = 0
    raw_k2 = (5 * ((-1) ** 2) + 7) // 10
    miss_pow = (5 * ((-1) ** 8) + 7) // 10
    miss_sign = (
        (1 << 6) * (28 * lucas(7) + 60 * fib(7) - 70) + 7
    ) // 10
    miss_p7 = (
        (1 << 6) * (28 * lucas(7) + 60 * fib(7) - 70)
        + 5 * ((-1) ** 8)
    ) // 10
    mask_sign7 = (
        (1 << 5) * (28 * lucas(6) + 60 * fib(6) - 70) + 7
    ) // 10
    if want_xor_unp_fl(0) != 0 or want_xor_unp_fl(1) != 0:
        return {"ok": False, "k01": True}
    if want_xor_unp_fl(2) != 3 or want_xor_unp_fl(3) != 15:
        return {"ok": False, "k23": True}
    if want_xor_unp_fl(8) != 9742:
        return {"ok": False, "k8": True}
    if want_xor_unp_fl(2) == raw_k2:
        return {"ok": False, "raw2": True}
    if want_xor_unp_fl(8) == miss_pow:
        return {"ok": False, "pow": True}
    if want_xor_unp_fl(8) == miss_sign:
        return {"ok": False, "sg": True}
    if want_xor_unp_fl(8) == miss_p7:
        return {"ok": False, "p7": True}
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
        if want_xor_unp_fl(k) != want_xor_unp_loe(k):
            return {"ok": False, "loe": True, "k": k}
        if want_xor_unp_fl(k) != want_extra_unp_fl(k) - want_clip_gp(k) - want_j0_odd_unp(k):
            return {"ok": False, "ex": True, "k": k}
        if want_xor_unp_fl(k) != want_xor_tot(k) - want_xor_lo_fl(k):
            return {"ok": False, "tot": True, "k": k}
        if want_ug_fl(k) + want_gu_fl(k) != want_xor_unp_fl(k):
            return {"ok": False, "sum": True, "k": k}
        if want_ug_fl(k) - want_gu_fl(k) != want_ug_minus_gu(k):
            return {"ok": False, "diff": True, "k": k}
        if k >= 2:
            n = (
                (1 << (k - 2)) * (28 * lucas(k - 1) + 60 * fib(k - 1) - 70)
                + 5 * ((-1) ** k)
                + 7
            )
            if n % 10 != 0 or n // 10 != want_xor_unp_fl(k):
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
        and want_xor_unp_fl(2) != raw_k2
        and want_xor_unp_fl(8) != miss_pow
        and want_xor_unp_fl(8) != miss_sign
        and want_xor_unp_fl(8) != miss_p7
        and want_xor_unp_fl(7) == mask_sign7
        and want_xor_unp_fl(8) != want_extra_unp_fl(8)
        and want_xor_unp_fl(8) != want_xor_lo_fl(8)
        and want_xor_unp_fl(8) != want_xor_tot(8)
        and want_xor_unp_fl(8) == 9742
        and want_ug_fl(8) == 4924
        and want_gu_fl(8) == 4818
        and want_extra_unp_fl(8) == 10019
        and want_xor_lo_fl(8) == 17311
        and want_xor_tot(8) == 27053
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and want_sm_fl(8) == 8790
        and want_sm(8) == 8790
        and want_ege_fl(8) == 5324
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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
        and miss_pow == 1
        and miss_sign == 9741
        and miss_p7 == 9741
        and mask_sign7 == 2925
        and raw_k2 == 1
        and want_xor_unp_fl(4) == 66
        and want_xor_unp_fl(5) == 245
        and want_xor_unp_fl(6) == 862
        and want_ug_fl(2) == 2
        and want_gu_fl(2) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def xor_unp_fold() -> dict:
    """k<=8 unpaired xor tot vs F/L; n_ug/n_gu halves."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = unpaired_xor_split(k)
        if a["n_bad"] != 0 or a["n_pg"] != 0:
            return {"ok": False, "bad": True, "k": k}
        xor = a["n_ug"] + a["n_gu"]
        if xor != want_xor_unp_fl(k):
            return {"ok": False, "xor": True, "k": k, "got": xor}
        if a["n_ug"] != want_ug_fl(k):
            return {"ok": False, "ug": True, "k": k, "got": a["n_ug"]}
        if a["n_gu"] != want_gu_fl(k):
            return {"ok": False, "gu": True, "k": k, "got": a["n_gu"]}
        if a["extra"] != want_extra_unp_fl(k):
            return {"ok": False, "ex": True, "k": k}
        if a["n_gp"] != want_clip_gp(k):
            return {"ok": False, "gp": True, "k": k}
        if a["n_neg"] != want_j0_odd_unp(k):
            return {"ok": False, "neg": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "xor_unp": xor,
            "n_ug": a["n_ug"],
            "n_gu": a["n_gu"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["xor_unp"] == 0
        and rows["2"]["xor_unp"] == 3
        and rows["2"]["n_ug"] == 2
        and rows["2"]["n_gu"] == 1
        and rows["3"]["xor_unp"] == 15
        and rows["8"]["xor_unp"] == 9742
        and rows["8"]["n_ug"] == 4924
        and rows["8"]["n_gu"] == 4818
        and want_xor_unp_fl(4) == 66
        and want_xor_unp_fl(5) == 245
        and want_xor_unp_fl(6) == 862
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L form at k=2 with shift 0; without power / sign / +7 at k=8."""
    raw_k2 = (5 * ((-1) ** 2) + 7) // 10
    miss_pow = (5 * ((-1) ** 8) + 7) // 10
    miss_sign = (
        (1 << 6) * (28 * lucas(7) + 60 * fib(7) - 70) + 7
    ) // 10
    miss_p7 = (
        (1 << 6) * (28 * lucas(7) + 60 * fib(7) - 70)
        + 5 * ((-1) ** 8)
    ) // 10
    mask_sign7 = (
        (1 << 5) * (28 * lucas(6) + 60 * fib(6) - 70) + 7
    ) // 10
    a8 = unpaired_xor_split(8)
    ok = (
        want_xor_unp_fl(2) != raw_k2
        and want_xor_unp_fl(8) != miss_pow
        and want_xor_unp_fl(8) != miss_sign
        and want_xor_unp_fl(8) != miss_p7
        and want_xor_unp_fl(7) == mask_sign7
        and want_xor_unp_fl(8) != want_extra_unp_fl(8)
        and want_xor_unp_fl(8) != want_xor_lo_fl(8)
        and want_xor_unp_fl(8) != want_xor_tot(8)
        and a8["n_ug"] + a8["n_gu"] == 9742
        and a8["n_ug"] == 4924
        and a8["n_gu"] == 4818
        and miss_pow == 1
        and miss_sign == 9741
        and miss_p7 == 9741
        and mask_sign7 == 2925
        and raw_k2 == 1
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
    wi = json.loads(WI_JSON.read_text())
    vr = json.loads(VR_JSON.read_text())
    uh = json.loads(UH_JSON.read_text())
    ok = (
        wi["checks"]["all_ok"]
        and vr["checks"]["all_ok"]
        and uh["checks"]["all_ok"]
        and wi["verdict"]["gpd1_s_eq_closed_k_ge_2"] == "LEMMA"
        and vr["verdict"]["extra_unp_eq_FL_closed_k_ge_2"] == "LEMMA"
        and uh["verdict"]["ug_minus_gu_eq_jacobsthal"] == "LEMMA"
        and wi["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wi["verdict"]["prize"] == "unsolved"
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
    cnt = xor_unp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "xor_unp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_unp_eq_FL_closed_k_ge_2": True,
            "xor_unp_eq_extra_unp_minus_clip_j0": True,
            "xor_unp_eq_xor_tot_minus_xor_lo": True,
            "ug_gu_eq_xor_unp_pm_diff": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_unp_eq_FL_closed_k_ge_2": "LEMMA",
            "xor_unp_eq_extra_unp_minus_clip_j0": "LEMMA",
            "xor_unp_eq_xor_tot_minus_xor_lo": "LEMMA",
            "ug_gu_eq_xor_unp_pm_diff": "LEMMA",
            "xor_unp_FL_shift0_at_k2": "KILLED",
            "xor_unp_without_pow_at_k8": "KILLED",
            "xor_unp_without_sign_at_k8": "KILLED",
            "xor_unp_without_p7_at_k8": "KILLED",
            "xor_unp_eq_extra_unp": "KILLED",
            "xor_unp_eq_xor_lo": "KILLED",
            "xor_unp_eq_xor_tot": "KILLED",
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
        "xor_unp k8",
        dump["xor_unp_fold"]["rows"]["8"]["xor_unp"],
        "ug",
        dump["xor_unp_fold"]["rows"]["8"]["n_ug"],
        "gu",
        dump["xor_unp_fold"]["rows"]["8"]["n_gu"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
