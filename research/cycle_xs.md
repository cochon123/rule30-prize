# Cycle XS: even partner-\(5U+1024\) unpaired extra has count \(J_k+171(-1)^k+170\)

Even-\(n\) unpaired extra at \(j=2n-5U-1024\) with \(j\ge 2\) has count
\(J_k+171(-1)^k+170\) for \(k\ge 11\), equal to the odd Cycle XR slice.
Together they are \(J_{k+1}+341(-1)^k+340\) for \(k\ge 11\). The first
even cell is \(n=5U/2+514\), \(j=4\) for \(k\ge 9\). Dies at \(k=10\)
for the \(k\ge 11\) formula (got \(340\), not \(682\)) and at \(k=9\)
(got \(84\), not \(170\)). Dies at \(k=9\) for even equals odd
(got \(84\), not \(86\)) and at \(k=10\) (got \(340\), not \(342\)).
Dies at \(k=10\) for tot equals \(J_{k+1}\) (got \(682\), not \(683\))
and at \(k=11\) (got \(1364\), not \(1365\)). Do **not** kill even
equals odd at \(k\le 8\) (both \(0\)) or \(k\ge 11\) (both \(682\) at
\(k=11\)). Do **not** kill equals even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\)
at \(k=10\) (all \(340\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or even partner-\(5U+256\) or even
partner-\(5U+64\) or odd at \(k=11\) (all \(682\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+514\), \(j=4\) for
\(k\ge 9\). Census \(k=8\): even slice \(0\), tot \(0\), first
`None` (not yet covering). Do **not** PREFIX pal-center tot from
small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_xs.py --certify` (~0.14s).
Dump: `research/cycle_xs.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR
(even partner-\(5U+1024\) slice \(J_k+171(-1)^k+170\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+1024\) unpaired extra has count \(J_k+171(-1)^k+170\) for \(k\ge 11\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR.
Special-case \(0\) at \(k\le 8\), \(84\) at \(k=9\), and \(340\) at
\(k=10\). Equals the odd slice for \(k\ge 11\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=10\) and \(k=9\) for the \(k\ge 11\) formula; at \(k=10\) and
\(k=9\) for equals odd; at \(k=8\) for equals \(J_k\); equals
\(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\); equals even
partner-\(5U+512\); equals odd partner-\(5U+256\); equals even
partner-\(5U+256\); equals even partner-\(5U+128\); equals odd
partner-\(5U+64\); equals even partner-\(5U+64\); equals odd
partner-\(5U+16\); equals even partner-\(5U+16\); equals odd
partner-\(5U+8\); equals even partner-\(5U+32\); equals even
partner-\(5U+8\); equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd
unpaired. Do **not** kill even equals odd at \(k\le 8\) or
\(k\ge 11\). Do **not** kill equals even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\)
at \(k=10\). Do **not** kill equals \(\mathrm{clip\_gp}\) or even
partner-\(5U+256\) or even partner-\(5U+64\) or odd at \(k=11\). Do
**not** PREFIX a unified partner-offset formula in \(m\).

## Lemma (odd+even partner-\(5U+1024\) tot is \(J_{k+1}+341(-1)^k+340\) for \(k\ge 11\))

Equals \(2(J_k+171(-1)^k+170)\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=9\), at
\(k=10\), and at \(k=11\) for tot equals \(J_{k+1}\). Do **not**
PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+514\), \(j=4\) for \(k\ge 9\))

The \(j=4\) cell has partner \(5U+1024\). At \(k=8\), \(n=1154\ge 1024\)
is not covering (though \(G(1154,4)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=8\) for covering. Do **not** kill unpaired at \(j=4\) for
\(k\ge 9\).

## Verdict

`LEMMA` (even partner-\(5U+1024\) slice count \(J_k+171(-1)^k+170\) for
\(k\ge 11\); tot \(J_{k+1}+341(-1)^k+340\); first even cell is
\(n=5U/2+514\), \(j=4\) for \(k\ge 9\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 11\) formula at \(k=10\) and at
\(k=9\); even equals odd at \(k=10\) and at \(k=9\); tot \(=J_{k+1}\)
at \(k=9\), at \(k=10\), and at \(k=11\); even slice
\(=\mathrm{clip\_gp}\); equals \(J_k\); equals odd partner-\(5U+512\);
equals even partner-\(5U+512\); equals odd partner-\(5U+256\);
equals even partner-\(5U+256\); equals even partner-\(5U+128\);
equals odd partner-\(5U+64\); equals even partner-\(5U+64\);
equals odd partner-\(5U+16\); equals even partner-\(5U+16\);
equals odd partner-\(5U+8\); equals even partner-\(5U+32\);
equals even partner-\(5U+8\); equals \(n_{\mathrm{ug}}\); equals
\(j=0\) odd unpaired; covering at \(n=5U/2+514\) at \(k=8\);
pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_xs.md` (this note)
- `research/cycle_xs.py`
- `research/cycle_xs.json`
