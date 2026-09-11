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
The leftover CFG parse-parity attack is recorded in Cycle I.
The prize is still open.

## Cycle I (ideas8, 2026-09-10)

The leftover Chomsky parse-parity freeze is unsatisfiable: no grammar
with four nonterminals and at most eight binary productions realises
\(c_n\) as the GF(2) parse count of \(\operatorname{bin}(n)\) on
\(n=1,\ldots,1023\).
[cfg_parse_parity.md](research/cfg_parse_parity.md).

A Condrey-style unique-left reconstruction at period 2 yields a
**finite theorem**, not a prize claim: every nonzero row of support
radius \(w\le 10\) has every period-2 centre run of length at most 24
inside \(tcap=8w+128\). The reconstructed left is infinite in the scan
but has no closed form, so this is not a uniform exclusion.
[period2_fiber.md](research/period2_fiber.md).

The 2-kernel of \(c\) is full through depth 12 on length-128 prefixes
(\(|K|\ge 4096\)); that is not an infinite-kernel proof. XOR-recodings
(first difference, \(t\bmod 2\), paperfolding, Laplacian, Thue–Morse)
all still have \(L(N)\approx N/2\). Packed-row OR-overlaps stay at
density \(\approx 1/2\). Left-permutivity forbids coalescence inside
the light cone. Residue-class discrepancies that vanish at \(N=10^5\)
fail on dyadic lengths.
[two_kernel.md](research/two_kernel.md),
[xor_transform.md](research/xor_transform.md),
[packed_valuation.md](research/packed_valuation.md),
[coalescence.md](research/coalescence.md),
[residue_discrepancy.md](research/residue_discrepancy.md).
The prize is still open.

## Cycle J (ideas9, 2026-09-10)

The constant \(L_{\mathrm{run}}\le 24\) dies at radius 11: mask
\(4369552\) has a period-2 centre burst of length 29 that survives
doubling the time cap. Cycle I’s statement for \(w\le 10\) *inside*
\(tcap=8w+128\) is unchanged; even at radius 10 a longer window
reveals a length-25 burst truncated by that cap.
[period2_lrun.md](research/period2_lrun.md).

Period-3 and isolated-zero period-9 finite-row scans have no eventual
witness, but \(L_3(w)\) and \(L_{\mathrm{iso}}(w)\) still grow through
the scanned radii, so they do not inherit a period-2-style plateau.
Short \(d\le 3\) matrix traces over \(\mathbb F_2\) and \(\mathbb F_3\)
are unsat on \(t=1,\ldots,255\).
[period3_fiber.md](research/period3_fiber.md),
[period9_fiber.md](research/period9_fiber.md),
[trace_product.md](research/trace_product.md).
The prize is still open.

## Cycle K (ideas10, 2026-09-11)

Concatenating Cycle J maximizers never exceeds length 29. A different
radius-17 row (mask \(281769\)) has a period-2 centre burst of length
31 that Cycle J’s shorter cap misses. That kills the constant 29, not
eventual period 2, and is not an unbounded family.
[period2_lrun_family.md](research/period2_lrun_family.md).

Period-5 finite-row runs still grow at radius 7; period 4 only plateaus
at the scan edge. Defects that break alternation have density \(\approx 1/2\)
and \(L(N)\approx N/2\), so they carry \(D(N)\). Cheap summaries of the
packed row do not determine the next centre bit.
[period45_fiber.md](research/period45_fiber.md),
[period2_defects.md](research/period2_defects.md),
[stream_nextbit.md](research/stream_nextbit.md).
The prize is still open.

## Cycle L (ideas11, 2026-09-11)

A complete-up-to-translation census of Hamming weight \(\le 8\) and
span \(\le 24\) (35 million placements, long cap) has max period-2
centre run 35. Every recorded run of length \(\ge 32\) has the origin
outside the live hull; origin-in-hull still maxes at 31 on that dump.
No run of length 40, and span is not strictly increasing.
[period2_weight8.md](research/period2_weight8.md).

Periods 6 and 7 still grow at radius 6. A period-2 centre does not
force any locally illegal \(3\times 3\) or \(4\times 4\) block: the
residual strip SCC is nonempty.
[period67_fiber.md](research/period67_fiber.md),
[forbidden_periodic.md](research/forbidden_periodic.md).
The prize is still open.

## Cycle M (ideas12, 2026-09-11)

Restricted to origin-in-hull placements, every Hamming-weight-\(\le 8\)
span-\(\le 24\) row has period-2 centre run length at most 31 (12 million
placements; maximizer still mask \(281769\)). Off-hull length-35 rows
are excluded by construction. This is a finite theorem for that class,
not a uniform exclusion of eventual period 2: a later prize-seed row
has weight \(\Theta(T)\) and span \(2T\).
[period2_hull.md](research/period2_hull.md).

Fixing the leftmost 1 at \(-w\) (the prize light-cone edge) does not
cut the bursts: the short-cap table matches unrestricted Cycle I, and
a long cap still grows (\(L=24,25,27\) at \(w=8,9,10\)).
[period2_leftbit.md](research/period2_leftbit.md).
The prize is still open.

## Cycle N (ideas13, 2026-09-11)

Origin-in-hull weights 9 and 10, span \(\le 20\), still have
\(L_{\mathrm{run}}\le 31\) (5.8 million placements). The maximizer is
mask \(806057\): Cycle M’s eight-one row plus a ninth 1 at \(+2\), same
burst \(t=320\ldots351\). Not a uniform exclusion.
[period2_hull910.md](research/period2_hull910.md).
The prize is still open.

Defects that carry \(D(N)\) are not a width-\(\le 8\) CA on the prize
seed: \(d_{t+1}\) is a Boolean of \((c_t,l_t,r_t)\), which is the
original radius-1 slice and does not close on the centre column.
[defect_recurrence.md](research/defect_recurrence.md).

## Cycle O (ideas14, 2026-09-11)

The unique left of a period-2 centre is the `L_0` problem at time 0:
no bypass via a Condrey-style closed form, and vacuum `u` is not
eventually period 7 (the `(0001010)` run breaks at even-time index
152). The `R≥4` identity that sends a long `L_0` to an `011` bump
under `S` is algebraic; the bump does not decrease Hamming weight or
last-1, and it hits `F_4=0` only for `T∈{2,3}`. Sound onsets `T=33,34`
die with `maxR=14,12`. Worst remains `T=20`, `R=16`.
[period2_germ.md](research/period2_germ.md).
The prize is still open.

## Cycle P (ideas14 items 2–3, 2026-09-11)

While a period-2 centre is in phase `01`, the even right neighbor `u`
has no five consecutive zeros. The pair `(e,f)` while `u=0` walks an
acyclic four-state graph whose unique longest path is
`11→01→10→00`, independent of the right half past column 5. Together
with no consecutive 1s this is the SFT forbidding `{11,00000}`. The
`T=20` onset with `R=16` already lies in that SFT, so period 2 is not
excluded. `F^2` is lag-2 permutive and not lag-1, so Kopra width 1 for
the even lattice is false.
[period2_ugap.md](research/period2_ugap.md).
The prize is still open.

## Cycle Q (ideas14 items 1, remainder of 2, and 5; 2026-09-11)

Morse–Hedlund rigidity of long `L_0` germs is false: last-sat words at
`T=20` and `T=22` have `p(n)>n` through half their length, so a long
zero run in `F` does not force a periodic `u`-tail. Free `(g,h)`
realises every length-8 word of the gap-4 SFT `X`; realizable `u` is
exactly `X`, not a proper subshift. Three of the six `T=20`, `R=16`
models lie in `X` and still die only at `F_37`. Driven isolated-zero
`q=8` does not force `σ` eventually periodic (35 mixers among 63
rights of width `≤5`).
[cycle_q.md](research/cycle_q.md).
The prize is still open.

## Cycle R (2026-09-11)

The even-decimation disagreement \(d(k)=\min\{n\ge 1:c_n\ne c_{n 2^k}\}\)
is not injective, so \(\{v_k=(c_{2^k n})\}\) is not an infinite 2-kernel
family by this route. The unique left of a period-2 centre, applied to
the prize row at time \(T\), does not miss the left light-cone edge
uniformly (predicted \(x(T,-T)=0\) for only 92 of 192 onsets).
[cycle_r.md](research/cycle_r.md).

Problem 2 has an exact rewrite: writing \(N_{11}\) and \(N_{00}\) for
the consecutive equal-bit pair counts,

\[
D(N)=N_{11}-N_{00}+c_{N-1}.
\]

Unsigned defect density \(\approx 1/2\) (Cycle K) therefore does not
kill density \(1/2\): only signed cancellation of \(11\) against \(00\)
is required. Adjacent \(1\)-run and \(0\)-run lengths are equal only
\(33.5\%\) of the time, so a local pairing fails. The prize is still
open.

## Cycle S (2026-09-11)

The lag-2 inverse of \(F^2\) is not a Condrey fiber: it determines
only column \(-2\), and on phase `01` that bit is the even right
neighbor \(u\) (already `fold_bit`). Spatial windows of radius
\(\le 8\) about a \(11\) do not determine the displacement to the
next \(00\). A width-8 right-edge word at time \(\lfloor t/2\rfloor\)
does not force an odd-time \(11\) at \(t\).
[cycle_s.md](research/cycle_s.md).
The prize is still open.

## Cycle T (2026-09-11)

Isolated-one words \(10^q\) do not acquire a Jen-forced neighbor at
radius 6 for any \(q\le 17\). The integer identity
\(e_t=c_t+c_{t+1}-1\) is \(1_{11}-1_{00}\) and recovers \(D(N)\); it is
not a packed-row current. First disagreement against residue 0 is not
an injective fingerprint of the other \(2^k-1\) kernel columns
(\(k=3\)).
[cycle_t.md](research/cycle_t.md).
The prize is still open.

## Cycle U (2026-09-11)

Every binary word of length \(\le 14\) is a factor of the centre
(witness: prefix \(2^{18}\)). An eventual period would therefore
satisfy \(T+p\ge 16384\). Twelve length-15 words are missing from that
prefix, so the language is not yet certified as the full 2-shift.
Predicted 2-kernel disagreement indices
(\(i=0,1,v_2(s-r),\mathrm{popcount}(r\oplus s),k-1\)) all fail.
[cycle_u.md](research/cycle_u.md).
The prize is still open.

## Cycle V (2026-09-11)

The \(p\)-step centre of Rule 30 depends on both light-cone edges:
a single \(1\) at \(\pm p\) is a shifted prize seed, whose left or
right edge lands on the origin after \(p\) steps. Thus \(F^p\) has
Kopra width \(2p\) for every \(p\ge 1\), and width-1 rapid left
expansivity never applies to an iterate. The prize even-right
neighbour has short factors in the period-2 SFT \(X\) (so it is not
uniformly excluded from \(X\)) and has many \(11\)s with max gap 46
in a \(2^{17}\) sample, which is not an infinitude proof. First
even-decimation disagreements stay in \(\{1,2,3\}\) through depth 15
without a closed form.
[cycle_v.md](research/cycle_v.md).
The prize is still open.

## Cycle W (2026-09-11)

The 4-step \((e,f)\) drain of Cycle P can sit inside two of the three
\(X\)-legal \(T=20\), \(R=16\) last-sat words, which still realise 16
zeros of \(F\) after a 1; the third word has max zero run only 3, so
the drain is not even universal on the worst onset. Closed forms for
\(c_{2^k}\) (parity, popcount, Rowland \(a(k)\)) fail by \(k\le 7\).
A centre `11` at time \(2^k\) is not uniform.
[cycle_w.md](research/cycle_w.md).
The prize is still open.

## Cycle X (2026-09-11)

The zero configuration is a fixed point with \(2c-1=-1\), so no
finite-window coboundary (nor a 2-phase family, nor a pair current)
can carry \(D(N)\) on all orbits. The prize light cone itself stays in
the spatial 5-window `00000` for five consecutive times, so the same
obstruction holds on this orbit. Gaussian elimination over \(\mathbb Q\)
kills every coboundary and bond-flux identity of width \(\le 5\) for
\(2c-1\), \(c_t+c_{t+1}-1\), and even the vacuum-compatible target
\(2c\). Every spatial 7-window about the origin occurs by \(t<2^{14}\).
Condrey’s zeros in column \(-1\) plus infinitely many 1s in \(c\) do
not force a centre `11`: period-2 phase `01` avoids \((c,\ell)=(1,0)\).
[cycle_x.md](research/cycle_x.md).
The prize is still open.

## Cycle Y (2026-09-11)

If \(v_k=v_{k+1}\) then \(v_k[n]=v_k[2n]\) for all \(n\), so
\((c_{2^j})_{j\ge k}\) is constant. A non-eventually-periodic
\((c_{2^k})\) therefore yields an infinite 2-kernel. Packed Rule 30
is Rule 150 XOR adjacent ANDs; Rule 150 from a single 1 has centre
identically 1 by palindrome. Predicted sibling-split indices
(including Rowland’s diagonal period) are not universal. Eventual
constancy of \((c_{2^k})\) is still open.
[cycle_y.md](research/cycle_y.md).
The prize is still open.

## Cycle Z (2026-09-11)

One doubling of packed Rule 150 sends the dyadic centre to itself XOR
the Green parity \(I_k\) of AND injections on \([2^{k-1},2^k)\): the
linear image of the half-time row is exactly \(b_{k-1}\) because both
light-cone edges are 1. Thus \(b_k=b_{k-1}\oplus I_k\), and \((b_k)\)
is eventually constant iff \(I_k\) is eventually 0. Local formulas for
\(I_k\) (3-window at half-time, unweighted 11-parity, right-edge AND)
fail. [cycle_z.md](research/cycle_z.md).
The prize is still open.

## Cycle AA (2026-09-11)

The central trinomial coefficient \([x^m](1+x+x^2)^m\) is \(1\) over
\(\mathrm{GF}(2)\) for every \(m\), so every centre-right AND
\(c_t\land r_t\) on \([2^{k-1},2^k)\) contributes to \(I_k\). This is
not a closed form: the off-centre remainder already disagrees at
\(k=3\). Packed bit 1 is identically 1 for \(t\ge 1\), but that
leftmost 11 never reaches the next dyadic centre.
\(G(m,m-1)=v_2(m+1)\bmod 2\). Mersenne-time 3-windows and small
recurrences for \(I_k\) fail.
[cycle_aa.md](research/cycle_aa.md).
The prize is still open.

## Cycle AB (2026-09-11)

The Rule 30 update makes \(c\oplus c'=\ell\oplus r\oplus(c\land r)\),
so summing over a dyadic annulus telescopes to \(I_k\). The Green
remainder is therefore the palindrome-defect parity
\(R_k=\bigoplus(\ell\oplus r)\). That defect cannot be eventually 0
(it would force an eventually constant centre). Spatial vacuums about
the origin have radius at most 7 on \(t<2^{16}\) and do not construct
the length-19 centre 0-runs. Infinitely many centred `000`s would
kill every isolated-zero eventual period, including period 2; that is
unproved.
[cycle_ab.md](research/cycle_ab.md).
The prize is still open.

## Cycle AC (2026-09-11)

Centre `00` is the triple `000` or `101`, not `000` alone. Those
triples arise from four 5-windows each (32-case local check). Every
left-diagonal \(e_j(t)=x(t,-t+j)\) is eventually periodic: the packed
step is a one-bit recurrence driven by two previous diagonals, hence
a \(2p\)-state machine. The centre samples the onset \(e_t(t)\), which
leaves the periodic tail at \(j=18\), so the tails are not a formula
for \(c\). Infinitely many `00`s remain unproved.
[cycle_ac.md](research/cycle_ac.md).
The prize is still open.








