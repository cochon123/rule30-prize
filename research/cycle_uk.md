# Cycle UK: leftover extra on \(n\le 5U/2\) is pal-left tot minus \(d=1\)

Covering \(n\le 5U/2\) cannot be unpaired: the pal-partner satisfies
\(2n-j\le 2n\le 5U\). For \(k\ge 2\) clip-edge pal-left is empty on
that half, so odd-\(n\) even-\(j\) pal-left is \(d=1\) plus leftover
extra. Pal-left tot is \(2W(5\cdot 2^{k-3})=2^{k-2}(4F_{k+1}+3F_{k-1})\)
from \(\mathrm{wt}(2^{a+2}+p)=3\,\mathrm{wt}(p)\). Large-\(n\) \(d=1\)
is \(2^{k-1}-(-1)^k\). Do **not** PREFIX leftover extra on \(n>5U/2\)
or unpaired extra or \(n_{pg}+n_{gp}\) or \(n_{ug}+n_{gu}\) from
small \(k\). Do **not** PREFIX leftover extra or unpaired extra
separately as a single closed form. Do **not** catalogue leftover
\(d\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
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

Certify: `python3 research/cycle_uk.py --certify`.
Dump: `research/cycle_uk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UJ
(small-n pal-left tot from \(W(5\cdot 2^a)\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-\(n\) even-\(j\) pal-left tot on \(n\le 5U/2\) is \(2^{k-2}(4F_{k+1}+3F_{k-1})\) for \(k\ge 2\))

Freshman: \((1+x+x^2)^{2^{a+2}}=1+x^{2^{a+2}}+x^{2^{a+3}}\). For
\(p<2^a\) the three copies of \(Q_p\) do not overlap, so
\(\mathrm{wt}(2^{a+2}+p)=3\,\mathrm{wt}(p)\) and
\(W(5\cdot 2^a)=2^a(4F_{a+4}+3F_{a+2})\). For \(k\ge 3\) the small
half has \(5\cdot 2^{k-2}\) odd-clock parents and tot
\(2W(5\cdot 2^{k-3})\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed:** small tot equals
half of Cycle UC's pal-left tot.

## Lemma (leftover extra on \(n\le 5U/2\) is small tot minus small \(d=1\))

Unpaired is empty on \(n\le 5U/2\). Clip-edge pal-left is empty
there for \(k\ge 2\). So leftover extra on the unpaired-free half
is pal-left tot minus \(d=1\). Large \(d=1\) is
\(2^{k-1}-(-1)^k\) for \(k\ge 2\), and small \(d=1\) is
\((5\cdot 2^{k-1}+2(-1)^k)/3\). Large leftover extra plus unpaired
extra is extra-sum minus this small leftover extra. Status:
**lemma**. **Killed:** leftover extra equals the small-n count.
**Killed:** small leftover extra equals extra-sum. Do **not**
PREFIX leftover extra on \(n>5U/2\) or unpaired extra.

## Verdict

`LEMMA` (small pal-left tot is \(2^{k-2}(4F_{k+1}+3F_{k-1})\);
leftover extra on \(n\le 5U/2\) is that tot minus small \(d=1\);
large \(d=1\) is \(2^{k-1}-(-1)^k\); \(W(5\cdot 2^a)=2^a(4F_{a+4}+3F_{a+2})\);
large leftover-plus-unpaired extra is extra-sum minus small leftover extra).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (small leftover extra equals leftover extra; small tot equals
half of pal-left tot; small \(d=1\) equals large \(d=1\); small leftover
extra equals extra-sum; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_uk.md` (this note)
- `research/cycle_uk.py`
- `research/cycle_uk.json`
