**Run 1, 2, and 3 first.** I rank these by how much a bounded first experiment can establish. These are proposals only; I have not implemented or run them.

1. **Stern–Brocot coordinates: search for rational dynamics of the entire row**

   **Target:** Problem 3 through an exact arithmetic formula.

   Read the packed row, from its right edge, as \(w_t=b_0\cdots b_{2t}\). Define
   \[
   L=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
   R=\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad
   q_t=(M_{b_0}\cdots M_{b_{2t}})\cdot1,
   \]
   with \(M_0=L,M_1=R\), acting by fractional linear transformations. This encoding is injective: successive inverse steps recover the word, including its middle letter \(c_t\).

   The speculation is that the rational coordinates obey a small birational recurrence even though the binary words do not simplify:
   \[
   q_{t+1}=\frac{P(q_t,q_{t-1})}{Q(q_t,q_{t-1})}.
   \]
   This tests arithmetic geometry of an injective row encoding. It uses neither low-bit orbit periods nor sections of the row-update automaton.

   **First experiment:** Fix bidegree at most \((2,2)\) for \(P,Q\). Solve the resulting homogeneous linear equations over \(\mathbb Q\) using rows \(0\) through \(63\), reject vanishing denominators and degenerate identities, then test every surviving candidate through row \(255\). Freeze the degree before fitting.

   A survivor earns an investigation of invariant curves and an exact iteration formula. QRT maps provide a concrete precedent for rational recurrences with invariant biquadratic curves; there is presently no evidence that this encoding produces one. [Hone, *ECM factorization with QRT maps*](https://arxiv.org/abs/2001.09076).

   **Kill criterion:** No valid rational recurrence in the fixed family survives the withheld rows. Do not rescue it by increasing degree or adding more previous rows. A surviving recurrence also fails as an algorithmic attack if computing \(q_n\) and extracting its middle letter still requires essentially the original simulation work.

2. **Holographic algorithms: can the Rule 30 constraint become a matchgate?**

   **Target:** Problem 3 through an exact determinant or Pfaffian representation.

   Regard each update as the four-leg tensor
   \[
   T(a,b,c,d)=\mathbf1\!\left[d=a\oplus(b\lor c)\right].
   \]
   Fix the single-cell bottom boundary and insert the indicator that the requested output is \(1\). Summing over internal bits gives exactly \(c_n\).

   Seek compatible changes of basis on contracted wires that turn the local constraints into **matchgate signatures**, which admit planar perfect-matching methods. This tests algebraic identities of the local tensors; it does not expand signed particle histories. The relevant machinery is the matchgate-identity characterization. [Cai–Choudhary, *On the Theory of Matchgate Computations*](https://eccc.weizmann.ac.il/eccc-reports/2006/TR06-018/index.html).

   **First experiment:** Write the simultaneous polynomial conditions for invertible \(2\times2\) wire bases, allowing orientation dependence and temporal parity. Include the rule tensor, copy tensors, seed/output boundaries, and any crossing tensors required by the chosen drawing. Test the elementary network and one explicitly fixed two-step blocking. Require exact algebraic certificates.

   **Payoff gate:** A successful transformation would justify trying to eliminate the uniform bulk analytically and retain a small boundary calculation. A Pfaffian on a graph with \(\Theta(n^2)\) vertices alone would not meet the prize’s computational threshold.

   **Kill criterion:** The complete tensor family has no compatible matchgate transformation in those two prescribed representations. Transforming only \(T\), while leaving an incompatible copy or crossing tensor, counts as failure.

3. **Adaptive Boolean certificates: how little of one cone must actually be evaluated?**

   **Target:** Problem 3 through a uniform algorithm for one requested \(c_n\).

   For the actual seed values, evaluating
   \[
   a\oplus(b\lor c)
   \]
   requires \(a\), but the OR can sometimes be certified by just one input equal to \(1\). When the OR is \(0\), both inputs must be certified. Shared subcalculations are charged once.

   Define \(C(n)\) as the smallest number of internal gates in such a certificate for \(c_n\). This is a data-dependent optimization on the evaluated Boolean circuit, with no finite-state ancestry recognizer.

   **First experiment:** Using independently generated rows solely as an oracle for this diagnostic, formulate minimum-certificate selection as a binary optimization problem. Require the output gate; impose the appropriate predecessor constraints at each selected gate; minimize the number selected. Obtain exact optima or certified lower bounds at \(n=32,64,128,256\). Compare these with an executable memoized short-circuit evaluator that receives only \(n\) and the seed.

   The gap between the oracle optimum and the executable evaluator is part of the experiment. A small certificate whose choices require knowing the whole triangle is not a fast algorithm.

   **Kill criterion:** As a preregistered research-budget rule, retire this prototype if certified lower bounds already exceed \(0.1n^2\) at both \(n=128\) and \(256\). Also retire it if the apparent savings depend on uncharged oracle values. That finite cutoff rejects this prototype; it is not a general complexity lower bound.

   The one-step streaming prompt itself supplies no lower bound: once the three relevant row bits are accessible, \(c_{t+1}\) is immediate. This proposal charges their recursive production.

4. **Discrete integrability: search for a genuine Lax representation**

   **Target:** An exact solution method for the seed evolution, initially aimed at Problem 3.

   Let \(f(a,b,c)=a\oplus(b\lor c)\). Seek small matrices \(L(b,c;\lambda)\) and \(M(a,b,c;\lambda)\) satisfying
   \[
   L\!\left(f(a,b,c),f(b,c,d);\lambda\right)M(a,b,c;\lambda)
   =
   M(b,c,d;\lambda)L(b,c;\lambda)
   \]
   for all sixteen quadruples.

   With invertible \(M\), this would evolve spatial matrix products by conjugation on periodic rings. The object sought is an isospectral representation valid for arbitrary ring lengths, followed by reconstruction of the finite-seed solution. Other cellular automata have yielded to Lax and commuting-transfer-matrix methods, though that supplies no integrability claim for Rule 30. [Pozsgay, *A Yang–Baxter integrable cellular automaton*](https://arxiv.org/abs/2106.00696).

   **First experiment:** Fix dimensions \(2\) and \(3\), with entries affine in \(\lambda\). Solve the sixteen polynomial matrix identities, explicitly enforcing generic invertibility. Screen solutions for configuration-dependent monodromy spectra and remove representations whose configuration dependence disappears under a local change of basis.

   **Kill criterion:** Every solution in the fixed family is singular, spectrally trivial, or removable by such a change of basis. A survivor must subsequently provide enough information to reconstruct the seed orbit; an isolated conserved trace does not justify continuing.

5. **Multiplicative-time disjointness: attack balance through prime dilations**

   **Target:** Problem 2.

   Put \(s_n=(-1)^{c_n}\) and study
   \[
   C_{p,q}(N)=\sum_{n=1}^{N}s_{pn}s_{qn},\qquad p\ne q\text{ prime}.
   \]
   A sufficient theorem is
   \[
   C_{p,q}(N)=o(N)\quad\text{for every distinct prime pair}.
   \]
   The Kátai–Bourgain–Sarnak–Ziegler criterion then gives \(\sum_{n\le N}s_n=o(N)\), by taking the multiplicative test function to be \(1\). [Bourgain–Sarnak–Ziegler, Theorem 2](https://publications.ias.edu/sites/default/files/disjointness%20b-s-z%20oct.pdf).

   The new mechanism to investigate is the joint evolution under **different powers** \(F^p\) and \(F^q\). It asks whether multiplicatively separated observations admit a structural disjointness argument. Additive lag correlations and mesoscopic block energy do not supply that argument.

   **First experiment:** Measure the exact dilation correlations for primes through \(13\) over several dyadic horizons. Then examine the first pair \((2,3)\) symbolically: derive the joint update and seek a seed-valid relation between its two boundary histories that can support a quantitative correlation estimate. The numerical screen earns only this one symbolic pass.

   **Kill criterion:** That pass produces only two independently growing cones, with no relation enabling an estimate stronger than the trivial bound. Random-looking correlation plots alone count as failure. This ranks fifth because the missing deterministic estimate could easily be harder than balance itself.