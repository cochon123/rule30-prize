# Cycle WM: covering \(j=0\) unpaired is exactly \(n\in(5U/2,4U)\)

\(\mathrm{pal\_kind}(n,0)\) is unpaired iff \(2n>5U\) iff \(n>5U/2\).
On covering \(n<4U\) those cells are \(n=5U/2+1,\ldots,4U-1\). The
odd count is Cycle UA \(3\cdot 2^{k-2}\) for \(k\ge 2\). The even
count is \(3\cdot 2^{k-2}-1\) for \(k\ge 2\); special-case \(1\) at
\(k=1\); \(0\) at \(k\le 0\). The tot is \(3\cdot 2^{k-1}-1\) for
\(k\ge 2\). For \(k\ge 2\) the even leftover \(j=0\) small plus this
even unpaired plus the three special even \(n\le 5U/2\) (\(n=0\)
pal-center, \(n=2\) \(d=2\), \(n=5U/2\) clip-edge) equals \(2U\).
Dies at \(k=2\) without the even \(-1\) (got \(3\), not \(2\)). Dies
at \(k=8\) without the even \(-1\) (got \(192\), not \(191\)), for
even equals odd (got \(191\), not \(192\)), even equals leftover
\(j=0\) small (got \(191\), not \(318\)), tot equals odd (got
\(383\), not \(192\)), \(\mathrm{pal\_kind}\) at \(n=5U/2\) unpaired
(it is pair), at \(n=1\) unpaired, and at \(n=0\) unpaired. Do
**not** kill unpaired at \(n=5U/2+1\) or \(n=4U-1\). Census \(k=8\):
even \(191\), odd \(192\), tot \(383\). Do **not** PREFIX pal-center
tot from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
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

Certify: `python3 research/cycle_wm.py --certify`.
Dump: `research/cycle_wm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WL
(\(j=0\) unpaired window; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering \(j=0\) is unpaired iff \(n\in(5U/2,4U)\))

\(\mathrm{pal\_kind}(n,0)\) is unpaired iff \(2n>5U\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=8\) for unpaired at \(n=5U/2\); at \(n=1\); at
\(n=0\). Do **not** kill unpaired at \(n=5U/2+1\) or \(n=4U-1\).

## Lemma (even \(j=0\) unpaired is \(3\cdot 2^{k-2}-1\) for \(k\ge 2\))

Special-case \(1\) at \(k=1\); \(0\) at \(k\le 0\). Odd count is
Cycle UA. Tot is \(3\cdot 2^{k-1}-1\) for \(k\ge 2\). Even leftover
small plus even unpaired plus 3 equals \(2U\) for \(k\ge 2\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=2\) without \(-1\); at \(k=8\) without \(-1\);
even equals odd; even equals leftover small; tot equals odd. Do
**not** PREFIX pal-center tot.

## Verdict

`LEMMA` (covering \(j=0\) unpaired is the window \(n\in(5U/2,4U)\);
even count \(3\cdot 2^{k-2}-1\) for \(k\ge 2\); tot
\(3\cdot 2^{k-1}-1\); even leftover small plus even unpaired plus 3
equals \(2U\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even form without \(-1\) at \(k=2\); without \(-1\) at
\(k=8\); even equals odd; even equals leftover small; tot equals
odd; unpaired at \(n=5U/2\); at \(n=1\); at \(n=0\); pal-center tot
equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_wm.md` (this note)
- `research/cycle_wm.py`
- `research/cycle_wm.json`
