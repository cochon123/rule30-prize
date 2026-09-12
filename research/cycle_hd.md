# Cycle HD: even-\(s\) in-support XOR is coboundary-1 even AND plus \(G=1\) odd AND

Cycle HC’s GY index. AND can fire on coboundary-0 even \(\rho\) and on
\(G=0\) odd \(\rho\) but those contribute 0. Even-\(s\) XOR is **not**
\(J_{\mathrm{tail}}\) (\(k=5\): \(0\) vs \(1\)) and is **not** the
even-\(\rho\) slice alone (\(k=2\): odd-\(\rho\) XOR \(=1\)). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the HA dual on in-support does not prove covering
never-fail (AND still has no closed form). Together with Cycle HC,
\(J_{\mathrm{tail}}\) and \(J_{\mathrm{mid10}}\) are fully in the
\(j\)-index.

Helper: `WINDOWS` / `odd_clock` from Cycles HC/GU. Certify:
`python3 research/cycle_hd.py --certify` (~0.2s). Dump:
`research/cycle_hd.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FR/GU/GY/HA/HC (packed \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (even-\(s\) XOR \(=\) coboundary-1 even AND \(\oplus\) \(G=1\) odd AND)

Certified \(k\le 6\), three covering windows. Dual of Cycle HA with
\(\rho=T-p\).

## Killed

AND only on coboundary-1 even \(\rho\): at \(k=1\), tail, a
coboundary-0 even column fires. Even-\(s\) XOR equals the even-\(\rho\)
slice: at \(k=2\), tail, odd-\(\rho\) XOR \(=1\). Even-\(s\) XOR equals
\(J_{\mathrm{tail}}\): at \(k=5\), \(0\neq 1\).

## Verdict

`LEMMA` (even-\(s\) in-support XOR = coboundary-1 even AND \(\oplus\)
\(G=1\) odd AND).
`KILLED` (AND only on coboundary 1; even-\(s\) XOR = even-\(\rho\)
slice; even-\(s\) XOR \(=J_{\mathrm{tail}}\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hd.md` (this note)
- `research/cycle_hd.py`
- `research/cycle_hd.json`
