# Cycle JI: even-\(n\) `iso1_lift5` is the cob-stretch of `iso3_even`

On even \(n>0\) the parent 5-window is
`freshman_lift5(iso3_even, odd parent)`: offset \(0\) maps to
\(00011\), offset \(2r\) to \(11000\), \(v_2\)-odd interiors to
\(01110\), \(v_2\)-even interiors to \(10101\). \(v_2\)-odd
interiors are **not** \(10101\). Offset \(0\) is **not** \(11000\).
\(v_2\)-even interiors are **not** \(01110\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a Green-only formula for even-\(n\) isolated-one
parent windows still leaves packed AND on those columns (and on
pairs), so covering never-fail stays open.

Helper: `iso1_even`. Certify:
`python3 research/cycle_ji.py --certify` (~0.16s).
Dump: `research/cycle_ji.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/IT/JD/JF/JH (\(n<64\); covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso1_lift5` is `iso1_even` on even \(n>0\))

For \(n<64\), every even isolated one has
`iso1_lift5==iso1_even`. Census \(n_{\mathrm{iso}}=461\): seed
\(1\), odd \(45\), even \(415\) split \(00011\) \(115\), \(11000\)
\(115\), \(01110\) \(141\), \(10101\) \(44\).

## Lemma (cob-stretch of `iso3_even` is `LIFT1`)

\(001\mapsto 00011\), \(100\mapsto 11000\), \(010\mapsto 01110\),
\(111\mapsto 10101\). This is Cycle JF’s cob-stretch evaluated on
Cycle JH’s slot/\(v_2\) 3-window.

## Lemma (covering even-\(n\) slot `LIFT1`)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\), odd \(741\), even \(7030\)). Even windows
\(00011\) \(2011\), \(11000\) \(1912\), \(01110\) \(2373\),
\(10101\) \(734\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(v_2\)-odd interiors lift from \(10101\): at \(k=0\), \(s=5\),
\(n=2\), \(j=2\), \(v_2=1\), slot \((0,1,1)\), window \(01110\),
\(p=6\). Offset \(0\) lifts from \(11000\): at \(k=0\), \(s=5\),
\(n=2\), \(j=0\), slot \((0,1,0)\), window \(00011\), \(p=10\).
\(v_2\)-even interiors lift from \(01110\): at \(k=1\), \(s=11\),
\(n=4\), \(j=4\), \(v_2=2\), slot \((0,1,1)\), window \(10101\),
\(p=12\).

## Verdict

`LEMMA` (`iso1_lift5` is `iso1_even` on even \(n>0\); cob-stretch of
`iso3_even` is `LIFT1`; covering even-\(n\) slot `LIFT1`).
`KILLED` (\(v_2\)-odd interiors lift from \(10101\); offset \(0\)
lifts from \(11000\); \(v_2\)-even interiors lift from \(01110\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ji.md` (this note)
- `research/cycle_ji.py`
- `research/cycle_ji.json`
