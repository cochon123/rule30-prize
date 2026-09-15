# Cycle WR: even partner-\(5U+2\) unpaired extra has count \(J_k\)

Odd-\(n\) unpaired extra at \(j=2n-5U-2\) is Cycle WN's slice of
count \(J_k\) for \(k\ge 2\). The even-\(n\) cells at the same \(j\)
have the same count \(J_k\). Together they are \(2J_k=J_{k+1}-(-1)^k\)
for \(k\ge 2\). The first even cell is Cycle WQ's \(n=5U/2+2\),
\(j=2\) for \(k\ge 3\). Dies at \(k=2\) for even slice equals
\(J_{k+1}\) (got \(1\), not \(3\)). Dies at \(k=7\) for even slice
equals \(\mathrm{clip\_gp}\) (got \(43\), not \(42\)). Dies at
\(k=8\) for tot equals \(J_{k+1}\) (got \(170\), not \(171\)). Do
**not** kill even slice equals \(J_k\) at \(k=8\), or even equals
odd slice. Census \(k=8\): even slice \(85\), tot \(170\), first
\((642,2)\). Do **not** PREFIX pal-center tot from small \(k\). Do
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

Certify: `python3 research/cycle_wr.py --certify`.
Dump: `research/cycle_wr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WM/WN/WO/WQ
(even partner-\(5U+2\) slice \(J_k\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even partner-\(5U+2\) unpaired extra has count \(J_k\) for \(k\ge 2\))

Equals Cycle WN's odd slice. Special-case \(0\) at \(k\le 1\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=2\) for equals \(J_{k+1}\); at \(k=7\)
for equals \(\mathrm{clip\_gp}\); at \(k=8\) for equals
\(n_{\mathrm{ug}}\); equals \(j=0\) odd unpaired. Do **not** kill
equals \(J_k\) at \(k=8\). Do **not** kill equals the odd slice.

## Lemma (odd+even partner-\(5U+2\) tot is \(2J_k=J_{k+1}-(-1)^k\) for \(k\ge 2\))

Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=8\) for tot equals \(J_{k+1}\). Do
**not** PREFIX pal-center tot.

## Lemma (first even slice cell is \(n=5U/2+2\), \(j=2\) for \(k\ge 3\))

Cycle WQ. At \(k=2\) the first cell is \(n=14\), \(j=6\) because
\(G(12,2)=0\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\).

## Verdict

`LEMMA` (even partner-\(5U+2\) slice count \(J_k\) for \(k\ge 2\);
odd+even tot \(2J_k=J_{k+1}-(-1)^k\); first even cell is Cycle WQ
for \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even slice \(=J_{k+1}\) at \(k=2\); even slice
\(=\mathrm{clip\_gp}\) at \(k=7\); tot \(=J_{k+1}\) at \(k=8\);
even slice equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd unpaired;
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

- `research/cycle_wr.md` (this note)
- `research/cycle_wr.py`
- `research/cycle_wr.json`
