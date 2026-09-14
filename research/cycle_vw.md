# Cycle VW: leftover-parent xor tot F/L closed form

Leftover-parent xor tot for \(k\ge 2\) is
\[
\frac{2^{k-2}(20 L_k+16 L_{k-1}-85)+5(-1)^k+14}{5}.
\]
Equals Cycle VU halves and Cycle UP \(4\,\mathrm{lo}_e(k-1)\) minus
Cycle UM. Special-case \(0\) at \(k\le 1\). Dies at \(k=2\) for the
F/L form with shift \(0\) (got \(3\), not \(2\)). Dies at \(k=8\)
without \(+14\) (got \(16884\), not \(16887\)) and without
\(5(-1)^k\) (got \(16886\), not \(16887\)). Dies at \(k=8\) for tot
equals small (got \(16887\), not \(10401\)). Census \(k=8\): tot
\(16887\). Do **not** PREFIX pal-center tot from small \(k\). Do
**not** PREFIX leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** catalogue leftover \(d\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_vw.py --certify`.
Dump: `research/cycle_vw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UM/UO/UP/UR/UU/UV/UW/UZ/VA/VU
(leftover-parent xor tot F/L; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover-parent xor tot is \((2^{k-2}(20 L_k+16 L_{k-1}-85)+5(-1)^k+14)/5\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). Equals Cycle VU halves. Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=2\) for the F/L form with shift \(0\); without
\(+14\) at \(k=8\); without \(5(-1)^k\) at \(k=8\). Do **not**
PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover-parent xor tot F/L closed form for \(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (F/L form at \(k=2\); without \(+14\); without \(5(-1)^k\);
tot equals small; pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vw.md` (this note)
- `research/cycle_vw.py`
- `research/cycle_vw.json`
