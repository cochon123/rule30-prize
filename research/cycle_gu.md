# Cycle GU: at odd \(s=t_0+2t+1\), even-\(r\) Green is \(G(UQ-t-1,W/2-r/2)\)

Cycle GT showed off-hit times still carry AND. Cycle GM’s freshman
half at hits is the \(t=qU\) slice of a clock that runs at every odd
\(s\): \(m=2(UQ-t-1)\), \(G(m,W-r)=G(UQ-t-1,W/2-r/2)\), and odd-\(r\)
Green vanishes. The clock is **not** the hit Mersenne clock off-hit;
naive half **fails** at even \(s\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: an odd-\(s\) Green clock does not prove covering
never-fail (AND still mixes; even \(s\) still contribute).

Helper: `odd_clock(t,U,Q)` in `research/cycle_gu.py`. Certify:
`python3 research/cycle_gu.py --certify` (~0.01s). Dump:
`research/cycle_gu.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GJ/GM/GT (clock \(k\le 11\); Green
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(m=2(UQ-t-1)\) on every odd \(s\))

Certified \(k\le 11\). Hits \(\delta=1+q\cdot 2U\) recover GM’s
clock \(U(Q-q)-1\).

## Lemma (even-\(r\) Green \(=G(UQ-t-1,W/2-r/2)\); odd-\(r\) Green \(=0\))

Certified \(k\le 6\), all covering \(W\), every odd \(s\) in the
window.

## Killed

Naive half at even \(s\): at \(k=0\), \(W=4U\), \(s=4\), \(r=2\),
\(G=1\) vs \(0\). Off-hit clock equals a hit Mersenne clock: at
\(k=2\), \(W=8U\), \(\delta=3\), clock \(6\notin\{7,3\}\). Reduced
\(G\) identically 1: at \(k=2\), \(W=8U\), \(\delta=3\), \(r=10\),
\(G_{\mathrm{red}}=0\).

## Verdict

`LEMMA` (odd-\(s\) clock \(UQ-t-1\); even-\(r\) Green; odd-\(r\)
Green \(0\)).
`KILLED` (even-\(s\) naive half; off-hit equals hit Mersenne;
reduced \(G\) identically 1).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gu.md` (this note)
- `research/cycle_gu.py`
- `research/cycle_gu.json`
