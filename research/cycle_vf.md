# Cycle VF: leftover extra xor tot difference is \(2^{k-2}+J_{k-3}\)

Leftover extra except \(j=0\) each produce one leftover-parent xor
child. The signed tot difference of those children equals Cycle UI
leftover xor \(n_{\mathrm{pg}}-n_{\mathrm{gp}}\) at the parent:
\(2^{k-2}+J_{k-3}\) for \(k\ge 3\), equivalently
\((7\cdot 2^{k-3}+(-1)^k)/3\). Also leftover-parent tot difference
minus Cycle VE xor small gap for \(k\ge 2\), and leftover extra xor
small difference plus leftover-parent xor large difference for
\(k\ge 4\). Dies at \(k=2\) for the Jacobsthal form if the parent
index is off by one (UI at \(k\) is \(2\), not \(1\)). Dies at
\(k=3\) for small difference plus leftover-parent large difference
helper (got \(2\), not \(3\)). Dies at \(k=8\) for equality with
leftover-parent tot difference (got \(75\), not \(233\)). Census
\(k=8\): tot difference \(75\). Do **not** PREFIX pal-center tot from
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

Certify: `python3 research/cycle_vf.py --certify`.
Dump: `research/cycle_vf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UI/UM/UO/UP/UR/UU/UV/UW/UY/UZ/VA/VC/VE
(leftover extra xor tot DIFF; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra xor tot difference is \(2^{k-2}+J_{k-3}\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Equals Cycle UI
\(n_{\mathrm{pg}}-n_{\mathrm{gp}}\) at \(k-1\) for every \(k\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=2\) for UI at \(k\) (got \(1\), not
\(2\)).

## Lemma (that difference equals leftover-parent tot minus xor small gap for \(k\ge 2\))

Equals leftover extra xor small difference plus leftover-parent xor
large difference for \(k\ge 4\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
small difference plus leftover-parent large difference helper; at
\(k=8\) for leftover-parent tot difference. Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (leftover extra xor tot difference is \(2^{k-2}+J_{k-3}\)
for \(k\ge 3\); equals parent leftover xor \(n_{\mathrm{pg}}-n_{\mathrm{gp}}\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (UI at \(k\) at \(k=2\); leftover-parent tot at \(k=8\);
small DIFF plus leftover-parent large helper at \(k=3\); pal-center
tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vf.md` (this note)
- `research/cycle_vf.py`
- `research/cycle_vf.json`
