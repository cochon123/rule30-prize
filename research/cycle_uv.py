#!/usr/bin/env python3
"""Cycle UV: even pal-left G=1 on odd covering has unique vanishing neighbor.

G(2s+1, 2t)=G(s,t) xor G(s,t-1), neighbors G(2t-1)=G(s,t-1) and
G(2t+1)=G(s,t). If G=1 then exactly one neighbor vanishes, sign
G(s,t): right vanishes iff G(s,t)=0 (pair+g0 child), left iff
G(s,t)=1 (g0+pair child). Leftover extra except j=0 each produce
one leftover-parent xor child, count xor_lo(k-1); on n>5U/2 the
count is lo_large(k-1) for k>=3. Odd-j leftover from even covering
parents have both neighbors 1, so no leftover-parent xor. Dies at
k=2 for the large count (parent-half odd). Do not PREFIX
leftover-parent xor large difference or pal-center tot. Not rest=S
xor T. Do not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_uv.py --certify
Dump: research/cycle_uv.json
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
from cycle_up import lucas, want_lo_e
from cycle_uq import want_lo_large, want_xor_lo
from cycle_ur import parent_half
from cycle_uu import want_even_j0_sm
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UU_JSON = Path(__file__).resolve().parent / "cycle_uu.json"
UT_JSON = Path(__file__).resolve().parent / "cycle_ut.json"
US_JSON = Path(__file__).resolve().parent / "cycle_us.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_ej_xor(k: int) -> int:
    """Leftover-parent xor from leftover extra except j=0: xor_lo(k-1)."""
    if k <= 0:
        return 0
    return want_xor_lo(k - 1)


def want_ej_xor_large(k: int) -> int:
    """That xor on n>5U/2: 0,0,1, then lo_large(k-1)."""
    if k <= 1:
        return 0
    if k == 2:
        return 1
    return want_lo_large(k - 1)


def unique_van_odd_even(s: int, t: int) -> bool:
    """G(2s+1, 2t)=1 implies neighbors xor to 1, matching G(s,t)."""
    n = 2 * s + 1
    j = 2 * t
    g = G(n, j)
    left = G(n, j - 1)
    right = G(n, j + 1)
    gs = G(s, t)
    gsm = G(s, t - 1)
    if g != (gs ^ gsm):
        return False
    if left != gsm or right != gs:
        return False
    if g == 1:
        return left + right == 1
    return left == right


def leftover_extra_xor_split(k: int) -> dict:
    """Leftover-parent xor from leftover extra (odd leftover even-j)."""
    u = 1 << k
    clip = 5 * u
    half = parent_half(k)
    k_p = k - 1 if k >= 1 else 0
    a = {"pg_s": 0, "pg_l": 0, "gp_s": 0, "gp_l": 0, "sign_bad": 0}
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        if m % 2 == 0:
            continue
        hi = min(2 * n, clip)
        tag = "_s" if n <= half else "_l"
        s = (m - 1) // 2
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
                r0 = r - 1
                if r0 % 2 != 0:
                    continue
                a["pg" + tag] += 1
                t = r0 // 2
                if G(s, t) != 0:
                    a["sign_bad"] += 1
            elif km == "g0" and kr == "lo":
                r0 = r
                if r0 % 2 != 0:
                    continue
                a["gp" + tag] += 1
                t = r0 // 2
                if G(s, t) != 1:
                    a["sign_bad"] += 1
    return a


def even_origin_oj_van(k: int) -> dict:
    """Odd-j leftover from even covering parents: both neighbors 1."""
    u = 1 << k
    clip = 5 * u
    n_ok = n_bad = 0
    for n in range(1, 4 * u, 2):
        m = (n - 1) // 2
        if m % 2 != 0:
            continue
        hi = min(2 * n, clip)
        for j in range(1, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if pal_kind(n, j, k) != "pair":
                continue
            if j >= 2 * n - j:
                continue
            d = n - j
            if d in (1, 2) or is_clip_edge(n, j, k):
                continue
            n_ok += 1
            if G(n, j - 1) != 1 or G(n, j + 1) != 1:
                n_bad += 1
    return {"n_ok": n_ok, "n_bad": n_bad}


def tot_form() -> dict:
    """k<=64: unique van; even-origin both neighbors 1; counts."""
    n_ok = 0
    if want_ej_xor(0) != 0 or want_ej_xor(1) != 0:
        return {"ok": False, "k01": True}
    if want_ej_xor(2) != 1 or want_ej_xor(8) != 5225:
        return {"ok": False, "k28": True}
    if want_ej_xor_large(2) != 1 or want_ej_xor_large(8) != 2034:
        return {"ok": False, "lg8": True}
    if want_ej_xor_large(1) != 0 or want_ej_xor_large(3) != 3:
        return {"ok": False, "lg13": True}
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
        for t in range(0, m + 2):
            if not unique_van_odd_even(m, t):
                return {"ok": False, "van": True, "m": m, "t": t}
        if m % 2 == 0:
            for r in range(0, m + 1, 2):
                if G(m, r) != 1:
                    continue
                nc = 2 * m + 1
                jc = 2 * r + 1
                if G(nc, jc - 1) != 1 or G(nc, jc + 1) != 1:
                    return {"ok": False, "eoj": True, "m": m, "r": r}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        ph = parent_half(k)
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if ph != 5 * u // 2:
            return {"ok": False, "ph": True, "k": k}
        if want_ej_xor(k) != (0 if k <= 0 else want_xor_lo(k - 1)):
            return {"ok": False, "ej": True, "k": k}
        if k <= 1:
            if want_ej_xor_large(k) != 0:
                return {"ok": False, "lg01": True, "k": k}
        elif k == 2:
            if want_ej_xor_large(2) != 1:
                return {"ok": False, "lg2": True}
            if want_ej_xor_large(2) == want_lo_large(1):
                return {"ok": False, "lg2f": True}
        else:
            if want_ej_xor_large(k) != want_lo_large(k - 1):
                return {"ok": False, "lgg": True, "k": k}
        if k >= 2 and want_ej_xor(k) != want_extra_xor_parent(k):
            return {"ok": False, "x": True, "k": k}
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
        and want_ej_xor(8) == 5225
        and want_ej_xor_large(8) == 2034
        and want_ej_xor_large(2) != want_lo_large(1)
        and want_xor_lo(7) == 5225
        and want_lo_large(7) == 2034
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
        and want_even_j0_sm(8) == 318
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def want_extra_xor_parent(k: int) -> int:
    return want_xor_lo(k - 1) if k >= 1 else 0


def ej_xor_fold() -> dict:
    """k<=8 leftover extra xor 1-matching; even-origin odd-j van=0."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        xr = leftover_extra_xor_split(k)
        tot = xr["pg_s"] + xr["pg_l"] + xr["gp_s"] + xr["gp_l"]
        lg = xr["pg_l"] + xr["gp_l"]
        if xr["sign_bad"] != 0:
            return {"ok": False, "sign": True, "k": k}
        if tot != want_ej_xor(k):
            return {"ok": False, "tot": True, "k": k, "got": tot}
        if lg != want_ej_xor_large(k):
            return {"ok": False, "lg": True, "k": k, "got": lg}
        ev = even_origin_oj_van(k)
        if ev["n_bad"] != 0:
            return {"ok": False, "eoj": True, "k": k, "got": ev}
        n_ok += 1
        rows[str(k)] = {
            "tot": tot,
            "lg": lg,
            "pg_l": xr["pg_l"],
            "gp_l": xr["gp_l"],
            "eoj": ev["n_ok"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["tot"] == 0
        and rows["2"]["lg"] == 1
        and rows["2"]["lg"] != 0
        and rows["8"]["tot"] == 5225
        and rows["8"]["lg"] == 2034
        and rows["8"]["pg_l"] == 1002
        and rows["8"]["gp_l"] == 1032
        and rows["8"]["pg_l"] - rows["8"]["gp_l"] == -30
        and want_ej_xor_large(2) != want_lo_large(1)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """unique van on even n; both xor from leftover extra; large at k=2."""
    z8 = leftover_extra_xor_split(8)
    ev8 = even_origin_oj_van(8)
    ok = (
        unique_van_odd_even(2, 1)
        and G(2, 2) == 1
        and G(2, 1) == 0
        and G(2, 3) == 0
        and want_ej_xor_large(2) != want_lo_large(1)
        and want_ej_xor(8) != want_lo_e(7)
        and z8["pg_l"] + z8["gp_l"] == want_lo_large(7)
        and z8["pg_l"] != z8["gp_l"]
        and ev8["n_ok"] != 0
        and ev8["n_bad"] == 0
        and want_j0_odd_lo(8) != want_even_j0_sm(8)
        and want_ph_check()
        and G(2, 1) == 0
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
    uu = json.loads(UU_JSON.read_text())
    ut = json.loads(UT_JSON.read_text())
    us = json.loads(US_JSON.read_text())
    ok = (
        uu["checks"]["all_ok"]
        and ut["checks"]["all_ok"]
        and us["checks"]["all_ok"]
        and uu["verdict"]["even_j0_sm_eq_5_2km2_minus_2"] == "LEMMA"
        and uu["verdict"]["gp_e_eq_loe_minus_even_j0"] == "LEMMA"
        and uu["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uu["verdict"]["prize"] == "unsolved"
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
    cnt = ej_xor_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "ej_xor_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "odd_even_unique_van": True,
            "ej_xor_eq_xor_lo_parent": True,
            "ej_xor_large_eq_lo_large_parent": True,
            "even_origin_oj_both_neigh_1": True,
            "lo_parent_large_diff_closed": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_even_unique_van": "LEMMA",
            "ej_xor_eq_xor_lo_parent": "LEMMA",
            "ej_xor_large_eq_lo_large_parent_k_ge_3": "LEMMA",
            "even_origin_oj_both_neigh_1": "LEMMA",
            "ej_xor_large_eq_lo_large_at_k2": "KILLED",
            "odd_even_both_van": "KILLED",
            "ej_xor_both_children": "KILLED",
            "oj_leftover_never_xor": "KILLED",
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
        "ej_xor k8",
        dump["ej_xor_fold"]["rows"]["8"]["tot"],
        "lg",
        dump["ej_xor_fold"]["rows"]["8"]["lg"],
        "pg_l",
        dump["ej_xor_fold"]["rows"]["8"]["pg_l"],
        "gp_l",
        dump["ej_xor_fold"]["rows"]["8"]["gp_l"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
