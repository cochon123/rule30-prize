#!/usr/bin/env python3
"""Cycle AI: dyadic step from arbitrary time; palindrome graphs at 2^k.

From any time t, evolving 2^k steps of packed Rule 150 multiplies by
1+x^{2^k}+x^{2^{k+1}}, so

    c_{t+2^k} = c_t XOR x(t,-2^k) XOR x(t,2^k) XOR J_{t,k},

with x(t,j)=0 for |j|>t and J the Green AND parity on [t, t+2^k).
Cycle Z is t=2^k (edges cancel). J is a Boolean of the causal window
[-2^k, 2^k] at time t. The same palindrome-constraint window graph that
reproves Cycle AB at distance 1 (every recurrent SCC has constant c)
has a mixing SCC at distances 2 and 4, so it does not prove that the
distance-2^k defect is not eventually 0.

Not a prize claim: I_k and infinitely many 00s remain open.

Run: python3 research/cycle_ai.py --certify
Dump: research/cycle_ai.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
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


def spatial(row: int, t: int, j: int) -> int:
    if abs(j) > t:
        return 0
    bit = j + t
    if bit < 0:
        return 0
    return (row >> bit) & 1


def and_remainder(rows: list[int], t0: int, t1: int, target_t: int) -> int:
    acc = 0
    for s in range(t0, t1):
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


def evolve_window(bits: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        step_cell(bits[i - 1], bits[i], bits[i + 1])
        for i in range(1, len(bits) - 1)
    )


def kosaraju(nodes, edges):
    adj = defaultdict(set)
    radj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        radj[b].add(a)
    seen = set()
    order = []

    def dfs(u):
        seen.add(u)
        stack = [u]
        it = {u: iter(adj[u])}
        while stack:
            x = stack[-1]
            nxt = next(it[x], None)
            if nxt is None:
                order.append(stack.pop())
                continue
            if nxt not in seen:
                seen.add(nxt)
                it[nxt] = iter(adj[nxt])
                stack.append(nxt)

    for u in nodes:
        if u not in seen:
            dfs(u)
    seen.clear()
    comps = []

    def rdfs(u, acc):
        seen.add(u)
        stack = [u]
        it = {u: iter(radj[u])}
        acc.append(u)
        while stack:
            x = stack[-1]
            nxt = next(it[x], None)
            if nxt is None:
                stack.pop()
                continue
            if nxt not in seen:
                seen.add(nxt)
                it[nxt] = iter(radj[nxt])
                stack.append(nxt)
                acc.append(nxt)

    for u in reversed(order):
        if u not in seen:
            acc = []
            rdfs(u, acc)
            comps.append(acc)
    return comps, adj


def palindrome_graph(k: int, extra: int = 1) -> dict:
    d = 1 << k
    rad = d + extra
    L = 2 * rad + 1
    center = rad
    nodes = []
    for mask in range(1 << L):
        bits = tuple((mask >> i) & 1 for i in range(L))
        if bits[center - d] == bits[center + d]:
            nodes.append(bits)
    edges = []
    for bits in nodes:
        for left_ext in (0, 1):
            for right_ext in (0, 1):
                nxt = evolve_window((left_ext,) + bits + (right_ext,))
                if nxt[center - d] == nxt[center + d]:
                    edges.append((bits, nxt))
    comps, adj = kosaraju(nodes, edges)
    rec = []
    for comp in comps:
        S = set(comp)
        if len(S) > 1:
            recurrent = any(v in S for u in S for v in adj[u])
        else:
            u = comp[0]
            recurrent = u in adj[u]
        if recurrent:
            cs = {bits[center] for bits in comp}
            rec.append({"n": len(comp), "c_vals": sorted(cs), "constant_c": len(cs) == 1})
    return {
        "k": k,
        "d": d,
        "L": L,
        "n_nodes": len(nodes),
        "n_edges": len(edges),
        "n_rec": len(rec),
        "all_rec_constant_c": all(s["constant_c"] for s in rec) if rec else True,
        "some_rec_both_c": any(s["c_vals"] == [0, 1] for s in rec),
        "rec": rec,
    }


def dyadic_identity(rows: list[int], kmax: int, tmax: int) -> dict:
    fail = 0
    n = 0
    zfail = 0
    k0_cr_fail = 0
    for k in range(0, kmax + 1):
        step = 1 << k
        for t in range(0, tmax):
            if t + step >= len(rows):
                break
            ct = spatial(rows[t], t, 0)
            c2 = spatial(rows[t + step], t + step, 0)
            xm = spatial(rows[t], t, -step)
            xp = spatial(rows[t], t, step)
            J = and_remainder(rows, t, t + step, t + step)
            n += 1
            if (ct ^ xm ^ xp ^ J) != c2:
                fail += 1
            if k == 0:
                cr = spatial(rows[t], t, 0) & spatial(rows[t], t, 1)
                if J != cr:
                    k0_cr_fail += 1
        tZ = 1 << k
        if tZ + tZ < len(rows):
            ct = spatial(rows[tZ], tZ, 0)
            c2 = spatial(rows[tZ + tZ], tZ + tZ, 0)
            xm = spatial(rows[tZ], tZ, -tZ)
            xp = spatial(rows[tZ], tZ, tZ)
            J = and_remainder(rows, tZ, tZ + tZ, tZ + tZ)
            if xm != 1 or xp != 1 or (ct ^ J) != c2:
                zfail += 1
    return {
        "fail": fail,
        "n": n,
        "Z_fail": zfail,
        "k0_J_eq_c_and_r_fail": k0_cr_fail,
    }


def window_locality(rows: list[int], k: int, tmax: int) -> dict:
    step = 1 << k
    windows: dict[tuple[int, ...], set[int]] = {}
    for t in range(step, tmax):
        bits = tuple(spatial(rows[t], t, j) for j in range(-step, step + 1))
        ct = spatial(rows[t], t, 0)
        c2 = spatial(rows[t + step], t + step, 0)
        xm = spatial(rows[t], t, -step)
        xp = spatial(rows[t], t, step)
        J = ct ^ xm ^ xp ^ c2
        windows.setdefault(bits, set()).add(J)
    ambig = sum(1 for js in windows.values() if len(js) > 1)
    return {"k": k, "n_windows": len(windows), "ambig": ambig}


def shift_00(rows: list[int], tmax: int) -> dict:
    zeros = [
        t
        for t in range(0, tmax)
        if spatial(rows[t], t, 0) == 0 and spatial(rows[t + 1], t + 1, 0) == 0
    ]
    hits = {}
    for k in range(0, 6):
        step = 1 << k
        hit = 0
        for t in zeros:
            tt = t + step
            if tt + 1 < len(rows) and spatial(rows[tt], tt, 0) == 0 and spatial(
                rows[tt + 1], tt + 1, 0
            ) == 0:
                hit += 1
        hits[str(k)] = {"hit": hit, "n00": len(zeros)}
    return hits


def self_checks(c20, ident: dict, loc: list, g0: dict, g1: dict, g2: dict) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert ident["fail"] == 0
    assert ident["Z_fail"] == 0
    assert ident["k0_J_eq_c_and_r_fail"] == 0
    for w in loc:
        assert w["ambig"] == 0
    assert g0["all_rec_constant_c"]
    assert not g0["some_rec_both_c"]
    assert g1["some_rec_both_c"]
    assert g2["some_rec_both_c"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    rows = evolve_rows(320)
    ident = dyadic_identity(rows, kmax=6, tmax=120)
    loc = [
        window_locality(rows, 1, 200),
        window_locality(rows, 2, 180),
        window_locality(rows, 3, 160),
    ]
    g0 = palindrome_graph(0)
    g1 = palindrome_graph(1)
    g2 = palindrome_graph(2)
    sh = shift_00(rows, 250)
    checks = self_checks(c20, ident, loc, g0, g1, g2)
    dump = {
        "cycle": "AI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "identity": ident,
        "window_locality": loc,
        "palindrome_k0": {
            "all_rec_constant_c": g0["all_rec_constant_c"],
            "n_rec": g0["n_rec"],
            "rec": g0["rec"],
        },
        "palindrome_k1": {
            "some_rec_both_c": g1["some_rec_both_c"],
            "n_rec": g1["n_rec"],
            "rec": g1["rec"],
        },
        "palindrome_k2": {
            "some_rec_both_c": g2["some_rec_both_c"],
            "n_rec": g2["n_rec"],
            "largest_rec": max(s["n"] for s in g2["rec"]),
        },
        "shift_00": sh,
        "lemmas": {
            "dyadic_step": True,
            "J_causal_window": True,
            "k0_palindrome_constant_c": True,
            "I_k_not_eventually_0": None,
            "prize": False,
        },
        "verdict": {
            "dyadic_step": "LEMMA",
            "J_causal_window": "LEMMA",
            "k0_palindrome_graph": "LEMMA",
            "k_ge_1_palindrome_graph": "KILLED",
            "shift_00_production": "KILLED",
            "I_k_eventually_0": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"], "ident_n", ident["n"], "fail", ident["fail"])


if __name__ == "__main__":
    main()
