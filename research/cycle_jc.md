# Cycle JC: `pair_lift6` is the freshman stretch of the half 3-neighborhood

On odd \(n=2m+1\), the parent 6-window is \(G(m)\) stretched onto the
even indices of \(n-1=2m\). Left/right have half 3-neigh \(010\); iso
even \(j\) has \(011\); iso odd \(j\) has \(110\). Iso half-neigh is
**not** \(010\). Left half-neigh is **not** \(011\). Stretch of
\(010\) at even start is **right**, not left. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the half 3-neigh still leaves packed AND on every
pair (all three kinds fire all four AND patterns), so covering
never-fail stays open.

Helper: `half_pair_k`, `half_neigh3`, `freshman_lift6`, `kind_half3`.
Certify:
`python3 research/cycle_jc.py --certify`.
Dump: `research/cycle_jc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/JA (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (`pair_lift6` is `freshman_lift6` of `kind_half3`)

For \(n<64\), every consecutive \(G=1\) pair has
`half_neigh3==kind_half3` and
`pair_lift6==freshman_lift6(kind_half3, j odd)`. Census
\(n_{11}=512\): left \(141\), right \(141\), iso even-\(j\) \(115\),
iso odd-\(j\) \(115\).

## Lemma (the three `kind_half3` shapes)

Left/right \(010\), iso even \(j\) \(011\), iso odd \(j\) \(110\).
Even-start stretch of \(010\) is \(001000\) (right); odd-start is
\(000100\) (left). Even-start \(110\) is \(101000\); odd-start
\(011\) is \(000101\).

## Lemma (covering half-stretch)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
\(8577\) (left \(2380\), right \(2380\), iso even-\(j\) \(1912\),
iso odd-\(j\) \(1905\)). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Iso half-neigh is \(010\): at \(k=1\), \(s=5\), \(n=3\), \(j=0\),
three \(011\), \(p=12\). Left half-neigh is \(011\): at \(k=0\),
\(s=3\), \(n=1\), \(j=0\), three \(010\), \(p=6\). Stretch of
\(010\) at even start is left: at \(k=0\), \(s=3\), \(n=1\),
\(j=1\), window \(001000\), \(p=4\).

## Verdict

`LEMMA` (`pair_lift6` is `freshman_lift6` of `kind_half3`; the three
`kind_half3` shapes; covering half-stretch).
`KILLED` (iso half-neigh is \(010\); left half-neigh is \(011\);
stretch of \(010\) at even start is left).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jc.md` (this note)
- `research/cycle_jc.py`
- `research/cycle_jc.json`
