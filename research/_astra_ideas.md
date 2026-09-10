I read [REPORT.md](/home/cochonhome/Documents/random-shit/wolfram/REPORT.md), [research/LOG.md](/home/cochonhome/Documents/random-shit/wolfram/research/LOG.md), the cited notes, and the core reconstruction, strip, and support code. I treated the latest checked notes as superseding earlier exploratory claims. Everything below is a proposed attack; I made no changes or ran experiments.

The gap is **uniform mathematical control of the missing boundary information**. For period 2, the free information is an infinite Fibonacci sequence \(u\); for \(q=8\), it is the aperiodic switching sequence \(\sigma\). Neither another fixed-depth identity nor larger surviving SCCs resolves that.

Two qualifications should guide the work:

- A constant bound \(R_0\) independent of onset \(T\) is stronger than necessary. A theorem giving **some finite \(R(T)\) for every \(T\)** would finish the period-2 left-edge exclusion. Compactness explains why each impossible fixed-\(T\) infinite system has a finite certificate; the missing ingredient is a proof covering all \(T\).
- Even excluding periods 2–7 and \(q=8\) would leave arbitrary periods. Finishing problem 1 needs an argument covering every primitive word, a seed-specific implication from one periodic column to a periodic adjacent pair, or unbounded linear complexity. The adjacent-pair implication would connect directly to [Kopra’s Corollary 3.7](https://www.utupub.fi/server/api/core/bitstreams/eeb04919-9fa7-443b-998f-032fab664a41/content).

I would rank the next attacks as follows.

1. **Period 2: turn “no last 1” into an inductive polynomial certificate.**

   **Why it could work.** [period2_vacuum.md](/home/cochonhome/Documents/random-shit/wolfram/research/period2_vacuum.md) already provides an exact fold operation, a finite vacuum-tail machine, and a sharp dependency bound. These are ingredients for symbolic induction, whereas the onset table alone is not.

   Work in
   \[
   \mathcal B=\mathbb F_2[u_0,u_1,\ldots]/
   \langle u_i^2+u_i,\ u_i u_{i+1}\rangle,
   \]
   with \(S(u_i)=u_{i+1}\) and
   \[
   F_k=G_{k-1}+(F_{k-1}\lor F_{k-2}),\qquad
   G_k=SF_{k-1}+(G_{k-1}\lor G_{k-2}).
   \]

   **First assignment.** Seek a finite family of certificate templates establishing, for every \(T\),
   \[
   F_T\in\langle F_{T+1},\ldots,F_{T+R(T)}\rangle_{\mathcal B}.
   \]
   Explicitly, find identities
   \[
   F_T=\sum_{j=1}^{R(T)}A_{T,j}F_{T+j}
   \]
   whose construction closes under spatial advancement and the shift \(S\). Such an identity directly contradicts \(F_T=1\) followed by zeros. Start by extracting the *structure* of the existing certificates—especially the \(T=20\) survivor—and test closure under \(T\mapsto T+2\). Allow \(R(T)\) to grow.

   The equivalent automata assignment is to classify residual fold constraints after reading a legal \(u\)-prefix, and prove a finite quotient or a well-founded rank for those residuals.

   **Likely obstruction.** The 16-state machine closes only when its input suffix is already vacuum. Arbitrary infinitely supported \(u\) may require unbounded residual memory or certificate degree. A finite quotient must be proved compatible with all continuations, not inferred from matching short prefixes.

2. **\(q=8\): prove finite left support forces eventual periodicity of \(\sigma\).**

   **Why it could work.** [period9_q8.md](/home/cochonhome/Documents/random-shit/wolfram/research/period9_q8.md) reduces the obstruction to one bit per period and supplies a 20-state phase-0 return graph. Moreover, **every eventually periodic \(\sigma\)** is Jen-excluded, including periodic mixing such as \(0101\ldots\). Forcing constant \(\sigma\) is unnecessarily restrictive.

   **First assignment.** Use the radius-6 return graph as an automaton recognizing an overapproximation of legal \(\sigma\)-streams. Define
   \[
   C_{k,a}(n)=x(9n+a,-k),\qquad 0\le a<9.
   \]
   Initialize \(C_0=011111111\) and \(C_1=\sigma_n00000001\); use the checked \(C_2\) table. Reconstruct by
   \[
   C_{k+1,a}(n)=C_{k,a+1}(n)
      +(C_{k,a}(n)\lor C_{k-1,a}(n)),
   \]
   interpreting phase \(9\) as phase \(0\) at \(n+1\).

   Target the lemma:
   \[
   C_{T,0}(0)=1,\quad C_{k,0}(0)=0\ (k>T)
   \quad\Longrightarrow\quad
   \sigma\text{ is eventually periodic}.
   \]

   Construct a quotient of the reconstruction constraints combined with the 20-state automaton. A sufficient certificate would make every surviving recurrent component force a periodic **label sequence**, even if internal states remain nondeterministic.

   **Likely obstruction.** Left-only extension through depth 26 already shows that a freely supplied outer bit preserves mixing. The new quotient must encode the infinite zero tail or a valid rank measuring its consequences. Zero entropy, few states, or recurrent mixing alone does not imply eventual periodicity.

3. **Periods 3–7: propagate phase constraints at a speed that can meet the moving edge.**

   **Why it could work.** The identities in [period_p_left_edge.md](/home/cochonhome/Documents/random-shit/wolfram/research/period_p_left_edge.md) constrain selected phases, but remain at fixed depths. The useful question is whether those constraints reproduce farther left with sufficiently little additional temporal delay.

   **First assignment.** Build an implication system whose states describe phase masks and Boolean relations on two adjacent temporal columns: forced bits, phase-restricted periodicity, and relations among injected zero-phase bits. Begin with \(001\) and \(0111\), using their depth-4 zeros.

   Derive exact implications over spatial displacements \(d=4,8\), initially using windows of roughly \(2p+8\) time steps. Include radius-3 right-side consistency, especially vacuum implications, rather than only the one-step Markov relaxation.

   Seek a repeatable implication cycle with total spatial displacement \(d\) and additional onset delay \(h<d\). Its forced-zero phase masks must intersect
   \[
   k=T+s,\qquad a\equiv s\pmod p,
   \]
   the actual moving left edge, for every relevant onset residue. That would turn a fixed-depth zero into a contradiction at arbitrarily large \(T\).

   **Likely obstruction.** The masks may lose information on every iteration, or require \(h\ge d\), allowing the edge to escape. A depth-4 identity by itself supplies no repeatable implication. This attack should stop if it merely regenerates the existing finite identities without a closed propagation rule.

4. **Period 2 / \(q=8\): add exact finite ancestry through the inverse row transducer.**

   **Why it could work.** The strips omit not only support boundaries but also membership in the orbit of the single seed. The integer representation gives a particularly concrete ancestry test.

   For
   \[
   z=f(y)=y\mathbin{\mathrm{XOR}}
        ((y\ll1)\mathbin{\mathrm{OR}}(y\ll2)),
   \]
   the unique 2-adic predecessor satisfies
   \[
   y_k=z_k+(y_{k-1}\lor y_{k-2}),\qquad y_{-1}=y_{-2}=0.
   \]
   This is a four-state transducer. Once the finite input \(z\) ends, its predecessor tail is finite precisely when the transducer reaches state \(00\); every other tail state eventually produces all ones.

   **First assignment.** Derive finite-word automata for rows admitting \(d=1,2,4\) successive finite predecessors, retaining both endpoints and a marked center. Then look for an inductive automaton abstraction covering arbitrary ancestry depth and containing the marked seed \(1\). Combine that abstraction with the period monitor and seek a ranking certificate excluding an infinite periodic-center continuation.

   The concrete deliverable is an invariant with mechanically checkable initialization and preservation—not another table indexed by ancestry depth.

   **Likely obstruction.** Fixed-depth ancestry constraints alone cannot identify the single-seed orbit. Many local patterns have arbitrarily deep finite-seed realizations. The decisive information is the coupling between ancestry depth, total width, center position, and termination at \(1\); the required automata may grow without stabilizing.

5. **Density: bound mesoscopic block energy on the actual seed orbit.**

   **Why it could work.** [balance.md](/home/cochonhome/Documents/random-shit/wolfram/balance.md) correctly targets maximal annulus discrepancy. A block-energy estimate controls those maxima while allowing substantial individual fluctuations and avoiding assumptions about random initial configurations.

   Put \(a_t=2c_t-1\), \(N=2^m\), and \(L=2^{\lfloor m/2\rfloor}\). Partition \([N,2N)\) into \(B=N/L\) blocks, and define
   \[
   S_{m,b}=\sum_{t=N+bL}^{N+(b+1)L-1}a_t,\qquad
   E_m=\sum_{b=0}^{B-1}S_{m,b}^2.
   \]
   Cauchy–Schwarz gives
   \[
   A_m\le\sqrt{BE_m}+L.
   \]
   Thus \(E_m=o(NL)\) suffices; a quantitative target is
   \[
   E_m\le CNL^{1-\delta}\qquad(\delta>0).
   \]

   **First assignment.** Expand
   \[
   E_m=N+
   2\sum_b\sum_{h=1}^{L-1}
   \sum_{\substack{t,t+h\\\text{in block }b}}
   (-1)^{c_t\oplus c_{t+h}}.
   \]
   Study these aggregate correlations through the exact disagreement dynamics. For reference configuration \(b\) and disagreement \(e\),
   \[
   e'_j=e_{j-1}+(1+b_{j+1})e_j+
        (1+b_j)e_{j+1}+e_je_{j+1}.
   \]
   The first experiment should measure energy and its cross terms at these prescribed scales, looking for a seed-valid cancellation identity or inequality that can be proved.

   **Likely obstruction.** Disagreement evolution is not autonomous, and grouping correlations does not manufacture cancellation. A successful argument must control the reference-background terms and block boundaries. This is stronger than the density claim itself, although compatible with the observed behavior.

6. **Complexity: compute the exact dependency closure of a diagonal Mahler query.**

   **Why it could work.** [support_exact.md](/home/cochonhome/Documents/random-shit/wolfram/research/support_exact.md) and [support_fast.md](/home/cochonhome/Documents/random-shit/wolfram/research/support_fast.md) provide an exact nonlinear representation with safe truncation. The unexplored opportunity is computing one parity without constructing every truncated support.

   Write \(a_{k,j}=[j\in S_k]\). For \(j\ge1\),
   \[
   a_{k,j}=a_{k-1,j-1}+a_{k-2,j-1}
     +\sum_{r\lor s=j-1}a_{k-1,r}a_{k-2,s},
   \]
   and
   \[
   c_n=\bigoplus_{j\subseteq n}a_{n,j}.
   \]

   **First assignment.** Construct the backward dependency closure starting from this final parity, eliminating coefficients with \(j<\lceil k/2\rceil\). Preserve XOR cancellations and shared OR-convolution subexpressions. Compare dependency and circuit growth for powers of two, all-ones binary indices, and general indices.

   Seek an exact representation whose construction **and evaluation** admit a uniform bound. The relevant counterattack to the formal prize predicate is an \(O(n)\) algorithm in a specified machine model; an \(O(n\log n)\) bound would be useful progress but insufficient. [Official detailed formulation](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/).

   **Likely obstruction.** At \(n=2^m\), the query \(j=n\) immediately produces \(j-1=2^m-1\), exposing a dense Boolean lattice of OR operands. Sparse binary queries need not have sparse ancestry. Conversely, failure of this representation to compress would establish no lower bound for arbitrary algorithms.

I would run **1, 2, and 6 first in parallel**: period-2 certificate induction, the \(q=8\) label transducer with finite-support constraints, and diagonal Mahler dependency analysis. Each has a precise existing mathematical interface and a clear deliverable beyond larger tables. Attack 3 should follow if the first two reveal reusable propagation templates; attack 5 is the best independent route into density.