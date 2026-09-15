# Cycle XM: even partner-\(5U+256\) unpaired extra has count \(J_k+43(-1)^k+42\)

Even-\(n\) unpaired extra at \(j=2n-5U-256\) with \(j\ge 2\) has count
\(J_k+43(-1)^k+42\) for \(k\ge 9\), equal to the odd Cycle XL slice.
Together they are \(J_{k+1}+85(-1)^k+84\) for \(k\ge 9\). The first
even cell is \(n=5U/2+130\), \(j=4\) for \(k\ge 7\). Dies at \(k=8\)
for the \(k\ge 9\) formula (got \(84\), not \(170\)) and at \(k=7\)
(got \(20\), not \(42\)). Dies at \(k=8\) for even equals odd
(got \(84\), not \(86\)) and for tot equals \(J_{k+1}\) (got
\(170\), not \(171\)). Do **not** kill even equals odd at \(k=9\)
(both \(170\)). Do **not** kill equals even partner-\(5U+128\) or
even partner-\(5U+32\) or even partner-\(5U+8\) at \(k=8\) (all
\(84\)). Do **not** kill \(\mathrm{pal\_kind}\) unpaired at
\(n=5U/2+130\), \(j=4\) for \(k\ge 7\). Census \(k=8\): even slice
\(84\), tot \(170\), first \((770,4)\). Do **not** PREFIX pal-center
tot from small \(k\). Do **not** PREFIX leftover spat tot. Do
**not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue
leftover \(d\). Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
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

Certify: `python3 research/cycle_xm.py --certify` (~0.14s).
Dump: `research/cycle_xm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL
(even partner-\(5U+256\) slice \(J_k+43(-1)^k+42\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+256\) unpaired extra has count \(J_k+43(-1)^k+42\) for \(k\ge 9\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL.
Special-case \(0\) at \(k\le 6\), \(20\) at \(k=7\), and \(84\) at
\(k=8\). Equals the odd slice for \(k\ge 9\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=8\) and \(k=7\) for the \(k\ge 9\) formula; at \(k=8\) and
\(k=7\) for equals odd; at \(k=8\) for equals \(J_k\); equals
\(\mathrm{clip\_gp}\); equals odd partner-\(5U+64\); equals even
partner-\(5U+64\); equals odd partner-\(5U+16\); equals even
partner-\(5U+16\); equals odd partner-\(5U+8\); equals
\(n_{\mathrm{ug}}\); equals \(j=0\) odd unpaired. Do **not** kill
even equals odd at \(k=9\). Do **not** kill equals even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\)
at \(k=8\). Do **not** PREFIX a unified partner-offset formula in
\(m\).

## Lemma (odd+even partner-\(5U+256\) tot is \(J_{k+1}+85(-1)^k+84\) for \(k\ge 9\))

Equals \(2(J_k+43(-1)^k+42)\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=8\) for tot
equals \(J_{k+1}\). Do **not** PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+130\), \(j=4\) for \(k\ge 7\))

The \(j=4\) cell has partner \(5U+256\). At \(k=6\), \(n=290\ge 256\)
is not covering (though \(G(290,4)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=6\) for covering. Do **not** kill unpaired at \(j=4\) for
\(k\ge 7\).

## Verdict

`LEMMA` (even partner-\(5U+256\) slice count \(J_k+43(-1)^k+42\) for
\(k\ge 9\); tot \(J_{k+1}+85(-1)^k+84\); first even cell is
\(n=5U/2+130\), \(j=4\) for \(k\ge 7\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 9\) formula at \(k=8\) and at
\(k=7\); even equals odd at \(k=8\) and at \(k=7\); tot \(=J_{k+1}\)
at \(k=8\); even slice \(=\mathrm{clip\_gp}\); equals \(J_k\);
equals odd partner-\(5U+64\); equals even partner-\(5U+64\);
equals odd partner-\(5U+16\); equals even partner-\(5U+16\);
equals odd partner-\(5U+8\); equals \(n_{\mathrm{ug}}\); equals
\(j=0\) odd unpaired; covering at \(n=5U/2+130\) at \(k=6\);
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

- `research/cycle_xm.md` (this note)
- `research/cycle_xm.py`
- `research/cycle_xm.json`
