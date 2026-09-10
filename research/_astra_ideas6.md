**Run 1, 2, and 3 first.** I rank these by the value of a bounded first test. These are proposals only: I read the research notes and sources, but ran no experiments and edited no files.

1. **Communication complexity: compress what crosses a spatial cut**

   **Target: Problem 3. Language: communication protocols and matrix rank.**

   Let \(f_h\) be the apex value after \(h\) steps from an arbitrary bottom word of length \(2h+1\). Form the Boolean communication matrix
   \[
   M_h(u,v)=f_h(uv),\qquad |u|=h,\quad |v|=h+1.
   \]
   Seek a decomposition
   \[
   f_h(uv)=\bigoplus_{i=1}^{r_h}A_{h,i}(u)B_{h,i}(v)
   \]
   with small \(r_h\) **and recursively computable features** \(A,B\).

   There is a specific historical lead: Goles and coauthors identified Rule 30 as a possible example with high one-way communication complexity but low matrix rank. They presented this as experimental evidence, not a theorem. [*Communications in cellular automata*, §4.4](https://arxiv.org/pdf/0906.3284).

   **First experiment:** Compute exact ranks over \(\mathbb F_2\) for \(h=2,\ldots,10\), including the central split and its two neighboring splits. Freeze the prototype’s envelope at \(r_h\le8h\). For survivors, extract exact factorizations and examine whether their feature spaces admit a uniform composition rule when two time blocks are joined.

   **What would matter:** A composition identity describing the features at arbitrary depth, with their construction and evaluation costs included. A successful universal protocol applies to the prescribed seed.

   **Kill criteria:** Any required rank exceeds \(8h\); or the factorization requires exponentially indexed truth tables; or the features can only be evaluated by simulating their original cones. Low communication with expensive computation is also failure.

   This tests the global prediction function across a cut. Compatibility with local matchgate tensors is not required.

2. **Exact block reuse: measure whether the seed admits a compressed simulation**

   **Target: Problem 3. Language: persistent data structures and memoized spacetime blocks.**

   Build a one-dimensional Hashlife-style evaluator: an interned binary tree represents spatial words, and cached operations advance their protected central portions by a prescribed number of steps. Identical words at different places or times share the same evolution calculation.

   The opportunity is **repeated evaluated blocks on this seed**, including repetitions across different branches of a query. The failed automaton-section calculation counted a different representation of composed maps. Hashlife’s established mechanism is reuse of spatial and temporal regularity. [Golly’s algorithm documentation](https://golly.sourceforge.io/Help/Algorithms/HashLife.html).

   **First experiment:** Specify one overlapping binary decomposition, leaf width eight, exact interning, and an initially empty cache. Compute individual targets at \(n=2^{10},\ldots,2^{15}\), restarting for every target. Record:
   
   - Distinct block-evolution requests at each scale.
   - Leaf updates, node construction, comparisons, and cache operations.
   - Reuse within the central region, separately from vacuum and ordered edges.

   **What would matter:** A recurrence bounding the number of distinct requested blocks, yielding a uniform algorithm. The prototype must construct its own blocks from the seed.

   **Kill criteria:** Retire this implementation if its charged work grows by at least \(3.8\) on each of the final two doublings and its savings remain confined to vacuum or edge regions. Also kill any result whose apparent speedup uses a precomputed spacetime dictionary.

   Those numerical thresholds are research-budget rules, not asymptotic lower bounds.

3. **Nonuniform substitution tilings: get balance without determining every time**

   **Target: Problem 2. Language: hierarchical word tilings and contraction of incidence matrices.**

   Seek a hierarchical description
   \[
   c=\tau\!\left(\lim_k
   \sigma_{i_0}\sigma_{i_1}\cdots\sigma_{i_k}(a_k)\right),
   \]
   using a small library of **nonuniform** substitutions. The directive sequence \(i_0,i_1,\ldots\) may remain unknown.

   The useful possibility is that *every permitted directive sequence is balanced*. Then determining the directive is unnecessary for Problem 2.

   A concrete sufficient certificate is:
   \[
   \text{length of every depth-}k\text{ tile}\ge2^k,\qquad
   |\text{ones}-\text{zeros}|\le C\rho^k,\quad 1<\rho<2.
   \]
   With bounded substitution lengths, decomposing any prefix into tiles gives
   \[
   |D(N)|=O\!\left(N^{\log_2\rho}\right)=o(N).
   \]
   The contraction would come from the substitution matrices on their imbalance subspace.

   **First experiment:** Freeze four auxiliary letters, two substitutions, image lengths two or three, and a letter-to-bit coding. Require at least one substitution to be nonuniform. Search for compatible hierarchical parses of the first \(1{,}024\) center bits; freeze each surviving library and test extension through \(16{,}384\). Require an exact common contraction certificate, not measured frequencies. Cap synthesis at two CPU-hours.

   **What would matter:** A survivor earns one symbolic attempt to derive its hierarchical tiles from the actual Rule 30 seed evolution. This must prove that the hierarchy continues indefinitely.

   **Kill criteria:** No library survives; no strict contraction exists; the budget expires without a candidate; or lifting the proposed substitutions to spacetime requires continually introducing new tile types or unrecorded boundary information.

   This permits variable expansion lengths and varying substitutions. It does not ask the previously studied sections of \(U\) to close.

4. **Signed carry corrections to multiplication by seven**

   **Target: Problem 3. Language: integer arithmetic and redundant binary representations.**

   For the right-edge packed row \(Z_t\), define
   \[
   U=Z_t\mathbin{\&}(2Z_t),\quad
   V=Z_t\mathbin{\&}(4Z_t),\quad
   W=Z_t\mathbin{\&}(2Z_t)\mathbin{\&}(4Z_t).
   \]
   Ordinary integer identities give
   \[
   Z_{t+1}=7Z_t-2Q_t,\qquad Q_t=2U+V-W.
   \]
   Consequently,
   \[
   Z_n=7^n-2\sum_{t<n}7^{\,n-1-t}Q_t.
   \]
   Only this expression modulo \(2^{n+1}\) is needed for \(c_n\).

   The speculative opening is a sparse **signed-digit representation of the correction stream**, together with arithmetic rules that update it without unpacking the rows. This concerns carries and borrows in ordinary arithmetic, rather than low-bit orbit periods or rational row coordinates.

   **First experiment:** At \(n=128,256,512\), compute the minimum signed-binary weight of each \(Q_t\bmod2^n\), allowing digits \(-1,0,1\). Measure the total weight
   \[
   S(n)=\sum_{t<n}w_{\pm}(Q_t\bmod2^n).
   \]
   Freeze this sparse-correction family before measurement. If it survives, derive an executable update for its signed digits and charge normalization, modular multiplication, and correction generation.

   **What would matter:** A provably sparse arithmetic source and a uniform way to generate it. Modular exponentiation supplies the homogeneous term; the correction is the entire research question.

   **Kill criteria:** \(S(n)>0.05n^2\) at both \(n=256\) and \(512\); or generating the corrections requires the full packed-row evolution; or carry normalization restores quadratic work.

   This deliberately tests a narrow arithmetic compression hypothesis. The displayed identity alone is not acceleration.

5. **A periodically driven invasion front that sweeps finite disturbances rightward**

   **Target: uniform exclusions for selected periods in Problem 1. Language: travelling fronts and stability under finite perturbations.**

   Work on the **right half-line**, driven at \(j=0\) by \(w=001\) or \(w=0111\). At any actual onset, that half-line is a finite word followed by zeros.

   Seek an exact travelling solution with a periodic wake on its left and zero vacuum on its right. Then seek a stability theorem: every finite perturbation is eventually swept away from each fixed site behind the advancing front.

   That would make column \(1\) eventually periodic for every finite initial right-hand word. Combined with the prescribed periodic center and the already available two-column theorem, it would exclude that center word independently of onset \(T\).

   **First experiment:** Search fronts with interface width at most twelve, wake spatial period at most eight, temporal period at most twelve compatible with the driver, and positive displacement per period. Verify any candidate exactly against the local rule, including both infinite tails.

   For each survivor, search a bounded local drift certificate. Let \(\ell_t\) be the leftmost disagreement with the reference front and \(R_t\) its position. Test potentials of the form
   \[
   B_t=\min(\ell_t,R_t)+\phi(s_t),
   \]
   where \(s_t\) records phase and a fixed local interface window. Require
   \[
   B_{t+1}\ge B_t+\varepsilon
   \]
   for every applicable local case, with bounded \(\phi\) and \(\varepsilon>0\). Freeze an eight-cell window and \(|\phi|\le16\).

   **What would matter:** An exact travelling solution plus a universally verified drift certificate covering arbitrary finite perturbations. Together these give an infinite-time, onset-independent statement.

   **Kill criteria:** No front exists in the fixed family; the drift constraints are infeasible; or certificate validity needs a bound on the initial perturbation’s length. A travelling front without the attraction certificate does not pass.

   This examines forward invasion and stability on the right half-line for two specified drivers. It does not extend the period-2 renewal bound or reconstruct more left strips.