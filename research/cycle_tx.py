#!/usr/bin/env python3
"""Cycle TX: leftover count recurrence lo(k)=2 lo(k-1)+4 J_k+extra.

Even leftover is parent leftover plus 2 J_k (Cycle TU). Odd leftover
is even leftover plus odd-n even-j extra (Cycles TV/TW). Hence
leftover(k)=2 leftover(k-1)+4 J_k+extra(k) for k>=2. Extra is
nonempty for k>=1, so the 4 J_k recurrence without extra fails.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tx.py --certify
Dump: research/cycle_tx.json
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
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering, want_even_lo_inc
from cycle_tv import leftover_j_split
from cycle_tw import want_j0_odd_lo
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TW_JSON = Path(__file__).resolve().parent / "cycle_tw.json"
TU_JSON = Path(__file__).resolve().parent / "cycle_tu.json"
TV_JSON = Path(__file__).resolve().parent / "cycle_tv.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_lo_rec(lo_prev: int, extra: int, k: int) -> int:
    """leftover(k)=2 leftover(k-1)+4 J_k+extra for k>=2."""
    return 2 * lo_prev + 4 * jacobsthal(k) + extra


def tot_form() -> dict:
    """k<=64: 4 J_k=2 even-inc; j=0 extra lower bound; unique even."""
    n_ok = 0
    if want_lo_rec(4, 10, 2) != 22:
        return {"ok": False, "k2": True}
    if want_j0_odd_lo(1) != 1 or want_j0_odd_lo(2) != 4:
        return {"ok": False, "j0": True}
    for k in range(0, K_ALG + 1):
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 2:
            if 2 * want_even_lo_inc(k) != 4 * jacobsthal(k):
                return {"ok": False, "inc": True, "k": k}
            if want_even_lo_inc(k) != 2 * jacobsthal(k):
                return {"ok": False, "d2": True, "k": k}
        if k >= 1 and want_j0_odd_lo(k) < 1:
            return {"ok": False, "ex": True, "k": k}
        if k >= 3 and want_j0_odd_lo(k) != 2 * want_j0_odd_lo(k - 1) + 1:
            return {"ok": False, "j0r": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_lo_rec(0, 2, 1) != 4
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def leftover_rec() -> dict:
    """k<=8: lo=2 lo_e+extra; k>=2 recurrence; extra nonempty."""
    n_ok = 0
    rows = {}
    prev_lo = None
    for k in range(0, K_COUNT + 1):
        r = leftover_j_split(k)
        extra = r["lo_ej_o"]
        if r["lo"] != 2 * r["lo_e"] + extra:
            return {"ok": False, "sum": True, "k": k, **r}
        if extra != r["lo_o"] - r["lo_e"]:
            return {"ok": False, "tv": True, "k": k}
        if extra < want_j0_odd_lo(k):
            return {"ok": False, "j0": True, "k": k, "extra": extra}
        if k >= 2:
            want = want_lo_rec(prev_lo, extra, k)
            if r["lo"] != want:
                return {"ok": False, "rec": True, "k": k, "lo": r["lo"], "want": want}
            if r["lo_e"] != prev_lo + want_even_lo_inc(k):
                return {"ok": False, "einc": True, "k": k}
            no_ex = 2 * prev_lo + 4 * jacobsthal(k)
            if r["lo"] == no_ex:
                return {"ok": False, "noex": True, "k": k}
        if k >= 1 and extra == 0:
            return {"ok": False, "empty": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "lo": r["lo"],
            "lo_e": r["lo_e"],
            "extra": extra,
        }
        prev_lo = r["lo"]
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["lo"] == 0
        and rows["1"]["lo"] == 4
        and rows["2"]["lo"] == 22
        and rows["8"]["lo"] == 45858
        and rows["8"]["extra"] == 17630
        and rows["8"]["lo"] != 2 * rows["7"]["lo"] + 4 * jacobsthal(8)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """leftover 2-folds parent; recurrence without extra."""
    ok = (
        want_lo_rec(4, 0, 2) != 22
        and want_lo_rec(4, 10, 2) == 22
        and want_j0_odd_lo(2) == 4
        and leftover_j_split(2)["lo_ej_o"] == 10
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
    tw = json.loads(TW_JSON.read_text())
    tu = json.loads(TU_JSON.read_text())
    tv = json.loads(TV_JSON.read_text())
    ok = (
        tw["checks"]["all_ok"]
        and tu["checks"]["all_ok"]
        and tv["checks"]["all_ok"]
        and tu["verdict"]["even_lo_eq_parent_lo_plus_d2_k_ge_2"] == "LEMMA"
        and tv["verdict"]["oddj_lo_eq_even_lo"] == "LEMMA"
        and tw["verdict"]["odd_ej_lo_from_parent_pair_xor"] == "LEMMA"
        and tw["verdict"]["j0_odd_lo_eq_5_2km2_minus_1"] == "LEMMA"
        and tw["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tw["verdict"]["prize"] == "unsolved"
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
    cnt = leftover_rec()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TX",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "leftover_rec": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_eq_2_even_plus_extra": True,
            "lo_rec_2prev_4J_extra_k_ge_2": True,
            "lo_rec_without_extra": False,
            "lo_eq_2_parent_lo": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_eq_2_even_plus_extra": "LEMMA",
            "lo_rec_2prev_4J_extra_k_ge_2": "LEMMA",
            "lo_rec_without_extra": "KILLED",
            "lo_eq_2_parent_lo": "KILLED",
            "odd_ej_lo_empty": "KILLED",
            "odd_lo_eq_even_lo": "KILLED",
            "leftover_pairs_empty": "KILLED",
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
        "lo k8",
        dump["leftover_rec"]["rows"]["8"]["lo"],
        "extra",
        dump["leftover_rec"]["rows"]["8"]["extra"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
