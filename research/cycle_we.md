# Cycle WE: even leftover large \(e_{\ge}\) F/L closed form

Even leftover pal-pairs on \(n\ge 5U/2\) count \(e_{\ge}\). For
\(k\ge 3\)
\[
e_{\ge}=\frac{2^{k-3}(21 F_{k+1}+11 F_{k-1}-25)-5(-1)^k+1}{5}.
\]
Special-case \(2\) at \(k=2\); \(0\) at \(k\le 1\). Even leftover
small is \(\mathrm{lo}_e-e_{\ge}\) for every \(k\). Dies at \(k=3\)
for the F/L form with shift \(0\) (got \(1\), not \(11\)). Dies at
\(k=8\) without the \(+1\) (got \(5323\), not \(5324\)) and without
the \(-5(-1)^k\) (got \(5325\), not \(5324\)). Do **not** kill
without both the \(+1\) and the sign at \(k=8\): floor-div masks
it. Dies at \(k=8\) for \(e_{\ge}\) equals tot \(\mathrm{lo}_e\)
(got \(5324\), not \(14114\)) and \(e_{\ge}\) equals leftover extra
large (got \(5324\), not \(6644\)). Census \(k=8\): \(e_{\ge}\)
\(5324\), small \(8790\). Do **not** PREFIX pal-center tot from
small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why
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

Certify: `python3 research/cycle_we.py --certify` (~0.38s).
Dump: `research/cycle_we.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UP/UQ/UR/UU/UV/UW/UZ/VA/WD
(\(e_{\ge}\) F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(e_{\ge}\) is \((2^{k-3}(21 F_{k+1}+11 F_{k-1}-25)-5(-1)^k+1)/5\) for \(k\ge 3\))

Special-case \(2\) at \(k=2\); \(0\) at \(k\le 1\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=3\) for the F/L form with shift \(0\); without
\(+1\) at \(k=8\); without \(-5(-1)^k\) at \(k=8\); \(e_{\ge}\)
equals tot \(\mathrm{lo}_e\) at \(k=8\); \(e_{\ge}\) equals leftover
extra large at \(k=8\).

## Lemma (even leftover small is \(\mathrm{lo}_e-e_{\ge}\) for every \(k\))

Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (\(e_{\ge}\) F/L closed form for \(k\ge 3\); even leftover
small is \(\mathrm{lo}_e-e_{\ge}\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (F/L form at \(k=3\) with shift \(0\); without \(+1\) at
\(k=8\); without sign at \(k=8\); \(e_{\ge}\) equals tot
\(\mathrm{lo}_e\); \(e_{\ge}\) equals leftover extra large;
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

- `research/cycle_we.md` (this note)
- `research/cycle_we.py`
- `research/cycle_we.json`
