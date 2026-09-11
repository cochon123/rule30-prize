# Cycle CL: the third scar-tail pair is never equal; `00` forces \(U\ne DV\)

\(W=\operatorname{reconstruct}(U,V)\) splits on \(V\): if \(V_t=1\) then
\(W_{t+1}=\lnot U_t\), else \(W_{t+1}=U_t\oplus W_t\). When \(U_t=0\),
the cyclic derivative is \(DV_t=S_t\). A `00` in \(T\) at
\((t-2,t-1)\) gives \(U_t=0\) and \(S_t=1\), so \(U\ne DV\). Even
\(T_0\|\lnot T_0\) is not alternating and therefore has a `00`, hence
\(W\ne V\) for every even \(|T_0|\ge 2\). Not a prize claim: later
pairs and the Fermat covering remain prefixes.

Helper: `python3 research/cycle_cl.py --certify` (~1s). Dump:
`research/cycle_cl.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(W\) splits on \(V\))

\(W_{t+1}=U_t\oplus(V_t\lor W_t)\). If \(V_t=1\) then
\(W_{t+1}=\lnot U_t\). If \(V_t=0\) then \(W_{t+1}=U_t\oplus W_t\).
This is the same split that \(V\) has on \(U\) (Cycle CK).

## Lemma (\(U_t=0\Rightarrow DV_t=S_t\))

If \(U_t=0\) then \(V_{t+1}=V_t\oplus\lnot T_{t-1}=V_t\oplus S_t\), so
\(DV_t=V_t\oplus V_{t+1}=S_t\).

## Lemma (`00` witnesses \(U\ne DV\))

A `00` at \(T_{t-2}T_{t-1}\) forces \(U_t=0\) (run-parity) and
\(S_t=\lnot T_{t-1}=1\), hence \(DV_t=1\ne 0=U_t\). Cycle CH: even
\(T_0\|\lnot T_0\) is never alternating, so a balanced length-\(2n_0\)
string has a `00`.

## Lemma (third tail pair never equal)

\(W=V\) iff \(U=DV\). The `00` witness kills that for every even
\(|T_0|\ge 2\). Combined with Cycles CH–CK, the three packed bits
after ident-\(1\) are never a consecutive equal pair. Checked on
every nonconstant even \(|T_0|\in\{2,4,\ldots,16\}\) (minimum Hamming
\(2,3,5,6,6,8,11\)).

## Prefix (every \(2\)-power \(|T_0|\))

No later ident-\(0\) is not proved past the first three pairs, nor for
\(|T_0|\ge 32\) on a long window. The fourth pair can have Hamming
\(1\) already at \(|T_0|=2\), which second-doubles (Cycle CG).
**PREFIX**.

## Verdict

`LEMMA` (\(W\) splits on \(V\); \(U=0\Rightarrow DV=S\); `00` witnesses
\(U\ne DV\); third pair never equal for every even \(|T_0|\ge 2\)).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cl.md` (this note)
- `research/cycle_cl.py`
- `research/cycle_cl.json`
