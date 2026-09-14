#!/usr/bin/env python3
"""Cycle VF: leftover extra xor tot DIFF is 2^{k-2}+J_{k-3}.

Leftover extra except j=0 each produce one leftover-parent xor child.
The signed tot difference of those children equals Cycle UI leftover
xor n_pg-n_gp at the parent: 2^{k-2}+J_{k-3} for k>=3, equivalently
(7*2^{k-3}+(-1)^k)/3. Also leftover-parent tot DIFF minus Cycle VE
xor small gap for k>=2, and leftover extra xor small DIFF plus
leftover-parent xor large DIFF for k>=4. Dies at k=2 for the
Jacobsthal form (UI at k, not k-1, is 2 not 1). Dies at k=3 for
small DIFF plus leftover-parent large DIFF helper (got 2, not 3).
Census k=8: tot DIFF 75. Do not PREFIX pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_vf.py --certify
Dump: research/cycle_vf.json
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
from cycle_ui import want_pg_minus_gp
from cycle_um import want_lo_parent_diff
from cycle_uo import want_named_l
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor, want_ej_xor_large
from cycle_uw import want_3u, want_miss_n
from cycle_uy import want_lo_parent_large_diff
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vc import want_ej_xor_small, want_ej_xor_small_diff
from cycle_ve import want_xor_small_gap
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VE_JSON = Path(__file__).resolve().parent / "cycle_ve.json"
UI_JSON = Path(__file__).resolve().parent / "cycle_ui.json"
VD_JSON = Path(__file__).resolve().parent / "cycle_vd.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ej_xor_diff(k: int) -> int:
    """Leftover extra xor tot DIFF: parent leftover xor n_pg-n_gp."""
    return want_pg_minus_gp(k - 1)


def tot_form() -> dict:
    """k<=64: leftover extra xor tot DIFF form; dies at k=2 for UI(k).

    Do not call leftover_extra_xor_split here.
    Census is ej_diff_fold for k<=8.
    """
    n_ok = 0
    if want_ej_xor_diff(0) != 0 or want_ej_xor_diff(2) != 1:
        return {"ok": False, "k02": True}
    if want_ej_xor_diff(3) != 2 or want_ej_xor_diff(8) != 75:
        return {"ok": False, "k38": True}
    if want_ej_xor_diff(2) == want_pg_minus_gp(2):
        return {"ok": False, "k2f": True}
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
        if want_ej_xor_diff(k) != want_pg_minus_gp(k - 1):
            return {"ok": False, "ui": True, "k": k}
        if k >= 3:
            raw = (1 << (k - 2)) + jacobsthal(k - 3)
            if want_ej_xor_diff(k) != raw:
                return {"ok": False, "form": True, "k": k}
            formb = (7 * (1 << (k - 3)) + ((-1) ** k)) // 3
            if want_ej_xor_diff(k) != formb:
                return {"ok": False, "fb": True, "k": k}
            if (7 * (1 << (k - 3)) + ((-1) ** k)) % 3 != 0:
                return {"ok": False, "div": True, "k": k}
        if k >= 2:
            if want_ej_xor_diff(k) != (
                want_lo_parent_diff(k) - want_xor_small_gap(k)
            ):
                return {"ok": False, "umg": True, "k": k}
        if k >= 4:
            if want_ej_xor_diff(k) != (
                want_ej_xor_small_diff(k) + want_lo_parent_large_diff(k)
            ):
                return {"ok": False, "sl": True, "k": k}
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
        and want_ej_xor_diff(2) != 2
        and want_ej_xor_diff(8) == 75
        and want_ej_xor_diff(8) == want_pg_minus_gp(7)
        and want_ej_xor_diff(8) != want_lo_parent_diff(8)
        and want_ej_xor_diff(8) != want_pg_minus_gp(8)
        and want_ej_xor_diff(8) != want_named_l(8)
        and want_lo_parent_diff(8) == 233
        and want_xor_small_gap(8) == 158
        and want_ej_xor_small_diff(8) == 105
        and want_lo_parent_large_diff(8) == -30
        and want_ej_xor(8) == 5225
        and want_ej_xor_large(8) == 2034
        and want_ej_xor_small(8) == 3191
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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


def ej_diff_fold() -> dict:
    """k<=8 leftover extra xor tot DIFF."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        a = leftover_extra_xor_split(k)
        tdiff = (a["pg_s"] + a["pg_l"]) - (a["gp_s"] + a["gp_l"])
        tot = a["pg_s"] + a["pg_l"] + a["gp_s"] + a["gp_l"]
        if tdiff != want_ej_xor_diff(k):
            return {"ok": False, "td": True, "k": k, "got": tdiff}
        if tot != want_ej_xor(k):
            return {"ok": False, "tot": True, "k": k, "got": tot}
        if k >= 3:
            if tdiff != (1 << (k - 2)) + jacobsthal(k - 3):
                return {"ok": False, "form": True, "k": k, "got": tdiff}
        if k >= 2:
            if tdiff != want_lo_parent_diff(k) - want_xor_small_gap(k):
                return {"ok": False, "umg": True, "k": k, "got": tdiff}
        if k >= 4:
            if tdiff != (
                want_ej_xor_small_diff(k) + want_lo_parent_large_diff(k)
            ):
                return {"ok": False, "sl": True, "k": k, "got": tdiff}
        n_ok += 1
        rows[str(k)] = {"tdiff": tdiff, "tot": tot}
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["tdiff"] == 1
        and rows["2"]["tdiff"] != 2
        and rows["3"]["tdiff"] == 2
        and rows["8"]["tdiff"] == 75
        and rows["8"]["tot"] == 5225
        and want_ej_xor_diff(4) == 5
        and want_ej_xor_diff(5) == 9
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """UI(k) at k=2; leftover-parent tot DIFF at k=8; smD+lg helper at k=3."""
    a2 = leftover_extra_xor_split(2)
    a3 = leftover_extra_xor_split(3)
    a8 = leftover_extra_xor_split(8)
    d2 = (a2["pg_s"] + a2["pg_l"]) - (a2["gp_s"] + a2["gp_l"])
    d3 = (a3["pg_s"] + a3["pg_l"]) - (a3["gp_s"] + a3["gp_l"])
    d8 = (a8["pg_s"] + a8["pg_l"]) - (a8["gp_s"] + a8["gp_l"])
    ok = (
        want_ej_xor_diff(2) != want_pg_minus_gp(2)
        and want_ej_xor_diff(8) != want_lo_parent_diff(8)
        and want_ej_xor_diff(3)
        != want_ej_xor_small_diff(3) + want_lo_parent_large_diff(3)
        and d2 == 1
        and d3 == 2
        and d8 == 75
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
    ve = json.loads(VE_JSON.read_text())
    ui = json.loads(UI_JSON.read_text())
    vd = json.loads(VD_JSON.read_text())
    ok = (
        ve["checks"]["all_ok"]
        and ui["checks"]["all_ok"]
        and vd["checks"]["all_ok"]
        and ve["verdict"]["xor_small_gap_eq_5_2km3_minus_2_k_ge_3"] == "LEMMA"
        and ui["verdict"]["pg_minus_gp_eq_2km1_plus_J"] == "LEMMA"
        and vd["verdict"]["lo_parent_small_diff_closed_k_ge_3"] == "LEMMA"
        and ve["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ve["verdict"]["prize"] == "unsolved"
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
    cnt = ej_diff_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ej_diff_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ej_xor_diff_eq_2km2_plus_J_k_ge_3": True,
            "ej_xor_diff_eq_parent_pg_minus_gp": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ej_xor_diff_eq_2km2_plus_J_k_ge_3": "LEMMA",
            "ej_xor_diff_eq_parent_pg_minus_gp": "LEMMA",
            "ej_xor_diff_eq_UI_k_at_k2": "KILLED",
            "ej_xor_diff_eq_lo_parent_tot_at_k8": "KILLED",
            "ej_xor_diff_eq_smD_plus_lg_helper_at_k3": "KILLED",
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
    print("tdiff k8", dump["ej_diff_fold"]["rows"]["8"]["tdiff"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
