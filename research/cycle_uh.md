# Cycle UH: unpaired xor \(n_{ug}-n_{gu}\) is Jacobsthal

Odd-\(n\) even-\(j\) unpaired extra from parent unpaired xor splits
into \(n_{ug}\) (unpaired then \(g_0\)) and \(n_{gu}\) (\(g_0\) then
unpaired). Their difference is \(0\) at \(k\le 1\), \(J_k+J_{k-2}\)
for even \(k\ge 2\), and \(J_k+2J_{k-3}\) for odd \(k\ge 3\),
equivalently \((5\cdot 2^{k-2}-2+(k\bmod 2))/3\). Do **not** PREFIX
\(n_{ug}+n_{gu}\) from small \(k\). Do **not** PREFIX leftover extra
or unpaired extra separately. Do **not** catalogue leftover \(d\).
Do **not** PREFIX leftover spat tot. Do **not** PREFIX pal-center
tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_uh.py --certify` (~0.29s).
Dump: `research/cycle_uh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/UA/UB/UC/UD/UE/UG
(unpaired xor difference Jacobsthal; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(n_{ug}-n_{gu}=J_k+J_{k-2}\) even, \(J_k+2J_{k-3}\) odd)

The two parent-unpaired adjacent-xor kinds differ by a Jacobsthal
form for \(k\ge 2\), equivalently
\((5\cdot 2^{k-2}-2+(k\bmod 2))/3\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed:**
\(n_{ug}=n_{gu}\). **Killed:** the difference equals \(J_k\).
**Killed:** \(n_{ug}+n_{gu}\) equals that form. Do **not** PREFIX
the xor-unp sum.

## Verdict

`LEMMA` (\(n_{ug}-n_{gu}\) is \(J_k+J_{k-2}\) for even \(k\ge 2\) and
\(J_k+2J_{k-3}\) for odd \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(n_{ug}=n_{gu}\); difference equals \(J_k\); xor-unp
equals the difference; unpaired extra is parent xor alone;
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

- `research/cycle_uh.md` (this note)
- `research/cycle_uh.py`
- `research/cycle_uh.json`
