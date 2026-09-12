# Cycle IA: both-non-cob Hamming 1 differs only in cob(\(j\)); AND xor is NOT copy(\(j\))

Among non-cob 4-tuples the unique Hamming-1 non-cob neighbor is the
flip of bit \(c\) (the cob(\(j\)) slot). AND xor equals \(\lnot b\)
(NOT copy(\(j\))). Covering both-non-cob Hamming 0 pairs are identical,
so they drop out of \(J\). Hamming-1 XOR is **not** always 1. It is
**not** always 0. Hamming-1 dual is **not** reverse. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: Hamming 1 still leaves Hamming \(2,3\) both-non-cob
disagreements and the center AND, so covering never-fail stays open.

Helper: `flip_c`. Certify: `python3 research/cycle_ia.py --certify` (~0.11s).
Dump: `research/cycle_ia.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HT/HU/HX/HY/HZ (16-row table; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (non-cob Hamming-1 neighbor is `flip_c`)

8 non-cob 4-tuples: the unique Hamming-1 non-cob neighbor is
`flip_c` \((z,a,b,c)\mapsto(z,a,b,1-c)\). Flipping \(z\), \(a\), or
\(b\) lands in cob.

## Lemma (Hamming-1 AND xor is NOT copy(\(j\)))

On those neighbors, `and_clause` xor equals \(\lnot b\). Certified on
packed covering \(J_6,J_{10}\) for \(k\le 6\): both-non-cob
Hamming 1 is \(258\) of \(2123\), all `flip_c`, XOR \(125\). Odd-\(s\)
\(J\) XOR matches Cycles HF/HG.

## Lemma (Hamming 0 both-non-cob AND xor \(0\))

Identical both-non-cob duals contribute 0. Covering census: Hamming 0
is \(299\) of \(2123\).

## Killed

Hamming-1 AND xor always 1: at \(k=3\), \(s=51\), \(n=14\), \(j=12\)
vs \(16\), fours \(0010\) vs \(0011\). Hamming-1 AND xor always 0: at
\(k=4\), \(s=67\), \(n=46\), \(j=20\) vs \(72\), fours \(1000\) vs
\(1001\). Hamming-1 dual equals reverse: same \(0010\) vs \(0011\),
reverse of \(0010\) is \(0100\).

## Verdict

`LEMMA` (non-cob Hamming-1 neighbor is `flip_c`; Hamming-1 AND xor is
NOT copy(\(j\)); Hamming 0 both-non-cob AND xor \(0\)).
`KILLED` (Hamming-1 xor always 1; Hamming-1 xor always 0; Hamming-1
equals reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ia.md` (this note)
- `research/cycle_ia.py`
- `research/cycle_ia.json`
