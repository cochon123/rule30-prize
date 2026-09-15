# Cycle WK: unpaired xor \(n_{\mathrm{ug}}/n_{\mathrm{gu}}\) F/L closed forms

Unpaired extra parent-xor halves. For \(k\ge 2\)
\[
n_{\mathrm{ug}}=\frac{2^{k-2}(42 L_{k-1}+90 F_{k-1}-80)+5(-1)^k+3}{30}
\]
\[
n_{\mathrm{gu}}=\frac{2^{k-2}(42 L_{k-1}+90 F_{k-1}-130)+10(-1)^k+18}{30}.
\]
Special-case \(0\) at \(k\le 1\). They sum to Cycle WJ
\(\mathrm{xor\_unp}\) and differ by Cycle UH \(n_{\mathrm{ug}}-n_{\mathrm{gu}}\).
Dies at \(k=2\) for both F/L forms with shift \(0\) (\(n_{\mathrm{ug}}\)
got \(0\), not \(2\); \(n_{\mathrm{gu}}\) got \(0\), not \(1\)). Dies
at \(k=8\) without the \(n_{\mathrm{ug}}\) \(2^{k-2}\) (got \(0\), not
\(4924\)), without the \(n_{\mathrm{ug}}\) sign (got \(4923\), not
\(4924\)), without the \(n_{\mathrm{ug}}\) \(+3\) (got \(4923\), not
\(4924\)), without the \(n_{\mathrm{ug}}\) \(-80\) (got \(5094\), not
\(4924\)), without the \(n_{\mathrm{gu}}\) \(2^{k-2}\) (got \(0\), not
\(4818\)), without the \(n_{\mathrm{gu}}\) sign (got \(4817\), not
\(4818\)), without the \(n_{\mathrm{gu}}\) \(+18\) (got \(4817\), not
\(4818\)), and without the \(n_{\mathrm{gu}}\) \(-130\) (got \(5095\),
not \(4818\)). Do **not** kill either sign at \(k=7\): floor-div
masks. Dies at \(k=8\) for \(n_{\mathrm{ug}}\) equals
\(\mathrm{xor\_unp}\) (got \(4924\), not \(9742\)), \(n_{\mathrm{ug}}\)
equals \(n_{\mathrm{gu}}\) (got \(4924\), not \(4818\)), and
\(n_{\mathrm{ug}}\) equals extra_unp (got \(4924\), not \(10019\)).
Census \(k=8\): \(n_{\mathrm{ug}}\) \(4924\), \(n_{\mathrm{gu}}\)
\(4818\). Do **not** PREFIX pal-center tot from small \(k\). Do
**not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_wk.py --certify`.
Dump: `research/cycle_wk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UH/UP/UR/UU/UV/UW/UZ/VA/VR/WE/WH/WI/WJ
(\(n_{\mathrm{ug}}/n_{\mathrm{gu}}\) F/L; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(n_{\mathrm{ug}}\) is \((2^{k-2}(42 L_{k-1}+90 F_{k-1}-80)+5(-1)^k+3)/30\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=2\) for
shift \(0\); without \(2^{k-2}\) at \(k=8\); without the sign at
\(k=8\); without \(+3\) at \(k=8\); without \(-80\) at \(k=8\);
equals \(\mathrm{xor\_unp}\); equals \(n_{\mathrm{gu}}\); equals
extra_unp. Do **not** kill the sign at \(k=7\).

## Lemma (\(n_{\mathrm{gu}}\) is \((2^{k-2}(42 L_{k-1}+90 F_{k-1}-130)+10(-1)^k+18)/30\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). The two halves sum to
\(\mathrm{xor\_unp}\) and differ by Cycle UH. Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=2\) for shift \(0\); without \(2^{k-2}\) at \(k=8\); without
the sign at \(k=8\); without \(+18\) at \(k=8\); without \(-130\) at
\(k=8\). Do **not** kill the sign at \(k=7\). Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (\(n_{\mathrm{ug}}/n_{\mathrm{gu}}\) F/L closed forms for
\(k\ge 2\); halves sum to \(\mathrm{xor\_unp}\) and differ by UH).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (both F/L forms at \(k=2\) with shift \(0\); without
\(n_{\mathrm{ug}}\) \(2^{k-2}\); without \(n_{\mathrm{ug}}\) sign;
without \(n_{\mathrm{ug}}\) \(+3\); without \(n_{\mathrm{ug}}\)
\(-80\); without \(n_{\mathrm{gu}}\) \(2^{k-2}\); without
\(n_{\mathrm{gu}}\) sign; without \(n_{\mathrm{gu}}\) \(+18\);
without \(n_{\mathrm{gu}}\) \(-130\); \(n_{\mathrm{ug}}\) equals
\(\mathrm{xor\_unp}\); \(n_{\mathrm{ug}}=n_{\mathrm{gu}}\);
\(n_{\mathrm{ug}}\) equals extra_unp; pal-center tot equals
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

- `research/cycle_wk.md` (this note)
- `research/cycle_wk.py`
- `research/cycle_wk.json`
