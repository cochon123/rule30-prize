# Cycle JR: 4-stretch preserves isolated-one iso3 windows

`iso3_even(4n,4j)` equals `iso3_parent(n,j)` for every isolated one
with \(n>0\), because `iso3_double` is an involution. Interiors do
**not** change under 4-stretch. Ends do **not** change. Odd iso does
**not** become \(010\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a period-2 parent 3-window still leaves packed AND
on those columns (and on pairs), so covering never-fail stays open.
This is the 3-window shadow of Cycle JK’s `LIFT1` 4-stretch.

Certify: `python3 research/cycle_jr.py --certify` (~0.16s).
Dump: `research/cycle_jr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/JF/JH/JQ (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso3_double` is an involution)

On the four iso3 windows, `iso3_double` twice is the identity.

## Lemma (`iso3_even(4n,4j)` equals the parent)

For \(n<64\), every isolated one with \(n>0\) has
`iso3_even(4n,4j)==iso3_parent(n,j)`. Census
\(n_{\mathrm{iso}}=461\): seed \(1\), \(001\) \(115\), \(100\)
\(115\), \(010\) \(141\), \(111\) \(89\).

## Lemma (covering 4-stretch)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\)); 4-stretch \(7771\): \(001\) \(2011\),
\(100\) \(1912\), \(010\) \(2373\), \(111\) \(1475\). Odd-\(s\)
\(J\) XOR matches Cycles HF/HG.

## Killed

Interiors change under 4-stretch: at \(k=3\), \(s=43\), \(n=2\),
\(j=2\) vs \(n=8\), \(j=8\), window \(010\) stays, \(p=44\) and
\(p=32\). Ends change: at \(k=3\), \(s=43\), \(n=2\), \(j=0\) vs
\(n=8\), \(j=0\), window \(001\) stays, \(p=48\). Odd iso becomes
\(010\): at \(k=3\), \(s=73\), \(n=3\), \(j=3\) vs \(n=12\),
\(j=12\), window \(111\) stays, \(p=74\) and \(p=56\).

## Verdict

`LEMMA` (`iso3_double` is an involution; `iso3_even(4n,4j)` equals
the parent; covering 4-stretch).
`KILLED` (interiors change under 4-stretch; ends change; odd iso
becomes \(010\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jr.md` (this note)
- `research/cycle_jr.py`
- `research/cycle_jr.json`
