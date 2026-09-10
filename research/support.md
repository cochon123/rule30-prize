# Algebraic support notes for Rule 30

Use the right-edge coordinate \(u(t,k)=x(t,t-k)\). Then
\[
 u(t+1,k)=u(t,k)\oplus(u(t,k-1)\lor u(t,k-2)).
\]
Over (F_2), with (p\lor q=p+q+pq), this is
\[
u'_{k}=u_k+u_{k-1}+u_{k-2}+u_{k-1}u_{k-2}. 
\]
The center value at time \(t\) is \(u(t,t)\).

For arbitrary Boolean initial variables (X_i), let (S_{t,k}) be the set
of square-free monomials having coefficient 1 in the ANF of (u(t,k)). If
(A\star B=\{a\cup b:a\in A,b\in B\}), with multiplicities reduced mod 2,
then the exact support recurrence is
\[
S_{t+1,k}=S_{t,k}\triangle S_{t,k-1}\triangle S_{t,k-2}
             \triangle(S_{t,k-1}\star S_{t,k-2}).
\]
This is a valid finite algebraic representation, but support cardinalities
grow rapidly; cancellation in the symmetric differences is essential.

The linearized recurrence (dropping the product) has the exact Lucas form
\[
L_{t,k}=\bigoplus_{j\ge0}\binom{t}{j}X_{k-j},
\]
where (inom tj) is reduced mod 2, equivalently (j\) is a bit-submask of
(t). The nonlinear support term is therefore a convolution under union of
these Lucas supports, followed by repeated nonlinear corrections. There is no
justification for replacing (S) by (L) when evaluating the single seed.

Direct packed evaluation gives the following center bits at special indices
(index 0 is the initial central 1):
\[
 c_{2^m}: 1,0,1,1,1,0,1,1,1,\ldots\quad(m=0,1,2,3,4,5,6,7,8,\ldots),
\]
and
\[
 c_{2^m-1}:1,0,1,1,0,1,0,1,1,\ldots\quad(m=1,2,3,4,5,6,7,8,9,\ldots).
\]
These short lists show no invariant at powers of two; they are only checks,
not evidence of a formula.

Correction to the earlier linearized display: the linear Rule-30 recurrence
has generating polynomial \(L_t(z)=(1+z+z^2)^t\) over \(\mathbb F_2\), hence
trinomial coefficients modulo 2. The binomial/Lucas formula for \((1+z)^t\)
belongs to Rule 90 and should not be used for Rule 30.

The tempting claim that Lucas parity determines the Rule-30 center column is
false: it determines Rule 90/linearized behavior, whereas the (u_{k-1}u_{k-2})
term creates square-free union products at every step. Any proposed lifting
must explicitly control these products and their mod-2 cancellations.

Notation correction: throughout the preceding Lucas display, read the
coefficient as \(\binom{t}{j}\bmod 2\), with \(j\subseteq t\) bitwise. The
stray control characters in the earlier plain-text parenthesized notation are
only formatting artifacts and have no mathematical meaning.
