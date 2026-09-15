# Cycle ZL: even partner-\(5U+33554432\) unpaired extra has count \(J_k-5592405(-1)^k+5592404\)

Even-\(n\) unpaired extra at \(j=2n-5U-33554432\) with \(j\ge 2\) has count
\(J_k-5592405(-1)^k+5592404\) for \(k\ge 26\). Together with Cycle ZK they are
\(J_{k+1}-11184811(-1)^k+11184810\) for \(k\ge 26\). The first even cell is
\(n=5U/2+16777218\), \(j=4\) for \(k\ge 24\). Dies at \(k=25\) for the
\(k\ge 26\) formula (got \(11184810\), not \(22369620\)) and at \(k=24\)
(got \(2796202\), not \(5592404\)). Dies at \(k=26\) for even equals odd
(got \(22369620\), not \(22369622\)) and for tot equals \(J_{k+1}\)
(got \(44739242\), not \(44739243\)). Dies at \(k=25\) for tot equals
\(J_{k+1}\) (got \(22369620\), not \(22369621\)) and at \(k=24\) (got
\(5592404\), not \(11184811\)). Do **not** kill even equals odd at
\(k\le 25\) (both \(0\) through \(k=23\), both \(2796202\) at \(k=24\),
both \(11184810\) at \(k=25\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or even partner-\(5U+16777216\) or even
partner-\(5U+4194304\) or even partner-\(5U+1048576\) or even
partner-\(5U+262144\) or even partner-\(5U+65536\) or even
partner-\(5U+16384\) or even partner-\(5U+4096\) or even partner-\(5U+1024\)
or even partner-\(5U+256\) or even partner-\(5U+64\) or even
partner-\(5U+16\) or odd partner-\(5U+4\) or odd at \(k=25\) (all
\(11184810\)). Do **not** kill equals even partner-\(5U+8388608\) or even
partner-\(5U+2097152\) or even partner-\(5U+524288\) or even
partner-\(5U+131072\) or even partner-\(5U+32768\) or even
partner-\(5U+8192\) or even partner-\(5U+2048\) or even partner-\(5U+512\)
or even partner-\(5U+128\) or even partner-\(5U+32\) or even
partner-\(5U+8\) at \(k=26\) (all \(22369620\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+16777218\), \(j=4\) for
\(k\ge 24\). Census \(k=8\): even slice \(0\), tot \(0\), first `None`
(not yet covering). Do **not** PREFIX pal-center tot from small \(k\).
Do **not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_zl.py --certify` (~0.14s; dump `wall_s` 0.139).
Dump: `research/cycle_zl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YF/YG/YH/YI/YJ/YK/YL/YM/YN/YO/YP/YQ/YR/YS/YT/YU/YV/YW/YX/YY/YZ/ZA/ZB/ZC/ZD/ZE/ZF/ZG/ZH/ZI/ZJ/ZK
(even partner-\(5U+33554432\) slice \(J_k-5592405(-1)^k+5592404\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+33554432\) unpaired extra has count \(J_k-5592405(-1)^k+5592404\) for \(k\ge 26\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM/YN/YP/YQ/YS/YT/YV/YW/YY/YZ/ZB/ZE/ZH/ZK.
Special-case \(0\) at \(k\le 23\), \(2796202\) at \(k=24\), and \(11184810\) at
\(k=25\). Equals the odd slice through \(k=25\); odd \(=\) even \(+2\)
for \(k\ge 26\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=25\) and \(k=24\) for the
\(k\ge 26\) formula; at \(k=26\) for equals odd; at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\);
equals even partner-\(5U+512\). Do **not** kill even equals odd at
\(k\le 25\). Do **not** kill equals \(\mathrm{clip\_gp}\) or even
partner-\(5U+16777216\) or even partner-\(5U+4194304\) or even
partner-\(5U+1048576\) or even partner-\(5U+262144\) or even
partner-\(5U+65536\) or even partner-\(5U+16384\) or even
partner-\(5U+4096\) or even partner-\(5U+1024\) or even
partner-\(5U+256\) or even partner-\(5U+64\) or even partner-\(5U+16\)
or odd partner-\(5U+4\) or odd at \(k=25\). Do **not** kill equals even
partner-\(5U+8388608\) or even partner-\(5U+2097152\) or even
partner-\(5U+524288\) or even partner-\(5U+131072\) or even
partner-\(5U+32768\) or even partner-\(5U+8192\) or even
partner-\(5U+2048\) or even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\)
at \(k=26\). Do **not** PREFIX a unified partner-offset formula in \(m\).

## Lemma (odd+even partner-\(5U+33554432\) tot is \(J_{k+1}-11184811(-1)^k+11184810\) for \(k\ge 26\))

Equals \(2(J_k-5592405(-1)^k+5592404)+2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=24\), at
\(k=25\), and at \(k=26\) for tot equals \(J_{k+1}\). Do **not**
PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+16777218\), \(j=4\) for \(k\ge 24\))

The \(j=4\) cell has partner \(5U+33554432\). At \(k=23\), \(n=37748738\ge 33554432\)
is not covering (though \(G(37748738,4)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=23\) for covering. Do **not** kill unpaired at \(j=4\) for
\(k\ge 24\).

## Verdict

`LEMMA` (even partner-\(5U+33554432\) slice count \(J_k-5592405(-1)^k+5592404\) for
\(k\ge 26\); tot \(J_{k+1}-11184811(-1)^k+11184810\) for \(k\ge 26\); first
even cell is \(n=5U/2+16777218\), \(j=4\) for \(k\ge 24\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 26\) formula at \(k=25\) and at
\(k=24\); equals odd at \(k=26\); tot equals \(J_{k+1}\) at \(k=24\),
\(k=25\), and \(k=26\); equals \(\mathrm{clip\_gp}\) at \(k=8\); equals
\(J_k\) at \(k=8\); covering at \(n=5U/2+16777218\) at \(k=23\); pal-center
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

- `research/cycle_zl.md` (this note)
- `research/cycle_zl.py`
- `research/cycle_zl.json`
