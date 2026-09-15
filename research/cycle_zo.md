# Cycle ZO: even partner-\(5U+67108864\) unpaired extra has count \(J_k+11184811(-1)^k+11184810\)

Even-\(n\) unpaired extra at \(j=2n-5U-67108864\) with \(j\ge 2\) has count
\(J_k+11184811(-1)^k+11184810\) for \(k\ge 27\), equal to the odd Cycle ZN slice.
Together they are \(J_{k+1}+22369621(-1)^k+22369620\) for \(k\ge 27\). The first
even cell is \(n=5U/2+33554434\), \(j=4\) for \(k\ge 25\). Dies at \(k=26\)
for the \(k\ge 27\) formula (got \(22369620\), not \(44739242\)) and at \(k=25\)
(got \(5592404\), not \(11184810\)). Dies at \(k=25\) for even equals odd
(got \(5592404\), not \(5592406\)) and at \(k=26\) (got \(22369620\), not
\(22369622\)). Dies at \(k=25\) for tot equals \(J_{k+1}\) (got \(11184810\), not
\(22369621\)) and at \(k=26\) (got \(44739242\), not \(44739243\)) and at \(k=27\)
(got \(89478484\), not \(89478485\)). Do **not** kill even equals odd at
\(k\le 24\) (both \(0\)) or \(k\ge 27\). Do **not** kill equals even
partner-\(5U+33554432\) or even partner-\(5U+8388608\) or even
partner-\(5U+2097152\) or even partner-\(5U+524288\) or even
partner-\(5U+131072\) or even partner-\(5U+32768\) or even partner-\(5U+8192\)
or even partner-\(5U+2048\) or even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\) at
\(k=26\) (all \(22369620\)). Do **not** kill \(\mathrm{pal\_kind}\) unpaired at
\(n=5U/2+33554434\), \(j=4\) for \(k\ge 25\). Census \(k=8\): even slice
\(0\), tot \(0\), first `None` (not yet covering). Do **not** PREFIX pal-center
tot from small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
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

Certify: `python3 research/cycle_zo.py --certify` (~0.14s).
Dump: `research/cycle_zo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YF/YG/YH/YI/YJ/YK/YL/YM/YN/YO/YP/YQ/YR/YS/YT/YU/YV/YW/YX/YY/YZ/ZA/ZB/ZC/ZD/ZE/ZF/ZG/ZH/ZI/ZJ/ZK/ZL/ZM/ZN
(even partner-\(5U+67108864\) slice \(J_k+11184811(-1)^k+11184810\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+67108864\) unpaired extra has count \(J_k+11184811(-1)^k+11184810\) for \(k\ge 27\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM/YN/YP/YQ/YS/YT/YV/YW/YY/YZ/ZB/ZE/ZH/ZK/ZN.
Special-case \(0\) at \(k\le 24\), \(5592404\) at \(k=25\), and \(22369620\) at
\(k=26\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=26\) and \(k=25\) for the
\(k\ge 27\) formula; at \(k=25\) and \(k=26\) for even equals odd.
Do **not** kill even equals odd at \(k\le 24\) or \(k\ge 27\). Do **not**
kill equals even partner-\(5U+33554432\) or even partner-\(5U+8388608\) or even
partner-\(5U+2097152\) or even partner-\(5U+524288\) or even
partner-\(5U+131072\) or even partner-\(5U+32768\) or even partner-\(5U+8192\)
or even partner-\(5U+2048\) or even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\) at
\(k=26\). Do **not** PREFIX a unified partner-offset formula in \(m\).
Do **not** kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+33554434\),
\(j=4\) for \(k\ge 25\).

## Lemma (odd+even partner-\(5U+67108864\) tot is \(J_{k+1}+22369621(-1)^k+22369620\) for \(k\ge 27\))

Status: **lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=25\), \(k=26\), and \(k=27\) for tot equals \(J_{k+1}\).

## Lemma (first even partner-\(5U+67108864\) cell is \(n=5U/2+33554434\), \(j=4\) for \(k\ge 25\))

Partner of \(j=4\) is \(5U+67108864\). Covering \(k\ge 25\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=24\) for covering (\(n=75497474\ge 67108864\)).

## Verdict

`LEMMA` (even partner-\(5U+67108864\) unpaired extra has count
\(J_k+11184811(-1)^k+11184810\) for \(k\ge 27\); tot
\(J_{k+1}+22369621(-1)^k+22369620\) for \(k\ge 27\); first cell
\(n=5U/2+33554434\), \(j=4\) for \(k\ge 25\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (formula at \(k=26\) and \(k=25\); even equals odd at \(k=25\)
and \(k=26\); tot equals \(J_{k+1}\) at \(k=25\), \(k=26\), and \(k=27\);
covering at \(k=24\); unpaired \(=\mathrm{clip\_gp}\) at \(k=8\); pal-center
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

- `research/cycle_zo.md` (this note)
- `research/cycle_zo.py`
- `research/cycle_zo.json`
