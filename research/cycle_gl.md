# Cycle GL: at a cone-hi hit, Green ones lie only on even \(r\)

Cycle GJ’s clock \(m=2U(Q-q)-2\) is even, so freshman \(G(m,\mathrm{odd})=0\).
Then \(G(m,W-r)=1\) forces \(W-r\) even, hence \(r\) even (\(W\) is
even). All even \(r\) in the cone have \(G=1\) iff \(k\le 1\) (then
the Cycle GK count equals \(U\)). Odd \(r\) in the cone are
Green-silent; **not** every even \(r\) is a one for \(k\ge 2\); AND
does **not** fire on every Green one. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: restricting Green ones to even \(r\) does not
prove covering never-fail (AND still selects a proper subset).

Helper: `python3 research/cycle_gl.py --certify` (~0.01s). Dump:
`research/cycle_gl.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FS/GJ/GK (algebraic \(k\le 11\); packed
\(k=1\) kill; no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (Green ones only on even \(r\); all even iff \(k\le 1\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\), 84 hits. Both endpoints
\(\mathrm{lo}\) and \(\chi\) are even.

## Killed

Odd-\(r\) ones: at \(k=2\), \(W=4U\), \(r=5\), \(G=0\). All even
\(r\): at \(k=2\), \(W=4U\), \(r=8\), \(G=0\). AND on all Green ones:
at \(k=1\), \(W=4U\), lo has \(G=1\) and dead AND.

## Verdict

`LEMMA` (ones only on even \(r\); all even \(r\) iff \(k\le 1\)).
`KILLED` (odd-\(r\) ones; all even \(r\); AND on all Green ones).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gl.md` (this note)
- `research/cycle_gl.py`
- `research/cycle_gl.json`
