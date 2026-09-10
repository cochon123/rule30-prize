**Run time-digit matrices, noise susceptibility, and bias-preserving coarse-graining first—in that order.** My research ranking is below. These are untested proposals; I only read files and sources.

Each kill criterion applies to the stated mechanism or bounded family. Passing a finite screen earns a proof attempt.

1. **Vanishing-noise susceptibility — stochastic perturbation theory; Problem 2**

   Start the *same single-cell seed*, but independently flip each updated cell with probability \(\varepsilon\). Define
   \[
   B_N(\varepsilon)=\frac1N\sum_{t<N}\mathbb E[2x^\varepsilon_{t,0}-1].
   \]
   Thus \(B_N(0)=D(N)/N\).

   Positive permutation noise makes a permutive CA converge to the uniform Bernoulli measure. That supplies a legitimate noisy comparison process, including for deterministic initial configurations. It does **not** supply the required zero-noise estimate. [Marcovici–Sablik–Taati, Theorem 3.16](https://arxiv.org/html/1712.05500#S3.SS6).

   **New mechanism:** cancellation among the *signed effects of injected faults*. Seek, uniformly in \(N,\varepsilon\),
   \[
   |B_N(\varepsilon)-B_N(0)|\le C\varepsilon N^{3/2},
   \qquad
   |\mathbb E[2x^\varepsilon_{t,0}-1]|
      \le C e^{-\kappa\sqrt\varepsilon\,t}.
   \]
   Both bounds are speculative. Together, choosing \(\varepsilon=N^{-7/4}\) gives
   \[
   |D(N)|/N=O(N^{-1/4}+N^{-1/8}),
   \]
   which would settle balance.

   **First experiment:** at \(N=64,128,256\), compute the exact first derivative
   \[
   B_N'(0)=\frac1N\sum_v\bigl(D_N^{[v]}-D_N\bigr),
   \]
   where \(v\) ranges over update sites in the relevant cone and \(D_N^{[v]}\) comes from exactly one flipped update. Separately test noisy center relaxation at \(\varepsilon=2^{-6},2^{-8},2^{-10}\), through time 512, using 8,192 trajectories per rate. Cap the screen at two hours.

   **Kill:** reject the proposed quantitative version if \(|B_N'(0)|>8N^{3/2}\), or statistically resolved relaxation contradicts the predeclared envelope \(2e^{-t\sqrt\varepsilon/4}\). Abandon this route if the analysis only recovers the unsigned \(O(\varepsilon N^2)\) fault bound. A surviving first derivative is insufficient: the essential next lemma must control higher-order fault interactions uniformly.

2. **Matrices driven by the digits of time — noncommutative rational series; Problem 3**

   Seek fixed matrices and vectors over \(\mathbb F_3\), of dimension at most 16, such that
   \[
   c_n=\lambda^\top M_{b_1}\cdots M_{b_m}\rho,
   \qquad b_1\cdots b_m=\operatorname{bin}(n),
   \]
   with the field output always \(0\) or \(1\).

   This tests a representation of the **fixed seed’s time-indexed output**. The killed communication matrix instead varied the initial bits of an apex function. The four-letter substitution failure also does not exclude a 16-dimensional weighted representation.

   **Payoff:** an exact representation computes \(c_n\) with \(O(\log n)\) fixed-size field operations. No row construction or growing truth table appears in the evaluator.

   **First experiment:** form concatenation matrices
   \[
   H_\ell(u,v)=c_{\operatorname{val}_2(uv)}
   \]
   over \(\mathbb F_3\), using all binary words \(u,v\) of length at most \(\ell\), for \(\ell=2,\ldots,7\). Define the representation consistently on leading zeros. This needs only times below \(2^{14}\). If rank permits, reconstruct matrices and test unused times through \(2^{16}-1\).

   **Kill:** any rank above 16 excludes this family, since
   \[
   H(u,v)=(\lambda^\top M_u)(M_v\rho).
   \]
   Any held-out mismatch kills the reconstructed candidate. A survivor must come with an induction connecting its digit operations to Rule 30; fitting the output alone is not that induction.

3. **Preserve cumulative bias under coarse-graining — dynamical factors and coboundaries; Problem 2**

   Search for a coarse process that retains the center’s accumulated signed count. Let \(F\) be Rule 30 and \(\sigma(x)=2x_0-1\). Seek a block projection \(P\), a simpler CA \(G\), and bounded local functions \(g,\psi\) satisfying
   \[
   PF^b=GP,
   \]
   \[
   \sum_{s=0}^{b-1}\sigma(F^s x)
      =g((Px)_0)+\psi(F^b x)-\psi(x).
   \]

   The second equation is the crucial addition: the correction telescopes. On the actual seed,
   \[
   D(bK)=\sum_{k<K}g((G^kP\delta_0)_0)+O(1).
   \]
   This asks for an exact observable identity, rather than another estimate on block energy. Exact CA coarse-graining provides the underlying factor framework. [Israeli–Goldenfeld](https://arxiv.org/abs/nlin/0508033).

   **First experiment:** restrict to \(b=2,3\); two- or four-state coarse alphabets; additive radius-one \(G\) over \(\mathbb F_2\) or \(\mathbb F_2^2\); projections reading one block plus one neighboring bit on each side; and radius-two rational \(\psi\) with \(\|\psi\|_\infty\le32\). Impose both identities on **every relevant local input**, with a two-hour search cap.

   These are finite checks of universal identities, independent of onset \(T\). Additive \(G\) supplies a concrete route to an exact digit representation of its seed trace and an analysis of its cumulative output.

   **Kill:** no nonconstant projection satisfying both identities; or every surviving factor loses the bias observable. Also reject any candidate whose remaining coarse trace has no demonstrated simplification. A factor diagram alone is insufficient.

4. **Parse the binary index with a recursive grammar — context-free algebra; Problem 3**

   Seek a fixed grammar over terminals \(0,1\) such that
   \[
   c_n=\#\{\text{parses of }\operatorname{bin}(n)\}\pmod2.
   \]

   This permits recursive stack memory. Its recursion divides a word of length \(O(\log n)\); it does not expand a time-\(n\) spacetime cone. Noncommutative context-free series extend the matrix-product family and need not correspond to finite-state substitutions.

   **First experiment:** synthesize a grammar with four nonterminals, at most eight binary productions, and terminal productions. Exclude empty and unit productions so every input has finitely many parses. Fit all canonical binary indices below 1,024, then test through \(2^{16}-1\). Cap synthesis at two hours.

   **Payoff:** a fixed grammar evaluates parse parity by dynamic programming with \(O((\log n)^3)\) arithmetic work; ordinary machine overhead remains polylogarithmic.

   **Kill:** unsatisfiable bounded grammar constraints, any held-out mismatch, or failure to obtain a candidate within the cap. A survivor must support a structural Rule 30 proof explaining its production rules. Allowing productions indexed by \(n\), or importing precomputed rows, kills the mechanism.

5. **Identify an algebraic number behind the entire bitstream — Diophantine approximation; Problem 1**

   Form
   \[
   \alpha=\sum_{t\ge0}c_t2^{-t-1}.
   \]
   Investigate whether \(\alpha\) is a particular algebraic irrational with a small defining polynomial. This is an arithmetic hypothesis about the output real, independent of the packed-row coordinate transformations already tried.

   **Payoff:** proving that identification settles nonperiodicity: an algebraic irrational cannot have an eventually periodic binary expansion. It would not establish balance.

   **First experiment:** use the first 256 bits to obtain the exact interval
   \[
   I_{256}=[\alpha_{256},\alpha_{256}+2^{-256}].
   \]
   Search primitive irreducible integer polynomials of degrees \(2\) through \(6\), coefficient height at most \(2^{16}\), having a real root in that interval. Use lattice reduction to find candidates and certified root isolation to check them. Validate against the first 4,096 bits; cap the search at two hours.

   **Kill:** certified exclusion of the bounded polynomial family, a validation mismatch, or no candidate within the cap. A numerical relation alone does not survive. The next required result would be an invariant derived from Rule 30 proving that successive center bits choose the binary intervals containing that specific root.

   I rank this last because it has the weakest structural motivation, but its hypothesis is precise, stronger than nonperiodicity, and cheaply falsifiable.