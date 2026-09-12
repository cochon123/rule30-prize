# Cycle HO: triple-AND 8-tuples are the `BOTH_AND` overlap chains

Three consecutive odd-\(s\) AND iff the even-\(s\) 8-tuple is one of
\(00100100\), \(01001001\), \(10010010\), \(10010011\). Those are
the overlapping pairs of Cycle HN's four both-AND 6-tuples.
Triple-AND is **not** absent on covering windows. It is **not** only
\(10010011\). It is **not** only when all three \(G=1\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a 4-row triple-AND table does not give a closed
form along Green ones, so covering never-fail stays open.

Helper: `TRIPLE_AND`. Certify: `python3 research/cycle_ho.py --certify` (~0.14s).
Dump: `research/cycle_ho.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HH/HN
(256-row table; covering \(k\le 6\); no Fermat table, no extra window,
no \(n_0=16\) window).

## Lemma (triple-AND iff four 8-tuples; overlap of `BOTH_AND`)

256-row identity. Each triple 8-tuple is two overlapping both-AND
6-tuples. Certified on \(J_6,J_{10}\) for \(k\le 6\). Odd-\(s\) \(J\)
XOR matches Cycles HF/HG.

## Killed

No covering triple-AND: at \(k=2\), \(s=19\), \(n=2\), \(j=2\),
\(p=20\), eight \(10010011\). Triple-AND only \(10010011\): at
\(k=4\), \(s=37\), \(n=29\), \(j=25\), \(p=46\), eight \(00100100\).
Triple-AND only when all three \(G=1\): the \(k=2\) witness has
\(G=(1,0,1)\).

## Verdict

`LEMMA` (triple-AND iff four 8-tuples; overlap of `BOTH_AND`).
`KILLED` (no covering triple-AND; triple-AND only \(10010011\);
triple-AND only when all three \(G=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ho.md` (this note)
- `research/cycle_ho.py`
- `research/cycle_ho.json`
