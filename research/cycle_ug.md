# Cycle UG: extra sum is odd(\(\mathrm{lo{+}unp}\))-even(\(\mathrm{lo{+}unp}\))-\(J_{k+1}\)

For \(k\ge 1\), leftover extra is odd leftover minus even leftover
(Cycle TV) and unpaired extra is odd unpaired minus even unpaired
minus \(J_{k+1}\) (Cycle UA). Cycle UF then gives leftover extra plus
unpaired extra equal to odd leftover-plus-unpaired minus even
leftover-plus-unpaired minus \(J_{k+1}\). Fibonacci and Jacobsthal
cancel to Cycle UC's \(2^{k+1}(F_{k+2}-1)+(-1)^k\). Do **not**
PREFIX leftover extra or unpaired extra separately. Do **not**
catalogue leftover \(d\). Do **not** PREFIX leftover spat tot. Do
**not** PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat
tot. Do **not** claim pal-center tot equals \(S\oplus T\). This is
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

Certify: `python3 research/cycle_ug.py --certify` (~0.51s).
Dump: `research/cycle_ug.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/UC/UD/UE/UF
(extra sum from n-parity leftover-plus-unpaired; no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (extra sum \(=\) odd(\(\mathrm{lo{+}unp}\))-even(\(\mathrm{lo{+}unp}\))-\(J_{k+1}\) for \(k\ge 1\))

Leftover extra \(=\) odd leftover \(-\) even leftover. Unpaired extra
\(=\) odd unpaired \(-\) even unpaired \(-\,J_{k+1}\). Cycle UF
closes the even and odd leftover-plus-unpaired counts. Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed:** leftover extra equals unpaired extra. **Killed:** extra
sum empty. **Killed:** leftover extra (or unpaired extra) equals
the UC sum.

## Lemma (parity extra sum \(=2^{k+1}(F_{k+2}-1)+(-1)^k\))

Expand Cycle UF: odd minus even is leftover-plus-unpaired minus
twice the even sum. Substitute \(2^{k+1}(F_{k+4}-3)\) and
\(2^k(F_{k+3}-3)+2J_k\). The Jacobsthal remainder is
\(4J_k+J_{k+1}=2^{k+1}-(-1)^k\), and the Fibonacci remainder is
\(2^{k+1}F_{k+2}\). Status: **lemma**. Algebra through \(k\le 64\).

## Verdict

`LEMMA` (leftover extra plus unpaired extra is odd leftover-plus-unpaired
minus even leftover-plus-unpaired minus \(J_{k+1}\) for \(k\ge 1\);
that equals Cycle UC's \(2^{k+1}(F_{k+2}-1)+(-1)^k\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (leftover extra equals unpaired extra; extra sum empty;
leftover extra equals the UC sum; unpaired extra equals the UC sum;
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

- `research/cycle_ug.md` (this note)
- `research/cycle_ug.py`
- `research/cycle_ug.json`
