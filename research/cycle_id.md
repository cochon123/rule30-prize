# Cycle ID: mixed Hamming 1 never includes cob(\(j\)); Hamming 2 always does

Odd zab Hamming (mixed cob/non-cob) is the complementary slot pattern
of Cycles IA/IB. Mixed Hamming 1 is a single \(z/a/b\) flip, **not**
`flip_c`. Mixed Hamming 2 is that plus cob(\(j\)). Mixed Hamming 3 is
exactly \((z,a,b)\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: mixed slot restrictions still leave mixed AND xor
as the non-cob AND (Cycle HY) without a Green-side formula, and the
center AND remains, so covering never-fail stays open.

Helper: `MIX_HAM1_SLOTS`. Certify: `python3 research/cycle_id.py --certify` (~0.11s).
Dump: `research/cycle_id.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HT/HU/HY/IA/IB/IC (16-row table; covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (mixed Hamming 1 never includes cob(\(j\)))

16\(\times\)16 and packed covering \(J_6,J_{10}\) for \(k\le 6\):
mixed Hamming 1 slots are only \((z)\), \((a)\), \((b)\). Covering
census: Hamming 1 is \(1666\) of \(4383\) mixed pairs.

## Lemma (mixed Hamming 2 always includes cob(\(j\)))

Slots only \((z,c)\), \((a,c)\), \((b,c)\). Covering Hamming 2 is
\(1672\).

## Lemma (mixed Hamming 3 is exactly \((z,a,b)\))

Never includes cob(\(j\)). Covering Hamming 3 is \(521\); Hamming 4
is the \(524\) complements. Mixed XOR \(2216\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

Mixed Hamming 1 equals `flip_c`: at \(k=1\), \(s=5\), \(n=7\),
\(j=6\) vs \(8\), fours \(0001\) vs \(1001\). Mixed Hamming 2 is
c-free: at \(k=2\), \(s=17\), \(n=3\), \(j=1\) vs \(5\), fours
\(0000\) vs \(0011\), slots \((2,3)\). Mixed Hamming 3 never
\((z,a,b)\): at \(k=2\), \(s=19\), \(n=2\), \(j=0\) vs \(4\), fours
\(0111\) vs \(1001\).

## Verdict

`LEMMA` (mixed Hamming 1 slots omit cob(\(j\)); mixed Hamming 2 always
includes cob(\(j\)); mixed Hamming 3 is \((z,a,b)\)).
`KILLED` (mixed Hamming 1 equals `flip_c`; mixed Hamming 2 is c-free;
mixed Hamming 3 never \((z,a,b)\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_id.md` (this note)
- `research/cycle_id.py`
- `research/cycle_id.json`
