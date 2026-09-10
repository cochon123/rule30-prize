#!/usr/bin/env python3
"""Stern–Brocot coordinates of packed Rule 30 rows (prize problem 3).

Preregistered family: q_{t+1} = P(q_t, q_{t-1}) / Q(q_t, q_{t-1}) with
bidegree(P), bidegree(Q) at most (2, 2). Fit on rows 0..63 over Q; test
through row 255. Degree is frozen. This is not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/stern_brocot.py
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


FIT_MAX = 63
TEST_MAX = 255
MONOMS = tuple((i, j) for i in range(3) for j in range(3))  # bidegree <= (2,2)
N_MON = len(MONOMS)
N_COL = 2 * N_MON  # P coeffs then Q coeffs


# ---------------------------------------------------------------------------
# Exact linear algebra over Q
# ---------------------------------------------------------------------------

def mat_mul(A, B):
    return (
        A[0] * B[0] + A[1] * B[2],
        A[0] * B[1] + A[1] * B[3],
        A[2] * B[0] + A[3] * B[2],
        A[2] * B[1] + A[3] * B[3],
    )


def rref_kernel(rows: list[list[Fraction]]) -> tuple[int, list[list[Fraction]]]:
    """Return (rank, kernel basis) of a matrix with N_COL columns over Q."""
    if not rows:
        identity = [
            [Fraction(1 if i == j else 0) for j in range(N_COL)]
            for i in range(N_COL)
        ]
        return 0, identity
    a = [row[:] for row in rows]
    n = len(a)
    pivot_col = [-1] * n
    used = [False] * N_COL
    rank = 0
    col = 0
    r = 0
    while r < n and col < N_COL:
        piv = None
        for i in range(r, n):
            if a[i][col] != 0:
                piv = i
                break
        if piv is None:
            col += 1
            continue
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][col]
        a[r] = [x / pv for x in a[r]]
        for i in range(n):
            if i == r or a[i][col] == 0:
                continue
            fac = a[i][col]
            a[i] = [a[i][k] - fac * a[r][k] for k in range(N_COL)]
        used[col] = True
        pivot_col[r] = col
        rank += 1
        r += 1
        col += 1

    free = [j for j in range(N_COL) if not used[j]]
    basis = []
    for f in free:
        vec = [Fraction(0)] * N_COL
        vec[f] = Fraction(1)
        for i, pc in enumerate(pivot_col):
            if pc < 0:
                continue
            vec[pc] = -a[i][f]
        basis.append(vec)
    return rank, basis


def poly_eval(coeffs: list[Fraction], x: Fraction, y: Fraction) -> Fraction:
    acc = Fraction(0)
    for (i, j), c in zip(MONOMS, coeffs):
        if c:
            acc += c * (x ** i) * (y ** j)
    return acc


def poly_is_zero(coeffs: list[Fraction]) -> bool:
    return all(c == 0 for c in coeffs)


def poly_terms(coeffs: list[Fraction]) -> list[str]:
    out = []
    for (i, j), c in zip(MONOMS, coeffs):
        if c == 0:
            continue
        mon = []
        if i:
            mon.append("x" if i == 1 else f"x^{i}")
        if j:
            mon.append("y" if j == 1 else f"y^{j}")
        m = "*".join(mon) if mon else "1"
        out.append(f"({c})*{m}" if m != "1" else f"({c})")
    return out


def vec_to_PQ(vec: list[Fraction]):
    return vec[:N_MON], vec[N_MON:]


def clear_denominators(vec: list[Fraction]) -> list[int]:
    dens = [c.denominator for c in vec]
    lcm = 1
    for d in dens:
        lcm = lcm * d // gcd_int(lcm, d)
    ints = [int(c * lcm) for c in vec]
    g = 0
    for v in ints:
        g = gcd_int(g, abs(v))
    if g > 1:
        ints = [v // g for v in ints]
    if any(v != 0 for v in ints) and next(v for v in ints if v != 0) < 0:
        ints = [-v for v in ints]
    return ints


def gcd_int(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


# ---------------------------------------------------------------------------
# Rule 30 rows packed from the right edge: b_k = x(t, t-k)
# ---------------------------------------------------------------------------

def packed_words(count: int) -> list[list[int]]:
    """LSB / b0 is the right edge x(t,t). Length 2t+1. Center is b_t."""
    row = 1
    words = []
    for t in range(count):
        width = 2 * t + 1
        word = [(row >> k) & 1 for k in range(width)]
        assert len(word) == width
        words.append(word)
        row = row ^ ((row << 1) | (row << 2))
    return words


def left_packed_words(count: int) -> list[list[int]]:
    """Cross-check: experiment.py packing, bit k = x(t, k-t)."""
    row = 1
    words = []
    for t in range(count):
        width = 2 * t + 1
        word = [(row >> (2 * t - k)) & 1 for k in range(width)]
        words.append(word)
        row = (row << 2) ^ ((row << 1) | row)
    return words


def stern_q(word: list[int]) -> Fraction:
    """q = (M_b0 ... M_b_{2t}) · 1 with M_0=L, M_1=R."""
    a, b, c, d = 1, 0, 0, 1
    for bit in word:
        if bit == 0:
            # * L = [[1,1],[0,1]]
            a, b, c, d = a, a + b, c, c + d
        else:
            # * R = [[1,0],[1,1]]
            a, b, c, d = a + b, b, c + d, d
    return Fraction(a + b, c + d)


def decode_q(q: Fraction, length: int) -> list[int]:
    """Peel leftmost matrices. L·z=z+1 > 1; R·z=z/(z+1) < 1."""
    bits = []
    z = q
    for _ in range(length):
        if z > 1:
            bits.append(0)
            z = z - 1
        elif z < 1:
            bits.append(1)
            z = z / (1 - z)
        else:
            raise ValueError("encoding hit 1 before the empty product")
    if z != 1:
        raise ValueError(f"did not reduce to 1, leftover {z}")
    return bits


def design_row(x: Fraction, y: Fraction, z: Fraction) -> list[Fraction]:
    """Coefficients of Q(x,y)*z - P(x,y)."""
    row = [Fraction(0)] * N_COL
    for k, (i, j) in enumerate(MONOMS):
        mon = (x ** i) * (y ** j)
        row[k] = -mon
        row[N_MON + k] = z * mon
    return row


def classify_vector(vec, pairs, zs):
    """Reject vanishing denominators and degenerate identities on `pairs`."""
    P, Q = vec_to_PQ(vec)
    info = {
        "P_zero": poly_is_zero(P),
        "Q_zero": poly_is_zero(Q),
        "P_terms": poly_terms(P),
        "Q_terms": poly_terms(Q),
        "P_int": clear_denominators(P),
        "Q_int": clear_denominators(Q),
    }
    if info["P_zero"] and info["Q_zero"]:
        info["status"] = "zero"
        return info
    if info["Q_zero"]:
        info["status"] = "degenerate_Q_identically_zero"
        return info
    if info["P_zero"]:
        # Would force z=0 wherever Q is nonzero.
        info["status"] = "degenerate_P_identically_zero"
        return info

    vanish_Q = []
    indeterminate = []
    mismatches = []
    for idx, ((x, y), z) in enumerate(zip(pairs, zs)):
        pv = poly_eval(P, x, y)
        qv = poly_eval(Q, x, y)
        if qv == 0:
            vanish_Q.append(idx)
            if pv == 0:
                indeterminate.append(idx)
            elif pv != 0:
                mismatches.append(idx)
            continue
        if pv / qv != z:
            mismatches.append(idx)

    info["n_vanish_Q"] = len(vanish_Q)
    info["n_indeterminate"] = len(indeterminate)
    info["n_mismatch"] = len(mismatches)
    info["first_vanish_Q"] = vanish_Q[0] if vanish_Q else None
    info["first_mismatch"] = mismatches[0] if mismatches else None

    if vanish_Q:
        info["status"] = "vanishing_denominator"
        return info
    if mismatches:
        info["status"] = "does_not_hold"
        return info
    info["status"] = "candidate"
    return info


def main() -> None:
    n_words = TEST_MAX + 1
    words = packed_words(n_words)
    left_words = left_packed_words(min(n_words, 64))
    assert words[: len(left_words)] == left_words

    qs: list[Fraction] = []
    centers = []
    roundtrip_ok = 0
    for t, word in enumerate(words):
        assert word[t] in (0, 1)
        centers.append(word[t])
        q = stern_q(word)
        qs.append(q)
        decoded = decode_q(q, len(word))
        assert decoded == word
        roundtrip_ok += 1

    assert len(set(qs)) == len(qs)

    # Training triples: (q_{t-1}, q_t, q_{t+1}) for t=1..FIT_MAX-1,
    # using only rows 0..FIT_MAX.
    train_t = list(range(1, FIT_MAX))
    train_pairs = [(qs[t], qs[t - 1]) for t in train_t]
    train_zs = [qs[t + 1] for t in train_t]
    A = [design_row(x, y, z) for (x, y), z in zip(train_pairs, train_zs)]
    rank, kernel = rref_kernel(A)

    train_classes = [classify_vector(vec, train_pairs, train_zs) for vec in kernel]

    # Held-out triples through row TEST_MAX: t=1..TEST_MAX-1, but report
    # failures with t+1 > FIT_MAX separately.
    all_t = list(range(1, TEST_MAX))
    all_pairs = [(qs[t], qs[t - 1]) for t in all_t]
    all_zs = [qs[t + 1] for t in all_t]
    test_classes = [classify_vector(vec, all_pairs, all_zs) for vec in kernel]

    candidates = []
    for i, (tr, te, vec) in enumerate(zip(train_classes, test_classes, kernel)):
        entry = {
            "kernel_index": i,
            "train": tr,
            "test": te,
        }
        if tr["status"] == "candidate":
            candidates.append(entry)

    survivors = [
        c for c in candidates if c["test"]["status"] == "candidate"
    ]

    # Diagnostic: bit size of the coordinates (for the cheaper-c_n question).
    heights = [max(q.numerator.bit_length(), q.denominator.bit_length()) for q in qs]
    # First-bit of the word is the right edge, always 1 on this seed, so q_t < 1.
    first_bits = [w[0] for w in words]
    q_sample = [
        {"t": t, "q": str(qs[t]), "c_t": centers[t], "height_bits": heights[t]}
        for t in list(range(8)) + [16, 32, 63, 64, 127, 255]
        if t <= TEST_MAX
    ]

    # Reconstructing the middle letter from q_t still peels t letters.
    peel_costs = []
    for t in (8, 16, 32, 63, 127, 255):
        z = qs[t]
        for _ in range(t):
            if z > 1:
                z = z - 1
            else:
                z = z / (1 - z)
        middle = 0 if z > 1 else 1
        peel_costs.append(
            {
                "t": t,
                "recovered_c": middle,
                "matches": middle == centers[t],
                "peels_to_middle": t,
                "word_length": 2 * t + 1,
            }
        )

    out = {
        "fit_rows": f"0..{FIT_MAX}",
        "test_rows": f"0..{TEST_MAX}",
        "n_train_equations": len(A),
        "n_columns": N_COL,
        "monomials": [f"x^{i} y^{j}" for i, j in MONOMS],
        "rank": rank,
        "kernel_dim": len(kernel),
        "roundtrip_ok": roundtrip_ok,
        "injective_on_prefix": len(set(qs)) == len(qs),
        "right_edge_always_one": all(b == 1 for b in first_bits),
        "all_q_lt_one": all(q < 1 for q in qs),
        "train_kernel_status": [c["status"] for c in train_classes],
        "test_kernel_status": [c["status"] for c in test_classes],
        "n_train_candidates": len(candidates),
        "n_survivors": len(survivors),
        "candidates": candidates,
        "survivors": survivors,
        "q_sample": q_sample,
        "height_bits_at": {
            str(t): heights[t]
            for t in (0, 1, 8, 16, 32, 63, 64, 127, 255)
            if t <= TEST_MAX
        },
        "peel_middle_letter": peel_costs,
        "kill": len(survivors) == 0,
    }

    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in (
        "rank", "kernel_dim", "n_train_equations", "n_columns",
        "n_train_candidates", "n_survivors", "kill",
        "train_kernel_status", "test_kernel_status",
        "roundtrip_ok", "injective_on_prefix",
    )}, indent=2))
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
