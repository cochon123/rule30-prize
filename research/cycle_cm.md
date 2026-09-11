# Cycle CM: the fourth scar-tail pair is never equal; \(V=0\Rightarrow DW=U\)

\(X=\operatorname{reconstruct}(V,W)\) splits on \(W\). When \(V_t=0\),
\(DW_t=U_t\), so \(V=DW\) iff \(U\to V\) and (\(V=1\Rightarrow W=U\)).
Every even \(T_0\|\lnot T_0\) has a witness against that: some
\(U=1,V=0\), or some \(V=1\) with \(W\ne U\). Neither witness is
universal (\(A\) misses \(|T_0|=2\); \(B\) misses some length-\(6\)
blocks), but they cover every block. Hence \(X\ne W\) for every even
\(|T_0|\ge 2\), including \(|T_0|=2\) where \(\operatorname{ham}(W,X)=1\).
Not a prize claim: later ident-\(0\) and the Fermat covering remain
prefixes.

Helper: `python3 research/cycle_cm.py --certify` (~1.1s). Dump:
`research/cycle_cm.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(X\) splits on \(W\))

\(X_{t+1}=V_t\oplus(W_t\lor X_t)\). If \(W_t=1\) then
\(X_{t+1}=\lnot V_t\). If \(W_t=0\) then \(X_{t+1}=V_t\oplus X_t\).

## Lemma (\(V_t=0\Rightarrow DW_t=U_t\))

If \(V_t=0\) then \(W_{t+1}=U_t\oplus W_t\), so
\(DW_t=W_t\oplus W_{t+1}=U_t\). Therefore \(V=DW\) iff there is no
\(U=1,V=0\) and no \(V=1\) with \(W\ne U\).

## Lemma (complementary witnesses)

On every nonconstant even \(|T_0|\in\{2,4,\ldots,16\}\) (\(70982\)
blocks), at least one witness fires (\(n_A=70232\), \(n_B=70626\),
\(n_{\mathrm{neither}}=0\)). **Not** a claim that \(A\) or \(B\)
alone is universal.

## Lemma (fourth tail pair never equal)

\(X=W\) iff \(V=DW\). The complementary witnesses kill that for every
even \(|T_0|\ge 2\) in the certified range. Hamming is at least
\(n_0/2\), tight. Combined with Cycles CH–CL, the four packed bits
after ident-\(1\) are never a consecutive equal pair on that range.
Length \(2\) still second-doubles later (Cycle CG).

## Prefix (every \(2\)-power \(|T_0|\))

No later ident-\(0\) is not proved past the first four pairs, nor for
\(|T_0|\ge 32\) on a long window. \(\operatorname{ham}(W,X)\ge n_0/2\)
is not a closed form. **PREFIX**.

## Verdict

`LEMMA` (\(X\) splits on \(W\); \(V=0\Rightarrow DW=U\); complementary
witnesses; fourth pair never equal through even length \(16\);
\(\operatorname{ham}(W,X)\ge n_0/2\) on that range).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cm.md` (this note)
- `research/cycle_cm.py`
- `research/cycle_cm.json`
