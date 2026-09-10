Creative round 3 (your ideas6) is over. All five of those attacks were run and HIT THEIR KILL CRITERIA. The human still wants more creativity. Propose a NEW set. Do NOT implement. Do NOT edit files. Do NOT say stop as the first line. Do NOT retread anything below.

Workspace: /home/cochonhome/Documents/random-shit/wolfram
Start with REPORT.md and research/LOG.md if you need orientation. Official site still open: https://rule30prize.org/

## What just died in ideas6 (do not repeat)

1. Communication rank of f_h: GF(2) rank of split (h-1,h+2) is 79>72 at h=9 and 104>80 at h=10. Central split stays just under 8h; features are high-degree truth tables / original cone. research/communication_rank.md
2. Hashlife: central reuse dominates (96–99.8% of hits), W(2^14)/W(2^13)=3.61, W/n² falling to 0.074, no closed recurrence, n=2^15 disk-slept after 40 min. Not O(n). research/hashlife_reuse.md
3. Nonuniform S-adic tilings: all 4 binary digrams in the first 1024 bits; 16 paired digrams; no 4-letter 2-morphism parse to a seed of length ≤4. research/substitution_tiling.md
4. Signed ×7 corrections: identity Z_{t+1}=7Z_t-2Q_t holds exactly; S(n)/n²≈0.19>0.05 at n=256 and 512. Mean weight ~0.19n. research/signed_carry.md
5. Invasion fronts for 001/0111: finite pulses exist; repeated periodic wake is not travelling; B=min(ℓ,R)+φ(8-window) decreases on a left-moving 1 outside a vacuum window. research/invasion_front.md

## Still dead from earlier (do not repeat)

Strips/onset SAT; F_T ideal certificates; q=8 σ transducer and H-invariants; (d,h) phase masks; ancestry DFAs; block energy; Mahler DAG; A_p⇒B_p rigidity; automaton sections of A^n; renewal E(w)≤2|w|+C; dual-particle pairing; Cartier on U; relative R_m; period-2 vacuum fold; isolated-zero family except q=8; Stern–Brocot; matchgates; adaptive certificates; Lax pairs; dilation C_{p,q}.

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

- 2-adic valuation / carry sequence of the packed integer row (this is not the ×7 signed-digit identity already killed)
- A matrix product over a finite ring whose *trace* (or a fixed matrix entry) equals c_t, then joint spectral radius / Lyapunov — not a Lax pair, not communication rank of f_h
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
