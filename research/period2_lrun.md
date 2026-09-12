# Period-2 `L_run`: radius 11 kills the constant 24

This note extends Cycle I (`research/period2_fiber.md`). It does **not**
exclude eventual period 2 for every finite row, and it does not claim a
prize result. It does **not** give a uniform-in-`w` bound.

Helper: `research/period2_lrun.py --certify`. Dump:
`research/period2_lrun.json`. Packed evolution is imported from
`research/period2_fiber.py` and that file is not modified.

## Attack

Cycle I proved: every nonzero finite row of support radius `w≤10` has
every period-2 centre run of length at most 24, **inside**
`tcap=8w+128`. The table plateaued at `L_run(w)=24` for `6≤w≤10`, with
maximizer `w=6` mask `7503`, a run of 24 from `t=94`. A bound
`L_run≤24` for every `w` would exclude an eventually period-2 centre
for every finite seed (a genuine eventual regime is an unbounded run).
The question is whether 24 upgrades to more radii, or dies.

**Kill:** a finite nonzero row with a period-2 centre run of length
`≥25` that still holds after doubling `tcap`.

**Finite-theorem extension:** exhaustive `w=11` also has `L_run≤24`.

**Survive / uniform proof:** a proof that `L_run≤24` for all `w`. Not
claimed; the scan kills the constant.

Packed Rule 30 is the Cycle I engine:

```
new = (row << 2) ^ ((row << 1) | row)
```

with the centre bit at time `t` equal to `(row >> (w+t)) & 1`. Bit 0 is
the leftmost cell of the current support (spatial `-w` at `t=0`).

## Self-checks

- `w=0` (prize seed, mask `1`), `tcap=128`: `L_run=7`.
- `w=6` mask `7503`, row `1111001010111`, `tcap=176`: a run of 24 from
  `t=94` to `t=118`.
- Inlined inner loop agrees with `period2_fiber.scan_mask_runs`.
- Packed traces match the independent live-cell spacetime on the prize
  seed and on mask `7503`.
- Zero-padding `7503` to `w=7,8,11,12` leaves the centre trace unchanged
  on the common window.

## Exhaustive `w=11`

`2^{23}-1 = 8 388 607` nonzero states, `tcap=8·11+128=216`. A probe gave
~3.2×10^4 masks/s, ~266s serial, ~67s on 4 processes; well under the
900s timeout, so the full enumeration ran (107.8s wall for the scan).

| `w` | states | `tcap` | `L_run` | `L_prefix` | mode |
|----:|-------:|-------:|--------:|-----------:|------|
| 0 | 1 | 128 | 7 | 1 | this run |
| 1 | 7 | 136 | 8 | 7 | Cycle I |
| 2 | 31 | 144 | 10 | 7 | Cycle I |
| 3 | 127 | 152 | 13 | 7 | Cycle I |
| 4 | 511 | 160 | 15 | 7 | Cycle I |
| 5 | 2047 | 168 | 15 | 9 | Cycle I |
| 6 | 8191 | 176 | 24 | 10 | this run |
| 7 | 32767 | 184 | 24 | 10 | Cycle I |
| 8 | 131071 | 192 | 24 | 15 | Cycle I |
| 9 | 524287 | 200 | 24 | 17 | Cycle I |
| 10 | 2097151 | 208 | 24 | 17 | Cycle I |
| 11 | 8388607 | 216 | **29** | 17 | this run, exhaustive |
| 12 | — | 224 | ≥29 | — | `w=11` maximizer embedded |
| 13 | — | 232 | ≥29 | — | embedded |
| 16 | — | 256 | ≥29 | — | embedded |
| 20 | — | 288 | ≥29 | — | embedded |

`L_run(11)=29`. Ten nonzero masks have a period-2 centre run of length
at least 25; each still has `L≥25` after doubling to `tcap=432`. None
has `L>4w+16=60`. `L_prefix(11)=17` matches the `w=9,10` plateau
(compatible with Condrey’s `H(2,w)≥w` lower bound on prefixes, and not
an escape). No scanned run is eventual in the cap: the longest suffix
is 21, the `L=29` bursts are interior.

## Witness

Least mask among the two length-29 rows:

- `w=11`, mask `4369552`
- packed row (bit 0 = spatial `-11`): `00001001001101010100001`
- live cells at `-7,-4,-1,0,2,4,6,11` (8 ones, span 19, true radius 11)
- run of 29 from `t=159` to `t=188` (exclusive end), bits
  `01010101010101010101010101010`
- the bits immediately before and after are both `0`, so the factor
  really breaks
- `tcap=216` and `tcap=432` give the same `(L,start,end)=(29,159,188)`

Packed, fast loop, and naive live-cell spacetime agree on this row
(`witness_check.ok`). Embedding the same physical row in radius
`12,13,16,20` (zeros on both sides) keeps `L=29` at `8w+128` and at
`2·(8w+128)`. Larger `tcap` does not lengthen the burst.

The other length-29 row is mask `4842768`, live at
`-7,-3,-1,2,3,4,5,8,11`, same time window `t=159..188`.

These are finite bursts, not eventual period 2. After `t=188` the
centre is no longer alternating.

## A radius-10 run truncated by Cycle I’s cap

One of the ten `L≥25` masks is a radius-10 row viewed at `w=11`:

- true radius 10, mask `1082165`, row `101011001100000100001`
- live at `-10,-8,-6,-5,-2,-1,5,10`
- at Cycle I’s `tcap=8·10+128=208` the engine reports `L=22`, start
  `186`, end `208` (the run is still going at the cap)
- extending to `tcap=416` completes a run of **25** from `t=186` to
  `t=211`

Cycle I’s finite theorem remains correct as a statement *inside*
`tcap=8w+128`: this row only scores 22 in that window, and the Cycle I
cap-extension predicate (suffix `≥16` after a light-cone transient, or
suffix `≥ max(16,L_run)`) does not fire, because the break at `t=186`
is far past `2w+8` and the truncated suffix `22` is below the then
global `L_run=24`. Three extra time steps reveal length 25. So the
plateau at 24 is not a cap-independent fact even at radius 10.

The `w=11` maximizers are not in this class: they have a live cell at
`+11`, need true radius 11, and their length-29 runs sit well inside
`tcap=216`.

## Samples at `w=12` (not needed for the kill)

Exhaustive `w=11` finished, so the prescribed fallback is only extra
radius. At `w=12`, `tcap=224`:

- `2^{20}` random nonzero masks: `L_run=24` (none `≥25`)
- every mask whose live bits lie in a single interval of length `≤10`,
  all placements in `[-12,12]`: `L_run=21`
- `w=6` maximizer `7503` padded by zeros: `L_run=24`, same run
  `t=94..118` as at `w=6`

Those families miss the kill: the length-29 supports have span 19, and
a `2^{20}` sample of `2^{25}` states is too thin to hit a 10-element
subset of a `2^{23}` slice. The embedded `w=11` maximizer is the
`w=12` lower bound `L_run(12)≥29`. Exhaustive `w=12` was not run.

## What is proved, what is not

Proved (machine-checked in this run):

- The Cycle I packed engine, on every nonzero radius-11 row, produces a
  longest period-2 centre run of length `L_run(11)=29` inside
  `tcap=216`.
- Mask `4369552` (and nine other radius-`≤11` rows) has a run of length
  `≥25` that is unchanged by doubling `tcap`.
- Mask `1082165` is a radius-10 row whose length-25 run is invisible
  at `tcap=208` and visible at `tcap=416`.
- Self-checks: `w=0` has `L_run=7`; `w=6` mask `7503` has a run of 24
  from `t=94`.

Not proved:

- Any uniform bound `L_run(w)≤C`. The constant 24 is false. Whether
  `L_run` is bounded in `w` at all is open; the `w=11` maximizer does
  not grow when padded.
- Eventual period 2 of any finite seed, including the prize seed. A
  bounded burst is compatible with every centre eventually leaving
  period 2, and with some larger-radius row staying in period 2
  forever. This kill is of the constant-24 claim, not of eventual
  period 2.
- Exhaustive `L_run(12)`. Only a lower bound 29.

## Verdict

`KILL`, wall time 151.4s.

- Kill: yes. Witness `w=11` mask `4369552`, `L=29` at `tcap=216` and
  at `tcap=432`.
- Survive / uniform proof: no.
- Finite theorem extension to `w≤11`: no (`L_run(11)=29`).
- Cycle I’s finite theorem for `w≤10` inside `tcap=8w+128` is
  untouched as a capped statement, and is not a cap-free `L_run≤24`.

## Files

- `research/period2_lrun.md` (this note)
- `research/period2_lrun.py` (`--certify` runs the checks, exhaustive
  `w=11`, `w=12` samples, embeddings, and cap-truncation rescans)
- `research/period2_lrun.json` (dump)
