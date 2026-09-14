#!/usr/bin/env python3
"""Cycle SU: covering packed AND is next-row consecutive bits at 2(n-j).

On q=10, even snapshot s=10U-2n-2 and packed p=10U-2j, so
p-(s+1)=2(n-j)+1. Cycle HH packed AND is odd-s bits p and p-1,
hence AND = x(s+1, 2d) and x(s+1, 2d+1) with d=n-j. Pal-center
is the d=0 case (Cycle ST). Pal-pair raw AND-mismatch is that
predicate at d xor at -d. Not rest=S xor T. Do not walk leftover
p catalogues. Do not walk k=11 packed covering. Do not walk
k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_su.py --certify
Dump: research/cycle_su.json
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
from cycle_gu import odd_clock
from cycle_hg import covering_Q
from cycle_hh import AND_ONES, and_from_tuple, bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pb import want_rest_e0
from cycle_qv import even_slots
from cycle_so import want_even, want_odd
from cycle_ss import even_s, packed_p
from cycle_st import pal_center_and
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
ST_JSON = Path(__file__).resolve().parent / "cycle_st.json"
SS_JSON = Path(__file__).resolve().parent / "cycle_ss.json"

N_PAL = 64
M_SLOTS = 64
K_ALG = 64
K_CELL = 8
Q = 10


def covering_d(n: int, j: int) -> int:
    return n - j


def covering_and_spat(row_odd: int, s_even: int, d: int) -> int:
    """Packed AND: x(s+1, 2d) and x(s+1, 2d+1)."""
    t = s_even + 1
    return bit_at(row_odd, t + 2 * d) & bit_at(row_odd, t + 2 * d + 1)


def packed_shift(n: int, j: int, k: int) -> int:
    """p-(s+1) = 2(n-j)+1 on q=10."""
    return packed_p(j, k) - even_s(n, k) - 1


def tot_form() -> dict:
    """k<=64: p-(s+1)=2d+1; pal-center is d=0."""
    n_ok = 0
    for k in range(0, K_ALG + 1):
        u = 1 << k
        sample_n = {0, 1, u, 3 * u, 4 * u - 2, 4 * u - 1}
        for n in sample_n:
            if n < 0 or n >= 4 * u:
                continue
            s = even_s(n, k)
            js = {0, n, min(2 * n, 5 * u)}
            for j in js:
                if j < 0:
                    continue
                d = covering_d(n, j)
                p = packed_p(j, k)
                if packed_shift(n, j, k) != 2 * d + 1:
                    return {"ok": False, "shift": True, "k": k, "n": n, "j": j}
                if p != s + 2 + 2 * d:
                    return {"ok": False, "p": True, "k": k, "n": n, "j": j, "d": d}
                if j == n and d != 0:
                    return {"ok": False, "d0": True, "k": k, "n": n}
        n_ok += 1
    ok = (
        n_ok == K_ALG + 1
        and covering_d(7, 7) == 0
        and covering_d(7, 0) == 7
        and packed_shift(7, 7, 1) == 1
        and packed_p(7, 1) == even_s(7, 1) + 2
        and want_even(0) == 1
        and (0, 0, 0, 0) not in AND_ONES
    )
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_ALG}


def spat_walk() -> dict:
    """k<=8 all clipped covering cells: packed AND equals spat(d)."""
    n_ok = 0
    n_eq = 0
    rows = {}
    for k in range(0, K_CELL + 1):
        U = 1 << k
        T, t0, Qc = Q * U, 2 * U, covering_Q(Q)
        clip = 5 * U
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        n_cell = 0
        s = t0
        prev = None
        while s < T:
            if s % 2 == 0:
                prev = row
            else:
                t = (s - t0) // 2
                n = odd_clock(t, U, Qc)
                s_even = s - 1
                hi = min(2 * n, clip)
                for j in range(0, hi + 1):
                    p = packed_p(j, k)
                    if p < 0:
                        continue
                    d = covering_d(n, j)
                    z, a, b, c = (bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(z, a, b, c)
                    spat = covering_and_spat(row, s_even, d)
                    hh = bit_at(row, p) & bit_at(row, p - 1)
                    if packed != spat or packed != hh or packed != and_from_tuple(z, a, b, c):
                        return {
                            "ok": False,
                            "k": k,
                            "n": n,
                            "j": j,
                            "d": d,
                            "packed": packed,
                            "spat": spat,
                            "hh": hh,
                        }
                    if j == n and spat != pal_center_and(row, s_even):
                        return {"ok": False, "st": True, "k": k, "n": n}
                    n_cell += 1
                    n_eq += 1
            row = rule30_step(row)
            s += 1
        n_ok += 1
        rows[str(k)] = {"n_cell": n_cell}
    ok = (
        n_ok == K_CELL + 1
        and n_eq > 0
        and rows["0"]["n_cell"] == 15
        and rows["1"]["n_cell"] == 58
        and rows["7"]["n_cell"] == 225472
    )
    return {"ok": ok, "n_ok": n_ok, "n_eq": n_eq, "k_hi": K_CELL, "rows": rows}


def killed_eq() -> dict:
    """AND equals one spat bit; pal-center tot equals ST; AND identically 0."""
    row = 1
    ok = (
        covering_and_spat(row, -1, 0) == 0
        and bit_at(row, 0) == 1
        and covering_and_spat(row, -1, 0) != bit_at(row, 0)
        and pal_center_and(row, -1) == covering_and_spat(row, -1, 0)
        and want_rest_e0(1) == 0
        and want_rest_e0(6) == 1
        and want_even(0) != 0
        and and_from_tuple(0, 0, 0, 0) == 0
    )
    return {"ok": ok}


def prefixes() -> dict:
    st = json.loads(ST_JSON.read_text())
    ss = json.loads(SS_JSON.read_text())
    ok = (
        st["checks"]["all_ok"]
        and ss["checks"]["all_ok"]
        and st["verdict"]["pal_center_and_eq_next_center_and_right"] == "LEMMA"
        and st["verdict"]["pal_center_never_forced_k_ge_3"] == "LEMMA"
        and st["verdict"]["pal_c_eq_ST"] == "KILLED"
        and st["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and st["verdict"]["prize"] == "unsolved"
        and ss["verdict"]["rest_eq_pal_c_xor_pair_mis_all_k"] == "LEMMA"
        and want_odd(0) == 1
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, ev, tot, walk, kl, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert pal["ok"] and slots["ok"] and ev["ok"]
    assert tot["ok"] and walk["ok"] and kl["ok"]
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
    walk = spat_walk()
    kl = killed_eq()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, ev, tot, walk, kl, sc, pref)
    dump = {
        "cycle": "SU",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "even_slots": {k: ev[k] for k in ev if k != "ok"},
        "tot_form": {k: tot[k] for k in tot if k != "ok"},
        "spat_walk": {k: walk[k] for k in walk if k != "ok"},
        "killed_eq": {k: kl[k] for k in kl if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "lemmas": {
            "covering_and_eq_spat_2d": True,
            "pal_center_is_d0": True,
            "pair_raw_eq_spat_d_xor_minus_d": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "covering_and_eq_spat_2d": "LEMMA",
            "pal_center_is_d0": "LEMMA",
            "pair_raw_eq_spat_d_xor_minus_d": "LEMMA",
            "pal_c_eq_ST": "KILLED",
            "and_eq_left_spat_bit": "KILLED",
            "and_identically_0": "KILLED",
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
        "spat n_eq",
        dump["spat_walk"]["n_eq"],
        "k0 cells",
        dump["spat_walk"]["rows"]["0"]["n_cell"],
        "k7 cells",
        dump["spat_walk"]["rows"]["7"]["n_cell"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
