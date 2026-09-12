# Cycle JS: doubling a consecutive \(G=1\) pair splits into iso3 windows

`iso3_even(2n,2j)` and `iso3_even(2n,2j+2)` are \(001/010\) for even
\(j\) and \(010/100\) for odd \(j\). The pair does **not** stay a
pair. Even \(j\) does **not** take the odd-\(j\) windows. The two
windows do **not** determine kind. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: splitting a pair into isolated-one 3-windows still
leaves packed AND on those columns (and on pairs), so covering
never-fail stays open. This is the 3-window shadow of Cycle JL’s
`pair_dbl_fives` (cob-stretch sends \(001/010/100\) to
\(00011/01110/11000\)).

Helper: `pair_dbl_threes`. Certify:
`python3 research/cycle_js.py --certify` (~0.16s).
Dump: `research/cycle_js.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IR/JF/JH/JR (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (a pair doubles to two isolated ones)

For \(n<64\), every consecutive \(G=1\) pair at \((n,j)\) (all odd
\(n\)) has isolated ones at \((2n,2j)\) and \((2n,2j+2)\), with the
odd midpoint vanishing. Census \(n_{\mathrm{g11}}=512\): left \(141\),
right \(141\), iso \(230\) (even \(j\) \(115\), odd \(j\) \(115\)).

## Lemma (`pair_dbl_threes` is \(j\)-parity)

Even \(j\) maps to \(001/010\). Odd \(j\) maps to \(010/100\).
Left is always even \(j\); right is always odd \(j\); iso takes both.

## Lemma (covering pair-split)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\) (left \(2380\), right \(2380\), iso \(3817\)); even \(j\)
\(4292\), odd \(j\) \(4285\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Pair stays a pair: at \(k=1\), \(s=9\), \(n=5\), \(j=0\) vs \(n=10\),
\(j=0\) and \(j=2\), windows \(001/010\), \(p=20,20,16\). Even \(j\)
takes odd-\(j\) windows: the same witness is \(001/010\), not
\(010/100\). Windows determine kind: left at \(k=1\), \(s=9\),
\(n=5\), \(j=0\) and iso at \(s=5\), \(n=7\), \(j=0\) share
\(001/010\), \(p=20\).

## Verdict

`LEMMA` (a pair doubles to two isolated ones; `pair_dbl_threes` is
\(j\)-parity; covering pair-split).
`KILLED` (pair stays a pair; even \(j\) takes odd-\(j\) windows;
windows determine kind).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_js.md` (this note)
- `research/cycle_js.py`
- `research/cycle_js.json`
