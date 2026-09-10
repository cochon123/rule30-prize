# Algebraic hypothesis for the centre bitstream

Attack on prize problem 1, as specified in [_astra_ideas7.md](_astra_ideas7.md)
item 5. Lattice reduction produces no primitive polynomial of degree
2 through 6 and height \(\le 2^{16}\) with a real root throughout
\(I_{256}\). This is not a prize claim.

Certifier: `research/algebraic_bitstream.py`. Dump:
`research/algebraic_bitstream.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Target

\[
\alpha=\sum_{t\ge 0}c_t 2^{-t-1}.
\]

The first 256 bits determine a closed interval \(I_{256}\) of length
\(2^{-256}\). An algebraic irrational of small degree and height in that
interval would have a non-periodic binary expansion, hence would prove
nonperiodicity of \(c\). It would not prove density \(1/2\).

Centre bits match `experiment.center_bits` on a prefix of length 256.

## LLL screen

For each degree \(d=2,\ldots,6\), integer LLL is run on the lattice
whose \(i\)-th basis vector carries the coefficient of \(\alpha^i\) and
a scaled embedding of \(\mathrm{mid}(I_{256})^i\). Primitive vectors of
coefficient height at most \(2^{16}\) are tested for a sign change of
\(P\) on \(I_{256}\), then on the 4096-bit interval.

Shortest coefficient heights found are of size \(10^{15}\) and larger —
far above \(2^{16}\). Crossing candidates at the frozen height: **zero**.
Validation on 4096 bits is vacuous.

## Why it died

Preregistered kill: certified exclusion of the bounded polynomial family,
a validation mismatch, or no candidate in the cap. LLL supplies no
vector in the family with a root in \(I_{256}\). A numerical relation
alone would not have survived without a Rule 30 invariant identifying
that root. Not a prize claim.
