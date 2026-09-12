# Cycle IK: Green avoids the four 6-windows that lift to a 4-run

\(G(n,j)=G(n-1,j)\oplus G(n-1,j-1)\oplus G(n-1,j-2)\). The 6-windows
that map to \(1111\) under that trinomial are \(001001\), \(010010\),
\(100100\), \(111111\) (odd-weight \((abc)^2\)). None of those windows
appear in \(G\) (\(n<64\), and covering clocks). This is the
mechanism of Cycle IJ’s no-4-run. \(G\) **does** have even-weight
period-3 6-windows. The recurrence is **not** two-term. \(G\) **does**
contain \(001\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: avoiding lift-4 windows still leaves packed AND on
Green pairs and triples, so covering never-fail stays open.

Helper: `g_step`, `g6`, `LIFT4`. Certify:
`python3 research/cycle_ik.py --certify`.
Dump: `research/cycle_ik.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IJ (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (Green trinomial recurrence)

For \(1\le n<64\) and \(j\in[-2,2n+2]\),
`G(n,j)==g_step(n,j)`. Census \(n_{\mathrm{rec}}=4347\).

## Lemma (Green has no lift-4 6-windows)

Padded 6-windows of \(G(n,\cdot)\) for \(n<64\) never lie in
`LIFT4`. Census \(n_{\mathrm{win}}=4032\), \(n_{\mathrm{lift}}=0\).

## Lemma (covering clocks have no lift-4 6-windows)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): every clock \(n\) has
no `LIFT4` window. Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(G\) never has a period-3 6-window: at \(k=1\), \(s=5\), \(n=7\),
\(j=1\), window \(101101\), \(p=18\). Recurrence is two-term (omit
\(j-2\)): at \(k=0\), \(s=5\), \(n=2\), \(j=2\), two-term \(0\) vs
\(G=1\). \(G\) never contains \(001\): at \(k=2\), \(s=15\), \(n=4\),
\(j=2\), \(p=20\).

## Verdict

`LEMMA` (Green trinomial recurrence; Green has no lift-4 6-windows;
covering clocks have no lift-4 6-windows).
`KILLED` (\(G\) never has a period-3 6-window; recurrence is
two-term; \(G\) never contains \(001\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ik.md` (this note)
- `research/cycle_ik.py`
- `research/cycle_ik.json`
