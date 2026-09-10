# Constant-tail exclusion for the Rule 30 center column

Use
\[
x_{t+1,j}=x_{t,j-1}\oplus(x_{t,j}\lor x_{t,j+1}),
\qquad c_t=x_{t,0},\ l_t=x_{t,-1},\ r_t=x_{t,1}.
\]

## Eventually one

If (c_t=1) for every (t\ge T), then
\[
1=l_t\oplus(1\lor r_t)=l_t\oplus1,
\]
so (l_t=0) for all (t\ge T). Columns (-1) and (0) are then both
eventually periodic, contradicting Jen's width-2 aperiodicity theorem for
Rule 30 from a nonzero finite seed (Kopra 2023, Corollary 3.7). Hence the
center has infinitely many zeros.

## Eventually zero: repaired argument

If (c_t=0) for every (t\ge T), the center equation gives
\[
l_t=r_t=:d_t.
\]
Now update the right neighbor. Since (c_t=0),
\[
d_{t+1}=r_{t+1}=c_t\oplus(r_t\lor x_{t,2})
                 =d_t\lor x_{t,2}.
\]
Therefore (d_{t+1}\ge d_t) in the binary order: (d_t) is a
nondecreasing binary sequence and must become constant after at most one
change. Consequently both columns (-1) and (0) are eventually constant
(indeed (l_t=d_t) and (c_t=0)), contradicting Jen/Kopra's width-2 theorem.

Thus the center is neither eventually all 1 nor eventually all 0. Equivalently,
it contains infinitely many 0s and infinitely many 1s. This still does not
exclude a nonconstant eventual period (p>1).

The width-2 theorem used here is stated in Kopra, “Rapid left expansivity, a
commonality between Wolfram's Rule 30 and powers of (p/q),” TCS 946 (2023),
Theorem 3.5 / Corollary 3.7:
https://www.utupub.fi/server/api/core/bitstreams/eeb04919-9fa7-443b-998f-032fab664a41/content
