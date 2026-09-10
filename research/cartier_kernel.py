#!/usr/bin/env python3
"""Cartier operators on the right-edge generating function (prize problem 1).

Does not claim a prize result. Derives/verifies the four bivariate Cartier
images of (1+z+zw+zw^2)U = 1 + z w^2 R, expands the first R-correlation
equation, and samples 2-kernel prefixes of the center. Witnesses are required
on Diag(W U); off-diagonal differences are reported only as negative controls.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict


# ---------------------------------------------------------------------------
# Packed Rule 30 in right-edge coordinates v(t,k)=x(t,t-k)
# ---------------------------------------------------------------------------

def center_bits(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def triangle(N: int) -> list[list[int]]:
    """v[t][k] for 0<=t<N, 0<=k<N, with v=0 for k<0."""
    v = [[0] * N for _ in range(N)]
    v[0][0] = 1
    for t in range(N - 1):
        for k in range(N):
            left1 = v[t][k - 1] if k >= 1 else 0
            left2 = v[t][k - 2] if k >= 2 else 0
            v[t + 1][k] = v[t][k] ^ (left1 | left2)
    return v


def gf2_poly_add(a: dict, b: dict) -> dict:
    out = dict(a)
    for key, val in b.items():
        out[key] = out.get(key, 0) ^ val
        if out[key] == 0:
            del out[key]
    return out


# ---------------------------------------------------------------------------
# Identity and Cartier images as truncated bivariate series over F2
# ---------------------------------------------------------------------------

def series_from_grid(grid: list[list[int]], N: int) -> dict:
    return {(t, k): 1 for t in range(N) for k in range(N) if grid[t][k]}


def mul_monomial(series: dict, dt: int, dk: int, N: int) -> dict:
    out = {}
    for (t, k), val in series.items():
        nt, nk = t + dt, k + dk
        if nt < N and nk < N:
            out[nt, nk] = out.get((nt, nk), 0) ^ val
    return {key: val for key, val in out.items() if val}


def cartier(series: dict, eps: int, delta: int, M: int) -> dict:
    out = {}
    for (t, k), val in series.items():
        if t % 2 == eps and k % 2 == delta:
            i, j = t // 2, k // 2
            if i < M and j < M:
                out[i, j] = out.get((i, j), 0) ^ val
    return {key: val for key, val in out.items() if val}


def diag_of(series: dict, M: int) -> list[int]:
    return [series.get((n, n), 0) for n in range(M)]


def apply_P(U: dict, N: int) -> dict:
    # P = 1 + z + z w + z w^2
    acc = dict(U)
    acc = gf2_poly_add(acc, mul_monomial(U, 1, 0, N))
    acc = gf2_poly_add(acc, mul_monomial(U, 1, 1, N))
    acc = gf2_poly_add(acc, mul_monomial(U, 1, 2, N))
    return acc


def rhs_series(R: dict, N: int) -> dict:
    # 1 + z w^2 R
    acc = {(0, 0): 1}
    acc = gf2_poly_add(acc, mul_monomial(R, 1, 2, N))
    return acc


def predicted_cartier(Uparts: dict, Rparts: dict, eps: int, delta: int, M: int):
    """Hand-derived images of the identity; keys are (eps, delta)."""
    U00, U10 = Uparts[0, 0], Uparts[1, 0]
    U01, U11 = Uparts[0, 1], Uparts[1, 1]
    R00, R10 = Rparts[0, 0], Rparts[1, 0]
    R01, R11 = Rparts[0, 1], Rparts[1, 1]

    def add(*series):
        acc = {}
        for s in series:
            acc = gf2_poly_add(acc, s)
        return acc

    z = lambda S: mul_monomial(S, 1, 0, M)
    w = lambda S: mul_monomial(S, 0, 1, M)
    zw = lambda S: mul_monomial(S, 1, 1, M)
    one = {(0, 0): 1}

    if (eps, delta) == (0, 0):
        # U00 + z U10 + z w (U10+U11) = 1 + z w R10
        # (Λ_{00}(z^2 w^2 F(z^2,w^2)) = z w F(z,w), not z w^2 F.)
        left = add(U00, z(U10), zw(add(U10, U11)))
        right = add(one, zw(R10))
    elif (eps, delta) == (0, 1):
        # U01 + z(U10+U11) + z w U11 = z w R11
        left = add(U01, z(add(U10, U11)), zw(U11))
        right = zw(R11)
    elif (eps, delta) == (1, 0):
        # U00 + U10 + w(U00+U01) = w R00
        left = add(U00, U10, w(add(U00, U01)))
        right = w(R00)
    else:
        # U00 + U01 + U11 + w U01 = w R01
        left = add(U00, U01, U11, w(U01))
        right = w(R01)
    return left, right


def verify_identity_and_cartier(N: int) -> dict:
    v = triangle(N)
    U = series_from_grid(v, N)
    Rgrid = [[v[t][k] & v[t][k + 1] if k + 1 < N else 0 for k in range(N)]
             for t in range(N)]
    R = series_from_grid(Rgrid, N)
    lhs = apply_P(U, N)
    rhs = rhs_series(R, N)
    # Truncation: identity is exact for t < N and k < N-2, except the
    # missing future of U at t=N is already absent from both grids.
    mismatches = []
    for t in range(N):
        for k in range(N - 2):
            if lhs.get((t, k), 0) != rhs.get((t, k), 0):
                mismatches.append((t, k))
    M = N // 2
    Uparts = {(e, d): cartier(U, e, d, M) for e in (0, 1) for d in (0, 1)}
    Rparts = {(e, d): cartier(R, e, d, M) for e in (0, 1) for d in (0, 1)}
    PU = apply_P(U, N)
    RHS = rhs_series(R, N)
    cartier_ok = {}
    predicted_ok = {}
    for e in (0, 1):
        for d in (0, 1):
            cl, cr = cartier(PU, e, d, M), cartier(RHS, e, d, M)
            cartier_ok[f"{e}{d}"] = cl == cr
            pl, pr = predicted_cartier(Uparts, Rparts, e, d, M)
            # Compare on a safe range: extra w^2 needs j+2 < M.
            bad = []
            for i in range(M - 1):
                for j in range(M - 2):
                    if pl.get((i, j), 0) != cl.get((i, j), 0) or pr.get((i, j), 0) != cr.get((i, j), 0):
                        bad.append((i, j))
            predicted_ok[f"{e}{d}"] = not bad
    # Diagonal readout of equal-index Cartier is the 2-kernel of c.
    c = [v[n][n] for n in range(N)]
    diag_match = {
        "00": diag_of(Uparts[0, 0], M) == [c[2 * n] for n in range(M)],
        "11": diag_of(Uparts[1, 1], M) == [c[2 * n + 1] for n in range(M)],
    }
    # Mixed Cartier diagonals are neighboring columns, not kernel states of c.
    mixed = {
        "01": diag_of(Uparts[0, 1], M),  # v(2n, 2n+1) = x(2n, -1)
        "10": diag_of(Uparts[1, 0], M),  # v(2n+1, 2n) = x(2n+1, 1)
        "c_even": [c[2 * n] for n in range(M)],
        "c_odd": [c[2 * n + 1] for n in range(M)],
    }
    mixed_is_center = {
        "01_eq_even": mixed["01"] == mixed["c_even"],
        "01_eq_odd": mixed["01"] == mixed["c_odd"],
        "10_eq_even": mixed["10"] == mixed["c_even"],
        "10_eq_odd": mixed["10"] == mixed["c_odd"],
    }
    return {
        "N": N,
        "identity_mismatches": len(mismatches),
        "identity_ok_interior": not mismatches,
        "cartier_lhs_eq_rhs": cartier_ok,
        "predicted_formulas_ok": predicted_ok,
        "diag_equal_index_is_kernel": diag_match,
        "mixed_diag_is_not_center": mixed_is_center,
        "right_edge_period1": all(v[t][0] == 1 for t in range(N)),
        "offset1_is_t_mod2": all(v[t][1] == (t & 1) for t in range(N) if N > 1),
    }


# ---------------------------------------------------------------------------
# First correlation equation for R
# ---------------------------------------------------------------------------

def product_next_polynomial() -> dict:
    """p' as a square-free polynomial in a,b,c,d = v_{k-2..k+1} over F2."""
    # Brute force ANF.
    table = []
    for bits in range(16):
        a, b, c, d = ((bits >> i) & 1 for i in range(4))
        vp = c ^ (b | a)
        wp = d ^ (c | b)
        table.append(vp & wp)
    # Möbius over the boolean lattice.
    anf = list(table)
    for i in range(4):
        for mask in range(16):
            if mask & (1 << i):
                anf[mask] ^= anf[mask ^ (1 << i)]
    names = ["a", "b", "c", "d"]
    terms = []
    for mask in range(16):
        if anf[mask]:
            if mask == 0:
                terms.append("1")
            else:
                terms.append("".join(names[i] for i in range(4) if mask >> i & 1))
    return {"terms": terms, "anf": anf}


def verify_product_formula(N: int) -> dict:
    """p' = (b+c)(1+d) + a(1+b)(c+d) on the triangle."""
    v = triangle(N)
    bad = 0
    needs_skip = 0  # rows where R does not determine the skip-2 product
    skip_both = [0, 0]
    for t in range(N - 1):
        for k in range(2, N - 1):
            a, b, c, d = v[t][k - 2], v[t][k - 1], v[t][k], v[t][k + 1]
            pred = ((b ^ c) & (1 ^ d)) ^ (a & (1 ^ b) & (c ^ d))
            actual = v[t + 1][k] & v[t + 1][k + 1]
            if pred != actual:
                bad += 1
            if b == 0:
                # When v_{k-1}=0, both adjacent products through k-1 vanish,
                # while v_{k-2}v_k may still vary.
                needs_skip += 1
                skip_both[a & c] += 1
    return {
        "formula_mismatches": bad,
        "middle_zero_cells": needs_skip,
        "skip1_values_when_middle_zero": {"0": skip_both[0], "1": skip_both[1]},
        "skip1_not_a_function_of_R": skip_both[0] > 0 and skip_both[1] > 0,
    }


def r_next_needs_distance3(N: int) -> dict:
    """When the adjacent window is 0, p' still sees v_{k-2} v_{k+1}."""
    v = triangle(N)
    # Compact form uses a(1+b)(c+d), hence a d = v_{k-2} v_{k+1} (distance 3).
    dist3 = [0, 0]
    for t in range(N):
        for k in range(2, N - 1):
            if v[t][k - 1] == 0 and v[t][k] == 0:
                dist3[v[t][k - 2] & v[t][k + 1]] += 1
    return {
        "distance3_when_bc_zero": {"0": dist3[0], "1": dist3[1]},
        "distance3_independent_of_R_window": dist3[0] > 0 and dist3[1] > 0,
    }


# ---------------------------------------------------------------------------
# 2-kernel samples of the center (finite prefixes only)
# ---------------------------------------------------------------------------

def kernel_element(bits: bytearray, m: int, r: int) -> bytes:
    n = len(bits)
    # s(n) = c(2^m n + r) for 2^m n + r < len
    out = bytearray()
    idx = r
    step = 1 << m
    while idx < n:
        out.append(bits[idx])
        idx += step
    return bytes(out)


def count_kernel(bits: bytearray, max_depth: int, min_len: int = 8) -> dict:
    rows = []
    nbits = len(bits)
    for m in range(max_depth + 1):
        seen = {}
        too_short = 0
        prefix_len = 0
        for r in range(1 << m):
            seq = kernel_element(bits, m, r)
            if len(seq) < min_len:
                too_short += 1
                continue
            prefix_len = len(seq)
            seen.setdefault(seq, []).append(r)
        # Birthday: n^2 / 2^{L+1} is tiny only if L is well above 2m.
        birthday = 0.0
        if prefix_len and seen:
            birthday = (len(seen) ** 2) / (2 * (2 ** min(prefix_len, 60)))
        rows.append({
            "depth": m,
            "residues": 1 << m,
            "prefix_len": prefix_len,
            "distinct_prefixes": len(seen),
            "too_short": too_short,
            "colliding_classes": sum(1 for rs in seen.values() if len(rs) > 1),
            "expected_birthday_collisions": birthday,
            "birthday_safe": birthday < 0.01,
        })
    return {"N": nbits, "rows": rows}


def verify_R_generating_equation(N: int) -> dict:
    """(1+z)R + z(1+w)U = zw(1+w)S2 + zw^2 S3 + zw^2 (T012+T013), interior."""
    v = triangle(N)
    bad = 0
    checked = 0
    for t in range(1, N):
        for k in range(2, N - 3):
            # Left: π(t,k) + π(t-1,k) + v(t-1,k) + v(t-1,k-1)
            pi = v[t][k] & v[t][k + 1]
            pi_prev = v[t - 1][k] & v[t - 1][k + 1]
            left = pi ^ pi_prev ^ v[t - 1][k] ^ v[t - 1][k - 1]
            s2 = v[t - 1][k - 1] & v[t - 1][k + 1]  # coeff of z w S2
            s2b = v[t - 1][k - 2] & v[t - 1][k]      # coeff of z w^2 S2
            s3 = v[t - 1][k - 2] & v[t - 1][k + 1]    # z w^2 S3
            t012 = v[t - 1][k - 2] & v[t - 1][k - 1] & v[t - 1][k]
            t013 = v[t - 1][k - 2] & v[t - 1][k - 1] & v[t - 1][k + 1]
            right = s2 ^ s2b ^ s3 ^ t012 ^ t013
            checked += 1
            if left != right:
                bad += 1
    return {"checked": checked, "mismatches": bad}


def sparse_subsequences(bits: bytearray, max_n: int) -> dict:
    pow2 = [{"m": m, "t": 1 << m, "c": int(bits[1 << m])}
            for m in range(0, max_n + 1) if (1 << m) < len(bits)]
    mersenne = [{"m": m, "t": (1 << m) - 1, "c": int(bits[(1 << m) - 1])}
                for m in range(0, max_n + 1) if (1 << m) - 1 < len(bits)]
    return {"c_at_2^m": pow2, "c_at_2^m-1": mersenne}


def prefixes_of_iterates(bits: bytearray, family: str, max_m: int, length: int) -> list[dict]:
    """Family '0'*m, '1'*m, or ('10')*m as operator words on C."""
    rows = []
    for m in range(max_m + 1):
        if family == "0":
            word = "0" * m
        elif family == "1":
            word = "1" * m
        elif family == "10":
            word = "10" * m
        else:
            raise ValueError(family)
        if word == "":
            seq = list(bits[:length])
            r, depth = 0, 0
        else:
            r = 0
            depth = 0
            for ch in reversed(word):
                r += int(ch) << depth
                depth += 1
            seq = list(kernel_element(bits, depth, r)[:length])
        rows.append({
            "m": m,
            "word": word or "ε",
            "residue": r if word else 0,
            "depth": depth if word else 0,
            "prefix": seq,
            "prefix_len": len(seq),
        })
    return rows


def pairwise_distinct_on_prefix(rows: list[dict]) -> dict:
    """Whether Diag(W_m U) prefixes collide. Finite prefixes only."""
    by_prefix = defaultdict(list)
    for row in rows:
        if row["prefix_len"] == 0:
            continue
        by_prefix[tuple(row["prefix"])].append(row["m"])
    return {
        "distinct_prefixes": len(by_prefix),
        "families": len(rows),
        "colliding_prefix_groups": [
            {"prefix": list(p), "m_values": ms}
            for p, ms in by_prefix.items() if len(ms) > 1
        ],
    }


def mixed_off_diagonal_family(v: list[list[int]], max_m: int, length: int) -> list[dict]:
    """Diag(Λ_{0,1} Λ_{0,0}^{m} U)_n = v(2^{m+1}n, 2^{m+1}n+1) = x(2^{m+1}n, -1).

    These live on the generating-function diagonal after mixed Cartier, but
    they are left-neighbor bits, not kernel states of c.
    """
    N = len(v)
    rows = []
    for m in range(max_m + 1):
        step = 1 << (m + 1)
        seq = []
        n = 0
        while len(seq) < length:
            t = step * n
            k = t + 1
            if t >= N or k >= N:
                break
            seq.append(v[t][k])
            n += 1
        rows.append({"m": m, "prefix": seq, "kind": "left_even_decimation"})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=1 << 16)
    parser.add_argument("--triangle", type=int, default=64)
    parser.add_argument("--kernel-depth", type=int, default=12)
    parser.add_argument("--word-prefix", type=int, default=16)
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    ident = verify_identity_and_cartier(args.triangle)
    poly = product_next_polynomial()
    prod = verify_product_formula(args.triangle)
    dist3 = r_next_needs_distance3(args.triangle)
    r_gf = verify_R_generating_equation(args.triangle)

    bits = center_bits(args.bits)
    # Diagonal of the triangle must match packed center.
    tri = triangle(min(args.triangle, 48))
    packed_match = [tri[n][n] for n in range(len(tri))] == list(bits[: len(tri)])

    kern = count_kernel(bits, args.kernel_depth, min_len=8)
    sparse = sparse_subsequences(bits, max_n=20)
    fam0 = prefixes_of_iterates(bits, "0", 12, args.word_prefix)
    fam1 = prefixes_of_iterates(bits, "1", 12, args.word_prefix)
    fam10 = prefixes_of_iterates(bits, "10", 6, args.word_prefix)
    mixed = mixed_off_diagonal_family(tri, 5, 8)

    report = {
        "bits": args.bits,
        "triangle_N": args.triangle,
        "packed_diagonal_matches_triangle": packed_match,
        "identity": ident,
        "R_next_ANF": poly,
        "R_formula": prod,
        "R_distance3": dist3,
        "R_generating_equation": r_gf,
        "kernel_prefix_counts": kern,
        "sparse": sparse,
        "family_Lambda0^m": {
            "rows": fam0,
            "prefix_collisions": pairwise_distinct_on_prefix(fam0),
        },
        "family_Lambda1^m": {
            "rows": fam1,
            "prefix_collisions": pairwise_distinct_on_prefix(fam1),
        },
        "family_Lambda10^m": {
            "rows": fam10,
            "prefix_collisions": pairwise_distinct_on_prefix(fam10),
        },
        "mixed_left_family_not_a_c_kernel": mixed,
        "note": (
            "Growing distinct prefixes do not prove an infinite kernel. "
            "No prize claim."
        ),
    }
    text = json.dumps(report, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(text)
            f.write("\n")
    print(text)


if __name__ == "__main__":
    main()
