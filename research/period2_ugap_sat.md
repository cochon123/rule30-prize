# Period-2 \(L_0\): onset table inside the ugap SFT

Checked census: a genuine period-2 even-right sequence \(u\) lies in the
subshift forbidding \(\{11,00000\}\) (`research/period2_ugap.md`). The
Fibonacci onset scan of `research/period2_certificate.md` ignores the
five-zero forbidden word, so several recorded last-sat models are not
prefixes of any period-2 \(u\). Intersecting with max zero-run \(\le 4\)
does **not** kill the worst onset: three of the six \(T=20\), \(R=16\)
words are ugap-legal and remain last-sat. Isolated ugap \(\max R=9\)
through \(T=32\). Not a prize claim.

Helper: `python3 research/period2_ugap_sat.py --certify`. Dump:
`research/period2_ugap_sat.json`. Sound scan: exactly `nvars(T+R)`
ugap strings, as in `research/period2_vacuum.md`.

## Correction of the gap-bound claim

`research/period2_ugap.md` stated that the \(T=20\) last-sat words
already obey the gap bound because their *period-3 tail*
`00010010010001` has max run 3. That check missed the prefix. The six
Fibonacci last-sat words split as

| word | max zero run | ugap |
| --- | ---: | --- |
| `000000010010010001` | 7 | no |
| `001000010010010001` | 4 | yes |
| `010000010010010001` | 5 | no |
| `010100010010010001` | 3 | yes |
| `100000010010010001` | 6 | no |
| `101000010010010001` | 4 | yes |

The three legal words share the same tail from index 4, and are last-sat
at \(R=16\), killed by \(F_{37}\). Restricting the enumerator to ugap
does not change the killing column.

`period2_ugap.py --certify` never scanned these words: it only checks the
4-state \((e,f)\) drain and finite-right width \(\le 8\).

## Ugap onset through \(T=32\)

Every width dies at finite extra \(R\). Global \(\max R=16\), uniquely
at \(T=20\). Every last-sat with \(R\ge 12\) is a bump
(\(F_{T-1}=1\)). Isolated \(\max R=9\), attained at \(T=8\) (one word
`010101001`) and \(T=16\) (two words). After \(T=16\), isolated
\(\max R\le 8\).

Long ugap last-sat and Q-forced obstruction (`research/period2_qshift.md`):

| \(T\) | max \(R\) | \(n\) | kind | stop | extra |
| ---: | ---: | ---: | --- | --- | ---: |
| 8 | 9 | 1 | iso | even \(F\) | 5 |
| 16 | 9 | 2 | iso | even \(F\) | 5 |
| 20 | 16 | 3 | bump | `11` | 8 |
| 22 | 12 | 5 | bump | `11` | 6 |
| 24 | 8 | 7 | bump | `11` | 4 |
| 26 | 11 | 4 | bump | even \(F\) | 6 |
| 29 | 12 | 4 | bump | even \(F\) | 6 |
| 31 | 12 | 3 | bump | even \(F\) | 6 |
| 32 | 8 | 6 | mixed | `11` | 4 |

The \(T=20,22,24\) 11-clips are the same family already recorded: extra
\(=28-T\). \(T=26,29,31\) are a different even-column family, extra 6.

## Fibonacci overcount at \(T=23..32\)

`research/period2_certificate.json` stops at \(T=22\). Filling the gap
on the full Fibonacci table:

- \(T=25\): Fibonacci last-sat \(\max R=9\), all 11 words contain
  `00000` (one has a run of 13). Ugap \(\max R=5\).
- \(T=26\): Fibonacci \(\max R=11\), not the stale pair \((26,5)\) in
  `research/period2_germ.py`. Four of five last-sat are ugap-legal.
- \(T=32\): Fibonacci \(\max R=13\), all 11 last-sat illegal; isolated
  Fibonacci \(\max R=10\). Ugap \(\max R=8\), isolated \(8\).

Ugap \(\max R\le\) Fibonacci \(\max R\) at every overlapping \(T\), as
required by inclusion.

## What this does not do

A uniform \(R(T)\) would still need a \(T\)-independent clip of the
Q-forced tail. Isolated onsets are empirically short on ugap
(\(\le 9\) through \(T=32\)), but that is not a bound: \(T=8\) and
\(T=16\) already hit 9, and \(T=32\) isolated still has \(R=8\).
Infinite \(L_0\) is untouched. The three surviving \(T=20\) words are
genuine ugap prefixes, so the SFT does not remove the worst onset.

Periodic \(u\) is already infinite on the left
(`research/period2_periodic.md`). Aperiodic \(u\) remains the
obstruction to period 2.

## Verdict

`LEMMA`, wall time ~25s.

- Kill of period 2: no.
- \(T=20\), \(R=16\) dies under ugap: no (3 models remain).
- Isolated ugap \(\max R\le 9\) through \(T=32\): yes, not a bound.

## Files

- `research/period2_ugap_sat.md` (this note)
- `research/period2_ugap_sat.py` (`--certify`)
- `research/period2_ugap_sat.json` (dump)
