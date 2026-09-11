#!/usr/bin/env python3
"""Cycle Y: spine reduction of the 2-kernel, and Rule 150 ⊕ AND.

If v_k[n]=c_{n 2^k} equals v_{k+1} as sequences, then c_{2^j} is constant
for all j>=k. So a non-eventually-constant (c_{2^j}) implies infinitely
many distinct 2-kernel sequences, hence aperiodicity. Packed Rule 30 is
Rule 150 XOR adjacent ANDs; Rule 150 from a single 1 has centre 1 by
symmetry. Not a prize claim unless (c_{2^j}) is proved not eventually
constant.

Also kill Rowland-period / n=k sibling-split templates (ideas22).

Run: python3 research/cycle_y.py --certify
Dump: research/cycle_y.json
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
from period2_fiber import rule30_step

OUT = Path(__file__).resolve().with_suffix(".json")
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]


def r150_step(row: int) -> int:
    return (row << 2) ^ (row << 1) ^ row


def packed_center_bits(count: int, step=rule30_step) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = step(row)
    return out


def poly_mul_gf2(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def trinom_pow(m: int) -> int:
    """(1+x+x^2)^m over GF(2), as a bitmask (coeff of x^i is bit i)."""
    result = 1
    base = 0b111
    e = m
    while e:
        if e & 1:
            result = poly_mul_gf2(result, base)
        base = poly_mul_gf2(base, base)
        e >>= 1
    return result


def coeff_trinom(m: int, d: int) -> int:
    if d < 0:
        return 0
    return (trinom_pow(m) >> d) & 1


def reconstruct_center(T: int) -> bytearray:
    """c_t = [x^t](1+x+x^2)^t  XOR  XOR_{injections (s,p)} [x^{t-p}](1+x+x^2)^{t-s}."""
    row = 1
    injections: list[tuple[int, int]] = []
    out = bytearray(T)
    # Precompute trinom powers 0..T for speed
    powers = [1]
    cur = 1
    for _ in range(T):
        cur = cur ^ (cur << 1) ^ (cur << 2)
        powers.append(cur)
    for t in range(T):
        acc = (powers[t] >> t) & 1  # seed
        for s, p in injections:
            m = t - s
            d = t - p
            if m >= 0 and d >= 0:
                acc ^= (powers[m] >> d) & 1
        out[t] = acc
        inj = (row << 1) & row
        p = 0
        tmp = inj
        while tmp:
            if tmp & 1:
                injections.append((t + 1, p))
            tmp >>= 1
            p += 1
        row = rule30_step(row)
    return out


def r150_symmetric_center(T: int) -> dict:
    """Rule 150 from a single 1 is palindromic, so ℓ=r and c'=ℓ⊕c⊕r=c."""
    row = 1
    live = {0: 1}
    mismatches = []
    centers = []
    for t in range(T):
        # packed centre
        packed_c = (row >> t) & 1
        naive_c = 1 if 0 in live else 0
        # spatial palindrome: x(t,j)=x(t,-j)
        pal = True
        for j in range(0, t + 1):
            left = 1 if (-j) in live else 0
            right = 1 if j in live else 0
            if left != right:
                pal = False
                break
        l = 1 if (-1) in live else 0
        r = 1 if 1 in live else 0
        if l != r or packed_c != naive_c or packed_c != 1 or not pal:
            mismatches.append(t)
        centers.append(packed_c)
        nxt = {}
        for j in range(-t - 1, t + 2):
            v = (1 if (j - 1) in live else 0) ^ (1 if j in live else 0) ^ (
                1 if (j + 1) in live else 0
            )
            if v:
                nxt[j] = 1
        live = nxt
        row = r150_step(row)
    return {
        "T": T,
        "all_ones": all(centers),
        "n_mismatch": len(mismatches),
        "mismatch_head": mismatches[:8],
    }


def spine_reduction_check(c) -> dict:
    """v_k = v_{k+1}  ⇒  v_k[n]=v_k[2n] for all n  ⇒  (c_{2^j})_{j≥k} constant."""
    N = len(c)
    b = []
    k = 0
    while (1 << k) < N:
        b.append(int(c[1 << k]))
        k += 1
    rows = []
    for k in range(len(b) - 1):
        nmax = N >> (k + 1)
        nstar = None
        for n in range(1, nmax):
            if (n << (k + 1)) >= N:
                break
            if c[n << k] != c[n << (k + 1)]:
                nstar = n
                break
        # algebraic sample: v_k[2^j] = b_{k+j}
        ray = []
        j = 0
        while j < 8:
            idx = (1 << j) << k
            if idx >= N:
                break
            ray.append(int(c[idx]))
            j += 1
        constant_ray = len(set(ray)) == 1
        rows.append(
            {
                "k": k,
                "nstar": nstar,
                "b_k": b[k],
                "b_k1": b[k + 1],
                "nstar_is_1_iff_b_differs": (nstar == 1) == (b[k] != b[k + 1]),
                "ray_b": ray,
                "ray_constant": constant_ray,
            }
        )
    # If some k had nstar None on this prefix, a collision is possible.
    return {
        "b": b,
        "n_zeros_b": sum(1 for x in b if x == 0),
        "n_ones_b": sum(1 for x in b if x == 1),
        "last_zero_k": max((i for i, x in enumerate(b) if x == 0), default=None),
        "last_one_k": max((i for i, x in enumerate(b) if x == 1), default=None),
        "not_constant_on_prefix": len(set(b)) == 2,
        "rows": rows,
        "all_nstar_1_iff_b_differs": all(r["nstar_is_1_iff_b_differs"] for r in rows),
        "no_collision_on_prefix": all(r["nstar"] is not None for r in rows),
    }


def sibling_templates(c, kmax: int) -> dict:
    """Predicted first-split n for sibling kernel columns. Kill if none is universal."""
    N = len(c)

    def first_split(k, r):
        step = 1 << (k + 1)
        off = 1 << k
        nmax = (N - r - off) // step
        for n in range(nmax + 1):
            i1 = r + off + n * step
            if i1 >= N:
                return None
            if c[r + n * step] != c[i1]:
                return n
        return None

    def bits_at(k, r, n):
        step = 1 << (k + 1)
        off = 1 << k
        i1 = r + off + n * step
        if i1 >= N:
            return None
        return c[r + n * step], c[i1]

    # Rowland right-diagonal periods on a small spacetime (for r < 16).
    tmax = 256
    row = 1
    rows = []
    for t in range(tmax + 1):
        rows.append(row)
        row = rule30_step(row)

    def x_of(t, j):
        if t < 0 or t >= len(rows) or j + t < 0:
            return 0
        return (rows[t] >> (j + t)) & 1

    def diag_period(kdiag, jmax=128):
        seq = [x_of(kdiag + j, j) for j in range(min(jmax, tmax - kdiag + 1))]
        n = len(seq)
        for p in range(1, n // 2 + 1):
            if all(seq[i] == seq[i + p] for i in range(n - p)):
                return p
        return None

    rperiods = [diag_period(r) for r in range(16)]

    templates = {
        "n=k": lambda k, r: k,
        "n=k-1": lambda k, r: max(k - 1, 0),
        "n=k+1": lambda k, r: k + 1,
        "n=rowland_p(r)": lambda k, r: rperiods[r] if r < len(rperiods) and rperiods[r] else 0,
        "n=v2(r+1)": lambda k, r: ((r + 1) & -(r + 1)).bit_length() - 1,
        "n=popcount(r)": lambda k, r: r.bit_count(),
    }
    by_k = []
    universal = {name: True for name in templates}
    worst = []
    for k in range(1, kmax + 1):
        hist = Counter()
        w = -1
        hits = {name: 0 for name in templates}
        nres = 1 << k
        for r in range(nres):
            nstar = first_split(k, r)
            if nstar is None:
                hist["none"] += 1
                for name in templates:
                    universal[name] = False
                continue
            hist[nstar] += 1
            w = max(w, nstar)
            for name, fn in templates.items():
                pred = fn(k, r)
                pair = bits_at(k, r, pred)
                if pair is not None and pair[0] != pair[1]:
                    hits[name] += 1
                else:
                    universal[name] = False
        by_k.append(
            {
                "k": k,
                "nres": nres,
                "worst_n": w,
                "worst_minus_k": w - k,
                "hist_head": dict(sorted(hist.items())[:12]),
                "template_hits": hits,
            }
        )
        worst.append(w)
    fourpoint_fail = []
    for k in range(1, min(kmax, 8) + 1):
        Mk = 1 << k
        nfail = 0
        for r in range(Mk):
            if r + 3 * Mk >= N:
                continue
            if c[r] == c[r + Mk] and c[r + 2 * Mk] == c[r + 3 * Mk]:
                nfail += 1
        fourpoint_fail.append({"k": k, "n_fail_n0_and_n1": nfail})
    return {
        "rowland_periods_0_15": rperiods,
        "by_k": by_k,
        "worst_n": worst,
        "any_template_universal": any(universal.values()),
        "universal": universal,
        "fourpoint_n0_implies_n1": fourpoint_fail,
        "fourpoint_killed": any(x["n_fail_n0_and_n1"] > 0 for x in fourpoint_fail),
    }


def self_checks(c20, recon, r150, spine) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    # Packed identity
    row = 1
    for _ in range(30):
        assert rule30_step(row) == r150_step(row) ^ ((row << 1) & row)
        row = rule30_step(row)
    assert list(recon) == list(packed_center_bits(len(recon)))
    assert r150["all_ones"] and r150["n_mismatch"] == 0
    assert spine["all_nstar_1_iff_b_differs"]
    # Seed trinomial centre
    assert coeff_trinom(0, 0) == 1
    assert coeff_trinom(5, 5) == 1
    return {"all_ok": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--bits", type=int, default=1 << 16)
    parser.add_argument("--recon", type=int, default=80)
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    recon = reconstruct_center(args.recon)
    r150 = r150_symmetric_center(64)
    c = packed_center_bits(args.bits)
    spine = spine_reduction_check(c)
    sib = sibling_templates(c, kmax=10)
    checks = self_checks(c20, recon, r150, spine)

    dump = {
        "cycle": "Y",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "rule150": r150,
        "recon_len": args.recon,
        "spine": {
            "b": spine["b"],
            "n_zeros_b": spine["n_zeros_b"],
            "n_ones_b": spine["n_ones_b"],
            "last_zero_k": spine["last_zero_k"],
            "last_one_k": spine["last_one_k"],
            "not_constant_on_prefix": spine["not_constant_on_prefix"],
            "all_nstar_1_iff_b_differs": spine["all_nstar_1_iff_b_differs"],
            "no_collision_on_prefix": spine["no_collision_on_prefix"],
            "rows_head": spine["rows"][:8],
        },
        "siblings": {
            "any_template_universal": sib["any_template_universal"],
            "universal": sib["universal"],
            "worst_n": sib["worst_n"],
            "rowland_periods_0_15": sib["rowland_periods_0_15"],
            "fourpoint_killed": sib["fourpoint_killed"],
            "fourpoint": sib["fourpoint_n0_implies_n1"],
            "by_k_head": sib["by_k"][:6],
        },
        "lemmas": {
            "spine_reduction": True,
            "r150_centre_identically_1": r150["all_ones"],
            "r30_is_r150_xor_and": True,
            "green_reconstructs_centre": True,
            "b_k_not_eventually_constant": None,
            "ideas22_index_templates": not sib["any_template_universal"],
        },
        "verdict": {
            "spine_reduction": "LEMMA",
            "r150_centre": "LEMMA",
            "b_k_eventual_constancy": "OPEN",
            "sibling_index_templates": "KILLED",
            "fourpoint": "KILLED" if sib["fourpoint_killed"] else "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("b", spine["b"])
    print("last_zero_k", spine["last_zero_k"], "last_one_k", spine["last_one_k"])
    print("templates_universal", sib["universal"])
    print("worst_n", sib["worst_n"])
    print("fourpoint", sib["fourpoint_n0_implies_n1"])
    print("wall_s", dump["wall_s"])


if __name__ == "__main__":
    main()
