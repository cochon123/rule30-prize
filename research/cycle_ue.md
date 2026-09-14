# Cycle UE: leftover plus unpaired is \(2^{k+1}(F_{k+4}-3)\) for \(k\ge 1\)

Cycle TU leftover count is pal-pair minus \(4U=2^{k+2}\) for
\(k\ge 1\). Cycle UD pal-pair plus unpaired is
\(2^{k+1}(F_{k+4}-1)\). Subtract pal-center to get leftover plus
unpaired \(2^{k+1}(F_{k+4}-3)\). Dies at \(k=0\): \(d=2\) overlaps
clip-edge, so leftover is not pal-pair minus \(4U\). Do **not**
claim leftover alone equals that Fibonacci form. Do **not** PREFIX
leftover extra or unpaired extra separately. Do **not** catalogue
leftover \(d\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot.
Do **not** claim pal-center tot equals \(S\oplus T\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\) covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_ue.py --certify`.
Dump: `research/cycle_ue.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TY/UC/UD
(leftover plus unpaired Fibonacci; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover plus unpaired \(=2^{k+1}(F_{k+4}-3)\) for \(k\ge 1\))

Cycle TU: leftover \(=\) pal-pair \(-2^{k+2}\) for \(k\ge 1\).
Cycle UD: pal-pair plus unpaired \(=2^{k+1}(F_{k+4}-1)\). Hence
leftover plus unpaired \(=2^{k+1}(F_{k+4}-1)-2^{k+2}
=2^{k+1}(F_{k+4}-3)\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed:** leftover alone
equals that Fibonacci form. **Killed:** the formula at \(k=0\).

## Verdict

`LEMMA` (leftover plus unpaired \(=2^{k+1}(F_{k+4}-3)\) for
\(k\ge 1\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (leftover alone equals \(2^{k+1}(F_{k+4}-3)\); the formula
at \(k=0\); \(G(n,n)=n\bmod 2\); pal-center count \(=2^{k+1}\);
pal-pair plus unpaired \(=2^{k+2}\); pal-center tot equals
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

- `research/cycle_ue.md` (this note)
- `research/cycle_ue.py`
- `research/cycle_ue.json`
