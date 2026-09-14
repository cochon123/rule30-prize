# Cycle VY: named leftover extra small/large closed forms

Named leftover extra (from \(d=1\)/\(d=2\) parents) splits by
\(n\le 5U/2\). For \(k\ge 3\) the small half is
\[
\frac{25\cdot 2^{k-3}+4(-1)^k-6}{3}
\]
and the large half is
\[
5\cdot 2^{k-3}-2(-1)^k.
\]
They sum to Cycle UL named_lo. Small is Cycle VT xor_lo small minus
Cycle VU parent small. Special-case small \(1\) at \(k=1\), both
\(2\) at \(k=2\); large \(0\) at \(k\le 1\); both \(0\) at \(k\le 0\).
Dies at \(k=3\) for both forms with shift \(0\) (small got \(-4\),
not \(5\); large got \(2\), not \(7\)). Dies at \(k=8\) without the
small \(-6\) (got \(268\), not \(266\)) and without the large
\(-2(-1)^k\) (got \(160\), not \(158\)). Dies at \(k=8\) for small
equals tot named (got \(266\), not \(424\)). Census \(k=8\): small
\(266\), large \(158\). Do **not** PREFIX pal-center tot from
small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_vy.py --certify`.
Dump: `research/cycle_vy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UL/UO/UP/UR/UU/UV/UW/UZ/VA/VT/VU
(named leftover extra small/large; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (named leftover extra small is \((25\cdot 2^{k-3}+4(-1)^k-6)/3\) for \(k\ge 3\))

Special-case \(1\) at \(k=1\); \(2\) at \(k=2\); \(0\) at \(k\le 0\).
Equals xor_lo small minus leftover-parent xor small. Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\).
**Killed** at \(k=3\) for the form with shift \(0\); without \(-6\)
at \(k=8\).

## Lemma (named leftover extra large is \(5\cdot 2^{k-3}-2(-1)^k\) for \(k\ge 3\))

Special-case \(2\) at \(k=2\); \(0\) at \(k\le 1\). The two halves
sum to Cycle UL named_lo. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
the form with shift \(0\); without \(-2(-1)^k\) at \(k=8\); small
equals tot named at \(k=8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (named leftover extra small/large closed forms for
\(k\ge 3\); halves sum to named_lo).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (small form at \(k=3\); large form at \(k=3\); without
\(-6\); without \(-2(-1)^k\); small equals tot named; pal-center
tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vy.md` (this note)
- `research/cycle_vy.py`
- `research/cycle_vy.json`
