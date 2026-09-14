# Cycle TM: \(d=1\) covering times are odd-\(a\) APs; \(d=2\) \(n\) splits by valuation

Covering times of \(d=1\) pal-pairs are the disjoint union of APs
\(t=10U-2^{a+1}+1\) down by \(2^{a+2}\) over odd \(a\). The \(a=1\)
slice is Cycle TH's \(n\equiv 1\pmod{4}\) 8-AP. Odd \(d=2\) covering
\(n\) is the even-\(a\ge 2\) \(n\)-AP union; even \(d=2\) is
\(n=2^{b+1}-2\) step \(2^{b+2}\) over odd \(b\). Do **not** claim
\(d=1\) times are a single AP. Do **not** PREFIX pal-center tot on
an \(a\)-slice. Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue leftover \(d\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_tm.py --certify` (~0.15s).
Dump: `research/cycle_tm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/OJ/PB/QV/SO/SV/SX/SY/TD/TE/TH/TI/TL (\(d=1\) times
are odd-\(a\) APs; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (\(d=1\) covering times are the odd-\(a\) time APs)

\(n=2^a-1+2^{a+1}\ell\) has covering time
\(t=10U-2^{a+1}+1-2^{a+2}\ell\). Over odd \(a\) with
\(2^a-1<4U\) these APs are disjoint and exhaust \(d=1\). Status:
**lemma**. Algebra through \(k\le 64\); set equality through
\(k\le 12\). **Killed:** \(d=1\) times are a single AP.

## Lemma (the \(a=1\) slice is the \(n\equiv 1\pmod{4}\) 8-AP)

\(a=1\) has step \(8\), length \(U\), endpoints \(2U+5\) and
\(10U-3\), matching Cycle TH / Cycle TI residue \(1\). Status:
**lemma**. Algebra through \(k\le 64\).

## Lemma (\(d=2\) covering \(n\) is even-\(a\) plus even-\(n\) APs)

Odd \(d=2\) is \(\{n:v_2(n+1)=a\}\) for even \(a\ge 2\), the APs
\(2^a-1\) step \(2^{a+1}\). Even \(d=2\) is
\(n=2^{b+1}-2+2^{b+2}\ell\) over odd \(b\). Each family has count
\(J_{k+1}\). Status: **lemma**. Algebraic counts through \(k\le 64\);
set equality through \(k\le 12\).

## Verdict

`LEMMA` (\(d=1\) covering times are the odd-\(a\) time APs; \(a=1\)
is the \(n\equiv 1\pmod{4}\) 8-AP; \(d=2\) covering \(n\) is even-\(a\)
plus even-\(n\) APs).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=1\) times are a single AP; \(G(n,n-1)=1\) iff
\(n\equiv 1\pmod{4}\); \(d=1\) iff \(n\equiv 1\pmod{4}\); pal-center
tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tm.md` (this note)
- `research/cycle_tm.py`
- `research/cycle_tm.json`
