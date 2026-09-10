# Nonuniform substitution tilings of the centre

Attack on prize problem 2, as specified in [_astra_ideas6.md](_astra_ideas6.md)
item 3. No library in the frozen family parses the first 1{,}024 centre
bits as an S-adic word over four letters with two substitutions of
length 2 or 3. This is not a prize claim, and a finite parse would not
have been a density proof.

Certifier: `research/substitution_tiling.py`. Dump:
`research/substitution_tiling.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Target

A hierarchical description

\[
c=\tau\!\left(\lim_k\sigma_{i_0}\sigma_{i_1}\cdots\sigma_{i_k}(a_k)\right)
\]

with a small library of nonuniform substitutions. The directive sequence
may stay unknown. If every permitted directive is balanced, Problem 2
does not need the directive.

A sufficient certificate, frozen before the search, is: every depth-\(k\)
tile has length at least \(2^k\), and
\(|\mathrm{ones}-\mathrm{zeros}|\le C\rho^k\) with \(1<\rho<2\). Bounded
image lengths then give \(|D(N)|=O(N^{\log_2\rho})=o(N)\). Contraction
must be an exact joint-spectral-radius bound on the imbalance subspace
of the substitution matrices, not a measured frequency.

## Frozen family

Four letters, two substitutions, image lengths in \(\{2,3\}\), a
letter-to-bit coding \(\tau\), at least one substitution nonuniform.
Codings restricted to the three splits that use both bits:
\(\tau=(0,0,1,1)\), \((0,0,0,1)\), and \((0,1,1,1)\).

Search subclass (not a loop over all morphisms): S-adic, one morphism
per level. Slice A enumerates every uniform length-2 finest morphism
(all letter-lifts of the four coded digrams) and tries to infer a
second morphism on the producer word. Slice B uses left-greedy
mixed-length finest inference. New producer types open only when no
bound image matches, except on words of length at most 96 (letters) or
256 (bits). Recursion stops at a seed of length \(\le 4\). Synthesis
budget two CPU-hours.

Self-check: packed centre bits match `experiment.center_bits` on 256
and 1{,}024 samples. An expanding synthetic library (imbalance
multiplies by 3) is rejected by the spectral-radius test.

## What the prefix already forbids

On the first 1{,}024 centre bits every binary digram occurs
(counts 145, 126, 118, 123). A length-2 finest morphism therefore
uses all four letters. Pairing those producer letters again produces
16 distinct length-2 blocks, which cannot be the image of a second
4-letter length-2 substitution.

The same obstruction is present at length 16{,}384: all four digrams,
and 16 paired digrams. This is a combinatorial fact about the prefix,
independent of greedy inference.

## Search outcome

Elapsed 37.4 seconds; the two-hour budget did not fire.

- 10{,}032 length-2 finest lifts enumerated across the three codings.
- 192 mixed-length finest morphisms inferred.
- Libraries with two complete nonuniform morphisms that parse 1{,}024
  bits down to a seed of length \(\le 4\): **zero**.
- Contracting libraries: zero. Extensions to 16{,}384: zero.

A synthetic mixed-length library used as a parser smoke test was not
recovered (expansion length 750; left-greedy finest inference missed
it) and was not contracting (\(\mathrm{spr}\ge 2\)). That limitation
is recorded. It does not create a surviving library on the actual
centre bits: the four-digram saturation already blocks a two-level
length-2 hierarchy over four letters.

## Why it died

Preregistered kill: no library survives the 1{,}024-bit parse.

No S-adic pair in the freeze writes the prefix as a short seed under
two substitutions of length 2 or 3 over four letters. Without a
library there is no contraction certificate and no spacetime lift.
The attack does not continue by enlarging the alphabet or the image
lengths. Not a prize claim.
