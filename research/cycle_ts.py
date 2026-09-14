#!/usr/bin/env python3
"""Cycle TS: {d=1,d=2,clip-edge} pair count is 2^{k+2}.

The three pal-pair types d=1, d=2, and clip-edge have total count
J_{k+3}+J_{k+2}=2^{k+2}, equal to the covering-clock count 4U.
Clip-edge packed pal-right is p=0, never forced, and Cycle TC
gives raw=0 cellwise, so the triple rest tot equals the TG-complex
rest tot. Not a partition of covering n. Leftover pal-pairs are
nonempty (unique even cell, pal-distance 2U). Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_ts.py --certify
Dump: research/cycle_ts.json
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
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import packed_p
from cycle_sv import forced_right_j, pal_left_never_forced, unique_even_n
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal, want_edge_n
from cycle_tc import clip_j
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tl import d1_v2, d2_v2
from cycle_tr import want_complex_corr, want_complex_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TR_JSON = Path(__file__).resolve().parent / "cycle_tr.json"
TQ_JSON = Path(__file__).resolve().parent / "cycle_tq.json"
TC_JSON = Path(__file__).resolve().parent / "cycle_tc.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def want_cover_n(k: int) -> int:
    """Covering-clock count: 4U = 2^{k+2}."""
    return 1 << (k + 2)


def want_triple_n(k: int) -> int:
    """{d=1,d=2,clip-edge} pal-pair count: 2^{k+2}."""
    return want_cover_n(k)


def tot_form() -> dict:
    """k<=64: J_{k+2}+J_{k+3}=2^{k+2}; p(5U)=0; unique even leftover."""
    n_ok = 0
    if jacobsthal(2) != 1 or jacobsthal(3) != 3:
        return {"ok": False, "J0": True}
    if want_triple_n(0) != 4 or want_d1_n(0) + want_d2_n(0) + want_edge_n(0) != 4:
        return {"ok": False, "base": True}
    if 0 in FORCED or packed_p(5, 0) != 0:
        return {"ok": False, "p0": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if jacobsthal(k + 2) + jacobsthal(k + 3) != want_cover_n(k):
            return {"ok": False, "J": True, "k": k}
        if want_complex_n(k) + want_edge_n(k) != want_triple_n(k):
            return {"ok": False, "sum": True, "k": k}
        if want_d1_n(k) + want_d2_n(k) + want_edge_n(k) != want_cover_n(k):
            return {"ok": False, "parts": True, "k": k}
        if packed_p(5 * u, k) != 0:
            return {"ok": False, "clipp": True, "k": k}
        n_hi = 4 * u - 1
        j_hi = clip_j(n_hi, k)
        if j_hi != 3 * u - 2:
            return {"ok": False, "jhi": True, "k": k}
        if packed_p(j_hi, k) != 4 * u + 4:
            return {"ok": False, "plo": True, "k": k}
        if packed_p(j_hi, k) in FORCED:
            return {"ok": False, "fr": True, "k": k}
        if k >= 1:
            n_u = unique_even_n(k)
            j_u = forced_right_j(4, k)
            if pal_kind(n_u, j_u, k) != "pair":
                return {"ok": False, "ukind": True, "k": k}
            if abs(n_u - j_u) == 2 or abs(n_u - j_u) == 1:
                return {"ok": False, "ud": True, "k": k}
            if j_u == 5 * u or clip_j(n_u, k) == j_u:
                return {"ok": False, "uedge": True, "k": k}
            if abs(n_u - j_u) != 2 * u:
                return {"ok": False, "u2u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_triple_n(7) == 512
        and want_triple_n(12) == 16384
        and want_complex_corr(0) == 1
        and want_complex_corr(2) == 0
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def triple_count() -> dict:
    """k<=12: triple count 4U; overlap; unique even leftover."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        clip = 5 * u
        n_d1 = n_d2 = n_edge = 0
        both_d1 = both_d2 = 0
        for n in range(0, 4 * u):
            is_d1 = n >= 1 and d1_v2(n)
            is_d2 = n >= 2 and d2_v2(n)
            j = 2 * n - clip
            is_edge = j >= 0 and j < n and G(n, j) == 1
            if is_d1:
                n_d1 += 1
            if is_d2:
                n_d2 += 1
            if is_edge:
                n_edge += 1
            if is_d1 and is_edge:
                both_d1 += 1
            if is_d2 and is_edge:
                both_d2 += 1
        if n_d1 != want_d1_n(k) or n_d2 != want_d2_n(k) or n_edge != want_edge_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_d1": n_d1,
                "n_d2": n_d2,
                "n_edge": n_edge,
            }
        if n_d1 + n_d2 + n_edge != want_cover_n(k):
            return {"ok": False, "sum": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n_d1": n_d1,
            "n_d2": n_d2,
            "n_edge": n_edge,
            "n_triple": n_d1 + n_d2 + n_edge,
            "both_d1": both_d1,
            "both_d2": both_d2,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["n_triple"] == 4
        and rows["1"]["both_d1"] >= 1
        and rows["7"]["n_triple"] == 512
        and rows["12"]["n_triple"] == 16384
        and rows["12"]["n_d1"] == 5461
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """three types partition covering n; leftover pal-pairs empty."""
    ok = (
        want_triple_n(0) == 4
        and want_cover_n(1) == 8
        and unique_even_n(1) == 4
        and abs(unique_even_n(1) - forced_right_j(4, 1)) == 4
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
    )
    return {"ok": ok}


def prefixes() -> dict:
    tr = json.loads(TR_JSON.read_text())
    tq = json.loads(TQ_JSON.read_text())
    tc = json.loads(TC_JSON.read_text())
    ok = (
        tr["checks"]["all_ok"]
        and tq["checks"]["all_ok"]
        and tc["checks"]["all_ok"]
        and tr["verdict"]["complex_count_eq_J_k3"] == "LEMMA"
        and tr["verdict"]["complex_rest_eq_raw_xor_k_le_1"] == "LEMMA"
        and tc["verdict"]["clip_pair_and_0_both_sides"] == "LEMMA"
        and tr["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tr["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
        and want_d2_n(0) == 2
        and want_edge_n(0) == 1
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
    cnt = triple_count()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "triple_count": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "triple_count_eq_4U": True,
            "clip_edge_never_forced": True,
            "triple_rest_eq_complex_rest": True,
            "three_types_partition_n": False,
            "leftover_pairs_empty": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "triple_count_eq_4U": "LEMMA",
            "clip_edge_never_forced": "LEMMA",
            "triple_rest_eq_complex_rest": "LEMMA",
            "three_types_partition_n": "KILLED",
            "leftover_pairs_empty": "KILLED",
            "d2_raw_eq_parent_d1": "KILLED",
            "d2_raw_eq_parent_xor_even": "KILLED",
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
        "triple k12",
        dump["triple_count"]["rows"]["12"]["n_triple"],
        "both_d1 k1",
        dump["triple_count"]["rows"]["1"]["both_d1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
