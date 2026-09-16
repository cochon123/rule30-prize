"""Cycle P: gap bound on the even right neighbor of a period-2 centre.

Under phase 01 (c_{2n}=0, c_{2n+1}=1), u_{n+1}=1 iff (u_n,e_n,f_n)=(0,0,0).
While u=0, the pair (e,f) is a 4-state graph whose longest path before
vacuum is 3 edges, so u has no 5 consecutive zeros. Independent of the
right half past column 3 (only g,h affect the 11-branch, and they cannot
create a loop). Together with no consecutive 1s, realizable and
unrealizable period-2 even-right sequences both live in the SFT
forbidding {11, 00000}.

This is not a prize claim: three of six T=20 last-sat L_0 models are
ugap-legal and still have R=16 (research/period2_ugap_sat.md).

Run: python3 research/period2_ugap.py --certify
Dump: research/period2_ugap.json
"""
from __future__ import annotations

import argparse
import json
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import forced_right_traces

OUT = Path(__file__).resolve().with_suffix(".json")


def two_step(bits):
    """Even then odd Rule 30 step, forcing centre 0 then 1 then 0."""
    row = 0
    for i, b in enumerate(bits):
        if b:
            row |= 1 << i
    nxt = (row << 1) ^ (row | (row >> 1))
    nxt = (nxt & ~1) | 1
    nxt2 = (nxt << 1) ^ (nxt | (nxt >> 1))
    nxt2 &= ~1
    return [(nxt2 >> i) & 1 for i in range(len(bits) + 2)]


def transition_table():
    """Complete map (e,f,g,h) -> (u', e', f') when u=c=0 at an even time."""
    rows = []
    for e, f, g, h in product([0, 1], repeat=4):
        bits = [0, 0, e, f, g, h, 0, 0]
        nxt = two_step(bits)
        rows.append(
            {
                "ef": (e, f),
                "gh": (g, h),
                "u_next": nxt[1],
                "ef_next": (nxt[2], nxt[3]),
            }
        )
    return rows


def certify_table(rows):
    """The four (e,f) cases, independent of extra right bits except 11."""
    by_ef = {}
    for r in rows:
        by_ef.setdefault(tuple(r["ef"]), []).append(r)
    # (0,0): always u'=1
    for r in by_ef[(0, 0)]:
        assert r["u_next"] == 1
    # (0,1): always u'=0 and (e',f')=(1,0)
    for r in by_ef[(0, 1)]:
        assert r["u_next"] == 0 and tuple(r["ef_next"]) == (1, 0)
    # (1,0): always u'=0 and (e',f')=(0,0)
    for r in by_ef[(1, 0)]:
        assert r["u_next"] == 0 and tuple(r["ef_next"]) == (0, 0)
    # (1,1): always u'=0; (e',f') is (0,0) iff g=h=0 else (0,1)
    for r in by_ef[(1, 1)]:
        assert r["u_next"] == 0
        g, h = r["gh"]
        if (g, h) == (0, 0):
            assert tuple(r["ef_next"]) == (0, 0)
        else:
            assert tuple(r["ef_next"]) == (0, 1)
    return True


def longest_zero_path():
    """Directed graph on (e,f) while staying at u=0; max path length in states."""
    # stay-in-zero edges (may be nondeterministic at 11)
    succ = {
        (0, 1): {(1, 0)},
        (1, 0): {(0, 0)},
        (1, 1): {(0, 0), (0, 1)},
        (0, 0): set(),  # exit: next u is 1
    }
    best = 0
    best_path = []

    def dfs(state, path):
        nonlocal best, best_path
        if len(path) > best:
            best = len(path)
            best_path = path[:]
        for nxt in succ[state]:
            if nxt in path:
                raise AssertionError("loop in u=0 graph")
            dfs(nxt, path + [nxt])

    for s in succ:
        dfs(s, [s])
    # each state on the path is one even time with u=0
    assert best == 4
    assert best_path == [(1, 1), (0, 1), (1, 0), (0, 0)]
    return {"max_states": best, "path": [list(p) for p in best_path]}


def scan_finite_rights(Wmax=8, T=240):
    """Empirically every width-W right has u-zero-run <=4, and some hit 4."""
    mx = 0
    hits4 = 0
    n = 0
    for W in range(0, Wmax + 1):
        for mask in range(1 << W) if W else [0]:
            if W and mask == 0:
                continue
            right = [(mask >> j) & 1 for j in range(W)]
            c, r, e, f = forced_right_traces(right, 0, T)
            u = [r[2 * k] for k in range(T // 2 + 1) if 2 * k <= T]
            z = 0
            local = 0
            for b in u:
                if b == 0:
                    z += 1
                    if z > local:
                        local = z
                else:
                    z = 0
            n += 1
            if local > mx:
                mx = local
            if local >= 4:
                hits4 += 1
            assert local <= 4, (W, mask, local)
    return {"Wmax": Wmax, "T": T, "n": n, "max_zero_run": mx, "n_hit4": hits4}


def g_not_width1():
    """F^2 always flips G_0 when x_{-2} flips, but not when x_{-1} flips."""
    def G0(xs):
        # xs: dict
        def F(row):
            keys = list(row) or [0]
            mn, mx = min(keys) - 1, max(keys) + 1
            nxt = {}
            for j in range(mn, mx + 1):
                a, b, c = row.get(j - 1, 0), row.get(j, 0), row.get(j + 1, 0)
                v = a ^ (b | c)
                if v:
                    nxt[j] = 1
            return nxt

        return F(F(xs)).get(0, 0)

    flip2 = True
    n_same_m1 = 0
    for bits in product([0, 1], repeat=4):
        r0 = {-1: bits[0], 0: bits[1], 1: bits[2], 2: bits[3]}
        r1 = {-2: 1, **r0}
        if G0(r0) == G0(r1):
            flip2 = False
        s0 = {-2: bits[0], 0: bits[1], 1: bits[2], 2: bits[3]}
        s1 = {-1: 1, **s0}
        if G0(s0) == G0(s1):
            n_same_m1 += 1
    assert flip2
    assert n_same_m1 == 4
    return {"lag2_permutive": True, "x_minus1_unseen": n_same_m1}


def certify():
    rows = transition_table()
    assert len(rows) == 16
    certify_table(rows)
    path = longest_zero_path()
    scan = scan_finite_rights(8, 240)
    ginfo = g_not_width1()
    return {
        "table": rows,
        "drain": path,
        "finite_rights": scan,
        "F2_width": ginfo,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    report = certify()
    print("drain path", report["drain"])
    print("finite rights", report["finite_rights"])
    print("F2", report["F2_width"])
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
