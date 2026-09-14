# Cycle RC: covering leftover \(n\equiv 2\pmod{4}\) tot equals rest \(n\equiv 2\pmod{4}\) tot for every \(k\)

UNIQUE_REST packed tot on \(n\equiv 2\pmod{4}\) is \(0\) (Cycle RB),
so the rest/unique partition on that residue is leftover \(n\equiv 2\)
tot \(=\) rest \(n\equiv 2\) tot. Leftover \(n\equiv 0\) tot is rest
\(n\equiv 0\) xor unique \(n\equiv 0\), matching Cycle QO's `lo_n0`
through \(k\le 10\). Leftover even-\(n\) tot is leftover \(n\equiv 0\)
xor leftover \(n\equiv 2\), equal to Cycle QT. This is **not** leftover
\(n\equiv 2\) tot equals \(S\oplus T\) (\(k=0\): \(1\) vs \(0\)).
**Not** leftover \(n\equiv 2\) tot equals leftover even-\(n\) tot
(\(k=3\): \(0\) vs \(1\)). This is **not** rest \(=S\oplus T\).
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
Do **not** claim leftover \(n\equiv 2\) tot equals \(S\oplus T\).
Do **not** claim leftover \(n\equiv 2\) tot equals leftover even-\(n\)
tot. Do **not** claim leftover \(n\bmod 4\) has a small period. Do
**not** claim cellwise 2-fold packed AND. Do **not** claim even-\(n\)
rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\).

Certify: `python3 research/cycle_rc.py --certify` (~0.14s).
Dump: `research/cycle_rc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PB/QO/QT/RB (leftover \(n\bmod 4\) from QO rest xor RB
unique; no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (leftover \(n\equiv 2\pmod{4}\) tot equals rest \(n\equiv 2\pmod{4}\) tot)

UNIQUE_REST vanishes on \(n\equiv 2\). Leftover \(n\bmod 4\) is rest
xor unique on each residue. Status: **lemma**. **Killed:** leftover
\(n\equiv 2\) tot equals \(S\oplus T\). **Killed:** leftover
\(n\equiv 2\) tot equals leftover even-\(n\) tot.

## Verdict

`LEMMA` (leftover \(n\equiv 2\pmod{4}\) tot equals rest \(n\equiv 2\)
tot for every \(k\); leftover \(n\bmod 4\) equals rest xor unique;
RB unique \(n\equiv 2\) tot \(0\); QT leftover even-\(n\) tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover \(n\equiv 2\) tot equals \(S\oplus T\); leftover
\(n\equiv 2\) tot equals leftover even-\(n\) tot; packed rest on
\(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at \(k-2\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rc.md` (this note)
- `research/cycle_rc.py`
- `research/cycle_rc.json`
