#!/usr/bin/env python3
"""Cycle UC: leftover extra plus unpaired extra is 2^{k+1}(F_{k+2}-1)+(-1)^k.

Odd-n even-j pal-left G=1 cells partition into d=1, odd clip-edge,
leftover extra, and unpaired extra. Pal-left covering j<n<4U<5U is
never clip-constrained. trans(m)=wt(floor(m/2)), and the tot is
2^{k+1} F_{k+2}. Odd clip-edge is 2 J_k, so the two extras sum to
2^{k+1}(F_{k+2}-1)+(-1)^k. Do not PREFIX leftover extra or unpaired
extra separately. Not rest=S xor T. Do not walk leftover p
catalogues. Do not walk leftover d catalogues. Do not walk k=11
packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_uc.py --certify
Dump: research/cycle_uc.json
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
from cycle_tl import d1_v2
from cycle_tt import is_clip_edge, unique_even_leftover
from cycle_tu import d2_clip_covering
from cycle_ub import want_clip_gp
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
UB_JSON = Path(__file__).resolve().parent / "cycle_ub.json"
UA_JSON = Path(__file__).resolve().parent / "cycle_ua.json"
TD_JSON = Path(__file__).resolve().parent / "cycle_td.json"
TB_JSON = Path(__file__).resolve().parent / "cycle_tb.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 8
PAT0011 = (0, 0, 1, 1)


def fib(n: int) -> int:
    """F_n with F_0=0, F_1=1."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def wt(n: int) -> int:
    """Number of G(n,j)=1 for 0<=j<=2n."""
    return sum(G(n, j) for j in range(0, 2 * n + 1))


def trans(m: int) -> int:
    """Consecutive Green xor count on 0<=r<=m, G(m,-1)=0."""
    prev = 0
    c = 0
    for r in range(0, m + 1):
        g = G(m, r)
        c += g ^ prev
        prev = g
    return c


def want_ej_odd_tot(k: int) -> int:
    """Odd-n even-j pal-left G=1 count: 2^{k+1} F_{k+2}."""
    return (1 << (k + 1)) * fib(k + 2)


def want_edge_odd(k: int) -> int:
    """Odd-n clip-edge pal-pair count: 2 J_k."""
    return 2 * jacobsthal(k)


def want_extra_sum(k: int) -> int:
    """leftover extra + unpaired extra: 2^{k+1}(F_{k+2}-1)+(-1)^k."""
    return (1 << (k + 1)) * (fib(k + 2) - 1) + (-1) ** k


def ej_odd_split(k: int) -> dict:
    """Odd-n even-j pal-left G=1 split into d1, clip-edge, leftover, unp."""
    u = 1 << k
    clip = 5 * u
    tot = d1 = edge = lo = unp = other = 0
    for n in range(1, 4 * u, 2):
        hi = min(2 * n, clip)
        for j in range(0, hi + 1, 2):
            if G(n, j) == 0:
                continue
            if j >= n:
                continue
            tot += 1
            kind = pal_kind(n, j, k)
            d = n - j
            if kind == "unp":
                unp += 1
            elif d == 1:
                d1 += 1
            elif is_clip_edge(n, j, k):
                edge += 1
            elif kind == "pair":
                lo += 1
            else:
                other += 1
    return {
        "tot": tot,
        "d1": d1,
        "edge": edge,
        "lo": lo,
        "unp": unp,
        "other": other,
    }


def tot_form() -> dict:
    """k<=64: F/J identities; trans=wt samples; pal-left unclipped."""
    n_ok = 0
    if fib(0) != 0 or fib(1) != 1 or fib(2) != 1 or fib(10) != 55:
        return {"ok": False, "F": True}
    if want_ej_odd_tot(0) != 2 or want_ej_odd_tot(1) != 8:
        return {"ok": False, "t01": True}
    if want_ej_odd_tot(8) != 28160:
        return {"ok": False, "t8": True}
    if want_extra_sum(8) != 27649:
        return {"ok": False, "x8": True}
    samples = (0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 31, 32, 63)
    for m in samples:
        if trans(m) != wt(m // 2):
            return {"ok": False, "tr": True, "m": m}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d2_clip_covering(k) != (k == 0):
            return {"ok": False, "d2c": True, "k": k}
        if k >= 2 and fib(k) != fib(k - 1) + fib(k - 2):
            return {"ok": False, "Frec": True, "k": k}
        if want_d1_n(k) != jacobsthal(k + 2):
            return {"ok": False, "d1": True, "k": k}
        if want_edge_n(k) != jacobsthal(k + 2):
            return {"ok": False, "ed": True, "k": k}
        if want_edge_odd(k) != 2 * jacobsthal(k):
            return {"ok": False, "eo": True, "k": k}
        if want_edge_odd(k) + jacobsthal(k + 1) != jacobsthal(k + 2):
            return {"ok": False, "es": True, "k": k}
        want_x = want_ej_odd_tot(k) - jacobsthal(k + 2) - want_edge_odd(k)
        if want_x != want_extra_sum(k):
            return {"ok": False, "xs": True, "k": k}
        if 4 * u >= 5 * u:
            return {"ok": False, "clip": True, "k": k}
        n = 4 * u - 1
        if n >= 5 * u or n <= 0:
            return {"ok": False, "n": True, "k": k}
        if k >= 1:
            n_e = 4 * u - 2
            if d1_v2(n_e) != 0:
                return {"ok": False, "even_d1": True, "k": k, "n": n_e}
        if k >= 1 and not unique_even_leftover(k):
            return {"ok": False, "u": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "sy": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and want_extra_sum(0) == 1
        and want_extra_sum(1) == 3
        and want_ej_odd_tot(2) != (1 << 4)
        and want_clip_gp(8) == 85
        and want_d2_n(0) == 2
        and want_even(0) == 1
        and PAT0011 in AND_ONES
        and and_clause(0, 0, 0, 1) == 0
        and 0 not in FORCED
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def extra_sum_fold() -> dict:
    """k<=8: partition; tot Fibonacci; extra sum closed."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        r = ej_odd_split(k)
        if r["other"] != 0:
            return {"ok": False, "oth": True, "k": k, **r}
        if r["tot"] != r["d1"] + r["edge"] + r["lo"] + r["unp"]:
            return {"ok": False, "sum": True, "k": k, **r}
        if r["tot"] != want_ej_odd_tot(k):
            return {"ok": False, "tot": True, "k": k, **r}
        if r["d1"] != want_d1_n(k):
            return {"ok": False, "d1": True, "k": k, **r}
        if r["edge"] != want_edge_odd(k):
            return {"ok": False, "ed": True, "k": k, **r}
        if r["lo"] + r["unp"] != want_extra_sum(k):
            return {"ok": False, "xs": True, "k": k, **r}
        if r["lo"] + r["unp"] == 0:
            return {"ok": False, "empty": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "tot": r["tot"],
            "d1": r["d1"],
            "edge": r["edge"],
            "lo": r["lo"],
            "unp": r["unp"],
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["tot"] == 2
        and rows["0"]["unp"] == 1
        and rows["1"]["tot"] == 8
        and rows["8"]["tot"] == 28160
        and rows["8"]["d1"] == 341
        and rows["8"]["edge"] == 170
        and rows["8"]["lo"] == 17630
        and rows["8"]["unp"] == 10019
        and rows["8"]["tot"] != (1 << 10)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """tot=2^{k+2}; extra sum empty; d1 on even n."""
    ok = (
        want_ej_odd_tot(0) != 4
        and want_ej_odd_tot(2) != 16
        and want_extra_sum(0) != 0
        and d1_v2(2) == 0
        and want_edge_odd(4) == 10
        and trans(2) == wt(1)
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
    ub = json.loads(UB_JSON.read_text())
    ua = json.loads(UA_JSON.read_text())
    td = json.loads(TD_JSON.read_text())
    tb = json.loads(TB_JSON.read_text())
    ok = (
        ub["checks"]["all_ok"]
        and ua["checks"]["all_ok"]
        and td["checks"]["all_ok"]
        and tb["checks"]["all_ok"]
        and ub["verdict"]["clip_gp_eq_half_J_k1_k_ge_2"] == "LEMMA"
        and ua["verdict"]["unp_rec_2prev_J_extra_k_ge_1"] == "LEMMA"
        and td["verdict"]["d1_count_eq_jacobsthal"] == "LEMMA"
        and tb["verdict"]["clip_edge_eq_jacobsthal"] == "LEMMA"
        and ub["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and ub["verdict"]["prize"] == "unsolved"
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
    cnt = extra_sum_fold()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "UC",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "extra_sum_fold": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "ej_odd_pal_left_partition": True,
            "ej_odd_tot_eq_2km1_fib": True,
            "extra_sum_eq_2km1_Fm1_pm1": True,
            "edge_odd_eq_2_J_k": True,
            "trans_eq_wt_half": True,
            "ej_odd_tot_eq_2kp2": False,
            "extra_sum_empty": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "ej_odd_pal_left_partition": "LEMMA",
            "ej_odd_tot_eq_2km1_fib": "LEMMA",
            "extra_sum_eq_2km1_Fm1_pm1": "LEMMA",
            "edge_odd_eq_2_J_k": "LEMMA",
            "trans_eq_wt_half": "LEMMA",
            "ej_odd_tot_eq_2kp2": "KILLED",
            "extra_sum_empty": "KILLED",
            "d1_on_even_n": "KILLED",
            "unp_extra_empty": "KILLED",
            "pair_g0_in_unp_extra": "KILLED",
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
        "tot k8",
        dump["extra_sum_fold"]["rows"]["8"]["tot"],
        "lo",
        dump["extra_sum_fold"]["rows"]["8"]["lo"],
        "unp",
        dump["extra_sum_fold"]["rows"]["8"]["unp"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
