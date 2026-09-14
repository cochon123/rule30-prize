# Cycle RJ: UNIQUE_REST 2-fold off-unique image is 13 even leftover columns

Packed column doubling is \(p\mapsto 2p\). Cycle RI stay is
\(\{16,30,38\}\). The other 13 UNIQUE_REST columns 2-fold off unique
to even packed \(p\) (\(p\bmod 4=0\)), disjoint from FORCED
\(\{4,6,14\}\) and from Cycle RF silent \(\{8,12,28\}\). The image
is \((64,84,104,108,116,120,144,152,172,176,196,212,228)\), with
\(p=64\) leftover silent for \(k\ge 6\) (Cycle PO). This is **not**
that image meeting unique or forced. **Not** a leftover \(p\) AND
xor catalogue. This is **not** rest \(=S\oplus T\). **Not**
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
Do **not** claim \(p=64\) is unique-rest.

Certify: `python3 research/cycle_rj.py --certify` (~0.13s).
Dump: `research/cycle_rj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/MD/PO/RF/RI (UNIQUE_REST 2-fold off-unique image 13 even
leftover columns; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (UNIQUE_REST 2-fold off-unique image is 13 even leftover columns)

The complement of Cycle RI stay 2-folds to even packed \(p\),
disjoint from unique, forced, and RF silent \(\{8,12,28\}\). Status:
**lemma**. **Killed:** that image meets unique. **Killed:** that
image meets forced.

## Verdict

`LEMMA` (UNIQUE_REST 2-fold off-unique image is 13 even leftover
columns, disjoint from unique/forced/RF silent; PO \(p=64\) leftover
silent for \(k\ge 6\); RI stay \(\{16,30,38\}\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (off-unique image meets unique; off-unique image meets
forced; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rj.md` (this note)
- `research/cycle_rj.py`
- `research/cycle_rj.json`
