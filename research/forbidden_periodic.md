# Forbidden spacetime blocks forced by a period-2 centre

This note is ideas11 item 2 (leftover ideas10 item 5, prize
Problem 1). It does **not** exclude eventual period 2, and it
does not claim a prize result.

Helper: `research/forbidden_periodic.py --certify`. Dump:
`research/forbidden_periodic.json`. The finite-strip graph is
imported from `strip_graph.graph` / `analyze` / `components`;
`strip_graph.py` is not modified.

## Attack

Let F be the finite list of h×w binary blocks that
Rule 30 **forbids locally**: some interior cell violates

```
x' = L XOR (C OR R).
```

Those blocks cannot appear in any Rule 30 spacetime. Under a
forced period-2 centre (both phases `01` and `10`), look at
columns -1..+1 (radius 1) and -2..+2 (radius 2) in the
finite-strip graph of `research/strip_graph.py`. If some block
of F is forced on every sufficiently long path, period 2 is
impossible.

This is **not** residual-SCC emptiness. Emptiness would kill
period 2 by leaving no infinite strip completion. A nonempty
residual means every locally legal period-2 strip path exists,
so a locally illegal pattern cannot be forced. That is the
predeclared kill for this route.

**Kill:** no block of F is forced, because every locally legal
period-2 strip path exists (the known residual SCC).

## Local forbidden list F

A cell at row r≥1, column c with 1≤c≤w-2
is interior: its neighbourhood on the previous row lies inside
the block. Edge columns are unconstrained. Row 0 is free; each
later row contributes two free edge bits and w-2 determined
interior bits, so

```
|legal(h,w)| = 2^{w + 2(h-1)}     (h>=2, w>=3).
```

There is no overconstraint: each determined bit depends only on
the already-chosen previous row. Enumeration matches the formula.

| block | total | legal | forbidden | formula legal |
|---|---:|---:|---:|---:|
| 3×3 | 512 | 128 | 384 | 128 |
| 4×4 | 65536 | 1024 | 64512 | 1024 |

Encoding: row-major, cell (r,c) is bit r*w+c, bit 0 =
top-left. The JSON dump lists every forbidden 3×3 as an integer
(`sha256` `51dd46f497701c2b…`) and every legal 4×4;
the 64512 forbidden 4×4 blocks are the bitset
`F.4x4.forbidden_bitset_hex` (bit i set iff block i is
forbidden; `sha256` `5b4a635e8fa03cfd…`).

Example. The 3×3 with top row `111` and middle centre `1` is
forbidden: `1 XOR (1 OR 1) = 0`. The all-zero 3×3 is legal
(vacuum). Both checks are in `checks`.

F is **local-rule violations**, not the (possibly larger) sofic
list of blocks that are locally fine but do not extend to a
global spacetime. The attack is specifically that the periodic
centre plus the local rule would still force a locally illegal
tile.

## Period-2 strip, both phases

`strip_graph.graph(radius, word)` is imported and not edited.
A genuine eventual period-2 centre must eventually walk in a
recurrent SCC at every fixed width. Residual SCCs are those
that do **not** force a periodic neighbour (Jen already excludes
the ones that do). Outer boundary bits are free, so a residual
path is an overapproximation of the prize spacetime.

| word | radius | residual SCCs | residual vertices | residual edges | forced columns | illegal residual edges | illegal F-windows | forced F |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| `01` | 1 | 1 | 4 | 8 | `0` | 0 | 0 | 0 |
| `01` | 2 | 1 | 8 | 16 | `0` | 0 | 0 | 0 |
| `10` | 1 | 1 | 4 | 8 | `0` | 0 | 0 | 0 |
| `10` | 2 | 1 | 8 | 16 | `0` | 0 | 0 | 0 |

Radius 1 is columns -1,0,+1; radius 2 is -2..+2. The
sizes 4 and 8 match `research/strip_results.json` for `01`.
Phase `10` is the same graph shifted by one step; it has the
same residual counts. In every residual vertex the centre bit
equals the imposed phase, and columns ±1 (and ±2 at radius 2)
take **both** values. Nothing in those columns is forced except
the prescribed centre. Residual rows, bit 0 = column −radius:

| word | radius | phase 0 rows | phase 1 rows |
|---|---:|---|---|
| `01` | 1 | `001`, `100` | `110`, `111` |
| `01` | 2 | `01000`, `01001`, `10010`, `10011` | `01101`, `01110`, `01111`, `11100` |
| `10` | 1 | `110`, `111` | `001`, `100` |
| `10` | 2 | `01101`, `01110`, `01111`, `11100` | `01000`, `01001`, `10010`, `10011` |

Phase `01` radius 1 already has two rows at each phase
(`001`/`100` with centre 0, and `110`/`111` with centre 1), so
a single 3-wide block is not forced.

Every residual edge was checked against the local rule on all
interior cells of the strip. There are none that violate it:
the graph is defined that way. Consequently every 3×3 window in
columns -1..+1 on a 3-row residual walk, and every 4×4
window in -2..+1 or -1..+2 on a 4-row residual walk, is
locally legal, hence not in F. Walking every such path on these
tiny residual graphs (4 or 8 vertices) finds 0 members of F.
No 3×3 or 4×4 tile at all — legal or not — is common to every
simple residual cycle (`n_unavoidable_windows = 0`), so nothing
in those columns is forced as a block. Intersecting with F is
empty.

A nonempty residual cycle is already an infinite locally legal
period-2 strip path. That path avoids every block of F, so no
block of F is forced on every sufficiently long path.

Period-3 residual SCCs at the same radii are also nonempty
(`001` / `011`), so the same obstruction would apply there.
The scan target was period 2.

## Prize seed spacetime

Evolve the single 1 for 64 steps, two ways: the
live-cell map `x(t+1,j)=x(t,j-1) XOR (x(t,j) OR x(t,j+1))`,
and the packed recurrence `row = (row<<2)^((row<<1)|row)` with
bit k at time t equal to spatial k-t. The two
spacetimes agree. The centre prefix is
`1101110011000101`, matching `experiment.center_bits`.

Every 3×3 and 4×4 window with a 3-cell vacuum margin, including
quiescent zeros outside the light cone, is locally legal.

| windows | scanned | illegal |
|---|---:|---:|
| 3×3 | 8379 | 0 |
| 4×4 | 8184 | 0 |

A planted centre-bit flip at t=5 is detected by the same
scanner, so the zero count is not a dead checker.

## Engine

- Local legality: interior cells only, as above. Independent
  count 2^{w+2(h-1)} agrees with the 512- and 65536-loop.
- Strip: `from strip_graph import graph, analyze, components`.
  Residual classification is `analyze(..., witnesses=True)`;
  walks and interior-rule checks use `graph` directly.
- Packed prize evolution matches `experiment.center_bits` on
  65 centre bits and matches the live-cell spacetime on every
  stored cell. Those files are not modified.

## Verdict

**KILL.** Period-2 residual SCCs are nonempty at radii 1 and 2 for both phases 01 and 10 (the known residual: 4 and 8 vertices). Every residual edge obeys x'=L XOR (C OR R) on interior cells, so no 3x3 or 4x4 local-rule violation appears on any residual walk, and none is forced on every sufficiently long path. Only the centre column is fixed; columns ±1 and ±2 remain free. Locally illegal patterns are therefore not forced. The prize-seed spacetime through t=64 contains no illegal 3x3 (8379 windows) or 4x4 (8184 windows). Distinct from residual emptiness: the residual is nonempty, which is exactly why this forbidden-block route dies. Not a prize claim.

## What this does not show

- Eventual period 2 of the prize seed, or of any finite row.
  The residual strip is an overapproximation; a path need not
  extend to the single-seed spacetime.
- Sofic / extendable-forbidden blocks (locally legal tiles that
  still do not appear in any global spacetime). F is only the
  local-rule list.
- Residual-SCC emptiness. The residual is nonempty; that is why
  the forbidden-block hope fails.

## Checks

All 38 machine checks passed.

## Files

- `research/forbidden_periodic.md` (this note)
- `research/forbidden_periodic.py` (`--certify` runs the census,
  the strip-graph import, the prize-spacetime scan, and writes
  the dump)
- `research/forbidden_periodic.json` (dump)

