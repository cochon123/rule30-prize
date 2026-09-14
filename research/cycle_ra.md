# Cycle RA: covering UNIQUE_EVEN packed AND xor on \(n\equiv 2\pmod{4}\) is \(0\) for every \(k\)

Cycle QQ freeze for \(k\ge 6\) has \(n\equiv 0\pmod{4}\) tot \(1\) and
\(n\equiv 2\pmod{4}\) tot \(0\), so even tot equals \(n\equiv 0\) tot.
Packed covering \(k\le 8\) has \(n\equiv 2\) tot \(0\) at every \(k\),
including \(k=3,5\) where even tot is \(1\). Hence \(n\equiv 0\) tot
equals Cycle QS even tot (\(1\) iff \(k=3\) or \(k\ge 5\)). Odd freeze
helpers all require \(n\equiv 1\pmod{4}\), so for \(k\ge 6\)
\(n\equiv 1\) tot is \(1\) and \(n\equiv 3\) tot is \(0\). Packed
\(k\le 8\) matches \(n\equiv 1\) tot \(1\) iff \(k\ge 2\) and
\(n\equiv 3\) tot \(1\) iff \(k\in\{2,3,5\}\). They xor to Cycle QS
odd tot. This is **not** \(n\equiv 3\) tot equals odd tot (\(k=2\):
\(1\) vs \(0\)). **Not** \(n\equiv 2\) tot equals even tot (\(k=3\):
\(0\) vs \(1\)). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
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
Do **not** claim UNIQUE_EVEN \(n\equiv 3\) tot equals unique even
odd-\(n\) tot. Do **not** claim UNIQUE_EVEN \(n\equiv 2\) tot equals
unique even even-\(n\) tot. Do **not** claim cellwise 2-fold packed
AND. Do **not** claim even-\(n\) rest xor at \(k\) equals odd-\(n\)
rest xor at \(k-1\) for all \(k\).

Certify: `python3 research/cycle_ra.py --certify` (~0.18s).
Dump: `research/cycle_ra.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PH/PK/PW/PX/PY/PZ/QB/QJ/QP/QS/QQ/QZ (UNIQUE_EVEN
\(n\bmod 4\) via freeze doubling \(k\ge 6\) and packed covering
\(k\le 8\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (UNIQUE_EVEN packed AND xor on \(n\equiv 2\pmod{4}\) is \(0\) for every \(k\))

Freeze AND on \(k\ge 6\) has \(n\equiv 2\) tot \(0\). Packed covering
on \(k\le 8\) has the same bit \(0\). Hence \(n\equiv 0\) tot equals
even tot, \(n\equiv 1\) tot is \(1\) iff \(k\ge 2\), and
\(n\equiv 3\) tot is \(1\) iff \(k\in\{2,3,5\}\). Status: **lemma**.
**Killed:** UNIQUE_EVEN \(n\equiv 3\) tot equals unique even odd-\(n\)
tot. **Killed:** UNIQUE_EVEN \(n\equiv 2\) tot equals unique even
even-\(n\) tot.

## Verdict

`LEMMA` (UNIQUE_EVEN packed xor on \(n\equiv 2\pmod{4}\) is \(0\) for
every \(k\); on \(n\equiv 0\) is \(1\) iff \(k=3\) or \(k\ge 5\); on
\(n\equiv 1\) is \(1\) iff \(k\ge 2\); on \(n\equiv 3\) is \(1\) iff
\(k\in\{2,3,5\}\); QS even/odd tots; QZ UNIQUE_ODD \(n\equiv 3\) tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (UNIQUE_EVEN \(n\equiv 3\) tot equals unique even odd-\(n\)
tot; UNIQUE_EVEN \(n\equiv 2\) tot equals unique even even-\(n\) tot;
Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ra.md` (this note)
- `research/cycle_ra.py`
- `research/cycle_ra.json`
