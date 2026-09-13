#!/usr/bin/env python3
"""Cycle PE: right-edge bits e0..e5; pal-duals of p=4 and p=6.

Packed bit e_i(t) is the bit at position 2t-i. Then e0=1,
e1=e2=t%2, e3=(t>>1)&1, e4=1 iff t%8 in (2, 4, 5, 7), and
e5=1 iff t%8 in (3, 5, 7). On even t the 4-tuple at p=2t is
1001 iff t%4==2, and the 4-tuple at p=2t-2 is an AND-one iff
t%8 in (4, 6). Covering pal-dual packed columns sum to 2s+4,
so p=4 duals with the right edge. The unique covering cells
(3U-2, U-2) and (3U-3, U-3) are those duals and have packed
AND=1 for k>=1 and k>=2; they cancel in rest xor for k>=2.
Even-n rest is not 1 iff k%8 in (0, 1, 2, 7) (dies at k=9).
Not rest=S xor T. Not E_k=0 for all k. Do not walk k=11 packed
covering. Do not walk k=12 T-bands. Not a prize claim.

Run: python3 research/cycle_pe.py --certify
Dump: research/cycle_pe.json
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
from cycle_hg import covering_Q
from cycle_hh import bit_at
from cycle_hu import and_clause
from cycle_kh import g4_xor_cover
from cycle_lz import FORCED
from cycle_oj import doubling_slots, green_center_corner_pal
from cycle_pc import in_p4, in_p6
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
PD_JSON = Path(__file__).resolve().parent / "cycle_pd.json"
PC_JSON = Path(__file__).resolve().parent / "cycle_pc.json"
PB_JSON = Path(__file__).resolve().parent / "cycle_pb.json"

N_PAL = 64
M_SLOTS = 64
N_EDGE = 64
K_CELL = 12
PAT1001 = (1, 0, 0, 1)
PAT0100 = (0, 1, 0, 0)


def want_e(i: int, t: int) -> int:
    """Closed right-edge bit e_i(t) for i=0..5."""
    if i == 0:
        return 1
    if i in (1, 2):
        return t % 2
    if i == 3:
        return (t >> 1) & 1
    if i == 4:
        return int(t % 8 in (2, 4, 5, 7))
    if i == 5:
        return int(t % 8 in (3, 5, 7))
    raise ValueError("i")


def want_and_edge0(t: int) -> int:
    """Even t>=2: AND at p=2t."""
    return int(t % 4 == 2)


def want_and_edge2(t: int) -> int:
    """Even t>=2: AND at p=2t-2."""
    return int(t % 8 in (4, 6))


def pal_dual_p(s: int, p: int) -> int:
    """Covering palindrome dual packed column: p + p' = 2s+4."""
    return 2 * s + 4 - p


def covering_even_s(n: int, k: int) -> int:
    """Even s whose 4-tuple is the covering row for n on q=10."""
    U = 1 << k
    return 10 * U - 2 * n - 2


def dual_p4(k: int) -> tuple[int, int]:
    """Unique even n in the p=4 Green set: (n, j)=(3U-2, U-2)."""
    U = 1 << k
    return 3 * U - 2, U - 2


def dual_p6(k: int) -> tuple[int, int]:
    """Unique n==1 mod 4 in the p=6 Green set: (n, j)=(3U-3, U-3)."""
    U = 1 << k
    return 3 * U - 3, U - 3


def edge_bits() -> dict:
    """t<=N_EDGE: e0..e5 match want_e; even-t AND at r=0,2."""
    row = 1
    n_ok = 0
    n_even = 0
    for t in range(0, N_EDGE + 1):
        for i in range(0, 6):
            p = 2 * t - i
            got = (row >> p) & 1 if p >= 0 else 0
            if got != want_e(i, t):
                return {"ok": False, "i": i, "t": t, "got": got, "w": want_e(i, t)}
        if t >= 2 and t % 2 == 0:
            e = []
            for i in range(0, 6):
                p = 2 * t - i
                e.append((row >> p) & 1 if p >= 0 else 0)
            four0 = (e[3], e[2], e[1], e[0])
            four2 = (e[5], e[4], e[3], e[2])
            a0 = and_clause(*four0)
            a2 = and_clause(*four2)
            if a0 != want_and_edge0(t) or a2 != want_and_edge2(t):
                return {"ok": False, "and": t, "a0": a0, "a2": a2}
            if want_and_edge0(t) == 1 and four0 != PAT1001:
                return {"ok": False, "p1001": t, "four": four0}
            n_even += 1
        n_ok += 1
        row = rule30_step(row)
    ok = n_ok == N_EDGE + 1 and n_even == N_EDGE // 2
    return {"ok": ok, "n_ok": n_ok, "n_even": n_even, "t_hi": N_EDGE}


def pal_dual_id() -> dict:
    """p + pal-dual p = 2s+4 on covering q=10 samples."""
    n_ok = 0
    for k in range(0, 6):
        U = 1 << k
        T = 10 * U
        for n in range(0, 4 * U):
            s = covering_even_s(n, k)
            for j in range(0, 2 * n + 1):
                p = T - 2 * j
                p2 = T - 2 * (2 * n - j)
                if p + p2 != 2 * s + 4:
                    return {"ok": False, "k": k, "n": n, "j": j}
                if pal_dual_p(s, p) != p2:
                    return {"ok": False, "fn": k, "n": n, "j": j}
                n_ok += 1
    ok = n_ok > 0
    return {"ok": ok, "n_ok": n_ok}


def thin_duals() -> dict:
    """k<=K_CELL: p=4/p=6 pal-dual cells have packed AND=1."""
    n_ok = 0
    rows = {}
    for k in range(1, K_CELL + 1):
        U = 1 << k
        T = 10 * U
        n4, j4 = dual_p4(k)
        s4 = covering_even_s(n4, k)
        p4 = T - 2 * j4
        if not in_p4(n4, k) or G(n4, j4) != 1:
            return {"ok": False, "g4": k, "n": n4}
        if pal_dual_p(s4, 4) != p4 or p4 != 2 * s4:
            return {"ok": False, "dual4": k, "p": p4, "s": s4}
        if p4 in FORCED:
            return {"ok": False, "forced4": k, "p": p4}
        t_hi = s4
        n6 = j6 = s6 = p6 = None
        if k >= 2:
            n6, j6 = dual_p6(k)
            s6 = covering_even_s(n6, k)
            p6 = T - 2 * j6
            if not in_p6(n6, k) or G(n6, j6) != 1:
                return {"ok": False, "g6": k, "n": n6}
            if pal_dual_p(s6, 6) != p6 or p6 != 2 * s6 - 2:
                return {"ok": False, "dual6": k, "p": p6, "s": s6}
            if p6 in FORCED:
                return {"ok": False, "forced6": k, "p": p6}
            t_hi = max(t_hi, s6)
        row = 1
        four4 = four6 = None
        for t in range(0, t_hi + 1):
            if t == s4:
                four4 = tuple(bit_at(row, p4 - 3 + i) for i in range(4))
            if k >= 2 and t == s6:
                four6 = tuple(bit_at(row, p6 - 3 + i) for i in range(4))
            row = rule30_step(row)
        a4 = and_clause(*four4)
        if a4 != 1 or four4 != PAT1001 or s4 % 4 != 2:
            return {"ok": False, "and4": k, "four": four4, "s": s4}
        a6 = None
        if k >= 2:
            a6 = and_clause(*four6)
            if a6 != 1:
                return {"ok": False, "and6": k, "four": four6, "s": s6}
            if k >= 2 and s6 % 8 == 4 and four6 != PAT0100:
                return {"ok": False, "p0100": k, "four": four6}
        rows[str(k)] = {
            "n4": n4,
            "j4": j4,
            "a4": a4,
            "n6": n6,
            "j6": j6,
            "a6": a6,
        }
        n_ok += 1
    ok = n_ok == K_CELL and rows["1"]["a6"] is None and rows["2"]["a6"] == 1
    return {"ok": ok, "n_ok": n_ok, "k_hi": K_CELL, "rows": rows}


def killed_re_mod8() -> dict:
    """Even-n rest is not 1 iff k%8 in (0,1,2,7): k=9 is 0."""
    k = 9
    U = 1 << k
    T, t0, Q = 10 * U, 2 * U, covering_Q(10)
    row = 1
    for _ in range(t0):
        row = rule30_step(row)
    re = 0
    n_cells = 0
    s = t0
    prev = None
    while s < T:
        if s % 2 == 0:
            prev = row
        else:
            t = (s - t0) // 2
            n = odd_clock(t, U, Q)
            if n % 2 == 0:
                for j in range(0, 2 * n + 1, 2):
                    p = T - 2 * j
                    if p < 0:
                        continue
                    four = tuple(bit_at(prev, p - 3 + i) for i in range(4))
                    packed = and_clause(*four)
                    if G(n, j) and packed and p not in FORCED:
                        re ^= 1
                        n_cells += 1
        row = rule30_step(row)
        s += 1
    want = int(k % 8 in (0, 1, 2, 7))
    ok = re == 0 and want == 1
    return {"ok": ok, "k": k, "re": re, "want": want, "n_cells": n_cells}


def prefixes() -> dict:
    pd = json.loads(PD_JSON.read_text())
    pc = json.loads(PC_JSON.read_text())
    pb = json.loads(PB_JSON.read_text())
    ok = (
        pd["checks"]["all_ok"]
        and pc["checks"]["all_ok"]
        and pb["checks"]["all_ok"]
        and pd["verdict"]["packed_forced_all_k"] == "LEMMA"
        and pc["verdict"]["p4_set"] == "LEMMA"
        and pb["verdict"]["ST_all_k"] == "LEMMA"
        and pd["verdict"]["packed_R_eq_ST"] == "PREFIX"
        and pd["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(c20, pal, slots, edge, dual, thin, k9, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        pal["ok"]
        and slots["ok"]
        and edge["ok"]
        and dual["ok"]
        and thin["ok"]
        and k9["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    pal = green_center_corner_pal(N_PAL)
    slots = doubling_slots(M_SLOTS)
    edge = edge_bits()
    dual = pal_dual_id()
    thin = thin_duals()
    k9 = killed_re_mod8()
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, pal, slots, edge, dual, thin, k9, sc, pref)
    dump = {
        "cycle": "PE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "green_center_corner_pal": {k: pal[k] for k in pal if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "edge_bits": {k: edge[k] for k in edge if k != "ok"},
        "pal_dual_id": {k: dual[k] for k in dual if k != "ok"},
        "thin_duals": {k: thin[k] for k in thin if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_re_mod8": {k: k9[k] for k in k9 if k != "ok"},
        "lemmas": {
            "edge_e0_e5": True,
            "and_edge_r0_r2": True,
            "pal_dual_sum": True,
            "dual_p4_and": True,
            "dual_p6_and": True,
            "duals_cancel_k_ge_2": True,
            "packed_R_eq_ST": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "edge_e0_e5": "LEMMA",
            "and_edge_r0_r2": "LEMMA",
            "pal_dual_sum": "LEMMA",
            "dual_p4_and": "LEMMA",
            "dual_p6_and": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "re_mod8": "KILLED",
            "packed_R_eq_ST": "PREFIX",
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
    print("edge_bits n_ok", dump["edge_bits"]["n_ok"])
    print("pal_dual_id n_ok", dump["pal_dual_id"]["n_ok"])
    print("thin_duals n_ok", dump["thin_duals"]["n_ok"])
    print("killed_re_mod8", dump["killed_re_mod8"])
    print("g4_xor_cover", dump["g4_xor_cover"])


if __name__ == "__main__":
    main()
