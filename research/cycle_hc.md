# Cycle HC: in-support remainder Green is GX/GY from \(\rho=T-p\)

On the covering windows \((T,t_0,Q)=(18U,10U,4)\), \((10U,6U,2)\),
\((6U,4U,1)\) the in-support remainder to \(T\) uses the same clock
\(n=UQ-t-1\). Odd-\(s\) even-\(\rho\) Green is \(G(n,\rho/2)\); odd-\(\rho\)
Green is 0. Even-\(s\) is the GY coboundary. Odd-\(s\) \(G\cdot\mathrm{AND}\)
XOR is AND on those \(G=1\) even columns, **not** \(J_{\mathrm{tail}}\)
(\(k=2\): \(0\) vs \(1\)). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: transferring GX/GY to in-support does not prove
covering never-fail (even \(s\) still contribute to \(J_{\mathrm{tail}}\);
AND has no closed form). Together with Cycle HB, \(J_{\mathrm{tail}}\)
is this in-support XOR, not the \(W=16U\) right strip.

Helper: `odd_clock` from `research/cycle_gu.py`. Certify:
`python3 research/cycle_hc.py --certify` (~0.19s). Dump:
`research/cycle_hc.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FR/GN/GU/GX/GY/HB (packed \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (odd-\(s\) even-\(\rho\) \(G(n,\rho/2)\); odd-\(\rho\) \(G=0\))

Certified \(k\le 6\), three covering windows. Dual of Cycle GX with
\(\rho=T-p\).

## Lemma (even-\(s\) GY coboundary in \(\rho\))

Certified \(k\le 6\). Dual of Cycle GY.

## Lemma (odd-\(s\) XOR \(=\) AND on \(G(n,j)=1\) even \(\rho\))

Certified \(k\le 6\). Dual of Cycle GZ. Totals match Cycle FR
\(J_{\mathrm{tail}}\) and \(J_{\mathrm{mid10}}\) on \(k=2..5\).

## Killed

Equals \(\mathrm{mer\_one}(j)\): at \(k=2\), tail \(s=43\), \(j=3\),
\(G=0\) vs \(1\). Odd-\(s\) XOR equals \(J_{\mathrm{tail}}\): at
\(k=2\), \(0\neq 1\). Even-\(s\) XOR identically 0: at \(k=2\), xor
\(=1\).

## Verdict

`LEMMA` (in-support GX/GY in \(\rho=T-p\); odd-\(s\) XOR = AND on
\(G=1\)).
`KILLED` (\(\mathrm{mer\_one}\); odd-\(s\) XOR \(=J_{\mathrm{tail}}\);
even-\(s\) XOR \(=0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hc.md` (this note)
- `research/cycle_hc.py`
- `research/cycle_hc.json`
