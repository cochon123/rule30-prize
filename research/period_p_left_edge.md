# Periods 3–7: left reconstruction and the seed light-cone

Assume, after a time origin, that the center is exactly periodic of
period `p∈{3,4,5,6,7}` with a primitive necklace `w`. Left columns are
recovered from the inverse

```
x(t, j-1) = x(t+1, j) XOR (x(t, j) OR x(t, j+1))
```

as Boolean functions of the right neighbor `r_t=x(t,1)`, reduced by the
local Markov rule `r_{t+1}=c_t XOR (r_t OR e_t)` with `e_t` free. The
prize seed contributes the left light-cone `L_0` at onset: leftmost 1 at
column `-T`, zeros strictly further left, and moving edge
`x(s,-(T+s))=1` for as long as the regime lasts.

Helper: `research/period_p_left_edge.py` (`--certify`, `--identities`,
`--chains`). Does not modify `strip_graph.py` / `strip_extend.py`.

No period in `{3,4,5,6,7}` is excluded. The lemmas below cut many onset
widths and force every checked `L_0` chain of `T≤8` to die in `O(1)`
time, but they do not give a `T`-independent bound, nor a periodic
neighbor to which Jen/Kopra would apply.

## Uniform lemmas

**Injection.** The bit `r_t` enters the left half only through
`x(t,-1)=c_{t+1} XOR (c_t OR r_t)`. When `c_t=1` this is `NOT c_{t+1}`,
independent of `r_t`. Consequently every left column is a function of
the right neighbor *only at 0-phases of the center*. Checked on every
primitive necklace of period 3–7 (`injection_check`). This is the
period-2 `v`-independence lemma with no extra work.

**Double-1.** If `c_s=c_{s+1}=1`, then `x(s,-2)=c_{s+2}` identically:

```
x(s,-1) = NOT c_{s+1} = 0,
x(s,-2) = x(s+1,-1) XOR 1,
x(s+1,-1) = c_{s+2} XOR 1,
```

so the two XORs cancel. In particular, for every isolated-zero word
`01^q` with `q≥2`, the penultimate 1 (phase `p-2`) has `c_{p}=0`, hence
`x(p-2,-2)=0`.

**Vacuum triangle.** If times `s,...,s+k` are all 1s, the reconstruction
of `x(s,-k)` reads no 0-phase, so the cell is a function of the center
word only. A 1-run of length `q` therefore determines columns
`-1,...,-(q-1-i)` at the `i`-th 1 of the run. Extra identities exist
beyond this sufficient condition (as `F_4` did for period 2).

**Window `10010`.** If `(c_t,...,c_{t+4})=(1,0,0,1,0)`, then
`x(t,-4)=0` as a Boolean polynomial in the injected right bits, with no
Markov reduction. Expanding the inverse at that 1:

```
x(t,-1)   = 1
x(t,-2)   = 1 XOR r_{t+1}
x(t+2,-1) = 1 XOR r_{t+2}
x(t+3,-1) = 1            (the second 1 of the window)
x(t,-4)   = 0
```

The last step is the same two-case cancellation as in the period-3
calculation below. Among primitive period 3–7 words this hits `001`
(every 1), `00101` (one of the two 1s), `0001001`, `0010011`, `0010101`,
`001011`, `0010111`. It does *not* hit `011` or `0111`.

No left column `-k` for `1≤k≤8` is identically a periodic word on all
phases, for any primitive necklace of period 3–7. Markov-legal `r` is a
superset of what a genuine spacetime can realize, so this does not rule
out a Jen pair on a thinner set of `r`; it does say the left
reconstruction of an arbitrary Markov `r` never hands Jen a periodic
column by itself.

## Closed identities for the two period-3 survivors and for `0111`

### `001`: `x(3n+2,-4)=0`

This is the `10010` window at the unique 1. Direct expansion, writing
`u=r_{3n}`, `v=r_{3n+1}`, `U=r_{3n+3}`:

```
x(2,-1) = 1
x(2,-2) = 1 XOR U
x(2,-3) = U XOR r_4
x(2,-4) = 0
```

The unreduced ANF in the two 0-phase streams is the zero polynomial
(`cell_anf(2,-4)`), so the identity does not use `u v=0` or the
isolated-one reset.

Onset `T=4` in this phase is impossible. Continuation that lands on a 1
of the center with depth 4 (for example onset phase 0 and `T=2`, time
`s=2`) is likewise impossible.

### `011`: plateau and `B_4=0`

One injected bit `u_n=r_{3n}` per period, unconstrained (`q=2≥2`). At
the 0-phase,

```
x(3n,-1) = x(3n,-2) = x(3n,-3) = 1 + u_n.
```

So a leftmost 1 at column `-T` with `T∈{1,2}` cannot have a zero
immediately to its left at a 0-phase onset. At the first 1,

```
x(3n+1,-1) = 0,   x(3n+1,-2) = 0,   x(3n+1,-4) = 0,
x(3n+1,-8) = 1.
```

The depths 1, 2, 4 vanish; 8 is identically 1, after which the
polynomials are mixed. Same shape as period 2’s `F_4`, not an infinite
family.

### `0111`: `x(4n,-4)=0`

Again one unconstrained bit `u_n=r_{4n}`. Double-1 plus a one-line OR
identity:

```
x(4n,-1) = 1 + u_n
x(4n,-2) = 1 + u_n
x(4n+1,-2) = 1,          (double-1, next bit is 1)
x(4n,-3) = u_n
x(4n+2,-2) = 0,          (double-1, next bit is the isolated 0)
x(4n+1,-3) = 1
x(4n,-4) = 1 XOR (u_n OR (1+u_n)) = 1 XOR 1 = 0.
```

This is the exact period-4 analogue of `F_4`, and it holds at every
isolated-zero time, with no constraint on `u`. Among isolated-zero words
`01^q` it is special to `q=3`: for `q≥4` the same expansion gives
`x(0,-4)=1`. Phases 2 and 3 of `0111` also have `x(-4)=0`; phase 1 is
`1+u_{n+1}`, mixed. Column `-4` is therefore not periodic, so Jen does
not apply.

## `L_0` lifetimes, `T≤8`

On-demand SAT (`fast_chain`, extra two zeros past the edge) for every
rotation of `001`, `011`, `0001`, `0011`, `0111` and `T=1..8`:

- Many onsets are unsatisfiable (`max_s=-1`), matching the identities
  above (`011` with `T=1,2,4`; `0111` with `T=4`; `001` with `T=1,5` in
  the lexicographic rotation, `T=4` in the `100` rotation, …).
- Every satisfiable onset dies by time `s≤4` in this range. The longest
  survivor seen is `0001` at `T=4`, which holds for `s=0..4` and fails
  at `s=5` even with `smax=8`.
- Isolated-zero `011` at `T=8` lasts four times (`s=0..3`), then dies.

This is the same shape as the period-2 table in
`period2_left_edge.md`: finite lifetime for every checked `T`, no
uniform-in-`T` bound. The search enumerates only Markov `r`, a superset
of realizable right halves, so an unsat here is a proof for that finite
`(w,T,extra)`; a sat is not a spacetime witness.

## What would finish a period

Any one of:

1. a left column that is *eventually periodic on every phase*, or a
   forced periodic neighbor, for Jen/Kopra;
2. a vanishing identity whose depth tracks the moving edge (depth
   `T+s`, not a fixed `k`);
3. an `O(1)` lifetime bound that is uniform in `T`.

None of the three is proved. Residual strip SCCs at radius 6–8
(`small_periods.md`) remain consistent with an aperiodic injected `r`
that keeps the left edge alive for a while and then dies — exactly what
the SAT table shows for small `T`.
