**Run the leftover CFG parse-parity test together with period-2 finite-row fibers and the 2-kernel screen first.** Cycle H left ideas7 item 4 unrun. The four items below are new. These are proposals; the certifiers are the authority.

Each kill criterion applies to the stated mechanism or bounded family. Passing a finite screen earns a proof attempt.

1. **Finite-row period-2 fibers — Condrey uniqueness for non-constant traces; Problem 1**

   Condrey (arXiv:2609.09431, 8 Sep 2026) proves that no nonzero finite configuration has an eventually *constant* central trace, by exhibiting a unique left half for every right half. This repository already has infinitely many 0s and 1s for the *single-cell* centre via Jen/Kopra. The new target is the next period:

   **No nonzero finite-support row has an eventually period-2 central trace.**

   Left reconstruction is unique given the centre and the right:
   \[
   \ell_t=c_{t+1}\oplus(c_t\lor r_t).
   \]
   For a prescribed period-2 centre and a quiescent finite right, either the reconstructed left is an infinite closed-form tail (Condrey-style, never a finite seed) or a finite bimaterial witness exists and the route dies.

   This is not strip residual SCCs, not \(T\le 28\) onset SAT, and not \(F_T\) ideal certificates.

   **First experiment:** exhaustive finite rows of radius \(w\le 8\); longest period-2 centre run \(L(w)\); reconstruct left from each finite right of width \(w\) under both phases; search for a finite witness lasting \(>4w+16\) steps.

   **Kill:** a finite nonzero witness that remains period-2 for the cap and for a doubled cap; or \(L(w)\) grows with no closed-form fiber. Survive only with a machine-checked unique infinite left fiber, as in Condrey’s constant case.

2. **2-kernel of the centre — automatic sequences / Cobham; Problem 1**

   An eventually periodic sequence is \(k\)-automatic, hence has a finite 2-kernel
   \[
   \bigl\{(c_{2^k n+r})_{n\ge 0}:k\ge 0,\,0\le r<2^k\bigr\}.
   \]
   An infinite kernel would prove nonperiodicity. This is not Berlekamp–Massey \(L(N)\), not S-adic substitutions, and not time-digit concatenation rank.

   **First experiment:** centre bits through \(2^{18}\) or \(2^{19}\); count distinct length-64 and length-128 prefixes of kernel words for \(k=0,\ldots,12\); check decimation closure.

   **Kill:** prefix counts saturate at some \(K_0\le 64\) (finite-kernel hypothesis survives; automaticity does not imply periodicity, so this is not a prize claim unless the 2-DFA is identified with \(c\) and proved aperiodic). Growth like \(2^k\) without a structural disagreement lemma also kills the *proof* route; a finite table of distinct prefixes is not an infinite kernel.

3. **Parse-parity of \(\operatorname{bin}(n)\) — leftover ideas7 item 4; Problem 3**

   Seek a Chomsky grammar with four nonterminals, at most eight binary productions, and terminal productions, no \(\varepsilon\)/unit rules, such that
   \[
   c_n=\#\{\text{parses of }\operatorname{bin}(n)\}\pmod 2.
   \]
   Fit \(n=1,\ldots,1023\); test through \(2^{16}-1\).

   **Kill:** unsatisfiable freeze, held-out mismatch, or no candidate in two hours.

4. **XOR-transforms of \(c\) — exact recoding; Problems 1 and 2**

   Screen \(c_t\oplus(t\bmod 2)\), first difference \(c_t\oplus c_{t+1}\), \(c_t\oplus c_{\lfloor t/2\rfloor}\), a discrete Laplacian, and \(c_t\oplus(\mathrm{popcount}(t)\bmod 2)\) for linear complexity, small-period witnesses, and dyadic discrepancy. The hope is a recoding whose structure is visible while \(c\) is not.

   **Kill:** every transform still has \(L(N)\ge N/4\) at \(N=4096\) and \(16384\), no small-period collapse, and discrepancy of the same order as \(D(N)\).

5. **Packed-row overlap valuation — 2-adic carries of \(z_{t+1}=z_t\oplus((z_t{\ll}1)\lor(z_t{\ll}2))\); Problem 3**

   Distinct from the killed signed \(\times 7\) identity and from residue periods of fixed low bits. Count nonlinear overlap sites \(N_t\) where the OR sees two 1s; record \(v_2\) of \(z_{t+1}\oplus z_t\) and related valuations.

   **Kill:** mean \(N_t/t>0.05\) (dense nonlinear core) or valuation sequences with no closed form cheaper than \(c_t\).

**Stop recommendation after these five.** Every remaining unused prompt from ideas7 is either equivalent to light-cone permutivity (coalescence of seeds that agree on \([-T,T]\)), another finite table, or a restatement of Problem 1. A coalescence lemma is recorded separately: flipping the extreme left ancestor always flips the centre, so coupling-from-the-past does not fire inside the cone.
