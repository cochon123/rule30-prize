# Cycle XV: even partner-\(5U+2048\) unpaired extra has count \(J_k-341(-1)^k+340\)

Even-\(n\) unpaired extra at \(j=2n-5U-2048\) with \(j\ge 2\) has count
\(J_k-341(-1)^k+340\) for \(k\ge 12\). Together with Cycle XU they are
\(J_{k+1}-683(-1)^k+682\) for \(k\ge 12\). The first even cell is
\(n=5U/2+1026\), \(j=4\) for \(k\ge 10\). Dies at \(k=11\) for the
\(k\ge 12\) formula (got \(682\), not \(1364\)) and at \(k=10\)
(got \(170\), not \(340\)). Dies at \(k=12\) for even equals odd
(got \(1364\), not \(1366\)) and for tot equals \(J_{k+1}\) (got
\(2730\), not \(2731\)). Do **not** kill even equals odd at \(k=10\)
or \(k=11\) (both \(170\) and \(682\)). Do **not** kill equals
\(\mathrm{clip\_gp}\) or even partner-\(5U+1024\) or even
partner-\(5U+256\) or even partner-\(5U+64\) at \(k=11\) (all
\(682\)). Do **not** kill equals even partner-\(5U+512\) or even
partner-\(5U+128\) or even partner-\(5U+32\) or even partner-\(5U+8\)
at \(k=12\) (all \(1364\)). Do **not** kill \(\mathrm{pal\_kind}\)
unpaired at \(n=5U/2+1026\), \(j=4\) for \(k\ge 10\). Census \(k=8\):
even slice \(0\), tot \(0\), first `None` (not yet covering). Do
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

Certify: `python3 research/cycle_xv.py --certify` (~0.14s).
Dump: `research/cycle_xv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WZ/XA/XC/XD/XF/XG/XH/XI/XJ/XK/XL/XM/XN/XO/XP/XQ/XR/XS/XT/XU
(even partner-\(5U+2048\) slice \(J_k-341(-1)^k+340\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+2048\) unpaired extra has count \(J_k-341(-1)^k+340\) for \(k\ge 12\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ/XA/XC/XD/XF/XG/XI/XJ/XL/XM/XO/XP/XR/XS/XU.
Special-case \(0\) at \(k\le 9\), \(170\) at \(k=10\), and \(682\) at
\(k=11\). Equals the odd slice minus \(2\) for \(k\ge 12\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=11\) and \(k=10\) for the \(k\ge 12\) formula; at
\(k=12\) for equals odd; at \(k=8\) for equals \(J_k\); equals
\(\mathrm{clip\_gp}\); equals odd partner-\(5U+512\); equals even
partner-\(5U+512\); equals even partner-\(5U+256\); equals odd
partner-\(5U+64\); equals even partner-\(5U+64\); equals odd
partner-\(5U+16\); equals even partner-\(5U+16\); equals odd
partner-\(5U+8\); equals even partner-\(5U+32\); equals even
partner-\(5U+8\); equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd
unpaired. Do **not** kill equals odd at \(k=10\) or \(k=11\). Do
**not** kill equals \(\mathrm{clip\_gp}\) or even partner-\(5U+1024\)
or even partner-\(5U+256\) or even partner-\(5U+64\) at \(k=11\). Do
**not** kill equals even partner-\(5U+512\) or even partner-\(5U+128\)
or even partner-\(5U+32\) or even partner-\(5U+8\) at \(k=12\). Do
**not** PREFIX a unified partner-offset formula in \(m\).

## Lemma (odd+even partner-\(5U+2048\) tot is \(J_{k+1}-683(-1)^k+682\) for \(k\ge 12\))

Equals \(2(J_k-341(-1)^k+340)+2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=10\), at
\(k=11\), and at \(k=12\) for tot equals \(J_{k+1}\). Do **not**
PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+1026\), \(j=4\) for \(k\ge 10\))

The \(j=4\) cell has partner \(5U+2048\). At \(k=9\), \(n=2306\ge 2048\)
is not covering (though \(G(2306,4)=1\)). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=9\) for covering. Do **not** kill unpaired at \(j=4\) for
\(k\ge 10\).

## Verdict

`LEMMA` (even partner-\(5U+2048\) slice count \(J_k-341(-1)^k+340\) for
\(k\ge 12\); tot \(J_{k+1}-683(-1)^k+682\); first even cell is
\(n=5U/2+1026\), \(j=4\) for \(k\ge 10\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 12\) formula at \(k=11\) and at
\(k=10\); even equals odd at \(k=12\); tot \(=J_{k+1}\) at \(k=10\),
at \(k=11\), and at \(k=12\); even slice \(=\mathrm{clip\_gp}\);
equals \(J_k\); equals odd partner-\(5U+512\); equals even
partner-\(5U+512\); equals even partner-\(5U+256\); equals odd
partner-\(5U+64\); equals even partner-\(5U+64\); equals odd
partner-\(5U+16\); equals even partner-\(5U+16\); equals odd
partner-\(5U+8\); equals even partner-\(5U+32\); equals even
partner-\(5U+8\); equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd
unpaired; covering at \(n=5U/2+1026\) at \(k=9\); pal-center tot
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

- `research/cycle_xv.md` (this note)
- `research/cycle_xv.py`
- `research/cycle_xv.json`
