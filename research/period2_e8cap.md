# Period-2 \(L_0\): extra \(\le 8\) through \(T=48\)

Checked census: every ugap onset with \(T\in[41,48]\) has Q-forced
extra \(\le 8\). Extra \(=8\) occurs at \(T=43\) (isolated even \(F\),
exactly the twelve \((00010010)^2\)-tail words), \(T=44\) (isolated
`11`), \(T=46\) (bump even \(F\)), \(T=47\) (isolated even \(F\)),
and \(T=48\) (bump even \(F\)). Combined with
`research/period2_alldesc.md` through \(T=40\), extra \(\le 8\) holds
through \(T=48\). This is **not** a \(T\)-independent bound. Not a
prize claim.

Helper: `python3 research/period2_e8cap.py --certify`. Dump:
`research/period2_e8cap.json`. Extra-to-\(R\) as in
`research/period2_qextra.md`; \(T=43\) family as in
`research/period2_t35ten.md`.

## Census (\(T=41\) to \(48\))

\(\mathrm{nvars}(48)=24\). A complete ugap scan finds no extra
\(\ge 9\). The maximum is \(8\), and it is attained:

| \(T\) | max extra | extra \(=8\) kind | sample tail |
| --- | --- | --- | --- |
| 41 | 7 | — | — |
| 42 | 7 | — | — |
| 43 | 8 | iso even \(F\) (12 words) | `(00010010)^2` |
| 44 | 8 | iso `11` | — |
| 45 | 7 | — | — |
| 46 | 8 | bump even \(F\) | — |
| 47 | 8 | iso even \(F\) | — |
| 48 | 8 | bump even \(F\) | — |

The \(T=43\) extra-\(8\) isolated class is exactly the twelve words
of `research/period2_t35ten.md`, all with suffix `0001001000010010`
\(=(00010010)^2\). A prefix-6 scan of that period-8 tail on
\(T\in[30,48]\) spikes to extra \(=8\) only at \(T=43\) (probe of
that restricted family, not this certificate’s only check).

Through \(T=40\), `research/period2_alldesc.md` already has max extra
\(8\) at \(T=20\) and \(T=37\) (bump `11`). The extra-\(8\) loci
through \(T=48\) are therefore
\(\{20,37,43,44,46,47,48\}\).

## What this does not do

Extra \(\le 8\) is still a census. Compactness would kill every
finite-seed \(L_0\) if the bound held for all \(T\), but that is not
proved. \(S\)-minimal extra \(=8\) exists (nine of the \(T=43\)
isolated words; the \(T=37\) bump `11` family). Infinite \(B_0\) is
untouched. Other periods of \(c_t\) are untouched.

## Verdict

`CENSUS`, wall time ~50s.

- Kill of period 2: no.
- Extra \(\le 8\) through \(T=48\): yes (census).
- Uniform extra \(\le 8\) for all \(T\): no.
- \(T=43\) isolated extra \(=8\) is the period-8 tail: yes.

## Files

- `research/period2_e8cap.md` (this note)
- `research/period2_e8cap.py` (`--certify`)
- `research/period2_e8cap.json` (dump)
- `research/period2_alldesc.md` (extra \(\le 8\) through \(T=40\))
- `research/period2_t35ten.md` (\(T=43\) extra-\(8\) words)
- `research/period2_e8fam.md` (extra \(=8\) is two prefix families)
- `research/period2_qextra.md` (extra to sound \(R\))
