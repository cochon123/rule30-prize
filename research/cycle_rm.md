# Cycle RM: leftover Green \(n\bmod 4\) is \((0,0,0,1)\) for every \(k\ge 6\)

Cycle RL leftover even-\(n\) tot is 0 for \(k\ge 6\) and odd-\(n\)
tot is 1. Leftover Green \(n\bmod 4=3\) tot is 1 iff \(k\le 1\) or
\(k\ge 6\) (Green \(n\bmod 4=3\) tot 1 xor unique Green \(n\bmod 4=3\)
tot, the latter 1 iff \(2\le k\le 5\)). Hence for \(k\ge 6\) the
tuple is \((0,0,0,1)\): leftover Green lives only on \(n\bmod 4=3\).
This is **not** that tuple for all \(k\) (\(k=0\) is \((1,0,0,1)\)).
**Not** leftover \(n\bmod 4=3\) tot equals packed leftover
\(n\bmod 4=3\) (\(k=0\) and \(k=9\)). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_rm.py --certify`.
Dump: `research/cycle_rm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/MD/QG/QJ/QX/RB/RL (leftover Green \(n\bmod 4=(0,0,0,1)\)
for \(k\ge 6\); leftover \(n\bmod 4=3\) tot \(1\) iff \(k\le 1\) or
\(k\ge 6\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (leftover Green \(n\bmod 4\) is \((0,0,0,1)\) for \(k\ge 6\))

Leftover \(n\bmod 4=3\) tot is 1 iff \(k\le 1\) or \(k\ge 6\). Status:
**lemma**. **Killed:** that tuple for all \(k\). **Killed:** leftover
Green \(n\bmod 4=3\) equals packed leftover \(n\bmod 4=3\).

## Verdict

`LEMMA` (leftover Green \(n\bmod 4\) is \((0,0,0,1)\) for every
\(k\ge 6\); leftover Green \(n\bmod 4=3\) tot is 1 iff \(k\le 1\) or
\(k\ge 6\); unique Green \(n\bmod 4=3\) tot is 1 iff \(2\le k\le 5\);
RL even/odd leftover Green).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover Green \(n\bmod 4=(0,0,0,1)\) for all \(k\);
leftover Green \(n\bmod 4=3\) equals packed leftover \(n\bmod 4=3\);
cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rm.md` (this note)
- `research/cycle_rm.py`
- `research/cycle_rm.json`
