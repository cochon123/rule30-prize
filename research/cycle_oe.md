# Cycle OE: on \(q=10\), NJ's \(S\) on \(n\ge 7U/2\) dies at \(k=9\)

On covering \(J_{10}\), Cycle NJ's XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(n\ge 7U/2\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff
\(k\bmod 8\in\{5,6\}\) for \(k\le 8\), but at \(k=9\) xor \(=1\)
while want \(=0\). It also dies at \(k=10\) (xor \(=1\), want
\(=0\)). Prefix NJ \(q=10\) for \(k\le 8\); walk \(k=9\) and
\(k=10\). Companion NY high \(S\) and OD \(2U\le n<3U\) death still
hold at those \(k\). This is **not** empty (\(k=9\):
\(n_{\mathrm{hi}72}=3235\)), **not** pointwise \(0\) (\(k=9\):
\(n_{\mathrm{hi}72g}=1211\)), **not** NY high \(S\) (\(k=5\):
\(1\) vs \(0\)), **not** NH \(2U\le n<3U\) (\(k=6\): \(1\) vs
\(0\)), **not** NI \(2U\le n<5U/2\) (\(k=5\): \(1\) vs \(0\)),
**not** rest (\(k=5\): \(1\) vs \(0\)), **not** NA \(S\) (\(k=5\):
\(1\) vs \(0\)), **not** the form through \(k\le 10\), and **not**
the form for all \(k\). Do **not** claim \(T\) is \(1\) iff
\(k=2\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_oe.py --certify`.
Dump: `research/cycle_oe.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/NJ/NE/NH/NI/OD/MJ (packed-free covering \(q=10\); prefix NJ
\(n\ge 7U/2\) for \(k\le 8\); walk \(k=9,10\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(n\ge 7U/2\) dies at \(k=9\))

Covering \(q=10\). The walk does not read the packed row. Same
cells as Cycle NJ. At \(k=8\), \(n_{\mathrm{hi}72}=874\) and xor
\(=0=\) want. At \(k=9\), \(n_{\mathrm{hi}72}=3235\) and xor
\(=1\neq 0=\) want, with \(n_{\mathrm{hi}72g}=1211\) fires. At
\(k=10\), \(n_{\mathrm{hi}72}=9688\) and xor \(=1\neq 0=\) want.
Companion high \(S\) still matches Cycle NY; the \(2U\le n<3U\)
slice still dies as in Cycle OD.

## Killed

Holds at \(k=9\): xor \(=1\neq\) want. Holds at \(k=10\): xor
\(=1\neq\) want. The form through \(k\le 10\). Equals NY high
\(S\): \(k=5\) is \(1\) vs \(0\). Equals NH \(2U\le n<3U\):
\(k=6\) is \(1\) vs \(0\). Equals NI \(2U\le n<5U/2\): \(k=5\) is
\(1\) vs \(0\). Equals NA \(S\): \(k=5\) is \(1\) vs \(0\). Equals
rest: \(k=5\) is \(1\) vs \(0\). Empty: \(k=9\) has
\(n_{\mathrm{hi}72}=3235\). Pointwise \(0\): \(k=9\) has
\(n_{\mathrm{hi}72g}=1211\). The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(n\ge 7U/2\) dies at \(k=9\) on \(q=10\); it
dies at \(k=10\); that form holds on \(q=10\) for \(k\le 8\);
\(S\) on \(2U\le n<3U\) dies at \(k=9\) on \(q=10\); rest10 census
on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (holds at \(k=9\); holds at \(k=10\); the form through
\(k\le 10\); equals NY high \(S\); equals NH \(2U\le n<3U\);
equals NI \(2U\le n<5U/2\); equals NA \(S\); equals rest; empty;
pointwise \(0\); the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oe.md` (this note)
- `research/cycle_oe.py`
- `research/cycle_oe.json`
