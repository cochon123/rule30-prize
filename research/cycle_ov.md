# Cycle OV: covering \(n=8t+7\) rem xor at \(k\) equals covering rem at \(k-2\)

Cycle OT folds clip-removed pal-right \(S(8t+7)\) at \(5\cdot 2^k\)
to rem\((2t+1)\) at \(5\cdot 2^{k-2}\). Covering \(n=8t+7\) in
\([0,4U)\) is \(t=0,\ldots,2^{k-1}-1\), so the parent \(2t+1\)
runs through every odd integer below \(2^k\). Covering at scale
\(k-2\) is exactly \(n\in[0,2^k)\) at the same
\(j_{\max}=5\cdot 2^{k-2}\). Even-\(n\) rem vanishes. An
unclipped child \(2(8t+7)\le 5\cdot 2^k\) forces the parent
\(2t+1\le 5\cdot 2^{k-3}-1\), hence unclipped too. Therefore the
covering \(n=8t+7\) rem xor at \(k\) equals the covering rem xor
at \(k-2\).

This is **not** one step (\(k=3\): n7 rem \(=0\), tot at \(k=2\)
is \(1\)). **Not** covering \(S\) for all \(k\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_ov.py --certify` (~0.21s).
Dump: `research/cycle_ov.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OR/OS/OT/OU/OG (n7 covering rem recurrence; prefix
OT fold, OU \(n=8t+3\) image, OR unclip window, OG \(E_k\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (covering \(n=8t+7\) indexes odds below \(2^k\))

For \(k\ge 2\), \(t=0,\ldots,2^{k-1}-1\) gives \(n=8t+7<4U\) and
\(\{2t+1\}=\{1,3,\ldots,2^k-1\}\). Status: **lemma**.

## Lemma (covering n7 rem xor recurses by two)

Covering clip-removed xor on \(n=8t+7\) at \(k\) equals covering
clip-removed xor at \(k-2\). Status: **lemma**. Checked on
\(2\le k\le 8\).

## Killed

One-step recurrence: at \(k=3\) the n7 rem xor is \(0\) while
covering rem at \(k=2\) is \(1\).

## Verdict

`LEMMA` (n7 covering index; n7 rem xor \(=\operatorname{rem}(k-2)\);
OT fold; OU \(n=8t+3\) rem).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (one-step rem recurrence).
`PREFIX` (covering \(S\) for all \(k\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ov.md` (this note)
- `research/cycle_ov.py`
- `research/cycle_ov.json`
