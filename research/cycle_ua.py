#!/usr/bin/env python3
"""Cycle UA: unpaired count recurrence unp(k)=2 unp(k-1)+J_{k+1}+extra.

Even unpaired is parent unpaired (Cycles TA/TZ). Odd unpaired is
odd-j unpaired plus odd-n even-j extra. Odd-j unpaired is parent
unpaired plus J_{k+1} (Cycle TZ). Hence unpaired(k)=2 unpaired(k-1)
+J_{k+1}+extra(k) for k>=1. Extra is nonempty for every k (it
contains j=0 unpaired on odd n>5U/2), so the J_{k+1} recurrence
without extra fails. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ua.py --certify
Dump: research/cycle_ua.json
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
from cycle_ta import pal_kind, pal_split
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_tz import unp_j_split, want_oddj_unp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TZ_JSON = Path(__file__).resolve().parent / "cycle_tz.json"
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_j0_odd_unp(k: int) -> int:
    """j=0 unpaired on odd n>5U/2: 1 at k<=1, then 3*2^{k-2}."""
    if k <= 1:
        return 1
    return 3 * (1 << (k - 2))


def want_unp_rec(unp_prev: int, extra: int, k: int) -> int:
    """unpaired(k)=2 unpaired(k-1)+J_{k+1}+extra for k>=1."""
    return 2 * unp_prev + jacobsthal(k + 1) + extra


def tot_form() -> dict:
    """k<=64: J_{k+1}=edge(k-1); j=0 extra lower bound; unique even."""
    n_ok = 0
    if want_unp_rec(1, 1, 1) != 4:
        return {"ok": False, "k1": True}
    if want_unp_rec(4, 7, 2) != 18:
        return {"ok": False, "k2": True}
    if want_j0_odd_unp(0) != 1 or want_j0_odd_unp(1) != 1:
        return {"ok": False, "j0": True}
    if want_j0_odd_unp(2) != 3 or want_j0_odd_unp(3) != 6:
        return {"ok": False, "j0b": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 1 and want_oddj_unp(0, k) != jacobsthal(k + 1):
            return {"ok": False, "J": True, "k": k}
        if k >= 1 and want_edge_n(k - 1) != jacobsthal(k + 1):
            return {"ok": False, "ed": True, "k": k}
        if k >= 3 and want_j0_odd_unp(k) != 2 * want_j0_odd_unp(k - 1):
            return {"ok": False, "j0r": True, "k": k}
        n = 4 * u - 1
        if pal_kind(n, 0, k) != "unp" or n % 2 == 0 or G(n, 0) != 1:
            return {"ok": False, "j0n": True, "k": k}
        if 2 * n <= clip:
            return {"ok": False, "clip": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_unp_rec(1, 0, 1) != 4
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def unpaired_rec() -> dict:
    """k<=8: unp=2 unp_e+extra; k>=1 recurrence; extra nonempty."""
    n_ok = 0
    rows = {}
    prev_unp = None
    for k in range(0, K_COUNT + 1):
        r = unp_j_split(k)
        extra = r["unp_o"] - r["unp_oj"]
        ps = pal_split(k, None)
        if r["unp"] != ps["n_unp"]:
            return {"ok": False, "ps": True, "k": k}
        if r["unp"] != 2 * r["unp_e"] + extra:
            return {"ok": False, "sum": True, "k": k, **r}
        if extra != r["unp_ej"] - r["unp_e"]:
            return {"ok": False, "ej": True, "k": k}
        if extra < want_j0_odd_unp(k):
            return {"ok": False, "j0": True, "k": k, "extra": extra}
        if extra == 0:
            return {"ok": False, "empty": True, "k": k}
        if k >= 1:
            if prev_unp is None:
                return {"ok": False, "prev": True, "k": k}
            want = want_unp_rec(prev_unp, extra, k)
            if r["unp"] != want:
                return {"ok": False, "rec": True, "k": k, "unp": r["unp"], "want": want}
            if r["unp_e"] != prev_unp:
                return {"ok": False, "even": True, "k": k}
            if r["unp_oj"] != want_oddj_unp(prev_unp, k):
                return {"ok": False, "oj": True, "k": k}
            no_ex = 2 * prev_unp + jacobsthal(k + 1)
            if r["unp"] == no_ex:
                return {"ok": False, "noex": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "unp": r["unp"],
            "unp_e": r["unp_e"],
            "extra": extra,
        }
        prev_unp = r["unp"]
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["unp"] == 1
        and rows["0"]["extra"] == 1
        and rows["1"]["unp"] == 4
        and rows["1"]["extra"] == 1
        and rows["2"]["unp"] == 18
        and rows["8"]["unp"] == 26334
        and rows["8"]["unp_e"] == 8072
        and rows["8"]["extra"] == 10019
        and rows["8"]["unp"] != 2 * rows["7"]["unp"] + jacobsthal(9)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """unpaired 2-folds parent; recurrence without extra."""
    ok = (
        want_unp_rec(1, 0, 1) != 4
        and want_unp_rec(1, 1, 1) == 4
        and want_unp_rec(4, 0, 2) != 18
        and want_unp_rec(4, 7, 2) == 18
        and want_j0_odd_unp(2) == 3
        and unp_j_split(2)["unp_o"] - unp_j_split(2)["unp_oj"] == 7
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
    tz = json.loads(TZ_JSON.read_text())
    ta = json.loads(TA_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ok = (
        tz["checks"]["all_ok"]
        and ta["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and tz["verdict"]["even_unp_eq_parent_unp"] == "LEMMA"
        and tz["verdict"]["oddj_unp_eq_parent_unp_plus_J_k1"] == "LEMMA"
        and tz["verdict"]["oddj_unp_eq_even_unp_plus_J_k1"] == "LEMMA"
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and tb["verdict"]["oddj_pairs_drop_clip_edge"] == "LEMMA"
        and tz["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tz["verdict"]["prize"] == "unsolved"
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
    cnt = unpaired_rec()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UA",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "unpaired_rec": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "unp_eq_2_even_plus_extra": True,
            "unp_rec_2prev_J_extra_k_ge_1": True,
            "j0_odd_unp_eq_3_2km2": True,
            "unp_rec_without_extra": False,
            "unp_eq_2_parent_unp": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "unp_eq_2_even_plus_extra": "LEMMA",
            "unp_rec_2prev_J_extra_k_ge_1": "LEMMA",
            "j0_odd_unp_eq_3_2km2": "LEMMA",
            "unp_rec_without_extra": "KILLED",
            "unp_eq_2_parent_unp": "KILLED",
            "extra_unp_empty": "KILLED",
            "odd_unp_eq_even_unp": "KILLED",
            "oddj_unp_eq_even_unp": "KILLED",
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
        "unp k8",
        dump["unpaired_rec"]["rows"]["8"]["unp"],
        "extra",
        dump["unpaired_rec"]["rows"]["8"]["extra"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
