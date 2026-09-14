# Cycle TR: \(\{d=1,d=2\}\) count is \(J_{k+3}\); complex rest tot is raw xor \(1_{k\le 1}\)

The TG complex of pal-distances 1 and 2 has count
\(J_{k+2}+2J_{k+1}=J_{k+3}\). Forced corr of the complex is
\(1_{k\le 1}\) (Cycle TP on \(d=1\), Cycle TQ on \(d=2\)), so
complex rest tot equals complex raw tot xor \(1_{k\le 1}\). Do
**not** claim \(d=2\) raw tot 2-folds parent \(d=1\) raw tot (dies
at \(k=9\)). Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not**
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

Certify: `python3 research/cycle_tr.py --certify` (~0.17s).
Dump: `research/cycle_tr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/OJ/PB/QV/SO/SS/SU/SV/SX/SY/TB/TD/TE/TP/TQ (complex
count and rest tot; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(\{d=1,d=2\}\) count is \(J_{k+3}\))

\(J_{k+3}=2^{k+1}+J_{k+1}=J_{k+2}+2J_{k+1}\). The right-hand side is
the Cycle TD \(d=1\) count plus the Cycle TE \(d=2\) count. Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 12\).

## Lemma (complex rest tot \(=\) raw tot xor \(1_{k\le 1}\))

Cycle TP: \(d=1\) forced corr is \(1_{k\le 1}\). Cycle TQ: \(d=2\)
forced corr is 0. The TG complex forced corr is therefore
\(1_{k\le 1}\), and pal-pair rest xor raw is the XOR of AND on
forced sides. For \(k\ge 2\) the complex is rest \(=\) raw as a tot.
Status: **lemma**. Algebra through \(k\le 64\).

## Verdict

`LEMMA` (\(\{d=1,d=2\}\) count is \(J_{k+3}\); complex rest tot
equals raw tot xor \(1_{k\le 1}\); for \(k\ge 2\) the complex tot is
raw).
`CERTIFIED` (census through \(k\le 12\); spat 2-fold kill through
\(k\le 10\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=2\) raw tot equals parent \(d=1\) raw tot; \(d=2\) raw
tot equals parent \(d=1\) xor \(1\) on even \(k\), dies at \(k=9\);
\(d=1\) never forced for all \(k\); pal-center tot equals
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

- `research/cycle_tr.md` (this note)
- `research/cycle_tr.py`
- `research/cycle_tr.json`
