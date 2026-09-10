# Period-2 center: exact constraint on the even right neighbor

Shift time so that a hypothetical eventual period-2 center satisfies
`c_{2n}=0` and `c_{2n+1}=1` for all large `n`. Write
`u_n = x(2n,1)`, `e_n = x(2n,2)`, `f_n = x(2n,3)`.

## Two-step identity

The local rule over one even step and one odd step gives

```
u_{n+1} = 1  if and only if  (u_n, e_n, f_n) = (0,0,0),
```

and `u_{n+1}=0` in the other seven cases. Direct expansion:

* even step, center 0: `r' = r OR e` and `e' = r XOR (e OR f)`;
* odd step, center 1: `u_{n+1} = NOT (r' OR e')`.

The disjunction `r' OR e'` vanishes only on the triple `(0,0,0)`.
In particular `u` never has two consecutive 1s.

## Infinitely many 1s, via Jen

If `u_n` is eventually 0, the even left neighbor is `l_{2n}=1 XOR u_n=1`
and the odd left neighbor is already 1. Column `-1` is eventually constant,
so columns `-1` and `0` are both eventually periodic, contradicting
Jen/Kopra for every nonzero finite seed.

Thus `u` has infinitely many isolated 1s. Equivalently, there are
infinitely many even times at which positions `0,1,2,3` are simultaneously
0 (center 0 together with the triple above).

If `u` itself is eventually periodic, the left reconstruction of
`research/alternating.md` makes every reconstructed left column eventually
periodic, and Jen applies again. So a period-2 center for a finite seed
requires an aperiodic even right-neighbor sequence with infinitely many
isolated 1s, each preceded by a width-3 right vacuum.

## What remains

The identity does not force `u` to be periodic. Period-2 left driving of a
semi-infinite right half can produce aperiodic `u` (the vacuum right half
already has Berlekamp–Massey length growing with the prefix). The missing
step is to use the actual finite right support of the seed, or the moving
left edge `x(t,-t)=1`, to rule that aperiodic `u` out.

Finite exhaustive search over all width-`(2T+1)` rows with both edges 1
finds no configuration whose center stays period 2 for much longer than
`O(T)` further steps (`T <= 11` fully, larger `T` sampled). That is
consistent with the claim but is not a bound.
