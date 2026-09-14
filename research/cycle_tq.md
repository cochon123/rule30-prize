# Cycle TQ: \(d=2\) pal-pair rest tot equals raw tot for all \(k\)

Even \(d=2\) pal-pairs never meet a forced column. Odd \(d=2\) meets
forced pal-right only at \(k=2\): \(n=11\) at \(p=14\), and \(n=15\)
at \(p=6\) and \(p=14\). Those three ANDs xor to 0, so odd \(d=2\)
rest tot equals raw tot too. Hence \(d=2\) rest tot equals raw tot
for all \(k\). Do **not** claim odd \(d=2\) never forced for all
\(k\). Do **not** claim \(d=2\) rest equals raw cellwise. Do **not**
PREFIX pal-center tot. Do **not** claim pal-center tot equals
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

Certify: `python3 research/cycle_tq.py --certify` (~0.14s).
Dump: `research/cycle_tq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/OJ/PB/QV/SO/SS/SV/SX/SY/TA/TE/TL/TP (\(d=2\) rest
equals raw; no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (even \(d=2\) never forced)

For \(k\ge 1\) the only even forced pal-right is \(j=5U-2\). Even
\(d=2\) sides \(n\pm 2\) hit that column iff \(n=5U-4\), covering
only at \(k=1\) where \(n=6\) has \(v_2(\lfloor n/2\rfloor+1)\)
even, so not \(d=2\). Cycle SV's unique even forced cell
\(n=3U-2\) is pal-distance \(2U\), not \(d=2\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 12\).

## Lemma (odd \(d=2\) forced only at \(k=2\); tot corr \(0\))

Odd covering \(n\) with large-\(j\) side \(n+2\) forced lies in
\(\{5U-5,5U-9\}\). Those are \(d=2\) only at \(k=2\): \(n=15\)
(both sides, \(p=6\) and \(p=14\)) and \(n=11\) (\(p=14\)).
Covering times \(t=9\) and \(t=17\). Packed AND is 1 at
\((t,p)=(9,6)\) and \((17,14)\), and 0 at \((9,14)\), so the tot
corr is \(1\oplus 1\oplus 0=0\). Status: **lemma**. Algebra through
\(k\le 64\); freeze through \(t\le 18\); census through \(k\le 12\).
**Killed:** odd \(d=2\) never forced for all \(k\); \(d=2\) rest
equals raw cellwise.

## Lemma (\(d=2\) rest tot \(=\) raw tot for all \(k\))

Even slice never forced, so rest equals raw cellwise. Odd slice tot
corr vanishes, so odd tot equals raw tot. Status: **lemma**.

## Verdict

`LEMMA` (even \(d=2\) never forced; odd \(d=2\) forced only at
\(k=2\) with tot corr 0; \(d=2\) rest tot equals raw tot for all
\(k\)).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (odd \(d=2\) never forced for all \(k\); \(d=2\) rest equals
raw cellwise; \(d=1\) never forced for all \(k\); \(d=1\) rest equals
raw for all \(k\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tq.md` (this note)
- `research/cycle_tq.py`
- `research/cycle_tq.json`
