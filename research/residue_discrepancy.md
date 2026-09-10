# Residue-class discrepancies of the centre

Extra Cycle I screen for prize problem 2: signed sums and Berlekamp–Massey
lengths of \(c\) along arithmetic progressions. This is not dyadic \(A_m\),
not block energy, and not a prize claim.

Certifier: `research/residue_discrepancy.py`. Dump:
`research/residue_discrepancy.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Target

If some residue class \(t\equiv r\pmod m\) had a closed signed sum, or even
a linear recurrence of order \(o(N)\), Problem 2 would reduce to finitely
many simpler sequences. The freeze is moduli
\(\{2,3,4,5,6,7,8,9,15,16\}\) at \(N=10^5\), with linear complexity on each
4096-bit subsample, plus a persistence check that an exactly unbiased class
at one \(N\) remain unbiased at every dyadic length \(2^8,\ldots,2^{17}\).

Centre bits match `experiment.center_bits` on a prefix of length 256.

## Outcome

At \(N=10^5\), residues \(2\) and \(12\) modulo \(16\) have signed
discrepancy exactly \(0\) (3125 ones in 6250 samples). That hit does **not**
persist: already at \(N=2^{16}\) those classes are \(-82\) and \(-20\), and
at \(N=2^{17}\) they are \(-26\) and \(-20\). Other exact zeros (residue
\(7\) mod \(16\) at \(N=2^{16}\); residue \(2\) mod \(16\) at \(N=256\))
are the same random-walk phenomenon. No pair \((m,r)\) vanishes on every
dyadic length in the freeze.

Every 4096-bit subsample has \(L(N)/N\approx 1/2\), identical to the raw
centre. Class ratios stay \(O(10^{-2})\), the same order as \(D(N)/N\).

## Why it died

Preregistered kill: no persistent unbiased residue class and no subsample
with \(L(N)<N/4\). Both fired. Arithmetic progressions do not simplify \(c\).
Not a prize claim.
