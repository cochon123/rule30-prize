# Cycle YA: odd partner-\(5U+8192\) unpaired extra has count \(J_k-1365(-1)^k+1366\)

Odd-\(n\) unpaired extra at \(j=2n-5U-8192\) with \(j\ge 2\) has count
\(J_k-1365(-1)^k+1366\) for \(k\ge 14\). The first cell is
\(n=5U/2+4097\), \(j=2\) for \(k\ge 12\). Dies at \(k=13\) for that
formula (got \(2730\), not \(5462\)). Dies at \(k=12\) for that
formula (got \(682\), not \(1366\)). Dies at \(k=12\) for equals odd
partner-\(5U+4096\) (got \(682\), not \(1366\)). Do **not** kill equals
odd partner-\(5U+4096\) or odd partner-\(5U+1024\) or odd
partner-\(5U+256\) or odd partner-\(5U+64\) or odd partner-\(5U+4\)
or \(\mathrm{clip\_gp}\) at \(k=13\) (all \(2730\)). Do **not** kill
equals odd partner-\(5U+2048\) or odd partner-\(5U+512\) or odd
partner-\(5U+128\) or odd partner-\(5U+32\) or odd partner-\(5U+8\)
or odd partner-\(5U+4\) at \(k=14\) (all \(5462\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+4097\), \(j=2\) for
\(k\ge 12\). Census \(k=8\): odd slice \(0\) (not yet covering). Do
**not** PREFIX pal-center tot from small \(k\). Do **not** PREFIX
leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do
**not** catalogue leftover \(d\). Do **not** claim pal-center tot
equals \(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_ya.py --certify` (~0.14s).
Dump: `research/cycle_ya.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU/XV/XW/XX/XY/XZ
(odd partner-\(5U+8192\) slice \(J_k-1365(-1)^k+1366\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+8192\) unpaired extra has count \(J_k-1365(-1)^k+1366\) for \(k\ge 14\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU/XV/XX/XY.
Special-case \(0\) at \(k\le 11\), \(682\) at \(k=12\), and \(2730\) at
\(k=13\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=13\) and \(k=12\) for the
\(k\ge 14\) formula; at \(k=12\) for equals odd partner-\(5U+4096\);
equals odd partner-\(5U+2048\); equals \(\mathrm{clip\_gp}\); at
\(k=11\) for equals odd partner-\(5U+4096\); equals odd
partner-\(5U+2048\); equals odd partner-\(5U+1024\); equals
\(\mathrm{clip\_gp}\); at \(k=10\) for equals odd partner-\(5U+2048\);
equals odd partner-\(5U+1024\); equals \(\mathrm{clip\_gp}\); at
\(k=9\) for equals odd partner-\(5U+1024\); equals \(\mathrm{clip\_gp}\);
at \(k=8\) for equals odd partner-\(5U+512\); equals
\(\mathrm{clip\_gp}\); equals \(J_k\); equals even partner-\(5U+512\).
Do **not** kill equals odd partner-\(5U+4096\) or odd
partner-\(5U+1024\) or odd partner-\(5U+256\) or odd partner-\(5U+64\)
or odd partner-\(5U+4\) or \(\mathrm{clip\_gp}\) at \(k=13\). Do
**not** kill equals odd partner-\(5U+2048\) or odd partner-\(5U+512\)
or odd partner-\(5U+128\) or odd partner-\(5U+32\) or odd
partner-\(5U+8\) or odd partner-\(5U+4\) at \(k=14\). Do **not**
PREFIX a unified partner-offset formula in \(m\).

## Lemma (first odd slice cell is \(n=5U/2+4097\), \(j=2\) for \(k\ge 12\))

The \(j=2\) cell has partner \(5U+8192\). At \(k=11\), \(n=9217\ge 8192\)
is not covering (though \(G(9217,2)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=11\) for covering. Do **not** kill unpaired at \(j=2\) for
\(k\ge 12\).

## Verdict

`LEMMA` (odd partner-\(5U+8192\) slice count \(J_k-1365(-1)^k+1366\) for
\(k\ge 14\); first odd cell is \(n=5U/2+4097\), \(j=2\) for
\(k\ge 12\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd slice equals the \(k\ge 14\) formula at \(k=13\) and at
\(k=12\); equals odd partner-\(5U+4096\) at \(k=12\) and at \(k=11\);
equals odd partner-\(5U+2048\) at \(k=12\), \(k=11\), and \(k=10\);
equals odd partner-\(5U+1024\) at \(k=11\), \(k=10\), and \(k=9\);
equals \(\mathrm{clip\_gp}\) at \(k=12\), \(k=11\), \(k=10\), \(k=9\),
and \(k=8\); equals odd partner-\(5U+512\) at \(k=8\); equals \(J_k\)
at \(k=8\); equals even partner-\(5U+512\) at \(k=8\); covering at
\(n=5U/2+4097\) at \(k=11\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ya.md` (this note)
- `research/cycle_ya.py`
- `research/cycle_ya.json`
