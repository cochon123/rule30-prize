# Cycle UQ: leftover extra large, parent-xor large sum, and xor_lo close

Leftover extra on \(n>5U/2\) is Cycle UP extra leftover minus Cycle
UK \(\mathrm{lo\_small}\). Leftover-parent xor large sum is
leftover-parent xor total minus Cycle UO small sum. Leftover xor-pair
\(n_{pg}+n_{gp}\) is extra leftover minus \(j=0\) leftover, equivalently
named leftover extra plus leftover-parent xor total. The large half
partitions as named large plus leftover-parent xor large (no \(j=0\)
on \(n>5U/2\)). Do **not** PREFIX leftover-parent xor large
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

Certify: `python3 research/cycle_uq.py --certify` (~0.40s).
Dump: `research/cycle_uq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TB/TD/TE/TT/TU/TW/UC/UD/UE/UK/UL/UM/UO/UP
(leftover extra large and xor_lo from extra_lo; no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra on \(n>5U/2\) \(=\) extra_lo minus lo_small)

Odd-\(n\) even-\(j\) leftover extra splits by \(n\le 5U/2\). Cycle
UK closed the small half; Cycle UP closed the tot. Census \(k=8\):
\(17630-10986=6644\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed:** leftover extra large equals
leftover extra tot. **Killed:** leftover extra large equals named
leftover extra.

## Lemma (leftover-parent xor large sum \(=\) total minus small)

Cycle UP closed \(\mathrm{pg{:}lo}+\mathrm{gp{:}lo}\); Cycle UO
closed the small half. Census \(k=8\): \(16887-10401=6486\). Large
leftover extra partitions as named large plus this sum (no \(j=0\)
on the large half): \(158+6486=6644\). Status: **lemma**. **Killed:**
leftover-parent xor large sum equals Cycle UM difference.
**Killed:** leftover-parent xor large sum equals the small sum. Do
**not** PREFIX leftover-parent xor large difference.

## Lemma (\(n_{pg}+n_{gp}=\) extra_lo minus \(j=0\))

Leftover extra parent-xor including named \(d=1\)/\(d=2\) is extra
leftover minus the \(j=0\) leftover edge, equivalently named plus
leftover-parent xor total. Census \(k=8\): \(17630-319=17311\).
Status: **lemma**. **Killed:** xor_lo equals leftover-parent xor
total (missing named).

## Verdict

`LEMMA` (leftover extra large is extra_lo minus lo_small;
leftover-parent xor large sum is total minus small; leftover extra
large is named large plus that sum; \(n_{pg}+n_{gp}\) is extra_lo
minus \(j=0\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (leftover extra large equals leftover extra tot;
leftover-parent xor large sum equals UM difference; leftover-parent
xor large sum equals the small sum; xor_lo equals leftover-parent
xor total; leftover extra large equals named leftover extra;
leftover extra large equals named large; pal-center tot equals
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

- `research/cycle_uq.md` (this note)
- `research/cycle_uq.py`
- `research/cycle_uq.json`
