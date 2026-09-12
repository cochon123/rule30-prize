# Cycle IT: \(n>0\) \(G=1\) is a stretched odd-core `IMAGE_ONES` slot

\(n=2^v\cdot\mathrm{odd}\) sends \(G(n,2^v j')=G(\mathrm{odd},j')\).
Every \(G=1\) with \(n>0\) is `g1_slot(odd, j')`. \(n=0\) is the
**seed** exception, not a core slot. Even \(G=1\) **is** a core slot
after stretch. `g1_slot` on even \(n\) is **not** the formula. Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: core slots still leave packed AND on every slot
type (and the seed), so covering never-fail stays open.

Helper: `odd_core`, `g1_core_slot`. Certify:
`python3 research/cycle_it.py --certify` (~0.32s).
Dump: `research/cycle_it.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IS (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(n>0\) \(G=1\) is a unique core slot)

For \(0\le n<64\), \(G=1\) count \(1344\): seed \(n=0\) once, and
\(1343\) unique `g1_core_slot` values. Slot census: run-1 offsets
\(206\) each, run-2 offsets \(100\) each, run-3 offsets \(65\) each.

## Lemma (\(n=0\) is the seed exception)

`g1_core_slot(0,0)` is `seed`, not an `IMAGE_ONES` triple.

## Lemma (covering core slots)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) \(22659\)
split as core slots \(22645\) plus seed \(14\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

Even \(G=1\) is not a core slot: at \(k=0\), \(s=5\), \(n=2\),
\(j=0\), core \((1,1)\), slot \((0,1,0)\), \(p=10\). `g1_slot` on
even \(n\) is the formula: same witness, `g1_slot` is `None`. Seed
\(n=0\) is a core slot: at \(k=0\), \(s=5\), \(n=0\), \(j=0\),
`seed`, \(p=6\).

## Verdict

`LEMMA` (\(n>0\) \(G=1\) is a unique core slot; \(n=0\) is the seed
exception; covering core slots).
`KILLED` (even \(G=1\) is not a core slot; `g1_slot` on even \(n\) is
the formula; seed \(n=0\) is a core slot).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_it.md` (this note)
- `research/cycle_it.py`
- `research/cycle_it.json`
