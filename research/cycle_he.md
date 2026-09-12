# Cycle HE: in-support remainder is the full Green row; odd \(s\) enumerates \(n\)

On covering windows the in-support \(\mathrm{lo}=2s-T+2\) has
\(T-\mathrm{lo}=2m\), so every Green column \(\rho\in[0,2m]\) is in-band
(width \(2m+1\)). Odd \(s=t_0+2t+1\) visits \(n=UQ-t-1\) for
\(t=0,\ldots,UQ-1\), i.e. every \(n\in[0,UQ)\) once; even \(s\) at the
same \(t\) shares that \(n\). AND at \((n,j)\) still depends on the
window. Width is **not** \(2U-1\); tail \(n\) is **not** only in
\([0,U)\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: removing the unified clip from \(J_{\mathrm{tail}}\)
does not prove covering never-fail (AND still has no closed form).
Odd-\(s\) \(J_{\mathrm{tail}}\) is
\(\bigoplus_{n<4U}\bigoplus_{G(n,j)=1}\mathrm{AND}(T-2j)\).

Helper: `WINDOWS` / `odd_clock` from Cycles HC/GU. Certify:
`python3 research/cycle_he.py --certify` (~0.05s). Dump:
`research/cycle_he.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/FQ/GU/HC/HD (algebra \(k\le 12\); packed
AND kill at \(k=0\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (in-support \(=\) full Green row, width \(2m+1\))

Certified \(k\le 12\). Dual of the unified sliding width \(2U-1\)
(Cycle FQ/FL): here nothing clips.

## Lemma (odd \(s\) enumerates \(n\in[0,UQ)\); even \(s\) shares \(n\))

Certified \(k\le 12\). Window length is \(2UQ\).

## Killed

Width \(2U-1\): at \(k=2\), tail, \(s=t_0+1\), width \(61\neq 7\).
AND\((n,j)\) independent of window: at \(k=0\), \(n=1\), \(j=2\), tail
\(0\) vs mid \(1\). Tail \(n\) only in \([0,U)\): first odd \(s\) has
\(n=4U-1\).

## Verdict

`LEMMA` (full Green row; odd-\(s\) \(n\)-scan; even \(s\) same \(n\)).
`KILLED` (width \(2U-1\); AND independent of window; tail \(n<U\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_he.md` (this note)
- `research/cycle_he.py`
- `research/cycle_he.json`
