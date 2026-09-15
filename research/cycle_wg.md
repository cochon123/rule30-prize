# Cycle WG: named leftover extra 4-way closed forms

Named leftover extra splits by \(n\le 5U/2\) and by
\(n_{\mathrm{pg}}/n_{\mathrm{gp}}\). For \(k\ge 3\)
\[
\mathrm{pg}_s=\frac{5\cdot 2^{k-2}-4(-1)^{k-1}}{3}
\]
\[
\mathrm{gp}_s=5\cdot 2^{k-3}-2
\]
\[
\mathrm{pg}_l=2^{k-2}+2(-1)^{k-1}
\]
\[
\mathrm{gp}_l=3\cdot 2^{k-3}.
\]
Small halves sum to Cycle VY named small. Large halves sum to
Cycle VY named large. Equal leftover xor 4-way minus leftover-parent
xor 4-way. \(\mathrm{pg}_s+\mathrm{pg}_l=2 J_k\) for \(k\ge 2\).
Special-case \(\mathrm{pg}_s=1\) at \(k=1\) and \(2\) at \(k=2\);
\(\mathrm{gp}_l=2\) at \(k=2\); \(\mathrm{gp}_s=\mathrm{pg}_l=0\)
at \(k\le 2\); all \(0\) at \(k\le 0\). Dies at \(k=3\) for
\(\mathrm{pg}_s\) and \(\mathrm{pg}_l\) with shift \(0\)
(\(\mathrm{pg}_s\) got \(-2\), not \(2\); \(\mathrm{pg}_l\) got
\(2\), not \(4\)). Do **not** kill \(\mathrm{gp}_s\) or
\(\mathrm{gp}_l\) shift \(0\) at \(k=3\): \(2^{0}=1\) so they
match. Dies at \(k=2\) for the \(\mathrm{pg}_s\) and
\(\mathrm{pg}_l\) forms (\(\mathrm{pg}_s\) got \(3\), not \(2\);
\(\mathrm{pg}_l\) got \(-1\), not \(0\)). Dies at \(k=8\) without
the \(\mathrm{pg}_s\) \(5\cdot 2^{k-2}\) (got \(1\), not \(108\)),
without the \(\mathrm{pg}_s\) sign (got \(106\), not \(108\)),
without the \(\mathrm{gp}_s\) \(-2\) (got \(160\), not \(158\)),
without the \(\mathrm{gp}_s\) \(5\cdot 2^{k-3}\) (got \(-2\), not
\(158\)), without the \(\mathrm{pg}_l\) \(2^{k-2}\) (got \(-2\),
not \(62\)), without the \(\mathrm{pg}_l\) sign (got \(64\), not
\(62\)), without the \(\mathrm{gp}_l\) \(3\) (got \(32\), not
\(96\)), and without the \(\mathrm{gp}_l\) \(2^{k-3}\) (got \(3\),
not \(96\)). Dies at \(k=8\) for \(\mathrm{pg}_s\) equals tot small
(got \(108\), not \(266\)), \(\mathrm{pg}_s\) equals tot
\(n_{\mathrm{pg}}\) (got \(108\), not \(170\)), and
\(\mathrm{pg}_s\) equals \(\mathrm{gp}_s\) (got \(108\), not
\(158\)). Census \(k=8\): \(\mathrm{pg}_s\) \(108\),
\(\mathrm{gp}_s\) \(158\), \(\mathrm{pg}_l\) \(62\),
\(\mathrm{gp}_l\) \(96\). Do **not** PREFIX pal-center tot from
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

Certify: `python3 research/cycle_wg.py --certify` (~0.35s).
Dump: `research/cycle_wg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UL/UO/UP/UR/UU/UV/UW/UZ/VA/VY/WC/WE/WF
(named leftover extra 4-way; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (named leftover extra small \(n_{\mathrm{pg}}\) is \((5\cdot 2^{k-2}-4(-1)^{k-1})/3\) for \(k\ge 3\))

Special-case \(1\) at \(k=1\) and \(2\) at \(k=2\); \(0\) at
\(k\le 0\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=3\) for shift \(0\); at
\(k=2\) for the form; without \(5\cdot 2^{k-2}\) at \(k=8\);
without the sign at \(k=8\); small equals tot at \(k=8\); small
equals tot \(n_{\mathrm{pg}}\) at \(k=8\);
\(\mathrm{pg}_s=\mathrm{gp}_s\) at \(k=8\).

## Lemma (named leftover extra small \(n_{\mathrm{gp}}\) is \(5\cdot 2^{k-3}-2\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). The two small halves sum to named
small. Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** without \(-2\) at \(k=8\); without
\(5\cdot 2^{k-3}\) at \(k=8\). Do **not** kill shift \(0\) at
\(k=3\).

## Lemma (named leftover extra large \(n_{\mathrm{pg}}\) is \(2^{k-2}+2(-1)^{k-1}\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
shift \(0\); at \(k=2\) for the form; without \(2^{k-2}\) at
\(k=8\); without the sign at \(k=8\).

## Lemma (named leftover extra large \(n_{\mathrm{gp}}\) is \(3\cdot 2^{k-3}\) for \(k\ge 3\))

Special-case \(2\) at \(k=2\); \(0\) at \(k\le 1\). The two large
halves sum to named large. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** without \(3\) at
\(k=8\); without \(2^{k-3}\) at \(k=8\). Do **not** kill shift
\(0\) at \(k=3\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (named leftover extra 4-way closed forms for \(k\ge 3\);
halves sum to named small/large; equal leftover xor 4-way minus
leftover-parent xor 4-way; \(\mathrm{pg}_s+\mathrm{pg}_l=2 J_k\)
for \(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(\mathrm{pg}_s/\mathrm{pg}_l\) shift \(0\) at \(k=3\);
\(\mathrm{pg}_s/\mathrm{pg}_l\) forms at \(k=2\); without
\(\mathrm{pg}_s\) \(5\cdot 2^{k-2}\); without \(\mathrm{pg}_s\)
sign; without \(\mathrm{gp}_s\) \(-2\); without \(\mathrm{gp}_s\)
\(5\cdot 2^{k-3}\); without \(\mathrm{pg}_l\) \(2^{k-2}\); without
\(\mathrm{pg}_l\) sign; without \(\mathrm{gp}_l\) \(3\); without
\(\mathrm{gp}_l\) \(2^{k-3}\); \(\mathrm{pg}_s\) equals tot small;
\(\mathrm{pg}_s\) equals tot \(n_{\mathrm{pg}}\);
\(\mathrm{pg}_s=\mathrm{gp}_s\); pal-center tot equals
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

- `research/cycle_wg.md` (this note)
- `research/cycle_wg.py`
- `research/cycle_wg.json`
