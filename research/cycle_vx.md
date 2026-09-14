# Cycle VX: leftover-parent xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) F/L closed forms

Cycle VW tot splits as pair-then-\(g_0\) versus \(g_0\)-then-pair.
For \(k\ge 2\)
\[
n_{\mathrm{pg}}=\frac{2^{k-2}(75 F_{k-1}+39 L_{k-1}-100)+10(-1)^k+6}{15}
\]
and
\[
n_{\mathrm{gp}}=\frac{2^{k-2}(60 L_k+9 L_{k-1}-75 F_{k-1}-155)+5(-1)^k+36}{15}.
\]
They sum to Cycle VW tot. \(n_{\mathrm{pg}}\) is \(2\,\mathrm{lo}_e(k-1)\).
Both \(0\) at \(k\le 1\). Dies at \(k=2\) for both F/L forms with
shift \(0\) (\(n_{\mathrm{pg}}\) got \(1\), not \(2\);
\(n_{\mathrm{gp}}\) got \(2\), not \(0\)). Dies at \(k=8\) without
the \(n_{\mathrm{pg}}\) \(+6\) (got \(8559\), not \(8560\)) and
without the \(n_{\mathrm{gp}}\) \(+36\) (got \(8324\), not
\(8327\)). Dies at \(k=8\) for \(n_{\mathrm{pg}}\) equals
\(n_{\mathrm{gp}}\) (got \(8560\), not \(8327\)). Census \(k=8\):
\(n_{\mathrm{pg}}\) \(8560\), \(n_{\mathrm{gp}}\) \(8327\). Do
**not** PREFIX pal-center tot from small \(k\). Do **not** PREFIX
leftover spat tot. Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do
**not** catalogue leftover \(d\). Do **not** claim pal-center tot
equals \(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_vx.py --certify`.
Dump: `research/cycle_vx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TW/UC/UD/UE/UL/UM/UP/UR/UU/UV/UW/UZ/VA/VW
(leftover-parent xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\) F/L; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (leftover-parent xor \(n_{\mathrm{pg}}\) is \((2^{k-2}(75 F_{k-1}+39 L_{k-1}-100)+10(-1)^k+6)/15\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). Equals \(2\,\mathrm{lo}_e(k-1)\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=2\) for the F/L form with shift
\(0\); without \(+6\) at \(k=8\).

## Lemma (leftover-parent xor \(n_{\mathrm{gp}}\) is \((2^{k-2}(60 L_k+9 L_{k-1}-75 F_{k-1}-155)+5(-1)^k+36)/15\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). The two halves sum to Cycle VW
tot. Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=2\) for the F/L form with shift
\(0\); without \(+36\) at \(k=8\); \(n_{\mathrm{pg}}\) equals
\(n_{\mathrm{gp}}\) at \(k=8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (leftover-parent xor \(n_{\mathrm{pg}}/n_{\mathrm{gp}}\)
F/L closed forms for \(k\ge 2\); halves sum to parent xor tot).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(n_{\mathrm{pg}}\) F/L form at \(k=2\);
\(n_{\mathrm{gp}}\) F/L form at \(k=2\); without \(+6\); without
\(+36\); \(n_{\mathrm{pg}}\) equals \(n_{\mathrm{gp}}\); pal-center
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

- `research/cycle_vx.md` (this note)
- `research/cycle_vx.py`
- `research/cycle_vx.json`
