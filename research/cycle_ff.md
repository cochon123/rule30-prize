# Cycle FF: Green translation \(G(n+q\cdot 2^a,d+q\cdot 2^a)=G(n,d)\) for \(n<2^{a-1}\)

The Green function is the coefficient of \(x^d\) in \((1+x+x^2)^n\).
Freshman’s map gives \((1+x+x^2)^{q\cdot 2^a}=Q_q(x^{2^a})\) with
\(Q_q=(1+x+x^2)^q\). The coefficient of \(x^{q\cdot 2^a}\) is
\(G(q,q)=1\). Expanding therefore yields

\[
G(n+q\cdot 2^a,\,d+q\cdot 2^a)
=\bigoplus_{i:\,G(q,i)=1}G\bigl(n,\,d+(q-i)2^a\bigr).
\]

If \(n<2^{a-1}\) and \(0\le d\le 2n\), then \(2n<2^a\). Every \(i\neq q\)
shifts the second argument off the support \([0,2n]\), so only \(i=q\)
survives and

\[
G(n+q\cdot 2^a,\,d+q\cdot 2^a)=G(n,d).
\]

The case \(q=1\) is a \(2^a\)-shift; \(q=3\) is the \(12U=3\cdot 4U\)
shift between covering targets \(6U\) and \(18U\). The bound \(n<2^a\)
is false (\(a=4\), \(n=8\), \(d=0\)). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** claim
covering never-fail. Do **not** push the even-spine scan past \(k=18\).
Do **not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\).

Not a prize claim: a Green translation on the half-window does not by
itself force the three off-cone \(J\) never to vanish.

Helper: `python3 research/cycle_ff.py --certify`. Dump:
`research/cycle_ff.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/AI/CA/FE (no new packed run, no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(G(n,n)=1\))

Even \(n=2\ell\) doubles to \(G(\ell,\ell)\); odd \(n=2\ell+1\) likewise.
Certified \(0\le n<256\).

## Lemma (translation for \(n<2^{a-1}\))

The Freshman expansion above. Certified on every
\(1\le a\le 8\), \(1\le q\le 6\), every \(n<2^{a-1}\), every
\(d\in[0,2n]\).

## Killed

The same identity for all \(n<2^a\): counterexample \(a=4\),
\(n=8=2^{a-1}\), \(d=0\), where \(G(8,0)=1\neq 0=G(24,16)\).

## Verdict

`LEMMA` (\(G(n,n)=1\); translation for \(n<2^{a-1}\)).
`KILLED` (translation for \(n<2^a\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ff.md` (this note)
- `research/cycle_ff.py`
- `research/cycle_ff.json`
