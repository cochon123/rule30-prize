# Small periods 3–9, other than isolated zeros

Isolated-zero words `01^q` are handled in `isolated_runs.md` and
`isolated_zero_uniform.md`. This note records every other primitive
necklace of period 3 through 9.

## Algebraic local maps

On every 1 in the center, the left neighbor is `NOT` of the next center
bit. During a 0-run of length `k>=2`, left and right neighbors are equal
and the right neighbor is nondecreasing for the first `k-1` steps
(`constant_tails.md` localized).

A width-3 right window with a free far bit, evolved for two periods,
never forces the whole left-neighbor *word* to a single possibility for
any of these necklaces (`small_period_cert.py`, field
`left_forced_periodic`). Forced bits occur only on 1s, as predicted.

## Radius 6–8 strips

`analyze_any_pair` (Jen prune if *any* adjacent pair of columns is
periodic, not just the center’s neighbors) still leaves residual
components at radius 6 and 7 for every primitive word of period 3, 4, 5,
6, 7 and for `011111111`. Radius 8 does not finish the period 3–5
survivors. Incremental `strip_extend` through radius 22 hits the
35,000-state cap on `001`, `011`, `0001`, `0011`, `0111`, `011111111`,
and all primitive period-5 words.

Known empties from the period-8 scan remain `00000001`, `00000011`, and
`01111111` (the last is isolated-zero `q=7`).

## Light-cone search

For `001`, `011`, `0001`, `0011`, `0111`, exhaustive search of all
width-`(2T+1)` rows with both edges 1, `T<=11`, finds no unbounded
period match. Best finite matches are `O(T)`, same as period 2. This
does not exclude a later onset.

## Status table

| period | word | strip residual | algebraic forced left word | seed light-cone |
|-------:|------|----------------|----------------------------|-----------------|
| 3 | 001, 011 | open at r=8 | no | finite `T<=11` |
| 4 | 0001, 0011, 0111 | open | no | finite `T<=11` |
| 5 | all 8 necklaces | open | no | not all scanned |
| 6 | all primitive | open at r=7 | no | — |
| 7 | all primitive | open at r=7 | no | — |
| 8 | 00000001, 00000011, 01111111 | excluded | — | — |
| 8 | other necklaces | mixed; most cap | — | — |
| 9 | 011111111 | open (isolated-zero exception) | no | — |

Problem 1 is therefore still open for period 2 and for every primitive
word of period 3–7, plus the period-9 isolated zero.

Raw dump: `research/small_period_cert.json`.
