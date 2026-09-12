# Cycle JZ: `cob_pair` commutes with reverse-swap

`cob_pair` of `pair_dbl_rev` on iso3 windows equals `pair_dbl_rev`
of `cob_pair`, and that is `pair_dbl_rev` of `pair_dbl_fives`. Cob of
reverse-swap even-\(j\) is **not** even-\(j\) fives. Cob of
reverse-swap \(001/010\) is **not** \(00011/01110\). Cob of
reverse-swap **is** the reverse-swap of cob. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: cob-stretch commuting with reverse-swap still
leaves packed AND on those columns (and on pairs and centers), so
covering never-fail stays open. This recovers Cycle JN from
Cycles JT+JV.

Helper: `cob_revsw`. Certify:
`python3 research/cycle_jz.py --certify` (~0.16s).
Dump: `research/cycle_jz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IY/JL/JN/JS/JT/JV/JY (\(n<64\); covering
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`cob_revsw` maps even/odd 3-windows onto swapped `LIFT1`)

\(001/010\mapsto 01110/11000\). \(010/100\mapsto 00011/01110\).

## Lemma (`cob_pair` commutes with reverse-swap)

For \(n<64\), every consecutive \(G=1\) pair at \(j\) has
`cob_revsw(pair_dbl_threes)==pair_dbl_rev(cob_pair)==pair_dbl_rev(pair_dbl_fives)`,
and that equals `pair_dbl_fives` of the dual start
\(2n-j-1\). Census \(n_{11}=512\): even \(j\) \(256\), odd \(j\)
\(256\).

## Lemma (covering cob-revsw)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\); even \(j\) \(4292\), odd \(j\) \(4285\); dual-in-support
\(6968\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Cob of reverse-swap even-\(j\) is even-\(j\) fives: at \(k=1\),
\(s=9\), \(n=5\), \(j=0\), windows \(001/010\) reverse-swap cob-stretch
to \(01110/11000\), not \(00011/01110\), \(p=20\). Cob of
reverse-swap \(001/010\) is \(00011/01110\): it is \(01110/11000\).
Cob of reverse-swap is not reverse-swap of cob: same first witness
matches.

## Verdict

`LEMMA` (`cob_revsw` maps even/odd 3-windows onto swapped `LIFT1`;
`cob_pair` commutes with reverse-swap; covering cob-revsw).
`KILLED` (cob of reverse-swap even-\(j\) is even-\(j\) fives; cob of
reverse-swap \(001/010\) is \(00011/01110\); cob of reverse-swap is
not reverse-swap of cob).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jz.md` (this note)
- `research/cycle_jz.py`
- `research/cycle_jz.json`
