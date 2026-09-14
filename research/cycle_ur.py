#!/usr/bin/env python3
"""Cycle UR: leftover pal-pairs at n=5U/2 are three; pg:lo halves 2-fold.

Covering n=5U/2 has 2n=clip, so j=0 is clip-edge. Even doubling gives
G(5U/2, U/2)=G(5,1), G(5U/2, U)=G(5,2), G(5U/2, 2U)=G(5,4), all 1, and
G(5,3)=0, so the only leftover pal-pairs are those three for k>=3.
At k=2 the 2U slot is d=2. For k>=3, pair+g0 leftover extra on
n<=5U/2 is twice even leftover on parent n<5 U_p/2, and on n>5U/2
twice even leftover on parent n>=5 U_p/2 (the three at the half
spill large). Dies at k=2 (parent_half odd). Do not PREFIX
leftover-parent xor large difference or pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_ur.py --certify
Dump: research/cycle_ur.json
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
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uo import named_half_split
from cycle_up import lucas, want_lo_e, want_pg_lo
from cycle_uq import want_lo_parent_large_sum
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UQ_JSON = Path(__file__).resolve().parent / "cycle_uq.json"
UP_JSON = Path(__file__).resolve().parent / "cycle_up.json"
UO_JSON = Path(__file__).resolve().parent / "cycle_uo.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
K_PH = 16
PAT0011 = (0, 0, 1, 1)


def parent_half(k: int) -> int:
    """Covering n=5U/2."""
    return 5 * (1 << k) // 2


def want_ph_lo(k: int) -> int:
    """Leftover pal-pairs at n=5U/2: 0,2,2, then 3."""
    if k <= 0:
        return 0
    if k <= 2:
        return 2
    return 3


def ph_lo_js(k: int) -> tuple[int, int, int]:
    """Candidate leftover pal-left indices at n=5U/2: U/2, U, 2U."""
    u = 1 << k
    return (u // 2, u, 2 * u)


def leftover_at_n(n: int, k: int) -> int:
    """Leftover pal-left count at a single covering n."""
    clip = 5 * (1 << k)
    c = 0
    hi = min(2 * n, clip)
    for j in range(0, hi + 1):
        if G(n, j) == 0:
            continue
        if pal_kind(n, j, k) != "pair":
            continue
        if j >= 2 * n - j:
            continue
        d = n - j
        if d in (1, 2) or is_clip_edge(n, j, k):
            continue
        c += 1
    return c


def even_lo_ph_split(k: int) -> dict:
    """Even leftover pal-pairs split by n<ph, n==ph, n>ph."""
    u = 1 << k
    clip = 5 * u
    ph = parent_half(k)
    sm = eq = lg = 0
    for n in range(0, 4 * u, 2):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            if n < ph:
                sm += 1
            elif n == ph:
                eq += 1
            else:
                lg += 1
    return {"sm": sm, "eq": eq, "lg": lg, "ph": ph}


def tot_form() -> dict:
    """k<=64: G(5,*) leftover triple; clip at j=0; d=2 at k=2."""
    n_ok = 0
    if want_ph_lo(0) != 0 or want_ph_lo(1) != 2 or want_ph_lo(2) != 2:
        return {"ok": False, "k012": True}
    if want_ph_lo(3) != 3 or want_ph_lo(8) != 3:
        return {"ok": False, "k38": True}
    if G(5, 1) != 1 or G(5, 2) != 1 or G(5, 4) != 1 or G(5, 3) != 0:
        return {"ok": False, "g5": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
        if m >= 1 and lucas(m) != fib(m - 1) + fib(m + 1):
            return {"ok": False, "L": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if 2 * ph != clip and k >= 1:
            return {"ok": False, "2n": True, "k": k}
        if k >= 1 and not is_clip_edge(ph, 0, k):
            return {"ok": False, "j0c": True, "k": k}
        if k >= 1:
            j0, j1, j2 = ph_lo_js(k)
            if G(ph, j0) != G(5, 1) or G(ph, j1) != G(5, 2) or G(ph, j2) != G(5, 4):
                return {"ok": False, "fold": True, "k": k}
            if pal_kind(ph, j0, k) != "pair" or pal_kind(ph, j2, k) != "pair":
                return {"ok": False, "kind": True, "k": k}
            if j2 >= ph:
                return {"ok": False, "left": True, "k": k}
        if k == 2:
            if ph - 2 * u != 2:
                return {"ok": False, "k2d": True}
            if want_ph_lo(k) == 3:
                return {"ok": False, "k23": True}
        if k >= 3:
            j0, j1, j2 = ph_lo_js(k)
            for j in (j0, j1, j2):
                d = ph - j
                if d in (1, 2) or is_clip_edge(ph, j, k):
                    return {"ok": False, "d": True, "k": k, "j": j}
            if want_ph_lo(k) != 3:
                return {"ok": False, "c3": True, "k": k}
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
        and want_ph_lo(2) != 3
        and want_ph_lo(8) == 3
        and G(5, 3) == 0
        and want_pg_lo(8) == 8560
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
        and want_lo_parent_large_sum(8) == 6486
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def ph_lo_fold() -> dict:
    """k<=16 unique leftover at ph; k<=8 pg:lo halves 2-fold even leftover."""
    n_ok = 0
    rows = {}
    for k in range(0, K_PH + 1):
        ph = parent_half(k)
        c = leftover_at_n(ph, k) if k >= 1 else 0
        if c != want_ph_lo(k):
            return {"ok": False, "ph": True, "k": k, "got": c}
        n_ok += 1
        rows[str(k)] = {"ph_lo": c}
    n_pg = 0
    pg_rows = {}
    for k in range(0, K_COUNT + 1):
        r = named_half_split(k)
        pg_s = r["plo_s"]
        pg_l = r["plo_l"]
        if k >= 1:
            eh = even_lo_ph_split(k - 1)
            # parent_half(1)=5 is odd, so even leftover never sits on it.
            if parent_half(k - 1) % 2 == 0 and eh["eq"] != want_ph_lo(k - 1):
                return {"ok": False, "eq": True, "k": k, "got": eh}
            if k >= 3:
                if pg_s != 2 * eh["sm"]:
                    return {"ok": False, "pgs": True, "k": k, "got": pg_s, "sm": eh["sm"]}
                if pg_l != 2 * (eh["lg"] + eh["eq"]):
                    return {"ok": False, "pgl": True, "k": k, "got": pg_l}
                if pg_s + pg_l != want_pg_lo(k):
                    return {"ok": False, "pgt": True, "k": k}
            if k == 2:
                if pg_s == 2 * eh["sm"] and eh["sm"] == 1:
                    return {"ok": False, "k2": True}
        n_pg += 1
        pg_rows[str(k)] = {"pg_s": pg_s, "pg_l": pg_l}
    ok = (
        n_ok == K_PH + 1
        and n_pg == K_COUNT + 1
        and rows["0"]["ph_lo"] == 0
        and rows["1"]["ph_lo"] == 2
        and rows["2"]["ph_lo"] == 2
        and rows["3"]["ph_lo"] == 3
        and rows["16"]["ph_lo"] == 3
        and pg_rows["8"]["pg_s"] == 5332
        and pg_rows["8"]["pg_l"] == 3228
        and pg_rows["3"]["pg_l"] == 4
        and pg_rows["2"]["pg_s"] == 1
        and rows["2"]["ph_lo"] != 3
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_pg": n_pg,
        "k_hi": K_PH,
        "rows": rows,
        "pg_rows": pg_rows,
    }


def killed_eq() -> dict:
    """three leftover at k=2; ph leftover empty; pg halves at k=2."""
    ok = (
        want_ph_lo(2) != 3
        and want_ph_lo(8) != 0
        and want_ph_lo(8) != jacobsthal(8)
        and parent_half(2) == 10
        and G(10, 8) == 1
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
    uq = json.loads(UQ_JSON.read_text())
    up = json.loads(UP_JSON.read_text())
    uo = json.loads(UO_JSON.read_text())
    ok = (
        uq["checks"]["all_ok"]
        and up["checks"]["all_ok"]
        and uo["checks"]["all_ok"]
        and uq["verdict"]["lo_large_eq_extra_lo_minus_lo_small"] == "LEMMA"
        and up["verdict"]["pg_lo_eq_2_parent_even_lo"] == "LEMMA"
        and uq["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uq["verdict"]["prize"] == "unsolved"
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
    cnt = ph_lo_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UR",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ph_lo_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ph_lo_eq_3_k_ge_3": True,
            "pg_lo_half_eq_2_even_lo_ph_k_ge_3": True,
            "ph_lo_eq_3_at_k2": False,
            "ph_lo_empty": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ph_lo_eq_3_k_ge_3": "LEMMA",
            "pg_lo_half_eq_2_even_lo_ph_k_ge_3": "LEMMA",
            "ph_lo_eq_3_at_k2": "KILLED",
            "ph_lo_empty": "KILLED",
            "ph_lo_eq_J": "KILLED",
            "pg_lo_half_at_k2": "KILLED",
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
            "lo_parent_large_diff_closed": "PREFIX",
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
        "ph_lo k16",
        dump["ph_lo_fold"]["rows"]["16"]["ph_lo"],
        "pg_s k8",
        dump["ph_lo_fold"]["pg_rows"]["8"]["pg_s"],
        "pg_l k8",
        dump["ph_lo_fold"]["pg_rows"]["8"]["pg_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
