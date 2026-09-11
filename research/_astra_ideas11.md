**Run a longer-cap census of weight-8 rows and the leftover forbidden-block search first.** Cycle K found L=31 on a weight-8 span-19 row; concatenation of maximizers does not grow L.

1. **Weight-8 census with a long cap — Problem 1**

   Both known maximizers (masks 4369552 and 281769) have eight 1s and span 19. Exhaustive (or complete up to translation) finite rows of Hamming weight \(\le 8\) and span \(\le 24\), with `tcap=32w+512` (Cycle J’s `8w+128` missed the length-31 burst). Record max L versus weight. Kill if some weight-8 row has L≥40, or if L keeps rising with span. A plateau L≤31 on this census is a finite theorem for those supports only.

2. **Forbidden spacetime block forced by a periodic centre — leftover ideas10 item 5; Problem 1**

   Search a finite \(h\times w\) pattern that Rule 30 forbids locally, but that a long period-2 (or period-3) centre column would force in every legal strip completion. Kill if every candidate appears in the seed spacetime or in a residual strip SCC.

3. **Periods 6 and 7 finite-row scans — Problem 1**

   Same engine as `period45_fiber.py`, exhaustive `w≤6`. Kill if L_p grows through the scanned radii with no plateau.

4. **Seed left edge as a missing strip constraint — Problem 1**

   Finite-row scans allow arbitrary finite supports. The prize seed has `x(t,-t)=1` for all t (left edge). Restrict period-2 reconstruction to rows whose leftmost 1 is exactly at `-t` at every time (the true light-cone edge). Kill if that class is empty for onset after a bounded time, or if it still admits long period-2 bursts.

5. **Exact defect generating function — Problem 2**

   Cycle K showed D(N) equals the defect signed sum plus O(1). Seek a closed recurrence for the defect sequence d_t = 1_{c_t=c_{t-1}} from the local rule and neighbours. Kill if the recurrence still involves an unbounded right/left window (the original CA).
