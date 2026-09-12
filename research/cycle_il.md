# Cycle IL: `LIFT4` is unsatisfiable on every freshman 6-window shape of \(G\)

Even \(n\) forces every other Green bit to \(0\); odd \(n\) interleaves
\(G(m)\) with its coboundary. All \(16\) `LIFT4` \(\times\)
(\(n\)-parity, \(j\)-parity) cases contradict those shapes, so \(G\)
has no lift-4 window for every \(n\) (the \(n<64\) census of Cycle IK
is the definition). Even \(n\) **does** vanish on odd indices. Odd
\(n\) **does not**. Odd-\(n\) even-index is **not** \(G(m,k)\) without
the coboundary XOR. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: LIFT4-unsat still leaves packed AND on Green pairs
and triples, so covering never-fail stays open.

Helper: `freshman_shape`. Certify:
`python3 research/cycle_il.py --certify`.
Dump: `research/cycle_il.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IK (\(n<64\) plus \(16\)-row; covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`LIFT4` is freshman-unsat)

For each of the four `LIFT4` 6-windows and each of the four
(\(n\) even/odd, \(j\) even/odd) freshman shapes,
`freshman_shape` is false. Census \(n_{\mathrm{unsat}}=16\).

## Lemma (Green 6-windows have freshman shape)

Padded 6-windows of \(G(n,\cdot)\) for \(n<64\) all satisfy
`freshman_shape`. Census \(n_{\mathrm{win}}=4032\).

## Lemma (covering clocks are LIFT4-unsat)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): every clock \(n\) has
freshman-shaped 6-windows and no `LIFT4`. Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

Even \(n\) has an odd-index Green \(1\): at \(k=0\), \(s=5\), \(n=2\),
\(j=1\), \(G(2,1)=0\), \(p=8\). Odd \(n\) vanishes on odd indices: at
\(k=0\), \(s=3\), \(n=1\), \(j=1\), \(G(1,1)=1\), \(p=4\). Odd-\(n\)
even-index equals \(G(m,k)\) without coboundary XOR: at \(k=0\),
\(s=3\), \(n=3\), \(j=2\), \(G(3,2)=0\) vs \(G(1,1)=1\), \(p=6\).

## Verdict

`LEMMA` (`LIFT4` is freshman-unsat; Green 6-windows have freshman
shape; covering clocks are LIFT4-unsat).
`KILLED` (even \(n\) has an odd-index Green \(1\); odd \(n\) vanishes
on odd indices; odd-\(n\) even-index equals \(G(m,k)\) without
coboundary XOR).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_il.md` (this note)
- `research/cycle_il.py`
- `research/cycle_il.json`
