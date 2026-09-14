# Cycle TZ: odd-\(j\) unpaired count is parent unpaired plus \(J_{k+1}\)

Even unpaired 2-folds parent unpaired (Cycle TA). Odd-\(j\) pal-pairs
drop clip-edge to unpaired (Cycle TB), and parent unpaired 2-folds
to odd-\(j\) unpaired, so odd-\(j\) unpaired at \(k\ge 1\) is
unpaired(\(k-1\))+ \(J_{k+1}\). Even \(n\) have no odd-\(j\) cells,
so that equals even unpaired plus \(J_{k+1}\). Do **not** claim
odd-\(j\) unpaired equals even unpaired. Do **not** claim unpaired
2-folds parent unpaired alone. Do **not** catalogue leftover \(d\).
Do **not** PREFIX leftover spat tot. Do **not** PREFIX pal-center
tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim
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

Certify: `python3 research/cycle_tz.py --certify`.
Dump: `research/cycle_tz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU
(odd-\(j\) unpaired 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even unpaired count equals parent unpaired count)

Cycle TA: even pal-split counts at \(k\) equal the full pal-split
at \(k-1\). Unpaired is one of those kinds. Even \(n\) have no
odd-\(j\) cells, so even unpaired is even-\(j\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\).

## Lemma (odd-\(j\) unpaired \(=\) parent unpaired \(+J_{k+1}\), \(k\ge 1\))

Cycle TB: odd-\(j\) pal-pairs drop clip-edge to unpaired, and the
odd-\(j\) 2-fold of parent unpaired stays unpaired. Clip-edge count
is \(J_{k+1}\) at the parent. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed:** odd-\(j\)
unpaired equals even unpaired. **Killed:** unpaired 2-folds parent
unpaired alone.

## Lemma (odd-\(j\) unpaired \(=\) even unpaired \(+J_{k+1}\))

Even unpaired(\(k\))= unpaired(\(k-1\)). Substitute. Status:
**lemma**. Census through \(k\le 8\). **Killed:** odd unpaired
equals even unpaired.

## Verdict

`LEMMA` (even unpaired count equals parent unpaired; odd-\(j\)
unpaired is parent unpaired plus \(J_{k+1}\) for \(k\ge 1\);
odd-\(j\) unpaired is even unpaired plus \(J_{k+1}\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd-\(j\) unpaired equals even unpaired; unpaired 2-folds
parent unpaired alone; odd unpaired equals even unpaired;
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

- `research/cycle_tz.md` (this note)
- `research/cycle_tz.py`
- `research/cycle_tz.json`
