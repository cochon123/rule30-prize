from collections import Counter


def zeta(a, q):
    a = a[:]
    for bit in (1 << r for r in range(q)):
        for mask in range(len(a)):
            if mask & bit:
                a[mask] ^= a[mask ^ bit]
    return a


def or_product(a, b, q):
    za, zb = zeta(a, q), zeta(b, q)
    zc = [x & y for x, y in zip(za, zb)]
    return zeta(zc, q)  # zeta is its own inverse over GF(2)


def supports(N):
    q = (N + 1).bit_length()
    size = 1 << q
    S = [[0] * size for _ in range(N + 1)]
    S[0][0] = 1
    for k in range(1, N + 1):
        a, b = S[k - 1], S[k - 2] if k >= 2 else [0] * size
        p = or_product(a, b, q)
        # Inc and truncate: output index j+1 <= N.
        S[k] = [0] + [p[j - 1] ^ a[j - 1] ^ b[j - 1] for j in range(1, N + 1)] + [0] * (size - N - 1)
    return S


def direct_bits(N):
    row, out = 1, []
    for t in range(N + 1):
        out.append((row >> t) & 1)
        row = (row << 2) ^ ((row << 1) | row)
    return out


if __name__ == '__main__':
    N = 512
    S = supports(N)
    bits = direct_bits(N)
    for n, row in enumerate(S):
        got = sum(row[j] for j in range(n + 1) if j & ~n == 0) & 1
        assert got == bits[n], (n, got, bits[n])
    print('verified', N + 1, 'center bits')
