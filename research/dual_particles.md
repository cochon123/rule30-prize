# Dual particles and last-step pairing

Attack on prize problem 2 via the Walsh pullback of Rule 30. No density
theorem is obtained, and this is not a prize claim. Helper:
`python3 research/dual_particles.py`. It does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

This is not the block-energy pairing of [block_energy.md](block_energy.md).
That argument grouped pairwise correlations of the centre column and never
produced a sign-reversing identity on the seed orbit. The object here is
the dual branching process of finite particle sets, and the pairing is
tested against **seed evaluation** \(\varphi\), not against an ensemble
average.

## Spin identity (corrected)

Write \(s_j=(-1)^{x_j}\). The assignment quoted

\[
s'_j=\tfrac12 s_{j-1}(1+s_j+s_{j+1}-s_js_{j+1}),
\]

which equals \(s_{j-1}(-1)^{x_j x_{j+1}}\) and is Rule 30 on only four of
the eight neighbourhoods. The identity that holds on all eight is

\[
s'_j=\tfrac12 s_{j-1}(-1+s_j+s_{j+1}+s_js_{j+1})
=s_{j-1}(-1)^{x_j\lor x_{j+1}}.
\]

Expanding the parenthesis gives four monomials. One particle at site \(j\)
branches to four particle sets, with weights \(-\tfrac12,+\tfrac12,+\tfrac12,+\tfrac12\):

| name | extra sites | set emitted | weight |
| --- | --- | --- | --- |
| L | none | \(\{j-1\}\) | \(-\frac12\) |
| C | \(j\) | \(\{j-1,j\}\) | \(+\frac12\) |
| R | \(j+1\) | \(\{j-1,j+1\}\) | \(+\frac12\) |
| B | \(j\) and \(j+1\) | \(\{j-1,j,j+1\}\) | \(+\frac12\) |

The assignment’s weight pattern \(+\frac12,+\frac12,+\frac12,-\frac12\) is
the AND-polynomial, not Rule 30. Products of several particles are
evaluated with \(s_k^2=1\), i.e. symmetric difference of supports. Empty
products are \(1\).

## Dual operator and the discrepancy

For finite \(A\subset\mathbb Z\) set \(\chi_A=\prod_{j\in A}s_j\). Pullback
along one Rule 30 step defines a signed linear operator \(K\) on the real
vector space with basis \(\{[A]\}\):

\[
\chi_A\circ F=\sum_B K_{A,B}\,\chi_B,\qquad
K[A]=\sum_B K_{A,B}[B].
\]

Seed evaluation is \(\varphi(A)=(-1)^{1_{0\in A}}\), because the initial
row is \(s_0=-1\) and \(s_j=+1\) for \(j\neq 0\). Let \(v=[\{0\}]\). Then

\[
\varphi(K^t v)=(-1)^{c_t},\qquad
D(N)=-\Bigl\langle\sum_{t<N}K^t v,\,\varphi\Bigr\rangle.
\]

Checked against `experiment.center_bits` through \(t=5\) (and the
one-step identity on all eight neighbourhoods). Every monomial of
\(K^t v\) contains \(-t\): the leftmost particle always emits its left
neighbour, and nothing lies further left to cancel it. Distinct times
therefore occupy disjoint basis vectors.

## One dual step

\[
K[\{0\}]
=-\tfrac12[\{-1\}]
+\tfrac12[\{-1,0\}]
+\tfrac12[\{-1,1\}]
+\tfrac12[\{-1,0,1\}].
\]

Contributions to \(\varphi\): \(-\frac12,-\frac12,+\frac12,-\frac12\),
sum \(-1=(-1)^{c_1}\). The equal-weight, opposite-\(\varphi\) pair is
C \(\leftrightarrow\) R, not L \(\leftrightarrow\) C. The latter would
have been the assignment’s pairing; on the true polynomial L and C have
opposite weights, so toggling origin occupancy **preserves** the sign of
the seed-evaluated term and doubles it.

## Exact cancellation: last-step C \(\leftrightarrow\) R

**Lemma.** Let \(A\) be any finite set. Write \(K[A]\) by expanding every
particle independently, then multiplying (symmetric difference).

1. If \(0\in A\), then for every fixed choice of branches of
   \(A\setminus\{0\}\), the C and R branches of the origin particle have
   equal weight \(+\frac12\) and opposite seed evaluation. Their
   \(\varphi\)-contributions cancel.
2. If \(0\notin A\) and \(-1\in A\), the same holds for C and R of the
   particle at \(-1\).

**Proof.** Let \(P\) be the set emitted by all particles other than the
distinguished one. Origin C produces \(P\Delta\{-1,0\}\), origin R
produces \(P\Delta\{-1,1\}\). Exactly one of these contains \(0\),
according as \(0\notin P\) or \(0\in P\). Weights agree, so
\(\varphi(\mathrm{C})+\varphi(\mathrm{R})=0\). If the distinguished
particle is \(-1\), C produces \(P\Delta\{-2,-1\}\) and R produces
\(P\Delta\{-2,0\}\); again exactly one contains \(0\). \(\square\)

Thus \(\varphi\circ K=\varphi\circ K_\flat\), where \(K_\flat\) retains
only the L and B branches of the distinguished particle (origin if
present, else \(-1\) if present) and the full four-branch \(K\) on every
other particle. If \(A\cap\{-1,0\}=\emptyset\), then \(K_\flat=K\): no
last-step C/R move can flip origin occupancy. In that case \(\varphi\)
is constant on the whole last-step fan, equal to \((-1)^{1_{1\in A}}\).

On the seed, the first row is \(1\) exactly on \(\{-1,0,1\}\), so
\(\varphi(K[A])=(-1)^{|A\cap\{-1,0,1\}|}\). The lemma is compatible with
this closed form; it does not use the rest of the orbit.

L \(\leftrightarrow\) B also flips origin occupancy, but the weights are
\(-\frac12\) and \(+\frac12\). Seed-evaluated contributions have the
**same** sign and add. That pair is not a cancellation.

## Two dual steps

\[
\begin{align*}
K^2[\{0\}]
&=\tfrac14\sum_{S\subseteq\{1,2\}}[\{-2\}\cup S]
+\tfrac14\sum_{\emptyset\neq S\subseteq\{1,2\}}[\{-2,-1,0\}\cup S]\\
&\qquad-\tfrac34[\{-2,-1,0\}].
\end{align*}
\]

Eight monomials, \(\varphi(K^2 v)=+1=(-1)^{c_2}\). The involution
\(\tau(A)=A\Delta\{-1,0\}\) identifies

\[
[\{-2\}\cup S]
\quad\text{with}\quad
[\{-2,-1,0\}\cup S]
\]

at equal weight \(+\frac14\) for every nonempty \(S\subseteq\{1,2\}\).
Each such pair has opposite \(\varphi\). Three pairs cancel. The
unpaired remainder is

\[
\rho=\tfrac14[\{-2\}]-\tfrac34[\{-2,-1,0\}],\qquad\varphi(\rho)=1.
\]

This is the same \(\varphi\) as the full two-step vector: the pairing
removes six of eight monomials and does not reduce the seed-evaluated
mass.

## Time-summed involution and unpaired boundary

A history of duration \(t\) is a chain of branch choices from \(\{0\}\)
through \(t\) pullbacks, with weight the product of the local
\(\pm\frac12\) and final set the symmetric difference of all emissions.
The time-sum \(\sum_{t<N}K^t v\) is the signed measure on all histories
with \(0\le t<N\).

**Involution \(\iota\), last-step orientation.** If \(t\ge 1\) and the
particle set \(A^{(1)}\) immediately before the seed-adjacent step meets
\(\{0\}\) (or else \(\{-1\}\)), and the distinguished particle chose C or
R, swap C \(\leftrightarrow\) R and leave every other choice fixed. This
is an involution, preserves the signed weight, and flips \(\varphi\).
Paired histories cancel in \(\langle\sum_{t<N}K^t v,\varphi\rangle\).

**Unpaired boundary.**

- Last distinguished branch in \(\{\mathrm{L},\mathrm{B}\}\).
- Last-layer sets with \(A^{(1)}\cap\{-1,0\}=\emptyset\) (the C/R move
  does not exist). For \(t=2\) these are exactly the four origin-free
  monomials in the display above; three of them still cancel against
  \(\tau\)-partners, leaving \(\rho\).
- The \(t=0\) history \([\{0\}]\), which has no last branch.
- No further unpaired cut at \(t=N\) arises from \(\iota\), because
  \(\iota\) never changes duration. Distinct times cannot share a
  monomial: every class at time \(t\) contains \(-t\).

After \(\iota\), the net \(\varphi\)-weight at each fixed \(t\) is still
\((-1)^{c_t}\). The involution does not pair opposite-sign times.

## Residual recursion

Let \(v_t=K^t v\). The lemma gives, for \(t\ge 1\),

\[
(-1)^{c_t}=\varphi(v_t)=\varphi(K_\flat v_{t-1}).
\]

When \(0\in A\), this is the two-term rule

\[
\varphi(K[A])=\varphi\bigl(\tfrac12(B_0-L_0)\,K[A\setminus\{0\}]\bigr)
=-\varphi(L_0 K[A\setminus\{0\}]),
\]

and likewise with particle \(-1\) if the origin is vacant. Substituting
\(A=\{0\}\) recovers

\[
(-1)^{c_t}
=-\tfrac12\,\varphi(K^{t-1}[\{-1\}])
+\tfrac12\,\varphi(K^{t-1}[\{-1,0,1\}]).
\]

This is an identity, not a contraction: the right-hand side has absolute
value \(1\). Intermediate C/R rewrites are **not** seed-eval reversing,
because \(\varphi\) sees only the initial row. One cannot replace every
factor of \(K\) by \(K_\flat\) and iterate. In particular
\(\varphi\circ K^2=\varphi\circ K_\flat^{(2)}\) on two seed-adjacent
steps (the \(\tau\)-pairing), but
\(\varphi(K^{t-2}\gamma)\) need not vanish when \(\varphi(\gamma)=0\).

The leftover \(\ell^1\) mass after the monomial involution
\(A\mapsto A\Delta\{-1,0\}\) on \(K^t v\) grows with \(t\) (measured
\(1,2,1,15/4,83/16,359/32\) for \(t=0,\ldots,5\)). It does not supply an
\(O(N^\alpha)\) envelope with \(\alpha<1\).

## Why this dies

The missing step for \(D(N)=o(N)\) is a pairing of **times** on this
orbit, or any other bound on unpaired weight strictly sublinear in \(N\).
What was obtained is a last-step identity on particle histories.

1. C \(\leftrightarrow\) R is a genuine seed-eval reversing involution,
   and the two-step \(\tau\)-pairing is a genuine monomial identity.
   Both are exact. Both live in the seed-adjacent layer.
2. After those cancellations, each time still contributes
   \(\varphi\)-weight \(\pm 1\). The time-sum of unpaired weight is
   \(\sum_{t<N}(-1)^{c_t}=-D(N)\), which is the original series.
3. Supports at different \(t\) are disjoint, so collapsing monomials in
   \(\sum_{t<N}K^t v\) cannot mix times. A duration-changing involution
   would have to match a weight-\(1\) history to a weight-\(\pm\frac12\)
   extension; L/B extensions have the wrong relative sign for
   cancellation, and no other single branch has weight of modulus \(1\).
4. The residual recursion does not compose. It is the CA, rewritten at
   the last dual step. No cancellation gain is demonstrated.

The same obstruction recorded in [balance.md](../balance.md) reappears
in dual variables: left-permutive pairing (here, C \(\leftrightarrow\) R)
pairs branches of the initial character expansion, not times along the
seed orbit. Block energy failed by grouping correlations that do not
cancel. This attack fails by cancelling everything that *does* cancel
and leaving a residual whose seed-evaluated mass is still \(1\) per time.

**Outcome.** Exact identities: the corrected four-branch pullback; last-step
C \(\leftrightarrow\) R cancellation; the two-step closed form and
\(\tau\)-pairing with residual \(\rho\). No bound \(D(N)=o(N)\), and no
unpaired-weight bound \(O(N^\alpha)\) with \(\alpha<1\). \(D(N)=o(N)\) is
not closer. This attack should stop.
