# Cycle GO: every cone-hi hit palindromes onto \(G(U-1,f)\) with \(f\not\equiv 2\pmod{3}\)

Palindrome sends \(e=W/2-r/2\) to \(f=2(U(Q-q)-1)-e\in[0,U)\) at
every Cycle GG hit, and \(G\) equals Cycle GN’s mod-3 bit
\(G(U-1,f)\). \(Q-q\) takes values \(1,2,3,4\) and is **not** always
a 2-power (\(W=16U\) has \(n=3\)). Raw \(e\) need **not** lie in
\([0,U)\); \(G(Un-1,f)\) need **not** equal \(G(U-1,f)\) for
\(f\ge U\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: lifting the mod-3 bit to every hit does not prove
covering never-fail (AND still selects a proper subset).

Helper: `python3 research/cycle_go.py --certify` (~0.01s). Dump:
`research/cycle_go.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GK/GM/GN (algebraic \(k\le 11\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (every hit palindromes to mod-3; \(n\in\{1,2,3,4\}\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\), 28665 even columns on
84 hits. This is why Cycle GK’s ones-count is independent of \(W\)
and \(q\).

## Killed

\(n\) always a 2-power: at \(k=2\), \(W=16U\), \(q=1\), \(n=3\). Raw
\(e\) in \([0,U)\): at \(k=2\), \(W=8U\), \(q=0\), \(e=14\notin[0,4)\).
\(G(Un-1,f)=G(U-1,f)\) for \(f\ge U\): \(G(7,4)=1\neq G(3,4)=0\).

## Verdict

`LEMMA` (every hit palindromes to mod-3; \(n\in\{1,2,3,4\}\)).
`KILLED` (\(n\) always a 2-power; raw \(e\) in \([0,U)\); \(G\) equal
past \(U\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_go.md` (this note)
- `research/cycle_go.py`
- `research/cycle_go.json`
