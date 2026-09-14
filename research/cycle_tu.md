# Cycle TU: even leftover count is parent leftover plus parent \(d=2\)

For \(k\ge 1\) the pal-pair types \(\{d=1,d=2,\mathrm{clip\text{-}edge},\mathrm{leftover}\}\)
partition pal-pairs (as pairs, not as covering \(n\)), so leftover
count is pal-pair count minus \(2^{k+2}\). Cycle TA even pal-pairs
are the 2-fold of all parent pal-pairs, distance doubles, and clip
matches, so even leftover count at \(k\ge 2\) equals leftover
count at \(k-1\) plus the parent \(d=2\) count \(2J_k\). Dies at
\(k=1\): parent \(d=2\) overlaps clip-edge (\(k=0\), \(n=3\)).
Do **not** claim the four types partition pal-pairs for all \(k\).
Do **not** claim even leftover equals parent leftover. Do **not**
catalogue leftover \(d\). Do **not** PREFIX leftover spat tot. Do
**not** PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_tu.py --certify` (~0.51s).
Dump: `research/cycle_tu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TS/TT
(even leftover 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (four pal-pair types partition pairs for \(k\ge 1\))

Distances \(d=1\) and \(d=2\) are disjoint. A \(d=1\) clip-edge
would need covering \(n=5U-1\), which is past \(4U-1\). A \(d=2\)
clip-edge is covering \(n=5U-2\), hence only \(k=0\), \(n=3\)
(Cycle TE). Thus for \(k\ge 1\) every pal-pair is exactly one of
\(d=1\), \(d=2\), clip-edge, or leftover, and leftover count is
pal-pair count minus \(2^{k+2}\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed:** the
four types partition pal-pairs for all \(k\). **Killed:** the four
types partition covering \(n\).

## Lemma (even leftover count \(=\) parent leftover \(+\) parent \(d=2\), \(k\ge 2\))

Cycle TA: even pal-pairs at \(k\) are the 2-fold of all pal-pairs
at \(k-1\), with distance doubled and clip matching. Parent
leftover maps to leftover; parent \(d=2\) maps to leftover
\(d=4\); parent \(d=1\) maps to named \(d=2\); parent clip-edge
maps to clip-edge. For \(k\ge 2\) the parent already partitions,
so even leftover count is leftover(\(k-1\))+ \(2J_k\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed:** even leftover equals parent leftover. **Killed:** the
2-fold holds for all \(k\) (dies at \(k=1\)).

## Verdict

`LEMMA` (four pal-pair types partition pairs for \(k\ge 1\);
leftover count is pal-pair count minus \(2^{k+2}\) for \(k\ge 1\);
even leftover count is parent leftover plus parent \(d=2\) for
\(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (four types partition pal-pairs for all \(k\); even
leftover equals parent leftover; even leftover 2-fold for all
\(k\); leftover pal-pairs empty; leftover \(n\) disjoint from
named types; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tu.md` (this note)
- `research/cycle_tu.py`
- `research/cycle_tu.json`
