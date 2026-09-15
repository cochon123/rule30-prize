# Cycle XO: odd partner-\(5U+512\) unpaired extra has count \(J_k-85(-1)^k+86\)

Odd-\(n\) unpaired extra at \(j=2n-5U-512\) with \(j\ge 2\) has count
\(J_k-85(-1)^k+86\) for \(k\ge 10\). The first cell is
\(n=5U/2+257\), \(j=2\) for \(k\ge 8\). Dies at \(k=9\) for that
formula (got \(170\), not \(342\)). Dies at \(k=8\) for that
formula (got \(42\), not \(86\)). Dies at \(k=8\) for equals odd
partner-\(5U+256\) (got \(42\), not \(86\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or odd partner-\(5U+256\) or odd
partner-\(5U+64\) or odd partner-\(5U+4\) at \(k=9\) (all \(170\)).
Do **not** kill \(\mathrm{pal\_kind}\) unpaired at
\(n=5U/2+257\), \(j=2\) for \(k\ge 8\). Census \(k=8\): odd slice
\(42\), first \((897,2)\). Do **not** PREFIX pal-center tot from
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

Certify: `python3 research/cycle_xo.py --certify` (~0.14s).
Dump: `research/cycle_xo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WU/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN
(odd partner-\(5U+512\) slice \(J_k-85(-1)^k+86\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+512\) unpaired extra has count \(J_k-85(-1)^k+86\) for \(k\ge 10\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM.
Special-case \(0\) at \(k\le 7\), \(42\) at \(k=8\), and \(170\) at
\(k=9\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=9\) and \(k=8\) for the
\(k\ge 10\) formula; at \(k=8\) for equals odd partner-\(5U+256\);
equals odd partner-\(5U+128\); equals odd partner-\(5U+64\);
equals odd partner-\(5U+32\); equals odd partner-\(5U+16\);
equals odd partner-\(5U+8\); equals odd partner-\(5U+4\); equals
\(J_k\); equals \(\mathrm{clip\_gp}\); equals even
partner-\(5U+256\); equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd
unpaired. Do **not** kill equals \(\mathrm{clip\_gp}\) or odd
partner-\(5U+256\) or odd partner-\(5U+64\) or odd partner-\(5U+4\)
at \(k=9\). Do **not** PREFIX a unified partner-offset formula in
\(m\).

## Lemma (first odd slice cell is \(n=5U/2+257\), \(j=2\) for \(k\ge 8\))

The \(j=2\) cell has partner \(5U+512\). At \(k=7\), \(n=577\ge 512\)
is not covering (though \(G(577,2)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=7\) for covering. Do **not** kill unpaired at \(j=2\) for
\(k\ge 8\).

## Verdict

`LEMMA` (odd partner-\(5U+512\) slice count \(J_k-85(-1)^k+86\) for
\(k\ge 10\); first odd cell is \(n=5U/2+257\), \(j=2\) for
\(k\ge 8\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd slice equals the \(k\ge 10\) formula at \(k=9\) and at
\(k=8\); equals odd partner-\(5U+256\) at \(k=8\) and at \(k=7\);
equals odd partner-\(5U+128\) at \(k=8\) and at \(k=9\); equals
odd partner-\(5U+64\); equals odd partner-\(5U+32\); equals odd
partner-\(5U+16\); equals odd partner-\(5U+8\); equals odd
partner-\(5U+4\) at \(k=8\); equals \(J_k\); equals
\(\mathrm{clip\_gp}\) at \(k=8\) and at \(k=7\); equals even
partner-\(5U+256\); equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd
unpaired; covering at \(n=5U/2+257\) at \(k=7\); pal-center tot
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

- `research/cycle_xo.md` (this note)
- `research/cycle_xo.py`
- `research/cycle_xo.json`
