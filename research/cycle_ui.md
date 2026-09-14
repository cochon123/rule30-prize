# Cycle UI: leftover xor \(n_{pg}-n_{gp}\) is \(2^{k-1}+J_{k-2}\)

Odd-\(n\) even-\(j\) leftover extra from parent pal-pair xor splits
into \(n_{pg}\) (pair then \(g_0\)) and \(n_{gp}\) (\(g_0\) then
pair). Their difference is \(0\) at \(k=0\), \(1\) at \(k=1\), and
\(2^{k-1}+J_{k-2}\) for \(k\ge 2\), equivalently \(J_k+2^{k-2}\).
Do **not** PREFIX \(n_{pg}+n_{gp}\) from small \(k\). Do **not**
PREFIX leftover extra or unpaired extra separately. Do **not**
PREFIX \(n_{ug}+n_{gu}\). Do **not** catalogue leftover \(d\). Do
**not** PREFIX leftover spat tot. Do **not** PREFIX pal-center tot.
Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim
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

Certify: `python3 research/cycle_ui.py --certify` (~0.30s).
Dump: `research/cycle_ui.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/TW/UC/UD/UE/UG/UH
(leftover xor difference; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(n_{pg}-n_{gp}=2^{k-1}+J_{k-2}\) for \(k\ge 2\))

The two parent-pal-pair adjacent-xor kinds differ by
\(2^{k-1}+J_{k-2}\) for \(k\ge 2\), equivalently \(J_k+2^{k-2}\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\), including the \(k=1\) base count \(1\). **Killed:**
\(n_{pg}=n_{gp}\). **Killed:** the difference equals \(2^{k-1}\).
**Killed:** \(n_{pg}+n_{gp}\) equals that form. Do **not** PREFIX
the leftover xor-pair sum.

## Verdict

`LEMMA` (\(n_{pg}-n_{gp}\) is \(2^{k-1}+J_{k-2}\) for \(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(n_{pg}=n_{gp}\); difference equals \(2^{k-1}\); leftover
xor-pair sum equals the difference; leftover extra empty;
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

- `research/cycle_ui.md` (this note)
- `research/cycle_ui.py`
- `research/cycle_ui.json`
