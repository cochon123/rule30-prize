#!/usr/bin/env python3
"""Cycle V: prize even-right vs X, even-decimation chain, F^p Kopra width.

Attacks that could finish Problem 1. None is a prize claim unless a named
lemma excludes every eventual period (or at least period 2 for this seed,
with a uniform argument).

1. Prize-seed even right neighbor u_n = x(2n,1) versus the SFT X that
   forbids {11, 00000}. A period-2 phase-01 onset requires a suffix of u
   in X. Kill a 'never in X' lemma if a long legal window exists; survive
   only if some uniform forbidden factor (e.g. 11) occurs with a CA proof.

2. Even-decimation chain v_k[n] = c_{n 2^k}. Sibling splitting is not
   enough (Thue–Morse). Distinctness of the chain {v_k} would give an
   infinite 2-kernel. Kill if a collision v_k = v_{k+m} appears, or if no
   closed witness index for v_k vs v_{k+1} exists (n_* already in {1,2,3}
   empirically). Survive only with a proof for every k, m > 0.

3. Kopra width of F^p: (m,n) left-permutivity of the p-step centre.
   Width 1 needs m+n = 1. Kill if every p>=1 has m>=1 and n>=1.

4. Longest right-special factor and last lag-p disagreement: finite T+p
   bounds only. Record them; do not treat a larger bound as a proof.

Run: python3 research/cycle_v.py --certify
Dump: research/cycle_v.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def packed_traces(count: int):
    """Centre, right neighbor, and +2 column. Bit k of the packed row is x(t, k-t)."""
    row = 1
    c = bytearray(count)
    r = bytearray(count)
    e = bytearray(count)
    for t in range(count):
        c[t] = (row >> t) & 1
        r[t] = (row >> (t + 1)) & 1
        e[t] = (row >> (t + 2)) & 1
        row = rule30_step(row)
    return c, r, e


def packed_center_bits(count: int) -> bytearray:
    c, _, _ = packed_traces(count)
    return c


def in_X_word(bits) -> bool:
    """Language of the period-2 even-right SFT: no 11, no five zeros."""
    prev = 0
    zeros = 0
    for b in bits:
        if b:
            if prev:
                return False
            zeros = 0
        else:
            zeros += 1
            if zeros >= 5:
                return False
        prev = b
    return True


def factor_in_X_stats(u, window: int) -> dict:
    n = len(u)
    n_legal = 0
    first = None
    last = None
    if n < window:
        return {"window": window, "n_windows": 0, "n_legal": 0}
    for i in range(n - window + 1):
        if in_X_word(u[i : i + window]):
            n_legal += 1
            if first is None:
                first = i
            last = i
    return {
        "window": window,
        "n_windows": n - window + 1,
        "n_legal": n_legal,
        "first_legal": first,
        "last_legal": last,
        "frac": n_legal / (n - window + 1),
    }


def run_and_factor_stats(seq) -> dict:
    n11 = 0
    n00000 = 0
    last11 = -1
    last5 = -1
    max11_gap = 0
    prev11 = -10**9
    zeros = 0
    prev = 0
    for i, b in enumerate(seq):
        if b:
            if prev:
                n11 += 1
                last11 = i - 1
                gap = (i - 1) - prev11
                if prev11 >= 0:
                    max11_gap = max(max11_gap, gap)
                prev11 = i - 1
            zeros = 0
        else:
            zeros += 1
            if zeros >= 5:
                n00000 += 1
                last5 = i - 4
        prev = b
    if prev11 >= 0:
        max11_gap = max(max11_gap, len(seq) - 1 - prev11)
    return {
        "len": len(seq),
        "n11": n11,
        "n00000": n00000,
        "last11": last11,
        "last00000": last5,
        "max11_gap": max11_gap,
        "density1": sum(seq) / len(seq) if seq else 0.0,
    }


def prize_u_vs_X(c, r, e) -> dict:
    N = len(c)
    u = bytearray(r[0:N:2])
    eu = bytearray(e[0:N:2])
    # phase-01 drain check: u'=1 iff (u,e,f)=(0,0,0) needs f; skip f.
    # We only need u vs X and whether a long centre-01 suffix exists.
    u_stats = run_and_factor_stats(u)
    windows = [factor_in_X_stats(u, w) for w in (8, 16, 32, 64)]
    last01 = last_phase_break(c, 0)
    last10 = last_phase_break(c, 1)
    # Suffix of u from each even time: is the remaining word in X?
    # Too long to test every suffix fully; test suffixes of length 64
    # starting at every index (already in windows) and the true suffixes
    # of length 8,16,32,64 from the end.
    end_suffix = {}
    for w in (8, 16, 32, 64, 128):
        if len(u) >= w:
            end_suffix[str(w)] = in_X_word(u[-w:])
    return {
        "n_even": len(u),
        "u_stats": u_stats,
        "windows": windows,
        "end_suffix_in_X": end_suffix,
        "last_phase01_break": last01,
        "last_phase10_break": last10,
        "N": N,
        # A 'never-in-X' lemma dies if any length-8 window is legal.
        "any_len8_in_X": windows[0]["n_legal"] > 0,
        "eu_density": (sum(eu) / len(eu)) if eu else 0.0,
    }


def last_phase_break(c, even_bit: int) -> int:
    last = -1
    for t, b in enumerate(c):
        expect = even_bit if (t % 2 == 0) else 1 - even_bit
        if b != expect:
            last = t
    return last


def even_decimation_chain(c, kmax: int = 16) -> dict:
    N = len(c)
    bpow = []
    k = 0
    while (1 << k) < N:
        bpow.append(int(c[1 << k]))
        k += 1
    rows = []
    collision = None
    nstar_vals = []
    for k in range(min(kmax, len(bpow) - 1)):
        nmax = N >> (k + 1)
        nstar = None
        nstar2 = None
        for n in range(1, nmax):
            ck = c[n << k]
            ck1 = c[n << (k + 1)]
            if nstar is None and ck != ck1:
                nstar = n
            if k + 2 <= len(bpow) and nstar2 is None:
                if n < (N >> (k + 2)) and ck != c[n << (k + 2)]:
                    nstar2 = n
            if nstar is not None and nstar2 is not None:
                break
        nstar_vals.append(nstar)
        rec = {
            "k": k,
            "nstar_vs_k+1": nstar,
            "nstar_vs_k+2": nstar2,
            "c_2k": int(c[1 << k]) if (1 << k) < N else None,
            "c_2k1": int(c[1 << (k + 1)]) if (1 << (k + 1)) < N else None,
        }
        rows.append(rec)
        if nstar is None:
            collision = {"kind": "v_k=v_{k+1}", "k": k}
    # Closed witness in {1,2,3}?
    closed = all(s in (1, 2, 3) for s in nstar_vals if s is not None)
    failed_123 = [i for i, s in enumerate(nstar_vals) if s not in (1, 2, 3)]
    return {
        "c_pow2": bpow,
        "rows": rows,
        "nstar_list": nstar_vals,
        "witness_in_1_2_3": closed and not failed_123,
        "failed_123_k": failed_123,
        "collision": collision,
        "chain_distinct_on_prefix": collision is None,
    }


def centre_after_p(cells, p: int) -> int:
    cur = list(cells)
    origin = p
    for _ in range(p):
        n = len(cur)
        nxt = [0] * n
        for i in range(n):
            L = cur[i - 1] if i else 0
            C = cur[i]
            R = cur[i + 1] if i + 1 < n else 0
            nxt[i] = L ^ (C | R)
        cur = nxt
    return cur[origin]


def fp_edge_witness(p: int) -> dict:
    """Single-1 light-cone edges: vacuum stays 0; a 1 at ±p is a shifted prize seed.

    x(p,0) for a 1 at +p equals the prize left edge x(p,-p)=1.
    x(p,0) for a 1 at -p equals the prize right edge x(p, p)=1.
    Hence the p-step centre depends on both x_{-p} and x_p, so m=n=p
    and Kopra width m+n=2p>=2.
    """
    width = 2 * p + 1
    vac = [0] * width
    left = [0] * width
    right = [0] * width
    left[0] = 1  # x_{-p}
    right[2 * p] = 1  # x_p
    assert centre_after_p(vac, p) == 0
    cl = centre_after_p(left, p)
    cr = centre_after_p(right, p)
    assert cl == 1, (p, cl)
    assert cr == 1, (p, cr)
    return {"p": p, "m_ge": p, "n_ge": p, "w_ge": 2 * p, "width1": False}


def fp_kopra_width(p: int) -> dict:
    """Minimal memory m and anticipation n of the p-step centre map."""
    width = 2 * p + 1
    ncfg = 1 << width
    # Which sites affect the output?
    affects = []
    for j in range(width):
        hit = False
        for mask in range(ncfg):
            bits = [(mask >> i) & 1 for i in range(width)]
            a = centre_after_p(bits, p)
            bits[j] ^= 1
            b = centre_after_p(bits, p)
            if a != b:
                hit = True
                break
        affects.append(hit)
    idxs = [j for j, h in enumerate(affects) if h]
    origin = p
    m = origin - min(idxs) if idxs else 0
    n = max(idxs) - origin if idxs else 0
    # Permutive in the leftmost affecting cell?
    left = min(idxs) if idxs else origin
    permutive = True
    keep = 0
    # Check: for every assignment of the other cells, flipping left flips output.
    for mask in range(ncfg):
        bits = [(mask >> i) & 1 for i in range(width)]
        bits2 = list(bits)
        bits2[left] ^= 1
        if centre_after_p(bits, p) == centre_after_p(bits2, p):
            permutive = False
            keep += 1
            if keep > 8:
                break
    return {
        "p": p,
        "affects": affects,
        "m": m,
        "n": n,
        "w": m + n,
        "left_permutive": permutive,
        "n_keep_sampled": keep,
        "width1": (m + n) == 1,
    }


def last_lag_disagreements(c, pmax: int) -> dict:
    """From the end: last i with c[i] != c[i+p]. Random-like => last ~ N-p."""
    N = len(c)
    pmax = min(pmax, N // 2)
    worst_last = N
    worst_p = 1
    near_end = 0
    for p in range(1, pmax + 1):
        last = -1
        lim = N - p
        # scan from the end
        for i in range(lim - 1, -1, -1):
            if c[i] != c[i + p]:
                last = i
                break
        if last < worst_last:
            worst_last = last
            worst_p = p
        if last >= N - p - 32:
            near_end += 1
    return {
        "pmax": pmax,
        "worst_last": worst_last,
        "worst_p": worst_p,
        "T_bound_if_period_p_in_range": worst_last + 1,
        "n_p_disagreement_within_32_of_end": near_end,
        "all_p_break_near_end": near_end == pmax,
    }


def has_right_special(c, L: int) -> bool:
    """Some length-L factor has both right extensions in this prefix."""
    N = len(c)
    if L <= 0 or N <= L + 1:
        return False
    if L <= 60:
        have0 = set()
        have1 = set()
        w = 0
        mask = (1 << L) - 1
        for i in range(L):
            w = (w << 1) | c[i]
        for j in range(0, N - L):
            nxt = c[j + L]
            if nxt:
                have1.add(w)
                if w in have0:
                    return True
            else:
                have0.add(w)
                if w in have1:
                    return True
            if j + L < N:
                w = ((w << 1) | c[j + L]) & mask
        return False
    # rolling Python int hash of the window
    seen = {}
    w = 0
    for i in range(L):
        w = (w << 1) | c[i]
    for j in range(0, N - L):
        nxt = c[j + L]
        prev = seen.get(w)
        if prev is None:
            seen[w] = nxt
        elif prev != nxt:
            return True
        if j + L < N:
            w = (w << 1) | c[j + L]
            # drop bit L+1 from the left: w now has L+1 bits
            w &= (1 << L) - 1
    return False


def longest_right_special(c, hi: int = 512) -> dict:
    lo = 1
    hi = min(hi, len(c) - 2)
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if has_right_special(c, mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return {"longest_right_special": best, "T_p_gt": best}


def self_checks(c20, r20):
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    # x(0,1)=0; at t=1 row=111, x(1,1)=1
    assert r20[0] == 0 and r20[1] == 1
    # F^1 is (1,1) left permutive, width 2
    w1 = fp_kopra_width(1)
    assert w1["m"] == 1 and w1["n"] == 1 and w1["left_permutive"]
    for p in range(1, 9):
        fp_edge_witness(p)
    # SFT X: 010010 is legal; 11 and 00000 are not
    assert in_X_word([0, 1, 0, 0, 1, 0])
    assert not in_X_word([1, 1])
    assert not in_X_word([0, 0, 0, 0, 0])
    return {"all_ok": True, "known20": True, "f1_width": 2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--bits", type=int, default=1 << 18)
    parser.add_argument("--pmax", type=int, default=0, help="0 means N//2")
    parser.add_argument("--fp-max", type=int, default=6, dest="fp_max")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20, r20, _ = packed_traces(20)
    checks = self_checks(c20, r20)
    c, r, e = packed_traces(args.bits)
    uX = prize_u_vs_X(c, r, e)
    chain = even_decimation_chain(c, kmax=16)
    fp = [fp_kopra_width(p) for p in range(1, args.fp_max + 1)]
    edge = [fp_edge_witness(p) for p in range(1, 33)]
    pmax = args.pmax if args.pmax > 0 else max(1, len(c) // 2)
    lags = last_lag_disagreements(c, pmax)
    spec = longest_right_special(c)
    any_width1 = any(row["width1"] for row in fp)
    dump = {
        "cycle": "V",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "prize_u_vs_X": uX,
        "even_chain": {
            "c_pow2": chain["c_pow2"],
            "nstar_list": chain["nstar_list"],
            "witness_in_1_2_3": chain["witness_in_1_2_3"],
            "failed_123_k": chain["failed_123_k"],
            "collision": chain["collision"],
            "chain_distinct_on_prefix": chain["chain_distinct_on_prefix"],
            "rows_head": chain["rows"][:8],
        },
        "fp_width": fp,
        "fp_edge_lemma": {
            "p_checked": 32,
            "all_m_n_eq_p": True,
            "width1_possible": False,
            "w_ge": [row["w_ge"] for row in edge],
        },
        "lag_disagreements": lags,
        "right_special": spec,
        "verdict": {
            "u_never_in_X": (not uX["any_len8_in_X"]),
            "period2_suffix": uX["last_phase01_break"] < args.bits - 64
            or uX["last_phase10_break"] < args.bits - 64,
            "even_chain_closed_witness": chain["witness_in_1_2_3"],
            "fp_width1": any_width1,
            "fp_edge_lemma": "m=n=p for p=1..32 (light-cone edges)",
            "longest_right_special": spec["longest_right_special"],
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("u_stats", uX["u_stats"])
    print("windows", [{k: w[k] for k in ("window", "n_legal", "frac", "first_legal", "last_legal")} for w in uX["windows"]])
    print("end_suffix_in_X", uX["end_suffix_in_X"])
    print("last_phase breaks", uX["last_phase01_break"], uX["last_phase10_break"])
    print("c_pow2", chain["c_pow2"])
    print("nstar", chain["nstar_list"])
    print("fp", [(row["p"], row["m"], row["n"], row["w"], row["left_permutive"]) for row in fp])
    print("lags", {k: lags[k] for k in lags})
    print("special", spec)
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
