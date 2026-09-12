# Cycle JO: doubling \(n\) preserves `g1_core_slot` on the stretched column

`g1_core_slot(2n,2j)` equals `g1_core_slot(n,j)` for every \(G=1\)
with \(n>0\). Doubling does **not** change the core slot. Left
doubling does **not** change \(r\). Doubling is **not** `g1_slot` of
\(2n\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a doubling-invariant core slot still leaves packed
AND on those columns (and on pairs), so covering never-fail stays
open.

Certify: `python3 research/cycle_jo.py --certify` (~0.16s).
Dump: `research/cycle_jo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IS/IT/JN (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`g1_core_slot(2n,2j)` equals the parent)

For \(n<64\), every \(G=1\) with \(n>0\) has
`g1_core_slot(2n,2j)==g1_core_slot(n,j)`. Census \(n_{G=1}=1344\):
seed \(1\), hit \(1343\), matching Cycle IT’s \((r,d)\) counts.

## Lemma (covering slot census is stable)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) \(22659\)
(seed \(14\), hit \(22645\)). Doubling preserves every core slot;
\((r,d)\) counts match Cycle IT. Odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Killed

Doubling changes the core slot: at \(k=0\), \(s=3\), \(n=1\),
\(j=0\) vs \(n=2\), \(j=0\), slot \((1,0)\) stays, \(p=6\). Left
doubling changes \(r\): the same witness keeps \(r=1\), not \(r=2\).
Doubling is `g1_slot` of \(2n\): `g1_slot(2,0)` is `None` because
\(n=2\) is even.

## Verdict

`LEMMA` (`g1_core_slot(2n,2j)` equals the parent; covering slot
census is stable).
`KILLED` (doubling changes the core slot; left doubling changes
\(r\); doubling is `g1_slot` of \(2n\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jo.md` (this note)
- `research/cycle_jo.py`
- `research/cycle_jo.json`
