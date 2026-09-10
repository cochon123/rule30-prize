# Stern–Brocot coordinates of packed rows

Attack on prize problem 3 via an injective rational encoding of each
finite row, as proposed in [_astra_ideas5.md](_astra_ideas5.md) item 1.
No birational recurrence in the preregistered family exists. This is not
a prize claim.

Helper: `python3 research/stern_brocot.py`. Dump:
`research/stern_brocot.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

Degree was frozen before fitting. The family was **not** enlarged after
the kernel came out trivial.

## Encoding

Write \(v(t,k)=x(t,t-k)\) for the right-edge coordinates, so \(v(t,0)\) is
the right edge, \(v(t,t)=c_t\), and \(v(t,2t)\) is the left edge. Pack the
row from that right edge as the word \(w_t=b_0\cdots b_{2t}\) of length
\(2t+1\), with \(b_k=v(t,k)\). The middle letter is \(c_t=b_t\).

On the single-cell seed the right-edge packed integer obeys
\(u\mapsto u\oplus((u\ll 1)\lor(u\ll 2))\) with \(u_0=1\). This matches
the left-packed generator of `experiment.py` after reversing each row.
Checked on the first 64 rows.

Stern–Brocot matrices and the fractional-linear encoding are

\[
L=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
R=\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad
M_0=L,\quad M_1=R,
\]
\[
q_t=(M_{b_0}\cdots M_{b_{2t}})\cdot 1
=\frac{a+b}{c+d}
\quad\text{if}\quad
M_{b_0}\cdots M_{b_{2t}}=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]

Leftmost peeling recovers the word: \(L\cdot z=z+1>1\) and
\(R\cdot z=z/(z+1)<1\), so the first letter is \(0\) iff \(q_t>1\). On
this seed the right edge is identically \(1\), hence \(b_0=1\) and
\(q_t<1\) for every computed \(t\). After \(t\) peels the next letter is
\(c_t\). Round-trip encode/decode succeeded for all \(256\) words
\(t=0,\ldots,255\); the \(256\) values \(q_t\) are pairwise distinct, so
the encoding is injective on the tested prefix.

Samples (exact):

| \(t\) | \(q_t\) | \(c_t\) | height in bits |
| --- | --- | --- | --- |
| 0 | \(1/2\) | 1 | 2 |
| 1 | \(1/4\) | 1 | 3 |
| 2 | \(7/10\) | 0 | 4 |
| 3 | \(4/19\) | 1 | 5 |
| 63 | \(121849529398046108651/1899025686180956133370\) | 1 | 71 |
| 255 | (see json) | 1 | 289 |

The \(t=2\) word is \(10011\) from the right, i.e. spacetime \(11001\)
left-to-right; the product \(RLLRR\) gives \(7/10\) by hand.

## Preregistered family

The speculation was a bidegree-\(\le(2,2)\) recurrence

\[
q_{t+1}=\frac{P(q_t,q_{t-1})}{Q(q_t,q_{t-1})},\qquad
P,Q\in\mathbb Q[x,y],\quad \deg_x,\deg_y\le 2.
\]

Nine monomials \(x^i y^j\) for \(0\le i,j\le 2\) for each of \(P\) and
\(Q\) give \(18\) unknown coefficients. Clearing the denominator produces
the homogeneous linear equation

\[
Q(q_t,q_{t-1})\,q_{t+1}-P(q_t,q_{t-1})=0.
\]

Fit: all triples \((q_{t-1},q_t,q_{t+1})\) whose three indices lie in
\(\{0,\ldots,63\}\), i.e. \(t=1,\ldots,62\) (\(62\) equations). Kernel
over \(\mathbb Q\) by exact RREF. Rejection rules, applied had the kernel
been nontrivial:

- \(P\equiv 0\) or \(Q\equiv 0\) as polynomials (including the zero
  vector);
- \(Q(q_t,q_{t-1})=0\) at a training (or later test) pair;
- the identity failing to reproduce \(q_{t+1}\) at a training pair.

Survivors, if any, were to be tested on every triple through row \(255\).
Degree was not increased. No extra lag \(q_{t-2}\) was added.

A self-check of the same solver on the Fibonacci sequence
\(q_{n+1}=q_n+q_{n-1}\) returns a kernel containing \(P=x+y\), \(Q=1\),
together with polynomial multiples that the \((2,2)\) box can still
represent. The pipeline therefore detects a genuine member of the family
when one exists.

## Result: empty kernel on the training rows

On the Rule 30 coordinates the \(62\times 18\) matrix over \(\mathbb Q\)
has **rank \(18\)** and **kernel dimension \(0\)**. The only solution is
\(P=Q=0\), which is degenerate. There is no candidate to promote to the
withheld rows \(64,\ldots,255\).

So the withheld-row test is vacuous: nothing in the fixed family even
interpolates rows \(0\) through \(63\). In particular no QRT-style
biquadratic relation of this shape holds on the prefix. The kill
criterion is met, and more strongly than by a training fit that later
breaks.

## It would not have been a cheaper \(c_n\) anyway

The encoding is injective, so \(c_n\) is a function of \(q_n\): peel \(n\)
leftmost letters. That extraction was checked at
\(n\in\{8,16,32,63,127,255\}\). It uses \(n\) exact inverse Möbius steps
on a rational whose height is already \(\Theta(n)\) bits (\(289\) bits at
\(n=255\); Stern–Brocot numerators at depth \(2n+1\) are at most
\(\sim\varphi^{2n}\)).

A surviving recurrence would still have to be iterated \(n\) times from
\((q_0,q_1)\). Each step is a constant number of arithmetic operations on
\(\Theta(n)\)-bit integers, hence \(\Omega(n^2)\) bit operations with
schoolbook arithmetic, the same order as the packed spacetime simulation.
Producing \(q_n\) by multiplying the \(2n+1\) matrices along the packed
word *is* that simulation plus \(O(n)\) integer \(2\times 2\) products.
There is therefore no route in this family to an exact \(c_n\) whose bit
complexity is \(o(n^2)\), and none that meets the prize’s \(O(n)\)
machine bound. No survivor appeared, so this paragraph is only a
complexity remark, not a second experiment.

## Why it died

The attack asked whether an injective rational reading of the row could
obey a small closed-form recurrence even though the binary words do not
simplify. Inside the frozen box of bidegree at most \((2,2)\) in the last
two coordinates, the homogeneous system on rows \(0\)–\(63\) is already
full rank. There is no valid rational recurrence in the family, hence
none that survives rows \(64\)–\(255\).

Files: `research/stern_brocot.py`, `research/stern_brocot.json`,
`research/stern_brocot.md`.
