# Cycle TA: even pal-split at \(k\) is the 2-fold of pal-split at \(k-1\)

Green even doubling is \(G(2m,2r)=G(m,r)\) and \(G(2m,\mathrm{odd})=0\).
Clip matches: parent pal-partner \(\le 5U\) iff child pal-partner
\(\le 5U'\). Pal-centers, pal-pairs, and unpaired cells keep their
kind, so even pal-split counts at \(k\) equal the full pal-split at
\(k-1\). Pal-pair distance doubles and the covering time is Cycle
SZ's even-child 2-fold. Do **not** claim even pal-pair raw tot
equals parent pal-pair raw tot (dies at \(k=2\)). Do **not** claim
cellwise spat 2-fold. Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
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

Certify: `python3 research/cycle_ta.py --certify`.
Dump: `research/cycle_ta.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SR/SS/SU/SV/SX/SY/SZ (even pal-split at
\(k\) is the 2-fold of pal-split at \(k-1\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even pal-split is the 2-fold of pal-split at \(k-1\))

Cycle QV: clipped even-\(n\) \(G=1\) at \(k\) is the 2-fold of
clipped \(G=1\) at \(k-1\), and clip matches. Pal-center \(j=n\)
maps to pal-center; pal-partner \(>5U\) maps to pal-partner
\(>5U'\); the remaining pal-pairs map to pal-pairs. Hence even
pal-center, pal-pair, and unpaired counts at \(k\) equal the
corresponding full counts at \(k-1\). Status: **lemma**. Kind
preservation through \(k\le 8\); algebra through \(k\le 64\).

## Lemma (even pal-pair distance and time 2-fold)

For a parent pal-pair \((m,r)\) the child is \((2m,2r)\), so
\(d'=2d\) and \(t_k(2m)=2t_{k-1}(m)+1\) (Cycle SZ). Even pal-pair
raw is spat at \(\pm 2d\) on that even-child covering time. Status:
**lemma**. Algebra through \(k\le 64\); spat identity through
\(k\le 6\). **Killed:** even pal-pair raw tot equals parent
pal-pair raw tot (dies at \(k=2\)). **Killed:** cellwise spat
2-fold (\(k=2\): 5 of 12 pairs mismatch).

## Verdict

`LEMMA` (even pal-split at \(k\) is the 2-fold of pal-split at
\(k-1\); even pal-pair distance doubles; even pal-pair covering
time is the even-child 2-fold).
`CERTIFIED` (kind counts through \(k\le 8\); spat through
\(k\le 6\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (even pal-pair raw tot equals parent pal-pair raw tot;
cellwise spat 2-fold; pal-center even tot period \(8\); pal-center
tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ta.md` (this note)
- `research/cycle_ta.py`
- `research/cycle_ta.json`
