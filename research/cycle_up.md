# Cycle UP: \(\mathrm{pg{:}lo}\) is twice even leftover; leftover extra is closed

Even leftover pal-pairs have next bit \(0\), because
\(G(\mathrm{even},\mathrm{odd})=0\). Every even leftover parent
\((m,r)\) therefore produces a leftover \(\mathrm{pair}+g_0\)
child \(n=2m+1\), \(j=2(r+1)\): distance \(2d-1\ge 5\), pal-partner
doubles and stays at most \(5U\), and the child is pal-left covering.
Census through \(k\le 8\) matches the odd-parent half to the same
even leftover count, so \(\mathrm{pg{:}lo}(k)=2\,\mathrm{lo}_e(k-1)\)
for \(k\ge 1\). Cycle UM's leftover-parent xor difference then
gives the total sum \(4\,\mathrm{lo}_e(k-1)\) minus that
difference. Leftover extra partitions as named plus \(j=0\) leftover
plus leftover-parent xor, and unpaired extra is Cycle UC's extra-sum
minus leftover extra. Even leftover itself solves the linear
recurrence from Cycles TU and TV plus the doubling, hence
\((75\cdot 2^k F_k+39\cdot 2^k L_k-100\cdot 2^k-20(-1)^k+12)/60\)
for \(k\ge 1\). The \(k=0\) numerator is not a multiple of \(60\).
Do **not** PREFIX pal-center tot or leftover-parent xor large
difference from small \(k\). Do **not** PREFIX leftover spat tot.
Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue
leftover \(d\). Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_up.py --certify` (~0.50s).
Dump: `research/cycle_up.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UL/UM/UO
(even leftover closed form and leftover extra from \(\mathrm{pg{:}lo}\)
doubling; no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (\(\mathrm{pg{:}lo}(k)=2\,\mathrm{lo}_e(k-1)\) for \(k\ge 1\))

Even leftover is even-\(j\) (Cycle TV). Next bit is \(0\), so every
even leftover pal-pair is \(\mathrm{pair}+g_0\) into a leftover
child. The odd-parent leftover next-\(0\) family has the same count
through \(k\le 8\). Census \(k=8\): \(8560=2\cdot 4280\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed:** \(\mathrm{pg{:}lo}\) equals even leftover (missing the
factor \(2\)).

## Lemma (leftover-parent xor total sum \(=4\,\mathrm{lo}_e(k-1)\) minus UM difference)

\(\mathrm{gp{:}lo}=\mathrm{pg{:}lo}\) minus Cycle UM's closed
difference, so the sum is \(4\,\mathrm{lo}_e(k-1)\) minus that
form. Census \(k=8\): \(17120-233=16887\). Status: **lemma**.
**Killed:** leftover-parent xor sum equals the difference.
**Killed:** leftover-parent xor total sum equals Cycle UO's small
sum. Do **not** PREFIX leftover-parent xor large difference.

## Lemma (leftover extra and unpaired extra)

Leftover extra is named plus \(j=0\) leftover plus leftover-parent
xor. Census \(k=8\): \(424+319+16887=17630\). Unpaired extra is
Cycle UC extra-sum minus leftover extra: \(10019\) at \(k=8\).
Status: **lemma**. **Killed:** leftover extra equals unpaired extra.

## Lemma (even leftover closed form for \(k\ge 1\))

Cycles TU and TV give \(\mathrm{lo}_e(k)=2\,\mathrm{lo}_e(k-1)+\mathrm{extra\_lo}(k-1)+2J_k\)
for \(k\ge 3\). Substituting leftover extra closes the recurrence
\(\mathrm{lo}_e(k)-2\mathrm{lo}_e(k-1)-4\mathrm{lo}_e(k-2)=(5\cdot 2^k+(-1)^k)/3-1\).
The Fibonacci–Lucas particular plus homogeneous solution is
\((75\cdot 2^k F_k+39\cdot 2^k L_k-100\cdot 2^k-20(-1)^k+12)/60\).
**Killed** at \(k=0\): the numerator is \(-30\). Status: **lemma**.

## Verdict

`LEMMA` (\(\mathrm{pg{:}lo}\) is twice even leftover at \(k-1\);
leftover-parent xor total sum is \(4\,\mathrm{lo}_e(k-1)\) minus UM
difference; leftover extra is named plus \(j=0\) plus that sum;
unpaired extra is extra-sum minus leftover extra; even leftover
closed form for \(k\ge 1\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(\mathrm{pg{:}lo}\) equals even leftover; leftover-parent
xor sum equals the difference; leftover-parent xor total sum equals
the small sum; even leftover formula at \(k=0\); leftover extra
equals unpaired extra; \(\mathrm{pg{:}lo}=\mathrm{gp{:}lo}\);
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

- `research/cycle_up.md` (this note)
- `research/cycle_up.py`
- `research/cycle_up.json`
