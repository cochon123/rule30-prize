# Cycle YN: even partner-\(5U+131072\) unpaired extra has count \(J_k-21845(-1)^k+21844\)

Even-\(n\) unpaired extra at \(j=2n-5U-131072\) with \(j\ge 2\) has count
\(J_k-21845(-1)^k+21844\) for \(k\ge 18\). Together with Cycle YM they are
\(J_{k+1}-43691(-1)^k+43690\) for \(k\ge 18\). The first even cell is
\(n=5U/2+65538\), \(j=4\) for \(k\ge 16\). Dies at \(k=17\) for the
\(k\ge 18\) formula (got \(43690\), not \(87380\)) and at \(k=16\)
(got \(10922\), not \(21844\)). Dies at \(k=18\) for even equals odd
(got \(87380\), not \(87382\)) and for tot equals \(J_{k+1}\)
(got \(174762\), not \(174763\)). Dies at \(k=17\) for tot equals
\(J_{k+1}\) (got \(87380\), not \(87381\)) and at \(k=16\) (got
\(21844\), not \(43691\)). Do **not** kill even equals odd at
\(k\le 17\) (both \(0\) through \(k=15\), both \(10922\) at \(k=16\),
both \(43690\) at \(k=17\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or even partner-\(5U+65536\) or even
partner-\(5U+16384\) or even partner-\(5U+4096\) or even
partner-\(5U+1024\) or even partner-\(5U+256\) or even partner-\(5U+64\)
or even partner-\(5U+16\) or odd at \(k=17\) (all \(43690\)). Do
**not** kill equals even partner-\(5U+32768\) or even partner-\(5U+8192\)
or even partner-\(5U+2048\) or even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\)
at \(k=18\) (all \(87380\)). Do **not** kill \(\mathrm{pal\_kind}\)
unpaired at \(n=5U/2+65538\), \(j=4\) for \(k\ge 16\). Census \(k=8\):
even slice \(0\), tot \(0\), first `None` (not yet covering). Do
**not** PREFIX pal-center tot from small \(k\). Do **not** PREFIX
leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do
**not** catalogue leftover \(d\). Do **not** claim pal-center tot
equals \(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_yn.py --certify` (~0.14s).
Dump: `research/cycle_yn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YF/YG/YH/YI/YJ/YK/YL/YM
(even partner-\(5U+131072\) slice \(J_k-21845(-1)^k+21844\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+131072\) unpaired extra has count \(J_k-21845(-1)^k+21844\) for \(k\ge 18\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM.
Special-case \(0\) at \(k\le 15\), \(10922\) at \(k=16\), and \(43690\) at
\(k=17\). Equals the odd slice through \(k=17\); odd \(=\) even \(+2\)
for \(k\ge 18\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=17\) and \(k=16\) for the
\(k\ge 18\) formula; at \(k=18\) for equals odd; at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\);
equals even partner-\(5U+512\). Do **not** kill even equals odd at
\(k\le 17\). Do **not** kill equals \(\mathrm{clip\_gp}\) or even
partner-\(5U+65536\) or even partner-\(5U+16384\) or even
partner-\(5U+4096\) or even partner-\(5U+1024\) or even
partner-\(5U+256\) or even partner-\(5U+64\) or even partner-\(5U+16\)
or odd at \(k=17\). Do **not** kill equals even partner-\(5U+32768\)
or even partner-\(5U+8192\) or even partner-\(5U+2048\) or even
partner-\(5U+512\) or even partner-\(5U+128\) or even partner-\(5U+32\)
or even partner-\(5U+8\) at \(k=18\). Do **not** PREFIX a unified
partner-offset formula in \(m\).

## Lemma (odd+even partner-\(5U+131072\) tot is \(J_{k+1}-43691(-1)^k+43690\) for \(k\ge 18\))

Equals \(2(J_k-21845(-1)^k+21844)+2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=16\), at
\(k=17\), and at \(k=18\) for tot equals \(J_{k+1}\). Do **not**
PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+65538\), \(j=4\) for \(k\ge 16\))

The \(j=4\) cell has partner \(5U+131072\). At \(k=15\), \(n=147458\ge 131072\)
is not covering (though \(G(147458,4)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=15\) for covering. Do **not** kill unpaired at \(j=4\) for
\(k\ge 16\).

## Verdict

`LEMMA` (even partner-\(5U+131072\) slice count \(J_k-21845(-1)^k+21844\) for
\(k\ge 18\); tot \(J_{k+1}-43691(-1)^k+43690\) for \(k\ge 18\); first
even cell is \(n=5U/2+65538\), \(j=4\) for \(k\ge 16\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 18\) formula at \(k=17\) and at
\(k=16\); equals odd at \(k=18\); tot equals \(J_{k+1}\) at \(k=16\),
\(k=17\), and \(k=18\); equals \(\mathrm{clip\_gp}\) at \(k=8\); equals
\(J_k\) at \(k=8\); covering at \(n=5U/2+65538\) at \(k=15\); pal-center
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

- `research/cycle_yn.md` (this note)
- `research/cycle_yn.py`
- `research/cycle_yn.json`
