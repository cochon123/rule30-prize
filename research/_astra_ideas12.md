**Run an origin-in-hull-only census first.** Cycle L’s L≥32 bursts are all off-hull. The prize seed has a 1 at the origin.

1. **Origin-in-hull weight-8 census — Problem 1**

   Repeat `period2_weight8.py` but keep only placements with `min live ≤ 0 ≤ max live`. Kill if some in-hull row has L≥32 (after doubling tcap). Finite theorem if every in-hull weight-≤8 span-≤24 row has L≤31.

2. **Prize-seed left edge — Problem 1**

   Restrict period-2 finite rows to those with `x(t,-t)=1` for all t in a window (true Rule 30 left edge from a finite seed that includes a leftmost 1 that never dies). Kill if this class still has long period-2 centre bursts; survive a lemma if the moving edge forces the centre off period 2 in O(1) extra time.

3. **Defect recurrence from neighbours — leftover ideas11 item 5; Problem 2**

   Seek a closed local rule for d_t=1_{c_t=c_{t-1}} using only a bounded window of previous defects. Kill if the window grows or the rule reconstructs the triangle.
