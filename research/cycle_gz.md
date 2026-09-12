# Cycle GZ: odd-\(s\) band XOR is AND on \(G(n,j)=1\) even columns

Cycle GX indexes those columns. AND can fire on \(G=0\) even columns
but contributes 0. Odd-\(s\) XOR is **not** \(\Delta_R\) (\(k=4\),
\(W=8U\): \(0\) vs \(1\)); even-\(s\) XOR is **not** identically 0.
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: reducing the odd-\(s\) slice to AND on Green ones
does not prove covering never-fail (even \(s\) still contribute; AND
has no closed form).

Helper: `odd_clock` from `research/cycle_gu.py`. Certify:
`python3 research/cycle_gz.py --certify` (~0.05s). Dump:
`research/cycle_gz.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FL/FR/GU/GX/GY (packed \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (odd-\(s\) XOR \(=\) AND on \(G(n,j)=1\) even columns)

Certified \(k\le 6\), all covering \(W\). Odd-\(r\) Green is 0 so
those ANDs drop out.

## Killed

AND only on \(G=1\): at \(k=1\), \(W=8U\), a \(G=0\) even column
fires. Odd-\(s\) XOR equals \(\Delta_R\): at \(k=4\), \(W=8U\),
\(0\neq 1\). Even-\(s\) XOR identically 0: at \(k=4\), \(W=8U\), xor
\(=1\).

## Verdict

`LEMMA` (odd-\(s\) band XOR = AND on \(G(n,j)=1\)).
`KILLED` (AND only on \(G=1\); odd-\(s\) XOR \(=\Delta_R\); even-\(s\)
XOR \(=0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gz.md` (this note)
- `research/cycle_gz.py`
- `research/cycle_gz.json`
