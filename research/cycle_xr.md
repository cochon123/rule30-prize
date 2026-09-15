# Cycle XR: odd partner-\(5U+1024\) unpaired extra has count \(J_k+171(-1)^k+170\)

Odd-\(n\) unpaired extra at \(j=2n-5U-1024\) with \(j\ge 2\) has count
\(J_k+171(-1)^k+170\) for \(k\ge 11\). The first cell is
\(n=5U/2+513\), \(j=2\) for \(k\ge 9\). Dies at \(k=10\) for that
formula (got \(342\), not \(682\)). Dies at \(k=9\) for that
formula (got \(86\), not \(170\)). Dies at \(k=9\) for equals odd
partner-\(5U+512\) (got \(86\), not \(170\)). Do **not** kill equals
odd partner-\(5U+512\) or odd partner-\(5U+128\) or odd
partner-\(5U+32\) or odd partner-\(5U+8\) or odd partner-\(5U+4\)
at \(k=10\) (all \(342\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or odd partner-\(5U+256\) or odd
partner-\(5U+64\) or odd partner-\(5U+4\) at \(k=11\) (all \(682\)).
Do **not** kill \(\mathrm{pal\_kind}\) unpaired at
\(n=5U/2+513\), \(j=2\) for \(k\ge 9\). Census \(k=8\): odd slice
\(0\) (not yet covering). Do **not** PREFIX pal-center tot from
small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover
\(d\). Do **not** claim pal-center tot equals \(S\oplus T\). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_xr.py --certify` (~0.14s).
Dump: `research/cycle_xr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ
(odd partner-\(5U+1024\) slice \(J_k+171(-1)^k+170\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+1024\) unpaired extra has count \(J_k+171(-1)^k+170\) for \(k\ge 11\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP.
Special-case \(0\) at \(k\le 8\), \(86\) at \(k=9\), and \(342\) at
\(k=10\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=10\) and \(k=9\) for the
\(k\ge 11\) formula; at \(k=9\) for equals odd partner-\(5U+512\);
equals odd partner-\(5U+256\); equals \(\mathrm{clip\_gp}\); at
\(k=8\) for equals odd partner-\(5U+512\); equals odd
partner-\(5U+256\); equals \(\mathrm{clip\_gp}\); equals \(J_k\);
equals even partner-\(5U+512\). Do **not** kill equals odd
partner-\(5U+512\) or odd partner-\(5U+128\) or odd partner-\(5U+32\)
or odd partner-\(5U+8\) or odd partner-\(5U+4\) at \(k=10\). Do
**not** kill equals \(\mathrm{clip\_gp}\) or odd partner-\(5U+256\)
or odd partner-\(5U+64\) or odd partner-\(5U+4\) at \(k=11\). Do
**not** PREFIX a unified partner-offset formula in \(m\).

## Lemma (first odd slice cell is \(n=5U/2+513\), \(j=2\) for \(k\ge 9\))

The \(j=2\) cell has partner \(5U+1024\). At \(k=8\), \(n=1153\ge 1024\)
is not covering (though \(G(1153,2)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=8\) for covering. Do **not** kill unpaired at \(j=2\) for
\(k\ge 9\).

## Verdict

`LEMMA` (odd partner-\(5U+1024\) slice count \(J_k+171(-1)^k+170\) for
\(k\ge 11\); first odd cell is \(n=5U/2+513\), \(j=2\) for
\(k\ge 9\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd slice equals the \(k\ge 11\) formula at \(k=10\) and at
\(k=9\); equals odd partner-\(5U+512\) at \(k=9\) and at \(k=8\);
equals odd partner-\(5U+256\) at \(k=9\) and at \(k=8\); equals
\(\mathrm{clip\_gp}\) at \(k=9\) and at \(k=8\); equals \(J_k\) at
\(k=8\); equals even partner-\(5U+512\) at \(k=8\); covering at
\(n=5U/2+513\) at \(k=8\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_xr.md` (this note)
- `research/cycle_xr.py`
- `research/cycle_xr.json`
