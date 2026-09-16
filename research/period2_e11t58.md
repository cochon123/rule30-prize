# Period-2 \(L_0\): extra \(\le 10\) fails; \(S\)-minimal extra \(=11\) at \(T=58\)

Checked lemma: a complete ugap onset scan of \(T=58\) has max extra
\(11\). The extra-\(11\) class is eight isolated even-\(F\) words,
\(R=21\), extra bits `01010001000`, \(n_{\mathrm{clip}}=40\). The
\(F\)-pattern is \(1\) then twenty-one zeros then \(1\). \(T=56\) has
max extra \(10\) (`research/period2_e10cap.md`), so extra \(13\) at
\(T=56\) does not exist and extra \(11\) at \(T=58\) is not a \(T+2\)
descent. Uniform extra \(\le 10\) is therefore false. Compactness via
an extra-\(10\) cap does not kill finite-seed \(L_0\). Not a prize
claim: extra may still be bounded.

Helper: `python3 research/period2_e11t58.py --certify`. Dump:
`research/period2_e11t58.json`. Extra \(\le 10\) through \(T=56\) as in
`research/period2_e10cap.md`; extra \(=10\) at \(T=51\) as in
`research/period2_e10t51.md`.

## Lemma (extra \(=11\) is \(S\)-minimal)

\(\mathrm{nvars}(58)=29\). The eight words are the length-\(8\)
prefixes
\[
\{00001000,00010000,00101000,01001000,01010000,10001000,10010000,10101000\}
\]
followed by the common tail `100101001000010000100`. They descend to
bump even \(F\) extra \(=9\) at \(T=60\). The scan also finds extra
\(=10\) (23 onsets) at the same \(T\), so extra \(=11\) is the maximum
rather than an isolated spike with nothing in between.

Sound \(R=21\) exceeds the \(T=51\) extra-\(10\) value \(R=20\) and
the extra-\(\le 8\) cap \(R=17\). Extra \(\le 8\) was already false at
\(T=51\).

## What this does not do

Extra may still admit a uniform bound larger than \(11\). Infinite
\(L_0\) / infinite \(B_0\) is untouched. Other periods of \(c_t\) are
untouched. The \(T\le 56\) extra-\(\le 10\) census remains correct as
a finite check.

## Verdict

`LEMMA`, wall time ~154s.

- Kill of period 2: no.
- Uniform extra \(\le 10\): no (counterexample).
- \(S\)-minimal extra \(=11\): yes, at \(T=58\).
- Extra unbounded: not proved.

## Files

- `research/period2_e11t58.md` (this note)
- `research/period2_e11t58.py` (`--certify`)
- `research/period2_e11t58.json` (dump)
- `research/period2_e10cap.md` (extra \(\le 10\) through \(T=56\))
- `research/period2_e10t51.md` (first extra \(=10\) at \(T=51\))
- `research/period2_alldesc.md` (extra descent)
