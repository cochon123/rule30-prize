# Cycle UU: even leftover at \(j=0\) on \(n<5U/2\) is \(5\cdot 2^{k-2}-2\)

\(G(n,0)=1\) for every \(n\). Pal-pair iff \(2n\le 5U\) iff
\(n\le 5U/2\). Clip-edge at \(n=5U/2\), \(d=2\) at \(n=2\), pal-center
at \(n=0\), so leftover \(j=0\) on even \(n\) is even covering
\(n=4,6,\ldots,5U/2-2\), count \(5\cdot 2^{k-2}-2\) for \(k\ge 2\).
Large \(n>5U/2\) has \(j=0\) unpaired, not leftover. Those even
leftover \(j=0\) parents produce leftover \(\mathrm{pair}+g_0\)
children (counted in \(\mathrm{pg{:}lo}\)) but \(g_0+\mathrm{pair}\)
at child \(j=0\), which Cycle UL skips as leftover not
\(\mathrm{gp{:}lo}\). Hence \(\mathrm{gp{:}lo}\) from even parents is
even leftover minus that count. Dies at \(k=1\) (count is \(1\);
\(5\cdot 2^{-1}-2\) is not an integer). Census \(k=8\): even \(j=0\)
small \(318\); \(\mathrm{gp}\) from even parents \(4122=4280-158\).
Do **not** PREFIX leftover-parent xor large difference or pal-center
tot from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\).
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

Certify: `python3 research/cycle_uu.py --certify`.
Dump: `research/cycle_uu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UL/UO/UP/UR
(even leftover \(j=0\) and even-parent \(\mathrm{gp{:}lo}\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (even leftover pal-pairs at \(j=0\) on \(n<5U/2\) equal \(5\cdot 2^{k-2}-2\) for \(k\ge 2\))

\(G(n,0)=1\). Pal-pair iff \(n\le 5U/2\). Exclude pal-center \(n=0\),
named \(d=2\) at \(n=2\), and clip-edge at the half. Unique through
\(k\le 16\). Equals odd \(j=0\) leftover minus \(1\). Status:
**lemma**. Algebra through \(k\le 64\). **Killed** at \(k=1\).
**Killed:** leftover at \(j=0\) on large even \(n\); equals odd
\(j=0\) leftover; equals \(\mathrm{named}_l\) for all \(k\).

## Lemma (\(\mathrm{gp{:}lo}\) from even parents equals \(\mathrm{lo}_e(k-1)\) minus even leftover \(j=0\))

Even leftover parents all produce leftover \(\mathrm{pair}+g_0\)
children (Cycle UP). The \(j=0\) slice produces \(g_0+\mathrm{pair}\)
at child \(j=0\), skipped as leftover not \(\mathrm{gp{:}lo}\).
Census through \(k\le 8\): small half is even leftover small minus
that count; large half is even leftover on \(n\ge 5U_p/2\) (no even
\(j=0\) leftover there). Status: **lemma**. **Killed:**
\(\mathrm{gp}_e=\mathrm{lo}_e\). Do **not** PREFIX leftover-parent
xor large difference.

## Verdict

`LEMMA` (even leftover pal-pairs at \(j=0\) on \(n<5U/2\) equal
\(5\cdot 2^{k-2}-2\) for \(k\ge 2\); \(\mathrm{gp{:}lo}\) from even
parents equals \(\mathrm{lo}_e(k-1)\) minus that count).
`CERTIFIED` (unique through \(k\le 16\); census through \(k\le 8\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (formula at \(k=1\); leftover \(j=0\) on large even \(n\);
equals odd \(j=0\) leftover; equals \(\mathrm{named}_l\) for all
\(k\); \(\mathrm{gp}_e=\mathrm{lo}_e\); pal-center tot equals
\(S\oplus T\)).
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

- `research/cycle_uu.md` (this note)
- `research/cycle_uu.py`
- `research/cycle_uu.json`
