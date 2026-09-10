# Truncated exact support and OR convolution

The support recurrence never lowers an index: `Inc` raises by one and
bitwise-OR is at least each operand. Therefore, while computing (S_0,ldots,S_N),
all indices (>N) may be discarded permanently; they cannot contribute to a
center term (j\subseteq N). The elementary lower bound is
\[
\min S_k\ge1+\min(\min S_{k-1},\min S_{k-2})=\lceil k/2\rceil,
\]
starting from (S_{-1}=\varnothing,S_0=\{0\}); symmetric-difference
cancellation can only increase the minimum.

For indicators on the (q)-bit Boolean lattice, OR-convolution is computed
exactly by the subset zeta transform: (Z_A(s)=\bigoplus_{i\subseteq s}A(i)),
then (Z_{A\star_{OR}B}=Z_A Z_B) pointwise, and the same zeta transform
inverts it over \(\mathbb F_2\). `support_fast.py` uses this plus the index
truncation and verifies every center bit through (N=512) against direct packed
Rule-30 evolution.

For (n>0), every contributing (j\subseteq n) satisfies (j\le n), and
the lower bound (j\ge\lceil n/2\rceil) forces the highest bit of (n) to
occur in (j): a submask omitting that bit is at most
(2^{\lfloor\log_2n\rfloor}-1<n/2). This trims the final parity scan to
top-bit-carrying supports, but does not itself yield a recurrence, since OR
products and `Inc` can move support across the top-bit boundary.
