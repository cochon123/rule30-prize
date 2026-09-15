# Cycle ZR: even partner-\(5U+134217728\) unpaired extra has count \(J_k-22369621(-1)^k+22369620\)

Even-\(n\) unpaired extra at \(j=2n-5U-134217728\) with \(j\ge 2\) has count
\(J_k-22369621(-1)^k+22369620\) for \(k\ge 28\). Together with Cycle ZQ they are
\(J_{k+1}-44739243(-1)^k+44739242\) for \(k\ge 28\). The first even cell is
\(n=5U/2+67108866\), \(j=4\) for \(k\ge 26\). Dies at \(k=27\) for the
\(k\ge 28\) formula (got \(44739242\), not \(89478484\)) and at \(k=26\)
(got \(11184810\), not \(22369620\)). Dies at \(k=28\) for even equals odd
(got \(89478484\), not \(89478486\)) and for tot equals \(J_{k+1}\)
(got \(178956970\), not \(178956971\)). Dies at \(k=27\) for tot equals
\(J_{k+1}\) (got \(89478484\), not \(89478485\)) and at \(k=26\) (got
\(22369620\), not \(44739243\)). Do **not** kill even equals odd at
\(k\le 27\) (both \(0\) through \(k=25\), both \(11184810\) at \(k=26\),
both \(44739242\) at \(k=27\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or even partner-\(5U+67108864\) or even
partner-\(5U+16777216\) or even partner-\(5U+4194304\) or even
partner-\(5U+1048576\) or even partner-\(5U+262144\) or even
partner-\(5U+65536\) or even partner-\(5U+16384\) or even partner-\(5U+4096\)
or even partner-\(5U+1024\) or even partner-\(5U+256\) or even
partner-\(5U+64\) or even partner-\(5U+16\) or odd partner-\(5U+4\) or odd at
\(k=27\) (all \(44739242\)). Do **not** kill equals even partner-\(5U+33554432\)
or even partner-\(5U+8388608\) or even partner-\(5U+2097152\) or even
partner-\(5U+524288\) or even partner-\(5U+131072\) or even
partner-\(5U+32768\) or even partner-\(5U+8192\) or even partner-\(5U+2048\)
or even partner-\(5U+512\) or even partner-\(5U+128\) or even
partner-\(5U+32\) or even partner-\(5U+8\) at \(k=28\) (all \(89478484\)).
Do **not** kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+67108866\),
\(j=4\) for \(k\ge 26\). Census \(k=8\): even slice \(0\), tot \(0\), first
`None` (not yet covering). Do **not** PREFIX pal-center tot from small \(k\).
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

Certify: `python3 research/cycle_zr.py --certify`
Dump: `research/cycle_zr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YF/YG/YH/YI/YJ/YK/YL/YM/YN/YO/YP/YQ/YR/YS/YT/YU/YV/YW/YX/YY/YZ/ZA/ZB/ZC/ZD/ZE/ZF/ZG/ZH/ZI/ZJ/ZK/ZL/ZM/ZN/ZO/ZP/ZQ
(even partner-\(5U+134217728\) slice \(J_k-22369621(-1)^k+22369620\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+134217728\) unpaired extra has count \(J_k-22369621(-1)^k+22369620\) for \(k\ge 28\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM/YN/YP/YQ/YS/YT/YV/YW/YY/YZ/ZB/ZE/ZH/ZK/ZN/ZQ.
Special-case \(0\) at \(k\le 25\), \(11184810\) at \(k=26\), and \(44739242\) at
\(k=27\). Equals the odd slice through \(k=27\); odd \(=\) even \(+2\)
for \(k\ge 28\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=27\) and \(k=26\) for the
\(k\ge 28\) formula; at \(k=28\) for equals odd; at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\);
equals even partner-\(5U+512\). Do **not** kill even equals odd at
\(k\le 27\). Do **not** kill equals \(\mathrm{clip\_gp}\) or even
partner-\(5U+67108864\) or even partner-\(5U+16777216\) or even
partner-\(5U+4194304\) or even partner-\(5U+1048576\) or even
partner-\(5U+262144\) or even partner-\(5U+65536\) or even
partner-\(5U+16384\) or even partner-\(5U+4096\) or even
partner-\(5U+1024\) or even partner-\(5U+256\) or even partner-\(5U+64\)
or even partner-\(5U+16\) or odd partner-\(5U+4\) or odd at \(k=27\).
Do **not** kill equals even partner-\(5U+33554432\) or even
partner-\(5U+8388608\) or even partner-\(5U+2097152\) or even
partner-\(5U+524288\) or even partner-\(5U+131072\) or even
partner-\(5U+32768\) or even partner-\(5U+8192\) or even
partner-\(5U+2048\) or even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\)
at \(k=28\). Do **not** PREFIX a unified partner-offset formula in \(m\).

## Lemma (odd+even partner-\(5U+134217728\) tot is \(J_{k+1}-44739243(-1)^k+44739242\) for \(k\ge 28\))

Equals \(2(J_k-22369621(-1)^k+22369620)+2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=26\), at
\(k=27\), and at \(k=28\) for tot equals \(J_{k+1}\). Do **not**
PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+67108866\), \(j=4\) for \(k\ge 26\))

The \(j=4\) cell has partner \(5U+134217728\). At \(k=25\), \(n=150994946\ge 134217728\)
is not covering (though \(G(150994946,4)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=25\) for covering. Do **not** kill unpaired at \(j=4\) for
\(k\ge 26\).

## Verdict

`LEMMA` (even partner-\(5U+134217728\) slice count \(J_k-22369621(-1)^k+22369620\) for
\(k\ge 28\); tot \(J_{k+1}-44739243(-1)^k+44739242\) for \(k\ge 28\); first
even cell is \(n=5U/2+67108866\), \(j=4\) for \(k\ge 26\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 28\) formula at \(k=27\) and at
\(k=26\); equals odd at \(k=28\); tot equals \(J_{k+1}\) at \(k=26\),
\(k=27\), and \(k=28\); equals \(\mathrm{clip\_gp}\) at \(k=8\); equals
\(J_k\) at \(k=8\); covering at \(n=5U/2+67108866\) at \(k=25\); pal-center
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

- `research/cycle_zr.md` (this note)
- `research/cycle_zr.py`
- `research/cycle_zr.json`
