# Hashlife-style block reuse on the seed orbit

Attack on prize problem 3, as specified in [_astra_ideas6.md](_astra_ideas6.md)
item 2. Interned overlapping blocks reuse central spacetime, but charged
work stays superlinear, no closed recurrence bounds the distinct blocks,
and \(n=2^{15}\) did not complete. This is not an \(O(n)\) algorithm and
not a prize claim.

Certifier: `research/hashlife_reuse.py`. Dump: `research/hashlife_reuse.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

## Evaluator

Leaf width 8. A node of width \(W=8\cdot 2^L\) stores two adjacent
halves. Evolution uses the overlapping triple (left, middle, right) so
the protected centre of width \(W/2\) after \(W/4\) steps is determined
and cached on the interned node. The cache starts empty for every
target. Blocks are built from the single-cell seed; there is no
precomputed spacetime dictionary.

The initial word has width \(4n\) and left edge at \(-2n\), so one
`result()` jump is exactly \(n\) steps and the centre bit of the evolved
node is \(c_n\).

Unit costs, frozen before measuring: 1 per intern lookup, 1 per new
node, 1 per cache lookup, 1 per cache fill, 1 per 8-cell leaf update of
one time step. Comparisons are the intern probes and are not charged
twice.

\[
W(n)=\text{intern lookups}+\text{node constructions}+\text{cache lookups}+\text{cache fills}+\text{leaf updates}.
\]

Self-checks: packed window step matches the local rule on all 8- and
16-cell words; \(c_n\) matches `experiment.center_bits` through \(n=256\)
and an independent packed generator at every reported \(n\); the full
evolved centre word matches naive evolution through \(n=256\).

## Measured work

Each \(n\) restarts from empty tables.

| \(n\) | \(c_n\) | \(W(n)\) | \(W/n^2\) | central cache hits | vacuum | edge | \(W\)-ratio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1024 | 1 | 266572 | 0.254 | 10354 | 79 | 168 | — |
| 2048 | 0 | 812886 | 0.194 | 62862 | 99 | 300 | 3.05 |
| 4096 | 1 | 1919501 | 0.114 | 370293 | 129 | 564 | 2.36 |
| 8192 | 1 | 5522942 | 0.082 | 1676378 | 158 | 821 | 2.88 |
| 16384 | 0 | 19953986 | 0.074 | 6920215 | 247 | 1335 | 3.61 |

Central intern-plus-cache savings are 96–99.8% of all hits. Vacuum and
edge reuse is negligible. Distinct central evolution requests at
\(n=16384\) still number 1.81 million. Leaf updates saturate at
\(2^{19}\) once \(n\ge 8192\); the remaining growth is intern and cache
traffic on chaotic interior blocks.

The first attempt at \(n=2^{15}\) ran more than 40 minutes, entered
disk sleep at about 1.5 GiB RSS, and never printed a result. It was not
rerun. That doubling is incomplete.

## Why it died

Preregistered numerical kill: retire if \(W\) grows by at least 3.8 on
**each** of the last two doublings **and** savings remain confined to
vacuum or edge. On the completed data,
\(W(2^{14})/W(2^{13})=3.61<3.8\), and central reuse dominates, so that
conjunction does not fire.

The continuation requirement was a recurrence bounding the number of
distinct requested blocks, giving a uniform algorithm. No such
recurrence was obtained. \(W(n)\) is superlinear on every completed
doubling (\(\log_2 3.61\approx 1.85\) at the high end) and is not
\(O(n)\). Incomplete \(n=2^{15}\) is itself evidence that the node table
does not stay small. Apparent speedup versus a naive \(\Theta(n^2)\)
leaf sweep is real central sharing, not a prize-threshold evaluator.

Not a prize claim.
