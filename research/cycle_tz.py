#!/usr/bin/env python3
"""Cycle TZ: odd-j unpaired count is parent unpaired plus J_{k+1}.

Even unpaired 2-folds parent unpaired (Cycle TA). Odd-j pal-pairs
drop clip-edge to unpaired (Cycle TB), and parent unpaired 2-folds
to odd-j unpaired, so odd-j unpaired at k>=1 is unpaired(k-1)+J_{k+1}.
Even n have no odd-j cells, so that equals even unpaired plus J_{k+1}.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tz.py --certify
Dump: research/cycle_tz.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
TA_JSON = Path(__file__).resolve().parent / "cycle_ta.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"
TY_JSON = Path(__file__).resolve().parent / "cycle_ty.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_oddj_unp(unp_prev: int, k: int) -> int:
    """odd-j unpaired = parent unpaired + J_{k+1} for k>=1."""
    return unp_prev + jacobsthal(k + 1)


def unp_j_split(k: int) -> dict:
    """Unpaired pal-left cells split by n-parity and j-parity."""
    u = 1 << k
    clip = 5 * u
    unp = unp_e = unp_o = 0
    unp_oj = unp_ej = 0
    unp_oj_e = unp_ej_e = 0
    for n in range(0, 4 * u):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "unp":
                continue
            if j >= n:
                continue
            unp += 1
            even_n = n % 2 == 0
            even_j = j % 2 == 0
            if even_n:
                unp_e += 1
            else:
                unp_o += 1
            if even_j:
                unp_ej += 1
                if even_n:
                    unp_ej_e += 1
            else:
                unp_oj += 1
                if even_n:
                    unp_oj_e += 1
    return {
        "unp": unp,
        "unp_e": unp_e,
        "unp_o": unp_o,
        "unp_oj": unp_oj,
        "unp_ej": unp_ej,
        "unp_oj_e": unp_oj_e,
        "unp_ej_e": unp_ej_e,
    }


def tot_form() -> dict:
    """k<=64: J_{k+1}=edge(k-1); even n odd j silent; unique even."""
    n_ok = 0
    if want_oddj_unp(1, 1) != 2 or jacobsthal(2) != 1:
        return {"ok": False, "k1": True}
    if want_oddj_unp(4, 2) != 7:
        return {"ok": False, "k2": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 1 and want_oddj_unp(0, k) != jacobsthal(k + 1):
            return {"ok": False, "J": True, "k": k}
        if k >= 1 and want_edge_n(k - 1) != jacobsthal(k + 1):
            return {"ok": False, "ed": True, "k": k}
        samples_m = {0, 1, u // 2 if u >= 2 else 0, u, 2 * u - 1}
        for m in samples_m:
            n = 2 * m
            if n >= 4 * u:
                continue
            for j in (1, 3, min(2 * n - 1, 5 * u) if 2 * n >= 1 else 1):
                if 0 <= j <= min(2 * n, 5 * u) and j % 2 == 1 and G(n, j) != 0:
                    return {"ok": False, "godd": True, "k": k, "n": n, "j": j}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_oddj_unp(1, 1) != 1
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def unp_j_fold() -> dict:
    """k<=8: even unp 2-folds parent; odd-j unp = parent unp + J_{k+1}."""
    n_ok = 0
    rows = {}
    prev = None
    for k in range(0, K_COUNT + 1):
        r = unp_j_split(k)
        ps = pal_split(k, None)
        if r["unp"] != ps["n_unp"]:
            return {"ok": False, "ps": True, "k": k}
        if r["unp"] != r["unp_e"] + r["unp_o"]:
            return {"ok": False, "sum": True, "k": k}
        if r["unp_oj_e"] != 0:
            return {"ok": False, "oje": True, "k": k}
        if r["unp_ej_e"] != r["unp_e"]:
            return {"ok": False, "eje": True, "k": k}
        if k >= 1:
            if prev is None:
                return {"ok": False, "prev": True, "k": k}
            if r["unp_e"] != prev["unp"]:
                return {"ok": False, "even": True, "k": k}
            want = want_oddj_unp(prev["unp"], k)
            if r["unp_oj"] != want:
                return {"ok": False, "oj": True, "k": k, "unp_oj": r["unp_oj"], "want": want}
            if r["unp_oj"] != r["unp_e"] + jacobsthal(k + 1):
                return {"ok": False, "ojeq": True, "k": k}
            if r["unp_oj"] == r["unp_e"]:
                return {"ok": False, "eq": True, "k": k}
            if r["unp_o"] == r["unp_e"]:
                return {"ok": False, "odd_eq": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "unp": r["unp"],
            "unp_e": r["unp_e"],
            "unp_o": r["unp_o"],
            "unp_oj": r["unp_oj"],
        }
        prev = r
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["unp"] == 1
        and rows["0"]["unp_oj"] == 0
        and rows["1"]["unp_oj"] == 2
        and rows["2"]["unp_oj"] == 7
        and rows["8"]["unp"] == 26334
        and rows["8"]["unp_e"] == 8072
        and rows["8"]["unp_oj"] == 8243
        and rows["8"]["unp_oj"] == rows["8"]["unp_e"] + jacobsthal(9)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """odd-j unpaired equals even unpaired; unpaired 2-folds parent only."""
    ok = (
        want_oddj_unp(1, 1) != 1
        and want_oddj_unp(4, 2) == 7
        and jacobsthal(3) == 3
        and d2_clip_covering(0)
        and not d2_clip_covering(1)
        and unique_even_leftover(1)
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_odd(0) == 1
        and want_d1_n(0) == 1
    )
    return {"ok": ok}


def prefixes() -> dict:
    ta = json.loads(TA_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ty = json.loads(TY_JSON.read_text())
    ok = (
        ta["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and ty["checks"]["all_ok"]
        and ta["verdict"]["even_pal_split_2fold"] == "LEMMA"
        and tb["verdict"]["oddj_pairs_drop_clip_edge"] == "LEMMA"
        and tb["verdict"]["clip_edge_eq_jacobsthal"] == "LEMMA"
        and ty["verdict"]["pair_rec_2prev_4J_extra_k_ge_2"] == "LEMMA"
        and ty["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ty["verdict"]["prize"] == "unsolved"
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
    cnt = unp_j_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TZ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "unp_j_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_unp_eq_parent_unp": True,
            "oddj_unp_eq_parent_unp_plus_J_k1": True,
            "oddj_unp_eq_even_unp_plus_J_k1": True,
            "oddj_unp_eq_even_unp": False,
            "unp_eq_2_parent_unp": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_unp_eq_parent_unp": "LEMMA",
            "oddj_unp_eq_parent_unp_plus_J_k1": "LEMMA",
            "oddj_unp_eq_even_unp_plus_J_k1": "LEMMA",
            "oddj_unp_eq_even_unp": "KILLED",
            "unp_eq_2_parent_unp": "KILLED",
            "odd_unp_eq_even_unp": "KILLED",
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
        dump["unp_j_fold"]["rows"]["8"]["unp"],
        "oj",
        dump["unp_j_fold"]["rows"]["8"]["unp_oj"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
