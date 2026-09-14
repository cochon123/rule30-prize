# Cycle TK: \(d=1\)/\(d=2\) pal-pairs split by \(n\bmod 8\)

\(G(n,n-1)\) is \(0\) if \(n\) is even, \(1\) if \(n\equiv 1\pmod{4}\),
and \(G(\lfloor n/4\rfloor,\lfloor n/4\rfloor-1)\) if
\(n\equiv 3\pmod{4}\). At \(k\ge 1\) every covering
\(n\equiv 1,5\pmod{8}\) is a \(d=1\) pal-pair and every covering
\(n\equiv 2,3\pmod{8}\) is a \(d=2\) pal-pair. Covering
\(n\equiv 7\pmod{8}\) is partitioned by \(d=1\) and \(d=2\), counts
\(J_k\) and \(J_{k-1}\). Covering \(n\equiv 6\pmod{8}\) carries the
remaining even \(d=2\), count \(J_{k-1}\). Covering times of
\(n\equiv r\pmod{8}\) are the 16-AP \(2U-2r+15,\ldots,10U-2r-1\).
Do **not** claim \(d=1\) on all \(n\equiv 7\pmod{8}\). Do **not**
claim \(d=2\) on all \(n\equiv 6\pmod{8}\). Do **not** claim
pal-center tot on a mod-8 residue identically \(0\). Do **not**
PREFIX pal-center tot by \(n\bmod 8\). Do **not** claim pal-center
tot equals \(S\oplus T\). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover
\(p\) one-by-one. Do **not** catalogue leftover \(d\). Do **not**
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

Certify: `python3 research/cycle_tk.py --certify`.
Dump: `research/cycle_tk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/ST/SV/SX/SY/TA/TB/TD/TE/TF/TI (\(d=1\)/\(d=2\)
pal-pairs split by \(n\bmod 8\); no Fermat table, no extra window,
no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(G(n,n-1)\) by residue)

Even \(n\) has \(G(n,n-1)=0\). If \(n\equiv 1\pmod{4}\) then
\(n=2m+1\) with \(m\) even, so \(G(m,m-1)=0\) and
\(G(n,n-1)=1\oplus 0=1\). If \(n\equiv 3\pmod{4}\) then
\(n=4\ell+3\) and \(G(n,n-1)=G(\ell,\ell-1)\). Status: **lemma**.
Samples through \(k\le 64\).

## Lemma (every \(n\equiv 1,5\pmod{8}\) is \(d=1\); every \(n\equiv 2,3\pmod{8}\) is \(d=2\))

\(n\equiv 1,5\pmod{8}\) is exactly Cycle TF's \(n\equiv 1\pmod{4}\).
At \(k\ge 1\), \(n=8\ell+2\) has parent \(m=4\ell+1\equiv 1\pmod{4}\),
so \(G(m,m-1)=1\) and \(G(n,n-2)=1\); \(n=8\ell+3=2(4\ell+1)+1\) has
the same parent, so \(G(n,n-2)=1\) and \(G(n,n-1)=0\). Counts are
\(2^{k-1}\) each. Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 12\). **Killed:** \(d=1\) on all
\(n\equiv 7\pmod{8}\); \(d=2\) on all \(n\equiv 6\pmod{8}\).

## Lemma (\(n\equiv 7\pmod{8}\) partitioned; remaining even \(d=2\) on \(n\equiv 6\))

Total \(n\equiv 7\pmod{8}\) is \(2^{k-1}\) for \(k\ge 1\), and
\(J_k+J_{k-1}=2^{k-1}\). Cycle TF's \(d=1\) on \(n\equiv 3\pmod{4}\)
is exactly \(d=1\) on \(n\equiv 7\pmod{8}\) (count \(J_k\)); the
complement is \(d=2\) (count \(J_{k-1}\)). Even \(d=2\) off
\(n\equiv 2\pmod{8}\) is \(n\equiv 6\pmod{8}\), count \(J_{k-1}\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 12\).

## Lemma (covering times of \(n\equiv r\pmod{8}\) are a 16-AP)

\(t=10U-2n-1\) with \(n=8\ell+r\) is the AP
\(2U-2r+15,\ldots,10U-2r-1\) of length \(2^{k-1}\) and difference
16. For \(k\ge 3\) these sit in \(t\equiv 15,13,11,9,7,5,3,1\pmod{16}\)
as \(r=0,\ldots,7\). Each is every other term of Cycle TI's
residue-\((r\bmod 4)\) 8-AP. Status: **lemma**. Algebra through
\(k\le 64\); set equality through \(k\le 12\). **Killed:**
pal-center tot on a mod-8 residue identically \(0\).

## Verdict

`LEMMA` (\(G(n,n-1)\) by residue; every \(n\equiv 1,5\pmod{8}\) is
\(d=1\) and every \(n\equiv 2,3\pmod{8}\) is \(d=2\);
\(n\equiv 7\pmod{8}\) partitioned by \(d=1\) and \(d=2\); covering
times of each \(n\bmod 8\) are a 16-AP).
`CERTIFIED` (Green census through \(k\le 12\); pal-tot fire through
\(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=1\) on all \(n\equiv 7\pmod{8}\); \(d=2\) on all
\(n\equiv 6\pmod{8}\); pal-center tot on a mod-8 residue
identically \(0\); \(d=1\) on all odd \(n\); \(d=2\) on all even
\(n\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tk.md` (this note)
- `research/cycle_tk.py`
- `research/cycle_tk.json`
