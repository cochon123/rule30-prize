# Cycle NL: on \(q=10\) for \(k\le 8\), NA's \(S\) on \(2U\le n<9U/4\) vanishes

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(2U\le n<9U/4\) (\(p=T-2j\ge 0\); no packed row) is \(0\). Lower
quarter of Cycle NI's \([2U,5U/2)\), so NI's xor lives in
\([9U/4,5U/2)\). This is **not** NI (\(k=2\): \(0\) vs \(1\)),
**not** rest (\(k=2\): \(0\) vs \(1\)), **not** NE high (\(k=4\):
\(0\) vs \(1\)), **not** NJ (\(k=5\): \(0\) vs \(1\)), **not** NH
(\(k=2\): \(0\) vs \(1\)), **not** NA \(S\) (\(k=6\): \(0\) vs
\(1\)), **not** \(T\) (\(k=2\): \(0\) vs \(1\)), **not** empty
(\(k=3\): \(n_{\mathrm{lo9}}=1\)), **not** pointwise \(0\)
(\(k=4\): \(n_{\mathrm{lo9},G(j+1)=1}=2\)), **not** the form on
\(q=6\) (empty; \(k=4\) \(n_{\mathrm{lo9}}=0\) vs \(q=10\)
\(n_{\mathrm{lo9}}=3\)), **not** Green-only rest, and **not** the
form for all \(k\). Do **not** claim \(T\) is \(1\) iff \(k=2\).
Do **not** claim even-\(n\) \(S\) vanishing (freshman tautology of
GL/AL). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nl.py --certify`.
Dump: `research/cycle_nl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/NA/NE/NH/NI/NJ/NK (packed-free covering \(q=10\) for
\(k\le 8\); prefix NI \(2U\le n<5U/2\) and NK through \(k\le 10\);
\(k=4\), \(q=6\) empty kill; no Fermat table, no extra window, no
\(n_0=16\) window).

## Lemma (\(S\) on \(2U\le n<9U/4\) vanishes)

Covering \(q=10\), \(k\le 8\). The walk does not read the packed
row. At \(k=4\), \(n_{\mathrm{lo9}}=3\) and \(G(j+1)\) fires twice.
The cut \(9U/4\) is the midpoint of Cycle NI's \([2U,5U/2)\). On
\(q=6\) the band is empty (\(n<2U\)).

## Killed

Equals NI \(2U\le n<5U/2\): \(k=2\) is \(0\) vs \(1\). Equals rest:
\(k=2\), \(q=10\) is \(0\) vs \(1\). Equals NE high: \(k=4\) is
\(0\) vs \(1\). Equals NJ \(n\ge 7U/2\): \(k=5\) is \(0\) vs
\(1\). Equals NH \(2U\le n<3U\): \(k=2\) is \(0\) vs \(1\). Equals
NA \(S\): \(k=6\) is \(0\) vs \(1\). Equals \(T\): \(k=2\) is \(0\)
vs \(1\). Empty: \(k=3\) has \(n_{\mathrm{lo9}}=1\). Pointwise
\(0\): \(k=4\) has \(n_{\mathrm{lo9},G(j+1)=1}=2\). The form on
\(q=6\): empty at \(k=4\), \(n_{\mathrm{lo9}}=0\). The form for
all \(k\).

## Verdict

`LEMMA` (\(S\) on \(2U\le n<9U/4\) vanishes on \(q=10\) for
\(k\le 8\); \(S\) on \(2U\le n<5U/2\) is \(1\) iff
\(k\bmod 4\in\{2,3\}\) through \(k\le 10\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (equals NI; equals rest; equals NE high; equals NJ;
equals NH; equals NA \(S\); equals \(T\); empty; pointwise \(0\);
the form on \(q=6\); the form for all \(k\); unique-rest xor
equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nl.md` (this note)
- `research/cycle_nl.py`
- `research/cycle_nl.json`
