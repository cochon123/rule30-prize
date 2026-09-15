# Cycle WS: even \(n=5U/2+4\) is the 2-fold of Cycle WQ at \(k-1\)

Covering \(n=5U/2+4\) equals \(2\cdot(5U_p/2+2)\). Even doubling
sends parent left Green to child left Green with
\(\mathrm{pal\_kind}\) and clip-edge preserved, so unpaired left is
\(\{0,4\}\) for \(k\ge 4\) and leftover+pal is the even 11-set
\(\{U/2,U/2+4,U/2+8,U,U+4,U+8,2U,2U+4,2U+8,5U/2,n\}\) for
\(k\ge 5\). The \(j=4\) cell has partner \(5U+4\), not \(5U+2\).
Dies at \(k=3\) for unpaired \(\{0,4\}\) (\(G\) at \(j=4\) is
\(0\)). Dies at \(k=4\) for leftover 11-set (got \(6\)). Do **not**
kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+4\), \(j=0\) or
\(j=4\) for \(k\ge 4\). Census \(k=8\): unpaired \(2\), leftover+pal
\(11\), clip \(1\). Do **not** PREFIX pal-center tot from small
\(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_ws.py --certify` (~0.14s).
Dump: `research/cycle_ws.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WQ/WR
(even \(n=5U/2+4\) 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(n=5U/2+4\) is \(2\cdot(5U_p/2+2)\) for \(k\ge 2\))

Even doubling preserves \(\mathrm{pal\_kind}\) and clip-edge on
this fibre. Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\).

## Lemma (unpaired left at \(n=5U/2+4\) is \(\{0,4\}\) for \(k\ge 4\))

The \(j=4\) cell has partner \(5U+4\). Special-case \(\{0\}\) at
\(k=3\); \(\{0,2,6\}\) at \(k=2\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for \(\{0,4\}\); at \(k=8\) for unpaired count equals
\(\mathrm{clip\_gp}\); equals the even partner-\(5U+2\) slice;
\(\mathrm{pal\_kind}\) pair at \(j=4\); \(G(n,4)=1\) at \(k=3\).
Do **not** kill unpaired at \(j=0\) or \(j=4\) for \(k\ge 4\).

## Lemma (leftover+pal at \(n=5U/2+4\) is the even 11-set for \(k\ge 5\))

The cells are \(2\) times Cycle WQ's 11-set at \(k-1\). Special-case
\(6\) at \(k=4\); \(1\) at \(k=3\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=4\) for equals \(11\); at \(k=8\) for equals
\(\mathrm{clip\_gp}\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (\(n=5U/2+4\) is the 2-fold of Cycle WQ; unpaired left
\(\{0,4\}\) for \(k\ge 4\); leftover+pal even 11-set for \(k\ge 5\);
\(j=4\) has partner \(5U+4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired \(\{0,4\}\) at \(k=3\); leftover 11-set at
\(k=4\); unpaired equals \(\mathrm{clip\_gp}\); leftover equals
\(\mathrm{clip\_gp}\); unpaired equals even partner-\(5U+2\) slice;
\(j=4\) pair; \(G(n,4)=1\) at \(k=3\); pal-center tot equals
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

- `research/cycle_ws.md` (this note)
- `research/cycle_ws.py`
- `research/cycle_ws.json`
