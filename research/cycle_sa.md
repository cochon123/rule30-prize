# Cycle SA: odd-child \(G=1\) even-\(j\) green4 is \((g,g\oplus 1,1,g)\)

Cycle RZ odd-child green4 at even \(j=2r\) is
\((G(m,r),G(m,r-1),G(m,r)\oplus G(m,r-1),G(m,r))\). On \(G=1\),
\(G(2m+1,2r)=G(m,r)\oplus G(m,r-1)=1\), so \(G(m,r-1)=G(m,r)\oplus 1\)
and the 4-tuple equals \((g,g\oplus 1,1,g)\) with \(g=G(m,r)\):
\((1,0,1,1)\) if \(g=1\), else \((0,1,1,0)\). Neither is in
AND_ONES, and \((1,0,1,1)\) is Cycle HS DIE \(1011\). Palindrome
\(G(n,j)=G(n,2n-j)\) sends \(r\mapsto 2m+1-r\) and
\(G(m,2m+1-r)=G(m,r-1)=g\oplus 1\), so the two types pair and
unclipped covering counts are equal. Clipped counts are **not**
equal (\(k=0\) is \(2\) vs \(1\)). Cycle RY even-child \(G=1\)
green4 is the single tuple \((0,1,1,1)\), **not** this pair.
Packed AND at consecutive-\(p\) can still fire (Cycle QV
mismatch). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_sa.py --certify`.
Dump: `research/cycle_sa.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RY/RZ (odd-child \(G=1\) even-\(j\)
green4 is \((g,g\oplus 1,1,g)\); palindrome pairs the types;
never AND; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (odd-child \(G=1\) even-\(j\) green4)

At \(n=2m+1\), even \(j=2r\), \(G=1\),
\(\mathrm{green4}=(g,g\oplus 1,1,g)\) with \(g=G(m,r)\).
Palindrome pairs \((1,0,1,1)\) with \((0,1,1,0)\), so unclipped
counts are equal. Status: **lemma**. **Killed:** that 4-tuple is
identically \((0,1,1,1)\). **Killed:** identically \((1,0,1,1)\).
**Killed:** identically \((0,1,1,0)\). **Killed:** clipped
covering counts of \((1,0,1,1)\) and \((0,1,1,0)\) are equal.

## Verdict

`LEMMA` (odd-child \(G=1\) even-\(j\) green4 is
\((g,g\oplus 1,1,g)\); palindrome pairs the two types; unclipped
counts equal; never AND; RY/RZ/HS closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (identically \((0,1,1,1)\); identically \((1,0,1,1)\);
identically \((0,1,1,0)\); clipped covering split equal; cellwise
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

- `research/cycle_sa.md` (this note)
- `research/cycle_sa.py`
- `research/cycle_sa.json`
