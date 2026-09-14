# Cycle TS: \(\{d=1,d=2,\mathrm{clip\text{-}edge}\}\) pair count is \(2^{k+2}\)

The three pal-pair types \(d=1\), \(d=2\), and clip-edge have total
count \(J_{k+3}+J_{k+2}=2^{k+2}\), equal to the covering-clock
count \(4U\). Clip-edge packed pal-right is \(p=0\), never forced,
and Cycle TC gives raw \(=0\) cellwise, so the triple rest tot
equals the TG-complex rest tot: raw xor \(1_{k\le 1}\). Do **not**
claim the three types partition covering \(n\) (the same \(n\) can
carry two types). Do **not** claim leftover pal-pairs are empty
(Cycle SV's unique even cell has pal-distance \(2U\)). Do **not**
catalogue leftover \(d\). Do **not** PREFIX pal-center tot. Do
**not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim pal-center
tot equals \(S\oplus T\). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover
\(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
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

Certify: `python3 research/cycle_ts.py --certify`.
Dump: `research/cycle_ts.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/PB/QV/SO/SS/SV/SX/SY/TA/TB/TC/TD/TE/TR
(triple count; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (triple pal-pair count is \(2^{k+2}\))

\(J_{k+2}+J_{k+3}=2^{k+2}\). The left side is clip-edge count plus
the Cycle TR complex count. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 12\). **Killed:** the three types
partition covering \(n\).

## Lemma (clip-edge never forced; triple rest tot equals complex rest tot)

Clip-edge pal-right is packed \(p=0\notin\{4,6,14\}\). Pal-left
packed \(p=4(5U-n)\ge 4U+4\) on covering \(n\). Cycle TC: both
sides AND \(=0\), so clip-edge rest \(=\) raw \(=0\). Triple rest
tot equals TG-complex rest tot, hence raw xor \(1_{k\le 1}\).
Status: **lemma**. Algebra through \(k\le 64\). **Killed:** leftover
pal-pairs empty.

## Verdict

`LEMMA` (triple pal-pair count is \(2^{k+2}\); clip-edge never
forced; triple rest tot equals complex rest tot).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (three types partition covering \(n\); leftover pal-pairs
empty; \(d=2\) raw tot 2-folds parent \(d=1\); pal-center tot equals
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

- `research/cycle_ts.md` (this note)
- `research/cycle_ts.py`
- `research/cycle_ts.json`
