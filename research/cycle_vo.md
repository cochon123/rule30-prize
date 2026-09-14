# Cycle VO: leftover extra xor COUNT gap pg/gp half F/L forms

Cycle VN tot halves split by leftover extra xor COUNT pg/gp.
For \(k\ge 3\) the small \(n_{\mathrm{pg}}\) is
\[
\frac{2^{k-3}(27 L_{k-2}+30 F_{k-2}-35)-8(-1)^k}{6},
\]
the small \(n_{\mathrm{gp}}\) is
\[
\frac{2^{k-3}(27 L_{k-2}+30 F_{k-2}-65)-8(-1)^k+12}{6},
\]
and the large \(n_{\mathrm{pg}}=n_{\mathrm{gp}}\) is
\[
\frac{2^{k-3}(L_{k-2}+16 F_{k-2}-7)+4(-1)^k}{2}.
\]
They sum to Cycle VM tot \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\).
Special-case small \(n_{\mathrm{pg}}\) \(1\) at \(k=2\); the rest
\(0\) at \(k\le 2\). Dies at \(k=2\) for the large F/L half with
shift \(0\) (got \(2\), not \(0\)) and the small \(n_{\mathrm{pg}}\)
F/L form with shift \(0\) (got \(-2\), not \(1\)). Census \(k=8\):
small \(3684/3526\), large \(2226/2226\). Do **not** PREFIX
pal-center tot from small \(k\). Do **not** PREFIX leftover spat tot.
Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue
leftover \(d\). Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_vo.py --certify`.
Dump: `research/cycle_vo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UO/UP/UR/UU/UV/UW/UZ/VA/VK/VM/VN
(xor count gap pg/gp half F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (COUNT gap small \(n_{\mathrm{pg}}\) is \((2^{k-3}(27 L_{k-2}+30 F_{k-2}-35)-8(-1)^k)/6\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=2\) for the F/L form with shift \(0\).

## Lemma (COUNT gap small \(n_{\mathrm{gp}}\) is \((2^{k-3}(27 L_{k-2}+30 F_{k-2}-65)-8(-1)^k+12)/6\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\).

## Lemma (COUNT gap large \(n_{\mathrm{pg}}=n_{\mathrm{gp}}\) is \((2^{k-3}(L_{k-2}+16 F_{k-2}-7)+4(-1)^k)/2\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). The halves sum to Cycle VM tot
\(n_{\mathrm{pg}}/n_{\mathrm{gp}}\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=2\) for the F/L form with shift \(0\); small \(n_{\mathrm{pg}}\)
equals tot \(n_{\mathrm{pg}}\) at \(k=8\). Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (COUNT gap small/large \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\)
F/L closed forms for \(k\ge 3\); halves sum to tot).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (large F/L half at \(k=2\); small \(n_{\mathrm{pg}}\) F/L
at \(k=2\); small \(n_{\mathrm{pg}}\) equals tot \(n_{\mathrm{pg}}\);
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

- `research/cycle_vo.md` (this note)
- `research/cycle_vo.py`
- `research/cycle_vo.json`
