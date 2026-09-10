# Cartier operators on the right-edge generating function

Attack on prize problem 1 via the 2-kernel of the center generating
function, as proposed in [_astra_ideas4.md](_astra_ideas4.md) item 4.
No infinite distinct-kernel family is proved. Nonautomaticity is not
proved. This is not a prize claim.

Helper: `python3 research/cartier_kernel.py --bits 65536 --output research/cartier_kernel.json`.
It does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.
The packed generator is checked against the right-edge triangle on a
prefix of 48 bits. The bivariate identity, the four Cartier images, the
first `R`-equation, and the independence of skip products from adjacent
pairs are checked on a `64×64` triangle.

Do not retread the Mahler-support DAG of
[mahler_dependency.md](mahler_dependency.md). The objects here are
arithmetic subsequences of `c`, not coefficient supports `S_k`.

## Target

Write `v(t,k)=x(t,t-k)` over \(\mathbb F_2\), with `v(t,k)=0` for `k<0`
and `v(t,0)=1`. The center is the diagonal `v(n,n)=c_n`. Set

\[
U(z,w)=\sum_{t,k\ge0}v(t,k)\,z^tw^k,\qquad
R(z,w)=\sum_{t,k\ge0}v(t,k)v(t,k+1)\,z^tw^k.
\]

The right-edge recurrence `v'=v+(v_{\leftarrow}\lor v_{\leftarrow\leftarrow})`
and `p\lor q=p+q+pq` give the exact identity

\[
(1+z+zw+zw^2)\,U=1+zw^2 R
\]

in \(\mathbb F_2[[z,w]]\). (The `t=0` slice of `U` is `1`; the `t=0`
slice of `R` is `0`.) Verified with no interior mismatches on the
`64×64` truncation.

Let `C(z)=\operatorname{Diag} U=\sum_n c_n z^n`. The four bivariate
Cartier operators are

\[
\Lambda_{\varepsilon\delta}F=\sum_{i,j}[z^{2i+\varepsilon}w^{2j+\delta}]F\cdot z^iw^j,
\qquad\varepsilon,\delta\in\{0,1\}.
\]

Equal-index operators commute with the diagonal:

\[
\Lambda_r C=\operatorname{Diag}\Lambda_{r,r}U.
\]

A sequence over a finite alphabet is 2-automatic if and only if its
2-kernel is finite (Christol; Allouche–Shallit). Eventually periodic
sequences are 2-automatic. An infinite family of pairwise distinct
iterated Cartier images of `C` would therefore prove that `c` is not
2-automatic, hence not eventually periodic. That is a strictly stronger
target than problem 1. The language is that of
[Rowland–Yassawi](https://jtnb.centre-mersenne.org/item/10.5802/jtnb.901.pdf);
nothing from that paper is claimed for Rule 30.

Witnesses are required on \(\operatorname{Diag}(WU)\). A difference
between two bivariate images that vanishes after taking the diagonal
does not distinguish kernel states of `C`.

## Four Cartier images of the identity

Write `U_{\varepsilon\delta}=\Lambda_{\varepsilon\delta}U` and likewise
for `R`. Substituting the even/odd splitting

\[
U=U_{00}(z^2,w^2)+z\,U_{10}(z^2,w^2)+w\,U_{01}(z^2,w^2)+zw\,U_{11}(z^2,w^2)
\]

into `PU` and extracting parities yields, after the substitution
`Λ_{00}(z^2 w^2 F(z^2,w^2))=zw\,F(z,w)`,

\begin{align*}
(00)&\quad
U_{00}+z\,U_{10}+zw(U_{10}+U_{11})=1+zw\,R_{10},\\
(01)&\quad
U_{01}+z(U_{10}+U_{11})+zw\,U_{11}=zw\,R_{11},\\
(10)&\quad
U_{00}+U_{10}+w(U_{00}+U_{01})=w\,R_{00},\\
(11)&\quad
U_{00}+U_{01}+U_{11}+w\,U_{01}=w\,R_{01}.
\end{align*}

All four are identities on the seed triangle (checked at truncation
`N=64`, interior range `i<M-1`, `j<M-2`). Solving for the Cartier
parts of `R` is therefore legitimate as a rewrite of the original
relation, not a new constraint on `U`.

Two divisibility statements make the divisions by `w` exact.

- Coefficient of `w^0` in `U_{00}+U_{10}` is `v(2t,0)+v(2t+1,0)=1+1=0`.
- Coefficient of `w^0` in `U_{00}+U_{01}+U_{11}` is
  `v(2t,0)+v(2t,1)+v(2t+1,1)`. Offset 1 is purely periodic of period 2
  (Rowland; [complexity.md](../complexity.md)): `v(t,1)=t\bmod 2`, so
  the sum is `1+0+1=0`.

Thus

\begin{align*}
R_{00}&=U_{00}+U_{01}+w^{-1}(U_{00}+U_{10}),\\
R_{01}&=U_{01}+w^{-1}(U_{00}+U_{01}+U_{11}),\\
R_{10}&=U_{10}+U_{11}+w^{-1}U_{10}+(zw)^{-1}(U_{00}+1),\\
R_{11}&=U_{11}+w^{-1}(U_{10}+U_{11})+(zw)^{-1}U_{01}.
\end{align*}

These express `R` in terms of `U` because the displayed identity already
does. Substituting them back into `PU=1+zw^2 R` is a tautology. A second,
independent equation for `R` is required.

Equal-index diagonals are kernel states of `C`:
`\operatorname{Diag} U_{00}=(c_{2n})`, `\operatorname{Diag} U_{11}=(c_{2n+1})`.
Mixed diagonals are neighboring columns, not kernel states of `C`:

\[
\operatorname{Diag} U_{01}=\bigl(v(2n,2n+1)\bigr)_n=\bigl(x(2n,-1)\bigr)_n,
\]
\[
\operatorname{Diag} U_{10}=\bigl(v(2n+1,2n)\bigr)_n=\bigl(x(2n+1,1)\bigr)_n.
\]

On the `64×64` triangle neither mixed diagonal equals the even or odd
decimation of `c`. Distinguishing `U_{01}` from `U_{10}` off the center
column is easy (right edge vs interior) and does not count.

## First correlation equation for `R`

Let `a,b,c,d=v(t,k-2),v(t,k-1),v(t,k),v(t,k+1)`. The adjacent product
at the next time is the 4-bit function

\[
\pi(t+1,k)=v'(t,k)\,v'(t,k+1)=(b+c)(1+d)+a(1+b)(c+d)
\]

over \(\mathbb F_2\). The algebraic normal form is

\[
\pi'=b+c+ac+ad+bd+cd+abc+abd,
\]

checked against the triangle (0 mismatches) and against the 16-row
truth table. In generating functions, with

\begin{align*}
S_d&=\sum v(t,k)v(t,k+d)\,z^tw^k,\\
T_{012}&=\sum v(t,k)v(t,k+1)v(t,k+2)\,z^tw^k,\\
T_{013}&=\sum v(t,k)v(t,k+1)v(t,k+3)\,z^tw^k,
\end{align*}

so that `S_1=R` and `S_0=U` (idempotence), the identity is

\[
(1+z)R+z(1+w)U
=zw(1+w)S_2+zw^2 S_3+zw^2(T_{012}+T_{013}).
\]

Checked on `3717` interior coefficients, 0 mismatches.

The right-hand side is not a function of `{U,R}`. Two seed-valid
independence statements:

- If `v(t,k-1)=0`, both adjacent products through index `k-1` vanish,
  while the skip-1 product `v(t,k-2)v(t,k)` still takes both values
  (`2060` zeros and `305` ones on the `64×64` triangle).
- If `v(t,k-1)=v(t,k)=0`, the `R`-window about `k-1` vanishes, while
  the distance-3 product `v(t,k-2)v(t,k+1)` still takes both values
  (`1479` zeros and `211` ones).

So `S_2` and `S_3` are not determined by adjacent pairs. The polynomial
`π'` depends on all four bits of the window (already visible from the
term `ad`). One time step of an adjacent product therefore depends on a
saturated 4-cell light cone; `s` steps depend on `2s+2` cells. A finite
list of multi-point generating functions is not closed under the
recurrence. Closing under all spatial products of a row is the row
itself; iterating in time reconstructs the spacetime triangle. This is
the same obstruction as the zeta-query DAG in
[mahler_dependency.md](mahler_dependency.md), in a different basis.

Applying the four Cartier operators to the `R`-equation produces four
further equations in the Cartier parts of `S_2,S_3,T_{012},T_{013}`.
It does not close the hierarchy.

## Diagonal kernel and parameterized words

The 2-kernel of `C` consists of the sequences

\[
\bigl(\Lambda_{\varepsilon_{m-1}}\cdots\Lambda_{\varepsilon_0}C\bigr)_n
=c(2^m n+r),\qquad r=\varepsilon_0+2\varepsilon_1+\cdots+2^{m-1}\varepsilon_{m-1}.
\]

Equivalently, `W` ranges over words in `{Λ_{00},Λ_{11}}`, and the
kernel element is `\operatorname{Diag}(WU)`. Mixed letters produce
decimated neighboring columns, which are excluded as witnesses.

If the kernel `K` is finite, then `Λ_0:K\to K` and `Λ_1:K\to K` are
maps on a finite set, so the orbits `Λ_0^m C` and `Λ_1^m C` are
eventually periodic as sequences of kernel elements. Constant terms
are `c(2^m)` and `c(2^m-1)` respectively. Hence:

**Lemma.** If `c` is 2-automatic, then `m\mapsto c(2^m)` and
`m\mapsto c(2^m-1)` are eventually periodic.

The converse is false, and the lemma is not a reduction of problem 1
to a weaker statement: aperiodicity of an exponentially sparse
subsequence is a special case of aperiodicity of `c`, not a stepping
stone. No independent argument for either subsequence is available
from the Cartier images, from Rowland's fixed-offset periods (the
offset here is `2^m`), or from the 2-adic low-bit valuations in
[twoadic_powers.md](twoadic_powers.md) (those probe bit position
`O(1)`, not bit position `2^m` of `f^{2^m}(1)`).

A witness rule valid for arbitrary `m` would be a function `m\mapsto n_m`
such that, for all `m`,

\[
c(2^m n_m+r_m)\ne c(2^{m+1}n_m+r_{m+1})
\]

with both evaluations on the diagonal. The constant term `n_m=0` never
distinguishes the family `Λ_0^m C`, because `c(0)=1` for every `m`.
The next coefficient `n_m=1` distinguishes `Λ_0^m C` from `Λ_0^{m+1}C`
precisely when `c(2^m)\ne c(2^{m+1})`, which already fails for several
computed consecutive pairs (e.g. `m=2,3` both give `1`). No uniform
backup index is supplied by the functional equation.

## Finite samples (not a proof)

Packed center bits through `N=65536`. At depth `m\le 11` every residue
class produces a distinct prefix of length `N/2^m\ge 32`. Birthday
expectation at `m=11` is `2^{11}/2^{33}<10^{-3}`. Distinct length-32
prefixes are genuine distinctions of infinite sequences, so this is a
finite lower bound `|K|\ge 2048`. At depth 12 the prefixes have length
16 and the 114 observed collisions match the birthday count; they are
not kernel identifications.

The one-parameter families `W_m=Λ_0^m`, `Λ_1^m`, and `(Λ_1Λ_0)^m` have
pairwise distinct length-16 diagonal prefixes for all computed `m`
(`m\le 12`, `12`, and `6` respectively). That is a finite distinct
family, not an infinite one.

Sparse diagonal bits, index `0` is the seed:

```
m          0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
c(2^m)     1 0 1 1 1 0 1 1 1 0  1  0  1  1  0  1
c(2^m-1)   1 1 1 0 1 0 1 0 1 0  0  1  1  1  0  0   (m=16: c(65535)=1)
```

Neither list is eventually periodic on the observed range. The range
is finite. Growing the table does not produce a witness rule for
arbitrary `m`.

## Why the attack died

The kill criterion fires on both named grounds.

1. **Off-diagonal mechanism.** Mixed Cartier words distinguish
   neighboring columns after `Diag`. Those sequences are not kernel
   states of `C`. Equal-index words *are* kernel states, but the
   identity after Cartier still refers to off-diagonal parts of `U`
   (`U_{10}` on the diagonal of `(00)` is `x(2n+1,1)`, not a center
   bit). Restricting to `t=k` in the identity reconstructs the three
   columns `(ℓ,c,r)` and is the original CA.

2. **Closure reconstructs the triangle.** The independent equation
   for `R` introduces skip products and triples. Those are not
   functions of `{U,R}` on the seed. The spatial support of the
   product recurrence saturates the light cone. A closed finite
   system of correlation series is the row; its time evolution is the
   spacetime triangle. The same thing happened to the Mahler DAG:
   exact cancellation rewrote the circuit as `u(t,k)`.

Growing finite kernel samples (`|K|\ge 2048`, thirteen distinct
`Λ_0^m` prefixes, an irregular `c(2^m)` list) prove neither
nonautomaticity nor nonperiodicity. Automatic sequences may have
arbitrarily large finite kernels. Aperiodicity of `m\mapsto c(2^m)`
would suffice, and is not proved.

Nonautomaticity is not proved. Eventual periodicity of `c` remains
open.

## What was obtained

- The four bivariate Cartier images of `(1+z+zw+zw^2)U=1+zw^2 R`,
  with the correct monomial degrees after `Λ_{00}(z^2 w^2\,\cdot)=zw`.
- The first correlation equation for `R`, and seed-valid independence
  of `S_2` and `S_3` from adjacent pairs.
- The exact reduction of 2-automaticity of `c` to eventual periodicity
  of `m\mapsto c(2^m)` and `m\mapsto c(2^m-1)`, with no proof of either.
- A birthday-safe finite lower bound `|K|\ge 2048` at depth 11 on
  `N=65536` bits, which is not an infinite family.
- No `W_m` with a coefficient witness valid for arbitrary `m` on the
  diagonal.
