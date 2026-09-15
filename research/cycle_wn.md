# Cycle WN: \(\mathrm{clip\_gp}\) is \(J_k-(k\bmod 2)\); partner-\(5U+2\) slice is \(J_k\)

Unpaired extra with child partner \(5U+2\) has \(j=2n-5U-2\). That
Green slice has count \(J_k\) for \(k\ge 2\). It is \(\mathrm{clip\_gp}\)
except one \(n_{\mathrm{ug}}\) when \(k\) is odd, so
\(\mathrm{clip\_gp}=J_k-(k\bmod 2)\) for \(k\ge 2\), equal to Cycle UB
\((J_{k+1}-1)/2\). Special-case \(0\) at \(k\le 1\). Dies at \(k=2\)
for \(\mathrm{clip\_gp}\) equals \(J_{k+1}\) (got \(1\), not \(3\)).
Dies at \(k=7\) for \(\mathrm{clip\_gp}\) equals \(J_k\) (got \(42\),
not \(43\)) and for the slice equals \(\mathrm{clip\_gp}\) (got \(43\),
not \(42\)). Dies at \(k=8\) for the slice equals \(n_{\mathrm{ug}}\)
(got \(85\), not \(4924\)), equals \(j=0\) odd unpaired (got \(85\),
not \(192\)), and equals \(J_{k+1}\) (got \(85\), not \(171\)). Do
**not** kill \(\mathrm{clip\_gp}\) equals \(J_k\) at \(k=8\): they
match. Census \(k=8\): slice \(85\), \(\mathrm{clip\_gp}\) \(85\),
slice \(n_{\mathrm{ug}}\) \(0\). Do **not** PREFIX pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\).
Do **not** claim pal-center tot equals \(S\oplus T\). This is **not**
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

Certify: `python3 research/cycle_wn.py --certify`.
Dump: `research/cycle_wn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UA/UB/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WH/WK/WL/WM
(\(\mathrm{clip\_gp}\) \(J_k\) form; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (partner-\(5U+2\) unpaired extra has count \(J_k\) for \(k\ge 2\))

Those cells have \(j=2n-5U-2\). Special-case \(0\) at \(k\le 1\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=7\) for equals \(\mathrm{clip\_gp}\);
at \(k=8\) for equals \(n_{\mathrm{ug}}\); equals \(j=0\) odd
unpaired; equals \(J_{k+1}\).

## Lemma (\(\mathrm{clip\_gp}\) is \(J_k-(k\bmod 2)\) for \(k\ge 2\))

Equals Cycle UB \((J_{k+1}-1)/2\). The partner-\(5U+2\) slice is
\(\mathrm{clip\_gp}\) except one \(n_{\mathrm{ug}}\) when \(k\) is
odd. Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=2\) for equals \(J_{k+1}\); at \(k=7\)
for equals \(J_k\). Do **not** kill equals \(J_k\) at \(k=8\). Do
**not** PREFIX pal-center tot.

## Verdict

`LEMMA` (partner-\(5U+2\) slice count \(J_k\) for \(k\ge 2\);
\(\mathrm{clip\_gp}=J_k-(k\bmod 2)\); slice \(n_{\mathrm{ug}}\) is
\(1\) iff \(k\) odd).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(\mathrm{clip\_gp}=J_{k+1}\) at \(k=2\);
\(\mathrm{clip\_gp}=J_k\) at \(k=7\); slice equals
\(\mathrm{clip\_gp}\) at \(k=7\); slice equals \(n_{\mathrm{ug}}\);
slice equals \(j=0\) odd unpaired; slice equals \(J_{k+1}\);
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

- `research/cycle_wn.md` (this note)
- `research/cycle_wn.py`
- `research/cycle_wn.json`
