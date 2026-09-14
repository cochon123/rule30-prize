# Cycle TY: pal-pair count is \(2\) parent pair \(+4J_k+\) extra

For \(k\ge 1\) pal-pair count is leftover plus \(2^{k+2}\) (Cycle TU
partition). The leftover recurrence then gives pal-pair(\(k\))=
\(2\) pal-pair(\(k-1\))+ \(4J_k+\) extra(\(k\)) for \(k\ge 2\).
Cycle TA even pal-pairs 2-fold the parent, so odd pal-pair count is
parent pal-pair plus \(4J_k\) plus extra. Do **not** claim pal-pair
2-folds parent pal-pair. Do **not** claim the recurrence without
extra. Do **not** catalogue leftover \(d\). Do **not** PREFIX
leftover spat tot. Do **not** PREFIX pal-center tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim pal-center tot
equals \(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
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

Certify: `python3 research/cycle_ty.py --certify` (~0.65s).
Dump: `research/cycle_ty.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TS/TT/TU/TV/TW/TX
(pal-pair count recurrence; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (pal-pair count \(=\) leftover \(+2^{k+2}\) for \(k\ge 1\))

Cycle TU: the four pal-pair types partition pairs for \(k\ge 1\),
and the named triple has count \(2^{k+2}\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed:**
that identity at \(k=0\) (\(d=2\) overlaps clip-edge).

## Lemma (pal-pair(\(k\))= \(2\) pal-pair(\(k-1\))+ \(4J_k+\) extra)

Substitute leftover(\(k\))= \(2\) leftover(\(k-1\))+ \(4J_k+\) extra
into pal-pair \(=\) leftover \(+2^{k+2}\). The covering-count terms
cancel. Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed:** pal-pair 2-folds parent pal-pair.
**Killed:** the recurrence without extra.

## Lemma (odd pal-pair count \(=\) parent pal-pair \(+4J_k+\) extra)

Cycle TA: even pal-pair count at \(k\) equals the full pal-pair
count at \(k-1\). Subtract from the pal-pair recurrence. Status:
**lemma**. Census through \(k\le 8\).

## Verdict

`LEMMA` (pal-pair count is leftover plus \(2^{k+2}\) for \(k\ge 1\);
pal-pair(\(k\))= \(2\) pal-pair(\(k-1\))+ \(4J_k+\) extra for
\(k\ge 2\); odd pal-pair count is parent pal-pair plus \(4J_k\)
plus extra).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (recurrence without extra; pal-pair 2-folds parent pal-pair;
leftover recurrence without extra; leftover pal-pairs empty;
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

- `research/cycle_ty.md` (this note)
- `research/cycle_ty.py`
- `research/cycle_ty.json`
