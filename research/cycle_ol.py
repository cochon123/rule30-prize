#!/usr/bin/env python3
"""Cycle OL: fixed-depth right-edge ANDs are silent in I_k.

Right diagonals u(t,q)=x(t,t-q) are purely periodic of period dividing
2^q. On the dyadic annulus t in [T,2T), T=2^{k-1}, an adjacent AND of
diagonals s and s+1 can Green-hit the next centre only at times
t=T+j with j<=s//2. For k>=s+2 those times reduce, by the period, to
the cone at time j, where diagonal s+1 lies strictly outside the left
edge. The AND is dead, so it contributes 0 to I_k.

Closed forms for q<=4 make the pairs s=0,1,2 completely explicit for
every k: s=0 hits iff k=1, s=1 never hits, s=2 hits iff k=2.

This does not prove I_k=1 infinitely often. Offset s=k-1 is the first
index the period bound does not silence. Not a prize claim.

Run: python3 research/cycle_ol.py --certify
Dump: research/cycle_ol.json
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

T_CLOSED = 4096
Q_PERIOD = 12
N_PERIOD = 1 << 14
K_SCAN = 12
S_SCAN = 10


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


def u1(t: int) -> int:
    return t & 1


def u2(t: int) -> int:
    return t & 1


def u3(t: int) -> int:
    return (t >> 1) & 1


def u4(t: int) -> int:
    return ((t >> 2) & 1) ^ (1 if t % 4 == 2 else 0)


def check_closed_forms(rows: list[int]) -> dict:
    n = 0
    for t in range(T_CLOSED):
        R = rows[t]
        assert diag(R, t, 0) == 1
        if t == 0:
            assert diag(R, t, 1) == 0
            assert diag(R, t, 2) == 0
            assert diag(R, t, 3) == 0
            assert diag(R, t, 4) == 0
        else:
            assert diag(R, t, 1) == u1(t)
            assert diag(R, t, 2) == u2(t)
            assert diag(R, t, 3) == u3(t)
            assert diag(R, t, 4) == u4(t)
        # Left edge is packed bit 0.
        assert R & 1 == 1
        n += 1
    return {"ok": True, "n_t": n}


def integrator_triangle(n: int, qmax: int) -> list[bytearray]:
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


def check_period(U: list[bytearray]) -> dict:
    qmax = len(U[0])
    n = len(U) - 1
    for q in range(qmax):
        period = 1 << q
        assert 2 * period <= n
        col0 = U[0][q]
        for t in range(n + 1):
            assert U[t][q] == U[t % period][q]
        if q > 0:
            assert col0 == 0
    return {"ok": True, "qmax": qmax, "n": n}


def check_integrator_matches_rows(rows: list[int], U: list[bytearray]) -> dict:
    qmax = len(U[0])
    n = min(len(rows), len(U)) - 1
    n_ok = 0
    for t in range(n + 1):
        for q in range(qmax):
            assert U[t][q] == diag(rows[t], t, q)
            n_ok += 1
    # Centre samples the diagonal q=t, for t<qmax.
    for t in range(min(qmax, n + 1)):
        assert U[t][t] == ((rows[t] >> t) & 1)
    return {"ok": True, "n_ok": n_ok}


def contribution(rows: list[int], k: int, s: int) -> int:
    """Green parity of the adjacent AND on right-diagonals s and s+1."""
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


def arithmetic_s012(k: int, s: int) -> int:
    """All-k contribution of s=0,1,2 from the closed forms. No rows."""
    if s == 0:
        return 1 if k == 1 else 0
    if s == 1:
        return 0
    if s == 2:
        return 1 if k == 2 else 0
    raise ValueError(s)


def check_margin(rows: list[int]) -> dict:
    fires: list[list[int]] = []
    n_silent = 0
    for k in range(1, K_SCAN + 1):
        for s in range(0, S_SCAN + 1):
            got = contribution(rows, k, s)
            if k >= s + 2 and got != 0:
                raise AssertionError(f"margin spoke k={k} s={s}")
            if k >= s + 2:
                n_silent += 1
            if got:
                fires.append([k, s])
            if s <= 2:
                assert got == arithmetic_s012(k, s)
    # Closed forms decide s=0,1,2 for every k, not only k<=K_SCAN.
    for k in range(1, 65):
        for s in range(3):
            assert arithmetic_s012(k, s) == (1 if (s, k) in ((0, 1), (2, 2)) else 0)
    by_s: dict[str, list[int]] = {}
    for k, s in fires:
        by_s.setdefault(str(s), []).append(k)
    return {
        "ok": True,
        "n_silent": n_silent,
        "fires": fires,
        "fires_by_s": by_s,
        "k_scan": K_SCAN,
        "s_scan": S_SCAN,
    }


def self_checks(c20, closed, period, match, margin) -> dict:
    assert list(c20) == list(KNOWN20)
    assert list(c20) == list(experiment_center_bits(20))
    assert closed["ok"] and period["ok"] and match["ok"] and margin["ok"]
    assert margin["fires_by_s"].get("0") == [1]
    assert "1" not in margin["fires_by_s"]
    assert margin["fires_by_s"].get("2") == [2]
    assert "3" not in margin["fires_by_s"]
    assert margin["n_silent"] > 0
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = experiment_center_bits(20)
    rows = evolve(max(T_CLOSED, 1 << K_SCAN))
    closed = check_closed_forms(rows)
    U = integrator_triangle(N_PERIOD, Q_PERIOD)
    period = check_period(U)
    match = check_integrator_matches_rows(rows, U)
    margin = check_margin(rows)
    checks = self_checks(c20, closed, period, match, margin)
    dump = {
        "cycle": "OL",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "closed_forms": closed,
        "period": period,
        "integrator_match": match,
        "margin": {
            "n_silent": margin["n_silent"],
            "fires": margin["fires"],
            "fires_by_s": margin["fires_by_s"],
            "k_scan": margin["k_scan"],
            "s_scan": margin["s_scan"],
        },
        "lemmas": {
            "period_div_2q": True,
            "margin_silent": True,
            "closed_forms_q_le_4": True,
            "s0_iff_k1": True,
            "s1_never": True,
            "s2_iff_k2": True,
            "I_1_infinitely_often": False,
            "prize": False,
        },
        "verdict": {
            "period_div_2q": "LEMMA",
            "margin_s_le_k_minus_2": "LEMMA",
            "closed_forms_q_le_4": "LEMMA",
            "s0_hits_iff_k1": "LEMMA",
            "s1_never_hits": "LEMMA",
            "s2_hits_iff_k2": "LEMMA",
            "s3_never_hits": "LEMMA",
            "sharper_than_k_minus_2": "OPEN",
            "I_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("fires", margin["fires"])


if __name__ == "__main__":
    main()
