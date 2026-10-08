**Run streaming next-centre-bit and an L_run-growth test first.** Cycle J killed the constant \(L_{\mathrm{run}}\le 24\) at radius 11 (witness length 29). Period 3 and \(q=8\) finite-row scans grow with \(w\). Short traces are unsat. Ideas9 item 5 was not run.

1. **Streaming the next centre bit from the packed row — Problem 3 (leftover ideas9 item 5)**

   After row \(t\) is known as a packed integer, \(c_{t+1}=x(t,-1)\oplus(x(t,0)\lor x(t,1))\) is three bits. Freeze: popcount, \(v_2\), and every length-\(\le 8\) sliding window of the packed word, plus those statistics on \(z\oplus(z{\ll}1)\) and \(z\land(z{\ll}1)\). Ask whether any such statistic determines the triple, or yields an \(o(t)\) evaluator.

   **Kill:** every statistic still requires reading \(\Theta(t)\) bits or fails to determine the triple on \(t\le 4096\).

2. **Is \(L_{\mathrm{run}}(w)\) unbounded? — Problem 1**

   The \(w=11\) maximizer does not grow when zero-padded. Search a one-parameter family (concatenate two distant period-2 bursts, or iterate the mask-4369552 motif) that produces arbitrarily long finite period-2 centre runs. Exhaustive \(w=12\) is optional; a constructive family with \(L(w)\to\infty\) kills every constant bound. A proof that \(L_{\mathrm{run}}=O(1)\) would still exclude eventual period 2.

   **Kill:** no family with \(L\ge 30\) in a two-hour search, and no \(O(1)\) proof.

3. **Period 4 and 5 finite-row scans — Problem 1**

   Same engine as `period3_fiber.py`, primitive necklaces of periods 4 and 5, exhaustive \(w\le 7\). Kill if \(L_p(w)\) grows with no plateau; finite theorem if it plateaus.

4. **Signed pairing of period-2 bursts — Problem 2**

   Interior period-2 centre bursts contribute almost 0 to \(D(N)\) (equal 0s and 1s). If the complement (the “defects” that break alternation) had density \(o(1)\) or a pairing, \(D(N)=o(N)\) would follow. Measure defect density on the prize seed through \(N=10^5\), and on exhaustive small-\(w\) rows.

   **Kill:** defect density stays \(\ge 1/4\) on the prize seed, or defects are themselves as irregular as \(c\).

5. **Forbidden spacetime block forced by a periodic centre — Problem 1**

   Search a finite \(h\times w\) pattern that Rule 30 forbids, but that every sufficiently long period-2 (or period-3) centre column would force in the strip. Distinct from residual-SCC emptiness (overapproximation). Kill if every candidate block appears in the seed spacetime or in a legal strip path.
