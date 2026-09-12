# Cycle IB: cob-shape lives on \((z,a,b)\); same class iff even zab Hamming

`cob_shaped` ignores bit \(c\), so two 4-tuples have the same cob class
iff the Hamming weight of differences on \((z,a,b)\) is even. Covering
both-non-cob Hamming 2 **never** includes cob(\(j\)). Hamming 3
**always** includes cob(\(j\)) and never differs only on \((z,a,b)\).
Hamming-2 AND xor is **not** always 1. Hamming-3 XOR is **not** always
1. Hamming-2 dual is **not** reverse. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the zab parity still leaves Hamming-2/3 AND xor
(and the center AND) without a Green-side formula, so covering
never-fail stays open.

Helper: `zab_parity`, `ham2_and_xor`. Certify:
`python3 research/cycle_ib.py --certify` (~0.11s).
Dump: `research/cycle_ib.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HT/HU/HX/HY/IA (16-row table; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (same cob class iff even zab Hamming)

16\(\times\)16: `cob_shaped` of two tuples agrees iff
`zab_parity` \(=0\). Mixed pairs have odd zab Hamming. On Hamming-2
non-cob neighbors, AND xor is \(1\) for slots \((z,a)\), \(\lnot c\)
for \((z,b)\), and \(c\) for \((a,b)\).

## Lemma (Hamming 2 never includes cob(\(j\)))

Packed covering \(J_6,J_{10}\) for \(k\le 6\): both-non-cob Hamming 2
is \(771\) of \(2123\), slots only \((0,1)/(0,2)/(1,2)\)
(\(284+220+267\)), XOR \(533\). Odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (Hamming 3 always includes cob(\(j\)))

Both-non-cob Hamming 3 is \(795\), slots only
\((0,1,3)/(0,2,3)/(1,2,3)\), XOR \(372\). Never \((0,1,2)\).

## Killed

Hamming-2 AND xor always 1: at \(k=0\), \(s=7\), \(n=1\), \(j=0\) vs
\(2\), fours \(0010\) vs \(0100\). Hamming-3 AND xor always 1: at
\(k=3\), \(s=31\), \(n=8\), \(j=0\) vs \(16\), fours \(0010\) vs
\(1001\). Hamming-2 dual equals reverse: at \(k=2\), \(s=33\),
\(n=3\), \(j=0\) vs \(6\), fours \(0100\) vs \(1000\), reverse of
\(0100\) is \(0010\).

## Verdict

`LEMMA` (same cob iff even zab Hamming; Hamming 2 never includes
cob(\(j\)); Hamming 3 always includes cob(\(j\))).
`KILLED` (Hamming-2 xor always 1; Hamming-3 xor always 1; Hamming-2
equals reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ib.md` (this note)
- `research/cycle_ib.py`
- `research/cycle_ib.json`
