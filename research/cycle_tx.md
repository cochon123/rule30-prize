# Cycle TX: leftover count is \(2\,\mathrm{lo}(k-1)+4J_k+\mathrm{extra}\)

Even leftover count is parent leftover plus \(2J_k\) (Cycle TU).
Odd leftover is even leftover plus the odd-\(n\) even-\(j\) extra
(Cycles TV/TW). Hence leftover(\(k\))= \(2\) leftover(\(k-1\))+
\(4J_k+\) extra(\(k\)) for \(k\ge 2\). Extra is nonempty for
\(k\ge 1\) (it contains \(j=0\) leftover on odd \(n\)), so the
recurrence without extra fails. Do **not** claim leftover
2-folds parent leftover. Do **not** claim leftover(\(k\))=
\(2\) leftover(\(k-1\))+ \(4J_k\). Do **not** catalogue leftover
\(d\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_tx.py --certify` (~0.52s).
Dump: `research/cycle_tx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/TV/TW
(leftover count recurrence; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover \(=\) twice even leftover plus extra)

Cycle TV: odd leftover \(=\) even leftover plus odd-\(n\) even-\(j\)
leftover. Hence leftover count is \(2\) even leftover plus extra.
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\).

## Lemma (leftover(\(k\))= \(2\) leftover(\(k-1\))+ \(4J_k+\) extra, \(k\ge 2\))

Cycle TU: even leftover(\(k\))= leftover(\(k-1\))+ \(2J_k\).
Substitute. Extra is the Cycle TW parent pal-pair adjacent xor
count, and is at least \(5\cdot 2^{k-2}-1\) for \(k\ge 2\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed:** leftover(\(k\))= \(2\) leftover(\(k-1\))+ \(4J_k\).
**Killed:** leftover 2-folds parent leftover.

## Verdict

`LEMMA` (leftover count is twice even leftover plus extra;
leftover(\(k\))= \(2\) leftover(\(k-1\))+ \(4J_k+\) extra for
\(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (recurrence without extra; leftover 2-folds parent leftover;
odd-\(n\) even-\(j\) leftover empty; odd leftover equals even
leftover; leftover pal-pairs empty; pal-center tot equals
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

- `research/cycle_tx.md` (this note)
- `research/cycle_tx.py`
- `research/cycle_tx.json`
