# Cycle GY: at even \(s\), the \(j\)-th even column is \(G(n,j)\oplus G(n,j-1)\)

Same clock \(n=UQ-t-1\) as Cycles GU/GX. \(j=0\) is the lo corner
\(G=1\). Odd-\(r\) Green is \(G(n,j)\) with \(j=(r-\mathrm{lo}-1)/2\).
Even-\(r\) Green is **not** the odd-\(s\) single term \(G(n,j)\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: a \(j\)-index for even-\(s\) Green does not prove
covering never-fail (AND still mixes).

Helper: `odd_clock` from `research/cycle_gu.py`. Certify:
`python3 research/cycle_gy.py --certify` (~0.02s). Dump:
`research/cycle_gy.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GN/GV/GW/GX (Green \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (even-\(r\) \(G(n,j)\oplus G(n,j-1)\); \(j=0\) has \(G=1\))

Certified \(k\le 6\). This is Cycle GX’s row coboundary in the
\(j\)-index.

## Lemma (odd-\(r\) \(G=G(n,j)\), \(j=(r-\mathrm{lo}-1)/2\))

Certified \(k\le 6\). Matches Cycle GW’s copy \(G(s,r)=G(s+1,r+1)\).

## Killed

Equals the odd-\(s\) term \(G(n,j)\): at \(k=1\), \(W=4U\), \(s=8\),
\(j=1\), \(G=0\) vs \(1\). Equals \(\mathrm{mer\_one}(j)\): same
witness, \(\mathrm{mer\_one}=1\). Identically 1: same \(G=0\).

## Verdict

`LEMMA` (even-\(r\) coboundary in \(j\); \(j=0\) is 1; odd-\(r\)
\(G(n,j)\)).
`KILLED` (equals odd-\(s\) \(G(n,j)\); \(\mathrm{mer\_one}\);
identically 1).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gy.md` (this note)
- `research/cycle_gy.py`
- `research/cycle_gy.json`
