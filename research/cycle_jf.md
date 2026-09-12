# Cycle JF: `iso1_lift5` is the freshman stretch of the half 3-window

On even \(n=2m>0\) the parent is odd, so the isolated-one 5-window
is the cob-stretch \((a,a\oplus b,b,b\oplus c,c)\) of
\((G(m-1,k-2),G(m-1,k-1),G(m-1,k))\) at even \(j=2k\). The four
odd-weight 3-tuples map onto `LIFT1`. On odd \(n\) the parent is
even and the 3-window is always \(111\), stretching to \(10101\).
Even iso is **not** always cob of \(111\). Even half 3-window is
**not** always \(010\). Even-\(n\) lift is **not** the even-parent
zero-stretch. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\).
Do **not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: stretching isolated-one 3-windows still leaves
packed AND on those columns (and on pairs), so covering never-fail
stays open.

Helper: `iso_half3`, `freshman_lift5`. Certify:
`python3 research/cycle_jf.py --certify` (~0.13s).
Dump: `research/cycle_jf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/JD/JE (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso1_lift5` is `freshman_lift5` of `iso_half3`)

For \(n<64\), every isolated one with \(n>0\) has
`iso1_lift5==freshman_lift5(iso_half3, n odd)`. Census
\(n_{\mathrm{iso}}=461\): seed \(1\), odd \(45\) all \(111\), even
\(415\) split \(001\) \(115\), \(010\) \(141\), \(100\) \(115\),
\(111\) \(44\).

## Lemma (odd-weight 3-tuples map onto `LIFT1`)

Cob-stretch: \(001\mapsto 00011\), \(010\mapsto 01110\),
\(100\mapsto 11000\), \(111\mapsto 10101\). Even-parent
zero-stretch of \(111\) is also \(10101\).

## Lemma (covering half-stretch)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\), odd \(741\) all \(111\), even \(7030\)).
Even 3-window census \(001\) \(2011\), \(010\) \(2373\), \(100\)
\(1912\), \(111\) \(734\). Odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Killed

Even iso always cob of \(111\): at \(k=0\), \(s=5\), \(n=2\),
\(j=0\), three \(001\), window \(00011\), \(p=10\). Even half
3-window always \(010\): at \(k=1\), \(s=7\), \(n=2\), \(j=4\),
three \(100\), \(p=4\). Even-\(n\) lift is even-parent
zero-stretch: same first witness, \(00001\neq 00011\).

## Verdict

`LEMMA` (`iso1_lift5` is `freshman_lift5` of `iso_half3`;
odd-weight 3-tuples map onto `LIFT1`; covering half-stretch).
`KILLED` (even iso always cob of \(111\); even half 3-window always
\(010\); even-\(n\) lift is even-parent zero-stretch).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jf.md` (this note)
- `research/cycle_jf.py`
- `research/cycle_jf.json`
