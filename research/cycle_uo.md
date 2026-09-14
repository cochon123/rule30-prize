# Cycle UO: leftover-parent xor small sum is lo_small minus named small minus \(j=0\)

Named leftover extra on \(n\le 5U/2\) follows parent \(d=1\)/\(d=2\)
halves. \(g_0+\mathrm{pair}\) of \(d=1\) is leftover extra except
parent \(n=1\) (child \(j=0\)): for \(k\ge 3\) the child is small iff
the odd parent is small, so \(\mathrm{gp{:}d1}\) small is parent
\(d=1\) small minus \(1\). \(\mathrm{pair}+g_0\) of every parent
\(d=2\) is leftover extra for \(k\ge 2\); for \(k\ge 4\) parent-half
\(5\cdot 2^{k-2}\) is even and not \(d=2\) (\(G(\mathrm{even},\mathrm{odd})=0\)),
so \(\mathrm{pg{:}d2}\) small is parent \(d=2\) small. \(g_0+\mathrm{pair}\)
of even parent \(d=2\) minus parent \(n=2\) likewise follows the even
parent half for \(k\ge 4\). Dies at \(k=3\): parent-half \(m=10\) is
\(d=2\), child \(n=21\) is large. Leftover extra on the small half is
named small plus leftover-parent xor small plus \(j=0\) leftover, so
the leftover-parent xor small sum is Cycle UK \(\mathrm{lo\_small}\)
minus named small minus \(j=0\). Do **not** PREFIX leftover-parent
xor total sum or leftover extra or unpaired extra or
\(n_{pg}+n_{gp}\) or \(n_{ug}+n_{gu}\) from small \(k\). Do **not**
catalogue leftover \(d\). Do **not** PREFIX leftover spat tot. Do
**not** PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat
tot. Do **not** claim pal-center tot equals \(S\oplus T\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
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

Certify: `python3 research/cycle_uo.py --certify` (~0.36s).
Dump: `research/cycle_uo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UK/UL/UM/UN
(named leftover extra halves from parent \(d=1\)/\(d=2\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (\(\mathrm{gp{:}d1}\) on each half is parent \(d=1\) minus \(n=1\) for \(k\ge 3\))

Child \(n=2m+1\), \(j=2(m-1)\) from \(g_0+\mathrm{pair}\) of a
\(d=1\) parent. For \(k\ge 3\) parent-half is even, so odd \(m\)
never sits on the boundary: the child is small iff the parent is
small. Parent \(n=1\) is the \(j=0\) exception. Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\).

## Lemma (\(\mathrm{pg{:}d2}\) and \(\mathrm{gp{:}d2}\) follow parent \(d=2\) halves for \(k\ge 4\))

Parent-half \(m=5\cdot 2^{k-2}\) is even for \(k\ge 3\) and not
\(d=2\) for \(k\ge 4\), because \(G(m/2,m/2-1)=0\) on even
\(m/2\). So \(\mathrm{pair}+g_0\) of parent \(d=2\) stays on the
same half, and \(g_0+\mathrm{pair}\) of even parent \(d=2\) minus
\(n=2\) does too. **Killed** at \(k=3\): parent \(m=10\) is
\(d=2\) (\(G(5,4)=1\)), child \(n=21>20\). Status: **lemma**.

## Lemma (leftover-parent xor small sum \(=\) lo_small minus named small minus \(j=0\))

Leftover extra on \(n\le 5U/2\) partitions as named small plus
leftover-parent xor small plus \(j=0\) leftover. Cycle UK closed
the small leftover extra tot; \(j=0\) leftover is
\(5\cdot 2^{k-2}-1\). Census \(k=8\): \(10986-266-319=10401\).
Status: **lemma**. **Killed:** named small equals named leftover
extra. **Killed:** leftover-parent xor small sum equals Cycle UM
difference. **Killed:** leftover-parent xor small sum equals the
total leftover-parent xor sum. Do **not** PREFIX leftover-parent
xor total sum or leftover extra on \(n>5U/2\).

## Verdict

`LEMMA` (\(\mathrm{gp{:}d1}\) halves follow parent \(d=1\) for
\(k\ge 3\); \(\mathrm{pg{:}d2}\) and \(\mathrm{gp{:}d2}\) follow
parent \(d=2\) halves for \(k\ge 4\); leftover-parent xor small sum
is lo_small minus named small minus \(j=0\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (named small equals named leftover extra; named small
equals named large; leftover-parent xor small sum equals UM
difference; leftover-parent xor small sum equals the total sum;
\(\mathrm{pg{:}d2}\) halves follow parent \(d=2\) at \(k=3\);
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

- `research/cycle_uo.md` (this note)
- `research/cycle_uo.py`
- `research/cycle_uo.json`
