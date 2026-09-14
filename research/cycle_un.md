# Cycle UN: even covering \(d=2\) on each half is parent \(d=1\)

Even covering \(n=2m\) has \(G(n,n-2)=G(m,m-1)\), so pal-distance
\(2\) iff parent \(d=1\). For \(k\ge 1\) the small half
\(n\le 5U/2\) is \(m\le 5U_p/2\), hence even \(d=2\) small/large
equals Cycle UK's \(d=1\) small/large at \(k-1\). Odd covering
\(n=2m+1\) has the same Green fold; for \(k\ge 3\) parent-half is
even so odd \(m\) never sits on the boundary, and odd \(d=2\)
matches parent \(d=1\) on each half. Dies at \(k=2\) (parent-half
\(5\) is odd: parent \(m=5\) is small, child \(n=11\) is large).
Do **not** PREFIX leftover extra or unpaired extra or
\(n_{pg}+n_{gp}\) or \(n_{ug}+n_{gu}\) or leftover-parent xor sum
from small \(k\). Do **not** PREFIX leftover extra or unpaired extra
separately as a single closed form. Do **not** catalogue leftover
\(d\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_un.py --certify` (~0.15s).
Dump: `research/cycle_un.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/UC/UD/UE/UK/UM
(even \(d=2\) halves from parent \(d=1\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even covering \(d=2\) on \(n\le 5U/2\) equals parent \(d=1\) small)

\(G(2m,2m-2)=G(m,m-1)\). Covering even \(n=2m\) ranges \(m\in[1,2U)\).
For \(k\ge 2\) the half \(5U/2\) is even, so \(n\le 5U/2\) iff
\(m\le 5U_p/2\). Parent \(d=1\) lives only on odd \(m\), which is
exactly even \(d=2\). Thus even \(d=2\) small is
\(\mathrm{want\_d1\_small}(k-1)\) and even \(d=2\) large is
\(\mathrm{want\_d1\_large}(k-1)\) for \(k\ge 1\) (and \(1,0\) at
\(k=0\)). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 12\).

## Lemma (odd covering \(d=2\) matches parent \(d=1\) halves for \(k\ge 3\))

\(G(2m+1,2m-1)=G(m,m-1)\). Child \(n=2m+1\le 5U/2\) iff
\(m\le 5U_p/2-1/2\). For \(k\ge 3\) parent-half \(5\cdot 2^{k-2}\)
is even, so the last odd small parent is \(m=5U_p/2-1\), whose
child \(n=5U-1\) still sits on the small half, and parent
\(m=5U_p/2\) is even (not \(d=1\)). Hence odd \(d=2\) small/large
equals parent \(d=1\) small/large. **Killed** at \(k=2\): parent
\(m=5\) is small and odd, child \(n=11>10\). Status: **lemma**.
**Killed:** even \(d=2\) small equals odd \(d=2\) small for all
\(k\). **Killed:** odd \(d=2\) halves follow parent \(d=1\) at
\(k=2\).

## Lemma (covering \(d=2\) on \(n\le 5U/2\) is twice parent \(d=1\) small for \(k\ge 3\))

Even plus odd halves: small \(d=2\) is \(2\cdot\mathrm{want\_d1\_small}(k-1)\)
and large \(d=2\) is \(2\cdot\mathrm{want\_d1\_large}(k-1)\). Census
\(k=8\): small \(106+106=212\), large \(65+65=130\). Status:
**lemma**. **Killed:** \(d=2\) small equals \(d=2\) large.
**Killed:** \(d=2\) small equals \(d=1\) small at the same \(k\).
Do **not** PREFIX leftover extra or leftover-parent xor sum.

## Verdict

`LEMMA` (even covering \(d=2\) on each half is parent \(d=1\);
odd covering \(d=2\) matches parent \(d=1\) halves for \(k\ge 3\);
covering \(d=2\) on \(n\le 5U/2\) is twice parent \(d=1\) small for
\(k\ge 3\)).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even \(d=2\) small equals odd \(d=2\) small; odd \(d=2\)
halves follow parent at \(k=2\); \(d=2\) small equals \(d=2\) large;
\(d=2\) small equals \(d=1\) small; pal-center tot equals
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

- `research/cycle_un.md` (this note)
- `research/cycle_un.py`
- `research/cycle_un.json`
