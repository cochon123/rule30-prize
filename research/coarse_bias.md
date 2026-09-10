# Bias-preserving coarse-graining

Attack on prize problem 2, as specified in [_astra_ideas7.md](_astra_ideas7.md)
item 3. No factor diagram in the frozen family of linear block projections
and additive radius-1 coarse maps. Without a factor there is no coboundary
and no exact digit formula for \(D(bK)\). This is not a prize claim.

Certifier: `research/coarse_bias.py`. Dump: `research/coarse_bias.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

## Identities

A block projection \(P\), a simpler CA \(G\), and local \(g,\psi\) should
satisfy \(PF^b=GP\) and

\[
\sum_{s=0}^{b-1}\sigma(F^s x)=g((Px)_0)+\psi(F^b x)-\psi(x),
\]

so that on the seed \(D(bK)=\sum_{k<K}g((G^k P\delta_0)_0)+O(1)\). These
are finite checks of universal local identities, independent of onset.

## Freeze

\(b\in\{2,3\}\); coarse alphabets \(\mathbb F_2\) and \(\mathbb F_2^2\);
\(G\) additive of radius 1; \(P\) a linear map on a \((b+2)\)-window
(one extra neighbour on each side of a \(b\)-block); \(\psi\) affine in a
radius-2 neighbourhood with coefficients in \(\{-4,\ldots,4\}\). Constant
projections excluded. Two-hour cap; the search finished in 54 seconds.

## Outcome

| \(b\) | coarse bits | linear \(P\) | additive \(G\) | factor diagrams | both identities |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 1 | 16 | 8 | 0 | 0 |
| 3 | 1 | 32 | 8 | 0 | 0 |
| 2 | 2 | 256 | 4096 | 0 | 0 |

No pair \((P,G)\) in the freeze intertwines \(F^b\) with an additive
radius-1 map. The coboundary screen never ran. A factor diagram alone
would not have been enough in any case.

## Why it died

Preregistered kill: no nonconstant projection satisfying both identities,
or every surviving factor loses the bias observable. The first clause
fires. The family was not enlarged. Not a prize claim.
