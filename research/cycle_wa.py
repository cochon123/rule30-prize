#!/usr/bin/env python3
"""Cycle WA: leftover xor n_pg/n_gp F/L closed forms.

n_pg is (2^{k-2}(75 F_{k-1}+39 L_{k-1}-60)+6)/15 for k>=2.
n_gp is (2^{k-2}(75 F_{k-1}+39 L_{k-1}-95)+5(-1)^k+6)/15 for k>=2.
They sum to Cycle VP xor_lo. Equal leftover extra xor n_pg/n_gp at
k+1. Dies at k=2 for both F/L forms with shift 0 (pg got 0, not 4;
gp got 0, not 2). Dies at k=8 without +6 (pg got 8729, not 8730;
gp got 8580, not 8581) and without gp 5(-1)^k (got 8580, not
8581). Do not kill without that sign at k=7: floor-div masks it.
Dies at k=8 for pg equals tot (got 8730, not 17311) and for pg
equals leftover-parent xor (got 8730, not 8560). Census k=8: pg
8730, gp 8581. Do not PREFIX pal-center tot. Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_wa.py --certify
Dump: research/cycle_wa.json
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
from cycle_tw import leftover_xor_split, want_j0_odd_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_ui import want_pg_minus_gp
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vg import want_gp, want_pg
from cycle_vp import want_xor_lo_fl
from cycle_vx import want_gp_lo_fl, want_pg_lo_fl
from cycle_vz import want_ej_xor_gp_fl, want_ej_xor_pg_fl
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VZ_JSON = Path(__file__).resolve().parent / "cycle_vz.json"
VG_JSON = Path(__file__).resolve().parent / "cycle_vg.json"
VP_JSON = Path(__file__).resolve().parent / "cycle_vp.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_xor_pg_fl(k: int) -> int:
    """leftover xor n_pg: F/L form for k>=2; 1 at k=1; 0 at k<=0."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    n = (1 << (k - 2)) * (75 * fib(k - 1) + 39 * lucas(k - 1) - 60) + 6
    return n // 15


def want_xor_gp_fl(k: int) -> int:
    """leftover xor n_gp: F/L form for k>=2; 0 at k<=1."""
    if k <= 1:
        return 0
    n = (
        (1 << (k - 2)) * (75 * fib(k - 1) + 39 * lucas(k - 1) - 95)
        + 5 * ((-1) ** k)
        + 6
    )
    return n // 15


def tot_form() -> dict:
    """k<=64: leftover xor n_pg/n_gp F/L; dies at k=2 with shift 0.

    Do not call leftover_xor_split / leftover_extra_xor_split here.
    Census is xor_pg_fold for k<=8.
    """
    n_ok = 0
    raw_pg2 = 6 // 15
    raw_gp2 = (5 * ((-1) ** 2) + 6) // 15
    miss_pg6 = ((1 << 6) * (75 * fib(7) + 39 * lucas(7) - 60)) // 15
    miss_gp6 = (
        (1 << 6) * (75 * fib(7) + 39 * lucas(7) - 95) + 5 * ((-1) ** 8)
    ) // 15
    miss_gsign8 = ((1 << 6) * (75 * fib(7) + 39 * lucas(7) - 95) + 6) // 15
    miss_gsign7 = ((1 << 5) * (75 * fib(6) + 39 * lucas(6) - 95) + 6) // 15
    if want_xor_pg_fl(0) != 0 or want_xor_pg_fl(1) != 1:
        return {"ok": False, "k01": True}
    if want_xor_pg_fl(2) != 4 or want_xor_gp_fl(2) != 2:
        return {"ok": False, "k2": True}
    if want_xor_pg_fl(8) != 8730 or want_xor_gp_fl(8) != 8581:
        return {"ok": False, "k8": True}
    if want_xor_pg_fl(2) == raw_pg2:
        return {"ok": False, "k2p": True}
    if want_xor_gp_fl(2) == raw_gp2:
        return {"ok": False, "k2g": True}
    if want_xor_pg_fl(8) == miss_pg6:
        return {"ok": False, "p6": True}
    if want_xor_gp_fl(8) == miss_gp6:
        return {"ok": False, "g6": True}
    if want_xor_gp_fl(8) == miss_gsign8:
        return {"ok": False, "g8": True}
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
        if want_xor_pg_fl(k) != want_pg(k):
            return {"ok": False, "pg": True, "k": k}
        if want_xor_gp_fl(k) != want_gp(k):
            return {"ok": False, "gp": True, "k": k}
        if want_xor_pg_fl(k) + want_xor_gp_fl(k) != want_xor_lo_fl(k):
            return {"ok": False, "sum": True, "k": k}
        if want_xor_pg_fl(k) - want_xor_gp_fl(k) != want_pg_minus_gp(k):
            return {"ok": False, "diff": True, "k": k}
        if k >= 1 and want_ej_xor_pg_fl(k) != want_xor_pg_fl(k - 1):
            return {"ok": False, "ejp": True, "k": k}
        if k >= 1 and want_ej_xor_gp_fl(k) != want_xor_gp_fl(k - 1):
            return {"ok": False, "ejg": True, "k": k}
        if k >= 2:
            np = (
                (1 << (k - 2)) * (75 * fib(k - 1) + 39 * lucas(k - 1) - 60)
                + 6
            )
            ng = (
                (1 << (k - 2)) * (75 * fib(k - 1) + 39 * lucas(k - 1) - 95)
                + 5 * ((-1) ** k)
                + 6
            )
            if np % 15 != 0 or np // 15 != want_xor_pg_fl(k):
                return {"ok": False, "dp": True, "k": k}
            if ng % 15 != 0 or ng // 15 != want_xor_gp_fl(k):
                return {"ok": False, "dg": True, "k": k}
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
        and want_xor_pg_fl(2) != raw_pg2
        and want_xor_gp_fl(2) != raw_gp2
        and want_xor_pg_fl(8) != miss_pg6
        and want_xor_gp_fl(8) != miss_gp6
        and want_xor_gp_fl(8) != miss_gsign8
        and want_xor_gp_fl(7) == miss_gsign7
        and want_xor_pg_fl(8) != want_xor_lo_fl(8)
        and want_xor_pg_fl(8) != want_pg_lo_fl(8)
        and want_xor_pg_fl(8) != want_ej_xor_pg_fl(8)
        and want_xor_pg_fl(8) != want_xor_gp_fl(8)
        and want_xor_pg_fl(8) == 8730
        and want_xor_gp_fl(8) == 8581
        and want_xor_lo_fl(8) == 17311
        and want_ej_xor(8) == 5225
        and want_j0_odd_lo(8) == 319
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
        and miss_pg6 == 8729
        and miss_gp6 == 8580
        and miss_gsign8 == 8580
        and miss_gsign7 == 2575
        and raw_pg2 == 0
        and raw_gp2 == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def xor_pg_fold() -> dict:
    """k<=8 leftover xor n_pg/n_gp vs F/L closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = leftover_xor_split(k)
        if r["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if r["n_pg"] != want_xor_pg_fl(k):
            return {"ok": False, "pg": True, "k": k, "got": r["n_pg"]}
        if r["n_gp"] != want_xor_gp_fl(k):
            return {"ok": False, "gp": True, "k": k, "got": r["n_gp"]}
        if r["n_pg"] + r["n_gp"] != want_xor_lo_fl(k):
            return {"ok": False, "tot": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"n_pg": r["n_pg"], "n_gp": r["n_gp"]}
    ok = (
        n_ok == K_COUNT + 1
        and rows["1"]["n_pg"] == 1
        and rows["1"]["n_gp"] == 0
        and rows["2"]["n_pg"] == 4
        and rows["2"]["n_gp"] == 2
        and rows["3"]["n_pg"] == 18
        and rows["3"]["n_gp"] == 13
        and rows["8"]["n_pg"] == 8730
        and rows["8"]["n_gp"] == 8581
        and want_xor_pg_fl(4) == 66
        and want_xor_gp_fl(5) == 215
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """F/L forms at k=2 with shift 0; +6 and gp sign at k=8."""
    raw_pg2 = 6 // 15
    raw_gp2 = (5 * ((-1) ** 2) + 6) // 15
    miss_pg6 = ((1 << 6) * (75 * fib(7) + 39 * lucas(7) - 60)) // 15
    miss_gp6 = (
        (1 << 6) * (75 * fib(7) + 39 * lucas(7) - 95) + 5 * ((-1) ** 8)
    ) // 15
    miss_gsign8 = ((1 << 6) * (75 * fib(7) + 39 * lucas(7) - 95) + 6) // 15
    miss_gsign7 = ((1 << 5) * (75 * fib(6) + 39 * lucas(6) - 95) + 6) // 15
    r8 = leftover_xor_split(8)
    ok = (
        want_xor_pg_fl(2) != raw_pg2
        and want_xor_gp_fl(2) != raw_gp2
        and want_xor_pg_fl(8) != miss_pg6
        and want_xor_gp_fl(8) != miss_gp6
        and want_xor_gp_fl(8) != miss_gsign8
        and want_xor_gp_fl(7) == miss_gsign7
        and want_xor_pg_fl(8) != want_xor_lo_fl(8)
        and want_xor_pg_fl(8) != want_pg_lo_fl(8)
        and want_xor_gp_fl(8) != want_gp_lo_fl(8)
        and want_xor_pg_fl(8) != want_ej_xor_pg_fl(8)
        and r8["n_pg"] == 8730
        and r8["n_gp"] == 8581
        and raw_pg2 == 0
        and raw_gp2 == 0
        and miss_pg6 == 8729
        and miss_gp6 == 8580
        and miss_gsign8 == 8580
        and miss_gsign7 == 2575
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
    vz = json.loads(VZ_JSON.read_text())
    vg = json.loads(VG_JSON.read_text())
    vp = json.loads(VP_JSON.read_text())
    ok = (
        vz["checks"]["all_ok"]
        and vg["checks"]["all_ok"]
        and vp["checks"]["all_ok"]
        and vz["verdict"]["ej_xor_pg_eq_FL_closed_k_ge_3"] == "LEMMA"
        and vg["verdict"]["leftover_pg_eq_xor_lo_plus_UI_over_2"] == "LEMMA"
        and vp["verdict"]["xor_lo_eq_FL_closed_k_ge_2"] == "LEMMA"
        and vz["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vz["verdict"]["prize"] == "unsolved"
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
    cnt = xor_pg_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "WA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "xor_pg_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "xor_pg_eq_FL_closed_k_ge_2": True,
            "xor_gp_eq_FL_closed_k_ge_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "xor_pg_eq_FL_closed_k_ge_2": "LEMMA",
            "xor_gp_eq_FL_closed_k_ge_2": "LEMMA",
            "xor_pg_FL_shift0_at_k2": "KILLED",
            "xor_gp_FL_shift0_at_k2": "KILLED",
            "xor_pg_without_plus6_at_k8": "KILLED",
            "xor_gp_without_plus6_at_k8": "KILLED",
            "xor_gp_without_sign_at_k8": "KILLED",
            "xor_pg_eq_xor_lo": "KILLED",
            "xor_pg_eq_pg_lo": "KILLED",
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
        "pg/gp k8",
        dump["xor_pg_fold"]["rows"]["8"]["n_pg"],
        dump["xor_pg_fold"]["rows"]["8"]["n_gp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
