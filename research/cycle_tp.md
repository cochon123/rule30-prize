# Cycle TP: \(d=1\) pal-pairs meet a forced column at two cells

\(d=1\) pal-pairs have sides \(j=n-1\) and \(j=n+1\). Forced pal-right
is \(j\in\{5U-2,5U-3,5U-7\}\) (packed \(p\in\{4,6,14\}\)). The
large-\(j\) side \(j=n+1\) hits a forced column iff
\((k,n)=(0,1)\) at \(p=6\) or \((1,7)\) at \(p=4\). The small-\(j\)
side never hits. Both cells fire packed AND, so \(d=1\) rest tot
equals \(d=1\) raw tot xor \(1_{k\le 1}\). For \(k\ge 2\) the slice
is never forced. Do **not** claim \(d=1\) never forced for all \(k\).
Do **not** claim \(d=1\) rest equals raw for all \(k\). Do **not**
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

Certify: `python3 research/cycle_tp.py --certify`.
Dump: `research/cycle_tp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/OJ/PB/QV/SO/SS/SV/SX/SY/TA/TD/TL/TO (\(d=1\) forced
cells; no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (\(d=1\) meets forced pal-right at two cells)

Forced pal-right \(j=5U-2,5U-3,5U-7\). The \(d=1\) large-\(j\) side
is \(j=n+1\), so covering \(n\in\{5U-3,5U-4,5U-8\}\). Among those,
\(v_2(n+1)\) is odd only for \((k,n)=(0,1)\) and \((1,7)\). The
small-\(j\) side \(j=n-1\) never meets a forced column. Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 12\).
**Killed:** \(d=1\) never forced for all \(k\).

## Lemma (\(d=1\) rest tot \(=\) raw tot xor \(1_{k\le 1}\))

Covering times are \(t=7\) at \((0,1)\) and \(t=5\) at \((1,7)\).
Packed AND at \(p=6\) on odd \(t\ge 3\) is 1 (Cycle SW); packed AND
at \(p=4\) on odd \(t\ge 3\) is 1 (Cycle SV). Pal-pair rest xor raw
is the XOR of AND on forced sides, so the \(d=1\) tot picks up
exactly those two 1s. For \(k\ge 2\) the slice is never forced, and
this is the \(d=1\) case of Cycle SY's odd-pair tot for \(k\ge 3\).
Status: **lemma**. Algebra through \(k\le 64\); freeze through
\(t\le 16\). **Killed:** \(d=1\) rest equals raw for all \(k\).

## Verdict

`LEMMA` (\(d=1\) meets a forced column iff \((k,n)=(0,1)\) at \(p=6\)
or \((1,7)\) at \(p=4\); \(d=1\) rest tot equals raw tot xor
\(1_{k\le 1}\); for \(k\ge 2\) the slice is never forced).
`CERTIFIED` (census through \(k\le 12\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=1\) never forced for all \(k\); \(d=1\) rest equals
raw for all \(k\); even children of \(d=1\) stay \(d=1\);
\(d=1\)/\(d=2\) times are a single AP; pal-center tot equals
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

- `research/cycle_tp.md` (this note)
- `research/cycle_tp.py`
- `research/cycle_tp.json`
