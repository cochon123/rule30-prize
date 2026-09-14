#!/usr/bin/env python3
"""Cycle VG: leftover extra xor n_pg/n_gp match parent leftover xor.

Leftover extra except j=0 each produce one leftover-parent xor child.
Cycle UV counts those children as xor_lo(k-1); Cycle VF signs them
as UI(k-1). Splitting by kind, leftover extra xor n_pg is parent
leftover xor n_pg=(xor_lo+UI)/2, and leftover extra xor n_gp is
parent leftover xor n_gp=(xor_lo-UI)/2. Dies at k=8 for same-k
leftover xor n_pg (got 2650, not 8730) and for leftover-parent xor
pg (got 2650, not 8560). Census k=8: pg 2650, gp 2575. Do not
PREFIX pal-center tot. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_vg.py --certify
Dump: research/cycle_vg.json
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
from cycle_tu import d2_clip_covering
from cycle_tw import leftover_xor_split
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_ui import want_pg_minus_gp
from cycle_up import lucas, want_lo_e, want_pg_lo
from cycle_uq import want_xor_lo
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from cycle_uv import leftover_extra_xor_split, unique_van_odd_even, want_ej_xor, want_ej_xor_large
from cycle_uw import want_3u, want_miss_n
from cycle_uz import want_ege
from cycle_va import want_sm
from cycle_vf import want_ej_xor_diff
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
VF_JSON = Path(__file__).resolve().parent / "cycle_vf.json"
UI_JSON = Path(__file__).resolve().parent / "cycle_ui.json"
UQ_JSON = Path(__file__).resolve().parent / "cycle_uq.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_pg(k: int) -> int:
    """Leftover xor n_pg: (xor_lo+UI)/2."""
    return (want_xor_lo(k) + want_pg_minus_gp(k)) // 2


def want_gp(k: int) -> int:
    """Leftover xor n_gp: (xor_lo-UI)/2."""
    return (want_xor_lo(k) - want_pg_minus_gp(k)) // 2


def want_ej_xor_pg(k: int) -> int:
    """Leftover extra xor n_pg: parent leftover xor n_pg."""
    return want_pg(k - 1)


def want_ej_xor_gp(k: int) -> int:
    """Leftover extra xor n_gp: parent leftover xor n_gp."""
    return want_gp(k - 1)


def tot_form() -> dict:
    """k<=64: leftover extra xor pg/gp from parent leftover xor.

    Do not call leftover_xor_split / leftover_extra_xor_split here.
    Census is ej_pg_fold for k<=8.
    """
    n_ok = 0
    if want_ej_xor_pg(0) != 0 or want_ej_xor_gp(2) != 0:
        return {"ok": False, "k02": True}
    if want_ej_xor_pg(2) != 1 or want_ej_xor_pg(8) != 2650:
        return {"ok": False, "k28": True}
    if want_ej_xor_gp(8) != 2575:
        return {"ok": False, "gp8": True}
    if want_ej_xor_pg(8) == want_pg(8):
        return {"ok": False, "k8s": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
        if G(m, 0) != 1:
            return {"ok": False, "g0": True, "m": m}
        if m > 0 and G(2 * m, 1) != 0:
            return {"ok": False, "eodd": True, "m": m}
        if not unique_van_odd_even(m, 0):
            return {"ok": False, "van": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if (want_xor_lo(k) + want_pg_minus_gp(k)) % 2 != 0:
            return {"ok": False, "par": True, "k": k}
        if want_pg(k) + want_gp(k) != want_xor_lo(k):
            return {"ok": False, "sum": True, "k": k}
        if want_pg(k) - want_gp(k) != want_pg_minus_gp(k):
            return {"ok": False, "dif": True, "k": k}
        if want_ej_xor_pg(k) != want_pg(k - 1):
            return {"ok": False, "pg": True, "k": k}
        if want_ej_xor_gp(k) != want_gp(k - 1):
            return {"ok": False, "gp": True, "k": k}
        if want_ej_xor_pg(k) + want_ej_xor_gp(k) != want_ej_xor(k):
            return {"ok": False, "ej": True, "k": k}
        if want_ej_xor_pg(k) - want_ej_xor_gp(k) != want_ej_xor_diff(k):
            return {"ok": False, "ed": True, "k": k}
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
        and want_ej_xor_pg(8) != want_pg(8)
        and want_ej_xor_pg(8) != want_pg_lo(8)
        and want_ej_xor_pg(8) != want_ej_xor_gp(8)
        and want_pg(8) == 8730
        and want_gp(8) == 8581
        and want_ej_xor_pg(8) == 2650
        and want_ej_xor_gp(8) == 2575
        and want_ej_xor_diff(8) == 75
        and want_ej_xor(8) == 5225
        and want_ej_xor_large(8) == 2034
        and want_sm(8) == 8790
        and want_ege(8) == 5324
        and want_lo_e(8) == 14114
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
        and lucas(8) == 47
        and want_even_j0_sm(8) == 318
        and want_miss_n(8) == 769
        and want_3u(8) == 768
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ej_pg_fold() -> dict:
    """k<=8 leftover extra xor pg/gp and leftover xor n_pg/n_gp."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = leftover_xor_split(k)
        if r["n_pg"] != want_pg(k) or r["n_gp"] != want_gp(k):
            return {
                "ok": False,
                "lo": True,
                "k": k,
                "got": (r["n_pg"], r["n_gp"]),
            }
        a = leftover_extra_xor_split(k)
        pg = a["pg_s"] + a["pg_l"]
        gp = a["gp_s"] + a["gp_l"]
        if pg != want_ej_xor_pg(k):
            return {"ok": False, "pg": True, "k": k, "got": pg}
        if gp != want_ej_xor_gp(k):
            return {"ok": False, "gp": True, "k": k, "got": gp}
        n_ok += 1
        rows[str(k)] = {
            "n_pg": r["n_pg"],
            "n_gp": r["n_gp"],
            "ej_pg": pg,
            "ej_gp": gp,
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["2"]["ej_pg"] == 1
        and rows["2"]["ej_gp"] == 0
        and rows["2"]["ej_pg"] != 4
        and rows["8"]["ej_pg"] == 2650
        and rows["8"]["ej_gp"] == 2575
        and rows["8"]["n_pg"] == 8730
        and rows["8"]["n_gp"] == 8581
        and want_ej_xor_pg(4) == 18
        and want_ej_xor_gp(4) == 13
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """same-k leftover xor n_pg; leftover-parent xor pg; pg=gp."""
    a8 = leftover_extra_xor_split(8)
    r8 = leftover_xor_split(8)
    pg = a8["pg_s"] + a8["pg_l"]
    gp = a8["gp_s"] + a8["gp_l"]
    ok = (
        want_ej_xor_pg(8) != want_pg(8)
        and want_ej_xor_pg(8) != want_pg_lo(8)
        and want_ej_xor_pg(8) != want_ej_xor_gp(8)
        and pg == 2650
        and gp == 2575
        and r8["n_pg"] == 8730
        and pal_kind(want_3u(8), 0, 8) == "unp"
        and is_clip_edge(want_3u(8), 1 << 8, 8)
        and parent_half(8) == 640
        and G(2, 1) == 0
        and G(4, 2) == G(2, 1)
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
    vf = json.loads(VF_JSON.read_text())
    ui = json.loads(UI_JSON.read_text())
    uq = json.loads(UQ_JSON.read_text())
    ok = (
        vf["checks"]["all_ok"]
        and ui["checks"]["all_ok"]
        and uq["checks"]["all_ok"]
        and vf["verdict"]["ej_xor_diff_eq_parent_pg_minus_gp"] == "LEMMA"
        and ui["verdict"]["pg_minus_gp_eq_2km1_plus_J"] == "LEMMA"
        and uq["verdict"]["xor_lo_eq_extra_lo_minus_j0"] == "LEMMA"
        and vf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and vf["verdict"]["prize"] == "unsolved"
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
    cnt = ej_pg_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "VG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ej_pg_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ej_xor_pg_eq_parent_leftover_pg": True,
            "leftover_pg_eq_xor_lo_plus_UI_over_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ej_xor_pg_eq_parent_leftover_pg": "LEMMA",
            "leftover_pg_eq_xor_lo_plus_UI_over_2": "LEMMA",
            "ej_xor_pg_eq_same_k_leftover_pg": "KILLED",
            "ej_xor_pg_eq_lo_parent_pg": "KILLED",
            "ej_xor_pg_eq_ej_xor_gp": "KILLED",
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
        "pg k8",
        dump["ej_pg_fold"]["rows"]["8"]["ej_pg"],
        "gp",
        dump["ej_pg_fold"]["rows"]["8"]["ej_gp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
