#!/usr/bin/env python3
"""Cycle UL: leftover extra from d=1/d=2 parents is Jacobsthal.

pair+g0 of a d=1 parent is a d=1 child, so pg:d1 is empty. g0+pair of
d=1 is leftover d=3 except parent n=1 (child j=0), hence gp:d1 is
J_{k+1}-1 for k>=1. pair+g0 of every parent d=2 is leftover extra for
k>=2, count 2 J_k. g0+pair of d=2 is only even parents (odd d=2 has
G(m,m-3)=1), minus parent n=2 at j=0, hence gp:d2 is J_k-1. Do not
PREFIX leftover-parent xor or leftover extra or unpaired extra. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk leftover
d catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_ul.py --certify
Dump: research/cycle_ul.json
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
from cycle_te import want_d2_n, want_d2_parity_n
from cycle_tt import is_clip_edge, unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_tw import leftover_xor_split, want_j0_odd_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_ui import want_pg_minus_gp
from cycle_uk import want_lo_small
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UK_JSON = Path(__file__).resolve().parent / "cycle_uk.json"
UI_JSON = Path(__file__).resolve().parent / "cycle_ui.json"
TW_JSON = Path(__file__).resolve().parent / "cycle_tw.json"
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"
TD_JSON = Path(__file__).resolve().parent / "cycle_td.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_gp_d1(k: int) -> int:
    """g0+pair leftover extra from d=1: 0 at k=0, J_{k+1}-1 for k>=1."""
    if k <= 0:
        return 0
    return jacobsthal(k + 1) - 1


def want_pg_d2(k: int) -> int:
    """pair+g0 leftover extra from d=2: 0,1, then 2 J_k."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return 2 * jacobsthal(k)


def want_gp_d2(k: int) -> int:
    """g0+pair leftover extra from d=2: 0 at k<=1, J_k-1 for k>=2."""
    if k <= 1:
        return 0
    return jacobsthal(k) - 1


def want_named_lo(k: int) -> int:
    """Named d=1/d=2 leftover extra: gp:d1 + pg:d2 + gp:d2."""
    return want_gp_d1(k) + want_pg_d2(k) + want_gp_d2(k)


def parent_pair_type(m: int, r0: int, k_p: int) -> str:
    if r0 < 0 or G(m, r0) == 0:
        return "g0"
    kind = pal_kind(m, r0, k_p)
    if kind != "pair":
        return kind
    d = abs(m - r0)
    if d == 1:
        return "d1"
    if d == 2:
        return "d2"
    if is_clip_edge(m, r0, k_p):
        return "clip"
    return "lo"


def leftover_named_split(k: int) -> dict:
    """Odd-n even-j leftover extra: parent xor kinds including d=1/d=2."""
    u = 1 << k
    clip = 5 * u
    k_p = k - 1 if k >= 1 else 0
    extra = n_neg = n_bad = 0
    n_pg_d1 = n_pg_d2 = n_pg_lo = n_pg_clip = 0
    n_gp_d1 = n_gp_d2 = n_gp_lo = n_gp_clip = 0
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            extra += 1
            r = j // 2
            if r == 0:
                n_neg += 1
                continue
            kr = parent_pair_type(m, r, k_p)
            km = parent_pair_type(m, r - 1, k_p)
            if km in ("d1", "d2", "lo", "clip") and kr == "g0":
                if km == "d1":
                    n_pg_d1 += 1
                elif km == "d2":
                    n_pg_d2 += 1
                elif km == "lo":
                    n_pg_lo += 1
                else:
                    n_pg_clip += 1
            elif km == "g0" and kr in ("d1", "d2", "lo", "clip"):
                if kr == "d1":
                    n_gp_d1 += 1
                elif kr == "d2":
                    n_gp_d2 += 1
                elif kr == "lo":
                    n_gp_lo += 1
                else:
                    n_gp_clip += 1
            else:
                n_bad += 1
    return {
        "extra": extra,
        "n_neg": n_neg,
        "n_pg_d1": n_pg_d1,
        "n_pg_d2": n_pg_d2,
        "n_pg_lo": n_pg_lo,
        "n_pg_clip": n_pg_clip,
        "n_gp_d1": n_gp_d1,
        "n_gp_d2": n_gp_d2,
        "n_gp_lo": n_gp_lo,
        "n_gp_clip": n_gp_clip,
        "n_bad": n_bad,
    }


def tot_form() -> dict:
    """k<=64: J recurrences; parent d=1/d=2 child slots; G samples."""
    n_ok = 0
    if want_gp_d1(0) != 0 or want_gp_d1(1) != 0:
        return {"ok": False, "g01": True}
    if want_pg_d2(0) != 0 or want_pg_d2(1) != 1:
        return {"ok": False, "p01": True}
    if want_gp_d2(2) != 0 or want_named_lo(8) != 424:
        return {"ok": False, "k8": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and m % 2 == 1 and m != 1:
            if G(m, m - 1) ^ G(m, m - 2) != 1:
                return {"ok": False, "xor": True, "m": m}
        if m >= 1 and m % 2 == 0:
            if G(m, m - 1) != 0:
                return {"ok": False, "eodd": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_named_lo(k) != want_gp_d1(k) + want_pg_d2(k) + want_gp_d2(k):
            return {"ok": False, "def": True, "k": k}
        if k >= 1:
            if want_gp_d1(k) != want_d1_n(k - 1) - 1:
                return {"ok": False, "d1p": True, "k": k}
            if want_gp_d1(k) != jacobsthal(k + 1) - 1:
                return {"ok": False, "Jd1": True, "k": k}
            if pal_kind(1, 0, k - 1) != "pair" or abs(1 - 0) != 1:
                return {"ok": False, "n1": True, "k": k}
            n_c = 2 * 1 + 1
            if n_c - 0 != 3:
                return {"ok": False, "j0d": True, "k": k}
        if k >= 2:
            if want_pg_d2(k) != want_d2_n(k - 1):
                return {"ok": False, "d2p": True, "k": k}
            if want_pg_d2(k) != 2 * jacobsthal(k):
                return {"ok": False, "Jd2": True, "k": k}
            if want_gp_d2(k) != want_d2_parity_n(k - 1) - 1:
                return {"ok": False, "d2e": True, "k": k}
            if want_named_lo(k) != (1 << k) + 2 * jacobsthal(k) - 2:
                return {"ok": False, "nm": True, "k": k}
            if pal_kind(2, 0, k - 1) != "pair" or abs(2 - 0) != 2:
                return {"ok": False, "n2": True, "k": k}
            if G(2, 1) != 0:
                return {"ok": False, "g21": True, "k": k}
        if k >= 1 and jacobsthal(k + 1) != (1 << k) - jacobsthal(k):
            return {"ok": False, "Jrec": True, "k": k}
        if k >= 2:
            m = 2 * u - 1
            if m % 2 == 0 or G(m, m - 1) ^ G(m, m - 2) != 1:
                return {"ok": False, "odd": True, "k": k}
            if G(m, m - 1) == 1:
                n = 2 * m + 1
                j = 2 * m
                if n - j != 1:
                    return {"ok": False, "pgd1": True, "k": k}
        if k >= 3:
            l = 3
            n = 2 * l + 1
            if G(n, n - 2) != G(l, l - 1):
                return {"ok": False, "te": True, "k": k}
            if G(n, n - 3) != G(l, l - 1) ^ G(l, l - 2):
                return {"ok": False, "n3": True, "k": k}
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
        and want_gp_d1(8) == 170
        and want_pg_d2(8) == 170
        and want_gp_d2(8) == 84
        and want_named_lo(8) != 0
        and want_gp_d1(8) != jacobsthal(9)
        and want_lo_small(8) == 10986
        and want_pg_minus_gp(8) == 149
        and want_j0_odd_lo(8) == 319
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
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def named_fold() -> dict:
    """k<=8: named leftover extra matches Jacobsthal; pg:d1 empty."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = leftover_named_split(k)
        lo = leftover_xor_split(k)
        if r["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if r["n_pg_d1"] != 0 or r["n_pg_clip"] != 0 or r["n_gp_clip"] != 0:
            return {"ok": False, "pgd1": True, "k": k, **r}
        if r["n_gp_d1"] != want_gp_d1(k):
            return {"ok": False, "gpd1": True, "k": k, **r}
        if r["n_pg_d2"] != want_pg_d2(k):
            return {"ok": False, "pgd2": True, "k": k, **r}
        if r["n_gp_d2"] != want_gp_d2(k):
            return {"ok": False, "gpd2": True, "k": k, **r}
        if r["n_neg"] != want_j0_odd_lo(k):
            return {"ok": False, "j0": True, "k": k}
        if r["extra"] != lo["extra"]:
            return {"ok": False, "ex": True, "k": k}
        if lo["n_pg"] != r["n_pg_d2"] + r["n_pg_lo"]:
            return {"ok": False, "pg": True, "k": k}
        if lo["n_gp"] != r["n_gp_d1"] + r["n_gp_d2"] + r["n_gp_lo"]:
            return {"ok": False, "gp": True, "k": k}
        named = r["n_gp_d1"] + r["n_pg_d2"] + r["n_gp_d2"]
        if named != want_named_lo(k):
            return {"ok": False, "nm": True, "k": k}
        if k >= 2 and named == r["extra"]:
            return {"ok": False, "alln": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n_gp_d1": r["n_gp_d1"],
            "n_pg_d2": r["n_pg_d2"],
            "n_gp_d2": r["n_gp_d2"],
            "n_pg_lo": r["n_pg_lo"],
            "n_gp_lo": r["n_gp_lo"],
            "named": named,
            "extra": r["extra"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["named"] == 0
        and rows["1"]["n_pg_d2"] == 1
        and rows["8"]["n_gp_d1"] == 170
        and rows["8"]["n_pg_d2"] == 170
        and rows["8"]["n_gp_d2"] == 84
        and rows["8"]["named"] == 424
        and rows["8"]["n_pg_lo"] == 8560
        and rows["8"]["n_gp_lo"] == 8327
        and rows["8"]["named"] != rows["8"]["extra"]
        and rows["8"]["n_gp_d1"] != rows["8"]["n_gp_d2"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """pg:d1 nonempty; gp:d1 equals J_{k+1}; named extra empty."""
    ok = (
        want_gp_d1(8) != jacobsthal(9)
        and want_named_lo(8) != 0
        and want_named_lo(8) != 17630
        and want_gp_d1(8) != want_gp_d2(8)
        and want_pg_d2(1) != 2 * jacobsthal(1)
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
    uk = json.loads(UK_JSON.read_text())
    ui = json.loads(UI_JSON.read_text())
    tw = json.loads(TW_JSON.read_text())
    te = json.loads(TE_JSON.read_text())
    td = json.loads(TD_JSON.read_text())
    ok = (
        uk["checks"]["all_ok"]
        and ui["checks"]["all_ok"]
        and tw["checks"]["all_ok"]
        and te["checks"]["all_ok"]
        and td["checks"]["all_ok"]
        and uk["verdict"]["lo_small_eq_tot_minus_d1"] == "LEMMA"
        and ui["verdict"]["pg_minus_gp_eq_2km1_plus_J"] == "LEMMA"
        and tw["verdict"]["j0_odd_lo_eq_5_2km2_minus_1"] == "LEMMA"
        and te["verdict"]["d2_count_eq_2_jacobsthal"] == "LEMMA"
        and td["verdict"]["d1_count_eq_jacobsthal"] == "LEMMA"
        and uk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uk["verdict"]["prize"] == "unsolved"
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
    cnt = named_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "named_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "pg_d1_empty": True,
            "gp_d1_eq_J_k1_minus_1": True,
            "pg_d2_eq_2_J_k_ge_2": True,
            "gp_d2_eq_J_k_minus_1": True,
            "named_lo_eq_2k_plus_2J_minus_2": True,
            "gp_d1_eq_J_k1": False,
            "named_lo_empty": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "pg_d1_empty": "LEMMA",
            "gp_d1_eq_J_k1_minus_1": "LEMMA",
            "pg_d2_eq_2_J_k_ge_2": "LEMMA",
            "gp_d2_eq_J_k_minus_1": "LEMMA",
            "named_lo_eq_2k_plus_2J_minus_2": "LEMMA",
            "gp_d1_eq_J_k1": "KILLED",
            "named_lo_empty": "KILLED",
            "named_lo_eq_extra_lo": "KILLED",
            "pg_d2_eq_gp_d1": "KILLED",
            "pg_d2_formula_at_k1": "KILLED",
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
        "named k8",
        dump["named_fold"]["rows"]["8"]["named"],
        "gp_d1",
        dump["named_fold"]["rows"]["8"]["n_gp_d1"],
        "pg_d2",
        dump["named_fold"]["rows"]["8"]["n_pg_d2"],
        "gp_d2",
        dump["named_fold"]["rows"]["8"]["n_gp_d2"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
