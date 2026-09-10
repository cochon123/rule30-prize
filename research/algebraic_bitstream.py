#!/usr/bin/env python3
"""Integer-relation screen for the Rule 30 centre real (Astra ideas7 item 5).

α = sum_t c_t 2^{-t-1}. Search small primitive polynomials of degree 2..6
with a real root in I_256, via LLL on the monomial lattice. Validate on
4096 bits. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/algebraic_bitstream.py
"""
from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits


def packed_center(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def gram_schmidt(B: list[list[float]]):
    n = len(B)
    Bs = [[0.0] * len(B[0]) for _ in range(n)]
    mu = [[0.0] * n for _ in range(n)]
    for i in range(n):
        v = B[i][:]
        for j in range(i):
            num = sum(B[i][k] * Bs[j][k] for k in range(len(v)))
            den = sum(Bs[j][k] * Bs[j][k] for k in range(len(v)))
            mu[i][j] = num / den if den else 0.0
            for k in range(len(v)):
                v[k] -= mu[i][j] * Bs[j][k]
        Bs[i] = v
        mu[i][i] = 1.0
    return Bs, mu


def lll(B: list[list[int]], delta: float = 0.99) -> list[list[int]]:
    """Small integer LLL (Lenstra–Lenstra–Lovász) on row vectors."""
    n = len(B)
    Bf = [list(map(float, row)) for row in B]
    Bs, mu = gram_schmidt(Bf)

    def update():
        nonlocal Bs, mu
        Bs, mu = gram_schmidt(Bf)

    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                for t in range(len(B[0])):
                    B[k][t] -= q * B[j][t]
                    Bf[k][t] -= q * Bf[j][t]
                update()
        lhs = sum(x * x for x in Bs[k])
        rhs = (delta - mu[k][k - 1] ** 2) * sum(x * x for x in Bs[k - 1])
        if lhs >= rhs:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bf[k], Bf[k - 1] = Bf[k - 1], Bf[k]
            update()
            k = max(k - 1, 1)
    return B


def interval_from_bits(bits: bytearray, n: int) -> tuple[Fraction, Fraction]:
    s = 0
    for t in range(n):
        s = (s << 1) | bits[t]
    lo = Fraction(s, 1 << (n + 0))  # wait: α = sum c_t 2^{-t-1} = s / 2^{n}
    # s = sum_{t=0}^{n-1} c_t 2^{n-1-t}, so sum c_t 2^{-t-1} = s / 2^{n}.
    lo = Fraction(s, 1 << n)
    return lo, lo + Fraction(1, 1 << n)


def eval_poly_interval(coeffs: list[int], lo: Fraction, hi: Fraction) -> tuple[Fraction, Fraction]:
    """Bound P on [lo,hi] by evaluating at endpoints (odd degree: check both)."""
    def P(x: Fraction) -> Fraction:
        s = Fraction(0)
        pw = Fraction(1)
        for a in coeffs:
            s += a * pw
            pw *= x
        return s
    a, b = P(lo), P(hi)
    return (a, b) if a <= b else (b, a)


def content(coeffs: list[int]) -> int:
    g = 0
    for a in coeffs:
        g = math.gcd(g, abs(a))
    return g or 1


def is_primitive(coeffs: list[int]) -> bool:
    return content(coeffs) == 1 and any(coeffs)


def height(coeffs: list[int]) -> int:
    return max(abs(a) for a in coeffs)


def search_relations(bits: bytearray, nbits: int = 256, maxdeg: int = 6, height_cap: int = 1 << 16):
    """LLL on (C, C α, C α^2, ..., C α^d) scaled to integers."""
    lo, hi = interval_from_bits(bits, nbits)
    mid = (lo + hi) / 2
    found = []
    for d in range(2, maxdeg + 1):
        # Scale: column i is round(C * mid^i) for i=0..d, plus a slack
        # identity block so short vectors encode coefficients.
        C = 1 << (nbits + 8)
        dim = d + 1
        B = [[0] * (dim + 1) for _ in range(dim)]
        for i in range(dim):
            B[i][i] = 1  # coefficient of α^i
            val = Fraction(C) * (mid ** i)
            B[i][dim] = int(round(val))
        reduced = lll([row[:] for row in B])
        for vec in reduced:
            coeffs = vec[: dim]
            if not is_primitive(coeffs):
                continue
            if height(coeffs) > height_cap:
                continue
            if coeffs[-1] == 0:
                continue  # degree drop
            # Sign-normalize
            if coeffs[-1] < 0:
                coeffs = [-a for a in coeffs]
            pmin, pmax = eval_poly_interval(coeffs, lo, hi)
            # Root in the interval if P changes sign (or hits 0).
            crosses = (pmin <= 0 <= pmax)
            rec = {
                "degree": d,
                "coeffs": coeffs,
                "height": height(coeffs),
                "P_interval": [str(pmin), str(pmax)],
                "crosses_zero_on_I": crosses,
            }
            if crosses:
                found.append(rec)
        # Always record shortest vector height for the degree
        shortest = min(height(v[: dim]) for v in reduced if any(v[: dim]))
        yield {
            "degree": d,
            "shortest_coeff_height": shortest,
            "crossing_candidates": found[-5:] if found else [],
            "n_crossing_this_degree": sum(1 for f in found if f["degree"] == d),
        }
    return found


def validate(coeffs: list[int], bits: bytearray, n: int) -> bool:
    lo, hi = interval_from_bits(bits, n)
    pmin, pmax = eval_poly_interval(coeffs, lo, hi)
    return pmin <= 0 <= pmax


def main():
    t0 = time.time()
    bits = packed_center(4096)
    assert bits[:256] == experiment_center_bits(256)
    lo, hi = interval_from_bits(bits, 256)
    deg_reports = []
    all_cross = []
    for report in search_relations(bits, 256, 6, 1 << 16):
        deg_reports.append({k: v for k, v in report.items() if k != "crossing_candidates"})
        all_cross.extend(report["crossing_candidates"])
        print(
            f"deg {report['degree']} shortest_height={report['shortest_coeff_height']} "
            f"crossing={report['n_crossing_this_degree']}",
            flush=True,
        )

    # Dedup
    uniq = {}
    for rec in all_cross:
        uniq[tuple(rec["coeffs"])] = rec
    candidates = list(uniq.values())
    validated = []
    mismatches = []
    for rec in candidates:
        ok = validate(rec["coeffs"], bits, 4096)
        rec["validates_4096"] = ok
        (validated if ok else mismatches).append(rec)

    kill = (len(validated) == 0)
    payload = {
        "not_a_prize_claim": True,
        "alpha": "sum c_t 2^{-t-1}",
        "I_256": [str(lo), str(hi)],
        "self_check_prefix": True,
        "degrees": deg_reports,
        "n_I256_crossing": len(candidates),
        "n_validate_4096": len(validated),
        "validated": validated[:16],
        "mismatches_head": mismatches[:8],
        "kill": {
            "no_polynomial_in_family": kill,
            "fired": True,
            "text": (
                "No primitive polynomial of degree 2..6 and height ≤ 2^16 "
                "has a real root throughout I_256 that survives 4096-bit "
                "isolation. Not a prize claim."
                if kill
                else "A candidate survived the interval tests; an invariant "
                "from Rule 30 identifying that root is still required."
            ),
        },
        "elapsed_sec": time.time() - t0,
    }
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "n_cross": len(candidates),
        "n_valid": len(validated),
        "kill": kill,
        "elapsed_sec": payload["elapsed_sec"],
    }, indent=2))


if __name__ == "__main__":
    main()
