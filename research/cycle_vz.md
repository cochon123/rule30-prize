# Cycle VZ: leftover extra xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) F/L closed forms

Leftover extra xor (odd leftover even-\(j\) except \(j=0\)) splits as
pair-then-\(g_0\) versus \(g_0\)-then-pair. For \(k\ge 3\)
\[
n_{\mathrm{pg}}=\frac{2^{k-3}(75 F_{k-2}+39 L_{k-2}-60)+6}{15}
\]
and
\[
n_{\mathrm{gp}}=\frac{2^{k-3}(75 F_{k-2}+39 L_{k-2}-95)+5(-1)^{k-1}+6}{15}.
\]
They sum to leftover extra xor tot. Equal leftover xor
\(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) at \(k-1\), not leftover-parent
xor at \(k-1\). Special-case \(n_{\mathrm{pg}}\) \(1\) at \(k=2\);
both \(0\) at \(k\le 1\); \(n_{\mathrm{gp}}\) \(0\) at \(k\le 2\).
Dies at \(k=3\) for both F/L forms with shift \(0\)
(\(n_{\mathrm{pg}}\) got \(0\), not \(4\); \(n_{\mathrm{gp}}\) got
\(0\), not \(2\)). Dies at \(k=8\) without the \(+6\)
(\(n_{\mathrm{pg}}\) got \(2649\), not \(2650\);
\(n_{\mathrm{gp}}\) got \(2574\), not \(2575\)). Dies at \(k=7\)
without the \(n_{\mathrm{gp}}\) \(5(-1)^{k-1}\) (got \(756\), not
\(757\)). Do **not** kill without that sign at \(k=8\): floor-div
masks it. Dies at \(k=8\) for \(n_{\mathrm{pg}}\) equals tot (got
\(2650\), not \(5225\)) and for \(n_{\mathrm{pg}}\) equals
leftover-parent xor at \(k-1\) (got \(2650\), not \(2564\)).
Census \(k=8\): \(n_{\mathrm{pg}}\) \(2650\), \(n_{\mathrm{gp}}\)
\(2575\). Do **not** PREFIX pal-center tot from small \(k\). Do
**not** PREFIX leftover spat tot. Do **not** PREFIX
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

Certify: `python3 research/cycle_vz.py --certify` (~0.24s).
Dump: `research/cycle_vz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UP/UR/UU/UV/UW/UZ/VA/VF/VG/VX
(leftover extra xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) F/L; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (leftover extra xor \(n_{\mathrm{pg}}\) is \((2^{k-3}(75 F_{k-2}+39 L_{k-2}-60)+6)/15\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Equals leftover
xor \(n_{\mathrm{pg}}\) at \(k-1\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for the F/L form with shift \(0\); without \(+6\) at
\(k=8\); equals leftover-parent xor \(n_{\mathrm{pg}}\) at \(k-1\).

## Lemma (leftover extra xor \(n_{\mathrm{gp}}\) is \((2^{k-3}(75 F_{k-2}+39 L_{k-2}-95)+5(-1)^{k-1}+6)/15\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). The two halves sum to leftover
extra xor tot. Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** at \(k=3\) for the F/L form
with shift \(0\); without \(+6\) at \(k=8\); without
\(5(-1)^{k-1}\) at \(k=7\); \(n_{\mathrm{pg}}\) equals tot at
\(k=8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\)
F/L closed forms for \(k\ge 3\); halves sum to leftover extra xor
tot).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(n_{\mathrm{pg}}\) F/L form at \(k=3\);
\(n_{\mathrm{gp}}\) F/L form at \(k=3\); without \(+6\); without
\(n_{\mathrm{gp}}\) sign at \(k=7\); \(n_{\mathrm{pg}}\) equals tot;
\(n_{\mathrm{pg}}\) equals leftover-parent xor at \(k-1\);
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

- `research/cycle_vz.md` (this note)
- `research/cycle_vz.py`
- `research/cycle_vz.json`
