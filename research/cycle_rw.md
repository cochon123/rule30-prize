# Cycle RW: covering Green \(G=1\) on \(n\bmod 4=0\) equals parent even \(G=1\)

Cycle QV even-\(n\) \(G=1\) at \(k\) is the 2-fold of all clipped
\(G=1\) at \(k-1\), split n0 from even parent and n2 from odd
parent. Cycle QX n0 \(G=1\) is clip xor at \(k-2\), which equals
even-\(n\) \(G=1\) at \(k-1\). Cycle QX n2 \(G=1\) is odd-\(n\)
\(G=1\) at \(k-1\). So \(G=1\) folds on even children: n0 \(G=1\)
equals parent even \(G=1\) and n2 \(G=1\) equals parent odd \(G=1\)
for every \(k\ge 1\) (the even-child dual of Cycle QY). Green rest
is \(G=1\) xor forced, so Cycle RS rest xor equals Cycle RV forced
xor. This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for
all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_rw.py --certify` (~0.13s).
Dump: `research/cycle_rw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QH/QW/QX/QY/QV/RS/RV (Green n0 \(G=1\) equals parent even
\(G=1\); Green n2 \(G=1\) equals parent odd \(G=1\); RS rest xor
equals RV forced xor; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (Green n0 \(G=1\) equals parent even \(G=1\))

Green n2 \(G=1\) equals parent odd \(G=1\) for every \(k\ge 1\).
Cycle RS rest xor equals Cycle RV forced xor. Status: **lemma**.
**Killed:** Green n0 \(G=1\) equals parent odd \(G=1\). **Killed:**
Green n2 \(G=1\) equals parent even \(G=1\).

## Verdict

`LEMMA` (Green \(G=1\) on \(n\bmod 4=0\) equals parent even \(G=1\);
Green \(G=1\) on \(n\bmod 4=2\) equals parent odd \(G=1\); Cycle RS
rest xor equals Cycle RV forced xor; QV/QX/QY closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green n0 \(G=1\) equals parent odd \(G=1\); Green n2
\(G=1\) equals parent even \(G=1\); cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rw.md` (this note)
- `research/cycle_rw.py`
- `research/cycle_rw.json`
