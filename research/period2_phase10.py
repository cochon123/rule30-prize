#!/usr/bin/env python3
"""Phase 10 even-right u lives in the SFT forbidding {00, 111}.

Under c_{2n}=1, c_{2n+1}=0, the two-step map on column 1 sends u=0 to
u'=1 independently of columns 2..5, and sends u=1 to u'=NOT(e OR f).
A 1-run of length 3 is impossible: the only 1→1 transition has (e,f)=(0,0)
and forces e'=1, so the next bit is 0. The SFT forbidding {00, 111} has
positive entropy (growth λ^3=λ+1), so aperiodic u exists. Not a prize
claim: finite seeds reduce to phase 01 by one Rule 30 step, and that
phase still has the ugap L_0 obstruction.

Run: python3 research/period2_phase10.py --certify
Dump: research/period2_phase10.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import forced_right_traces

OUT = Path(__file__).resolve().with_suffix(".json")


def two_step_10(bits):
    """Even C=1, odd C=0, next even C=1."""
    row = 0
    for i, b in enumerate(bits):
        if b:
            row |= 1 << i
    nxt = (row << 1) ^ (row | (row >> 1))
    nxt &= ~1
    nxt2 = (nxt << 1) ^ (nxt | (nxt >> 1))
    nxt2 = (nxt2 & ~1) | 1
    return [(nxt2 >> i) & 1 for i in range(len(bits) + 2)]


def transition_table(extra: int = 4):
    """Map (u, e, f, extra...) -> (u', e', f') with C=1 at even time."""
    rows = []
    for bits in product([0, 1], repeat=3 + extra):
        u, e, f = bits[0], bits[1], bits[2]
        body = [1, u, e, f, *bits[3:], 0, 0]
        nxt = two_step_10(body)
        rows.append(
            {
                "u": u,
                "ef": [e, f],
                "extra": list(bits[3:]),
                "u_next": nxt[1],
                "ef_next": [nxt[2], nxt[3]],
            }
        )
    return rows


def certify_sft(rows):
    """u' depends only on (u,e,f); 0→1; 1→1 iff e=f=0."""
    by_uef = defaultdict(set)
    n0_to_1 = n1_to_1 = n1_to_0 = 0
    for r in rows:
        key = (r["u"], tuple(r["ef"]))
        by_uef[key].add(r["u_next"])
        if r["u"] == 0:
            assert r["u_next"] == 1
            n0_to_1 += 1
        elif r["ef"] == [0, 0]:
            assert r["u_next"] == 1
            n1_to_1 += 1
        else:
            assert r["u_next"] == 0
            n1_to_0 += 1
    for key, vals in by_uef.items():
        assert vals == {1} if key[0] == 0 or key[1] == (0, 0) else {0}
    assert n0_to_1 > 0 and n1_to_1 > 0 and n1_to_0 > 0
    return {
        "n_01": n0_to_1,
        "n_11": n1_to_1,
        "n_10": n1_to_0,
        "n_uef": len(by_uef),
    }


def max_one_run(rows):
    """Longest consecutive u=1 on the (u,e,f) graph."""
    succ = defaultdict(set)
    for r in rows:
        succ[(r["u"], tuple(r["ef"]))].add((r["u_next"], tuple(r["ef_next"])))
    best = 0
    best_path = []

    def dfs(state, run, path, seen):
        nonlocal best, best_path
        if run > best:
            best = run
            best_path = path[:]
        assert run <= 4
        for nxt in succ[state]:
            if nxt[0] == 1:
                assert nxt not in seen
                dfs(nxt, run + 1, path + [list(nxt[0:1] + nxt[1])], seen | {nxt})

    for s in succ:
        dfs(s, 1 if s[0] == 1 else 0, [list(s[0:1] + s[1])], {s} if s[0] == 1 else set())
    assert best == 2
    return {"max_one_run": best, "path": best_path}


def in_sft(u):
    prev = 1
    run1 = 0
    for b in u:
        if b == 0:
            if prev == 0:
                return False
            run1 = 0
        else:
            run1 += 1
            if run1 >= 3:
                return False
        prev = b
    return True


def scan_finite_rights(Wmax=8, T=240):
    """Every finite right of width <=Wmax has even-u in the {00,111}-SFT."""
    n = 0
    n_all1 = 0
    n_hit0 = 0
    max_ones = 0
    max_zeros = 0
    for W in range(0, Wmax + 1):
        for mask in range(1 << W) if W else [0]:
            if W and mask == 0:
                continue
            right = [(mask >> j) & 1 for j in range(W)]
            c, r, e, f = forced_right_traces(right, 1, T)
            assert all(c[t] == ((t + 1) & 1) for t in range(T + 1))
            u = [r[2 * k] for k in range(T // 2 + 1) if 2 * k <= T]
            assert in_sft(u), (W, mask, "".join(map(str, u[:40])))
            n += 1
            if all(u):
                n_all1 += 1
            if 0 in u:
                n_hit0 += 1
            run1 = run0 = 0
            for b in u:
                if b:
                    run1 += 1
                    run0 = 0
                    if run1 > max_ones:
                        max_ones = run1
                else:
                    run0 += 1
                    run1 = 0
                    if run0 > max_zeros:
                        max_zeros = run0
    assert max_ones <= 2 and max_zeros <= 1
    return {
        "Wmax": Wmax,
        "T": T,
        "n": n,
        "n_all1": n_all1,
        "n_hit0": n_hit0,
        "max_one_run": max_ones,
        "max_zero_run": max_zeros,
    }


def left_even_is_one(W=6, T=80):
    """On phase 10, reconstructed even-time left neighbor is identically 1."""
    n = 0
    for mask in range(1 << W):
        right = [(mask >> j) & 1 for j in range(W)]
        c, r, _, _ = forced_right_traces(right, 1, T)
        for t in range(0, T, 2):
            if t + 1 > T:
                break
            l = c[t + 1] ^ (c[t] | r[t])
            assert l == 1, (mask, t, l, c[t], c[t + 1], r[t])
            n += 1
    return {"W": W, "T": T, "n_even": n}


def certify():
    rows4 = transition_table(4)
    rows6 = transition_table(6)
    sft4 = certify_sft(rows4)
    sft6 = certify_sft(rows6)
    run4 = max_one_run(rows4)
    scan = scan_finite_rights(8, 240)
    left = left_even_is_one(6, 80)
    return {
        "sft_extra4": sft4,
        "sft_extra6": sft6,
        "one_run": run4,
        "finite_rights": scan,
        "left_even": left,
        "forbidden": ["00", "111"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("sft extra4", report["sft_extra4"])
    print("sft extra6", report["sft_extra6"])
    print("one run", report["one_run"])
    print("finite rights", report["finite_rights"])
    print("left even", report["left_even"])
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
