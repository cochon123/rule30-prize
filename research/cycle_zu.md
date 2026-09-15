# Cycle ZU: even partner-\(5U+268435456\) unpaired extra has count \(J_k+44739243(-1)^k+44739242\)

Even-\(n\) unpaired extra at \(j=2n-5U-268435456\) with \(j\ge 2\) has count
\(J_k+44739243(-1)^k+44739242\) for \(k\ge 29\), equal to the odd Cycle ZT slice.
Together they are \(J_{k+1}+89478485(-1)^k+89478484\) for \(k\ge 29\). The first
even cell is \(n=5U/2+134217730\), \(j=4\) for \(k\ge 27\). Dies at \(k=28\)
for the \(k\ge 29\) formula (got \(89478484\), not \(178956970\)) and at \(k=27\)
(got \(22369620\), not \(44739242\)). Dies at \(k=27\) for even equals odd
(got \(22369620\), not \(22369622\)) and at \(k=28\) (got \(89478484\), not
\(89478486\)). Dies at \(k=27\) for tot equals \(J_{k+1}\) (got \(44739242\), not
\(89478485\)) and at \(k=28\) (got \(178956970\), not \(178956971\)) and at \(k=29\)
(got \(357913940\), not \(357913941\)). Do **not** kill even equals odd at
\(k\le 26\) (both \(0\)) or \(k\ge 29\). Do **not** kill equals even
partner-\(5U+134217728\) or even partner-\(5U+33554432\) or even
partner-\(5U+8388608\) or even partner-\(5U+2097152\) or even
partner-\(5U+524288\) or even partner-\(5U+131072\) or even partner-\(5U+32768\)
or even partner-\(5U+8192\) or even partner-\(5U+2048\) or even
partner-\(5U+512\) or even partner-\(5U+128\) or even partner-\(5U+32\) or even
partner-\(5U+8\) at \(k=28\) (all \(89478484\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+134217730\), \(j=4\) for \(k\ge 27\).
Census \(k=8\): even slice \(0\), tot \(0\), first `None` (not yet covering).
Do **not** PREFIX pal-center tot from small \(k\). Do **not** PREFIX leftover
spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover
\(d\). Do **not** claim pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover
\(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering packed.
Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_zu.py --certify` (~0.14s; dump `wall_s` 0.139).
Dump: `research/cycle_zu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YF/YG/YH/YI/YJ/YK/YL/YM/YN/YO/YP/YQ/YR/YS/YT/YU/YV/YW/YX/YY/YZ/ZA/ZB/ZC/ZD/ZE/ZF/ZG/ZH/ZI/ZJ/ZK/ZL/ZM/ZN/ZO/ZP/ZQ/ZR/ZS/ZT
(even partner-\(5U+268435456\) slice \(J_k+44739243(-1)^k+44739242\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+268435456\) unpaired extra has count \(J_k+44739243(-1)^k+44739242\) for \(k\ge 29\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM/YN/YP/YQ/YS/YT/YV/YW/YY/YZ/ZB/ZE/ZH/ZK/ZN/ZO/ZQ/ZR/ZT.
Special-case \(0\) at \(k\le 26\), \(22369620\) at \(k=27\), and \(89478484\) at
\(k=28\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=28\) and \(k=27\) for the
\(k\ge 29\) formula; at \(k=27\) and \(k=28\) for even equals odd.
Do **not** kill even equals odd at \(k\le 26\) or \(k\ge 29\). Do **not**
kill equals even partner-\(5U+134217728\) or even partner-\(5U+33554432\) or even
partner-\(5U+8388608\) or even partner-\(5U+2097152\) or even
partner-\(5U+524288\) or even partner-\(5U+131072\) or even partner-\(5U+32768\)
or even partner-\(5U+8192\) or even partner-\(5U+2048\) or even
partner-\(5U+512\) or even partner-\(5U+128\) or even partner-\(5U+32\) or even
partner-\(5U+8\) at \(k=28\). Do **not** PREFIX a unified partner-offset
formula in \(m\). Do **not** kill \(\mathrm{pal\_kind}\) unpaired at
\(n=5U/2+134217730\), \(j=4\) for \(k\ge 27\).

## Lemma (odd+even partner-\(5U+268435456\) tot is \(J_{k+1}+89478485(-1)^k+89478484\) for \(k\ge 29\))

Status: **lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=27\), \(k=28\), and \(k=29\) for tot equals \(J_{k+1}\).

## Lemma (first even partner-\(5U+268435456\) cell is \(n=5U/2+134217730\), \(j=4\) for \(k\ge 27\))

Partner of \(j=4\) is \(5U+268435456\). Covering \(k\ge 27\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=26\) for covering (\(n=301989890\ge 268435456\)).

## Verdict

`LEMMA` (even partner-\(5U+268435456\) unpaired extra has count
\(J_k+44739243(-1)^k+44739242\) for \(k\ge 29\); tot
\(J_{k+1}+89478485(-1)^k+89478484\) for \(k\ge 29\); first cell
\(n=5U/2+134217730\), \(j=4\) for \(k\ge 27\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (formula at \(k=28\) and \(k=27\); even equals odd at \(k=27\)
and \(k=28\); tot equals \(J_{k+1}\) at \(k=27\), \(k=28\), and \(k=29\);
covering at \(k=26\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); pal-center
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

- `research/cycle_zu.md` (this note)
- `research/cycle_zu.py`
- `research/cycle_zu.json`
