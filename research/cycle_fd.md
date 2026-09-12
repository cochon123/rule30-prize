# Cycle FD: reconstruct consecutive `00` iff \(U=0\) and \(A=B\)

Let \(U=\operatorname{reconstruct}(A,B)\). The recurrence is
\(U_{t+1}=A_t\oplus(B_t\lor U_t)\). If \(U_t=0\), then
\(U_{t+1}=A_t\oplus B_t\), so \(U_t=U_{t+1}=0\) if and only if
\(A_t=B_t\). Therefore \(U\) has consecutive `00` if and only if some
\(t\) has \(U_t=0\) and \(A_t=B_t\). This is the dual of Cycle EZ
(consecutive `11` iff \(U\) meets a 0 of \(A\)).

On even-\(n_0\) scars this restates Cycle FB without \(F\)-invariance
of `00`: \(n_5\) has `00` iff \(n_5=0\) on an \(n_3=n_4\) agreement,
and \(n_6\) has `00` iff \(n_6=0\) on an \(n_4=n_5\) agreement. Always
\(\operatorname{ham}(n_4,n_5)=n_0\). The no-`00` class is exactly the
words where \(n_6=1\) on every \(n_4=n_5\) agreement. Kills: generic
reconstruct pairs do **not** satisfy
\(\operatorname{has00}(U)\Leftrightarrow\operatorname{has00}(\operatorname{reconstruct}(B,U))\).
Do **not** claim an 11-bit gap. Do **not** claim no-`00` iff extra 22
or 89. Do **not** claim a formula for extra 414990. Do **not** bump
all \(n_0=16\) past 414990. Do **not** compute \(\varphi^{(3,5,9)}\)
at \(k=16\). Do **not** push the \(n_0=2\) seed past \(k=21\).

Not a prize claim: the `00` criterion does not give covering never-fail
or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_fd.py --certify`. Dump:
`research/cycle_fd.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CH/DV/ER/EV/EW/EZ/FB/FC (no new packed run,
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (consecutive `00` criterion)

Certified on every defined pair of length \(2..8\) (86868 words, same
universe as Cycle EZ).

## Lemma (scar restatement)

Certified on all 1364 even-\(n_0=2..10\) O-types, and on \(T^*\). The
124 no-`00` words are exactly those with \(n_6=1\) on every
\(n_4=n_5\) agreement.

## Killed

Generic \(\operatorname{has00}(U)\Leftrightarrow\operatorname{has00}(F(U))\):
27169 counterexamples on length \(2..8\). Cycle FB's iff is
scar-specific.

## Verdict

`LEMMA` (consecutive `00` iff \(U=0\) and \(A=B\); scar \(n_5\)/\(n_6\)
`00` iff zero on agreement; no-`00` is one on all agreements;
\(\operatorname{ham}(n_4,n_5)=n_0\)).
`KILLED` (generic `00` \(F\)-invariance).
`PREFIX` (11-bit gap; formula for extra 414990; at-most-one-odd for
all \(k\); seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fd.md` (this note)
- `research/cycle_fd.py`
- `research/cycle_fd.json`
