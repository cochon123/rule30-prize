# Cycle OL: fixed-depth right-edge ANDs are silent in \(I_k\)

Right diagonals \(u(t,q)=x(t,t-q)\) are purely periodic of period
dividing \(2^q\). On a dyadic annulus the adjacent AND of diagonals
\(s\) and \(s+1\) can reach \(I_k\) only at the opening times
\(t=2^{k-1}+j\) with \(j\le\lfloor s/2\rfloor\). For every \(k\ge s+2\) those times
reduce to a left-cone zero, so the AND contributes nothing.

Pairs at depth \(s\le 2\) are settled for every \(k\), not only for
large \(k\): depth 0 hits if and only if \(k=1\), depth 1 never hits,
depth 2 hits if and only if \(k=2\). Depth 3 is silent for every
\(k\le 12\), hence for every \(k\), because \(k\ge 5\) is the margin
lemma and \(k\le 4\) is a finite check.

The first offset the period bound does not kill is \(s=k-1\). That
index still moves only logarithmically in from the right edge. No
stronger margin is claimed. \(I_k=1\) infinitely often stays open.
Not a prize claim. Do not walk \(k=12\) \(T\)-bands. Do not treat a
wider empirical margin as a theorem.

Certify: `python3 research/cycle_ol.py --certify` (~0.04s). Dump:
`research/cycle_ol.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Integrator triangle matches
packed diagonals. Period bound checked for \(q<12\) on
\(t<2^{14}\). Margin checked for \(k\le 12\), \(s\le 10\).

## Lemma (right diagonals, all \(t\))

Packed bit \(b\) at time \(t\) is spatial \(b-t\), so
\(u(t,q)\) is bit \(2t-q\). The update
\(x(t+1,j)=x(t,j-1)\oplus(x(t,j)\lor x(t,j+1))\) rewrites as

\[
u(t+1,q)=u(t,q)\oplus\bigl(u(t,q-1)\lor u(t,q-2)\bigr),
\]

with \(u(t,q)=0\) for \(q<0\). The right edge is \(u(t,0)=1\): it
holds at \(t=0\), and the two cells to its right are outside the
cone, so the edge is copied. The left edge \(x(t,-t)\) is packed
bit 0 and is likewise 1 for every \(t\) (Cycle AA; rechecked on
\(t<4096\)).

Forcing \(\varphi_q(t)=u(t,q-1)\lor u(t,q-2)\) and \(u(0,q)=0\) for
\(q>0\) give \(u(t,q)=\bigoplus_{s<t}\varphi_q(s)\).

## Lemma (closed forms through depth 4)

\[
\begin{align*}
u(t,1)&=t\bmod 2,\\
u(t,2)&=t\bmod 2,\\
u(t,3)&=\lfloor t/2\rfloor\bmod 2,\\
u(t,4)&=\lfloor t/4\rfloor\bmod 2\;\oplus\;[t\equiv 2\pmod 4].
\end{align*}
\]

The first two forcings are identically 1, because each ORs against
the right edge. The third forcing is \(t\bmod 2\), and the partial
sum of that bit is \(\lfloor t/2\rfloor\bmod 2\). The fourth forcing
is 0 exactly on multiples of 4. Writing \(t=4q+r\), the number of
non-multiples in \([0,t)\) is \(3q\) plus \(0,0,1,2\) for
\(r=0,1,2,3\), so the parity is \(q\bmod 2\) plus 1 only when
\(r=2\). Checked against packed bits for \(t<4096\).

## Lemma (period divides \(2^q\))

The sequence \(t\mapsto u(t,q)\) is purely periodic of period dividing
\(2^q\), for every \(q\ge 0\).

Induction. Depth 0 is the constant 1, period \(2^0\). Negative depths
are the constant 0, period 1. Assume the claim for every depth less
than \(q\ge 1\). Then \(\varphi_q\) has period dividing
\(Q=2^{q-1}\). Let \(\sigma\) be the XOR of one such block. The
integrator shifts by exactly \(\sigma\) across each block, so
\(u(t+Q,q)=u(t,q)\oplus\sigma\). If \(\sigma=0\) the period divides
\(Q\). If \(\sigma=1\) then \(u(t+2Q,q)=u(t,q)\), and the period
divides \(2^q\). The identity holds at \(t=0\), so there is no
preperiod. Checked for \(q<12\) on \(t<2^{14}\).

## Lemma (margin: \(s\le k-2\) is silent)

Fix \(s\ge 0\) and \(k\ge s+2\). Let \(T=2^{k-1}\). The adjacent AND
of right-diagonals \(s\) and \(s+1\) is packed bit \(p=2t-s\) of
\((\mathrm{row}\ll 1)\land\mathrm{row}\) (Cycle AA): bit \(p\) is
diagonal \(s\) and bit \(p-1\) is diagonal \(s+1\). It contributes to
\(I_k\) only when \(t\in[T,2T)\) and
\(G(m,2T-p)=1\) with \(m=2T-1-t\).

The target degree is \(2T-p=s-2(t-T)\). It is negative once
\(t>T+\lfloor s/2\rfloor\), and then \(G=0\). The only surviving
times are \(t=T+j\) for \(0\le j\le\lfloor s/2\rfloor\).

Period of diagonal \(q\le s+1\) divides \(2^{s+1}\), and
\(k-1\ge s+1\) makes \(T\) a multiple of that period. Pure
periodicity gives \(u(T+j,s)=u(j,s)\) and
\(u(T+j,s+1)=u(j,s+1)\). But \(2j\le s\), so diagonal \(s+1\ge 2j+1\).
The cell \(u(j,2j+1)\) is strictly left of the left edge, hence 0.
The AND is dead at every time that could have hit, and the
contribution is 0.

Checked: every pair with \(k\le 12\), \(s\le 10\), and \(k\ge s+2\)
has Green parity 0 (\(n_{\mathrm{silent}}>0\)).

## Lemma (depths 0, 1, 2 for every \(k\))

These three do not use the period bound.

- Depth 0. Degree \(2(T-t)\) is nonnegative only at \(t=T\), where it
  is 0 and \(G=1\). The AND is the right edge with diagonal 1, hence
  live exactly when \(T\) is odd, i.e. only for \(k=1\).
- Depth 1. Degree \(2(T-t)+1\) survives only at \(t=T\). For \(k\ge 2\),
  \(T\) is even and both diagonals 1 and 2 are 0. For \(k=1\),
  \(m=0\) and the degree is 1, so \(G(0,1)=0\).
- Depth 2. The AND of diagonals 2 and 3 is live exactly when
  \(t\equiv 3\pmod 4\). The only candidate times in the annulus are
  \(t=T\) and, when it still lies in the annulus, \(t=T+1\). Neither
  is \(3\bmod 4\) except \(t=T+1\) at \(k=2\). There \(m=0\), the
  degree is 0, and \(G(0,0)=1\), so the pair contributes 1. For every
  other \(k\) the contribution is 0.

The arithmetic form agrees with the packed Green sum for \(k\le 12\),
and the same arithmetic is checked for \(k\le 64\).

## Lemma (depth 3 never hits)

For \(k\ge 5\) the margin lemma applies. For \(1\le k\le 4\) the
annulus is finite (length at most 8) and the packed Green sum is 0.
Together, diagonal pair \((3,4)\) contributes 0 to \(I_k\) for every
\(k\ge 1\).

## What still speaks

The argument stops at \(s=k-1\): the period of diagonal \(k\) may be
\(2^k\), which does not divide \(T=2^{k-1}\), so the reduction
\(u(T+j,k)=u(j,k)\) can fail. Empirically the first live offset on
\(k\le 12\) is often strictly larger than \(k-1\). That gap is not a
theorem. Offsets \(s\ge k-1\) remain able to carry \(I_k\). They sit
\(O(k)\) cells in from the right edge of a row of width \(2^k\), so
the centre and the bulk are untouched.

## Verdict

`LEMMA` (period divides \(2^q\); margin \(s\le k-2\) silent for
\(k\ge s+2\); closed forms through depth 4; depth 0 hits iff \(k=1\);
depth 1 never hits; depth 2 hits iff \(k=2\); depth 3 never hits).
`OPEN` (any margin past \(s=k-2\) for all \(k\); \(I_k=1\) infinitely
often).
Prize unsolved.

## Files

- `research/cycle_ol.md` (this note)
- `research/cycle_ol.py`
- `research/cycle_ol.json`
- `research/cycle_aa.md` (which ANDs enter \(I_k\))
- `research/cycle_ae.md` (right diagonals are integrators)
