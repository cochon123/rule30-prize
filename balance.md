# Rule 30 Problem 2: rigorous footholds and the gap

Use (F) for the global Rule-30 map and (c_t=(F^tdelta_0)_0), where

\[
 (Fx)_j=x_{j-1}\mathbin{\oplus}(x_j\lor x_{j+1})
       =x_{j-1}\oplus x_j\oplus x_{j+1}\oplus(x_jx_{j+1}).
\]

The prize statement is \(n^{-1}\sum_{t<n}c_t\to 1/2\). The official
statement and Wolfram's announcement are at [rule30prize.org](https://www.rule30prize.org/)
and [the 2019 announcement](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/).
OEIS records the sequence as [A051023](https://oeis.org/A051023) and its
partial sums as [A327982](https://oeis.org/A327982); the latter explicitly
notes that proving the ratio limit solves Problem 2.

## Exact lemma: every finite-time bit is unbiased in the Bernoulli ensemble

Let (X_j) be iid Bernoulli(1/2) on \(\mathbb Z\). For every (t\ge0),
\(Y_t=(F^tX)_0\) is Bernoulli(1/2).

Reason: Rule 30 is left-permutive: for fixed \((b,c)\), the map
\(a\mapsto a\oplus(b\lor c)\) is a bit flip. Iterating this property shows
that \((F^t x)_0\), as a Boolean function of the finite cone
\(x_{-t},\ldots,x_t\), is left-permutive in the extreme variable \(x_{-t}):
for each fixing of \(x_{-t+1},\ldots,x_t\), changing \(x_{-t}) changes the
output. Pairing the two assignments of \(x_{-t}) proves
\(\Pr(Y_t=1)=1/2\), hence \(E[Y_t]=1/2\) exactly.

The same fact can be phrased dynamically. Uniform Bernoulli measure is
preserved by every surjective one-dimensional CA (and left-permutivity gives
surjectivity), so \((F^tX)_0\) is a stationary process in time. If one could
prove ergodicity of this process (or of (F) for this observable), Birkhoff
would give time-average (1/2) for almost every *random* initial
configuration.

## Why this does not solve the prize problem

The single seed \(\delta_0\) is a measure-zero initial configuration. An
almost-sure statement under Bernoulli measure gives no information about this
particular orbit. Also, the one-time unbiasedness above says nothing about
correlations among (Y_t); independent-looking marginals do not imply a law
of large numbers. Thus replacing the finite seed by a “random-looking” or
ergodic argument is an invalid proof of Problem 2.

## Possible analytic target

It would suffice to prove a deterministic discrepancy bound
\[
 D(n):=\sum_{t<n}(2c_t-1)=o(n).
\]
The left-permutive pairing only pairs *spatial initial configurations*, not
the times \(t\) in the fixed finite-seed triangle. A useful intermediate
result would be a block/cylinder involution on the single-seed spacetime cone
whose boundary cost is (o(n)); no such involution is currently established.

Numerics in the official announcement (up to (10^6) and (10^9) bits) are
evidence only and cannot replace this missing deterministic step.

## Dyadic discrepancy criterion

Write (a_t=2c_t-1), (D(N)=sum_{t<N}a_t), and define
\[
 A_m=\max_{0\le h\le2^m}|D(2^m+h)-D(2^m)|.
\]
Then the desired conclusion is exactly equivalent to (A_m=o(2^m)).
Necessity is immediate: if (D(N)=o(N)), then uniformly for
(2^m\le N\le2^{m+1}), both (D(N)) and (D(2^m)) are (o(2^m)).
Conversely, (D(2^{m+1})-D(2^m)) is bounded by (A_m), hence
(D(2^m)=D(1)+sum_{j<m}O(A_j)=o(2^m)) whenever (A_j=o(2^j)).
For any (N\in[2^m,2^{m+1}]), this endpoint estimate plus the definition
of (A_m) gives (D(N)=o(2^m)=o(N)).

A condition such as (E_k=\sup_q|B(q,k)|=o(2^k)) for every translated aligned
dyadic block is valid but much too strong: a typical iid sequence has runs of
(+1)'s of every fixed length somewhere, making that supremum attain (2^k).
Endpoint control (D(2^m)=o(2^m)) alone is insufficient. Set (a_0=+1,a_1=-1),
and on each annulus ([2^m,2^{m+1})) for (m\ge1), use (+1) on the first
half and (-1) on the second. Then (D(2^m)=0) for every (m\ge1), but at
(N=3\cdot2^{m-1}), (D(N)=2^{m-1}), so (D(N)/N\to1/3) along that
subsequence.

## Experiment audit

`experiment.py` passes its independent dictionary-reference self-check and
uses the convention (x(0,0)=1), sampling (t=0,…,n-1). The packed-period
comparison has the right bit orientation; BM checks are finite evidence only.
The bit-packed update in `center_bits` is algebraically different in appearance
from the comment in `right_edge_periods`, but it produces the same center bits
and is verified against the direct reference through 256 steps. No counting or
Berlekamp–Massey convention bug was found. The only documentation issue is
that the two equivalent-looking spatial encodings should state their differing
bit-coordinate orientations explicitly.
