# Cycle HP: quadruple-AND 10-tuples are the `TRIPLE_AND` overlap chains

Four consecutive odd-\(s\) AND iff the even-\(s\) 10-tuple is one of
\(0010010010\), \(0010010011\), \(0100100100\), \(1001001001\). Those
are the overlapping pairs of Cycle HO's four triple-AND 8-tuples.
Quad-AND is **not** absent on covering windows. It is **not** only
\(0010010010\). It is **not** only when all four \(G=1\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a 4-row quad-AND table does not give a closed
form along Green ones, so covering never-fail stays open.

Helper: `QUAD_AND`. Certify: `python3 research/cycle_hp.py --certify` (~0.16s).
Dump: `research/cycle_hp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HH/HO
(1024-row table; covering \(k\le 6\); no Fermat table, no extra window,
no \(n_0=16\) window).

## Lemma (quad-AND iff four 10-tuples; overlap of `TRIPLE_AND`)

1024-row identity. Each quad 10-tuple is two overlapping triple-AND
8-tuples. Certified on \(J_6,J_{10}\) for \(k\le 6\). Odd-\(s\) \(J\)
XOR matches Cycles HF/HG.

## Killed

No covering quad-AND: at \(k=3\), \(s=45\), \(n=1\), \(j=2\),
\(p=44\), ten \(0010010010\). Quad-AND only \(0010010010\): at
\(k=3\), \(s=31\), \(n=24\), \(j=9\), \(p=62\), ten \(0100100100\).
Quad-AND only when all four \(G=1\): the \(k=3\) witness has
\(G=(1,0,0,0)\).

## Verdict

`LEMMA` (quad-AND iff four 10-tuples; overlap of `TRIPLE_AND`).
`KILLED` (no covering quad-AND; quad-AND only \(0010010010\);
quad-AND only when all four \(G=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hp.md` (this note)
- `research/cycle_hp.py`
- `research/cycle_hp.json`
