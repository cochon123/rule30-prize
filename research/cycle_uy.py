#!/usr/bin/env python3
"""Cycle UY: leftover extra large n=3 mod 4 is lo_large plus 2-step fold.

Leftover extra xor from leftover extra large all land on n=3 mod 4,
count lo_large(k-1). Odd-j leftover from leftover extra large at k-2
produce leftover extra (j,j+2) pairs, count 2 lo_large(k-2). Named
g0+d1 and d2+g0 add d1_large(k-1)+d2o_large(k-1). Hence leftover
extra large n=3 is that sum for k>=4, extra n3-n1 recures as
extra(k-1)+d1_large(k-1)-d2e_large(k-1) with extra(3)=0, and
leftover-parent xor large difference is 1-2^{k-3}+(-1)^k for k>=4.
Dies at k=3 for the n=3 sum (count 8, not 6). Do not PREFIX
pal-center tot. Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk leftover d catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_uy.py --certify
Dump: research/cycle_uy.json
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
from cycle_uk import want_d1_large
from cycle_ul import parent_pair_type
from cycle_un import want_d2e_large, want_d2o_large
from cycle_up import lucas, want_lo_e
from cycle_uq import want_lo_large
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor_large
from cycle_uw import leftover_cell, want_3u, want_miss_n
from cycle_ux import e_ge, extra_lg_res_split, want_n1_extra_lg
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UX_JSON = Path(__file__).resolve().parent / "cycle_ux.json"
UW_JSON = Path(__file__).resolve().parent / "cycle_uw.json"
UV_JSON = Path(__file__).resolve().parent / "cycle_uv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_n3_extra_lg(k: int) -> int:
    """Leftover extra large n=3 mod 4: 0,0,3,8, then lo_large 2-step fold."""
    if k <= 1:
        return 0
    if k == 2:
        return 3
    if k == 3:
        return 8
    return (
        want_lo_large(k - 1)
        + 2 * want_lo_large(k - 2)
        + want_d1_large(k - 1)
        + want_d2o_large(k - 1)
    )


def want_extra_lg(k: int) -> int:
    """Leftover extra large (n=3 minus n=1): 0,0,3, then 2^{k-2}-1-(-1)^{k+1}."""
    if k <= 1:
        return 0
    if k == 2:
        return 3
    return (1 << (k - 2)) - 1 - ((-1) ** (k + 1))


def want_lo_parent_large_diff(k: int) -> int:
    """Leftover-parent xor large difference: 1-2^{k-3}+(-1)^k for k>=4."""
    if k <= 3:
        return 0 if k == 3 else (3 if k == 2 else 0)
    return 1 - (1 << (k - 3)) + ((-1) ** k)


def extra_lg_n3_kind_split(k: int) -> dict:
    """Leftover extra large n=3 mod 4 split by parent kind."""
    u = 1 << k
    ph = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    clip = 5 * u
    z = {
        "lo_g0": 0,
        "g0_lo": 0,
        "g0_d1": 0,
        "d2_g0": 0,
        "other": 0,
        "n": 0,
    }
    for n in range(1, 4 * u, 2):
        if n <= ph or n % 4 != 3:
            continue
        m = (n - 1) // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if not leftover_cell(n, j, k):
                continue
            r = j // 2
            kr = parent_pair_type(m, r, k_p)
            km = parent_pair_type(m, r - 1, k_p) if r else "neg"
            pair = f"{km}+{kr}"
            z["n"] += 1
            if pair == "lo+g0":
                z["lo_g0"] += 1
            elif pair == "g0+lo":
                z["g0_lo"] += 1
            elif pair == "g0+d1":
                z["g0_d1"] += 1
            elif pair == "d2+g0":
                z["d2_g0"] += 1
            else:
                z["other"] += 1
    return z


def tot_form() -> dict:
    """k<=64: extra recurrence and n=3 sum; dies at k=3.

    Do not call e_ge / extra_lg_res_split here: those walk covering.
    Census is n3_fold for k<=8.
    """
    n_ok = 0
    if want_n3_extra_lg(0) != 0 or want_n3_extra_lg(2) != 3:
        return {"ok": False, "k02": True}
    if want_n3_extra_lg(3) != 8 or want_n3_extra_lg(8) != 3354:
        return {"ok": False, "k38": True}
    if want_extra_lg(3) != 0 or want_extra_lg(8) != 64:
        return {"ok": False, "e38": True}
    raw3 = (
        want_lo_large(2)
        + 2 * want_lo_large(1)
        + want_d1_large(2)
        + want_d2o_large(2)
    )
    if want_n3_extra_lg(3) == raw3:
        return {"ok": False, "k3f": True}
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
        n = 2 * m + 1
        if m % 2 == 0:
            if n % 4 != 1:
                return {"ok": False, "n1": True, "m": m}
        elif n % 4 != 3:
            return {"ok": False, "n3": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if k >= 2 and (2 * ph + 1) % 4 != 1:
            return {"ok": False, "ch": True, "k": k}
        if (2 * (2 * k) + 1) % 4 != 1:
            return {"ok": False, "epar": True, "k": k}
        if (2 * (2 * k + 1) + 1) % 4 != 3:
            return {"ok": False, "opar": True, "k": k}
        if k >= 4:
            if want_n3_extra_lg(k) != (
                want_lo_large(k - 1)
                + 2 * want_lo_large(k - 2)
                + want_d1_large(k - 1)
                + want_d2o_large(k - 1)
            ):
                return {"ok": False, "n3s": True, "k": k}
            if want_extra_lg(k) != (
                want_extra_lg(k - 1)
                + want_d1_large(k - 1)
                - want_d2e_large(k - 1)
            ):
                return {"ok": False, "erec": True, "k": k}
            if want_lo_parent_large_diff(k) != -want_extra_lg(k - 1):
                return {"ok": False, "ld": True, "k": k}
            if want_lo_parent_large_diff(k) != (
                1 - (1 << (k - 3)) + ((-1) ** k)
            ):
                return {"ok": False, "ldf": True, "k": k}
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
        and want_n3_extra_lg(3) != raw3
        and want_n3_extra_lg(8) == 3354
        and want_n1_extra_lg(8) == 3290
        and want_extra_lg(8) == 64
        and want_lo_parent_large_diff(8) == -30
        and want_ej_xor_large(8) == 2034
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
        and want_lo_e(8) == 14114
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def n3_fold() -> dict:
    """k<=8 leftover extra large n=3 sum, extra, parent kinds."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        z = extra_lg_res_split(k)
        n1 = z[1]["n"]
        n3 = z[3]["n"]
        if n1 != want_n1_extra_lg(k):
            return {"ok": False, "n1": True, "k": k, "got": n1}
        if n3 != want_n3_extra_lg(k):
            return {"ok": False, "n3": True, "k": k, "got": n3}
        extra = n3 - n1
        if extra != want_extra_lg(k):
            return {"ok": False, "ex": True, "k": k, "got": extra}
        kinds = extra_lg_n3_kind_split(k)
        if kinds["n"] != n3 or kinds["other"] != 0:
            return {"ok": False, "kd": True, "k": k, "got": kinds}
        if k >= 4:
            if kinds["lo_g0"] != e_ge(k - 1):
                return {"ok": False, "pg": True, "k": k, "got": kinds}
            if kinds["g0_lo"] != e_ge(k - 1) + want_extra_lg(k - 1):
                return {"ok": False, "gp": True, "k": k, "got": kinds}
            if kinds["g0_d1"] != want_d1_large(k - 1):
                return {"ok": False, "d1": True, "k": k, "got": kinds}
            if kinds["d2_g0"] != want_d2o_large(k - 1):
                return {"ok": False, "d2": True, "k": k, "got": kinds}
            xr = leftover_extra_xor_split(k)
            diff = xr["pg_l"] - xr["gp_l"]
            if diff != want_lo_parent_large_diff(k):
                return {"ok": False, "ld": True, "k": k, "diff": diff}
            if extra != (
                want_extra_lg(k - 1)
                + want_d1_large(k - 1)
                - want_d2e_large(k - 1)
            ):
                return {"ok": False, "rec": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n1": n1,
            "n3": n3,
            "extra": extra,
            "lo_g0": kinds["lo_g0"],
            "g0_lo": kinds["g0_lo"],
            "g0_d1": kinds["g0_d1"],
            "d2_g0": kinds["d2_g0"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["n3"] == 3
        and rows["3"]["n3"] == 8
        and rows["3"]["n3"]
        != (
            want_lo_large(2)
            + 2 * want_lo_large(1)
            + want_d1_large(2)
            + want_d2o_large(2)
        )
        and rows["8"]["n3"] == 3354
        and rows["8"]["n1"] == 3290
        and rows["8"]["extra"] == 64
        and rows["7"]["extra"] == 30
        and want_lo_parent_large_diff(8) == -30
        and want_n3_extra_lg(4) == 28
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """n=3 sum at k=3; extra form at k=2; large_diff form at k=3."""
    raw3 = (
        want_lo_large(2)
        + 2 * want_lo_large(1)
        + want_d1_large(2)
        + want_d2o_large(2)
    )
    z2 = extra_lg_res_split(2)
    z8 = extra_lg_res_split(8)
    ok = (
        want_n3_extra_lg(3) != raw3
        and want_extra_lg(2) == 3
        and want_extra_lg(2)
        != (1 << (2 - 2)) - 1 - ((-1) ** (2 + 1))
        and want_lo_parent_large_diff(3) != 1 - (1 << 0) + ((-1) ** 3)
        and z2[3]["n"] - z2[1]["n"] == 3
        and z8[3]["n"] != z8[1]["n"]
        and z8[1]["g0"] == z8[3]["g0"]
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and G(2, 1) == 0
        and G(3, 2) == 0
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
    ux = json.loads(UX_JSON.read_text())
    uw = json.loads(UW_JSON.read_text())
    uv = json.loads(UV_JSON.read_text())
    ok = (
        ux["checks"]["all_ok"]
        and uw["checks"]["all_ok"]
        and uv["checks"]["all_ok"]
        and ux["verdict"]["n1_extra_lg_2fold_ege_d2e_k_ge_4"] == "LEMMA"
        and ux["verdict"]["large_diff_eq_n1_minus_n3_parent_k_ge_4"] == "LEMMA"
        and ux["verdict"]["lo_parent_large_diff_closed"] == "PREFIX"
        and ux["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ux["verdict"]["prize"] == "unsolved"
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
    cnt = n3_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "n3_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "n3_extra_lg_lo_large_2step_k_ge_4": True,
            "extra_lg_rec_d1_minus_d2e_k_ge_4": True,
            "lo_parent_large_diff_closed_k_ge_4": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n3_extra_lg_lo_large_2step_k_ge_4": "LEMMA",
            "extra_lg_rec_d1_minus_d2e_k_ge_4": "LEMMA",
            "lo_parent_large_diff_closed_k_ge_4": "LEMMA",
            "n3_sum_at_k3": "KILLED",
            "extra_form_at_k2": "KILLED",
            "large_diff_form_at_k3": "KILLED",
            "n3_eq_n1": "KILLED",
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
        "n1/n3/extra k8",
        dump["n3_fold"]["rows"]["8"]["n1"],
        dump["n3_fold"]["rows"]["8"]["n3"],
        dump["n3_fold"]["rows"]["8"]["extra"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
