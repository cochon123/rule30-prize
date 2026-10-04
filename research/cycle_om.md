# Cycle OM: one third off the right-diagonal period

Cycle OL bounds the period of the right diagonal \(u(t,q)\) by \(2^q\).
The forcing that feeds diagonal \(q\) is already periodic of period
dividing \(2^{q-2}\) once \(q\ge 3\), so the integrator only doubles
once and the period divides \(2^{q-1}\). That extra halving repeats.
For every \(r\ge 0\) and every \(q\ge 3r+2\),

\[
t\mapsto u(t,q)
\quad\text{has period dividing}\quad
2^{q-1-r}.
\]

The largest admissible \(r\) is \(\lfloor(q-2)/3\rfloor\), so for
\(q\ge 2\)

\[
\text{period divides}\quad
2^{\gamma(q)},
\qquad
\gamma(q)=q-1-\left\lfloor\frac{q-2}{3}\right\rfloor,
\]

with \(\gamma(0)=0\) and \(\gamma(1)=1\). About one third of the
exponent in the Cycle OL bound is removed. On \(q<22\) the bound
meets the minimal exponent for every \(q\le 9\), and it is already
strict at \(q=10\) (minimal exponent \(6\), bound \(7\)). Diagonal
\(4\) still has \(u(4,4)=1\), so the period does not divide
\(4=2^{q-2}\).

On the dyadic annulus the same cone argument as Cycle OL now silences
every adjacent AND whose depth \(s\) satisfies
\(\gamma(s+1)\le k-1\). That is \(s-\lfloor(s-1)/3\rfloor\le k-1\),
about \(\tfrac32 k\) rather than \(k-2\). Depths \(s\le k\) collapse
completely: the only nonzero contributions to \(I_k\) in that range
are the two Cycle OL hits \((k,s)=(1,0)\) and \((2,2)\).

\(I_k=1\) infinitely often stays open. The first unsilenced offset is
still \(O(k)\) cells in from the right edge of a row of width \(2^k\).
Not a prize claim. Do not walk \(k=12\) \(T\)-bands. Do not treat a
wider empirical margin as a theorem.

Certify: `python3 research/cycle_om.py --certify` (~0.27s). Dump:
`research/cycle_om.json`. Packed centre matches
`experiment.center_bits` on 20 bits. The exponent is checked for
\(q<22\) on \(t<2^{16}\). The margin is checked for \(k\le 12\),
\(s\le 20\).

## Lemma (period divides \(2^{q-1}\) for \(q\ge 2\))

Depths \(0\) and \(1\) are the constant \(1\) and \(t\bmod 2\). Depth
\(2\) is \(t\bmod 2\), so its period divides \(2^{1}\) and
\(u(2,2)=0\). These are the Cycle OL closed forms.

Take \(q\ge 3\) and assume the claim at every depth in
\(\{2,\ldots,q-1\}\). Then \(u(\cdot,q-1)\) has period dividing
\(2^{q-2}\). The depth \(q-2\) has period dividing \(2^{q-2}\) as
well: the inductive bound if \(q-2\ge 2\), the closed form
\(t\bmod 2\) if \(q-2=1\), and the constant \(1\) if \(q-2=0\). The
forcing \(\varphi_q(t)=u(t,q-1)\lor u(t,q-2)\) therefore has period
dividing \(Q=2^{q-2}\). Any window of length \(Q\) has the same XOR
\(\sigma\), so

\[
u(t+Q,q)=u(t,q)\oplus\sigma
\]

for every \(t\ge 0\). Hence \(u(t+2Q,q)=u(t,q)\). The period divides
\(2^{q-1}\). There is no preperiod: the identity is the partial-sum
relation and it holds at \(t=0\). In particular
\(u(2^{q-1},q)=u(0,q)=0\).

## Lemma (the saving repeats)

Write level \(r\) for the statement: for every \(q\ge 3r+2\), the map
\(t\mapsto u(t,q)\) has period dividing \(2^{q-1-r}\). Level \(0\) is
the previous lemma. Level \(r\) for every \(r\ge 0\) is the formula
for \(\gamma\).

Fix \(r\ge 0\) and assume levels \(0,\ldots,r\) are known. The next
level starts at \(q_*=3r+5\). Set \(S=2^{2r+3}\) and \(H=S/2\), and
write \(A(t)=u(t,3r+4)\), \(B(t)=u(t,3r+3)\).

Level \(r\) gives \(A\) period dividing \(S\) and \(B\) period dividing
\(H\). The forcing of \(A\) reads diagonals \(3r+3\) and \(3r+2\),
both of which have period dividing \(H\) by level \(r\), so

\[
A(t+H)=A(t)\oplus\rho,
\qquad
\rho=u(H,3r+4),
\]

for every \(t\), while \(B(t+H)=B(t)\). The forcing \(\varphi\) of
diagonal \(q_*\) therefore has period dividing \(S\), and

\[
u(t+S,q_*)=u(t,q_*)\oplus\sigma
\]

with the same \(\sigma=u(S,q_*)\) for every \(t\). The two halves of
that window differ by

\[
\delta(t)=(A(t)\lor B(t))\oplus\bigl((A(t)\oplus\rho)\lor B(t)\bigr).
\]

If \(\rho=0\) then \(\delta=0\). If \(\rho=1\) the four Boolean rows
give \(\delta(t)=\lnot B(t)\). Since \(H\) is even,

\[
\sigma=\bigoplus_{t<H}B(t).
\]

That sum is itself an integrator parity. Let \(m=3r+3\) and
\(Q=2^{2r+1}\), so the window has length \(2Q\). The forcing of
diagonal \(m\) has period dividing \(Q\): its inputs are diagonal
\(3r+2\), which level \(r\) bounds by \(2^{2r+1}\), and diagonal
\(3r+1\). For \(r=0\) that lower diagonal is \(u(t,1)=t\bmod 2\),
period \(2=Q\). For \(r\ge 1\) level \(r-1\) applies, because
\(3r+1\ge 3(r-1)+2\), and the resulting exponent is again \(2r+1\).
Let \(v(t)=u(t,m)\) and let \(\tau\) be the XOR of one forcing period.
Then \(v(t+Q)=v(t)\oplus\tau\), so

\[
\bigoplus_{t<2Q}v(t)
=\bigoplus_{t<Q}\tau
=0
\]

because \(Q\) is even. Thus \(\sigma=0\) in both cases, and diagonal
\(q_*\) has period dividing \(S=2^{(q_*)-1-(r+1)}\). Level \(r+1\)
holds at its first index.

For the later indices, take \(q>q_*\) and assume level \(r+1\) at
\(q-1\). Diagonal \(q-1\) then has period dividing
\(2^{q-r-3}\). Diagonal \(q-2\) is at least \(3r+4\), so level \(r\)
bounds it by the same power. The forcing of diagonal \(q\) has period
dividing \(S/2\) with \(S=2^{q-r-2}\), and two identical blocks cancel,
so the period divides \(S\). Level \(r+1\) follows for every
\(q\ge 3r+5\).

Checked: every \(q<22\) satisfies \(u(t+2^{\gamma(q)},q)=u(t,q)\) on
\(t<2^{16}\), and each ladder base with \(2r+3\le 16\) is the bit
\(0\). The Boolean identity and the even-window integrator parity are
checked directly.

## Lemma (margin about \(\tfrac32 k\))

Fix \(s\ge 1\) and \(k\ge 1\) with \(\gamma(s+1)\le k-1\). Let
\(T=2^{k-1}\). As in Cycle OL, the adjacent AND of diagonals \(s\)
and \(s+1\) can meet \(I_k\) only at times \(t=T+j\) with
\(0\le j\le\lfloor s/2\rfloor\): the Green degree
\(s-2(t-T)\) is negative past that point.

\(\gamma\) is non-decreasing for \(q\ge 2\), and \(\gamma(s)\le\gamma(s+1)\),
so both diagonals have period dividing \(2^{k-1}\). Pure periodicity
from time \(0\) gives \(u(T+j,s+1)=u(j,s+1)\). But \(s+1>2j\), so
that cell lies strictly outside the left edge and is \(0\). The AND
is dead, and the contribution is \(0\).

The inequality \(\gamma(s+1)\le k-1\) is
\(s-\lfloor(s-1)/3\rfloor\le k-1\). For large \(k\) it allows depths
up to about \(\tfrac32 k\). Cycle OL's hypothesis was the stronger
\(k\ge s+2\), i.e. only depths \(s\le k-2\). Pairs with
\(k<s+2\) that this lemma still kills are present in the scan
(\(k\le 12\), \(s\le 20\)).

## Lemma (depths \(s\le k\) have only two hits)

The contribution of depth \(s\) to \(I_k\) is \(0\) for every pair with
\(s\le k\), except \((k,s)=(1,0)\) and \((2,2)\), where it is \(1\).

Depth \(0\) hits if and only if \(k=1\), and depths \(1\) and \(2\) are
the Cycle OL arithmetic: depth \(1\) never hits, depth \(2\) hits if
and only if \(k=2\).

For \(1\le s\le k-1\), \(\gamma(s+1)=s-\lfloor(s-1)/3\rfloor\le s\le k-1\),
so the margin applies.

For \(s=k\ge 2\), level \(0\) gives diagonal \(k\) period dividing
\(T\), hence \(u(T+j,k)=u(j,k)\). If \(k\) is odd then \(k>2j\)
throughout the surviving range, so the AND is dead. If \(k\) is even
the only surviving cell with diagonal \(k\) nonzero is \(j=k/2\),
where that diagonal is the left edge and equals \(1\). The Green
degree there is \(0\), so \(G=1\), and the contribution equals the
single bit \(u(T+k/2,\,k+1)\). Level \(0\) supplies
\(u(T+j,k+1)=u(j,k+1)\oplus u(T,k+1)\). The cone term \(u(j,k+1)\)
is \(0\) because \(k+1>k=2j\). The remaining bit is
\(u(2^{k-1},k+1)\), which level \(1\) kills for \(k+1\ge 5\), i.e.
for every even \(k\ge 4\). The case \(k=2\) is the depth-\(2\) hit.

Checked against the packed Green sum for every \(s\le k\le 12\).

## What still speaks

The margin stops once \(\gamma(s+1)>k-1\). Depth \(s=k+1\) is already
past that line for small \(k\), and it fires: \((k,s)=(3,4)\) and
\((5,6)\) both contribute \(1\). Offsets that survive are still
\(O(k)\) cells in from the right edge. The centre-right AND is
untouched. \(I_k=1\) infinitely often is open.

## Verdict

`LEMMA` (period divides \(2^{q-1}\) for \(q\ge 2\); the one-third
saving \(\gamma(q)\); margin \(s-\lfloor(s-1)/3\rfloor\le k-1\);
depths \(s\le k\) contribute only at \((1,0)\) and \((2,2)\)).
`OPEN` (\(I_k=1\) infinitely often).
Prize unsolved.

## Files

- `research/cycle_om.md` (this note)
- `research/cycle_om.py`
- `research/cycle_om.json`
- `research/cycle_ol.md` (period \(2^q\) and the cone argument)
- `research/cycle_aa.md` (which ANDs enter \(I_k\))
