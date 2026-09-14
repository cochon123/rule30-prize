# Cycle QZ: covering UNIQUE_ODD packed AND xor on \(n\equiv 3\pmod{4}\) is \(1\) for \(k\ge 2\)

UNIQUE_ODD lives only on odd \(n\) (Cycle QR even tot \(0\)). Cycle QR
freeze for \(k\ge 6\) has \(n\equiv 1\pmod{4}\) equal to \(p=54\)
(xor \(1\)) and \(n\equiv 3\pmod{4}\) equal to
\(p=42\oplus 58\oplus 98\oplus 106\oplus 114\) (xor \(1\)); silent
\(p=30,38,86\) tot is \(0\). Packed covering \(k\le 8\) matches
\(n\equiv 3\) tot \(1\) iff \(k\ge 2\) and \(n\equiv 1\) tot \(1\)
iff \(k=2\) or \(k\ge 6\), including the \(k=2..5\) gap where freeze
\(n\bmod 4\) labels are not yet packed-AND locations. They xor to
Cycle QP unique odd packed tot. This is **not** \(n\equiv 3\) tot
equals unique odd tot (\(k=2\): \(1\) vs \(0\)). **Not** Green
\(n\equiv 3\) rest equals this bit (\(k=0\): Green \(1\) vs \(0\)).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\).
Do **not** claim UNIQUE_ODD \(n\equiv 3\) tot equals unique odd packed
tot. Do **not** claim Green rest \(n\equiv 3\) equals UNIQUE_ODD
\(n\equiv 3\) tot. Do **not** claim leftover odd-\(n\) tot equals
UNIQUE_ODD \(n\equiv 3\) tot. Do **not** claim cellwise 2-fold packed
AND. Do **not** claim even-\(n\) rest xor at \(k\) equals odd-\(n\)
rest xor at \(k-1\) for all \(k\).

Certify: `python3 research/cycle_qz.py --certify` (~0.17s).
Dump: `research/cycle_qz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PM/PN/PR/PS/PV/QA/QC/QD/QE/QJ/QO/QP/QR/QS/QX (UNIQUE_ODD
\(n\bmod 4\) via freeze doubling \(k\ge 6\) and packed covering
\(k\le 8\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (UNIQUE_ODD packed AND xor on \(n\equiv 3\pmod{4}\) is \(1\) for \(k\ge 2\))

Pack helpers vanish at \(k=0,1\). Packed covering on \(k=2..5\) has
\(n\equiv 3\) tot \(1\). Freeze AND on \(k\ge 6\) has \(n\equiv 3\)
tot \(1\). Status: **lemma**. **Killed:** UNIQUE_ODD \(n\equiv 3\) tot
equals unique odd packed tot. **Killed:** Green rest \(n\equiv 3\)
equals UNIQUE_ODD \(n\equiv 3\) tot. **Killed:** leftover odd-\(n\) tot
equals UNIQUE_ODD \(n\equiv 3\) tot.

## Verdict

`LEMMA` (UNIQUE_ODD packed xor on \(n\equiv 3\pmod{4}\) is \(1\) iff
\(k\ge 2\); on \(n\equiv 1\pmod{4}\) is \(1\) iff \(k=2\) or \(k\ge 6\);
QR UNIQUE_ODD even-\(n\) tot \(0\); QY Green \(n\equiv 3\) rest \(1\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (UNIQUE_ODD \(n\equiv 3\) tot equals unique odd packed tot;
Green rest \(n\equiv 3\) equals UNIQUE_ODD \(n\equiv 3\) tot; leftover
odd-\(n\) tot equals UNIQUE_ODD \(n\equiv 3\) tot; Green rest
\(n\bmod 4\) equals packed rest \(n\bmod 4\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qz.md` (this note)
- `research/cycle_qz.py`
- `research/cycle_qz.json`
