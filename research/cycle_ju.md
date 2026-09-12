# Cycle JU: cob-stretch commutes with reverse, so even-\(n\) dual `iso1_even` is reverse

`freshman_lift5(iso3_rev(three),` odd parent\()\) equals `lift5_rev` of
the cob-stretch. Dual of even-\(n\) `iso1_even` is therefore
`lift5_rev`, recovering Cycle JE on even \(n\) from Cycles JP+JI.
Cob does **not** fail to commute. Dual of \(00011\) does **not** stay
\(00011\). Dual `iso1_even` **is** the reverse. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: commuting cob-stretch with reverse still leaves
packed AND on those columns (and on pairs), so covering never-fail
stays open.

Helper: `cob_lift5`. Certify:
`python3 research/cycle_ju.py --certify` (~0.22s).
Dump: `research/cycle_ju.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/JE/JF/JH/JI/JP/JT (\(n<64\); covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`cob_lift5` commutes with reverse)

On the four iso3 windows, `cob_lift5(iso3_rev(three))` equals
`lift5_rev(cob_lift5(three))`. Maps \(001\mapsto 00011\),
\(010\mapsto 01110\), \(100\mapsto 11000\), \(111\mapsto 10101\).

## Lemma (dual even-\(n\) `iso1_even` is `lift5_rev`)

For \(n<64\), every even-\(n>0\) isolated one at \(j\) has
`iso1_even(n,2n-j)==lift5_rev(iso1_even(n,j))`. Census \(415\):
palindrome \(185\), swap \(230\); \(00011\) \(115\), \(01110\) \(141\),
\(11000\) \(115\), \(10101\) \(44\).

## Lemma (covering dual-in-support cob-reverse)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): even isolated ones
\(7030\); dual-in-support \(5833\) (palindrome \(2537\), swap
\(3296\)); windows \(00011\) \(1648\), \(01110\) \(1935\), \(11000\)
\(1648\), \(10101\) \(602\). Matches Cycle JP’s even iso3 census via
cob-stretch. Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Cob does not commute with reverse: `cob_lift5(rev(001))=11000=`
`rev(cob_lift5(001))`. Dual of \(00011\) stays \(00011\): at \(k=1\),
\(s=15\), \(n=2\), \(j=0\) vs \(4\), windows \(00011\) vs \(11000\),
\(p=20\) and \(p=12\). Dual `iso1_even` is not reverse: same first
witness.

## Verdict

`LEMMA` (`cob_lift5` commutes with reverse; dual even-\(n\)
`iso1_even` is `lift5_rev`; covering dual-in-support cob-reverse).
`KILLED` (cob does not commute; dual of \(00011\) stays \(00011\);
dual `iso1_even` is not reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ju.md` (this note)
- `research/cycle_ju.py`
- `research/cycle_ju.json`
