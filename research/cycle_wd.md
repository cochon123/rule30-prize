# Cycle WD: leftover extra xor 4-way F/L closed forms

Leftover extra xor splits by \(n\le 5U/2\) and by \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\).
For \(k\ge 4\)
\[
\mathrm{pg}_s=2^{k-4}(4 F_k+3 F_{k-2}-5)
\]
\[
\mathrm{gp}_s=\frac{2^{k-4}(12 F_k+9 F_{k-2}-35)-2(-1)^{k-1}+3}{3}
\]
\[
\mathrm{pg}_l=\frac{2^{k-4}(5 F_{k-2}+16 L_{k-2}-15)+2}{5}
\]
\[
\mathrm{gp}_l=\frac{2^{k-4}(5 F_{k-2}+16 L_{k-2}-5)+5(-1)^{k-1}-3}{5}.
\]
Small halves sum to Cycle WB leftover extra xor small. Large
halves sum to Cycle WB leftover extra xor large.
\(\mathrm{pg}_s+\mathrm{pg}_l\) is Cycle VZ leftover extra xor
\(n_{\mathrm{pg}}\). \(\mathrm{gp}_s+\mathrm{gp}_l\) is Cycle VZ
leftover extra xor \(n_{\mathrm{gp}}\). Equal Cycle WC leftover xor
4-way at \(k-1\) for \(k\ge 3\), not at \(k=2\). Special-case
\(\mathrm{pg}_s=3\) at \(k=3\) and \(0\) at \(k\le 2\);
\(\mathrm{gp}_s=0\) at \(k\le 3\); \(\mathrm{pg}_l=1\) at \(k=2\)
and \(k=3\); \(\mathrm{gp}_l=2\) at \(k=3\) and \(0\) at \(k\le 2\).
Dies at \(k=4\) for \(\mathrm{gp}_s\), \(\mathrm{pg}_l\), and
\(\mathrm{gp}_l\) F/L forms with shift \(0\) (\(\mathrm{gp}_s\)
got \(1\), not \(5\); \(\mathrm{pg}_l\) got \(0\), not \(8\);
\(\mathrm{gp}_l\) got \(-2\), not \(8\)). Do **not** kill
\(\mathrm{pg}_s\) shift \(0\) at \(k=4\): \(2^{0}=1\) so it
matches. Dies at \(k=8\) without the \(\mathrm{pg}_s\) \(2^{k-4}\)
(got \(103\), not \(1648\)), without the \(\mathrm{gp}_s\) \(+3\)
(got \(1542\), not \(1543\)), without the \(\mathrm{pg}_l\) \(+2\)
(got \(1001\), not \(1002\)), and without the \(\mathrm{gp}_l\)
\(5(-1)^{k-1}\) (got \(1033\), not \(1032\)). Do **not** kill
without the \(\mathrm{gp}_l\) \(-3\) at \(k=8\): floor-div masks
it. Dies at \(k=2\) for parent leftover xor 4-way (\(\mathrm{pg}_s\)
got \(0\), not \(1\); \(\mathrm{pg}_l\) got \(1\), not \(0\)). Dies
at \(k=8\) for \(\mathrm{pg}_s\) equals tot small (got \(1648\), not
\(3191\)), \(\mathrm{pg}_s\) equals tot \(n_{\mathrm{pg}}\) (got
\(1648\), not \(2650\)), and \(\mathrm{pg}_s\) equals
\(\mathrm{gp}_s\) (got \(1648\), not \(1543\)). Census \(k=8\):
\(\mathrm{pg}_s\) \(1648\), \(\mathrm{gp}_s\) \(1543\),
\(\mathrm{pg}_l\) \(1002\), \(\mathrm{gp}_l\) \(1032\). Do **not**
PREFIX pal-center tot from small \(k\). Do **not** PREFIX leftover
spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not**
catalogue leftover \(d\). Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
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

Certify: `python3 research/cycle_wd.py --certify` (~0.24s).
Dump: `research/cycle_wd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/VH/VZ/WB/WC
(leftover extra xor 4-way F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra xor small \(n_{\mathrm{pg}}\) is \(2^{k-4}(4 F_k+3 F_{k-2}-5)\) for \(k\ge 4\))

Special-case \(3\) at \(k=3\); \(0\) at \(k\le 2\). Equals leftover
xor small \(n_{\mathrm{pg}}\) at \(k-1\) for \(k\ge 3\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** without \(2^{k-4}\) at \(k=8\); parent leftover xor
small \(n_{\mathrm{pg}}\) at \(k=2\); small equals tot at \(k=8\);
small equals tot \(n_{\mathrm{pg}}\) at \(k=8\);
\(\mathrm{pg}_s=\mathrm{gp}_s\) at \(k=8\).

## Lemma (leftover extra xor small \(n_{\mathrm{gp}}\) is \((2^{k-4}(12 F_k+9 F_{k-2}-35)-2(-1)^{k-1}+3)/3\) for \(k\ge 4\))

Special-case \(0\) at \(k\le 3\). The two small halves sum to
leftover extra xor small. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=4\) for
the F/L form with shift \(0\); without \(+3\) at \(k=8\).

## Lemma (leftover extra xor large \(n_{\mathrm{pg}}\) is \((2^{k-4}(5 F_{k-2}+16 L_{k-2}-15)+2)/5\) for \(k\ge 4\))

Special-case \(1\) at \(k=2\) and \(k=3\); \(0\) at \(k\le 1\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=4\) for the F/L form with shift \(0\);
without \(+2\) at \(k=8\); parent leftover xor large
\(n_{\mathrm{pg}}\) at \(k=2\).

## Lemma (leftover extra xor large \(n_{\mathrm{gp}}\) is \((2^{k-4}(5 F_{k-2}+16 L_{k-2}-5)+5(-1)^{k-1}-3)/5\) for \(k\ge 4\))

Special-case \(2\) at \(k=3\); \(0\) at \(k\le 2\). The two large
halves sum to leftover extra xor large. Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=4\) for the F/L form with shift \(0\); without \(5(-1)^{k-1}\)
at \(k=8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra xor 4-way F/L closed forms for \(k\ge 4\);
halves sum to leftover extra xor small/large and leftover extra xor
\(n_{\mathrm{pg}}/n_{\mathrm{gp}}\); equal leftover xor 4-way at
\(k-1\) for \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(\mathrm{gp}_s/\mathrm{pg}_l/\mathrm{gp}_l\) F/L forms at
\(k=4\); without \(\mathrm{pg}_s\) \(2^{k-4}\); without
\(\mathrm{gp}_s\) \(+3\); without \(\mathrm{pg}_l\) \(+2\); without
\(\mathrm{gp}_l\) sign at \(k=8\); parent leftover xor 4-way at
\(k=2\); \(\mathrm{pg}_s\) equals tot small; \(\mathrm{pg}_s\)
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

- `research/cycle_wd.md` (this note)
- `research/cycle_wd.py`
- `research/cycle_wd.json`
