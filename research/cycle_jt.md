# Cycle JT: dual of `pair_dbl_threes` is reverse-swap of the two iso3 windows

Palindrome dual \(j\mapsto 2n-j-1\) sends even-\(j\) \(001/010\)
to odd-\(j\) \(010/100\). Dual of even-\(j\) windows is **not**
even-\(j\). Dual of odd-\(j\) windows is **not** odd-\(j\). Dual
`pair_dbl` **is** the reverse-swap. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: reverse-swapping doubled pair 3-windows still
leaves packed AND on those columns (and on pairs), so covering
never-fail stays open. This is the 3-window shadow of Cycle JN’s
`pair_dbl_rev` on `LIFT1`.

Helper: `pair_dbl_rev`. Certify:
`python3 research/cycle_jt.py --certify` (~0.16s).
Dump: `research/cycle_jt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IY/JH/JS (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`pair_dbl_rev` swaps even/odd windows)

\(001/010\leftrightarrow 010/100\). Twice is the identity.

## Lemma (dual `pair_dbl_threes` is `pair_dbl_rev`)

For \(n<64\), every consecutive \(G=1\) pair at \(j\) has
`pair_dbl_threes(n,2n-j-1)==pair_dbl_rev(pair_dbl_threes(n,j))`. Census
\(n_{11}=512\): even \(j\) \(256\), odd \(j\) \(256\).

## Lemma (covering dual-in-support reverse-swap)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
whose dual is also in-support \(6968\) (even \(j\) \(3484\), odd
\(j\) \(3484\)). Clipped pairs from Cycle JS’s \(8577\) are omitted.
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Dual of even-\(j\) windows stays even-\(j\): at \(k=0\), \(s=3\),
\(n=1\), \(j=0\) vs \(1\), windows \(001/010\) vs \(010/100\),
\(p=6\) and \(p=4\). Dual of odd-\(j\) windows stays odd-\(j\): at
\(k=0\), \(s=3\), \(n=1\), \(j=1\) vs \(0\), windows \(010/100\) vs
\(001/010\), \(p=4\) and \(p=6\). Dual `pair_dbl` is not reverse-swap:
same first witness.

## Verdict

`LEMMA` (`pair_dbl_rev` swaps even/odd windows; dual
`pair_dbl_threes` is `pair_dbl_rev`; covering dual-in-support
reverse-swap).
`KILLED` (dual of even-\(j\) windows stays even-\(j\); dual of
odd-\(j\) windows stays odd-\(j\); dual `pair_dbl` is not
reverse-swap).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jt.md` (this note)
- `research/cycle_jt.py`
- `research/cycle_jt.json`
