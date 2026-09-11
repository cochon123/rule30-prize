# Cycle CS: \((W,X)\) has a `10`; sixth tail pair closed

Every \(V\) \(1\)-run starts with \(U=0\). Cycle CQ gives a \(V\) run of
length at least \(2\), so that start is a \(V\) `11` with \(U=01\). If
\(W=1\) there, \(X_{\mathrm{next}}=0\) is a `10` in \((W,X)\). If
\(W=0\) and \(X=1\), \(W_{\mathrm{next}}\) is an isolated \(1\) with
\(X_{\mathrm{next}}=0\), again a `10` in \((W,X)\). Every even
\(T_0\|\lnot T_0\) has one of those two, so skip-\(2\) gives \(Y\ne Z\).
This closes the sixth tail pair. Not a prize claim.

Helper: `python3 research/cycle_cs.py --certify`. Dump:
`research/cycle_cs.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(U=0\) at every \(V\) \(1\)-run start)

Let \(s\) start a \(V\) \(1\)-run, so \(V_{s-1}=0\) and \(V_s=1\). If
\(U_{s-1}=1\) then \(U_s=0\) (no consecutive \(1\)s in \(U\)). If
\(U_{s-1}=0\) then \(V_s=V_{s-1}\oplus\lnot T_{s-2}=\lnot T_{s-2}\), so
\(V_s=1\) forces \(T_{s-2}=0\) and \(U_s=0\).

## Lemma (`10` in \((W,X)\) from a long \(V\) run)

Cycle CQ: \(V\) has a `11`, hence a \(1\)-run of length \(\ge 2\) starting
at some \(s\) with \(U_s=0\) and \(V_s=V_{s+1}=1\). Then
\(W_{s+1}=\lnot U_s=1\) and \(W_{s+2}=\lnot U_{s+1}=0\) (Cycle CR: \(U\)
flips on a \(V\) `11`).

- If \(W_s=1\), then \(W_s=W_{s+1}=1\) and \(X_{s+1}=\lnot V_s=0\): a
  `10` in \((W,X)\) at \(s+1\).
- If \(W_s=0\) and \(X_s=1\), then \(X_{s+1}=V_s\oplus X_s=0\) with
  \(W_{s+1}=1\) and \(W_{s+2}=0\): an isolated \(W\) \(1\) that is a
  `10` in \((W,X)\).

Every nonconstant even \(|T_0|\in\{2,4,\ldots,16\}\) has the first arm
(\(n_A=65454\)) or the second (\(n_{\mathrm{isoB}}=53760\)), with
\(n_{\mathrm{both}}=48232\) and \(n_{\mathrm{neither}}=0\).

## Lemma (sixth tail pair never equal)

A `10` in \((W,X)\) is skip-\(2\) from Cycle CO, so
\(Z=\operatorname{reconstruct}(X,Y)\) differs from \(Y\) for every even
\(|T_0|\ge 2\). Combined with Cycles CH–CQ, the six packed bits after
ident-\(1\) are never a consecutive equal pair.

## Prefix (every \(2\)-power \(|T_0|\))

The seventh pair is not proved. No later ident-\(0\) on a window as long
as the next high half remains a prefix. Do not claim every pair has a
`10`. Do not classify a seventh pair unless a closed witness appears.
**PREFIX**.

## Verdict

`LEMMA` (\(U=0\) at every \(V\) \(1\)-run start; \((W,X)\) has a `10`
from origin \(A\) or isolated-\(B\); sixth pair never equal for every
even \(|T_0|\ge 2\)).
`PREFIX` (every \(2\)-power \(|T_0|\); seventh pair; at most one odd
toggle for all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cs.md` (this note)
- `research/cycle_cs.py`
- `research/cycle_cs.json`
