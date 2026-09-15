# Cycle WJ: unpaired xor tot \(\mathrm{xor\_unp}\) F/L closed form

Unpaired extra parent-xor sum \(n_{\mathrm{ug}}+n_{\mathrm{gu}}\).
For \(k\ge 2\)
\[
\mathrm{xor\_unp}=\frac{2^{k-2}(28 L_{k-1}+60 F_{k-1}-70)+5(-1)^k+7}{10}.
\]
Special-case \(0\) at \(k\le 1\). Equals extra_unp minus clip-edge
\(g_0+\mathrm{pair}\) minus \(j=0\) unpaired. Equals leftover-plus-
unpaired xor tot minus leftover xor tot. \(n_{\mathrm{ug}}\) and
\(n_{\mathrm{gu}}\) are \((\mathrm{xor\_unp}\pm(n_{\mathrm{ug}}-n_{\mathrm{gu}}))/2\).
Dies at \(k=2\) for the F/L form with shift \(0\) (got \(1\), not
\(3\)). Dies at \(k=8\) without the \(2^{k-2}\) (got \(1\), not
\(9742\)), without the \(5(-1)^k\) (got \(9741\), not \(9742\)),
and without the \(+7\) (got \(9741\), not \(9742\)). Do **not**
kill the sign at \(k=7\): floor-div masks (\(2925=2925\)). Dies at
\(k=8\) for \(\mathrm{xor\_unp}\) equals extra_unp (got \(9742\),
not \(10019\)), equals leftover xor tot (got \(9742\), not
\(17311\)), and equals xor tot (got \(9742\), not \(27053\)).
Census \(k=8\): \(\mathrm{xor\_unp}\) \(9742\), \(n_{\mathrm{ug}}\)
\(4924\), \(n_{\mathrm{gu}}\) \(4818\). Do **not** PREFIX pal-center
tot from small \(k\). Do **not** PREFIX leftover spat tot. Do
**not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue
leftover \(d\). Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_wj.py --certify`.
Dump: `research/cycle_wj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UH/UJ/UP/UR/UU/UV/UW/UZ/VA/VP/VR/WE/WH/WI
(\(\mathrm{xor\_unp}\) F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(\mathrm{xor\_unp}\) is \((2^{k-2}(28 L_{k-1}+60 F_{k-1}-70)+5(-1)^k+7)/10\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=2\) for
shift \(0\); without \(2^{k-2}\) at \(k=8\); without \(5(-1)^k\) at
\(k=8\); without \(+7\) at \(k=8\); equals extra_unp; equals leftover
xor tot; equals xor tot. Do **not** kill the sign at \(k=7\).

## Lemma (\(\mathrm{xor\_unp}\) is extra_unp minus clip_gp minus \(j=0\) unpaired)

Status: **lemma**. Algebra through \(k\le 64\). Equals xor tot minus
leftover xor tot.

## Lemma (\(n_{\mathrm{ug}}\) and \(n_{\mathrm{gu}}\) are \((\mathrm{xor\_unp}\pm(n_{\mathrm{ug}}-n_{\mathrm{gu}}))/2\))

Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (\(\mathrm{xor\_unp}\) F/L closed form for \(k\ge 2\);
equals extra_unp minus clip_gp minus \(j=0\) unpaired; equals xor
tot minus leftover xor tot; \(n_{\mathrm{ug}}/n_{\mathrm{gu}}\)
halves).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (F/L form at \(k=2\) with shift \(0\); without \(2^{k-2}\)
at \(k=8\); without \(5(-1)^k\) at \(k=8\); without \(+7\) at
\(k=8\); \(\mathrm{xor\_unp}\) equals extra_unp; equals leftover xor
tot; equals xor tot; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_wj.md` (this note)
- `research/cycle_wj.py`
- `research/cycle_wj.json`
