# Period-2 unique left of an alternating even-right neighbor

Checked lemma: if a phase-`01` period-2 centre has even right neighbor
`u` strictly alternating, the unique left is an explicit period-7
word, hence infinite. Two finite rights realise the two oscillators
through the certified horizon. This is a Condrey-style closed form
for that class. It does **not** exclude eventual period 2 for every
finite row — Jen already forbids eventually-periodic `u` for a
nonzero finite seed, and the remaining obstruction is aperiodic `u`.
Not a prize claim.

Helper: `python3 research/period2_mod7.py --certify`. Dump:
`research/period2_mod7.json`. Column recurrences as in
`research/period2_left_edge.md`; vacuum-triple identity as in
`research/period2_neighbor.md`. Does not modify those files.

## Lemma (alternating `u` forces a period-7 left)

Assume `c_{2n}=0`, `c_{2n+1}=1`, and `u_n=x(2n,1)` satisfies
`u_{n+1}=1-u_n` for every `n`. Write `F_k=x(2n,-k)` and
`G_k=x(2n+1,-k)` as functions of `(u_n,u_{n+1},\ldots)`, and
`F',G'` for the same columns on the shifted sequence `Su`. The
spatial recurrences

```
F_k = G_{k-1} XOR (F_{k-1} OR F_{k-2}),
G_k = F'_{k-1} XOR (G_{k-1} OR G_{k-2}),
```

and the symmetric pair for `(F',G')`, close on eight bits
`(F_{k-1},F_{k-2},G_{k-1},G_{k-2},F'_{k-1},F'_{k-2},G'_{k-1},G'_{k-2})`.
Initial data: `F_0=0`, `G_0=1`, `F_1=1+u_0`, `G_1=1`, and the same
with `u_0` flipped for the shift.

That 8-bit state is period 7 for both values of `u_0`
(`state_7cycle`). The `F`-track is

- `u_0=0`: `(1000000)^∞`, i.e. `L_k=1` iff `k\equiv 1\pmod 7`;
- `u_0=1`: `(0110010)^∞`.

Each block contains at least one `1`, so the unique left has
infinitely many `1`s. The same values match the ANF of `F_k` on
`(01)^∞` and `(10)^∞` through `k=16`.

If `e_n=f_n=0` at every even time, the vacuum-triple identity
`u_{n+1}=1` iff `(u_n,e_n,f_n)=(0,0,0)` collapses to
`u_{n+1}=1-u_n`. So even-time vacuum in columns `2` and `3` is a
sufficient condition for the lemma.

## Kernel rights

The length-6 right `000001` (a single `1` at position `6`) has
`(u_0,e_0,f_0)=(0,0,0)`, hence `u_1=1`. Through `T=256` even-time
`e=f=0` and `u=(01)^∞`, and the reconstructed left equals
`(1000000)^∞` on `256` bits (prefix-stable at `T=64`). The dual
right `1001` has `u_0=1`, `u=(10)^∞`, and left `(0110010)^∞`.

Every width-`≤8` right with even-time `e=f=0` (`22` of them) lies
in one of those two families and matches the corresponding word.
Vacuum is not an oscillator. The prefix `000001` is not freely
extendable: `00000111` already makes `e` or `f` fire.

Do **not** PREFIX that `000001` keeps `e=f=0` for all time from the
`T=256` window. The FSM lemma itself has no time cap: it applies
whenever `u` is strictly alternating, for as long as that holds.

## What this does not do

A finite seed whose even right neighbor is eventually periodic
already makes every reconstructed left *column* eventually periodic
(`research/alternating.md`), so Jen/Kopra width 2 applies. The
kernel is consistent with that: its unique left is the infinite
period-7 word, so those rights cannot occur with a finite left and
a period-2 centre. Generic finite rights have aperiodic `u` (BM of
the spatial left grows; `research/period2_fiber.md`). The missing
step for period 2 is still a last `1` in `F_k` for aperiodic `u`,
or a uniform `L_0` bound. Infinitude for every finite period of
`u`, not just period 2, is `research/period2_periodic.md`.

`L_1\oplus L_2=1` holds for every `u` (`F_1=1+u_0`, `F_2=u_0`), so
every unique left has a `1` at depth `1` or `2`. That is not
infinitude.

## Verdict

`LEMMA`, wall time <1s.

- Kill of period 2 for every finite seed: no.
- Closed-form infinite unique left on alternating `u`: yes.
- Witness finite bimaterial period-2 row: none.

## Files

- `research/period2_mod7.md` (this note)
- `research/period2_mod7.py` (`--certify`)
- `research/period2_mod7.json` (dump)
