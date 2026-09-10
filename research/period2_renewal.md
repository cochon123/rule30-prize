# Period-2 L_0: renewal gaps and the insulation estimate

This note is a checked lemma plus a finite scan of a proposed Lyapunov
function. It does **not** exclude eventual period 2, and it does not
claim a prize result.

Helper: `research/period2_renewal.py --certify`. Dump:
`research/period2_renewal.json`. Notation as in
`research/period2_vacuum.md`: after a time origin the center is
`c_{2n}=0`, `c_{2n+1}=1`, and `F_k(u_n,u_{n+1},\ldots)=x(2n,-k)` on
Fibonacci `u` (no consecutive 1s). Isolated 1s of `u` are renewal
events; the gaps between them are the object.

## Gap window (proved)

Let `u` be Fibonacci, and suppose `u_i=0` for `a ≤ i < b`. Write `w`
for the length-`a` prefix and `w0^∞` for its zero-padded extension
(equivalently: replace the suffix from index `a` by zero).

**Lemma (agreement through the next 1).**
`F_k(u)=F_k(w0^∞)` for every `k ≤ 2b`.

Proof: `max_index(F_k) ≤ floor((k-1)/2)` (`period2_vacuum.md`, variable
bound). The bit `u_b` first appears when `floor((k-1)/2) ≥ b`, i.e.
`k ≥ 2b+1`. Checked on all length-`5` prefixes with a gap of `12`
(`certify_variable_bound_gap`).

**Lemma (truncated vacuum).** `E(w) := max{k : F_k(w0^∞) ≠ k mod 2}`
is finite, and `E(w) ≤ 11|w|+C` for an absolute `C` (each fold increases
the last disagreement by at most 11; the 16-state tail machine absorbs
in at most 9 columns). Thus `F_k(w0^∞)=k mod 2` for all `k > E(w)`.

**Corollary (exposure).** If the interval `E(w)+1 ≤ k ≤ 2b` is
nonempty, then `F_k(u)=k mod 2` throughout it. Any odd index in that
interval is a `1` arbitrarily far left as `a,b → ∞`, which an `L_0`
onset (`F_T=1` and `F_k=0` for `k>T`) cannot survive once the interval
sits to the right of `T`.

The FSM bound `E(w) ≤ 11|w|+C` therefore already forbids *multiplicative*
gaps with `2b ≥ 11a+C+1`, i.e. `b/a ≳ 11/2`. That is the bridge stated
in the assignment. It does not bound gap *lengths*.

## Insulation `E(w) ≤ 2|w|+C` (false)

The variable-bound window grows by two columns per extra zero in the
gap. A bound `E(w) ≤ 2|w|+C` would make every sufficiently large
*additive* gap expose vacuum, hence force bounded zero-gaps in any
`L_0` counterexample. The two legal left extensions of a Fibonacci word
are prepend-`0` and prepend-`10`; a weighted potential with increment at
most `2` per consumed bit would prove the estimate by induction from
`E(ε)=-1`.

**Kill family.** Let `w_m = 0^m 1`. Then

```
E(w_m) = 8m − 14    for every 5 ≤ m ≤ 36
```

(`certify_single_1_formula`; the values `m=5..10` already appear in
`period2_vacuum.json`). Excess over the proposed bound is

```
E(w_m) − 2|w_m| = 6m − 16,
```

which is already `200` at `m=36` and increases by `6` at every further
step in the scanned range. The family is explicit, Fibonacci, and
makes excess front displacement unbounded. The coefficient-`2`
estimate is false.

The same growth is not an artefact of a single isolated 1:

- `(10)^n` has `E=16n-22` for `3 ≤ n ≤ 12`, excess `6|w|-22`.
- For `4 ≤ L ≤ 14`, `max E(w)` over length `L` is `8L-14`, achieved
  *exactly* on the Fibonacci words ending in `0101` (`n=F_{L-2}` of
  them). Excess `6L-14 → ∞`.

No Lyapunov function of the form `2|w|+C`, nor any other potential
whose prepend-`0` increment is at most `2`, can dominate `E`.

## Prepend-0 and prepend-10

Folding is from the right, so `F(0w)=Φ_0(F(w))` and
`F(10w)=Φ_1(Φ_0(F(w)))`. On every Fibonacci word of length `≤ 8`
(`n=142` samples):

```
E(0w) − E(w)  ∈ {0, 3, 5, 8}
E(10w) − E(w) ∈ {3, 8, 13, 16}
```

The increment `0` occurs only on all-zero words (vacuum). On every
scanned word that contains a `1`, prepend-`0` strictly increases `E`.
The maximum increments are `8` and `16=8+2`, saturating a speed-`8`
budget, not a speed-`2` budget.

Once the front has reached `E ≥ 18`, the increment is no longer a
choice: every Fibonacci word of length `≤ 11` with `E≥18` has
`E(0w)=E(w)+8` (`n=541`). In the single-`1` family this cruise begins
at `m=4` (`E=18`) and continues through `m=36`. The new defect mask
on the eight columns past the old front takes one of two values, both
with last bit `1` at offset `8` and vacuum thereafter; the companion
`G`-mask is the same for both types.

Trailing zeros (right of the last `1`) are no-ops: they fold onto
vacuum first. The relevant scale is the index of the rightmost `1`,
not the zero-padded length. That is why `0101 0^m` stays at `E=18`
while `0^m 0101` runs at `8(m+4)-14`.

## Weaker linear bound (empirical, not a gap-length bound)

The data are consistent with `E(w) ≤ 8|w|-14` for `|w|≥4`, tight on
the `0101` family, and with `E(w) ≤ 8(r+1)+O(1)` where `r` is the
index of the rightmost `1`. Combined with prepend increments `≤ 8`
per bit, this would follow by induction from a genuine speed-`8`
cruise lemma. It is **not** proved for arbitrary length; it is
checked through `L=14` and on the single-`1` family through length
`37`.

Even if `E(w) ≤ 8|w|+C` were a theorem, the exposure window
`8a+C < k ≤ 2b` is nonempty only for `b/a ≳ 4`. That still forbids
only large multiplicative gaps. It does not force bounded gaps, and it
does not exclude `L_0`.

## Scattering

Two isolated 1s `1 0^g 1`: write `E_right` for the front of the
right-hand `0^g 1` alone. The collision shift `E − E_right` is

```
g=1: +5,    g=2: +3,    g=3: +5,    g≥4: +8
```

through `g=24`. A well-separated left-hand 1 *adds* eight columns to
the front; it does not annihilate, bind, or retreat. The same `+8`
is the prepend-`0` cruise increment, so an extra renewal event at
large separation is equivalent to eight more zero-folds, not a
cancellation.

There is therefore no finite dictionary of isolated-defect scattering
rules in which collisions dissipate. The wake behind the front is not
a compact particle: for `w_m=0^m 1` the defect support in `k` grows
like `E(w_m)` itself, carrying the whole history, which is the
obstruction named in the assignment.

A nonzero “defect flux” incompatible with an eventually-zero left
tail would need the front to *lose* to the `2b` window. Speed `8>2`
is the opposite: the front outruns agreement, and vacuum is never
exposed inside the variable bound.

## What is proved, what is not

Proved: the gap-window corollary (agreement through `k=2b`, truncated
vacuum past `E(w)`); hence any `L_0` counterexample has
`b ≤ (E(w)+1)/2` at every gap `[a,b)`, in particular `b/a ≲ 11/2`
from the FSM bound.

Proved as a finite certificate: `E(0^m 1)=8m-14` for `5≤m≤36`;
`max_{|w|=L} E(w)=8L-14` for `4≤L≤12`, uniquely on words ending
`0101`; prepend increments lie in the speed-`8` set above through
length `8`; two-defect shift `+8` for `4≤g≤24`.

Not proved: `E(w)≤2|w|+C` (false); `E(w)≤8|w|+C` for all `w`; any
uniform additive bound on zero-gaps; a compact scattering theory;
exclusion of `L_0` or of eventual period 2.

## Why the attack dies

The kill criterion was: retire if an explicit Fibonacci-word family
makes excess front displacement grow without bound and invalidates
the insulation estimate.

That family is `0^m 1`, with excess `6m-16`. The mechanism is a
speed-`8` cruise under prepend-`0` once `E≥18`, visible on every
short Fibonacci word and on every denser family tested (`(10)^n`,
words ending `0101`). The variable-bound window expands at speed
`2`; a front that runs at speed `8` never falls behind it, so
large additive gaps need not expose an odd-indexed vacuum `1`.
Bounded gaps are not forced. Isolated defects do not cancel.
Period 2 remains open.

## Files

- `research/period2_renewal.md` (this note)
- `research/period2_renewal.py` (`--certify` checks the single-`1`
  formula, the `0101` maximizers, prepend increments, the `E≥18`
  cruise on short words, two-defect shifts, and the variable-bound
  gap window)
- `research/period2_vacuum.py` / `period2_vacuum.md` (variable bound,
  vacuum FSM, `E(0^m 1)` through `m=10`)
