# Cycle WP: first \(n_{\mathrm{ug}}/n_{\mathrm{gu}}/n_{\mathrm{gp}}\) is \(n=5U/2+5\) for \(k\ge 5\)

The first three odd covering \(n>5U/2\) are \(5U/2+1\), \(+3\),
\(+5\). Cycle WO has only \(j=0\) even-\(j\) unpaired extra at
\(+1\). At \(+3\), \(G(n,2)=0\) because both parent bits at the WO
parent fire, so even-\(j\) unpaired extra is again only \(j=0\) for
\(k\ge 4\). At \(+5\), the parent is even \(n=5U_p/2+2\) with
unpaired \(j=0\) and \(j=2\), and even-\(j\) unpaired extra is
\(\{0,2,4,6,8\}=(\mathrm{neg},\mathrm{ug},\mathrm{gu},\mathrm{ug},\mathrm{gp})\)
for \(k\ge 5\). Dies at \(k=4\) for the five-cell (got \(4\), no
\(\mathrm{gp}\)) and for first \(\mathrm{gp}\) at \(+5\) (got \(+7\)).
Dies at \(k=3\) for first \(n_{\mathrm{ug}}\) at \(+5\) (got \(+3\)).
Do **not** kill \(\mathrm{pal\_kind}\) unpaired at \(n=5U/2+5\),
\(j=0,2,4,6,8\). Census \(k=8\): \(+3\) extra \(1\), \(+5\) extra
\(5\) with \(n_{\mathrm{ug}}=2\), \(n_{\mathrm{gu}}=1\),
\(n_{\mathrm{gp}}=1\). Do **not** PREFIX pal-center tot from small
\(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
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

Certify: `python3 research/cycle_wp.py --certify` (~0.14s).
Dump: `research/cycle_wp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WO
(\(n=5U/2+5\) five-cell; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(n=5U/2+3\) has only \(j=0\) even-\(j\) unpaired extra for \(k\ge 4\))

\(G(n,2)=0\) because both parent bits at Cycle WO's \(n=5U_p/2+1\)
fire. Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=3\) for \(n_{\mathrm{ug}}=0\).

## Lemma (even-\(j\) unpaired extra at \(n=5U/2+5\) is \(\{0,2,4,6,8\}\) for \(k\ge 5\))

Kinds \((\mathrm{neg},\mathrm{ug},\mathrm{gu},\mathrm{ug},\mathrm{gp})\).
The \(j=8\) cell is the partner-\(5U+2\) slice. Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=4\) for the five-cell (got \(4\)); at \(k=4\) for \(G(n,8)=1\);
at \(k=8\) for equals \(\mathrm{clip\_gp}\); equals \(j=0\) odd
unpaired; equals the partner-\(5U+2\) slice tot. Do **not** kill
unpaired at \(j=0,2,4,6,8\).

## Lemma (first \(n_{\mathrm{ug}}\) is \(n=5U/2+5\) for \(k\ge 4\); first \(n_{\mathrm{gp}}\) for \(k\ge 5\))

The first three odd \(n>5U/2\) are \(+1,+3,+5\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for first \(n_{\mathrm{ug}}\) at \(+5\); at \(k=4\) for first
\(n_{\mathrm{gp}}\) at \(+5\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (\(n=5U/2+3\) only \(j=0\) for \(k\ge 4\); five-cell at
\(n=5U/2+5\) for \(k\ge 5\); first \(n_{\mathrm{ug}}\) at \(+5\) for
\(k\ge 4\); first \(n_{\mathrm{gp}}\) at \(+5\) for \(k\ge 5\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (five-cell at \(k=4\); first \(n_{\mathrm{ug}}\) at \(+5\)
at \(k=3\); first \(n_{\mathrm{gp}}\) at \(+5\) at \(k=4\);
\(n_{\mathrm{ug}}=0\) at \(+3\) at \(k=3\); five-cell equals
\(\mathrm{clip\_gp}\); equals \(j=0\) odd unpaired; equals slice tot;
\(G(n,8)=1\) at \(k=4\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_wp.md` (this note)
- `research/cycle_wp.py`
- `research/cycle_wp.json`
