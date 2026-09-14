# Cycle VA: odd-\(j\) leftover equals even leftover; extra small \(n_3-n_1\) is \(d_{2e}^{\mathrm{small}}\)

Odd-\(j\) leftover pal-pairs on odd covering match even leftover on
each half, so odd-\(j\) leftover tot equals \(\mathrm{lo}_e\). Even
leftover on \(n<5U/2\) is the \(G\)-copy of parent even leftover
small, leftover extra small, odd-\(j\) leftover small, and small
\(d=2\), hence
\(\mathrm{sm}(k)=2\mathrm{sm}(k-1)+2d_{2e}^{\mathrm{small}}(k-1)+\mathrm{lo\_small}(k-1)\)
for \(k\ge 4\), matching \(\mathrm{lo}_e-e_{\ge}\). Leftover extra
small \((n\equiv 3\) minus \(n\equiv 1)\) equals \(d_{2e}^{\mathrm{small}}\)
for \(k\ge 3\). Dies at \(k=3\) for the \(2d_{2e}\) small recurrence
(\(d_{2o}\ne d_{2e}\) at \(k=2\); count \(17\), not \(19\)). Dies at
\(k=2\) for extra small \(n_3-n_1\). Census \(k=8\):
\(\mathrm{sm}=8790\); leftover extra small \(n\equiv 1/3\) is
\(5440/5546\). Do **not** PREFIX pal-center tot from small \(k\).
Do **not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_va.py --certify` (~0.54s).
Dump: `research/cycle_va.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UK/UL/UN/UP/UR/UU/UV/UW/UY/UZ
(even leftover small \(G\)-copy, odd-\(j\) leftover tot, leftover extra
small \(n_3-n_1\); no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (odd-\(j\) leftover equals even leftover on each half)

Odd-\(j\) leftover pal-pairs on odd covering match \(\mathrm{sm}\) on
\(n\le 5U/2\) and \(e_{\ge}\) on \(n>5U/2\). Tot equals
\(\mathrm{lo}_e\). Status: **lemma**. Census through \(k\le 8\).

## Lemma (\(\mathrm{sm}(k)=2\mathrm{sm}(k-1)+2d_{2e}^{\mathrm{small}}(k-1)+\mathrm{lo\_small}(k-1)\) for \(k\ge 4\))

\(G\)-copy of parent even leftover small, leftover extra small,
odd-\(j\) leftover small, and small \(d=2\) both parities.
For \(k\ge 4\), parent \(d_{2o}^{\mathrm{small}}=d_{2e}^{\mathrm{small}}\).
Equals \(\mathrm{lo}_e-e_{\ge}\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\)
(count \(17\), not \(19\)).

## Lemma (leftover extra small \(n_3-n_1=d_{2e}^{\mathrm{small}}\) for \(k\ge 3\))

Hence \(n_1^{\mathrm{sm}}=(\mathrm{lo\_small}-d_{2e}^{\mathrm{small}})/2\)
and \(n_3^{\mathrm{sm}}=(\mathrm{lo\_small}+d_{2e}^{\mathrm{small}})/2\)
for \(k\ge 3\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** at \(k=2\). Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (odd-\(j\) leftover equals even leftover on each half;
\(\mathrm{sm}(k)=2\mathrm{sm}(k-1)+2d_{2e}^{\mathrm{small}}(k-1)+\mathrm{lo\_small}(k-1)\)
for \(k\ge 4\); leftover extra small \(n_3-n_1=d_{2e}^{\mathrm{small}}\)
for \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(2d_{2e}\) small recurrence at \(k=3\); extra small
\(n_3-n_1=d_{2e}\) at \(k=2\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_va.md` (this note)
- `research/cycle_va.py`
- `research/cycle_va.json`
