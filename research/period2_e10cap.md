# Period-2 \(L_0\): extra \(\le 10\) through \(T=56\); extra \(=10\) recurs

Checked census: a complete ugap onset scan of \(T\in[53,56]\) has max
extra \(9\) at \(T=53\) and max extra \(10\) at \(T=54,55,56\). Combined
with `research/period2_e10t51.md` (\(T=49,50\) max \(8\); \(T=51,52\)
max \(10\)), extra \(\le 10\) holds through \(T=56\). The extra-\(10\)
onsets at \(T=54,55,56\) are \(S\)-minimal. Extra does not climb past
\(10\) on this range. This is **not** a \(T\)-independent bound. Not a
prize claim.

Helper: `python3 research/period2_e10cap.py --certify`. Dump:
`research/period2_e10cap.json`. Extra \(=10\) at \(T=51,52\) as in
`research/period2_e10t51.md`; \(P_{35}\) as in
`research/period2_t35ten.md`.

## Census (\(T=53\) to \(56\))

\(\mathrm{nvars}(56)=28\). Descent of extra \(e\ge 3\) at \(T+2\) needs
a parent of extra \(e+2\). \(T=52\) has max extra \(10\), so extra
\(10\) at \(T=54\) is \(S\)-minimal; \(T=53\) has max extra \(9\), so
extra \(10\) at \(T=55\) is \(S\)-minimal; \(T=54\) has max extra
\(10\), so extra \(10\) at \(T=56\) is \(S\)-minimal.

| \(T\) | max extra | extra \(=10\) |
| --- | --- | --- |
| 53 | 9 | none (26 extra \(=9\) even-\(F\)) |
| 54 | 10 | six isolated `11`, all of \(P_{35}\), tail `101010000101001001010`, \(R=20\) |
| 55 | 10 | seven isolated even \(F\), prefixes \(\{000101,001001,010001,010101,100001,100101,101001\}\), tail `0010001010000100101001`, \(R=20\) |
| 56 | 10 | the same seven prefixes, tail `0010000100010101000100`, \(R=19\) |

Each listed extra-\(10\) family descends to extra \(=8\) at \(T+2\).
The \(T=54\) prefixes are exactly the six \(T=35\) \(10\)-tail
prefixes. The \(T=55,56\) prefixes are the seven length-\(6\) ugap
words that end in `01` and lie in \(P_{43}\).

## What this does not do

Extra \(\le 10\) is a census through \(T=56\). \(S\)-minimal extra
\(=10\) keeps being born, so compactness via extra \(\le 8\) stays
dead and extra \(\le 10\) is not a theorem. Infinite \(L_0\) is
untouched. Other periods of \(c_t\) are untouched.

## Verdict

`CENSUS`, wall time ~271s.

- Kill of period 2: no.
- Extra \(\le 10\) through \(T=56\): yes (census).
- Uniform extra \(\le 10\): no.
- \(S\)-minimal extra \(=10\) recurs: yes.

## Files

- `research/period2_e10cap.md` (this note)
- `research/period2_e10cap.py` (`--certify`)
- `research/period2_e10cap.json` (dump)
- `research/period2_e10t51.md` (first extra \(=10\) at \(T=51\))
- `research/period2_t35ten.md` (\(P_{35}\))
- `research/period2_e8cap.md` (extra \(\le 8\) through \(T=48\))
