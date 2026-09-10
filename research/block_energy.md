# Mesoscopic block energy on the seed orbit

Attack on prize problem 2 via the Cauchy–Schwarz block-energy bound of
[balance.md](../balance.md). No density theorem is obtained, and this is
not a prize claim. Grouping pairwise correlations does **not** manufacture
a cancellation identity on the single-seed orbit.

Helper: `python3 research/block_energy.py --bits 262144`.
It does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.
The packed generator is checked against `experiment.center_bits` on a
prefix of 256 bits, and the lag-1 CA identity is checked at every measured
time.

## Target

Write \(a_t=2c_t-1\), \(N=2^m\), \(L=2^{\lfloor m/2\rfloor}\), and partition
the annulus \([N,2N)\) into \(B=N/L\) blocks of length \(L\). Set

\[
S_{m,b}=\sum_{t=N+bL}^{N+(b+1)L-1}a_t,\qquad
E_m=\sum_{b=0}^{B-1}S_{m,b}^2.
\]

Let \(A_m=\max_{0\le h\le N}|D(N+h)-D(N)|\) as in `balance.md`. Density
\(n^{-1}\sum_{t<n}c_t\to 1/2\) is equivalent to \(A_m=o(N)\).

## Proved bound: Cauchy–Schwarz reduction

A prefix of the annulus is \(k\) complete blocks plus a remainder of
length \(r<L\). Cauchy–Schwarz on those \(k\) block sums gives

\[
\Bigl|\sum_{b<k}S_{m,b}\Bigr|
\le\sqrt{k}\sqrt{\sum_{b<k}S_{m,b}^2}
\le\sqrt{B\,E_m},
\]

and the remainder is at most \(L\) in absolute value. Therefore

\[
A_m\le\sqrt{B E_m}+L.
\]

Since \(L=o(N)\), the condition \(E_m=o(NL)\) implies \(A_m=o(N)\). A
quantitative form is \(E_m\le C N L^{1-\delta}\) for some \(\delta>0\),
which yields \(A_m=O(N L^{-\delta/2})\).

This criterion is **sufficient and strictly stronger than density**. It is
not necessary: block signs may cancel in the running sum even if many
blocks are large. On the measured orbit the Cauchy–Schwarz envelope is
about ten times \(A_m\) (table below), so the energy target is a genuine
strengthening, not a rewriting of \(A_m=o(N)\).

The trivial estimate \(|S_{m,b}|\le L\) gives only \(E_m\le NL\), hence
\(A_m\le N+L\), which is the useless bound already implied by \(|a_t|=1\).
No improvement of \(E_m\le NL\) is proved below.

## Pairwise expansion

Because \(a_t^2=1\) and \(a_t a_{t+h}=(-1)^{c_t\oplus c_{t+h}}\),

\[
E_m=N+2\sum_{h=1}^{L-1}C_m(h),
\]

where

\[
C_m(h)=\sum_{b=0}^{B-1}\sum_{\substack{t,\,t+h\\\text{in block }b}}
(-1)^{c_t\oplus c_{t+h}}.
\]

The inner \(t\)-sum has \(L-h\) terms per block, so \(|C_m(h)|\le B(L-h)\le N\).
Summing \(L\) such bounds recovers \(E_m\le N+NL\). The expansion is an
identity, not a cancellation: \(E_m=o(NL)\) is exactly the statement that
the average in-block correlation is \(o(1)\). That is a mesoscopic law of
large numbers for this orbit. Grouping the pairs by blocks does not force
the signs of \(C_m(h)\) to cancel.

## Haar increment (exact)

Let \(E_m(\ell)\) be the same energy with block length \(2^\ell\) instead of
the prescribed \(L\). Merging adjacent blocks of length \(\ell\) into length
\(2\ell\) gives the elementary identity

\[
E_m(\ell)=E_m(\ell/2)+2\sum_{b}S^{({\ell/2})}_{2b}\,S^{({\ell/2})}_{2b+1}.
\]

In particular \(E_m(1)=N\), and the prescribed \(E_m\) is \(N\) plus twice
the sum of these adjacent-block products from scale \(1\) up to \(L\).
A seed-valid cancellation would have to live in those cross terms (a sign
law, a factorisation, or a telescoping after some involution). None is
obtained.

## Disagreement is not an autonomous two-point equation

For a reference row \(b\) and disagreement \(e=a\oplus b\), the Rule 30
update is the formula recorded in [disagreement.md](disagreement.md):

\[
e'_j=e_{j-1}+(1+b_{j+1})e_j+(1+b_j)e_{j+1}+e_je_{j+1}
\]

over \(\mathrm{GF}(2)\). The two-time centre correlation is the special case
\(e_j(t)=x(t,j)\oplus x(t+h,j)\), so

\[
(-1)^{c_t\oplus c_{t+h}}=(-1)^{e_0(t)}.
\]

Advancing \(t\) by one applies the displayed update with background equal
to the actual row \(F^t\delta_0\). In \(\pm 1\) variables
\(\chi_j=(-1)^{e_j}\) this is the cocycle

\[
\chi'_0
=\chi_{-1}
\cdot\chi_0^{1+b_1}
\cdot\chi_1^{1+b_0}
\cdot(-1)^{e_0 e_1}.
\]

The background bits \(b_j=(F^t\delta_0)_j\) are not free Bernoulli bits;
they are the seed orbit. The quadratic factor \((-1)^{e_0 e_1}\) is not
optional. Consequently there is no closed linear recurrence for \(C_m(h)\)
and no ensemble in which one could average the background to zero. This is
the same obstruction as in `balance.md`: left-permutive pairing pairs
*spatial* initial configurations, not times on this orbit.

## Exact lag-1 identity (does not cancel in blocks)

The local rule gives \(c_{t+1}=x(t,-1)\oplus(c_t\lor r_t)\), hence

\[
c_t\oplus c_{t+1}
=x(t,-1)\oplus x(t,1)\oplus c_t r_t,
\]

and \(a_t a_{t+1}=(-1)^{l_t\oplus r_t\oplus c_t r_t}\). This identity is
checked at every time in the measurement. Summing it over a block is a
sum of a local function of \((l_t,c_t,r_t)\). Partitioning by the
background pair \((c_t,r_t)\) produces four buckets whose contributions do
not cancel against each other, nor against a fixed linear combination with
coefficients in \(\{0,\pm 1\}\).

The quadratic disagreement term \(e_0 e_1\) on consecutive times equals 1
on about \(1/4\) of in-block lag-1 pairs (table). Linearising the
disagreement update is therefore false on this orbit, not merely
unjustified.

## Closed forms that fail

On every annulus where every lag \(h<L\) was computed, the following
quantities are nonzero for all sufficiently large \(m\):

- \(\sum_h C_m(h)\) (would give \(E_m=N\) if it vanished identically),
- \(\sum_h C_m(h)+N/2\) (would give \(E_m=0\)),
- even-lag sum, odd-lag sum, and \(\sum_h(-1)^h C_m(h)\).

An accidental zero occurs at \(m=6\) (\(\sum C=0\)), and the odd-lag sum
at \(m=17\) is only \(-28\). Neither persists. Adjacent Haar products
change sign irregularly with scale and with \(m\).

## Measurements on the seed (finite, not a proof)

Times \(0\le t<262144\), single cell seed, prescribed \(L=2^{\lfloor m/2\rfloor}\).
\(E_m/(NL)\) is the mean square of the block bias \(S_{m,b}/L\). The
column \(E_m/N\) would stay \(O(1)\) for an iid \(\pm 1\) sequence
(\(S_{m,b}^2\sim L\), \(B=N/L\)). The Cauchy–Schwarz envelope is
\(\sqrt{BE_m}+L\).

| \(m\) | \(N\) | \(L\) | \(E_m\) | \(E_m/(NL)\) | \(E_m/N\) | \(A_m\) | \(A_m/N\) | CS\(/N\) | rms\(/\sqrt{L}\) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 256 | 16 | 276 | 0.06738 | 1.078 | 12 | 0.04688 | 0.322 | 1.038 |
| 10 | 1024 | 32 | 1280 | 0.03906 | 1.250 | 36 | 0.03516 | 0.229 | 1.118 |
| 12 | 4096 | 64 | 5264 | 0.02008 | 1.285 | 65 | 0.01587 | 0.157 | 1.134 |
| 14 | 16384 | 128 | 14312 | 0.00682 | 0.874 | 249 | 0.01520 | 0.090 | 0.935 |
| 15 | 32768 | 128 | 31544 | 0.00752 | 0.963 | 180 | 0.00549 | 0.091 | 0.981 |
| 16 | 65536 | 256 | 72656 | 0.00433 | 1.109 | 367 | 0.00560 | 0.070 | 1.053 |
| 17 | 131072 | 256 | 142224 | 0.00424 | 1.085 | 889 | 0.00678 | 0.067 | 1.042 |

The \(A_m\) values through \(N=32768\) match `results.json` dyadic annuli.
Through \(m=17\), \(E_m/N\) stays near 1 and \(E_m/(NL)\) decays like
\(1/L\). Haar energy as a function of block length stays the same order
from scale 2 through the prescribed \(L\) (and somewhat beyond); the
cross terms are \(O(N)\), not of size \(N\ell\). Mean in-block
correlations at lags \(1,2,4,\ldots\) are \(O(10^{-3})\) to \(O(10^{-2})\)
with irregular signs. The ratio \(|\sum C|/\sum|C|\) is small at large
\(L\) (0.05–0.11 for \(m=15,16,17\)), which is the size expected from
randomly signed \(C_m(h)\), not from a structured pairing.

These figures are compatible with a random-walk annulus. They do **not**
prove \(E_m=O(N)\), nor \(E_m=o(NL)\), nor density. A systematic bias of
size \(L^{-\delta/2}\) in a positive-density set of blocks would still be
invisible at these \(m\) for small \(\delta\), and a later annulus could
saturate.

Lag-1 background split \((c_t,r_t)\) on in-block pairs, and the rate at
which the quadratic disagreement bit \(e_0 e_1\) is 1:

| \(m\) | \(00\) | \(01\) | \(10\) | \(11\) | quadratic ones |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 14 | −104 | 82 | 54 | 32 | 4104/16256 |
| 15 | 83 | −128 | −51 | −76 | 8193/32512 |
| 16 | 155 | 172 | 10 | −47 | 16218/65280 |
| 17 | −338 | −204 | 38 | 210 | 32778/130560 |

No bucket is identically zero. The four-term sum is \(C_m(1)\), which
already fails to vanish. The quadratic term is occupied on \(24.8\%\) to
\(25.6\%\) of pairs, so the nonlinear piece of disagreement is not a
sparse error.

## Why this is stronger than density, and why it stops

Proving \(E_m=O(N)\) would in fact finish problem 2: Cauchy–Schwarz would
give \(A_m=O(N L^{-1/2})=O(N^{3/4})=o(N)\). That statement is a uniform
\(L^2\) bound on all mesoscopic blocks of length \(\sqrt{N}\). Density
only needs the running sum of those blocks to stay \(o(N)\). The attack
therefore aimed at a stronger theorem than the prize, using a rewriting
(pairwise / Haar) that is exact on every sequence in \(\{\pm 1\}^{\mathbb N}\).

No further identity is available from Rule 30 on this seed:

1. The pairwise and Haar expansions hold for an arbitrary \(\pm 1\)
   sequence. They cannot encode the CA.
2. The CA enters only through disagreement, whose update depends on the
   unknown background and a quadratic term that is empirically dense.
3. The one exact local correlation identity (lag 1) does not telescope
   or cancel after grouping by background bits.
4. Finite measurements that look like an iid energy cascade are the same
   species of evidence already recorded in `balance.md` and
   `results.json`. They are not a bound.

The missing step remains a deterministic pairing or mixing estimate that
uses the finite seed in an essential way. Block energy does not supply it.

**Outcome.** The only proved bounds are \(A_m\le\sqrt{BE_m}+L\) and the
trivial \(E_m\le NL\). No bound \(E_m=o(NL)\) (and no \(\delta>0\)) is
established. Grouping correlations does not manufacture cancellation. This
attack should stop.
