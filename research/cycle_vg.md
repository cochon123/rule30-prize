# Cycle VG: leftover extra xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) match parent leftover xor

Leftover extra except \(j=0\) each produce one leftover-parent xor
child. Cycle UV counts those children as \(\mathrm{xor\_lo}(k-1)\);
Cycle VF signs them as Cycle UI at \(k-1\). Splitting by kind,
leftover extra xor \(n_{\mathrm{pg}}\) is parent leftover xor
\(n_{\mathrm{pg}}=(\mathrm{xor\_lo}+\mathrm{UI})/2\), and leftover
extra xor \(n_{\mathrm{gp}}\) is parent leftover xor
\(n_{\mathrm{gp}}=(\mathrm{xor\_lo}-\mathrm{UI})/2\). Dies at
\(k=8\) for same-\(k\) leftover xor \(n_{\mathrm{pg}}\) (got
\(2650\), not \(8730\)) and for leftover-parent xor \(\mathrm{pg}\)
(got \(2650\), not \(8560\)). Dies at \(k=8\) for
\(n_{\mathrm{pg}}=n_{\mathrm{gp}}\) (got \(2650\), not \(2575\)).
Census \(k=8\): leftover extra xor \(\mathrm{pg}\) \(2650\),
\(\mathrm{gp}\) \(2575\). Do **not** PREFIX pal-center tot from
small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_vg.py --certify` (~0.40s).
Dump: `research/cycle_vg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UI/UP/UQ/UR/UU/UV/UW/UZ/VA/VF
(leftover extra xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (leftover extra xor \(n_{\mathrm{pg}}\) is parent leftover xor \(n_{\mathrm{pg}}\))

Equals \((\mathrm{xor\_lo}(k-1)+\mathrm{UI}(k-1))/2\) for every
\(k\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=8\) for same-\(k\) leftover
xor \(n_{\mathrm{pg}}\) and for leftover-parent xor \(\mathrm{pg}\).

## Lemma (leftover xor \(n_{\mathrm{pg}}=(\mathrm{xor\_lo}+\mathrm{UI})/2\))

Leftover xor \(n_{\mathrm{gp}}=(\mathrm{xor\_lo}-\mathrm{UI})/2\).
Parity \(\mathrm{xor\_lo}+\mathrm{UI}\) even for every \(k\le 64\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** leftover extra xor \(n_{\mathrm{pg}}=n_{\mathrm{gp}}\).
Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) match
parent leftover xor; leftover xor \(n_{\mathrm{pg}}=(\mathrm{xor\_lo}+\mathrm{UI})/2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (same-\(k\) leftover xor \(n_{\mathrm{pg}}\) at \(k=8\);
leftover-parent xor \(\mathrm{pg}\) at \(k=8\); leftover extra xor
\(n_{\mathrm{pg}}=n_{\mathrm{gp}}\); pal-center tot equals
\(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vg.md` (this note)
- `research/cycle_vg.py`
- `research/cycle_vg.json`
