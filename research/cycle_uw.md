# Cycle UW: leftover extra on \(n\equiv 1\pmod{4}\) is sign-balanced; empty at \(3U+1\)

Covering \(n=3U\) has pal-left \(G=1\) only at \(j=0\) (unpaired) and
\(j=U\) (clip-edge), plus pal-center, by folding \(G(3\cdot 2^k,2^k d)=G(3,d)\).
No leftover pal-pairs. Even parent leftover \(\cup d=2\) is therefore
empty at \(n=3U_p\), so leftover extra is empty at the child
\(n=3U+1\). On \(n\equiv 1\pmod{4}\), \(s\) is even, so leftover extra
has \(G(s,t)=1\) iff \(j\equiv 0\pmod{4}\) and \(G(s,t)=0\) iff
\(j\equiv 2\pmod{4}\). Those cells pair as \((j,j+2)\) from even
parent leftover \(\cup d=2\) for \(k\ge 2\), so the signs balance and leftover extra
on \(n\equiv 1\pmod{4}\) contributes \(0\) to leftover-parent xor
large difference. The imbalance lives on \(n\equiv 3\pmod{4}\). Dies
at \(k=1\) for equal \(j\bmod 4\) counts. Dies at \(k=0\) for leftover
empty at \(3U\) (\(d=2\) clip overlap). Census
\(k=8\): large \(n\equiv 1\) leftover extra \(j\equiv 0\) and
\(j\equiv 2\) both \(1645\). Unique empty at \(3U+1\) through
\(k\le 16\). Do **not** PREFIX leftover-parent xor large difference
or pal-center tot from small \(k\). Do **not** PREFIX leftover spat
tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue
leftover \(d\). Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_uw.py --certify`.
Dump: `research/cycle_uw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UP/UR/UU/UV
(\(n=3U\) pal-left fold and leftover extra \(n\equiv 1\) signs; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (covering \(n=3U\) has no leftover pal-pairs for \(k\ge 1\))

Pal-left \(G=1\) only at \(j=0\) (unpaired, partner \(6U>5U\)) and
\(j=U\) (clip-edge, partner \(5U\)). Pal-center at \(j=n\). Status:
**lemma**. Algebra through \(k\le 64\); unique through \(k\le 16\).
**Killed** at \(k=0\) as a \(d=2\) clip overlap.

## Lemma (leftover extra is empty at covering \(n=3U+1\))

The even parent \(n=3U_p\) has no leftover and no \(d=2\) (\(n\equiv 0
\pmod{4}\) for \(k\ge 2\)). Status: **lemma**. Unique through
\(k\le 16\). **Killed:** leftover extra at \(3U+1\).

## Lemma (leftover extra on \(n\equiv 1\pmod{4}\) is sign-balanced)

\(s\) even, so \(G(s,t)=0\) on odd \(t\) and leftover extra at even
\(t\) has \(G(s,t)=1\). Even parent leftover \(\cup d=2\) produces
pal-left leftover extra in \((j,j+2)\) pairs for \(k\ge 2\), hence equal \(j\equiv 0
\pmod{4}\) and \(j\equiv 2\pmod{4}\) counts. Large \(n\equiv 1\)
therefore contributes \(0\) to leftover-parent xor large difference.
Census through \(k\le 8\): every large \(n\equiv 3\pmod{4}\) has
leftover extra; every large \(n\equiv 1\pmod{4}\) except \(3U+1\)
has leftover extra. Status: **lemma**. **Killed** at \(k=1\) for
equal counts. **Killed:** unbalanced signs
on \(n\equiv 1\); large difference from leftover extra on \(n\equiv
1\). Do **not** PREFIX leftover-parent xor large difference.

## Verdict

`LEMMA` (covering \(n=3U\) has no leftover pal-pairs for \(k\ge 1\);
leftover extra empty at \(n=3U+1\); leftover extra on
\(n\equiv 1\pmod{4}\) is sign-balanced and contributes \(0\) to
leftover-parent xor large difference).
`CERTIFIED` (unique through \(k\le 16\); census through \(k\le 8\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (equal \(j\bmod 4\) counts at \(k=1\); leftover empty at \(3U\) as no \(d=2\) at \(k=0\); leftover
extra at \(3U+1\); \(n\equiv 1\) unbalanced; large difference from
\(n\equiv 1\); pal-center tot equals \(S\oplus T\)).
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

- `research/cycle_uw.md` (this note)
- `research/cycle_uw.py`
- `research/cycle_uw.json`
