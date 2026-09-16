# Period-2 phase `10`: SFT forbidding `{00, 111}`

Checked lemma: under \(c_{2n}=1\), \(c_{2n+1}=0\), the even-right bit
\(u_n=x(2n,1)\) satisfies \(u_n=0\Rightarrow u_{n+1}=1\) and
\(u_n=1\Rightarrow u_{n+1}=\lnot(e_n\lor f_n)\), independently of
columns \(4\) and \(5\). Consequently \(u\) has no two consecutive
zeros and no three consecutive ones. The SFT forbidding `{00, 111}`
has growth root \(\lambda^3=\lambda+1\) (\(\lambda\approx 1.32>1\)), so
aperiodic sequences exist and Jen/Kopra does **not** kill the phase.
Finite seeds still reduce to phase `01` by one Rule 30 step
(`research/period2_fiber.md`). Not a prize claim: phase `01` remains.

Helper: `python3 research/period2_phase10.py --certify`. Dump:
`research/period2_phase10.json`. Two-step table as in
`research/period2_ugap.md`; finite-right traces from
`research/period2_fiber.py` with `c0=1`.

## Lemma (two-step identities)

Force the centre \(1,0,1\) over two steps. Write \(u,e,f\) for even-time
columns \(1,2,3\). Even step with \(C=1\):

\[
r'=1\oplus(u\lor e)=\lnot(u\lor e),\qquad
e'=u\oplus(e\lor f).
\]

Odd step with \(C'=0\):

\[
u''=0\oplus(r'\lor e')=r'\lor e'.
\]

If \(u=0\), then \(r'=\lnot e\) and \(e'=e\lor f\), so
\(u''=(\lnot e)\lor(e\lor f)=1\). If \(u=1\), then \(r'=0\) and
\(e'=1\oplus(e\lor f)\), so \(u''=\lnot(e\lor f)\). In particular
\(u=1\Rightarrow u'=1\) if and only if \(e=f=0\).

The complete table on \((u,e,f)\) plus four further right bits
(neighborhood radius 2 over two steps) matches these identities in
every row; extending to six further bits does not change \(u'\).

## Corollary (SFT `{00, 111}`)

Zeros are not absorbing: every \(0\) is followed by a \(1\). A run of
three \(1\)s is impossible: the unique \(1\to 1\) transition has
\((e,f)=(0,0)\), which forces \(e'=1\), hence the next bit is \(0\).
Thus every compatible \(u\) (finite or infinite right) lies in the
subshift of finite type forbidding `{00, 111}`.

This SFT is not a finite union of periodic orbits. Its transfer matrix
on last-two blocks \(\{01,10,11\}\) has characteristic polynomial
\(\lambda^3-\lambda-1\), with real root \(>1\).

## Finite seeds reduce to phase `01`

A nonzero finite seed whose centre is eventually phase `10` remains
finite after one Rule 30 step, and that image has eventual phase `01`.
Killing every finite-seed phase-`01` centre therefore kills phase `10`
as well. The remaining obstruction is the ugap \(L_0\) of
`research/period2_ugap.md` / `research/period2_qextra.md`.

## Checks

- Identities on extra-\(4\) and extra-\(6\) complete tables; \(u'\) is
  a function of \((u,e,f)\) alone.
- Longest \(1\)-run on the \((u,e,f)\) graph is \(2\).
- Every nonzero-or-empty right of width \(\le 8\), forced phase `10`
  through time \(240\): even-\(u\) lies in the SFT (max \(1\)-run \(2\),
  max \(0\)-run \(1\)). No all-\(1\) survivor on this width.
- Even-time left neighbor identically \(1\) on every width-\(6\) right
  through time \(80\) (spatial:
  \(\ell_{2n}=c_{2n+1}\oplus(c_{2n}\lor u_n)=0\oplus 1=1\)).

## What this does not do

Phase `01` is untouched. An aperiodic word in this SFT is still a
legal even-right of a (possibly two-sided) phase-`10` fibre; Jen does
not apply. The false claim that zeros absorb, so \(u\) is \(1^*0^*\),
is killed by the identity \(0\to 1\).

## Verdict

`LEMMA`, wall time <1s.

- Kill of period 2 phase `10` for finite seeds: only via the \(F\)-reduction
  to phase `01`, which is still open.
- New uniform constraint on phase-`10` \(u\): yes, SFT `{00, 111}`.

## Files

- `research/period2_phase10.md` (this note)
- `research/period2_phase10.py` (`--certify`)
- `research/period2_phase10.json` (dump)
