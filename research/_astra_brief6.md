Creative round 2 (your ideas5) is over. All five of those attacks were run and HIT THEIR KILL CRITERIA. The human still wants more creativity. Propose a NEW set. Do NOT implement. Do NOT edit files. Do NOT say stop as the first line. Do NOT retread anything below.

Workspace: /home/cochonhome/Documents/random-shit/wolfram
Start with REPORT.md and research/LOG.md if you need orientation. Official site still open: https://rule30prize.org/

## What just died in ideas5 (do not repeat)

1. Stern–Brocot q_t: bidegree (2,2) on rows 0–63 has rank 18, kernel 0. Empty family. research/stern_brocot.md
2. Matchgates: no compatible GL(2) holographic transform of the complete tensor family (T, EQ4, crossings, two-step block) in either prescribed drawing. research/matchgate.md
3. Adaptive certificates: C(128)≥6438 and C(256)≥27139, both >0.1 n². Executable left-first evaluator is ~0.4 n². research/adaptive_certificate.md
4. Lax pairs: 36 constant GL(2,F2) solutions, M(0,0,0)=I. Six config-blind; rest have at most a 1-bit monodromy trace. Affine L0+λ L1 screen empty. Restricted GL(3) catalog: 252 solutions, same obstruction. Isolated traces do not reconstruct the seed. research/lax_pair.md
5. Dilation C_{p,q}: measured through primes 13 and N=2^14. Symbolic (F^2,F^3) pass is two independently growing cones (speeds 4 and 6). Bounded edges do not determine s_{2n}s_{3n}. Unique-key windows at halfwidth ≥16 are a sample artifact. No estimate stronger than |C|≤N. research/dilation_disjointness.md

## Still dead from earlier (do not repeat)

Strips/onset SAT; F_T ideal certificates; q=8 σ transducer and H-invariants; (d,h) phase masks; ancestry DFAs; block energy; Mahler DAG; A_p⇒B_p rigidity (equivalent to ¬A_p given Jen/Kopra); automaton sections of A^n; renewal E(w)≤2|w|+C; dual-particle pairing; Cartier on U; relative R_m; period-2 vacuum fold; isolated-zero family except q=8.

## Already proved (do not re-prove)

Infinitely many 0s and 1s in c. Isolated-zero 01^q excluded for q=7 and all q≥9 (q=8 survives). Period-2: Fibonacci u, F_4=u0 u1, vacuum u ⇒ L_0 impossible; every onset T=1..28 dies at finite extra R, no uniform-in-T bound. Periods 3–7 and q=8 still have residual strip SCCs.

Problems 2 and 3 unsolved. Prize unsolved. No submission, no contact.

## Constraints

- Do not overwrite research/strip_graph.py, strip_extend.py, or experiment.py.
- Finite T tables are not a prize proof.
- Surviving strip SCCs are an overapproximation. Empty residual SCC IS a seed-applicable exclusion.
- Prefer a T-independent lemma, a seed-specific constraint the strips omit, or a genuine attack on problems 2/3.
- A first experiment must be concrete, bounded, and have a kill criterion. Speculative mechanism is OK.

## Places still unused (prompts, not a mandatory list)

- 2-adic valuation / carry sequence of the packed integer row (this is not Stern–Brocot)
- A matrix product over a finite ring whose *trace* (or a fixed matrix entry) equals c_t, then joint spectral radius / Lyapunov — not a Lax pair
- Exact sampling of c at times n and 2n+1 as a Cobham morphism that you can break
- A topological invariant of the spacetime as a 2D subshift (Nivat, or a forbidden pattern that a periodic-center slice would force)
- Problem 3 as streaming: after seeing row t, can an online algorithm produce c_{t+1} with o(t) bit operations on the packed word?
- Coupling from the past / coalescence of two seeds that agree on [-T,T]
- Something from permutive-CA literature that is not Jen/Kopra restated
- An exact closed form for a transformed sequence (first difference of c, or c_t XOR (t mod 2)) that is easier than c
- Any other language you have not used

## Required output

5 NEW attacks in a different language from all of the above. Rank them. Name 3 to run first. Kill criteria mandatory.

If you genuinely believe no remaining attack exists that is not another finite table, not equivalent to a prize problem, and not a method whose obstruction already fired, you MAY end with a stop recommendation AFTER the five proposals — but the five proposals are still required.
