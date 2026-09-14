# Cycle RZ: odd-child green4 at even \(j\) is \((G(m,r),G(m,r-1),G(m,r)\oplus G(m,r-1),G(m,r))\)

Cycle HJ \(\mathrm{green4}\) is the even-\(s\) Green 4-tuple at packed
\(p-3\ldots p\), and odd-child consecutive Green equals parent
green4. Cycle QV \(G(2m+1,2k)=G(m,k)\oplus G(m,k-1)\) and
\(G(2m+1,2k+1)=G(m,k)\), so at odd child \(n=2m+1\) and even
\(j=2r\) that packed-slot 4-tuple equals
\((G(m,r),G(m,r-1),G(m,r)\oplus G(m,r-1),G(m,r))\). At odd
\(j=2r+1\) it equals
\((G(m,r+1)\oplus G(m,r),G(m,r+1),G(m,r),G(m,r-1))\). Both are
never in AND_ONES (Cycle HS). This is **not** parent green4 and
**not** Cycle RY even-child green4. Together with HJ/RX/RY this
closes even/odd child times consecutive Green / green4. Packed
AND at consecutive-\(p\) can still fire (Cycle QV mismatch). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_rz.py --certify`.
Dump: `research/cycle_rz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RY (odd-child green4 at even \(j\) is
\((G(m,r),G(m,r-1),G(m,r)\oplus G(m,r-1),G(m,r))\); never AND; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (odd-child green4)

At \(n=2m+1\), \(j=2r\),
\(\mathrm{green4}=(G(m,r),G(m,r-1),G(m,r)\oplus G(m,r-1),G(m,r))\).
At odd \(j=2r+1\),
\(\mathrm{green4}=(G(m,r+1)\oplus G(m,r),G(m,r+1),G(m,r),G(m,r-1))\).
Both never in AND_ONES. Status: **lemma**. **Killed:** odd-child
green4 equals parent green4. **Killed:** odd-child green4 equals
even-child green4. **Killed:** odd-child green4 equals Cycle HJ
consecutive Green.

## Verdict

`LEMMA` (odd-child green4 at even \(j\) is
\((G(m,r),G(m,r-1),G(m,r)\oplus G(m,r-1),G(m,r))\); never AND;
HJ/HS/QV/RY closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (odd-child green4 equals parent green4; odd-child green4
equals even-child green4; odd-child green4 equals HJ consecutive
Green; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rz.md` (this note)
- `research/cycle_rz.py`
- `research/cycle_rz.json`
