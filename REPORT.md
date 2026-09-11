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

## Cycle AD (2026-09-11)

Over \(\mathrm{GF}(2)\), \(G(m,d)\) is the parity of writings of \(d\)
as a sum of one term from each \(\{0,2^i,2^{i+1}\}\) with \(m_i=1\).
The left-diagonal recurrence is either a reset (period dividing the
driver period) or an integrator (period doubling when the driver XOR
is odd). If two consecutive left-diagonals agree and are not
eventually 0, the next is a white stripe. Closed forms give
\(e_7\equiv 0\) and \(e_9\equiv 1\); the same implication on the
period-4 tails of \(e_{26}\) and \(e_{27}\) gives \(e_{28}\equiv 0\).
Each fixed left-diagonal meets the centred 5-window at most five
times, and 1-run endings occupy all eight `11***` windows, so neither
nested left nor a 1-run ending is a production of infinitely many
centre `00`s. Infinitely many white stripes remain open and would not
by themselves give `00`s.
[cycle_ad.md](research/cycle_ad.md).
The prize is still open.

## Cycle AE (2026-09-11)

Right-diagonals \(u(t,k)=x(t,t-k)\) are pure integrators of
\(u_{k-1}\lor u_{k-2}\). The only eventually-constant one is the right
edge, so there are no white stripes on the right (unlike \(e_7\) and
\(e_{28}\) on the left). Each fixed \(k\) meets the centred 5-window
at most five times. The palindrome defect \(d=\ell\oplus r\) is the
Green difference of AND injections to packed bits \(t-1\) and \(t+1\).
A 1-run ending is followed by `00` iff \(x(-2)=r\lor x(2)\). Nested
right is not a `00` production; the remaining gap is a bulk production.
[cycle_ae.md](research/cycle_ae.md).
The prize is still open.

## Cycle AF (2026-09-11)

\(G(1,\cdot)\) is supported on \(\{0,1,2\}\), so the only time-\(s\)
ANDs that hit \(c_{s+2}\) are \((\ell,c)\), \((c,r)\), and
\((r,e)\). The two-step identity is
\(c_{s+2}=1\oplus(\ell\land c)\oplus(c\land r)\oplus(r\land e)\oplus(c'\land r')\oplus O_s\).
At a 1-run ending this is \((r\land\lnot e)\oplus O_s\), and \(O_s\)
takes both values, so the local ANDs do not force `00`. Annulus
parities of `10`, `00`, `11`, and of the 1-run Booleans
\(r\land\lnot e\) and \(a=r\lor e\), are not \(I_k\).
[cycle_af.md](research/cycle_af.md).
The prize is still open.

## Cycle AG (2026-09-11)

The older Green remainder \(O_s\) in the two-step identity equals the
local Boolean \(c''\oplus 1\oplus(\ell\land c)\oplus(c\land r)\oplus(r\land e)\oplus(c'\land r')\)
of the centred 5-window on the prize orbit. At a 1-run ending this is
\(a\oplus e\). Chasing \(O_s=r\land\lnot e\) in the past light cone is
the same 5-window condition as Cycles AD–AE, not a new bulk
production of `00`s.
[cycle_ag.md](research/cycle_ag.md).
The prize is still open.

## Cycle AH (2026-09-11)

For every \(q\ge 1\), Freshman gives
\((1+x+x^2)^{q 2^k}=Q(x^{2^k})\) with \(Q=(1+x+x^2)^q\). The
light-cone edges cancel and the centre contributes, so
\(c_{2qU}=c_{qU}\oplus\Delta^{(q)}_k\oplus J^{(q)}_k\). Cycle Z is
the \(q=1\) case (\(\Delta=0\) by empty extras). For
\(q\in\{3,5,7,9\}\) neither \(\Delta\) nor \(J\) is identically 0 or
a formula for the spine flip (\(\Delta^{(9)}\) dies at \(k=8\)). If
\(c\) is eventually period \(2^m r\) with \(r\) odd, then
\((c_{2^k})\) is eventually periodic with period dividing
\(\mathrm{ord}_r(2)\); \(r=1\) forces eventual constancy, so
infinitely many \(I_k=1\) would kill every power-of-2 period. The
one-step Green remainder \(O^{(1)}=1\oplus\ell\oplus c\oplus r\) is
local and is not \(I_k\).
[cycle_ah.md](research/cycle_ah.md).
The prize is still open.

## Cycle AI (2026-09-11)

Packed Rule 150 for \(2^k\) steps multiplies by
\(1+x^{2^k}+x^{2^{k+1}}\) from every time \(t\), so
\(c_{t+2^k}=c_t\oplus x(t,-2^k)\oplus x(t,2^k)\oplus J_{t,k}\).
Cycle Z is the case \(t=2^k\). \(J_{t,k}\) is a Boolean of the
causal window \([-2^k,2^k]\). The 16-node palindrome graph at
distance 1 has only constant-centre recurrent SCCs (Cycle AB). At
distances 2 and 4 a mixing SCC takes both colours of \(c\), so
eventual palindrome at those distances is not excluded by this
method, and a `00` at \(t\) does not force a `00` at \(t+2^k\).
[cycle_ai.md](research/cycle_ai.md).
The prize is still open.

## Cycle AJ (2026-09-11)

AI’s step from \(t=2^k\) by \(2^{k+1}\) has both extras off the cone, so
\(\theta_k:=c_{3\cdot 2^k}\oplus c_{2^k}\) is the Green AND remainder
on \([2^k,3\cdot 2^k)\). Eventual period \(2^m\) forces \(\theta_k=0\)
(the 3-spine and 1-spine agree). The leftmost 11, which never hits
\(I_k\), always hits \(\theta_k\) because
\(G(2^{k+1}-1,3\cdot 2^k-1)=1\), hence \(\theta_k=1\oplus S_k\).
\(S\equiv 0\) would already kill every \(2^m\) period; it fails.
Infinitely many \(\theta_k=1\) remains open.
[cycle_aj.md](research/cycle_aj.md).
The prize is still open.

## Cycle AK (2026-09-11)

For every \(q=2^a+1\), Cycle AI from \(t=2^k\) by \(2^{k+a}\) gives
\(\varphi^{(q)}_k=c_{q 2^k}\oplus c_{2^k}\) as a Green remainder on
\([2^k,q\cdot 2^k)\). Eventual period \(2^m\) forces every such
\(\varphi\) to 0. A doubling argument on \(G\) shows that the XOR of
leftmost-11 hits on that interval is identically 1, so
\(\varphi^{(q)}_k=1\oplus S^{(q)}_k\) for the whole family (Cycle AJ
is \(q=3\)). \(S\equiv 0\) fails for \(q=3,5,9\). On \(k\le 10\) at
least one of those three is 1 for every \(k\ge 2\); that is not a proof.
[cycle_ak.md](research/cycle_ak.md).
The prize is still open.

## Cycle AL (2026-09-11)

The identity \(\varphi^{(q)}_k=c_{q 2^k}\oplus c_{2^k}=J\) on
\([2^k,q\cdot 2^k)\) holds for every integer \(q\ge 1\), not only
Fermat-odd \(q\). Packed Rule 150 for \((q-1)U\) steps multiplies by
\(Q_{q-1}(x^U)\); only three indices land in the light cone, the
centre coefficient is 1, and the two edges have coefficient
\(v_2(q)\bmod 2\), so they cancel. For odd \(q\), chained Cycle-AI
steps keep extras strictly outside the cone. The XOR of leftmost-11
Green hits is independent of \(k\) and equals
\(1\oplus\mathrm{popcount}(q)\), so \(\varphi^{(q)}=P(q)\oplus S^{(q)}\)
with \(P(q)=1\oplus\mathrm{wt}(q)\). Cycle AK is the even-weight case.
Odd \(p=1\) parity fails for \(q=7\). Eventual period \(2^m\) forces
every integer spine to vanish. [cycle_al.md](research/cycle_al.md).
The prize is still open.

## Cycle AM (2026-09-11)

Packed-bit-4 ANDs fire on every odd \(t\ge 4\) and contribute exactly
once to \(I_k\) (\(k\ge 3\)): the unique Green hit is the first odd
time of the annulus, using \(G(m,2m)=1\). Packed bit 6 contributes 1
for \(k\ge 4\) and cancels that production. New closed forms:
\(e_8(t)=1\) iff \(t\equiv 0,1\pmod{4}\) (\(t\ge 8\));
\(e_{10}(t)=1\) iff \(t\equiv 0,3\pmod{4}\) (\(t\ge 10\)). Nested
remainder through packed bit 9 is then 1, so
\(I_k=1\oplus B_k^{\ge 10}\) for \(k\ge 5\). Bit 10 cancels again.
[cycle_am.md](research/cycle_am.md).
The prize is still open.

## Cycle AN (2026-09-11)

Over \(\mathrm{GF}(2)\), \(x(1+x)\sum_{m<n}(1+x+x^2)^m=1+(1+x+x^2)^n\).
At \(n=2^a\) this is the interval \(W(2^a,D)=1\) iff
\(2^a-1\le D\le 2^{a+1}-2\), which contains Cycle AM’s two endpoint
identities. Mersenne \(G(2^a-1,d)\) is the mod-3 window
\(f(d)\oplus f(d-2^a)\oplus f(d-2^{a+1})\); Fermat \(G(2^a+1,d)\) is
the 3-sparse product with \(1+x+x^2\);
\(W(3\cdot 2^a,D)\) occupies two intervals. The \(W(T,\cdot)\) support
splits \(I_k=I^{\mathrm{left}}\oplus I^{\mathrm{right}}\) on packed
bits \([2,T+1]\) versus \(\ge T+2\). \(I^{\mathrm{left}}=0\) holds on
\(7\le k\le 12\) but is not proved. The time-\(T\) Mersenne slice is
not a formula for \(I_k\).
[cycle_an.md](research/cycle_an.md).
The prize is still open.

## Cycle AO (2026-09-11)

\(G(m,3\cdot 2^k-1)=1\) iff \(m\equiv 2^{k+1}-1\) or
\(3\cdot 2^k-1\pmod{2^{k+2}}\). In the 3-fold annulus only the first
residue appears, so the leftmost 11 hits \(\theta_k\) at exactly one
time, \(t=2^k\). The number \(N(q)\) of such hits on
\([2^k,q\cdot 2^k)\) is independent of \(k\) and has parity
\(1\oplus\mathrm{wt}(q)\); \(N(5)=1\) locates the unique \(q=5\) hit
at \(t=2^{k+1}\). The two-point family of packed bits
\(p=3(2^k-2^j)+1\) is bulk but is not a formula for \(\theta_k\).
[cycle_ao.md](research/cycle_ao.md).
The prize is still open.

## Cycle AP (2026-09-11)

\(G(m,2^a-1)=1\) iff \(2^a\mid(m+1)\). \(G(m,5\cdot 2^k-1)\) occupies
four residue classes modulo \(2^{k+3}\). On the 3-fold annulus these
laws, with Cycle AO’s two-point form, give four unique-Green packed
bits for \(k\ge 3\): \(p=1\) at \(t=2^k\) (always fires),
\(p=2^{k-1}+1\) at \(t=3\cdot 2^{k-1}\), \(p=2^k+1\) at \(t=2^k\)
(centre-right), and \(p=2^{k+1}+1\) at \(t=2^{k+1}\) (centre-right at
\(2U\); the other Mersenne time lies outside the cone). The extra
three take both firing values. Exhaustiveness of the four is a prefix
through \(k=8\).
[cycle_ap.md](research/cycle_ap.md).
The prize is still open.

## Cycle AQ (2026-09-11)

\(G(m,2^a)=\mathrm{bit}_a(m)\oplus(L_a(m)\bmod 2)\), where \(L_a\) is
the run of \(1\)s from bit \(a-1\) downward. The sequence is periodic
of period \(2^{a+1}\) with complementary halves. On the 3-fold
annulus the unique double-Green packed bit is Cycle AO’s
\(p=3\cdot 2^{k-1}+1\) at times \(3U/2\) and \(2U\); it does not
always fire. Five triple-Green bits follow a scaling list on
\(4\le k\le 8\) (prefix).
[cycle_aq.md](research/cycle_aq.md).
The prize is still open.

## Cycle AR (2026-09-11)

\(G(m,q\cdot 2^j-1)=1\) iff \(2^j\mid(m+1)\) and
\(G((m+1)/2^j-1,q-1)=1\). Fermat-odd \(q=2^a+1\) reduces to Cycle AQ
and recovers the two-point and four-point laws. On the 3-fold annulus
the five triple-Green bits and four quadruple-Green bits have closed
times, because the lift window in \(n\) is independent of \(k\). None
of those nine bits is an identically-1 production; bit B’s XOR is not
\(k\bmod 2\). Exhaustiveness of the nine, and bit D never firing, are
prefixes.
[cycle_ar.md](research/cycle_ar.md).
The prize is still open.

## Cycle AS (2026-09-11)

On \(n<2^{a-1}\), \(G(n,2^a-2)=1\) iff \(n=2^{a-1}-1\); for
\(a\ge 3\), \(G(n,2^a-4)=1\) iff \(n=2^{a-1}-2\). Packed bits
\(p=2^j+1\) are unique-Green for \(I_k\) at time \(T=2^{k-1}\), and
\(p=3\cdot 2^j+1\) (\(j\le k-3\)) at time \(T+2^j\). The two
double-Green bits are \(p=5\cdot 2^{k-3}+1\) and
\(p=3\cdot 2^{k-2}+1\). Packed bit 9 always fires at \(T\). The XOR
of unique firings is not \(I_k\). Exhaustiveness of \(2k-2\) unique
bits and two doubles is a prefix.
[cycle_as.md](research/cycle_as.md).
The prize is still open.

## Cycle AT (2026-09-11)

For \(n<2^{a-1}\), \(G(n,2^a-2^b)=1\) iff \(2^{a-1}-1-n\in S_b\),
where \(S_b\) is the Jacobsthal set of size
\((2^b-(-1)^b)/3\). Packed bits \(p=(2^c-1)2^j+1\) on the dyadic
annulus Green-hit at \(t=T+s\cdot 2^j\) for \(s\in S_c\) (when
\(k-j>c\)), recovering Cycle AS at \(c=1,2\). The \(c=3\) family is
triple-Green and not identically 1; the XOR of all Mersenne-odd
families is not \(I_k\).
[cycle_at.md](research/cycle_at.md).
The prize is still open.

## Cycle AU (2026-09-11)

\(G(n,2^a-2^c-1)=1\) iff \(n=2^{a-1}-1\) on the half-window.
Derived laws for \(2^a-6,7,10,12\) give packed bits 10–12 explicit
Green times. The new period-4 tails \(e_{11}(t)=1\) iff
\(t\equiv 2\pmod{4}\) and \(e_{12}(t)=1\) iff \(t\not\equiv 0\pmod{4}\)
make those contributions \(1,0,1\). Hence
\(I_k=1\oplus B_k^{\ge 13}\) for \(k\ge 5\). Nested depth 12 is not a
closed form.
[cycle_au.md](research/cycle_au.md).
The prize is still open.

## Cycle AV (2026-09-11)

Unique half-window \(G\)-supports are exactly Cycle AS’s \(2\)-family
and \(3\)-family (induction on the doubling recurrence and the
\(W\)-interval). Unique-Green packed bits for \(I_k\) are therefore
exactly those \(2k-2\) indices. The tails \(e_{13},\ldots,e_{17}\)
are period 4, so bits 13 and 17 contribute \(0\). The remaining
unique \(3\)-family fires at \(k=15\); the double \(p=3T/2+1\) has
XOR \(1\) at \(k=12\). Nested left is not a formula for \(I_k\).
[cycle_av.md](research/cycle_av.md).
The prize is still open.

## Cycle AW (2026-09-11)

For \(a\ge 4\) there are no even half-window doubles of \(G\). Both
double targets are the odd lifts of the \(a=4\) pair, so
\(|S(a,D)|=2\) iff \(D=2^{a-2}-1\) or \(D=3\cdot 2^{a-3}-1\).
Double-Green packed bits for \(I_k\) are exactly \(p=3T/2+1\) and
\(p=5T/8+1\). All left-diagonals eventually period 4 is false
(\(e_{29}\) has period 8). Bit 33 firing at \(T\) is a prefix.
[cycle_aw.md](research/cycle_aw.md).
The prize is still open.

## Cycle AX (2026-09-11)

Even half-window triples are \(2^a-\{6,8,10,14\}\) for \(a\ge 5\);
odd triples are one doubling of a previous triple. Packed bits are
the families \(p=q\cdot 2^{j}+1\) for \(q\in\{5,7,9,13\}\), with
times from \(s\in\{0,1,2\}\), \(\{0,2,3\}\), \(\{1,2,4\}\),
\(\{0,5,6\}\). Bits 14 and 15 contribute \(0\). Triple XOR is not
\(I_k\). Exactly five quads is a prefix.
[cycle_ax.md](research/cycle_ax.md).
The prize is still open.

## Cycle AY (2026-09-11)

Packed bit 16 is Jacobsthal \(S_4=\{1,4,5,6,7\}\) and contributes
\(0\). The new period-4 tail \(e_{18}(t)=1\) iff \(t\equiv 1,2\pmod{4}\)
(\(t\ge 20\)) makes \(e_{18}\land e_{17}\) identically 0, so bit 18
never fires. Hence \(I_k=1\oplus B_k^{\ge 19}\) for \(k\ge 5\). Nested
depth 18 is not a closed form.
[cycle_ay.md](research/cycle_ay.md).
The prize is still open.

## Cycle AZ (2026-09-11)

For \(a\ge 6\) there are no even half-window quads, so the five quads
are the odd-lift orbit of \(\{18,19,23,27,29\}\) at \(a=5\). Packed
bit 19 is the \(j=1\) 9-family triple and contributes 1 for
\(k\ge 6\), hence \(I_k=B_k^{\ge 20}\). Nested depth 19 is not a
closed form. Quad XOR is not \(I_k\).
[cycle_az.md](research/cycle_az.md).
The prize is still open.

## Cycle BA (2026-09-11)

Even half-window pentuples are \(2^a-\{12,16,18,20,26,28,34,50\}\) for
\(a\ge 7\); odd pentuples are one doubling of a previous pentuple.
Packed bits are the families \(p=r\cdot 2^{j}+1\) for
\(r\in\{11,15,17,19,25,27,33,49\}\), with times from the eight
\(s\)-sets. The tails \(e_{20},\ldots,e_{27}\) are period 4 and
\(e_{30}\equiv 1\) for \(t\ge 33\), so bits 20, 24, and 25 never fire.
Pentuple XOR is not \(I_k\). Nested left is still not a closed form.
[cycle_ba.md](research/cycle_ba.md).
The prize is still open.

## Cycle BB (2026-09-11)

There are no even half-window sextuples for \(a\ge 8\), so the five
sextuples are the odd-lift orbit of \(\{66,67,71,77,85\}\) at \(a=7\).
Even septuples stabilize at ten seeds
\(2^a-\{22,30,36,52,66,68,98,100,130,194\}\) for \(a\ge 9\). Packed
bit 22 is the \(j=0\) 21-family septuple and contributes 1. Sextuple
XOR and septuple XOR are not \(I_k\). Nested left is still not a
closed form.
[cycle_bb.md](research/cycle_bb.md).
The prize is still open.

## Cycle BC (2026-09-11)

There are no even half-window octuples for \(a\ge 10\), so the eleven
octuples are the odd-lift orbit of
\(\{258,259,263,269,329,369,393,401,433,465,481\}\) at \(a=9\). Even
nonuples stabilize at ten seeds
\(2^a-\{38,54,132,196,258,260,386,388,514,770\}\) for \(a\ge 11\).
Octuple XOR and nonuple XOR are not \(I_k\). Nested left is still not
a closed form.
[cycle_bc.md](research/cycle_bc.md).
The prize is still open.

## Cycle BD (2026-09-11)

Cycle BA’s \(e_{27}\) period 4, \(e_{28}\equiv 0\), and
\(e_{30}\equiv 1\) force period-8 tails for \(e_{29},e_{31},e_{32},e_{33}\).
The AND at packed bit 33 fires iff \(t\equiv 0\pmod{8}\), and
\(T=2^{k-1}\equiv 0\pmod{8}\) for \(k\ge 4\), so bit 33 contributes 1
for every \(k\ge 7\). This upgrades Cycle AW’s prefix. Nested left is
still not a closed form.
[cycle_bd.md](research/cycle_bd.md).
The prize is still open.

## Cycle BE (2026-09-11)

Cycle AK’s Fermat covering (at least one of
\(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\) is 1) holds through
\(k=15\), not only \(k=10\). No single Fermat \(q\le 17\) is
identically 1. Still a prefix: a proof for all \(k\ge 2\) would kill
every eventual period \(2^m\). Nested left is still not a closed form.
[cycle_be.md](research/cycle_be.md).
The prize is still open.













