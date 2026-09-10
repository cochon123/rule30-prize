"""Dual-particle operator for Rule 30 (prize problem 2).

Pullback of characters chi_A = prod_{j in A} s_j, s_j = (-1)^{x_j}.
Checks the exact one-step identity, the last-step C<->R seed-eval pairing,
and the two-step monomial involution. Does not prove density.

Run: python3 research/dual_particles.py
Does not modify experiment.py, strip_graph.py, or strip_extend.py.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits, reference_bits

HALF = Fraction(1, 2)

# Branch of a particle at j: always emit j-1, optionally j and/or j+1.
# Correct Rule 30 weights: L=-1/2, C=R=B=+1/2.
BRANCHES = (
    (-HALF, lambda j: frozenset({j - 1})),  # L
    (HALF, lambda j: frozenset({j - 1, j})),  # C
    (HALF, lambda j: frozenset({j - 1, j + 1})),  # R
    (HALF, lambda j: frozenset({j - 1, j, j + 1})),  # B
)
BRANCH_NAMES = ("L", "C", "R", "B")


def s_from_bit(x: int) -> int:
    return 1 - 2 * int(x)


def rule30_bit(xm: int, x: int, xp: int) -> int:
    return xm ^ (x | xp)


def spin_identity_rhs(sm: int, s: int, sp: int) -> int:
    """Correct real identity: (1/2) s_{j-1} (-1 + s_j + s_{j+1} + s_j s_{j+1})."""
    val = sm * (-1 + s + sp + s * sp)
    assert val % 2 == 0
    return val // 2


def brief_identity_rhs(sm: int, s: int, sp: int) -> int:
    """Formula in the assignment (incorrect for Rule 30)."""
    val = sm * (1 + s + sp - s * sp)
    assert val % 2 == 0
    return val // 2


def check_spin_identity() -> None:
    for bits in product((0, 1), repeat=3):
        xm, x, xp = bits
        sm, s, sp = map(s_from_bit, bits)
        got = spin_identity_rhs(sm, s, sp)
        want = s_from_bit(rule30_bit(xm, x, xp))
        assert got == want, (bits, got, want)
        brief = brief_identity_rhs(sm, s, sp)
        if bits == (0, 1, 0):
            # centre 1, neighbors 0: output is 1, spin -1.
            # Assignment parenthesis is (-1)^{AND}, not (-1)^{OR}.
            assert want == -1
            assert brief == 1
    # Brief formula matches AND rather than OR in the nonlinear slot.
    mismatches = sum(
        brief_identity_rhs(*map(s_from_bit, bits))
        != s_from_bit(rule30_bit(*bits))
        for bits in product((0, 1), repeat=3)
    )
    assert mismatches == 4


def K_of(A: frozenset[int]) -> dict[frozenset[int], Fraction]:
    acc: dict[frozenset[int], Fraction] = {frozenset(): Fraction(1)}
    for j in sorted(A):
        new: dict[frozenset[int], Fraction] = defaultdict(lambda: Fraction(0))
        for S, w in acc.items():
            for wb, emit in BRANCHES:
                new[S ^ emit(j)] += w * wb
        acc = {S: w for S, w in new.items() if w}
    return acc


def apply_K(vec: dict[frozenset[int], Fraction]) -> dict[frozenset[int], Fraction]:
    out: dict[frozenset[int], Fraction] = defaultdict(lambda: Fraction(0))
    for A, w in vec.items():
        for B, wb in K_of(A).items():
            out[B] += w * wb
    return {A: w for A, w in out.items() if w}


def phi(A: frozenset[int]) -> int:
    return -1 if 0 in A else 1


def pairing(vec: dict[frozenset[int], Fraction]) -> Fraction:
    return sum(w * phi(A) for A, w in vec.items())


def check_pullback_matches_center(steps: int = 8) -> None:
    bits = center_bits(steps)
    assert bits == reference_bits(steps)
    vec = {frozenset({0}): Fraction(1)}
    for t in range(steps):
        got = pairing(vec)
        want = Fraction((-1) ** bits[t])
        assert got == want, (t, got, want)
        vec = apply_K(vec)


def last_step_CR_residual(A: frozenset[int]) -> dict[frozenset[int], Fraction]:
    """Keep only L,B on the distinguished last-step particle; full K elsewhere."""
    distinguished = None
    if 0 in A:
        distinguished = 0
    elif -1 in A:
        distinguished = -1
    if distinguished is None:
        return K_of(A)
    rest = K_of(A - {distinguished})
    out: dict[frozenset[int], Fraction] = defaultdict(lambda: Fraction(0))
    # L and B of the distinguished particle.
    for emit_w, emit in (BRANCHES[0], BRANCHES[3]):
        for S, w in rest.items():
            out[S ^ emit(distinguished)] += w * emit_w
    return {S: w for S, w in out.items() if w}


def check_CR_lemma(max_size: int = 4) -> None:
    sites = range(-3, 4)
    for n in range(0, max_size + 1):
        for occ in product((0, 1), repeat=len(sites)):
            if sum(occ) != n:
                continue
            A = frozenset(s for s, b in zip(sites, occ) if b)
            full = pairing(K_of(A))
            res = pairing(last_step_CR_residual(A))
            assert full == res, (sorted(A), full, res)
            # Closed form: first seed row is 1 on {-1,0,1}.
            want = Fraction((-1) ** len(A & {-1, 0, 1}))
            assert full == want, (sorted(A), full, want)


def k2_closed_form() -> dict[frozenset[int], Fraction]:
    out: dict[frozenset[int], Fraction] = defaultdict(lambda: Fraction(0))
    for mask in range(4):
        S = frozenset(j for j, bit in ((1, 1), (2, 2)) if mask & bit)
        out[frozenset({-2}) | S] += Fraction(1, 4)
        if S:
            out[frozenset({-2, -1, 0}) | S] += Fraction(1, 4)
    out[frozenset({-2, -1, 0})] -= Fraction(3, 4)
    return {A: w for A, w in out.items() if w}


def check_two_step() -> None:
    k2 = apply_K({frozenset({0}): Fraction(1)})
    k2 = apply_K(k2)
    closed = k2_closed_form()
    assert k2 == closed, (k2, closed)
    tau = frozenset({-1, 0})
    cancelled = 0
    residual = {}
    seen = set()
    for A, w in k2.items():
        if A in seen:
            continue
        B = A ^ tau
        seen.add(A)
        seen.add(B)
        wB = k2.get(B, Fraction(0))
        if B in k2 and w == wB and phi(A) == -phi(B):
            cancelled += 1
        else:
            residual[A] = w
            if B in k2 and B != A:
                residual[B] = wB
    assert cancelled == 3
    assert residual == {
        frozenset({-2}): Fraction(1, 4),
        frozenset({-2, -1, 0}): Fraction(-3, 4),
    }
    assert pairing(residual) == pairing(k2) == 1


def leftover_l1_after_tau(vec, tau_sites):
    tau = frozenset(tau_sites)
    seen = set()
    leftover = Fraction(0)
    for A, w in vec.items():
        if A in seen:
            continue
        B = A ^ tau
        seen.add(A)
        seen.add(B)
        wB = vec.get(B, Fraction(0))
        if B not in vec:
            leftover += abs(w)
        else:
            leftover += abs(w - wB)
    return leftover


def table_through(steps: int = 8) -> list[dict]:
    bits = center_bits(steps)
    vec = {frozenset({0}): Fraction(1)}
    rows = []
    for t in range(steps):
        ph = pairing(vec)
        l1 = sum(abs(w) for w in vec.values())
        rows.append(
            {
                "t": t,
                "phi": str(ph),
                "spin": int((-1) ** bits[t]),
                "monomials": len(vec),
                "l1": str(l1),
                "tau_m10_leftover_l1": str(leftover_l1_after_tau(vec, [-1, 0])),
            }
        )
        vec = apply_K(vec)
    return rows


def main() -> None:
    check_spin_identity()
    check_pullback_matches_center(6)
    check_CR_lemma(3)
    check_two_step()
    rows = table_through(6)
    print("dual_particles self-check OK")
    print("t  phi  spin  monomials  l1  leftover_l1(A Δ {-1,0})")
    for row in rows:
        print(
            f"{row['t']:d}  {row['phi']:>4}  {row['spin']:+d}  "
            f"{row['monomials']:9d}  {row['l1']:>8}  {row['tau_m10_leftover_l1']:>8}"
        )
    # Each slice still has |phi|=1 after every pairing, so the time-sum
    # unpaired seed-eval weight is exactly |D(N)| in magnitude per term,
    # i.e. N units, not o(N).
    assert all(abs(int(r["spin"])) == 1 for r in rows)


if __name__ == "__main__":
    main()
