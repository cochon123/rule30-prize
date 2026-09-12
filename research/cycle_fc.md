# Cycle FC: even-\(n_0\) \(n_7\) consecutive `11` by \(n_5\)-`00` / no-`00` case split

If \(n_5\) has a `00`, some `00` starts at \(n_6=1\). Then
\(n_{7,s+1}=\neg n_{5,s}=1\) and \(n_{5,s+1}=0\), so \(n_7\) meets a 0
of \(n_5\) (Cycle EZ). If \(n_5\) has no `00`, \(n_7\) is O-type
(Cycle FB) and even-\(n_0\) O-type has a `11` (Cycle EV). Together
every even-\(n_0\) scar has consecutive `11` in \(n_7\). Kills: every
\(n_5\)-`00` starts at \(n_6=0\). Do **not** claim an 11-bit gap. Do
**not** claim \(n_7\) type N. Do **not** claim a formula for extra
414990. Do **not** bump all \(n_0=16\) past 414990. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push the \(n_0=2\) seed
past \(k=21\).

Not a prize claim: consecutive `11` in \(n_7\) does not give covering
never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_fc.py --certify` (~0.02s). Dump:
`research/cycle_fc.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CB/DV/ER/EV/EW/EZ/FB (no new packed run, no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(n_5\) `00` \(\Rightarrow\) \(n_6=1\) at some `00` start)

Certified on all 1240 even-\(n_0\) O-types with a `00` in \(n_5\), and
on \(T^*\). Never all such starts have \(n_6=0\).

## Lemma (has-`00` class: \(n_7\) consecutive `11`)

At that start \(s\), \(n_{7,s+1}=1\) and \(n_{5,s+1}=0\), so Cycle EZ’s
meet criterion fires.

## Lemma (no-`00` class: \(n_7\) O-type has `11`)

Cycle FB: no-`00` \(\Rightarrow\) \(n_7\) O-type. Cycle EV: even
\(n_0\) O-type has a `11`. Certified on all 124 no-`00` words.

## Lemma (even \(n_0\): \(n_7\) consecutive `11` is proved)

The two classes partition even-\(n_0\) O-types.

## Killed

Every \(n_5\)-`00` starts with \(n_6=0\).

## Verdict

`LEMMA` (\(n_6=1\) at some \(n_5\)-`00` start; has-`00` \(n_7\) `11`;
no-`00` \(n_7\) O-type `11`; even \(n_0\) \(n_7\) consecutive `11`
proved).
`KILLED` (all \(n_5\)-`00` starts at \(n_6=0\)).
`PREFIX` (11-bit gap; formula for extra 414990; at-most-one-odd for
all \(k\); seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fc.md` (this note)
- `research/cycle_fc.py`
- `research/cycle_fc.json`
