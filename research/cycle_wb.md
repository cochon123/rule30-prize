# Cycle WB: leftover extra xor small/large F/L closed forms

Leftover extra xor splits by \(n\le 5U/2\). For \(k\ge 3\)
\[
\mathrm{small}=\frac{2^{k-3}(12 F_k+9 F_{k-2}-25)-2(-1)^{k-1}+3}{3}
\]
and
\[
\mathrm{large}=\frac{2^{k-3}(5 F_{k-2}+16 L_{k-2}-10)+5(-1)^{k-1}-1}{5}.
\]
They sum to leftover extra xor tot. Equal Cycle VT xor_lo
small/large at \(k-1\) for \(k\ge 3\), not at \(k=2\). Special-case
small \(0\) at \(k\le 2\); large \(1\) at \(k=2\); both \(0\) at
\(k\le 1\). Dies at \(k=3\) for both F/L forms with shift \(0\)
(small got \(0\), not \(3\); large got \(0\), not \(3\)). Dies at
\(k=8\) without the small \(+3\) (got \(3190\), not \(3191\)) and
without the large \(5(-1)^{k-1}\) (got \(2035\), not \(2034\)). Do
**not** kill without the large \(-1\) at \(k=8\): floor-div masks
it. Dies at \(k=2\) for parent xor_lo halves (small got \(0\), not
\(1\); large got \(1\), not \(0\)). Dies at \(k=8\) for small
equals tot (got \(3191\), not \(5225\)). Census \(k=8\): small
\(3191\), large \(2034\). Do **not** PREFIX pal-center tot from
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

Certify: `python3 research/cycle_wb.py --certify`.
Dump: `research/cycle_wb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/VC/VT/VZ
(leftover extra xor small/large F/L; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra xor small is \((2^{k-3}(12 F_k+9 F_{k-2}-25)-2(-1)^{k-1}+3)/3\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). Equals xor_lo small at \(k-1\)
for \(k\ge 3\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** at \(k=3\) for the F/L form
with shift \(0\); without \(+3\) at \(k=8\); parent xor_lo small
at \(k=2\).

## Lemma (leftover extra xor large is \((2^{k-3}(5 F_{k-2}+16 L_{k-2}-10)+5(-1)^{k-1}-1)/5\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). The two halves
sum to leftover extra xor tot. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
the F/L form with shift \(0\); without \(5(-1)^{k-1}\) at \(k=8\);
small equals tot at \(k=8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra xor small/large F/L closed forms for
\(k\ge 3\); halves sum to leftover extra xor tot).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (small F/L form at \(k=3\); large F/L form at \(k=3\);
without \(+3\); without large sign at \(k=8\); parent xor_lo
halves at \(k=2\); small equals tot; pal-center tot equals
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

- `research/cycle_wb.md` (this note)
- `research/cycle_wb.py`
- `research/cycle_wb.json`
