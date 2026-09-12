# Cycle JP: dual of `iso3_even` is the bit-reverse of the half 3-window

Palindrome dual \(j\mapsto 2n-j\) reverses even-\(n\) `iso3_even`.
\(001\) swaps with \(100\). \(010\) and \(111\) are palindromes. Dual
of \(001\) is **not** \(001\). Dual of \(010\) is **not** \(001\).
Dual iso3 **is** the reverse. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: reversing even-\(n\) isolated-one 3-windows still
leaves packed AND on those columns (and on pairs), so covering
never-fail stays open.

Helper: `iso3_rev`. Certify:
`python3 research/cycle_jp.py --certify` (~0.19s).
Dump: `research/cycle_jp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/JE/JF/JH/JO (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso3_rev` swaps ends and fixes interiors)

\(001\leftrightarrow 100\). \(010\) and \(111\) are palindromes.

## Lemma (dual `iso3_even` is `iso3_rev`)

For \(n<64\), every even-\(n>0\) isolated one at \(j\) has
`iso3_even(n,2n-j)==iso3_rev(iso3_even(n,j))`. Census \(415\):
\(001\) \(115\), \(010\) \(141\), \(100\) \(115\), \(111\) \(44\);
palindrome \(185\), swap \(230\).

## Lemma (covering dual-in-support reverse)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): even isolated ones
\(7030\); dual-in-support \(5833\) (palindrome \(2537\), swap
\(3296\)); windows \(001\) \(1648\), \(010\) \(1935\), \(100\)
\(1648\), \(111\) \(602\). Clipped columns from Cycle JI’s \(7030\)
are omitted. Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Dual of \(001\) is \(001\): at \(k=1\), \(s=15\), \(n=2\), \(j=0\) vs
\(4\), windows \(001\) vs \(100\), \(p=20\) and \(p=12\). Dual of
\(010\) is \(001\): at \(k=1\), \(s=15\), \(n=2\), \(j=2\), window
\(010\) stays, \(p=16\). Dual iso3 is not reverse: same first
witness, \(100=\mathrm{rev}(001)\).

## Verdict

`LEMMA` (`iso3_rev` swaps ends and fixes interiors; dual
`iso3_even` is `iso3_rev`; covering dual-in-support reverse).
`KILLED` (dual of \(001\) is \(001\); dual of \(010\) is \(001\);
dual iso3 is not reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jp.md` (this note)
- `research/cycle_jp.py`
- `research/cycle_jp.json`
