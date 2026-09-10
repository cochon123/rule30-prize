"""Exact Mahler-support recurrence for the Rule-30 right-edge form.

S[k] stores indices j whose b_j(t)=binomial(t,j) mod 2 term has odd
coefficient in u(t,k).  The OR-product is counted with multiplicity mod 2.
"""
from collections import Counter


def supports(K):
    S = [{0}]
    for k in range(1, K + 1):
        a = S[k - 1]
        b = S[k - 2] if k >= 2 else set()
        counts = Counter(i | j for i in a for j in b)
        star = {j for j, count in counts.items() if count & 1}
        S.append({j + 1 for j in (a ^ b ^ star)})
    return S


def direct_center(n):
    row = 1
    for _ in range(n):
        row = (row << 2) ^ ((row << 1) | row)
    return (row >> n) & 1


def main(K=35):
    S = supports(K)
    for n, support in enumerate(S):
        mahler = sum((j & ~n) == 0 for j in support) & 1
        if mahler != direct_center(n):
            raise AssertionError((n, mahler, direct_center(n)))
        print(n, len(support), max(support, default=-1), mahler)


if __name__ == "__main__":
    main()
