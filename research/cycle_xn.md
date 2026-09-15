# Cycle XN: even \(n=5U/2+512\) is the 2-fold of Cycle XK at \(k-1\)

Covering \(n=5U/2+512\) equals \(2\cdot(5U_p/2+256)\). Even doubling
sends parent left Green to child left Green with
\(\mathrm{pal\_kind}\) and clip-edge preserved, so unpaired left is
\(\{0,512\}\) for \(k\ge 11\) and leftover+pal is the even 11-set
\(\{U/2,U/2+512,U/2+1024,U,U+512,U+1024,2U,2U+512,2U+1024,5U/2,n\}\)
for \(k\ge 12\). The \(j=512\) cell has partner \(5U+512\). Dies at
\(k=10\) for unpaired \(\{0,512\}\) (\(G\) at \(j=512\) is \(0\)).
Dies at \(k=11\) for leftover 11-set (got \(6\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+512\), \(j=0\) for
\(k\ge 9\) or \(j=512\) for \(k\ge 11\). Census \(k=8\): unpaired
\(0\), leftover+pal \(0\), clip \(0\) (not yet covering). Do **not**
PREFIX pal-center tot from small \(k\). Do **not** PREFIX leftover
spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not**
catalogue leftover \(d\). Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_xn.py --certify` (~0.14s).
Dump: `research/cycle_xn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/XH/XK
(even \(n=5U/2+512\) 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even \(n=5U/2+512\) is the 2-fold of Cycle XK for \(k\ge 2\))

Fold identity \(n=2\cdot\mathrm{ph256}(k-1)\). Covering
(\(n<4U\)) only for \(k\ge 9\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=8\) for
covering (\(n=1152\ge 1024\)).

## Lemma (unpaired left Green is \(\{0,512\}\) for \(k\ge 11\))

Special-case \(3\) at \(k=9\) and \(1\) at \(k=10\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=10\) for \(\{0,512\}\). Do **not** kill unpaired at
\(j=0\) for \(k\ge 9\) or at \(j=512\) for \(k\ge 11\).

## Lemma (leftover+pal is the even 11-set for \(k\ge 12\))

Special \(6\) at \(k=11\), \(1\) at \(k=10\), \(2\) at \(k=9\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=11\) for the 11-set.

## Lemma (\(j=512\) has partner \(5U+512\))

Clip-edge at \(j=1024\). Status: **lemma**. Algebra through
\(k\le 64\). **Killed** at \(k=9\) for \(\mathrm{pal\_kind}\) pair
at \(j=512\); at \(k=10\) for \(G(n,512)=1\).

## Verdict

`LEMMA` (even \(n=5U/2+512\) is 2-fold of XK; unpaired \(\{0,512\}\)
for \(k\ge 11\); leftover 11-set for \(k\ge 12\); \(j=512\) has
partner \(5U+512\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired \(\{0,512\}\) at \(k=10\); leftover 11-set at
\(k=11\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); leftover
\(=\mathrm{clip\_gp}\); unpaired equals even partner-\(5U+2\)
slice; \(\mathrm{pal\_kind}\) pair at \(j=512\);
\(G(\mathrm{ph}+512,512)=1\) at \(k=10\); covering at
\(n=5U/2+512\) at \(k=8\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_xn.md` (this note)
- `research/cycle_xn.py`
- `research/cycle_xn.json`
