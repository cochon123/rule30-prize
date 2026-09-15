# Cycle XU: odd partner-\(5U+2048\) unpaired extra has count \(J_k-341(-1)^k+342\)

Odd-\(n\) unpaired extra at \(j=2n-5U-2048\) with \(j\ge 2\) has count
\(J_k-341(-1)^k+342\) for \(k\ge 12\). The first cell is
\(n=5U/2+1025\), \(j=2\) for \(k\ge 10\). Dies at \(k=11\) for that
formula (got \(682\), not \(1366\)). Dies at \(k=10\) for that
formula (got \(170\), not \(342\)). Dies at \(k=10\) for equals odd
partner-\(5U+1024\) (got \(170\), not \(342\)). Do **not** kill equals
odd partner-\(5U+1024\) or odd partner-\(5U+256\) or odd
partner-\(5U+64\) or odd partner-\(5U+4\) or \(\mathrm{clip\_gp}\)
at \(k=11\) (all \(682\)). Do **not** kill equals odd
partner-\(5U+512\) or odd partner-\(5U+128\) or odd partner-\(5U+32\)
or odd partner-\(5U+8\) or odd partner-\(5U+4\) at \(k=12\) (all
\(1366\)). Do **not** kill \(\mathrm{pal\_kind}\) unpaired at
\(n=5U/2+1025\), \(j=2\) for \(k\ge 10\). Census \(k=8\): odd slice
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

Certify: `python3 research/cycle_xu.py --certify` (~0.14s).
Dump: `research/cycle_xu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT
(odd partner-\(5U+2048\) slice \(J_k-341(-1)^k+342\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+2048\) unpaired extra has count \(J_k-341(-1)^k+342\) for \(k\ge 12\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS.
Special-case \(0\) at \(k\le 9\), \(170\) at \(k=10\), and \(682\) at
\(k=11\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=11\) and \(k=10\) for the
\(k\ge 12\) formula; at \(k=10\) for equals odd partner-\(5U+1024\);
equals odd partner-\(5U+512\); equals \(\mathrm{clip\_gp}\); at
\(k=9\) for equals odd partner-\(5U+1024\); equals odd
partner-\(5U+512\); equals \(\mathrm{clip\_gp}\); at \(k=8\) for
equals odd partner-\(5U+512\); equals \(\mathrm{clip\_gp}\); equals
\(J_k\); equals even partner-\(5U+512\). Do **not** kill equals odd
partner-\(5U+1024\) or odd partner-\(5U+256\) or odd partner-\(5U+64\)
or odd partner-\(5U+4\) or \(\mathrm{clip\_gp}\) at \(k=11\). Do
**not** kill equals odd partner-\(5U+512\) or odd partner-\(5U+128\)
or odd partner-\(5U+32\) or odd partner-\(5U+8\) or odd
partner-\(5U+4\) at \(k=12\). Do **not** PREFIX a unified
partner-offset formula in \(m\).

## Lemma (first odd slice cell is \(n=5U/2+1025\), \(j=2\) for \(k\ge 10\))

The \(j=2\) cell has partner \(5U+2048\). At \(k=9\), \(n=2305\ge 2048\)
is not covering (though \(G(2305,2)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=9\) for covering. Do **not** kill unpaired at \(j=2\) for
\(k\ge 10\).

## Verdict

`LEMMA` (odd partner-\(5U+2048\) slice count \(J_k-341(-1)^k+342\) for
\(k\ge 12\); first odd cell is \(n=5U/2+1025\), \(j=2\) for
\(k\ge 10\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd slice equals the \(k\ge 12\) formula at \(k=11\) and at
\(k=10\); equals odd partner-\(5U+1024\) at \(k=10\) and at \(k=9\);
equals odd partner-\(5U+512\) at \(k=10\) and at \(k=9\) and at
\(k=8\); equals \(\mathrm{clip\_gp}\) at \(k=10\) and at \(k=9\) and
at \(k=8\); equals \(J_k\) at \(k=8\); equals even partner-\(5U+512\)
at \(k=8\); covering at \(n=5U/2+1025\) at \(k=9\); pal-center tot
equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_xu.md` (this note)
- `research/cycle_xu.py`
- `research/cycle_xu.json`
