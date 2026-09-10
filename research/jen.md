# Jen's Rule-30 column theorem: source audit

## Primary-source trail

Jen's papers are:

* E. Jen, “Global Properties of Cellular Automata,” *Journal of Statistical
  Physics* 43 (1986), 219–242, DOI [10.1007/BF01010579](https://doi.org/10.1007/BF01010579).
* E. Jen, “Aperiodicity in One-dimensional Cellular Automata,” *Physica D*
  45 (1990), 3–18, DOI [10.1016/0167-2789(90)90169-P](https://doi.org/10.1016/0167-2789(90)90169-P).

The publisher pages expose abstracts but not an accessible full text in this
environment. The 1986 paper's abstract (available through the MIT LANL
technical-report scan) describes the relevant mechanism: certain elementary
rules have a deterministic structure sideways, where two adjacent temporal
sequences determine the sequence to their left; one-to-one sideways rules
generate aperiodic behavior. The later primary exposition by Rowland gives
the usable lemma and cites Jen's Theorem 4:
[Rowland, *Local Nested Structure in Rule 30*](https://ericrowland.github.io/papers/Local_nested_structure_in_rule_30.pdf), pp. 5–6.

## Sideways reconstruction

For the convention used in the report,
\[
x_{t+1,j}=x_{t,j-1}\oplus(x_{t,j}\lor x_{t,j+1}),
\]
the left predecessor bit is uniquely recovered from the output and the two
upper right bits:
\[
x_{t,j-1}=x_{t+1,j}\oplus(x_{t,j}\lor x_{t,j+1}).
\]
Hence two adjacent temporal columns (say (j,j+1)), together with the
recurrence, uniquely reconstruct every column strictly to their left. The
same reconstruction can be iterated across a finite gap when the required
intermediate values are supplied by the two temporal traces; this is the
“sideways” deterministic structure referred to by Wolfram and Jen.

For the single-cell initial row, reconstruction of two eventually periodic
columns would make the reconstructed left pattern eventually periodic in
time. But the initial row has a single finite defect against the homogeneous
zero tail, so it cannot agree with such a doubly periodic reconstruction.
This is the source of the standard consequence quoted by Wolfram: no two
columns can both become periodic. The exact quantifiers in the prize context
are eventual temporal periodicity, not spatial periodicity.

Rowland's formal version for the reflected right-bijective orientation is
Lemma 1: if two rows differ first at position (M), then the value in column
(M) differs at every future and past time. His Lemma 2 shows that once the
preceding (d) columns are periodic, the next column is periodic with an
explicit lcm bound. These support the reconstruction logic but do not by
themselves prove the prize's one-column claim.

## Attempted application to an eventually-zero center

If (c_t=x_{t,0}=0) for all (t\ge T), the center equation gives
\[
x_{t,-1}=x_{t,1}\qquad(t\ge T).
\]
This is equality of two temporal traces, not periodicity of either trace.
Sideways reconstruction therefore cannot invoke Jen: it supplies only one
distinct trace (the common neighbor trace) plus the zero center trace, and
the zero trace is already periodic. The missing second independent periodic
column is exactly the obstruction. Local updates imply further constraints,
for example if (d_t=x_{t,-1}=x_{t,1}), (a_t=x_{t,-2}), and
 (e_t=x_{t,2}), then
\[
a_t\oplus d_t=d_t\lor e_t,
\]
but this permits irregular (d_t) and does not force a periodic pair.

## Reliable consequence for the prize

If (c_t=1) eventually, then (x_{t,-1}=0) eventually, so columns (-1)
and (0) are both eventually periodic; Jen's theorem gives a contradiction.
Therefore the center column has infinitely many zeros. No corresponding
contradiction for an eventually-zero center tail follows from Jen's theorem.

Wolfram's official announcement states both the two-column theorem and its
limitation: [announcement, lines 178–203](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/).
The official prize page remains open: [rule30prize.org](https://rule30prize.org/).

## Open-access modern restatement (Kopra 2023)

Kopra, “Rapid left expansivity, a commonality between Wolfram's Rule 30 and
powers of (p/q),” *Theoretical Computer Science* 946 (2023), DOI
[10.1016/j.tcs.2022.12.018](https://doi.org/10.1016/j.tcs.2022.12.018), gives
an accessible general theorem. Theorem 3.5 states that for every rapidly
left-expansive CA and every configuration left-asymptotic to (0^{\mathbb Z}),
every trace of the theorem's width (w) is not eventually periodic. Rule 30
is left permutive and left spreading, with left-expansive width (w=2), so
this recovers Jen's exact result: every width-2 trace of every nonzero finite
configuration is not eventually periodic. Kopra's introduction states this
explicitly and identifies it as Corollary 3.7.

The proof is quantitative and explains the one-column gap. Lemma 3.2 says
eventual (p)-periodicity of a width-(w) trace propagates one column left,
with a bounded preperiod increase (h). Iteration makes every column to the
left eventually (p)-periodic. Since the initial configuration has a left
zero tail and the CA spreads its left edge at positive speed, sufficiently
far-left columns contain a zero block of length exceeding preperiod plus
period; periodicity then forces those whole columns to be identically zero.
That contradicts left spreading, which eventually moves the nonzero left edge
past every fixed coordinate. For Rule 30, (h=0), (w=2), and spreading
speed (1).

The same proof cannot start from a width-1 trace for Rule 30: the elementary
left-expansivity rectangle has width (m+n=2), because the inverse update
needs both upper-right cells. This is a precise formulation of the obstacle,
not merely lack of ingenuity. In the eventual-zero-center scenario,
`Tr_[0,1]=(0,d_t)` may be nonperiodic even though its first coordinate is
constant; Kopra/Jen therefore supplies no contradiction.

Primary PDF: https://www.utupub.fi/server/api/core/bitstreams/eeb04919-9fa7-443b-998f-032fab664a41/content
(Theorem 3.5, Lemma 3.2, Example 2.3, and Corollary 3.7 context.)
