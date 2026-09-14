# Cycle UB: odd-\(n\) even-\(j\) unpaired is parent unpaired xor plus clip-edge

\(G(2m+1,2r)=G(m,r)\oplus G(m,r-1)\) (Cycle TW). Odd-\(n\) even-\(j\)
unpaired cells are that adjacent xor. Parent pal-pair at \(r-1\)
with \(G(m,r)=0\) stays a pal-pair at the child (leftover extra,
Cycle TW), so \(\mathrm{pair}+g_0\) is empty in unpaired extra.
Parent clip-edge pal-pair at \(r\ge 1\) with \(G(m,r-1)=0\) has
child partner past clip, and that \(g_0+\mathrm{pair}\) count is
\((J_{k+1}-1)/2\) for \(k\ge 2\). The rest is parent unpaired xor
plus \(j=0\) unpaired (Cycle UA). Do **not** claim unpaired extra
is parent unpaired xor alone. Do **not** PREFIX unpaired extra from
small \(k\). Do **not** catalogue leftover \(d\). Do **not** PREFIX
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

Certify: `python3 research/cycle_ub.py --certify`.
Dump: `research/cycle_ub.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/TZ/UA
(unpaired extra parent xor; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-\(n\) even-\(j\) unpaired is parent unpaired xor plus clip-edge)

A leftover \(\mathrm{pair}+g_0\) child stays a pal-pair. Pal-center
parents become \(d=1\) (Cycle TW). Unpaired extra is parent unpaired
adjacent xor, plus \(g_0+\mathrm{pair}\) clip-edge, plus \(j=0\).
Status: **lemma**. Census through \(k\le 8\). **Killed:** unpaired
extra is parent unpaired xor alone. **Killed:** \(\mathrm{pair}+g_0\)
nonempty in unpaired extra.

## Lemma (\(g_0+\mathrm{pair}\) unpaired extra \(=(J_{k+1}-1)/2\), \(k\ge 2\))

Clip-edge count is \(J_{k+1}\) (Cycle TB). Jacobsthal numbers
\(J_n\) for \(n\ge 1\) are odd. The unique clip-edge at \(r=0\)
folds to \(j=0\) unpaired, not \(g_0+\mathrm{pair}\). The remaining
clip-edge cells with \(G(m,r-1)=0\) have count \((J_{k+1}-1)/2\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\).

## Verdict

`LEMMA` (odd-\(n\) even-\(j\) unpaired is parent unpaired xor plus
clip-edge plus \(j=0\); \(g_0+\mathrm{pair}\) count is
\((J_{k+1}-1)/2\) for \(k\ge 2\); \(\mathrm{pair}+g_0\) empty in
unpaired extra).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired extra is parent unpaired xor alone;
\(\mathrm{pair}+g_0\) nonempty in unpaired extra; unpaired extra
empty; twice even unpaired plus extra; unpaired 2-folds parent
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

- `research/cycle_ub.md` (this note)
- `research/cycle_ub.py`
- `research/cycle_ub.json`
