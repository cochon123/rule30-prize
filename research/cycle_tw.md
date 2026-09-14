# Cycle TW: odd-\(n\) even-\(j\) leftover is parent pal-pair adjacent xor

\(G(2m+1,2r)=G(m,r)\oplus G(m,r-1)\) with \(G(m,-1)=0\). Odd-\(n\)
even-\(j\) leftover pal-pairs are the children of a unique parent
pal-pair at \(r\) or \(r-1\). Unpaired parents stay unpaired.
Pal-center parents become \(d=1\). Left-edge \(j=0\) leftover on
odd \(n\) has count \(5\cdot 2^{k-2}-1\) for \(k\ge 2\). Do **not**
claim that extra leftover is empty. Do **not** claim
\(G(2m+1,2r)=G(m,r)\). Do **not** claim odd leftover equals even
leftover. Do **not** catalogue leftover \(d\). Do **not** PREFIX
leftover spat tot. Do **not** PREFIX pal-center tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim pal-center tot
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

Certify: `python3 research/cycle_tw.py --certify`.
Dump: `research/cycle_tw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TV
(odd-\(n\) even-\(j\) leftover parent xor; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(G(2m+1,2r)=G(m,r)\oplus G(m,r-1)\))

Green recurrence \(G(n,j)=G(n-1,j)+G(n-1,j-1)+G(n-1,j-2)\) and
\(G(2m,\mathrm{odd})=0\) give \(G(2m+1,2r)=G(m,r)\oplus G(m,r-1)\),
with \(G(m,-1)=0\). Status: **lemma**. Algebra through \(k\le 64\).
**Killed:** \(G(2m+1,2r)=G(m,r)\).

## Lemma (odd-\(n\) even-\(j\) leftover is parent pal-pair xor)

A leftover even-\(j\) pal-pair on odd \(n=2m+1\), \(j=2r\), has
exactly one of \(G(m,r),G(m,r-1)\) equal to \(1\), and that cell
is a pal-pair (or \(r=0\)). Unpaired parents have child partner
past clip. Pal-center \(r=m\) gives child \(d=1\). Status:
**lemma**. Census through \(k\le 8\). **Killed:** that extra
leftover is empty.

## Lemma (\(j=0\) leftover on odd \(n\) is \(5\cdot 2^{k-2}-1\))

\(G(n,0)=1\). Pal-pair iff \(2n<5U\). Odd covering \(n\in[3,5U/2)\)
has size \(5\cdot 2^{k-2}-1\) for \(k\ge 2\), and size \(1\) at
\(k=1\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\).

## Verdict

`LEMMA` (\(G(2m+1,2r)=G(m,r)\oplus G(m,r-1)\); odd-\(n\) even-\(j\)
leftover is parent pal-pair adjacent xor; \(j=0\) leftover on odd
\(n\) is \(5\cdot 2^{k-2}-1\) for \(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd-\(n\) even-\(j\) leftover empty; \(G(2m+1,2r)=G(m,r)\);
odd leftover equals even leftover; odd-\(j\) leftover 2-fold for
all \(k\); leftover pal-pairs empty; pal-center tot equals
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

- `research/cycle_tw.md` (this note)
- `research/cycle_tw.py`
- `research/cycle_tw.json`
