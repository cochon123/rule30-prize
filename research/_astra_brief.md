You are advising a Rule 30 prize research attempt. READ the workspace, then propose the next attacks. Do NOT implement them. Do NOT edit files. Do NOT claim a prize result. Do NOT contact anyone.

Workspace: /home/cochonhome/Documents/random-shit/wolfram
Start with REPORT.md and research/LOG.md, then the notes they cite.

## The prize (still open: https://rule30prize.org/)

Rule 30 from a single 1 at the origin:

  x_{t+1,j} = x_{t,j-1} XOR (x_{t,j} OR x_{t,j+1})
  x_{0,j} = 1 iff j=0
  c_t = x_{t,0}

Three problems:
1. Center not eventually periodic.
2. Density of 1s → 1/2.
3. Computing c_n requires not O(n) effort (detailed announcement: no exact finite machine with limsup T(n)/n < ∞).

Jen/Kopra: width-2 traces of nonzero finite seeds are never eventually periodic (Kopra 2023, Cor. 3.7). Width 1 is the gap.

## Already proved (checked)

- Infinitely many 0s and 1s in c (constant tails + Jen). Period 1 is dead.
- Isolated-zero family 01^q: q=7 and all q≥9 excluded by radius-6 strip + Jen (uniform gadget for q≥17). Exception q=8 (period 9).
- Period 2: even right neighbor u has no consecutive 1s; infinitely many isolated 1s else Jen; left reconstruction independent of odd right neighbor v; F_4 = u0 u1 unreduced, so x(2n,-4)=0 on legal u.
- Eventually-zero u ⇒ F_k eventually equals k mod 2 (16-state fold FSM absorbs in ≤9 columns) ⇒ L_0 impossible. Same exclusion as Jen on u, read on the left edge.
- Sound onset scan: every T=1..28 has finite extra R making F_T=1 and R further zeros unsat. Worst T=20, R=16. NO uniform-in-T bound.
- Periods 3–7: injection, double-1, vacuum triangle, window 10010. L_0 chains T≤8 die by s≤4. Residual strip SCCs remain.
- Period 9 / q=8: mixed residual SCC; constant σ is Jen-excluded; mixing of last-1 prefixes 110001101 and 000111100 is the obstruction.

Problems 2 and 3 barely touched. Prize unsolved.

## Constraints on ideas

- Do not overwrite research/strip_graph.py or strip_extend.py.
- Surviving strip SCCs are an overapproximation (free outer bits). Empty residual SCC IS a seed-applicable exclusion. Nonempty is not a construction.
- Finite T tables are not a prize proof.
- Prefer a T-independent lemma, a seed-specific finite-support constraint the strips omit, or a genuine attack on problems 2/3.

## Required output

After reading, write:

1. A short critique of the current gap (what would actually finish problem 1, vs busywork).
2. 5–8 concrete next attacks, ranked. For each:
   - Target (period 2 / q=8 / periods 3–7 / density / complexity)
   - Why it could work given what is already proved
   - First experiment or lemma statement, specific enough to assign to a subagent
   - Likely obstruction
3. Which 2–3 to run first in parallel.

Be technically specific (polynomials, radii, automata, identities). No generic “try more SAT”.
