#!/usr/bin/env python3
"""Cycle UT: leftover pal-pairs at n=5U/2 produce both xor children.

The three leftover pal-pairs at covering n=5U/2 (Cycle UR) sit on
even n for k>=3, so both odd neighbors vanish. Each therefore
produces a leftover pair+g0 child and a leftover g0+pair child at
n=5U/2+1, pal-left, distances 2d-1 and 2d+1, none of {1,2}, not
clip-edge. Dies at k=2 (parent-half odd). Do not PREFIX
leftover-parent xor large difference or pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_ut.py --certify
Dump: research/cycle_ut.json
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
from cycle_uo import named_half_split
from cycle_up import lucas
from cycle_ur import parent_half, ph_lo_js, want_ph_lo
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
US_JSON = Path(__file__).resolve().parent / "cycle_us.json"
UR_JSON = Path(__file__).resolve().parent / "cycle_ur.json"
UQ_JSON = Path(__file__).resolve().parent / "cycle_uq.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
K_PH = 16
PAT0011 = (0, 0, 1, 1)


def child_n_from_ph(k: int) -> int:
    """Odd covering child of parent-half: 5U/2+1."""
    return 2 * parent_half(k - 1) + 1 if k >= 1 else 1


def leftover_child_ok(n: int, j: int, k: int) -> bool:
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


def ph_xor_children(k: int) -> dict:
    """pair+g0 and g0+pair leftover children of the three at parent-half."""
    if k <= 2:
        return {"ok": False, "k": k, "n_pg": 0, "n_gp": 0}
    php = parent_half(k - 1)
    nch = child_n_from_ph(k)
    half = 5 * (1 << k) // 2
    n_pg = n_gp = 0
    for j in ph_lo_js(k - 1):
        if php % 2 != 0:
            return {"ok": False, "odd": True, "k": k}
        if G(php, j - 1) != 0 or G(php, j + 1) != 0:
            return {"ok": False, "nb": True, "k": k, "j": j}
        j_gp = 2 * j
        j_pg = 2 * (j + 1)
        if not leftover_child_ok(nch, j_gp, k):
            return {"ok": False, "gp": True, "k": k, "j": j}
        if not leftover_child_ok(nch, j_pg, k):
            return {"ok": False, "pg": True, "k": k, "j": j}
        if nch <= half:
            return {"ok": False, "half": True, "k": k}
        n_gp += 1
        n_pg += 1
    ok = n_pg == 3 and n_gp == 3
    return {"ok": ok, "n_pg": n_pg, "n_gp": n_gp, "nch": nch}


def tot_form() -> dict:
    """k<=64: even half, odd neighbors 0, child large, distances."""
    n_ok = 0
    if want_ph_lo(0) != 0 or want_ph_lo(2) != 2 or want_ph_lo(3) != 3:
        return {"ok": False, "ph": True}
    if G(5, 1) != 1 or G(5, 3) != 0:
        return {"ok": False, "g5": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
        if m > 0 and G(2 * m, 1) != 0:
            return {"ok": False, "eodd": True, "m": m}
        if G(2 * m + 1, 2 * m) != G(m, m) ^ G(m, m - 1):
            return {"ok": False, "gp": True, "m": m}
        if G(2 * m + 1, 2) != G(m, 1) ^ G(m, 0):
            return {"ok": False, "pg": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if (ph % 2 == 0) != (k != 1):
            return {"ok": False, "pev": True, "k": k}
        if k >= 3:
            php = parent_half(k - 1)
            nch = child_n_from_ph(k)
            half = 5 * u // 2
            if php % 2 != 0 or nch != half + 1:
                return {"ok": False, "nch": True, "k": k}
            if nch >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            j0, j1, j2 = ph_lo_js(k - 1)
            if php - j0 != (1 << k):
                return {"ok": False, "d0": True, "k": k, "got": php - j0}
            if php - j1 != 3 * (1 << (k - 2)):
                return {"ok": False, "d1": True, "k": k}
            if php - j2 != (1 << (k - 2)):
                return {"ok": False, "d2": True, "k": k}
            for j, d in ((j0, php - j0), (j1, php - j1), (j2, php - j2)):
                if 2 * d + 1 in (1, 2) or 2 * d - 1 in (1, 2):
                    return {"ok": False, "cd": True, "k": k, "j": j}
                if j % 2 == 0 and G(php, j - 1) != 0:
                    return {"ok": False, "gl": True, "k": k}
                if j % 2 == 0 and G(php, j + 1) != 0:
                    return {"ok": False, "gr": True, "k": k}
        if k == 2:
            if parent_half(1) % 2 == 0:
                return {"ok": False, "k2": True}
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
        and want_ph_lo(2) != 3
        and want_ph_lo(8) == 3
        and G(10, 1) == 0
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
        and child_n_from_ph(8) == 641
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ph_xor_fold() -> dict:
    """k<=16 unique both xor children; k<=8 census gp/pg from parent-half."""
    n_ok = 0
    rows = {}
    for k in range(3, K_PH + 1):
        r = ph_xor_children(k)
        if not r["ok"]:
            return {"ok": False, "ch": True, "k": k, "got": r}
        n_ok += 1
        rows[str(k)] = {"n_pg": r["n_pg"], "n_gp": r["n_gp"], "nch": r["nch"]}
    n_c = 0
    c_rows = {}
    for k in range(0, K_COUNT + 1):
        hs = named_half_split(k)
        php = parent_half(k - 1) if k >= 1 else 0
        n_pg = n_gp = 0
        if k >= 3:
            u = 1 << k
            clip = 5 * u
            half = 5 * u // 2
            nch = child_n_from_ph(k)
            k_p = k - 1
            hi = min(2 * nch, clip)
            m = (nch - 1) // 2
            for j in range(0, hi + 1, 2):
                if G(nch, j) == 0:
                    continue
                if pal_kind(nch, j, k) != "pair":
                    continue
                if j >= 2 * nch - j:
                    continue
                d = nch - j
                if d in (1, 2) or is_clip_edge(nch, j, k):
                    continue
                r = j // 2
                if r == 0:
                    continue
                kr = parent_pair_type(m, r, k_p)
                km = parent_pair_type(m, r - 1, k_p)
                if km == "lo" and kr == "g0":
                    n_pg += 1
                elif km == "g0" and kr == "lo":
                    n_gp += 1
            if m != php:
                return {"ok": False, "m": True, "k": k}
            if n_pg != want_ph_lo(k - 1) or n_gp != want_ph_lo(k - 1):
                return {"ok": False, "cnt": True, "k": k, "got": (n_pg, n_gp)}
            if k >= 4 and (n_pg != 3 or n_gp != 3):
                return {"ok": False, "c3": True, "k": k}
            if k == 3 and (n_pg != 2 or n_gp != 2):
                return {"ok": False, "c2": True, "k": k}
            if nch <= half:
                return {"ok": False, "lg": True, "k": k}
        n_c += 1
        c_rows[str(k)] = {
            "n_pg": n_pg,
            "n_gp": n_gp,
            "plo_l": hs["plo_l"],
            "glo_l": hs["glo_l"],
        }
    ok = (
        n_ok == K_PH - 2
        and n_c == K_COUNT + 1
        and rows["3"]["n_pg"] == 3
        and rows["3"]["n_gp"] == 3
        and rows["16"]["n_pg"] == 3
        and rows["16"]["n_gp"] == 3
        and c_rows["8"]["n_pg"] == 3
        and c_rows["8"]["n_gp"] == 3
        and c_rows["3"]["n_pg"] == 2
        and c_rows["3"]["n_gp"] == 2
        and c_rows["2"]["n_pg"] == 0
        and want_ph_lo(2) != 3
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_c": n_c,
        "k_hi": K_PH,
        "rows": rows,
        "c_rows": c_rows,
    }


def killed_eq() -> dict:
    """both xor at k=2; gp never on even half; children named."""
    r2 = ph_xor_children(2)
    r8 = ph_xor_children(8)
    ok = (
        r2["ok"] is False
        and r8["ok"]
        and r8["n_pg"] == 3
        and r8["n_gp"] == 3
        and want_ph_lo(2) != 3
        and want_ph_lo(2) == 2
        and parent_half(1) == 5
        and G(5, 1) == 1
        and G(2, 1) == 0
        and G(2, 2) != 2 % 2
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
    us = json.loads(US_JSON.read_text())
    ur = json.loads(UR_JSON.read_text())
    uq = json.loads(UQ_JSON.read_text())
    ok = (
        us["checks"]["all_ok"]
        and ur["checks"]["all_ok"]
        and uq["checks"]["all_ok"]
        and us["verdict"]["oj_lg_eq_even_lo_ge_k_ge_2"] == "LEMMA"
        and ur["verdict"]["ph_lo_eq_3_k_ge_3"] == "LEMMA"
        and ur["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ur["verdict"]["prize"] == "unsolved"
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
    cnt = ph_xor_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph_xor_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph_lo_both_xor_k_ge_3": True,
            "ph_xor_lo_eq_ph_lo_parent": True,
            "ph_lo_both_xor_at_k2": False,
            "gp_never_on_even_ph": False,
            "ph_xor_lo_eq_3_at_k3": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph_lo_both_xor_k_ge_3": "LEMMA",
            "ph_xor_lo_eq_ph_lo_parent": "LEMMA",
            "ph_lo_both_xor_at_k2": "KILLED",
            "gp_never_on_even_ph": "KILLED",
            "ph_xor_lo_eq_3_at_k3": "KILLED",
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
            "lo_parent_large_diff_closed": "PREFIX",
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
        "n_pg k16",
        dump["ph_xor_fold"]["rows"]["16"]["n_pg"],
        "n_gp k16",
        dump["ph_xor_fold"]["rows"]["16"]["n_gp"],
        "census k8",
        dump["ph_xor_fold"]["c_rows"]["8"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
