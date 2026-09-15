# Cycle WU: odd partner-\(5U+4\) unpaired extra has count \(J_k+(-1)^k\)

Odd-\(n\) unpaired extra at \(j=2n-5U-4\) has count
\(J_k+(-1)^k\) for \(k\ge 2\). The first cell is Cycle WP's
\(n=5U/2+5\), \(j=6\) for \(k\ge 4\). Dies at \(k=2\) for equals
\(J_{k+1}\) (got \(2\), not \(3\)). Dies at \(k=7\) for equals
\(J_k\) (got \(42\), not \(43\)). Dies at \(k=8\) for equals
\(\mathrm{clip\_gp}\) (got \(86\), not \(85\)). Do **not** kill
equals \(\mathrm{clip\_gp}\) at \(k=7\) (both \(42\)). Do **not**
kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+5\), \(j=6\) for
\(k\ge 4\). Census \(k=8\): odd slice \(86\), first \((645,6)\).
Do **not** PREFIX pal-center tot from small \(k\). Do **not**
PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat
tot. Do **not** catalogue leftover \(d\). Do **not** claim
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

Certify: `python3 research/cycle_wu.py --certify` (~0.14s).
Dump: `research/cycle_wu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WP/WR/WS
(odd partner-\(5U+4\) slice \(J_k+(-1)^k\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd partner-\(5U+4\) unpaired extra has count \(J_k+(-1)^k\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=2\) for equals \(J_{k+1}\); at \(k=7\) for equals \(J_k\); at
\(k=8\) for equals \(\mathrm{clip\_gp}\); equals the even
partner-\(5U+2\) slice; equals \(n_{\mathrm{ug}}\); equals \(j=0\)
odd unpaired. Do **not** kill equals \(\mathrm{clip\_gp}\) at
\(k=7\).

## Lemma (first odd slice cell is \(n=5U/2+5\), \(j=6\) for \(k\ge 4\))

Cycle WP. The \(j=6\) cell has partner \(5U+4\). At \(k=3\),
\(G(25,6)=0\) so the first cell is \(n=29\), \(j=14\). At \(k=2\)
the first cell is \(n=13\), \(j=2\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for \(G(n,6)=1\). Do **not** kill unpaired at \(j=6\) for
\(k\ge 4\).

## Verdict

`LEMMA` (odd partner-\(5U+4\) slice count \(J_k+(-1)^k\) for
\(k\ge 2\); first odd cell is Cycle WP for \(k\ge 4\); \(j=6\) has
partner \(5U+4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd slice \(=J_{k+1}\) at \(k=2\); odd slice \(=J_k\) at
\(k=7\); odd slice \(=\mathrm{clip\_gp}\) at \(k=8\); equals even
partner-\(5U+2\) slice; equals \(n_{\mathrm{ug}}\); equals \(j=0\)
odd unpaired; \(G(\mathrm{ph}+5,6)=1\) at \(k=3\); pal-center tot
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

- `research/cycle_wu.md` (this note)
- `research/cycle_wu.py`
- `research/cycle_wu.json`
