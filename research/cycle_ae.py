#!/usr/bin/env python3
"""Cycle AE: no white stripes on the right; Green formula for d; nested-right kill.

Cycle AD found extra left-diagonals that are eventually 0 (white stripes)
and killed bounded-depth nested left as a centre-00 production. This cycle
records the chiral dual: every right-diagonal u(t,k)=x(t,t-k) is a pure
integrator of (u_{k-1} OR u_{k-2}), so the only eventually-constant one is
the right edge u(*,0)≡1. Each fixed k meets the centred 5-window at most
five times, so nested right is not a 00 production either.

The palindrome defect d=ell XOR r is exactly the Green difference of AND
injections to packed bits t-1 and t+1 (linear parts cancel by Cycle AA).
A 1-run ending is followed by 00 iff x(t,-2) = r OR x(t,2).

Not a prize claim: infinitely many 00s still need a bulk production.

Run: python3 research/cycle_ae.py --certify
Dump: research/cycle_ae.json
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
    """[x^d](1+x+x^2)^m over GF(2), doubling recurrence (Cycle AA)."""
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


def u_bit(rows: list[int], t: int, k: int) -> int:
    """x(t, t-k) = packed bit 2t-k."""
    if k < 0:
        return 0
    bitpos = 2 * t - k
    if bitpos < 0:
        return 0
    return (rows[t] >> bitpos) & 1


def finite_incidence_right(k: int, t_lo: int, t_hi: int) -> list[int]:
    """Times at which right-diagonal k sits in the centred 5-window."""
    hits = []
    for t in range(t_lo, t_hi + 1):
        spatial = t - k
        if -2 <= spatial <= 2:
            hits.append(t)
    return hits


def green_defect(rows: list[int], t: int) -> int:
    """AND-Green difference between packed bits t-1 and t+1."""
    acc = 0
    for s in range(t):
        A = (rows[s] << 1) & rows[s]
        delta = t - s - 1
        tmp = A
        p = 0
        while tmp:
            if tmp & 1:
                acc ^= G(delta, (t - 1) - p) ^ G(delta, (t + 1) - p)
            tmp >>= 1
            p += 1
    return acc


def green_center(rows: list[int], t: int) -> int:
    acc = G(t, t)
    for s in range(t):
        A = (rows[s] << 1) & rows[s]
        delta = t - s - 1
        tmp = A
        p = 0
        while tmp:
            if tmp & 1:
                acc ^= G(delta, t - p)
            tmp >>= 1
            p += 1
    return acc


def self_checks(
    c20,
    rec_ok: bool,
    edge0: bool,
    toggle12: bool,
    no_const: bool,
    hits: dict,
    d_ok: bool,
    c_ok: bool,
    ae_ok: bool,
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert rec_ok
    assert edge0
    assert toggle12
    assert no_const
    assert d_ok
    assert c_ok
    assert ae_ok
    for _k, h in hits.items():
        assert len(h) <= 5
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--tmax", type=int, default=8)
    args = parser.parse_args()
    t0 = time.perf_counter()
    tmax = 1 << args.tmax
    c20 = packed_center_bits(20)
    rows = evolve_rows(tmax)

    rec_fail = 0
    rec_n = 0
    rec_cap = min(tmax, 64)
    for t in range(rec_cap):
        for k in range(0, 2 * t + 1):
            got = u_bit(rows, t + 1, k)
            want = u_bit(rows, t, k) ^ (
                u_bit(rows, t, k - 1) | u_bit(rows, t, k - 2)
            )
            rec_n += 1
            if got != want:
                rec_fail += 1
    rec_ok = rec_fail == 0

    edge0 = all(u_bit(rows, t, 0) == 1 for t in range(tmax + 1))
    # k=1,2: forcing is identically 1, so they toggle.
    tcap = min(tmax, 128)
    f1 = all(
        (u_bit(rows, t, 0) | u_bit(rows, t, -1)) == 1 for t in range(1, tcap + 1)
    )
    f2 = all(
        (u_bit(rows, t, 1) | u_bit(rows, t, 0)) == 1 for t in range(1, tcap + 1)
    )
    tog1 = all(
        u_bit(rows, t + 1, 1) == (u_bit(rows, t, 1) ^ 1)
        for t in range(1, tcap)
    )
    tog2 = all(
        u_bit(rows, t + 1, 2) == (u_bit(rows, t, 2) ^ 1)
        for t in range(1, tcap)
    )
    toggle12 = f1 and f2 and tog1 and tog2 and u_bit(rows, 1, 1) == 1

    both_values = []
    for k in range(0, 13):
        seq = [u_bit(rows, t, k) for t in range((k + 1) // 2, tcap + 1)]
        both_values.append(
            {"k": k, "values": sorted(set(seq)), "n": len(seq)}
        )
    no_const = all(set(d["values"]) == {0, 1} for d in both_values if d["k"] >= 1)
    no_const = no_const and both_values[0]["values"] == [1]

    hits = {
        str(k): finite_incidence_right(k, max((k + 1) // 2, 2), tmax)
        for k in range(0, 8)
    }

    d_fail = 0
    c_fail = 0
    gcap = min(tmax, 40)
    for t in range(1, gcap):
        ell = (rows[t] >> (t - 1)) & 1
        rbit = (rows[t] >> (t + 1)) & 1
        if green_defect(rows, t) != (ell ^ rbit):
            d_fail += 1
        if green_center(rows, t) != ((rows[t] >> t) & 1):
            c_fail += 1
    d_ok = d_fail == 0
    c_ok = c_fail == 0

    ae_fail = 0
    n10 = n10_00 = 0
    for t in range(2, tmax - 2):

        def bit(tt: int, jj: int) -> int:
            kk = jj + tt
            if kk < 0:
                return 0
            return (rows[tt] >> kk) & 1

        if bit(t, 0) == 1 and bit(t + 1, 0) == 0:
            n10 += 1
            a, rbit, e = bit(t, -2), bit(t, 1), bit(t, 2)
            is00 = bit(t + 2, 0) == 0
            if is00:
                n10_00 += 1
            if is00 != (a == (rbit | e)):
                ae_fail += 1
    ae_ok = ae_fail == 0

    checks = self_checks(
        c20, rec_ok, edge0, toggle12, no_const, hits, d_ok, c_ok, ae_ok
    )

    dump = {
        "cycle": "AE",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "recurrence_ok": rec_ok,
        "recurrence_n": rec_n,
        "right_edge_one": edge0,
        "k1_k2_toggle": toggle12,
        "right_diagonals": both_values,
        "no_right_white_stripe_k1_12": no_const,
        "finite_incidence": hits,
        "green_d_fail": d_fail,
        "green_c_fail": c_fail,
        "n10": n10,
        "n10_00": n10_00,
        "ae_fail": ae_fail,
        "lemmas": {
            "right_integrator": rec_ok,
            "only_u0_constant": no_const,
            "finite_incidence_right": True,
            "green_defect": d_ok,
            "run_end_00_iff_a_eq_r_or_e": ae_ok,
            "infinitely_many_00": None,
            "prize": False,
        },
        "verdict": {
            "right_integrator": "LEMMA",
            "no_right_white_stripe": "LEMMA",
            "finite_incidence_right": "LEMMA",
            "green_defect": "LEMMA",
            "run_end_00_iff_a_eq_r_or_e": "LEMMA",
            "nested_right_5window_00": "KILLED",
            "right_white_stripes_like_left": "KILLED",
            "green_d_closed_form_for_I_k": "KILLED",
            "infinitely_many_00": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("rec_fail", rec_fail, "d_fail", d_fail, "c_fail", c_fail, "ae_fail", ae_fail)
    print("no_right_stripe", no_const, "n10", n10, "n10_00", n10_00)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
