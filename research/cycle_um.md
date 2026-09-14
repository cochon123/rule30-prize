# Cycle UM: leftover-parent xor difference is \(3\cdot 2^{k-1}+J_{k-2}-2J_k-2\)

Cycle UI leftover xor \(n_{pg}-n_{gp}\) is \(2^{k-1}+J_{k-2}\). Cycle
UL splits those into named \(d=1\)/\(d=2\) plus leftover-parent xor.
Named difference is closed, so leftover-parent xor difference
\(\mathrm{pg{:}lo}-\mathrm{gp{:}lo}\) is
\(3\cdot 2^{k-1}+J_{k-2}-2J_k-2\) for \(k\ge 2\). Do **not** PREFIX
\(\mathrm{pg{:}lo}\) or \(\mathrm{gp{:}lo}\) sums or leftover extra or
unpaired extra or \(n_{pg}+n_{gp}\) or \(n_{ug}+n_{gu}\) from small
\(k\). Do **not** catalogue leftover \(d\). Do **not** PREFIX leftover
spat tot. Do **not** PREFIX pal-center tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor vanishes
for all \(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk
\(k=11\) covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_um.py --certify` (~0.30s).
Dump: `research/cycle_um.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/UC/UD/UE/UI/UK/UL
(leftover-parent xor difference from UI minus named; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (leftover-parent xor difference \(=\) UI minus named difference)

Cycle UL: \(\mathrm{pair}+g_0\) of \(d=1\) is empty, so
\(n_{pg}-n_{gp}=(\mathrm{pg{:}d2}+\mathrm{pg{:}lo})-(\mathrm{gp{:}d1}+\mathrm{gp{:}d2}+\mathrm{gp{:}lo})\).
Named pieces are Jacobsthal, hence
\(\mathrm{pg{:}lo}-\mathrm{gp{:}lo}=n_{pg}-n_{gp}-\mathrm{pg{:}d2}+\mathrm{gp{:}d1}+\mathrm{gp{:}d2}\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\).

## Lemma (\(\mathrm{pg{:}lo}-\mathrm{gp{:}lo}=3\cdot 2^{k-1}+J_{k-2}-2J_k-2\) for \(k\ge 2\))

Expand Cycle UI and Cycle UL: the difference is \(0\) at \(k\le 1\)
and \(3\cdot 2^{k-1}+J_{k-2}-2J_k-2\) for \(k\ge 2\). Census \(k=8\):
\(8560-8327=233\). Status: **lemma**. **Killed:** \(\mathrm{pg{:}lo}=\mathrm{gp{:}lo}\).
**Killed:** the difference equals Cycle UI. **Killed:** the difference
equals named leftover extra. **Killed:** leftover-parent xor sum
equals the difference (dies at \(k=2\): \(\mathrm{gp{:}lo}=0\)). Do **not** PREFIX \(\mathrm{pg{:}lo}+\mathrm{gp{:}lo}\).

## Verdict

`LEMMA` (leftover-parent xor difference is UI minus named;
\(\mathrm{pg{:}lo}-\mathrm{gp{:}lo}=3\cdot 2^{k-1}+J_{k-2}-2J_k-2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(\mathrm{pg{:}lo}=\mathrm{gp{:}lo}\); difference equals UI;
difference equals named leftover extra; difference empty;
leftover-parent xor sum equals the difference; pal-center tot equals
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

- `research/cycle_um.md` (this note)
- `research/cycle_um.py`
- `research/cycle_um.json`
