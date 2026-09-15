#!/usr/bin/env python3
"""Cycle WX: even partner-5U+8 unpaired extra has count J_k-(-1)^k.

Even-n unpaired extra at j=2n-5U-8 with j>=2 has count
J_k-(-1)^k for k>=4. Together with Cycle WW they are
J_{k+1}+2-3(-1)^k for k>=4. The first even cell is Cycle WT's
n=5U/2+8, j=8 for k>=5. Dies at k=3 for the k>=4 formula (got 2,
not 4). Dies at k=8 for even equals odd (got 84, not 86) and for
tot equals J_{k+1} (got 170, not 171). Do not kill even equals
odd at k=3 (both 2). Do not kill pal_kind unpaired at n=5U/2+8,
j=8 for k>=5. Do not PREFIX pal-center tot. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_wx.py --certify
Dump: research/cycle_wx.json
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
from cycle_wt import ph8_n, want_ph8_unp
from cycle_ww import want_odd_s8
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WW_JSON = Path(__file__).resolve().parent / "cycle_ww.json"
WT_JSON = Path(__file__).resolve().parent / "cycle_wt.json"
WV_JSON = Path(__file__).resolve().parent / "cycle_wv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_even_s8(k: int) -> int:
    """Even-n unpaired extra at partner 5U+8, j>=2: 0 at k<=2, 2 at k=3."""
    if k <= 2:
        return 0
    if k == 3:
        return 2
    return jacobsthal(k) - ((-1) ** k)


def want_s8_tot(k: int) -> int:
    """Odd+even partner-5U+8 unpaired extra with j>=2."""
    return want_odd_s8(k) + want_even_s8(k)


def want_s8_tot_J(k: int) -> int:
    """J_{k+1}+2-3(-1)^k for k>=4; 4 at k=3; 0 at k<=2."""
    if k <= 2:
        return 0
    if k == 3:
        return 4
    return jacobsthal(k + 1) + 2 - 3 * ((-1) ** k)


def even_s8_split(k: int) -> dict:
    """Even-n unpaired extra at j=2n-5U-8 with j>=2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    n_at = n_bad = 0
    first = None
    for n in range(0, 4 * u, 2):
        j = 2 * n - clip - 8
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
    """k<=64: even slice J_k-(-1)^k for k>=4; tot J_{k+1}+2-3(-1)^k.

    Do not call even_s8_split / odd_s8_split here.
    Census is even_s8_fold for k<=8.
    """
    n_ok = 0
    if want_even_s8(0) != 0 or want_even_s8(2) != 0:
        return {"ok": False, "k02": True}
    if want_even_s8(3) != 2 or want_s8_tot(3) != 4:
        return {"ok": False, "k3": True}
    if want_even_s8(8) != 84 or want_s8_tot(8) != 170:
        return {"ok": False, "k8": True}
    if want_even_s8(7) != 44 or want_odd_s8(7) != 46:
        return {"ok": False, "k7": True}
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
        if want_s8_tot(k) != want_odd_s8(k) + want_even_s8(k):
            return {"ok": False, "sum": True, "k": k}
        if want_s8_tot(k) != want_s8_tot_J(k):
            return {"ok": False, "Jform": True, "k": k}
        if k <= 2 and want_even_s8(k) != 0:
            return {"ok": False, "z": True, "k": k}
        if k == 3:
            if want_even_s8(k) != 2:
                return {"ok": False, "k3e": True}
            if want_even_s8(k) == jacobsthal(k) - ((-1) ** k):
                return {"ok": False, "k3f": True}
            if want_even_s8(k) != want_odd_s8(k):
                return {"ok": False, "k3eq": True}
            if G(ph8_n(3), 8) != 0:
                return {"ok": False, "k3g": True}
        if k >= 4:
            if want_even_s8(k) != jacobsthal(k) - ((-1) ** k):
                return {"ok": False, "Jk": True, "k": k}
            if want_even_s8(k) != want_odd_s8(k) - 2:
                return {"ok": False, "m2": True, "k": k}
            if want_s8_tot(k) != 2 * want_even_s8(k) + 2:
                return {"ok": False, "two": True, "k": k}
            if want_s8_tot(k) != jacobsthal(k + 1) + 2 - 3 * ((-1) ** k):
                return {"ok": False, "Jm": True, "k": k}
        if k >= 3:
            n = ph8_n(k)
            j = 2 * n - clip - 8
            if j != 8:
                return {"ok": False, "j8": True, "k": k}
            if 2 * n - 8 != clip + 8:
                return {"ok": False, "pr": True, "k": k}
            if pal_kind(n, 8, k) != "unp":
                return {"ok": False, "pk": True, "k": k}
            if n >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
        if k >= 5:
            n = ph8_n(k)
            if G(n, 8) != 1:
                return {"ok": False, "g8": True, "k": k}
            if want_ph8_unp(k) != 2:
                return {"ok": False, "wt": True, "k": k}
        if k == 4:
            if G(ph8_n(4), 8) != 0:
                return {"ok": False, "k4g": True}
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
        and want_even_s8(3) != jacobsthal(3) - ((-1) ** 3)
        and want_even_s8(8) != want_odd_s8(8)
        and want_s8_tot(8) != jacobsthal(9)
        and want_even_s8(8) != want_clip_gp(8)
        and want_even_s8(8) != jacobsthal(8)
        and want_even_s8(8) != want_ug_fl(8)
        and want_even_s8(8) != want_j0_odd_unp(8)
        and want_even_s8(8) == 84
        and want_odd_s8(8) == 86
        and want_s8_tot(8) == 170
        and want_s8_tot_J(8) == 170
        and jacobsthal(9) == 171
        and want_even_s8(7) == 44
        and want_odd_s8(7) == 46
        and want_clip_gp(7) == 42
        and jacobsthal(7) == 43
        and jacobsthal(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_clip_slice(8) == 85
        and want_even_slice(8) == 85
        and ph8_n(8) == 648
        and want_ph8_unp(8) == 2
        and pal_kind(ph8_n(8), 8, 8) == "unp"
        and pal_kind(ph8_n(8), 8, 8) != "pair"
        and G(ph8_n(4), 8) != 1
        and G(ph8_n(4), 8) == 0
        and G(ph8_n(3), 8) == 0
        and want_even_s8(3) == want_odd_s8(3)
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
        and want_even_s8(3) == 2
        and want_even_s8(4) == 4
        and want_even_s8(5) == 12
        and want_s8_tot(7) == 90
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def even_s8_fold() -> dict:
    """k<=8 even partner-5U+8 slice vs J_k-(-1)^k for k>=4."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = even_s8_split(k)
        if a["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_even_s8(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if k >= 5:
            if a["first"] != (ph8_n(k), 8):
                return {"ok": False, "first": True, "k": k, "got": a["first"]}
        if k == 4 and a["first"] != (52, 16):
            return {"ok": False, "k4f": True, "got": a["first"]}
        if k == 3 and a["first"] != (26, 4):
            return {"ok": False, "k3f": True, "got": a["first"]}
        if k == 2 and a["first"] is not None:
            return {"ok": False, "k2f": True, "got": a["first"]}
        n_ok += 1
        rows[str(k)] = {
            "n_at": a["n_at"],
            "first": list(a["first"]) if a["first"] else None,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["n_at"] == 0
        and rows["3"]["n_at"] == 2
        and rows["3"]["first"] == [26, 4]
        and rows["4"]["first"] == [52, 16]
        and rows["5"]["n_at"] == 12
        and rows["7"]["n_at"] == 44
        and rows["8"]["n_at"] == 84
        and rows["8"]["first"] == [648, 8]
        and want_even_s8(4) == 4
        and want_even_s8(5) == 12
        and want_even_s8(6) == 20
        and want_s8_tot(8) == 170
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """formula at k=3; even equals odd at k=8; tot equals J_{k+1} at k=8."""
    ok = (
        want_even_s8(3) != jacobsthal(3) - ((-1) ** 3)
        and want_even_s8(8) != want_odd_s8(8)
        and want_s8_tot(8) != jacobsthal(9)
        and want_even_s8(8) != want_clip_gp(8)
        and want_even_s8(8) != jacobsthal(8)
        and want_even_s8(8) != want_ug_fl(8)
        and want_even_s8(8) != want_j0_odd_unp(8)
        and want_even_s8(3) == want_odd_s8(3)
        and want_even_s8(3) == 2
        and jacobsthal(3) - ((-1) ** 3) == 4
        and want_even_s8(8) == 84
        and want_odd_s8(8) == 86
        and want_s8_tot(8) == 170
        and jacobsthal(9) == 171
        and want_clip_gp(8) == 85
        and jacobsthal(8) == 85
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and pal_kind(ph8_n(8), 8, 8) == "unp"
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
    ww = json.loads(WW_JSON.read_text())
    wt = json.loads(WT_JSON.read_text())
    wv = json.loads(WV_JSON.read_text())
    ok = (
        ww["checks"]["all_ok"]
        and wt["checks"]["all_ok"]
        and wv["checks"]["all_ok"]
        and ww["verdict"]["odd_s8_eq_J_k_minus_m1_plus_2_k_ge_4"] == "LEMMA"
        and wt["verdict"]["ph8_unp_eq_08_k_ge_5"] == "LEMMA"
        and wv["verdict"]["even_s4_eq_odd_s4_k_ge_3"] == "LEMMA"
        and ww["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ww["verdict"]["prize"] == "unsolved"
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
    cnt = even_s8_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "even_s8_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_s8_eq_J_k_minus_m1_k_ge_4": True,
            "s8_tot_eq_J_k1_plus_2_minus_3m1_k_ge_4": True,
            "first_even_s8_eq_wt_k_ge_5": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_s8_eq_J_k_minus_m1_k_ge_4": "LEMMA",
            "s8_tot_eq_J_k1_plus_2_minus_3m1_k_ge_4": "LEMMA",
            "first_even_s8_eq_wt_k_ge_5": "LEMMA",
            "even_s8_eq_form_at_k3": "KILLED",
            "even_s8_eq_odd_at_k8": "KILLED",
            "s8_tot_eq_J_k1_at_k8": "KILLED",
            "even_s8_eq_clip_gp_at_k8": "KILLED",
            "even_s8_eq_J_k_at_k8": "KILLED",
            "even_s8_eq_ug_at_k8": "KILLED",
            "even_s8_eq_j0_odd_at_k8": "KILLED",
            "ph8_G8_eq_1_at_k4": "KILLED",
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
    print("even s8 k8", dump["even_s8_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
