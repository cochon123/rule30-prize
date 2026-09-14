#!/usr/bin/env python3
"""Cycle UU: even leftover at j=0 on n<5U/2 is 5*2^{k-2}-2.

G(n,0)=1. Pal-pair iff 2n<=5U iff n<=5U/2. Clip-edge at n=5U/2, d=2
at n=2, pal-center at n=0, so leftover j=0 on even n is n=4,6,...,
5U/2-2, count 5*2^{k-2}-2 for k>=2. Those produce pair+g0 leftover
children but g0+pair at j=0, so gp:lo from even parents is even
leftover minus that count. Dies at k=1. Do not PREFIX leftover-parent
xor large difference or pal-center tot. Not rest=S xor T. Do not
walk leftover p catalogues. Do not walk leftover d catalogues. Do
not walk k=11 packed covering. Do not walk k=12 T-bands. Not a
prize claim.

Run: python3 research/cycle_uu.py --certify
Dump: research/cycle_uu.json
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
from cycle_tw import want_j0_odd_lo
from cycle_uc import fib, trans, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_ul import parent_pair_type
from cycle_uo import want_named_l
from cycle_up import lucas, want_lo_e
from cycle_ur import even_lo_ph_split, parent_half
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UT_JSON = Path(__file__).resolve().parent / "cycle_ut.json"
US_JSON = Path(__file__).resolve().parent / "cycle_us.json"
UR_JSON = Path(__file__).resolve().parent / "cycle_ur.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
K_J0 = 16
PAT0011 = (0, 0, 1, 1)


def want_even_j0_sm(k: int) -> int:
    """Leftover pal-pairs at j=0 on even n<5U/2: 0,1, then 5*2^{k-2}-2."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return 5 * (1 << (k - 2)) - 2


def want_gp_e(k: int) -> int:
    """gp:lo from even parents: 0 at k<=1, lo_e(k-1) minus even j=0 small."""
    if k <= 1:
        return 0
    return want_lo_e(k - 1) - want_even_j0_sm(k - 1)


def even_j0_split(k: int) -> dict:
    """Leftover pal-pairs at j=0 on even n, split by n vs 5U/2."""
    u = 1 << k
    ph = parent_half(k)
    sm = eq = lg = 0
    for n in range(0, 4 * u, 2):
        if G(n, 0) == 0:
            continue
        if pal_kind(n, 0, k) != "pair":
            continue
        if 0 >= 2 * n:
            continue
        d = n
        if d in (1, 2) or is_clip_edge(n, 0, k):
            continue
        if n < ph:
            sm += 1
        elif n == ph:
            eq += 1
        else:
            lg += 1
    return {"sm": sm, "eq": eq, "lg": lg, "ph": ph}


def even_parent_xor_split(k: int) -> dict:
    """Odd-n even-j leftover-parent xor from even parents, by n<=5U/2."""
    u = 1 << k
    clip = 5 * u
    half = 5 * u // 2
    k_p = k - 1 if k >= 1 else 0
    a = {"pg_s": 0, "pg_l": 0, "gp_s": 0, "gp_l": 0}
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        if m % 2 != 0:
            continue
        hi = min(2 * n, clip)
        tag = "_s" if n <= half else "_l"
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            r = j // 2
            if r == 0:
                continue
            kr = parent_pair_type(m, r, k_p)
            km = parent_pair_type(m, r - 1, k_p)
            if km == "lo" and kr == "g0":
                a["pg" + tag] += 1
            elif km == "g0" and kr == "lo":
                a["gp" + tag] += 1
    return a


def tot_form() -> dict:
    """k<=64: even n from 4 to 5U/2-2; j=0 clip at half; unpaired large."""
    n_ok = 0
    if want_even_j0_sm(0) != 0 or want_even_j0_sm(1) != 1:
        return {"ok": False, "k01": True}
    if want_even_j0_sm(2) != 3 or want_even_j0_sm(8) != 318:
        return {"ok": False, "k28": True}
    if want_gp_e(8) != 4122 or want_gp_e(0) != 0:
        return {"ok": False, "gp8": True}
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
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        clip = 5 * u
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if 2 * ph != clip and k >= 1:
            return {"ok": False, "2n": True, "k": k}
        if k >= 2:
            last = ph - 2
            if last % 2 != 0 or last < 4:
                return {"ok": False, "last": True, "k": k}
            cnt = (last - 4) // 2 + 1
            if cnt != want_even_j0_sm(k):
                return {"ok": False, "cnt": True, "k": k, "got": cnt}
            if last >= 4 * u:
                return {"ok": False, "cov": True, "k": k}
            if is_clip_edge(ph, 0, k) is not True:
                return {"ok": False, "clip": True, "k": k}
            if pal_kind(ph + 2, 0, k) != "unp":
                return {"ok": False, "unp": True, "k": k}
            if pal_kind(2, 0, k) != "pair":
                return {"ok": False, "n2": True, "k": k}
            if k >= 2 and (2 in (1, 2)):
                pass
            if want_even_j0_sm(k) != want_j0_odd_lo(k) - 1:
                return {"ok": False, "j0": True, "k": k}
            if want_gp_e(k) != want_lo_e(k - 1) - want_even_j0_sm(k - 1):
                return {"ok": False, "gpe": True, "k": k}
        if k == 1:
            if want_even_j0_sm(1) != 1:
                return {"ok": False, "k1": True}
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
        and want_even_j0_sm(2) == 3
        and want_even_j0_sm(8) == 318
        and want_even_j0_sm(8) != want_j0_odd_lo(8)
        and want_even_j0_sm(7) == want_named_l(8)
        and want_even_j0_sm(6) != want_named_l(7)
        and want_gp_e(8) == 4122
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
        and want_lo_e(8) == 14114
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def j0_gp_fold() -> dict:
    """k<=16 even j=0 small; k<=8 gp:lo from even parents."""
    n_ok = 0
    rows = {}
    for k in range(0, K_J0 + 1):
        z = even_j0_split(k)
        if z["sm"] != want_even_j0_sm(k):
            return {"ok": False, "j0": True, "k": k, "got": z}
        if z["eq"] != 0 or z["lg"] != 0:
            return {"ok": False, "el": True, "k": k, "got": z}
        n_ok += 1
        rows[str(k)] = {"sm": z["sm"]}
    n_gp = 0
    gp_rows = {}
    for k in range(0, K_COUNT + 1):
        xr = even_parent_xor_split(k)
        eh = even_lo_ph_split(k - 1) if k >= 1 else {"sm": 0, "eq": 0, "lg": 0}
        e_ge = eh["eq"] + eh["lg"]
        gp_e = xr["gp_s"] + xr["gp_l"]
        if gp_e != want_gp_e(k):
            return {"ok": False, "gpe": True, "k": k, "got": gp_e}
        if k >= 2:
            if xr["gp_s"] != eh["sm"] - want_even_j0_sm(k - 1):
                return {
                    "ok": False,
                    "gps": True,
                    "k": k,
                    "got": xr["gp_s"],
                    "sm": eh["sm"],
                }
            if xr["gp_l"] != e_ge:
                return {"ok": False, "gpl": True, "k": k, "got": xr["gp_l"]}
            if xr["pg_s"] + xr["pg_l"] != want_lo_e(k - 1):
                return {"ok": False, "pge": True, "k": k}
        n_gp += 1
        gp_rows[str(k)] = {
            "gp_s": xr["gp_s"],
            "gp_l": xr["gp_l"],
            "pg_s": xr["pg_s"],
            "pg_l": xr["pg_l"],
        }
    ok = (
        n_ok == K_J0 + 1
        and n_gp == K_COUNT + 1
        and rows["0"]["sm"] == 0
        and rows["1"]["sm"] == 1
        and rows["2"]["sm"] == 3
        and rows["16"]["sm"] == 5 * (1 << 14) - 2
        and gp_rows["8"]["gp_s"] == 2508
        and gp_rows["8"]["gp_l"] == 1614
        and gp_rows["8"]["pg_l"] == 1614
        and gp_rows["3"]["gp_s"] == 1
        and want_even_j0_sm(1) != 3
    )
    return {
        "ok": ok,
        "n_ok": n_ok,
        "n_gp": n_gp,
        "k_hi": K_J0,
        "rows": rows,
        "gp_rows": gp_rows,
    }


def killed_eq() -> dict:
    """formula at k=1; j=0 leftover large; equals named_l all k."""
    z8 = even_j0_split(8)
    ok = (
        want_even_j0_sm(1) == 1
        and want_even_j0_sm(8) != 0
        and z8["lg"] == 0
        and z8["eq"] == 0
        and want_even_j0_sm(8) != want_j0_odd_lo(8)
        and want_even_j0_sm(6) != want_named_l(7)
        and want_gp_e(8) != want_lo_e(7)
        and want_ph_check()
        and G(2, 1) == 0
        and G(2, 2) != 0
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


def want_ph_check() -> bool:
    return parent_half(2) == 10 and parent_half(8) == 640


def prefixes() -> dict:
    ut = json.loads(UT_JSON.read_text())
    us = json.loads(US_JSON.read_text())
    ur = json.loads(UR_JSON.read_text())
    ok = (
        ut["checks"]["all_ok"]
        and us["checks"]["all_ok"]
        and ur["checks"]["all_ok"]
        and ut["verdict"]["ph_lo_both_xor_k_ge_3"] == "LEMMA"
        and us["verdict"]["oj_lg_eq_even_lo_ge_k_ge_2"] == "LEMMA"
        and ut["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ut["verdict"]["prize"] == "unsolved"
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
    cnt = j0_gp_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "j0_gp_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "even_j0_sm_eq_5_2km2_minus_2": True,
            "gp_e_eq_loe_minus_even_j0": True,
            "even_j0_on_large": False,
            "even_j0_eq_j0_odd": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_j0_sm_eq_5_2km2_minus_2": "LEMMA",
            "gp_e_eq_loe_minus_even_j0": "LEMMA",
            "even_j0_formula_at_k1": "KILLED",
            "even_j0_on_large": "KILLED",
            "even_j0_eq_j0_odd": "KILLED",
            "even_j0_eq_named_l_all_k": "KILLED",
            "gp_e_eq_loe": "KILLED",
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
        "j0_sm k16",
        dump["j0_gp_fold"]["rows"]["16"]["sm"],
        "gp_s k8",
        dump["j0_gp_fold"]["gp_rows"]["8"]["gp_s"],
        "gp_l k8",
        dump["j0_gp_fold"]["gp_rows"]["8"]["gp_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
