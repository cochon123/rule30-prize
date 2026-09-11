#!/usr/bin/env python3
"""Cycle BV: left 2^k+1 machine; L_k freeze implies J_B->2U=0.

Packed bits 0..2^k evolve autonomously (each update reads only lower
packed bits). Freshman of length W=2^k targeting packed W picks up the
left edge, so Q_k(r):=J_{[rW,(r+1)W)->W} equals 1 XOR alpha_k(r) XOR
alpha_k(r+1). For k=1, packed bit 2 is 0 for every t>=2; for k=2,
packed bit 4 is 1 for every t>=2. If the left word at time 2W equals
that at time 3W, autonomy freezes it at every later sample rW (r>=2),
hence Q_k(r)=1 and alpha_k(3)=alpha_k(5). That last equality is
J_B^{->2U}=0 at covering scale k-1. L_k(2)=L_k(3) holds through
k=12 (prefix). Not a prize claim: the Fermat covering remains a prefix.

Run: python3 research/cycle_bv.py --certify
Dump: research/cycle_bv.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


@lru_cache(maxsize=None)
def G(m: int, d: int) -> int:
    if d < 0 or d > 2 * m:
        return 0
    if m == 0:
        return int(d == 0)
    if m % 2 == 0:
        if d % 2:
            return 0
        return G(m // 2, d // 2)
    n = m // 2
    if d % 2 == 0:
        return G(n, d // 2) ^ G(n, d // 2 - 1)
    return G(n, (d - 1) // 2)


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def packed_bit(row: int, t: int, p: int) -> int:
    if p < 0 or p > 2 * t:
        return 0
    return (row >> p) & 1


def left_word(row: int, W: int) -> int:
    return row & ((1 << (W + 1)) - 1)


def left_step(word: int, W: int) -> int:
    """One truncated left-machine step on bits 0..W. Bit 0 stays 1."""
    out = 1  # packed 0
    for p in range(1, W + 1):
        lo = (word >> (p - 2)) & 1 if p >= 2 else 0
        mid = (word >> (p - 1)) & 1
        hi = (word >> p) & 1
        bit = lo ^ (mid | hi)
        if bit:
            out |= 1 << p
    return out


def green_xor(rows: list[int], t0: int, t1: int, Tbit: int) -> int:
    acc = 0
    for t in range(t0, t1):
        tmp = (rows[t] << 1) & rows[t]
        m = t1 - t - 1
        p = 0
        while tmp:
            if tmp & 1 and G(m, Tbit - p):
                acc ^= 1
            tmp >>= 1
            p += 1
    return acc


def evolve(tmax: int) -> list[int]:
    rows = []
    row = 1
    for _t in range(tmax + 1):
        rows.append(row)
        row = rule30_step(row)
    return rows


def bit2_bit4_ok(tmax: int) -> bool:
    row = 1
    for t in range(tmax + 1):
        if t >= 2:
            if packed_bit(row, t, 2) != 0:
                return False
            if packed_bit(row, t, 4) != 1:
                return False
        if t >= 1:
            if packed_bit(row, t, 0) != 1 or packed_bit(row, t, 1) != 1:
                return False
        row = rule30_step(row)
    return True


def autonomy_ok(kmax: int, rmax: int) -> bool:
    tmax = (rmax + 1) * (1 << kmax)
    rows = evolve(tmax)
    for k in range(1, kmax + 1):
        W = 1 << k
        for t in range(W, rmax * W):
            cur = left_word(rows[t], W)
            nxt = left_word(rows[t + 1], W)
            if left_step(cur, W) != nxt:
                return False
    return True


def Q_identity_ok(rows: list[int], kmax: int, rmax: int) -> bool:
    for k in range(1, kmax + 1):
        W = 1 << k
        for r in range(1, rmax + 1):
            t0 = r * W
            t1 = (r + 1) * W
            if t1 >= len(rows):
                continue
            a0 = packed_bit(rows[t0], t0, W)
            a1 = packed_bit(rows[t1], t1, W)
            Q = green_xor(rows, t0, t1, W)
            if Q != (1 ^ a0 ^ a1):
                return False
    return True


def snapshot_left(kmax: int, rmax: int) -> dict:
    need: dict[int, list[tuple[int, int]]] = {}
    for k in range(1, kmax + 1):
        W = 1 << k
        for r in range(1, rmax + 1):
            need.setdefault(r * W, []).append((k, r))
    tmax = rmax * (1 << kmax)
    row = 1
    words: dict[tuple[int, int], int] = {}
    for t in range(tmax + 1):
        if t in need:
            for k, r in need[t]:
                W = 1 << k
                words[(k, r)] = left_word(row, W)
        row = rule30_step(row)
    eq23 = []
    eq_rge2 = []
    alpha2 = []
    Q_from2 = []
    for k in range(1, kmax + 1):
        W = 1 << k
        freeze = all(
            words[(k, r)] == words[(k, 2)] for r in range(2, rmax + 1)
        )
        eq23.append(words[(k, 2)] == words[(k, 3)])
        eq_rge2.append(freeze)
        a = [(words[(k, r)] >> W) & 1 for r in range(1, rmax + 1)]
        alpha2.append(a[1])
        Q_from2.append([1 ^ a[i] ^ a[i + 1] for i in range(1, len(a) - 1)])
    return {
        "eq23": eq23,
        "eq_rge2": eq_rge2,
        "all_eq23": all(eq23),
        "all_freeze": all(eq_rge2),
        "alpha_at_r2": alpha2,
        "Q_r_ge2": Q_from2,
        "Q_r_ge2_all_1": all(all(q == 1 for q in row) for row in Q_from2),
    }


def JB2_from_alpha(kmax: int) -> dict:
    """J_B->2U = alpha_{k+1}(3) xor alpha_{k+1}(5)."""
    need = set()
    for k in range(1, kmax + 1):
        U = 1 << k
        W = 2 * U
        need.update((3 * W, 5 * W, 6 * U, 10 * U))
    tmax = 10 * (1 << kmax)
    row = 1
    samp: dict[int, int] = {}
    for t in range(tmax + 1):
        if t in need:
            samp[t] = row
        row = rule30_step(row)
    eq = []
    zeros = []
    for k in range(1, kmax + 1):
        U = 1 << k
        W = 2 * U
        a3 = packed_bit(samp[3 * W], 3 * W, W)
        a5 = packed_bit(samp[5 * W], 5 * W, W)
        left6 = packed_bit(samp[6 * U], 6 * U, 2 * U)
        left10 = packed_bit(samp[10 * U], 10 * U, 2 * U)
        eq.append(a3 == left6 and a5 == left10 and (a3 ^ a5) == (left6 ^ left10))
        zeros.append(a3 == a5)
    return {"alpha_is_left_extra": all(eq), "JB2_zero": zeros, "all_zero": all(zeros)}


def bit2_not_const_high(kmax: int) -> bool:
    """Packed bit 2^k is not identically constant on [2^k, 4*2^k] for some k>=3."""
    both = False
    for k in range(3, kmax + 1):
        W = 1 << k
        row = 1
        seen = set()
        for t in range(0, 4 * W + 1):
            if t >= W:
                seen.add(packed_bit(row, t, W))
            row = rule30_step(row)
        if seen == {0, 1}:
            both = True
    return both


def self_checks(
    c20,
    b24: bool,
    aut: bool,
    qid: bool,
    snap: dict,
    jb: dict,
    both: bool,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert b24 and aut and qid
    assert snap["all_eq23"] and snap["all_freeze"]
    assert snap["Q_r_ge2_all_1"]
    assert jb["alpha_is_left_extra"] and jb["all_zero"]
    assert both
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    b24 = bit2_bit4_ok(128)
    aut = autonomy_ok(6, 6)
    rows = evolve(6 * (1 << 5))
    qid = Q_identity_ok(rows, 5, 4)
    snap = snapshot_left(12, 4)
    jb = JB2_from_alpha(11)
    both = bit2_not_const_high(6)
    checks = self_checks(c20, b24, aut, qid, snap, jb, both)
    dump = {
        "cycle": "BV",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "freeze_k12": {
            "eq23": snap["eq23"],
            "Q_r_ge2_all_1": snap["Q_r_ge2_all_1"],
        },
        "JB2_zero_k11": jb["JB2_zero"],
        "lemmas": {
            "left_machine_autonomous": True,
            "packed_bit_2_zero_t_ge_2": True,
            "packed_bit_4_one_t_ge_2": True,
            "Q_eq_1_xor_alpha_xor_alpha": True,
            "L2_eq_L3_implies_freeze": True,
            "JB2_eq_alpha3_xor_alpha5": True,
            "L_k_2_eq_L_k_3_all_k": None,
            "packed_2k_identically_constant": False,
            "fermat_cover_359_all_k": None,
            "prize": False,
        },
        "verdict": {
            "left_machine_autonomous": "LEMMA",
            "packed_bit_2_zero_t_ge_2": "LEMMA",
            "packed_bit_4_one_t_ge_2": "LEMMA",
            "Q_eq_1_xor_alpha_xor_alpha": "LEMMA",
            "L2_eq_L3_implies_freeze": "LEMMA",
            "JB2_eq_alpha3_xor_alpha5": "LEMMA",
            "L_k_2_eq_L_k_3_all_k": "PREFIX",
            "packed_2k_identically_constant": "KILLED",
            "fermat_cover_359_all_k": "PREFIX",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("eq23", snap["eq23"])


if __name__ == "__main__":
    main()
