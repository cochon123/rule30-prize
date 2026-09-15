# Cycle ZT: odd partner-\(5U+268435456\) unpaired extra has count \(J_k+44739243(-1)^k+44739242\)

Odd-\(n\) unpaired extra at \(j=2n-5U-268435456\) with \(j\ge 2\) has count
\(J_k+44739243(-1)^k+44739242\) for \(k\ge 29\). The first cell is
\(n=5U/2+134217729\), \(j=2\) for \(k\ge 27\). Dies at \(k=28\) for that
formula (got \(89478486\), not \(178956970\)). Dies at \(k=27\) for that
formula (got \(22369622\), not \(44739242\)). Dies at \(k=27\) for equals odd
partner-\(5U+134217728\) and odd partner-\(5U+67108864\) and
\(\mathrm{clip\_gp}\) (got \(22369622\), not \(44739242\)). Dies at
\(k=26\) for covering. Do **not** kill equals odd
partner-\(5U+134217728\) or odd partner-\(5U+33554432\) or odd
partner-\(5U+8388608\) or odd partner-\(5U+2097152\) or odd
partner-\(5U+524288\) or odd partner-\(5U+131072\) or odd
partner-\(5U+32768\) or odd partner-\(5U+8192\) or odd
partner-\(5U+2048\) or odd partner-\(5U+512\) or odd partner-\(5U+128\)
or odd partner-\(5U+32\) or odd partner-\(5U+8\) or odd partner-\(5U+4\)
at \(k=28\) (all \(89478486\)). Do **not** kill \(\mathrm{pal\_kind}\)
unpaired at \(n=5U/2+134217729\), \(j=2\) for \(k\ge 27\). Census \(k=8\):
odd slice \(0\), first `None` (not yet covering). Do **not** PREFIX
pal-center tot from small \(k\). Do **not** PREFIX leftover spat tot.
Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover
\(d\). Do **not** claim pal-center tot equals \(S\oplus T\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\). Do
**not** claim pal-left leftover xor vanishes for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_zt.py --certify` (~0.14s; dump `wall_s` 0.14).
Dump: `research/cycle_zt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YG/YH/YJ/YK/YL/YM/YN/YP/YQ/YR/YS/YT/YU/YV/YW/YX/YY/YZ/ZA/ZB/ZC/ZD/ZE/ZF/ZG/ZH/ZI/ZJ/ZK/ZL/ZM/ZN/ZO/ZP/ZQ/ZR/ZS
(odd partner-\(5U+268435456\) slice \(J_k+44739243(-1)^k+44739242\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+268435456\) unpaired extra has count \(J_k+44739243(-1)^k+44739242\) for \(k\ge 29\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM/YN/YP/YQ/YS/YT/YV/YW/YY/YZ/ZB/ZE/ZH/ZK/ZN/ZQ.
Special-case \(0\) at \(k\le 26\), \(22369622\) at \(k=27\), and \(89478486\) at
\(k=28\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=28\) and \(k=27\) for the
\(k\ge 29\) formula; at \(k=27\) for equals odd partner-\(5U+134217728\);
equals odd partner-\(5U+67108864\); equals \(\mathrm{clip\_gp}\); at
\(k=26\) for equals odd partner-\(5U+134217728\); at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\).
Do **not** kill equals the even-\(m\) family at \(k=28\). Do **not**
PREFIX a unified partner-offset formula in \(m\). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+134217729\), \(j=2\) for
\(k\ge 27\).

## Lemma (first odd partner-\(5U+268435456\) cell is \(n=5U/2+134217729\), \(j=2\) for \(k\ge 27\))

Partner of \(j=2\) is \(5U+268435456\). Covering \(k\ge 27\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=26\) for covering (\(n=301989889\ge 268435456\)).

## Verdict

`LEMMA` (odd partner-\(5U+268435456\) unpaired extra has count
\(J_k+44739243(-1)^k+44739242\) for \(k\ge 29\); first cell
\(n=5U/2+134217729\), \(j=2\) for \(k\ge 27\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (formula at \(k=28\) and \(k=27\); equals odd
partner-\(5U+134217728\) at \(k=27\); equals odd partner-\(5U+67108864\)
at \(k=27\); equals \(\mathrm{clip\_gp}\) at \(k=27\); covering at
\(k=26\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); unpaired
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

- `research/cycle_zt.md` (this note)
- `research/cycle_zt.py`
- `research/cycle_zt.json`
