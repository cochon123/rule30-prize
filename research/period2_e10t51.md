# Period-2 \(L_0\): extra \(\le 8\) fails; \(S\)-minimal extra \(=10\) at \(T=51\)

Checked lemma: a complete ugap onset scan of \(T\in[49,52]\) has max
extra \(8\) at \(T=49\) and \(T=50\), then extra \(10\) at \(T=51\)
(four isolated even-\(F\) words, \(R=20\)) and at \(T=52\) (eight
`11`-clips, \(R=20\)). Neither class is a \(T+2\) descent (that would
need extra \(12\) at \(T=49\) or \(T=50\)) and the \(T=51\) isolated
class has no \(R=3\) preimage. Uniform extra \(\le 8\) is therefore
false. Compactness via an extra-\(8\) cap does not kill finite-seed
\(L_0\). Not a prize claim: extra may still be bounded.

Helper: `python3 research/period2_e10t51.py --certify`. Dump:
`research/period2_e10t51.json`. Census through \(T=48\) as in
`research/period2_e8cap.md`; extra-to-\(R\) as in
`research/period2_qextra.md`; \(R=3\) as in
`research/period2_r3pull.md`.

## Lemma (extra \(=10\) is \(S\)-minimal)

\(\mathrm{nvars}(51)=\mathrm{nvars}(52)=26\). Descent of extra
\(e\ge 3\) at \(T+2\) requires a parent of extra \(e+2\)
(`research/period2_alldesc.md`). The scan has max extra \(8\) at
\(T=49\) and \(T=50\), so extra \(9\) and \(10\) at \(T=51,52\) have
no such parent.

- \(T=51\): four isolated even-\(F\) extra-\(10\) words, all with
  suffix `00100001001010001010100`, extra bits `0010010001`,
  \(n_{\mathrm{clip}}=36\), \(R=20\). The \(F\)-pattern is \(1\) then
  twenty zeros then \(1\). Prefixes
  \(\{001001,010001,100001,101001\}\). No \(R=3\) preimage. They
  descend to bump even \(F\) extra \(=8\) at \(T=53\).
- \(T=51\): eleven bump even-\(F\) extra-\(9\) words, \(R=18\). Eight
  share suffix `00100100010101000010`; three are the
  \(10\)-run prefixes \(\{000101,010101,100101\}\) with suffix
  `01010101010101010001`. They descend to extra \(=7\) at \(T=53\).
  There is no extra \(=8\) at \(T=51\).
- \(T=52\): eight extra-\(10\) `11`-clips (six isolated, two bump),
  all with suffix `101001001001000100`, \(R=20\), extra bits
  `0101010101`. They descend to bump `11` extra \(=8\) at \(T=54\).

Sound \(R=20\) exceeds the \(T=37\) value \(17\) that was sharp for
extra \(\le 8\).

## What this does not do

Extra may still admit a uniform bound larger than \(8\). Infinite
\(L_0\) / infinite \(B_0\) is untouched. Other periods of \(c_t\) are
untouched. The \(T\le 48\) extra-\(\le 8\) census remains correct as a
finite check.

## Verdict

`LEMMA`, wall time ~100s.

- Kill of period 2: no.
- Uniform extra \(\le 8\): no (counterexample).
- \(S\)-minimal extra \(=10\): yes, at \(T=51\) and \(T=52\).
- Extra unbounded: not proved.

## Files

- `research/period2_e10t51.md` (this note)
- `research/period2_e10t51.py` (`--certify`)
- `research/period2_e10t51.json` (dump)
- `research/period2_e8cap.md` (extra \(\le 8\) through \(T=48\))
- `research/period2_alldesc.md` (extra descent)
- `research/period2_r3pull.md` (\(R=3\) pullback)
- `research/period2_qextra.md` (extra to sound \(R\))
