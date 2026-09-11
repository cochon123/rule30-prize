# Cycle BQ: packed bit 1 cannot Green-hit after \(t=(T-1)/2\)

A Green hit \(G(T-t-1,T-1)=1\) forces \(t\le(T-1)/2\). On the covering
coboundary blocks \([6U,10U)\) targeting \(10U\) and \([10U,18U)\)
targeting \(18U\), every time is strictly past that cone, so there
are **zero** packed-bit-1 hits for every \(k\ge 1\). Those remainders
are purely \(S_{\mathrm{other}}\). The first block \([2U,6U)\)
targeting \(6U\) still has bit-1 net 1 (Cycle AJ/BN). Covering fails
at \(k+1\) iff \(S_A=1\) and \(S_B=S_C=0\). Not a prize claim: the
Fermat covering remains a prefix.

Helper: `python3 research/cycle_bq.py --certify` (~0.1s). Dump:
`research/cycle_bq.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (bit-1 cone)

Packed bit 1 at time \(t\) Green-hits target \(T\) iff
\(G(T-t-1,T-1)=1\). The support bound \(d\le 2m\) is
\(T-1\le 2(T-t-1)\), i.e. \(t\le(T-1)/2\). Certified: no counterexample
for \(2\le T\le 48\) and \(1\le t<T\).

## Lemma (zero bit-1 hits on blocks \(B\) and \(C\))

Let \(U=2^k\). Write

- \(A=[2U,6U)\) targeting \(6U\),
- \(B=[6U,10U)\) targeting \(10U\),
- \(C=[10U,18U)\) targeting \(18U\).

Then \((10U-1)/2=5U-1/2\), so integer times in \(B\) satisfy
\(t\ge 6U>5U-1\ge(10U-1)/2\). Likewise
\((18U-1)/2=9U-1/2\), and \(t\ge 10U>9U-1\). By the cone, every
Green coefficient of packed bit 1 on \(B\) and on \(C\) is 0, for
every \(k\ge 1\). Certified: the inequalities for \(1\le k\le 12\),
and a direct Green scan for \(1\le k\le 6\). Equivalently the
prefix sums vanish:
\(\bigoplus_{m<2^{n+1}}G(m,5\cdot 2^n-1)=0\) and
\(\bigoplus_{m<2^{n+2}}G(m,9\cdot 2^n-1)=0\) (each term is 0 because
the target already exceeds \(2m\)). Certified \(1\le n\le 10\).

On \(A\), the cone allows \(t\le 3U-1\), which includes the unique
Cycle-AJ hit at \(t=2U\). The bit-1 net on \(A\) is
\(P(3,2U)=1\) (Cycle BN). Certified as
\(\bigoplus_{m<2^{n+1}}G(m,3\cdot 2^n-1)=1\) for \(1\le n\le 10\).
The full 5-fold and 9-fold nets from time \(2U\) remain
\(P(5)=P(9)=1\); those odd hits all lie in \(A\cup B\) before the
cone cut of \(C\), and the 5-fold unique hit at \(t=4U\) lies in
\(A\), not in \(B\).

## Lemma (sharpened covering failure)

Let \(S_A,S_B,S_C\) be the Green parities of *non*-bit-1 AND hits on
\(A,B,C\). Then \(\varphi^{(3)}_{k+1}=1\oplus S_A\),
\(\varphi^{(5)}_{k+1}\oplus\varphi^{(3)}_{k+1}=S_B\), and
\(\varphi^{(9)}_{k+1}\oplus\varphi^{(5)}_{k+1}=S_C\). Covering fails
at \(k+1\) iff \(S_A=1\) and \(S_B=S_C=0\). This is Cycle BO’s
even-spine alignment, with the bit-1 production removed from \(B\)
and \(C\). It is not a proof that the alignment is empty.

## Verdict

`LEMMA` (bit-1 cone; zero bit-1 hits on \(B\) and \(C\) for every
\(k\ge 1\); bit-1 net on \(A\) equals 1; covering fails iff
\(S_A=1\) and \(S_B=S_C=0\)).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bq.md` (this note)
- `research/cycle_bq.py`
- `research/cycle_bq.json`
