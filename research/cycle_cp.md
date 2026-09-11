# Cycle CP: \((U,V)\) has a `10` iff \(T\) has an odd \(1\)-run; fourth pair closed

A `10` in \((U,V)\) occurs only at the first odd offset of a \(1\)-run,
and there \(V=0\) iff the preceding \(0\)-run is odd. The half-period
run bijection of Cycle CK makes that equivalent to \(n_{\mathrm{odd}}>0\).
Skip-\(2\) from Cycle CO then gives \(X\ne W\) on odd-run blocks. On
even-run blocks \(U\to V\), \(\mathrm{wt}(U)=n_0/2\), and the \(V=1\)
subsequence has \(n_0\) zeros and \(n_0/2\) ones, so two consecutive
\(V=1\) times share a \(U\) value and complementary witness \(B\) of
Cycle CM fires. Hence \(X\ne W\) for every even \(|T_0|\ge 2\). Even-run
blocks also have a `10` in \((V,W)\), so skip-\(2\) kills the fifth pair
on that gap; the fifth pair on odd-run blocks remains a prefix. Not a
prize claim.

Helper: `python3 research/cycle_cp.py --certify`. Dump:
`research/cycle_cp.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (later odd offsets of a \(1\)-run have \(V=1\))

\(U_t=1\) only at odd run-offsets of \(1\)-runs of \(T\). If
\(\mathrm{run\_ending}(T,t-2)\ge 3\), then \(T_{t-4}=T_{t-3}=T_{t-2}=1\),
so \(U_{t-2}=1\) and \(U_{t-1}=0\). The CK split gives
\(V_{t-1}=T_{t-3}=1\) and \(V_t=V_{t-1}\oplus\lnot T_{t-2}=1\). A `10`
in \((U,V)\) can occur only at the first bit of a \(1\)-run.

## Lemma (first-of-run \(V\) is the previous \(0\)-run parity)

After any \(1\)-run the first \(0\)-run \(U\)-slot has \(V=0\): an odd
run resets \(V\) to the following \(0\), and an even run resets to \(1\)
then toggles across the last \(1\). Walking \(z\) steps of \(U=0\) with
\(T_{t-1}=0^{z-1}1\) then yields \(V=(z-1)\bmod 2\) at the next
\(1\)-run start. So \(V_{s+2}=0\) iff the preceding \(0\)-run is odd.

## Lemma (\((U,V)\) has a `10` iff \(n_{\mathrm{odd}}>0\))

A `10` exists iff some \(1\)-run start has odd previous \(0\)-run, iff
\(n_{\mathrm{odd},0}>0\). Cycle CK's half-period bijection equates that
with \(n_{\mathrm{odd}}>0\). Checked on every nonconstant even
\(|T_0|\in\{2,4,\ldots,16\}\) (\(70232\) odd-run blocks have a `10`;
\(750\) even-run blocks have none).

## Lemma (skip-\(2\) kills \(X=W\) on odd-run blocks)

A `10` in \((U,V)\) is skip-\(2\) from Cycle CO, so
\(X=\operatorname{reconstruct}(V,W)\) differs from \(W\) whenever
\(n_{\mathrm{odd}}>0\).

## Lemma (even-run witness \(B\))

If \(n_{\mathrm{odd}}=0\) then every \(1\)-run is even, so
\(\mathrm{wt}(U)=n_0/2\), and \(U\to V\). With
\(\operatorname{ham}(U,V)=n_0\) the pair counts are
\((1,1)=n_0/2\), \((0,1)=n_0\), \((0,0)=n_0/2\), \((1,0)=0\).
While \(U\to V\), \(W\) freezes on \(V=0\) and
\(W_{t+1}=\lnot U_t\) on \(V=1\), so at each \(V=1\) time \(W\) equals
the negation of \(U\) at the previous \(V=1\) time. The \(V=1\)
subsequence therefore has \(n_0\) zeros of \(U\) and \(n_0/2\) ones.
For \(n_0\ge 2\) those counts are unequal, so the circular subsequence
is not alternating: two consecutive \(V=1\) times share a \(U\) value,
hence some \(V=1\) has \(W\ne U\). That is Cycle CM's witness \(B\), so
\(V\ne DW\) and \(X\ne W\).

The same unequal counts give a \(10\) in the subsequence, hence a `10`
in \((V,W)\), and skip-\(2\) yields \(Y\ne X\) on every even-run block.
This does **not** close the fifth pair: some odd-run blocks lack a `10`
in \((V,W)\).

## Lemma (fourth tail pair never equal)

Odd-run blocks: skip-\(2\) from \((U,V)\). Even-run blocks: witness
\(B\). Together \(X\ne W\) for every even \(|T_0|\ge 2\), including
\(|T_0|=2\) where \(\operatorname{ham}(W,X)=1\). This closes the
length-\(16\) census of Cycle CM.

## Prefix (every \(2\)-power \(|T_0|\))

The fifth pair is not proved on odd-run blocks. No later ident-\(0\) on
a window as long as the next high half remains a prefix. Do not claim
every pair has a `10`. Do not classify a sixth pair unless a closed
witness appears. **PREFIX**.

## Verdict

`LEMMA` (later odd offsets have \(V=1\); first-of-run \(V\) is previous
\(0\)-run parity; \((U,V)\) has a `10` iff \(n_{\mathrm{odd}}>0\);
skip-\(2\) kills \(X=W\) on odd-run blocks; even-run witness \(B\);
fourth pair never equal for every even \(|T_0|\ge 2\); even-run
\((V,W)\) has a `10`).
`PREFIX` (every \(2\)-power \(|T_0|\); fifth pair on odd-run blocks;
at most one odd toggle for all \(k\); seed for all \(k\); Fermat
covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cp.md` (this note)
- `research/cycle_cp.py`
- `research/cycle_cp.json`
