#!/usr/bin/env python3
"""Cycle VA: odd-j leftover equals even leftover; small extra n3-n1 is d2e_small.

Odd-j leftover pal-pairs on odd covering match even leftover on each
half, so odd-j leftover tot equals lo_e. Even leftover on n<5U/2 is
the G-copy of parent even leftover small, leftover extra small,
odd-j leftover small, and small d=2, hence
sm(k)=2 sm(k-1)+2 d2e_small(k-1)+lo_small(k-1) for k>=4, matching
lo_e-e_ge. Leftover extra small (n=3 minus n=1) equals d2e_small for
k>=3. Dies at k=3 for the 2 d2e small recurrence (count 17, not 19).
Dies at k=2 for extra small n3-n1. Do not PREFIX pal-center tot.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_va.py --certify
Dump: research/cycle_va.json
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
from cycle_uk import want_lo_small
from cycle_ul import parent_pair_type
from cycle_un import want_d2e_small, want_d2o_small
from cycle_up import lucas, want_lo_e
from cycle_ur import even_lo_ph_split, parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor_large
from cycle_uw import leftover_cell, want_3u, want_miss_n
from cycle_uy import want_lo_parent_large_diff
from cycle_uz import leftover_even_cell, leftover_odd_j_cell, want_ege
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UZ_JSON = Path(__file__).resolve().parent / "cycle_uz.json"
UY_JSON = Path(__file__).resolve().parent / "cycle_uy.json"
UX_JSON = Path(__file__).resolve().parent / "cycle_ux.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_sm(k: int) -> int:
    """Even leftover on n<5U/2: 0,1,4,17, then 2 sm+2 d2e_small+lo_small."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    if k == 2:
        return 4
    if k == 3:
        return 17
    return (
        2 * want_sm(k - 1)
        + 2 * want_d2e_small(k - 1)
        + want_lo_small(k - 1)
    )


def want_n1_extra_sm(k: int) -> int:
    """Leftover extra small n=1 mod 4: (lo_small-d2e_small)/2 for k>=3."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    if k == 2:
        return 4
    return (want_lo_small(k) - want_d2e_small(k)) // 2


def want_n3_extra_sm(k: int) -> int:
    """Leftover extra small n=3 mod 4: (lo_small+d2e_small)/2 for k>=3."""
    if k <= 1:
        return k
    if k == 2:
        return 3
    return (want_lo_small(k) + want_d2e_small(k)) // 2


def odd_j_lo_ph_split(k: int) -> dict:
    """Odd-j leftover pal-pairs split by n<=ph versus n>ph."""
    u = 1 << k
    ph = parent_half(k)
    clip = 5 * u
    sm = lg = 0
    for n in range(1, 4 * u, 2):
        hi = min(2 * n, clip)
        for j in range(1, hi + 1, 2):
            if not leftover_odd_j_cell(n, j, k):
                continue
            if n <= ph:
                sm += 1
            else:
                lg += 1
    return {"sm": sm, "lg": lg}


def leftover_extra_sm_split(k: int) -> dict:
    """Leftover extra on n<=5U/2 split by n mod 4."""
    u = 1 << k
    ph = parent_half(k)
    clip = 5 * u
    z = {1: 0, 3: 0}
    for n in range(1, 4 * u, 2):
        if n > ph:
            continue
        r = n % 4
        if r not in (1, 3):
            continue
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if leftover_cell(n, j, k):
                z[r] += 1
    return z


def sm_kind_split(k: int) -> dict:
    """Even leftover on n<5U/2 split by parent kind."""
    u = 1 << k
    ph = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    ph_p = parent_half(k_p) if k >= 1 else 0
    clip = 5 * u
    z = {
        "lo_e_sm": 0,
        "lo_o_evenj": 0,
        "lo_o_oddj": 0,
        "d2_e": 0,
        "d2_o": 0,
        "other": 0,
        "n": 0,
    }
    for n in range(0, 4 * u, 2):
        if n >= ph:
            continue
        m = n // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if not leftover_even_cell(n, j, k):
                continue
            z["n"] += 1
            if j % 2 == 1:
                z["other"] += 1
                continue
            r = j // 2
            kr = parent_pair_type(m, r, k_p)
            tag = "sm" if m < ph_p else ("eq" if m == ph_p else "lg")
            if kr == "lo" and m % 2 == 0 and tag == "sm":
                z["lo_e_sm"] += 1
            elif kr == "lo" and m % 2 == 1 and r % 2 == 0:
                z["lo_o_evenj"] += 1
            elif kr == "lo" and m % 2 == 1 and r % 2 == 1:
                z["lo_o_oddj"] += 1
            elif kr == "d2" and m % 2 == 0:
                z["d2_e"] += 1
            elif kr == "d2" and m % 2 == 1:
                z["d2_o"] += 1
            else:
                z["other"] += 1
    return z


def tot_form() -> dict:
    """k<=64: sm recurrence equals lo_e-e_ge; dies at k=3.

    Do not call even_lo_ph_split / odd_j walks here.
    Census is sm_fold for k<=8.
    """
    n_ok = 0
    if want_sm(0) != 0 or want_sm(2) != 4:
        return {"ok": False, "k02": True}
    if want_sm(3) != 17 or want_sm(8) != 8790:
        return {"ok": False, "k38": True}
    raw3 = (
        2 * want_sm(2)
        + 2 * want_d2e_small(2)
        + want_lo_small(2)
    )
    if want_sm(3) == raw3:
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
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if want_sm(k) != want_lo_e(k) - want_ege(k):
            return {"ok": False, "diff": True, "k": k}
        if k >= 4:
            if want_sm(k) != (
                2 * want_sm(k - 1)
                + 2 * want_d2e_small(k - 1)
                + want_lo_small(k - 1)
            ):
                return {"ok": False, "rec": True, "k": k}
            if want_d2o_small(k - 1) != want_d2e_small(k - 1):
                return {"ok": False, "d2eq": True, "k": k}
            if (want_lo_small(k) - want_d2e_small(k)) % 2 != 0:
                return {"ok": False, "par": True, "k": k}
            if want_n1_extra_sm(k) + want_n3_extra_sm(k) != want_lo_small(k):
                return {"ok": False, "sum": True, "k": k}
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
        and want_sm(3) != raw3
        and want_sm(8) == 8790
        and want_n1_extra_sm(8) == 5440
        and want_n3_extra_sm(8) == 5546
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


def sm_fold() -> dict:
    """k<=8 odd-j leftover halves, extra small n mod 4, sm parent kinds."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        eh = even_lo_ph_split(k)
        if eh["sm"] != want_sm(k):
            return {"ok": False, "sm": True, "k": k, "got": eh["sm"]}
        oj = odd_j_lo_ph_split(k)
        if oj["sm"] != want_sm(k) or oj["lg"] != want_ege(k):
            return {"ok": False, "oj": True, "k": k, "got": oj}
        if oj["sm"] + oj["lg"] != want_lo_e(k):
            return {"ok": False, "ojt": True, "k": k}
        ex = leftover_extra_sm_split(k)
        if ex[1] != want_n1_extra_sm(k) or ex[3] != want_n3_extra_sm(k):
            return {"ok": False, "ex": True, "k": k, "got": ex}
        kinds = sm_kind_split(k)
        if kinds["n"] != want_sm(k):
            return {"ok": False, "kn": True, "k": k, "got": kinds}
        if k >= 4:
            if kinds["other"] != 0:
                return {"ok": False, "oth": True, "k": k, "got": kinds}
            if kinds["lo_e_sm"] != want_sm(k - 1):
                return {"ok": False, "les": True, "k": k, "got": kinds}
            if kinds["lo_o_evenj"] != want_lo_small(k - 1):
                return {"ok": False, "ej": True, "k": k, "got": kinds}
            if kinds["lo_o_oddj"] != want_sm(k - 1):
                return {"ok": False, "ojp": True, "k": k, "got": kinds}
            if kinds["d2_e"] != want_d2e_small(k - 1):
                return {"ok": False, "d2e": True, "k": k, "got": kinds}
            if kinds["d2_o"] != want_d2o_small(k - 1):
                return {"ok": False, "d2o": True, "k": k, "got": kinds}
        n_ok += 1
        rows[str(k)] = {
            "sm": eh["sm"],
            "oj_sm": oj["sm"],
            "oj_lg": oj["lg"],
            "n1": ex[1],
            "n3": ex[3],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["3"]["sm"] == 17
        and rows["3"]["sm"]
        != (
            2 * want_sm(2)
            + 2 * want_d2e_small(2)
            + want_lo_small(2)
        )
        and rows["2"]["n3"] - rows["2"]["n1"] != want_d2e_small(2)
        and rows["8"]["sm"] == 8790
        and rows["8"]["oj_sm"] == 8790
        and rows["8"]["n1"] == 5440
        and rows["8"]["n3"] == 5546
        and want_sm(4) == 66
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """2 d2e small rec at k=3; extra small n3-n1 at k=2."""
    raw3 = (
        2 * want_sm(2)
        + 2 * want_d2e_small(2)
        + want_lo_small(2)
    )
    ok = (
        want_sm(3) != raw3
        and want_d2o_small(2) != want_d2e_small(2)
        and want_n3_extra_sm(2) - want_n1_extra_sm(2) != want_d2e_small(2)
        and want_sm(8) == want_lo_e(8) - want_ege(8)
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
    uz = json.loads(UZ_JSON.read_text())
    uy = json.loads(UY_JSON.read_text())
    ux = json.loads(UX_JSON.read_text())
    ok = (
        uz["checks"]["all_ok"]
        and uy["checks"]["all_ok"]
        and ux["checks"]["all_ok"]
        and uz["verdict"]["oj_lo_large_eq_ege"] == "LEMMA"
        and uz["verdict"]["ege_rec_2ege_2d2e_lo_large_k_ge_4"] == "LEMMA"
        and uz["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uz["verdict"]["prize"] == "unsolved"
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
    cnt = sm_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "sm_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "oj_lo_eq_even_lo_halves": True,
            "sm_rec_2sm_2d2e_lo_small_k_ge_4": True,
            "extra_sm_n3_minus_n1_eq_d2e_small_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "oj_lo_eq_even_lo_halves": "LEMMA",
            "sm_rec_2sm_2d2e_lo_small_k_ge_4": "LEMMA",
            "extra_sm_n3_minus_n1_eq_d2e_small_k_ge_3": "LEMMA",
            "sm_2d2e_rec_at_k3": "KILLED",
            "extra_sm_n3n1_eq_d2e_at_k2": "KILLED",
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
        "sm/oj/n1n3 k8",
        dump["sm_fold"]["rows"]["8"]["sm"],
        dump["sm_fold"]["rows"]["8"]["oj_sm"],
        dump["sm_fold"]["rows"]["8"]["n1"],
        dump["sm_fold"]["rows"]["8"]["n3"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
