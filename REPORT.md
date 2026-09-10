# Rule 30 prize: swarm research attempt

Date: 2026-09-09. Three `gpt-5.6-luna` agents worked on separate problems,
then received follow-up attacks and corrections. The coordinating agent
checked the mathematics and ran the experiments below.

**Outcome: no prize problem solved.** The official site still presents the
three challenges and does not announce a winner. We found partial deductions,
exact reformulations, and finite evidence, not a proof of any prize claim.
No novelty is claimed for the elementary lemmas in these notes.
[Official prize site](https://rule30prize.org/).

## Definition and target

Let

\[
x_{t+1,j}=x_{t,j-1}\oplus(x_{t,j}\lor x_{t,j+1}),\qquad
x_{0,j}=\mathbf1_{j=0},\qquad c_t=x_{t,0}.
\]

The problems ask about eventual periodicity of `c`, its limiting frequency
of ones, and the effort required to compute an individual `c_n`.
The detailed announcement's computational predicate rules out an exact
finite machine with `limsup T(n)/n < infinity`, meaning an `O(n)` algorithm.
This is distinct from both ruling out `o(n)` and proving `Omega(n)`;
machine model and operation costs matter.
[Detailed announcement](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/).

## Problem 1: what the argument actually establishes

Write `l_t=x(t,-1)` and `r_t=x(t,1)`. If the center is eventually all one,
then

\[
1=l_t\oplus(1\lor r_t)=l_t\oplus1,
\]

so the adjacent left column is eventually all zero. Jen's known
two-column aperiodicity result excludes this for the single-cell seed.
Thus the center has infinitely many zeros. This is a small consequence of
an existing theorem, not a solution to the prize.
The announcement explains the two-column theorem and its limitation.
[Source](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/).

The sustained follow-up also excludes an eventually all-zero center. In that
case `l_t=r_t=d_t`, and the right-neighbor update gives
`d_(t+1)=d_t OR x(t,2)`. A nondecreasing binary sequence is eventually
constant, again contradicting the width-2 theorem. **Both colors therefore
occur infinitely often.** This repairs the first pass, which missed that
monotonicity. It does not exclude any nonconstant eventual period.
Details: [constant_tails.md](research/constant_tails.md) and
[nonperiodicity.md](nonperiodicity.md).

An exact algebraic target is available. Let `L(N)` be the least order `r`
for which fixed coefficients `a_1,...,a_r` in GF(2) satisfy
`c_n = a_1*c_(n-1) XOR ... XOR a_r*c_(n-r)` for every `r<=n<N`.
Thus the recurrence must start at its order, not at an arbitrary later onset.
Then

\[
c\text{ is not eventually periodic}
\quad\Longleftrightarrow\quad \sup_N L(N)=\infty.
\]

Proof: an eventual period `p` starting at `T` gives the recurrence
`c_n=c_(n-p)` for `n>=T+p`, so all prefix complexities are bounded by
`T+p`. Conversely, if all complexities are at most `B`, pad each recurrence
to length `B`. There are only `2^B` coefficient vectors. One fits arbitrarily
long prefixes, hence the entire sequence for `n>=B`. Its `B`-bit state
evolves deterministically in a finite state space, so it eventually repeats.

**Missing step:** prove unbounded `L(N)` for this seed. Large measured values
do not prove that unboundedness.

## Problem 2: an exact discrepancy target

Define

\[
D(N)=\sum_{t=0}^{N-1}(2c_t-1),\quad
A_m=\max_{0\le h\le 2^m}|D(2^m+h)-D(2^m)|.
\]

The desired limiting frequency is equivalent to `D(N)=o(N)`, and also to
`A_m=o(2^m)`. Necessity follows by bounding both discrepancies for times
between `2^m` and `2^(m+1)`. For sufficiency, telescope across the previous
dyadic annuli:

\[
|D(2^m)|\le |D(1)|+\sum_{j<m}A_j=o(2^m).
\]

The extra partial annulus contributes at most `A_m`.

Checking only `D(2^m)` is insufficient. Set `a_0=+1,a_1=-1`, then on each
annulus `[2^m,2^(m+1))`, `m>=1`, put `+1` on its first half and `-1` on
its second. Its dyadic endpoint discrepancies are all zero, but the
discrepancy-to-length ratio at `N=3*2^(m-1)` is `1/3`.

For iid fair initial data, left-permutivity does give exact unbiasedness at
each fixed time: flipping the extreme left ancestor flips the output.
That pairs different initial configurations. It does not pair times in
the single-seed orbit. Even almost-sure time-average results would not
settle this prescribed, measure-zero initial configuration.

**Missing step:** a deterministic bound on `A_m` for this orbit.
Details and rejected stronger conditions: [balance.md](balance.md).

## Problem 3: edge structure and the remaining cost

Put `u(t,k)=x(t,t-k)`, so `u(t,k)=0` for `k<0`, `u(t,0)=1`, and

\[
u(t+1,k)=u(t,k)\oplus\big(u(t,k-1)\lor u(t,k-2)\big).
\]

Every fixed `k` has a pure temporal period dividing `2^k`. Inductively,
the forcing term has a period `P` dividing `2^(k-1)`. Over `P` steps the
bit changes by a fixed XOR parity. Over `2P` steps that parity cancels.
This is consistent with established periodicity of edge diagonals.
[Rowland, Local Nested Structure in Rule 30](https://wpmedia.wolfram.com/sites/13/2018/02/16-3-4.pdf).

But the center is `u(n,n)`: its offset grows with the requested time.
A fixed-offset periodicity result supplies neither a cheap representation
of that period nor a way to extract its required phase cheaply. It also
does not exclude a future compressed algorithm.

Likewise, sensitivity to many arbitrary initial bits cannot prove a running
time lower bound for this task: all initial bits here are fixed constants,
including the central one. Uniform computation of a growing table is valid,
but its construction costs must be counted. Our packed Python simulation
uses growing integers, whose operations are not constant-cost bit operations.

**Missing step:** an exact uniform algorithm with a proved resource bound,
or a lower bound applying to the fixed sequence itself.
Details: [complexity.md](complexity.md).

## Reproducible finite experiments

Run from this directory:

```sh
python3 experiment.py --bits 100000 --output results.json
```

The run computes times `0..99999`, including the initial seed. Counts agree
with the checkpoints in the published announcement.

| Prefix length | Ones | Frequency | Signed discrepancy |
|---:|---:|---:|---:|
| 100 | 52 | 0.52000 | 4 |
| 1,000 | 481 | 0.48100 | -38 |
| 10,000 | 5,032 | 0.50320 | 64 |
| 100,000 | 50,098 | 0.50098 | 196 |

For each period `p=1..4096`, the script records the last observed mismatch
`c_t != c_(t+p)`. The smallest of those last-mismatch times is `95902`.
Consequently every period in that range is excluded for every proposed
onset at or before `95902`. No conclusion is drawn about an arbitrary later
onset or larger period.

| Training bits | Minimum binary recurrence length | First failure of fitted recurrence |
|---:|---:|---:|
| 100 | 48 | index 100 |
| 1,000 | 500 | index 1,000 |
| 10,000 | 5,001 | index 10,001 |
| 20,000 | 10,000 | index 20,002 |

Failure indices use zero-based time and come from subsequent, unused bits.
These tests reject the fitted finite-prefix recurrences as universal formulas.
They do not prove a lower bound for arbitrary algorithms.

Validation includes agreement between packed and direct spatial simulations
through 256 samples; exhaustive recurrence-minimality checks for all 256
eight-bit words; direct checks of period witnesses; and an independent
right-edge recurrence implementation. The complete result includes all
4,096 witnesses, measured dyadic annuli, and a SHA-256 digest of the generated
sequence encoded as one byte per bit.

Files: [experiment.py](experiment.py), [edge_audit.py](edge_audit.py),
[results.json](results.json).

## Next research target

Of the approaches tested here, Problem 1 offers the clearest next theorem
to pursue: force unbounded binary recurrence length from the nonlinear
spacetime recurrence, or strengthen the two-column argument to constrain
one periodic column. Our work supplies neither bridge. Increasing the
simulation length alone would not fill that gap.

## Sustained research continuation

The user authorized a persistent solution goal after the initial attempt.
Current progress is tracked in [research/LOG.md](research/LOG.md).
The goal remains open; no complete prize solution has been obtained.

## Cycle B (same day)

A uniform Jen certificate now excludes every isolated-zero eventual
period `01^q` except `q in {1,2,3,4,5,6,8}`: at radius 6 the unique
recurrent strip component has a periodic left neighbor.
[isolated_zero_uniform.md](research/isolated_zero_uniform.md).
Period 2 is not among the exclusions. For that case the even right
neighbor must be an aperiodic Fibonacci sequence, column `-4` is `0` at
every even time, and a machine-checked `L_0` left-edge chain dies after
at most four extra steps for every onset width `T<=16`. That is not yet
a proof for arbitrary onset.
[period2_left_edge.md](research/period2_left_edge.md).
Periods 3–7 remain open in the strip.

## Cycle C (2026-09-10)

Period-2 left columns return to vacuum (`F_k = k mod 2`) whenever the
even right neighbor is eventually zero; a 16-state tail machine absorbs
in at most 9 columns. Sound onset enumeration kills every `L_0` width
`T=1..28`, still with no uniform bound.
[period2_vacuum.md](research/period2_vacuum.md).
The period-9 isolated zero and periods 3–7 are still not excluded.
[period9_q8.md](research/period9_q8.md),
[period_p_left_edge.md](research/period_p_left_edge.md).
The prize is still open.

## Cycle D (Astra loop)

GPT-6 Astra (high) ranked six attacks; all were executed. Certificates,
transducers, phase propagation, ancestry automata, block energy, and
Mahler dependency each died at a named obstruction (unbounded residual
memory, full 2-shift labels, no \((d,h)\) cycle, DFAs that reconstruct
the triangle, no pairing, \(\Theta(n^2)\) DAG). The proposed rigidity
implication \(e_p(t,0)=0\Rightarrow e_p(t,-1)=0\) is equivalent to
problem 1 given Jen/Kopra, and is false on a spatially 7-periodic orbit.
[rigidity_ep.md](research/rigidity_ep.md).
Astra’s third pass recommends stopping this program: no remaining attack
that is not another finite table, not equivalent to the prize, and not a
method whose obstruction already fired. The prize is still open.

## Cycle E (creative Astra)

The stop was overridden. Five language-shift attacks all hit their kill
criteria: automaton sections expand as \(\Theta(n^2)\) on every ray;
renewal insulation \(E(w)\le 2|w|+C\) is false on \(0^m1\); dual-particle
residual weight is \(D(N)\) itself; Cartier images of \(U\) reconstruct
the triangle; relative fibre complexities \(R_1=2\), \(R_2=3\) do not
amplify without a free exterior bit.
[automaton_sections.md](research/automaton_sections.md),
[period2_renewal.md](research/period2_renewal.md),
[dual_particles.md](research/dual_particles.md),
[cartier_kernel.md](research/cartier_kernel.md),
[relative_complexity.md](research/relative_complexity.md).

## Cycle F (Astra ideas5)

A second creative set of five was run to completion. Stern–Brocot
bidegree \((2,2)\) has trivial kernel. No holographic matchgate basis
exists in the two prescribed drawings. Adaptive circuit certificates
satisfy \(C(128)\ge 6438\) and \(C(256)\ge 27139\), both above \(0.1n^2\).
Constant \(\mathrm{GL}(2,\mathrm{GF}(2))\) Lax pairs exist but supply at
most one spectral bit, not a seed reconstruction. Dilation correlations
\(C_{p,q}\) have no seed-valid estimate beyond \(|C|\le N\): the pair
\((F^2,F^3)\) is two independently growing cones.
[stern_brocot.md](research/stern_brocot.md),
[matchgate.md](research/matchgate.md),
[adaptive_certificate.md](research/adaptive_certificate.md),
[lax_pair.md](research/lax_pair.md),
[dilation_disjointness.md](research/dilation_disjointness.md).
The prize is still open.

## Cycle G (Astra ideas6)

A third creative set of five was run. Communication rank of the apex
exceeds \(8h\) on a required split at \(h=9,10\). Hashlife reuses
central blocks but charged work stays superlinear and \(n=2^{15}\) did
not complete. Four-letter S-adic substitutions cannot parse the first
1{,}024 centre bits. The ×7 correction stream has signed-binary weight
\(\approx 0.19n^2\). Driven invasion fronts have no feasible drift
certificate.
[communication_rank.md](research/communication_rank.md),
[hashlife_reuse.md](research/hashlife_reuse.md),
[substitution_tiling.md](research/substitution_tiling.md),
[signed_carry.md](research/signed_carry.md),
[invasion_front.md](research/invasion_front.md).
The prize is still open.

## Cycle H (Astra ideas7)

Time-digit concatenation matrices over \(\mathbb F_3\) have rank
\(32>16\) already at block length 5. Noise susceptibility has
\(B_N'(0)=O(N)\) inside the frozen envelope, but higher-order fault
clusters are uncontrolled. Linear block projections do not intertwine
Rule 30 with an additive radius-1 factor. LLL finds no low-height
algebraic equation for the centre real.
[time_digit_matrices.md](research/time_digit_matrices.md),
[noise_susceptibility.md](research/noise_susceptibility.md),
[coarse_bias.md](research/coarse_bias.md),
[algebraic_bitstream.md](research/algebraic_bitstream.md).
The prize is still open.



