# Cycle YU: even \(n=5U/2+1048576\) is the 2-fold of Cycle YR at \(k-1\)

Covering \(n=5U/2+1048576\) equals \(2\cdot(5U_p/2+524288)\). Even doubling
sends parent left Green to child left Green with
\(\mathrm{pal\_kind}\) and clip-edge preserved, so unpaired left is
\(\{0,1048576\}\) for \(k\ge 22\) and leftover+pal is the even 11-set
\(\{U/2,U/2+1048576,U/2+2097152,U,U+1048576,U+2097152,2U,2U+1048576,2U+2097152,5U/2,n\}\)
for \(k\ge 23\). The \(j=1048576\) cell has partner \(5U+1048576\). Dies at
\(k=21\) for unpaired \(\{0,1048576\}\) (\(G\) at \(j=1048576\) is \(0\)).
Dies at \(k=22\) for leftover 11-set (got \(6\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+1048576\), \(j=0\) for
\(k\ge 20\) or \(j=1048576\) for \(k\ge 22\). Do **not** call
\(\mathrm{ph1048576\_lo\_js}\) below \(k=23\). Do **not** call
\(\mathrm{ph524288\_lo\_js}\) below \(k=22\). Census \(k=8\): unpaired
\(0\), leftover+pal \(0\), clip \(0\) (not yet covering). Do **not**
PREFIX pal-center tot from small \(k\). Do **not** PREFIX leftover
spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not**
catalogue leftover \(d\). Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_yu.py --certify` (~0.14s).
Dump: `research/cycle_yu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/YF/YI/YL/YO/YR
(even \(n=5U/2+1048576\) 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even \(n=5U/2+1048576\) is the 2-fold of Cycle YR for \(k\ge 2\))

Fold identity \(n=2\cdot\mathrm{ph524288}(k-1)\). Covering
(\(n<4U\)) only for \(k\ge 20\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=19\) for
covering (\(n=2359296\ge 2097152\)).

## Lemma (unpaired left Green is \(\{0,1048576\}\) for \(k\ge 22\))

Special-case \(3\) at \(k=20\) and \(1\) at \(k=21\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=21\) for \(\{0,1048576\}\). Do **not** kill unpaired at
\(j=0\) for \(k\ge 20\) or at \(j=1048576\) for \(k\ge 22\).

## Lemma (leftover+pal is the even 11-set for \(k\ge 23\))

Special \(6\) at \(k=22\), \(1\) at \(k=21\), \(2\) at \(k=20\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=22\) for the 11-set. Do **not** call
\(\mathrm{ph1048576\_lo\_js}\) below \(k=23\).

## Lemma (\(j=1048576\) has partner \(5U+1048576\))

Clip-edge at \(j=2097152\). Status: **lemma**. Algebra through
\(k\le 64\). **Killed** at \(k=20\) for \(\mathrm{pal\_kind}\) pair
at \(j=1048576\); at \(k=21\) for \(G(n,1048576)=1\).

## Verdict

`LEMMA` (even \(n=5U/2+1048576\) is 2-fold of YR; unpaired \(\{0,1048576\}\)
for \(k\ge 22\); leftover 11-set for \(k\ge 23\); \(j=1048576\) has
partner \(5U+1048576\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired \(\{0,1048576\}\) at \(k=21\); leftover 11-set at
\(k=22\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); leftover
\(=\mathrm{clip\_gp}\); unpaired equals even partner-\(5U+2\)
slice; \(\mathrm{pal\_kind}\) pair at \(j=1048576\);
\(G(\mathrm{ph}+1048576,1048576)=1\) at \(k=21\); covering at
\(n=5U/2+1048576\) at \(k=19\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_yu.md` (this note)
- `research/cycle_yu.py`
- `research/cycle_yu.json`
