#!/usr/bin/env python3
"""Cycle TM: d=1 covering times are odd-a APs; d=2 n is even-a plus even-n.

Covering times of d=1 pal-pairs are the disjoint union of APs
t=10U-2^{a+1}+1 down by 2^{a+2} over odd a. The a=1 slice is
Cycle TH's n=1 mod 4 8-AP. Odd d=2 covering n is the even-a>=2
n-AP union; even d=2 is n=2^{b+1}-2 step 2^{b+2} over odd b.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
leftover d catalogues. Do not walk k=11 packed covering. Do not
walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tm.py --certify
Dump: research/cycle_tm.json
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
from cycle_al import v2
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hh import AND_ONES
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_td import want_d1_n
from cycle_te import want_d2_n, want_d2_parity_n
from cycle_th import n1_ap_ok
from cycle_ti import residue_t_hi, residue_t_lo
from cycle_tl import d1_ap_count, d1_v2, d1_val_count, d2_v2

OUT = Path(__file__).resolve().with_suffix(".json")
TL_JSON = Path(__file__).resolve().parent / "cycle_tl.json"
TK_JSON = Path(__file__).resolve().parent / "cycle_tk.json"
TH_JSON = Path(__file__).resolve().parent / "cycle_th.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def d1_time_hi(k: int, a: int) -> int:
    """Greatest covering time on the v2(n+1)=a d=1 AP."""
    return 10 * (1 << k) - (1 << (a + 1)) + 1


def d1_time_step(a: int) -> int:
    """Time step of the v2(n+1)=a AP: 2^{a+2}."""
    return 1 << (a + 2)


def d1_time_lo(k: int, a: int) -> int:
    """Least covering time on the v2(n+1)=a d=1 AP."""
    cnt = d1_val_count(k, a)
    return d1_time_hi(k, a) - d1_time_step(a) * (cnt - 1) if cnt else 0


def d1_time_ap_ok(k: int, a: int) -> bool:
    """Odd a: length d1_val_count, endpoints matching covering_t of n-AP."""
    if a < 1 or a % 2 == 0:
        return False
    cnt = d1_val_count(k, a)
    if cnt == 0:
        return (1 << a) - 1 >= (1 << (k + 2))
    hi = d1_time_hi(k, a)
    lo = d1_time_lo(k, a)
    step = d1_time_step(a)
    if lo > hi or (hi - lo) % step or ((hi - lo) // step) + 1 != cnt:
        return False
    n_lo = (1 << a) - 1
    n_hi = n_lo + (1 << (a + 1)) * (cnt - 1)
    return covering_t(k, n_lo) == hi and covering_t(k, n_hi) == lo


def d2_even_val_count(k: int, b: int) -> int:
    """Even covering n with v2(n/2+1)=b: AP 2^{b+1}-2 step 2^{b+2}."""
    if b < 1:
        return 0
    cap = 1 << (k + 2)
    lo = (1 << (b + 1)) - 2
    if lo >= cap:
        return 0
    step = 1 << (b + 2)
    return ((cap - 1 - lo) // step) + 1


def d2_even_ap_count(k: int) -> int:
    """Sum of even d=2 AP lengths over odd b."""
    tot = 0
    b = 1
    cap = 1 << (k + 2)
    while (1 << (b + 1)) - 2 < cap:
        tot += d2_even_val_count(k, b)
        b += 2
    return tot


def d2_odd_ap_count(k: int) -> int:
    """Sum of odd d=2 n-AP lengths over even a>=2."""
    tot = 0
    a = 2
    cap = 1 << (k + 2)
    while (1 << a) - 1 < cap:
        tot += d1_val_count(k, a)
        a += 2
    return tot


def tot_form() -> dict:
    """k<=64: d=1 time AP endpoints; a=1 is n=1 mod 4; d=2 AP counts."""
    n_ok = 0
    if not d1_time_ap_ok(0, 1):
        return {"ok": False, "k0": True}
    if d1_time_hi(0, 1) != 7 or covering_t(0, 1) != 7:
        return {"ok": False, "t0": True}
    if d2_even_ap_count(0) != 1 or d2_odd_ap_count(0) != 1:
        return {"ok": False, "d20": True}
    for k in range(0, K_ALG + 1):
        u = 1 << k
        if d1_ap_count(k) != want_d1_n(k):
            return {"ok": False, "d1": True, "k": k}
        if d2_even_ap_count(k) != want_d2_parity_n(k):
            return {"ok": False, "d2e": True, "k": k}
        if d2_odd_ap_count(k) != want_d2_parity_n(k):
            return {"ok": False, "d2o": True, "k": k}
        if d2_even_ap_count(k) + d2_odd_ap_count(k) != want_d2_n(k):
            return {"ok": False, "d2sum": True, "k": k}
        a = 1
        while (1 << a) - 1 < (1 << (k + 2)):
            if a % 2 and not d1_time_ap_ok(k, a):
                return {"ok": False, "ap": True, "k": k, "a": a}
            a += 2
        if not n1_ap_ok(k):
            return {"ok": False, "n1": True, "k": k}
        if d1_time_lo(k, 1) != residue_t_lo(k, 1):
            return {"ok": False, "a1lo": True, "k": k}
        if d1_time_hi(k, 1) != residue_t_hi(k, 1):
            return {"ok": False, "a1hi": True, "k": k}
        if d1_time_step(1) != 8 or d1_val_count(k, 1) != u:
            return {"ok": False, "a1n": True, "k": k}
        samples = {
            1,
            5,
            7,
            11,
            15,
            u + 1,
            4 * u - 7,
            4 * u - 5,
            4 * u - 3,
            4 * u - 1,
        }
        for n in samples:
            if n < 0 or n >= 4 * u:
                continue
            if not d1_v2(n):
                continue
            aa = v2(n + 1)
            t = covering_t(k, n)
            lo = d1_time_lo(k, aa)
            hi = d1_time_hi(k, aa)
            if t < lo or t > hi or (hi - t) % d1_time_step(aa):
                return {"ok": False, "t": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and d1_time_ap_ok(64, 1)
        and d1_time_ap_ok(64, 65)
        and d2_even_ap_count(7) == 85
        and d2_odd_ap_count(12) == 2731
        and want_d1_n(0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def residue_count() -> dict:
    """k<=12: d=1 times = odd-a time APs; d=2 n = even-a plus even-n APs."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        cap = 4 * u
        d1_t = []
        d2_n = []
        for n in range(0, cap):
            if d1_v2(n):
                d1_t.append(covering_t(k, n))
            if n >= 2 and d2_v2(n):
                d2_n.append(n)
        recon_t = []
        a = 1
        while (1 << a) - 1 < cap:
            lo = d1_time_lo(k, a)
            hi = d1_time_hi(k, a)
            step = d1_time_step(a)
            recon_t.extend(range(lo, hi + 1, step))
            a += 2
        if sorted(d1_t) != sorted(recon_t):
            return {
                "ok": False,
                "t": True,
                "k": k,
                "n_got": len(d1_t),
                "n_recon": len(recon_t),
            }
        recon_n = []
        b = 1
        while (1 << (b + 1)) - 2 < cap:
            recon_n.extend(
                range((1 << (b + 1)) - 2, cap, 1 << (b + 2))
            )
            b += 2
        c = 2
        while (1 << c) - 1 < cap:
            recon_n.extend(range((1 << c) - 1, cap, 1 << (c + 1)))
            c += 2
        if sorted(d2_n) != sorted(recon_n):
            return {
                "ok": False,
                "n": True,
                "k": k,
                "n_got": len(d2_n),
                "n_recon": len(recon_n),
            }
        n_ok += 1
        rows[str(k)] = {
            "d1": len(d1_t),
            "d2": len(d2_n),
            "a1_lo": d1_time_lo(k, 1),
            "a1_hi": d1_time_hi(k, 1),
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["d1"] == 1
        and rows["0"]["d2"] == 2
        and rows["0"]["a1_lo"] == 7
        and rows["7"]["d1"] == 171
        and rows["12"]["d1"] == 5461
        and rows["12"]["d2"] == 5462
        and rows["12"]["a1_lo"] == residue_t_lo(12, 1)
        and rows["12"]["a1_hi"] == residue_t_hi(12, 1)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """d=1 times are a single AP; d=1 iff n=1 mod 4."""
    ok = (
        d1_val_count(1, 3) == 1
        and d1_val_count(1, 1) == 2
        and d1_time_step(3) != 8
        and d1_v2(7) == 1
        and (7 % 4) == 3
        and d2_v2(3) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tl = json.loads(TL_JSON.read_text())
    tk = json.loads(TK_JSON.read_text())
    th = json.loads(TH_JSON.read_text())
    ok = (
        tl["checks"]["all_ok"]
        and tk["checks"]["all_ok"]
        and th["checks"]["all_ok"]
        and tl["verdict"]["d1_eq_odd_a_ap_union"] == "LEMMA"
        and tl["verdict"]["G_nm1_eq_v2_nplus1"] == "LEMMA"
        and th["verdict"]["n1_times_eq_8_ap"] == "LEMMA"
        and tl["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tl["verdict"]["prize"] == "unsolved"
        and want_odd(0) == 1
        and want_d1_n(0) == 1
        and want_d2_n(0) == 2
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
    cnt = residue_count()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "residue_count": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d1_times_eq_odd_a_ap_union": True,
            "a1_times_eq_n1_mod4_8_ap": True,
            "d2_n_eq_even_a_plus_even_n_aps": True,
            "d1_times_single_ap": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d1_times_eq_odd_a_ap_union": "LEMMA",
            "a1_times_eq_n1_mod4_8_ap": "LEMMA",
            "d2_n_eq_even_a_plus_even_n_aps": "LEMMA",
            "d1_times_single_ap": "KILLED",
            "G_nm1_iff_n1_mod4": "KILLED",
            "d1_iff_n1_mod4": "KILLED",
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
        "d1 k12",
        dump["residue_count"]["rows"]["12"]["d1"],
        "a1_lo",
        dump["residue_count"]["rows"]["12"]["a1_lo"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
