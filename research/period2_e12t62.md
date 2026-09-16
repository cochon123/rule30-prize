# Period-2 \(L_0\): extra \(\le 13\) fails; \(S\)-minimal extra \(=14\) at \(T=62\)

Checked lemma: a complete ugap onset scan of \(T=62\) has max extra
\(14\). The extra-\(14\) class is ten bump even-\(F\) words,
\(R=27\), extra bits `01001010001000`, \(n_{\mathrm{clip}}=45\). The
\(F\)-pattern is \(1\) then twenty-seven zeros then \(1\). \(T=60\) has
max extra \(11\), so extra \(16\) at \(T=60\) does not exist and extra
\(14\) at \(T=62\) is not a \(T+2\) descent. Uniform extra \(\le 11\),
\(\le 12\), and \(\le 13\) are therefore false. Compactness via those
caps does not kill finite-seed \(L_0\). Not a prize claim: extra may
still be bounded.

Helper: `python3 research/period2_e12t62.py --certify`. Dump:
`research/period2_e12t62.json`. Extra \(\le 10\) through \(T=56\) as in
`research/period2_e10cap.md`; extra \(=11\) at \(T=58\) as in
`research/period2_e11t58.md`.

## Lemma (extra \(=14\) is \(S\)-minimal)

\(\mathrm{nvars}(62)=31\). The ten words are the length-\(5\) prefixes
\[
\{00001,00010,00100,00101,01001,01010,10001,10010,10100,10101\}
\]
followed by the common tail `00100001000100010001000100`. They descend
to bump even \(F\) extra \(=12\) at \(T=64\). The same \(T\) also has
fifteen isolated even-\(F\) extra-\(12\) onsets (\(R=23\)); eight of
those are the \(T=58\) extra-\(11\) prefixes \(P_8\) with tail
`10001001001000100100100`. There is no extra \(=13\) at \(T=62\).

Sound \(R=27\) exceeds the \(T=58\) extra-\(11\) value \(R=21\) and the
isolated extra-\(12\) value \(R=23\). Extra \(\le 8\) was already false
at \(T=51\); extra \(\le 10\) at \(T=58\).

The eight \(P_8\) prefixes also give isolated even-\(F\) extra \(=12\)
at \(T=64\) (tail `100100100101010001010010`, \(R=23\)). That class is
not needed for the extra-\(\le 13\) kill.

## What this does not do

Extra may still admit a uniform bound larger than \(14\). Infinite
\(L_0\) / infinite \(B_0\) is untouched. Other periods of \(c_t\) are
untouched. The \(T\le 58\) extra-\(\le 11\) census remains correct as a
finite check. Extra unbounded is not proved.

## Verdict

`LEMMA`, wall time ~665s (T=60 scan + T=62 scan).

- Kill of period 2: no.
- Uniform extra \(\le 11\): no (counterexample).
- Uniform extra \(\le 12\): no (counterexample).
- Uniform extra \(\le 13\): no (counterexample).
- \(S\)-minimal extra \(=14\): yes, at \(T=62\).
- Extra unbounded: not proved.

## Files

- `research/period2_e12t62.md` (this note)
- `research/period2_e12t62.py` (`--certify`)
- `research/period2_e12t62.json` (dump)
- `research/period2_e11t58.md` (\(P_8\) extra \(=11\))
- `research/period2_e10cap.md` (extra \(\le 10\) through \(T=56\))
- `research/period2_e10t51.md` (extra \(\le 8\) fails)
- `research/period2_alldesc.md` (extra descent)
