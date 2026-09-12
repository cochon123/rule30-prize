# Cycle JV: cob-stretch of `pair_dbl_threes` recovers `pair_dbl_fives`

`cob_lift5` of \(001/010\) is \(00011/01110\); `cob_lift5` of
\(010/100\) is \(01110/11000\). So cob of `pair_dbl_threes` equals
`pair_dbl_fives`. Cob of even-\(j\) is **not** the odd-\(j\) fives.
Cob of \(001\) is **not** \(01110\). Cob of `pair_dbl_threes` **is**
`pair_dbl_fives`. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: cob-stretching doubled pair 3-windows still
leaves packed AND on those columns (and on pairs), so covering
never-fail stays open. This recovers Cycle JL from Cycles JS+JU.

Helper: `cob_pair`. Certify:
`python3 research/cycle_jv.py --certify` (~0.16s).
Dump: `research/cycle_jv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/JD/JL/JS/JU (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`cob_pair` maps even/odd 3-windows onto `LIFT1`)

\(001/010\mapsto 00011/01110\). \(010/100\mapsto 01110/11000\).

## Lemma (`cob_pair` of `pair_dbl_threes` is `pair_dbl_fives`)

For \(n<64\), every consecutive \(G=1\) pair at \(j\) has
`cob_pair(pair_dbl_threes(n,j))==pair_dbl_fives(n,j)`. Census
\(n_{11}=512\): even \(j\) \(256\), odd \(j\) \(256\).

## Lemma (covering cob-pair)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\); even \(j\) \(4292\), odd \(j\) \(4285\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

Cob of even-\(j\) is odd-\(j\) fives: at \(k=1\), \(s=9\), \(n=5\),
\(j=0\), windows \(001/010\) cob-stretch to \(00011/01110\), not
\(01110/11000\), \(p=20\). Cob of \(001\) is \(01110\):
`cob_lift5(001)=00011`. Cob of `pair_dbl_threes` is not
`pair_dbl_fives`: same first witness.

## Verdict

`LEMMA` (`cob_pair` maps even/odd 3-windows onto `LIFT1`; `cob_pair`
of `pair_dbl_threes` is `pair_dbl_fives`; covering cob-pair).
`KILLED` (cob of even-\(j\) is odd-\(j\) fives; cob of \(001\) is
\(01110\); cob of `pair_dbl_threes` is not `pair_dbl_fives`).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jv.md` (this note)
- `research/cycle_jv.py`
- `research/cycle_jv.json`
