# Cycle DU: at-most-one odd per annulus implies the period-\(H\) seed

\(\pi_1=1\), and unique continuation multiplies the left-word period by
\(2\) on an odd ident-0 and preserves it on reconstruct / even ident-0.
Odds that sit in the \(k\)-word are those in \((2^m,2^{m+1}]\) for
\(1\le m<k\). If each of those \(k-1\) annuli has at most one odd, then
\(\pi_k\mid 2^{k-1}\), i.e. the period-\(H\) seed holds. The exact
formula \(2^{\lceil\log_2 k\rceil}\) is strictly stronger. On the prize
orbit the hypothesis holds through \(k=19\). Do not push \(\pi\) past
\(19\).

Cycle DT’s one-sided \(11\Rightarrow 0\) reduces covering failure to
the \(I=0\) all-zero kernel \(c_U=c_{2U}=c_{6U}=c_{10U}=c_{18U}\), empty
through \(k=18\). Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: at-most-one-odd for all \(k\) remains open.

Helper: `python3 research/cycle_du.py --certify`. Dump:
`research/cycle_du.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(\pi_1=1\); odd doubles, even/reconstruct preserve)

`prize_cycle(1)` has min-period \(1\). `reconstruct` returns a list of
the same length. Unfold of even-weight \(a\) stays length \(\pi\);
unfold of odd-weight \(a\) concatenated with its complement has length
\(2\pi\) and even weight. Certified exhaustively for lengths \(2\le n
\le 8\).

## Lemma (at-most-one-odd implies seed)

The \(k\)-word contains packed bits \(0,\ldots,2^k\). Odd ident-0s that
have already doubled \(\pi\) are those in \((2^m,2^{m+1}]\) for
\(1\le m<k\) (\(k-1\) annuli). Starting from \(\pi_1=1\), at most one
odd per annulus gives \(\pi_k=2^{e}\) with \(0\le e\le k-1\), hence
\(\pi_k\mid 2^{k-1}=H_k\). Certified for every exponent \(0\le e<k\)
through \(k=64\). Two odds in the first annulus would give
\(\pi_2=4\nmid 2=H_2\), so a bound of \(1\) is sharp at \(k=2\). The
exact formula \(\pi_k=2^{\lceil\log_2 k\rceil}\) is **not** required
for the seed: any at-most-doubling \(2\)-power works. **Killed** as a
necessary condition.

## Prefix (hypothesis through \(k=19\))

Cycles DE/DO: odd ident-0 in \((2^k,2^{k+1}]\) iff \(k\in\{1,2,4,8,16\}\)
through \(k=19\), so \(n_{\mathrm{odd}}\le 1\) on that range, and the
constructed \(\pi\) matches the measured periods
\(1,2,4,4,8^{\times 4},16^{\times 8},32,32,32\). **PREFIX**, not a
theorem that every later annulus has at most one odd.

## Lemma (covering failure reduces to the \(I=0\) kernel)

Under \(\varphi^{(6)}=\varphi^{(10)}=1\Rightarrow\varphi^{(18)}=0\),
the even-spine dangerous pattern \(a=b=g=I\) is exactly
\(a=b=g=I=0\). That kernel is \(c_U=c_{2U}=c_{6U}=c_{10U}=c_{18U}\).
Certified on all bit tuples. Cycle DT: the one-sided implication and
empty \(I=0\) kernel hold through \(k=18\). **PREFIX** for all \(k\).

## Verdict

`LEMMA` (\(\pi_1=1\); odd doubles / even preserves; at-most-one-odd
implies seed; two odds can kill seed; one-sided \(11\Rightarrow 0\)
reduces failure to the \(I=0\) kernel; five-equal iff that kernel).
`KILLED` (seed requires the exact \(\pi\) formula).
`PREFIX` (at-most-one-odd for all \(k\); period-\(H\) seed for all
\(k\); one-sided implication for all \(k\); Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_du.md` (this note)
- `research/cycle_du.py`
- `research/cycle_du.json`
