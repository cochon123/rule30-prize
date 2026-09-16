# Period-2 \(L_0\): \(u_1\) in \(F_k\) factors through \(u_3\) for \(k\ge 8\)

Checked lemma: on a phase-`01` period-2 centre, every monomial of
\(F_k\) that contains \(u_1\) also contains \(u_3\), for all \(k\ge 8\).
Equivalently \(F_k=A_k\oplus u_1 u_3 C_k\) with \(A_k,C_k\) independent
of \(u_1\). On the slice \(u_3=0\), \(F_k\) is independent of \(u_1\)
for \(k\ge 8\), so extra, kind, and stop of a ugap onset \(T\ge 8\) are
unchanged by flipping \(u_1\). The \(u_3=1\) slice still sees \(u_1\).
This does **not** bound extra. Not a prize claim.

Helper: `python3 research/period2_u1u3.py --certify`. Dump:
`research/period2_u1u3.json`. Silent \(u_1\) in \(G_k\) as in
`research/period2_gsilent.md`; silent \(u_0\) as in
`research/period2_silent.md`.

## Lemma (\(u_1\) factors through \(u_3\))

Work in \(\mathcal B=\mathbb F_2[u_i]/\langle u_i^2+u_i,u_i u_{i+1}\rangle\).
Write a polynomial as having the form \(A\oplus u_1 u_3 C\) when \(A\)
and \(C\) are free of \(u_1\). \(F_8=u_1 u_3\) has this form, and
\(F_7=1+u_2+u_3\) has no \(u_1\) (the form with \(C=0\)).

The OR of two such polynomials is again of this form: if
\(F_i=A_i\oplus u_1 u_3 C_i\) and \(F_j=A_j\oplus u_1 u_3 C_j\), then
\[
F_i F_j
=A_i A_j\oplus u_1 u_3\bigl(A_i C_j\oplus C_i A_j\oplus C_i C_j\bigr)
\]
on the ring (\(u_1^2=u_1\), \(u_3^2=u_3\)), so
\[
F_i\lor F_j
=A_i\oplus A_j\oplus A_i A_j
\oplus u_1 u_3\bigl(C_i\oplus C_j\oplus A_i C_j\oplus C_i A_j\oplus C_i C_j\bigr).
\]
For \(k\ge 9\), \(G_{k-1}\) has no \(u_1\)
(`research/period2_gsilent.md`), hence
\[
F_k=G_{k-1}\oplus(F_{k-1}\lor F_{k-2})
\]
has the form \(A_k\oplus u_1 u_3 C_k\). Induction on \(k\).

Certified as reduced ANF through \(k=20\): no monomial of \(F_k\)
contains \(u_1\) without \(u_3\) for \(k\ge 8\); \(F_8=u_1 u_3\);
\(F_7\) has no \(u_1\); \(F_5=1+u_1+u_2\) still has \(u_1\) without
\(u_3\), so the identity does not start earlier.

## Corollary (slice \(u_3=0\))

If \(u_3=0\) and \(k\ge 8\) then \(F_k(u)=F_k(u\textrm{ with }u_1\textrm{ flipped})\)
whenever the flipped word remains Fibonacci-legal. A ugap onset at
\(T\ge 8\) on this slice therefore has extra, kind, and stop unchanged
by the flip. Certified on every ugap word of length \(\mathrm{nvars}(T)\)
with \(u_3=0\) for \(T\in[8,28]\): 1085 onsets, 238 legal flips, 238
extra/kind/stop matches, 0 failures; \(F_k\) agrees for every \(k\ge 8\).

## What this does not do

The factorisation does not kill \(u_1\) on \(u_3=1\). Extra on that
slice still depends on \(u_1\). Uniform extra \(\le 8\) is still a
census. Other periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~0.3s.

- Kill of period 2: no.
- \(u_1\) in \(F_k\) (\(k\ge 8\)) factors through \(u_3\): yes.
- Extra invariant on \(u_3=0\): yes.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_u1u3.md` (this note)
- `research/period2_u1u3.py` (`--certify`)
- `research/period2_u1u3.json` (dump)
- `research/period2_gsilent.md` (\(u_1\) silent in \(G_k\) for \(k\ge 8\))
