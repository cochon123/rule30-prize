# Cycle YJ: odd partner-\(5U+65536\) unpaired extra has count \(J_k+10923(-1)^k+10922\)

Odd-\(n\) unpaired extra at \(j=2n-5U-65536\) with \(j\ge 2\) has count
\(J_k+10923(-1)^k+10922\) for \(k\ge 17\). The first cell is
\(n=5U/2+32769\), \(j=2\) for \(k\ge 15\). Dies at \(k=16\) for that
formula (got \(21846\), not \(43690\)). Dies at \(k=15\) for that
formula (got \(5462\), not \(10922\)). Dies at \(k=15\) for equals odd
partner-\(5U+32768\) and odd partner-\(5U+16384\) and
\(\mathrm{clip\_gp}\) (got \(5462\), not \(10922\)). Dies at
\(k=14\) for covering. Do **not** kill equals odd
partner-\(5U+32768\) or odd partner-\(5U+8192\) or odd
partner-\(5U+2048\) or odd partner-\(5U+512\) or odd partner-\(5U+128\)
or odd partner-\(5U+32\) or odd partner-\(5U+8\) or odd
partner-\(5U+4\) at \(k=16\) (all \(21846\)). Do **not** kill equals
odd partner-\(5U+16384\) or even partner-\(5U+16384\) or odd
partner-\(5U+4096\) or even partner-\(5U+4096\) or odd
partner-\(5U+1024\) or odd partner-\(5U+256\) or odd partner-\(5U+64\)
or odd partner-\(5U+16\) or odd partner-\(5U+4\) or
\(\mathrm{clip\_gp}\) at \(k=17\) (all \(43690\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+32769\), \(j=2\) for
\(k\ge 15\). Census \(k=8\): odd slice \(0\), first `None` (not yet
covering). Do **not** PREFIX pal-center tot from small \(k\). Do
**not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
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

Certify: `python3 research/cycle_yj.py --certify` (~0.14s).
Dump: `research/cycle_yj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YG/YH/YI
(odd partner-\(5U+65536\) slice \(J_k+10923(-1)^k+10922\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+65536\) unpaired extra has count \(J_k+10923(-1)^k+10922\) for \(k\ge 17\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH.
Special-case \(0\) at \(k\le 14\), \(5462\) at \(k=15\), and \(21846\) at
\(k=16\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=16\) and \(k=15\) for the
\(k\ge 17\) formula; at \(k=15\) for equals odd partner-\(5U+32768\);
equals odd partner-\(5U+16384\); equals \(\mathrm{clip\_gp}\); at
\(k=14\) for equals odd partner-\(5U+32768\); at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\).
Do **not** kill equals odd partner-\(5U+32768\) or odd
partner-\(5U+8192\) or odd partner-\(5U+2048\) or odd
partner-\(5U+512\) or odd partner-\(5U+128\) or odd partner-\(5U+32\)
or odd partner-\(5U+8\) or odd partner-\(5U+4\) at \(k=16\). Do
**not** kill equals odd partner-\(5U+16384\) or even
partner-\(5U+16384\) or odd partner-\(5U+4096\) or even
partner-\(5U+4096\) or odd partner-\(5U+1024\) or odd
partner-\(5U+256\) or odd partner-\(5U+64\) or odd partner-\(5U+16\)
or odd partner-\(5U+4\) or \(\mathrm{clip\_gp}\) at \(k=17\). Do
**not** PREFIX a unified partner-offset formula in \(m\).

## Lemma (first odd slice cell is \(n=5U/2+32769\), \(j=2\) for \(k\ge 15\))

The \(j=2\) cell has partner \(5U+65536\). At \(k=14\), \(n=73729\ge 65536\)
is not covering (though \(G(73729,2)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=14\) for covering. Do **not** kill unpaired at \(j=2\) for
\(k\ge 15\).

## Verdict

`LEMMA` (odd partner-\(5U+65536\) slice count \(J_k+10923(-1)^k+10922\) for
\(k\ge 17\); first odd cell is \(n=5U/2+32769\), \(j=2\) for \(k\ge 15\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd slice equals the \(k\ge 17\) formula at \(k=16\) and at
\(k=15\); equals odd partner-\(5U+32768\) at \(k=15\) and at \(k=14\);
equals \(\mathrm{clip\_gp}\) at \(k=8\); equals \(J_k\) at \(k=8\);
covering at \(n=5U/2+32769\) at \(k=14\); pal-center tot equals
\(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_yj.md` (this note)
- `research/cycle_yj.py`
- `research/cycle_yj.json`
