#!/usr/bin/env python3
"""Cycle UF: even leftover plus even unpaired is lo_unp(k-1)+2 J_k.

For k>=2, even leftover is leftover(k-1)+2 J_k (Cycle TU) and even
unpaired is unpaired(k-1) (Cycle TZ). Cycle UE leftover plus unpaired
at k-1 then gives the sum. k=1 matches the same closed form by
census; using leftover+unpaired at k=0 plus 2 J_1 overcounts.
Do not PREFIX leftover extra or unpaired extra separately. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_uf.py --certify
Dump: research/cycle_uf.json
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
from cycle_tu import d2_clip_covering, want_even_lo_inc
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UE_JSON = Path(__file__).resolve().parent / "cycle_ue.json"
TU_JSON = Path(__file__).resolve().parent / "cycle_tu.json"
TZ_JSON = Path(__file__).resolve().parent / "cycle_tz.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_even_lo_unp(k: int) -> int:
    """Even leftover plus even unpaired: lo_unp(k-1)+2 J_k for k>=1."""
    return want_lo_unp(k - 1) + 2 * jacobsthal(k)


def want_odd_lo_unp(k: int) -> int:
    """Odd leftover plus odd unpaired for k>=1."""
    return want_lo_unp(k) - want_even_lo_unp(k)


def even_lo_unp_split(k: int) -> dict:
    """Leftover and unpaired pal-left cells split by n-parity."""
    u = 1 << k
    clip = 5 * u
    lo = lo_e = unp = unp_e = 0
    for n in range(0, 4 * u):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            kind = pal_kind(n, j, k)
            if kind == "unp":
                if j >= n:
                    continue
                unp += 1
                if n % 2 == 0:
                    unp_e += 1
            elif kind == "pair" and j < 2 * n - j:
                d = n - j
                if d == 1 or d == 2 or is_clip_edge(n, j, k):
                    continue
                lo += 1
                if n % 2 == 0:
                    lo_e += 1
    return {
        "lo": lo,
        "lo_e": lo_e,
        "lo_o": lo - lo_e,
        "unp": unp,
        "unp_e": unp_e,
        "unp_o": unp - unp_e,
        "even": lo_e + unp_e,
        "odd": (lo - lo_e) + (unp - unp_e),
    }


def tot_form() -> dict:
    """k<=64: even lo+unp closed form; TU increment; k=1 not parent leftover."""
    n_ok = 0
    if want_even_lo_unp(1) != 2 or want_odd_lo_unp(1) != 6:
        return {"ok": False, "k1": True}
    if want_even_lo_unp(8) != 22186 or want_odd_lo_unp(8) != 50006:
        return {"ok": False, "k8": True}
    if want_even_lo_unp(1) == 1 + 2 * jacobsthal(1):
        return {"ok": False, "k1p": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
        if k >= 1:
            if want_even_lo_unp(k) != want_lo_unp(k - 1) + 2 * jacobsthal(k):
                return {"ok": False, "sum": True, "k": k}
            if want_even_lo_unp(k) != (1 << k) * (fib(k + 3) - 3) + 2 * jacobsthal(
                k
            ):
                return {"ok": False, "F": True, "k": k}
            if want_odd_lo_unp(k) != want_lo_unp(k) - want_even_lo_unp(k):
                return {"ok": False, "odd": True, "k": k}
            if want_even_lo_unp(k) + want_odd_lo_unp(k) != want_lo_unp(k):
                return {"ok": False, "part": True, "k": k}
        if k >= 2:
            if want_even_lo_inc(k) != 2 * jacobsthal(k):
                return {"ok": False, "inc": True, "k": k}
            if want_even_lo_unp(k) != want_lo_unp(k - 1) + want_even_lo_inc(k):
                return {"ok": False, "comp": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        if 4 * u >= 5 * u:
            return {"ok": False, "clip": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and G(2, 2) != 0
        and want_pal_c(1) != (1 << 2)
        and want_pair_unp(1) != (1 << 3)
        and want_lo_unp(1) != 4
        and want_even_lo_unp(2) != 8
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def even_lo_unp_fold() -> dict:
    """k<=8: even leftover+unpaired closed for k>=1; dies at k=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = even_lo_unp_split(k)
        if r["even"] != r["lo_e"] + r["unp_e"]:
            return {"ok": False, "e": True, "k": k, **r}
        if r["odd"] != r["lo_o"] + r["unp_o"]:
            return {"ok": False, "o": True, "k": k, **r}
        if r["lo"] + r["unp"] != r["even"] + r["odd"]:
            return {"ok": False, "sum": True, "k": k, **r}
        if k >= 1:
            if r["lo"] + r["unp"] != want_lo_unp(k):
                return {"ok": False, "lu": True, "k": k, **r}
            if r["even"] != want_even_lo_unp(k):
                return {"ok": False, "ev": True, "k": k, **r}
            if r["odd"] != want_odd_lo_unp(k):
                return {"ok": False, "od": True, "k": k, **r}
            if r["lo_e"] == r["unp_e"] and k >= 2:
                return {"ok": False, "eq": True, "k": k, **r}
        else:
            if r["lo"] != 0 or r["unp"] != 1 or r["even"] != 0:
                return {"ok": False, "k0": True, **r}
        n_ok += 1
        rows[str(k)] = {
            "lo": r["lo"],
            "lo_e": r["lo_e"],
            "unp": r["unp"],
            "unp_e": r["unp_e"],
            "even": r["even"],
            "odd": r["odd"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["even"] == 0
        and rows["0"]["unp"] == 1
        and rows["1"]["even"] == 2
        and rows["1"]["odd"] == 6
        and rows["1"]["lo_e"] == 1
        and rows["1"]["unp_e"] == 1
        and rows["1"]["even"] != 3
        and rows["2"]["even"] == 10
        and rows["2"]["lo_e"] != rows["2"]["unp_e"]
        and rows["8"]["even"] == 22186
        and rows["8"]["odd"] == 50006
        and rows["8"]["lo"] + rows["8"]["unp"] == 72192
        and rows["8"]["even"] != (1 << 10)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """Parent leftover+unp plus 2 J at k=1; even leftover equals unpaired."""
    ok = (
        want_even_lo_unp(1) != 3
        and want_even_lo_unp(2) != 8
        and want_lo_unp(8) != 45858
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
    ue = json.loads(UE_JSON.read_text())
    tu = json.loads(TU_JSON.read_text())
    tz = json.loads(TZ_JSON.read_text())
    ok = (
        ue["checks"]["all_ok"]
        and tu["checks"]["all_ok"]
        and tz["checks"]["all_ok"]
        and ue["verdict"]["lo_unp_eq_2km1_Fm3_k_ge_1"] == "LEMMA"
        and tu["verdict"]["even_lo_eq_parent_lo_plus_d2_k_ge_2"] == "LEMMA"
        and tz["verdict"]["even_unp_eq_parent_unp"] == "LEMMA"
        and ue["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ue["verdict"]["prize"] == "unsolved"
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
    cnt = even_lo_unp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UF",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "even_lo_unp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_lo_unp_eq_parent_lu_plus_2J_k_ge_1": True,
            "odd_lo_unp_eq_lu_minus_even_k_ge_1": True,
            "even_lo_unp_eq_actual_parent_lu_plus_2J": False,
            "even_lo_eq_even_unp": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_lo_unp_eq_parent_lu_plus_2J_k_ge_1": "LEMMA",
            "odd_lo_unp_eq_lu_minus_even_k_ge_1": "LEMMA",
            "even_lo_unp_eq_actual_parent_lu_plus_2J": "KILLED",
            "even_lo_eq_even_unp": "KILLED",
            "lo_eq_2km1_Fm3": "KILLED",
            "lo_unp_eq_form_k0": "KILLED",
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
        "even k8",
        dump["even_lo_unp_fold"]["rows"]["8"]["even"],
        "odd",
        dump["even_lo_unp_fold"]["rows"]["8"]["odd"],
        "lo_e",
        dump["even_lo_unp_fold"]["rows"]["8"]["lo_e"],
        "unp_e",
        dump["even_lo_unp_fold"]["rows"]["8"]["unp_e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
