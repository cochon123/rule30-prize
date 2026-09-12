# Cycle FH: \(J_{18}=J_6\oplus J_{[6U,18U)\to 18U}\)

Cycle FG’s cone bounds did not need \(s\ge 4U\) except as the window.
For every light-cone AND on \(s\in[2U,6U)\),
\(d+8U-2m=2(U+s+1)-p\ge 2U+2>0\) and \(d-8U\le -2U<0\), so the four
Freshman extras of the \(12U\)-shift still leave \([0,2m]\). Hence
\(J_{[2U,6U)\to 6U}=J_{[2U,6U)\to 18U}\). The left-hand side is Cycle
FE’s \(J_6\), and splitting \(J_{18}=J_{[2U,18U)\to 18U}\) gives

\[
J_{18}=J_6\oplus J_{[6U,18U)\to 18U}.
\]

So \(J_6=0\) reduces \(J_{18}\) to the post-\(6U\) remainder, which is
**not** identically 1 (\(k=2\) has \(J_6=J_{18}=0\)). Never-fail on
the candidate slice \(J_6=J_{10}=0\) is exactly
\(J_{[6U,18U)\to 18U}=1\). Do **not** claim that implication for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\).

Not a prize claim: reducing \(J_{18}\) to a later window does not prove
that window is 1 on candidates.

Helper: `python3 research/cycle_fh.py --certify` (~0.32s). Dump:
`research/cycle_fh.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/DS/FE/FF/FG (packed check on \(k=2..6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (cone on \([2U,6U)\))

The same four extras leave the support. Certified on endpoint samples
\(k\le 12\).

## Lemma (\(J_6=J_{[2U,6U)\to 18U}\); split)

Packed AND XOR on \(2\le k\le 6\). Then
\(J_{18}=J_6\oplus J_{[6U,18U)\to 18U}\).

## Killed

\(J_6=0\Rightarrow J_{18}=1\): Cycle FE at \(k=2\) has both 0.

## Verdict

`LEMMA` (cone on \([2U,6U)\); \(J_6\) matches the pre-\(6U\) remainder
to \(18U\); \(J_{18}=J_6\oplus J_{\mathrm{post}}\)).
`KILLED` (\(J_6=0\Rightarrow J_{18}=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fh.md` (this note)
- `research/cycle_fh.py`
- `research/cycle_fh.json`
