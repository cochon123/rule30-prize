# Period-2 \(L_0\): \(u_2\) in \(G_k\) factors through \(u_4\) for \(k\ge 9\)

Checked lemma: on a phase-`01` period-2 centre, every monomial of
\(G_k\) that contains \(u_2\) also contains \(u_4\), for all \(k\ge 9\).
Equivalently \(G_k=D_k\oplus u_2 u_4 E_k\) with \(D_k,E_k\) independent
of \(u_2\). This is the shift of the \(u_1 u_3\) factorisation of
\(F_j\) (`research/period2_u1u3.md`). On the slice \(u_4=0\), \(G_k\)
is independent of \(u_2\) for \(k\ge 9\). \(F_k\) still has a linear
\(u_2\), so extra is not invariant under flipping \(u_2\). Not a prize
claim.

Helper: `python3 research/period2_gu2u4.py --certify`. Dump:
`research/period2_gu2u4.json`. Factorisation of \(F\) as in
`research/period2_u1u3.md`; silent \(u_1\) in \(G\) as in
`research/period2_gsilent.md`.

## Lemma (\(u_2\) factors through \(u_4\) in \(G_k\))

Work in \(\mathcal B=\mathbb F_2[u_i]/\langle u_i^2+u_i,u_i u_{i+1}\rangle\).
For \(j\ge 8\) one has \(F_j=A_j\oplus u_1 u_3 C_j\) with \(A_j,C_j\)
free of \(u_1\), hence
\[
SF_j=SA_j\oplus u_2 u_4\,(SC_j).
\]
In particular \(SF_8=u_2 u_4\). The fold at \(k=9\) uses
\(G_8\lor G_7=1\) (`research/period2_gsilent.md`), so
\[
G_9=SF_8\oplus 1=1+u_2 u_4.
\]
\(G_8=u_3+u_4\) has no \(u_2\). The OR of two polynomials of the form
\(D\oplus u_2 u_4 E\) stays in that form, by the same ring expansion
as `research/period2_u1u3.md` with indices raised by 1. For \(k\ge 10\),
\(G_k=SF_{k-1}\oplus(G_{k-1}\lor G_{k-2})\) with \(k-1\ge 9\ge 8\), so
\(SF_{k-1}\) has the form and both previous \(G\) have it. Induction
on \(k\).

Certified as reduced ANF through \(k=20\): no monomial of \(G_k\)
contains \(u_2\) without \(u_4\) for \(k\ge 8\); \(G_8\) has no \(u_2\);
\(G_9=1+u_2 u_4\); \(G_4=u_2\) still has \(u_2\) without \(u_4\);
\(F_{10}=u_2+u_4+u_2 u_4\) still has linear \(u_2\).

## Corollary (slice \(u_4=0\))

If \(u_4=0\) and \(k\ge 9\) then \(G_k(u)=G_k(u\textrm{ with }u_2\textrm{ flipped})\)
whenever the flipped word remains Fibonacci-legal. Certified on every
ugap word of length 8 with \(u_4=0\), every \(k\in[9,16]\).

## What this does not do

The factorisation does not kill \(u_2\) in \(F\). Extra, kind, and
stop of a ugap onset are not invariant under flipping \(u_2\) on
\(u_4=0\) (mismatches already at \(T=9\)). Uniform extra \(\le 8\) is
still a census. Other periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~0.2s.

- Kill of period 2: no.
- \(u_2\) in \(G_k\) (\(k\ge 9\)) factors through \(u_4\): yes.
- Extra invariant on \(u_4=0\): no.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_gu2u4.md` (this note)
- `research/period2_gu2u4.py` (`--certify`)
- `research/period2_gu2u4.json` (dump)
- `research/period2_u1u3.md` (\(u_1\) in \(F_k\) factors through \(u_3\))
