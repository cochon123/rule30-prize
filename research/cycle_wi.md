# Cycle WI: named leftover extra gpd1/gpd2 closed forms

Named leftover extra \(n_{\mathrm{gp}}\) splits by parent \(d=1\)
versus even \(d=2\). For \(k\ge 2\)
\[
\mathrm{gpd1}_s=\frac{5\cdot 2^{k-2}-2(-1)^k-3}{3}
\]
\[
\mathrm{gpd1}_l=2^{k-2}+(-1)^k.
\]
For \(k\ge 3\)
\[
\mathrm{gpd2}_s=\frac{5\cdot 2^{k-3}+2(-1)^k-3}{3}
\]
\[
\mathrm{gpd2}_l=2^{k-3}-(-1)^k.
\]
Halves sum to Cycle UL \(\mathrm{gp}{:}d=1\) / \(\mathrm{gp}{:}d=2\)
and Cycle WG named \(\mathrm{gp}\) halves. Special-case all \(0\) at
\(k\le 1\); \(\mathrm{gpd2}\) also \(0\) at \(k=2\) except
\(\mathrm{gpd1}_l=2\). Dies at \(k=3\) for \(\mathrm{gpd1}_s\) and
\(\mathrm{gpd1}_l\) with shift \(0\) (\(\mathrm{gpd1}_s\) got \(1\),
not \(3\); \(\mathrm{gpd1}_l\) got \(0\), not \(1\)). Dies at
\(k=4\) for \(\mathrm{gpd2}_s\) and \(\mathrm{gpd2}_l\) with shift
\(0\) (\(\mathrm{gpd2}_s\) got \(1\), not \(3\); \(\mathrm{gpd2}_l\)
got \(0\), not \(1\)). Do **not** kill \(\mathrm{gpd1}\) shift \(0\)
at \(k=2\) or \(\mathrm{gpd2}\) shift \(0\) at \(k=3\): they match.
Do **not** kill \(\mathrm{gpd1}_s\) sign at \(k=8\): floor-div
masks (\(105=105\)); kill that sign at \(k=7\) (\(52\) vs \(53\)).
Dies at \(k=8\) without the \(\mathrm{gpd1}_s\) \(5\cdot 2^{k-2}\)
(got \(-2\), not \(105\)), without the \(\mathrm{gpd1}_s\) \(-3\)
(got \(106\), not \(105\)), without the \(\mathrm{gpd1}_l\)
\(2^{k-2}\) (got \(1\), not \(65\)), without the \(\mathrm{gpd1}_l\)
sign (got \(64\), not \(65\)), without the \(\mathrm{gpd2}_s\)
\(5\cdot 2^{k-3}\) (got \(-1\), not \(53\)), without the
\(\mathrm{gpd2}_s\) sign (got \(52\), not \(53\)), without the
\(\mathrm{gpd2}_s\) \(-3\) (got \(54\), not \(53\)), without the
\(\mathrm{gpd2}_l\) \(2^{k-3}\) (got \(-1\), not \(31\)), and
without the \(\mathrm{gpd2}_l\) sign (got \(32\), not \(31\)). Dies
at \(k=8\) for \(\mathrm{gpd1}_s\) equals tot \(\mathrm{gp}_s\)
(got \(105\), not \(158\)), \(\mathrm{gpd1}_s\) equals
\(\mathrm{gpd2}_s\) (got \(105\), not \(53\)), \(\mathrm{gpd1}_s\)
equals tot small (got \(105\), not \(266\)), and
\(\mathrm{gpd1}_s\) equals \(\mathrm{gpd1}_l\) (got \(105\), not
\(65\)). Census \(k=8\): \(\mathrm{gpd1}_s\) \(105\),
\(\mathrm{gpd1}_l\) \(65\), \(\mathrm{gpd2}_s\) \(53\),
\(\mathrm{gpd2}_l\) \(31\). Do **not** PREFIX pal-center tot from
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

Certify: `python3 research/cycle_wi.py --certify` (~0.35s).
Dump: `research/cycle_wi.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UL/UO/UP/UR/UU/UV/UW/UZ/VA/VY/WE/WG/WH
(\(\mathrm{gpd1}/\mathrm{gpd2}\) closed forms; no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(\mathrm{gpd1}_s\) is \((5\cdot 2^{k-2}-2(-1)^k-3)/3\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=3\) for
shift \(0\); without \(5\cdot 2^{k-2}\) at \(k=8\); without \(-3\)
at \(k=8\); without the sign at \(k=7\); small equals tot
\(\mathrm{gp}_s\) at \(k=8\); small equals \(\mathrm{gpd2}_s\) at
\(k=8\); small equals tot named at \(k=8\);
\(\mathrm{gpd1}_s=\mathrm{gpd1}_l\) at \(k=8\). Do **not** kill
shift \(0\) at \(k=2\). Do **not** kill the sign at \(k=8\).

## Lemma (\(\mathrm{gpd1}_l\) is \(2^{k-2}+(-1)^k\) for \(k\ge 2\))

Special-case \(0\) at \(k\le 1\). The two \(\mathrm{gpd1}\) halves
sum to Cycle UL \(\mathrm{gp}{:}d=1\). Status: **lemma**. Algebra
through \(k\le 64\); census through \(k\le 8\). **Killed** at
\(k=3\) for shift \(0\); without \(2^{k-2}\) at \(k=8\); without
the sign at \(k=8\). Do **not** kill shift \(0\) at \(k=2\).

## Lemma (\(\mathrm{gpd2}_s\) is \((5\cdot 2^{k-3}+2(-1)^k-3)/3\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=4\) for
shift \(0\); without \(5\cdot 2^{k-3}\) at \(k=8\); without the
sign at \(k=8\); without \(-3\) at \(k=8\). Do **not** kill shift
\(0\) at \(k=3\).

## Lemma (\(\mathrm{gpd2}_l\) is \(2^{k-3}-(-1)^k\) for \(k\ge 3\))

Special-case \(0\) at \(k\le 2\). The two \(\mathrm{gpd2}\) halves
sum to Cycle UL \(\mathrm{gp}{:}d=2\). The \(\mathrm{gpd1}\) plus
\(\mathrm{gpd2}\) small/large halves sum to Cycle WG named
\(\mathrm{gp}\) halves. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 8\). **Killed** at \(k=4\) for
shift \(0\); without \(2^{k-3}\) at \(k=8\); without the sign at
\(k=8\). Do **not** kill shift \(0\) at \(k=3\). Do **not** PREFIX
pal-center tot.

## Verdict

`LEMMA` (\(\mathrm{gpd1}/\mathrm{gpd2}\) closed forms; halves sum
to UL \(\mathrm{gp}{:}d=1\)/\(\mathrm{gp}{:}d=2\) and WG named
\(\mathrm{gp}\) halves).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (\(\mathrm{gpd1}\) shift \(0\) at \(k=3\);
\(\mathrm{gpd2}\) shift \(0\) at \(k=4\); without \(\mathrm{gpd1}_s\)
\(5\cdot 2^{k-2}\); without \(\mathrm{gpd1}_s\) \(-3\); without
\(\mathrm{gpd1}_s\) sign at \(k=7\); without \(\mathrm{gpd1}_l\)
\(2^{k-2}\); without \(\mathrm{gpd1}_l\) sign; without
\(\mathrm{gpd2}_s\) \(5\cdot 2^{k-3}\); without \(\mathrm{gpd2}_s\)
sign; without \(\mathrm{gpd2}_s\) \(-3\); without
\(\mathrm{gpd2}_l\) \(2^{k-3}\); without \(\mathrm{gpd2}_l\) sign;
\(\mathrm{gpd1}_s\) equals tot \(\mathrm{gp}_s\);
\(\mathrm{gpd1}_s=\mathrm{gpd2}_s\); \(\mathrm{gpd1}_s\) equals tot
small; \(\mathrm{gpd1}_s=\mathrm{gpd1}_l\); pal-center tot equals
\(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_wi.md` (this note)
- `research/cycle_wi.py`
- `research/cycle_wi.json`
