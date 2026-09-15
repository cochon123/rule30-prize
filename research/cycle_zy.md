# Cycle ZY: even \(n=5U/2+1073741824\) is the 2-fold of Cycle ZV at \(k-1\)

Covering \(n=5U/2+1073741824\) equals \(2\cdot(5U_p/2+536870912)\). Even doubling
sends parent left Green to child left Green with
\(\mathrm{pal\_kind}\) and clip-edge preserved, so unpaired left is
\(\{0,1073741824\}\) for \(k\ge 32\) and leftover+pal is the even 11-set
\(\{U/2,U/2+1073741824,U/2+2147483648,U,U+1073741824,U+2147483648,2U,2U+1073741824,2U+2147483648,5U/2,n\}\)
for \(k\ge 33\). The \(j=1073741824\) cell has partner \(5U+1073741824\). Dies at
\(k=31\) for unpaired \(\{0,1073741824\}\) (\(G\) at \(j=1073741824\) is \(0\)).
Dies at \(k=32\) for leftover 11-set (got \(6\)). Leftover at first covering
\(k=30\) is \(2\), not a blind \(+1\) shift of Cycle ZV's \(2\). Do **not**
kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+1073741824\), \(j=0\) for
\(k\ge 30\) or \(j=1073741824\) for \(k\ge 32\). Do **not** call
\(\mathrm{ph1073741824\_lo\_js}\) below \(k=33\). Do **not** call
\(\mathrm{ph536870912\_lo\_js}\) below \(k=32\). Do **not** call
\(\mathrm{ph268435456\_lo\_js}\) below \(k=31\). Do **not** call
\(\mathrm{ph134217728\_lo\_js}\) below \(k=30\). Do **not** call
\(\mathrm{ph67108864\_lo\_js}\) below \(k=29\). Do **not** call
\(\mathrm{ph33554432\_lo\_js}\) below \(k=28\). Do **not** call
\(\mathrm{ph16777216\_lo\_js}\) below \(k=27\). Do **not** call
\(\mathrm{ph8388608\_lo\_js}\) below \(k=26\). Do **not** call
\(\mathrm{ph4194304\_lo\_js}\) below \(k=25\). Census \(k=8\): unpaired
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

Certify: `python3 research/cycle_zy.py --certify` (~0.14s; dump `wall_s` 0.145).
Dump: `research/cycle_zy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/YF/YI/YL/YO/YR/YU/YX/ZA/ZD/ZG/ZJ/ZM/ZP/ZS/ZV
(even \(n=5U/2+1073741824\) 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even \(n=5U/2+1073741824\) is the 2-fold of Cycle ZV for \(k\ge 2\))

Fold identity \(n=2\cdot\mathrm{ph536870912}(k-1)\). Covering
(\(n<4U\)) only for \(k\ge 30\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=29\) for
covering (\(n=2415919104\ge 2147483648\)).

## Lemma (unpaired left Green is \(\{0,1073741824\}\) for \(k\ge 32\))

Special-case \(3\) at \(k=30\) and \(1\) at \(k=31\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=31\) for \(\{0,1073741824\}\). Do **not** kill unpaired at
\(j=0\) for \(k\ge 30\) or at \(j=1073741824\) for \(k\ge 32\).

## Lemma (leftover+pal is the even 11-set for \(k\ge 33\))

Special \(6\) at \(k=32\), \(1\) at \(k=31\), \(2\) at \(k=30\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=32\) for the 11-set. Do **not** call
\(\mathrm{ph1073741824\_lo\_js}\) below \(k=33\).

## Lemma (\(j=1073741824\) has partner \(5U+1073741824\))

Clip-edge at \(j=2147483648\). Status: **lemma**. Algebra through
\(k\le 64\). **Killed** at \(k=30\) for \(\mathrm{pal\_kind}\) pair
at \(j=1073741824\); at \(k=31\) for \(G(n,1073741824)=1\).

## Verdict

`LEMMA` (even \(n=5U/2+1073741824\) is 2-fold of ZV; unpaired \(\{0,1073741824\}\)
for \(k\ge 32\); leftover 11-set for \(k\ge 33\); \(j=1073741824\) has
partner \(5U+1073741824\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired \(\{0,1073741824\}\) at \(k=31\); leftover 11-set at
\(k=32\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); leftover
\(=\mathrm{clip\_gp}\); unpaired equals even partner-\(5U+2\)
slice; \(\mathrm{pal\_kind}\) pair at \(j=1073741824\);
\(G(\mathrm{ph}+1073741824,1073741824)=1\) at \(k=31\); covering at
\(n=5U/2+1073741824\) at \(k=29\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_zy.md` (this note)
- `research/cycle_zy.py`
- `research/cycle_zy.json`
