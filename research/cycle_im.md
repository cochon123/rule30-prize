# Cycle IM: even \(n\) has no Green \(11\); every run-3 lifts from \(00100\)

The 5-windows that trinomial-lift to \(111\) are
`LIFT3` \(=\{00100,01001,10010,11111\}\). Only \(00100\) is
freshman-sat (even \(n\), even \(j\)). Every run-3 of \(G\) (\(n<64\))
lifts from \(00100\). Even \(n\) has **no** consecutive ones, so
covering \(G=1\) pairs are all odd \(n\). Even \(n\) **does** have
isolated ones. Run-3 is **not** from \(11111\). Even \(n\) is **not**
1-free. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: even-\(n\) no \(11\) still leaves packed AND on
odd-\(n\) Green pairs and triples, so covering never-fail stays open.

Helper: `g5`, `LIFT3`, `lift3_extend_sat`. Certify:
`python3 research/cycle_im.py --certify` (~0.14s).
Dump: `research/cycle_im.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IL (\(n<64\) plus \(16\)-row; covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (even \(n\) has no consecutive Green ones)

For \(n<64\) even, \(G(n,j)=G(n,j+1)=1\) never occurs. Consecutive
\(G=1\) pairs \(512\) are all odd \(n\).

## Lemma (every run-3 lifts from \(00100\))

Of \(16\) `LIFT3` \(\times\) parity cases, only \(00100\) on even
\(n\), even \(j\) is freshman-sat. Every run-3 for \(1\le n<64\)
has `g5(n-1, j-2)==00100`. Census \(n_{\mathrm{run3}}=141\).

## Lemma (covering \(G=1\) pairs are odd \(n\))

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\), all odd \(n\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Even \(n\) has a Green \(11\): at \(k=0\), \(s=5\), \(n=2\),
\(G(2)=10101\), positions \(0,1\) are \(10\), \(p=10\). Run-3 lifts
from \(11111\): at \(k=0\), \(s=3\), \(n=1\), five \(00100\), \(p=6\).
Even \(n\) has no Green ones: at \(k=0\), \(s=5\), \(n=2\), \(j=2\),
\(G(2,2)=1\), \(p=6\).

## Verdict

`LEMMA` (even \(n\) has no consecutive Green ones; every run-3 lifts
from \(00100\); covering \(G=1\) pairs are odd \(n\)).
`KILLED` (even \(n\) has a Green \(11\); run-3 lifts from \(11111\);
even \(n\) has no Green ones).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_im.md` (this note)
- `research/cycle_im.py`
- `research/cycle_im.json`
