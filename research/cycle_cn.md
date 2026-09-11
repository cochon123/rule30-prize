# Cycle CN: unique continuation always splits on \(B\); fifth pair never equal

Packed update \(C'=A\oplus(B\lor C)\) splits pointwise: if \(B=1\) then
\(C'=\lnot A\), if \(B=0\) then \(C'=A\oplus C\), hence \(DC=A\). That
is the same split used for \(U,V,W,X\). \(Y=\operatorname{reconstruct}(W,X)\)
equals \(X\) iff \(W=DX\), iff \(V\to W\) and (\(W=1\Rightarrow X=V\)).
Every even \(T_0\|\lnot T_0\) through length \(16\) has \(W=1\) with
\(X\ne V\) (universal on this range), so \(Y\ne X\). Not a prize claim:
later ident-\(0\) and the Fermat covering remain prefixes.

Helper: `python3 research/cycle_cn.py --certify` (~1.3s). Dump:
`research/cycle_cn.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (pointwise split)

For every bits \(A,B,C\), the packed update \(C'=A\oplus(B\lor C)\)
satisfies \(B=1\Rightarrow C'=\lnot A\) and \(B=0\Rightarrow C\oplus C'=A\).
Eight triples, exhaustive. Unique continuation of a period-\(\pi\) pair
is this recurrence with cyclic wrap, so the same split holds along any
scar-tail pair.

## Lemma (\(B=0\Rightarrow DC=A\))

If \(B_t=0\) then \(C_{t+1}=A_t\oplus C_t\), so \(DC_t=A_t\). In
particular \(W=0\Rightarrow DX=V\), and \(Y=X\) iff \(W=DX\).

## Lemma (fifth tail pair never equal)

On every nonconstant even \(|T_0|\in\{2,4,\ldots,16\}\) (\(70982\)
blocks), some \(W=1\) has \(X\ne V\) (\(n_B=n_{\mathrm{ok}}\)). The
companion \(V=1,W=0\) misses \(20\) length-\(10\) blocks, so it is
not universal. Hamming of \((X,Y)\) is at least \(2,3,4,5,6,7,5\)
respectively; the length-\(16\) minimum is \(5\), not monotone.
Combined with Cycles CH–CM, the five packed bits after ident-\(1\)
are never a consecutive equal pair on that range.

## Prefix (every \(2\)-power \(|T_0|\))

The split licenses an inductive \(A\ne DB\) along the tail, but does
not by itself produce a later-pair witness. No later ident-\(0\) is
not proved past the first five pairs, nor for \(|T_0|\ge 32\) on a
long window. **PREFIX**.

## Verdict

`LEMMA` (pointwise split; \(B=0\Rightarrow DC=A\); fifth pair never
equal through even length \(16\), via universal \(W=1\) with
\(X\ne V\)).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cn.md` (this note)
- `research/cycle_cn.py`
- `research/cycle_cn.json`
