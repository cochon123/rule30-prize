# Periods 3–7: phase-mask propagation (no closed cycle)

Assume a periodic center of primitive word `001` or `0111`. Existing
identities force selected phases at **fixed** depth 4
(`period_p_left_edge.md`):

```
001:   x(3n+2, -4) = 0
0111:  x(4n, -4) = x(4n+2, -4) = x(4n+3, -4) = 0
```

Question: do those constraints reproduce farther left with extra onset
delay `h` strictly less than the spatial step `d`, so that iterating
meets the moving edge `k=T+s`, `a≡s (mod p)`, for every onset residue?

Helper: `research/period_p_propagate.py` (`--certify`; full scan writes
`period_p_propagate_slim.json`). Does not modify `strip_graph.py` /
`strip_extend.py`. Left cells are reconstructed by `fill_left` on
injected 0-phase right bits (injection lemma). Depth-4 identities were
already enum-certified; this file does not use the ANF bit-coding in
`period_p_left_edge.py` for three or more injected variables (that
encoding collides `u2` with `u0 u1`).

**Outcome.** No period is excluded. There is **no** closed implication
cycle with spatial displacement `d∈{4,8}` and extra delay `h<d` whose
forced-zero mask hits the moving edge for every onset residue. The
depth-4 zeros do not reappear at depths 8 or 12, under one-step Markov
or radius-3 right consistency. The assignment therefore **stops**: the
computation regenerates finite identities (and one radius-3 extra at
depth 11) without a repeatable propagation rule. Same obstruction
shape as the period-2 shift that loses a zero tail
(`period2_certificate.md`).

## Implication system

State at depth `k`: the pair of temporal columns
`(x(t,-k), x(t,-(k-1)))` over a window of width `w=2p+8`, together with
the phase mask of bits that are identically 0 or 1, and the language of
injected 0-phase right bits.

One inverse step is Jen’s reconstruction

```
x(t, -(k+1)) = x(t+1, -k) XOR (x(t, -k) OR x(t, -(k-1)))
```

so a `d`-step map on two-column windows needs no extra right bits.
Radius-3 right evolution tracks columns `+1,+2,+3` with a free bit at
`+4`:

```
x1' = c XOR (x1 OR x2)
x2' = x1 XOR (x2 OR x3)
x3' = x2 XOR (x3 OR x4)
```

This is a proper subset of the one-step Markov walk on column `+1`.
Vacuum implications: the full right vacuum `(x1,x2,x3)=(0,0,0)` forces
`x1'=c`. If only `+2` and `+3` are vacuum, `x1'=c XOR x1`. Both fire in
the 8-state automaton; they do not by themselves force new left zeros
at the depths below except one listed extra.

A closed cycle would be a mask `Z` of forced-zero phases at depth `k0`
such that after `d` inverse steps and time delay `h<d`,

```
Z(k0 + m d) ⊇ (Z(k0) + m h)  (mod p)
```

and `{k0 + m d - α : α∈Z(k0+md)}` covers every onset residue
`T mod p`. Then `T+s = k0+m(d-h)` can be solved for arbitrarily large
`T` with the edge phase on a forced zero.

## Unconditional masks (`k≤16`)

Forced-zero phases, Markov and radius-3 **agree** on `001` through
depth 16: the only left identity is the known `k=4`, phase 2. Depths
5–16 are mixed on every phase.

For `0111`, Markov forced zeros at `k≥1`:

| `k` | forced 0 | forced 1 | note |
|----:|----------|----------|------|
| 1 | 1, 2 | 3 | left neighbor on the 1-run |
| 2 | 2 | 1 | double-1 |
| 4 | 0, 2, 3 | — | known `F_4` analogue |
| 6 | 2 | — | extra finite identity |
| 10 | 2 | — | extra finite identity |
| 8, 12, 14, 16 | — | — | fully mixed |

Phase 2 vanishes at `{1,2,4,6,10}`, **not** at `8,12,14,16`. That is
not an arithmetic progression of difference 4 or 8.

Radius-3 adds exactly one extra through depth 16: `x(4n+3, -11)=0`.
It does not restore a zero at depth 8 or 12, and it does not sit at
`k=4+d` for `d∈{4,8}`.

## Injected bits and two-column windows

`001`: one-step Markov already forbids `(u,v)=(1,0)` on a single
period (`v=r_{3n+1}` is `u OR e`). Radius-3 does not shrink that pair
set, but it shrinks longer words (4 periods: 40 injected strings vs 58
Markov). Consecutive 1s in the 0-phase stream still occur.

`0111`: Markov leaves the isolated-zero bit `u_n=r_{4n}` **free**.
Radius-3 forces **no consecutive 1s** on `(u_n)` (13 Fibonacci words
of length 5, vs all 32). This is a genuine right-side tightening. It
is not enough to make column `-8` or `-12` identically zero on any
phase.

One-period two-column windows at depth 4, radius-3: `001` has 7
realised pairs at every start phase; column `-4` is the known 0 only
when the window starts at phase 2. At depth 8 the pair counts **grow**
(13 / 17 / 13) and phase 2 of column `-8` takes both values. `0111`
likewise: 2–3 pairs at depth 4 with three phases forced 0, then 3–5
pairs at depth 8 with every phase mixed. Constraint is lost, not
copied.

## Implications over `d=4,8`

From every legal depth-4 window of width `2p+8`, including those
restricted to the known forced-zero phases, `d` inverse steps produce
**no** output offset that is identically 0 (common over window-start
phase, and none even as a union of start phases, once the window is
long enough to include every residue). Unique output windows are
sometimes fewer than the inputs (`001`, `d=4`, start phase 0: 137→109
radius-3 pairs) but the collapse is not onto a bit. Start phase 2,
where the `001` identity lives, maps 84→84 with empty forced-zero
output.

So the known mask at `k=4` does not imply a mask at `k=8` or `k=12`.
The unconditional chain is

```
001:    Z(4)={2},  Z(8)=∅,  Z(12)=∅
0111:   Z(4)={0,2,3}, Z(8)=∅, Z(12)=∅
```

No `h` realises `Z(4+d) ⊇ Z(4)+h`. Onset residues killed by the
depth-4 identities remain the finite list already in
`period_p_left_edge.md` (`T+s=4` on a zero phase).

## Mixed-column shift equalities (not a zero cycle)

On `0111`, several mixed columns satisfy exact equalities of the form
`x(s+h, -(k+d)) = x(s,-k)` or `1+x(s,-k)` after a shift of `u`,
checked on every Markov / radius-3 string with `kmax=12`. Examples
(Markov, `d=4`):

- `x(0,-7) = x(0,-3)` after one period of `u`;
- `x(2,-8) = x(2,-4)` after one period of `u` (both mixed: the depth-4
  zero phases are **not** in this family);
- `x(3,-6) = 1 + x(3,-2)` after one period of `u`.

These are the analogue of the period-2 coincidences `F_6=S^2 F_2`.
They move mixed information. They do not send a forced-zero mask to a
forced-zero mask. `001` has **no** non-constant equality of this form
for `d∈{4,8}`.

## `L_0` germ transport

A local germ is `x(t,-k)=1` and `R∈{2,3}` further zeros. Image at
`(t+h, k+d)` for `d∈{4,8}`, `h=0..8`:

- No pair `(d,h)` with `h<d` maps every germ to an `L_0` germ or to a
  forced-zero tail.
- The majority image is a **bump** (extra 1s in the would-be zero
  tail): about 67% already for `001`, `R=2`, `d=4`, `h=0`, and at best
  still 54% for `0111`, `R=2`, `d=8`, `h=3` (radius-3). The remaining
  mass splits between occasional `L_0` copies and occasional all-zero
  tails, never all of one.

This is the same failure mode as the period-2 lemma
`F_{T+3}=1+F_{T+1}(Su)`: a 1-then-zeros is not sent to a smaller
1-then-zeros. A descent that shortens the zero tail cannot catch an
onset of width `T>0`.

## What would have finished a period, and what did not

A `T`-independent contradiction needed the forced-zero mask to travel
left faster than the edge (`h<d`) and to cover every onset residue.
The depth-4 identities stay at depth 4. Extra zeros at `0111` depths
6 and 10 (phase 2) and the radius-3 zero at depth 11 (phase 3) are
more finite identities. Mixed-column Mahler-style shifts do not carry
zeros. Germ transport produces bumps.

No period in `{3,4,5,6,7}` is excluded by this attack. Residual strip
SCCs in `small_periods.md` remain consistent with an aperiodic injected
`r` that keeps a left edge alive for a while and then dies.

## Files

- `research/period_p_propagate.md` (this note)
- `research/period_p_propagate.py` (`--certify`; `--slim-out` for the
  scan dump)
- `research/period_p_propagate_slim.json`
- `research/period_p_left_edge.md` / `.py` (source identities, not
  overwritten)
