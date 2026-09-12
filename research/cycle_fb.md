# Cycle FB: even-\(n_0\) \(n_5\) has `00` iff \(n_6\) has `00`; no-`00` class has \(z=n_0/2\)

On every even-\(n_0\) O-type, \(n_5\) has a consecutive `00` iff \(n_6\)
does. The no-`00` class has size \(2^{n_0/2+1}\), empty-pair count
\(z=n_0/2\), and \(n_7\) O-type. \(n_0=4\) no-`00` is FAM89; \(n_0=6\)
no-`00` contains the extra-22 3-folds. Kills: \(n_7\) O-type implies
\(n_5\) has no `00` (316 counterexamples); no-`00` is only extra 22
(\(n_0=4\) is FAM89). Do **not** claim no-`00` iff extra 22 or 89
(\(n_0=6\) also has extra 99; \(n_0=8\) has 32 no-`00` with extra
\(>500\)). Do **not** claim \(n_7\) consecutive `11` as a production.
Do **not** claim an 11-bit gap. Do **not** bump extras. Do **not**
claim a formula for extra 414990. Do **not** bump all \(n_0=16\) past
414990. Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\). Do
**not** push the \(n_0=2\) seed past \(k=21\).

Not a prize claim: the no-`00` class does not give covering never-fail
or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_fb.py --certify` (~0.02s). Dump:
`research/cycle_fb.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CB/DV/EB/ER/EV/EW/EX/FA (no new packed run,
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(n_5\) has `00` iff \(n_6\) has `00`)

Certified every even-\(n_0\) O-type \(2\le n_0\le 10\) (1364 words),
and on \(T^*\) (both have `00`).

## Lemma (no-`00` class: size \(2^{n_0/2+1}\), \(z=n_0/2\), \(n_7\) O-type)

Counts \(4,8,16,32,64\). Empty-pair count is exactly \(n_0/2\). \(n_7\)
is O-type on that class. \(n_0=4\) is FAM89; \(n_0=6\) contains
\(\{001100,011001,100110,110011\}\).

## Killed

\(n_7\) O-type implies no `00` in \(n_5\) (316 words have both). No-`00`
is only extra 22 (\(n_0=4\) no-`00` is the extra-89 family).

## Verdict

`LEMMA` (\(n_5\) `00` iff \(n_6\) `00`; no-`00` has \(z=n_0/2\) and
\(n_7\) O-type).
`KILLED` (\(n_7\) O \(\Rightarrow\) no `00`; no-`00` only extra 22).
`PREFIX` (\(n_7\) consecutive `11`; 11-bit gap; formula for extra
414990; at-most-one-odd for all \(k\); seed for all \(k\); \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fb.md` (this note)
- `research/cycle_fb.py`
- `research/cycle_fb.json`
