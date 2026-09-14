#!/usr/bin/env python3
"""Cycle TN: every v2(n+1)=a class has a time AP; even d=2 times too.

Covering times of n with v2(n+1)=a are the AP 10U-2^{a+1}+1 step
2^{a+2}, for every a>=1. Odd a is d=1 (Cycle TM); even a>=2 is odd
d=2. Even d=2 times are the APs 10U-2^{b+2}+3 step 2^{b+3} over
odd b; b=1 recovers n=2 mod 8. Not rest=S xor T. Do not walk
leftover p catalogues. Do not walk leftover d catalogues. Do not
walk k=11 packed covering. Do not walk k=12 T-bands. Not a prize
claim.

Run: python3 research/cycle_tn.py --certify
Dump: research/cycle_tn.json
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
from cycle_tk import residue8_ap_ok, residue8_t_hi, residue8_t_lo
from cycle_tl import d1_val_count, d1_v2, d2_v2
from cycle_tm import (
    d1_time_ap_ok,
    d1_time_hi,
    d1_time_lo,
    d1_time_step,
    d2_even_ap_count,
    d2_even_val_count,
    d2_odd_ap_count,
)

OUT = Path(__file__).resolve().with_suffix(".json")
TM_JSON = Path(__file__).resolve().parent / "cycle_tm.json"
TL_JSON = Path(__file__).resolve().parent / "cycle_tl.json"
TK_JSON = Path(__file__).resolve().parent / "cycle_tk.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def val_time_ap_ok(k: int, a: int) -> bool:
    """Any a>=1: length d1_val_count, endpoints matching covering_t of n-AP."""
    if a < 1:
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


def even_d2_time_hi(k: int, b: int) -> int:
    """Greatest covering time on even d=2 AP with v2(n/2+1)=b."""
    return 10 * (1 << k) - (1 << (b + 2)) + 3


def even_d2_time_step(b: int) -> int:
    """Time step of even d=2 AP: 2^{b+3}."""
    return 1 << (b + 3)


def even_d2_time_lo(k: int, b: int) -> int:
    """Least covering time on even d=2 AP with v2(n/2+1)=b."""
    cnt = d2_even_val_count(k, b)
    return even_d2_time_hi(k, b) - even_d2_time_step(b) * (cnt - 1) if cnt else 0


def even_d2_time_ap_ok(k: int, b: int) -> bool:
    """Odd b: length d2_even_val_count, endpoints matching covering_t."""
    if b < 1 or b % 2 == 0:
        return False
    cnt = d2_even_val_count(k, b)
    if cnt == 0:
        return (1 << (b + 1)) - 2 >= (1 << (k + 2))
    hi = even_d2_time_hi(k, b)
    lo = even_d2_time_lo(k, b)
    step = even_d2_time_step(b)
    if lo > hi or (hi - lo) % step or ((hi - lo) // step) + 1 != cnt:
        return False
    n_lo = (1 << (b + 1)) - 2
    n_hi = n_lo + (1 << (b + 2)) * (cnt - 1)
    return covering_t(k, n_lo) == hi and covering_t(k, n_hi) == lo


def tot_form() -> dict:
    """k<=64: every a has a time AP; even d=2 times; b=1 is n=2 mod 8."""
    n_ok = 0
    if not val_time_ap_ok(0, 1) or not val_time_ap_ok(0, 2):
        return {"ok": False, "k0": True}
    if not even_d2_time_ap_ok(0, 1):
        return {"ok": False, "e0": True}
    if even_d2_time_hi(0, 1) != 5 or covering_t(0, 2) != 5:
        return {"ok": False, "t0": True}
    for k in range(0, K_ALG + 1):
        if d2_even_ap_count(k) != want_d2_parity_n(k):
            return {"ok": False, "d2e": True, "k": k}
        if d2_odd_ap_count(k) != want_d2_parity_n(k):
            return {"ok": False, "d2o": True, "k": k}
        cap = 1 << (k + 2)
        a = 1
        while (1 << a) - 1 < cap:
            if not val_time_ap_ok(k, a):
                return {"ok": False, "val": True, "k": k, "a": a}
            if a % 2 and not d1_time_ap_ok(k, a):
                return {"ok": False, "odd": True, "k": k, "a": a}
            a += 1
        b = 1
        while (1 << (b + 1)) - 2 < cap:
            if not even_d2_time_ap_ok(k, b):
                return {"ok": False, "eb": True, "k": k, "b": b}
            b += 2
        if d1_time_hi(k, 2) != 10 * (1 << k) - 7:
            return {"ok": False, "a2hi": True, "k": k}
        if d1_time_step(2) != 16:
            return {"ok": False, "a2st": True, "k": k}
        if k >= 1:
            if not residue8_ap_ok(k, 2) or not residue8_ap_ok(k, 3):
                return {"ok": False, "r8": True, "k": k}
            if even_d2_time_lo(k, 1) != residue8_t_lo(k, 2):
                return {"ok": False, "b1lo": True, "k": k}
            if even_d2_time_hi(k, 1) != residue8_t_hi(k, 2):
                return {"ok": False, "b1hi": True, "k": k}
            if d1_time_lo(k, 2) != residue8_t_lo(k, 3):
                return {"ok": False, "a2lo": True, "k": k}
            if d1_time_hi(k, 2) != residue8_t_hi(k, 3):
                return {"ok": False, "a2r": True, "k": k}
        u = 1 << k
        samples = {2, 3, 6, 7, 10, 11, 14, 15, 4 * u - 2, 4 * u - 1}
        for n in samples:
            if n < 0 or n >= 4 * u:
                continue
            t = covering_t(k, n)
            if n % 2:
                aa = v2(n + 1)
                lo, hi = d1_time_lo(k, aa), d1_time_hi(k, aa)
                if t < lo or t > hi or (hi - t) % d1_time_step(aa):
                    return {"ok": False, "ot": True, "k": k, "n": n}
            elif n >= 2 and d2_v2(n):
                bb = v2((n // 2) + 1)
                lo, hi = even_d2_time_lo(k, bb), even_d2_time_hi(k, bb)
                if t < lo or t > hi or (hi - t) % even_d2_time_step(bb):
                    return {"ok": False, "et": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and val_time_ap_ok(64, 2)
        and even_d2_time_ap_ok(64, 1)
        and d2_even_ap_count(7) == 85
        and even_d2_time_step(1) == 16
        and want_d1_n(0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def residue_count() -> dict:
    """k<=12: valuation times and even d=2 times equal the APs."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        cap = 4 * u
        odd_d2_t = []
        even_d2_t = []
        val_t = {}
        for n in range(0, cap):
            t = covering_t(k, n)
            if n >= 1:
                aa = v2(n + 1)
                val_t.setdefault(aa, []).append(t)
            if n >= 2 and d2_v2(n):
                if n % 2:
                    odd_d2_t.append(t)
                else:
                    even_d2_t.append(t)
        recon_odd = []
        a = 2
        while (1 << a) - 1 < cap:
            recon_odd.extend(
                range(d1_time_lo(k, a), d1_time_hi(k, a) + 1, d1_time_step(a))
            )
            a += 2
        if sorted(odd_d2_t) != sorted(recon_odd):
            return {"ok": False, "odd": True, "k": k}
        recon_even = []
        b = 1
        while (1 << (b + 1)) - 2 < cap:
            recon_even.extend(
                range(
                    even_d2_time_lo(k, b),
                    even_d2_time_hi(k, b) + 1,
                    even_d2_time_step(b),
                )
            )
            b += 2
        if sorted(even_d2_t) != sorted(recon_even):
            return {"ok": False, "even": True, "k": k}
        a = 1
        while (1 << a) - 1 < cap:
            got = sorted(val_t.get(a, []))
            want = list(
                range(d1_time_lo(k, a), d1_time_hi(k, a) + 1, d1_time_step(a))
            )
            if got != want:
                return {"ok": False, "val": True, "k": k, "a": a}
            a += 1
        n_ok += 1
        rows[str(k)] = {
            "odd_d2": len(odd_d2_t),
            "even_d2": len(even_d2_t),
            "b1_lo": even_d2_time_lo(k, 1),
            "b1_hi": even_d2_time_hi(k, 1),
            "a2_lo": d1_time_lo(k, 2),
            "a2_hi": d1_time_hi(k, 2),
        }
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["odd_d2"] == 1
        and rows["0"]["even_d2"] == 1
        and rows["0"]["b1_hi"] == 5
        and rows["7"]["odd_d2"] == 85
        and rows["7"]["even_d2"] == 85
        and rows["12"]["odd_d2"] == 2731
        and rows["12"]["even_d2"] == 2731
        and rows["12"]["b1_lo"] == residue8_t_lo(12, 2)
        and rows["12"]["a2_hi"] == residue8_t_hi(12, 3)
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """d=2 times are a single AP; d=1 times are a single AP."""
    ok = (
        d2_even_val_count(2, 1) == 2
        and d2_even_val_count(2, 3) == 1
        and even_d2_time_step(3) != 16
        and d1_time_step(2) == 16
        and d1_v2(7) == 1
        and d2_v2(3) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tm = json.loads(TM_JSON.read_text())
    tl = json.loads(TL_JSON.read_text())
    tk = json.loads(TK_JSON.read_text())
    ok = (
        tm["checks"]["all_ok"]
        and tl["checks"]["all_ok"]
        and tk["checks"]["all_ok"]
        and tm["verdict"]["d1_times_eq_odd_a_ap_union"] == "LEMMA"
        and tm["verdict"]["d2_n_eq_even_a_plus_even_n_aps"] == "LEMMA"
        and tl["verdict"]["d1_iff_v2_odd"] == "LEMMA"
        and tm["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tm["verdict"]["prize"] == "unsolved"
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
        "cycle": "TN",
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
            "val_times_eq_ap_all_a": True,
            "even_a_times_eq_odd_d2": True,
            "even_d2_times_eq_odd_b_aps": True,
            "b1_times_eq_n2_mod8_16_ap": True,
            "d2_times_single_ap": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "val_times_eq_ap_all_a": "LEMMA",
            "even_a_times_eq_odd_d2": "LEMMA",
            "even_d2_times_eq_odd_b_aps": "LEMMA",
            "b1_times_eq_n2_mod8_16_ap": "LEMMA",
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
        "odd_d2 k12",
        dump["residue_count"]["rows"]["12"]["odd_d2"],
        "b1_lo",
        dump["residue_count"]["rows"]["12"]["b1_lo"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
