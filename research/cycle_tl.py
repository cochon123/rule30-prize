#!/usr/bin/env python3
"""Cycle TL: G(n, n-1) is v2(n+1) mod 2.

The pal-adjacent Green bit equals the 2-adic valuation of n+1
mod 2. Hence d=1 pal-pairs are covering n with v2(n+1) odd, and
d=2 pal-pairs are covering n with v2(floor(n/2)+1) odd. The d=1
set is the disjoint union of APs 2^a-1, 2^a-1+2^{a+1}, ... over
odd a. Not rest=S xor T. Do not walk leftover p catalogues. Do
not walk leftover d catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tl.py --certify
Dump: research/cycle_tl.json
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
from cycle_al import G, v2
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hh import AND_ONES
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced
from cycle_sy import odd_forced_corr
from cycle_ta import pal_kind
from cycle_tb import jacobsthal
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tk import (
    G_nm1,
    residue8_ap_ok,
    want_d1_r1_n8,
    want_d1_r5_n8,
    want_d1_r7_n8,
)

OUT = Path(__file__).resolve().with_suffix(".json")
TK_JSON = Path(__file__).resolve().parent / "cycle_tk.json"
TJ_JSON = Path(__file__).resolve().parent / "cycle_tj.json"
TF_JSON = Path(__file__).resolve().parent / "cycle_tf.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def d1_v2(n: int) -> int:
    """1 iff v2(n+1) is odd (d=1 pal-pair)."""
    return v2(n + 1) & 1


def d2_v2(n: int) -> int:
    """1 iff v2(floor(n/2)+1) is odd (d=2 pal-pair, n>=2)."""
    return v2((n // 2) + 1) & 1


def d1_val_count(k: int, a: int) -> int:
    """Covering n with v2(n+1)=a: AP 2^a-1 step 2^{a+1} inside 4U."""
    if a < 1:
        return 0
    cap = 1 << (k + 2)
    lo = (1 << a) - 1
    if lo >= cap:
        return 0
    step = 1 << (a + 1)
    return ((cap - 1 - lo) // step) + 1


def d1_ap_count(k: int) -> int:
    """Sum of d=1 AP lengths over odd a."""
    tot = 0
    a = 1
    while (1 << a) - 1 < (1 << (k + 2)):
        tot += d1_val_count(k, a)
        a += 2
    return tot


def tot_form() -> dict:
    """k<=64: v2 form; d=1 AP counts; TK residue sums."""
    n_ok = 0
    if d1_v2(0) != 0 or d1_v2(1) != 1 or d1_v2(3) != 0:
        return {"ok": False, "base": True}
    if d1_v2(7) != 1 or G_nm1(7) != 1 or (v2(8) & 1) != 1:
        return {"ok": False, "n7": True}
    if d2_v2(2) != 1 or d2_v2(3) != 1 or d2_v2(6) != 0:
        return {"ok": False, "d2b": True}
    if d1_ap_count(0) != 1 or d1_ap_count(1) != 3:
        return {"ok": False, "ap0": True}
    for k in range(0, K_ALG + 1):
        if d1_ap_count(k) != want_d1_n(k):
            return {"ok": False, "ap": True, "k": k}
        if d1_ap_count(k) != jacobsthal(k + 2):
            return {"ok": False, "J": True, "k": k}
        if want_d1_r1_n8(k) + want_d1_r5_n8(k) + want_d1_r7_n8(k) != want_d1_n(
            k
        ):
            return {"ok": False, "tk": True, "k": k}
        if k >= 1 and not all(residue8_ap_ok(k, r) for r in range(8)):
            return {"ok": False, "r8": True, "k": k}
        u = 1 << k
        samples = {
            0,
            1,
            2,
            3,
            5,
            6,
            7,
            11,
            15,
            u,
            u + 1,
            3 * u,
            4 * u - 8,
            4 * u - 7,
            4 * u - 6,
            4 * u - 5,
            4 * u - 4,
            4 * u - 3,
            4 * u - 2,
            4 * u - 1,
        }
        for n in samples:
            if n < 0 or n >= 4 * u:
                continue
            g1 = G(n, n - 1) if n >= 1 else 0
            if g1 != G_nm1(n) or g1 != d1_v2(n):
                return {"ok": False, "g1": True, "k": k, "n": n}
            if n >= 2:
                g2 = G(n, n - 2)
                if g2 != d2_v2(n):
                    return {"ok": False, "g2": True, "k": k, "n": n}
            if d1_v2(n) and pal_kind(n, n - 1, k) != "pair":
                return {"ok": False, "kind1": True, "k": k, "n": n}
            if n >= 2 and d2_v2(n) and pal_kind(n, n - 2, k) != "pair":
                return {"ok": False, "kind2": True, "k": k, "n": n}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and d1_ap_count(7) == 171
        and d1_ap_count(12) == 5461
        and d1_v2(7) == 1
        and d1_v2(15) == 0
        and d2_v2(14) == 1
        and G_nm1(7) == (v2(8) & 1)
        and want_d1_n(0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def residue_count() -> dict:
    """k<=12: v2 bits match Green; d=1 equals odd-a AP union."""
    n_ok = 0
    rows = {}
    for k in range(0, K_COUNT + 1):
        u = 1 << k
        cap = 4 * u
        d1 = d2 = 0
        got = set()
        for n in range(0, cap):
            if G_nm1(n) != d1_v2(n):
                return {"ok": False, "nm1": True, "k": k, "n": n}
            if n >= 1 and G(n, n - 1) != d1_v2(n):
                return {"ok": False, "g1": True, "k": k, "n": n}
            if n >= 2 and G(n, n - 2) != d2_v2(n):
                return {"ok": False, "g2": True, "k": k, "n": n}
            if d1_v2(n):
                if pal_kind(n, n - 1, k) != "pair":
                    return {"ok": False, "kind1": True, "k": k, "n": n}
                d1 += 1
                got.add(n)
            if n >= 2 and d2_v2(n):
                if pal_kind(n, n - 2, k) != "pair":
                    return {"ok": False, "kind2": True, "k": k, "n": n}
                d2 += 1
        recon = set()
        a = 1
        while (1 << a) - 1 < cap:
            recon.update(range((1 << a) - 1, cap, 1 << (a + 1)))
            a += 2
        if got != recon:
            return {
                "ok": False,
                "union": True,
                "k": k,
                "n_got": len(got),
                "n_recon": len(recon),
            }
        if d1 != want_d1_n(k) or d2 != want_d2_n(k):
            return {"ok": False, "count": True, "k": k, "d1": d1, "d2": d2}
        if d1 != d1_ap_count(k):
            return {"ok": False, "apc": True, "k": k}
        n_ok += 1
        rows[str(k)] = {"d1": d1, "d2": d2, "n_ap": len(recon)}
    ok = (
        n_ok == K_COUNT + 1
        and rows["0"]["d1"] == 1
        and rows["0"]["d2"] == 2
        and rows["1"]["d1"] == 3
        and rows["7"]["d1"] == 171
        and rows["12"]["d1"] == 5461
        and rows["12"]["d2"] == 5462
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """G(n,n-1)=1 iff n=1 mod 4; d=1 iff n=1 mod 4."""
    ok = (
        d1_v2(7) == 1
        and (7 % 4) == 3
        and d1_v2(15) == 0
        and G_nm1(7) != G_nm1(3)
        and want_d1_r7_n8(2) == 1
        and want_d1_r7_n8(2) != 2
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tk = json.loads(TK_JSON.read_text())
    tj = json.loads(TJ_JSON.read_text())
    tf = json.loads(TF_JSON.read_text())
    ok = (
        tk["checks"]["all_ok"]
        and tj["checks"]["all_ok"]
        and tf["checks"]["all_ok"]
        and tk["verdict"]["G_nm1_closed_form"] == "LEMMA"
        and tk["verdict"]["d2_all_n2_n3_mod8"] == "LEMMA"
        and tf["verdict"]["d1_all_n1_mod4"] == "LEMMA"
        and tk["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tk["verdict"]["prize"] == "unsolved"
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
        "cycle": "TL",
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
            "G_nm1_eq_v2_nplus1": True,
            "d1_iff_v2_odd": True,
            "d2_iff_v2_half_odd": True,
            "d1_eq_odd_a_ap_union": True,
            "G_nm1_iff_n1_mod4": False,
            "d1_iff_n1_mod4": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "G_nm1_eq_v2_nplus1": "LEMMA",
            "d1_iff_v2_odd": "LEMMA",
            "d2_iff_v2_half_odd": "LEMMA",
            "d1_eq_odd_a_ap_union": "LEMMA",
            "G_nm1_iff_n1_mod4": "KILLED",
            "d1_iff_n1_mod4": "KILLED",
            "d1_all_n7_mod8": "KILLED",
            "d2_all_n6_mod8": "KILLED",
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
        "d2",
        dump["residue_count"]["rows"]["12"]["d2"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
