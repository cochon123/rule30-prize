# Cycle JX: consecutive \(G=1\) packed pair-shapes take all 64 values

Given `slot_kind` (which fixes `KIND_GREEN4`), covering packed
4-tuple pairs hit every \(64\) stride-2-overlapping shapes per kind;
pair-start 4-tuples hit all \(16\) rows per kind; AND fires all four
`AND_ONES` per kind. Pair packed is **not** a function of kind.
Pair packed is **not** always \(\mathrm{green4}\). Pair-start AND
does **not** vanish. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: consecutive \(G=1\) packed pair-shapes still fire
AND on every `AND_ONES` pattern (and on every pair kind), so covering
never-fail stays open.

Helper: `pair_shape`. Certify:
`python3 research/cycle_jx.py --certify` (~0.14s).
Dump: `research/cycle_jx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HU/II/IN/IZ/JW (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (pair \(\mathrm{green4}\) overlaps stride-2)

For \(n<64\), every consecutive \(G=1\) pair has
\(\mathrm{green4}\) equal to `KIND_GREEN4[kind]` and those two
4-tuples overlap stride-2. Census \(n_{11}=512\): left \(141\),
right \(141\), iso \(230\).

## Lemma (covering pair-shapes hit all 64 per kind)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\) (left \(2380\), right \(2380\), iso \(3817\)); all \(16\)
pair-start 4-tuples and all \(64\) overlapping 6-windows occur on
each kind; stride-2 overlap on all \(8577\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Lemma (pair-start AND fires all four `AND_ONES` per kind)

Pair-start AND \(1711\): left \(431\), right \(534\), iso \(746\).
Both-AND \(463\).

## Killed

Packed pair is a function of kind: at \(k=1\), \(s=5\), \(n=7\),
\(j=6\), packed \(0001/0100\) vs left \(\mathrm{green4}\)
\(1011/1010\), \(p=8\) and \(p=6\). Pair packed always equals
\(\mathrm{green4}\): the same witness. Pair-start AND vanishes: at
\(k=1\), \(s=17\), \(n=1\), \(j=0\), packed \(0100/1101\), AND \(1\),
\(p=20\).

## Verdict

`LEMMA` (pair \(\mathrm{green4}\) overlaps stride-2; covering
pair-shapes hit all \(64\) per kind; pair-start AND fires all four
`AND_ONES` per kind).
`KILLED` (packed pair is a function of kind; pair packed always
equals \(\mathrm{green4}\); pair-start AND vanishes).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jx.md` (this note)
- `research/cycle_jx.py`
- `research/cycle_jx.json`
