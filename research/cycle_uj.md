# Cycle UJ: leftover xor-pair plus unpaired xor-unp is extra-sum minus edges

Leftover extra is parent pal-pair xor plus \(j=0\) leftover (Cycle TW).
Unpaired extra is parent unpaired xor plus clip-edge plus \(j=0\)
unpaired (Cycle UB). Extra-sum is closed (Cycle UC). Subtracting the
three known edges leaves leftover xor-pair sum plus unpaired xor-unp
sum. Do **not** PREFIX \(n_{pg}+n_{gp}\) or \(n_{ug}+n_{gu}\) from
small \(k\). Do **not** PREFIX leftover extra or unpaired extra
separately. Do **not** catalogue leftover \(d\). Do **not** PREFIX
leftover spat tot. Do **not** PREFIX pal-center tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim pal-center tot
equals \(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_uj.py --certify` (~0.35s).
Dump: `research/cycle_uj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/TW/UA/UB/UC/UD/UE/UH/UI
(xor-tot from extra-sum minus edges; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (xor-pair plus xor-unp \(=\) extra-sum minus \(j=0\) leftover minus clip-edge minus \(j=0\) unpaired)

Cycle TW leftover extra \(=\) xor-pair \(+\) \(j=0\) leftover. Cycle
UB unpaired extra \(=\) xor-unp \(+\) clip-edge \(+\) \(j=0\) unpaired,
and \(\mathrm{pair}+g_0\) is empty in unpaired extra. Cycle UC extra
sum is \(2^{k+1}(F_{k+2}-1)+(-1)^k\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed:** xor-tot
equals extra-sum. **Killed:** leftover xor-pair equals unpaired
xor-unp. **Killed:** xor-tot empty. Do **not** PREFIX either xor-sum.

## Verdict

`LEMMA` (leftover xor-pair plus unpaired xor-unp is extra-sum minus
\(j=0\) leftover minus clip-edge minus \(j=0\) unpaired).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (xor-tot equals extra-sum; leftover xor-pair equals unpaired
xor-unp; xor-tot empty; leftover xor-pair equals xor-tot; pal-center
tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_uj.md` (this note)
- `research/cycle_uj.py`
- `research/cycle_uj.json`
