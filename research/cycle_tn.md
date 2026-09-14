# Cycle TN: every \(v_2(n+1)=a\) class has a time AP; even \(d=2\) times too

Covering times of \(n\) with \(v_2(n+1)=a\) are the AP
\(10U-2^{a+1}+1\) with step \(2^{a+2}\), for every \(a\ge 1\). Odd
\(a\) is \(d=1\) (Cycle TM); even \(a\ge 2\) is odd \(d=2\). Even
\(d=2\) times are the APs \(10U-2^{b+2}+3\) with step \(2^{b+3}\)
over odd \(b\); \(b=1\) recovers \(n\equiv 2\pmod{8}\). Do **not**
claim \(d=2\) times are a single AP. Do **not** PREFIX pal-center
tot on a valuation slice. Do **not** claim pal-center tot equals
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

Certify: `python3 research/cycle_tn.py --certify` (~0.15s).
Dump: `research/cycle_tn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/OJ/PB/QV/SO/SV/SX/SY/TD/TE/TK/TL/TM (valuation time
APs for every \(a\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering times of \(v_2(n+1)=a\) are an AP for every \(a\ge 1\))

The Cycle TM time formula does not use that \(a\) is odd:
\(t=10U-2^{a+1}+1-2^{a+2}\ell\). Even \(a\ge 2\) is odd \(d=2\);
\(a=2\) is the \(n\equiv 3\pmod{8}\) 16-AP. Status: **lemma**.
Algebra through \(k\le 64\); set equality through \(k\le 12\).

## Lemma (even \(d=2\) covering times are odd-\(b\) APs)

\(n=2^{b+1}-2+2^{b+2}\ell\) has covering time
\(t=10U-2^{b+2}+3-2^{b+3}\ell\). Over odd \(b\) these APs exhaust
even \(d=2\). The \(b=1\) slice is Cycle TK's \(n\equiv 2\pmod{8}\)
16-AP. Status: **lemma**. Algebra through \(k\le 64\); set equality
through \(k\le 12\). **Killed:** \(d=2\) times are a single AP.

## Verdict

`LEMMA` (covering times of every \(v_2(n+1)=a\) class are an AP;
even \(a\ge 2\) is odd \(d=2\); even \(d=2\) times are odd-\(b\)
APs; \(b=1\) is the \(n\equiv 2\pmod{8}\) 16-AP).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=2\) times are a single AP; \(d=1\) times are a single
AP; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tn.md` (this note)
- `research/cycle_tn.py`
- `research/cycle_tn.json`
