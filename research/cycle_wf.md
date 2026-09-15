# Cycle WF: leftover-parent xor 4-way F/L closed forms

Leftover-parent xor splits by \(n\le 5U/2\) and by \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\).
For \(k\ge 3\)
\[
\mathrm{plo}_s=\frac{2^{k-3}(33 F_k-21 F_{k-2}-25)+4(-1)^{k-1}}{3}
\]
\[
\mathrm{glo}_s=\frac{2^{k-3}(33 F_k-21 F_{k-2}-50)+2(-1)^{k-1}+9}{3}
\]
\[
\mathrm{plo}_l=\frac{2^{k-3}(21 F_k+11 F_{k-2}-25)-10(-1)^{k-1}+2}{5}
\]
\[
\mathrm{glo}_l=\frac{2^{k-3}(21 F_k+11 F_{k-2}-20)-5(-1)^{k-1}-3}{5}.
\]
Small halves sum to Cycle VU leftover-parent xor small. Large
halves sum to Cycle VU leftover-parent xor large.
\(\mathrm{plo}_s+\mathrm{plo}_l\) is Cycle VX leftover-parent xor
\(n_{\mathrm{pg}}\). \(\mathrm{glo}_s+\mathrm{glo}_l\) is Cycle VX
leftover-parent xor \(n_{\mathrm{gp}}\). \(\mathrm{plo}_s=2\,\mathrm{sm}(k-1)\)
and \(\mathrm{plo}_l=2\,e_{\ge}(k-1)\) for \(k\ge 3\), not at \(k=2\).
Special-case \(\mathrm{plo}_s=\mathrm{plo}_l=1\) at \(k=2\);
\(\mathrm{glo}_s=\mathrm{glo}_l=0\) at \(k\le 2\); all \(0\) at
\(k\le 1\). Dies at \(k=3\) for all four F/L forms with shift \(0\)
(\(\mathrm{plo}_s\) got \(1\), not \(8\); \(\mathrm{glo}_s\) got
\(3\), not \(2\); \(\mathrm{plo}_l\) got \(-2\), not \(4\);
\(\mathrm{glo}_l\) got \(-2\), not \(5\)). Dies at \(k=8\) without
the \(\mathrm{plo}_s\) \(2^{k-3}\) (got \(165\), not \(5332\)),
without the \(\mathrm{plo}_s\) \(4(-1)^{k-1}\) (got \(5333\), not
\(5332\)), without the \(\mathrm{glo}_s\) \(+9\) (got \(5066\), not
\(5069\)), without the \(\mathrm{plo}_l\) \(+2\) (got \(3227\), not
\(3228\)), without the \(\mathrm{plo}_l\) \(-10(-1)^{k-1}\) (got
\(3226\), not \(3228\)), and without the \(\mathrm{glo}_l\)
\(-5(-1)^{k-1}\) (got \(3257\), not \(3258\)). Dies at \(k=7\)
without the \(\mathrm{glo}_s\) \(2(-1)^{k-1}\) (got \(1464\), not
\(1465\)). Do **not** kill \(\mathrm{glo}_s\) sign at \(k=8\) or
\(\mathrm{glo}_l\) \(-3\) at \(k=8\): floor-div masks them. Dies at
\(k=2\) for \(2\,\mathrm{sm}(k-1)\) (\(\mathrm{plo}_s\) got \(1\),
not \(2\)) and \(2\,e_{\ge}(k-1)\) (\(\mathrm{plo}_l\) got \(1\),
not \(0\)). Dies at \(k=8\) for \(\mathrm{plo}_s\) equals tot small
(got \(5332\), not \(10401\)), \(\mathrm{plo}_s\) equals tot
\(n_{\mathrm{pg}}\) (got \(5332\), not \(8560\)), and
\(\mathrm{plo}_s\) equals \(\mathrm{glo}_s\) (got \(5332\), not
\(5069\)). Census \(k=8\): \(\mathrm{plo}_s\) \(5332\),
\(\mathrm{glo}_s\) \(5069\), \(\mathrm{plo}_l\) \(3228\),
\(\mathrm{glo}_l\) \(3258\). Do **not** PREFIX pal-center tot from
small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why
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

Certify: `python3 research/cycle_wf.py --certify`.
Dump: `research/cycle_wf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UO/UP/UR/UU/UV/UW/UZ/VA/VU/VX/WE
(leftover-parent xor 4-way F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover-parent xor small \(n_{\mathrm{pg}}\) is \((2^{k-3}(33 F_k-21 F_{k-2}-25)+4(-1)^{k-1})/3\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Equals
\(2\,\mathrm{sm}(k-1)\) for \(k\ge 3\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for the F/L form with shift \(0\); without \(2^{k-3}\) at
\(k=8\); without \(4(-1)^{k-1}\) at \(k=8\); \(2\,\mathrm{sm}(k-1)\)
at \(k=2\); small equals tot at \(k=8\); small equals tot
\(n_{\mathrm{pg}}\) at \(k=8\); \(\mathrm{plo}_s=\mathrm{glo}_s\)
at \(k=8\).

## Lemma (leftover-parent xor small \(n_{\mathrm{gp}}\) is \((2^{k-3}(33 F_k-21 F_{k-2}-50)+2(-1)^{k-1}+9)/3\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). The two small halves sum to
leftover-parent xor small. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
the F/L form with shift \(0\); without \(+9\) at \(k=8\); without
\(2(-1)^{k-1}\) at \(k=7\).

## Lemma (leftover-parent xor large \(n_{\mathrm{pg}}\) is \((2^{k-3}(21 F_k+11 F_{k-2}-25)-10(-1)^{k-1}+2)/5\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Equals
\(2\,e_{\ge}(k-1)\) for \(k\ge 3\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for the F/L form with shift \(0\); without \(+2\) at
\(k=8\); without \(-10(-1)^{k-1}\) at \(k=8\); \(2\,e_{\ge}(k-1)\)
at \(k=2\).

## Lemma (leftover-parent xor large \(n_{\mathrm{gp}}\) is \((2^{k-3}(21 F_k+11 F_{k-2}-20)-5(-1)^{k-1}-3)/5\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). The two large halves sum to
leftover-parent xor large. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
the F/L form with shift \(0\); without \(-5(-1)^{k-1}\) at \(k=8\).
Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover-parent xor 4-way F/L closed forms for \(k\ge 3\);
halves sum to leftover-parent xor small/large and leftover-parent
xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\); \(\mathrm{plo}_s=2\,\mathrm{sm}(k-1)\)
and \(\mathrm{plo}_l=2\,e_{\ge}(k-1)\) for \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (all four F/L forms at \(k=3\) with shift \(0\); without
\(\mathrm{plo}_s\) \(2^{k-3}\); without \(\mathrm{plo}_s\) sign;
without \(\mathrm{glo}_s\) \(+9\); without \(\mathrm{glo}_s\) sign
at \(k=7\); without \(\mathrm{plo}_l\) \(+2\); without
\(\mathrm{plo}_l\) sign; without \(\mathrm{glo}_l\) sign at \(k=8\);
\(2\,\mathrm{sm}\) at \(k=2\); \(2\,e_{\ge}\) at \(k=2\);
\(\mathrm{plo}_s\) equals tot small; \(\mathrm{plo}_s\) equals tot
\(n_{\mathrm{pg}}\); \(\mathrm{plo}_s=\mathrm{glo}_s\); pal-center
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

- `research/cycle_wf.md` (this note)
- `research/cycle_wf.py`
- `research/cycle_wf.json`
