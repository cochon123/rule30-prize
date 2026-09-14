# Cycle SD: odd-child \(G=1\) odd-\(j\) consecutive Green is \((g_2\oplus g_1,g_1,g_1\oplus 1,1)\)

On \(n=2m+1\), odd \(j=2r+1\), \(G=1\), doubling gives
\(G(m,r)=1\) and consecutive Green
\((G(n,j+3),G(n,j+2),G(n,j+1),G(n,j))\) equals
\((g_2\oplus g_1,g_1,g_1\oplus 1,1)\) with \(g_1=G(m,r+1)\) and
\(g_2=G(m,r+2)\): one of \((1,0,1,1)\), \((0,0,1,1)\),
\((1,1,0,1)\), \((0,1,0,1)\). The type \((0,0,1,1)\) is in
AND_ONES (\(g_1=g_2=0\)). Cycle SB odd-\(j\) green4 is never AND,
so consecutive AND does **not** imply green4 / packed-slot AND.
Cycle SC even-\(j\) consecutive is **not** this 4-tuple. Type
counts are **not** equal. Packed AND at consecutive-\(p\) can
still fire (Cycle QV mismatch). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover
\(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_sd.py --certify`.
Dump: `research/cycle_sd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RX/SB/SC (odd-child \(G=1\) odd-\(j\)
consecutive Green is \((g_2\oplus g_1,g_1,g_1\oplus 1,1)\); meets
AND_ONES at \(0011\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-child \(G=1\) odd-\(j\) consecutive Green)

At \(n=2m+1\), odd \(j=2r+1\), \(G=1\),
\(\mathrm{cons\_g4}=(g_2\oplus g_1,g_1,g_1\oplus 1,1)\) with
\(g_1=G(m,r+1)\) and \(g_2=G(m,r+2)\). AND fires iff the 4-tuple
is \(0011\). Status: **lemma**. **Killed:** that 4-tuple never
meets AND_ONES. **Killed:** identically one of the four values.
**Killed:** it equals Cycle SB green4. **Killed:** it equals
Cycle SC consecutive Green. **Killed:** the four type counts are
equal. **Killed:** consecutive AND implies green4 AND.

## Verdict

`LEMMA` (odd-child \(G=1\) odd-\(j\) consecutive Green is
\((g_2\oplus g_1,g_1,g_1\oplus 1,1)\); meets AND_ONES iff
\(0011\); SB/SC closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (never AND; identically one tuple; equals SB green4;
equals SC consecutive; type counts equal; consecutive AND implies
green4 AND; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sd.md` (this note)
- `research/cycle_sd.py`
- `research/cycle_sd.json`
