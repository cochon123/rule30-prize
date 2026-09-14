# Cycle TO: valuation classes 2-fold; odd child \(a\) maps to \(a+1\)

At \(k\ge 1\), odd children of covering \(n\) with \(v_2(n+1)=a\)
have \(v_2=a+1\) and covering times \(2t-1\), filling the child
\(a+1\) time AP. Even children have \(v_2(n/2+1)=a\) and are even
\(d=2\) iff \(a\) is odd, with times \(2t+1\) filling the even-\(d=2\)
\(b=a\) AP. Do **not** claim even children of \(d=1\) stay \(d=1\).
Do **not** claim cellwise spat 2-fold. Do **not** PREFIX pal-center
tot by valuation class. Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue leftover \(d\). Do **not**
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

Certify: `python3 research/cycle_to.py --certify` (~0.16s).
Dump: `research/cycle_to.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/OJ/PB/QV/SO/SV/SX/SY/SZ/TD/TE/TL/TM/TN (valuation
2-fold; no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (odd child of class \(a\) is class \(a+1\), times \(2t-1\))

\(v_2(2N+2)=1+v_2(N+1)\). Parent times \(t\) map to \(2t-1\), so
parent endpoints \(10U_p-2^{a+1}+1\) become child endpoints
\(10U-2^{a+2}+1\) with step \(2^{a+3}\). Counts match:
\(d_1(k-1,a)=d_1(k,a+1)\). Status: **lemma**. Algebra through
\(k\le 64\); set equality through \(k\le 12\).

## Lemma (even child of class \(a\) is even \(d=2\) iff \(a\) odd)

Even child \(n=2N\) has \(v_2(n/2+1)=a\), hence even \(d=2\) iff
\(a\) is odd (Cycle TL). Times \(2t+1\) fill the even-\(d=2\)
\(b=a\) AP. This is Cycle TG's \(d=2=\) both children of \(d=1\) in
valuation language. Status: **lemma**. Algebra through \(k\le 64\);
set equality through \(k\le 12\). **Killed:** even children of
\(d=1\) stay \(d=1\).

## Verdict

`LEMMA` (odd child of class \(a\) is class \(a+1\) with times
\(2t-1\); even child is even \(d=2\) iff \(a\) odd, times \(2t+1\)).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (even children of \(d=1\) stay \(d=1\); \(d=1\)/\(d=2\)
times are a single AP; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_to.md` (this note)
- `research/cycle_to.py`
- `research/cycle_to.json`
