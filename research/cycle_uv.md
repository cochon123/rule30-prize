# Cycle UV: even pal-left \(G=1\) on odd covering has unique vanishing neighbor

\(G(2s+1,2t)=G(s,t)\oplus G(s,t-1)\), with neighbors
\(G(2t-1)=G(s,t-1)\) and \(G(2t+1)=G(s,t)\). If the cell is Green,
exactly one neighbor vanishes, and the side is \(G(s,t)\): right
vanishes iff \(G(s,t)=0\) (leftover \(\mathrm{pair}+g_0\) child),
left iff \(G(s,t)=1\) (leftover \(g_0+\mathrm{pair}\) child).
Leftover extra except \(j=0\) therefore each produce one
leftover-parent xor child, count \(\mathrm{xor\_lo}(k-1)\); on
\(n>5U/2\) the count is \(\mathrm{lo\_large}(k-1)\) for \(k\ge 3\).
Odd-\(j\) leftover from even covering parents have both neighbors
\(1\), so they produce no leftover-parent xor. Dies at \(k=2\) for
the large count (parent-half odd). Census \(k=8\): leftover extra
xor \(5225\), large \(2034=1002+1032\). Do **not** PREFIX
leftover-parent xor large difference or pal-center tot from small
\(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\).
Do **not** claim pal-center tot equals \(S\oplus T\). This is **not**
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

Certify: `python3 research/cycle_uv.py --certify` (~0.33s).
Dump: `research/cycle_uv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UL/UP/UQ/UR/UU
(unique vanishing neighbor and leftover extra xor; no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even pal-left \(G=1\) on odd covering has unique vanishing neighbor)

Neighbors of \(G(2s+1,2t)\) are \(G(s,t-1)\) and \(G(s,t)\). Status:
**lemma**. Algebra through \(k\le 64\). **Killed:** both neighbors
vanish (that is even covering).

## Lemma (leftover extra except \(j=0\) produce leftover-parent xor of count \(\mathrm{xor\_lo}(k-1)\))

Each leftover extra pal-pair with \(j>0\) has unique vanishing
neighbor, and \(j=0\) leftover extra has the \(g_0+\mathrm{pair}\)
child skipped at \(r=0\) with the \(\mathrm{pair}+g_0\) side unfired.
Census through \(k\le 8\). On \(n>5U/2\) there is no leftover \(j=0\),
so the large count is \(\mathrm{lo\_large}(k-1)\) for \(k\ge 3\).
Status: **lemma**. **Killed** at \(k=2\) for the large identification.
**Killed:** leftover extra produce both xor children.

## Lemma (odd-\(j\) leftover from even covering parents have both neighbors \(1\))

Even covering has \(G(\mathrm{even},\mathrm{odd})=0\), so both
neighbors of the odd-\(j\) 2-fold are \(1\). Those leftover pal-pairs
produce no leftover-parent xor. Status: **lemma**. Census through
\(k\le 8\). **Killed:** odd-\(j\) leftover never produce leftover-parent
xor. Do **not** PREFIX leftover-parent xor large difference.

## Verdict

`LEMMA` (even pal-left \(G=1\) on odd covering has unique vanishing
neighbor; leftover extra except \(j=0\) produce leftover-parent xor
of count \(\mathrm{xor\_lo}(k-1)\); that xor on \(n>5U/2\) equals
\(\mathrm{lo\_large}(k-1)\) for \(k\ge 3\); odd-\(j\) leftover from
even covering parents have both neighbors \(1\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (large count at \(k=2\); both neighbors vanish on odd
covering even pal-left; leftover extra both xor children; odd-\(j\)
leftover never xor; pal-center tot equals \(S\oplus T\)).
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

- `research/cycle_uv.md` (this note)
- `research/cycle_uv.py`
- `research/cycle_uv.json`
