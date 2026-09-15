# Cycle ZS: even \(n=5U/2+268435456\) is the 2-fold of Cycle ZP at \(k-1\)

Covering \(n=5U/2+268435456\) equals \(2\cdot(5U_p/2+134217728)\). Even doubling
sends parent left Green to child left Green with
\(\mathrm{pal\_kind}\) and clip-edge preserved, so unpaired left is
\(\{0,268435456\}\) for \(k\ge 30\) and leftover+pal is the even 11-set
\(\{U/2,U/2+268435456,U/2+536870912,U,U+268435456,U+536870912,2U,2U+268435456,2U+536870912,5U/2,n\}\)
for \(k\ge 31\). The \(j=268435456\) cell has partner \(5U+268435456\). Dies at
\(k=29\) for unpaired \(\{0,268435456\}\) (\(G\) at \(j=268435456\) is \(0\)).
Dies at \(k=30\) for leftover 11-set (got \(6\)). Leftover at first covering
\(k=28\) is \(2\), not a blind \(+1\) shift of Cycle ZP's \(2\). Do **not**
kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+268435456\), \(j=0\) for
\(k\ge 28\) or \(j=268435456\) for \(k\ge 30\). Do **not** call
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

Certify: `python3 research/cycle_zs.py --certify` (~0.14s; dump `wall_s` 0.145).
Dump: `research/cycle_zs.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/YF/YI/YL/YO/YR/YU/YX/ZA/ZD/ZG/ZJ/ZM/ZP
(even \(n=5U/2+268435456\) 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even \(n=5U/2+268435456\) is the 2-fold of Cycle ZP for \(k\ge 2\))

Fold identity \(n=2\cdot\mathrm{ph134217728}(k-1)\). Covering
(\(n<4U\)) only for \(k\ge 28\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=27\) for
covering (\(n=603979776\ge 536870912\)).

## Lemma (unpaired left Green is \(\{0,268435456\}\) for \(k\ge 30\))

Special-case \(3\) at \(k=28\) and \(1\) at \(k=29\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=29\) for \(\{0,268435456\}\). Do **not** kill unpaired at
\(j=0\) for \(k\ge 28\) or at \(j=268435456\) for \(k\ge 30\).

## Lemma (leftover+pal is the even 11-set for \(k\ge 31\))

Special \(6\) at \(k=30\), \(1\) at \(k=29\), \(2\) at \(k=28\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=30\) for the 11-set. Do **not** call
\(\mathrm{ph268435456\_lo\_js}\) below \(k=31\).

## Lemma (\(j=268435456\) has partner \(5U+268435456\))

Clip-edge at \(j=536870912\). Status: **lemma**. Algebra through
\(k\le 64\). **Killed** at \(k=28\) for \(\mathrm{pal\_kind}\) pair
at \(j=268435456\); at \(k=29\) for \(G(n,268435456)=1\).

## Verdict

`LEMMA` (even \(n=5U/2+268435456\) is 2-fold of ZP; unpaired \(\{0,268435456\}\)
for \(k\ge 30\); leftover 11-set for \(k\ge 31\); \(j=268435456\) has
partner \(5U+268435456\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired \(\{0,268435456\}\) at \(k=29\); leftover 11-set at
\(k=30\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); leftover
\(=\mathrm{clip\_gp}\); unpaired equals even partner-\(5U+2\)
slice; \(\mathrm{pal\_kind}\) pair at \(j=268435456\);
\(G(\mathrm{ph}+268435456,268435456)=1\) at \(k=29\); covering at
\(n=5U/2+268435456\) at \(k=27\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_zs.md` (this note)
- `research/cycle_zs.py`
- `research/cycle_zs.json`
