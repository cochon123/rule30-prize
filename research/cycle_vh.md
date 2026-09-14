# Cycle VH: leftover extra xor small/large \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) match parent halves

Leftover extra except \(j=0\) each produce one leftover-parent xor
child. Cycle VG matches tot \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) to
parent leftover xor. Splitting by \(n\le 5U/2\), leftover extra xor
small \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) equal parent leftover xor
small \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) for \(k\ge 3\), and the
large half likewise. All \(j=0\) leftover is on the small half.
Leftover xor small difference is \(j_0-d_{2e}^{\mathrm{small}}\) for
\(k\ge 3\); leftover xor large difference is
\(1-2^{k-2}+(-1)^{k+1}\) for \(k\ge 2\). Dies at \(k=2\) for the
parent-half match (small got \(0\), parent \(1\); large got \(1\),
parent \(0\)). Dies at \(k=2\) for leftover xor small difference
form (got \(3\), form \(2\)). Census \(k=8\): leftover extra xor
small \(\mathrm{pg}/\mathrm{gp}\) \(1648/1543\), large
\(1002/1032\). Do **not** PREFIX pal-center tot from small \(k\).
Do **not** PREFIX leftover spat tot. Do **not** PREFIX
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

Certify: `python3 research/cycle_vh.py --certify`.
Dump: `research/cycle_vh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UK/UN/UP/UQ/UR/UU/UV/UW/UZ/VA/VC/VG
(leftover extra xor halves; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra xor small/large \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) match parent leftover xor halves for \(k\ge 3\))

Special-case leftover extra xor large \(n_{\mathrm{pg}}=1\) at
\(k=2\); zeros at \(k\le 2\) on the small half. Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=2\) for the parent-half match.

## Lemma (leftover xor small difference is \(j_0-d_{2e}^{\mathrm{small}}\) for \(k\ge 3\))

Leftover xor large difference is \(1-2^{k-2}+(-1)^{k+1}\) for
\(k\ge 2\). \(j=0\) leftover is entirely on \(n\le 5U/2\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** leftover xor small difference form at \(k=2\); leftover
extra xor small \(n_{\mathrm{pg}}\) equals tot \(n_{\mathrm{pg}}\).
Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra xor halves match parent leftover xor halves
for \(k\ge 3\); leftover xor small difference is
\(j_0-d_{2e}^{\mathrm{small}}\) for \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (parent-half match at \(k=2\); leftover xor small
difference form at \(k=2\); leftover extra xor small
\(n_{\mathrm{pg}}\) equals tot \(n_{\mathrm{pg}}\); pal-center tot
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

- `research/cycle_vh.md` (this note)
- `research/cycle_vh.py`
- `research/cycle_vh.json`
