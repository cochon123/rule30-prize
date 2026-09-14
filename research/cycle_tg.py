#!/usr/bin/env python3
"""Cycle TG: d=2 pal-pairs are both children of parent d=1.

At k>=1, every d=1 pal-pair N at k-1 has even child n=2N (j=2N-2)
and odd child n=2N+1 (j=2N-1), both d=2 pal-pairs at k. Conversely
every d=2 pal-pair at k is one of those children. Covering times
are Cycle SZ's 2-fold. Parent d=1 is never clip-edge, so the odd
child stays a pair. Count 2 J_{k+1} is twice the parent d=1 count
J_{k+1}. Not rest=S xor T. Do not walk leftover p catalogues. Do
not walk leftover d catalogues. Do not walk k=11 packed covering.
Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_tg.py --certify
Dump: research/cycle_tg.json
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
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sv import pal_left_never_forced
from cycle_sx import covering_t
from cycle_sy import odd_forced_corr
from cycle_sz import even_child_t, odd_child_t
from cycle_ta import pal_kind
from cycle_tb import want_edge_n
from cycle_tc import clip_j
from cycle_td import want_d1_n
from cycle_te import want_d2_n, want_d2_parity_n
from cycle_tf import want_d1_r1_n, want_d2_r2_n, want_d2_r3_n

OUT = Path(__file__).resolve().with_suffix(".json")
TF_JSON = Path(__file__).resolve().parent / "cycle_tf.json"
TE_JSON = Path(__file__).resolve().parent / "cycle_te.json"
TD_JSON = Path(__file__).resolve().parent / "cycle_td.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_COUNT = 12
PAT0011 = (0, 0, 1, 1)


def d1_children(n: int) -> tuple[int, int]:
    """Even and odd children of a d=1 pal-pair: both have d=2."""
    return 2 * n, 2 * n + 1


def tot_form() -> dict:
    """k<=64: child d=2; times 2-fold; parent d=1 never clip-edge."""
    n_ok = 0
    if want_d2_n(1) != 2 * want_d1_n(0):
        return {"ok": False, "base": True}
    for k in range(0, K_ALG + 1):
        if k >= 1 and want_d2_n(k) != 2 * want_d1_n(k - 1):
            return {"ok": False, "twice": True, "k": k}
        if k >= 1 and want_d2_parity_n(k) != want_d1_n(k - 1):
            return {"ok": False, "par": True, "k": k}
        if k >= 1 and want_d2_r2_n(k) != want_d1_n(k - 1):
            return {"ok": False, "r2": True, "k": k}
        if k >= 1 and want_d2_r3_n(k) != want_d1_n(k - 1):
            return {"ok": False, "r3": True, "k": k}
        u = 1 << k
        clip = 5 * u
        if k >= 1:
            up = 1 << (k - 1)
            clip_p = 5 * up
            samples = {1, 5, up + 1, 3 * up - 3, 4 * up - 3}
            for n in samples:
                if n < 0 or n >= 4 * up or n % 2 == 0:
                    continue
                if G(n, n - 1) != 1:
                    continue
                if n + 1 == clip_p:
                    return {"ok": False, "edge": True, "k": k, "n": n}
                ev, od = d1_children(n)
                if ev >= 4 * u or od >= 4 * u:
                    return {"ok": False, "range": True, "k": k, "n": n}
                if ev - (2 * n - 2) != 2 or od - (2 * n - 1) != 2:
                    return {"ok": False, "d": True, "k": k, "n": n}
                if G(ev, ev - 2) != 1 or G(od, od - 2) != 1:
                    return {"ok": False, "g": True, "k": k, "n": n}
                if pal_kind(ev, ev - 2, k) != "pair":
                    return {"ok": False, "ke": True, "k": k, "n": n}
                if pal_kind(od, od - 2, k) != "pair":
                    return {"ok": False, "ko": True, "k": k, "n": n}
                if even_child_t(n, k) != covering_t(k, ev):
                    return {"ok": False, "te": True, "k": k, "n": n}
                if odd_child_t(n, k) != covering_t(k, od):
                    return {"ok": False, "to": True, "k": k, "n": n}
                if ev % 4 != 2 or od % 4 != 3:
                    return {"ok": False, "mod": True, "k": k, "n": n}
        if 0 <= clip - 1 < 4 * u:
            return {"ok": False, "d1edge": True, "k": k}
        if k >= 3 and (
            not pal_left_never_forced(k) or odd_forced_corr(k) != 0
        ):
            return {"ok": False, "corr": True, "k": k}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and d1_children(1) == (2, 3)
        and want_d2_n(7) == 2 * want_d1_n(6)
        and want_d1_n(6) == 85
        and want_d1_r1_n(0) == 1
        and want_edge_n(0) == 1
        and G(1, 0) == 1
        and want_even(0) == 1
        and PAT0011 in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def fold_count() -> dict:
    """k<=12: d=2 cells == {2N, 2N+1 : N d=1 at k-1}."""
    n_ok = 0
    rows = {}
    parent = []
    u0 = 1
    for n in range(1, 4 * u0):
        if G(n, n - 1) == 1 and pal_kind(n, n - 1, 0) == "pair":
            parent.append(n)
    if parent != [1]:
        return {"ok": False, "k0": True, "parent": parent}
    for k in range(1, K_COUNT + 1):
        u = 1 << k
        child = []
        for n in range(2, 4 * u):
            if G(n, n - 2) == 1 and pal_kind(n, n - 2, k) == "pair":
                child.append(n)
        want = []
        for n in parent:
            ev, od = d1_children(n)
            if pal_kind(ev, ev - 2, k) != "pair" or pal_kind(od, od - 2, k) != "pair":
                return {"ok": False, "kind": True, "k": k, "n": n}
            if even_child_t(n, k) != covering_t(k, ev):
                return {"ok": False, "te": True, "k": k, "n": n}
            if odd_child_t(n, k) != covering_t(k, od):
                return {"ok": False, "to": True, "k": k, "n": n}
            want.extend((ev, od))
        if sorted(child) != sorted(want):
            return {
                "ok": False,
                "set": True,
                "k": k,
                "n_child": len(child),
                "n_want": len(want),
            }
        if len(child) != want_d2_n(k) or len(parent) != want_d1_n(k - 1):
            return {"ok": False, "count": True, "k": k}
        n_ok += 1
        rows[str(k)] = {
            "n_parent": len(parent),
            "n_child": len(child),
        }
        nxt = []
        for n in range(1, 4 * u):
            if G(n, n - 1) == 1 and pal_kind(n, n - 1, k) == "pair":
                nxt.append(n)
        parent = nxt
    ok = (
        n_ok == K_COUNT
        and rows["1"]["n_child"] == 2
        and rows["7"]["n_child"] == 170
        and rows["12"]["n_child"] == 5462
        and rows["12"]["n_parent"] == 2731
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_COUNT, "rows": rows}


def killed_eq() -> dict:
    """cellwise spat 2-fold; d=2 AND identically 0; d=1 is clip-edge."""
    ok = (
        want_d2_n(1) == 2 * want_d1_n(0)
        and d1_children(1) == (2, 3)
        and want_d1_n(0) == 1
        and want_edge_n(0) == 1
        and clip_j(1, 0) != 0
        and G(2, 0) == 1
        and PAT0011 in AND_ONES
        and odd_forced_corr(2) != 0
        and want_rest_e0(1) == 0
        and pal_left_never_forced(3)
        and and_clause(0, 0, 0, 1) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    tf = json.loads(TF_JSON.read_text())
    te = json.loads(TE_JSON.read_text())
    td = json.loads(TD_JSON.read_text())
    ok = (
        tf["checks"]["all_ok"]
        and te["checks"]["all_ok"]
        and td["checks"]["all_ok"]
        and tf["verdict"]["d1_all_n1_mod4"] == "LEMMA"
        and te["verdict"]["d2_count_eq_2_jacobsthal"] == "LEMMA"
        and td["verdict"]["d1_count_eq_jacobsthal"] == "LEMMA"
        and tf["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and tf["verdict"]["prize"] == "unsolved"
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
    cnt = fold_count()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, cnt, kl, sc, pref)
    dump = {
        "cycle": "TG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "fold_count": {k: cnt[k] for k in cnt if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "d2_eq_both_children_of_d1": True,
            "d2_count_eq_2_parent_d1": True,
            "parent_d1_never_clip_edge": True,
            "d2_spat_eq_parent_d1_spat": False,
            "d2_and_identically_0": False,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "d2_eq_both_children_of_d1": "LEMMA",
            "d2_count_eq_2_parent_d1": "LEMMA",
            "parent_d1_never_clip_edge": "LEMMA",
            "d2_child_times_2fold": "LEMMA",
            "d2_spat_eq_parent_d1_spat": "KILLED",
            "d2_and_identically_0": "KILLED",
            "d1_all_odd_n": "KILLED",
            "d2_all_even_n": "KILLED",
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
        "d2 k12",
        dump["fold_count"]["rows"]["12"]["n_child"],
        "parent",
        dump["fold_count"]["rows"]["12"]["n_parent"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
