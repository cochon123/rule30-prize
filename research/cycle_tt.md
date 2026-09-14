# Cycle TT: leftover pal-pair rest tot is leftover raw xor \(1\) for \(k\ge 3\)

Leftover pal-pairs are those with pal-distance not in \(\{1,2\}\) and
not clip-edge. Leftover is a pal-pair property, not an \(n\)
property: Cycle SV's unique even forced cell \(n=3U-2\) has
pal-distance \(2U\), so that pair is leftover, and it is the unique
even forced pal-pair, even though the same covering \(n\) also
carries a \(d=2\) pal-pair when \(k\) is even. Even leftover rest
tot is therefore leftover-even raw xor \(1\) for \(k\ge 1\). Odd
leftover rest tot equals odd leftover raw for \(k\ge 3\) (Cycles
SY/TP/TQ/TS). Hence leftover rest tot equals leftover raw xor \(1\)
for \(k\ge 3\). Do **not** claim leftover rest equals raw for all
\(k\). Do **not** claim leftover pal-pairs empty. Do **not** claim
leftover \(n\) disjoint from named types. Do **not** catalogue
leftover \(d\). Do
**not** PREFIX leftover spat tot. Do **not** PREFIX pal-center tot.
Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_tt.py --certify`.
Dump: `research/cycle_tt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/PB/QV/SO/SV/SY/TA/TB/TC/TD/TE/TP/TQ/TS
(leftover rest tot; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even leftover rest tot \(=\) raw xor \(1\) for \(k\ge 1\))

Even pal-pair rest tot is raw xor \(1\) (Cycle SV), from the unique
even cell at pal-distance \(2U\). Even \(d=2\) never forced (Cycle
TQ); clip-edge never forced (Cycle TS). So that unique pair is the
unique even leftover forced pal-pair. The same covering \(n\) also
has a \(d=2\) pal-pair when \(k\) is even; that other pair is named,
not leftover. Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 12\). **Killed:** leftover \(n\) disjoint from named
types.

## Lemma (leftover rest tot \(=\) raw xor \(1\) for \(k\ge 3\))

Odd pal-pair rest tot equals raw for \(k\ge 3\) (Cycle SY). Odd
\(d=1\) never forced for \(k\ge 2\) (Cycle TP); odd \(d=2\) forced
corr is 0 (Cycle TQ); clip-edge never forced. Odd leftover rest tot
equals odd leftover raw. Xor with the even leftover lemma gives
leftover rest tot \(=\) leftover raw xor \(1\). Status: **lemma**.
Algebra through \(k\le 64\). **Killed:** leftover rest equals raw
for all \(k\).

## Verdict

`LEMMA` (even leftover rest tot equals raw xor \(1\) for \(k\ge 1\);
leftover rest tot equals leftover raw xor \(1\) for \(k\ge 3\);
unique even forced cell is leftover).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (leftover rest equals raw for all \(k\); leftover pal-pairs
empty; leftover \(n\) disjoint from named types; three types
partition covering \(n\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tt.md` (this note)
- `research/cycle_tt.py`
- `research/cycle_tt.json`
