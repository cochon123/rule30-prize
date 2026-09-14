# Cycle RP: UNIQUE_EVEN Green \(n\bmod 4\) is \((0,1,1,1)\) for every \(k\ge 6\)

Cycle RN unique Green \(n\bmod 4\) is \((0,1,1,0)\) for \(k\ge 6\).
Cycle RO UNIQUE_ODD Green \(n\bmod 4\) is \((0,0,0,1)\). Their xor is
UNIQUE_EVEN Green \((0,1,1,1)\). Cycle QK UNIQUE_EVEN odd-\(n\) tot
is 0, so \(n\bmod 4=1\) tot equals \(n\bmod 4=3\) tot, 1 iff
\(k\ge 2\) and \(k\ne 4\). Even tot is UNIQUE_EVEN tot, 1 iff
\(k=3\) or \(k\ge 6\). This is **not** that tuple for all \(k\)
(\(k=2\) is \((1,1,1,1)\); \(k=4\) is \((0,0,0,0)\)). **Not**
UNIQUE_EVEN Green \(n\bmod 4\) equals packed UNIQUE_EVEN
\(n\bmod 4\) (packed \(k\ge 6\) is \((1,1,0,0)\)). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_rp.py --certify` (~0.14s).
Dump: `research/cycle_rp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QJ/QK/RA/RK/RM/RN/RO (UNIQUE_EVEN Green
\(n\bmod 4=(0,1,1,1)\) for \(k\ge 6\); n1 tot equals n3 tot, 1 iff
\(k\ge 2\) and \(k\ne 4\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (UNIQUE_EVEN Green \(n\bmod 4\) is \((0,1,1,1)\) for \(k\ge 6\))

UNIQUE_EVEN Green \(n\bmod 4=1\) tot equals \(n\bmod 4=3\) tot
(QK odd-\(n\) tot 0), 1 iff \(k\ge 2\) and \(k\ne 4\). Status:
**lemma**. **Killed:** that tuple for all \(k\). **Killed:**
UNIQUE_EVEN Green \(n\bmod 4\) equals packed UNIQUE_EVEN
\(n\bmod 4\).

## Verdict

`LEMMA` (UNIQUE_EVEN Green \(n\bmod 4\) is \((0,1,1,1)\) for every
\(k\ge 6\); n1 tot equals n3 tot, 1 iff \(k\ge 2\) and \(k\ne 4\);
RN unique \((0,1,1,0)\) xor RO UNIQUE_ODD \((0,0,0,1)\); QK odd-\(n\)
tot 0).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (UNIQUE_EVEN Green \(n\bmod 4=(0,1,1,1)\) for all \(k\);
UNIQUE_EVEN Green \(n\bmod 4\) equals packed UNIQUE_EVEN
\(n\bmod 4\); cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rp.md` (this note)
- `research/cycle_rp.py`
- `research/cycle_rp.json`
