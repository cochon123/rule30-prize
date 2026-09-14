#!/usr/bin/env python3
"""Cycle TY: pal-pair count is 2 parent pair + 4 J_k + extra.

For k>=1 pal-pair count is leftover plus 2^{k+2} (Cycle TU partition).
The leftover recurrence then gives pair(k)=2 pair(k-1)+4 J_k+extra(k)
for k>=2. Cycle TA even pal-pairs 2-fold the parent, so odd pal-pair
count is parent pal-pair plus 4 J_k plus extra. Not rest=S xor T.
Do not walk leftover p catalogues. Do not walk leftover d catalogues.
Do not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_ty.py --certify
Dump: research/cycle_ty.json
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
from cycle_ta import pal_split
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_ts import want_cover_n
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering, want_even_lo_inc
from cycle_tv import leftover_j_split
from cycle_tw import want_j0_odd_lo
from cycle_tx import want_lo_rec
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TX_JSON = Path(__file__).resolve().parent / "cycle_tx.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
TU_JSON = Path(__file__).resolve().parent / "cycle_tu.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_pair_from_lo(lo: int, k: int) -> int:
    """Pal-pair count = leftover + 2^{k+2} for k>=1."""
    return lo + want_cover_n(k)


def want_pair_rec(pair_prev: int, extra: int, k: int) -> int:
    """pair(k)=2 pair(k-1)+4 J_k+extra for k>=2."""
    return 2 * pair_prev + 4 * jacobsthal(k) + extra


def tot_form() -> dict:
    """k<=64: pair-from-lo vs rec; even 2-fold increment; j=0 extra."""
    n_ok = 0
    if want_pair_from_lo(4, 1) != 12 or want_pair_from_lo(22, 2) != 38:
        return {"ok": False, "base": True}
    if want_pair_rec(12, 10, 2) != 38:
        return {"ok": False, "rec2": True}
    if want_lo_rec(4, 10, 2) != 22:
        return {"ok": False, "lo2": True}
    for k in range(0, K_ALG + 1):
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 1:
            if want_cover_n(k) != 1 << (k + 2):
                return {"ok": False, "cov": True, "k": k}
            if not unique_even_leftover(k):
                return {"ok": False, "u": True, "k": k}
            if want_j0_odd_lo(k) < 1:
                return {"ok": False, "ex": True, "k": k}
        if k >= 2:
            if 2 * want_even_lo_inc(k) != 4 * jacobsthal(k):
                return {"ok": False, "inc": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_pair_rec(12, 0, 2) != 38
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def pair_rec() -> dict:
    """k<=8: pair=lo+4U; pair rec; even pair=parent pair; odd rec."""
    n_ok = 0
    rows = {}
    prev_pair = None
    prev_lo = None
    for k in range(0, K_COUNT + 1):
        r = leftover_j_split(k)
        extra = r["lo_ej_o"]
        ev = pal_split(k, 0)
        od = pal_split(k, 1)
        pair = ev["n_pair"] + od["n_pair"]
        if k >= 1:
            if pair != want_pair_from_lo(r["lo"], k):
                return {"ok": False, "fromlo": True, "k": k, "pair": pair, "lo": r["lo"]}
        else:
            if pair != 3 or r["lo"] != 0:
                return {"ok": False, "k0": True, "pair": pair}
        if k >= 2:
            want = want_pair_rec(prev_pair, extra, k)
            if pair != want:
                return {"ok": False, "rec": True, "k": k, "pair": pair, "want": want}
            if ev["n_pair"] != prev_pair:
                return {"ok": False, "even": True, "k": k, "ev": ev["n_pair"]}
            odd_pair = od["n_pair"]
            if odd_pair != prev_pair + 4 * jacobsthal(k) + extra:
                return {"ok": False, "odd": True, "k": k, "odd_pair": odd_pair}
            if pair == 2 * prev_pair + 4 * jacobsthal(k):
                return {"ok": False, "noex": True, "k": k}
            if r["lo"] != want_lo_rec(prev_lo, extra, k):
                return {"ok": False, "lo": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "pair": pair,
            "lo": r["lo"],
            "extra": extra,
            "even_pair": ev["n_pair"],
            "odd_pair": od["n_pair"],
        }
        prev_pair = pair
        prev_lo = r["lo"]
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["pair"] == 3
        and rows["1"]["pair"] == 12
        and rows["2"]["pair"] == 38
        and rows["8"]["pair"] == 46882
        and rows["8"]["even_pair"] == 14456
        and rows["8"]["odd_pair"] == 32426
        and rows["8"]["pair"] != 2 * rows["7"]["pair"] + 4 * jacobsthal(8)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """pair 2-folds parent; recurrence without extra."""
    ok = (
        want_pair_rec(12, 0, 2) != 38
        and want_pair_rec(12, 10, 2) == 38
        and want_pair_from_lo(0, 0) != 3
        and want_j0_odd_lo(2) == 4
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
    tx = json.loads(TX_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    tu = json.loads(TU_JSON.read_text())
    ok = (
        tx["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and tu["checks"]["all_ok"]
        and tx["verdict"]["lo_rec_2prev_4J_extra_k_ge_2"] == "LEMMA"
        and tu["verdict"]["pair_types_partition_k_ge_1"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and tx["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tx["verdict"]["prize"] == "unsolved"
        and want_d2_n(0) == 2
        and jacobsthal(2) == 1
        and want_cover_n(0) == 4
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
    cnt = pair_rec()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TY",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "pair_rec": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "pair_eq_lo_plus_4U_k_ge_1": True,
            "pair_rec_2prev_4J_extra_k_ge_2": True,
            "odd_pair_eq_parent_plus_4J_extra": True,
            "pair_rec_without_extra": False,
            "pair_eq_2_parent_pair": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "pair_eq_lo_plus_4U_k_ge_1": "LEMMA",
            "pair_rec_2prev_4J_extra_k_ge_2": "LEMMA",
            "odd_pair_eq_parent_plus_4J_extra": "LEMMA",
            "pair_rec_without_extra": "KILLED",
            "pair_eq_2_parent_pair": "KILLED",
            "lo_rec_without_extra": "KILLED",
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
        "pair k8",
        dump["pair_rec"]["rows"]["8"]["pair"],
        "odd",
        dump["pair_rec"]["rows"]["8"]["odd_pair"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
