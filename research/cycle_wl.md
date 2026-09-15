# Cycle WL: unpaired xor 4-way is identically large

Unpaired Green cells cannot sit on \(n\le 5U/2\): the palindrome
partner is \(2n-j\le 2n\le 5U\), so \(\mathrm{pal\_kind}\) is never
\(\mathrm{unp}\). Unpaired xor \(n_{\mathrm{ug}}/n_{\mathrm{gu}}\),
clip-edge \(\mathrm{clip\_gp}\), and \(j=0\) unpaired therefore all
lie on \(n>5U/2\). The 4-way split is
\[
(n_{\mathrm{ug},s},n_{\mathrm{ug},l},n_{\mathrm{gu},s},n_{\mathrm{gu},l})
=(0,n_{\mathrm{ug}},0,n_{\mathrm{gu}}),
\]
and likewise \(\mathrm{gp}_s=0\), \(\mathrm{gp}_l=\mathrm{clip\_gp}\),
\(\mathrm{neg}_s=0\), \(\mathrm{neg}_l=j{=}0\) unpaired. Dies at
\(k=8\) for \(\mathrm{ug}_s\) equals tot \(n_{\mathrm{ug}}\) (got
\(0\), not \(4924\)), \(\mathrm{gu}_s\) equals tot \(n_{\mathrm{gu}}\)
(got \(0\), not \(4818\)), \(\mathrm{gp}_s\) equals \(\mathrm{clip\_gp}\)
(got \(0\), not \(85\)), \(\mathrm{neg}_s\) equals \(j=0\) unpaired
(got \(0\), not \(192\)), \(\mathrm{ug}_l\) equals \(0\) (got \(4924\),
not \(0\)), \(\mathrm{pal\_kind}\) at \(n=5U/2\), \(j=0\) unpaired
(it is pair), \(\mathrm{pal\_kind}\) at \(n=1\) unpaired, and
\(\mathrm{pal\_kind}\) at \(n=639\) unpaired. Do **not** kill
\(\mathrm{pal\_kind}\) at \(n=4U-1\) unpaired: that cell is
\(\mathrm{unp}\). Census \(k=8\): \(\mathrm{ug}_s\) \(0\),
\(\mathrm{ug}_l\) \(4924\), \(\mathrm{gu}_s\) \(0\), \(\mathrm{gu}_l\)
\(4818\), \(\mathrm{gp}_s\) \(0\), \(\mathrm{gp}_l\) \(85\),
\(\mathrm{neg}_s\) \(0\), \(\mathrm{neg}_l\) \(192\). Do **not**
PREFIX pal-center tot from small \(k\). Do **not** PREFIX leftover
spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not**
catalogue leftover \(d\). Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_wl.py --certify` (~0.34s).
Dump: `research/cycle_wl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UA/UB/UC/UD/UE/UH/UP/UR/UU/UV/UW/UZ/VA/VR/WE/WH/WJ/WK
(unpaired 4-way identically large; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(\mathrm{pal\_kind}\) is never \(\mathrm{unp}\) for \(n\le 5U/2\))

Partner \(2n-j\le 2n\le 5U\), so the cell is pair or pal-center.
Equality \(n=5U/2\) still has partner \(\le 5U\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=8\) for unpaired at \(n=5U/2\), at \(n=1\), and at
\(n=639\). Do **not** kill unpaired at \(n=4U-1\).

## Lemma (unpaired xor 4-way small halves are \(0\))

\(n_{\mathrm{ug},s}=n_{\mathrm{gu},s}=\mathrm{gp}_s=\mathrm{neg}_s=0\)
for every \(k\). Large halves equal Cycle WK \(n_{\mathrm{ug}}/n_{\mathrm{gu}}\),
Cycle UB \(\mathrm{clip\_gp}\), and Cycle UA \(j=0\) unpaired.
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=8\) for \(\mathrm{ug}_s=n_{\mathrm{ug}}\);
\(\mathrm{gu}_s=n_{\mathrm{gu}}\); \(\mathrm{gp}_s=\mathrm{clip\_gp}\);
\(\mathrm{neg}_s=j{=}0\) unpaired; \(\mathrm{ug}_l=0\). Do **not**
PREFIX pal-center tot.

## Verdict

`LEMMA` (\(\mathrm{pal\_kind}\) never \(\mathrm{unp}\) for
\(n\le 5U/2\); unpaired xor / clip_gp / \(j=0\) unpaired 4-way
small halves identically \(0\); large halves equal the tots).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(\mathrm{ug}_s=n_{\mathrm{ug}}\) at \(k=8\);
\(\mathrm{gu}_s=n_{\mathrm{gu}}\); \(\mathrm{gp}_s=\mathrm{clip\_gp}\);
\(\mathrm{neg}_s=j{=}0\) unpaired; \(\mathrm{ug}_l=0\);
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2\); at \(n=1\); at
\(n=639\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_wl.md` (this note)
- `research/cycle_wl.py`
- `research/cycle_wl.json`
