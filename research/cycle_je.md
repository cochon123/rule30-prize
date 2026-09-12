# Cycle JE: dual of `iso1_lift5` is the bit-reverse of the parent 5-window

Palindrome dual \(j\mapsto 2n-j\) reverses the parent 5-window. That
swaps \(11000\) with \(00011\). Windows \(01110\) and \(10101\) are
palindromes, so odd-\(n\) isolated ones (all \(10101\)) are
self-dual on the window. Dual of \(00011\) is **not** \(00011\).
Dual of \(10101\) is **not** \(00011\). Dual lift **is** the
reverse. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: reversing isolated-one parent windows still
leaves packed AND on those columns (and on pairs), so covering
never-fail stays open.

Helper: `lift5_rev`, `dual_iso_start`. Certify:
`python3 research/cycle_je.py --certify`.
Dump: `research/cycle_je.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/JD (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (dual `iso1_lift5` is `lift5_rev`)

For \(n<64\), every isolated one with \(n>0\) at \(j\) has
`iso1_lift5(n,2n-j)==lift5_rev(iso1_lift5(n,j))`. Census
\(n_{\mathrm{iso}}=461\): seed \(1\), palindrome windows \(230\),
swap windows \(230\).

## Lemma (`lift5_rev` swaps \(11000/00011\); \(01110\) and \(10101\) are palindromes)

`11000↔00011`. Odd-\(n\) isolated ones stay \(10101\).

## Lemma (covering dual-in-support reverse)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\)); dual-in-support \(6442\) (palindrome
\(3146\), swap \(3296\)). Clipped columns from Cycle JD’s \(7785\)
are omitted. Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

Dual of \(00011\) is \(00011\): at \(k=1\), \(s=15\), \(n=2\),
\(j=0\) vs \(4\), windows \(00011\) vs \(11000\), \(p=20\) and
\(p=12\). Dual of \(10101\) is \(00011\): at \(k=0\), \(s=3\),
\(n=3\), \(j=3\), self-dual \(10101\), \(p=4\). Dual lift is not
reverse: same first witness, \(11000=\mathrm{rev}(00011)\).

## Verdict

`LEMMA` (dual `iso1_lift5` is `lift5_rev`; `lift5_rev` swaps
\(11000/00011\); covering dual-in-support reverse).
`KILLED` (dual of \(00011\) is \(00011\); dual of \(10101\) is
\(00011\); dual lift is not reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_je.md` (this note)
- `research/cycle_je.py`
- `research/cycle_je.json`
