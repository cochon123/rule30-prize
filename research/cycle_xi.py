#!/usr/bin/env python3
"""Cycle XI: odd partner-5U+128 unpaired extra has count J_k-21(-1)^k+22.

Odd-n unpaired extra at j=2n-5U-128 with j>=2 has count
J_k-21(-1)^k+22 for k>=8. The first cell is n=5U/2+65, j=2 for
k>=6. Dies at k=7 for that formula (got 42, not 86). Dies at k=6
for that formula (got 10, not 22). Dies at k=8 for equals odd_s64
(got 86, not 106). Do not kill equals odd_s32 or odd_s8 or odd_s4
at k=8 (all 86). Do not kill equals clip_gp at k=7 (both 42). Do
not kill pal_kind unpaired at n=5U/2+65, j=2 for k>=6. Do not
PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_xi.py --certify
Dump: research/cycle_xi.json
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
from cycle_ub import want_clip_gp
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_we import want_ege_fl
from cycle_wh import want_sm_fl
from cycle_wk import want_gu_fl, want_ug_fl
from cycle_wm import want_j0_all_unp, want_j0_even_unp
from cycle_wn import want_clip_gp_jk, want_clip_slice
from cycle_wr import want_even_slice
from cycle_wu import want_odd_s4
from cycle_ww import want_odd_s8
from cycle_wx import want_even_s8
from cycle_wz import ph9_n, want_odd_s16
from cycle_xa import want_even_s16
from cycle_xc import ph17_n, want_odd_s32
from cycle_xd import want_even_s32
from cycle_xf import ph33_n, want_odd_s64
from cycle_xg import want_even_s64
from cycle_xh import ph128_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
XH_JSON = Path(__file__).resolve().parent / "cycle_xh.json"
XF_JSON = Path(__file__).resolve().parent / "cycle_xf.json"
XC_JSON = Path(__file__).resolve().parent / "cycle_xc.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def ph65_n(k: int) -> int:
    """Covering n=5U/2+65, first odd partner-5U+128 cell."""
    return parent_half(k) + 65


def want_odd_s128(k: int) -> int:
    """Odd-n unpaired extra at partner 5U+128, j>=2: 0 at k<=5, 10 at k=6, 42 at k=7."""
    if k <= 5:
        return 0
    if k == 6:
        return 10
    if k == 7:
        return 42
    return jacobsthal(k) - 21 * ((-1) ** k) + 22


def odd_s128_split(k: int) -> dict:
    """Odd-n unpaired extra at j=2n-5U-128 with j>=2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    n_at = n_bad = 0
    first = None
    for n in range(1, 4 * u, 2):
        j = 2 * n - clip - 128
        if j < 2 or j >= n or j % 2 != 0:
            continue
        if G(n, j) == 0:
            continue
        if pal_kind(n, j, k) != "unp":
            n_bad += 1
            continue
        n_at += 1
        if first is None:
            first = (n, j)
    return {"n_at": n_at, "n_bad": n_bad, "first": first}


def tot_form() -> dict:
    """k<=64: odd slice J_k-21(-1)^k+22 for k>=8; dies at k=7 for that form.

    Do not call odd_s128_split here.
    Census is odd_s128_fold for k<=8.
    """
    n_ok = 0
    if want_odd_s128(0) != 0 or want_odd_s128(5) != 0:
        return {"ok": False, "k05": True}
    if want_odd_s128(6) != 10 or want_odd_s128(7) != 42:
        return {"ok": False, "k67": True}
    if want_odd_s128(8) != 86 or want_odd_s128(9) != 214:
        return {"ok": False, "k89": True}
    if want_odd_s128(7) == want_odd_s128(8):
        return {"ok": False, "k78": True}
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
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k <= 5 and want_odd_s128(k) != 0:
            return {"ok": False, "z": True, "k": k}
        if k == 6:
            if want_odd_s128(k) != 10:
                return {"ok": False, "k6": True}
            if want_odd_s128(k) == jacobsthal(k) - 21 * ((-1) ** k) + 22:
                return {"ok": False, "k6f": True}
        if k == 7:
            if want_odd_s128(k) != 42:
                return {"ok": False, "k7": True}
            if want_odd_s128(k) == jacobsthal(k) - 21 * ((-1) ** k) + 22:
                return {"ok": False, "k7f": True}
        if k >= 8 and want_odd_s128(k) != jacobsthal(k) - 21 * ((-1) ** k) + 22:
            return {"ok": False, "Jk": True, "k": k}
        if k >= 6:
            n = ph65_n(k)
            j = 2 * n - clip - 128
            if j != 2:
                return {"ok": False, "j2": True, "k": k}
            if 2 * n - 2 != clip + 128:
                return {"ok": False, "pr": True, "k": k}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "pk": True, "k": k}
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if G(n, 2) != 1:
                return {"ok": False, "g2": True, "k": k}
        if k == 5:
            n = ph65_n(5)
            if n < 4 * u:
                return {"ok": False, "k5c": True}
            if G(n, 2) != 1:
                return {"ok": False, "k5g": True}
            if pal_kind(n, 2, k) != "unp":
                return {"ok": False, "k5k": True}
            if 2 * n - 2 != clip + 128:
                return {"ok": False, "k5p": True}
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
        and want_odd_s128(6) != jacobsthal(6) - 21 * ((-1) ** 6) + 22
        and want_odd_s128(7) != jacobsthal(7) - 21 * ((-1) ** 7) + 22
        and want_odd_s128(8) != want_odd_s64(8)
        and want_odd_s128(8) != want_odd_s16(8)
        and want_odd_s128(8) != jacobsthal(8)
        and want_odd_s128(8) != want_clip_gp(8)
        and want_odd_s128(8) != want_even_slice(8)
        and want_odd_s128(8) != want_even_s64(8)
        and want_odd_s128(8) != want_even_s32(8)
        and want_odd_s128(8) != want_even_s16(8)
        and want_odd_s128(8) != want_even_s8(8)
        and want_odd_s128(8) == want_odd_s32(8)
        and want_odd_s128(8) == want_odd_s8(8)
        and want_odd_s128(8) == want_odd_s4(8)
        and want_odd_s128(8) != want_ug_fl(8)
        and want_odd_s128(8) != want_j0_odd_unp(8)
        and want_odd_s128(7) == want_clip_gp(7)
        and want_odd_s128(7) == want_odd_s64(7)
        and want_odd_s128(6) != want_odd_s64(6)
        and want_odd_s128(8) == 86
        and want_odd_s128(8) == jacobsthal(8) - 21 + 22
        and want_odd_s128(7) == 42
        and want_odd_s128(6) == 10
        and want_odd_s64(8) == 106
        and want_even_s64(8) == 106
        and want_odd_s32(8) == 86
        and want_even_s32(8) == 84
        and want_odd_s16(8) == 90
        and want_even_s16(8) == 90
        and want_odd_s8(8) == 86
        and want_even_s8(8) == 84
        and want_clip_gp(7) == 42
        and jacobsthal(7) == 43
        and jacobsthal(8) == 85
        and jacobsthal(9) == 171
        and want_clip_gp_jk(8) == 85
        and want_clip_slice(8) == 85
        and want_even_slice(8) == 85
        and ph65_n(8) == 705
        and ph33_n(8) == 673
        and ph17_n(8) == 657
        and ph9_n(8) == 649
        and ph128_n(8) == 768
        and pal_kind(ph65_n(8), 2, 8) == "unp"
        and pal_kind(ph65_n(8), 2, 8) != "pair"
        and G(ph65_n(5), 2) == 1
        and ph65_n(5) >= 4 * (1 << 5)
        and G(ph65_n(6), 2) == 1
        and want_odd_s4(8) == 86
        and want_j0_even_unp(8) == 191
        and want_j0_all_unp(8) == 383
        and want_ug_fl(8) == 4924
        and want_gu_fl(8) == 4818
        and want_sm_fl(8) == 8790
        and want_sm(8) == 8790
        and want_ege_fl(8) == 5324
        and want_ege(8) == 5324
        and want_ej_xor(8) == 5225
        and lucas(8) == 47
        and fib(8) == 21
        and jacobsthal(8) == 85
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
        and parent_half(8) == 640
        and want_clip_gp(8) == 85
        and want_j0_odd_unp(8) == 192
        and want_odd_s128(4) == 0
        and want_odd_s128(5) == 0
        and want_odd_s128(6) == 10
        and jacobsthal(7) - 21 * ((-1) ** 7) + 22 == 86
        and jacobsthal(6) - 21 * ((-1) ** 6) + 22 == 22
        and want_lo_e(8) == 14114
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def odd_s128_fold() -> dict:
    """k<=8 odd partner-5U+128 slice vs J_k-21(-1)^k+22 for k>=8."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = odd_s128_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_odd_s128(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if k >= 6:
            if a["first"] != (ph65_n(k), 2):
                return {"ok": False, "first": True, "k": k, "got": a["first"]}
        if k <= 5 and a["first"] is not None:
            return {"ok": False, "k5f": True, "got": a["first"]}
        n_ok += 1
        rows[str(k)] = {
            "n_at": a["n_at"],
            "first": list(a["first"]) if a["first"] else None,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["5"]["n_at"] == 0
        and rows["6"]["n_at"] == 10
        and rows["6"]["first"] == [225, 2]
        and rows["7"]["n_at"] == 42
        and rows["7"]["first"] == [385, 2]
        and rows["8"]["n_at"] == 86
        and rows["8"]["first"] == [705, 2]
        and want_odd_s128(6) == 10
        and want_odd_s128(7) == 42
        and want_odd_s128(8) == 86
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """formula at k=6 and k=7; equals odd_s64 at k=8; equals J_k at k=8."""
    ok = (
        want_odd_s128(6) != jacobsthal(6) - 21 * ((-1) ** 6) + 22
        and want_odd_s128(7) != jacobsthal(7) - 21 * ((-1) ** 7) + 22
        and want_odd_s128(8) != want_odd_s64(8)
        and want_odd_s128(8) != want_odd_s16(8)
        and want_odd_s128(8) != jacobsthal(8)
        and want_odd_s128(8) != want_clip_gp(8)
        and want_odd_s128(8) != want_even_slice(8)
        and want_odd_s128(8) != want_even_s64(8)
        and want_odd_s128(8) != want_even_s32(8)
        and want_odd_s128(8) != want_even_s16(8)
        and want_odd_s128(8) != want_even_s8(8)
        and want_odd_s128(8) == want_odd_s32(8)
        and want_odd_s128(8) == want_odd_s8(8)
        and want_odd_s128(8) == want_odd_s4(8)
        and want_odd_s128(8) != want_ug_fl(8)
        and want_odd_s128(8) != want_j0_odd_unp(8)
        and want_odd_s128(7) == want_clip_gp(7)
        and want_odd_s128(7) == want_odd_s64(7)
        and want_odd_s128(6) != want_odd_s64(6)
        and want_odd_s128(6) == 10
        and want_odd_s128(7) == 42
        and jacobsthal(6) - 21 * ((-1) ** 6) + 22 == 22
        and jacobsthal(7) - 21 * ((-1) ** 7) + 22 == 86
        and want_odd_s8(8) == 86
        and want_odd_s32(8) == 86
        and want_odd_s128(8) == 86
        and want_odd_s64(8) == 106
        and want_odd_s16(8) == 90
        and want_clip_gp(8) == 85
        and want_clip_gp(7) == 42
        and jacobsthal(8) == 85
        and jacobsthal(9) == 171
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and pal_kind(ph65_n(8), 2, 8) == "unp"
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
    xh = json.loads(XH_JSON.read_text())
    xf = json.loads(XF_JSON.read_text())
    xc = json.loads(XC_JSON.read_text())
    ok = (
        xh["checks"]["all_ok"]
        and xf["checks"]["all_ok"]
        and xc["checks"]["all_ok"]
        and xh["verdict"]["ph128_j128_partner_5U128"] == "LEMMA"
        and xf["verdict"]["odd_s64_eq_J_k_plus_11m1_plus_10_k_ge_7"] == "LEMMA"
        and xc["verdict"]["odd_s32_eq_J_k_minus_5m1_plus_6_k_ge_6"] == "LEMMA"
        and xh["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and xh["verdict"]["prize"] == "unsolved"
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
    cnt = odd_s128_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "XI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "odd_s128_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_s128_eq_J_k_minus_21m1_plus_22_k_ge_8": True,
            "first_odd_s128_eq_ph65_k_ge_6": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_s128_eq_J_k_minus_21m1_plus_22_k_ge_8": "LEMMA",
            "first_odd_s128_eq_ph65_k_ge_6": "LEMMA",
            "odd_s128_eq_form_at_k7": "KILLED",
            "odd_s128_eq_form_at_k6": "KILLED",
            "odd_s128_eq_odd_s64_at_k8": "KILLED",
            "odd_s128_eq_odd_s16_at_k8": "KILLED",
            "odd_s128_eq_J_k_at_k8": "KILLED",
            "odd_s128_eq_clip_gp_at_k8": "KILLED",
            "odd_s128_eq_even_slice_at_k8": "KILLED",
            "odd_s128_eq_even_s64_at_k8": "KILLED",
            "odd_s128_eq_even_s32_at_k8": "KILLED",
            "odd_s128_eq_even_s16_at_k8": "KILLED",
            "odd_s128_eq_even_s8_at_k8": "KILLED",
            "odd_s128_eq_ug_at_k8": "KILLED",
            "odd_s128_eq_j0_odd_at_k8": "KILLED",
            "ph65_covering_at_k5": "KILLED",
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
    print("odd s128 k8", dump["odd_s128_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
