# Cycle RX: even-child consecutive Green 4-tuple is \((0,G(m,r+1),0,G(m,r))\)

Cycle QV \(G(2m,2r)=G(m,r)\) and \(G(2m,\mathrm{odd})=0\), so at even
child \(n=2m\) and even \(j=2r\) the consecutive Green bits
\((G(n,j+3),G(n,j+2),G(n,j+1),G(n,j))\) equal
\((0,G(m,r+1),0,G(m,r))\). Cycle HJ's odd-child identity is
\(G(2n+1,2j\ldots 2j+3)=\mathrm{green4}(n,j)\); the even-child
4-tuple is **not** parent green4. On \(G=1\) cells that 4-tuple is
\((0,G(m,r+1),0,1)\), never in AND_ONES, so Green AND is dead on
even-child \(G=1\). Packed AND at the consecutive-\(p\) window can
still fire (Cycle QV mismatch). This is **not** rest \(=S\oplus T\).
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

Certify: `python3 research/cycle_rx.py --certify`.
Dump: `research/cycle_rx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RW (even-child consecutive Green 4-tuple
is \((0,G(m,r+1),0,G(m,r))\); never AND on \(G=1\); no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even-child consecutive Green 4-tuple)

At \(n=2m\), \(j=2r\), consecutive Green bits equal
\((0,G(m,r+1),0,G(m,r))\). On \(G=1\) that 4-tuple is never in
AND_ONES. Status: **lemma**. **Killed:** even-child consecutive
Green 4-tuple equals parent green4. **Killed:** that 4-tuple never
meets AND_ONES (dies off \(G=1\) at \(0100\)).

## Verdict

`LEMMA` (even-child consecutive Green 4-tuple is
\((0,G(m,r+1),0,G(m,r))\); never AND on even-child \(G=1\); QV/HJ/HS
closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (even-child consecutive Green 4-tuple equals parent green4;
that 4-tuple never meets AND_ONES; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rx.md` (this note)
- `research/cycle_rx.py`
- `research/cycle_rx.json`
