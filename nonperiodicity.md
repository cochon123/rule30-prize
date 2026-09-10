# Rule 30 center-column attack (initial pass)

For the convention
\[
x(t+1,j)=x(t,j-1)\mathbin{\mathsf{XOR}}(x(t,j)\mathbin{\mathsf{OR}}x(t,j+1)),
\]
write `c_t=x(t,0)`, `l_t=x(t,-1)`, and `r_t=x(t,1)`. Then
\[
c_{t+1}=l_t\oplus(c_t\lor r_t).
\]

## Rigorous reduction for constant tails

* If `c_t=1` for every `t>=T`, then `c_{t+1}=l_t XOR 1`, hence `l_t=0` for every `t>=T`. Thus columns `-1` and `0` are both eventually constant, so their pair is eventually periodic. This contradicts Jen's theorem (as summarized by Wolfram): for the single-black-cell initial condition, no two columns can both become periodic. Therefore the center column cannot be eventually all 1.

* If `c_t=0` for every `t>=T`, the center equation gives `l_t=r_t=d_t`.
  The right-neighbor update additionally gives `d_(t+1)=d_t OR x(t,2)`.
  Thus `d_t` is nondecreasing and eventually constant. Columns `-1` and `0`
  are eventually constant, contradicting the same width-2 theorem.

Both constant tails are excluded. The center contains infinitely many zeros
and infinitely many ones. The first pass missed monotonicity in the zero-tail
case; the sustained follow-up and independent review repaired that gap.
Full proof: [research/constant_tails.md](research/constant_tails.md).

## Period-2 center tail: local constraints, but no exclusion yet

Suppose the center is eventually alternating, and choose the phase so that
`c_t=0` for even `t` and `c_t=1` for odd `t`. (The other phase is the same
argument shifted by one.) Put `a_t=x(t,-2)` and `e_t=x(t,2)`.

At odd `t`, the center equation with `c_t=1,c_{t+1}=0` forces `l_t=1`. At even `t`,
the center equation with `c_t=0,c_{t+1}=1` gives `r_t=not l_t`. The update
at `j=-1` during an odd step then gives
`l_{t+1}=a_t XOR 1=not a_t`; this auxiliary relation is not needed below.

Use the right-column update at the two phases:

* for odd `t`, `r_{t+1}=not(r_t OR e_t)`, so (since `r_{t+1}=not l_{t+1}`)
  `l_{t+1}=r_t OR e_t`;
* for even `t`, `r_{t+1}=r_t OR e_t`; in particular, an even-phase `r_t=1`
  forces the following odd-phase `r_{t+1}=1`.

The tempting final step is invalid: if an even-phase `l_t=0`, the updates
force the *next* even-phase value `l_{t+2}=1`, but they do not force the
current `l_t=1`. More precisely, writing `q_n=l_{T+2n}` for even phases,
one obtains `q_n=0 => q_{n-1}=q_{n+1}=1` (and an additional outer-cell bit is
forced to 0). This still permits an aperiodic sequence of isolated zeros in
the even subsequence, so Jen's theorem cannot be invoked. Period 2 therefore
remains open under this local analysis, just like periods 3 and 4.

## Sources

* Official prize statement: https://rule30prize.org/
* Wolfram's prize announcement, explicitly stating Jen's result and that it does not extend to one column: https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/
* Rowland, *Local Nested Structure in Rule 30*, citing Jen, “Global Properties of Cellular Automata,” J. Stat. Phys. 43 (1986), 219–242, and “Aperiodicity in One-dimensional Cellular Automata,” Physica D 45 (1990), 3–18: https://ericrowland.github.io/papers/Local_nested_structure_in_rule_30.pdf (see Lemma 1 and discussion around Theorem 4, PDF pages 5–6).

The Wolfram announcement reports a billion-bit computation but explicitly distinguishes finite evidence from a proof about the entire center column. Numerical evidence is not used in the constant-one exclusion above.
