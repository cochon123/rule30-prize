# Period-2 \(L_0\): extra \(=14\) recurs \(S\)-minimally at \(T=66\)

Checked lemma: a complete ugap onset scan of \(T=66\) has max extra
\(14\). The extra-\(14\) class is thirty-three bump even-\(F\) words,
\(R=27\), extra bits `10101001010101`, \(n_{\mathrm{clip}}=47\). The
\(F\)-run at \(T\) has length \(3\) (\(F_{64}=F_{65}=F_{66}=1\)), then
zeros until the even fire \(F_{94}=1\). \(T=64\) has max extra \(12\)
(`research/period2_e12t62.md` probe), so extra \(16\) at \(T=64\) does
not exist and extra \(14\) at \(T=66\) is not a \(T+2\) descent. Extra
\(=14\) is therefore a recurring \(S\)-minimal class (also at \(T=62\)),
not a one-off spike. Uniform extra \(\le 14\) is **not** proved. Not a
prize claim: extra may still be bounded.

Helper: `python3 research/period2_e14t66.py --certify`. Dump:
`research/period2_e14t66.json`. Extra \(=14\) at \(T=62\) as in
`research/period2_e12t62.md`.

## Lemma (extra \(=14\) is \(S\)-minimal at \(T=66\))

\(\mathrm{nvars}(66)=33\). The thirty-three words are the length-\(9\)
prefixes
\[
\begin{aligned}
&\{000010010,000010100,000010101,000100010,000100101,\\
&000101010,001000010,001000101,001001010,001010010,\\
&001010100,001010101,010000101,010001010,010010010,\\
&010010100,010010101,010100010,010100101,010101010,\\
&100001010,100010010,100010100,100010101,100100010,\\
&100100101,100101010,101000010,101000101,101001010,\\
&101010010,101010100,101010101\}
\end{aligned}
\]
followed by the common tail `001000101000100001010100`. They descend
to bump even \(F\) extra \(=12\) at \(T=68\). There is no extra \(=13\)
at \(T=66\); extra \(=12\) occurs (11 onsets). Sound \(R=27\) matches
the \(T=62\) extra-\(14\) value.

The \(T=62\) extra-\(14\) family had \(F\)-run \(4\) and a different
`0001`-rich tail. The \(T=66\) family has \(F\)-run \(3\) and is larger
(33 versus 10). Both are \(S\)-minimal births of extra \(=14\).

## What this does not do

Extra may still admit a uniform bound of \(14\), or it may climb
again. Infinite \(L_0\) is untouched. Other periods of \(c_t\) are
untouched. Extra unbounded is not proved. The \(T=64\) max-extra-\(12\)
fact used for \(S\)-minimality is a complete scan recorded as a probe
in `research/period2_e12t62.md`, not re-run here.

## Verdict

`LEMMA`, wall time ~1077s.

- Kill of period 2: no.
- Extra \(=14\) only at \(T=62\): no (recurs at \(T=66\)).
- \(S\)-minimal extra \(=14\) at \(T=66\): yes.
- Uniform extra \(\le 14\): not proved.
- Extra unbounded: not proved.

## Files

- `research/period2_e14t66.md` (this note)
- `research/period2_e14t66.py` (`--certify`)
- `research/period2_e14t66.json` (dump)
- `research/period2_e12t62.md` (first extra \(=14\) at \(T=62\); \(T=64\) max \(12\))
- `research/period2_alldesc.md` (extra descent)
