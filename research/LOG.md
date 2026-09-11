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

## Cycle L (2026-09-11)

Ideas11. No prize claim.

1. Weight-8 span-24 census, tcap=32w+512: 536155 supports, 3.53e7
   placements. Max L vs wt = 7,19,26,31,32,32,32,35. Witness w=38
   mask 17057305, L=35 off-hull. Origin-in-hull dump still L<=31.
   No L>=40. period2_weight8.md.
2. Forbidden periodic-centre blocks: residual SCC nonempty; no 3x3/4x4
   local-rule violation is forced. forbidden_periodic.md.
3. Periods 6–7, w<=6: L6 to 21, L7 to 23, still growing.
   period67_fiber.md.

Prize status: still unsolved. Next: origin-in-hull-only census
(possible L<=31); prize-seed left-edge constraint.

## Cycle M (2026-09-11)

Ideas12. One finite theorem; left-edge restriction dies. No prize claim.

1. Origin-in-hull weight<=8 span<=24: 12.1e6 placements, max L=31,
   n_ge32=0. Maximizer mask 281769. Off-hull L=35 excluded.
   period2_hull.md.
2. Left-edge bit 0 fixed: short cap matches Cycle I; long cap L=24,25,27
   at w=8,9,10. period2_leftbit.md.

Prize status: still unsolved. The hull theorem does not cover later
prize-seed rows (weight Theta(T), span 2T).

## Cycle N (2026-09-11)

Ideas13. In-hull wt=9,10 span<=20: 5.82e6 placements, max L=31,
n_ge32=0. Maximizer mask 806057 (281769 plus a 1 at +2). period2_hull910.md.

Defect recurrence: d_{t+1} is not a Boolean of a width-<=8 defect
window; the only exact local rule uses (c,l,r), the original CA.
defect_recurrence.md.

Prize status: still unsolved.

## Cycle O (2026-09-11)

Ideas14. Unique-left infinitude is L_0 at time 0; vacuum u's period-7
attractor dies at n=152. Algebraic L_0 → 011-bump under S, no rank,
onsets T=33,34 still maxR≤16. period2_germ.md. Fiber note corrected.

Prize status: still unsolved.

## Cycle P (2026-09-11)

Ideas14 items 2–3. Period-2 even neighbor u has no 5 consecutive zeros
(4-state drain of (e,f) while u=0). SFT {11, 00000} forbidden. Does not
kill T=20 R=16. F^2 is not width-1 left-expansive. period2_ugap.md.

Prize status: still unsolved.

## Cycle Q (2026-09-11)

Ideas14 Morse-Hedlund, exact language of u, q=8 drive. MH rigidity
killed (T=20,22 germs have p(n)>n through half). Realizable u is all
of X (43 octuples). q=8: 35/63 finite rights mix sigma. Three T=20
R=16 models survive the gap bound. cycle_q.md.

Prize status: still unsolved.

## Cycle R (2026-09-11)

Kernel d(k) of v_k vs v_0 is not injective
(1,2,2,5,1,2,2,3,1,5,1,2,3,1). Prize-seed fiber_left predicts left
edge 0 for only 92/192 onsets. Exact lemma
D(N)=N_11-N_00+c_{N-1}; local run-length pairing dies (33.5% equal).
Square 2-kernel columns distinct through k=9, not a lemma.
cycle_r.md.

Prize status: still unsolved.

## Cycle S (2026-09-11)

F^2 lag-2 inverse is G_0 = x_{-2} XOR ((x_{-1} XNOR x_0) AND (x_1 OR x_2)).
On phase 01 this is F_2=u (127/127 finite rights). Uniqueness stops at
lag 2; ell=1 zeros x_{-2}; no Condrey horizon. Radius-8 spatial windows
do not determine displacement from 11 to next 00 (44 collisions).
Half-time right-edge width-8 gadget is a full 2-shift of fires.
cycle_s.md.

Prize status: still unsolved.

## Cycle T (2026-09-11)

Isolated-one 10^q has residual radius-6 SCCs for every q=1..17.
e_t=c_t+c_{t+1}-1 restates D(N); packed excess corr -0.005.
Kernel phi_k injective only for k=1,2. Square columns still
distinct through k=9. cycle_t.md.

Prize status: still unsolved.

## Cycle U (2026-09-11)

Every binary word of length <=14 occurs in the first 2^18 centre bits
(T+p >= 16384 if eventually periodic). Twelve length-15 words missing.
Predicted kernel disagreement indices all fail by k=2.
cycle_u.md.

Prize status: still unsolved.

## Cycle V (2026-09-11)

Light-cone lemma: a 1 at ±p is a shifted prize seed, so the
p-step centre depends on both edges and F^p has Kopra width 2p.
Never width 1. Prize u=x(2n,1) has length-8 factors in X (16.7%)
and 32738 factors 11, max gap 46; no never-in-X lemma.
Even-decimation n_* in {1,2,3} through k=15, not a proof.
Longest right-special factor length 33. cycle_v.md.

Prize status: still unsolved.

## Cycle W (2026-09-11)

Coupled 4-zero drain sits in two T=20 R=16 X-models (the third has
only gap 3). Odd-column vacuum disagreements 12-13 on the same words.
No closed form for c_{2^k}. Centre 11 at 2^k for 5/16 values of k,
not uniformly. cycle_w.md.

Prize status: still unsolved.

## Cycle X (2026-09-11)

Vacuum kills every finite-window current for 2c-1 and the pair
current (0=-1 on 00000; prize orbit has a vacuum-5 run of length 5).
All 21 universal families and all 8 orbit-restricted families die,
including 2c with flux. Spatial 7-windows about the origin are a
full 2-shift on t<2^14. ideas21.1 is not a reduction: period-2
phase 01 avoids (c,l)=(1,0). cycle_x.md.

Prize status: still unsolved.

## Cycle Y (2026-09-11)

Spine lemma: v_k=v_{k+1} forces (c_{2^j})_{j>=k} constant. Packed
Rule 30 is Rule 150 XOR AND; Rule 150 centre is identically 1.
Sibling split templates (Rowland period, n=k, 4-point) all fail.
b_k not-eventually-constant remains open. cycle_y.md.

Prize status: still unsolved.

## Cycle Z (2026-09-11)

Half-step lemma: b_k = b_{k-1} XOR I_k with I_k the Green parity of
AND injections on [2^{k-1}, 2^k). Linear part is b_{k-1} via the two
edges. Local I_k formulas die. Eventual constancy of b_k iff I_k
eventually 0, still open. cycle_z.md.

Prize status: still unsolved.

## Cycle AA (2026-09-11)

Central trinomial \(G(m,m)=1\); every \(c_t\land r_t\) on the dyadic
annulus hits \(I_k\). Remainder \(R_k\) is not identically 0 (fails
at \(k=3\)). Leftmost 11 always present, never hits. Near-central
\(G(m,m-1)=v_2(m+1)\bmod 2\). Mersenne locals and small recurrences
die. cycle_aa.md.

Prize status: still unsolved.

## Cycle AB (2026-09-11)

Annulus coboundary: I_k = XOR (ell XOR r XOR (c AND r)) on [T,2T).
R_k is the palindrome-defect parity. d=ell XOR r is not eventually 0.
Spatial vacuums radius 7 do not explain centre 0-runs of length 19.
Infinitely many centred 000s would kill isolated-zero periods
including period 2; unproved. cycle_ab.md.

Prize status: still unsolved.

## Cycle AC (2026-09-11)

00 is 000 or 101; each has four 5-window preimages (32-case check).
Every left-diagonal e_j(t)=x(t,-t+j) is eventually periodic via a
2p-state driven bit. The centre is the onset e_t(t), not the tail
(first fail j=18). Infinitely many 00s still open. cycle_ac.md.

Prize status: still unsolved.

## Cycle AD (2026-09-11)

Freshman Green matches doubling; Fibonacci-binary m have a unique
writing. Reset/integrator dichotomy; white-stripe implication
(agreeing nonzero drivers force e_j=0). Closed forms through e_9
including e_7=0; e_28=0 on period-4 tails. Nested left and 1-run
endings killed as 00 productions (finite incidence; all eight 11***
windows occur). White-stripe onsets are 01 not 00. cycle_ad.md.

Prize status: still unsolved.

## Cycle AE (2026-09-11)

Right-diagonals are pure integrators; only u(*,0)=1 is eventually
constant (no right white stripes). Finite incidence of each k in the
centred 5-window. Green formula for d=ell XOR r (linear parts cancel).
00 after a 1-run ending iff x(-2)=r OR x(2). Nested right killed as a
00 production. cycle_ae.md.

Prize status: still unsolved.

## Cycle AF (2026-09-11)

Two-step Green support G(1,d)=1 for d=0,1,2. Identity
c_{s+2}=1 XOR (ell AND c) XOR (c AND r) XOR (r AND e) XOR (c' AND r')
XOR O_s. At a 1-run ending this is (r AND NOT e) XOR O_s, and O_s
takes both values (local ANDs do not force 00). Annulus 10/00/11
parities are not I_k. cycle_af.md.

Prize status: still unsolved.

## Cycle AG (2026-09-11)

O_s in the two-step identity is a local 5-window Boolean on the prize
orbit (Green matches c'' XOR 1 XOR local ANDs). At 1-run endings
O_s = a XOR e, the distance-2 palindrome defect. Killed as a bulk 00
handle: it restates a = r OR e. cycle_ag.md.

Prize status: still unsolved.

## Cycle AH (2026-09-11)

Odd-spine half-step: c_{2 q 2^k} = c_{q 2^k} XOR Delta XOR J with
Q=(1+x+x^2)^q, edges cancelling, centre from G(q,q)=1. Cycle Z is
q=1 (empty extras). Delta and J are not identically 0 for
q=3,5,7,9 (q=9 Delta dies at k=8) and neither is the spine flip.
Eventual period 2^m r (r odd) forces (b_k) eventually periodic of
period dividing ord_r(2); r=1 forces constancy, so non-vanishing
I_k would kill every power-of-2 period. One-step O^{(1)} is local
and is not I_k. cycle_ah.md.

Prize status: still unsolved.

## Cycle AI (2026-09-11)

Dyadic step from arbitrary time: c_{t+2^k} = c_t XOR x(t,-2^k) XOR
x(t,2^k) XOR J_{t,k}. Cycle Z is t=2^k. J is a Boolean of the
causal 2^{k+1}+1 window. Distance-1 palindrome graph has only
constant-c recurrent SCCs (Cycle AB). Distances 2 and 4 have mixing
SCCs; 00 at lag 2^k is not a production. cycle_ai.md.

Prize status: still unsolved.

## Cycle AJ (2026-09-11)

theta_k = c_{3*2^k} XOR c_{2^k} is the Green remainder on
[2^k, 3*2^k) targeting 3*2^k. Period 2^m forces theta=0. Leftmost
11 always hits (G(2^{k+1}-1, 3*2^k-1)=1 by induction), so
theta = 1 XOR S. S is not identically 0; theta is not I_k, XOR d,
or XOR (c AND r). cycle_aj.md.

Prize status: still unsolved.

## Cycle AK (2026-09-11)

Fermat-odd spines q=2^a+1: phi^{(q)}_k = c_{q 2^k} XOR c_{2^k} is
the Green remainder on [2^k, q 2^k). Period 2^m forces every phi=0.
Leftmost-11 hit parity on that interval is identically 1 (G doubling:
XOR_m G(m, 2^b-1)=1, then the Fermat target), so phi=1 XOR S for
every such q. S is not identically 0. cycle_ak.md.

Prize status: still unsolved.

## Cycle AL (2026-09-11)

All-q identity: c_{q 2^k} = c_{2^k} XOR J on [2^k, q 2^k). Freshman
edges cancel because G(q-1,q)=G(q-1,q-2)=v_2(q) mod 2. Leftmost-11
hit parity is 1 XOR popcount(q), independent of k. Fermat-odd is the
even-weight case of that formula, not a special production. q=7 has
P=0 (p=1 odd for every odd q is killed). Odd q: chained AI extras
stay outside. Period 2^m forces every integer phi^{(q)}=0. TM has
Fermat phi ≡ 1 (Cycle AK's TM parenthetical was wrong). cycle_al.md.

Unshifted GF(2) span of 13 spines does not contain the constant 1 on
k<=15. The 7-term sum phi^{2,6,7,9,10,11,17} vanishes on k=2..15 and
dies at k=16 (prefix accident). Extra hits for q=3 are bulk, not local S.

Prize status: still unsolved.

## Cycle AM (2026-09-11)

Packed bit 4 contributes 1 to every I_k (k>=3): unique Green hit at
the first odd time of the annulus, G(m,2m)=1. Packed bit 6 cancels it
for k>=4. e_8(t)=1 iff t%4 in {0,1} (t>=8); e_10(t)=1 iff t%4 in
{0,3} (t>=10). Nested through p=9 is 1, so I_k = 1 XOR bulk_{p>=10}
for k>=5. Bit 10 cancels again. cycle_am.md.

Prize status: still unsolved.

## Cycle AN (2026-09-11)

W generating function x(1+x) sum_{m<n} r^m = 1+r^n over GF(2).
W(2^a, D)=1 iff D in [2^a-1, 2^{a+1}-2]. Mersenne G(2^a-1,d) is
f(d) XOR f(d-2^a) XOR f(d-2^{a+1}) with f=1 iff n>=0 and n not 2
mod 3. Fermat G(2^a+1,d) is 3-sparse. W(3*2^a, D) is two intervals.
I_k splits as left packed bits [2, T+1] XOR right p>=T+2. I_left=0
on 7<=k<=12 (prefix, not a theorem). Time-T slice equals the
Mersenne filter of ANDs at t=T and is not I_k. cycle_an.md.

Prize status: still unsolved.

## Cycle AO (2026-09-11)

G(m, 3*2^k-1)=1 iff m ≡ 2^{k+1}-1 or 3*2^k-1 (mod 2^{k+2}). Unique
leftmost-11 Green hit for theta_k at t=2^k. N(q) independent of k,
parity P(q); N(5)=1 at t=2^{k+1}. Two-point family XOR is not a
formula for theta. cycle_ao.md.

Prize status: still unsolved.

## Cycle AP (2026-09-11)

G(m, 2^a-1)=1 iff 2^a | (m+1). G(m, 5*2^k-1) is four residues mod
2^{k+3}. Four unique-Green bits on the 3-fold annulus for k>=3:
p=1 (always fires), p=2^{k-1}+1, p=2^k+1, p=2^{k+1}+1. The extra
three do not always fire. Exactly-four is a prefix k=3..8.
cycle_ap.md.

Prize status: still unsolved.

## Cycle AQ (2026-09-11)

G(m, 2^a) = bit_a(m) XOR (L mod 2), L the 1-run from bit a-1 down.
Period 2^{a+1}, complementary halves. Unique double-Green bit on
the 3-fold annulus is p=3*2^{k-1}+1 at t=3U/2 and 2U; firing XOR
takes both values. Five triples on k=4..8 (prefix). cycle_aq.md.

Prize status: still unsolved.

## Cycle AR (2026-09-11)

G(m, q*2^j-1)=1 iff 2^j | (m+1) and G((m+1)/2^j-1, q-1)=1.
Fermat-odd q recovers AO (q=3) and AP (q=5). Five triples and four
quadruples on the 3-fold annulus have closed times from a k-independent
n-window. None always XOR to 1. Bit B xor = k mod 2 dies at k=9.
Exactly-five / exactly-four / bit D silent are prefixes. cycle_ar.md.

Prize status: still unsolved.

## Cycle AS (2026-09-11)

Half-window G(n, 2^a-2)=1 iff n=2^{a-1}-1; G(n, 2^a-4)=1 iff
n=2^{a-1}-2 (a>=3). Unique 2^j+1 family at t=T and 3*2^j+1 family
at t=T+2^j (j<=k-3) for I_k. Two doubles p=5*2^{k-3}+1 and
p=3*2^{k-2}+1. Bit 9 always fires at T. Unique XOR is not I_k.
Exactly 2k-2 unique / two doubles are prefixes. cycle_as.md.

Prize status: still unsolved.

## Cycle AT (2026-09-11)

G(n, 2^a-2^b)=1 on n<2^{a-1} iff 2^{a-1}-1-n in Jacobsthal S_b.
Mersenne-odd packed bits p=(2^c-1)2^j+1 hit I_k at t=T+s*2^j,
s in S_c. Recovers AS at c=1,2. 7-family is triples, not identically 1.
Mersenne-odd XOR is not I_k. cycle_at.md.

Prize status: still unsolved.

## Cycle AU (2026-09-11)

G(n, 2^a-2^c-1)=1 iff n=2^{a-1}-1 on the half-window. Derived
2^a-6,7,10,12. e_11=1 iff t≡2 mod 4; e_12=1 iff t not≡0 mod 4.
Bits 10,11,12 contribute 1,0,1, so I_k=1 XOR B^{>=13} for k>=5.
Nested depth 12 is not a closed form. cycle_au.md.

Prize status: still unsolved.

## Cycle AV (2026-09-11)

Unique half-window G-supports are exactly the AS 2-family and
3-family. Unique-Green bits for I_k are exactly those 2k-2 packed
indices (AS prefix upgraded). e_13..e_17 period 4; bits 13 and 17
contribute 0. Unique 3-family p>=13 is not identically 0 (k=15).
Double p=3T/2+1 XOR 0 dies at k=12. Nested left is not a formula
for I_k. cycle_av.md.

Prize status: still unsolved.

## Cycle AW (2026-09-11)

No even half-window doubles for a>=4. Double D are exactly
2^{a-2}-1 and 3*2^{a-3}-1, so I_k has exactly two double-Green
bits p=3T/2+1 and p=5T/8+1 (AS prefix upgraded). All e_j period 4
is false (e_29). Bit 33 fires at T on 7<=k<=12 (prefix).
cycle_aw.md.

Prize status: still unsolved.

## Cycle AX (2026-09-11)

Even triples are 2^a-{6,8,10,14} for a>=5; all triples are the
5,7,9,13 families p=q*2^j+1. G(n, 2^a-14) has s in {0,5,6}.
Bits 14 and 15 contribute 0. Triple XOR is not I_k. Exactly five
quads is a prefix. cycle_ax.md.

Prize status: still unsolved.

## Cycle AY (2026-09-11)

Bit 16 is Jacobsthal S_4 and contributes 0. e_18=1 iff t≡1,2 mod 4
(t>=20); e_18 AND e_17 is identically 0, so bit 18 never fires.
I_k=1 XOR B^{>=19} for k>=5. Nested depth 18 is not a closed form.
cycle_ay.md.

Prize status: still unsolved.

## Cycle AZ (2026-09-11)

No even quads for a>=6; exactly five quads, the odd-lift orbit of
{18,19,23,27,29}. e_19 period 4; bit 19 (9-family j=1) contributes
1, so I_k=B^{>=20} for k>=6. Nested depth 19 is not a closed form.
Quad XOR is not I_k. cycle_az.md.

Prize status: still unsolved.

## Cycle BA (2026-09-11)

Even pentuples are 2^a-{12,16,18,20,26,28,34,50} for a>=7; all
pentuples are the 11,15,17,19,25,27,33,49 families p=r*2^j+1.
e_20..e_27 period 4; e_30=1 for t>=33; bits 20, 24, 25 never fire.
Pentuple XOR is not I_k. Nested left is still not a closed form.
cycle_ba.md.

Prize status: still unsolved.

## Cycle BB (2026-09-11)

No even sextuples for a>=8; exactly five sextuples, the odd-lift
orbit of {66,67,71,77,85}. Even septuples are ten seeds for a>=9,
the 21,29,35,51,65,67,97,99,129,193 families. Bit 22 contributes 1.
Sextuple XOR and septuple XOR are not I_k. Nested left is still not
a closed form. cycle_bb.md.

Prize status: still unsolved.

## Cycle BC (2026-09-11)

No even octuples for a>=10; exactly eleven octuples, the odd-lift
orbit of a=9's eleven packed bits. Even nonuples are ten seeds for
a>=11. Octuple XOR and nonuple XOR are not I_k. Nested left is still
not a closed form. cycle_bc.md.

Prize status: still unsolved.

## Cycle BD (2026-09-11)

Period-8 tails e_29, e_31, e_32, e_33 from e_27 period 4, e_28=0,
e_30=1. Bit 33 AND fires iff t≡0 mod 8, so it contributes 1 for every
k>=7 (AW prefix upgraded). Bit 29 never fires. Nested left is still
not a closed form. cycle_bd.md.

Prize status: still unsolved.

## Cycle BE (2026-09-11)

Fermat covering phi^(3), phi^(5), phi^(9) has a 1 for every 2<=k<=15
(AK prefix k<=10 extended). No single Fermat q<=17 is identically 1.
Still a prefix, not a theorem. A proof for all k>=2 would kill every
eventual period 2^m. cycle_be.md.

Prize status: still unsolved.

## Cycle BF (2026-09-11)

Fermat p=1 times are t=(2^a-s)U with G(s,2^a)=1; covering triple
q=3,5,9 at U / 2U / {U,3U,4U}. Mersenne centre-right unique bits
p=U+1 and p=(2^{a-1}+1)U+1 on every Fermat-odd annulus. Extra unique
bits are not identically-1 productions. Doubling
phi^(q)_{k+1}=phi^(2q)_k XOR I_{k+1}. Covering still a prefix.
cycle_bf.md.

Prize status: still unsolved.

## Cycle BG (2026-09-11)

Second hit for G(.,2m) in (m, 3m/2+1] by mod-4 / 2-adic cases; unique even windows have
3d>=4N-2, which 5-fold and 9-fold annuli contradict for M>=1.
Exactly three unique-Green bits on the 5-fold annulus and two on the
9-fold, for every k>=3 (BF prefix upgraded). Extra unique bits are
not identically-1 productions. Covering still a prefix.
cycle_bg.md.

Prize status: still unsolved.

## Cycle BH (2026-09-11)

G(n,n)=1; third even-target hit n3<=2m for m>=3; cone dominates d
for M>=1; Cycle AW kills N=W doubles. Exactly two double-Green bits
on the 5-fold annulus (p=2U+1, 4U+1) and three on the 9-fold
(p=3U+1, 6U+1, 7U+1), for every k>=3. Doubles are not identically-1
productions. Covering still a prefix.
cycle_bh.md.

Prize status: still unsolved.

## Cycle BI (2026-09-11)

H(m)=3 only for m in {3,6}; complementary hit at 2m-2 or 2m-1 for
m>=8. Truncated windows have C_le>=4 except two 5-fold M=1 slots;
Cycle AX leaves only 5-fold M=2, r=19. Exactly four triple-Green
bits on the 5-fold annulus and three on the 9-fold, for every k>=3.
Triples are not identically-1 productions. Covering still a prefix.
cycle_bi.md.

Prize status: still unsolved.

## Cycle BJ (2026-09-11)

H(m)=4 only for m in {4,7,14}; n3 before complementary except m=14.
Cycle AZ kills even N=W quads for a>=6. Exactly two quad-Green bits
on each of the 5-fold and 9-fold annuli, for every k>=3. Quads are
not identically-1 productions. Covering still a prefix.
cycle_bj.md.

Prize status: still unsolved.

## Cycle BK (2026-09-11)

C_le=5 at nine 5-fold (M,r) slots and seven 9-fold slots; BA even
pentuples leave only r=17,37,39,79 on full windows. Exactly nine
pentuple-Green bits on the 5-fold annulus for k>=4 (eight at k=3)
and seven on the 9-fold. Pentuples are not identically-1 productions.
Covering still a prefix.
cycle_bk.md.

Prize status: still unsolved.

## Cycle BL (2026-09-11)

C_le unique through pentuple on the 3-fold annulus upgrades AP/AQ/AR
prefixes: exactly four unique-Green bits, one double, five triples,
and four quads for every k>=3, and exactly eight pentuples for every
k>=5. Classified bits are not identically-1; unique XOR triple XOR
pentuple is not theta_k. Covering still a prefix.
cycle_bl.md.

Prize status: still unsolved.

## Cycle BM (2026-09-11)

chi(T)=G(2T-1, 3T-1) depends only on the odd part of T and equals 1
iff that part is 1, or 3 (mod 4) with no adjacent 0-bits. Time T is
a bit-1 hit for every T=2^k and T=3*2^k; on [3U,9U) a second hit at
4U cancels the net parity, so phi9 xor theta is not a forced 1.
{theta, phi9} fails at k=3. Covering still a prefix.
cycle_bm.md.

Prize status: still unsolved.

## Cycle BN (2026-09-11)

P(q,T) = XOR_{m<(q-1)T} G(m, qT-1) is net packed-bit-1 parity on
[T,qT). Even doubling P(q,2S)=P(q,S) recovers Cycle AL for every q.
P(3,4p+1)=P(3,p) and P(3,4p+3)=P(3, p OR 1), so P(3,T) reduces to
{1,3}. Families P(3,2^k)=1 and P(3,3*2^k)=0 are net parities, not
1-productions: S_other still cancels on theta. Covering still a prefix.
cycle_bn.md.

Prize status: still unsolved.

## Cycle BO (2026-09-11)

Covering fails at k+1 iff phi6_k = phi10_k = phi18_k = I_{k+1}.
That dangerous set is empty for 2<=k<=12. phi6 is not identically 1
for k>=5 (zero at k=13), and {phi5, phi6} is not a covering.
Covering still a prefix.
cycle_bo.md.

Prize status: still unsolved.

## Cycle BP (2026-09-11)

The 9-fold unique-Green bit p=5U+1 fires at k=13 and k=14, so
gamma_k = c_{5U} and r_{5U} is not identically 0. The vanishing
through k=12 was a prefix. Covering still a prefix.
cycle_bp.md.

Prize status: still unsolved.

## Cycle BQ (2026-09-11)

Packed bit 1 Green-hits target T only for t<=(T-1)/2. The covering
blocks [6U,10U)->10U and [10U,18U)->18U lie past that cone, so they
have zero bit-1 hits for every k. Covering fails iff S_A=1 and
S_B=S_C=0. Covering still a prefix.
cycle_bq.md.

Prize status: still unsolved.

## Cycle BR (2026-09-11)

The Green cone t<=(T+p-2)/2 makes every packed bit p<=2U+1 silent
on covering blocks B and C. Packed bit p=2U+2 is unique-Green on B
at t=6U and on C at t=10U (both G(m,2m)=1). That AND takes both
firing values. Covering still a prefix.
cycle_br.md.

Prize status: still unsolved.

## Cycle BS (2026-09-11)

The four leftmost admissible bits p=2U+2..2U+5 are unique-Green on
B (times 6U, 6U, 6U+1, 6U) and on C (times 10U, 10U, 10U+1, 10U).
Their firing XOR takes both values. Covering still a prefix.
cycle_bs.md.

Prize status: still unsolved.

## Cycle BT (2026-09-11)

For M=2^a, freshman gives c_{t+M} xor c_t = x(t,M) xor x(t,-M) xor J.
Extras vanish on dyadic block A (4U>2U) and survive on B (4U<6U)
and C (8U<10U). Covering fails iff J_A=0 and J_B=d_B and J_C=d_C.
The defects d_B, d_C take both values, so the centre coboundaries
are not the raw Green AND-parities. Covering still a prefix.
cycle_bt.md.

Prize status: still unsolved.

## Cycle BU (2026-09-11)

S(2^a,d)=XOR_{m<2^a} G(m,d) vanishes for d<2^{a-1}. Palindrome
defects chain when 2M>t, so d_C = d_B xor J_B->2U xor J_B->18U,
with those three Green parities on disjoint packed-bit ranges.
J_B->2U=0 through k=12 is a prefix; J_B->18U takes both values.
Covering still a prefix.
cycle_bu.md.

Prize status: still unsolved.

## Cycle BV (2026-09-11)

The left 2^k+1 packed bits evolve autonomously. Packed bit 2 is 0
for t>=2 and packed bit 4 is 1 for t>=2. Q_k(r)=1 xor alpha(r) xor
alpha(r+1). One equality L_k(2)=L_k(3) freezes every later sample
and forces J_B->2U=0. That equality holds through k=12 (prefix).
Covering still a prefix.
cycle_bv.md.

Prize status: still unsolved.

## Cycle BW (2026-09-11)

Green shift G(m+2^a,d)=G(m,d) for m,d<2^a. The left word has period
H=2^{k-1} for t>=2 when k=1,2, and a single seed F^H(L(2W))=L(2W)
extends that period to all later times (stronger than BV freeze).
Low bits induct from P_{k-1}. Unique attracting 4-cycle at k=3,4; unique 8-cycle lift at k=5.
The seed is a prefix through k=12. Period H from time W is killed
at k=5. Covering still a prefix.
cycle_bw.md.

Prize status: still unsolved.

## Cycle BX (2026-09-11)

A 1-reset in the driver forces a unique period-pi continuation of
the next packed bit; wrap-around is automatic. An identically-0
driver toggles, doubling the period iff the driver XOR is 1.
Unblocked lifts match the prize through k=12. Period 8 for all
k>=5 is false (k=9 has period 16); frozen zeros 2,7,28 grow.
Covering still a prefix.
cycle_bx.md.

Prize status: still unsolved.

## Cycle BY (2026-09-11)

Ident-0 at p with a live left neighbour forces ident-1 at p+2.
The left-word period is a 2-power and a nested multiple, so
pi_{k+1}=pi_k * 2^r with r the odd-toggle count. If r<=1 at every
scale then the BW seed holds for all k. Ratios stay in {1,2}
through k=16 (prefix). Two ident-0 bits can appear without
doubling. Covering still a prefix.
cycle_by.md.

Prize status: still unsolved.

## Cycle BZ (2026-09-11)

ident-0 at p iff the two previous packed-bit strings are equal.
If a=b is not identically 0, the unique continuation is 0. Consecutive
ident-0 would cascade left to bit 0, which is 1. After an odd high
toggle the Hamming distance stays positive on the k=4 and k=8 lifts
(prefix). Even weight is not invariant. Covering still a prefix.
cycle_bz.md.

Prize status: still unsolved.

## Cycle CA (2026-09-11)

Unique continuation equals B iff A is the cyclic derivative of B.
A later ident-0 is exactly a later A=DB pair. After an odd doubling
the scar pairs (0,T), (T,1), (1,~T) are not derivatives (pre-toggle
period a 2-power at least 2). The rest of the k=4 and k=8 high
halves also avoid A=DB (prefix). No linear functional of B xor U
is constant after the scar. Covering still a prefix.
cycle_ca.md.

Prize status: still unsolved.

## Cycle CB (2026-09-11)

Half-xor v(s)_t = s_t xor s_{t+pi} intertwines with the cyclic
derivative: v(DB)=D(v(B)). Odd 2-copy strings are never derivatives
of 2-copy bits. Unique continuation does not preserve 2-copy type,
and the half-xor obstruction is not absorbing on arbitrary drives.
After the scar window on the k=8 odd lift it fires on every remaining
pair (prefix). Covering still a prefix.
cycle_cb.md.

Prize status: still unsolved.

## Cycle CC (2026-09-11)

A=DB iff the next-right packed bit is the spatial AND of the pair
(3-bit identity). Later ident-0 is exactly a later AND-triple.
The pattern 011 is not a universal witness. No AND-triple after
the scar on the k=4 and k=8 odd lifts (prefix). Covering still a
prefix.
cycle_cc.md.

Prize status: still unsolved.

## Cycle CD (2026-09-11)

If a packed triple is AND-closed, the update collapses to a'=d xor a
and b'=a xor b, and the next triple stays AND-closed iff a forced
fifth bit. Identically AND forces d=Da. Forbidden triples cannot
enter S when (e,d)=(0,1). S is not absorbing. No AND-triple after
the scar on the k=4 and k=8 odd lifts (prefix). Covering still a
prefix.
cycle_cd.md.

Prize status: still unsolved.

## Cycle CE (2026-09-11)

d=Da iff c implies a, from the packed update of a. Identically AND
needs c implies a and c implies b; the latter forbids consecutive
11s in c. On the k=4 and k=8 odd lifts both implications hold
together only at the ident-0/ident-1 scar triple, where 011 kills
AND (prefix). Covering still a prefix.
cycle_ce.md.

Prize status: still unsolved.

## Cycle CF (2026-09-11)

Ident-1 at p>=2 iff ident-0 at p-2. Consecutive ident-1 only at
bits 0 and 1. Both implications with c not 0, and identically AND
with c not 0, exist on consistent length-4 windows (killed as
orbit-free). After the scar both hold together only at c=0 (prefix).
Covering still a prefix.
cycle_cf.md.

Prize status: still unsolved.
