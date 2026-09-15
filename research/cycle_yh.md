# Cycle YH: even partner-\(5U+32768\) unpaired extra has count \(J_k-5461(-1)^k+5460\)

Even-\(n\) unpaired extra at \(j=2n-5U-32768\) with \(j\ge 2\) has count
\(J_k-5461(-1)^k+5460\) for \(k\ge 16\). Together with Cycle YG they are
\(J_{k+1}-10923(-1)^k+10922\) for \(k\ge 16\). The first even cell is
\(n=5U/2+16386\), \(j=4\) for \(k\ge 14\). Dies at \(k=15\) for the
\(k\ge 16\) formula (got \(10922\), not \(21844\)) and at \(k=14\)
(got \(2730\), not \(5460\)). Dies at \(k=16\) for even equals odd
(got \(21844\), not \(21846\)) and for tot equals \(J_{k+1}\)
(got \(43690\), not \(43691\)). Dies at \(k=15\) for tot equals
\(J_{k+1}\) (got \(21844\), not \(21845\)). Do **not** kill even
equals odd at \(k\le 15\) (both \(0\) through \(k=13\), both \(2730\)
at \(k=14\), both \(10922\) at \(k=15\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or even partner-\(5U+16384\) or even
partner-\(5U+4096\) or even partner-\(5U+1024\) or even
partner-\(5U+256\) or even partner-\(5U+64\) or even partner-\(5U+16\)
or odd at \(k=15\) (all \(10922\)). Do **not** kill equals even
partner-\(5U+8192\) or even partner-\(5U+2048\) or even
partner-\(5U+512\) or even partner-\(5U+128\) or even partner-\(5U+32\)
or even partner-\(5U+8\) at \(k=16\) (all \(21844\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+16386\), \(j=4\) for
\(k\ge 14\). Census \(k=8\): even slice \(0\), tot \(0\), first `None`
(not yet covering). Do **not** PREFIX pal-center tot from small \(k\).
Do **not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue
leftover \(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_yh.py --certify` (~0.14s).
Dump: `research/cycle_yh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YF/YG
(even partner-\(5U+32768\) slice \(J_k-5461(-1)^k+5460\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+32768\) unpaired extra has count \(J_k-5461(-1)^k+5460\) for \(k\ge 16\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG.
Special-case \(0\) at \(k\le 13\), \(2730\) at \(k=14\), and \(10922\) at
\(k=15\). Equals the odd slice through \(k=15\); odd \(=\) even \(+2\)
for \(k\ge 16\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=15\) and \(k=14\) for the
\(k\ge 16\) formula; at \(k=16\) for equals odd; at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\);
equals even partner-\(5U+512\). Do **not** kill even equals odd at
\(k\le 15\). Do **not** kill equals \(\mathrm{clip\_gp}\) or even
partner-\(5U+16384\) or even partner-\(5U+4096\) or even
partner-\(5U+1024\) or even partner-\(5U+256\) or even
partner-\(5U+64\) or even partner-\(5U+16\) or odd at \(k=15\). Do
**not** kill equals even partner-\(5U+8192\) or even partner-\(5U+2048\)
or even partner-\(5U+512\) or even partner-\(5U+128\) or even
partner-\(5U+32\) or even partner-\(5U+8\) at \(k=16\). Do **not**
PREFIX a unified partner-offset formula in \(m\).

## Lemma (odd+even partner-\(5U+32768\) tot is \(J_{k+1}-10923(-1)^k+10922\) for \(k\ge 16\))

Equals \(2(J_k-5461(-1)^k+5460)+2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=14\), at
\(k=15\), and at \(k=16\) for tot equals \(J_{k+1}\). Do **not**
PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+16386\), \(j=4\) for \(k\ge 14\))

The \(j=4\) cell has partner \(5U+32768\). At \(k=13\), \(n=36866\ge 32768\)
is not covering (though \(G(36866,4)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=13\) for covering. Do **not** kill unpaired at \(j=4\) for
\(k\ge 14\).

## Verdict

`LEMMA` (even partner-\(5U+32768\) slice count \(J_k-5461(-1)^k+5460\) for
\(k\ge 16\); tot \(J_{k+1}-10923(-1)^k+10922\) for \(k\ge 16\); first
even cell is \(n=5U/2+16386\), \(j=4\) for \(k\ge 14\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 16\) formula at \(k=15\) and at
\(k=14\); equals odd at \(k=16\); tot equals \(J_{k+1}\) at \(k=14\),
\(k=15\), and \(k=16\); equals \(\mathrm{clip\_gp}\) at \(k=8\); equals
\(J_k\) at \(k=8\); covering at \(n=5U/2+16386\) at \(k=13\); pal-center
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

- `research/cycle_yh.md` (this note)
- `research/cycle_yh.py`
- `research/cycle_yh.json`
