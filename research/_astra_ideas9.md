**Run the period-2 \(L_{\mathrm{run}}\) extension and the period-3 finite-row scan first.** Cycle I left a plateau \(L_{\mathrm{run}}(w)=24\) for \(6\le w\le 10\). That is the only surviving non-kill. These are proposals.

1. **Uniform bound or counterexample for period-2 centre runs — Problem 1**

   Cycle I proved: every nonzero row of radius \(w\le 10\) has every period-2 centre run of length at most 24. Upgrade this to a \(w\)-independent bound, or kill it with a radius-\(11\) (or \(12\)) witness of length \(\ge 25\).

   **First experiment:** exhaustive \(w=11\) (\(2^{23}-1\) states, \(tcap=8\cdot 11+128=216\)). If too heavy, random plus boundary-heavy sampling of \(2^{20}\) masks at \(w=11,12\), plus every row whose live support is a single interval of length \(\le 8\) placed at the edge. Record \(L_{\mathrm{run}}\) and a maximizer.

   **Kill:** a finite nonzero row with a period-2 centre run of length \(\ge 25\) that survives doubling the time cap. Survive only with a proof that no finite row has a period-2 run longer than 24 (or some other constant), which would exclude eventual period 2 for every finite seed.

2. **Period-3 finite-row analog of the radius-10 theorem — Problem 1**

   Same exhaustive scan as `period2_fiber.py`, but for centre words `001` and `011` (both phases/rotations). Measure longest exact period-3 run \(L_3(w)\) for \(w\le 8\).

   **Kill:** \(L_3(w)\) grows through the scanned radii with no plateau, or a witness that looks eventual in the cap. Survive a finite theorem if \(L_3\) plateaus at a constant on \(w\le 8\).

3. **Trace of a short matrix product over a finite ring — Problem 3**

   Seek \(d\le 4\) matrices \(A_0,A_1\) over \(\mathbb F_2\), \(\mathbb F_3\), or \(\mathbb Z/8\mathbb Z\) such that \(c_t=\mathrm{Tr}(A_{b_1}\cdots A_{b_m})\) or a fixed entry, with \(b=\mathrm{bin}(t)\) **or** with the product taken along the packed row’s bits. Not a Lax pair, not communication rank of \(f_h\), not the killed \(\mathbb F_3\) concatenation-rank freeze of dimension 16.

   **First experiment:** for \(d=2,3\) enumerate matrix pairs (or sample if \(d=3\) over \(\mathbb Z/8\mathbb Z\)) and test \(c_t\) on \(t<256\). Kill on no fit, or a fit that fails hold-out \(t<4096\).

4. **Period-9 / \(q=8\) finite-row scan — Problem 1**

   The isolated-zero exception `011111111` still has residual strip SCCs. Exhaustive finite rows of radius \(w\le 6\): longest exact period-9 isolated-zero centre run. Kill if some finite row realises a long mixing-\(\sigma\) tail; a small \(L_9(w)\) plateau is a finite theorem in the same sense as period 2.

5. **Streaming next-centre-bit from the packed row — Problem 3**

   After row \(t\) is known as a packed integer, \(c_{t+1}=x(t,-1)\oplus(x(t,0)\lor x(t,1))\) is three bits. Ask whether those three bits (not the whole next row) admit an \(o(t)\)-bit-operation evaluator in the freeze of: popcount, valuation, and length-\(\le 8\) sliding windows of the packed word. Kill if every such statistic still requires reading \(\Theta(t)\) bits or fails to determine the triple.
