# Cycle RK: UNIQUE_ODD Green xor on even \(n\) is 0 for every \(k\)

Cycle QK UNIQUE_EVEN odd-\(n\) Green tot vanishes. Dual: UNIQUE_ODD
has \(p\bmod 4=2\), so for \(k\ge 2\) covering \(j\) is odd and
\(G(\mathrm{even},\mathrm{odd})=0\), hence even-\(n\) tot is 0 per
column. At \(k=0,1\) every UNIQUE_ODD packed \(p\) exceeds \(T=10U\)
and is clipped. Unique Green even-\(n\) tot is therefore
UNIQUE_EVEN tot, and unique Green odd-\(n\) tot is UNIQUE_ODD tot.
This is **not** UNIQUE_ODD Green \(n\bmod 4=(0,0,0,1)\) for all \(k\)
(\(k=5\) lives on \(n\bmod 4=1\)). **Not** unique Green \(n\bmod 4\)
equals packed unique \(n\bmod 4\). This is **not** rest \(=S\oplus T\).
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

Certify: `python3 research/cycle_rk.py --certify`.
Dump: `research/cycle_rk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QG/QJ/QK/QV/RB/RJ (UNIQUE_ODD Green even-\(n\) tot 0;
unique Green \(n\)-parity equals QJ \(p\)-parity tots; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (UNIQUE_ODD Green xor on even \(n\) is 0)

For \(k\ge 2\), covering \(j\) at UNIQUE_ODD is odd, so
\(G(2m,2r+1)=0\). At \(k=0,1\) the columns are clipped. Unique
Green even-\(n\) tot equals UNIQUE_EVEN tot. Status: **lemma**.
**Killed:** UNIQUE_ODD Green \(n\bmod 4=(0,0,0,1)\) for all \(k\).
**Killed:** unique Green \(n\bmod 4\) equals packed unique \(n\bmod 4\).

## Verdict

`LEMMA` (UNIQUE_ODD Green xor on even \(n\) is 0 for every \(k\);
unique Green even-\(n\) tot equals UNIQUE_EVEN tot; QK UNIQUE_EVEN
odd-\(n\) tot 0; QJ \(p\)-parity tots).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (UNIQUE_ODD Green \(n\bmod 4=(0,0,0,1)\) for all \(k\);
unique Green \(n\bmod 4\) equals packed unique \(n\bmod 4\);
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

- `research/cycle_rk.md` (this note)
- `research/cycle_rk.py`
- `research/cycle_rk.json`
