# Period-2 \(L_0\): \(u_1\) is silent in \(G_k\) for \(k\ge 8\)

Checked lemma: on a phase-`01` period-2 centre, silent \(u_0\) keeps
\(u_1\) out of every \(SF_{k-1}\) for \(k\ge 4\). The remaining OR in
the fold then dies: \(G_6\lor G_7=1\) on the Fibonacci ring, so
\(G_8=u_3+u_4\), and \(G_7\lor G_8=1\), so \(G_9=1+u_2 u_4\). Hence
\(G_k\) is independent of \(u_1\) for every \(k\ge 8\). \(F_k\) still
sees \(u_1\) (\(F_8=u_1 u_3\)), so \(Q_n\) is not a sliding window
and extra is not invariant under flipping \(u_1\). Not a prize claim.

Helper: `python3 research/period2_gsilent.py --certify`. Dump:
`research/period2_gsilent.json`. Silent \(u_0\) as in
`research/period2_silent.md`; variable bound as in
`research/period2_vacuum.md`.

## Lemma (\(u_1\) silent in \(G_k\), \(k\ge 8\))

Work in \(\mathcal B=\mathbb F_2[u_i]/\langle u_i^2+u_i,u_i u_{i+1}\rangle\).
The fold is \(G_k=SF_{k-1}\oplus(G_{k-1}\lor G_{k-2})\). Silent \(u_0\)
says \(F_j\) has no \(u_0\) for \(j\ge 3\), so \(SF_{k-1}\) has no
\(u_1\) for \(k\ge 4\). For those \(k\), any \(u_1\) in \(G_k\) must
come from the OR.

The small columns are \(F_7=1+u_2+u_3\), \(F_8=u_1 u_3\),
\(G_6=u_1+u_2+u_3\), \(G_7=1+u_3+u_1 u_3\). Then
\(SF_7=1+u_3+u_4\). Expanding the OR on the ring,
\[
G_6\lor G_7
=1+u_2 u_3+u_1 u_2 u_3
=1,
\]
because \(u_2 u_3=u_1 u_2=0\). Hence
\[
G_8=SF_7\oplus 1=u_3+u_4.
\]
The next OR is \(G_7\lor G_8=1+u_3 u_4+u_1 u_3 u_4=1\), and
\(SF_8=u_2 u_4\), so
\[
G_9=SF_8\oplus 1=1+u_2 u_4.
\]
Neither \(G_8\) nor \(G_9\) contains \(u_1\). For \(k\ge 10\),
\(SF_{k-1}\) has no \(u_1\) and both previous \(G\) have no \(u_1\)
by induction.

Certified as reduced ANF through \(k=20\): \(G_7\) still contains
\(u_1\); \(G_k\) for \(k\ge 8\) does not; \(G_6\lor G_7=G_7\lor G_8=1\);
\(G_8=u_3+u_4\); \(G_9=1+u_2 u_4\); \(F_8=u_1 u_3\).

## Corollary (flip \(u_1\) on odd columns)

If \(k\ge 8\) then \(G_k(u)=G_k(u\textrm{ with }u_1\textrm{ flipped})\)
whenever the flipped word remains Fibonacci-legal. Spatial
reconstruction \(G_k=F_{k+1}\oplus(F_k\lor F_{k-1})\) is therefore
independent of \(u_1\) for those \(k\). Certified on every ugap word
of length 8, every \(k\in[8,16]\).

## What this does not do

Silent \(u_1\) in \(G\) does not make \(u_1\) silent in \(F\):
\(\min\mathrm{index}(F_k)=1\) for every \(k\ge 8\) except \(k=10\),
and \(F_8=u_1 u_3\). Extra, kind, and stop of a ugap onset are not
invariant under flipping \(u_1\) (mismatch already at \(T=5\) and
\(T=8\)). Every such \(u_1\) in \(F_k\) for \(k\ge 8\) is a multiple
of \(u_3\) (`research/period2_u1u3.md`). The shift of that
factorisation puts \(u_2\) in \(G_k\) only with \(u_4\)
(`research/period2_gu2u4.md`). \(Q_n\) still sees \(u_1\)
on \(u_3=1\). Uniform extra \(\le 8\) is still a census.

## Verdict

`LEMMA`, wall time ~0.2s.

- Kill of period 2: no.
- \(u_1\) silent in \(G_k\) for \(k\ge 8\): yes.
- \(u_1\) silent in \(F_k\): no.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_gsilent.md` (this note)
- `research/period2_gsilent.py` (`--certify`)
- `research/period2_gsilent.json` (dump)
- `research/period2_silent.md` (\(u_0\) silent in \(F_k\) for \(k\ge 3\))
- `research/period2_u1u3.md` (\(u_1\) in \(F_k\) factors through \(u_3\) for \(k\ge 8\))
- `research/period2_gu2u4.md` (\(u_2\) in \(G_k\) factors through \(u_4\) for \(k\ge 9\))
