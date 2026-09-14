#!/usr/bin/env python3
"""Cycle TO: valuation classes 2-fold; odd child a maps to a+1.

At k>=1, odd children of covering n with v2(n+1)=a have v2=a+1
and covering times 2t-1, filling the child a+1 time AP. Even
children have v2(n/2+1)=a and are even d=2 iff a is odd, with
times 2t+1 filling the even-d=2 b=a AP. Not rest=S xor T. Do
not walk leftover p catalogues. Do not walk leftover d
catalogues. Do not walk k=11 packed covering. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_to.py --certify
Dump: research/cycle_to.json
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
from cycle_sz import even_child_t, odd_child_t
from cycle_td import want_d1_n
from cycle_te import want_d2_n
from cycle_tl import d1_val_count, d1_v2, d2_v2
from cycle_tm import (
    d1_time_hi,
    d1_time_lo,
    d1_time_step,
    d2_even_val_count,
)
from cycle_tn import (
    even_d2_time_ap_ok,
    even_d2_time_hi,
    even_d2_time_lo,
    even_d2_time_step,
    val_time_ap_ok,
)

OUT = Path(__file__).resolve().with_suffix(".json")
TN_JSON = Path(__file__).resolve().parent / "cycle_tn.json"
TM_JSON = Path(__file__).resolve().parent / "cycle_tm.json"
TL_JSON = Path(__file__).resolve().parent / "cycle_tl.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def tot_form() -> dict:
    """k=1..64: odd child a->a+1 endpoints; even child even-d=2 iff a odd."""
    n_ok = 0
    if v2(1 + 1) != 1 or v2(2 * 1 + 1 + 1) != 2:
        return {"ok": False, "base": True}
    if odd_child_t(1, 1) != 2 * covering_t(0, 1) - 1:
        return {"ok": False, "t0": True}
    for k in range(1, K_ALG + 1):
        cap_p = 1 << (k + 1)
        a = 1
        while (1 << a) - 1 < cap_p:
            if not val_time_ap_ok(k - 1, a):
                return {"ok": False, "p": True, "k": k, "a": a}
            if not val_time_ap_ok(k, a + 1):
                return {"ok": False, "c": True, "k": k, "a": a}
            if d1_val_count(k - 1, a) != d1_val_count(k, a + 1):
                return {"ok": False, "cnt": True, "k": k, "a": a}
            plo = d1_time_lo(k - 1, a)
            phi = d1_time_hi(k - 1, a)
            pst = d1_time_step(a)
            if 2 * phi - 1 != d1_time_hi(k, a + 1):
                return {"ok": False, "ohi": True, "k": k, "a": a}
            if 2 * plo - 1 != d1_time_lo(k, a + 1):
                return {"ok": False, "olo": True, "k": k, "a": a}
            if 2 * pst != d1_time_step(a + 1):
                return {"ok": False, "ost": True, "k": k, "a": a}
            if a % 2:
                if d1_val_count(k - 1, a) != d2_even_val_count(k, a):
                    return {"ok": False, "ecnt": True, "k": k, "a": a}
                if not even_d2_time_ap_ok(k, a):
                    return {"ok": False, "eap": True, "k": k, "a": a}
                if 2 * phi + 1 != even_d2_time_hi(k, a):
                    return {"ok": False, "ehi": True, "k": k, "a": a}
                if 2 * plo + 1 != even_d2_time_lo(k, a):
                    return {"ok": False, "elo": True, "k": k, "a": a}
                if 2 * pst != even_d2_time_step(a):
                    return {"ok": False, "est": True, "k": k, "a": a}
            n_lo = (1 << a) - 1
            if n_lo < cap_p:
                if v2(2 * n_lo + 1 + 1) != a + 1:
                    return {"ok": False, "ov": True, "k": k, "a": a}
                if odd_child_t(n_lo, k) != 2 * covering_t(k - 1, n_lo) - 1:
                    return {"ok": False, "ot": True, "k": k, "a": a}
                if even_child_t(n_lo, k) != 2 * covering_t(k - 1, n_lo) + 1:
                    return {"ok": False, "et": True, "k": k, "a": a}
                if d2_v2(2 * n_lo) != (a % 2):
                    return {"ok": False, "ed2": True, "k": k, "a": a}
            a += 1
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG
        and val_time_ap_ok(64, 1)
        and even_d2_time_ap_ok(64, 1)
        and d1_val_count(6, 1) == d1_val_count(7, 2)
        and d1_v2(1) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def residue_count() -> dict:
    """k<=12: odd-child times fill child a+1 AP; even children fill even d=2."""
    n_ok = 0
    rows = {}
    for k in range(1, K_COUNT + 1):
        cap_p = 1 << (k + 1)
        rec = {}
        a = 1
        while (1 << a) - 1 < cap_p:
            parents = [n for n in range(cap_p) if v2(n + 1) == a]
            got_o = sorted(odd_child_t(n, k) for n in parents)
            want_o = list(
                range(
                    d1_time_lo(k, a + 1),
                    d1_time_hi(k, a + 1) + 1,
                    d1_time_step(a + 1),
                )
            )
            if got_o != want_o:
                return {"ok": False, "odd": True, "k": k, "a": a}
            if any(v2(2 * n + 1 + 1) != a + 1 for n in parents):
                return {"ok": False, "oval": True, "k": k, "a": a}
            got_e = sorted(even_child_t(n, k) for n in parents)
            if a % 2:
                want_e = list(
                    range(
                        even_d2_time_lo(k, a),
                        even_d2_time_hi(k, a) + 1,
                        even_d2_time_step(a),
                    )
                )
                if got_e != want_e:
                    return {"ok": False, "even": True, "k": k, "a": a}
                if any(not d2_v2(2 * n) for n in parents):
                    return {"ok": False, "ed2": True, "k": k, "a": a}
            else:
                if any(d2_v2(2 * n) for n in parents):
                    return {"ok": False, "ned2": True, "k": k, "a": a}
            rec[str(a)] = {"n": len(parents), "odd": len(got_o)}
            a += 1
        n_ok += 1
        rows[str(k)] = rec
    ok = (
        n_ok == K_COUNT
        and rows["1"]["1"]["n"] == 1
        and rows["7"]["1"]["n"] == 64
        and rows["12"]["1"]["n"] == 2048
        and rows["12"]["2"]["n"] == 1024
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """cellwise spat 2-fold; even children of d=1 stay d=1."""
    ok = (
        d2_v2(2) == 1
        and d1_v2(1) == 1
        and d1_v2(2) == 0
        and even_child_t(1, 2) == covering_t(2, 2)
        and d2_v2(2 * 1) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tn = json.loads(TN_JSON.read_text())
    tm = json.loads(TM_JSON.read_text())
    tl = json.loads(TL_JSON.read_text())
    ok = (
        tn["checks"]["all_ok"]
        and tm["checks"]["all_ok"]
        and tl["checks"]["all_ok"]
        and tn["verdict"]["val_times_eq_ap_all_a"] == "LEMMA"
        and tn["verdict"]["even_d2_times_eq_odd_b_aps"] == "LEMMA"
        and tm["verdict"]["d1_times_eq_odd_a_ap_union"] == "LEMMA"
        and tn["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tn["verdict"]["prize"] == "unsolved"
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
        "cycle": "TO",
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
            "odd_child_val_a_to_a1": True,
            "odd_child_times_fill_child_ap": True,
            "even_child_d2_iff_a_odd": True,
            "even_child_times_fill_even_d2_ap": True,
            "even_child_stays_d1": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_child_val_a_to_a1": "LEMMA",
            "odd_child_times_fill_child_ap": "LEMMA",
            "even_child_d2_iff_a_odd": "LEMMA",
            "even_child_times_fill_even_d2_ap": "LEMMA",
            "even_child_stays_d1": "KILLED",
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
        "a1 k12",
        dump["residue_count"]["rows"]["12"]["1"]["n"],
        "a2",
        dump["residue_count"]["rows"]["12"]["2"]["n"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
