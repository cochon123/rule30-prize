# Cycle RQ: UNIQUE_EVEN Green \(n\bmod 4\) equals Green rest \(n\bmod 4\) for every \(k\ge 6\)

Cycle QX/QY Green rest \(n\bmod 4\) is \((0,1,1,1)\) for \(k\ge 3\).
Cycle RP UNIQUE_EVEN Green \(n\bmod 4\) is \((0,1,1,1)\) for \(k\ge 6\).
Hence they agree for \(k\ge 6\): Green rest on each residue is
UNIQUE_EVEN's profile. Dual: leftover Green \(n\bmod 4\) equals
UNIQUE_ODD Green \(n\bmod 4\), both \((0,0,0,1)\), so leftover and
UNIQUE_ODD cancel on \(n\bmod 4=3\). This is **not** equal for all
\(k\) (\(k=3\): Green \((0,1,1,1)\), UNIQUE_EVEN \((1,1,0,1)\)).
**Not** leftover Green equals UNIQUE_ODD Green for all \(k\). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_rq.py --certify`.
Dump: `research/cycle_rq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QX/QY/RM/RN/RO/RP (UNIQUE_EVEN Green \(n\bmod 4\) equals
Green rest for \(k\ge 6\); leftover Green equals UNIQUE_ODD Green
for \(k\ge 6\); prefixes RP/RO/RM walks rather than re-walking; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (UNIQUE_EVEN Green \(n\bmod 4\) equals Green rest for \(k\ge 6\))

Leftover Green \(n\bmod 4\) equals UNIQUE_ODD Green \(n\bmod 4\) for
\(k\ge 6\). Status: **lemma**. **Killed:** UNIQUE_EVEN Green equals
Green rest for all \(k\). **Killed:** leftover Green equals
UNIQUE_ODD Green for all \(k\).

## Verdict

`LEMMA` (UNIQUE_EVEN Green \(n\bmod 4\) equals Green rest \(n\bmod 4\)
for every \(k\ge 6\); leftover Green equals UNIQUE_ODD Green for
\(k\ge 6\); QX/QY \((0,1,1,1)\) xor RP/RO).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (UNIQUE_EVEN Green equals Green rest for all \(k\);
leftover Green equals UNIQUE_ODD Green for all \(k\); cellwise
2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rq.md` (this note)
- `research/cycle_rq.py`
- `research/cycle_rq.json`
