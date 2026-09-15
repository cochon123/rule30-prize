# Cycle WO: covering \(n=5U/2+1\) is the unique \(j=0\) partner-\(5U+2\) cell

Covering \(n=5U/2+1\) has \(2n=5U+2\), so \(j=0\) is unpaired with
that partner. Even-\(j\) unpaired extra there is exactly \(j=0\);
odd-\(j\) unpaired is exactly \(j=1\). The parent is clip-edge
\(n=5U_p/2\), which has no unpaired cells, so
\(n_{\mathrm{ug}}=n_{\mathrm{gu}}=n_{\mathrm{gp}}=0\) at this \(n\).
Leftover+pal left Green is the 11-set
\(\{U/2,U/2+1,U/2+2,U,U+1,U+2,2U,2U+1,2U+2,5U/2,n\}\) for
\(k\ge 3\). Dies at \(k=2\) for the 11-set (got \(6\), not \(11\))
and for \(G(n,2)=1\) (got \(0\)). Dies at \(k=8\) for leftover+pal
equals \(\mathrm{clip\_gp}\) (got \(11\), not \(85\)) and equals
\(j=0\) odd unpaired (got \(11\), not \(192\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+1\), \(j=0\) or \(j=1\).
Census \(k=8\): even unpaired \(1\), odd unpaired \(1\),
leftover+pal \(11\), clip \(1\). Do **not** PREFIX pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\).
Do **not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_wo.py --certify` (~0.14s).
Dump: `research/cycle_wo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN
(\(n=5U/2+1\) partner \(5U+2\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(n=5U/2+1\) is the unique covering time with \(2n=5U+2\))

For \(k\ge 1\), \(j=0\) is unpaired with partner \(5U+2\), and is
not clip-edge. Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** for \(\mathrm{pal\_kind}\)
pair at this cell.

## Lemma (even-\(j\) unpaired extra at \(n=5U/2+1\) is exactly \(j=0\))

Odd-\(j\) unpaired is exactly \(j=1\) for \(k\ge 2\). Parent
clip-edge \(n=5U_p/2\) has no unpaired cells, so
\(n_{\mathrm{ug}}=n_{\mathrm{gu}}=n_{\mathrm{gp}}=0\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** for even unpaired equals \(0\); for \(n_{\mathrm{ug}}=1\);
for even unpaired equals \(2\); for odd unpaired at \(k=1\). Do
**not** kill unpaired at \(j=0\) or \(j=1\).

## Lemma (leftover+pal at \(n=5U/2+1\) is the 11-set for \(k\ge 3\))

The cells are \(\{U/2,U/2+1,U/2+2,U,U+1,U+2,2U,2U+1,2U+2,5U/2,n\}\).
Doubling from Cycle UR's three leftover pal-pairs at parent
\(n=5U_p/2\). Special-case \(6\) at \(k=2\); \(1\) at \(k\le 1\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=2\) for equals \(11\); at \(k=2\) for
\(G(n,2)=1\); at \(k=8\) for equals \(\mathrm{clip\_gp}\); equals
\(j=0\) odd unpaired. Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (\(n=5U/2+1\) has partner \(5U+2\) at \(j=0\); even-\(j\)
unpaired extra is \(1\); odd-\(j\) unpaired is \(1\) for \(k\ge 2\);
\(n_{\mathrm{ug}}=n_{\mathrm{gu}}=n_{\mathrm{gp}}=0\); leftover+pal
is the 11-set for \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (11-set at \(k=2\); \(G(n,2)=1\) at \(k=2\); even unpaired
equals \(0\); \(n_{\mathrm{ug}}=1\); \(j=0\) pair; leftover+pal
equals \(\mathrm{clip\_gp}\); equals \(j=0\) odd unpaired; even
unpaired equals \(2\); odd unpaired at \(k=1\); clip Green at
\(k=2\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_wo.md` (this note)
- `research/cycle_wo.py`
- `research/cycle_wo.json`
