# Period-2 \(L_0\): deep-tail shift of \(Q_n\)

Checked lemma: on a phase-`01` period-2 centre, three consecutive zeros
\(F_{2n-1}=F_{2n-2}=F_{2n-3}=0\) skip two columns under the Fibonacci
shift,
\[
F_{2n+1}(u)=F_{2n-1}(Su).
\]
The leading-variable identity of `research/period2_lead.md` then gives
\(Q_n(u)=Q_{n-1}(Su)\) as values. An \(L_0\) tail of width \(T\) forces
this for every \(n\) with \(2n-3>T\), so the unique continuation is
\(u_n=Q_{n-1}(Su)\). Four consecutive zeros give the even companion
\(F_{2n}(u)=F_{2n-2}(Su)\). This is the second step of tail-forcing. It
does **not** exclude eventual period 2: \(Q_n\) is still not a
\(T\)-independent sliding window, and iterating a fixed \(Q_{n_0}\)
along \(S\) fails because \(Su\) is a bump, not \(L_0\). Not a prize
claim.

Helper: `python3 research/period2_qshift.py --certify`. Dump:
`research/period2_qshift.json`. Notation as in
`research/period2_lead.md` and `research/period2_germ.md`. Does not
modify those files' certificates.

## Lemma (three-zero odd skip)

Work on any \(u\) for which the spatial identity
\(G_k=F_{k+1}\oplus(F_k\lor F_{k-1})\) (\(k\ge 1\)) and the fold
\(G_k(u)=F_{k-1}(Su)\oplus(G_{k-1}\lor G_{k-2})\) hold. Fix \(n\ge 2\)
with \(F_{2n-1}=F_{2n-2}=F_{2n-3}=0\). Spatial reconstruction gives
\[
G_{2n-2}=0,\qquad G_{2n-1}=F_{2n}.
\]
Fold at \(2n\) then spatial at \(2n\):
\begin{align*}
G_{2n}
&=F_{2n-1}(Su)\oplus(F_{2n}\lor 0)
=F_{2n-1}(Su)\oplus F_{2n},\\
F_{2n+1}
&=G_{2n}\oplus(F_{2n}\lor 0)
=F_{2n-1}(Su).
\end{align*}
The even column \(F_{2n}\) cancels; it is not needed as a hypothesis.
`research/period2_lead.md` writes \(F_{2n+1}=u_n\oplus Q_n\) and
\(F_{2n-1}(Su)=u_n\oplus Q_{n-1}(Su)\), hence \(Q_n(u)=Q_{n-1}(Su)\).

## Lemma (four-zero even skip)

If also \(F_{2n-4}=0\), fold at \(2n-1\) gives
\(G_{2n-1}=F_{2n-2}(Su)\) (the two neighbouring \(G\) vanish), and
spatial at \(2n-1\) with the two odd/even zeros already in the
three-zero hypothesis yields \(F_{2n}(u)=F_{2n-2}(Su)\).

## Corollary (\(L_0\) deep tail)

If \(F_T=1\) and \(F_k=0\) for all \(k>T\), then for every
\(n>(T+3)/2\) one has \(2n-3>T\), hence \(u_n=Q_{n-1}(Su)\). The
one-step identity does **not** iterate to a sliding evaluation of a
fixed \(Q_{n_0}\): \(Su\) is the length-2 bump of
`research/period2_germ.md`, not an \(L_0\), so
\(Q_n(u)=Q_{n_0}(S^{n-n_0}u)\) fails.

## Checks

- Every Fibonacci word of length 12, every \(n\ge 2\) with the three
  (resp. four) zeros: odd skip and \(Q_n=Q_{n-1}(Su)\); even skip.
- Last-sat models of
  \((T,R)\in\{(8,9),(15,6),(16,9),(20,16),(22,12),(26,5)\}\): deep-tail
  \(Q\) identity on every odd index with \(2n-3>T\); the unique
  \(Q\)-forced continuation leaves the ugap SFT (`11` or `00000`) or
  fires an even \(F_{2n}>T\).
- \(T=20\): all six last-sat words 11-clip at \(n=18\)
  (\(u_{17}=1\), \(Q_{18}=1\)). The \(F_{37}\) of the bounded-\(nvars\)
  scan is the padding-zero artifact of refusing that clip. Sliding
  \(Q_{11}\) along the word fails at four of the six deep indices.

## What this does not do

A uniform \(R(T)\) would still need a \(T\)-independent reason that the
forced continuation 11-clips, 00000-clips, or fires an even column
inside a bounded window. The one-step identity \(Q_n=Q_{n-1}\circ S\)
is that reason's second step, not the bound. Window-of-\(w\le 8\)
locality of \(Q_n\) already fails on the \(T=20\) last-sat words
(`research/period2_lead.md`). Finite extra zeros of the 11-bump do
descend under \(S\) (`research/period2_b0.md`); an infinite \(L_0\)
tail does not.

The three ugap-legal \(T=20\) last-sat words still 11-clip at \(n=18\)
with extra \(8\) (`research/period2_ugap_sat.md`).

Periodic \(u\) is already infinite on the left
(`research/period2_periodic.md`). Aperiodic \(u\) remains the
obstruction to period 2.

## Verdict

`LEMMA`, wall time <2s.

- Kill of period 2: no.
- Deep-tail \(Q_n=Q_{n-1}(Su)\): yes.
- Uniform \(R\): no.

## Files

- `research/period2_qshift.md` (this note)
- `research/period2_qshift.py` (`--certify`)
- `research/period2_qshift.json` (dump)
- `research/period2_ugap_sat.md` (ugap last-sat Q-force)
- `research/period2_qextra.md` (clip-to-\(R\); \(T=37\) has \(R=17\))
