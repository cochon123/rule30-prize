# Cycle JQ: doubling \(n\) maps isolated-one iso3 by flipping interiors

`iso3_even(2n,2j)` equals `iso3_double` of the parent 3-window for
every isolated one with \(n>0\). Ends \(001\) and \(100\) stay.
Interiors swap \(010\) with \(111\). Odd-\(n\) \(111\) doubles to
\(010\). Interiors do **not** stay. Ends do **not** swap. Odd iso
does **not** stay \(111\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: flipping iso3 interiors still leaves packed AND
on those columns (and on pairs), so covering never-fail stays open.
This is the 3-window shadow of Cycle JJ’s `LIFT1` doubling (cob-stretch
sends \(010\leftrightarrow 111\) to \(01110\leftrightarrow 10101\)).

Helper: `iso3_double`. Certify:
`python3 research/cycle_jq.py --certify` (~0.16s).
Dump: `research/cycle_jq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/JF/JH/JP (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso3_even(2n,2j)` is `iso3_double` of the parent)

For \(n<64\), every isolated one with \(n>0\) has
`iso3_even(2n,2j)==iso3_double(iso3_parent(n,j))`. Census
\(n_{\mathrm{iso}}=461\): seed \(1\), stay \(001\) \(115\), stay
\(100\) \(115\), flip \(010\to 111\) \(141\), flip \(111\to 010\)
\(89\).

## Lemma (`iso3_double` fixes ends and swaps interiors)

\(001\) and \(100\) stay. \(010\leftrightarrow 111\). Odd-\(n\)
isolated ones (all \(111\)) therefore double to \(010\).

## Lemma (covering doubling)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\)); doubling \(7771\): stay \(001\) \(2011\),
stay \(100\) \(1912\), flip \(010\) \(2373\), flip \(111\) \(1475\).
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Interiors stay: at \(k=1\), \(s=15\), \(n=2\), \(j=2\) vs \(n=4\),
\(j=4\), windows \(010\) vs \(111\), \(p=16\) and \(p=12\). Ends
swap: at \(k=1\), \(s=15\), \(n=2\), \(j=0\) vs \(n=4\), \(j=0\),
window \(001\) stays, \(p=20\). Odd iso stays \(111\): at \(k=2\),
\(s=17\), \(n=3\), \(j=3\) vs \(n=6\), \(j=6\), windows \(111\) vs
\(010\), \(p=18\) and \(p=12\).

## Verdict

`LEMMA` (`iso3_even(2n,2j)` is `iso3_double` of the parent;
`iso3_double` fixes ends and swaps interiors; covering doubling).
`KILLED` (interiors stay; ends swap; odd iso stays \(111\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jq.md` (this note)
- `research/cycle_jq.py`
- `research/cycle_jq.json`
