# Cycle VD: leftover-parent xor small difference is \((25\cdot 2^{k-3}-9-2(-1)^k)/3\)

\(\mathrm{pg}{:}\mathrm{lo}-\mathrm{gp}{:}\mathrm{lo}\) on \(n\le 5U/2\)
equals the Cycle UM tot minus Cycle UY large difference for
\(k\ge 4\), and the closed form
\((25\cdot 2^{k-3}-9-2(-1)^k)/3\) for \(k\ge 3\). Dies at \(k=2\) for
the form (walk \(1\); tot-large is \(-1\)). Dies at \(k=3\) for
tot-large (got \(6\), not \(5\); large difference special-case \(0\)).
Census \(k=8\): leftover-parent xor small difference \(263\). Do
**not** PREFIX pal-center tot from small \(k\). Do **not** PREFIX
leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do
**not** catalogue leftover \(d\). Do **not** claim pal-center tot
equals \(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_vd.py --certify` (~0.35s).
Dump: `research/cycle_vd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UM/UO/UP/UR/UU/UV/UW/UY/UZ/VA/VC
(leftover-parent xor small difference closed form; no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover-parent xor small difference is \((25\cdot 2^{k-3}-9-2(-1)^k)/3\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
as tot-large at \(k=2\) (walk \(1\), tot-large \(-1\)).

## Lemma (leftover-parent xor small difference equals tot minus large for \(k\ge 4\))

Cycle UM tot minus Cycle UY large difference. Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=3\) (walk \(6\), tot-large \(5\)). Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (leftover-parent xor small difference is
\((25\cdot 2^{k-3}-9-2(-1)^k)/3\) for \(k\ge 3\); equals tot minus
large for \(k\ge 4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (tot-large at \(k=2\) and \(k=3\); pal-center tot equals
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

- `research/cycle_vd.md` (this note)
- `research/cycle_vd.py`
- `research/cycle_vd.json`
