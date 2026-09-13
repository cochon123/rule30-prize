# Cycle OF: on \(q=10\) through \(k\le 10\), NA's \(S\) on \(3U/2\le n<2U\) is \(1\) iff \(k>0\) and \(k\bmod 4\in\{0,3\}\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(3U/2\le n<2U\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff
\(k>0\) and \(k\bmod 4\in\{0,3\}\). Complementary low-high slice of
Cycle NY's \(n\ge 3U/2\); disjoint from NH \(2U\le n<3U\) and NJ
\(n\ge 7U/2\). This is **not** a death at \(k=9\), **not** a death
at \(k=10\), **not** NY high \(S\) (\(k=3\): \(1\) vs \(0\)),
**not** NH \(2U\le n<3U\) (\(k=2\): \(0\) vs \(1\)), **not** NJ
\(n\ge 7U/2\) (\(k=5\): \(0\) vs \(1\)), **not** rest (\(k=3\):
\(1\) vs \(0\)), **not** OA \(n<U\) (\(k=3\): \(1\) vs \(0\)),
**not** identically \(0\) (\(k=3\): \(1\)), **not** empty
(\(k=9\): \(n_{\mathrm{lohi}}=5315\)), **not** pointwise \(0\)
(\(k=9\): \(n_{\mathrm{lohig}}=2522\)), **not** the form on
\(q=6\) (\(k=7\): xor \(=0\), want \(=1\)), and **not** the form
for all \(k\). Do **not** claim \(T\) is \(1\) iff \(k=2\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_of.py --certify` (~8.46s).
Dump: `research/cycle_of.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OE/NY/NE/NH/NJ/NC/MJ (packed-free covering \(q=10\); walk
\(k\le 10\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (\(S\) on \(3U/2\le n<2U\) is \(1\) iff \(k>0\) and \(k\bmod 4\in\{0,3\}\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. At \(k=3\), \(n_{\mathrm{lohi}}=1\) and xor \(=1\). At
\(k=8\), \(n_{\mathrm{lohi}}=1761\) and xor \(=1\). At \(k=9\),
\(n_{\mathrm{lohi}}=5315\) and xor \(=0\) with
\(n_{\mathrm{lohig}}=2522\) fires. Companion NY high \(S\) still
holds; NH \(2U\le n<3U\) and NJ \(n\ge 7U/2\) still die at
\(k=9\).

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=0=\)
want. Equals NY high \(S\): \(k=3\) is \(1\) vs \(0\). Equals NH
\(2U\le n<3U\): \(k=2\) is \(0\) vs \(1\). Equals NJ \(n\ge 7U/2\):
\(k=5\) is \(0\) vs \(1\). Equals OA \(n<U\): \(k=3\) is \(1\) vs
\(0\). Equals rest: \(k=3\) is \(1\) vs \(0\). Vanishes
identically: \(k=3\) is \(1\). Empty: \(k=9\) has
\(n_{\mathrm{lohi}}=5315\). Pointwise \(0\): \(k=9\) has
\(n_{\mathrm{lohig}}=2522\). The form on \(q=6\): \(k=7\) xor
\(=0\). The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(3U/2\le n<2U\) is \(1\) iff \(k>0\) and
\(k\bmod 4\in\{0,3\}\) on \(q=10\) for \(k\le 10\); \(S\) on
\(n\ge 3U/2\) is \(1\) iff \(k\bmod 8\in\{4,6\}\) on \(q=10\) for
\(k\le 10\); \(S\) on \(n\ge 7U/2\) dies at \(k=9\) on \(q=10\);
rest10 census on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals NY high \(S\);
equals NH \(2U\le n<3U\); equals NJ \(n\ge 7U/2\); equals OA
\(n<U\); equals rest; vanishes identically; empty; pointwise \(0\);
the form on \(q=6\); the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_of.md` (this note)
- `research/cycle_of.py`
- `research/cycle_of.json`
