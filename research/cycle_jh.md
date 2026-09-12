# Cycle JH: even-\(n\) `iso_half3` interiors are \(010\) iff \(v_2(n)\) is odd

On even \(n>0\), core-slot offset \(0\) is \(001\) and offset \(2r\)
is \(100\) for every \(v_2\). Interiors are \(010\) when \(v_2(n)\)
is odd and \(111\) when \(v_2(n)\) is even. Cycle JG is the \(v_2=1\)
case. \(v_2\)-even interiors are **not** \(010\). \(v_2\)-odd
interiors are **not** \(111\). \(v_2\)-even ends are **not** \(111\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: the \(v_2\)-parity 3-window still leaves packed
AND on those columns (and on pairs), so covering never-fail stays
open.

Helper: `iso3_even`. Certify:
`python3 research/cycle_jh.py --certify` (~0.16s).
Dump: `research/cycle_jh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/IT/JF/JG (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso_half3` is `iso3_even` on even \(n>0\))

For \(n<64\), every even isolated one has `iso_half3==iso3_even`.
Census \(n_{\mathrm{iso}}=461\): seed \(1\), odd \(45\), even
\(415\) split \(001\) \(115\), \(010\) \(141\), \(100\) \(115\),
\(111\) \(44\). \(v_2\) odd \(319\), \(v_2\) even \(96\). Cycle JG
agrees on \(n\equiv 2\pmod{4}\).

## Lemma (interiors are \(010\) iff \(v_2(n)\) is odd)

All \(141\) copies of \(010\) have odd \(v_2\). All \(44\) copies of
\(111\) have even \(v_2\). Ends are \(001/100\) independently of
\(v_2\).

## Lemma (covering even-\(n\) \(v_2\) 3-windows)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\), odd \(741\), even \(7030\)). Even split
\(001\) \(2011\), \(010\) \(2373\), \(100\) \(1912\), \(111\)
\(734\). \(v_2\) odd \(5365\), \(v_2\) even \(1665\). Odd-\(s\)
\(J\) XOR matches Cycles HF/HG.

## Killed

\(v_2\)-even interiors are \(010\): at \(k=1\), \(s=11\), \(n=4\),
\(j=4\), \(v_2=2\), slot \((0,1,1)\), three \(111\), \(p=12\).
\(v_2\)-odd interiors are \(111\): at \(k=0\), \(s=5\), \(n=2\),
\(j=2\), \(v_2=1\), slot \((0,1,1)\), three \(010\), \(p=6\).
\(v_2\)-even ends are \(111\): at \(k=1\), \(s=11\), \(n=4\),
\(j=0\), \(v_2=2\), slot \((0,1,0)\), three \(001\), \(p=20\).

## Verdict

`LEMMA` (`iso_half3` is `iso3_even` on even \(n>0\); interiors are
\(010\) iff \(v_2(n)\) is odd; covering even-\(n\) \(v_2\)
3-windows).
`KILLED` (\(v_2\)-even interiors are \(010\); \(v_2\)-odd interiors
are \(111\); \(v_2\)-even ends are \(111\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jh.md` (this note)
- `research/cycle_jh.py`
- `research/cycle_jh.json`
