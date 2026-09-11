# Cycle CR: \(W\) always has consecutive \(1\)s; \((W,U)\) has a `10`

\(U\) flips on every \(V\) `11`. On a `00` of \(U\), \(V\) is `01` or `10`.
Some \(U\) `00` has \(V=10\): a \(T\) \(0\)-run of length at least \(3\),
or an even-length \(1\)-run (the only remaining non-alternating case).
Then \((U,V)=(0,1)\) with \(U_{\mathrm{next}}=0\), so \(W_{\mathrm{next}}=1\)
on a \(0\) of \(U\), and \(W\) stays \(1\) one more step. Hence \((W,U)\)
has a `10` and \(W\) has a `11`. On even-run blocks the \(V=1\)
subsequence has a `00` of \(U\), which makes a \(W\) `11` start at
\(V=1\) and gives a `10` in \((W,X)\). The sixth pair on odd-run blocks
remains a prefix. Not a prize claim.

Helper: `python3 research/cycle_cr.py --certify`. Dump:
`research/cycle_cr.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(U\) flips on every \(V\) `11`)

\(U\) has no consecutive \(1\)s. If \(V_t=V_{t+1}=1\) and \(U_t=0\), the
CK split forces \(T_{t-1}=1\). Then either \(T_{t-2}=0\), so \(U_{t+1}=1\),
or \(T_{t-2}=1\), so consecutive run-parities differ. In both cases
\(U_t\ne U_{t+1}\). Checked on every nonconstant even
\(|T_0|\in\{2,4,\ldots,16\}\).

## Lemma (on a `00` of \(U\), \(V\) is `01` or `10`)

After \(U=0\), \(\delta\) toggles, so \(V\) cannot stay constant on a
`00` of \(U\). Equivalently \(V_t=V_{t+1}=1\) cannot sit on \(U=00\)
(previous lemma).

## Lemma (some \(U\) `00` has \(V=10\))

If \(T\) has a \(0\)-run of length \(\ge 3\), incoming \(V=0\) at the
run start (Cycle CP) toggles to \(10\) on the interior \(U\) `00`.
Otherwise every \(0\)-run (and by the half-period bijection every
\(1\)-run) has length \(1\) or \(2\). Not alternating, so some \(1\)-run
has length \(2\). After an even \(1\)-run, \(V_{p+1}=1\) and
\(V_{p+2}=0\) with \(U_{p+1}=U_{p+2}=0\). Checked: \(68256\) by a long
\(0\)-run, \(2726\) by an even \(1\)-run.

## Lemma (\(W\) has a `11`; \((W,U)\) has a `10`)

At such a site \(U_t=0\), \(V_t=1\), \(U_{t+1}=0\). Then
\(W_{t+1}=\lnot U_t=1\) and \(W_{t+2}=U_{t+1}\oplus(V_{t+1}\lor 1)=1\).
So \(W_{t+1}=1=W_{t+2}\) with \(U_{t+1}=0\).

## Lemma (even-run \((W,X)\) has a `10`)

If \(n_{\mathrm{odd}}=0\) then \(U\to V\) and the \(V=1\) subsequence
has \(n_0\) zeros of \(U\) and \(n_0/2\) ones (Cycle CP), so a `00` of
\(U\) along it. At the second of that `00`, \(W=\lnot U_{\mathrm{prev}}=1\)
with \(V=1\), and \(W_{\mathrm{next}}=1\). A \(W\) `11` starting at
\(V=1\) forces \(X_{\mathrm{next}}=\lnot V=0\), a `10` in \((W,X)\).
Skip-\(2\) then gives \(Y\ne Z\) on every even-run block.

## Prefix (sixth pair)

\((W,X)\) has a `10` on every certified odd-run block as well, so
\(Y\ne Z\) through even length \(16\), but that arm is not closed.
Do not claim every pair has a `10`. Do not classify a sixth pair as a
theorem. **PREFIX**.

## Verdict

`LEMMA` (\(U\) flips on every \(V\) `11`; on \(U\) `00`, \(V\) is `01`
or `10`; some \(U\) `00` has \(V=10\); \(W\) has a `11` and \((W,U)\)
has a `10`; even-run \((W,X)\) has a `10`).
`PREFIX` (sixth pair on odd-run blocks; every \(2\)-power \(|T_0|\);
at most one odd toggle for all \(k\); seed for all \(k\); Fermat
covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cr.md` (this note)
- `research/cycle_cr.py`
- `research/cycle_cr.json`
