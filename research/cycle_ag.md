# Cycle AG: \(O_s\) is local; at 1-run endings \(O_s=a\oplus e\)

Cycle AF treated the older Green remainder \(O_s\) as bulk data in
the past light cone. On the prize orbit \(c_{s+2}\) is a function of
the centred 5-window, so \(O_s\) equals a local Boolean of that
window. At a 1-run ending it is the distance-2 palindrome defect
\(a\oplus e\). Not a prize claim: infinitely many `00`s are still the
same 5-window production as Cycles AD–AE.

Helper: `python3 research/cycle_ag.py --certify`. Dump:
`research/cycle_ag.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(O_s\) is local)

The Rule 30 5-window \((a,\ell,c,r,e)\) determines
\((\ell',c',r')\) and then \(c''\). Cycle AF’s identity therefore
solves for the Green remainder as

\[
O_s
=c''
\oplus 1
\oplus(\ell\land c)
\oplus(c\land r)
\oplus(r\land e)
\oplus(c'\land r').
\]

The right-hand side is a function of the 5-window. Certified: Green
\(O_s\) matches this Boolean for all \(s<36\) on the prize orbit
(28 of 32 windows occur). The leading 1 is the prize-seed Rule 150
centre (Cycle Y/AA), so the match is for this orbit, not a general
initial condition. \(O_s\) is not an independent bulk bit.

## Lemma (\(O_s=a\oplus e\) at 1-run endings)

Restrict to \((\ell,c)=(1,1)\). Then \(c'=0\) and Cycle AF gives
\(c''=(r\land\lnot e)\oplus O_s\). Independently, Cycle AE gives
\(c''=0\) iff \(a=r\lor e\), i.e. \(c''=a\oplus(r\lor e)\). Hence

\[
O_s
=(r\land\lnot e)\oplus a\oplus(r\lor e)
=a\oplus e,
\]

since \((r\land\lnot e)\oplus(r\lor e)=e\). Certified as an 8-row
truth table, and against Green \(O_s\) on 1-run endings with
\(s<36\). Thus \(O_s\) is the palindrome defect of the \(\pm 2\)
cells, the distance-2 analogue of \(d=\ell\oplus r\).

`00` follows a 1-run ending iff \(O_s=r\land\lnot e\) iff
\(a\oplus e=r\land\lnot e\) iff \(a=r\lor e\), recovering Cycle AE.

## \(O_s\) as a bulk `00` handle — killed

Chasing a production of \(O_s=r\land\lnot e\) in the past light cone
is the same 5-window condition as Cycles AD–AE. Nested edges are
already excluded (AD, AE). There is no extra Green degree of freedom
to force infinitely many `00`s. **Killed.**

## Verdict

`LEMMA` (\(O_s\) local on the prize orbit; \(O_s=a\oplus e\) at
1-run endings). `KILLED` (\(O_s\) as a bulk `00` handle). `OPEN`
(infinitely many `00`s). Wall time 0.01s. Prize unsolved.

## Files

- `research/cycle_ag.md` (this note)
- `research/cycle_ag.py`
- `research/cycle_ag.json`
