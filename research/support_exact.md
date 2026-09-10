# Exact Mahler-support computation

Let (b_j(t)=\binom tj\bmod2). Lucas' theorem gives

\[
b_i(t)b_j(t)=b_{i\,\mathrm{OR}\,j}(t),
\qquad
b_j(t+1)=b_j(t)+b_{j-1}(t).
\]

For the right-edge Rule-30 coordinate, write
\[
u(t,k)=\bigoplus_{j\in S_k}b_j(t).
\]
With (S_{-1}=\varnothing,S_0=\{0\}), solving the temporal finite-difference
identity for successive spatial columns gives the exact recurrence requested:
\[
S_k=\operatorname{Inc}\left(S_{k-1}\triangle S_{k-2}
 \triangle [S_{k-1}\star_{\rm OR}S_{k-2}]\right),
\]
where (operatorname{Inc}(A)=\{j+1:j\in A\}), and the OR-star is a
multiset product reduced mod 2. In code, this parity reduction is essential;
using a plain set of (i\lor j) gives wrong center bits from (n=6) onward.

The center is (u(n,n)), and (b_j(n)=1) exactly when (j\) is a bit-submask
of (n). Thus the exact test is
\[
c_n=\#\{j\in S_n:j\mathbin{\&}\neg n=0\}\pmod2.
\]
`support_exact.py` verifies this against packed Rule-30 evolution through
(n=35). Initial support sizes are:

```text
k       0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 ... 30
|S_k|   1 1 1 1 3 3 3 7 13 11 27 27 29 23 29 25 55 ... 1925
max j  0 1 1 2 4 7 8 16 25 32 58 63 63 63 63 64 128 ... 3843
```

The only general degree/index bound obtained immediately from the recurrence
is (\max S_k\le 2^k-1): if all earlier indices are below (2^{k-1}), their
OR is below (2^{k-1}), and `Inc` raises this below (2^k). This is crude;
the observed maxima are much smaller at many (k), but no invariant at
(2^m) or (2^m-1) follows. At powers of two, the center test simplifies to
the parity of whether (2^m\in S_{2^m}), since all other nonnegative
submasks are below (2^m). The computed values for (m=0,\ldots,5) are
(1,0,1,1,1,0), matching direct evolution.
