# Cycle UZ: even leftover on \(n\ge 5U/2\) is the \(G\)-copy of parent leftover kinds

\(G(2m,2t)=G(m,t)\). Even leftover pal-pairs on \(n\ge 5U/2\) are that
copy of parent even leftover on \(n\ge 5U_p/2\), leftover extra large,
odd-\(j\) leftover large, and large \(d=2\) (even and odd covering).
Odd-\(j\) leftover large equals \(e_{\ge}\) at the same \(k\). Hence
\(e_{\ge}(k)=2e_{\ge}(k-1)+2d_{2e}^{\mathrm{large}}(k-1)+\mathrm{lo\_large}(k-1)\)
for \(k\ge 4\), and \(e_{\ge}(k)=n_1(k)+\mathrm{lo\_large}(k-1)\) for
\(k\ge 3\). Dies at \(k=3\) for the \(2d_{2e}\) recurrence (\(d_{2o}\ne
d_{2e}\) at \(k=2\); count \(11\), not \(9\)). Dies at \(k=2\) for
\(n_1+\mathrm{lo\_large}\). Census \(k=8\): \(e_{\ge}=5324=3290+2034\);
odd-\(j\) leftover large \(5324\). Do **not** PREFIX pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\).
Do **not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_uz.py --certify`.
Dump: `research/cycle_uz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UL/UN/UP/UQ/UR/UU/UV/UW/UX/UY
(even leftover large \(G\)-copy and odd-\(j\) leftover large; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (odd-\(j\) leftover large equals even leftover on \(n\ge 5U/2\))

Odd-\(j\) leftover pal-pairs on odd covering \(n>5U/2\) match
\(e_{\ge}(k)\). Status: **lemma**. Census through \(k\le 8\).

## Lemma (\(e_{\ge}(k)=2e_{\ge}(k-1)+2d_{2e}^{\mathrm{large}}(k-1)+\mathrm{lo\_large}(k-1)\) for \(k\ge 4\))

\(G\)-copy of parent even leftover on \(n\ge 5U_p/2\), leftover extra
large, odd-\(j\) leftover large, and large \(d=2\) both parities.
For \(k\ge 4\), parent \(d_{2o}^{\mathrm{large}}=d_{2e}^{\mathrm{large}}\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=3\) (count \(11\), not \(9\)).

## Lemma (\(e_{\ge}(k)=n_1(k)+\mathrm{lo\_large}(k-1)\) for \(k\ge 3\))

Cycle UX \(n_1=2(e_{\ge}(k-1)+d_{2e}^{\mathrm{large}}(k-1))\) for
\(k\ge 4\) matches the recurrence. Status: **lemma**. Census through
\(k\le 8\). **Killed** at \(k=2\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (odd-\(j\) leftover large equals \(e_{\ge}\);
\(e_{\ge}(k)=2e_{\ge}(k-1)+2d_{2e}^{\mathrm{large}}(k-1)+\mathrm{lo\_large}(k-1)\)
for \(k\ge 4\); \(e_{\ge}(k)=n_1(k)+\mathrm{lo\_large}(k-1)\) for
\(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(2d_{2e}\) recurrence at \(k=3\); \(n_1+\mathrm{lo\_large}\)
at \(k=2\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_uz.md` (this note)
- `research/cycle_uz.py`
- `research/cycle_uz.json`
