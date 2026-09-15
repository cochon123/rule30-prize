# Cycle XA: even partner-\(5U+16\) unpaired extra equals the odd slice

Even-\(n\) unpaired extra at \(j=2n-5U-16\) with \(j\ge 2\) equals
Cycle WZ's odd slice \(J_k+2+3(-1)^k\) for \(k\ge 5\). Together
they are \(J_{k+1}+4+5(-1)^k\) for \(k\ge 5\). The first even cell
is \(n=5U/2+10\), \(j=4\) for \(k\ge 4\). Dies at \(k=3\) for even
equals odd (got \(0\), not \(2\)). Dies at \(k=8\) for tot equals
\(J_{k+1}\) (got \(180\), not \(171\)). Do **not** kill even
equals odd at \(k\ge 5\). Do **not** kill \(\mathrm{pal\_kind}\)
unpaired at \(n=5U/2+10\), \(j=4\) for \(k\ge 4\). Census \(k=8\):
even slice \(90\), tot \(180\), first \((650,4)\). Do **not**
PREFIX pal-center tot from small \(k\). Do **not** PREFIX leftover
spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not**
catalogue leftover \(d\). Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_xa.py --certify` (~0.14s).
Dump: `research/cycle_xa.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WR/WW/WX/WY/WZ
(even partner-\(5U+16\) slice equals odd; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+16\) unpaired extra equals the odd slice for \(k\ge 5\))

Same \(j\ge 2\) filter as Cycle WN/WR/WU/WV/WW/WX/WZ. Special-case
\(0\) at \(k\le 3\) and \(4\) at \(k=4\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for equals odd; at \(k=8\) for equals \(\mathrm{clip\_gp}\);
equals \(J_k\); equals odd partner-\(5U+8\); equals
\(n_{\mathrm{ug}}\); equals \(j=0\) odd unpaired. Do **not** kill
equals the odd slice at \(k=8\).

## Lemma (odd+even partner-\(5U+16\) tot is \(J_{k+1}+4+5(-1)^k\) for \(k\ge 5\))

Equals \(2(J_k+2+3(-1)^k)\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=8\) for tot
equals \(J_{k+1}\). Do **not** PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+10\), \(j=4\) for \(k\ge 4\))

The \(j=4\) cell has partner \(5U+16\). At \(k=3\), \(G(30,4)=0\)
so the slice is empty. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
\(G(n,4)=1\). Do **not** kill unpaired at \(j=4\) for \(k\ge 4\).

## Verdict

`LEMMA` (even partner-\(5U+16\) slice equals odd \(J_k+2+3(-1)^k\)
for \(k\ge 5\); tot \(J_{k+1}+4+5(-1)^k\); first even cell is
\(n=5U/2+10\), \(j=4\) for \(k\ge 4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even equals odd at \(k=3\); tot \(=J_{k+1}\) at \(k=8\);
even slice \(=\mathrm{clip\_gp}\); equals \(J_k\); equals odd
partner-\(5U+8\); equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd
unpaired; \(G(\mathrm{ph}+10,4)=1\) at \(k=3\); pal-center tot
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

- `research/cycle_xa.md` (this note)
- `research/cycle_xa.py`
- `research/cycle_xa.json`
