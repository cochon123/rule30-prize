# Cycle EZ: reconstruct consecutive `11` iff \(U\) meets a 0 of \(A\); even-\(n_0\) \(n_6\) `11` proved

For \(U=\operatorname{reconstruct}(A,B)\),
\(U_{t+1}=A_t\oplus(B_t\lor U_t)\). If \(U_t=1\) then
\(U_{t+1}=\neg A_t\), so consecutive `11` iff some \(t\) has \(U_t=1\)
and \(A_t=0\). On an even-\(n_0\) scar, an empty \(n_4\)-pair \(i\) has
\(n_{6,i+1}=n_{6,i+1+n_0}=1\) (Cycle EX). Complementary support forbids
\(n_{4,i+1}=n_{4,i+1+n_0}=1\), so at least one successor is a 0 of
\(n_4\) with \(n_6=1\). That proves consecutive `11` in \(n_6\) (Cycle
EX certified it exhaustively). Kills: \(n_4=0\) implies \(n_6=1\). Do
**not** claim an 11-bit gap. Do **not** claim \(n_6\) type N for odd
\(n_0\). Do **not** claim a formula for extra 414990. Do **not** bump
all \(n_0=16\) past 414990. Do **not** compute \(\varphi^{(3,5,9)}\) at
\(k=16\). Do **not** push the \(n_0=2\) seed past \(k=21\).

Not a prize claim: a proved consecutive `11` in \(n_6\) does not give
covering never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_ez.py --certify` (~0.2s). Dump:
`research/cycle_ez.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/DV/ER/EV/EW/EX/EY (no new packed run, no
Fermat table, no even-spine, no \(n_0=16\) window).

## Lemma (consecutive `11` iff \(U\) meets a 0 of \(A\))

The reconstruct recurrence with \(U_t=1\) forces \(U_{t+1}=\neg A_t\).
Certified on every pair of length \(2..8\) for which reconstruct is
defined (86868 words, 69583 with a consecutive `11`).

## Lemma (empty-pair successors hit by complementary)

Empty pair \(i\): \(n_{6,i+1}=n_{6,i+1+n_0}=1\). Never both successor
\(n_4\) bits are 1. Therefore some successor has \(n_4=0\) and
\(n_6=1\). Certified even \(2\le n_0\le 10\): 978 words hit both
successors, 193 left only, 193 right only.

## Lemma (even \(n_0\): \(n_6\) consecutive `11` is proved)

The two lemmas give a production, not only an exhaustion. Holds on
\(T^*\) (\(z=5\)).

## Killed

\(n_4=0\) does not imply \(n_6=1\) (0 of 1364 even-\(n_0\) words, and
not \(T^*\)).

## Verdict

`LEMMA` (consecutive `11` iff \(U\) meets a 0 of \(A\); empty-pair
successors complementary-hit; even \(n_0\) \(n_6\) consecutive `11`
proved).
`KILLED` (\(n_4=0\Rightarrow n_6=1\)).
`PREFIX` (11-bit gap; formula for extra 414990; at-most-one-odd for
all \(k\); seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ez.md` (this note)
- `research/cycle_ez.py`
- `research/cycle_ez.json`
