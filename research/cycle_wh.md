# Cycle WH: even leftover small \(\mathrm{sm}\) F/L closed form

Even leftover pal-pairs on \(n<5U/2\) count \(\mathrm{sm}\). For
\(k\ge 2\)
\[
\mathrm{sm}=\frac{2^{k-2}(33 F_{k+1}-21 F_{k-1}-25)+4(-1)^k}{6}.
\]
Special-case \(1\) at \(k=1\); \(0\) at \(k\le 0\). Equals
\(\mathrm{lo}_e-e_{\ge}\) for every \(k\). \(2\,\mathrm{sm}(k)\) is
leftover-parent xor \(\mathrm{plo}_s(k+1)\) for \(k\ge 2\). Dies at
\(k=2\) for the F/L form with shift \(0\) (got \(0\), not \(4\)).
Dies at \(k=8\) without the \(2^{k-2}\) (got \(138\), not \(8790\))
and without the \(4(-1)^k\) (got \(8789\), not \(8790\)). Dies at
\(k=8\) for \(\mathrm{sm}\) equals tot \(\mathrm{lo}_e\) (got
\(8790\), not \(14114\)) and \(\mathrm{sm}\) equals \(e_{\ge}\)
(got \(8790\), not \(5324\)). Census \(k=8\): \(\mathrm{sm}\)
\(8790\), \(e_{\ge}\) \(5324\). Do **not** PREFIX pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover
\(d\). Do **not** claim pal-center tot equals \(S\oplus T\). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
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

Certify: `python3 research/cycle_wh.py --certify` (~0.38s).
Dump: `research/cycle_wh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/WE/WF/WG
(\(\mathrm{sm}\) F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(\mathrm{sm}\) is \((2^{k-2}(33 F_{k+1}-21 F_{k-1}-25)+4(-1)^k)/6\) for \(k\ge 2\))

Special-case \(1\) at \(k=1\); \(0\) at \(k\le 0\). Equals
\(\mathrm{lo}_e-e_{\ge}\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=2\) for
the F/L form with shift \(0\); without \(2^{k-2}\) at \(k=8\);
without \(4(-1)^k\) at \(k=8\); \(\mathrm{sm}\) equals tot
\(\mathrm{lo}_e\) at \(k=8\); \(\mathrm{sm}\) equals \(e_{\ge}\) at
\(k=8\).

## Lemma (\(2\,\mathrm{sm}(k)\) is leftover-parent xor \(\mathrm{plo}_s(k+1)\) for \(k\ge 2\))

Status: **lemma**. Algebra through \(k\le 64\). Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (\(\mathrm{sm}\) F/L closed form for \(k\ge 2\); equals
\(\mathrm{lo}_e-e_{\ge}\); \(2\,\mathrm{sm}(k)=\mathrm{plo}_s(k+1)\)
for \(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (F/L form at \(k=2\) with shift \(0\); without \(2^{k-2}\)
at \(k=8\); without \(4(-1)^k\) at \(k=8\); \(\mathrm{sm}\) equals
tot \(\mathrm{lo}_e\); \(\mathrm{sm}\) equals \(e_{\ge}\);
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

- `research/cycle_wh.md` (this note)
- `research/cycle_wh.py`
- `research/cycle_wh.json`
