# Cycle UR: leftover pal-pairs at \(n=5U/2\) are three; \(\mathrm{pg{:}lo}\) halves 2-fold

Covering \(n=5U/2\) has \(2n=\)clip, so \(j=0\) is clip-edge. Even
doubling gives \(G(5U/2,U/2)=G(5,1)\), \(G(5U/2,U)=G(5,2)\),
\(G(5U/2,2U)=G(5,4)\), all \(1\), and \(G(5,3)=0\). The only
non-clip Green pal-left cells are those three indices, leftover for
\(k\ge 3\). At \(k=1\) there are two leftover pal-pairs; at \(k=2\)
the \(2U\) slot is \(d=2\). For \(k\ge 3\),
\(\mathrm{pg{:}lo}\) on \(n\le 5U/2\) is twice even leftover on
parent \(n<5U_p/2\), and on \(n>5U/2\) twice even leftover on parent
\(n\ge 5U_p/2\) (the three at the half spill large). Dies at \(k=2\)
(parent-half odd). Do **not** PREFIX leftover-parent xor large
difference or pal-center tot from small \(k\). Do **not** PREFIX
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

Certify: `python3 research/cycle_ur.py --certify` (~0.54s).
Dump: `research/cycle_ur.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UO/UP/UQ
(leftover triple at the covering half; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover pal-pairs at \(n=5U/2\) are three for \(k\ge 3\))

\(n=5\cdot 2^{k-1}\) is a multiple of \(2^{k-1}\), so \(G(n,j)\)
vanishes unless \(j=2^{k-1}t\). Pal-left forces \(t\le 4\). \(G(5,t)\)
is \(1,1,1,0,1\) on \(t=0,\ldots,4\); \(t=0\) is clip-edge
(\(2n=5U\)). The remaining three have distances \(2U\), \(3U/2\),
\(U/2\), none of \(\{1,2\}\) for \(k\ge 3\). **Killed** at \(k=2\):
distance \(U/2=2\) is \(d=2\). Status: **lemma**. Algebra through
\(k\le 64\); unique count through \(k\le 16\).

## Lemma (\(\mathrm{pg{:}lo}\) halves are twice even leftover split at parent-half for \(k\ge 3\))

Child \(n=2m+1\) is large iff \(m\ge 5U_p/2\). Even leftover at
parent-half therefore spills large; even leftover strictly below
stays small. Cycle UP's odd-parent half matches even leftover on
each side. Census \(k=8\): small \(2\cdot 2666=5332\), large
\(2\cdot(1611+3)=3228\). **Killed** at \(k=2\) (parent-half odd).
Status: **lemma**. Do **not** PREFIX leftover-parent xor large
difference.

## Verdict

`LEMMA` (leftover pal-pairs at \(n=5U/2\) are three for \(k\ge 3\);
\(\mathrm{pg{:}lo}\) halves 2-fold even leftover split at
parent-half for \(k\ge 3\)).
`CERTIFIED` (unique count through \(k\le 16\); census through
\(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (three leftover at \(k=2\); leftover at the half empty;
leftover at the half equals Jacobsthal; \(\mathrm{pg{:}lo}\) halves
at \(k=2\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (leftover-parent xor large difference; even-\(n\) rest xor
at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\); packed
rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\); leftover
after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ur.md` (this note)
- `research/cycle_ur.py`
- `research/cycle_ur.json`
