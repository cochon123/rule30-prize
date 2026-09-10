# 2-adic valuations and OR-overlaps of the packed Rule 30 row

Attack on prize problem 3 (maybe 1). This is not the signed ×7 identity
\(Z_{t+1}=7Z_t-2Q_t\) of [signed_carry.md](signed_carry.md), and not the
residue periods of \(f\) on \(\mathbb Z_2\) in [twoadic.md](twoadic.md)
(fixed low bits; no centre extraction). It asks whether the orbit of the
packed integer itself has sparse nonlinear sites or a cheap valuation
formula for \(c_t\). This is not a prize claim.

Certifier: `research/packed_valuation.py`. Dump:
`research/packed_valuation.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Packing

Primary: right-edge coordinates \(u(t,k)=x(t,t-k)\), packed as

\[
z_0=1,\qquad z_{t+1}=z_t\oplus\bigl((z_t\ll 1)\lor(z_t\ll 2)\bigr).
\]

Bit \(k\) is the cell \(k\) steps left of the right edge. The centre is
bit \(t\). The orbit begins \(1,7,25,111,401,\ldots\), matching
[twoadic.md](twoadic.md) and the centre column of
`experiment.center_bits` through time 80.

Secondary: the `experiment.py` packing
`row=(row<<2)^((row<<1)|row)`, LSB = left edge. It is the bit-reversal
of the \(2t+1\)-bit right-edge word. Overlap counts \(N_t\) agree
exactly. The two packings differ by left versus right growth.

## Overlaps and carries

Write \(a=z\ll 1\) and \(b=z\ll 2\). The OR in \(f\) is nonlinear exactly
where \(a\) and \(b\) both have a 1:

\[
N_t=\operatorname{popcount}\bigl((z\ll 1)\land(z\ll 2)\bigr)
=\operatorname{popcount}\bigl(z\land(z\ll 1)\bigr).
\]

That is the number of adjacent `11` pairs, equivalently (ones) minus
(the number of 1-runs). Carry-ins of the integer add \(a+b=6z\) are

\[
K_t=\operatorname{popcount}\bigl(\bigl((a+b)\oplus a\oplus b\bigr)\gg 1\bigr).
\]

XOR-collision sites of the outer \(\oplus\) are
\(M_t=\operatorname{popcount}\bigl(z\land((z\ll 1)\lor(z\ll 2))\bigr)\).

A sparse-carry evaluator would need \(N_t=O(1)\) or \(O(\log t)\).

| \(T\) | \(\operatorname{mean}_t N_t/t\) | \(N_T/T\) | late min \(N_t/t\) | \(\operatorname{mean} K_t/t\) | \(\operatorname{mean} M_t/t\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 256 | 0.534 | 0.547 | 0.358 | 1.047 | 0.772 |
| 1024 | 0.507 | 0.521 | 0.401 | 1.015 | 0.758 |
| 4096 | 0.503 | 0.520 | 0.455 | 1.005 | 0.753 |
| 16384 | 0.501 | 0.501 | 0.471 | 1.001 | 0.751 |

Late means \(t\in[T/2,T)\). Pearson correlation of \(N_t\) with \(c_t\)
through \(T=16384\) is \(0.014\). Mean \(N_t/t\) given \(c_t=0\) or \(1\)
differs by \(0.001\). Parity of \(N_t\) agrees with \(c_t\) on
\(8178/16384\approx 1/2\) of times. No cheap formula in the frozen
family (\(\operatorname{popcount}(t)\), \(t/2\), \(t\), \((3t)/5\),
ones minus 1) matches \(N_t\).

## Valuations

\(z_t\) is always odd (both edges of the single-cell seed are 1). Hence
the listed valuations collapse:

| quantity | value on this orbit |
| --- | --- |
| \(v_2(z_{t+1}\oplus z_t)\) | \(1\) for every \(t\) |
| \(v_2(z_t\oplus(z_t\ll 1))\) | \(0\) for every \(t\) |
| \(v_2(z_t\oplus 2^t)\) for \(t>0\) | \(0\) (does **not** extract \(c_t\)) |
| \(v_2(z_t-2^k)\) for \(k\ge 1\) | \(0\) (odd minus even) |
| \(v_2(z_t+1)\) | \(1\) on even \(t\); \(\ge 3\) on odd \(t\) |
| experiment packing \(v_2(z_t+1)\) | \(2\) for all \(t\ge 2\) |
| \(v_2(z_t\gg t)=0\) | iff \(c_t=1\) |

The last line is exactly \((z\gg t)\land 1\): it reads bit \(t\) of the
packed row and secretly reconstructs the centre from the whole word.

The experiment-packing question is settled in the negative:
\(v_2(z_t\oplus(1\ll t))=0\) for every \(t>0\), in both packings,
because the XOR does not touch the LSB. It does not extract the centre.

### Exact identity (all odd \(z\), not just the orbit)

Let \(f(z)=z\oplus((z\ll 1)\lor(z\ll 2))\). For every odd integer \(z\),

\[
v_2\bigl(f(z)-1\bigr)=v_2(z+1).
\]

Proof. Let \(k=v_2(z+1)\), so bits \(0,\ldots,k-1\) of \(z\) are 1 and
bit \(k\) is 0. Then \(f(z)_i=z_i\oplus(z_{i-1}\lor z_{i-2})\). Direct
inspection of bits \(0,\ldots,k\) gives \(f(z)\equiv 1+2^k\pmod{2^{k+1}}\),
hence \(v_2(f(z)-1)=k\). Checked on every odd residue mod \(2^{12}\) and
on the orbit through \(t=16384\). On the orbit this is
\(v_2(z_t-1)=v_2(z_{t-1}+1)\). It only constrains the right-edge 1-run
and does not yield \(c_t\).

The even-\(t\) evaluation \(v_2(z_t+1)=1\) is the mod-8 cycle of
[twoadic.md](twoadic.md): \(f^t(1)\equiv 1\pmod 8\) for even \(t\).
Thresholds \(\{v_2(z_t+1)\ge k\}\) are periodic with period dividing
\(2^{k-1}\) (same source: offset \(k-1\) has period dividing \(2^{k-1}\)).
Measured min-periods through \(t=16384\): \(1,2,2,4,8,8,16,32\) for
\(k=1,\ldots,8\). The integer sequence itself is unbounded (max \(37\)
at \(t=16383\)) and is not a ruler function of \(t\) in the frozen
family. Linear complexity of \(N_t\bmod 2\) at \(n=8192\) is \(4098\),
matching \(c_t\) (\(4096\)).

## Why it died

Preregistered kill: mean \(N_t/t\) stays above \(0.05\) at both
\(T=4096\) and \(T=16384\) (analogue of the ×7 kill
\(S(n)/n^2>0.05\)).

Both fire: \(0.503\) and \(0.501\). Late-window minima remain above
\(0.45\). The nonlinear core is a positive-density subset of the row.
There is no sparse-carry evaluator.

Valuation sequences are either constant / period-2 (fixed offsets,
already in twoadic.md) or have unbounded linear complexity comparable
to \(c_t\). The only identity that returns \(c_t\) reads bit \(t\) of
\(z_t\). Not a prize claim.

Wall time: \(0.34\) seconds for \(T=16384\) (stdlib, exact integers).
The \(t=10^5\) extension was not run: \(N_t\) is not \(O(\log t)\).
