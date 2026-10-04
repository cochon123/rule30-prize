#!/usr/bin/env python3
"""Cycle ON: the dyadic left-diagonal OR-sum is the centre.

The sum checked for k<=11 in the previous pass,

    b_k = XOR_{J=1}^{T-1} (e_{2J+1}(T+J) OR e_{2J+2}(T+J)),

with T=2^{k-1}, is proved for every k>=2 by telescoping the diagonal
recurrence. It equals c_{2^k} and is not a compression. The same
cancellation is the Mahler prefix form in mahler_dependency.md, read
on right diagonals u(t, n-1) and u(t, n-2).

Not a prize claim: I_k=1 infinitely often, nonperiodicity of (b_k),
and infinitely many centre 00s stay open.

Run: python3 research/cycle_on.py --certify
Dump: research/cycle_on.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
N_CHECK = 512
K_PACKED = 12


def step_row(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def evolve_packed(count: int) -> tuple[list[int], list[int]]:
    row = 1
    rows = []
    cent = []
    for t in range(count):
        cent.append((row >> t) & 1)
        rows.append(row)
        row = step_row(row)
    cent.append((row >> count) & 1)
    return rows, cent


def prefix_sum_matches_centre(n_max: int) -> dict:
    """c_n = XOR_{t<n} (u(t,n-1) OR u(t,n-2)), u from the edge recurrence."""
    st = [0] * (n_max + 1)
    st[0] = 1
    acc = [0] * (n_max + 1)
    cent = []
    cone_ok = True
    for t in range(n_max):
        cent.append(st[t])
        for k in range(2 * t + 1, n_max + 1):
            if st[k]:
                cone_ok = False
                break
        for n in range(t + 1, n_max + 1):
            left = st[n - 1]
            right = st[n - 2] if n >= 2 else 0
            acc[n] ^= left | right
        new = [0] * (n_max + 1)
        new[0] = 1
        for k in range(1, n_max + 1):
            b = st[k - 1]
            c = st[k - 2] if k >= 2 else 0
            new[k] = st[k] ^ (b | c)
        st = new
    cent.append(st[n_max])
    mismatches = [n for n in range(1, n_max + 1) if acc[n] != cent[n]]
    return {
        "n_max": n_max,
        "cone_ok": cone_ok,
        "n_mismatch": len(mismatches),
        "first_mismatch": mismatches[:5],
        "c1": cent[1],
    }


def endpoint_bits(rows: list[int], k: int) -> dict:
    """The two 1s that cancel, leaving the J=1..T-1 sum.

    At t=T-1 the depth 2T-2 cell is the left edge (packed bit 0).
    At t=T the same two depths are packed bits 1 and 2, i.e. e_1 and e_2.
    """
    T = 1 << (k - 1)
    edge = rows[T - 1] & 1
    e1 = (rows[T] >> 1) & 1
    e2 = (rows[T] >> 2) & 1
    return {"edge": edge, "e1": e1, "e2": e2, "j0": e1 | e2}


def j_sum(rows: list[int], k: int) -> int:
    T = 1 << (k - 1)
    acc = 0
    for J in range(1, T):
        t = T + J
        acc ^= ((rows[t] >> (2 * J + 1)) & 1) | ((rows[t] >> (2 * J + 2)) & 1)
    return acc


def certify() -> dict:
    t0 = time.perf_counter()
    ref = list(experiment_center_bits(20))
    rows, cent = evolve_packed(1 << K_PACKED)
    prefix = prefix_sum_matches_centre(N_CHECK)
    ends = []
    j_ok = True
    for k in range(2, K_PACKED + 1):
        ep = endpoint_bits(rows, k)
        got = j_sum(rows, k)
        want = cent[1 << k]
        ends.append({"k": k, "edge": ep["edge"], "e1": ep["e1"], "e2": ep["e2"], "j0": ep["j0"], "sum": got, "b": want})
        if ep["edge"] != 1 or ep["e1"] != 1 or ep["e2"] != 0 or ep["j0"] != 1:
            j_ok = False
        if got != want:
            j_ok = False
    wall = time.perf_counter() - t0
    ok = (
        ref == KNOWN20
        and list(cent[:20]) == KNOWN20
        and prefix["n_mismatch"] == 0
        and prefix["cone_ok"]
        and prefix["c1"] == 1
        and j_ok
    )
    return {
        "ok": ok,
        "wall_s": round(wall, 3),
        "known20": ref == KNOWN20,
        "prefix": prefix,
        "j_sum_ok": j_ok,
        "endpoints": ends,
        "verdict": {
            "telescope": "LEMMA",
            "compression_of_b_k": "KILLED",
            "I_1_infinitely_often": "OPEN",
            "b_not_eventually_periodic": "OPEN",
            "infinitely_many_00": "OPEN",
            "prize": "unsolved",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    if not args.certify:
        parser.print_help()
        return
    report = certify()
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("ok", "wall_s", "j_sum_ok", "verdict")}, indent=2))
    if not report["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
