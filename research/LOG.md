# Persistent research log

Goal created 2026-09-09 21:49 UTC: find a rigorously checked solution to at
least one Rule 30 prize problem. User authorized sustained work and continued
Luna swarm. No submission or contact is authorized. Goal remains active.

## Cycle A

New verified partial theorem: center has infinitely many 0s AND 1s.
The eventually-zero case forces a nondecreasing binary right neighbor and
then an eventually constant width-2 trace. See constant_tails.md. This
repairs an overlooked step in the first report; no novelty claim.

Primary source: Kopra 2023, DOI 10.1016/j.tcs.2022.12.018, generalizes Jen's
width-2 aperiodicity theorem. No direct width-1 theorem found there yet.

New exact experiment: strip_graph.py enumerates finite-width spacetime
constraints under a periodic center. A genuine eventual periodic-center
orbit must eventually remain in a recurrent SCC at every fixed width. If
every such SCC forces a periodic neighbor, the width-2 theorem excludes it.
Outer boundary values are arbitrary, so surviving paths are NOT claimed
to extend to the single-seed global spacetime.

strip_extend.py extends only recurrent strip states, and safely removes
SCCs with a forced periodic neighbor. Self-check compares unpruned extension
to full enumeration through radius 4 for four words. The alternating word
01 still has 114,281 surviving states at radius 23, when the 100,000-state
soft cap is reached. Three residual SCCs survive. Thus this bounded-strip
test does not exclude period 2 at the explored widths.

Mahler supports: exact recurrence S_k=Inc(S_(k-1) symmetric_difference
S_(k-2) symmetric_difference OR_convolution(S_(k-1),S_(k-2))), counting
OR products with parity. Verified through k=35. Full supports grow quickly.
The next task is target-index truncation, subset-zeta acceleration, and
minimum-index/leading-bit invariants.

2-adic experiments recover known edge repetition lengths (Rowland's
sequence). No cheap center-bit extraction or lower bound follows. Coordinate
orientation and claimed row-prefix values still require final source cleanup.

## Active assignments after cycle A

- nonperiodicity agent: alternating-center sideways reconstruction and
  whether finite left support can be ruled out in the spatial limit.
- balance agent: exact truncated Mahler supports and dyadic invariants;
  correct its initial linearized formula and verify all numerical claims.
- complexity agent: disagreement evolution between x and F^2(x), with
  a periodic erasure constraint at the center, and front-speed arguments.
- root: finite-strip symbolic analysis, source audit, proof review, and
  stronger seed-specific constraints.

Files are owned separately. Agents must not overwrite root scripts. Initial
exploratory notes can contain superseded arguments; REPORT.md and this log
track the checked conclusions.

## Cycle B

Isolated-zero family `01^q`: for `q=7` and every `q>=9`, the radius-6
strip has a unique recurrent component whose left neighbor is periodic,
so Jen/Kopra exclude that eventual center. The infinite tail `q>=17` is
a finite gadget (14-state cruise plus wrap-through-zero); `9<=q<=16`
are finite graphs. Period 9 (`q=8`) is a genuine exception: an extra
last-1 prefix with bit 4 equal to 1 keeps both left bits alive.
Proof: isolated_zero_uniform.md. Certificate: isolated_zero_uniform.py,
checked through `q=40`.

Period 2: `u_{n+1}=1` iff a width-3 right vacuum; `u` has infinitely
many isolated 1s else Jen. Left reconstruction ignores the odd right
neighbor. Unreduced `F_4=u_0 u_1`, hence `x(2n,-4)=0` on legal `u`.
Onsets `T=2` and `T=4` are impossible. On-demand SAT gives finite
`L_0` lifetime for every `1<=T<=16` (longest is `T=8` for five times).
No uniform-in-`T` bound yet. See period2_neighbor.md and
period2_left_edge.md.

Periods 3–7 and the period-9 isolated zero still have residual strip
SCCs at radius 6–8; extend hits the state cap. Algebraic one-period
maps do not force a periodic neighbor word. small_periods.md.

Prize status: still unsolved. Next: a `T`-independent lifetime bound
for the period-2 left edge, or a seed-specific constraint that the
strips omit.

## Cycle C (2026-09-10)

Period 2, left edge. New lemma: eventually-zero Fibonacci `u` makes
`F_k` eventually equal to `k mod 2` (16-state tail machine, absorb in
at most 9 columns), so `L_0` is impossible for those `u`. Sound onset
enumeration (variable bound `max_index(F_k) <= floor((k-1)/2)`) kills
every onset width `T=1..28`; longest extra is `R=16` at `T=20`. No
uniform-in-`T` bound. period2_vacuum.md, period2_vacuum.py.

Period 9 (`q=8`): still mixed. Unique residual SCC at radius 6–9; left
bit on the isolated 0 takes both values in one component. Constant
`sigma` is Jen-excluded; mixing is the obstruction. period9_q8.md.

Periods 3–7: injection, double-1, vacuum-triangle, and the local window
`10010` (hence `x(3n+2,-4)=0` on `001`, `x(4n,-4)=0` on `0111`). No
Jen pair. `L_0` chains for `T<=8` die by `s<=4`. period_p_left_edge.md.

Prize status: still unsolved.

## Cycle D (Astra loop, 2026-09-10)

GPT-6 Astra (high) ranked six attacks. All were run. None solves a prize
problem.

1. Period-2 ideal certificates: explicit multipliers for `T<=12`; linear
   ansatz fails at 16 and 20; shift `F_{T+3}=1+F_{T+1}(Su)` maps `L_0`
   to a bump, not a smaller `L_0`. Residual memory grows with `T`.
   period2_certificate.md.
2. q=8 `σ` transducer: 20-state graph is a full 2-shift. Depth-wrap of
   `I` can be eventually periodic without `σ` being so. period9_sigma.md.
3. Phase-mask propagation for `001`/`0111`: no closed `(d,h)` with `h<d`.
   period_p_propagate.md.
4. Inverse ancestry transducer: `L_d` DFAs grow (3,7,16,35,71,141);
   local center factors fill the 2-shift; pinning the kernel to `1` is
   the original triangle. ancestry_transducer.md.
5. Block energy: `E_m ~ N` empirically, no pairing identity. Attack
   stopped. block_energy.md.
6. Mahler dependency: `Θ(n²)` DAG, zeta cancellation is the CA.
   mahler_dependency.md.

Astra retarget: rigidity `e_p(t,0)=0 eventually ⇒ e_p(t,-1)=0 eventually`.
Proved equivalent to problem 1 given Jen/Kopra (`A_p ⇒ B_p` iff `¬A_p`).
False on a spatially 7-periodic orbit for `p=2`. Unproved on the seed.
rigidity_ep.md.

q=8 local invariant excluding vacuum quotient `I`: 1-site full shift
enters `I`; 2-/3-site closures neither enter `I` nor stabilize.
period9_invariant.md.

Astra’s third pass: **stop**. No remaining attack that is not another
finite table, not equivalent to problem 1, and not a method whose
obstruction already fired. Rigidity restates \(\neg A_p\). The q=8
closures do not prove nonexistence of a 2–3-site \(K\).

Prize status: still unsolved. Computational program stopped.

## Cycle E (creative Astra, 2026-09-10)

Human overrode the stop. Astra proposed five language-shift attacks; all
hit their kill criteria.

1. Automaton-group sections: wreath identities, Θ(n²) expansion on every
   query ray. automaton_sections.md.
2. Renewal insulation E(w)≤2|w|+C is false: E(0^m 1)=8m-14. period2_renewal.md.
3. Dual-particle C↔R pairing is exact; residual weight is D(N). dual_particles.md.
4. Cartier images of U do not close; diagonal witnesses reconstruct the
   triangle. cartier_kernel.md.
5. Relative R_m: only R_1=2, R_2=3 proved; amplification needs a free
   exterior bit. relative_complexity.md.

Prize status: still unsolved.

## Cycle F (Astra ideas5, 2026-09-10)

Human still overrode stop. Astra’s second creative set of five was run.
Items 1–3 had already been certified; items 4–5 were completed in this
pass. All five hit their kill criteria.

1. Stern–Brocot row coordinates: bidegree-(2,2) fit on rows 0–63 has
   rank 18, kernel 0. Empty family. stern_brocot.md.
2. Matchgates: no GL(2) holographic transform makes the complete tensor
   family into matchgates in either prescribed drawing. matchgate.md.
3. Adaptive certificates: C(128)≥6438 and C(256)≥27139, both >0.1 n².
   No subquadratic evaluator. adaptive_certificate.md.
4. Lax pairs: 36 constant GL(2,F2) solutions under M(0,0,0)=I; six are
   configuration-blind; the rest have at most a 1-bit monodromy trace.
   Affine L0+λ L1 screen empty. Restricted GL(3) catalog: 252 solutions,
   same obstruction. Isolated traces do not reconstruct the seed.
   lax_pair.md.
5. Dilation disjointness: C_{p,q}(2^14)/N is O(10^{-2}) for primes
   through 13, but the (2,3) symbolic pass yields only independently
   growing cones (speeds 4 and 6). Bounded edges do not determine
   s_{2n}s_{3n}. No estimate stronger than |C|≤N. dilation_disjointness.md.

Prize status: still unsolved.

## Cycle G (Astra ideas6, 2026-09-10)

Astra’s third creative set of five was run. All five died.

1. Communication rank of the apex \(f_h\): GF(2) rank exceeds \(8h\) on
   the left-of-centre split at \(h=9\) (79>72) and \(h=10\) (104>80).
   Central features are high-degree truth tables, not a recursive rule.
   communication_rank.md.
2. Hashlife block reuse: central cache hits dominate, but \(W(n)\) stays
   superlinear (\(W(2^{14})/W(2^{13})=3.61\)), no closed recurrence, and
   \(n=2^{15}\) did not complete. Not \(O(n)\). hashlife_reuse.md.
3. Nonuniform substitutions: all four binary digrams occur in the first
   1024 centre bits, saturating four letters at the finest length-2
   level; no two-morphism S-adic parse to a short seed.
   substitution_tiling.md.
4. Signed ×7 corrections: \(Z_{t+1}=7Z_t-2Q_t\) holds, but
   \(S(n)/n^2\approx 0.19>0.05\) at \(n=256\) and \(512\). signed_carry.md.
5. Invasion fronts for `001`/`0111`: finite pulses exist; repeating the
   putative wake destroys the travelling match; Astra drift is infeasible
   on a left-moving defect outside an 8-zero window. invasion_front.md.

Prize status: still unsolved.

## Cycle H (Astra ideas7, 2026-09-10)

Astra ranked five more attacks. Time-digit matrices, noise, and
coarse-graining were run first; the algebraic bitstream screen was run
as well.

1. Time-digit concatenations over F_3: rank \(H_5=32>16\), then full
   rank \(2^\ell\). No 16-dimensional digit evaluator. time_digit_matrices.md.
2. Noise susceptibility: \(B_N'(0)=O(N)\) below \(8N^{3/2}\); noisy
   means unresolved vs the exponential envelope; pair faults uncontrolled.
   Route abandoned. noise_susceptibility.md.
3. Bias-preserving coarse-graining: zero factor diagrams for linear P
   and additive radius-1 G. coarse_bias.md.
5. Algebraic \(\alpha=\sum c_t 2^{-t-1}\): LLL finds no degree-2..6
   height-\(\le 2^{16}\) polynomial with a root in \(I_{256}\).
   algebraic_bitstream.md.

(CFG parse-parity of bin(n), item 4, completed in Cycle I: unsat.)

Prize status: still unsolved.

## Cycle I (2026-09-10)

Leftover ideas7 item 4 plus five new screens. One finite theorem; the
rest hit their kill criteria. No prize claim.

1. CFG parse-parity of bin(n): 4 NT, ≤8 binary productions, no ε/unit.
   Bit-sliced CYK over 5.13e9 subsets; unsat on n=1..1023 in 644s.
   Nested 2- and 3-NT freezes also unsat. cfg_parse_parity.md.
2. 2-kernel of c: distinct length-128 prefixes = 2^k through k=12.
   Finite lower bound |K|≥4096, not an infinite kernel. No disagreement
   lemma. Kill the proof-via-automaticity route. two_kernel.md.
3. Period-2 finite-row fiber (Condrey analogue): every nonzero row of
   radius w≤10 has L_run(w)≤24 inside tcap=8w+128. Unique left is
   infinite in the scan, not a closed-form tail. Verdict FINITE_THEOREM;
   not a uniform exclusion. period2_fiber.md.
4. Packed-row OR-overlaps: mean N_t/t≈0.50 at T=16384>0.05. Valuations
   of z XOR shifts do not extract c_t. packed_valuation.md.
5. XOR-transforms of c: a_t, first difference, paperfolding, Laplacian,
   Thue–Morse XOR all have L(N)≈N/2 and discrepancy of the same order
   as D(N). xor_transform.md.

Extras: coalescence killed by left-permutivity (disagree at time W+1);
residue-class exact zeros at N=10^5 do not persist dyadically.

Prize status: still unsolved. Next: upgrade L_run≤24 to a uniform-in-w
bound, or run the same finite-row scan at periods 3–7 and q=8.

## Cycle J (2026-09-10)

Ideas9. The constant-24 hope dies; periods 3 and q=8 do not plateau;
short traces are unsat. No prize claim.

1. Period-2 L_run extension: exhaustive w=11 (2^{23}-1 states).
   L_run(11)=29, witness mask 4369552, run t=159..188, stable at
   tcap=432. Ten masks have L≥25 after doubling. A radius-10 row
   (mask 1082165) reaches L=25 only past Cycle I’s cap. period2_lrun.md.
2. Period-3 finite rows w≤8: L3=[11,11,12,12,17,18,20,20,22], still
   growing, n_eventual=0. period3_fiber.md.
3. Isolated-zero q=8 finite rows w≤7: L_iso grows to 23, no eventual
   01^8 witness. period9_fiber.md.
4. Trace of d≤3 products over F2/F3: unsat on t=1..255. trace_product.md.

Prize status: still unsolved. Next: leftover streaming next-bit
(ideas9 item 5); whether L_run(w) is unbounded; periods 4–7.

## Cycle K (2026-09-11)

Ideas10. No prize claim.

1. L_run families: concat/repeat of 4369552 and 7503 never beat L=29.
   Hunt found w=17 mask 281769 with L=31 (t=320..351), stable at
   tcap=784; Cycle J cap 8w+128 misses it. Not an unbounded family.
   period2_lrun_family.md.
2. Periods 4–5, w≤7: L5 still grows (max 22 at w=7); L4≤22 on w=6..7
   only. No eventual witness. period45_fiber.md.
3. Defect pairing: density 0.4997 at N=10^5, L(d)/n=0.5, D almost
   entirely on defects. period2_defects.md.
4. Streaming next bit: popcount/v2/windows fail on t=8..4096.
   stream_nextbit.md.

Prize status: still unsolved. Next: leftover forbidden-spacetime-block
search (ideas10 item 5); periods 6–7; seed-specific constraints the
all-finite-row scans omit.



