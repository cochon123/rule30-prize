# Cycle CK: \(\operatorname{ham}(U,V)=|T_0|\) because \(+n_0\) pairs \(1\)-runs with \(0\)-runs

\(U\) never has consecutive \(1\)s. Packed update of \(V\) splits on
\(U\): if \(U_t=1\) then \(V_{t+1}=T_{t-1}\), else
\(V_{t+1}=V_t\oplus\lnot T_{t-1}\). Then \(\delta=U\oplus V\) toggles
after \(U=0\) and resets to \(T_{t-1}\) after \(U=1\). Odd \(2\)-copy
\(T=T_0\|\lnot T_0\) sends each \(1\)-run to a \(0\)-run of the same
length by a half-period shift, so the odd-run counts match and
\(\operatorname{ham}(U,V)=\sum\lfloor r/2\rfloor+\sum\lceil z/2\rceil=|T_0|\).
This is the closed form of Cycle CI's exhaustive
\(\operatorname{ham}(U,V)=n_0\). Not a prize claim: later pairs and
the Fermat covering remain prefixes.

Helper: `python3 research/cycle_ck.py --certify` (~1.4s). Dump:
`research/cycle_ck.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(U\) has no consecutive \(1\)s)

Reset-toggle is \(U_{t+1}=T_{t-1}\land\lnot U_t\). If \(U_t=1\) then
\(U_{t+1}=0\). Isolated \(1\)s of \(U\) are the odd-offset bits of
\(1\)-runs of \(T\).

## Lemma (\(V\) splits on \(U\))

\(V_{t+1}=S_t\oplus(U_t\lor V_t)\) with \(S_t=\lnot T_{t-1}\). If
\(U_t=1\) then \(V_{t+1}=T_{t-1}\). If \(U_t=0\) then
\(V_{t+1}=V_t\oplus\lnot T_{t-1}\).

## Lemma (\(\delta\) toggle-reset)

Write \(\delta=U\oplus V\). After \(U_t=0\), \(\delta_{t+1}=\lnot\delta_t\).
After \(U_t=1\), \(\delta_{t+1}=T_{t-1}\). Together with isolated \(1\)s
of \(U\), each \(1\)-run of length \(r\) followed by a \(0\)-run of
length \(z\) contributes \(\lfloor r/2\rfloor+\lceil z/2\rceil\) to
\(\operatorname{ham}(U,V)\).

## Lemma (half-period pairs runs)

\(T_{t+n_0}=\lnot T_t\). A maximal \(1\)-run on \([s,s+r)\) maps to a
maximal \(0\)-run on \([s+n_0,s+n_0+r)\): the boundaries flip from
\(0\) to \(1\). This is a length-preserving bijection between
\(1\)-runs and \(0\)-runs, so their length multisets agree and
\(n_{\mathrm{odd}}(0)=n_{\mathrm{odd}}(1)\).

## Lemma (\(\operatorname{ham}(U,V)=|T_0|\))

Summing the per-run contributions gives
\(\frac12(n_0-n_{\mathrm{odd},1})+\frac12(n_0+n_{\mathrm{odd},0})=n_0\)
once the odd-run counts match. In particular the second tail pair is
never equal, with exact distance \(n_0\), for every even
\(|T_0|\ge 2\). Checked on every nonconstant even
\(|T_0|\in\{2,4,\ldots,16\}\).

## Prefix (every \(2\)-power \(|T_0|\))

No later ident-\(0\) is not proved past the first two pairs, nor for
\(|T_0|\ge 32\) on a long window. **PREFIX**.

## Verdict

`LEMMA` (no consecutive \(1\)s in \(U\); \(V\) splits on \(U\);
\(\delta\) toggle-reset; half-period pairs runs;
\(\operatorname{ham}(U,V)=|T_0|\) for every even \(|T_0|\ge 2\)).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ck.md` (this note)
- `research/cycle_ck.py`
- `research/cycle_ck.json`
