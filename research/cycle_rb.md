# Cycle RB: covering UNIQUE_REST packed AND xor on \(n\equiv 2\pmod{4}\) is \(0\) for every \(k\)

UNIQUE_EVEN \(n\bmod 4\) xor UNIQUE_ODD \(n\bmod 4\) is unique packed
tot by \(n\bmod 4\). Cycle RA \(n\equiv 2\) tot is \(0\) and Cycle QR
UNIQUE_ODD even tot is \(0\), so unique \(n\equiv 2\) tot is \(0\).
Unique \(n\equiv 0\) tot equals UNIQUE_EVEN even tot (\(1\) iff
\(k=3\) or \(k\ge 5\)). Unique \(n\equiv 1\) tot equals unique even
packed tot (\(1\) iff \(k\in\{3,4,5\}\)). Unique \(n\equiv 3\) tot
equals UNIQUE_EVEN odd tot (\(1\) iff \(k=4\) or \(k\ge 6\)). They
xor to Cycle QF unique packed tot \(0\). This is **not** unique
\(n\equiv 0\) tot equals unique even packed tot (\(k=4\): \(0\) vs
\(1\)). **Not** unique \(n\equiv 3\) tot equals unique odd packed tot
(\(k=6\): \(1\) vs \(0\)). This is **not** rest \(=S\oplus T\).
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
Do **not** claim Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\).
Do **not** claim unique \(n\equiv 0\) tot equals unique even packed
tot. Do **not** claim unique \(n\equiv 3\) tot equals unique odd
packed tot. Do **not** claim leftover \(n\bmod 4\) has a small
period. Do **not** claim cellwise 2-fold packed AND. Do **not**
claim even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\).

Certify: `python3 research/cycle_rb.py --certify` (~0.14s).
Dump: `research/cycle_rb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QP/QS/QZ/RA (unique \(n\bmod 4\) from RA xor QZ dumps;
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (UNIQUE_REST packed AND xor on \(n\equiv 2\pmod{4}\) is \(0\) for every \(k\))

UNIQUE_EVEN and UNIQUE_ODD both vanish on \(n\equiv 2\). Unique
\(n\equiv 0\) tot equals UNIQUE_EVEN even tot, unique \(n\equiv 1\)
tot equals unique even packed tot, and unique \(n\equiv 3\) tot
equals UNIQUE_EVEN odd tot. Status: **lemma**. **Killed:** unique
\(n\equiv 0\) tot equals unique even packed tot. **Killed:** unique
\(n\equiv 3\) tot equals unique odd packed tot.

## Verdict

`LEMMA` (UNIQUE_REST packed xor on \(n\equiv 2\pmod{4}\) is \(0\) for
every \(k\); on \(n\equiv 0\) is \(1\) iff \(k=3\) or \(k\ge 5\); on
\(n\equiv 1\) is \(1\) iff \(k\in\{3,4,5\}\); on \(n\equiv 3\) is
\(1\) iff \(k=4\) or \(k\ge 6\); RA UNIQUE_EVEN \(n\bmod 4\); QZ
UNIQUE_ODD \(n\equiv 3\) tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (unique \(n\equiv 0\) tot equals unique even packed tot;
unique \(n\equiv 3\) tot equals unique odd packed tot; Green rest
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

- `research/cycle_rb.md` (this note)
- `research/cycle_rb.py`
- `research/cycle_rb.json`
