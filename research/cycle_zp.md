# Cycle ZP: even \(n=5U/2+134217728\) is the 2-fold of Cycle ZM at \(k-1\)

Covering \(n=5U/2+134217728\) equals \(2\cdot(5U_p/2+67108864)\). Even doubling
sends parent left Green to child left Green with
\(\mathrm{pal\_kind}\) and clip-edge preserved, so unpaired left is
\(\{0,134217728\}\) for \(k\ge 29\) and leftover+pal is the even 11-set
\(\{U/2,U/2+134217728,U/2+268435456,U,U+134217728,U+268435456,2U,2U+134217728,2U+268435456,5U/2,n\}\)
for \(k\ge 30\). The \(j=134217728\) cell has partner \(5U+134217728\). Dies at
\(k=28\) for unpaired \(\{0,134217728\}\) (\(G\) at \(j=134217728\) is \(0\)).
Dies at \(k=29\) for leftover 11-set (got \(6\)). Leftover at first covering
\(k=27\) is \(2\), not a blind \(+1\) shift of Cycle ZM's \(2\). Do **not**
kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+134217728\), \(j=0\) for
\(k\ge 27\) or \(j=134217728\) for \(k\ge 29\). Do **not** call
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

Certify: `python3 research/cycle_zp.py --certify` (~0.14s; dump `wall_s` 0.144).
Dump: `research/cycle_zp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/YF/YI/YL/YO/YR/YU/YX/ZA/ZD/ZG/ZJ/ZM
(even \(n=5U/2+134217728\) 2-fold; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even \(n=5U/2+134217728\) is the 2-fold of Cycle ZM for \(k\ge 2\))

Fold identity \(n=2\cdot\mathrm{ph67108864}(k-1)\). Covering
(\(n<4U\)) only for \(k\ge 27\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=26\) for
covering (\(n=301989888\ge 268435456\)).

## Lemma (unpaired left Green is \(\{0,134217728\}\) for \(k\ge 29\))

Special-case \(3\) at \(k=27\) and \(1\) at \(k=28\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=28\) for \(\{0,134217728\}\). Do **not** kill unpaired at
\(j=0\) for \(k\ge 27\) or at \(j=134217728\) for \(k\ge 29\).

## Lemma (leftover+pal is the even 11-set for \(k\ge 30\))

Special \(6\) at \(k=29\), \(1\) at \(k=28\), \(2\) at \(k=27\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=29\) for the 11-set. Do **not** call
\(\mathrm{ph134217728\_lo\_js}\) below \(k=30\).

## Lemma (\(j=134217728\) has partner \(5U+134217728\))

Clip-edge at \(j=268435456\). Status: **lemma**. Algebra through
\(k\le 64\). **Killed** at \(k=27\) for \(\mathrm{pal\_kind}\) pair
at \(j=134217728\); at \(k=28\) for \(G(n,134217728)=1\).

## Verdict

`LEMMA` (even \(n=5U/2+134217728\) is 2-fold of ZM; unpaired \(\{0,134217728\}\)
for \(k\ge 29\); leftover 11-set for \(k\ge 30\); \(j=134217728\) has
partner \(5U+134217728\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (unpaired \(\{0,134217728\}\) at \(k=28\); leftover 11-set at
\(k=29\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); leftover
\(=\mathrm{clip\_gp}\); unpaired equals even partner-\(5U+2\)
slice; \(\mathrm{pal\_kind}\) pair at \(j=134217728\);
\(G(\mathrm{ph}+134217728,134217728)=1\) at \(k=28\); covering at
\(n=5U/2+134217728\) at \(k=26\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_zp.md` (this note)
- `research/cycle_zp.py`
- `research/cycle_zp.json`
