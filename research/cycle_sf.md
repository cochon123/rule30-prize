# Cycle SF: odd-child odd-\(j\) consecutive Green is \((g_2\oplus g_1,g_1,g_1\oplus g,g)\)

On \(n=2m+1\), odd \(j=2r+1\), doubling gives consecutive Green
\((G(n,j+3),G(n,j+2),G(n,j+1),G(n,j))\) equal to
\((g_2\oplus g_1,g_1,g_1\oplus g,g)\) with \(g=G(m,r)\),
\(g_1=G(m,r+1)\), and \(g_2=G(m,r+2)\). On \(G=1\) this is Cycle
SD. AND fires iff the 4-tuple is \((0,0,1,1)\), which requires
\(g=1\); off \(G=1\) the form is AND-dead. Cycle SE even-child
odd-\(j\) form is \((g_2,0,g_1,0)\), **not** this 4-tuple. Packed
AND at consecutive-\(p\) can still fire (Cycle QV mismatch). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_sf.py --certify`.
Dump: `research/cycle_sf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RX/SD/SE (odd-child odd-\(j\)
consecutive Green is \((g_2\oplus g_1,g_1,g_1\oplus g,g)\); on
\(G=1\) equals Cycle SD; AND iff \(0011\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-child odd-\(j\) consecutive Green)

At \(n=2m+1\), odd \(j=2r+1\), consecutive Green bits equal
\((g_2\oplus g_1,g_1,g_1\oplus g,g)\). On \(G=1\) this is Cycle
SD. AND fires iff the 4-tuple is \(0011\). Status: **lemma**.
**Killed:** that 4-tuple never meets AND_ONES. **Killed:** it
equals Cycle SD on every cell. **Killed:** it equals Cycle SE
even-child odd-\(j\) consecutive Green. **Killed:** identically
\((0,0,0,0)\).

## Verdict

`LEMMA` (odd-child odd-\(j\) consecutive Green is
\((g_2\oplus g_1,g_1,g_1\oplus g,g)\); on \(G=1\) equals Cycle SD;
AND iff \(0011\); SE/SD closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (never AND; identically SD; equals SE; identically
\((0,0,0,0)\); cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sf.md` (this note)
- `research/cycle_sf.py`
- `research/cycle_sf.json`
