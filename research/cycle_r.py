#!/usr/bin/env python3
"""Cycle R: 2-kernel disagreement, prize-seed left-edge fiber, D(N) pairs.

Attacks that could finish a prize problem. None is claimed until a named
lemma excludes every onset (Problem 1) or proves D(N)=o(N) (Problem 2).

1. Let v_k = (c_{2^k n})_{n>=0} and d(k) = min{n>=1: c_n != c_{n 2^k}}.
   If d is injective then the v_k are pairwise distinct, the 2-kernel is
   infinite, c is not 2-automatic, hence not eventually periodic.
   Kill if d is not injective and no simple closed form holds.

2. Prize row at time T: actual left edge x(T,-T)=1. If fiber_left of the
   actual right, with period-2 centre starting at c_T, predicts 0 at
   spatial -T for every T>=1, that obstructs every onset.
   Kill if the predicted edge is sometimes 1, or first disagreement
   is not at a fixed column.

3. Exact identity D(N) = (#11 pairs) - (#00 pairs) + c_{N-1}, so
   Problem 2 is signed cancellation of equal-bit pairs. Kill a local
   run-length pairing if adjacent 1-run and 0-run lengths are not
   equal on a positive-density set of exceptions.

Run: python3 research/cycle_r.py --certify
Dump: research/cycle_r.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from period2_fiber import fiber_left, rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")

KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
N_BITS = 1 << 18
K_MAX = 14  # nmax = N/2^k >= 16
T_FIBER_MAX = 192


def packed_center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = rule30_step(row)
    return out


def kernel_family(c: bytearray) -> dict:
    N = len(c)
    rows = []
    d_vals = []
    d_odd_vals = []
    d_pow_vals = []
    c_pow2 = [int(c[1 << k]) for k in range(0, (N.bit_length() - 1))]
    injective = True
    seen_d = {}
    for k in range(1, K_MAX + 1):
        nmax = N >> k
        d = None
        d_odd = None
        d_pow = None  # first n = 2^a
        for n in range(1, nmax):
            if c[n] != c[n << k]:
                if d is None:
                    d = n
                if d_odd is None and (n & 1):
                    d_odd = n
                if d_pow is None and (n & (n - 1)) == 0:
                    d_pow = n
                if d is not None and d_odd is not None and d_pow is not None:
                    break
        # first disagreement of v_k against v_{k+1} on the v_k index
        nmax2 = N >> (k + 1)
        d_adj = None
        for n in range(1, nmax2):
            if c[n << k] != c[n << (k + 1)]:
                d_adj = n
                break
        # sibling: (k,0) vs (k, 2^{k-1}) i.e. c_{2^k n} vs c_{2^k n + 2^{k-1}}
        d_sib = None
        half = 1 << (k - 1)
        nmax_s = (N - half) >> k
        for n in range(0, nmax_s):
            if c[(n << k)] != c[(n << k) + half]:
                d_sib = n
                break
        rec = {
            "k": k,
            "d": d,
            "d_odd": d_odd,
            "d_pow": d_pow,
            "d_adj": d_adj,
            "d_sib": d_sib,
            "c_2k": int(c[1 << k]) if (1 << k) < N else None,
            "c_2k_plus_1": int(c[(1 << k) + 1]) if (1 << k) + 1 < N else None,
        }
        rows.append(rec)
        d_vals.append(d)
        d_odd_vals.append(d_odd)
        d_pow_vals.append(d_pow)
        if d is None:
            injective = False
        elif d in seen_d:
            injective = False
        else:
            seen_d[d] = k

    def strictly_inc(vals):
        return all(
            a is not None and b is not None and b > a
            for a, b in zip(vals, vals[1:])
        )

    # closed-form screens
    forms = {}
    ks = list(range(1, K_MAX + 1))
    forms["d_eq_1"] = all(v == 1 for v in d_vals)
    forms["d_eq_k"] = all(v == k for v, k in zip(d_vals, ks))
    forms["d_eq_k_plus_1"] = all(v == k + 1 for v, k in zip(d_vals, ks))
    forms["d_eq_2k"] = all(v == 1 << k for v, k in zip(d_vals, ks))
    forms["d_eq_2k_minus_1"] = all(v == (1 << k) - 1 for v, k in zip(d_vals, ks))
    forms["d_odd_eq_1"] = all(v == 1 for v in d_odd_vals)
    forms["d_strictly_inc"] = strictly_inc(d_vals)
    forms["d_odd_strictly_inc"] = strictly_inc(d_odd_vals)
    forms["d_injective"] = injective and None not in d_vals

    # d(k)=1 iff c_{2^k}=0, since c_1=1. Record where that fails.
    fail_d_eq_1 = [k for k, v in zip(ks, d_vals) if v != 1]

    return {
        "N": N,
        "K_MAX": K_MAX,
        "c_pow2": c_pow2,
        "rows": rows,
        "d_vals": d_vals,
        "d_odd_vals": d_odd_vals,
        "d_pow_vals": d_pow_vals,
        "forms": forms,
        "fail_d_eq_1": fail_d_eq_1,
        "d_counter": dict(Counter(d_vals)),
        "kill_injective": not forms["d_injective"],
        "kill_closed_form": not any(
            forms[k]
            for k in (
                "d_eq_1",
                "d_eq_k",
                "d_eq_k_plus_1",
                "d_eq_2k",
                "d_eq_2k_minus_1",
                "d_odd_eq_1",
                "d_strictly_inc",
                "d_odd_strictly_inc",
            )
        ),
    }


def prize_row_at(T: int) -> int:
    row = 1
    for _ in range(T):
        row = rule30_step(row)
    return row


def prize_slice(T: int) -> dict:
    """Packed prize row at time T. Bit k = spatial k-T."""
    row = prize_row_at(T)
    centre = (row >> T) & 1
    left_edge = row & 1
    right_edge = (row >> (2 * T)) & 1
    right = [((row >> (T + 1 + j)) & 1) for j in range(T)]
    left = [((row >> (T - k)) & 1) for k in range(1, T + 1)]
    left_nb = (row >> (T - 1)) & 1 if T >= 1 else None
    right_nb = (row >> (T + 1)) & 1
    return {
        "row": row,
        "centre": centre,
        "left_edge": left_edge,
        "right_edge": right_edge,
        "right": right,
        "left": left,
        "left_nb": left_nb,
        "right_nb": right_nb,
    }


def seed_locked_fiber(Tmax: int) -> dict:
    rows = []
    n_edge_zero = 0
    n_edge_one = 0
    n_match = 0
    first_dis_counter = Counter()
    odd_left_zero = []
    even_left_not_flip = []
    for T in range(1, Tmax + 1):
        sl = prize_slice(T)
        assert sl["left_edge"] == 1, T
        fib = fiber_left(sl["right"], sl["centre"], T)
        pred = fib["left"]
        actual = sl["left"]
        assert len(pred) == T == len(actual)
        first = None
        for i, (a, p) in enumerate(zip(actual, pred)):
            if a != p:
                first = i  # 0-based; spatial -(i+1)
                break
        edge_pred = pred[-1]
        if edge_pred == 0:
            n_edge_zero += 1
        else:
            n_edge_one += 1
        if first is None:
            n_match += 1
        else:
            first_dis_counter[first] += 1
        # phase-01 local neighbor constraints on the actual row
        # odd T, phase 01 requires left_nb = 1
        if T & 1 and sl["left_nb"] == 0:
            odd_left_zero.append(T)
        # even T, phase 01 requires left_nb = NOT right_nb (if c_T=0)
        if (T & 1) == 0 and sl["centre"] == 0:
            if sl["left_nb"] == sl["right_nb"]:
                even_left_not_flip.append(T)
        rows.append(
            {
                "T": T,
                "c": sl["centre"],
                "left_nb": sl["left_nb"],
                "right_nb": sl["right_nb"],
                "edge_pred": edge_pred,
                "first_dis": first,
                "first_dis_spatial": None if first is None else -(first + 1),
                "n_left_ones_pred": sum(pred),
                "n_left_ones_act": sum(actual),
            }
        )
    # is first disagreement always at a fixed column?
    fixed_first = None
    if first_dis_counter:
        common, cnt = first_dis_counter.most_common(1)[0]
        if cnt == Tmax:
            fixed_first = common
    edge_always_zero = n_edge_one == 0 and n_edge_zero == Tmax
    return {
        "Tmax": Tmax,
        "n_edge_zero": n_edge_zero,
        "n_edge_one": n_edge_one,
        "n_match": n_match,
        "edge_always_zero": edge_always_zero,
        "fixed_first_dis": fixed_first,
        "first_dis_counter": {str(k): v for k, v in sorted(first_dis_counter.items())},
        "n_odd_left_zero": len(odd_left_zero),
        "odd_left_zero_head": odd_left_zero[:24],
        "n_even_left_not_flip": len(even_left_not_flip),
        "even_left_not_flip_head": even_left_not_flip[:24],
        "rows_head": rows[:40],
        "rows_tail": rows[-8:],
        "kill_edge": not edge_always_zero,
        "kill_fixed_dis": fixed_first is None,
    }


def column_minus_one(N: int) -> dict:
    """x(t,-1) = (row >> (t-1)) & 1 for t>=1. Infinitely many odd zeros
    would exclude eventual phase-01 (which forces odd-time left neighbor 1).
    Finite screen only."""
    row = 1
    odd_zeros = []
    even_zeros = []
    bits = []
    for t in range(N):
        if t >= 1:
            bit = (row >> (t - 1)) & 1
            bits.append(bit)
            if bit == 0:
                (odd_zeros if t & 1 else even_zeros).append(t)
        row = rule30_step(row)
    last_odd_zero = odd_zeros[-1] if odd_zeros else None
    last_even_zero = even_zeros[-1] if even_zeros else None
    # density of zeros on odd times
    n_odd = N // 2
    n_odd_zero = len(odd_zeros)
    return {
        "N": N,
        "n_odd_zero": n_odd_zero,
        "n_even_zero": len(even_zeros),
        "last_odd_zero": last_odd_zero,
        "last_even_zero": last_even_zero,
        "odd_zero_density": n_odd_zero / n_odd if n_odd else None,
        "odd_zeros_head": odd_zeros[:20],
        "odd_zeros_tail": odd_zeros[-10:],
        "prefix32": bits[:32],
        "kill_eventual_odd_one": last_odd_zero is not None
        and last_odd_zero < N // 2,  # looks eventually 1 on odds
    }


def min_L_and_square_columns(c: bytearray) -> dict:
    """Smallest L with 2^k distinct length-L kernel prefixes, and
    whether length 2^k prefixes of the 2^k residues are distinct.
    Distinct square columns for all k would prove |K|=∞."""
    N = len(c)
    rows = []
    for k in range(0, 10):
        R = 1 << k
        # min L
        Lmax = min(64, N // R) if R else 1
        minL = None
        for L in range(1, Lmax + 1):
            seen = set()
            ok = True
            for r in range(R):
                w = 0
                for i in range(L):
                    w = (w << 1) | c[r + i * R]
                if w in seen:
                    ok = False
                    break
                seen.add(w)
            if ok:
                minL = L
                break
        square_ok = None
        need = (R - 1) * R + (R - 1)
        if need < N:
            cols = set()
            for r in range(R):
                w = 0
                for i in range(R):
                    w = (w << 1) | c[r + i * R]
                cols.add(w)
            square_ok = len(cols) == R
        rows.append(
            {
                "k": k,
                "min_L": minL,
                "need_at_least": max(k, 1),
                "square_distinct": square_ok,
            }
        )
    supported = [r for r in rows if r["square_distinct"] is not None]
    return {
        "rows": rows,
        "square_distinct_through": max((r["k"] for r in supported), default=None)
        if supported and all(r["square_distinct"] for r in supported)
        else None,
        "all_supported_square_distinct": bool(supported)
        and all(r["square_distinct"] for r in supported),
        "kill_L_eq_k": any(
            r["min_L"] is not None and r["min_L"] != r["need_at_least"]
            for r in rows
            if r["k"] >= 1
        ),
    }


def pair_identity(c: bytearray) -> dict:
    """D(N) = n11 - n00 + c[N-1]. Adjacent 1-run / 0-run pairing."""
    N = len(c)
    n11 = n00 = 0
    last11 = last00 = last11_odd = None
    for t in range(N - 1):
        if c[t] == 1 and c[t + 1] == 1:
            n11 += 1
            last11 = t
            if t & 1:
                last11_odd = t
        elif c[t] == 0 and c[t + 1] == 0:
            n00 += 1
            last00 = t
    ones = sum(c)
    D = 2 * ones - N
    rhs = n11 - n00 + c[N - 1]
    runs = []
    cur, L = c[0], 1
    for t in range(1, N):
        if c[t] == cur:
            L += 1
        else:
            runs.append((cur, L))
            cur, L = c[t], 1
    runs.append((cur, L))
    pairs = []
    for i in range(len(runs) - 1):
        if runs[i][0] == 1 and runs[i + 1][0] == 0:
            pairs.append((runs[i][1], runs[i + 1][1]))
    n_eq = sum(1 for a, b in pairs if a == b)
    sum_diff = sum(a - b for a, b in pairs)
    return {
        "N": N,
        "D": D,
        "n11": n11,
        "n00": n00,
        "rhs": rhs,
        "identity_ok": D == rhs,
        "last11": last11,
        "last00": last00,
        "last11_odd": last11_odd,
        "n_run_pairs": len(pairs),
        "n_equal_len": n_eq,
        "frac_equal_len": round(n_eq / len(pairs), 6) if pairs else None,
        "sum_L_minus_M": sum_diff,
        "pair_counter_head": [[a, b, n] for (a, b), n in Counter(pairs).most_common(8)],
        "kill_local_pairing": n_eq < (len(pairs) * 3) // 4 if pairs else True,
    }


def self_checks() -> dict:
    c = packed_center_bits(256)
    ref = experiment_center_bits(256)
    assert list(c) == list(ref)
    assert list(c[:20]) == KNOWN20
    # packing identities
    row = 1
    for t in range(1, 64):
        row = rule30_step(row)
        assert (row & 1) == 1  # left edge
        assert ((row >> t) & 1) == c[t]
    # fiber of empty right / width-0
    sl = prize_slice(1)
    assert sl["left_edge"] == 1
    fib = fiber_left(sl["right"], sl["centre"], 1)
    assert len(fib["left"]) == 1
    # c_4 = c_8 = 1 (known kernel screen)
    assert c[4] == 1 and c[8] == 1
    pid = pair_identity(c)
    assert pid["identity_ok"]
    return {
        "all_ok": True,
        "known20": True,
        "left_edge_64": True,
        "c4_c8": True,
        "D_identity_256": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--n-bits", type=int, default=N_BITS)
    parser.add_argument("--t-fiber", type=int, default=T_FIBER_MAX)
    args = parser.parse_args()
    t0 = time.perf_counter()
    checks = self_checks()
    c = packed_center_bits(args.n_bits)
    ker = kernel_family(c)
    cols = min_L_and_square_columns(c)
    fib = seed_locked_fiber(args.t_fiber)
    col = column_minus_one(min(args.n_bits, 1 << 16))
    pairs = pair_identity(c)
    kernel_kill = ker["kill_injective"] and ker["kill_closed_form"]
    fiber_kill = fib["kill_edge"] and fib["kill_fixed_dis"]
    dump = {
        "cycle": "R",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "kernel": {
            k: ker[k]
            for k in (
                "N",
                "K_MAX",
                "c_pow2",
                "d_vals",
                "d_odd_vals",
                "d_pow_vals",
                "forms",
                "fail_d_eq_1",
                "d_counter",
                "kill_injective",
                "kill_closed_form",
                "rows",
            )
        },
        "kernel_columns": cols,
        "fiber": fib,
        "column_m1": col,
        "pairs": pairs,
        "verdict": {
            "kernel": "KILLED" if kernel_kill else "OPEN",
            "fiber": "KILLED" if fiber_kill else "OPEN",
            "column_m1": "KILLED_AS_LEMMA"
            if col["kill_eventual_odd_one"]
            else "FINITE_ZEROS_ONLY",
            "local_run_pairing": "KILLED" if pairs["kill_local_pairing"] else "OPEN",
            "D_identity": "OK" if pairs["identity_ok"] else "FAIL",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print(f"wrote {OUT}")
    print(json.dumps(dump["verdict"], indent=2))
    print("kernel.forms", json.dumps(ker["forms"]))
    print("kernel.d_vals", ker["d_vals"])
    print("kernel.c_pow2", ker["c_pow2"])
    print(
        "fiber",
        {
            k: fib[k]
            for k in (
                "Tmax",
                "n_edge_zero",
                "n_edge_one",
                "n_match",
                "edge_always_zero",
                "fixed_first_dis",
                "n_odd_left_zero",
                "kill_edge",
                "kill_fixed_dis",
            )
        },
    )
    print("column_m1 last_odd_zero", col["last_odd_zero"], "n", col["n_odd_zero"])
    print("kernel_columns", cols["rows"])
    print(
        "pairs D",
        pairs["D"],
        "n11",
        pairs["n11"],
        "n00",
        pairs["n00"],
        "eq_frac",
        pairs["frac_equal_len"],
        "id",
        pairs["identity_ok"],
    )
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
