# Cycle JM: dual of `half_neigh3` is the bit-reverse of the half 3-window

Palindrome dual \(j\mapsto 2n-j-1\) reverses the half 3-neighborhood.
\(010\) is a palindrome (left/right). Iso even \(011\) swaps with iso
odd \(110\). Dual of \(010\) is **not** \(011\). Dual of \(011\) is
**not** \(011\). Dual half **is** the reverse. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: reversing half 3-neighborhoods still leaves packed
AND on every pair (all three kinds fire all four AND patterns), so
covering never-fail stays open.

Helper: `half3_rev`. Certify:
`python3 research/cycle_jm.py --certify` (~0.14s).
Dump: `research/cycle_jm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IY/JC/JL (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (dual `half_neigh3` is `half3_rev`)

For \(n<64\), every consecutive \(G=1\) pair at \(j\) has
`half_neigh3(n,2n-j-1)==half3_rev(half_neigh3(n,j))`. Census
\(n_{11}=512\): left \(141\), right \(141\), iso even \(115\), iso
odd \(115\); palindrome \(282\), swap \(230\).

## Lemma (`half3_rev` fixes \(010\) and swaps \(011/110\))

Left/right \(010\) is a palindrome. Iso even \(011\leftrightarrow 110\)
iso odd.

## Lemma (covering dual-in-support reverse)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
whose dual is also in-support \(6968\) (left \(1942\), right
\(1942\), iso even \(1542\), iso odd \(1542\)); palindrome \(3884\),
swap \(3084\). Clipped pairs from Cycle JA’s \(8577\) are omitted.
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Dual of \(010\) is \(011\): at \(k=0\), \(s=3\), \(n=1\), \(j=0\) vs
\(1\), window \(010\) stays, \(p=6\) and \(p=4\). Dual of \(011\) is
\(011\): at \(k=1\), \(s=13\), \(n=3\), \(j=0\) vs \(5\), windows
\(011\) vs \(110\), \(p=20\) and \(p=10\). Dual half is not reverse:
same first witness, \(010=\mathrm{rev}(010)\).

## Verdict

`LEMMA` (dual `half_neigh3` is `half3_rev`; `half3_rev` fixes \(010\)
and swaps \(011/110\); covering dual-in-support reverse).
`KILLED` (dual of \(010\) is \(011\); dual of \(011\) is \(011\);
dual half is not reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jm.md` (this note)
- `research/cycle_jm.py`
- `research/cycle_jm.json`
