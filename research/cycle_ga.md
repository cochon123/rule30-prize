# Cycle GA: unclipped hi-1 times are \(t_0+q\cdot 2U+\varepsilon\) with \(q<W/(4U)\)

Covering \(W\in\{4U,8U,16U\}\) is \(0\bmod 4U\), so \(Q=W/(4U)\) is an
integer (strengthening Cycle FX’s \(0\bmod 2U\)). Cycle FZ’s dyadic
offsets in one \(2U\)-period, copied over \(q=0,\ldots,Q-1\), are
exactly the unclipped times with hi Green 1. The last such time is
clip, at \(q=Q-1\) and \(\varepsilon=U=2^{a-1}\). Whole-window hi is 1
iff \(s>\mathrm{clip}\) or \(s\) is one of those times. Clip hi AND is
**not** always live, \(W\) is **not** \(0\bmod 8U\), and \(E_a\) is
**not** all of \([0,U]\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: a \(q\)-parametrization of hi-1 times does not prove
covering never-fail (Cycle FX already killed hi AND whenever \(G=1\)).

Helper: `python3 research/cycle_ga.py --certify` (~0.02s). Dump:
`research/cycle_ga.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FX/FY/FZ (walk \(k\le 11\); piecewise
Green \(k\le 7\); packed clip AND at \(k=2\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(W\equiv 0\pmod{4U}\))

Certified \(k\le 20\), \(W\in\{4U,8U,16U\}\).

## Lemma (\(q\)-parametrization; clip is last)

\(s=t_0+q\cdot 2U+\varepsilon\) for \(0\le q<Q\) and
\(\varepsilon\in E_a=\{2^j:0\le j<a\}\cup(\{0\}\text{ if }a\text{ odd})\).
Clip is \(q=Q-1\), \(\varepsilon=U\). Certified \(k\le 11\).

## Lemma (piecewise whole-window hi)

\(G=1\) iff \(s>\mathrm{clip}\) or \(s\) is a \(q\)-param time.
Certified \(k\le 7\).

## Killed

\(W\equiv 0\pmod{8U}\): \(W=4U\). Clip hi AND always live: at \(k=2\),
\(W=8U\), AND is 0. \(E_a=[0,U]\): \(a=3\) misses 3.

## Verdict

`LEMMA` (\(W\equiv 0\pmod{4U}\); \(q\)-param; clip is last dyadic;
piecewise hi).
`KILLED` (\(W\equiv 0\pmod{8U}\); clip AND always live; \(E_a=[0,U]\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ga.md` (this note)
- `research/cycle_ga.py`
- `research/cycle_ga.json`
