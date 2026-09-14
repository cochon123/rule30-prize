# Cycle UA: unpaired count is \(2\,\mathrm{unp}(k-1)+J_{k+1}+\mathrm{extra}\)

Even unpaired count equals parent unpaired (Cycles TA/TZ). Odd
unpaired is odd-\(j\) unpaired plus the odd-\(n\) even-\(j\) extra.
Odd-\(j\) unpaired is even unpaired plus \(J_{k+1}\) (Cycle TZ), so
unpaired count is \(2\) even unpaired plus \(J_{k+1}\) plus extra
for \(k\ge 1\). Substituting even unpaired \(=\) parent unpaired
gives unpaired(\(k\))= \(2\) unpaired(\(k-1\))+ \(J_{k+1}+\) extra(\(k\))
for \(k\ge 1\). Extra is nonempty (it contains \(j=0\) unpaired on
odd \(n>5U/2\)), so the recurrence without extra fails. Do **not**
claim unpaired \(=\) twice even unpaired plus extra (that misses
\(J_{k+1}\)). Do **not** claim unpaired 2-folds parent unpaired.
Do **not** claim unpaired(\(k\))= \(2\) unpaired(\(k-1\))+ \(J_{k+1}\).
Do **not** catalogue leftover \(d\). Do **not** PREFIX leftover spat tot. Do
**not** PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat
tot. Do **not** PREFIX unpaired extra from small \(k\). Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
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

Certify: `python3 research/cycle_ua.py --certify` (~0.65s).
Dump: `research/cycle_ua.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TZ
(unpaired count recurrence; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (unpaired \(=\) twice even unpaired plus \(J_{k+1}\) plus extra, \(k\ge 1\))

Cycle TZ: odd-\(j\) unpaired \(=\) even unpaired plus \(J_{k+1}\),
and even unpaired is even-\(j\). Odd unpaired is odd-\(j\) unpaired
plus odd-\(n\) even-\(j\) unpaired. Hence unpaired count is \(2\)
even unpaired plus \(J_{k+1}\) plus extra for \(k\ge 1\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed:** unpaired equals twice even unpaired plus extra.

## Lemma (unpaired(\(k\))= \(2\) unpaired(\(k-1\))+ \(J_{k+1}+\) extra, \(k\ge 1\))

Cycle TZ: even unpaired(\(k\))= unpaired(\(k-1\)). Substitute. Extra
contains \(j=0\) unpaired on odd covering \(n>5U/2\), with count
\(1\) at \(k\le 1\) and \(3\cdot 2^{k-2}\) for \(k\ge 2\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed:** unpaired(\(k\))= \(2\) unpaired(\(k-1\))+ \(J_{k+1}\).
**Killed:** unpaired 2-folds parent unpaired.

## Verdict

`LEMMA` (unpaired count is twice even unpaired plus \(J_{k+1}\) plus
extra for \(k\ge 1\); unpaired(\(k\))= \(2\) unpaired(\(k-1\))+
\(J_{k+1}+\) extra for \(k\ge 1\); \(j=0\) odd-\(n\) unpaired count
is \(1\) then \(3\cdot 2^{k-2}\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (twice even plus extra; recurrence without extra; unpaired
2-folds parent unpaired; odd-\(n\) even-\(j\) unpaired empty; odd
unpaired equals even unpaired; odd-\(j\) unpaired equals even
unpaired; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ua.md` (this note)
- `research/cycle_ua.py`
- `research/cycle_ua.json`
