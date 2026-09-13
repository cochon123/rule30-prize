# Cycle QU: covering even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) through \(k\le 10\)

Cycle QO's 4-fold tot rest on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\)
at \(k-2\) dies at \(k=10\). The 2-fold tot even-\(n\) rest xor at \(k\)
equals parent odd-\(n\) rest xor for every \(1\le k\le 10\), including
\(k=10\). Slicewise \(n\equiv 2\pmod{4}\) tot equals parent odd tot
fails at \(k=2\). Even-\(n\) rest equals parent rest tot / \(S\oplus T\)
at \(k-1\) fails at \(k=1\). Given this tot, rest \(=S\oplus T\) iff
odd-\(n\) rest at \(k\) equals odd-\(n\) rest at \(k-1\) xor \(S\oplus T\)
at \(k\); that is a rewrite, not a packed identity. For \(k\ge 6\)
UNIQUE_EVEN even-\(n\) tot and unique odd-\(n\) tot at \(k-1\) are both
\(1\), so the same tot is leftover even-\(n\) at \(k\) equals leftover
odd-\(n\) at \(k-1\). This is **not** rest \(=S\oplus T\) for all \(k\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\). Do **not** walk \(k=11\) covering packed. Do **not** walk
\(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim packed rest on \(n\equiv 0\pmod{4}\) equals
\(S\oplus T\) at \(k-2\). Do **not** claim even-\(n\) rest equals
parent rest tot. Do **not** claim cellwise 2-fold packed AND.

Certify: `python3 research/cycle_qu.py --certify` (~0.14s).
Dump: `research/cycle_qu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/QO/QR/QS/QT (even-\(n\) rest tot vs parent odd-\(n\)
rest tot from QO \(k\le 10\); leftover fold from QT \(k=6..8\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Certificate (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) through \(k\le 10\))

Holds at \(k=10\), where Cycle QO's 4-fold \(n\equiv 0\) tot dies.
Leftover even-\(n\) tot at \(k\) equals leftover odd-\(n\) tot at
\(k-1\) for \(k=6,7,8\). Status: **certified** \(k\le 10\). Closed
unique cancellation on \(k\le 64\). **Killed:** even-\(n\) rest
equals \(S\oplus T\) at \(k-1\). **Killed:** \(n\equiv 2\pmod{4}\)
tot equals parent odd tot.

## Verdict

`CERTIFIED` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for \(1\le k\le 10\); leftover even-\(n\) tot at \(k\) equals
leftover odd-\(n\) tot at \(k-1\) for \(k=6,7,8\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (even-\(n\) rest equals \(S\oplus T\) at \(k-1\);
\(n\equiv 2\pmod{4}\) tot equals parent odd tot; packed rest on
\(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at \(k-2\); leftover
even-\(n\) tot equals even rest; leftover even-\(n\) tot equals
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

- `research/cycle_qu.md` (this note)
- `research/cycle_qu.py`
- `research/cycle_qu.json`
