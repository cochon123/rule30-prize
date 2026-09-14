# Cycle UY: leftover extra large on \(n\equiv 3\pmod{4}\) is \(\mathrm{lo\_large}\) plus a 2-step fold

Leftover extra xor from leftover extra large all land on
\(n\equiv 3\pmod{4}\), count \(\mathrm{lo\_large}(k-1)\) (Cycle UV).
Odd-\(j\) leftover from leftover extra large at \(k-2\) produce leftover
extra \((j,j+2)\) pairs, count \(2\,\mathrm{lo\_large}(k-2)\). Named
\(g_0{+}d{=}1\) and \(d{=}2{+}g_0\) add \(d_1^{\mathrm{large}}(k-1)+
d_{2o}^{\mathrm{large}}(k-1)\). Hence leftover extra large on
\(n\equiv 3\pmod{4}\) is that sum for \(k\ge 4\). With Cycle UX
\(n_1=2(e_{\ge}(k-1)+d_{2e}^{\mathrm{large}}(k-1))\), the extra
\(n_3-n_1\) recures as \(\mathrm{extra}(k-1)+d_1^{\mathrm{large}}(k-1)
-d_{2e}^{\mathrm{large}}(k-1)\) with \(\mathrm{extra}(3)=0\), so
\(\mathrm{extra}(k)=2^{k-2}-1-(-1)^{k+1}\) for \(k\ge 3\) and
leftover-parent xor large difference is \(1-2^{k-3}+(-1)^k\) for
\(k\ge 4\). Dies at \(k=3\) for the \(n\equiv 3\) sum (count \(8\),
not \(6\)). Dies at \(k=2\) for the extra form. Dies at \(k=3\) for
the large-difference form. Census \(k=8\): leftover extra large
\(n\equiv 3\) is \(3354=2034+2\cdot 612+65+31\); extra \(64\);
leftover-parent xor large difference \(-30\). Do **not** PREFIX
pal-center tot from small \(k\). Do **not** PREFIX leftover spat tot.
Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover
\(d\). Do **not** claim pal-center tot equals \(S\oplus T\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_uy.py --certify` (~0.39s).
Dump: `research/cycle_uy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UK/UL/UN/UP/UQ/UR/UU/UV/UW/UX
(leftover extra large \(n\equiv 3\) 2-step fold and leftover-parent xor
large difference; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (leftover extra large on \(n\equiv 3\pmod{4}\) is \(\mathrm{lo\_large}(k-1)+2\,\mathrm{lo\_large}(k-2)+d_1^{\mathrm{large}}(k-1)+d_{2o}^{\mathrm{large}}(k-1)\) for \(k\ge 4\))

Leftover extra xor from leftover extra large land on \(n\equiv 3\).
Odd-\(j\) leftover from leftover extra large at \(k-2\) 2-fold to
leftover extra pairs. Named \(g_0{+}d{=}1\) and odd \(d=2{+}g_0\) add
the remaining cells. Status: **lemma**. Census through \(k\le 8\).
Special-case \(8\) at \(k=3\); \(3\) at \(k=2\). **Killed** at \(k=3\)
for the sum.

## Lemma (leftover extra large extra recures as \(d_1^{\mathrm{large}}-d_{2e}^{\mathrm{large}}\) for \(k\ge 4\))

Parent kinds on leftover extra large \(n\equiv 3\) are \(\mathrm{lo}{+}g_0\),
\(g_0{+}\mathrm{lo}\), \(g_0{+}d{=}1\), \(d{=}2{+}g_0\), with
\(\mathrm{lo}{+}g_0=e_{\ge}(k-1)\) and \(g_0{+}\mathrm{lo}=e_{\ge}(k-1)
+\mathrm{extra}(k-1)\). Cycle UX \(n_1\) then cancels \(e_{\ge}\), so
\(\mathrm{extra}(k)=\mathrm{extra}(k-1)+d_1^{\mathrm{large}}(k-1)
-d_{2e}^{\mathrm{large}}(k-1)\) with \(\mathrm{extra}(3)=0\). Hence
\(\mathrm{extra}(k)=2^{k-2}-1-(-1)^{k+1}\) for \(k\ge 3\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=2\) for the extra form.

## Lemma (leftover-parent xor large difference is \(1-2^{k-3}+(-1)^k\) for \(k\ge 4\))

Cycle UX: large difference equals leftover extra large \((n_1-n_3)\)
at \(k-1\), hence \(-\mathrm{extra}(k-1)\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\).
Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra large on \(n\equiv 3\pmod{4}\) is
\(\mathrm{lo\_large}(k-1)+2\,\mathrm{lo\_large}(k-2)+d_1^{\mathrm{large}}(k-1)+d_{2o}^{\mathrm{large}}(k-1)\)
for \(k\ge 4\); extra recures as \(d_1^{\mathrm{large}}-d_{2e}^{\mathrm{large}}\)
with \(\mathrm{extra}(3)=0\); leftover-parent xor large difference is
\(1-2^{k-3}+(-1)^k\) for \(k\ge 4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(n\equiv 3\) sum at \(k=3\); extra form at \(k=2\);
large-difference form at \(k=3\); leftover extra \(n\equiv 3\) equals
\(n\equiv 1\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_uy.md` (this note)
- `research/cycle_uy.py`
- `research/cycle_uy.json`
