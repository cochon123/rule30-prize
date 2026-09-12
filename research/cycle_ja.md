# Cycle JA: isolated Green pairs lift from the two SAT `LIFT2` windows

The 6-windows that trinomial-lift to \(0110\) are
`LIFT2` \(=\{101000,011110,000101,110011\}\). Only \(101000\) (even
\(n\), even \(j\)) and \(000101\) (even \(n\), odd \(j\)) are
freshman-sat. Every isolated pair lifts from those two, predicted by
\(j\) parity (`kind_lift6`). Left of a triple lifts from \(000100\);
right from \(001000\). Iso is **not** from \(011110\). Iso is **not**
a unique SAT window. Left is **not** from \(011111\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: pair-kind parent windows still leave packed AND
on every pair (all three kinds fire all four AND patterns), so
covering never-fail stays open.

Helper: `LIFT2`, `trinomial4`, `pair_lift6`, `kind_lift6`,
`lift2_sat`. Certify:
`python3 research/cycle_ja.py --certify` (~0.14s).
Dump: `research/cycle_ja.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IK/IL/IN (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`LIFT2` has two freshman-sat windows)

Exactly four 6-windows map to \(0110\). Of \(16\) `LIFT2` \(\times\)
parity cases, only \(101000\) on even \(n\), even \(j\) and
\(000101\) on even \(n\), odd \(j\) are freshman-sat.

## Lemma (every iso pair lifts from the SAT windows)

For \(n<64\), every consecutive \(G=1\) pair has
`pair_lift6==kind_lift6`. Isolated pairs \(230\) split \(115/115\) by
\(j\) even/odd into \(000101\) / \(101000\). Left \(141\) all
\(000100\); right \(141\) all \(001000\).

## Lemma (covering pair-kind lifts)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
\(8577\) (iso \(3817\) even-\(j\) \(1912\) / odd-\(j\) \(1905\);
left \(2380\); right \(2380\)). Odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Killed

Iso lifts from \(011110\): at \(k=1\), \(s=5\), \(n=3\), \(j=0\),
parent \(000101\), \(p=12\). Iso from a unique SAT window: at
\(k=1\), \(s=13\), \(n=3\), \(j=5\), parent \(101000\), \(p=10\).
Left lifts from \(011111\): at \(k=0\), \(s=3\), \(n=1\), \(j=0\),
parent \(000100\), \(p=6\).

## Verdict

`LEMMA` (`LIFT2` has two freshman-sat windows; every iso pair lifts
from the SAT windows; covering pair-kind lifts).
`KILLED` (iso lifts from \(011110\); iso from a unique SAT window;
left lifts from \(011111\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ja.md` (this note)
- `research/cycle_ja.py`
- `research/cycle_ja.json`
