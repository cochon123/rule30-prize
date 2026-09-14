# Cycle VC: leftover extra xor small is \(\mathrm{lo\_small}\) minus \(j=0\); difference is \(j_0-d_{2e}^{\mathrm{small}}\)

Leftover extra except \(j=0\) each produce one leftover-parent xor
child. On \(n\le 5U/2\) that count is
\(\mathrm{lo\_small}(k-1)-j_0(k-1)\) for \(k\ge 3\), the complement of
Cycle UV's \(\mathrm{lo\_large}(k-1)\) on \(n>5U/2\). The signed
difference is \(j_0(k-1)-d_{2e}^{\mathrm{small}}(k-1)\) for \(k\ge 4\):
leftover extra small \((n\equiv 1\) minus \(n\equiv 3)\) at the parent
plus \(j=0\) leftover extra, since \(n\equiv 1\) extra small is
sign-balanced (Cycle VB) and \(j=0\) is excluded from the xor. Dies
at \(k=2\) for the count (got \(0\), not \(1\)). Dies at \(k=3\) for
the difference (got \(3\), not \(2\)). Census \(k=8\): leftover extra
xor small \(3191\); difference \(105\). Do **not** PREFIX pal-center
tot from small \(k\). Do **not** PREFIX leftover spat tot. Do **not**
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

Certify: `python3 research/cycle_vc.py --certify`.
Dump: `research/cycle_vc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UK/UN/UP/UR/UU/UV/UW/UY/UZ/VA
(leftover extra xor small count and difference; no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover extra xor small is \(\mathrm{lo\_small}(k-1)-j_0(k-1)\) for \(k\ge 3\))

Complement of Cycle UV leftover extra xor large
\(=\mathrm{lo\_large}(k-1)\). Equals leftover extra small except
\(j=0\) at the parent. Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** at \(k=2\) (count \(0\), not
\(1\)).

## Lemma (leftover extra xor small difference is \(j_0(k-1)-d_{2e}^{\mathrm{small}}(k-1)\) for \(k\ge 4\))

Cycle VB leftover extra small \(n\equiv 1\) is sign-balanced, so the
xor sign is leftover extra small \((n\equiv 1-n\equiv 3)\) at the
parent plus \(j=0\). Closed form \(5\cdot 2^{k-3}-1-d_{2e}^{\mathrm{small}}(k-1)\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=3\) (count \(3\), not \(2\)). Do **not**
PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover extra xor small is
\(\mathrm{lo\_small}(k-1)-j_0(k-1)\) for \(k\ge 3\); leftover extra xor
small difference is \(j_0(k-1)-d_{2e}^{\mathrm{small}}(k-1)\) for
\(k\ge 4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (xor small count at \(k=2\); xor small difference at \(k=3\);
pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vc.md` (this note)
- `research/cycle_vc.py`
- `research/cycle_vc.json`
