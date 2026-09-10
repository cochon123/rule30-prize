# Alternating-center sideways reconstruction

Assume (after shifting the time origin) that the eventual center trace is
\(c_{2n}=0,c_{2n+1}=1\). Let
\[
u_n=r_{2n}=x(2n,1),\qquad v_n=r_{2n+1}=x(2n+1,1).
\]
The left neighbor is reconstructed exactly from center and right traces by
\[
l_t=c_{t+1}\oplus(c_t\lor r_t).
\]
Therefore
\[
l_{2n}=1\oplus u_n=1-u_n,\qquad l_{2n+1}=0\oplus1=1.
\]
In particular, the odd-time part of column −1 is periodic, but its even-time
part is the arbitrary sequence (1-u_n).

Let (a_t=x(t,-2)). Sideways reconstruction gives
\[
a_t=l_{t+1}\oplus(l_t\lor c_t),
\]
so
\[
a_{2n}=u_n,qquad a_{2n+1}=u_{n+1}.
\]
The odd right trace (v_n) has disappeared. For (b_t=x(t,-3)),
\[
b_t=a_{t+1}\oplus(a_t\lor l_t),
\]
which yields
\[
b_{2n}=b_{2n+1}=1-u_{n+1}.
\]
Thus all columns reconstructed to the left are sliding Boolean transforms of
the single decimated sequence (u=(u_n)); alternating center data alone do
not force any of these columns to be periodic.

This identifies the exact obstruction to a Jen-style contradiction for period
2. To use the finite seed, one would need an independent theorem that the
right trace (r_t) (or its even subsequence (u_n)) cannot have the special
forms required by the actual right-expanding Rule 30 half. The left-zero tail
at time 0 imposes only finite initial conditions on these temporal traces and
does not, by itself, rule out arbitrary aperiodic (u). Bounded strip SCC
survivors are therefore consistent with this symbolic reconstruction.

For reference, this is just the iterated inverse update for the left-permutive
Rule 30 local rule; it is the same sideways mechanism used in Jen's width-2
theorem and Kopra's left-expansivity formulation.
