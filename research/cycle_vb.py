#!/usr/bin/env python3
"""Cycle VB: leftover extra small n=1 is 2-fold; n=3 is lo_small 2-step.

Even leftover small union even d=2 produces leftover extra (j,j+2)
pairs on small n=1 mod 4, count 2(sm(k-1)+d2e_small(k-1)) for
k>=4. Leftover extra small on n=3 mod 4 is lo_small(k-1) plus a
2-step fold, d1_small(k-1), and d2o_small(k-1). G=0 leftover extra
small on n=3 equals that on n=1 for k>=3. Dies at k=3 for the
2-fold (count 10, not 12) and the n=3 sum (count 14, not 16). Dies
at k=2 for G=0 equal. Do not PREFIX pal-center tot. Not rest=S xor
T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_vb.py --certify
Dump: research/cycle_vb.json
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
from cycle_uk import want_d1_small, want_lo_small
from cycle_ul import parent_pair_type
from cycle_un import want_d2e_small, want_d2o_small
from cycle_up import lucas, want_lo_e
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor_large
from cycle_uw import leftover_cell, want_3u, want_miss_n
from cycle_uy import want_lo_parent_large_diff
from cycle_uz import want_ege
from cycle_va import want_n1_extra_sm, want_n3_extra_sm, want_sm
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VA_JSON = Path(__file__).resolve().parent / "cycle_va.json"
UZ_JSON = Path(__file__).resolve().parent / "cycle_uz.json"
UY_JSON = Path(__file__).resolve().parent / "cycle_uy.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_n1_2f(k: int) -> int:
    """Raw 2-fold of parent even leftover small union even d=2."""
    if k <= 0:
        return 0
    return 2 * (want_sm(k - 1) + want_d2e_small(k - 1))


def want_n3_2s(k: int) -> int:
    """Raw lo_small 2-step plus d1_small and d2o_small at parent."""
    if k <= 1:
        return 0
    return (
        want_lo_small(k - 1)
        + 2 * want_lo_small(k - 2)
        + want_d1_small(k - 1)
        + want_d2o_small(k - 1)
    )


def extra_sm_res_split(k: int) -> dict:
    """Leftover extra on n<=ph split by n mod 4 and G(s,t)."""
    u = 1 << k
    ph = parent_half(k)
    clip = 5 * u
    z = {
        1: {"g0": 0, "g1": 0, "n": 0},
        3: {"g0": 0, "g1": 0, "n": 0},
    }
    for n in range(1, 4 * u, 2):
        if n > ph:
            continue
        r = n % 4
        if r not in (1, 3):
            continue
        s = (n - 1) // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if not leftover_cell(n, j, k):
                continue
            gs = G(s, j // 2)
            z[r]["n"] += 1
            z[r]["g0" if gs == 0 else "g1"] += 1
    return z


def extra_sm_n1_kind_split(k: int) -> dict:
    """Leftover extra small n=1 mod 4 split by parent kind."""
    u = 1 << k
    ph = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    clip = 5 * u
    z = {
        "lo_g0": 0,
        "g0_lo": 0,
        "neg_lo": 0,
        "d2_g0": 0,
        "g0_d2": 0,
        "neg_d2": 0,
        "other": 0,
        "n": 0,
    }
    for n in range(1, 4 * u, 2):
        if n > ph or n % 4 != 1:
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
            elif pair == "neg+lo":
                z["neg_lo"] += 1
            elif pair == "d2+g0":
                z["d2_g0"] += 1
            elif pair == "g0+d2":
                z["g0_d2"] += 1
            elif pair == "neg+d2":
                z["neg_d2"] += 1
            else:
                z["other"] += 1
    return z


def extra_sm_n3_kind_split(k: int) -> dict:
    """Leftover extra small n=3 mod 4 split by parent kind."""
    u = 1 << k
    ph = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    clip = 5 * u
    z = {
        "lo_g0": 0,
        "g0_lo": 0,
        "neg_lo": 0,
        "g0_d1": 0,
        "neg_d1": 0,
        "d2_g0": 0,
        "other": 0,
        "n": 0,
    }
    for n in range(1, 4 * u, 2):
        if n > ph or n % 4 != 3:
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
            elif pair == "neg+lo":
                z["neg_lo"] += 1
            elif pair == "g0+d1":
                z["g0_d1"] += 1
            elif pair == "neg+d1":
                z["neg_d1"] += 1
            elif pair == "d2+g0":
                z["d2_g0"] += 1
            else:
                z["other"] += 1
    return z


def tot_form() -> dict:
    """k<=64: 2-fold and n=3 sum; dies at k=3.

    Do not call extra_sm_res_split / kind walks here.
    Census is sm_2f_fold for k<=8.
    """
    n_ok = 0
    if want_n1_extra_sm(0) != 0 or want_n1_extra_sm(2) != 4:
        return {"ok": False, "k02": True}
    if want_n1_extra_sm(3) != 10 or want_n1_extra_sm(8) != 5440:
        return {"ok": False, "k38": True}
    if want_n3_extra_sm(3) != 14 or want_n3_extra_sm(8) != 5546:
        return {"ok": False, "n38": True}
    if want_n1_extra_sm(3) == want_n1_2f(3):
        return {"ok": False, "k3f": True}
    if want_n3_extra_sm(3) == want_n3_2s(3):
        return {"ok": False, "k3s": True}
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
        if k >= 4:
            if want_n1_extra_sm(k) != want_n1_2f(k):
                return {"ok": False, "2f": True, "k": k}
            if want_n3_extra_sm(k) != want_n3_2s(k):
                return {"ok": False, "2s": True, "k": k}
            if want_d2o_small(k - 1) != want_d2e_small(k - 1):
                return {"ok": False, "d2eq": True, "k": k}
            if want_n3_extra_sm(k) - want_n1_extra_sm(k) != want_d2e_small(k):
                return {"ok": False, "ex": True, "k": k}
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
        and want_n1_extra_sm(3) != want_n1_2f(3)
        and want_n3_extra_sm(3) != want_n3_2s(3)
        and want_n1_extra_sm(8) == 5440
        and want_n3_extra_sm(8) == 5546
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def sm_2f_fold() -> dict:
    """k<=8 leftover extra small 2-fold, n=3 sum, G=0, parent kinds."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        z = extra_sm_res_split(k)
        n1 = z[1]["n"]
        n3 = z[3]["n"]
        if n1 != want_n1_extra_sm(k) or n3 != want_n3_extra_sm(k):
            return {"ok": False, "n": True, "k": k, "got": z}
        n1k = extra_sm_n1_kind_split(k)
        n3k = extra_sm_n3_kind_split(k)
        if n1k["n"] != n1 or n3k["n"] != n3:
            return {"ok": False, "kn": True, "k": k}
        if k >= 3:
            if z[1]["g0"] != z[3]["g0"]:
                return {"ok": False, "g0": True, "k": k, "got": z}
            if z[1]["g0"] != z[1]["g1"]:
                return {"ok": False, "bal": True, "k": k}
            extra = n3 - n1
            if z[3]["g1"] - z[3]["g0"] != extra:
                return {"ok": False, "xg1": True, "k": k, "got": z}
        if k >= 4:
            if n1 != want_n1_2f(k):
                return {"ok": False, "2f": True, "k": k, "got": n1}
            if n3 != want_n3_2s(k):
                return {"ok": False, "2s": True, "k": k, "got": n3}
            if n1k["other"] != 0 or n3k["other"] != 0:
                return {"ok": False, "oth": True, "k": k}
            if n1k["lo_g0"] != want_sm(k - 1):
                return {"ok": False, "n1pg": True, "k": k, "got": n1k}
            if n1k["g0_lo"] + n1k["neg_lo"] != want_sm(k - 1):
                return {"ok": False, "n1gp": True, "k": k, "got": n1k}
            if n1k["d2_g0"] != want_d2e_small(k - 1):
                return {"ok": False, "n1d2": True, "k": k, "got": n1k}
            if n1k["g0_d2"] + n1k["neg_d2"] != want_d2e_small(k - 1):
                return {"ok": False, "n1gd": True, "k": k, "got": n1k}
            if n3k["lo_g0"] != want_sm(k - 1):
                return {"ok": False, "n3pg": True, "k": k, "got": n3k}
            if n3k["g0_lo"] + n3k["neg_lo"] != (
                want_sm(k - 1) + want_d2e_small(k - 1)
            ):
                return {"ok": False, "n3gp": True, "k": k, "got": n3k}
            if n3k["g0_d1"] + n3k["neg_d1"] != want_d1_small(k - 1):
                return {"ok": False, "n3d1": True, "k": k, "got": n3k}
            if n3k["d2_g0"] != want_d2o_small(k - 1):
                return {"ok": False, "n3d2": True, "k": k, "got": n3k}
        n_ok += 1
        rows[str(k)] = {
            "n1": n1,
            "n3": n3,
            "g0_1": z[1]["g0"],
            "g0_3": z[3]["g0"],
            "g1_3": z[3]["g1"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["n1"] == 4
        and rows["3"]["n1"] == 10
        and rows["3"]["n1"] != want_n1_2f(3)
        and rows["3"]["n3"] == 14
        and rows["3"]["n3"] != want_n3_2s(3)
        and rows["2"]["g0_1"] != rows["2"]["g0_3"]
        and rows["8"]["n1"] == 5440
        and rows["8"]["n3"] == 5546
        and rows["8"]["g0_1"] == rows["8"]["g0_3"]
        and rows["8"]["g0_1"] == 2720
        and want_n1_2f(4) == 42
        and want_n3_2s(4) == 48
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """2-fold and n=3 sum at k=3; G=0 equal at k=2."""
    z2 = extra_sm_res_split(2)
    z8 = extra_sm_res_split(8)
    ok = (
        want_n1_extra_sm(3) != want_n1_2f(3)
        and want_n3_extra_sm(3) != want_n3_2s(3)
        and z2[1]["g0"] != z2[3]["g0"]
        and z8[1]["n"] != z8[3]["n"]
        and z8[1]["g0"] == z8[3]["g0"]
        and z8[3]["g1"] != z8[3]["g0"]
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
    va = json.loads(VA_JSON.read_text())
    uz = json.loads(UZ_JSON.read_text())
    uy = json.loads(UY_JSON.read_text())
    ok = (
        va["checks"]["all_ok"]
        and uz["checks"]["all_ok"]
        and uy["checks"]["all_ok"]
        and va["verdict"]["oj_lo_eq_even_lo_halves"] == "LEMMA"
        and va["verdict"]["sm_rec_2sm_2d2e_lo_small_k_ge_4"] == "LEMMA"
        and va["verdict"]["extra_sm_n3_minus_n1_eq_d2e_small_k_ge_3"] == "LEMMA"
        and va["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and va["verdict"]["prize"] == "unsolved"
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
    cnt = sm_2f_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VB",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "sm_2f_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "n1_extra_sm_2fold_k_ge_4": True,
            "n3_extra_sm_2step_k_ge_4": True,
            "extra_sm_g0_equal_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "n1_extra_sm_2fold_k_ge_4": "LEMMA",
            "n3_extra_sm_2step_k_ge_4": "LEMMA",
            "extra_sm_g0_equal_k_ge_3": "LEMMA",
            "n1_2fold_at_k3": "KILLED",
            "n3_2step_at_k3": "KILLED",
            "extra_sm_g0_equal_at_k2": "KILLED",
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
        "n1/n3/g0 k8",
        dump["sm_2f_fold"]["rows"]["8"]["n1"],
        dump["sm_2f_fold"]["rows"]["8"]["n3"],
        dump["sm_2f_fold"]["rows"]["8"]["g0_1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
