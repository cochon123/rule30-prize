**Run weight-9 origin-in-hull next.** Cycle M proved L≤31 for in-hull weight≤8 span≤24. The prize seed’s later rows have much larger weight.

1. **Origin-in-hull weight 9–10, span ≤20 — Problem 1**

   Same census as `period2_hull.py`, wt=9 and 10, span≤20 (keep the state space comparable). Kill if some in-hull row has L≥32. Finite theorem if L≤31 still holds.

2. **Defect recurrence — leftover ideas11/12 item; Problem 2**

   Seek a local rule for d_t=1_{c_t=c_{t-1}} on a bounded window of (c,l,r). Kill if the window is the original cone.
