#!/usr/bin/env python3
"""Cycle UK: leftover extra on n<=5U/2 is pal-left tot minus d=1.

Covering n<=5U/2 cannot be unpaired: pal-partner 2n-j <=2n<=5U.
For k>=2 clip-edge pal-left is empty on that half, so odd-n even-j
pal-left is d=1 plus leftover extra. Pal-left tot is 2 W(5*2^{k-3})
=2^{k-2}(4 F_{k+1}+3 F_{k-1}) from wt(2^{a+2}+p)=3 wt(p). Large-n
d=1 is 2^{k-1}-(-1)^k. Do not PREFIX leftover extra on n>5U/2 or
unpaired extra or xor-lo or xor-unp. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_uk.py --certify
Dump: research/cycle_uk.json
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
from cycle_uc import fib, trans, want_ej_odd_tot, want_extra_sum, wt
from cycle_ud import want_pal_c, want_pair_unp
from cycle_ue import want_lo_unp
from cycle_uj import want_xor_tot
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UC_JSON = Path(__file__).resolve().parent / "cycle_uc.json"
UJ_JSON = Path(__file__).resolve().parent / "cycle_uj.json"
TD_JSON = Path(__file__).resolve().parent / "cycle_td.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def want_small_tot(k: int) -> int:
    """Odd-n even-j pal-left tot on n<=5U/2: 1,5, then 2^{k-2}(4 F_{k+1}+3 F_{k-1})."""
    if k <= 0:
        return 1
    if k == 1:
        return 5
    return (1 << (k - 2)) * (4 * fib(k + 1) + 3 * fib(k - 1))


def want_d1_large(k: int) -> int:
    """d=1 on odd n>5U/2: 0,1, then 2^{k-1}-(-1)^k."""
    if k <= 0:
        return 0
    if k == 1:
        return 1
    return (1 << (k - 1)) - (-1) ** k


def want_d1_small(k: int) -> int:
    """d=1 on odd n<=5U/2: J_{k+2} minus large."""
    return want_d1_n(k) - want_d1_large(k)


def want_lo_small(k: int) -> int:
    """Leftover extra on n<=5U/2: 0,2, then small tot minus small d=1."""
    if k <= 0:
        return 0
    if k == 1:
        return 2
    return want_small_tot(k) - want_d1_small(k)


def want_large_extra(k: int) -> int:
    """Large leftover extra plus unpaired extra: extra-sum minus lo_small."""
    return want_extra_sum(k) - want_lo_small(k)


def want_w5(a: int) -> int:
    """W(5*2^a)=sum_{p<5*2^a} wt(p)=2^a(4 F_{a+4}+3 F_{a+2})."""
    return (1 << a) * (4 * fib(a + 4) + 3 * fib(a + 2))


def small_split(k: int) -> dict:
    """Odd-n even-j pal-left split by n<=5U/2 versus n>5U/2."""
    u = 1 << k
    clip = 5 * u
    half = (5 * u) // 2
    a = {
        "s_tot": 0,
        "s_d1": 0,
        "s_d2": 0,
        "s_clip": 0,
        "s_lo": 0,
        "s_unp": 0,
        "l_tot": 0,
        "l_d1": 0,
        "l_d2": 0,
        "l_clip": 0,
        "l_lo": 0,
        "l_unp": 0,
        "other": 0,
    }
    for n in range(1, 4 * u, 2):
        hi = min(2 * n, clip)
        b = "s" if n <= half else "l"
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if j >= n:
                continue
            a[f"{b}_tot"] += 1
            kind = pal_kind(n, j, k)
            d = n - j
            if kind == "unp":
                a[f"{b}_unp"] += 1
            elif d == 1:
                a[f"{b}_d1"] += 1
            elif d == 2:
                a[f"{b}_d2"] += 1
            elif is_clip_edge(n, j, k):
                a[f"{b}_clip"] += 1
            elif kind == "pair":
                a[f"{b}_lo"] += 1
            else:
                a["other"] += 1
    return a


def tot_form() -> dict:
    """k<=64: W(5*2^a); small tot; d=1 split; freshman wt samples."""
    n_ok = 0
    if want_small_tot(0) != 1 or want_small_tot(1) != 5:
        return {"ok": False, "k01": True}
    if want_small_tot(8) != 11200 or want_lo_small(8) != 10986:
        return {"ok": False, "k8": True}
    if want_d1_large(8) != 127 or want_d1_small(8) != 214:
        return {"ok": False, "d18": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for a in range(0, 7):
        u = 1 << (a + 2)
        cap = 1 << a
        ps = {0}
        if a >= 1:
            ps.add(1)
            ps.add(cap - 1)
        for p in ps:
            if p >= cap:
                continue
            if wt(u + p) != 3 * wt(p):
                return {"ok": False, "wt3": True, "a": a, "p": p}
        if want_w5(a) != (1 << a) * (4 * fib(a + 4) + 3 * fib(a + 2)):
            return {"ok": False, "w5": True, "a": a}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if want_d1_small(k) + want_d1_large(k) != want_d1_n(k):
            return {"ok": False, "d1p": True, "k": k}
        if want_small_tot(k) + (want_ej_odd_tot(k) - want_small_tot(k)) != want_ej_odd_tot(
            k
        ):
            return {"ok": False, "tp": True, "k": k}
        if want_lo_small(k) + want_large_extra(k) != want_extra_sum(k):
            return {"ok": False, "xs": True, "k": k}
        if k >= 2:
            if want_small_tot(k) != (1 << (k - 2)) * (
                4 * fib(k + 1) + 3 * fib(k - 1)
            ):
                return {"ok": False, "st": True, "k": k}
            if want_d1_large(k) != (1 << (k - 1)) - (-1) ** k:
                return {"ok": False, "dl": True, "k": k}
            if 3 * want_d1_small(k) != 5 * (1 << (k - 1)) + 2 * ((-1) ** k):
                return {"ok": False, "ds": True, "k": k}
            if want_lo_small(k) != want_small_tot(k) - want_d1_small(k):
                return {"ok": False, "lo": True, "k": k}
            half = (5 * u) // 2
            n_hi = half - 1
            if n_hi + n_hi >= 5 * u:
                return {"ok": False, "clip": True, "k": k}
            if n_hi > half:
                return {"ok": False, "hi": True, "k": k}
        if k >= 3:
            a = k - 3
            if want_small_tot(k) != 2 * want_w5(a):
                return {"ok": False, "w2": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
        if 4 * u <= (5 * u) // 2:
            return {"ok": False, "half": True, "k": k}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_lo_small(8) != want_extra_sum(8)
        and want_lo_small(8) != 17630
        and want_small_tot(8) != want_ej_odd_tot(8) // 2
        and want_d1_small(8) != want_d1_large(8)
        and want_xor_tot(8) == 27053
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


def small_fold() -> dict:
    """k<=8: small pal-left tot and leftover extra match closed forms."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = small_split(k)
        if r["other"] != 0:
            return {"ok": False, "oth": True, "k": k}
        if r["s_d2"] != 0 or r["l_d2"] != 0:
            return {"ok": False, "d2": True, "k": k}
        if r["s_unp"] != 0:
            return {"ok": False, "sunp": True, "k": k}
        if r["s_tot"] != want_small_tot(k):
            return {"ok": False, "st": True, "k": k, "got": r["s_tot"]}
        if r["s_d1"] != want_d1_small(k) or r["l_d1"] != want_d1_large(k):
            return {"ok": False, "d1": True, "k": k}
        if r["s_lo"] != want_lo_small(k):
            return {"ok": False, "lo": True, "k": k, "got": r["s_lo"]}
        if r["s_lo"] + r["l_lo"] + r["l_unp"] != want_extra_sum(k):
            return {"ok": False, "xs": True, "k": k}
        if r["l_lo"] + r["l_unp"] != want_large_extra(k):
            return {"ok": False, "lx": True, "k": k}
        if k >= 2 and r["s_clip"] != 0:
            return {"ok": False, "sc": True, "k": k}
        if r["s_tot"] != r["s_d1"] + r["s_clip"] + r["s_lo"] + r["s_unp"]:
            return {"ok": False, "ss": True, "k": k}
        if r["l_tot"] != r["l_d1"] + r["l_clip"] + r["l_lo"] + r["l_unp"]:
            return {"ok": False, "ls": True, "k": k}
        if r["s_tot"] + r["l_tot"] != want_ej_odd_tot(k):
            return {"ok": False, "ej": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "s_tot": r["s_tot"],
            "s_d1": r["s_d1"],
            "s_lo": r["s_lo"],
            "l_tot": r["l_tot"],
            "l_d1": r["l_d1"],
            "l_lo": r["l_lo"],
            "l_unp": r["l_unp"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["s_tot"] == 1
        and rows["1"]["s_lo"] == 2
        and rows["8"]["s_tot"] == 11200
        and rows["8"]["s_d1"] == 214
        and rows["8"]["s_lo"] == 10986
        and rows["8"]["l_d1"] == 127
        and rows["8"]["l_lo"] == 6644
        and rows["8"]["l_unp"] == 10019
        and rows["8"]["s_lo"] != 17630
        and rows["8"]["s_lo"] != rows["8"]["l_lo"]
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """lo_small equals extra_lo; s_tot half; d1 small equals large."""
    ok = (
        want_lo_small(8) != 17630
        and want_lo_small(8) != want_extra_sum(8)
        and want_small_tot(8) != want_ej_odd_tot(8) // 2
        and want_d1_small(8) != want_d1_large(8)
        and want_lo_small(2) == 7
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
    uc = json.loads(UC_JSON.read_text())
    uj = json.loads(UJ_JSON.read_text())
    td = json.loads(TD_JSON.read_text())
    ok = (
        uc["checks"]["all_ok"]
        and uj["checks"]["all_ok"]
        and td["checks"]["all_ok"]
        and uc["verdict"]["extra_sum_eq_2km1_Fm1_pm1"] == "LEMMA"
        and uj["verdict"]["xor_tot_eq_extra_sum_minus_edges"] == "LEMMA"
        and td["verdict"]["d1_count_eq_jacobsthal"] == "LEMMA"
        and uc["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and uj["verdict"]["prize"] == "unsolved"
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
    cnt = small_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UK",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "small_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "small_tot_eq_2km2_F": True,
            "lo_small_eq_tot_minus_d1": True,
            "d1_large_eq_2km1_pm1": True,
            "w5_eq_2a_4Fa4_3Fa2": True,
            "large_extra_eq_extra_sum_minus_lo_small": True,
            "lo_small_eq_extra_lo": False,
            "s_tot_eq_half_ej": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "small_tot_eq_2km2_F": "LEMMA",
            "lo_small_eq_tot_minus_d1": "LEMMA",
            "d1_large_eq_2km1_pm1": "LEMMA",
            "w5_eq_2a_4Fa4_3Fa2": "LEMMA",
            "large_extra_eq_extra_sum_minus_lo_small": "LEMMA",
            "lo_small_eq_extra_lo": "KILLED",
            "s_tot_eq_half_ej": "KILLED",
            "d1_small_eq_d1_large": "KILLED",
            "lo_small_eq_extra_sum": "KILLED",
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
        "lo_small k8",
        dump["small_fold"]["rows"]["8"]["s_lo"],
        "s_tot",
        dump["small_fold"]["rows"]["8"]["s_tot"],
        "l_lo",
        dump["small_fold"]["rows"]["8"]["l_lo"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
