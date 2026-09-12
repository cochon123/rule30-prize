# Cycle HA: even-\(s\) band XOR is coboundary-1 even AND plus \(G=1\) odd AND

Cycle GY indexes those columns. AND can fire on coboundary-0 even
columns and on \(G=0\) odd columns but those contribute 0. Even-\(s\)
XOR is **not** \(\Delta_R\) (\(k=2\), \(W=8U\): \(0\) vs \(1\)) and is
**not** the even-\(r\) slice alone (\(k=3\), \(W=8U\): odd-\(r\)
XOR \(=1\)). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: reducing the even-\(s\) slice to Green-weighted
AND does not prove covering never-fail (AND still has no closed
form). Together with Cycle GZ the band XOR is fully in the
\(j\)-index; for \(W=8U\) that XOR is already \(\Delta_R\)
(Cycle FL).

Helper: `odd_clock` from `research/cycle_gu.py`. Certify:
`python3 research/cycle_ha.py --certify` (~0.05s). Dump:
`research/cycle_ha.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FL/FR/GU/GY/GZ (packed \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (even-\(s\) XOR \(=\) coboundary-1 even AND \(\oplus\) \(G=1\) odd AND)

Certified \(k\le 6\), all covering \(W\). Even-\(r\) Green is
\(G(n,j)\oplus G(n,j-1)\); odd-\(r\) Green is \(G(n,j)\).

## Killed

AND only on coboundary-1 even columns: at \(k=3\), \(W=8U\), a
coboundary-0 even column fires. Even-\(s\) XOR equals the even-\(r\)
slice: at \(k=3\), \(W=8U\), odd-\(r\) XOR \(=1\). Even-\(s\) XOR
equals \(\Delta_R\): at \(k=2\), \(W=8U\), \(0\neq 1\).

## Verdict

`LEMMA` (even-\(s\) band XOR = coboundary-1 even AND \(\oplus\)
\(G=1\) odd AND).
`KILLED` (AND only on coboundary 1; even-\(s\) XOR = even-\(r\)
slice; even-\(s\) XOR \(=\Delta_R\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ha.md` (this note)
- `research/cycle_ha.py`
- `research/cycle_ha.json`
