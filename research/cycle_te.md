# Cycle TE: pal-distance \(2\) pairs partition odd \(n\) with \(d=1\); count \(2J_{k+1}\)

Pal-distance \(2\) pairs have \(d=2\), so \(j=n-2\) and partner
\(n+2\). For \(n=2m\) or \(n=2m+1\), \(G(n,n-2)=G(m,m-1)\), so the
cell is a pal-pair iff \(G(m,m-1)=1\). Even and odd covering \(n\)
each contribute \(J_{k+1}\) pairs, total \(2J_{k+1}\). On odd
covering \(n\), \(G(n,n-1)\oplus G(n,n-2)=1\) (\(n=1\) has only
\(d=1\)), so \(d=1\) and \(d=2\) partition the odd covering clocks:
\(J_{k+1}+J_{k+2}=2^{k+1}\). Partner \(n+2\) is clipped except the
single clip-edge cell \(n=3\) at \(k=0\). Spat mismatch is **not**
identically \(0\). Do **not** claim \(d=2\) AND identically \(0\).
Do **not** claim \(d=2\) cells equal clip-edge cells. Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue leftover
\(d\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_te.py --certify`.
Dump: `research/cycle_te.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/ST/SU/SV/SX/SY/TA/TB/TC/TD (pal-distance
\(2\) pal-pairs partition odd \(n\) with \(d=1\); no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(G(n,n-2)=G(m,m-1)\))

Even \(n=2m\): \(G(2m,2m-2)=G(m,m-1)\). Odd \(n=2m+1\):
\(G(2m+1,2m-1)=G(m,m-1)\). Pal-pair iff \(G(m,m-1)=1\). Status:
**lemma**. \(G\)-fold samples through \(k\le 64\); census through
\(k\le 12\).

## Lemma (odd covering \(n\) is partitioned by \(d=1\) and \(d=2\))

Odd \(n=2m+1\ge 3\): \(G(n,n-1)=1\oplus G(m,m-1)\) and
\(G(n,n-2)=G(m,m-1)\), so exactly one of the two distances is a
pal-pair. The leftover clock \(n=1\) is only \(d=1\)
(\(G(0,-1)=0\)). Thus \(J_{k+1}+J_{k+2}=2^{k+1}\) counts every odd
covering \(n\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 12\).

## Lemma (pal-distance \(2\) count is \(2J_{k+1}\))

\(m\in[0,2^{k+1})\) with \(G(m,m-1)=1\) has size
\(2^{k+1}-J_{k+2}=J_{k+1}\). Even covering \(n=2m\) (\(m\ge 1\)) and
odd covering \(n=2m+1\) each contribute that many pairs. Partner
\(n+2\le 4U+1\le 5U\), with equality only at \(k=0\), \(n=3\)
(clip-edge). Status: **lemma**. Count through \(k\le 12\); sum
identity through \(k\le 64\). **Killed:** \(d=2\) cells equal
clip-edge cells. **Killed:** \(d=2\) AND identically \(0\) (spat
mismatch fires at \(k=0,2,6,7\)).

## Verdict

`LEMMA` (\(G(n,n-2)=G(m,m-1)\); odd covering \(n\) partitioned by
\(d=1\) and \(d=2\); pal-distance \(2\) count is \(2J_{k+1}\);
clipped except \(k=0\), \(n=3\)).
`CERTIFIED` (Green census through \(k\le 12\); spat mismatch through
\(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=2\) AND identically \(0\); \(d=2\) cells equal
clip-edge cells; \(d=2\) spat tot equals pal-center tot; \(d=1\)
AND identically \(0\); \(d=1\) cells equal clip-edge cells;
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

- `research/cycle_te.md` (this note)
- `research/cycle_te.py`
- `research/cycle_te.json`
