# Period-2 unique left of a periodic even-right neighbor

Checked lemma: if a phase-`01` period-2 centre has even right neighbor
`u` of any finite period, the unique left is spatially eventually
periodic and has infinitely many `1`s. This is the Condrey-style
infinitude for the whole periodic-`u` class.
`research/period2_mod7.md` is the explicit period-7 word at period 2.
It does **not** exclude eventual period 2 for every finite row — Jen
already forbids eventually-periodic `u` for a nonzero finite seed, and
the remaining obstruction is aperiodic `u`. Not a prize claim.

Helper: `python3 research/period2_periodic.py --certify`. Dump:
`research/period2_periodic.json`. Column recurrences as in
`research/period2_left_edge.md`; spatial identity as in
`research/period2_vacuum.md`. Does not modify those files.

## Lemma (global zero is unreachable)

Assume `c_{2n}=0`, `c_{2n+1}=1`, and `u_{n+p}=u_n` for some `p\ge 1`.
Write `F^{(j)}_k=F_k(S^j u)` and `G^{(j)}_k` for the left columns of
the `j`-th shift, `j\in\mathbb Z/p`. The recurrences

```
F^{(j)}_k = G^{(j)}_{k-1} XOR (F^{(j)}_{k-1} OR F^{(j)}_{k-2}),
G^{(j)}_k = F^{(j+1)}_{k-1} XOR (G^{(j)}_{k-1} OR G^{(j)}_{k-2}),
```

close on the `4p`-bit state
`(F_{k-1},F_{k-2},G_{k-1},G_{k-2})` of every phase. Initial data:
`F_0=0`, `G_0=1`, `F_1=1+u_j`, `G_1=1`.

The global-zero state (every phase has those four bits `0`) is a fixed
point. It is the unique preimage of itself: if the image is global
zero then `F_{k-1}=G_{k-1}=0` already, and

```
F_k = F_{k-2},     G_k = G_{k-2},
```

so the previous two columns vanish as well. Certified by enumerating
all `2^{4p}` states for `p\le 4`. The initial state has `G_0=1`, so
the orbit never visits global zero.

## Lemma (periodic `u` forces an infinite unique left)

The state space is finite, so `(F_k)` is eventually periodic in the
column index. If it were eventually `0`, the cycle would have
`F^{(0)}=0` at every cycle index. The spatial identity
`G_k=F_{k+1} XOR (F_k OR F_{k-1})` (`k\ge 1`) then forces `G^{(0)}=0`
on the cycle, and the fold `G_k=F_{k-1}(Su) XOR (G_{k-1} OR G_{k-2})`
forces `F^{(1)}=0`. Iterating around the circle, every phase vanishes
and the cycle is global zero, contradicting the previous lemma.

Hence `F_k` has infinitely many `1`s. The unique left is a spatially
eventually-periodic infinite word.

## Checks

- Period `1` is vacuum: `F_k=k\bmod 2`, matching
  `research/period2_vacuum.md`.
- Period `2` recovers `(1000000)^\infty` and `(0110010)^\infty` from
  `research/period2_mod7.md`.
- The `p`-phase FSM matches the ANF fold `F_of_u` and
  `compute_columns` through `k=16` on vacuum, both oscillators,
  `(001)^\infty`, `(0001)^\infty`, and `(00100)^\infty`.
- Spatial identity holds on those orbits through column `48`.
- Every circular ugap word of period `p\le 7` (the SFT forbidding
  `{11,00000}` wrapping around) has an `F`-cycle containing a `1`.
- Period `4` word `0001`: after an 11-column transient the `F`-track
  is `(0000010)^\infty`, another explicit period-7 tail.

## What this does not do

A finite seed whose even right neighbor is eventually periodic already
makes every reconstructed left *column* eventually periodic
(`research/alternating.md`), so Jen/Kopra width 2 applies. The lemma
is the same exclusion read on the spatial left instead of on `u`.
Generic finite rights have aperiodic `u` (BM of the spatial left
grows; `research/period2_fiber.md`). The missing step for period 2 is
still a last `1` in `F_k` for aperiodic `u`, or a uniform `L_0`
bound.

The argument uses finiteness of the `p`-phase state. It does not
apply to aperiodic `u`: there the shifts `S^j u` are all distinct and
the 011-bump of an `L_0` germ (`research/period2_germ.md`) lives on a
different shift, not a contradiction.

`L_1\oplus L_2=1` holds for every `u`, periodic or not. That is not
infinitude.

## Verdict

`LEMMA`, wall time <1s.

- Kill of period 2 for every finite seed: no.
- Infinite unique left on every periodic `u`: yes.
- Closed form except `p=1,2` and the `p=4` tail `0001`: no (cycles of
  length `84,155,138,728,1316` for primitive `p=3,5,6,7`).
- Witness finite bimaterial period-2 row: none.

## Files

- `research/period2_periodic.md` (this note)
- `research/period2_periodic.py` (`--certify`)
- `research/period2_periodic.json` (dump)
