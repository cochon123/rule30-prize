# Period-2 \(L_0\): \(u_0\) is silent in \(F_k\) for \(k\ge 3\)

Checked lemma: on a phase-`01` period-2 centre, \(F_1=1+u_0\) and
\(F_2=u_0\), but \(F_k\) for every \(k\ge 3\) is independent of \(u_0\)
in the Fibonacci ring, and no \(G_k\) contains \(u_0\). Every onset
\(T\ge 3\) is unchanged by flipping \(u_0\). For odd \(T\), the
leading-variable identity forces the last prefix bit from
\(u_1,\ldots,u_{\mathrm{nvars}(T)-2}\). This tightens the free onset
data by one or two bits. It does **not** bound extra. Not a prize
claim.

Helper: `python3 research/period2_silent.py --certify`. Dump:
`research/period2_silent.json`. Variable bound as in
`research/period2_vacuum.md`; leading \(u_n\) as in
`research/period2_lead.md`; extra as in
`research/period2_alldesc.md`.

## Lemma (\(u_0\) silent)

Work in \(\mathcal B=\mathbb F_2[u_i]/\langle u_i^2+u_i,u_i u_{i+1}\rangle\).
The columns are \(F_1=1+u_0\), \(F_2=u_0\), \(G_0=G_1=1\), and
\[
F_k=G_{k-1}\oplus(F_{k-1}\lor F_{k-2}),\qquad
G_k=SF_{k-1}\oplus(G_{k-1}\lor G_{k-2}).
\]
The shift \(S\) sends \(u_i\mapsto u_{i+1}\) and never produces \(u_0\).

**Claim.** \(u_0\) is absent from every \(G_k\), and from \(F_k\) for
all \(k\ge 3\).

Proof. \(G_0\) and \(G_1\) are constants. \(G_2=SF_1\oplus 1=u_1\).
On the ring \(F_1\lor F_2=1\), so \(F_3=G_2\oplus 1=1+u_1\). Then
\(F_4=G_3\oplus(F_3\lor F_2)=0\) as in
`research/period2_left_edge.md`. For \(k\ge 3\), \(G_k\) is assembled
from \(SF_{k-1}\) and earlier \(G\); if \(k-1\ge 3\) then \(F_{k-1}\)
has no \(u_0\), and the remaining cases \(G_2,G_3\) were just checked.
For \(k\ge 5\), \(F_k\) is assembled from \(G_{k-1}\) and \(F_{k-1}\),
\(F_{k-2}\) with \(k-2\ge 3\), all free of \(u_0\).

Certified as reduced ANF through \(k=20\): \(G_k\) never contains
\(u_0\); \(F_k\) contains \(u_0\) only at \(k=1,2\); \(F_3=1+u_1\);
\(F_4=0\).

## Corollary (flip \(u_0\); odd \(T\) last bit)

If \(T\ge 3\) then \(F_T(u)=F_T(u\textrm{ with }u_0\textrm{ flipped})\).
If also \(T\ge 4\) then \(F_{T-1}\) is independent of \(u_0\), so the
onset kind (isolated vs bump) is unchanged. The Q-forced extra, clip
kind, and stop of a ugap onset are unchanged whenever the flipped
prefix remains ugap-legal.

For odd \(T\ge 3\) one has \(\mathrm{nvars}(T)=(T+1)/2\) and
\(2\mathrm{nvars}(T)-1=T\), so
\(F_T=u_{n_0-1}\oplus Q_{n_0-1}\) with \(Q_{n_0-1}\) independent of
\(u_0\) and of \(u_{n_0-1}\). An onset \(F_T=1\) therefore forces
\[
u_{n_0-1}=1\oplus Q_{n_0-1}(u_1,\ldots,u_{n_0-2}).
\]
The free onset data at odd \(T\) are \(u_1,\ldots,u_{n_0-2}\): two
bits fewer than \(\mathrm{nvars}(T)\).

Certified on every ugap word of length \(\mathrm{nvars}(T)\) for
\(T\in[5,32]\), \(T\neq 4\): \(F_T\) agrees under flip of \(u_0\);
every legal flip of an onset preserves extra, kind, and stop; every
odd \(T\) onset class with fixed \(u_1,\ldots,u_{n_0-2}\) has a unique
last bit.

## What this does not do

Silent \(u_0\) does not make \(Q_n\) a sliding window:
\(\min\mathrm{index}(F_k)=1\) for many \(k\ge 3\), so \(u_1\) remains
visible. Extra \(\le 8\) is still a census. The \(T=20\) and \(T=37\)
extra-\(8\) families are \(u_0\)-triples of a common tail, not a
bound. Other periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~2s.

- Kill of period 2: no.
- \(u_0\) silent in \(F_k\) for \(k\ge 3\): yes.
- Odd \(T\) last prefix bit forced: yes.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_silent.md` (this note)
- `research/period2_silent.py` (`--certify`)
- `research/period2_silent.json` (dump)
