# Cycle WC: leftover xor 4-way F/L closed forms

Leftover xor splits by \(n\le 5U/2\) and by \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\).
For \(k\ge 3\)
\[
\mathrm{pg}_s=2^{k-3}(4 F_{k+1}+3 F_{k-1}-5)
\]
\[
\mathrm{gp}_s=\frac{2^{k-3}(12 F_{k+1}+9 F_{k-1}-35)-2(-1)^k+3}{3}
\]
\[
\mathrm{pg}_l=\frac{2^{k-3}(5 F_{k-1}+16 L_{k-1}-15)+2}{5}
\]
\[
\mathrm{gp}_l=\frac{2^{k-3}(5 F_{k-1}+16 L_{k-1}-5)+5(-1)^k-3}{5}.
\]
Small halves sum to Cycle VT xor_lo small. Large halves sum to
Cycle VT xor_lo large. \(\mathrm{pg}_s+\mathrm{pg}_l\) is Cycle WA
leftover xor \(n_{\mathrm{pg}}\). \(\mathrm{gp}_s+\mathrm{gp}_l\) is
Cycle WA leftover xor \(n_{\mathrm{gp}}\). Special-case
\(\mathrm{pg}_s=1\) at \(k=1\) and \(3\) at \(k=2\);
\(\mathrm{gp}_s=0\) at \(k\le 2\); \(\mathrm{pg}_l=1\) at \(k=2\);
\(\mathrm{gp}_l=2\) at \(k=2\) (not \(0\)); zeros at \(k\le 1\) on
the large half. Dies at \(k=3\) for all four F/L forms with shift
\(0\) (\(\mathrm{pg}_s\) got \(0\), not \(10\); \(\mathrm{gp}_s\)
got \(1\), not \(5\); \(\mathrm{pg}_l\) got \(0\), not \(8\);
\(\mathrm{gp}_l\) got \(-2\), not \(8\)). Dies at \(k=8\) without
the \(\mathrm{gp}_s\) \(+3\) (got \(5226\), not \(5227\)), without
the \(\mathrm{pg}_l\) \(+2\) (got \(3289\), not \(3290\)), and
without the \(\mathrm{gp}_l\) \(5(-1)^k\) (got \(3353\), not
\(3354\)). Do **not** kill without the \(\mathrm{gp}_l\) \(-3\) at
\(k=8\): floor-div masks it. Dies at \(k=8\) for \(\mathrm{pg}_s\)
equals tot small (got \(5440\), not \(10667\)), \(\mathrm{pg}_s\)
equals tot \(n_{\mathrm{pg}}\) (got \(5440\), not \(8730\)), and
\(\mathrm{pg}_s\) equals \(\mathrm{gp}_s\) (got \(5440\), not
\(5227\)). Census \(k=8\): \(\mathrm{pg}_s\) \(5440\),
\(\mathrm{gp}_s\) \(5227\), \(\mathrm{pg}_l\) \(3290\),
\(\mathrm{gp}_l\) \(3354\). Do **not** PREFIX pal-center tot from
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

Certify: `python3 research/cycle_wc.py --certify`.
Dump: `research/cycle_wc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/VH/VT/WA
(leftover xor 4-way F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover xor small \(n_{\mathrm{pg}}\) is \(2^{k-3}(4 F_{k+1}+3 F_{k-1}-5)\) for \(k\ge 3\))

Special-case \(1\) at \(k=1\); \(3\) at \(k=2\); \(0\) at \(k\le 0\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=3\) for the F/L form with shift \(0\);
small equals tot at \(k=8\); small equals tot \(n_{\mathrm{pg}}\) at
\(k=8\); \(\mathrm{pg}_s=\mathrm{gp}_s\) at \(k=8\).

## Lemma (leftover xor small \(n_{\mathrm{gp}}\) is \((2^{k-3}(12 F_{k+1}+9 F_{k-1}-35)-2(-1)^k+3)/3\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). The two small halves sum to xor_lo
small. Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=3\) for the F/L form with
shift \(0\); without \(+3\) at \(k=8\).

## Lemma (leftover xor large \(n_{\mathrm{pg}}\) is \((2^{k-3}(5 F_{k-1}+16 L_{k-1}-15)+2)/5\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=3\) for the F/L form with shift \(0\); without
\(+2\) at \(k=8\).

## Lemma (leftover xor large \(n_{\mathrm{gp}}\) is \((2^{k-3}(5 F_{k-1}+16 L_{k-1}-5)+5(-1)^k-3)/5\) for \(k\ge 3\))

Special-case \(2\) at \(k=2\); \(0\) at \(k\le 1\). The two large
halves sum to xor_lo large. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
the F/L form with shift \(0\); without \(5(-1)^k\) at \(k=8\). Do
**not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover xor 4-way F/L closed forms for \(k\ge 3\); halves
sum to xor_lo small/large and leftover xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (all four F/L forms at \(k=3\); without \(\mathrm{gp}_s\)
\(+3\); without \(\mathrm{pg}_l\) \(+2\); without \(\mathrm{gp}_l\)
sign at \(k=8\); \(\mathrm{pg}_s\) equals tot small; \(\mathrm{pg}_s\)
equals tot \(n_{\mathrm{pg}}\); \(\mathrm{pg}_s=\mathrm{gp}_s\);
pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_wc.md` (this note)
- `research/cycle_wc.py`
- `research/cycle_wc.json`
