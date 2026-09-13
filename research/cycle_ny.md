# Cycle NY: on \(q=10\) through \(k\le 10\), NA's \(S\) on \(n\ge 3U/2\) is \(1\) iff \(k\bmod 8\in\{4,6\}\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(n\ge 3U/2\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff
\(k\bmod 8\in\{4,6\}\). Lift of Cycle NE (\(k\le 8\)). Prefix NE
\(q=10\) for \(k\le 8\); walk \(k=9\) and \(k=10\). Companion NC
\(n<U\) and ND mid still hold at those \(k\). This is **not** a
death at \(k=9\), **not** a death at \(k=10\), **not** rest
(\(k=4\): \(1\) vs \(0\)), **not** NC \(n<U\) (\(k=6\): \(1\) vs
\(0\)), **not** NA \(S\) (\(k=4\): \(1\) vs \(0\)), **not** ND mid
(\(k=4\): \(1\) vs \(0\)), **not** identically \(0\) (\(k=4\):
\(1\)), **not** empty (\(k=9\): \(n_{\mathrm{hi}}=21245\)), **not**
pointwise \(0\) (\(k=9\): \(n_{\mathrm{hig}}=8898\)), **not** the
form on \(q=6\), and **not** the form for all \(k\). Do **not**
claim \(T\) is \(1\) iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_ny.py --certify` (~8.76s).
Dump: `research/cycle_ny.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/NE/NX/ND/NC/MJ (packed-free covering \(q=10\); prefix NE
high \(S\) for \(k\le 8\); walk \(k=9,10\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(n\ge 3U/2\) is \(1\) iff \(k\bmod 8\in\{4,6\}\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle NE. At \(k=4\), \(n_{\mathrm{hi}}=48\) and
xor \(=1\). At \(k=9\), \(n_{\mathrm{hi}}=21245\) and xor \(=0\)
with \(n_{\mathrm{hig}}=8898\) fires. Companion \(S\) on \(n<U\)
and on \(U\le n<3U/2\) still match Cycles NC and ND.

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=0=\)
want. Equals rest: \(k=4\) is \(1\) vs \(0\). Equals NC \(n<U\):
\(k=6\) is \(1\) vs \(0\). Equals NA \(S\): \(k=4\) is \(1\) vs
\(0\). Equals ND mid: \(k=4\) is \(1\) vs \(0\). Vanishes
identically: \(k=4\) is \(1\). Empty: \(k=9\) has
\(n_{\mathrm{hi}}=21245\). Pointwise \(0\): \(k=9\) has
\(n_{\mathrm{hig}}=8898\). The form on \(q=6\): \(k=3\) xor \(=1\).
The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(n\ge 3U/2\) is \(1\) iff \(k\bmod 8\in\{4,6\}\)
on \(q=10\) for \(k\le 10\); that form holds on \(q=10\) for
\(k\le 8\); \(S\) on \(U\le n<3U/2\) vanishes on both covering
\(q\) for \(k\le 8\); inner \(G=1\) count is odd iff \(k\) odd on
\(q=10\) for \(k\le 10\); rest10 census on \(k\le 10\); \(J\)
closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NC \(n<U\); equals NA \(S\); equals ND mid; vanishes identically;
empty; pointwise \(0\); the form on \(q=6\); the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ny.md` (this note)
- `research/cycle_ny.py`
- `research/cycle_ny.json`
