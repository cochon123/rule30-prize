# Cycle RY: even-child green4 is \((0,G(m,r),G(m,r),G(m,r))\) at even \(j\)

Cycle HJ \(\mathrm{green4}(n,j)=(G(n,j+1),G(n,j+1)\oplus G(n,j),G(n,j),
G(n,j)\oplus G(n,j-1))\) is the even-\(s\) Green 4-tuple at packed
\(p-3\ldots p\). Cycle QV \(G(2m,2r)=G(m,r)\) and
\(G(2m,\mathrm{odd})=0\), so at even child \(n=2m\) and even
\(j=2r\) that 4-tuple equals \((0,G(m,r),G(m,r),G(m,r))\). On
\(G=1\) it is \((0,1,1,1)\), never in AND_ONES. At odd \(j=2r+1\)
it equals \((G(m,r+1),G(m,r+1),0,G(m,r))\), also never in
AND_ONES, so Green AND is dead on every even-child cell. Packed
AND at consecutive-\(p\) can still fire (Cycle QV mismatch).
Cycle RX consecutive Green is \((0,G(m,r+1),0,G(m,r))\), **not**
this 4-tuple. This is **not** rest \(=S\oplus T\). **Not**
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
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_ry.py --certify`.
Dump: `research/cycle_ry.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RX (even-child green4 is
\((0,G(m,r),G(m,r),G(m,r))\) at even \(j\); \((0,1,1,1)\) on
\(G=1\); never AND on even children; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even-child green4)

At \(n=2m\), \(j=2r\), \(\mathrm{green4}=(0,G(m,r),G(m,r),G(m,r))\).
On \(G=1\) that 4-tuple is \((0,1,1,1)\), never in AND_ONES. At
odd \(j=2r+1\), \(\mathrm{green4}=(G(m,r+1),G(m,r+1),0,G(m,r))\),
also never in AND_ONES. Status: **lemma**. **Killed:** even-child
green4 equals parent green4. **Killed:** even-child green4 equals
Cycle RX consecutive Green.

## Verdict

`LEMMA` (even-child green4 is \((0,G(m,r),G(m,r),G(m,r))\) at even
\(j\); \((0,1,1,1)\) on \(G=1\); never AND on even children;
QV/HJ/HS/RX closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (even-child green4 equals parent green4; even-child
green4 equals Cycle RX consecutive Green; cellwise 2-fold packed
AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ry.md` (this note)
- `research/cycle_ry.py`
- `research/cycle_ry.json`
