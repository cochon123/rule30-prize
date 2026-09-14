# Cycle VB: leftover extra small \(n\equiv 1\) is 2-fold; \(n\equiv 3\) is \(\mathrm{lo\_small}\) 2-step

Even leftover small union even \(d=2\) produces leftover extra
\((j,j+2)\) pairs on small \(n\equiv 1\pmod{4}\), count
\(2(\mathrm{sm}(k-1)+d_{2e}^{\mathrm{small}}(k-1))\) for \(k\ge 4\).
Leftover extra small on \(n\equiv 3\pmod{4}\) is
\(\mathrm{lo\_small}(k-1)+2\,\mathrm{lo\_small}(k-2)+d_1^{\mathrm{small}}(k-1)+d_{2o}^{\mathrm{small}}(k-1)\).
\(G=0\) leftover extra small on \(n\equiv 3\) equals that on
\(n\equiv 1\) for \(k\ge 3\), so extra cells are all \(G=1\). Dies at
\(k=3\) for the 2-fold (count \(10\), not \(12\)) and the \(n\equiv 3\)
sum (count \(14\), not \(16\)). Dies at \(k=2\) for \(G=0\) equal.
Census \(k=8\): leftover extra small \(n\equiv 1/3\) is \(5440/5546\);
both \(g_0=2720\). Do **not** PREFIX pal-center tot from small \(k\).
Do **not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_vb.py --certify`.
Dump: `research/cycle_vb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UK/UL/UN/UP/UR/UU/UV/UW/UY/UZ/VA
(leftover extra small \(n\equiv 1\) 2-fold and \(n\equiv 3\) 2-step;
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (leftover extra small on \(n\equiv 1\pmod{4}\) is \(2(\mathrm{sm}(k-1)+d_{2e}^{\mathrm{small}}(k-1))\) for \(k\ge 4\))

Parent kinds: \(\mathrm{lo}{+}g_0=\mathrm{sm}(k-1)\),
\(g_0{+}\mathrm{lo}\) with \(j=0\) folds to \(\mathrm{sm}(k-1)\),
\(d{=}2{+}g_0=d_{2e}^{\mathrm{small}}(k-1)\), \(g_0{+}d{=}2\) with
\(j=0\) folds to \(d_{2e}^{\mathrm{small}}(k-1)\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=3\) (count \(10\), not \(12\)).

## Lemma (leftover extra small on \(n\equiv 3\pmod{4}\) is \(\mathrm{lo\_small}(k-1)+2\,\mathrm{lo\_small}(k-2)+d_1^{\mathrm{small}}(k-1)+d_{2o}^{\mathrm{small}}(k-1)\) for \(k\ge 4\))

Parent kinds: \(\mathrm{lo}{+}g_0=\mathrm{sm}(k-1)\),
\(g_0{+}\mathrm{lo}\) with \(j=0\) folds to
\(\mathrm{sm}(k-1)+d_{2e}^{\mathrm{small}}(k-1)\), \(g_0{+}d{=}1\)
with \(j=0\) folds to \(d_1^{\mathrm{small}}(k-1)\),
\(d{=}2{+}g_0=d_{2o}^{\mathrm{small}}(k-1)\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=3\) (count \(14\), not \(16\)).

## Lemma (\(G=0\) leftover extra small on \(n\equiv 3\) equals that on \(n\equiv 1\) for \(k\ge 3\))

Hence leftover extra small \(n\equiv 1\) is sign-balanced, and extra
cells \(n_3-n_1=d_{2e}^{\mathrm{small}}\) (Cycle VA) are all \(G=1\).
Status: **lemma**. Census through \(k\le 8\). **Killed** at \(k=2\).
Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra small on \(n\equiv 1\pmod{4}\) is
\(2(\mathrm{sm}(k-1)+d_{2e}^{\mathrm{small}}(k-1))\) for \(k\ge 4\);
leftover extra small on \(n\equiv 3\pmod{4}\) is
\(\mathrm{lo\_small}(k-1)+2\,\mathrm{lo\_small}(k-2)+d_1^{\mathrm{small}}(k-1)+d_{2o}^{\mathrm{small}}(k-1)\)
for \(k\ge 4\); \(G=0\) equal for \(k\ge 3\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (2-fold at \(k=3\); \(n\equiv 3\) sum at \(k=3\); \(G=0\)
equal at \(k=2\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vb.md` (this note)
- `research/cycle_vb.py`
- `research/cycle_vb.json`
