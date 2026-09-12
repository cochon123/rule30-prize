# Cycle JB: dual of `pair_lift6` is the bit-reverse of the parent 6-window

Palindrome dual \(j\mapsto 2n-j-1\) reverses the parent 6-window.
That swaps left \(000100\) with right \(001000\) and the two iso SAT
windows \(000101\) and \(101000\). Unsat `LIFT2` windows \(011110\)
and \(110011\) are palindromes. Dual of left lift is **not** left.
Dual of an iso SAT window is **not** the same window. Dual lift
**is** the reverse. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: reversing parent 6-windows still leaves packed
AND on every pair (all three kinds fire all four AND patterns), so
covering never-fail stays open.

Helper: `lift6_rev`. Certify:
`python3 research/cycle_jb.py --certify`.
Dump: `research/cycle_jb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IY/JA (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (dual `pair_lift6` is `lift6_rev`)

For \(n<64\), every consecutive \(G=1\) pair at \(j\) has
`pair_lift6(n,2n-j-1)==lift6_rev(pair_lift6(n,j))`. Census
\(n_{11}=512\): left \(141\), right \(141\), iso \(230\).

## Lemma (`lift6_rev` swaps left/right and the two iso SAT windows)

`000100↔001000`, `000101↔101000`. Unsat `LIFT2` windows
\(011110\) and \(110011\) are palindromes.

## Lemma (covering dual-in-support reverse)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
whose dual is also in-support \(6968\) (left \(1942\), right
\(1942\), iso \(3084\)). Clipped pairs from Cycle JA’s \(8577\) are
omitted. Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Dual of left lift is left: at \(k=0\), \(s=3\), \(n=1\), \(j=0\) vs
\(1\), windows \(000100\) vs \(001000\), \(p=6\) and \(p=4\). Dual
of iso SAT is the same window: at \(k=1\), \(s=13\), \(n=3\),
\(j=0\) vs \(5\), windows \(000101\) vs \(101000\), \(p=20\) and
\(p=10\). Dual lift is not reverse: same first witness,
\(001000=\mathrm{rev}(000100)\).

## Verdict

`LEMMA` (dual `pair_lift6` is `lift6_rev`; `lift6_rev` swaps
left/right and the two iso SAT windows; covering dual-in-support
reverse).
`KILLED` (dual of left lift is left; dual of iso SAT is the same
window; dual lift is not reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jb.md` (this note)
- `research/cycle_jb.py`
- `research/cycle_jb.json`
