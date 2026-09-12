# Cycle GK: at a cone-hi hit, cone Green ones-count is \((2U+1+(k\bmod 2))/3\)

On Cycle GG’s hits the cone \([\mathrm{lo},\chi]\) has width \(2U-1\),
but the number of \(r\) with \(G(m,W-r)=1\) is
\((2U+1+(k\bmod 2))/3\), independent of covering \(W\) and of \(q\).
It is **not** \(k+1\) (Cycle GC’s in-cone time-count), **not** the
full width, and **not** dependent on \(q\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a ones-count on the cone at the \(Q\) hits does
not prove covering never-fail (AND still selects a proper subset).

Helper: `python3 research/cycle_gk.py --certify` (~0.01s). Dump:
`research/cycle_gk.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FS/GC/GJ (algebraic \(k\le 11\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (ones-count \((2U+1+(k\bmod 2))/3\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\), 84 hits. Both endpoints
are 1 (lo-edge \(G(m,2m)=1\), cone-hi \(G(m,2U-2)=1\)).

## Killed

Count \(=k+1\): at \(k=4\), \(11\neq 5\). Count \(=\) width: at
\(k=2\), \(3\neq 7\). Count depends on \(q\): \(k=2\), \(W=8U\),
\(q=0\) and \(q=1\) both give 3.

## Verdict

`LEMMA` (ones-count \((2U+1+(k\bmod 2))/3\); independent of \(W,q\)).
`KILLED` (count \(=k+1\); count \(=\) width; count depends on \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gk.md` (this note)
- `research/cycle_gk.py`
- `research/cycle_gk.json`
