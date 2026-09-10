#!/usr/bin/env python3
"""Backward dependency of a diagonal Mahler query for Rule 30 c_n.

Does not claim a prize result. Verifies the a_{k,j} recurrence, constructs
the truncated backward closure, and measures coefficient / zeta-query /
shared-convolution growth. Construction+evaluation costs are counted in a
bit / transdichotomous-RAM model stated in mahler_dependency.md.
"""
from __future__ import annotations

import argparse
from collections import Counter


def ceil_half(k: int) -> int:
    return (k + 1) // 2


def submasks(x: int):
    s = x
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & x


def direct_center(n: int) -> int:
    row = 1
    for _ in range(n):
        row = (row << 2) ^ ((row << 1) | row)
    return (row >> n) & 1


def supports_exact(K: int):
    """Untruncated exact supports; same recurrence as support_exact.py."""
    S = [{0}]
    for k in range(1, K + 1):
        a = S[k - 1]
        b = S[k - 2] if k >= 2 else set()
        counts = Counter(i | j for i in a for j in b)
        star = {j for j, count in counts.items() if count & 1}
        S.append({j + 1 for j in (a ^ b ^ star)})
    return S


def coeff_rows(K: int, cap: int | None = None):
    """a[k][j] for 0<=k<=K, 0<=j<=cap (cap=None keeps untruncated maxima)."""
    S = supports_exact(K)
    if cap is None:
        cap = max((max(s) if s else 0) for s in S)
    rows = []
    for k, support in enumerate(S):
        row = [0] * (cap + 1)
        for j in support:
            if j <= cap:
                row[j] = 1
        rows.append(row)
    return rows


def or_conv_at(a, b, m: int) -> int:
    total = 0
    for r in submasks(m):
        s_need = m & ~r
        extra = r
        e = extra
        while True:
            s = s_need | e
            total ^= a[r] & b[s] if r < len(a) and s < len(b) else 0
            if e == 0:
                break
            e = (e - 1) & extra
    return total


def verify_recurrence(K: int = 16) -> None:
    S = supports_exact(K)
    cap = max(max(s) if s else 0 for s in S)
    a = coeff_rows(K, cap)
    for k in range(1, K + 1):
        prev1 = a[k - 1]
        prev2 = a[k - 2] if k >= 2 else [0] * (cap + 1)
        lo = ceil_half(k)
        for j, bit in enumerate(a[k]):
            if j == 0:
                if bit != 0:
                    raise AssertionError(f"a[{k},0] should be 0")
                continue
            m = j - 1
            lin = (prev1[m] if m < len(prev1) else 0) ^ (
                prev2[m] if m < len(prev2) else 0
            )
            star = or_conv_at(prev1, prev2, m)
            got = lin ^ star
            if got != bit:
                raise AssertionError((k, j, bit, got, lin, star))
            if j < lo and bit:
                raise AssertionError(f"min-support failed at k={k} j={j}")
    for n in range(K + 1):
        mahler = 0
        for j in submasks(n):
            if j < len(a[n]):
                mahler ^= a[n][j]
        if mahler != direct_center(n):
            raise AssertionError(("mahler", n, mahler, direct_center(n)))


def final_need(n: int) -> set[int]:
    """Indices j required for c_n = XOR_{j ⊆ n} a_{n,j}, after min-support."""
    if n == 0:
        return {0}
    lo = ceil_half(n)
    return {j for j in submasks(n) if j >= lo}


def expand_operands(j: int, k: int, n: int) -> tuple[set[int], set[int]]:
    """Formal operands of a_{k,j} at layers k-1 and k-2, truncated."""
    if j <= 0:
        return set(), set()
    m = j - 1
    need1, need2 = set(), set()
    lo1 = ceil_half(k - 1) if k >= 1 else 0
    lo2 = ceil_half(k - 2) if k >= 2 else 0

    def take(dest: set[int], idx: int, lo: int) -> None:
        if lo <= idx <= n:
            dest.add(idx)

    take(need1, m, lo1)
    if k >= 2:
        take(need2, m, lo2)
    for r in submasks(m):
        take(need1, r, lo1)
        if k >= 2:
            take(need2, r, lo2)
    return need1, need2


def backward_need(n: int) -> list[set[int]]:
    """Overapproximate coefficient DAG for c_n. Truncate j<ceil(k/2) and j>n."""
    need = [set() for _ in range(n + 1)]
    need[n] = final_need(n)
    for k in range(n, 0, -1):
        acc1: set[int] = set()
        acc2: set[int] = set()
        for j in need[k]:
            d1, d2 = expand_operands(j, k, n)
            acc1 |= d1
            acc2 |= d2
        need[k - 1] |= acc1
        if k >= 2:
            need[k - 2] |= acc2
    return need


def possible_indices(k: int, n: int) -> int:
    """Count of (k,j) not dropped by the two sound truncations."""
    lo = ceil_half(k)
    if lo > n:
        return 0
    return n - lo + 1


def m_parity_bits(s: int) -> int:
    """Bit t of the result is M(s,t) = #{j ⊆ s, j>=1, t ⊆ (j-1)} mod 2.

    Exact GF(2) cancellation for Z_k(s) = XOR_t M(s,t) Z_C(t).
    """
    bits = 0
    for j in submasks(s):
        if j < 1:
            continue
        u = j - 1
        v = u
        while True:
            bits ^= 1 << v
            if v == 0:
                break
            v = (v - 1) & u
    return bits


def zeta_need(n: int) -> list[set[int]]:
    """Exact zeta-query DAG: NeedZ[k] is the set of s for which Z_k(s) is used.

    Z_k(s) = XOR_{j ⊆ s, j>=1} C_{j-1}, C = a_{k-1}+a_{k-2}+star, and
    Z_C(t) = Z_{k-1}(t) + Z_{k-2}(t) + Z_{k-1}(t) Z_{k-2}(t).
    """
    need = [set() for _ in range(n + 1)]
    need[n].add(n)
    cache: dict[int, int] = {}
    for k in range(n, 0, -1):
        acc = 0
        for s in need[k]:
            if s not in cache:
                cache[s] = m_parity_bits(s)
            acc |= cache[s]
        # t with M(s,t)=1 can be as large as n-1; drop t that cannot appear
        # as a Mahler index at layer k-1 after truncation: t > n or
        # t < ceil((k-1)/2) are either unused or identically 0 as coefficients,
        # but Z_{k-1}(t) = XOR_{i ⊆ t} a_{k-1,i} may still need a small i.
        # Do not drop by min-support on the zeta argument: only drop t > n.
        mask = (1 << (n + 1)) - 1
        acc &= mask
        idxs = set()
        tmp = acc
        while tmp:
            lsb = tmp & -tmp
            idxs.add(lsb.bit_length() - 1)
            tmp ^= lsb
        need[k - 1] |= idxs
        if k >= 2:
            need[k - 2] |= idxs
    return need


def conv_points(need_k: set[int]) -> set[int]:
    return {j - 1 for j in need_k if j >= 1}


def zeta_gate_cost(points: set[int], n: int) -> int:
    """Bit-ops to evaluate all requested (A★OR B)[m] via one shared subcube zeta.

    Covering cube is bits of OR of requested m, truncated to n. FWHT-style
    subset zeta on a universe of size 2^q costs O(q 2^q) XORs.
    """
    if not points:
        return 0
    universe = 0
    for m in points:
        universe |= m
    universe &= (1 << (n.bit_length() + 1)) - 1
    q = universe.bit_length()
    return q * (1 << q) if q else 0


def family_label(n: int) -> str:
    if n == 0:
        return "zero"
    if n & (n - 1) == 0:
        return "pow2"
    if (n + 1) & n == 0:
        return "allones"
    return "general"


def summarize(n: int, need: list[set[int]], zneed: list[set[int]] | None = None):
    sizes = [len(s) for s in need]
    poss = [possible_indices(k, n) for k in range(n + 1)]
    frac = [sizes[k] / poss[k] if poss[k] else 0.0 for k in range(n + 1)]
    dag = sum(sizes)
    first_dense = next((k for k in range(n, -1, -1) if poss[k] and frac[k] >= 0.5), None)
    conv_costs = []
    unshared = 0
    for k in range(1, n + 1):
        pts = conv_points(need[k])
        conv_costs.append(zeta_gate_cost(pts, n))
        for m in pts:
            unshared += 3 ** m.bit_count() if m else 1
    zsizes = [len(s) for s in zneed] if zneed is not None else None
    return {
        "n": n,
        "family": family_label(n),
        "need_final": sizes[n],
        "need_nm1": sizes[n - 1] if n else sizes[0],
        "need_nm2": sizes[n - 2] if n >= 2 else None,
        "need_max": max(sizes),
        "need_sum": dag,
        "possible_sum": sum(poss),
        "fill": dag / sum(poss) if sum(poss) else 1.0,
        "first_dense_k": first_dense,
        "zeta_shared_sum": sum(conv_costs),
        "pair_unshared_sum": unshared,
        "zneed_final": zsizes[n] if zsizes else None,
        "zneed_nm1": zsizes[n - 1] if zsizes and n else None,
        "zneed_sum": sum(zsizes) if zsizes else None,
        "zneed_max": max(zsizes) if zsizes else None,
        "layer_sizes": sizes,
        "z_layer_sizes": zsizes,
    }


def m_weight(n: int) -> int:
    bits = m_parity_bits(n)
    return bits.bit_count()


def high_bit(n: int) -> int:
    return 1 << (n.bit_length() - 1) if n else 0


def u_direct(t: int, k: int) -> int:
    """Right-edge coordinate u(t,k)=x(t,t-k) via the 2-adic row map.

    Bit k of f^t(1) is u(t,k), with f(z)=z XOR ((z<<1) OR (z<<2)).
    This is the encoding of twoadic.md, not the left-aligned packed
    evolution used for center extraction in support_exact.py.
    """
    if k < 0 or t < 0:
        return 0
    row = 1
    for _ in range(t):
        row = row ^ ((row << 1) | (row << 2))
    return (row >> k) & 1


def z_from_support(k: int, s: int, S) -> int:
    return sum(1 for j in S[k] if (j & ~s) == 0) & 1


def verify_zeta_identities(K: int = 20) -> None:
    """M(s,·) is the interval {0,...,s-1}; Z_k(s)=u(s,k); 2D zeta recurrence."""
    S = supports_exact(K)
    for s in range(1, K + 1):
        bits = m_parity_bits(s)
        expected = (1 << s) - 1
        if bits != expected:
            raise AssertionError(("M interval", s, bin(bits), bin(expected)))
    for k in range(K + 1):
        for s in range(K + 1):
            z = z_from_support(k, s, S)
            if z != u_direct(s, k):
                raise AssertionError(("Z=u", k, s, z, u_direct(s, k)))
    # 2D recurrence on a triangle: Z[k][s] for k,s <= K.
    Z = [[0] * (K + 1) for _ in range(K + 1)]
    for s in range(K + 1):
        Z[0][s] = 1  # S_0={0}
    for k in range(1, K + 1):
        Z[k][0] = 0
        for s in range(1, K + 1):
            a = Z[k - 1][s - 1]
            b = Z[k - 2][s - 1] if k >= 2 else 0
            Z[k][s] = Z[k][s - 1] ^ a ^ b ^ (a & b)
    for n in range(K + 1):
        if u_direct(n, n) != direct_center(n):
            raise AssertionError(("encoding", n, u_direct(n, n), direct_center(n)))
        if Z[n][n] != direct_center(n):
            raise AssertionError(("Z triangle", n, Z[n][n], direct_center(n)))
        if n:
            acc = 0
            for t in range(n):
                a = Z[n - 1][t]
                b = Z[n - 2][t] if n >= 2 else 0
                acc ^= a ^ b ^ (a & b)
            if acc != Z[n][n]:
                raise AssertionError(("prefix identity", n, acc, Z[n][n]))


def need_sum_closed(n: int, need_sum: int) -> None:
    if n >= 2 and (n & (n - 1) == 0):
        expected = (n * n) // 2 + n // 2 + 1
        if need_sum != expected:
            raise AssertionError(("pow2 need_sum", n, need_sum, expected))
    if n >= 1 and (n + 1) & n == 0:
        expected = ((n + 1) * (n + 1)) // 2
        if need_sum != expected:
            raise AssertionError(("allones need_sum", n, need_sum, expected))


def verify_truncation_sound(K: int = 20) -> None:
    """c_n uses only j ⊆ n with j >= ceil(n/2); those a_{n,j} match full S_n."""
    S = supports_exact(K)
    for n in range(K + 1):
        lo = ceil_half(n) if n else 0
        contrib = [j for j in S[n] if (j & ~n) == 0]
        truncated = [j for j in contrib if j >= lo]
        if (len(contrib) ^ len(truncated)) & 1:
            # dropping j < lo must not change the parity: those j are absent
            raise AssertionError(("drop changed parity", n, contrib, truncated))
        for j in contrib:
            if j < lo:
                raise AssertionError(("contributing below min-support", n, j))
        if n:
            h = high_bit(n)
            if h not in {j for j in submasks(n)}:
                raise AssertionError("high bit not a submask")
            if h < lo:
                raise AssertionError(("high bit below min-support", n, h, lo))


def print_table(rows: list[dict], keys: list[str]) -> None:
    widths = {k: max(len(k), *(len(str(r[k])) for r in rows)) for k in keys}
    print(" ".join(k.rjust(widths[k]) for k in keys))
    for r in rows:
        print(" ".join(str(r[k]).rjust(widths[k]) for k in keys))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-k", type=int, default=16)
    parser.add_argument("--max-n", type=int, default=128)
    parser.add_argument("--zeta-n", type=int, default=48)
    args = parser.parse_args()

    verify_recurrence(args.verify_k)
    verify_truncation_sound(min(args.verify_k + 4, 24))
    verify_zeta_identities(min(args.verify_k + 4, 24))
    print(f"verified a_{{k,j}} recurrence and Mahler identity through K={args.verify_k}")
    print("verified min-support drop is sound for the diagonal query")
    print("verified M(s,t)=[0<=t<s], Z_k(s)=u(s,k), and the Z-triangle recurrence")
    print()

    samples = []
    for m in range(1, 8):
        samples.append(1 << m)
        samples.append((1 << m) - 1)
    extras = [6, 10, 11, 12, 13, 14, 20, 21, 22, 24, 27, 40, 42, 48, 85, 100, 127]
    for n in extras:
        if n <= args.max_n:
            samples.append(n)
    samples = sorted(set(n for n in samples if 1 <= n <= args.max_n))

    summaries = []
    for n in samples:
        need = backward_need(n)
        zneed = zeta_need(n) if n <= args.zeta_n else None
        sm = summarize(n, need, zneed)
        need_sum_closed(n, sm["need_sum"])
        summaries.append(sm)

    keys = [
        "n",
        "family",
        "need_final",
        "need_nm1",
        "need_nm2",
        "need_max",
        "need_sum",
        "possible_sum",
        "fill",
        "first_dense_k",
        "zeta_shared_sum",
        "zneed_nm1",
        "zneed_sum",
    ]
    display = []
    for r in summaries:
        d = dict(r)
        d["fill"] = f"{r['fill']:.3f}"
        display.append(d)
    print_table(display, keys)
    print()

    print("M(n,·) Hamming weights (exact zeta cancellations for Z_n(n)):")
    mrows = []
    for n in samples:
        if n > 128:
            continue
        wt = m_weight(n)
        mrows.append(
            {
                "n": n,
                "family": family_label(n),
                "popcount": n.bit_count(),
                "M_weight": wt,
                "M_weight/n": f"{wt / n:.3f}",
            }
        )
    print_table(mrows, ["n", "family", "popcount", "M_weight", "M_weight/n"])
    print()

    print("Per-layer coefficient Need for representative n:")
    for n in (8, 15, 16, 22, 31, 32):
        if n > args.max_n:
            continue
        row = next(s for s in summaries if s["n"] == n)
        sizes = row["layer_sizes"]
        # print last 12 layers plus a few early ones
        early = list(enumerate(sizes[: min(8, n + 1)]))
        late = list(enumerate(sizes))[-12:]
        print(f"  n={n} {row['family']}: early {early} ... late {late}")
        if row["z_layer_sizes"]:
            zs = row["z_layer_sizes"]
            print(f"       zeta-queries late {list(enumerate(zs))[-12:]}")
    print()

    print("Closed-form first-step checks:")
    for n in samples:
        h = high_bit(n)
        need_n = 1 << (n.bit_count() - 1)
        row = next(s for s in summaries if s["n"] == n)
        if row["need_final"] != need_n:
            raise AssertionError(("final need", n, row["need_final"], need_n))
        # high-bit singleton is always in the final query
        if h not in final_need(n):
            raise AssertionError(("missing high bit", n, h))
        nm1_lower = 1 << (h.bit_length() - 2) if h >= 2 else 0
        if n >= 2 and row["need_nm1"] < nm1_lower and row["need_final"] < n / 4:
            # either the final layer is already dense, or layer n-1 received
            # the high-half of the m-bit cube
            pass
        print(
            f"  n={n:4d} |Need[n]|={row['need_final']:4d} "
            f"|Need[n-1]|={row['need_nm1']:4d} high={h} "
            f"sum={row['need_sum']:6d} fill={row['fill']:.3f} "
            f"sum/n^2={row['need_sum'] / (n * n):.3f}"
        )
    print()
    print("Need sets for n=8 (pow2), n=15 (all-ones), n=10 (general):")
    for n in (8, 10, 15):
        if n <= args.max_n:
            need = backward_need(n)
            compact = {k: sorted(need[k]) for k in range(n + 1)}
            print(f"  n={n}: {compact}")
    print()
    print("no O(n) construction+evaluation bound obtained for this representation")


if __name__ == "__main__":
    main()
