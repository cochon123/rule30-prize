# Cycle VE: leftover-parent xor small difference minus leftover extra xor small difference is \(5\cdot 2^{k-3}-2\)

\(\mathrm{pg}{:}\mathrm{lo}-\mathrm{gp}{:}\mathrm{lo}\) on \(n\le 5U/2\)
minus leftover extra xor small difference equals \(5\cdot 2^{k-3}-2\)
for \(k\ge 3\), and \(\mathrm{named}_l-2(1-(-1)^k)\) for \(k\ge 4\)
(\(\mathrm{named}_l\) when \(k\) is even; \(\mathrm{named}_l-4\) when
\(k\) is odd). Dies at \(k=2\) (got \(1\); form \(3\)). Dies at \(k=5\)
for equality with \(\mathrm{named}_l\) (got \(18\), not \(22\)). Census
\(k=8\): gap \(158\). Do **not** PREFIX pal-center tot from small
\(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
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

Certify: `python3 research/cycle_ve.py --certify` (~0.40s).
Dump: `research/cycle_ve.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UO/UP/UR/UU/UV/UW/UY/UZ/VA/VC/VD
(xor small gap; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (leftover-parent xor small difference minus leftover extra xor small difference is \(5\cdot 2^{k-3}-2\) for \(k\ge 3\))

Special-case \(1\) at \(k=2\); \(0\) at \(k\le 1\). Status: **lemma**.
Algebra through \(k\le 64\); census through \(k\le 8\). **Killed**
at \(k=2\) (got \(1\), form \(3\)).

## Lemma (that gap equals \(\mathrm{named}_l-2(1-(-1)^k)\) for \(k\ge 4\))

Equals \(\mathrm{named}_l\) on even \(k\ge 4\); \(\mathrm{named}_l-4\)
on odd \(k\ge 5\). Status: **lemma**. Algebra through \(k\le 64\);
census through \(k\le 8\). **Killed** at \(k=5\) for equality with
\(\mathrm{named}_l\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (xor small gap is \(5\cdot 2^{k-3}-2\) for \(k\ge 3\); equals
\(\mathrm{named}_l-2(1-(-1)^k)\) for \(k\ge 4\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (form at \(k=2\); gap equals \(\mathrm{named}_l\) at \(k=5\);
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

- `research/cycle_ve.md` (this note)
- `research/cycle_ve.py`
- `research/cycle_ve.json`
