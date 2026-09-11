#!/usr/bin/env python3
"""Cycle AG: O_s is local; at 1-run endings O_s = a XOR e.

Cycle AF wrote c_{s+2} = 1 XOR local ANDs XOR O_s with O_s the Green
parity of older AND hits, and treated O_s as bulk. On the prize orbit
c_{s+2} is already a function of the centred 5-window, so O_s equals
the local Boolean

    c'' XOR 1 XOR (ell AND c) XOR (c AND r) XOR (r AND e) XOR (c' AND r').

At a 1-run ending this is a XOR e, the distance-2 palindrome defect.
Infinitely many 00s is still infinitely many 1-run endings with
a = r OR e; O_s is not an extra bulk bit.

Not a prize claim.

Run: python3 research/cycle_ag.py --certify
Dump: research/cycle_ag.json
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


def evolve_rows(tmax: int) -> list[int]:
    row = 1
    out = []
    for _ in range(tmax + 1):
        out.append(row)
        row = rule30_step(row)
    return out


def older_parity(rows: list[int], t: int, target_t: int) -> int:
    acc = 0
    for s in range(t):
        A = (rows[s] << 1) & rows[s]
        delta = target_t - s - 1
        tmp, p = A, 0
        while tmp:
            if tmp & 1 and G(delta, target_t - p):
                acc ^= 1
            tmp >>= 1
            p += 1
    return acc


def step_cell(x: int, y: int, z: int) -> int:
    return x ^ (y | z)


def local_O(a: int, ell: int, c: int, r: int, e: int) -> int:
    cp = step_cell(ell, c, r)
    rp = step_cell(c, r, e)
    lp = step_cell(a, ell, c)
    cpp = step_cell(lp, cp, rp)
    local = (ell & c) ^ (c & r) ^ (r & e) ^ (cp & rp)
    return cpp ^ 1 ^ local


def ending_boolean() -> dict:
    """At (ell,c)=(1,1), local O equals a XOR e; 00 iff a == r OR e."""
    recs = {}
    ok_ae = True
    ok_00 = True
    for mask in range(8):
        a, r, e = (mask >> 2) & 1, (mask >> 1) & 1, mask & 1
        ell = c = 1
        O = local_O(a, ell, c, r, e)
        if O != (a ^ e):
            ok_ae = False
        lp = step_cell(a, ell, c)
        cp = step_cell(ell, c, r)
        rp = step_cell(c, r, e)
        cpp = step_cell(lp, cp, rp)
        is00 = cp == 0 and cpp == 0
        pred00 = a == (r | e)
        if is00 != pred00:
            ok_00 = False
        recs[f"{a}1{c}{r}{e}"] = {
            "O": O,
            "a_xor_e": a ^ e,
            "is00": is00,
            "a_eq_r_or_e": pred00,
        }
    return {"ok_ae": ok_ae, "ok_00": ok_00, "rows": recs}


def self_checks(c20, bools: dict, match_ok: bool, ending_ok: bool) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert bools["ok_ae"]
    assert bools["ok_00"]
    assert match_ok
    assert ending_ok
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    bools = ending_boolean()

    cap = 36
    rows = evolve_rows(cap + 4)
    match_fail = 0
    ending_fail = 0
    n10 = 0
    n_win = {}
    for t in range(0, cap):
        R = rows[t]
        a = (R >> (t - 2)) & 1 if t >= 2 else 0
        ell = (R >> (t - 1)) & 1 if t >= 1 else 0
        c = (R >> t) & 1
        r = (R >> (t + 1)) & 1
        e = (R >> (t + 2)) & 1
        O = older_parity(rows, t, t + 2)
        loc = local_O(a, ell, c, r, e)
        if O != loc:
            match_fail += 1
        w = f"{a}{ell}{c}{r}{e}"
        n_win[w] = n_win.get(w, 0) + 1
        cp = step_cell(ell, c, r)
        if c == 1 and cp == 0:
            n10 += 1
            if O != (a ^ e):
                ending_fail += 1
    match_ok = match_fail == 0
    ending_ok = ending_fail == 0

    checks = self_checks(c20, bools, match_ok, ending_ok)
    dump = {
        "cycle": "AG",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "boolean_O_eq_a_xor_e": bools["ok_ae"],
        "boolean_00_eq_a_or": bools["ok_00"],
        "green_vs_local_fail": match_fail,
        "ending_a_xor_e_fail": ending_fail,
        "n10": n10,
        "n_windows_seen": len(n_win),
        "lemmas": {
            "O_is_local": match_ok,
            "O_eq_a_xor_e_at_10": bools["ok_ae"] and ending_ok,
            "infinitely_many_00": None,
            "prize": False,
        },
        "verdict": {
            "O_is_local": "LEMMA",
            "O_eq_a_xor_e_at_10": "LEMMA",
            "O_is_bulk_00_handle": "KILLED",
            "infinitely_many_00": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("match_fail", match_fail, "ending_fail", ending_fail, "n10", n10)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
