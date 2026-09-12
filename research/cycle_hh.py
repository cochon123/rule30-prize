#!/usr/bin/env python3
"""Cycle HH: covering s=T-2n-1; packed AND steps on four bit tuples.

On every covering remainder window of length 2UQ, odd s=T-2n-1 and
even s=T-2n-2, so odd-s AND(n,j) is packed AND at (T-2n-1, T-2j).
The AND step is 1 iff the previous 4-tuple of row bits is in
{0010,0011,0100,1001}. Not s=t0+2n+1; not AND=G(n,j); not independent
of T. Do not claim J6=J10=0 implies J18=1 for all k; do not push
even-spine past k=18; do not bump all n0=16 past 414990. Not a prize
claim.

Run: python3 research/cycle_hh.py --certify
Dump: research/cycle_hh.json
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
from cycle_gu import odd_clock
from cycle_hc import WINDOWS
from cycle_hf import J6_WINDOW
from cycle_hg import J10_WINDOW, J18_WINDOW, covering_Q
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
HG_JSON = Path(__file__).resolve().parent / "cycle_hg.json"
HF_JSON = Path(__file__).resolve().parent / "cycle_hf.json"

ALL_WINDOWS = WINDOWS + (J6_WINDOW, J10_WINDOW, J18_WINDOW)
AND_ONES = ((0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 0, 0), (1, 0, 0, 1))


def and_from_tuple(z: int, a: int, b: int, c: int) -> int:
    """Packed AND after one Rule 30 step, from row bits p-3..p."""
    return int((z, a, b, c) in AND_ONES)


def bit_at(row: int, i: int) -> int:
    if i < 0:
        return 0
    return (row >> i) & 1


def s_clock() -> dict:
    """odd s=T-2n-1, even s=T-2n-2 on all covering windows. k<=12."""
    n_ok = 0
    for k in range(0, 13):
        U = 1 << k
        for _name, Tmul, t0mul, Q in ALL_WINDOWS:
            T, t0 = Tmul * U, t0mul * U
            UQ = U * Q
            if T - t0 != 2 * UQ:
                return {"ok": False, "len": True, "k": k, "Q": Q}
            for t in range(UQ):
                n = odd_clock(t, U, Q)
                if t0 + 2 * t + 1 != T - 2 * n - 1:
                    return {"ok": False, "odd": True, "k": k, "t": t, "n": n}
                if t0 + 2 * t != T - 2 * n - 2:
                    return {"ok": False, "even": True, "k": k, "t": t, "n": n}
            n_ok += 1
    return {"ok": n_ok == 13 * 6, "n_ok": n_ok}


def and_truth() -> dict:
    """16-row table: A'=(a^(b|c))&(z^(a|b)) iff 4-tuple in AND_ONES."""
    n_ok = 0
    for z in (0, 1):
        for a in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    want = (a ^ (b | c)) & (z ^ (a | b))
                    got = and_from_tuple(z, a, b, c)
                    if want != got:
                        return {
                            "ok": False,
                            "z": z,
                            "a": a,
                            "b": b,
                            "c": c,
                            "want": want,
                            "got": got,
                        }
                    n_ok += 1
    ones = [
        (z, a, b, c)
        for z in (0, 1)
        for a in (0, 1)
        for b in (0, 1)
        for c in (0, 1)
        if and_from_tuple(z, a, b, c)
    ]
    if tuple(ones) != AND_ONES:
        return {"ok": False, "ones": ones}
    return {"ok": n_ok == 16, "n_ok": n_ok, "n_ones": len(ones)}


def packed_and_step() -> dict:
    """AND_p(s+1) matches the 4-tuple rule. t<64, p<=2s+4."""
    n_ok = 0
    row = 1
    for s in range(0, 64):
        nxt = rule30_step(row)
        A = (nxt << 1) & nxt
        for p in range(0, 2 * (s + 1) + 4):
            z, a, b, c = bit_at(row, p - 3), bit_at(row, p - 2), bit_at(row, p - 1), bit_at(
                row, p
            )
            if and_from_tuple(z, a, b, c) != ((A >> p) & 1):
                return {"ok": False, "s": s, "p": p}
            n_ok += 1
        row = nxt
    return {"ok": n_ok > 0, "n_ok": n_ok}


def killed_forward_clock() -> dict:
    """s is not t0+2n+1: k=2, J6, first odd s."""
    k = 2
    U = 1 << k
    T, t0, Q = 6 * U, 2 * U, 2
    n = odd_clock(0, U, Q)
    s_odd = t0 + 1
    forward = t0 + 2 * n + 1
    want = T - 2 * n - 1
    ok = s_odd == want == 9 and forward == 23 and n == 7
    return {"ok": ok, "k": k, "n": n, "s_odd": s_odd, "forward": forward, "want": want}


def killed_and_eq_G() -> dict:
    """Odd-s AND(n,j) is not G(n,j): k=1, q=6, n=3, j=0."""
    k = 1
    U = 1 << k
    T, t0, Q = 6 * U, 2 * U, covering_Q(6)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    s = t0
    found = None
    while s < T:
        if s % 2:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            if n == 3:
                A = (row << 1) & row
                p = T - 2 * 0
                found = (A >> p) & 1
                break
        row = rule30_step(row)
        s += 1
    g = G(3, 0)
    ok = found == 0 and g == 1
    return {"ok": ok, "k": 1, "n": 3, "j": 0, "AND": found, "G": g}


def killed_and_indep_T() -> dict:
    """AND(n,j) still depends on T: k=0, n=0, j=0, J6 vs J10."""
    vals = {}
    for name, Tmul, t0mul, Q in (("j6", 6, 2, 2), ("j10", 10, 2, 4)):
        T, t0 = Tmul * 1, t0mul * 1
        row = 1
        for _ in range(t0):
            row = rule30_step(row)
        s = t0
        found = None
        while s < T:
            if s % 2:
                t = (s - t0) // 2
                n = odd_clock(t, 1, Q)
                if n == 0:
                    A = (row << 1) & row
                    p = T - 2 * 0
                    found = (A >> p) & 1
                    break
            row = rule30_step(row)
            s += 1
        vals[name] = found
    ok = vals["j6"] == 1 and vals["j10"] == 0
    return {"ok": ok, "k": 0, "n": 0, "j": 0, **vals}


def prefixes() -> dict:
    hg = json.loads(HG_JSON.read_text())
    hf = json.loads(HF_JSON.read_text())
    ok = (
        hg["checks"]["all_ok"]
        and hf["checks"]["all_ok"]
        and hg["verdict"]["J10_eq_in_support_j_index_Q4"] == "LEMMA"
        and hg["verdict"]["J18_eq_in_support_j_index_Q8"] == "LEMMA"
        and hf["verdict"]["J6_eq_in_support_j_index_Q2"] == "LEMMA"
        and hg["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, sc: dict, at: dict, pk: dict, kf: dict, kg: dict, kt: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        sc["ok"]
        and at["ok"]
        and pk["ok"]
        and kf["ok"]
        and kg["ok"]
        and kt["ok"]
        and pref["ok"]
    )
    assert covering_Q(6) == 2
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    sc = s_clock()
    at = and_truth()
    pk = packed_and_step()
    kf = killed_forward_clock()
    kg = killed_and_eq_G()
    kt = killed_and_indep_T()
    pref = prefixes()
    checks = self_checks(c20, sc, at, pk, kf, kg, kt, pref)
    dump = {
        "cycle": "HH",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "s_clock": {k: sc[k] for k in sc if k != "ok"},
        "and_truth": {k: at[k] for k in at if k != "ok"},
        "packed_and_step": {k: pk[k] for k in pk if k != "ok"},
        "killed_forward_clock": {k: kf[k] for k in kf if k != "ok"},
        "killed_and_eq_G": {k: kg[k] for k in kg if k != "ok"},
        "killed_and_indep_T": {k: kt[k] for k in kt if k != "ok"},
        "lemmas": {
            "odd_s_eq_T_minus_2n_minus_1": True,
            "even_s_eq_T_minus_2n_minus_2": True,
            "AND_step_eq_4tuple_ones": True,
            "s_eq_t0_plus_2n_plus_1": False,
            "AND_n_j_eq_G_n_j": False,
            "AND_n_j_independent_of_T": False,
            "J6_J10_0_implies_J18_1_all_k": None,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "odd_s_eq_T_minus_2n_minus_1": "LEMMA",
            "even_s_eq_T_minus_2n_minus_2": "LEMMA",
            "AND_step_eq_4tuple_ones": "LEMMA",
            "s_eq_t0_plus_2n_plus_1": "KILLED",
            "AND_n_j_eq_G_n_j": "KILLED",
            "AND_n_j_independent_of_T": "KILLED",
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
    print("s_clock n_ok", dump["s_clock"]["n_ok"])
    print("and_truth n_ok", dump["and_truth"]["n_ok"], "n_ones", dump["and_truth"]["n_ones"])
    print("packed_and_step n_ok", dump["packed_and_step"]["n_ok"])
    print("killed_forward_clock", dump["killed_forward_clock"])
    print("killed_and_eq_G", dump["killed_and_eq_G"])
    print("killed_and_indep_T", dump["killed_and_indep_T"])


if __name__ == "__main__":
    main()
