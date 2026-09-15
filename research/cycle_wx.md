# Cycle WX: even partner-\(5U+8\) unpaired extra has count \(J_k-(-1)^k\)

Even-\(n\) unpaired extra at \(j=2n-5U-8\) with \(j\ge 2\) has count
\(J_k-(-1)^k\) for \(k\ge 4\). Together with Cycle WW they are
\(J_{k+1}+2-3(-1)^k\) for \(k\ge 4\). The first even cell is
Cycle WT's \(n=5U/2+8\), \(j=8\) for \(k\ge 5\). Dies at \(k=3\)
for the \(k\ge 4\) formula (got \(2\), not \(4\)). Dies at \(k=8\)
for even equals odd (got \(84\), not \(86\)) and for tot equals
\(J_{k+1}\) (got \(170\), not \(171\)). Do **not** kill even
equals odd at \(k=3\) (both \(2\)). Do **not** kill
\(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+8\), \(j=8\) for
\(k\ge 5\). Census \(k=8\): even slice \(84\), tot \(170\), first
\((648,8)\). Do **not** PREFIX pal-center tot from small \(k\). Do
**not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_wx.py --certify` (~0.14s).
Dump: `research/cycle_wx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WT/WV/WW
(even partner-\(5U+8\) slice \(J_k-(-1)^k\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+8\) unpaired extra has count \(J_k-(-1)^k\) for \(k\ge 4\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW. Special-case \(0\)
at \(k\le 2\) and \(2\) at \(k=3\). Equals the odd slice minus \(2\)
for \(k\ge 4\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** at \(k=3\) for the \(k\ge 4\)
formula; at \(k=8\) for equals odd; equals \(J_k\); equals
\(\mathrm{clip\_gp}\); equals \(n_{\mathrm{ug}}\); equals \(j=0\)
odd unpaired. Do **not** kill equals odd at \(k=3\).

## Lemma (odd+even partner-\(5U+8\) tot is \(J_{k+1}+2-3(-1)^k\) for \(k\ge 4\))

Equals \(2(J_k-(-1)^k)+2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=8\) for tot
equals \(J_{k+1}\). Do **not** PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+8\), \(j=8\) for \(k\ge 5\))

Cycle WT. The \(j=8\) cell has partner \(5U+8\). At \(k=4\),
\(G(48,8)=0\) so the first cell is \(n=52\), \(j=16\). At \(k=3\)
the first cell is \(n=26\), \(j=4\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=4\) for \(G(n,8)=1\). Do **not** kill unpaired at \(j=8\) for
\(k\ge 5\).

## Verdict

`LEMMA` (even partner-\(5U+8\) slice count \(J_k-(-1)^k\) for
\(k\ge 4\); tot \(J_{k+1}+2-3(-1)^k\); first even cell is Cycle WT
for \(k\ge 5\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice equals the \(k\ge 4\) formula at \(k=3\); even
equals odd at \(k=8\); tot \(=J_{k+1}\) at \(k=8\); even slice
\(=\mathrm{clip\_gp}\); equals \(J_k\); equals \(n_{\mathrm{ug}}\);
equals \(j=0\) odd unpaired; \(G(\mathrm{ph}+8,8)=1\) at \(k=4\);
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

- `research/cycle_wx.md` (this note)
- `research/cycle_wx.py`
- `research/cycle_wx.json`
