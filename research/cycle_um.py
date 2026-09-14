#!/usr/bin/env python3
"""Cycle UM: leftover-parent xor difference is 3*2^{k-1}+J_{k-2}-2 J_k-2.

Cycle UI leftover xor n_pg-n_gp is 2^{k-1}+J_{k-2}. Cycle UL splits
those into named d=1/d=2 plus leftover-parent xor. Named difference
is closed, so leftover-parent xor difference pg:lo-gp:lo is
3*2^{k-1}+J_{k-2}-2 J_k-2 for k>=2. Do not PREFIX pg:lo or gp:lo
sums or leftover extra or unpaired extra. Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk leftover d catalogues. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_um.py --certify
Dump: research/cycle_um.json
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
from cycle_tb import jacobsthal, want_edge_n
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tt import unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_ui import want_pg_minus_gp
from cycle_uk import want_lo_small
from cycle_ul import (
    leftover_named_split,
    want_gp_d1,
    want_gp_d2,
    want_named_lo,
    want_pg_d2,
)
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UL_JSON = Path(__file__).resolve().parent / "cycle_ul.json"
UI_JSON = Path(__file__).resolve().parent / "cycle_ui.json"
UK_JSON = Path(__file__).resolve().parent / "cycle_uk.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_lo_parent_diff(k: int) -> int:
    """pg:lo-gp:lo: 0 at k<=1, 3*2^{k-1}+J_{k-2}-2 J_k-2 for k>=2."""
    if k <= 1:
        return 0
    return 3 * (1 << (k - 1)) + jacobsthal(k - 2) - 2 * jacobsthal(k) - 2


def tot_form() -> dict:
    """k<=64: difference from UI minus named; J recurrences."""
    n_ok = 0
    if want_lo_parent_diff(0) != 0 or want_lo_parent_diff(1) != 0:
        return {"ok": False, "k01": True}
    if want_lo_parent_diff(2) != 2 or want_lo_parent_diff(8) != 233:
        return {"ok": False, "k28": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_lo_parent_diff(k) != (
            want_pg_minus_gp(k)
            - want_pg_d2(k)
            + want_gp_d1(k)
            + want_gp_d2(k)
        ):
            return {"ok": False, "ui": True, "k": k}
        if k >= 2:
            if want_lo_parent_diff(k) != (
                3 * (1 << (k - 1))
                + jacobsthal(k - 2)
                - 2 * jacobsthal(k)
                - 2
            ):
                return {"ok": False, "cl": True, "k": k}
            if want_named_lo(k) != (1 << k) + 2 * jacobsthal(k) - 2:
                return {"ok": False, "nm": True, "k": k}
            if want_pg_minus_gp(k) != (1 << (k - 1)) + jacobsthal(k - 2):
                return {"ok": False, "pg": True, "k": k}
        if k >= 1 and jacobsthal(k + 1) != (1 << k) - jacobsthal(k):
            return {"ok": False, "Jrec": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
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
        and want_lo_parent_diff(8) == 233
        and want_lo_parent_diff(8) != want_pg_minus_gp(8)
        and want_lo_parent_diff(8) != want_named_lo(8)
        and want_lo_small(8) == 10986
        and want_gp_d1(8) == 170
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


def parent_diff_fold() -> dict:
    """k<=8: pg:lo-gp:lo matches; sums not the form."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = leftover_named_split(k)
        if r["n_bad"] != 0:
            return {"ok": False, "bad": True, "k": k}
        if r["n_pg_d1"] != 0:
            return {"ok": False, "pgd1": True, "k": k}
        diff = r["n_pg_lo"] - r["n_gp_lo"]
        tot = r["n_pg_lo"] + r["n_gp_lo"]
        if diff != want_lo_parent_diff(k):
            return {"ok": False, "diff": True, "k": k, "got": diff}
        xor_lo = r["n_pg_d2"] + r["n_pg_lo"] + r["n_gp_d1"] + r["n_gp_d2"] + r["n_gp_lo"]
        if xor_lo - (r["n_gp_d1"] + r["n_pg_d2"] + r["n_gp_d2"]) != tot:
            return {"ok": False, "xor": True, "k": k}
        if k >= 3 and tot == want_lo_parent_diff(k):
            return {"ok": False, "sum": True, "k": k}
        if k >= 2 and r["n_pg_lo"] == r["n_gp_lo"]:
            return {"ok": False, "eq": True, "k": k}
        if k >= 4 and diff == want_pg_minus_gp(k):
            return {"ok": False, "ui": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n_pg_lo": r["n_pg_lo"],
            "n_gp_lo": r["n_gp_lo"],
            "diff": diff,
            "tot": tot,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["diff"] == 0
        and rows["1"]["diff"] == 0
        and rows["8"]["n_pg_lo"] == 8560
        and rows["8"]["n_gp_lo"] == 8327
        and rows["8"]["diff"] == 233
        and rows["8"]["tot"] == 16887
        and rows["8"]["diff"] != 149
        and rows["8"]["tot"] != 233
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """pg:lo=gp:lo; difference equals UI or named; difference empty."""
    ok = (
        want_lo_parent_diff(8) != 0
        and want_lo_parent_diff(8) != want_pg_minus_gp(8)
        and want_lo_parent_diff(8) != want_named_lo(8)
        and want_lo_parent_diff(8) != 16887
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
    ul = json.loads(UL_JSON.read_text())
    ui = json.loads(UI_JSON.read_text())
    uk = json.loads(UK_JSON.read_text())
    ok = (
        ul["checks"]["all_ok"]
        and ui["checks"]["all_ok"]
        and uk["checks"]["all_ok"]
        and ul["verdict"]["named_lo_eq_2k_plus_2J_minus_2"] == "LEMMA"
        and ui["verdict"]["pg_minus_gp_eq_2km1_plus_J"] == "LEMMA"
        and uk["verdict"]["lo_small_eq_tot_minus_d1"] == "LEMMA"
        and ul["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ul["verdict"]["prize"] == "unsolved"
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
    cnt = parent_diff_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "parent_diff_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "lo_parent_diff_eq_3_2km1_J": True,
            "lo_parent_diff_eq_ui_minus_named": True,
            "pg_lo_eq_gp_lo": False,
            "lo_parent_diff_eq_ui": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "lo_parent_diff_eq_3_2km1_J": "LEMMA",
            "lo_parent_diff_eq_ui_minus_named": "LEMMA",
            "pg_lo_eq_gp_lo": "KILLED",
            "lo_parent_diff_eq_ui": "KILLED",
            "lo_parent_diff_eq_named": "KILLED",
            "lo_parent_diff_empty": "KILLED",
            "lo_parent_sum_eq_diff": "KILLED",
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
        "diff k8",
        dump["parent_diff_fold"]["rows"]["8"]["diff"],
        "pg_lo",
        dump["parent_diff_fold"]["rows"]["8"]["n_pg_lo"],
        "gp_lo",
        dump["parent_diff_fold"]["rows"]["8"]["n_gp_lo"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
