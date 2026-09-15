#!/usr/bin/env python3
"""Cycle WM: covering j=0 unpaired is exactly n in (5U/2, 4U).

pal_kind(n,0) is unp iff 2n>5U iff n>5U/2. On covering n<4U those
cells are n=5U/2+1,...,4U-1. Odd count is Cycle UA 3*2^{k-2} for
k>=2. Even count is 3*2^{k-2}-1 for k>=2; 1 at k=1; 0 at k<=0. Tot
is 3*2^{k-1}-1 for k>=2. Dies at k=2 without the even -1 (got 3,
not 2). Dies at k=8 without the even -1 (got 192, not 191), for
even equals odd (got 191, not 192), even equals leftover j=0 small
(got 191, not 318), tot equals odd (got 383, not 192), pal_kind at
n=5U/2 unpaired (it is pair), pal_kind at n=1 unpaired, and
pal_kind at n=0 unpaired. Do not kill pal_kind at n=5U/2+1 or
n=4U-1 unpaired: those cells are unp. Do not PREFIX pal-center tot.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wm.py --certify
Dump: research/cycle_wm.json
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
from cycle_wl import want_neg_l, want_neg_s
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
WL_JSON = Path(__file__).resolve().parent / "cycle_wl.json"
UA_JSON = Path(__file__).resolve().parent / "cycle_ua.json"
UU_JSON = Path(__file__).resolve().parent / "cycle_uu.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_j0_even_unp(k: int) -> int:
    """j=0 unpaired on even n in (5U/2, 4U): 0,1, then 3*2^{k-2}-1."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return 3 * (1 << (k - 2)) - 1


def want_j0_all_unp(k: int) -> int:
    """j=0 unpaired on all covering n in (5U/2, 4U)."""
    return want_j0_odd_unp(k) + want_j0_even_unp(k)


def j0_unp_split(k: int) -> dict:
    """Covering j=0 unpaired even/odd counts. Do not call from tot_form."""
    u = 1 << k
    ph = parent_half(k)
    even = odd = extra = 0
    for n in range(0, 4 * u):
        if pal_kind(n, 0, k) != "unp":
            continue
        extra += 1
        if G(n, 0) != 1 or n <= ph:
            extra += 1000
            continue
        if n % 2 == 0:
            even += 1
        else:
            odd += 1
    return {"even": even, "odd": odd, "all": even + odd, "extra": extra}


def tot_form() -> dict:
    """k<=64: j=0 unpaired window; dies at k=2 without even -1.

    Do not call j0_unp_split / unpaired_xor_half here.
    Census is j0_unp_fold for k<=8.
    """
    n_ok = 0
    raw_e2 = 3 * (1 << 0)
    miss_e8 = 3 * (1 << 6)
    if want_j0_even_unp(0) != 0 or want_j0_even_unp(1) != 1:
        return {"ok": False, "k01": True}
    if want_j0_even_unp(2) != 2 or want_j0_all_unp(2) != 5:
        return {"ok": False, "k2": True}
    if want_j0_even_unp(8) != 191 or want_j0_all_unp(8) != 383:
        return {"ok": False, "k8": True}
    if pal_kind(parent_half(8), 0, 8) == "unp":
        return {"ok": False, "ph8": True}
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
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if pal_kind(0, 0, k) == "unp":
            return {"ok": False, "n0": True, "k": k}
        if pal_kind(1, 0, k) == "unp":
            return {"ok": False, "n1": True, "k": k}
        if pal_kind(ph, 0, k) == "unp":
            return {"ok": False, "phu": True, "k": k}
        n_hi = 4 * u - 1
        if pal_kind(n_hi, 0, k) != "unp":
            return {"ok": False, "nl": True, "k": k}
        if pal_kind(ph + 1, 0, k) != "unp":
            return {"ok": False, "ph1": True, "k": k}
        if (pal_kind(ph + 1, 0, k) == "unp") != (2 * (ph + 1) > clip):
            return {"ok": False, "iff": True, "k": k}
        if want_j0_odd_unp(k) != want_neg_l(k):
            return {"ok": False, "neg": True, "k": k}
        if want_neg_s(k) != 0:
            return {"ok": False, "negs": True, "k": k}
        if want_j0_all_unp(k) != want_j0_odd_unp(k) + want_j0_even_unp(k):
            return {"ok": False, "sum": True, "k": k}
        if k >= 2:
            if want_j0_even_unp(k) != 3 * (1 << (k - 2)) - 1:
                return {"ok": False, "ef": True, "k": k}
            if want_j0_odd_unp(k) != 3 * (1 << (k - 2)):
                return {"ok": False, "of": True, "k": k}
            if want_j0_all_unp(k) != 3 * (1 << (k - 1)) - 1:
                return {"ok": False, "af": True, "k": k}
            if want_j0_even_unp(k) + want_even_j0_sm(k) + 3 != 2 * u:
                return {"ok": False, "part": True, "k": k}
        if k >= 3 and want_j0_even_unp(k) != 2 * want_j0_even_unp(k - 1) + 1:
            return {"ok": False, "erec": True, "k": k}
        if k >= 2 and want_j0_all_unp(k) != 2 * want_j0_all_unp(k - 1) + 1:
            return {"ok": False, "arec": True, "k": k}
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
        and want_j0_even_unp(2) != raw_e2
        and want_j0_even_unp(8) != miss_e8
        and want_j0_even_unp(8) != want_j0_odd_unp(8)
        and want_j0_even_unp(8) != want_even_j0_sm(8)
        and want_j0_all_unp(8) != want_j0_odd_unp(8)
        and pal_kind(parent_half(8), 0, 8) != "unp"
        and pal_kind(1, 0, 8) != "unp"
        and pal_kind(0, 0, 8) != "unp"
        and pal_kind(parent_half(8) + 1, 0, 8) == "unp"
        and pal_kind((1 << 8) * 4 - 1, 0, 8) == "unp"
        and want_j0_even_unp(8) == 191
        and want_j0_odd_unp(8) == 192
        and want_j0_all_unp(8) == 383
        and want_even_j0_sm(8) == 318
        and want_clip_gp(8) == 85
        and want_ug_fl(8) == 4924
        and want_gu_fl(8) == 4818
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
        and want_miss_n(8) == 769
        and want_3u(8) == 768
        and parent_half(8) == 640
        and raw_e2 == 3
        and miss_e8 == 192
        and want_j0_even_unp(3) == 5
        and want_j0_even_unp(4) == 11
        and want_j0_even_unp(5) == 23
        and want_j0_even_unp(6) == 47
        and want_j0_even_unp(7) == 95
        and want_j0_all_unp(2) == 5
        and want_j0_all_unp(3) == 11
        and want_j0_even_unp(1) == want_even_j0_sm(1)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def j0_unp_fold() -> dict:
    """k<=8 covering j=0 unpaired vs even/odd/all forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = j0_unp_split(k)
        if a["extra"] != a["all"]:
            return {"ok": False, "extra": True, "k": k, "got": a}
        if a["even"] != want_j0_even_unp(k):
            return {"ok": False, "even": True, "k": k, "got": a["even"]}
        if a["odd"] != want_j0_odd_unp(k):
            return {"ok": False, "odd": True, "k": k, "got": a["odd"]}
        if a["all"] != want_j0_all_unp(k):
            return {"ok": False, "all": True, "k": k, "got": a["all"]}
        n_ok += 1
        rows[str(k)] = {"even": a["even"], "odd": a["odd"], "all": a["all"]}
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["even"] == 0
        and rows["0"]["odd"] == 1
        and rows["1"]["even"] == 1
        and rows["1"]["odd"] == 1
        and rows["2"]["even"] == 2
        and rows["2"]["odd"] == 3
        and rows["2"]["all"] == 5
        and rows["8"]["even"] == 191
        and rows["8"]["odd"] == 192
        and rows["8"]["all"] == 383
        and want_j0_even_unp(3) == 5
        and want_j0_even_unp(4) == 11
        and want_j0_even_unp(5) == 23
        and want_j0_even_unp(6) == 47
        and want_j0_even_unp(7) == 95
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """Even form without -1 at k=2 and k=8; equals odd/sm/tot-odd."""
    raw_e2 = 3 * (1 << 0)
    miss_e8 = 3 * (1 << 6)
    ok = (
        want_j0_even_unp(2) != raw_e2
        and want_j0_even_unp(8) != miss_e8
        and want_j0_even_unp(8) != want_j0_odd_unp(8)
        and want_j0_even_unp(8) != want_even_j0_sm(8)
        and want_j0_all_unp(8) != want_j0_odd_unp(8)
        and pal_kind(parent_half(8), 0, 8) != "unp"
        and pal_kind(1, 0, 8) != "unp"
        and pal_kind(0, 0, 8) != "unp"
        and pal_kind(parent_half(8) + 1, 0, 8) == "unp"
        and pal_kind((1 << 8) * 4 - 1, 0, 8) == "unp"
        and want_j0_even_unp(8) == 191
        and want_j0_odd_unp(8) == 192
        and want_j0_all_unp(8) == 383
        and want_even_j0_sm(8) == 318
        and raw_e2 == 3
        and miss_e8 == 192
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
    wl = json.loads(WL_JSON.read_text())
    ua = json.loads(UA_JSON.read_text())
    uu = json.loads(UU_JSON.read_text())
    ok = (
        wl["checks"]["all_ok"]
        and ua["checks"]["all_ok"]
        and uu["checks"]["all_ok"]
        and wl["verdict"]["unp_never_n_le_ph"] == "LEMMA"
        and ua["verdict"]["j0_odd_unp_eq_3_2km2"] == "LEMMA"
        and uu["verdict"]["even_j0_sm_eq_5_2km2_minus_2"] == "LEMMA"
        and wl["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wl["verdict"]["prize"] == "unsolved"
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
    cnt = j0_unp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "j0_unp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "j0_unp_eq_window": True,
            "j0_even_unp_eq_3_2km2_minus_1": True,
            "j0_all_unp_eq_3_2km1_minus_1": True,
            "j0_even_plus_sm_plus_3_eq_2U": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "j0_unp_eq_window": "LEMMA",
            "j0_even_unp_eq_3_2km2_minus_1": "LEMMA",
            "j0_all_unp_eq_3_2km1_minus_1": "LEMMA",
            "j0_even_plus_sm_plus_3_eq_2U": "LEMMA",
            "j0_even_without_m1_at_k2": "KILLED",
            "j0_even_without_m1_at_k8": "KILLED",
            "j0_even_eq_odd_at_k8": "KILLED",
            "j0_even_eq_sm_at_k8": "KILLED",
            "j0_all_eq_odd_at_k8": "KILLED",
            "ph_j0_unp_at_k8": "KILLED",
            "n1_unp_at_k8": "KILLED",
            "n0_unp_at_k8": "KILLED",
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
    print("j0 k8", dump["j0_unp_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
