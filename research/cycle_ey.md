# Cycle EY: `11` in \(S\) forces consecutive `00` in \(\operatorname{gap}(S)\); even-\(n_0\) \(n_4\) has `00`

If \(S\) has `11` at \((t-1,t)\) then \(\operatorname{back\_dist}(t)=\operatorname{back\_dist}(t+1)=1\),
so \(\operatorname{gap}(S)_t=\operatorname{gap}(S)_{t+1}=0\). Even-\(n_0\)
O-type always has a `11` (Cycle EV), so \(\operatorname{gap}(T)\) and
scar \(n_4=\operatorname{rot}^{n_0-1}(\operatorname{gap}(T))\) always
have a consecutive `00`. The converse is false (`100` and `100100` have
gap `00` with no `11`). Even-\(n_0\) \(n_6\) can lack a consecutive `00`
(124 of 1364 words). Kills: gap has `00` iff \(S\) has `11`; \(n_6\)
always has `00`. Do **not** claim an 11-bit gap. Do **not** claim
\(n_6\) type N for odd \(n_0\). Do **not** claim a formula for extra
414990. Do **not** bump all \(n_0=16\) past 414990. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push the \(n_0=2\) seed
past \(k=21\).

Not a prize claim: consecutive `00` in \(n_4\) does not give covering
never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_ey.py --certify` (~0.02s). Dump:
`research/cycle_ey.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/DV/EU/EV/EW/EX (no new packed run, no
Fermat table, no even-spine, no \(n_0=16\) window).

## Lemma (`11` \(\Rightarrow\) consecutive `00` in gap)

At the second 1 of a `11`, backward distance is 1. At the next bit the
previous 1 is that second 1, so backward distance is again 1. Gap-parity
is 1 only on even distance, hence both bits of gap are 0. Certified on
every nonzero word of length \(2..10\) (2035 words, 4608 sites).

## Lemma (even \(n_0\): \(\operatorname{gap}(T)\) and \(n_4\) have consecutive `00`)

Cycle EV: even-\(n_0\) O-type always has a `11`. The previous lemma
places a consecutive `00` in \(\operatorname{gap}(T)\). Scar \(n_4\) is
a rotation of that gap (Cycle EW), so it has a consecutive `00` too.
Certified even \(2\le n_0\le 10\), and on \(T^*\).

## Killed

Gap has `00` iff \(S\) has `11` (counterexamples `100` and `100100`).
Even-\(n_0\) \(n_6\) always has a consecutive `00` (124 of 1364 words
lack one; \(T^*\) happens to have one).

## Verdict

`LEMMA` (`11` \(\Rightarrow\) gap `00`; even \(n_0\) gap has `00`; even
\(n_0\) \(n_4\) has `00`).
`KILLED` (gap `00` iff `11`; \(n_6\) always has `00`).
`PREFIX` (11-bit gap; formula for extra 414990; at-most-one-odd for
all \(k\); seed for all \(k\); \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ey.md` (this note)
- `research/cycle_ey.py`
- `research/cycle_ey.json`
