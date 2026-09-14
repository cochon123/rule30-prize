#!/usr/bin/env python3
"""Cycle SS: clip-unpaired packed AND is 0 for all k.

Unpaired covering cells have pal-partner j=2n-j_pal > 5U, so
p-(2s+6)=2(2n-j-5U-1)>=0 with s=10U-2n-2 the even snapshot.
Thus p>=2s+6 and p-3>2s. Packed support at time s is bits 0..2s
(right edge bit 2s=1), so the 4-tuple is 0000, not an AND-one.
Clip-unpaired packed AND vanishes for every k, even and odd n.
Rest tot is pal-center AND xor pal-pair AND-mismatch for all k.
Not rest=S xor T. Do not walk leftover p catalogues. Do not walk
k=11 packed covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_ss.py --certify
Dump: research/cycle_ss.json
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
from cycle_ca import KNOWN20, packed_center_bits
from cycle_hh import AND_ONES, and_from_tuple, bit_at
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_sr import pal_center_count
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
SR_JSON = Path(__file__).resolve().parent / "cycle_sr.json"
GE_JSON = Path(__file__).resolve().parent / "cycle_ge.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_CELL = 8
S_SUP = 128
Q = 10


def even_s(n: int, k: int) -> int:
    """Covering even snapshot s=T-2n-2 on q=10."""
    return Q * (1 << k) - 2 * n - 2


def packed_p(j: int, k: int) -> int:
    return Q * (1 << k) - 2 * j


def unpaired_excess(n: int, j: int, k: int) -> int:
    """p-(2s+6)=2(2n-j-5U-1) on q=10."""
    u = 1 << k
    return 2 * (2 * n - j - 5 * u - 1)


def support_width() -> dict:
    """s<128: packed bits live in 0..2s, bit 2s=1."""
    n_ok = 0
    row = 1
    for s in range(0, S_SUP):
        if row >> (2 * s + 1):
            return {"ok": False, "hi": True, "s": s}
        if bit_at(row, 2 * s) != 1:
            return {"ok": False, "edge": True, "s": s}
        if s >= 1 and bit_at(row, 2 * s - 1) != (s % 2):
            return {"ok": False, "odd": True, "s": s}
        four = tuple(bit_at(row, 2 * s + 6 - 3 + i) for i in range(4))
        if four != (0, 0, 0, 0) or and_from_tuple(*four):
            return {"ok": False, "past": True, "s": s, "four": four}
        n_ok += 1
        row = rule30_step(row)
    ok = n_ok == S_SUP and (0, 0, 0, 0) not in AND_ONES
    return {"ok": ok, "n_ok": n_ok, "s_hi": S_SUP - 1}


def unpaired_bound() -> dict:
    """k<=8 all covering n,j unpaired: p>=2s+6 and the excess identity."""
    n_ok = 0
    rows = {}
    for k in range(0, K_CELL + 1):
        u = 1 << k
        clip = 5 * u
        n_cell = 0
        for n in range(0, 4 * u):
            s = even_s(n, k)
            jmax = 2 * n - clip - 1
            if jmax < 0:
                continue
            jhi = min(2 * n, clip, jmax)
            for j in range(0, jhi + 1):
                p = packed_p(j, k)
                ex = unpaired_excess(n, j, k)
                if p - (2 * s + 6) != ex or ex < 0 or p < 2 * s + 6:
                    return {
                        "ok": False,
                        "k": k,
                        "n": n,
                        "j": j,
                        "p": p,
                        "s": s,
                        "ex": ex,
                    }
                if p - 3 <= 2 * s:
                    return {"ok": False, "tuple": True, "k": k, "n": n, "j": j}
                n_cell += 1
                n_ok += 1
        rows[str(k)] = {"n_cell": n_cell, "n_pal": pal_center_count(k)}
    ok = (
        n_ok > 0
        and rows["0"]["n_cell"] == 1
        and rows["1"]["n_cell"] == 6
        and rows["8"]["n_pal"] == 512
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CELL, "rows": rows}


def tot_form() -> dict:
    """k<=64: excess identity on window corners; pal-center count even."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        u = 1 << k
        clip = 5 * u
        if pal_center_count(k) != 2 * u or pal_center_count(k) % 2 != 0:
            return {"ok": False, "pal": True, "k": k}
        if 4 * u - 2 > 5 * u:
            return {"ok": False, "clip": True, "k": k}
        sample_n = {0, 1, u, 3 * u, 4 * u - 2, 4 * u - 1}
        for n in sample_n:
            if n < 0 or n >= 4 * u:
                continue
            s = even_s(n, k)
            if s != Q * u - 2 * n - 2:
                return {"ok": False, "s": True, "k": k, "n": n}
            jmax = 2 * n - clip - 1
            if jmax < 0:
                continue
            for j in (0, jmax):
                if j > min(2 * n, clip):
                    continue
                p = packed_p(j, k)
                ex = unpaired_excess(n, j, k)
                if p - (2 * s + 6) != ex or ex < 0:
                    return {"ok": False, "ex": True, "k": k, "n": n, "j": j}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and unpaired_excess(7, 0, 1) >= 0
        and even_s(0, 0) == 8
        and want_even(0) == 1
        and want_odd(0) == 1
        and (0, 0, 0, 0) not in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def killed_eq() -> dict:
    """0000 is AND-one; pal-center tot equals ST; unpaired empty at k=1."""
    ok = (
        and_from_tuple(0, 0, 0, 0) == 0
        and want_even(0) != want_rest_e0(0)
        and want_even(6) != want_rest_e0(6)
        and want_odd(0) != want_rest_e0(0)
        and want_rest_e0(2) == 1
        and pal_center_count(1) == 4
    )
    return {"ok": ok}


def prefixes() -> dict:
    sr = json.loads(SR_JSON.read_text())
    ge = json.loads(GE_JSON.read_text())
    ok = (
        sr["checks"]["all_ok"]
        and ge["checks"]["all_ok"]
        and sr["verdict"]["unpaired_packed_and_0_k_le_10"] == "CERTIFIED"
        and sr["verdict"]["rest_eq_pal_c_xor_pair_mis_k_le_10"] == "CERTIFIED"
        and sr["verdict"]["unpaired_packed_and_0_all_k"] == "PREFIX"
        and sr["verdict"]["g1_eq_unpaired"] == "LEMMA"
        and sr["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and sr["verdict"]["prize"] == "unsolved"
        and want_even(7) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, sup, bound, tot, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert sup["ok"] and bound["ok"] and tot["ok"] and kl["ok"]
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
    sup = support_width()
    bound = unpaired_bound()
    tot = tot_form()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, sup, bound, tot, kl, sc, pref)
    dump = {
        "cycle": "SS",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "support_width": {k: sup[k] for k in sup if k != "ok"},
        "unpaired_bound": {k: bound[k] for k in bound if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "packed_support_0_to_2s": True,
            "unpaired_p_past_2s": True,
            "unpaired_packed_and_0_all_k": True,
            "rest_eq_pal_c_xor_pair_mis_all_k": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "packed_support_0_to_2s": "LEMMA",
            "unpaired_p_past_2s": "LEMMA",
            "unpaired_packed_and_0_all_k": "LEMMA",
            "rest_eq_pal_c_xor_pair_mis_all_k": "LEMMA",
            "pal_c_eq_ST": "KILLED",
            "even_eq_ST": "KILLED",
            "tuple_0000_is_and": "KILLED",
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
        "support n_ok",
        dump["support_width"]["n_ok"],
        "bound n_ok",
        dump["unpaired_bound"]["n_ok"],
        "k0 cells",
        dump["unpaired_bound"]["rows"]["0"]["n_cell"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
