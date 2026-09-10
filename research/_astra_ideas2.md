I read the three Round 1 notes and the supporting phase, ancestry, and disagreement notes. **I would retire the period-2 certificate template and Mahler dependency attack, and retarget \(q=8\) toward an invariant that preserves wrap consistency.** The remaining results do not suggest that the prize is close.

For the unrun attacks:

- **Old 3, phase propagation:** still worth one bounded attempt. Its deliverable must be a repeatable implication that catches the moving edge, including phase residues.
- **Old 4, inverse ancestry:** worth running only with ancestry depth, exact row width, and the marked center coupled together. Fixed-depth predecessor languages are insufficient.
- **Old 5, block energy:** remains mathematically valid but lower priority. Retarget it toward an exact cancellation mechanism before investing in energy measurements.

My revised ranking follows.

1. **\(q=8\): exclude the vacuum quotient using an invariant on neighboring period blocks.**

   **Target.** Prove that consistent reconstruction never enters \(I\), uniformly in spatial depth. This would exclude \(q=8\) directly, without proving periodicity of \(\sigma\).

   **Why.** [period9_sigma.md](/home/cochonhome/Documents/random-shit/wolfram/research/period9_sigma.md) identifies exactly what the failed quotient discarded: its wrap is another coordinate of the same reconstructed stream.

   Set
   \[
   S_k(n)=(W_{k-1}(n),W_k(n)).
   \]
   Reconstruction defines a one-sided cellular automaton in \(n\):
   \[
   S_{k+1}(n)=H(S_k(n),S_k(n+1)),
   \]
   where the second argument supplies \(C_{k,0}(n+1)\). The initial configurations have
   \[
   S_1(n)=(011111111,\ \sigma_n00000001)
   \]
   for arbitrary binary \(\sigma\). Thus consistency can be incorporated into the dynamics itself.

   **First assignment.** Seek a set \(K\) specified by relations on two or three neighboring \(S\)-symbols, satisfying:
   \[
   \text{all initial streams}\subseteq K,\qquad H(K)\subseteq K,
   \qquad K\text{ contains no symbol in }I.
   \]
   Derive candidate relations from the checked consistent blocks, then verify preservation over **every** locally compatible input block. The deliverable is an initialization-and-preservation proof, or an explicit failure of this abstraction.

   Start with exclusion of \(I\). Preserving rank \(\le3\) is stronger and unnecessary; excluding \(I\) alone does **not** establish the five-zero bound.

   **Obstruction.** Correlations may require arbitrarily long blocks in \(n\). A finite alphabet does not imply a finite local description of its reachable configurations. If short-block closure admits \(I\), extending the depth table is not progress toward this proof.

2. **\(001/0111\): prove a phase-sensitive propagation cycle with positive speed margin.**

   **Target.** Turn the depth-4 zeros into implications that reach \(k=T+s\) for every onset distance \(T\).

   **Why.** This remains untested, and the initial identities hold without the Fibonacci reduction that complicated period 2. Round 1 nevertheless makes the required speed comparison explicit.

   **First assignment.** Starting from the exact masks in [period_p_left_edge.md](/home/cochonhome/Documents/random-shit/wolfram/research/period_p_left_edge.md), derive implications on adjacent columns that retain forced bits **and relations among the free phases**. Examine spatial displacements \(4\) and \(8\), with the necessary right-side consistency constraints.

   Seek a closed implication cycle with spatial advance \(d\) and onset delay \(h<d\). Then separately prove that its zero phases intersect the moving edge for every onset residue. For a cycle with a fixed phase mask, this entails checking the relevant congruences involving \(d\), \(p\), and \(T\); speed alone is insufficient.

   **Obstruction.** Each application may introduce another unresolved stream, or require \(h\ge d\). Stop if the proposed cycle requires more information than it returns. A succession of different deeper identities is not an inductive certificate.

3. **Period 2 first: use exact seed ancestry with its width constraint.**

   **Target.** Extract an invariant of the single-seed orbit that survives arbitrary ancestry depth and constrains a hypothetical periodic continuation.

   **Why.** Round 1 repeatedly exposes missing boundary information. The inverse transducer provides an exact interface to both endpoints, rather than another free-boundary approximation.

   There is a useful sharpening of the old assignment. For a positive odd row integer \(z\) of bitlength \(2t+1\), **having \(t\) successive finite predecessors already forces termination at \(1\)**: each finite predecessor reduces bitlength by two, and oddness is preserved. Coupling depth and width therefore identifies the seed orbit exactly. The difficulty is compressing that condition.

   **First assignment.** Write the inverse scans as a triangular transducer diagram: predecessor \(i\) has width \(2(t-i)+1\), its marked center is at offset \(t-i\), and its tail must terminate in state \(00\). Start with the period-2 monitor.

   Seek a relation among the transducer states at the marked center and the two boundaries that is preserved when one ancestry layer is added. Keep the width/depth counters explicit. Require an identity or invariant valid for arbitrary diagram height; do not substitute the languages for \(d=1,2,4\).

   **Obstruction.** Exact ancestry can simply reconstruct the entire spacetime triangle. Terminal-state summaries may discard precisely the interior information that determines the center. If preservation requires retaining the complete row, this is an exact reformulation without a new proof mechanism.

4. **All periods: compose run gadgets and classify the unresolved word families.**

   **Target.** Replace a necklace-by-necklace program with a structural description covering arbitrary concatenations of zero and one runs.

   **Why.** Even successful exclusions of the currently targeted periods leave arbitrary primitive words. The isolated-zero work supplies one example of a run-length argument that could potentially compose.

   **First assignment.** At the existing radius, construct transfer relations for blocks \(0^a1^b\), retaining the left-neighbor output information needed by the periodic-neighbor test. Analyze powers of the constant-center transfer relations to separate bounded transients from recurrent behavior.

   Then test composition across **two unequal successive run blocks**. The concrete question is whether the long-one-run constraint still determines the relevant neighbor bits when the next gap differs. A useful result would classify arbitrary compositions by finitely many interface types, with proved rules for their neighbor outputs.

   Every claimed transient bound must exclude longer directed cycles; uniqueness of a self-loop is insufficient.

   **Obstruction.** Endpoint reachability can stabilize while output-label freedom remains unrestricted—the \(q=8\) full shift is the warning. The residual family may contain arbitrary concatenations and therefore infinitely many primitive periods. That outcome would establish a limitation of this strip abstraction, not solve the residual cases.

5. **Density: seek a deterministic cancellation certificate for block energy.**

   **Target.** Prove
   \[
   E_m=o(NL),\qquad N=2^m,\quad L=2^{\lfloor m/2\rfloor},
   \]
   on the actual seed orbit. The existing inequality
   \[
   A_m\le\sqrt{(N/L)E_m}+L
   \]
   then gives the desired discrepancy bound.

   **Why.** Mahler circuit growth says nothing against aggregate signed cancellation. But measuring small energy alone would supply another numerical conjecture.

   **First assignment.** Expand the energy into time-lag correlations and seek a deterministic pairing of opposite-sign terms, or a telescoping identity, with total unpaired or boundary contribution \(o(NL)\).

   Any proposed pairing must specify its domain, preserve multiplicities, prove sign reversal from Rule 30 identities, and count its exceptions. First derive the exact boundary remainder on one block; then determine whether those remainders combine favorably over the annulus.

   **Obstruction.** The disagreement dynamics depend on the reference background. No pairing or telescoping identity is currently supplied by the notes. Random-initial-condition symmetry cannot replace a pairing within the seed orbit, and the energy condition is stronger than density itself.

**Run revised 1, 2, and 3 next in parallel:** consistent-stream invariance for \(q=8\), phase propagation, and ancestry with exact width. They test three distinct missing mechanisms. If only two slots are available, choose 1 and 2; their success conditions and failure certificates are sharper.

**I no longer regard the existing local-certificate, strip, and Mahler program as a credible complete route to Problem 1 without a new global theorem.** That is a research judgment, not an impossibility result. The next round could still produce worthwhile period exclusions.

A qualitatively different direction is **seed-specific rigidity of time-shifted orbits**. For arbitrary \(p>0\), set
\[
e_p(t,j)=x(t+p,j)\oplus x(t,j).
\]
Seek a theorem using the common single-seed ancestry and both expanding boundaries:
\[
e_p(t,0)=0\text{ eventually}
\quad\Longrightarrow\quad
e_p(t,-1)=0\text{ eventually}.
\]
This would produce an eventually periodic adjacent pair and invoke the established width-2 obstruction. [Kopra, Corollary 3.7](https://www.utupub.fi/bitstream/handle/10024/174540/1-s2.0-S0304397522007502-main.pdf?isAllowed=y&sequence=1).

The spatially periodic counterexample in the disagreement notes rules out proving that implication by local causality alone. It would need a global boundary or ancestry argument. If the next three assignments produce only larger residual descriptions, I would stop expanding this computational program and redirect effort to that theorem.