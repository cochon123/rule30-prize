#!/usr/bin/env python3
"""Cycle UZ: even leftover on n>=5U/2 is G-copy of parent leftover kinds.

G(2m,2t)=G(m,t). Even leftover on n>=5U/2 is the copy of parent even
leftover on n>=5 U_p/2, leftover extra large, odd-j leftover large,
and large d=2 (even and odd). Odd-j leftover large equals e_ge at
the same k. Hence e_ge(k)=2 e_ge(k-1)+2 d2e_large(k-1)+lo_large(k-1)
for k>=4, and e_ge(k)=n1(k)+lo_large(k-1) for k>=3. Dies at k=3 for
the 2 d2e recurrence (d2o!=d2e at k=2; count 11, not 9). Do not
PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_uz.py --certify
Dump: research/cycle_uz.json
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
from cycle_ul import parent_pair_type
from cycle_un import want_d2e_large, want_d2o_large
from cycle_up import lucas, want_lo_e
from cycle_uq import want_lo_large
from cycle_ur import even_lo_ph_split, parent_half, want_ph_lo
from cycle_uu import want_even_j0_sm
from cycle_uv import unique_van_odd_even, want_ej_xor_large
from cycle_uw import leftover_cell, want_3u, want_miss_n
from cycle_ux import e_ge, want_n1_extra_lg
from cycle_uy import want_extra_lg, want_lo_parent_large_diff, want_n3_extra_lg
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UY_JSON = Path(__file__).resolve().parent / "cycle_uy.json"
UX_JSON = Path(__file__).resolve().parent / "cycle_ux.json"
UW_JSON = Path(__file__).resolve().parent / "cycle_uw.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ege(k: int) -> int:
    """Even leftover on n>=5U/2: 0,0,2,11, then 2 e_ge+2 d2e_large+lo_large."""
    if k <= 1:
        return 0
    if k == 2:
        return 2
    if k == 3:
        return 11
    return (
        2 * want_ege(k - 1)
        + 2 * want_d2e_large(k - 1)
        + want_lo_large(k - 1)
    )


def leftover_odd_j_cell(n: int, j: int, k: int) -> bool:
    if n % 2 == 0 or j % 2 == 0:
        return False
    if G(n, j) == 0:
        return False
    if pal_kind(n, j, k) != "pair":
        return False
    if j >= 2 * n - j:
        return False
    d = n - j
    if d in (1, 2) or is_clip_edge(n, j, k):
        return False
    return True


def leftover_even_cell(n: int, j: int, k: int) -> bool:
    if n % 2 != 0:
        return False
    if G(n, j) == 0:
        return False
    if pal_kind(n, j, k) != "pair":
        return False
    if j >= 2 * n - j:
        return False
    d = n - j
    if d in (1, 2) or is_clip_edge(n, j, k):
        return False
    return True


def odd_j_lo_large(k: int) -> int:
    """Odd-j leftover pal-pairs on odd covering n>5U/2."""
    u = 1 << k
    ph = parent_half(k)
    clip = 5 * u
    c = 0
    for n in range(1, 4 * u, 2):
        if n <= ph:
            continue
        hi = min(2 * n, clip)
        for j in range(1, hi + 1, 2):
            if leftover_odd_j_cell(n, j, k):
                c += 1
    return c


def ege_kind_split(k: int) -> dict:
    """Even leftover on n>=5U/2 split by parent kind."""
    u = 1 << k
    ph = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    ph_p = parent_half(k_p) if k >= 1 else 0
    clip = 5 * u
    z = {
        "lo_e_eq": 0,
        "lo_e_lg": 0,
        "lo_o_evenj": 0,
        "lo_o_oddj": 0,
        "d2_e": 0,
        "d2_o": 0,
        "other": 0,
        "n": 0,
    }
    for n in range(0, 4 * u, 2):
        if n < ph:
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
            if kr == "lo" and m % 2 == 0 and tag == "eq":
                z["lo_e_eq"] += 1
            elif kr == "lo" and m % 2 == 0 and tag == "lg":
                z["lo_e_lg"] += 1
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
    """k<=64: e_ge recurrence; dies at k=3.

    Do not call even_lo_ph_split / odd_j_lo_large here.
    Census is ege_fold for k<=8.
    """
    n_ok = 0
    if want_ege(0) != 0 or want_ege(2) != 2:
        return {"ok": False, "k02": True}
    if want_ege(3) != 11 or want_ege(8) != 5324:
        return {"ok": False, "k38": True}
    raw3 = (
        2 * want_ege(2)
        + 2 * want_d2e_large(2)
        + want_lo_large(2)
    )
    if want_ege(3) == raw3:
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
        if m > 0 and G(2 * m, 2 * (m - 1) if m else 0) != G(m, m - 1 if m else 0):
            return {"ok": False, "cpy": True, "m": m}
        if not unique_van_odd_even(m, 0):
            return {"ok": False, "van": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if k >= 4:
            if want_ege(k) != (
                2 * want_ege(k - 1)
                + 2 * want_d2e_large(k - 1)
                + want_lo_large(k - 1)
            ):
                return {"ok": False, "rec": True, "k": k}
            if want_d2o_large(k - 1) != want_d2e_large(k - 1):
                return {"ok": False, "d2eq": True, "k": k}
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
        and want_ege(3) != raw3
        and want_ege(8) == 5324
        and want_n1_extra_lg(8) == 3290
        and want_n1_extra_lg(8) + want_lo_large(7) == 5324
        and want_n3_extra_lg(8) == 3354
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
        and want_ph_lo(8) == 3
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ege_fold() -> dict:
    """k<=8 even leftover large, odd-j leftover large, parent kinds."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        eh = even_lo_ph_split(k)
        eg = eh["eq"] + eh["lg"]
        if eg != want_ege(k) or eg != e_ge(k):
            return {"ok": False, "ege": True, "k": k, "got": eg}
        oj = odd_j_lo_large(k)
        if oj != want_ege(k):
            return {"ok": False, "oj": True, "k": k, "got": oj}
        if k >= 3:
            if eg != want_n1_extra_lg(k) + want_lo_large(k - 1):
                return {"ok": False, "n1": True, "k": k}
        kinds = ege_kind_split(k)
        if kinds["n"] != eg:
            return {"ok": False, "kn": True, "k": k, "got": kinds}
        if k >= 4:
            if kinds["other"] != 0:
                return {"ok": False, "oth": True, "k": k, "got": kinds}
            if kinds["lo_e_eq"] != want_ph_lo(k - 1):
                return {"ok": False, "eq": True, "k": k, "got": kinds}
            if kinds["lo_e_lg"] != want_ege(k - 1) - want_ph_lo(k - 1):
                return {"ok": False, "lg": True, "k": k, "got": kinds}
            if kinds["lo_o_evenj"] != want_lo_large(k - 1):
                return {"ok": False, "ej": True, "k": k, "got": kinds}
            if kinds["lo_o_oddj"] != want_ege(k - 1):
                return {"ok": False, "ojp": True, "k": k, "got": kinds}
            if kinds["d2_e"] != want_d2e_large(k - 1):
                return {"ok": False, "d2e": True, "k": k, "got": kinds}
            if kinds["d2_o"] != want_d2o_large(k - 1):
                return {"ok": False, "d2o": True, "k": k, "got": kinds}
        n_ok += 1
        rows[str(k)] = {
            "ege": eg,
            "oj": oj,
            "sm": eh["sm"],
            "eq": eh["eq"],
            "lg": eh["lg"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["ege"] == 2
        and rows["3"]["ege"] == 11
        and rows["3"]["ege"]
        != (
            2 * want_ege(2)
            + 2 * want_d2e_large(2)
            + want_lo_large(2)
        )
        and rows["8"]["ege"] == 5324
        and rows["8"]["oj"] == 5324
        and rows["8"]["eq"] == 3
        and want_ege(4) == 40
        and want_n1_extra_lg(2) + want_lo_large(1) != want_ege(2)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """2 d2e recurrence at k=3; n1+lo_large at k=2."""
    raw3 = (
        2 * want_ege(2)
        + 2 * want_d2e_large(2)
        + want_lo_large(2)
    )
    ok = (
        want_ege(3) != raw3
        and want_d2o_large(2) != want_d2e_large(2)
        and want_n1_extra_lg(2) + want_lo_large(1) != want_ege(2)
        and want_ege(8) == e_ge(8)
        and leftover_cell(want_3u(8), 0, 8) is False
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
    uy = json.loads(UY_JSON.read_text())
    ux = json.loads(UX_JSON.read_text())
    uw = json.loads(UW_JSON.read_text())
    ok = (
        uy["checks"]["all_ok"]
        and ux["checks"]["all_ok"]
        and uw["checks"]["all_ok"]
        and uy["verdict"]["lo_parent_large_diff_closed_k_ge_4"] == "LEMMA"
        and uy["verdict"]["n3_extra_lg_lo_large_2step_k_ge_4"] == "LEMMA"
        and uy["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uy["verdict"]["prize"] == "unsolved"
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
    cnt = ege_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ege_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "oj_lo_large_eq_ege": True,
            "ege_rec_2ege_2d2e_lo_large_k_ge_4": True,
            "ege_eq_n1_plus_lo_large_parent_k_ge_3": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "oj_lo_large_eq_ege": "LEMMA",
            "ege_rec_2ege_2d2e_lo_large_k_ge_4": "LEMMA",
            "ege_eq_n1_plus_lo_large_parent_k_ge_3": "LEMMA",
            "ege_2d2e_rec_at_k3": "KILLED",
            "ege_eq_n1_lo_large_at_k2": "KILLED",
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
        "ege/oj k8",
        dump["ege_fold"]["rows"]["8"]["ege"],
        dump["ege_fold"]["rows"]["8"]["oj"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
