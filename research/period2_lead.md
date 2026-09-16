# Period-2 \(L_0\): leading variable of \(F_{2n+1}\)

Checked lemma: on a phase-`01` period-2 centre,
\(F_{2n+1}=u_n\oplus Q_n(u_0,\ldots,u_{n-1})\) in the Fibonacci ring.
An \(L_0\) tail therefore forces a unique continuation of \(u\) past
`nvars(T)`. This is the algebraic engine of tail-forcing. It does
**not** exclude eventual period 2: the \(T=20\) last-sat words already
obey the forcing through \(n=17\) and die only at \(F_{37}\). Not a
prize claim.

Helper: `python3 research/period2_lead.py --certify`. Dump:
`research/period2_lead.json`. Variable bound as in
`research/period2_vacuum.md`; ANF as in
`research/period2_left_edge.md`. Does not modify those files.

## Lemma (leading \(u_n\))

Work in the Boolean Fibonacci ring
\(\mathcal B=\mathbb F_2[u_0,u_1,\ldots]/\langle u_i^2+u_i,\ u_i u_{i+1}\rangle\).
The column recurrences and the variable bound
\(\max\mathrm{index}(F_k)\le\lfloor(k-1)/2\rfloor\),
\(\max\mathrm{index}(G_k)\le\lfloor k/2\rfloor\) are
`research/period2_vacuum.md`. In particular \(u_n\) cannot appear in
\(F_0,\ldots,F_{2n}\) or in \(G_0,\ldots,G_{2n-1}\), and
`nvars(2n+1)=n+1`.

**Claim.** The coefficient of the monomial \(u_n\) in \(F_{2n+1}\) is
\(1\). Equivalently \(F_{2n+1}=u_n\oplus Q_n\) with \(Q_n\) independent
of \(u_n\). The same linear term is the unique \(u_n\) in \(G_{2n}\) for \(n\ge 1\)
(\(G_0=1\) has no \(u_0\)).

Proof by induction on \(n\). The case \(n=0\) is \(F_1=1+u_0\). Assume
the coefficient of \(u_{n-1}\) in \(F_{2n-1}\) is \(1\). Then

\[
F_{2n+1}=G_{2n}\oplus(F_{2n}\lor F_{2n-1}).
\]

Neither \(F_{2n}\) nor \(F_{2n-1}\) contains \(u_n\), so the
coefficient of \(u_n\) in \(F_{2n+1}\) equals that in \(G_{2n}\). For
\(n\ge 1\) the fold is

\[
G_{2n}=SF_{2n-1}\oplus(G_{2n-1}\lor G_{2n-2}).
\]

Neither \(G_{2n-1}\) nor \(G_{2n-2}\) contains \(u_n\). The shift sends
the monomial \(u_{n-1}\) to \(u_n\), and sends products to products, so
the linear coefficient of \(u_n\) in \(SF_{2n-1}\) is the linear
coefficient of \(u_{n-1}\) in \(F_{2n-1}\), which is \(1\). Reduction
modulo \(u_i u_{i+1}=0\) does not touch the square-free monomial
\(u_n\).

## Corollary (\(L_0\) tail forcing)

If \(F_T=1\) and \(F_k=0\) for all \(k>T\), then for every
\(n>\lfloor(T-1)/2\rfloor\) one has \(2n+1>T\), hence \(F_{2n+1}=0\),
hence \(u_n=Q_n(u_0,\ldots,u_{n-1})\). The bits of \(u\) past
`nvars(T)` are a deterministic function of the onset prefix.

Certified: the six last-sat words of \(T=20\), \(R=16\) from
`research/period2_certificate.md` satisfy \(u_n=Q_n\) for
\(n=10,\ldots,17\), with \(F_{21}=\cdots=F_{36}=0\) and \(F_{37}=1\).

## Checks

- Reduced ANF through \(k=16\): linear \(u_n\) in \(F_{2n+1}\) and in
  \(G_{2n}\) for \(n\le 7\); \(u_n\) absent from earlier \(F\) and from
  \(G_k\) with \(k<2n\).
- Fold of the single-1 word \(e_n\) through \(n=48\): \(F_k\) for
  \(k\le 2n\) is vacuum, and \(F_{2n+1}(e_n)=0=1\oplus 1\).
- Vacuum \(F_{2n+1}=1\) (constant term of \(Q_n\)).

## What this does not do

Forcing determines the tail; it does not make the tail illegal. The
\(T=20\) period-3 tail `00010010010001` is ugap-legal and matches
\(u_n=Q_n\) through \(n=17\); the next forced bit is \(Q_{18}=1\) with
\(u_{17}=1\), which is the 11-clip of `research/period2_qshift.md`.
The bounded-`nvars` scan's extra zero at \(u_{18}\) is what produces
\(F_{37}=1\).
A uniform \(R(T)\) would still need a \(T\)-independent reason that
the forced continuation fires a later \(F_k\) (or a `11` / `00000`)
inside a bounded window. The leading-variable identity is that
reason's first step, not the bound. The second step is the
three-zero skip \(Q_n(u)=Q_{n-1}(Su)\) of
`research/period2_qshift.md`: on \(T=20\) the forced bit is an
11-clip at \(n=18\), and \(F_{37}\) is the padding artifact of
refusing it.

Periodic \(u\) is already infinite on the left
(`research/period2_periodic.md`). Aperiodic \(u\) remains the
obstruction to period 2.

## Verdict

`LEMMA`, wall time <1s.

- Kill of period 2: no.
- Unique \(L_0\) tail given the onset prefix: yes.
- Uniform \(R\): no.

## Files

- `research/period2_lead.md` (this note)
- `research/period2_lead.py` (`--certify`)
- `research/period2_lead.json` (dump)
- `research/period2_silent.md` (\(u_0\) silent in \(F_k\) for \(k\ge 3\))
- `research/period2_gsilent.md` (\(u_1\) silent in \(G_k\) for \(k\ge 8\))
