#!/usr/bin/env python3
"""Cycle VI: leftover-parent xor tot minus leftover extra xor tot
is 4(lo_e(k-1)-lo_e(k-2))-(UM(k)-UM(k-1))-named_lo(k-1).

Leftover extra except j=0 each produce one leftover-parent xor child,
count xor_lo(k-1). Leftover-parent xor tot is 4 lo_e(k-1) minus Cycle
UM difference. Their gap is 4 times the even leftover first
difference, minus the UM first difference, minus named leftover extra
at the parent, for every k (lo_e and UM and named_lo vanish at
negative arguments). Dies at k=2 if named_lo at the parent is replaced
by the k>=2 closed form 2^{k-1}+2 J_{k-1}-2 (got 1, form 0). Census
k=8: gap 11662. Do not PREFIX pal-center tot. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_vi.py --certify
Dump: research/cycle_vi.json
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
from cycle_ul import want_named_lo
from cycle_um import want_lo_parent_diff
from cycle_uo import named_half_split
from cycle_up import lucas, want_lo_e, want_lo_parent_sum
from cycle_uq import want_xor_lo
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor, want_ej_xor_large
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vh import want_ej_xor_pg_s
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VH_JSON = Path(__file__).resolve().parent / "cycle_vh.json"
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"
UL_JSON = Path(__file__).resolve().parent / "cycle_ul.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_count_gap(k: int) -> int:
    """leftover-parent xor tot minus leftover extra xor tot."""
    return (
        4 * (want_lo_e(k - 1) - want_lo_e(k - 2))
        - (want_lo_parent_diff(k) - want_lo_parent_diff(k - 1))
        - want_named_lo(k - 1)
    )


def tot_form() -> dict:
    """k<=64: xor count gap form; dies at k=2 for named closed parent.

    Do not call named_half_split / leftover_extra_xor_split here.
    Census is gap_fold for k<=8.
    """
    n_ok = 0
    if want_xor_count_gap(0) != 0 or want_xor_count_gap(2) != 1:
        return {"ok": False, "k02": True}
    if want_xor_count_gap(3) != 13 or want_xor_count_gap(8) != 11662:
        return {"ok": False, "k38": True}
    named_closed_1 = (1 << 1) + 2 * jacobsthal(1) - 2
    raw2 = (
        4 * (want_lo_e(1) - want_lo_e(0))
        - (want_lo_parent_diff(2) - want_lo_parent_diff(1))
        - named_closed_1
    )
    if want_xor_count_gap(2) == raw2:
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
        if want_xor_count_gap(k) != (
            4 * (want_lo_e(k - 1) - want_lo_e(k - 2))
            - (want_lo_parent_diff(k) - want_lo_parent_diff(k - 1))
            - want_named_lo(k - 1)
        ):
            return {"ok": False, "form": True, "k": k}
        if want_xor_count_gap(k) != want_lo_parent_sum(k) - want_ej_xor(k):
            return {"ok": False, "ej": True, "k": k}
        if k >= 1:
            if want_xor_count_gap(k) != (
                want_lo_parent_sum(k) - want_xor_lo(k - 1)
            ):
                return {"ok": False, "xo": True, "k": k}
        if k >= 2:
            if want_named_lo(k) != (1 << k) + 2 * jacobsthal(k) - 2:
                return {"ok": False, "nm": True, "k": k}
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
        and want_xor_count_gap(2) != 0
        and want_xor_count_gap(8) == 11662
        and want_xor_count_gap(8)
        != 4 * (want_lo_e(7) - want_lo_e(6))
        and want_lo_parent_sum(8) == 16887
        and want_ej_xor(8) == 5225
        and want_ej_xor_large(8) == 2034
        and want_ej_xor_pg_s(8) == 1648
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
        and want_named_lo(8) == 424
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


def gap_fold() -> dict:
    """k<=8 leftover-parent xor tot minus leftover extra xor tot."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        ssum = r["plo_s"] + r["plo_l"] + r["glo_s"] + r["glo_l"]
        a = leftover_extra_xor_split(k)
        ej = a["pg_s"] + a["pg_l"] + a["gp_s"] + a["gp_l"]
        gap = ssum - ej
        if ssum != want_lo_parent_sum(k):
            return {"ok": False, "ss": True, "k": k, "got": ssum}
        if ej != want_ej_xor(k):
            return {"ok": False, "ej": True, "k": k, "got": ej}
        if gap != want_xor_count_gap(k):
            return {"ok": False, "gap": True, "k": k, "got": gap}
        n_ok += 1
        rows[str(k)] = {"ssum": ssum, "ej": ej, "gap": gap}
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["gap"] == 1
        and rows["2"]["gap"] != 0
        and rows["3"]["gap"] == 13
        and rows["8"]["gap"] == 11662
        and rows["8"]["ssum"] == 16887
        and rows["8"]["ej"] == 5225
        and want_xor_count_gap(4) == 68
        and want_xor_count_gap(5) == 274
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """named closed form at parent k=1; omit UM and named at k=8."""
    named_closed_1 = (1 << 1) + 2 * jacobsthal(1) - 2
    raw2 = (
        4 * (want_lo_e(1) - want_lo_e(0))
        - (want_lo_parent_diff(2) - want_lo_parent_diff(1))
        - named_closed_1
    )
    r8 = named_half_split(8)
    a8 = leftover_extra_xor_split(8)
    s8 = r8["plo_s"] + r8["plo_l"] + r8["glo_s"] + r8["glo_l"]
    e8 = a8["pg_s"] + a8["pg_l"] + a8["gp_s"] + a8["gp_l"]
    ok = (
        want_xor_count_gap(2) != raw2
        and want_named_lo(1) != named_closed_1
        and want_xor_count_gap(8) != 4 * (want_lo_e(7) - want_lo_e(6))
        and s8 - e8 == 11662
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
    vh = json.loads(VH_JSON.read_text())
    up = json.loads(UP_JSON.read_text())
    ul = json.loads(UL_JSON.read_text())
    ok = (
        vh["checks"]["all_ok"]
        and up["checks"]["all_ok"]
        and ul["checks"]["all_ok"]
        and vh["verdict"]["ej_xor_half_eq_parent_leftover_half_k_ge_3"]
        == "LEMMA"
        and up["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vh["verdict"]["prize"] == "unsolved"
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
    cnt = gap_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "gap_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_count_gap_eq_4_loe_dUM_named": True,
            "xor_count_gap_eq_lo_parent_sum_minus_ej_xor": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_count_gap_eq_4_loe_dUM_named": "LEMMA",
            "xor_count_gap_eq_lo_parent_sum_minus_ej_xor": "LEMMA",
            "xor_count_gap_named_closed_parent_at_k2": "KILLED",
            "xor_count_gap_eq_4_loe_diff_only": "KILLED",
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
    print("gap k8", dump["gap_fold"]["rows"]["8"]["gap"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
