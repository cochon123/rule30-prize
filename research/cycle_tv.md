# Cycle TV: odd-\(j\) leftover count equals even leftover count

Even leftover pal-pairs are even-\(j\) (\(G(2m,\mathrm{odd})=0\)).
Odd-\(j\) pal-pairs 2-fold parent pal-pairs dropping clip-edge
(Cycle TB), so odd-\(j\) leftover at \(k\ge 2\) is parent leftover
plus parent \(d=2\), matching even leftover (Cycle TU). The two
families are disjoint: even leftover sits on even \(n\), odd-\(j\)
leftover on odd \(n\). Dies at \(k=1\) for the same \(d=2\)/clip-edge
overlap. Odd leftover is strictly larger (even-\(j\) leftover on
odd \(n\)). Do **not** claim odd leftover equals even leftover. Do
**not** claim the odd-\(j\) 2-fold for all \(k\). Do **not**
catalogue leftover \(d\). Do **not** PREFIX leftover spat tot. Do
**not** PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_tv.py --certify` (~0.51s).
Dump: `research/cycle_tv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU
(odd-\(j\) leftover equals even leftover; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-\(j\) leftover count equals even leftover count)

Even leftover is even-\(j\) by \(G(2m,\mathrm{odd})=0\). For
\(k\ge 2\), Cycle TB gives odd-\(j\) leftover as the 2-fold of
parent leftover union parent \(d=2\), which is Cycle TU's even
leftover count. Direct check: \(k=0\) both empty, \(k=1\) both
\(1\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed:** odd leftover equals even leftover.

## Lemma (odd-\(j\) leftover \(=\) parent leftover \(+\) parent \(d=2\), \(k\ge 2\))

Cycle TB: odd-\(j\) pal-pairs drop clip-edge. Parent leftover and
parent \(d=2\) land in leftover at doubled odd \(j\). Same
increment \(2J_k\) as even leftover. Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed:** the
2-fold holds for all \(k\) (dies at \(k=1\)).

## Verdict

`LEMMA` (odd-\(j\) leftover count equals even leftover count;
odd-\(j\) leftover is parent leftover plus parent \(d=2\) for
\(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd leftover equals even leftover; odd-\(j\) leftover
2-fold for all \(k\); even leftover equals parent leftover; four
types partition pal-pairs for all \(k\); leftover pal-pairs empty;
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

- `research/cycle_tv.md` (this note)
- `research/cycle_tv.py`
- `research/cycle_tv.json`
