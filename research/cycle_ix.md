# Cycle IX: consecutive \(G=1\) kind is the core-slot `IMAGE_ONES` offset

On odd \(n\), `g_run_kind` is `SLOT_KIND[r,d]`: run-1 offset \(0\) is
**left**, offset \(1\) is **right**; run-2 offsets \(0,3\) and run-3
offsets \(0,5\) are **iso**. Even \(n\) and non-pairs are `None`.
Run-1 offset \(1\) is **not** left. Run-2 is **not** a triple. Even
\(n\) has **no** `slot_kind`. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: pair kind still leaves packed AND on every kind
(all three fire), so covering never-fail stays open.

Helper: `SLOT_KIND`, `slot_kind`. Certify:
`python3 research/cycle_ix.py --certify` (~0.40s).
Dump: `research/cycle_ix.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IT (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (consecutive \(G=1\) kind is `slot_kind`)

For \(n<64\), every consecutive \(G=1\) pair has
`g_run_kind==slot_kind`. Census \(n_{11}=512\): left \(141\), right
\(141\), iso \(230\).

## Lemma (`SLOT_KIND` partitions consecutive \(G=1\))

The six keys are disjoint and cover every pair: run-1 offsets
\(141\) each, run-2 offsets \(70\) each, run-3 offsets \(45\) each.

## Lemma (covering slot kind)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
\(8577\) (left \(2380\), right \(2380\), iso \(3817\); clipped
run-2 \(1171/1168\), run-3 \(741/737\)). Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

Run-1 offset \(1\) is left: at \(k=0\), \(s=3\), \(n=1\), \(j=1\),
slot \((0,1,1)\), kind `right`, \(p=4\). Run-2 is a triple: at
\(k=2\), \(s=9\), \(n=7\), \(j=0\), slot \((0,2,0)\), kind `iso`,
\(p=24\). Even \(n\) has a `slot_kind`: at \(k=1\), \(s=7\), \(n=2\),
\(j=0\), `None`, \(p=12\).

## Verdict

`LEMMA` (consecutive \(G=1\) kind is `slot_kind`; `SLOT_KIND`
partitions consecutive \(G=1\); covering slot kind).
`KILLED` (run-1 offset \(1\) is left; run-2 is a triple; even \(n\)
has a `slot_kind`).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ix.md` (this note)
- `research/cycle_ix.py`
- `research/cycle_ix.json`
