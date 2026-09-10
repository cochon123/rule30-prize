# Holographic matchgates for the Rule 30 Holant

Attack on prize problem 3, as specified in [_astra_ideas5.md](_astra_ideas5.md)
item 2. No compatible invertible \(2\times 2\) wire bases make the complete
tensor family into matchgates, in either prescribed representation. There is
no small boundary Pfaffian. This is not a prize claim, and a Pfaffian on
\(\Theta(n^2)\) vertices would not have met the prize threshold even if the
local tensors had been matchgates.

Certifier: `research/matchgate.py`. Dump: `research/matchgate.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

Matchgate identities are Cai–Choudhary / Cai–Gorenstein
([arXiv:1303.6729](https://arxiv.org/abs/1303.6729), Theorem 1; equivalently
Cai–Gorenstein, *Matchgates Revisited*, Theorem 2.1). For a signature \(\Gamma\)
of arity \(k\) and all \(\alpha,\beta\in\{0,1\}^k\), if \(P=\{p_1<\cdots<p_\ell\}\)
indexes the bits where \(\alpha\) and \(\beta\) differ, then

\[
\sum_{i=1}^\ell (-1)^i\,\Gamma_{\alpha\oplus e_{p_i}}\,\Gamma_{\beta\oplus e_{p_i}}=0.
\]

These identities imply the parity condition and are necessary and sufficient
for planar matchgate signatures. The 4-bit Grassmann–Plücker instance used
as a one-line certificate is

\[
\Gamma_{0000}\Gamma_{1111}-\Gamma_{0011}\Gamma_{1100}+\Gamma_{0101}\Gamma_{1010}-\Gamma_{0110}\Gamma_{1001}=0.
\]

## Local Holant

Each update is the 4-leg tensor \(T(a,b,c,d)=1\) iff \(d=a\oplus(b\lor c)\).
The bit \(x(t,j)\) is produced once and consumed three times in the next row
(as left, centre, and right parent), so the bulk family also contains the copy
\(\mathrm{EQ}_4\) (value 1 iff all four bits equal). Seed unaries pin the
bottom row; an output unary is the indicator that the requested bit is 1.
Summing internals is exactly \(c_n\).

Untransformed, \(T\) has mixed parity (6 even and 2 odd support points among
the 8 ones), so it is not a matchgate. \(\mathrm{EQ}_4\) is even but has
Grassmann–Plücker value 1, so it is not a matchgate either. Arity-1 seed and
output unaries are always matchgates; invertibility of the incident basis
keeps them nonzero.

The untransformed elementary Holant reproduces the CA: \(c_1=1\) and
\(c_2=0\).

## Two prescribed representations

**Elementary network.** One \(T\) drawn as a diamond, clockwise legs
\((a,d,c,b)\), fused on the \(d\)-wire to an \(\mathrm{EQ}_4\) with clockwise
legs \((d_{\mathrm{in}},A,V,C)\). Seed/output unaries on the dangling copies.
No crossing is required in this drawing.

**Two-step blocking.** (i) Unblocked two-row grid drawing: the same \(T\) and
\(\mathrm{EQ}_4\) with temporal parity of bases, plus the bosonic crossover
of the two diagonals of each spacetime square, clockwise
\((A_{\mathrm{in}},C_{\mathrm{in}},A_{\mathrm{out}},C_{\mathrm{out}})\), value 1
iff bit1=bit3 and bit2=bit4. (ii) The blocked 6-ary light cone

\[
T_2(a,b,c,d,e,o)=1\iff o=f\bigl(f(a,b,c),f(b,c,d),f(c,d,e)\bigr),
\]

clockwise \((a,b,c,d,e,o)\), with \(f(x,y,z)=x\oplus(y\lor z)\). Internals of
the block need not themselves be matchgates; the block signature must be,
and copies used to tile blocks remain in the family.

Bases are invertible \(2\times 2\), orientation-dependent, with temporal parity
allowed. On a contracted wire the two ends are dual (\(M\) and \(M^{-1}\));
for a single tensor, inverses are absorbed into the four matrix names, which
is the most general \(\mathrm{GL}(2)^4\) holographic transform of that
tensor. Consumer contractions use the adjugate in place of \(M^{-1}\);
matchgate identities are homogeneous, so vanishing is unaffected for
\(\det M\neq 0\).

## Certificates

Self-checks: the fermionic crossover (\(\Gamma_{1111}=-1\)) satisfies the
MGI; the bosonic one does not (Grassmann–Plücker \(=2\)); a generic \(K_4\)
Pfaffian signature is a matchgate; \(\mathrm{EQ}_2\) is a matchgate.

### Crossing (two-step unblocked)

Through-going dual bases leave the bosonic crossover unchanged up to
determinants. Exactly,

\[
X' = (\det A)(\det C)\,X,
\]

as a 16-entry identity of polynomials (all sixteen differences vanish). The
transformed Grassmann–Plücker value is \(2(\det A\det C)^2\), which is nonzero
on \(\mathrm{GL}(2)\). The crossing is never a matchgate. Replacing it by the
fermionic gadget would change the Holant by a sign on double-occupied
crossings and would not compute \(c_n\).

This kills the unblocked two-step drawing by itself. Transforming only \(T\)
and leaving this crossing counts as failure.

### Rule tensor \(T\) (elementary, and any drawing that uses \(T\))

A common \(2\times 2\) basis on all four legs: the MGI plus \(\det M\neq 0\)
have Groebner basis \(\{1\}\) over \(\mathbb Q\). Diagonal and upper-triangular
independent bases likewise give \(\{1\}\) over \(\mathbb Q\).

For four independent bases, \(\mathrm{GL}(2)^4\) is covered by 16 charts:
each matrix is either \(\{M_{00}=1\}\) or \(\{M_{00}=0,\,M_{01}=1\}\). On each
chart, even- and odd-matchgate parity (odd or even entries vanish) together
with Rabinowitsch invertibility are decided over \(\mathbb F_{32003}\) and
again over \(\mathbb F_{104729}\). The two primes agree on every chart:

- 8 chart/sector pairs have a nonempty parity variety: both of \(A\) and
  \(D\) must lie in the chart \(\{M_{00}=1\}\) (masks \(0,2,4,6\)), each
  in even and odd parity.
- The other 24 chart/sector pairs have Groebner basis \(\{1\}\) (empty).

Every nonempty component lifts to an explicit family over \(\mathbb Q\)
(coefficients \(\pm 1\) after the standard balanced lift). Substituting into
the remaining MGI and saturating invertibility gives Groebner basis \(\{1\}\)
over \(\mathbb Q\) on every such family. There are no survivors.

Thus \(T\) itself has no invertible \(2\times 2\) wire-basis transform to a
matchgate. The elementary family dies even before copies are imposed.

### Copy \(\mathrm{EQ}_4\)

\(\mathrm{EQ}_4\) *is* realizable: the Hadamard basis
\(\begin{pmatrix}1&1\\1&-1\end{pmatrix}\) makes it an even matchgate
(Grassmann–Plücker \(0\)). The common-basis chart \(\{M_{00}=1\}\) is a
nonempty variety over \(\mathbb Q\) containing that point. Transforming only
the copy, while leaving \(T\) (or the crossing) incompatible, is the failure
mode named in the kill criterion; here the obstruction is \(T\) and the
crossing, not the copy.

Seed/output unaries remain matchgates after any invertible basis.

### Blocked two-step \(T_2\)

\(T_2\) has mixed parity (32 ones). Under a common basis, both charts
\(\{M_{00}=1\}\) and \(\{M_{00}=0,M_{01}=1\}\) have even- and odd-parity
ideals equal to \(\{1\}\) over \(\mathbb Q\). A diagonal six-leg ansatz is
empty at parity over \(\mathbb F_{32003}\). The blocked representation
therefore has no common (or diagonal) matchgate transform either.

## Small boundary Pfaffian

None. Even a successful local matchgate transform would have produced a
planar matching sum on the whole light cone, \(\Theta(n^2)\) vertices, which
the assignment already excludes as a prize algorithm. With no compatible
bases there is no FKT instance at all, and no residual boundary calculation
after eliminating a matchgate bulk.

## Why it died

The complete tensor family \(\{T,\mathrm{EQ}_4,X,\text{seed},\text{output}\}\)
has no compatible matchgate transformation in either prescribed representation.

- Elementary: \(T\) admits no \(\mathrm{GL}(2)^4\) matchgate transform
  (16-chart cover; nonempty parity components die in MGI over \(\mathbb Q\)).
- Two-step unblocked: the bosonic crossover is invariant and has
  Grassmann–Plücker \(2(\det A\det C)^2\neq 0\).
- Two-step blocked: \(T_2\) has no common invertible basis even at the
  parity stage over \(\mathbb Q\).

Copies and unaries are not the obstruction (\(\mathrm{EQ}_4\) is Hadamard-
realizable; unaries always are). The kill criterion counts a \(T\)-only
success with incompatible copy or crossing as failure; here \(T\) and the
crossing fail, so the family fails.

No compatible bases. No small boundary Pfaffian. Not a prize claim.
