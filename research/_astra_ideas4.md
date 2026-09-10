**Run attacks 1, 2, and 3 first in parallel.** They target different problems and each starts from an exact identity. Attacks 4 and 5 are higher-risk alternatives.

I read [REPORT.md](/home/cochonhome/Documents/random-shit/wolfram/REPORT.md), [LOG.md](/home/cochonhome/Documents/random-shit/wolfram/research/LOG.md), and [_astra_ideas3.md](/home/cochonhome/Documents/random-shit/wolfram/research/_astra_ideas3.md), plus the notes linked below. These are proposals only; no implementation or file edits were performed. The proposed proof mechanisms are speculative.

**1. Automaton groups: compress powers along the particular input ray**

**Target:** Problem 3, by constructing an exact algorithm.

The row map
\[
f(z)=z\mathbin{\mathrm{XOR}}\bigl((2z)\mathbin{\mathrm{OR}}(4z)\bigr)
\]
has a particularly small description as an automorphism of the binary tree, reading bits least-significant first. Its three states satisfy
\[
A=(A,C),\qquad B=(A,C)\sigma,\qquad C=(B,C)\sigma,
\]
where \(\sigma\) flips the current bit and \(A=f\). The states remember whether the previous two input bits are \(00,01,\) or \(1*\).

A *section* is the action remaining after an input prefix has been read. Consequently, for \(n\ge1\),
\[
c_n=\varepsilon\!\left(A^n|_{\,10^{n-1}}\right),
\]
where \(\varepsilon\) records whether the section flips its first bit. In particular, \(A^n|_1=C^n\). This translates the query into **compressed group arithmetic followed along one ray**. Wreath recursions and sections are standard objects in [automaton-group theory](https://gap-packages.github.io/automgrp/htm/CHAP001.htm).

**Why this is different:** The old [ancestry transducer](/home/cochonhome/Documents/random-shit/wolfram/research/ancestry_transducer.md) recognized finite predecessors. This asks whether powers of the *forward* map admit shared algebraic descriptions sufficient for one output bit. It also goes beyond the already-known [odometer conjugacy](/home/cochonhome/Documents/random-shit/wolfram/research/orbit_conjugacy.md), whose moving-observable obstruction remains valid.

**First assignment:** Derive symbolic section rules, with exponent \(m\) left arbitrary, for \(B^m,C^m,(BC)^m,(CB)^m\). Seek a straight-line grammar closed under squaring and taking the next section on the query ray. Deliver a proposed representation, exact rewrite identities, and a construction-plus-evaluation cost recurrence. Count exponent arithmetic and all preprocessing; \(O(n\log n)\) would be progress, while the prize threshold requires \(O(n)\) in an appropriate bit-cost model.

**Likely obstruction:** The whole group is already noncontracting: \(A^m|_{0^k}=A^m\), and \(A\) has infinite order. Any useful simplification must therefore concern the actual query ray. Section words may otherwise retain linear size through linearly many levels.

**Kill criterion:** Retire this representation if its proved rewrite rules require \(\Omega(n^2)\) total expansion along an explicit infinite family of query rays.

**2. Renewal theory: transport defects through the gaps of the Fibonacci neighbor**

**Target:** Problem 1, initially period 2.

Under the alternating-center hypothesis, write \(u_n=x(2n,1)\), and regard its isolated ones as renewal events. Their gap sequence becomes the primary object.

There is an immediate bridge from the [vacuum lemma](/home/cochonhome/Documents/random-shit/wolfram/research/period2_vacuum.md). Suppose
\[
u_i=0\qquad(a\le i<b).
\]
Replace everything from index \(a\) onward by zero. The resulting reconstructed \(F_k\) becomes \(k\bmod2\) beyond \(11a+C\), for an absolute constant \(C\), using the note’s bound on propagation per fold. The true and truncated reconstructions agree through \(k=2b\), by the variable bound. Hence
\[
F_k=k\bmod2\qquad(11a+C\le k\le2b).
\]
Sufficiently large multiplicative gaps therefore expose an odd-indexed \(1\) arbitrarily far left, contradicting an eventually-zero spatial tail.

This already restricts a hypothetical counterexample: its renewal gaps cannot repeatedly overwhelm their starting positions by that factor.

**Why this is different:** The proposed invariant is the propagation of a defect front relative to consumed input length. Neither onset \(T\) nor strip width is enumerated.

**First assignment:** For a finite Fibonacci word \(w\), let \(E(w)\) be the last disagreement of its zero-padded reconstruction with vacuum. Analyze the operations that prepend \(0\) and \(10\). Seek a weighted defect potential proving
\[
E(w)\le2|w|+C,
\]
or another uniform insulation bound. This sharper inequality would imply that any hypothetical finite-support continuation has **bounded zero gaps** in \(u\). Derive scattering rules for isolated defects and their collisions, with symbolic gap lengths.

The next step would use the resulting return-gap dynamics to seek a nonzero defect flux incompatible with an eventually-zero left tail.

**Likely obstruction:** Collisions may carry information about the entire preceding renewal history. Bounded-gap aperiodic sequences would also remain after the first lemma.

**Kill criterion:** Retire the proposed potential if an explicit Fibonacci-word family makes its excess front displacement grow without bound and invalidates the claimed insulation estimate.

**3. Signed dual particles: cancel expansion histories before evaluating the seed**

**Target:** Problem 2.

Set \(s_j=(-1)^{x_j}\). Rule 30 has the exact real-valued identity
\[
s'_j=\frac12s_{j-1}
 \bigl(1+s_j+s_{j+1}-s_js_{j+1}\bigr).
\]
For characters \(\chi_A=\prod_{j\in A}s_j\), multiplication combines particle sets by symmetric difference. Pullback by Rule 30 therefore defines a signed linear operator \(K\) on finite particle sets. A single particle produces four branches with weights \(+\tfrac12,+\tfrac12,+\tfrac12,-\tfrac12\).

The single-cell seed evaluates a terminal particle set by
\[
\phi(A)=(-1)^{\mathbf1_{0\in A}}.
\]
Thus, with \(v\) the singleton particle at the origin,
\[
D(N)=-\left\langle\sum_{t<N}K^t v,\phi\right\rangle.
\]

**Why this is different:** This starts with a Rule-30-specific signed identity and acts on backward expansion histories. The failed [block-energy attack](/home/cochonhome/Documents/random-shit/wolfram/research/block_energy.md) grouped time correlations without obtaining such a cancellation mechanism. No random initial configuration is introduced here.

**First assignment:** Expand one and two dual steps symbolically, retaining rational weights and symmetric-difference collisions. Identify a local rewrite pairing histories with opposite **seed-evaluated** contributions. Then determine whether the rewrite can be oriented into an involution on the time-summed histories, with explicitly described unpaired boundary histories. The first deliverable is one nontrivial exact cancellation rule plus its residual recursion—not a numerical discrepancy estimate.

A successful extension would bound the absolute weight of unpaired contributions by \(O(N^\alpha)\), \(\alpha<1\).

**Likely obstruction:** This is a signed process, not a probability process. Absolute branching weight increases, and useful cancellation may require global information. Merely changing basis could reproduce the original computation.

**Kill criterion:** Retire the proposed pairing if it fails to preserve the single-seed evaluation or leaves a residual recursion with no demonstrable cancellation gain.

**4. Cartier operators: distinguish infinitely many diagonal kernel states**

**Target:** Problem 1 for all periods; possible secondary progress on Problem 3.

Let \(v(t,k)=x(t,t-k)\), and work over \(\mathbb F_2\):
\[
U(z,w)=\sum_{t,k\ge0}v(t,k)z^tw^k,\qquad
R(z,w)=\sum_{t,k\ge0}v(t,k)v(t,k+1)z^tw^k.
\]
The recurrence gives
\[
\bigl(1+z+zw+zw^2\bigr)U=1+zw^2R.
\]
The center generating function is \(C(z)=\operatorname{Diag}U\).

Cartier operators select coefficients at even or odd indices. In particular,
\[
\Lambda_r C=\operatorname{Diag}\Lambda_{r,r}U.
\]
An infinite family of distinct iterated Cartier images of \(C\) would prove that \(c\) is not 2-automatic, hence not eventually periodic. This uses the automatic-sequence/algebraic-series language developed in work such as [Rowland–Yassawi](https://jtnb.centre-mersenne.org/item/10.5802/jtnb.901.pdf).

**Why this is different:** The objects are arithmetic subsequences of the center, rather than Mahler support sets. The [quadratic Mahler dependency result](/home/cochonhome/Documents/random-shit/wolfram/research/mahler_dependency.md) does not establish growth of this kernel.

**First assignment:** Apply the four bivariate Cartier operators to the displayed identity and derive the first correlation equations required for \(R\). Seek a parameterized family of operator words \(W_m\) with explicit coefficient witnesses distinguishing
\[
\operatorname{Diag}(W_mU).
\]
The essential deliverable is a witness rule valid for arbitrary \(m\). Differences confined off the diagonal do not count.

**Likely obstruction:** Adjacent correlations may generate an unclosed hierarchy. Nonautomaticity is also a stronger target than nonperiodicity; growing finite kernel samples establish neither.

**Kill criterion:** Retire this route if its purported distinguishing mechanism exists only off the diagonal or its closure simply reconstructs the spacetime triangle.

**5. Relative symbolic complexity: prove that the center carries unbounded additional information**

**Target:** Problem 1 for all periods.

Let \(\ell_t=x(t,-1)\). Define the maximal fiber size
\[
R_m=\max_{a\in\{0,1\}^m}
\#\{b:(a,b)\text{ occurs as a length-}m
\text{ block of }(\ell,c)\}.
\]
This counts how many center words actually accompany the **same** left-column word along the single-seed orbit.

If \(c\) has eventual period \(p\) after onset \(T\), it has at most \(T+p\) distinct length-\(m\) factors. Therefore
\[
R_m\le T+p\quad\text{for every }m.
\]
Proving \(\sup_mR_m=\infty\) would exclude every eventual period.

This criterion is stronger than center aperiodicity as a statement about sequence pairs: an aperiodic pair with \(c=\ell\) has \(R_m=1\). It is therefore an independent sufficient condition, rather than the rejected periodic-neighbor implication.

**Why this is different:** This studies relative language complexity and factor fibers of an individual orbit. It uses neither wider strips nor entropy of arbitrary initial configurations. Directional symbolic dynamics, including [Boyle–Lind’s framework](https://sites.math.washington.edu/~lind/Papers/ExpansiveSubdynamics.pdf), supplies relevant language, but no seed-specific conclusion automatically follows.

**First assignment:** Derive the exact conditional branching rule:
\[
c_t=1\Longrightarrow c_{t+1}=1-\ell_t,
\]
while \(c_t=0\) allows branching through the right neighbor. Seek a seed-valid return-word construction producing, for every \(r\), one left word accompanied at actual occurrence times by at least \(r\) distinct center words. The deliverable must specify how occurrence times and their spacetime certificates extend inductively; a freely chosen boundary is insufficient.

**Likely obstruction:** Locally admissible branches need not all occur on the prescribed orbit. Establishing repeatable branching there may approach a normality-strength problem.

**Kill criterion:** Retire the construction if its amplification step requires changing the initial seed or independently choosing an exterior boundary.