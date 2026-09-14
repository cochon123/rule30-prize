# Cycle UL: leftover extra from \(d=1\)/\(d=2\) parents is Jacobsthal

\(\mathrm{pair}+g_0\) of a \(d=1\) parent is a \(d=1\) child, so
\(n_{pg}\) from \(d=1\) is empty in leftover extra. \(g_0+\mathrm{pair}\)
of \(d=1\) is leftover \(d=3\) except parent \(n=1\) (child \(j=0\)),
hence that count is \(J_{k+1}-1\) for \(k\ge 1\).
\(\mathrm{pair}+g_0\) of every parent \(d=2\) is leftover extra for
\(k\ge 2\), count \(2J_k\). \(g_0+\mathrm{pair}\) of \(d=2\) occurs
only for even parents (odd \(d=2\) has \(G(m,m-3)=1\)), minus parent
\(n=2\) at \(j=0\), hence \(J_k-1\). Named leftover extra is
\(2^k+2J_k-2\) for \(k\ge 2\). Do **not** PREFIX leftover-parent xor
\(n_{pg}^{\mathrm{lo}}+n_{gp}^{\mathrm{lo}}\) or leftover extra or
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

Certify: `python3 research/cycle_ul.py --certify`.
Dump: `research/cycle_ul.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UI/UK
(named leftover extra from parent \(d=1\)/\(d=2\); no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(g_0+\mathrm{pair}\) leftover extra from \(d=1\) is \(J_{k+1}-1\))

Parent \(d=1\) count is \(J_{k+1}\) (Cycle TD), all odd. Odd covering
\(n\) has \(G(n,n-1)\oplus G(n,n-2)=1\) (Cycle TE), so the left
neighbour is \(g_0\). The child is leftover \(d=3\) except parent
\(n=1\), whose child is the \(j=0\) leftover cell. Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed:**
the count equals \(J_{k+1}\). **Killed:** \(\mathrm{pair}+g_0\) of
\(d=1\) is nonempty in leftover extra.

## Lemma (\(\mathrm{pair}+g_0\) leftover extra from \(d=2\) is \(2J_k\) for \(k\ge 2\))

Parent \(d=2\) count is \(2J_k\) (Cycle TE), disjoint from clip-edge
for \(k-1\ge 1\). Even \(m\) has \(G(m,m-1)=0\), and odd \(d=2\) has
the same by Cycle TE, so every such parent fires \(\mathrm{pair}+g_0\).
The child is leftover \(d=3\), never clip-edge in range. Dies at
\(k=1\): parent \(d=2\) overlaps clip-edge. Status: **lemma**.
**Killed:** the \(k=1\) count equals \(2J_1\).

## Lemma (\(g_0+\mathrm{pair}\) leftover extra from \(d=2\) is \(J_k-1\))

Even \(d=2\) has \(G(m,m-3)=0\) (odd index). Odd \(d=2\) has
\(G(m,m-3)=1\), so it does not fire \(g_0+\mathrm{pair}\). Parent
\(n=2\) gives child \(j=0\). Even \(d=2\) count is \(J_k\), minus that
cell. Status: **lemma**. Named leftover extra is then
\(2^k+2J_k-2\) for \(k\ge 2\). **Killed:** named leftover extra empty.
**Killed:** named leftover extra equals leftover extra. Do **not**
PREFIX leftover-parent xor from small \(k\).

## Verdict

`LEMMA` (\(g_0+\mathrm{pair}\) from \(d=1\) is \(J_{k+1}-1\);
\(\mathrm{pair}+g_0\) from \(d=2\) is \(2J_k\) for \(k\ge 2\);
\(g_0+\mathrm{pair}\) from \(d=2\) is \(J_k-1\);
\(\mathrm{pair}+g_0\) from \(d=1\) empty; named leftover extra is
\(2^k+2J_k-2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(g_0+\mathrm{pair}\) from \(d=1\) equals \(J_{k+1}\); named
leftover extra empty; named leftover extra equals leftover extra;
\(\mathrm{pair}+g_0\) from \(d=2\) equals \(g_0+\mathrm{pair}\) from
\(d=1\); \(d=2\) formula at \(k=1\); pal-center tot equals
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

- `research/cycle_ul.md` (this note)
- `research/cycle_ul.py`
- `research/cycle_ul.json`
