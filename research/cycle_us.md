# Cycle US: odd-\(j\) leftover halves match even leftover for \(k\ge 2\)

Odd-\(j\) leftover and even leftover both 2-fold parent leftover
union \(d=2\) (Cycles TU/TV). Restricting the parent to
\(n<5U_p/2\) versus \(n\ge 5U_p/2\), even doubling lands on
\(n<5U/2\) versus \(n\ge 5U/2\), while odd-\(j\) doubling lands on
\(n<5U/2\) versus \(n>5U/2\) (parent-half is even, so odd \(n\)
never equals it). Hence odd-\(j\) leftover on \(n<5U/2\) equals
even leftover on \(n<5U/2\), and odd-\(j\) leftover on \(n>5U/2\)
equals even leftover on \(n\ge 5U/2\), for \(k\ge 2\). Dies at
\(k=1\) (parent-half odd; odd-\(j\) leftover sits on \(n=5\)).
Census \(k=8\): small \(8790\), large \(5324=5321+3\). Do **not**
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

Certify: `python3 research/cycle_us.py --certify` (~0.80s).
Dump: `research/cycle_us.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UP/UR
(odd-\(j\) leftover half-split of Cycle TV; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-\(j\) leftover on \(n>5U/2\) \(=\) even leftover on \(n\ge 5U/2\), \(k\ge 2\))

Even doubling \(G(2m,2r)=G(m,r)\) sends parent leftover \(\cup d=2\)
on \(m\ge 5U_p/2\) to even leftover on \(n\ge 5U/2\). Odd-\(j\)
doubling \(G(2m+1,2r+1)=G(m,r)\) sends the same parent set to
odd-\(j\) leftover on \(n>5U/2\). Cycle UR's three leftover pal-pairs
at the even half have even \(j\), so they spill into the odd-\(j\)
large count. Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=1\). **Killed:** odd-\(j\)
large empty; equals leftover; equals \(3\).

## Lemma (odd-\(j\) leftover on \(n<5U/2\) \(=\) even leftover on \(n<5U/2\), \(k\ge 2\))

The complementary parent set \(m<5U_p/2\) 2-folds to both small
halves. Odd-\(j\) never sits on even parent-half. Status: **lemma**.
**Killed** at \(k=1\). Do **not** PREFIX leftover-parent xor large
difference.

## Verdict

`LEMMA` (odd-\(j\) leftover on \(n>5U/2\) equals even leftover on
\(n\ge 5U/2\) for \(k\ge 2\); odd-\(j\) leftover on \(n<5U/2\)
equals even leftover on \(n<5U/2\) for \(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd-\(j\) halves at \(k=1\); odd-\(j\) leftover on even
parent-half; odd-\(j\) large empty; equals leftover; equals \(3\);
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

- `research/cycle_us.md` (this note)
- `research/cycle_us.py`
- `research/cycle_us.json`
