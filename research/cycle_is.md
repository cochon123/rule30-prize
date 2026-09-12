# Cycle IS: every odd-\(n\) \(G=1\) is a unique parent-image slot

`IMAGE_ONES` maps run length to \(G=1\) offsets from \(\mathrm{lo}=2\cdot\mathrm{start}\):
\(r=1\mapsto(0,1,2)\), \(r=2\mapsto(0,1,3,4)\),
\(r=3\mapsto(0,1,3,5,6)\). Every \(G=1\) on odd \(n\) is exactly one
`(start, r, offset)`. Odd \(G=1\) does **not** miss the dictionary.
Slots do **not** overlap. Even-\(n\) \(G=1\) is **not** a parent
slot. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: the slot partition still leaves packed AND on
every slot type, so covering never-fail stays open.

Helper: `IMAGE_ONES`, `g1_slot`. Certify:
`python3 research/cycle_is.py --certify`.
Dump: `research/cycle_is.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IP/IR (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (odd-\(n\) \(G=1\) is a unique slot)

For odd \(n<64\), every \(G=1\) has a unique `g1_slot`. Census
\(n_{G=1}=928\): run-1 offsets \(141\) each, run-2 offsets \(70\)
each, run-3 offsets \(45\) each.

## Lemma (`IMAGE_ONES` partitions odd \(G=1\))

The twelve \((r,d)\) keys of `IMAGE_ONES` are disjoint and cover
every odd-\(n\) one.

## Lemma (covering odd-\(n\) \(G=1\) slots)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): odd-\(n\) \(G=1\)
\(15615\), all unique slots (clipped counts: run-1
\(2431/2380/2380\), run-2 \(1194/1171/1168/1168\), run-3
\(766/741/741/738/737\)). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Odd-\(n\) \(G=1\) misses the dictionary: at \(k=0\), \(s=3\),
\(n=1\), \(j=0\), slot \((0,1,0)\), \(p=6\). Two images share a
\(G=1\): at \(k=1\), \(s=5\), \(n=7\), \(j=6\), unique slot
\((3,1,0)\), \(p=8\). Even-\(n\) \(G=1\) is a parent slot: at
\(k=0\), \(s=5\), \(n=2\), \(j=0\), \(G(2,0)=1\), no slot, \(p=10\).

## Verdict

`LEMMA` (odd-\(n\) \(G=1\) is a unique slot; `IMAGE_ONES` partitions
odd \(G=1\); covering odd-\(n\) \(G=1\) slots).
`KILLED` (odd-\(n\) \(G=1\) misses the dictionary; slot overlap;
even-\(n\) \(G=1\) is a parent slot).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_is.md` (this note)
- `research/cycle_is.py`
- `research/cycle_is.json`
