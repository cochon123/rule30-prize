# Cycle IU: dual \(j\mapsto 2n-j\) palindromes core `IMAGE_ONES` slots

A core slot \((start,r,d)\) maps to \((2m-start-r+1,r,2r-d)\) on the
odd core's parent \(m\). Dual **preserves** \(r\). The Green center
is **self-dual** of type \((r,d)\in\{(1,1),(3,3)\}\). \(n=0\) stays
**seed**. Dual does **not** change parent run length. Dual start is
**not** \(2m-start\). Dual of even-\(n\) \(G=1\) is **not** a parent
slot. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: dual slots still leave packed AND on every slot
type (and the seed), so covering never-fail stays open.

Helper: `dual_slot`, `dual_core_slot`. Certify:
`python3 research/cycle_iu.py --certify`.
Dump: `research/cycle_iu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IS/IT (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (dual core slot is `dual_slot`)

For \(0\le n<64\), every \(G=1\) satisfies
`g1_core_slot(n,2n-j)==dual_core_slot(n,j)`. Census \(n_{G=1}=1344\):
seed once, and \(1343\) dual hits. `IMAGE_ONES` offsets are closed
under \(d\mapsto 2r-d\).

## Lemma (center is self-dual of type \((1,1)\) or \((3,3)\))

For \(n>0\), the center \(G(n,n)=1\) has `dual_core_slot==g1_core_slot`,
with \((r,d)=(1,1)\) count \(42\) and \((3,3)\) count \(21\). Never
run-2. Seed \(n=0\) maps to seed.

## Lemma (covering dual slots)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support dual pairs
\(9692\) (centers \(748\), seed pairs \(14\)), AND xor \(3246\).
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Dual changes parent run length: at \(k=1\), \(s=9\), \(n=1\),
\(j=0\) vs \(2\), slots \((0,1,0)\) vs \((0,1,2)\), \(p=12\) and
\(p=8\). Dual start is \(2m-start\): at \(k=2\), \(s=9\), \(n=7\),
\(j=4\) vs \(10\), slots \((0,2,4)\) vs \((5,2,0)\), naive start
\(6\), \(p=16\) and \(p=4\). Dual of even-\(n\) \(G=1\) is a parent
slot: at \(k=1\), \(s=7\), \(n=2\), \(j=0\) vs \(4\), core slots
\((0,1,0)\) vs \((0,1,2)\), `g1_slot` none, \(p=12\) and \(p=4\).

## Verdict

`LEMMA` (dual core slot is `dual_slot`; center is self-dual of type
\((1,1)\) or \((3,3)\); covering dual slots).
`KILLED` (dual changes parent run length; dual start is \(2m-start\);
dual of even-\(n\) \(G=1\) is a parent slot).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_iu.md` (this note)
- `research/cycle_iu.py`
- `research/cycle_iu.json`
