# Cycle ON: the dyadic OR-sum telescopes to the centre

The sum

\[
\bigoplus_{J=1}^{T-1}\bigl(e_{2J+1}(T+J)\lor e_{2J+2}(T+J)\bigr),
\qquad T=2^{k-1},
\]

was checked for \(k\le 11\) and is not a formula for \(b_k\). It is
\(c_{2^k}\), by a cancellation already present in the diagonal
recurrence. Splitting the sum into periodic tails and a hard
transient does not remove that identity: the completed XOR is the
centre bit. Not a prize claim.

Helper: `python3 research/cycle_on.py --certify`. Dump:
`research/cycle_on.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (prefix telescope)

Write \(u(t,q)=x(t,t-q)\) for the right diagonal, \(u(t,q)=0\) when
\(q<0\), and \(u(t,0)=1\). The edge recurrence is

\[
u(t+1,q)=u(t,q)\oplus\bigl(u(t,q-1)\lor u(t,q-2)\bigr).
\]

For \(n\ge 1\) and \(q=n\),

\[
u(t,n-1)\lor u(t,n-2)=u(t+1,n)\oplus u(t,n).
\]

Summing \(t\) from \(0\) to \(n-1\) cancels every interior term:

\[
\bigoplus_{t<n}\bigl(u(t,n-1)\lor u(t,n-2)\bigr)
=u(n,n)\oplus u(0,n)=c_n,
\]

because \(u(0,n)=x(0,-n)=0\) for \(n>0\). This is the Mahler prefix
form of `mahler_dependency.md`, read off the recurrence instead of
the zeta transform. Certified for every \(n\le 512\), including the
light-cone vanishings \(u(t,q)=0\) for \(q>2t\).

## Lemma (dyadic endpoints)

Let \(n=2T\) with \(T=2^{k-1}\) and \(k\ge 2\). For \(t<T-1\) both
depths \(2T-1\) and \(2T-2\) lie outside the left light cone, so those
OR-terms are \(0\). At \(t=T-1\) the depth-\(2T-2\) cell is the left
edge, hence \(1\), and depth \(2T-1\) is still outside, so the OR is
\(1\). At \(t=T\) (the \(J=0\) term) the same cells are
\(e_1(T)=1\) and \(e_2(T)=0\), so the OR is again \(1\). The two
endpoint \(1\)s cancel, and

\[
c_{2T}
=\bigoplus_{J=1}^{T-1}\bigl(e_{2J+1}(T+J)\lor e_{2J+2}(T+J)\bigr).
\]

The same identity is the one-line reindexing
\(e_{2J+1}\lor e_{2J+2}=e_{2J+2}(\,\cdot\,+1)\oplus e_{2J}\), whose
interior terms cancel and leave \(e_{2T}(2T)\oplus e_2(T+1)\). Here
\(e_{2T}(2T)=c_{2T}\) and \(e_2\equiv 0\) for times \(\ge 2\).
Certified on every \(k\le 12\): both endpoints are \(1\), \(e_2(T)=0\),
and the \(J\)-sum equals \(b_k\). Wall time about \(0.03\)s.

## Killed as a compression

Evaluating the sum, in tails or in transients, evaluates \(c_{2^k}\).
A periodic formula for individual left diagonals does not collapse the
XOR unless it cancels inside the sum, and the only cancellation the
recurrence produces is the one that returns the centre. Rowland’s
Proposition 2 already allows the left-diagonal period to drop between
white stripes, and the column two steps after a white stripe is
eventually black; neither fact samples \(c_t=e_t(t)\) along the tail
(Cycle AC). No new value of \(I_k\) or of a centre `00` follows.

## Verdict

`LEMMA` (prefix telescope; dyadic endpoint cancellation). `KILLED`
(the \(J\)-sum as a formula for \(b_k\)). `OPEN` (\(I_k=1\) infinitely
often; \((b_k)\) not eventually periodic; infinitely many centre
`00`s). Prize unsolved.

## Files

- `research/cycle_on.md` (this note)
- `research/cycle_on.py`
- `research/cycle_on.json`
