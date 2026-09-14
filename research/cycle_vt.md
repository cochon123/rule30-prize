# Cycle VT: leftover xor-pair small/large F/L closed forms

Cycle VP tot splits by \(n\le 5U/2\). For \(k\ge 2\) the small half
is
\[
\frac{2^{k-2}(12 F_{k+1}+9 F_{k-1}-25)-2(-1)^k+3}{3}
\]
and the large half is
\[
\frac{2^{k-2}(5 F_{k-1}+16 L_{k-1}-10)+5(-1)^k-1}{5}.
\]
They sum to Cycle VP xor_lo. Small is Cycle VS lo_small minus
Cycle TW \(j=0\) leftover; large equals Cycle VS lo_large.
Special-case small \(1\) at \(k=1\); both \(0\) at \(k\le 0\);
large \(0\) at \(k=1\). Dies at \(k=2\) for both F/L forms with
shift \(0\) (small got \(0\), not \(3\); large got \(0\), not
\(3\)). Dies at \(k=8\) without the small \(+3\) (got \(10666\),
not \(10667\)) and for small equals tot xor_lo (got \(10667\),
not \(17311\)). Census \(k=8\): small \(10667\), large \(6644\).
Do **not** PREFIX pal-center tot from small \(k\). Do **not**
PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat
tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_vt.py --certify`.
Dump: `research/cycle_vt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UO/UP/UR/UU/UV/UW/UZ/VA/VP/VS
(xor_lo small/large F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover xor-pair small is \((2^{k-2}(12 F_{k+1}+9 F_{k-1}-25)-2(-1)^k+3)/3\) for \(k\ge 2\))

Special-case \(1\) at \(k=1\); \(0\) at \(k\le 0\). Equals lo_small
minus \(j=0\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** at \(k=2\) for the F/L form
with shift \(0\); without \(+3\) at \(k=8\).

## Lemma (leftover xor-pair large is \((2^{k-2}(5 F_{k-1}+16 L_{k-1}-10)+5(-1)^k-1)/5\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). Equals Cycle VS lo_large. The two
halves sum to Cycle VP xor_lo. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=2\) for
the F/L form with shift \(0\); small equals tot xor_lo at \(k=8\).
Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (xor_lo small/large F/L closed forms for \(k\ge 2\); halves
sum to xor_lo).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (small F/L form at \(k=2\); large F/L form at \(k=2\);
small without \(+3\); small equals tot xor_lo; pal-center tot
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

- `research/cycle_vt.md` (this note)
- `research/cycle_vt.py`
- `research/cycle_vt.json`
