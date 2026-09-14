#!/usr/bin/env python3
"""Cycle TP: d=1 pal-pairs meet a forced column at two cells.

d=1 sides are j=n-1 and j=n+1. Forced pal-right is j in
{5U-2, 5U-3, 5U-7}. The large-j side hits iff (k,n)=(0,1) at
p=6 or (1,7) at p=4. Both fire AND, so d=1 rest tot equals d=1
raw tot xor 1_{k<=1}. For k>=2 the slice is never forced. Not
rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do
not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tp.py --certify
Dump: research/cycle_tp.json
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
from cycle_hh import AND_ONES, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import packed_p
from cycle_sv import forced_right_j, pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_td import want_d1_n
from cycle_tl import d1_v2
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TO_JSON = Path(__file__).resolve().parent / "cycle_to.json"
TN_JSON = Path(__file__).resolve().parent / "cycle_tn.json"
TD_JSON = Path(__file__).resolve().parent / "cycle_td.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
T_FREEZE = 16
PAT0011 = (0, 0, 1, 1)


def want_d1_forced(k: int) -> list[tuple[int, int]]:
    """Covering d=1 cells whose large-j side is forced: (n, p)."""
    if k == 0:
        return [(1, 6)]
    if k == 1:
        return [(7, 4)]
    return []


def want_d1_corr(k: int) -> int:
    """d=1 rest tot xor raw tot: 1 iff k<=1."""
    return int(k <= 1)


def d1_forced_hits(k: int) -> list[tuple[int, int]]:
    """Covering n with d=1 and pal-right j=n+1 forced."""
    u = 1 << k
    cap = 4 * u
    hits: list[tuple[int, int]] = []
    for p in (4, 6, 14):
        n = forced_right_j(p, k) - 1
        if 0 <= n < cap and d1_v2(n):
            hits.append((n, p))
    return hits


def tot_form() -> dict:
    """k<=64: forced d=1 hits; small-j never forced; times; corr."""
    n_ok = 0
    if want_d1_forced(0) != [(1, 6)] or want_d1_forced(1) != [(7, 4)]:
        return {"ok": False, "base": True}
    if covering_t(0, 1) != 7 or covering_t(1, 7) != 5:
        return {"ok": False, "t": True}
    if packed_p(2, 0) != 6 or packed_p(8, 1) != 4:
        return {"ok": False, "p": True}
    if d1_v2(1) != 1 or d1_v2(7) != 1 or d1_v2(3) != 0:
        return {"ok": False, "v2": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        cap = 4 * u
        got = d1_forced_hits(k)
        if got != want_d1_forced(k):
            return {"ok": False, "hit": True, "k": k, "got": got}
        if want_d1_corr(k) != int(k <= 1):
            return {"ok": False, "corr": True, "k": k}
        for p in (4, 6, 14):
            j_hi = forced_right_j(p, k)
            if j_hi != {4: 5 * u - 2, 6: 5 * u - 3, 14: 5 * u - 7}[p]:
                return {"ok": False, "j": True, "k": k, "p": p}
            n_hi = j_hi - 1
            if 0 <= n_hi < cap and d1_v2(n_hi):
                if (n_hi, p) not in want_d1_forced(k):
                    return {"ok": False, "hi": True, "k": k, "n": n_hi}
                if packed_p(n_hi + 1, k) != p:
                    return {"ok": False, "php": True, "k": k}
                if pal_kind(n_hi, n_hi - 1, k) != "pair":
                    return {"ok": False, "kind": True, "k": k, "n": n_hi}
            n_lo = j_hi + 1
            if 0 <= n_lo < cap and d1_v2(n_lo):
                return {"ok": False, "lo": True, "k": k, "n": n_lo}
        if k >= 2 and want_d1_forced(k):
            return {"ok": False, "k2": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_d1_corr(0) == 1
        and want_d1_corr(2) == 0
        and want_d1_n(0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and 4 in FORCED
        and 6 in FORCED
        and 14 in FORCED
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def freeze_and() -> dict:
    """Packed AND at p=4 on t=5 and p=6 on t=7 is 1."""
    row = 1
    got: dict[int, dict[str, int]] = {}
    for t in range(0, T_FREEZE):
        if t in (5, 7):
            got[t] = {
                "and4": bit_at(row, 3) & bit_at(row, 4),
                "and6": bit_at(row, 5) & bit_at(row, 6),
            }
        row = rule30_step(row)
    ok = (
        got[5]["and4"] == 1
        and got[7]["and6"] == 1
        and covering_t(1, 7) == 5
        and covering_t(0, 1) == 7
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok, "t5_and4": got[5]["and4"], "t7_and6": got[7]["and6"]}


def d1_forced_count() -> dict:
    """k<=12: only (0,1) and (1,7); small-j side never forced."""
    n_ok = 0
    n_hit = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        hits: list[tuple[int, int]] = []
        n_d1 = 0
        for n in range(0, 4 * u):
            if not d1_v2(n):
                continue
            if n < 1 or pal_kind(n, n - 1, k) != "pair":
                return {"ok": False, "kind": True, "k": k, "n": n}
            n_d1 += 1
            p_hi = packed_p(n + 1, k)
            p_lo = packed_p(n - 1, k)
            if p_lo in FORCED:
                return {"ok": False, "lo": True, "k": k, "n": n, "p": p_lo}
            if p_hi in FORCED:
                hits.append((n, p_hi))
        if n_d1 != want_d1_n(k):
            return {
                "ok": False,
                "count": True,
                "k": k,
                "n_d1": n_d1,
                "want": want_d1_n(k),
            }
        if hits != want_d1_forced(k) or hits != d1_forced_hits(k):
            return {"ok": False, "hit": True, "k": k, "hits": hits}
        n_hit += len(hits)
        n_ok += 1
        rows[str(k)] = {"n_d1": n_d1, "n_fr": len(hits)}
    ok = (
        n_ok == K_COUNT + 1
        and n_hit == 2
        and rows["0"]["n_fr"] == 1
        and rows["1"]["n_fr"] == 1
        and rows["2"]["n_fr"] == 0
        and rows["12"]["n_d1"] == 5461
        and rows["12"]["n_fr"] == 0
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_hit": n_hit,
        "k_hi": K_COUNT,
        "rows": rows,
    }


def killed_eq() -> dict:
    """d=1 never forced all k; d=1 rest equals raw all k."""
    ok = (
        want_d1_forced(0) == [(1, 6)]
        and want_d1_forced(1) == [(7, 4)]
        and want_d1_corr(0) == 1
        and want_d1_corr(1) == 1
        and want_d1_corr(2) == 0
        and d1_v2(1) == 1
        and d1_v2(7) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    to = json.loads(TO_JSON.read_text())
    tn = json.loads(TN_JSON.read_text())
    td = json.loads(TD_JSON.read_text())
    ok = (
        to["checks"]["all_ok"]
        and tn["checks"]["all_ok"]
        and td["checks"]["all_ok"]
        and to["verdict"]["odd_child_val_a_to_a1"] == "LEMMA"
        and to["verdict"]["even_child_d2_iff_a_odd"] == "LEMMA"
        and td["verdict"]["d1_odd_iff_G_m_m1_0"] == "LEMMA"
        and to["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and to["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, frz, cnt, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and frz["ok"] and cnt["ok"] and kl["ok"]
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
    frz = freeze_and()
    cnt = d1_forced_count()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, frz, cnt, kl, sc, pref)
    dump = {
        "cycle": "TP",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "freeze_and": {k: frz[k] for k in frz if k != "ok"},
        "d1_forced_count": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d1_forced_two_cells": True,
            "d1_rest_eq_raw_xor_k_le_1": True,
            "d1_never_forced_k_ge_2": True,
            "d1_never_forced_all_k": False,
            "d1_rest_eq_raw_all_k": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d1_forced_two_cells": "LEMMA",
            "d1_rest_eq_raw_xor_k_le_1": "LEMMA",
            "d1_never_forced_k_ge_2": "LEMMA",
            "d1_never_forced_all_k": "KILLED",
            "d1_rest_eq_raw_all_k": "KILLED",
            "even_child_stays_d1": "KILLED",
            "d2_times_single_ap": "KILLED",
            "d1_times_single_ap": "KILLED",
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
        "n_hit",
        dump["d1_forced_count"]["n_hit"],
        "k12_d1",
        dump["d1_forced_count"]["rows"]["12"]["n_d1"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
