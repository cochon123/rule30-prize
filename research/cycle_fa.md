# Cycle FA: even-\(n_0\) \(n_5\) consecutive `11` via O-type xor at empty \(n_4\)-pair

\(n_3\) is O-type, so \(n_{3,i}\oplus n_{3,i+n_0}=1\). An empty
\(n_4\)-pair has \(n_5=11\) (Cycle EX). Consecutive `11` iff \(U=1\) on
a 0 of \(A\) (Cycle EZ), here \(A=n_3\) and \(U=n_5\), so the 0 of that
\(n_3\)-pair is a meet. That proves consecutive `11` in \(n_5\). Kills:
\(n_5\) always has `00` (124 of 1364 lack it); \(n_7\) always type N
(440 O-type). Do **not** claim \(n_7\) consecutive `11` as a
production. Do **not** claim an 11-bit gap. Do **not** claim \(n_6\)
type N for odd \(n_0\). Do **not** claim a formula for extra 414990.
Do **not** bump all \(n_0=16\) past 414990. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push the \(n_0=2\) seed
past \(k=21\).

Not a prize claim: consecutive `11` in \(n_5\) does not give covering
never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_fa.py --certify` (~0.02s). Dump:
`research/cycle_fa.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CB/DV/ER/EV/EW/EX/EZ (no new packed run, no
Fermat table, no even-spine, no \(n_0=16\) window).

## Lemma (even \(n_0\): \(n_5\) consecutive `11` is proved)

O-type pair-xor plus empty-pair \(n_5=11\) plus Cycle EZ’s meet
criterion. Certified even \(2\le n_0\le 10\), and on \(T^*\) (\(z=5\),
\(\mathrm{wt}(n_5)=15\)).

## Killed

\(n_5\) always has a consecutive `00` (124 words lack one; the same
count as \(n_6\) in Cycle EY). \(n_7\) always type N (440 O-type, 924
N). \(n_7\) has a consecutive `11` on this range (`PREFIX`, no
production for the 124 \(n_5\) with no `00`).

## Verdict

`LEMMA` (even \(n_0\) \(n_5\) consecutive `11` proved).
`KILLED` (\(n_5\) always has `00`; \(n_7\) always type N).
`PREFIX` (\(n_7\) consecutive `11`; 11-bit gap; formula for extra
414990; at-most-one-odd for all \(k\); seed for all \(k\); \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fa.md` (this note)
- `research/cycle_fa.py`
- `research/cycle_fa.json`
