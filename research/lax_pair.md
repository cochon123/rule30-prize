# Bounded Lax-pair search for Rule 30

Attack on prize problem 3 via an isospectral representation, as specified
in [_astra_ideas5.md](_astra_ideas5.md) item 4. Constant \(2\times 2\)
pairs over \(\mathrm{GF}(2)\) exist, but they do not reconstruct a finite
seed orbit. A restricted affine screen and a restricted \(3\times 3\)
catalog add no reconstructing spectrum. This is not a prize claim.

Certifier: `research/lax_pair.py`. Dump: `research/lax_pair.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

## Identity

Let \(f(a,b,c)=a\oplus(b\lor c)\). A discrete Lax pair is a pair of
matrices \(L(b,c;\lambda)\), \(M(a,b,c;\lambda)\) such that

\[
L\bigl(f(a,b,c),f(b,c,d);\lambda\bigr)\,M(a,b,c;\lambda)
=
M(b,c,d;\lambda)\,L(b,c;\lambda)
\]

for every one of the sixteen quadruples. Invertible \(M\) would conjugate
spatial products of \(L\) along a periodic ring, so the monodromy spectrum
would be a constant of the evolution. The object sought was a
configuration-dependent spectrum that still reconstructs the single-cell
seed, not merely a commuting diagram.

Gauge: \(M(0,0,0)=I\), and every matrix value is required to lie in
\(\mathrm{GL}(n,\mathrm{GF}(2))\) for the constant searches. The rewrite

\[
M(b,c,d)=L\bigl(f(a,b,c),f(b,c,d)\bigr)\,M(a,b,c)\,L(b,c)^{-1}
\]

fills \(M\) from \(L\) and is then checked on all sixteen slots.

## Constant \(\mathrm{GL}(2,\mathrm{GF}(2))\)

There are six invertible \(2\times 2\) matrices over \(\mathrm{GF}(2)\).
All \(6^4=1296\) assignments of \(L(b,c)\) were tried. Exactly 36 yield a
consistent invertible \(M\) with the gauge above.

- 6 of those 36 have a single matrix \(L\) independent of \((b,c)\). Those
  are configuration-blind: every ring has the same monodromy.
- The other 30 have 2, 3, or 4 distinct \(L\)-values. Periodic traces of
  length 4 and 6 take values in \(\{0\}\) or \(\{0,1\}\).

Over \(\mathrm{GF}(2)\) the trace of a \(2\times 2\) matrix has two
possible values. A configuration-dependent choice between them is at most
one bit per ring length. That is not a reconstruction of a finite-seed
orbit, which was the preregistered continuation requirement.

Self-check: every reported solution satisfies the sixteen matrix
identities; the six configuration-independent solutions have identical
\(L\) on all four slots.

## Affine screen \(L=L_0+\lambda L_1\)

The next family is affine in a formal parameter \(\lambda\in\mathrm{GF}(2)\),
with the same \(M\) at \(\lambda=0\) and \(\lambda=1\). \(L_1\) was restricted
to \(\{0,I\}\) union three elements of \(\mathrm{GL}(2)\), independently on
each of the four slots; \(L_0\) ranged over all of \(\mathrm{GL}(2)^4\).
That is a screen (43753 trials after skipping pure constants), not the
full affine space.

No extra pair survived: whenever \(L_0\) admits an \(M\), \(L_0+L_1\)
fails either invertibility or the identity at the same \(M\).

## Restricted constant \(\mathrm{GL}(3,\mathrm{GF}(2))\)

A catalog of 20 invertible \(3\times 3\) matrices (the six permutation
matrices of \(S_3\) and the unitriangular upper/lower matrices) gives
\(20^4=160000\) assignments of \(L\). Of these, 252 admit a consistent
invertible \(M\). Twenty have configuration-independent \(L\). Twenty of
the configuration-dependent solutions have a non-constant length-4
monodromy trace; the rest have a single trace value.

Again the spectrum is at most one bit. The catalog is not all of
\(\mathrm{GL}(3,\mathrm{GF}(2))\) (order 168), and affine \(3\times 3\)
pairs over \(\mathbb Q\) were not Gröbner-solved. Those omissions do not
rescue the families that *were* searched: isolated conserved traces were
already forbidden as a continuation.

## Why it died

Preregistered kill: every solution in the fixed family is singular,
spectrally trivial, or removable by a local change of basis; a survivor
must subsequently reconstruct the seed orbit, and an isolated conserved
trace does not justify continuing.

The constant \(\mathrm{GL}(2)\) family is completely classified under the
stated gauge. Its configuration-dependent members are not spectrally
constant, but they still fail reconstruction. The affine and
\(\mathrm{GL}(3)\) screens produced the same obstruction. No exact
iteration formula for \(c_n\) follows.

This is not a proof that Rule 30 is non-integrable, and it is not a prize
claim.
