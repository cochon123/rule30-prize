# Cycle IY: dual of consecutive \(G=1\) pairs swaps left/right, keeps iso

Pair \((j,j+1)\) dualizes to \((2n-j-1,2n-j)\). `KIND_DUAL` sends
left to **right**, right to **left**, iso to **iso**. Dual of left
is **not** left. Dual of iso is **not** a triple. Dual of a pair
**is** a pair. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: dual pair kinds still leave packed AND xor on
those pairs, so covering never-fail stays open.

Helper: `KIND_DUAL`, `dual_pair_start`, `dual_kind`. Certify:
`python3 research/cycle_iy.py --certify` (~0.20s).
Dump: `research/cycle_iy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IX (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (dual pair kind is `KIND_DUAL`)

For \(n<64\), every consecutive \(G=1\) pair at \(j\) has
`g_run_kind(n,2n-j-1)==dual_kind(g_run_kind(n,j))`. Census
\(n_{11}=512\): left \(141\), right \(141\), iso \(230\).

## Lemma (`KIND_DUAL` swaps left/right and preserves iso)

`left↔right`, `iso↦iso`. `slot_kind` agrees on the dual start.

## Lemma (covering dual pair kinds)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
whose dual is also in-support \(6968\) (left \(1942\), right
\(1942\), iso \(3084\); pair-start AND xor \(2586\)). Clipped pairs
from Cycle IX’s \(8577\) are omitted. Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

Dual of left is left: at \(k=0\), \(s=3\), \(n=1\), \(j=0\) vs
\(1\), kinds `left` vs `right`, \(p=6\) and \(p=4\). Dual of iso is
a triple: at \(k=2\), \(s=9\), \(n=7\), \(j=3\) vs \(10\), both
`iso`, \(p=18\) and \(p=4\). Dual of a pair is not a pair: same
first witness, dual is `right`.

## Verdict

`LEMMA` (dual pair kind is `KIND_DUAL`; `KIND_DUAL` swaps left/right
and preserves iso; covering dual pair kinds).
`KILLED` (dual of left is left; dual of iso is a triple; dual of a
pair is not a pair).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_iy.md` (this note)
- `research/cycle_iy.py`
- `research/cycle_iy.json`
