#!/usr/bin/env python3
"""Cycle OM: right diagonals have period dividing 2^{q-floor((q-2)/3)-1}.

Cycle OL bounds the period of u(t,q) by 2^q. One more halving is free
for every q>=2, because the forcing of diagonal q then has period
dividing 2^{q-2}. The same halving repeats. For each r>=0 and every
q>=3r+2, the period divides 2^{q-1-r}, i.e.

    period | 2^{q - 1 - floor((q-2)/3)}     (q>=2).

On a dyadic annulus the adjacent AND of diagonals s and s+1 is silent
whenever that period divides T=2^{k-1}. The resulting margin is
s - floor((s-1)/3) <= k-1, about (3/2)k rather than k-2. Depths
s<=k collapse further: the only nonzero contributions are the two
Cycle OL hits (k,s)=(1,0) and (2,2).

This does not prove I_k=1 infinitely often. The first unsilenced
offset is still O(k) cells in from the right edge. Not a prize claim.

Run: python3 research/cycle_om.py --certify
Dump: research/cycle_om.json
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
from cycle_ca import KNOWN20

OUT = Path(__file__).resolve().with_suffix(".json")

Q_CHECK = 22
N_PERIOD = 1 << 16
K_SCAN = 12
S_SCAN = 20


def gamma(q: int) -> int:
    """Proved exponent: period of u(·,q) divides 2^{gamma(q)}."""
    if q <= 0:
        return 0
    if q == 1:
        return 1
    return q - 1 - (q - 2) // 3


def evolve(tmax: int) -> list[int]:
    rows = [1]
    row = 1
    for _ in range(tmax):
        row = (row << 2) ^ ((row << 1) | row)
        rows.append(row)
    return rows


def diag(row: int, t: int, q: int) -> int:
    if q < 0 or q > 2 * t:
        return 0
    return (row >> (2 * t - q)) & 1


def integrator(n: int, qmax: int) -> list[bytearray]:
    U = [bytearray(qmax) for _ in range(n + 1)]
    for t in range(n + 1):
        U[t][0] = 1
    for t in range(n):
        prev = U[t]
        nxt = U[t + 1]
        for q in range(1, qmax):
            left = prev[q - 1]
            left2 = prev[q - 2] if q >= 2 else 0
            nxt[q] = prev[q] ^ (left | left2)
    return U


def check_closed_forms(U: list[bytearray]) -> dict:
    n = min(len(U) - 1, 4096)
    for t in range(n):
        assert U[t][0] == 1
        assert U[t][1] == (t & 1)
        assert U[t][2] == (t & 1)
        assert U[t][3] == (t >> 1) & 1
        assert U[t][4] == ((t >> 2) & 1) ^ (1 if t % 4 == 2 else 0)
    # The r=0 bound is sharp at q=4: u(4,4)=1, so the period does not divide 4.
    assert U[4][4] == 1
    return {"ok": True, "n_t": n}


def check_exponent(U: list[bytearray]) -> dict:
    """Measured minimal exponent is at most gamma(q), and the bound holds on the window."""
    qmax = min(Q_CHECK, len(U[0]))
    n = len(U) - 1
    measured = []
    sharp = []
    for q in range(qmax):
        g = gamma(q)
        P = 1 << g
        assert 2 * P <= n, (q, g, n)
        for t in range(n - P + 1):
            if U[t][q] != U[t + P][q]:
                raise AssertionError(f"period failed q={q} t={t} P={P}")
        # minimal exponent among powers of two
        amin = g
        for a in range(g + 1):
            p = 1 << a
            if all(U[t][q] == U[t + p][q] for t in range(n - p + 1)):
                amin = a
                break
        assert amin <= g
        measured.append(amin)
        if amin == g:
            sharp.append(q)
        # ladder vanishing: u(2^{q-1-r}, q)=0 whenever level r applies and the time fits
        for r in range((q - 2) // 3 + 1 if q >= 2 else 0):
            if q < 3 * r + 2:
                continue
            exp = q - 1 - r
            if exp < 0 or (1 << exp) > n:
                continue
            assert U[1 << exp][q] == 0, (q, r, exp)
    return {
        "ok": True,
        "qmax": qmax,
        "measured": measured,
        "sharp_q": sharp,
        "gamma": [gamma(q) for q in range(qmax)],
    }


def check_base_bits(U: list[bytearray]) -> dict:
    """The ladder base u(2^{2r+3}, 3r+5)=0, while the time still lies in the triangle."""
    n = len(U) - 1
    bases = []
    r = 0
    while True:
        a = 2 * r + 3
        q = 3 * r + 5
        if q >= len(U[0]) or (1 << a) > n:
            break
        bit = U[1 << a][q]
        assert bit == 0, (r, a, q, bit)
        bases.append({"r": r, "time_exp": a, "q": q, "bit": bit})
        r += 1
    assert len(bases) >= 4
    return {"ok": True, "bases": bases}


def truth_table() -> dict:
    """(A∨B) ⊕ ((A⊕1)∨B) = ¬B. Integrator parity over an even window is 0."""
    for A in (0, 1):
        for B in (0, 1):
            delta = (A | B) ^ (((A ^ 1) | B))
            assert delta == (B ^ 1)
    # Running XOR of a period-Q forcing, summed on [0, 2Q), Q even.
    for width in (2, 4, 8):
        for mask in range(1 << width):
            phi = [(mask >> i) & 1 for i in range(width)]
            total = 0
            acc = 0
            for t in range(2 * width):
                total ^= acc
                acc ^= phi[t % width]
            assert total == 0
    return {"ok": True}


def contribution(rows: list[int], k: int, s: int) -> int:
    T = 1 << (k - 1)
    xor = 0
    for t in range(T, 2 * T):
        p = 2 * t - s
        if p < 1:
            continue
        R = rows[t]
        if ((R >> p) & 1) and ((R >> (p - 1)) & 1):
            if G(2 * T - 1 - t, 2 * T - p):
                xor ^= 1
    return xor


def silenced(k: int, s: int) -> bool:
    """Margin: s>=1 and gamma(s+1) <= k-1."""
    if s < 1:
        return False
    return gamma(s + 1) <= k - 1


def check_margin(rows: list[int]) -> dict:
    fires = []
    n_silent = 0
    beyond_ol = 0
    for k in range(1, K_SCAN + 1):
        for s in range(0, S_SCAN + 1):
            got = contribution(rows, k, s)
            if silenced(k, s):
                if got != 0:
                    raise AssertionError(f"new margin spoke k={k} s={s}")
                n_silent += 1
                if k < s + 2:
                    beyond_ol += 1
            if got:
                fires.append([k, s])
    # Depths s<=k: only the two classical hits. Finite for k<=K_SCAN,
    # and the writeup proves it for every k.
    for k in range(1, K_SCAN + 1):
        for s in range(0, k + 1):
            got = contribution(rows, k, s)
            expect = 1 if (k, s) in ((1, 0), (2, 2)) else 0
            assert got == expect, (k, s, got)
    assert [1, 0] in fires and [2, 2] in fires
    # A pair OL's s<=k-2 bound does not kill, which the new bound does.
    assert silenced(8, 10) and not (8 >= 10 + 2)
    assert contribution(rows, 8, 10) == 0
    # s=k+1 still fires, so the margin is not the whole annulus.
    assert [3, 4] in fires and [5, 6] in fires
    return {
        "ok": True,
        "n_silent": n_silent,
        "beyond_ol": beyond_ol,
        "fires": fires,
        "k_scan": K_SCAN,
        "s_scan": S_SCAN,
    }


def self_checks(c20, closed, exponent, bases, table, margin) -> dict:
    assert list(c20) == list(KNOWN20)
    assert list(c20) == list(experiment_center_bits(20))
    assert closed["ok"] and exponent["ok"] and bases["ok"]
    assert table["ok"] and margin["ok"]
    assert exponent["measured"][4] == 3
    assert exponent["measured"][5] == 3
    assert 4 in exponent["sharp_q"] and 5 in exponent["sharp_q"] and 8 in exponent["sharp_q"]
    assert margin["beyond_ol"] > 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = experiment_center_bits(20)
    U = integrator(N_PERIOD, Q_CHECK)
    closed = check_closed_forms(U)
    exponent = check_exponent(U)
    bases = check_base_bits(U)
    table = truth_table()
    rows = evolve(1 << K_SCAN)
    margin = check_margin(rows)
    checks = self_checks(c20, closed, exponent, bases, table, margin)
    dump = {
        "cycle": "OM",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "closed_forms": closed,
        "exponent": {
            "qmax": exponent["qmax"],
            "measured": exponent["measured"],
            "gamma": exponent["gamma"],
            "sharp_q": exponent["sharp_q"],
        },
        "bases": bases["bases"],
        "margin": {
            "n_silent": margin["n_silent"],
            "beyond_ol": margin["beyond_ol"],
            "fires": margin["fires"],
            "k_scan": margin["k_scan"],
            "s_scan": margin["s_scan"],
        },
        "verdict": {
            "period_div_2_to_q_minus_1": "LEMMA",
            "period_third_saving": "LEMMA",
            "margin_three_halves": "LEMMA",
            "s_le_k_only_two_hits": "LEMMA",
            "I_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("sharp_q", exponent["sharp_q"])
    print("beyond_ol", margin["beyond_ol"], "silent", margin["n_silent"])
    print("bases", len(bases["bases"]))


if __name__ == "__main__":
    main()
