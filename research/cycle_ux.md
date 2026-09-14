# Cycle UX: leftover extra large on \(n\equiv 1\pmod{4}\) is 2-fold parent even leftover large \(\cup d=2\)

Even leftover \(\cup d=2\) on \(n\ge 5U_p/2\) produces leftover extra
\((j,j+2)\) pairs on large covering \(n\equiv 1\pmod{4}\), count
\(2(e_{\ge}(k-1)+d_{2e}^{\mathrm{large}}(k-1))\) for \(k\ge 4\).
\(G(s,t)=0\) leftover extra large on \(n\equiv 3\pmod{4}\) equals
that on \(n\equiv 1\pmod{4}\) for \(k\ge 3\), and leftover extra on
\(n\equiv 1\) is sign-balanced (Cycle UW), so the extra cells
\(n_3-n_1\) are all \(G(s,t)=1\). Leftover extra xor large
difference (hence leftover-parent xor large difference: even parents
net \(0\) by Cycle UU) is leftover extra large \((n_1-n_3)\) at
\(k-1\) for \(k\ge 4\). Dies at \(k=3\) for the 2-fold (count \(8\),
not \(2(e_{\ge}(2)+d_{2e}^{\mathrm{large}}(2))=6\)). Dies at \(k=2\)
for \(g_0\) equal. Census \(k=8\): leftover extra large \(n\equiv 1\)
is \(3290=2(1614+65)\); \(n\equiv 3\) is \(3354\); both residues have
\(g_0=1645\). Parent \(k=7\): \(n_1-n_3=-30\). Do **not** PREFIX
leftover-parent xor large difference as a 0-1 form or pal-center tot
from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\).
Do **not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_ux.py --certify` (~0.38s).
Dump: `research/cycle_ux.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UN/UP/UR/UU/UV/UW
(leftover extra large \(n\equiv 1\) 2-fold and \(g_0\) equality; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (leftover extra large on \(n\equiv 1\pmod{4}\) is \(2(e_{\ge}(k-1)+d_{2e}^{\mathrm{large}}(k-1))\) for \(k\ge 4\))

Even covering leftover \(\cup d=2\) on \(n\ge 5U_p/2\) 2-fold to
leftover extra \((j,j+2)\) on large \(n\equiv 1\pmod{4}\). Status:
**lemma**. Census through \(k\le 8\). Special-case \(8\) at \(k=3\);
\(0\) at \(k\le 2\). **Killed** at \(k=3\) for the 2-fold.

## Lemma (\(G(s,t)=0\) leftover extra large on \(n\equiv 3\pmod{4}\) equals that on \(n\equiv 1\pmod{4}\) for \(k\ge 3\))

Leftover extra on \(n\equiv 1\) is sign-balanced, so \(g_0=n_1/2\).
The extra cells \(n_3-n_1\) are all \(G(s,t)=1\). Status: **lemma**.
Census through \(k\le 8\). **Killed** at \(k=2\) for \(g_0\) equal.
**Killed:** leftover extra \(n\equiv 3\) equals \(n\equiv 1\).

## Lemma (leftover-parent xor large difference equals leftover extra large \((n_1-n_3)\) at \(k-1\) for \(k\ge 4\))

Leftover extra xor large difference is \(g_0-g_1\) on leftover extra
large parents, which is \(n_1-n_3\). Even leftover parents net \(0\)
on large (Cycle UU). Status: **lemma**. Census through \(k\le 8\).
Do **not** PREFIX leftover-parent xor large difference as a 0-1
form.

## Verdict

`LEMMA` (leftover extra large on \(n\equiv 1\pmod{4}\) is
\(2(e_{\ge}(k-1)+d_{2e}^{\mathrm{large}}(k-1))\) for \(k\ge 4\);
\(G(s,t)=0\) leftover extra large on \(n\equiv 3\) equals that on
\(n\equiv 1\) for \(k\ge 3\); leftover-parent xor large difference
equals leftover extra large \((n_1-n_3)\) at \(k-1\) for \(k\ge 4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (2-fold at \(k=3\); \(g_0\) equal at \(k=2\); leftover extra
\(n\equiv 3\) equals \(n\equiv 1\); pal-center tot equals
\(S\oplus T\)).
`PREFIX` (leftover-parent xor large difference as a 0-1 form;
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\); packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\)
for all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ux.md` (this note)
- `research/cycle_ux.py`
- `research/cycle_ux.json`
