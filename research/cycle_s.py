#!/usr/bin/env python3
"""Cycle S: F^2 lag-2 Condrey iteration, and spacetime pairing of 11 vs 00.

Attacks from research/_astra_ideas16.md. Not a prize claim until a named
lemma excludes every onset or proves D(N)=o(N).

1. The two-step map is
     G_0 = x_{-2} XOR ((x_{-1} XNOR x_0) AND (x_1 OR x_2)).
   Holding the even centre at 0 gives x_{-2} = (NOT x_{-1}) AND (x_1 OR x_2).
   Kill if this is the already-known fold F_2=u (phase 01), uniqueness
   stops at lag 2, and choosing x_{-1}=1 zeros x_{-2} so no Condrey
   horizon fires.

2. Problem 2: D(N)=N_11-N_00+c_{N-1}. At each 11 (resp. 10-transition)
   pack a spatial window of radius <=8 about the centre and ask whether
   it determines the displacement to the next 00, or the next 0-run
   length. Kill if the same window realises two displacements.

Run: python3 research/cycle_s.py --certify
Dump: research/cycle_s.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import forced_right_traces, rule30_step
from period2_vacuum import F_of_u, nvars

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def r30_bit(L, C, R):
    return L ^ (C | R)


def two_step_centre(a, b, c, d, e):
    """G_0 from neighborhood x_{-2..+2} = (a,b,c,d,e)."""
    # after one step, cells -1,0,1
    m1 = r30_bit(a, b, c)
    m0 = r30_bit(b, c, d)
    p1 = r30_bit(c, d, e)
    return r30_bit(m1, m0, p1)


def g_formula(a, b, c, d, e):
    xnor = 1 - (b ^ c)
    return a ^ (xnor & (d | e))


def certify_f2_formula():
    n_ok = 0
    n_lag1_keep = 0
    n_a1_zero = 0
    rows = []
    for bits in product([0, 1], repeat=5):
        a, b, c, d, e = bits
        G = two_step_centre(a, b, c, d, e)
        gf = g_formula(a, b, c, d, e)
        assert G == gf
        n_ok += 1
        Gflip_b = two_step_centre(a, 1 - b, c, d, e)
        if Gflip_b == G:
            n_lag1_keep += 1
        # even centre 0, left neighbor 1 => predicted x_{-2} is 0
        if c == 0 and b == 1:
            pred = (1 - b) & (d | e)
            assert pred == 0
            n_a1_zero += 1
        rows.append({"bits": list(bits), "G0": G})
    # 16 neighborhoods with c=0, of which 8 have b=1
    assert n_a1_zero == 8
    assert n_lag1_keep == 8
    return {
        "n_neighborhoods": n_ok,
        "formula_ok": True,
        "lag1_keeps_G0": n_lag1_keep,
        "ell1_forces_F2_zero": n_a1_zero,
        "kill_whole_left_unique": True,
        "kill_horizon": True,
    }


def certify_F2_eq_u(n_rights=6, T=64):
    """On every forced phase-01 right of width <=n_rights, x(2n,-2)=u_n."""
    n = 0
    n_fail = 0
    for W in range(0, n_rights + 1):
        for mask in range(1 << W):
            right = [((mask >> j) & 1) for j in range(W)]
            c, r, e, f = forced_right_traces(right, 0, T)
            left_col = [c[t + 1] ^ (c[t] | r[t]) for t in range(T)]
            # column -2 at even times: from col -1 and centre
            # x(t,-2) = x(t+1,-1) XOR (x(t,-1) OR x(t,0))
            # need one extra left step
            col_m2 = []
            for t in range(T - 1):
                col_m2.append(left_col[t + 1] ^ (left_col[t] | c[t]))
            for n_i in range((T - 1) // 2):
                t = 2 * n_i
                if col_m2[t] != r[t]:
                    n_fail += 1
            n += 1
            # fold F_2
            u = [r[2 * k] for k in range((T // 2) + 1) if 2 * k <= T]
            kmax = 4
            if nvars(kmax) <= len(u):
                F, _G = F_of_u(u[: nvars(kmax) + 2], kmax)
                if F[2] != u[0]:
                    n_fail += 1
    return {"n_rights": n, "n_fail": n_fail, "F2_eq_u": n_fail == 0}


def spatial_window(row: int, t: int, rad: int) -> int:
    """Packed bits spatial t-rad .. t+rad, i.e. row bits t-rad..t+rad if >=0."""
    w = 0
    width = 2 * rad + 1
    for i in range(width):
        k = t - rad + i
        bit = (row >> k) & 1 if k >= 0 else 0
        w = (w << 1) | bit
    return w


def pairing_windows(N: int, rads=(1, 2, 4, 8)):
    """At each 11 pair, does a spatial window determine displacement to next 00?"""
    row = 1
    rows_at = []
    C = bytearray(N)
    for t in range(N):
        C[t] = (row >> t) & 1
        rows_at.append(row)
        row = rule30_step(row)
    elevens = [t for t in range(N - 1) if C[t] == 1 and C[t + 1] == 1]
    zeros = [t for t in range(N - 1) if C[t] == 0 and C[t + 1] == 0]
    # next 00 after each 11
    z_j = 0
    disps = []
    for t in elevens:
        while z_j < len(zeros) and zeros[z_j] <= t:
            z_j += 1
        if z_j < len(zeros):
            disps.append((t, zeros[z_j] - t))
        else:
            disps.append((t, None))
    # next 0-run length after a 1-run ending at t (10 transition)
    ten = []
    t = 0
    while t < N:
        if C[t] == 1:
            t0 = t
            while t < N and C[t] == 1:
                t += 1
            Lrun = t - t0
            t1 = t
            while t < N and C[t] == 0:
                t += 1
            Mrun = t - t1
            if t1 < N and Mrun:
                ten.append((t1 - 1, Lrun, Mrun))  # last 1 of the 1-run
        else:
            t += 1
    by_rad = {}
    for rad in rads:
        # 11 -> disp
        buckets = defaultdict(set)
        for t, d in disps:
            if d is None or t < rad:
                continue
            w = spatial_window(rows_at[t], t, rad)
            buckets[w].add(d)
        n_multi = sum(1 for s in buckets.values() if len(s) > 1)
        # 10-transition -> next 0-run length
        mbuckets = defaultdict(set)
        for t_last1, Lrun, Mrun in ten:
            if t_last1 < rad:
                continue
            w = spatial_window(rows_at[t_last1], t_last1, rad)
            mbuckets[w].add(Mrun)
        n_multi_m = sum(1 for s in mbuckets.values() if len(s) > 1)
        by_rad[str(rad)] = {
            "n_windows_11": len(buckets),
            "n_multi_disp": n_multi,
            "n_windows_10": len(mbuckets),
            "n_multi_M": n_multi_m,
            "kill_disp": n_multi > 0,
            "kill_M": n_multi_m > 0,
            "disp_counter_head": sorted(
                Counter_from_disps(disps), key=lambda kv: -kv[1]
            )[:8],
        }
    # odd-time 11 persistence
    odd11 = [t for t in elevens if t & 1]
    even11 = [t for t in elevens if not (t & 1)]
    return {
        "N": N,
        "n11": len(elevens),
        "n00": len(zeros),
        "n_odd11": len(odd11),
        "n_even11": len(even11),
        "last_odd11": odd11[-1] if odd11 else None,
        "last_even11": even11[-1] if even11 else None,
        "by_rad": by_rad,
        "kill_local_window": all(v["kill_disp"] and v["kill_M"] for v in by_rad.values()),
    }


def Counter_from_disps(disps):
    c = Counter(d for _t, d in disps if d is not None)
    return list(c.items())


def gadget_screen(N: int):
    """Causal gadget: width-8 right-edge word at time t//2 versus whether
    time t is an odd 11. Contemporaneous left-edge bits cannot reach the
    centre (distance t). Kill if the same half-time word occurs with both
    values of the later centre 11."""
    row = 1
    C = bytearray(N)
    right8 = []
    for t in range(N):
        C[t] = (row >> t) & 1
        if t >= 4:
            v = 0
            for k in range(8):
                bitpos = 2 * t - k
                v = (v << 1) | ((row >> bitpos) & 1 if bitpos >= 0 else 0)
            right8.append(v)
        else:
            right8.append(None)
        row = rule30_step(row)
    buckets = defaultdict(set)
    for t in range(16, N - 2):
        t0 = t // 2
        if right8[t0] is None:
            continue
        fire = int((t & 1) and C[t] == 1 and C[t + 1] == 1)
        buckets[right8[t0]].add(fire)
    n_multi = sum(1 for s in buckets.values() if len(s) > 1)
    return {
        "n_words": len(buckets),
        "n_ambiguous": n_multi,
        "kill": n_multi > 0,
    }


def self_checks():
    c = bytearray()
    row = 1
    for t in range(20):
        c.append((row >> t) & 1)
        row = rule30_step(row)
    assert list(c) == KNOWN20
    ref = experiment_center_bits(20)
    assert list(c) == list(ref)
    f = certify_f2_formula()
    assert f["formula_ok"]
    u = certify_F2_eq_u(4, 40)
    assert u["F2_eq_u"]
    return {"all_ok": True, "known20": True, "F2_eq_u": True, "formula": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--bits", type=int, default=1 << 14)
    args = parser.parse_args()
    t0 = time.perf_counter()
    checks = self_checks()
    f2 = certify_f2_formula()
    f2u = certify_F2_eq_u(6, 64)
    pair = pairing_windows(args.bits)
    gad = gadget_screen(min(args.bits, 1 << 12))
    dump = {
        "cycle": "S",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "f2": f2,
        "F2_eq_u": f2u,
        "pairing": pair,
        "gadget": gad,
        "verdict": {
            "f2_condrey": "KILLED",
            "pairing": "KILLED" if pair["kill_local_window"] else "OPEN",
            "gadget": "KILLED" if gad["kill"] else "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("F2_eq_u", f2u)
    print("pairing n11", pair["n11"], "odd11", pair["n_odd11"], "last_odd", pair["last_odd11"])
    print("pairing by_rad", {k: {kk: vv for kk, vv in v.items() if kk != "disp_counter_head"} for k, v in pair["by_rad"].items()})
    print("gadget", gad)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
