# Cycle ZW: odd partner-\(5U+536870912\) unpaired extra has count \(J_k-89478485(-1)^k+89478486\)

Odd-\(n\) unpaired extra at \(j=2n-5U-536870912\) with \(j\ge 2\) has count
\(J_k-89478485(-1)^k+89478486\) for \(k\ge 30\). The first cell is
\(n=5U/2+268435457\), \(j=2\) for \(k\ge 28\). Dies at \(k=29\) for that
formula (got \(178956970\), not \(357913942\)). Dies at \(k=28\) for that
formula (got \(44739242\), not \(89478486\)). Dies at \(k=28\) for equals odd
partner-\(5U+268435456\) and odd partner-\(5U+134217728\) and
\(\mathrm{clip\_gp}\) (got \(44739242\), not \(89478486\)/\(89478485\)). Dies at
\(k=27\) for covering. Do **not** kill equals odd
partner-\(5U+268435456\) or odd partner-\(5U+67108864\) or odd
partner-\(5U+16777216\) or odd partner-\(5U+4194304\) or odd
partner-\(5U+1048576\) or odd partner-\(5U+262144\) or odd
partner-\(5U+65536\) or odd partner-\(5U+16384\) or odd
partner-\(5U+4096\) or odd partner-\(5U+1024\) or odd partner-\(5U+256\)
or odd partner-\(5U+64\) or odd partner-\(5U+16\) or odd partner-\(5U+4\)
or even partner-\(5U+268435456\) or even partner-\(5U+67108864\) or even
partner-\(5U+16777216\) or \(\mathrm{clip\_gp}\) at \(k=29\) (all
\(178956970\)). Do **not** kill \(\mathrm{pal\_kind}\) unpaired at
\(n=5U/2+268435457\), \(j=2\) for \(k\ge 28\). Census \(k=8\): odd slice
\(0\), first `None` (not yet covering). Do **not** PREFIX pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue
leftover \(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\). Do **not** walk \(k=11\) covering packed. Do **not** walk
\(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_zw.py --certify` (~0.14s; dump `wall_s` 0.138).
Dump: `research/cycle_zw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YG/YH/YJ/YK/YL/YM/YN/YP/YQ/YR/YS/YT/YU/YV/YW/YX/YY/YZ/ZA/ZB/ZC/ZD/ZE/ZF/ZG/ZH/ZI/ZJ/ZK/ZL/ZM/ZN/ZO/ZP/ZQ/ZR/ZS/ZT/ZU/ZV
(odd partner-\(5U+536870912\) slice \(J_k-89478485(-1)^k+89478486\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+536870912\) unpaired extra has count \(J_k-89478485(-1)^k+89478486\) for \(k\ge 30\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM/YN/YP/YQ/YS/YT/YV/YW/YY/YZ/ZB/ZE/ZH/ZK/ZN/ZQ/ZT.
Special-case \(0\) at \(k\le 27\), \(44739242\) at \(k=28\), and \(178956970\) at
\(k=29\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=29\) and \(k=28\) for the
\(k\ge 30\) formula; at \(k=28\) for equals odd partner-\(5U+268435456\);
equals odd partner-\(5U+134217728\); equals \(\mathrm{clip\_gp}\); at
\(k=27\) for equals odd partner-\(5U+268435456\); at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\).
Do **not** kill equals the even-\(m\) family at \(k=29\). Do **not**
PREFIX a unified partner-offset formula in \(m\). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+268435457\), \(j=2\) for
\(k\ge 28\).

## Lemma (first odd partner-\(5U+536870912\) cell is \(n=5U/2+268435457\), \(j=2\) for \(k\ge 28\))

Partner of \(j=2\) is \(5U+536870912\). Covering \(k\ge 28\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=27\) for covering (\(n=603979777\ge 536870912\)).

## Verdict

`LEMMA` (odd partner-\(5U+536870912\) unpaired extra has count
\(J_k-89478485(-1)^k+89478486\) for \(k\ge 30\); first cell
\(n=5U/2+268435457\), \(j=2\) for \(k\ge 28\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (formula at \(k=29\) and \(k=28\); equals odd
partner-\(5U+268435456\) at \(k=28\); equals odd partner-\(5U+134217728\)
at \(k=28\); equals \(\mathrm{clip\_gp}\) at \(k=28\); covering at
\(k=27\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); unpaired
equals \(J_k\); unpaired equals odd partner-\(5U+512\); pal-center
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

- `research/cycle_zw.md` (this note)
- `research/cycle_zw.py`
- `research/cycle_zw.json`
