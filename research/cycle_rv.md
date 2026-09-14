# Cycle RV: covering Green forced \(n\bmod 4\) is \((0,1,1,1)\) except \(k=1,2\)

Green rest is clipped \(G=1\) xor forced. Cycle QY \(G=1\) on
\(n\bmod 4=1\) at \(k\) equals even-\(n\) \(G=1\) at \(k-1\), so
Cycle RU's n1 rest equals parent even rest iff forced n1 tot equals
parent even forced tot. Forced n1 tot is \(1\) for every \(k\), and
parent even forced tot is \(1\) for every \(k\ge 0\), so they agree.
Dual: forced n3 tot is \(1\) iff \(k\notin\{1,2\}\); xor parent odd
forced tot is \(1\) iff \(k=2\) or \(k\ge 4\), the same bit as
Cycle RU's n3 rest xor. Forced \(n\bmod 4\) is \((0,1,1,1)\) at
\(k=0\) and every \(k\ge 3\), but \((1,1,0,0)\) at \(k=1\) and
\((0,1,1,0)\) at \(k=2\). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_rv.py --certify`.
Dump: `research/cycle_rv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QX/QY/RU (Green forced n1 tot is \(1\) for every \(k\);
equals parent even forced tot; Green forced n3 tot xor parent odd
forced tot is 1 iff \(k=2\) or \(k\ge 4\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (Green forced n1 tot is \(1\) for every \(k\))

Green forced n1 tot equals parent even forced tot. Green forced n3
tot xor parent odd forced tot is 1 iff \(k=2\) or \(k\ge 4\).
Forced \(n\bmod 4\) is \((0,1,1,1)\) except \(k=1,2\). Status:
**lemma**. **Killed:** Green forced \(n\bmod 4\) is \((0,1,1,1)\)
for all \(k\). **Killed:** Green forced n3 tot equals parent odd
forced tot.

## Verdict

`LEMMA` (Green forced xor on \(n\bmod 4=1\) is \(1\) for every
\(k\); equals parent even forced tot; Green forced xor on
\(n\bmod 4=3\) xor parent odd forced tot is 1 iff \(k=2\) or
\(k\ge 4\); QX/QY/RU closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green forced \(n\bmod 4\) is \((0,1,1,1)\) for all \(k\);
Green forced n3 tot equals parent odd forced tot; cellwise 2-fold
packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rv.md` (this note)
- `research/cycle_rv.py`
- `research/cycle_rv.json`
