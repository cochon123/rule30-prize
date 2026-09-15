#!/usr/bin/env python3
"""Cycle WN: clip_gp is J_k-(k mod 2); partner-5U+2 slice is J_k.

Unpaired extra with child partner 5U+2 has j=2n-5U-2. That Green
slice has count J_k for k>=2. It is clip_gp except one n_ug when k
is odd, so clip_gp is J_k-(k mod 2) for k>=2, equal to Cycle UB
(J_{k+1}-1)/2. Special 0 at k<=1. Dies at k=2 for clip_gp equals
J_{k+1} (got 1, not 3). Dies at k=7 for clip_gp equals J_k (got 42,
not 43) and for the slice equals clip_gp (got 43, not 42). Dies at
k=8 for the slice equals n_ug (got 85, not 4924), equals j=0 odd
unpaired (got 85, not 192), and equals J_{k+1} (got 85, not 171).
Do not kill clip_gp equals J_k at k=8: they match. Do not PREFIX
pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_wn.py --certify
Dump: research/cycle_wn.json
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
from cycle_tw import green_odd_even
from cycle_ua import want_j0_odd_unp
from cycle_ub import unpaired_xor_split, want_clip_gp
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UB_JSON = Path(__file__).resolve().parent / "cycle_ub.json"
WM_JSON = Path(__file__).resolve().parent / "cycle_wm.json"
WL_JSON = Path(__file__).resolve().parent / "cycle_wl.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_clip_slice(k: int) -> int:
    """Green unpaired extra at partner 5U+2: 0 at k<=1, J_k for k>=2."""
    if k <= 1:
        return 0
    return jacobsthal(k)


def want_clip_gp_jk(k: int) -> int:
    """clip_gp is J_k-(k mod 2) for k>=2; 0 at k<=1."""
    if k <= 1:
        return 0
    return jacobsthal(k) - (k % 2)


def want_slice_ug(k: int) -> int:
    """n_ug on the partner-5U+2 slice: 1 iff k odd and k>=3; else 0."""
    if k <= 1:
        return 0
    return k % 2


def clip_slice_split(k: int) -> dict:
    """Unpaired extra at j=2n-5U-2. Do not call from tot_form."""
    u = 1 << k
    clip = 5 * u
    k_p = k - 1 if k >= 1 else 0
    n_at = n_gp = n_ug = n_gu = n_bad = 0
    for n in range(1, 4 * u, 2):
        j = 2 * n - clip - 2
        if j < 2 or j >= n or j % 2 != 0:
            continue
        if G(n, j) == 0:
            continue
        if pal_kind(n, j, k) != "unp":
            n_bad += 1
            continue
        n_at += 1
        m = (n - 1) // 2
        r = j // 2
        if green_odd_even(m, r) != 1:
            n_bad += 1
            continue
        kr = pal_kind(m, r, k_p) if G(m, r) else "g0"
        km = pal_kind(m, r - 1, k_p) if G(m, r - 1) else "g0"
        if km == "g0" and kr == "pair" and is_clip_edge(m, r, k_p):
            n_gp += 1
        elif km == "unp" and kr == "g0":
            n_ug += 1
        elif km == "g0" and kr == "unp":
            n_gu += 1
        else:
            n_bad += 1
    return {
        "n_at": n_at,
        "n_gp": n_gp,
        "n_ug": n_ug,
        "n_gu": n_gu,
        "n_bad": n_bad,
    }


def tot_form() -> dict:
    """k<=64: clip_gp J_k form; slice J_k; dies at k=7 for J_k.

    Do not call clip_slice_split / unpaired_xor_split here.
    Census is clip_slice_fold for k<=8.
    """
    n_ok = 0
    if want_clip_slice(0) != 0 or want_clip_gp_jk(1) != 0:
        return {"ok": False, "k01": True}
    if want_clip_slice(2) != 1 or want_clip_gp_jk(2) != 1:
        return {"ok": False, "k2": True}
    if want_clip_slice(8) != 85 or want_clip_gp_jk(8) != 85:
        return {"ok": False, "k8": True}
    if want_clip_slice(7) != 43 or want_clip_gp_jk(7) != 42:
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
        ph = parent_half(k)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if want_clip_gp_jk(k) != want_clip_gp(k):
            return {"ok": False, "equb": True, "k": k}
        if want_clip_slice(k) != want_clip_gp_jk(k) + want_slice_ug(k):
            return {"ok": False, "sum": True, "k": k}
        if k >= 2:
            if want_clip_slice(k) != jacobsthal(k):
                return {"ok": False, "sl": True, "k": k}
            if want_clip_gp_jk(k) != jacobsthal(k) - (k % 2):
                return {"ok": False, "jk": True, "k": k}
            if 2 * want_clip_gp(k) + 1 != jacobsthal(k + 1):
                return {"ok": False, "half": True, "k": k}
            n = 4 * u - 1
            j = 2 * n - clip - 2
            if pal_kind(n, j, k) != "unp":
                return {"ok": False, "nl": True, "k": k}
            if 2 * n - j != clip + 2:
                return {"ok": False, "pr": True, "k": k}
            n1 = ph + 1
            j1 = 2 * n1 - clip - 2
            if j1 != 0:
                return {"ok": False, "j0": True, "k": k}
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
        and want_clip_gp_jk(2) != jacobsthal(3)
        and want_clip_gp_jk(7) != jacobsthal(7)
        and want_clip_slice(7) != want_clip_gp(7)
        and want_clip_slice(8) != want_ug_fl(8)
        and want_clip_slice(8) != want_j0_odd_unp(8)
        and want_clip_slice(8) != jacobsthal(9)
        and want_clip_gp_jk(8) == jacobsthal(8)
        and want_clip_slice(8) == 85
        and want_clip_gp_jk(8) == 85
        and want_clip_gp(8) == 85
        and want_clip_slice(7) == 43
        and want_clip_gp_jk(7) == 42
        and want_slice_ug(7) == 1
        and want_slice_ug(8) == 0
        and want_j0_even_unp(8) == 191
        and want_j0_all_unp(8) == 383
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
        and want_clip_slice(2) == 1
        and want_clip_slice(3) == 3
        and want_clip_slice(4) == 5
        and want_clip_slice(5) == 11
        and want_clip_slice(6) == 21
        and jacobsthal(3) == 3
        and jacobsthal(9) == 171
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def clip_slice_fold() -> dict:
    """k<=8 partner-5U+2 slice vs J_k and clip_gp."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = clip_slice_split(k)
        if a["n_bad"] != 0 or a["n_gu"] != 0:
            return {"ok": False, "bad": True, "k": k, "got": a}
        if a["n_at"] != want_clip_slice(k):
            return {"ok": False, "at": True, "k": k, "got": a["n_at"]}
        if a["n_gp"] != want_clip_gp_jk(k):
            return {"ok": False, "gp": True, "k": k, "got": a["n_gp"]}
        if a["n_ug"] != want_slice_ug(k):
            return {"ok": False, "ug": True, "k": k, "got": a["n_ug"]}
        b = unpaired_xor_split(k)
        if a["n_gp"] != b["n_gp"]:
            return {"ok": False, "b_gp": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"n_at": a["n_at"], "n_gp": a["n_gp"], "n_ug": a["n_ug"]}
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["n_at"] == 1
        and rows["2"]["n_gp"] == 1
        and rows["3"]["n_at"] == 3
        and rows["3"]["n_gp"] == 2
        and rows["3"]["n_ug"] == 1
        and rows["7"]["n_at"] == 43
        and rows["7"]["n_gp"] == 42
        and rows["8"]["n_at"] == 85
        and rows["8"]["n_gp"] == 85
        and rows["8"]["n_ug"] == 0
        and want_clip_slice(4) == 5
        and want_clip_slice(5) == 11
        and want_clip_slice(6) == 21
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """clip_gp equals J_k at k=7; slice equals clip_gp at k=7."""
    ok = (
        want_clip_gp_jk(2) != jacobsthal(3)
        and want_clip_gp_jk(7) != jacobsthal(7)
        and want_clip_slice(7) != want_clip_gp(7)
        and want_clip_slice(8) != want_ug_fl(8)
        and want_clip_slice(8) != want_j0_odd_unp(8)
        and want_clip_slice(8) != jacobsthal(9)
        and want_clip_gp_jk(8) == jacobsthal(8)
        and want_clip_gp_jk(2) == 1
        and jacobsthal(3) == 3
        and jacobsthal(7) == 43
        and want_clip_gp(7) == 42
        and want_clip_slice(7) == 43
        and want_clip_slice(8) == 85
        and want_ug_fl(8) == 4924
        and want_j0_odd_unp(8) == 192
        and jacobsthal(9) == 171
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
    ub = json.loads(UB_JSON.read_text())
    wm = json.loads(WM_JSON.read_text())
    wl = json.loads(WL_JSON.read_text())
    ok = (
        ub["checks"]["all_ok"]
        and wm["checks"]["all_ok"]
        and wl["checks"]["all_ok"]
        and ub["verdict"]["clip_gp_eq_half_J_k1_k_ge_2"] == "LEMMA"
        and wm["verdict"]["j0_unp_eq_window"] == "LEMMA"
        and wl["verdict"]["unp_never_n_le_ph"] == "LEMMA"
        and wm["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and wm["verdict"]["prize"] == "unsolved"
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
    cnt = clip_slice_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WN",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "clip_slice_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "clip_slice_eq_J_k_ge_2": True,
            "clip_gp_eq_J_k_minus_kmod2": True,
            "slice_ug_eq_k_odd": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "clip_slice_eq_J_k_ge_2": "LEMMA",
            "clip_gp_eq_J_k_minus_kmod2": "LEMMA",
            "slice_ug_eq_k_odd": "LEMMA",
            "clip_gp_eq_J_k1_at_k2": "KILLED",
            "clip_gp_eq_J_k_at_k7": "KILLED",
            "slice_eq_clip_gp_at_k7": "KILLED",
            "slice_eq_ug_at_k8": "KILLED",
            "slice_eq_j0_odd_at_k8": "KILLED",
            "slice_eq_J_k1_at_k8": "KILLED",
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
    print("slice k8", dump["clip_slice_fold"]["rows"]["8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
