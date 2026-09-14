# Cycle VK: leftover extra xor COUNT gap \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\)

Cycle VI tot gap difference equals Cycle VE xor small gap for every
\(k\), so
\(n_{\mathrm{pg}}=(\mathrm{gap}+\mathrm{VE})/2\) and
\(n_{\mathrm{gp}}=(\mathrm{gap}-\mathrm{VE})/2\). Small halves split
the same way. Large halves are equal, each \(\mathrm{gl}/2\). Dies
at \(k=2,3\) for the leftover-parent xor large difference
reconstruction of large \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) (got
\(1/-1\) and \(3/2\); walk \(0/0\) and \(3/3\)). Dies at \(k=8\)
for small \(n_{\mathrm{pg}}\) equals tot \(n_{\mathrm{pg}}\) (got
\(3684\), not \(5910\)). Census \(k=8\): tot \(5910/5752\), small
\(3684/3526\), large \(2226/2226\). Do **not** PREFIX pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\).
Do **not** claim pal-center tot equals \(S\oplus T\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
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

Certify: `python3 research/cycle_vk.py --certify`.
Dump: `research/cycle_vk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UO/UP/UQ/UR/UU/UV/UW/UY/UZ/VA/VD/VE/VG/VH/VI/VJ
(xor count gap pg/gp; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra xor COUNT gap tot \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) is \((\mathrm{gap}\pm\mathrm{xor\ small\ gap})/2\))

Parity \(\mathrm{gap}+\mathrm{VE}\) is even through \(k\le 64\).
Equals leftover-parent xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) minus
leftover extra xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\). Small halves
split the same way. Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\).

## Lemma (leftover extra xor COUNT gap large \(n_{\mathrm{pg}}=n_{\mathrm{gp}}=\mathrm{gl}/2\))

The two large halves sum to Cycle VJ large gap. Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
UM large reconstruction at \(k=2\) (got \(1/-1\), walk \(0/0\)) and
\(k=3\) \(\mathrm{gp}\) (got \(2\), walk \(3\)); small
\(n_{\mathrm{pg}}\) equals tot \(n_{\mathrm{pg}}\) at \(k=8\). Do
**not** PREFIX pal-center tot.

## Verdict

`LEMMA` (COUNT gap tot/small \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) from
xor small gap; large halves equal).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (UM large recon at \(k=2,3\); small pg equals tot pg;
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

- `research/cycle_vk.md` (this note)
- `research/cycle_vk.py`
- `research/cycle_vk.json`
