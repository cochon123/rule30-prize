# Cycle SW: packed AND at \(p=6\) is \(1\) on odd \(t\ge 3\)

Bits \(5\) and \(6\) equal \(t\bmod 2\) for \(t\ge 2\), from the
\(p=4\) freeze (bits \(3,4\)) and the packed update. Packed AND at
\(p=6\) is bits \(5\) and \(6\), hence \(1\) on every odd \(t\ge 3\).
Odd pal-right at \(p=6\) is the Green set \(\{4U-1\}\) union
\(\{3U-1\}\) if \(k\) even union \(\{3U-1-2^i:i=1,\ldots,k-1\}\)
for \(k\ge 2\), count \(k+1-(k\bmod 2)\), always odd. Those cells
all fire AND, so odd pal-right \(p=6\) AND tot is \(1\) through the
exact-set range. Do **not** claim that Green set for all \(k\). Do
**not** claim odd pal-pair rest equals raw for all \(k\). Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue
leftover \(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_sw.py --certify`.
Dump: `research/cycle_sw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LD/LF/OJ/PB/QV/SO/SR/SV (packed AND at \(p=6\) is
\(1\) on odd \(t\ge 3\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (bits \(5,6=t\bmod 2\) for \(t\ge 2\))

Packed bit \(4\) is \(1\) for \(t\ge 2\) and bit \(3=t\bmod 2\)
(Cycle SV). The update at \(p=5\) is bit \(3\oplus 1\), so bit
\(5=t\bmod 2\). The update at \(p=6\) is \(1\oplus(\mathrm{bit}\,5\lor\mathrm{bit}\,6)\),
and the base \(t=2\) has bits \(5=6=0\), so bit \(6=t\bmod 2\).
Packed AND at \(p=6\) is bits \(5\) and \(6\), hence \(1\) on every
odd \(t\ge 3\). Status: **lemma**. Freeze through \(t<128\).
**Killed:** AND at \(p=6\) identically \(1\) (fails at \(t=0\)).

## Lemma (listed odd pal-right \(p=6\) count is \(k+1-(k\bmod 2)\))

The listed set \(\{4U-1\}\cup\{3U-1\text{ if }k\text{ even}\}\cup\{3U-1-2^i:i=1,\ldots,k-1\}\)
has cardinality \(k+1-(k\bmod 2)\) with no collisions, matching
`want_p6_n(k,10)` for \(k\ge 2\). Each listed \(n\) is an odd
covering pal-right at \(j=5U-3\) with \(G=1\). Status: **lemma**
(count and \(G=1\) on listed \(n\)). Exactness of the set is
**certified** \(2\le k\le 12\). **Prefix** exact set for all \(k\).

## Verdict

`LEMMA` (bits \(5,6=t\bmod 2\) for \(t\ge 2\); packed AND at \(p=6\)
is \(1\) on odd \(t\ge 3\); listed odd pal-right \(p=6\) count).
`CERTIFIED` (exact Green sets at \(p=6,14\) through \(k\le 12\);
odd pal-right \(p=6\) AND tot \(1\) for \(2\le k\le 10\); odd
pal-right AND tot \(0\) for \(3\le k\le 10\); \(E_k=0\) on odd-\(s\)
rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot equals \(S\oplus T\); AND at \(p=6\)
identically \(1\); cellwise 2-fold packed AND).
`PREFIX` (exact \(p=6\) Green set for all \(k\); odd pal-right
\(p=6\) AND tot \(1\) for all \(k\ge 2\); \(p=14\) AND on \(G=1\)
for all \(k\); odd pal-pair rest equals raw for all \(k\ge 3\);
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\); packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\)
for all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sw.md` (this note)
- `research/cycle_sw.py`
- `research/cycle_sw.json`
