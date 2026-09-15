# Cycle YY: odd partner-\(5U+2097152\) unpaired extra has count \(J_k-349525(-1)^k+349526\)

Odd-\(n\) unpaired extra at \(j=2n-5U-2097152\) with \(j\ge 2\) has count
\(J_k-349525(-1)^k+349526\) for \(k\ge 22\). The first cell is
\(n=5U/2+1048577\), \(j=2\) for \(k\ge 20\). Dies at \(k=21\) for that
formula (got \(699050\), not \(1398102\)). Dies at \(k=20\) for that
formula (got \(174762\), not \(349526\)). Dies at \(k=20\) for equals odd
partner-\(5U+1048576\) and odd partner-\(5U+524288\) and
\(\mathrm{clip\_gp}\) (got \(174762\), not \(349526\)/\(349525\)). Dies at
\(k=19\) for covering. Do **not** kill equals odd
partner-\(5U+1048576\) or even partner-\(5U+1048576\) or odd
partner-\(5U+262144\) or even partner-\(5U+262144\) or odd
partner-\(5U+65536\) or even partner-\(5U+65536\) or odd
partner-\(5U+16384\) or even partner-\(5U+16384\) or odd
partner-\(5U+4096\) or even partner-\(5U+4096\) or odd
partner-\(5U+1024\) or even partner-\(5U+1024\) or odd
partner-\(5U+256\) or even partner-\(5U+256\) or odd
partner-\(5U+64\) or even partner-\(5U+64\) or odd
partner-\(5U+16\) or even partner-\(5U+16\) or odd partner-\(5U+4\)
or \(\mathrm{clip\_gp}\) at \(k=21\) (all \(699050\)). Do **not** kill
equals odd partner-\(5U+524288\) or odd partner-\(5U+131072\) or odd
partner-\(5U+32768\) or odd partner-\(5U+8192\) or odd
partner-\(5U+2048\) or odd partner-\(5U+512\) or odd partner-\(5U+128\)
or odd partner-\(5U+32\) or odd partner-\(5U+8\) or odd
partner-\(5U+4\) at \(k=22\) (all \(1398102\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+1048577\), \(j=2\) for
\(k\ge 20\). Census \(k=8\): odd slice \(0\), first `None` (not yet
covering). Do **not** PREFIX pal-center tot from small \(k\). Do **not**
PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot.
Do **not** catalogue leftover \(d\). Do **not** claim pal-center tot
equals \(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\) one-by-one.
Do **not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
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

Certify: `python3 research/cycle_yy.py --certify` (~0.14s).
Dump: `research/cycle_yy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ/YA/YB/YC/YD/YE/YG/YH/YJ/YK/YL/YM/YN/YP/YQ/YR/YS/YT/YU/YV/YW/YX
(odd partner-\(5U+2097152\) slice \(J_k-349525(-1)^k+349526\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+2097152\) unpaired extra has count \(J_k-349525(-1)^k+349526\) for \(k\ge 22\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY/YA/YB/YD/YE/YG/YH/YJ/YK/YM/YN/YP/YQ/YS/YT/YV/YW.
Special-case \(0\) at \(k\le 19\), \(174762\) at \(k=20\), and \(699050\) at
\(k=21\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=21\) and \(k=20\) for the
\(k\ge 22\) formula; at \(k=20\) for equals odd partner-\(5U+1048576\);
equals odd partner-\(5U+524288\); equals \(\mathrm{clip\_gp}\); at
\(k=19\) for equals odd partner-\(5U+1048576\); at \(k=8\) for equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\).
Do **not** kill equals odd partner-\(5U+1048576\) or even
partner-\(5U+1048576\) or odd partner-\(5U+262144\) or even
partner-\(5U+262144\) or odd partner-\(5U+65536\) or even
partner-\(5U+65536\) or odd partner-\(5U+16384\) or even
partner-\(5U+16384\) or odd partner-\(5U+4096\) or even
partner-\(5U+4096\) or odd partner-\(5U+1024\) or even
partner-\(5U+1024\) or odd partner-\(5U+256\) or even
partner-\(5U+256\) or odd partner-\(5U+64\) or even
partner-\(5U+64\) or odd partner-\(5U+16\) or even
partner-\(5U+16\) or odd partner-\(5U+4\) or \(\mathrm{clip\_gp}\) at
\(k=21\). Do **not** kill equals odd partner-\(5U+524288\) or odd
partner-\(5U+131072\) or odd partner-\(5U+32768\) or odd
partner-\(5U+8192\) or odd partner-\(5U+2048\) or odd partner-\(5U+512\)
or odd partner-\(5U+128\) or odd partner-\(5U+32\) or odd
partner-\(5U+8\) or odd partner-\(5U+4\) at \(k=22\). Do **not** PREFIX
a unified partner-offset formula in \(m\).

## Lemma (first odd slice cell is \(n=5U/2+1048577\), \(j=2\) for \(k\ge 20\))

The \(j=2\) cell has partner \(5U+2097152\). At \(k=19\), \(n=2359297\ge 2097152\)
is not covering (though \(G(2359297,2)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=19\) for covering. Do **not** kill unpaired at \(j=2\) for
\(k\ge 20\).

## Verdict

`LEMMA` (odd partner-\(5U+2097152\) slice count \(J_k-349525(-1)^k+349526\) for
\(k\ge 22\); first odd cell is \(n=5U/2+1048577\), \(j=2\) for \(k\ge 20\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd slice equals the \(k\ge 22\) formula at \(k=21\) and at
\(k=20\); equals odd partner-\(5U+1048576\) at \(k=20\) and at \(k=19\);
equals \(\mathrm{clip\_gp}\) at \(k=8\); equals \(J_k\) at \(k=8\);
covering at \(n=5U/2+1048577\) at \(k=19\); pal-center tot equals
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

- `research/cycle_yy.md` (this note)
- `research/cycle_yy.py`
- `research/cycle_yy.json`
