# Cycle JJ: doubling \(n\) maps isolated-one `LIFT1` by swapping palindromes

`iso1_lift5(2n,2j)` equals `lift5_double` of `iso1_lift5(n,j)` for
every isolated one with \(n>0\). Ends \(00011\) and \(11000\) stay.
Interiors swap \(01110\) with \(10101\). Odd-\(n\) \(10101\) doubles
to \(01110\). Interiors do **not** stay. Ends do **not** swap.
Odd iso does **not** double to \(10101\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: doubling isolated-one parent windows still
leaves packed AND on those columns (and on pairs), so covering
never-fail stays open.

Helper: `lift5_double`. Certify:
`python3 research/cycle_jj.py --certify` (~0.14s).
Dump: `research/cycle_jj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/JD/JI (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso1_lift5(2n,2j)` is `lift5_double` of the parent)

For \(n<64\), every isolated one with \(n>0\) has
`iso1_lift5(2n,2j)==lift5_double(iso1_lift5(n,j))`. Census
\(n_{\mathrm{iso}}=461\): seed \(1\), stay \(00011\) \(115\), stay
\(11000\) \(115\), swap \(01110\to 10101\) \(141\), swap
\(10101\to 01110\) \(89\).

## Lemma (`lift5_double` fixes ends and swaps palindromes)

\(00011\) and \(11000\) stay. \(01110\leftrightarrow 10101\). Odd-\(n\)
isolated ones (all \(10101\)) therefore double to \(01110\).

## Lemma (covering doubling)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\)); doubling \(7771\): stay \(00011\) \(2011\),
stay \(11000\) \(1912\), swap \(01110\) \(2373\), swap \(10101\)
\(1475\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Interiors stay: at \(k=1\), \(s=15\), \(n=2\), \(j=2\) vs
\(n=4\), \(j=4\), windows \(01110\) vs \(10101\), \(p=16\) and
\(p=12\). Ends swap: at \(k=1\), \(s=15\), \(n=2\), \(j=0\) vs
\(n=4\), \(j=0\), window \(00011\) stays, \(p=20\). Odd iso doubles
to \(10101\): at \(k=2\), \(s=17\), \(n=3\), \(j=3\) vs \(n=6\),
\(j=6\), windows \(10101\) vs \(01110\), \(p=18\) and \(p=12\).

## Verdict

`LEMMA` (`iso1_lift5(2n,2j)` is `lift5_double` of the parent;
`lift5_double` fixes ends and swaps palindromes; covering doubling).
`KILLED` (interiors stay; ends swap; odd iso doubles to \(10101\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jj.md` (this note)
- `research/cycle_jj.py`
- `research/cycle_jj.json`
