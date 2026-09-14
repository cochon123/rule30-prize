#!/usr/bin/env python3
"""Cycle TU: even leftover count is parent leftover plus parent d=2.

For k>=1 the pal-pair types {d=1, d=2, clip-edge, leftover}
partition pal-pairs, so leftover count is pal-pair count minus
2^{k+2}. Even pal-pairs 2-fold all parent pal-pairs (Cycle TA),
distance doubles, clip matches, so even leftover count at k>=2
equals leftover(k-1)+2 J_k. Dies at k=1: parent d=2 overlaps
clip-edge. Not rest=S xor T. Do not walk leftover p catalogues.
Do not walk leftover d catalogues. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tu.py --certify
Dump: research/cycle_tu.json
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
from cycle_ts import want_cover_n, want_triple_n
from cycle_tt import is_clip_edge, unique_even_leftover
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TT_JSON = Path(__file__).resolve().parent / "cycle_tt.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def d1_clip_n(k: int) -> int:
    """Covering n whose d=1 partner would be clip-edge: 5U-1."""
    return 5 * (1 << k) - 1


def d2_clip_n(k: int) -> int:
    """Covering n whose d=2 partner is clip-edge: 5U-2."""
    return 5 * (1 << k) - 2


def d2_clip_covering(k: int) -> bool:
    """d=2 overlaps clip-edge iff n=5U-2 is covering, i.e. k=0."""
    n = d2_clip_n(k)
    return 0 <= n < 4 * (1 << k)


def want_even_lo_inc(k: int) -> int:
    """Even leftover count increment: parent d=2 count 2 J_k, k>=2."""
    return want_d2_n(k - 1)


def leftover_split(k: int) -> dict:
    """Pal-pair type counts: d=1, d=2, clip-edge, leftover."""
    u = 1 << k
    clip = 5 * u
    n_lo = n_lo_e = n_lo_o = 0
    n_d1 = n_d2 = n_edge = n_pair = 0
    for n in range(0, 4 * u):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            n_pair += 1
            d = n - j
            if d == 1:
                n_d1 += 1
                continue
            if d == 2:
                n_d2 += 1
                continue
            if is_clip_edge(n, j, k):
                n_edge += 1
                continue
            n_lo += 1
            if n % 2 == 0:
                n_lo_e += 1
            else:
                n_lo_o += 1
    return {
        "pair": n_pair,
        "d1": n_d1,
        "d2": n_d2,
        "edge": n_edge,
        "lo": n_lo,
        "lo_e": n_lo_e,
        "lo_o": n_lo_o,
    }


def tot_form() -> dict:
    """k<=64: d=1 never clip-edge; d=2 clip-edge iff k=0; 2-fold inc."""
    n_ok = 0
    if d2_clip_covering(0) is not True or d2_clip_n(0) != 3:
        return {"ok": False, "k0": True}
    if d2_clip_covering(1) or d1_clip_n(0) < 4:
        return {"ok": False, "k1": True}
    if want_even_lo_inc(2) != 2 or want_d2_n(1) != 2:
        return {"ok": False, "inc0": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d1_clip_n(k) < 4 * u:
            return {"ok": False, "d1c": True, "k": k}
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_d1_n(k) + want_d2_n(k) + want_edge_n(k) != want_cover_n(k):
            return {"ok": False, "tri": True, "k": k}
        if want_triple_n(k) != want_cover_n(k):
            return {"ok": False, "ts": True, "k": k}
        if k >= 2:
            if want_even_lo_inc(k) != 2 * jacobsthal(k):
                return {"ok": False, "inc": True, "k": k}
            if want_even_lo_inc(k) != want_d2_n(k - 1):
                return {"ok": False, "d2p": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_cover_n(8) == 1024
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def leftover_fold() -> dict:
    """k<=8: pair types partition for k>=1; even leftover 2-fold k>=2."""
    n_ok = 0
    rows = {}
    prev_lo = None
    for k in range(0, K_COUNT + 1):
        r = leftover_split(k)
        if r["d1"] != want_d1_n(k) or r["d2"] != want_d2_n(k):
            return {"ok": False, "named": True, "k": k, **r}
        if k >= 1:
            if r["edge"] != want_edge_n(k):
                return {"ok": False, "edge": True, "k": k, **r}
            if r["d1"] + r["d2"] + r["edge"] + r["lo"] != r["pair"]:
                return {"ok": False, "part": True, "k": k}
            if r["lo"] != r["pair"] - want_cover_n(k):
                return {"ok": False, "lo": True, "k": k}
            if r["d1"] + r["d2"] + r["edge"] != want_cover_n(k):
                return {"ok": False, "tri": True, "k": k}
        else:
            if r["edge"] != 0 or r["lo"] != 0 or r["pair"] != 3:
                return {"ok": False, "k0": True, **r}
        if k >= 2:
            if prev_lo is None or r["lo_e"] != prev_lo + want_even_lo_inc(k):
                return {
                    "ok": False,
                    "fold": True,
                    "k": k,
                    "lo_e": r["lo_e"],
                    "want": None if prev_lo is None else prev_lo + want_even_lo_inc(k),
                }
        if k == 1:
            if r["lo_e"] != 1 or prev_lo + want_d2_n(0) == r["lo_e"]:
                return {"ok": False, "k1": True, "lo_e": r["lo_e"]}
        n_ok += 1
        rows[str(k)] = {
            "pair": r["pair"],
            "lo": r["lo"],
            "lo_e": r["lo_e"],
            "lo_o": r["lo_o"],
        }
        prev_lo = r["lo"]
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["lo"] == 0
        and rows["1"]["lo"] == 4
        and rows["1"]["lo_e"] == 1
        and rows["2"]["lo_e"] == 6
        and rows["8"]["lo"] == 45858
        and rows["8"]["lo_e"] == 14114
        and rows["8"]["pair"] == 46882
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """four types partition pairs all k; even leftover = parent leftover."""
    ok = (
        d2_clip_covering(0)
        and not d2_clip_covering(1)
        and d1_clip_n(3) >= 4 * 8
        and want_even_lo_inc(2) == 2
        and unique_even_leftover(1)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
    )
    return {"ok": ok}


def prefixes() -> dict:
    tt = json.loads(TT_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    te = json.loads(TE_JSON.read_text())
    ok = (
        tt["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and te["checks"]["all_ok"]
        and tt["verdict"]["lo_rest_eq_raw_xor_1_k_ge_3"] == "LEMMA"
        and tt["verdict"]["unique_even_is_leftover"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and te["verdict"]["d2_count_eq_2_jacobsthal"] == "LEMMA"
        and tt["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tt["verdict"]["prize"] == "unsolved"
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
    cnt = leftover_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "leftover_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "pair_types_partition_k_ge_1": True,
            "lo_count_eq_pair_minus_4U_k_ge_1": True,
            "even_lo_eq_parent_lo_plus_d2_k_ge_2": True,
            "pair_types_partition_all_k": False,
            "even_lo_eq_parent_lo": False,
            "even_lo_fold_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "pair_types_partition_k_ge_1": "LEMMA",
            "lo_count_eq_pair_minus_4U_k_ge_1": "LEMMA",
            "even_lo_eq_parent_lo_plus_d2_k_ge_2": "LEMMA",
            "pair_types_partition_all_k": "KILLED",
            "even_lo_eq_parent_lo": "KILLED",
            "even_lo_fold_all_k": "KILLED",
            "leftover_pairs_empty": "KILLED",
            "lo_n_disjoint_named": "KILLED",
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
        dump["leftover_fold"]["rows"]["8"]["lo"],
        "lo_e",
        dump["leftover_fold"]["rows"]["8"]["lo_e"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
