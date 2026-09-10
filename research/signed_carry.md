# Signed-digit weight of the ×7 correction stream

Attack on prize problem 3, as specified in [_astra_ideas6.md](_astra_ideas6.md)
item 4. The integer identity \(Z_{t+1}=7Z_t-2Q_t\) holds, but the
correction stream is not sparse in signed binary. This is not a prize
claim. The identity alone is not acceleration.

Certifier: `research/signed_carry.py`. Dump: `research/signed_carry.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

## Identity

Pack the row from the right edge as \(Z_t=\sum_{k\ge 0}x(t,t-k)\,2^k\),
so bit \(k\) is \(u(t,k)\) in the edge coordinates of the announcement,
bit \(0\) is identically 1, and the centre is bit \(t\). The local rule
is the integer XOR-OR update \(Z\mapsto Z\oplus((Z\ll 1)\lor(Z\ll 2))\).
Checked against `experiment.center_bits` through time 80.

Write \(U=Z_t\land(Z_t\ll 1)\), \(V=Z_t\land(Z_t\ll 2)\),
\(W=Z_t\land(Z_t\ll 1)\land(Z_t\ll 2)\), and \(Q_t=2U+V-W\). Then

\[
Z_{t+1}=7Z_t-2Q_t
\]

holds exactly as integers through the same range (maximum absolute error
0). Unrolling from \(Z_0=1\) gives
\(Z_n=7^n-2\sum_{t<n}7^{n-1-t}Q_t\). Only this expression modulo
\(2^{n+1}\) is needed for \(c_n\). Modular exponentiation supplies the
homogeneous term. The corrections are the whole question.

## Signed-binary weight

Digits \(\{-1,0,1\}\). The weight \(w_\pm\) of a residue class modulo
\(2^n\) is the minimum non-adjacent-form weight among \(Q_t\bmod 2^n\),
that representative minus \(2^n\), and that representative plus \(2^n\).
NAF is a minimum-weight signed-binary expansion. The family was frozen
before measurement. Self-check: \(w_{\mathrm{NAF}}(0,1,2,3,5,6,7,43)=(0,1,1,2,2,2,2,4)\).

\[
S(n)=\sum_{t<n}w_\pm(Q_t\bmod 2^n).
\]

| \(n\) | \(S(n)\) | \(S(n)/n^2\) | \(0.05n^2\) |
| ---: | ---: | ---: | ---: |
| 128 | 3103 | 0.1895 | 819.2 |
| 256 | 12214 | 0.1864 | 3276.8 |
| 512 | 49650 | 0.1893 | 13107.2 |

Mean weight per time is \(\approx 0.19n\), about one fifth of the bits,
not a sparse signed-digit source. Generating each \(Q_t\) used the packed
row at that time.

## Why it died

Preregistered kill: \(S(n)>0.05n^2\) at both \(n=256\) and \(n=512\).

Both fire. There is no sparse correction stream to update by local
carry rules. The displayed identity is exact and does not compress the
work. Not a prize claim.
