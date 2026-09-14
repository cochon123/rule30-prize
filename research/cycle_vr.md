# Cycle VR: unpaired extra tot is \(2^{k+1}F_{k+2}-2^{k+2}-4\,\mathrm{lo}_e(k-1)+2(-1)^k+1\)

Cycle UC extra-sum minus Cycle VQ leftover extra. For \(k\ge 2\)
\[
\mathrm{extra\_unp}=2^{k+1}F_{k+2}-2^{k+2}-4\,\mathrm{lo}_e(k-1)+2(-1)^k+1
\]
and the F/L form is
\[
\frac{2^{k-2}(42 L_{k-1}+90 F_{k-1}-40)+10(-1)^k+3}{15}.
\]
Special-case \(1\) at \(k\le 1\). Dies at \(k=1\) for the
\(\mathrm{lo}_e\) form without the special case (got \(-1\), not
\(1\)). Dies at \(k=8\) without the F/L \(+3\) (got \(10018\), not
\(10019\)). Dies at \(k=2\) for the F/L form with shift \(0\) (got
\(0\), not \(7\)). Dies at \(k=0\) for tot \(0\) (got \(0\), not
\(1\)). Census \(k=8\): extra_unp \(10019\). Do **not** PREFIX
pal-center tot from small \(k\). Do **not** PREFIX leftover spat tot.
Do **not** PREFIX \(d=1\)/\(d=2\) spat tot. Do **not** catalogue
leftover \(d\). Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
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

Certify: `python3 research/cycle_vr.py --certify` (~0.35s).
Dump: `research/cycle_vr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UO/UP/UR/UU/UV/UW/UZ/VA/VQ
(extra_unp \(4\,\mathrm{lo}_e\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (unpaired extra tot is \(2^{k+1}F_{k+2}-2^{k+2}-4\,\mathrm{lo}_e(k-1)+2(-1)^k+1\) for \(k\ge 2\))

Special-case \(1\) at \(k\le 1\). Equals Cycle UC extra-sum minus
Cycle VQ leftover extra. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=1\) for
the form without the special case.

## Lemma (unpaired extra tot is \((2^{k-2}(42 L_{k-1}+90 F_{k-1}-40)+10(-1)^k+3)/15\) for \(k\ge 2\))

Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 8\). **Killed** at \(k=2\) for the F/L form with shift \(0\);
at \(k=8\) without the \(+3\); at \(k=0\) for tot \(0\). Do **not**
PREFIX pal-center tot.

## Verdict

`LEMMA` (extra_unp \(4\,\mathrm{lo}_e\) form and F/L closed form for
\(k\ge 2\)).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (lo_e form at \(k=1\); F/L form with shift \(0\) at
\(k=2\); form without \(+3\) at \(k=8\); tot \(0\) at \(k=0\);
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

- `research/cycle_vr.md` (this note)
- `research/cycle_vr.py`
- `research/cycle_vr.json`
