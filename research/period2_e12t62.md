# Period-2 \(L_0\): extra \(\le 11\) fails; extra \(=12\) at \(T=62\)

Checked lemma: the eight length-\(8\) prefixes of the \(T=58\)
isolated extra-\(11\) family
(`research/period2_e11t58.md`) each extend to an isolated even-\(F\)
extra-\(12\) ugap onset at \(T=62\), with \(R=23\),
\(n_{\mathrm{clip}}=43\), extra bits `010000101001`, and \(F\)-pattern
\(1\) then twenty-three zeros then \(1\). The same eight prefixes
repeat extra \(=12\) at \(T=64\) (\(R=23\), \(n_{\mathrm{clip}}=44\)).
Uniform extra \(\le 11\) is therefore false. This is a forced-word
certificate, not a complete \(T=62\) scan, and \(S\)-minimality is
not claimed. Not a prize claim: extra may still be bounded.

Helper: `python3 research/period2_e12t62.py --certify`. Dump:
`research/period2_e12t62.json`. Prefixes as in
`research/period2_e11t58.md`.

## Lemma (extra \(=12\) on the extra-\(11\) prefixes)

Write \(P_8\) for
\[
\{00001000,00010000,00101000,01001000,01010000,10001000,10010000,10101000\}.
\]
At \(T=62\), \(\mathrm{nvars}(62)=31\) and the eight words \(P_8\)
followed by `10001001001000100100100` are isolated even-\(F\) extra
\(=12\). They descend to bump even \(F\) extra \(=10\) at \(T=64\).
At \(T=64\), \(\mathrm{nvars}(64)=32\) and \(P_8\) followed by
`100100100101010001010010` are again isolated even-\(F\) extra
\(=12\), descending to extra \(=10\) at \(T=66\).

High extra on this cylinder climbs \(11\) at \(T=58\) then \(12\) at
\(T=62\) and \(T=64\). Sound \(R=23\) exceeds the \(T=58\) value
\(R=21\).

## What this does not do

Max extra at \(T=62\) on prefixes outside \(P_8\) is not scanned.
\(S\)-minimal extra \(=12\) is not certified (that would need a
complete \(T=60\) scan). Infinite \(L_0\) is untouched. Other periods
of \(c_t\) are untouched. Extra unbounded is not proved.

## Verdict

`LEMMA`, wall time ~0.2s.

- Kill of period 2: no.
- Uniform extra \(\le 11\): no (counterexample).
- Extra \(=12\) on the \(T=58\) prefixes: yes.
- Extra unbounded: not proved.

## Files

- `research/period2_e12t62.md` (this note)
- `research/period2_e12t62.py` (`--certify`)
- `research/period2_e12t62.json` (dump)
- `research/period2_e11t58.md` (\(P_8\) extra \(=11\))
- `research/period2_e10t51.md` (extra \(\le 8\) fails)
- `research/period2_e10cap.md` (extra \(\le 10\) through \(T=56\))
