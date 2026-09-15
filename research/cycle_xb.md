# Cycle XB: even \(n=5U/2+32\) is the 2-fold of Cycle WY at \(k-1\)

Covering \(n=5U/2+32\) equals \(2\cdot(5U_p/2+16)\). Even doubling
sends parent left Green to child left Green with
\(\mathrm{pal\_kind}\) and clip-edge preserved, so unpaired left is
\(\{0,32\}\) for \(k\ge 7\) and leftover+pal is the even 11-set
\(\{U/2,U/2+32,U/2+64,U,U+32,U+64,2U,2U+32,2U+64,5U/2,n\}\) for
\(k\ge 8\). The \(j=32\) cell has partner \(5U+32\). Dies at \(k=6\)
for unpaired \(\{0,32\}\) (\(G\) at \(j=32\) is \(0\)). Dies at
\(k=7\) for leftover 11-set (got \(6\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+32\), \(j=0\) or
\(j=32\) for \(k\ge 7\). Census \(k=8\): unpaired \(2\),
leftover+pal \(11\), clip \(1\). Do **not** PREFIX pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover
\(d\). Do **not** claim pal-center tot equals \(S\oplus T\). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\) covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_xb.py --certify` (~0.14s).
Dump: `research/cycle_xb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WT/WY
(even \(n=5U/2+32\) 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even \(n=5U/2+32\) is the 2-fold of Cycle WY for \(k\ge 2\))

Fold identity \(n=2\cdot\mathrm{ph16}(k-1)\). Covering
(\(n<4U\)) only for \(k\ge 5\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\).

## Lemma (unpaired left Green is \(\{0,32\}\) for \(k\ge 7\))

Special-case \(3\) at \(k=5\) and \(1\) at \(k=6\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=6\) for \(\{0,32\}\). Do **not** kill unpaired at
\(j=0\) or \(j=32\) for \(k\ge 7\).

## Lemma (leftover+pal is the even 11-set for \(k\ge 8\))

Special \(6\) at \(k=7\), \(1\) at \(k=6\), \(2\) at \(k=5\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=7\) for the 11-set.

## Lemma (\(j=32\) has partner \(5U+32\))

Clip-edge at \(j=64\). Status: **lemma**. Algebra through
\(k\le 64\). **Killed** at \(k=8\) for \(\mathrm{pal\_kind}\) pair
at \(j=32\); at \(k=6\) for \(G(n,32)=1\).

## Verdict

`LEMMA` (even \(n=5U/2+32\) is 2-fold of WY; unpaired \(\{0,32\}\)
for \(k\ge 7\); leftover 11-set for \(k\ge 8\); \(j=32\) has partner
\(5U+32\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired \(\{0,32\}\) at \(k=6\); leftover 11-set at
\(k=7\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); leftover
\(=\mathrm{clip\_gp}\); unpaired equals even partner-\(5U+2\)
slice; \(\mathrm{pal\_kind}\) pair at \(j=32\);
\(G(\mathrm{ph}+32,32)=1\) at \(k=6\); pal-center tot equals
\(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_xb.md` (this note)
- `research/cycle_xb.py`
- `research/cycle_xb.json`
