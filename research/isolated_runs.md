# Isolated runs in a hypothetical periodic center

Assume the center trace is eventually periodic. After a time shift, an
isolated-zero period has primitive word `01^q` (exactly one 0 per period).
An isolated-one period has primitive word `0^q1`.

Jen/Kopra still require a second eventually periodic column. The local
update already determines the left neighbor on every 1 that is followed by
a 1: if `c_t=1`, then `l_t = 1 XOR c_{t+1}`. Thus during a 1-run of length
`q`, the left neighbor is `0^{q-1}1`. The only undetermined left bit is the
one sitting on the isolated 0, where `l = 1 XOR r`.

## Radius-6 certificate for isolated zeros

Consider width-13 strips (radius 6) with arbitrary outer boundary bits.
Any genuine eventual `01^q` tail of the finite seed must eventually occupy a
recurrent strongly connected component of this finite directed graph. If
every such component has a periodic adjacent column, Jen/Kopra exclude it.

Full enumeration of that graph (independent of the incremental extender)
gives the following at radius 6, for `1 <= q <= 30`:

* residual (no forced periodic neighbor) if and only if
  `q ∈ {1,2,3,4,5,6,8}`;
* otherwise a unique recurrent component, graph period `q+1`, and left
  neighbor forced at every phase.

In the excluded cases the forced left column is exactly the locally
predicted word: `1` on the isolated 0, `0` on every 1 except the last, and
`1` on the last 1. Columns `-1` and `0` are then both eventually periodic,
which is forbidden for every nonzero finite seed.

Reproducible check: `python3 research/isolated_zero_cert.py`.
Raw table: `research/isolated_zero_radius6.json`.

The period-9 word `011111111` is a genuine exception at this radius: the
unique recurrent component still admits both left-neighbor bits on the
isolated 0. Incremental extension through radius 22 with a 90,000-state
cap does not empty it. Periods 2–7 likewise retain residual components at
every width explored.

For `q >= 9` the unique component has a rigid shape: a fixed gadget of
about nine phases around the isolated 0, plus a 14-state “cruise” layer
for each extra 1. In a cruise phase the leftmost nine strip bits are
constant and the rightmost four bits omit two of the sixteen patterns.
This is why the same radius-6 obstruction repeats for every larger `q`
checked; it is not a proof for all `q`, but it is a uniform finite-width
certificate for every concrete `q` that one is willing to enumerate
(`(q+1) 2^{13}` vertices).

## Isolated ones

The symmetric family `0^q1` is weaker at radius 6–7. Full enumeration at
radius 7 empties residual components for `q >= 10`. Incremental
Jen-pruned extension additionally empties `q = 7` at radius 13 and `q >= 9`
except `q = 8`. As with isolated zeros, `q = 8` (period 9) retains a
residual component. These are seed-applicable exclusions only after the
neighbor is forced periodic; they do not by themselves forbid a 0-run of
that length in a non-isolated-one word.

## What this does not do

Period 2 is the isolated-zero word with `q = 1`. It retains residual
components at radius 6 and at every larger width that has been explored.
Excluding long isolated zeros therefore does not force a 00 or 11 in an
eventual period, and does not reduce Problem 1 to period 2.
