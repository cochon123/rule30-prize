# Cycle GP: \(j\)-th even cone column at a hit has palindrome index \(f=j\)

On Cycle GG’s hits the even columns \(r=\mathrm{lo}+2j\) for
\(0\le j<U\) fill the cone, and Cycle GO’s palindrome index is
\(f=j\). Green is \(\mathrm{mer\_one}(j)\) (\(j\not\equiv 2\pmod{3}\)).
Lo maps to \(f=0\) and cone-hi to \(f=U-1\). The map is **not**
reversed (\(f=U-1-j\)); Green is **not** “\(j\) even”; AND is **not**
live on every \(\mathrm{mer\_one}\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: parametrizing even cone columns by \(j\) does not
prove covering never-fail (AND still selects a proper subset).

Helper: `python3 research/cycle_gp.py --certify` (~0.01s). Dump:
`research/cycle_gp.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GL/GN/GO (algebraic \(k\le 11\); packed
\(k=1\) kill; no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(r=\mathrm{lo}+2j\) has \(f=j\); \(G=\mathrm{mer\_one}(j)\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\), 28665 even columns on
84 hits. Endpoints: \(j=0\) is lo, \(j=U-1\) is cone-hi.

## Killed

Reversed \(f=U-1-j\): at \(k=1\), \(j=0\), \(f=0\neq 1\). Green iff
\(j\) even: at \(k=1\), \(j=1\), \(G=1\). AND on every
\(\mathrm{mer\_one}\): at \(k=1\), \(W=4U\), \(j=0\), dead AND.

## Verdict

`LEMMA` (\(f=j\) on even cone columns; \(G=\mathrm{mer\_one}(j)\)).
`KILLED` (reversed; iff \(j\) even; AND on every mer_one).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gp.md` (this note)
- `research/cycle_gp.py`
- `research/cycle_gp.json`
