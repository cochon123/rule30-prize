# Cycle UT: leftover pal-pairs at \(n=5U/2\) produce both xor children

The three Green pal-left cells at covering \(n=5U/2\) (Cycle UR:
\(j=U/2,U,2U\)) sit on even \(n\) for \(k\ge 2\), so both odd
neighbors vanish. Each therefore produces a leftover
\(\mathrm{pair}+g_0\) child and a leftover \(g_0+\mathrm{pair}\)
child at \(n=5U/2+1\), pal-left, distances \(2d-1\) and \(2d+1\).
At parent \(k=2\) the \(2U\) slot is \(d=2\), so those two children
are named; leftover-parent xor from the half is
\(\mathrm{want\_ph\_lo}(k-1)\) of each kind (\(2\) at \(k=3\), \(3\)
for \(k\ge 4\)). Dies at \(k=2\) (parent-half odd). Do **not**
PREFIX leftover-parent xor large difference or pal-center tot from
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

Certify: `python3 research/cycle_ut.py --certify` (~0.80s).
Dump: `research/cycle_ut.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UL/UO/UP/UR/US
(both xor children of the covering half; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (three Green pal-left cells at \(n=5U/2\) produce both leftover xor children for \(k\ge 3\))

Parent-half is even for \(k\ge 2\), so \(G(\mathrm{even},\mathrm{odd})=0\).
Child \(n=5U/2+1\) is covering and large. Distances \(2d\pm 1\) miss
\(\{1,2\}\). Unique through \(k\le 16\): three pair+\(g_0\) and three
\(g_0\)+pair leftover children. Status: **lemma**. Algebra through
\(k\le 64\). **Killed** at \(k=2\). **Killed:** \(\mathrm{gp{:}lo}\)
never sits on even parent-half.

## Lemma (leftover-parent xor from the half is \(\mathrm{want\_ph\_lo}(k-1)\) of each kind)

At parent \(k=2\) the \(2U\) slot is \(d=2\), so leftover-parent xor
is \(2\) of each kind at \(k=3\). For \(k\ge 4\) all three parents
are leftover, hence \(3+3\). Status: **lemma**. Census through
\(k\le 8\). **Killed:** leftover-parent xor is three of each kind at
\(k=3\). Do **not** PREFIX leftover-parent xor large difference.

## Verdict

`LEMMA` (three Green pal-left cells at \(n=5U/2\) produce both
leftover xor children for \(k\ge 3\); leftover-parent xor from the
half is \(\mathrm{want\_ph\_lo}(k-1)\) of each kind).
`CERTIFIED` (unique through \(k\le 16\); census through \(k\le 8\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (both xor at \(k=2\); \(\mathrm{gp{:}lo}\) never on even
parent-half; leftover-parent xor three of each kind at \(k=3\);
pal-center tot equals \(S\oplus T\)).
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

- `research/cycle_ut.md` (this note)
- `research/cycle_ut.py`
- `research/cycle_ut.json`
