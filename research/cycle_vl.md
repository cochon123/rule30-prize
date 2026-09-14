# Cycle VL: leftover extra xor COUNT gap \(n_{\mathrm{pg}}\) is \(2\,\mathrm{lo}_e(k-1)\) minus parent leftover xor \(n_{\mathrm{pg}}\)

Cycle UP \(\mathrm{pg{:}lo}\) is twice even leftover. Leftover extra
xor \(n_{\mathrm{pg}}\) is parent leftover xor \(n_{\mathrm{pg}}\),
so the COUNT gap \(n_{\mathrm{pg}}\) is \(2\,\mathrm{lo}_e(k-1)\)
minus that parent count. COUNT gap \(n_{\mathrm{gp}}\) is the same
minus Cycle UM. Small \(n_{\mathrm{pg}}\) is \(2\,\mathrm{sm}(k-1)\)
minus parent leftover xor small \(n_{\mathrm{pg}}\); large
\(n_{\mathrm{pg}}\) is \(2\,e_{\ge}(k-1)\) minus parent leftover xor
large \(n_{\mathrm{pg}}\). Dies at \(k=2\) for small \(\mathrm{gp}\)
(got \(1\), walk \(0\)). Dies at \(k=2,3\) for large \(\mathrm{gp}\)
(got \(-3\) and \(2\); walk \(0\) and \(3\)). Census \(k=8\): tot
\(5910/5752\). Do **not** PREFIX pal-center tot from small \(k\).
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

Certify: `python3 research/cycle_vl.py --certify` (~0.44s).
Dump: `research/cycle_vl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UM/UO/UP/UR/UU/UV/UW/UY/UZ/VA/VD/VE/VG/VH/VI/VJ/VK
(xor count gap 2 lo_e; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra xor COUNT gap \(n_{\mathrm{pg}}\) is \(2\,\mathrm{lo}_e(k-1)\) minus parent leftover xor \(n_{\mathrm{pg}}\))

COUNT gap \(n_{\mathrm{gp}}\) is that quantity minus Cycle UM.
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\).

## Lemma (COUNT gap small \(n_{\mathrm{pg}}\) is \(2\,\mathrm{sm}(k-1)\) minus parent leftover xor small \(n_{\mathrm{pg}}\); large \(n_{\mathrm{pg}}\) is \(2\,e_{\ge}(k-1)\) minus parent leftover xor large \(n_{\mathrm{pg}}\))

Small \(\mathrm{gp}\) is \(2\,\mathrm{sm}(k-1)\) minus \(\mathrm{UM}_s\)
minus parent small \(n_{\mathrm{gp}}\) for \(k\ge 3\). Large
\(\mathrm{gp}\) is \(2\,e_{\ge}(k-1)\) minus \(\mathrm{UM}_l\) minus
parent large \(n_{\mathrm{gp}}\) for \(k\ge 4\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
small \(\mathrm{gp}\) 2-sm form at \(k=2\); large \(\mathrm{gp}\)
2-ege form at \(k=2,3\); small \(n_{\mathrm{pg}}\) equals tot
\(n_{\mathrm{pg}}\) at \(k=8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (COUNT gap tot \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) from
\(2\,\mathrm{lo}_e\); small/large \(n_{\mathrm{pg}}\) from
\(2\,\mathrm{sm}/2\,e_{\ge}\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (small gp 2-sm at \(k=2\); large gp 2-ege at \(k=2,3\);
small pg equals tot pg; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vl.md` (this note)
- `research/cycle_vl.py`
- `research/cycle_vl.json`
