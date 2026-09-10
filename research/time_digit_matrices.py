#!/usr/bin/env python3
"""Time-digit linear representations of c_n over F_3 (Astra ideas7 item 2).

Seek dim ≤ 16 matrices M_0, M_1 over F_3 with c_n = λ^T M_{b1}...M_{bm} ρ
where b1..bm = bin(n), including a consistent leading-zero action.

Kill: any concatenation-matrix rank > 16, or a reconstructed candidate
mismatches a held-out time. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/time_digit_matrices.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits

DIM_CAP = 16
L_MAX = 7
HOLDOUT_BITS = 1 << 16


def packed_center(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def gf3_rank(rows: list[list[int]]) -> int:
    """Gaussian elimination over F_3. rows are mutated copies."""
    if not rows:
        return 0
    a = [row[:] for row in rows]
    n, m = len(a), len(a[0])
    r = 0
    for col in range(m):
        piv = None
        for i in range(r, n):
            if a[i][col] % 3:
                piv = i
                break
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        inv = a[r][col] % 3
        inv = 1 if inv == 1 else 2  # 2*2=1 mod 3
        a[r] = [(inv * x) % 3 for x in a[r]]
        for i in range(n):
            if i == r:
                continue
            fac = a[i][col] % 3
            if not fac:
                continue
            a[i] = [(a[i][j] - fac * a[r][j]) % 3 for j in range(m)]
        r += 1
        if r == n:
            break
    return r


def concat_matrix(bits: bytearray, left_len: int, right_len: int) -> list[list[int]]:
    nr, nc = 1 << left_len, 1 << right_len
    M = [[0] * nc for _ in range(nr)]
    for u in range(nr):
        for v in range(nc):
            n = (u << right_len) | v
            M[u][v] = bits[n]
    return M


def leading_zero_matrix(bits: bytearray, ell: int) -> list[list[int]]:
    """Rows: all words of length ≤ ell as left factors, padded on the left
    with zeros to length ell (so the same integer n has several rows).
    Columns: right factors of length ell. This is the leading-zero test:
    extra left zeros must not change the output, hence those rows equal.
    """
    nc = 1 << ell
    rows = []
    labels = []
    for L in range(0, ell + 1):
        for u in range(1 << L):
            row = []
            for v in range(nc):
                n = (u << ell) | v
                row.append(bits[n])
            rows.append(row)
            labels.append((L, u))
    return rows, labels


def try_reconstruct(bits: bytearray, ell: int, rank: int):
    """Factor H = A B over F_3 with A (2^ell × r), B (r × 2^ell) if rank≤16.

    Then M_0, M_1 would have to act on the r-dimensional row space.
    We only test whether a linear representation of this Hankel block
    predicts c at times that use more than 2 ell bits — it cannot, unless
    we build the actual automata. Here: reconstruct by taking r independent
    rows as A and solving for B, then check the block identity. Held-out
    times with |bin(n)| > 2 ell are a different test: apply the digit
    recurrences if we can fit M_0, M_1.

    Digit matrices: the row vector after reading prefix u is A_u = λ^T M_u.
    From the factorization, row u of H is A_u * (columns = M_v ρ).
    Fit M_b on the prefix space by least squares over F_3: for each prefix
    u of length < ell, row_{u||b} should equal row_u * M_b, using the
    r-dimensional coordinates.
    """
    H = concat_matrix(bits, ell, ell)
    # Row-space basis
    coords, basis_idx = row_space_coords(H)
    r = len(basis_idx)
    if r == 0 or r > DIM_CAP:
        return {"ok": False, "reason": "rank out of range", "r": r}
    # B is the basis rows; coordinates give A such that H = A B, A[u]=coords[u]
    B = [H[i][:] for i in basis_idx]
    # Verify factorization
    for u, cu in enumerate(coords):
        recon = [sum(cu[k] * B[k][j] for k in range(r)) % 3 for j in range(len(H[0]))]
        if recon != H[u]:
            return {"ok": False, "reason": "factorization failed", "r": r}

    def fit_Mb(bit: int):
        """Solve coords[u] M = coords[u||bit] for all |u|=ell-1, u||bit as ell bits
        when reading one more left digit... Our H rows are length-ell left words.
        Transition on appending a RIGHT bit is easier: columns.
        Left-append of a high digit: row (b << (ell-1) | u') for |u'|=ell-1
        vs row u' padded — leading-zero consistency is separate.

        Fit right-multiplication on coordinates: coords[u] M_b = coords[u]
        wait, right digit extends the TIME value as (val(u)<<1)|b but then
        the split is no longer ell/ell.

        For a linear representation, M_b acts when reading the next MSB or LSB.
        We use MSB-first: n's binary from high bit. Then left-factor u is the
        high bits. Reading one more high bit is not a right concatenation.

        LSB-first: reading the low bit of n. Then H(u,v) with u high, v low
        means M_v is the low-bit product. The right transition:
        coords_left(u) * N_v = H(u,·) row, already used.

        Transition for appending one low bit to a high prefix of length ell:
        not closed. Fit instead on prefixes of length ell-1 as left and
        length ell+1 as need more bits.

        Practical screen: try to find 2 r×r matrices over F_3 such that
        for all n < 2^{2 ell}, writing bits MSB-first,
          vec starts at ρ, multiply M_{b_i}, output λ·vec equals c_n.
        Brute 3^{2 r^2} is impossible for r=16. For r≤3 brute is 3^{18}.

        We only brute-fit when r ≤ 2 (two 2×2 matrices: 3^8=6561 per matrix
        if λ,ρ also free that's more). Skip reconstruction when r>4;
        rank≤16 is the kill screen, reconstruction is optional.
        """
        return None

    return {
        "ok": True,
        "r": r,
        "factorization_checked": True,
        "digit_matrices": "not reconstructed (rank permits the family; induction required)",
    }


def row_space_coords(H: list[list[int]]):
    """Return coords[u] in F_3^{r} and basis row indices."""
    n, m = len(H), len(H[0])
    a = [row[:] for row in H]
    basis_idx = []
    ops = []  # how to express each pivot row
    pivcol = []
    r = 0
    # Eliminate to find independent rows
    used = [False] * n
    for col in range(m):
        piv = None
        for i in range(n):
            if used[i]:
                continue
            if a[i][col] % 3:
                piv = i
                break
        if piv is None:
            continue
        used[piv] = True
        basis_idx.append(piv)
        inv = a[piv][col] % 3
        inv = 1 if inv == 1 else 2
        a[piv] = [(inv * x) % 3 for x in a[piv]]
        for i in range(n):
            if i == piv:
                continue
            fac = a[i][col] % 3
            if fac:
                a[i] = [(a[i][j] - fac * a[piv][j]) % 3 for j in range(m)]
        r += 1
        if r == n:
            break
    # Coordinates of original rows in the basis: solve basis^T x = H[u]
    # Use original H and original basis rows.
    orig_basis = [H[i][:] for i in basis_idx]
    coords = []
    for u in range(n):
        coords.append(express(orig_basis, H[u]))
    return coords, basis_idx


def express(basis: list[list[int]], vec: list[int]) -> list[int]:
    r = len(basis)
    if r == 0:
        return []
    m = len(vec)
    A = [basis[j][:] + [0] * 0 for j in range(r)]
    # columns of B are basis rows... solve B^T x = vec i.e. rows of basis as equations
    # Augment: [basis^T | vec] is m × (r+1) with rows
    M = [[basis[j][i] for j in range(r)] + [vec[i]] for i in range(m)]
    # GE over F3
    row = 0
    pivot_of = [-1] * r
    for col in range(r):
        piv = None
        for i in range(row, m):
            if M[i][col] % 3:
                piv = i
                break
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        inv = M[row][col] % 3
        inv = 1 if inv == 1 else 2
        M[row] = [(inv * x) % 3 for x in M[row]]
        for i in range(m):
            if i == row:
                continue
            fac = M[i][col] % 3
            if fac:
                M[i] = [(M[i][j] - fac * M[row][j]) % 3 for j in range(r + 1)]
        pivot_of[col] = row
        row += 1
    x = [0] * r
    for col in range(r):
        pr = pivot_of[col]
        if pr >= 0:
            x[col] = M[pr][r] % 3
    return x


def main():
    t0 = time.time()
    bits = packed_center(max(HOLDOUT_BITS, 1 << (2 * L_MAX)))
    assert bits[:256] == experiment_center_bits(256)
    ranks = []
    kill_rank = False
    violations = []
    for ell in range(2, L_MAX + 1):
        H = concat_matrix(bits, ell, ell)
        rk = gf3_rank(H)
        Hz, _ = leading_zero_matrix(bits, ell)
        rk_z = gf3_rank(Hz)
        rec = {
            "ell": ell,
            "shape": [1 << ell, 1 << ell],
            "rank_exact_split": rk,
            "rank_leading_zeros_rows": rk_z,
            "dim_cap": DIM_CAP,
            "exceeds_cap": rk > DIM_CAP or rk_z > DIM_CAP,
        }
        # Neighbor splits
        if ell >= 2:
            Hn = concat_matrix(bits, ell - 1, ell + 1)
            rec["rank_split_ell-1_ell+1"] = gf3_rank(Hn)
            rec["exceeds_cap"] = rec["exceeds_cap"] or rec["rank_split_ell-1_ell+1"] > DIM_CAP
        ranks.append(rec)
        if rec["exceeds_cap"]:
            kill_rank = True
            violations.append(rec)

    payload = {
        "not_a_prize_claim": True,
        "field": "F_3",
        "dim_cap": DIM_CAP,
        "l_range": list(range(2, L_MAX + 1)),
        "self_check_prefix": True,
        "ranks": ranks,
        "kill": {
            "rank_above_16": kill_rank,
            "violations": violations,
            "fired": kill_rank,
            "text": (
                "A concatenation matrix over F_3 has rank > 16, so no "
                "16-dimensional linear representation of this family exists."
                if kill_rank
                else "All tested ranks ≤ 16; reconstruction/induction still required."
            ),
        },
        "elapsed_sec": time.time() - t0,
    }
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "wrote": str(dest),
        "ranks": [(r["ell"], r["rank_exact_split"], r.get("rank_split_ell-1_ell+1"), r["rank_leading_zeros_rows"]) for r in ranks],
        "kill": kill_rank,
        "elapsed_sec": payload["elapsed_sec"],
    }, indent=2))


if __name__ == "__main__":
    main()
