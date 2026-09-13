# Cycle NM: on \(q=10\) through \(k\le 10\), NL \(S\) on \(2U\le n<9U/4\) vanishes

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(2U\le n<9U/4\) (\(p=T-2j\ge 0\); no packed row) is \(0\). Prefix
Cycle NL for \(k\le 8\); walk \(k=9\) and \(k=10\). This is **not**
a death at \(k=9\) (xor \(=0\)), **not** a death at \(k=10\) (xor
\(=0\)), **not** NI through \(k\le 10\) (\(k=10\): \(0\) vs
\(1\)), **not** rest (\(k=2\): \(0\) vs \(1\)), **not** empty
(\(k=9\): \(n_{\mathrm{lo9}}=1389\)), **not** pointwise \(0\)
(\(k=9\): \(n_{\mathrm{lo9},G(j+1)=1}=560\)), **not** the form on
\(q=6\), and **not** the form for all \(k\). Do **not** claim
\(T\) is \(1\) iff \(k=2\). Do **not** claim even-\(n\) \(S\)
vanishing (freshman tautology of GL/AL). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nm.py --certify` (~8.71s).
Dump: `research/cycle_nm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/NL/NK/NI/MD (packed-free covering \(q=10\) for
\(k=9,10\); prefix NL vanish on \(k\le 8\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(2U\le n<9U/4\) vanishes through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). Cycle NL's vanish holds at \(k=9\)
and \(k=10\) (both \(0\)). The walk does not read the packed row.
Together with Cycle NL that is the lower-quarter vanish of NI's
band on the full Cycle MD rest10 range, so NI's xor through
\(k\le 10\) still lives in \([9U/4,5U/2)\).

## Killed

Dies at \(k=9\): xor \(=0\). Dies at \(k=10\): xor \(=0\). Equals
NI through \(k\le 10\): \(k=10\) is \(0\) vs \(1\). Equals rest:
\(k=2\) is \(0\) vs \(1\). Empty at \(k=9\):
\(n_{\mathrm{lo9}}=1389\). Pointwise \(0\) at \(k=9\):
\(n_{\mathrm{lo9},G(j+1)=1}=560\). The form on \(q=6\). The form
for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(2U\le n<9U/4\) vanishes on \(q=10\) for
\(k\le 10\); \(S\) on \(2U\le n<9U/4\) vanishes on \(k\le 8\);
\(S\) on \(2U\le n<5U/2\) is \(1\) iff \(k\bmod 4\in\{2,3\}\)
through \(k\le 10\); rest10 census on \(k\le 10\); \(J\) closed
form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals NI; equals
rest; empty at \(k=9\); pointwise \(0\) at \(k=9\); the form on
\(q=6\); the form for all \(k\); unique-rest xor equals \(J\);
leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nm.md` (this note)
- `research/cycle_nm.py`
- `research/cycle_nm.json`
