# Cycle VS: leftover extra small/large F/L closed forms

Cycle VQ tot splits by \(n\le 5U/2\). For \(k\ge 2\) the small half
is
\[
\frac{2^{k-2}(12 F_{k+1}+9 F_{k-1}-10)-2(-1)^k}{3}
\]
and the large half is
\[
\frac{2^{k-2}(5 F_{k-1}+16 L_{k-1}-10)+5(-1)^k-1}{5}.
\]
They sum to Cycle VQ extra_lo. Special-case small \(2\) at \(k=1\);
both \(0\) at \(k\le 0\); large \(0\) at \(k=1\). Dies at \(k=2\)
for both F/L forms with shift \(0\) (small got \(-1\), not \(7\);
large got \(0\), not \(3\)). Dies at \(k=8\) for small equals tot
extra_lo (got \(10986\), not \(17630\)). Census \(k=8\): small
\(10986\), large \(6644\). Do **not** PREFIX pal-center tot from
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

Certify: `python3 research/cycle_vs.py --certify` (~0.35s).
Dump: `research/cycle_vs.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UK/UO/UP/UQ/UR/UU/UV/UW/UZ/VA/VQ
(lo_small/lo_large F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra small is \((2^{k-2}(12 F_{k+1}+9 F_{k-1}-10)-2(-1)^k)/3\) for \(k\ge 2\))

Special-case \(2\) at \(k=1\); \(0\) at \(k\le 0\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=2\) for the F/L form with shift \(0\).

## Lemma (leftover extra large is \((2^{k-2}(5 F_{k-1}+16 L_{k-1}-10)+5(-1)^k-1)/5\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). The two halves sum to Cycle VQ
extra_lo. Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=2\) for the F/L form with
shift \(0\); small equals tot extra_lo at \(k=8\). Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (lo_small/lo_large F/L closed forms for \(k\ge 2\); halves
sum to extra_lo).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (small F/L form at \(k=2\); large F/L form at \(k=2\);
small equals tot extra_lo; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vs.md` (this note)
- `research/cycle_vs.py`
- `research/cycle_vs.json`
