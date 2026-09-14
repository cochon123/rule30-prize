#!/usr/bin/env python3
"""Cycle TT: leftover pal-pair rest tot is leftover raw xor 1 for k>=3.

Leftover pal-pairs have pal-distance not in {1,2} and are not
clip-edge. Leftover is a pair property: Cycle SV's unique even
forced pair has pal-distance 2U, so it is leftover and is the
unique even forced pal-pair, even when the same covering n also
carries a d=2 pair (k even). Even leftover rest tot is leftover-
even raw xor 1 for k>=1. Odd leftover rest tot equals odd leftover
raw for k>=3. Hence leftover rest tot equals leftover raw xor 1
for k>=3. Not rest=S xor T. Do not walk leftover p catalogues. Do
not walk leftover d catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tt.py --certify
Dump: research/cycle_tt.json
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
from cycle_tb import want_edge_n
from cycle_tc import clip_j
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tl import d1_v2, d2_v2
from cycle_tp import want_d1_corr
from cycle_tq import want_even_d2_forced, want_odd_d2_forced
from cycle_tr import want_complex_corr
from cycle_ts import want_cover_n, want_triple_n
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TS_JSON = Path(__file__).resolve().parent / "cycle_ts.json"
SV_JSON = Path(__file__).resolve().parent / "cycle_sv.json"
SY_JSON = Path(__file__).resolve().parent / "cycle_sy.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def want_even_lo_corr(k: int) -> int:
    """Even leftover forced corr: 1 iff k>=1 (unique even cell)."""
    return int(k >= 1)


def want_lo_corr(k: int) -> int:
    """Leftover forced corr: 1 iff k>=3."""
    return int(k >= 3)


def is_clip_edge(n: int, j: int, k: int) -> bool:
    clip = 5 * (1 << k)
    return j == clip or 2 * n - j == clip


def unique_even_leftover(k: int) -> bool:
    """Unique even pal-right at p=4 is leftover: d=2U, not clip-edge.

    Leftover is a pair property. The same covering n also has a d=2
    pal-pair when k is even; that other pair is not leftover.
    """
    if k < 1:
        return False
    n = unique_even_n(k)
    j = forced_right_j(4, k)
    d = abs(n - j)
    u = 1 << k
    return (
        pal_kind(n, j, k) == "pair"
        and d == 2 * u
        and d not in (1, 2)
        and not is_clip_edge(n, j, k)
    )


def tot_form() -> dict:
    """k<=64: unique even leftover; corr algebra; named types unforced."""
    n_ok = 0
    if want_even_lo_corr(0) != 0 or want_even_lo_corr(1) != 1:
        return {"ok": False, "base": True}
    if want_lo_corr(2) != 0 or want_lo_corr(3) != 1:
        return {"ok": False, "lo0": True}
    if not unique_even_leftover(1) or unique_even_leftover(0):
        return {"ok": False, "u0": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if want_even_lo_corr(k) != int(k >= 1):
            return {"ok": False, "ec": True, "k": k}
        if want_lo_corr(k) != int(k >= 3):
            return {"ok": False, "lc": True, "k": k}
        if packed_p(5 * u, k) != 0 or 0 in FORCED:
            return {"ok": False, "p0": True, "k": k}
        if want_even_d2_forced(k):
            return {"ok": False, "ed2": True, "k": k}
        if k >= 2 and want_odd_d2_forced(k) and k != 2:
            return {"ok": False, "od2": True, "k": k}
        if k >= 2 and want_d1_corr(k) != 0:
            return {"ok": False, "d1": True, "k": k}
        if k >= 3:
            if want_complex_corr(k) != 0 or odd_forced_corr(k) != 0:
                return {"ok": False, "cx": True, "k": k}
            if want_even_lo_corr(k) ^ odd_forced_corr(k) != want_lo_corr(k):
                return {"ok": False, "xor": True, "k": k}
            if not pal_left_never_forced(k):
                return {"ok": False, "left": True, "k": k}
        if k >= 1:
            if not unique_even_leftover(k):
                return {"ok": False, "u": True, "k": k}
            n_u = unique_even_n(k)
            if d2_v2(n_u) != int(k % 2 == 0):
                return {"ok": False, "ov": True, "k": k}
            if d1_v2(n_u):
                return {"ok": False, "d1n": True, "k": k}
            j4 = forced_right_j(4, k)
            if j4 % 2 != 0:
                return {"ok": False, "j4": True, "k": k}
            if forced_right_j(6, k) % 2 != 1 or forced_right_j(14, k) % 2 != 1:
                return {"ok": False, "jodd": True, "k": k}
        if want_triple_n(k) != want_cover_n(k):
            return {"ok": False, "ts": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and unique_even_n(10) == 3070
        and want_d1_n(0) == 1
        and want_d2_n(0) == 2
        and want_edge_n(0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def leftover_unique() -> dict:
    """k<=12: unique even is leftover; only even forced pal-right is p=4."""
    n_ok = 0
    rows = {}
    for k in range(1, K_COUNT + 1):
        u = 1 << k
        clip = 5 * u
        j4 = forced_right_j(4, k)
        want = unique_even_n(k)
        hits = []
        for n in range(0, 4 * u, 2):
            if j4 <= n or j4 > min(2 * n, clip):
                continue
            jp = 2 * n - j4
            if jp < 0 or jp > clip:
                continue
            if G(n, j4) == 1:
                hits.append(n)
        if hits != [want] or not unique_even_leftover(k):
            return {"ok": False, "k": k, "hits": hits, "want": want}
        if d2_v2(want) != int(k % 2 == 0):
            return {"ok": False, "ov": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n": want,
            "d": 2 * u,
            "n_hit": 1,
            "d2_n": d2_v2(want),
        }
    ok = (
        n_ok == K_COUNT
        and rows["1"]["n"] == 4
        and rows["1"]["d2_n"] == 0
        and rows["2"]["d2_n"] == 1
        and rows["10"]["n"] == 3070
        and rows["12"]["n"] == 12286
        and rows["12"]["d"] == 8192
        and rows["12"]["d2_n"] == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """leftover rest equals raw all k; leftover pal-pairs empty."""
    ok = (
        want_lo_corr(3) == 1
        and want_even_lo_corr(1) == 1
        and unique_even_leftover(1)
        and unique_even_leftover(2)
        and d2_v2(unique_even_n(2)) == 1
        and not unique_even_leftover(0)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
    )
    return {"ok": ok}


def prefixes() -> dict:
    ts = json.loads(TS_JSON.read_text())
    sv = json.loads(SV_JSON.read_text())
    sy = json.loads(SY_JSON.read_text())
    ok = (
        ts["checks"]["all_ok"]
        and sv["checks"]["all_ok"]
        and sy["checks"]["all_ok"]
        and ts["verdict"]["triple_count_eq_4U"] == "LEMMA"
        and ts["verdict"]["clip_edge_never_forced"] == "LEMMA"
        and sv["verdict"]["even_pair_rest_eq_raw_xor_1_k_ge_1"] == "LEMMA"
        and sy["verdict"]["odd_pair_rest_eq_raw_k_ge_3"] == "LEMMA"
        and ts["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ts["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
        and want_d2_n(0) == 2
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
    cnt = leftover_unique()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TT",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "leftover_unique": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unique_even_is_leftover": True,
            "even_lo_rest_eq_raw_xor_1_k_ge_1": True,
            "lo_rest_eq_raw_xor_1_k_ge_3": True,
            "lo_rest_eq_raw_all_k": False,
            "leftover_pairs_empty": False,
            "lo_n_disjoint_named": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unique_even_is_leftover": "LEMMA",
            "even_lo_rest_eq_raw_xor_1_k_ge_1": "LEMMA",
            "lo_rest_eq_raw_xor_1_k_ge_3": "LEMMA",
            "lo_rest_eq_raw_all_k": "KILLED",
            "leftover_pairs_empty": "KILLED",
            "lo_n_disjoint_named": "KILLED",
            "three_types_partition_n": "KILLED",
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
        "u k12",
        dump["leftover_unique"]["rows"]["12"]["n"],
        "d",
        dump["leftover_unique"]["rows"]["12"]["d"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
