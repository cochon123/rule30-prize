# Cycle UD: pal-pair plus unpaired is \(2^{k+1}(F_{k+4}-1)\)

\(G(n,n)=1\) for every \(n\): even doubling gives \(G(2m,2m)=G(m,m)\)
and odd doubling gives \(G(2m+1,2m+1)=G(m,m)\), so the centre bit
is \(G(0,0)=1\). Pal-center count is \(4U=2^{k+2}\). Pal-left covering
cells have \(j\le n<4U<5U\), so they are never clip-constrained, and
the pal-left \(G=1\) tot is \((W(4U)+4U)/2=2^{k+1}(F_{k+4}+1)\) from
Cycle UC's \(W(2^a)=2^a F_{a+2}\). Hence pal-pair plus unpaired is
\(2^{k+1}(F_{k+4}-1)\). Do **not** PREFIX leftover extra or unpaired
extra separately. Do **not** catalogue leftover \(d\). Do **not**
PREFIX leftover spat tot. Do **not** PREFIX pal-center tot. Do
**not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** claim pal-center
tot equals \(S\oplus T\). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
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

Certify: `python3 research/cycle_ud.py --certify` (~0.51s).
Dump: `research/cycle_ud.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TW/TZ/UA/UB/UC
(\(G(n,n)=1\); pal-pair plus unpaired Fibonacci; no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(G(n,n)=1\) for every \(n\); pal-center count \(=4U\))

Freshman doubling: \(G(2m,2m)=G(m,m)\) and
\(G(2m+1,2m+1)=G(m,m)\). Iterate to \(G(0,0)=1\). Covering \(n<4U\)
gives pal-center count \(2^{k+2}\). Status: **lemma**. Algebra
through \(n\le 64\) and \(k\le 64\). **Killed:** \(G(n,n)=n\bmod 2\).
**Killed:** pal-center count \(=2^{k+1}\).

## Lemma (pal-pair plus unpaired \(=2^{k+1}(F_{k+4}-1)\))

Pal-left covering cells are unclipped. Pal-left tot is
\((W(4U)+4U)/2=2^{k+1}(F_{k+4}+1)\). Subtract pal-center.
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed:** pal-pair plus unpaired \(=2^{k+2}\).

## Verdict

`LEMMA` (\(G(n,n)=1\) for every \(n\); pal-center count \(=4U\);
pal-left tot \(=2^{k+1}(F_{k+4}+1)\); pal-pair plus unpaired
\(=2^{k+1}(F_{k+4}-1)\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(G(n,n)=n\bmod 2\); pal-center count \(=2^{k+1}\);
pal-pair plus unpaired \(=2^{k+2}\); extra sum empty; tot
\(=2^{k+2}\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ud.md` (this note)
- `research/cycle_ud.py`
- `research/cycle_ud.json`
