# Period-2 `L_run` families: length 31, no unbounded construction

This note extends Cycle J (`research/period2_lrun.md`). It does **not**
exclude eventual period 2 for every finite row, and it does not claim a
prize result. It does **not** prove that `L_run` is bounded or unbounded.

Helper: `research/period2_lrun_family.py --certify`. Dump:
`research/period2_lrun_family.json`. Packed evolution is imported from
`research/period2_fiber.py` and that file is not modified.

## Attack

Cycle J killed `L_run≤24`: radius-11 mask `4369552` has a period-2
centre run of length 29. Zero-padding that row does not lengthen the
burst. ideas10 item 2 asks whether a one-parameter family of finite
rows can make the longest period-2 centre run `L` tend to infinity
(for example `L≥20+k/2` at spacing `k`). A family with `L(param)→∞`
would kill every constant bound on `L_run`. A proof that `L_run=O(1)`
would still exclude eventual period 2.

**Kill of a uniform bound:** a constructive family whose `L` grows in
the parameter.

**Kill of this search:** no row with `L≥30` in the prescribed
families, and no `O(1)` proof. (If the best `L` stays 29, the
concat/motif construction is dead; that is not a proof of a bound.)

**Hunt:** `L≥30`, then `L≥40` if it appears.

Packed Rule 30 is the Cycle I engine:

```
new = (row << 2) ^ ((row << 1) | row)
```

with the centre bit at time `t` equal to `(row >> (w+t)) & 1`. Bit 0 is
the leftmost cell of the current support (spatial `-w` at `t=0`).
Family scans use `tcap=8w+256` (Cycle J used `8w+128`). Any `L≥30`
candidate is re-evolved at `2·tcap`.

## Self-checks

- `w=11` mask `4369552`, `tcap=216`: `L=29` from `t=159` to `t=188`.
  Live cells `-7,-4,-1,0,2,4,6,11`. The family cap `8·11+256=344` still
  reports `(29,159,188)`.
- `w=6` mask `7503`, `tcap=176`: a run of 24 from `t=94`.
- Inlined inner loop agrees with `period2_fiber.scan_mask_runs`.
- Packed traces match the independent live-cell spacetime on the prize
  seed and on mask `4369552`.
- Zero-padding `4369552` to `w=12,13,16,20` leaves the centre trace
  unchanged on the common window and keeps `L=29` at `8w+256`.

## Concatenate two copies

Take the live-support block of a maximizer (first live cell through
last live cell) and concatenate two copies separated by `k=0..64`
zeros. Slide the rigid pair through the origin, including fully left
and fully right of cell 0.

| source | block | `n` | `L` | `L(k=0)` | `L(k=64)` | `k` with `L` equal to the single-copy burst |
|--------|-------|----:|----:|---------:|----------:|---------------------------------------------|
| `4369552` | `1001001101010100001` (span 19) | 4680 | 29 | 12 | 15 | 47, 51, 54 |
| `7503` | `1111001010111` (span 13) | 3900 | 24 | 11 | 24 | recovers 24 at large `k`, never 29 |
| `4842768` | `1000101001111001001` (span 19) | 4680 | 29 | 12 | 17 | 50, 52, 61, 62 |

None satisfies `L≥20+k/2` (0 of 65 spacings). Adjacent copies interfere
and *shorten* the burst (`L=12` at `k=0` for `4369552`). The length-29
rows are recoveries of the single-copy burst: one copy sits at the
Cycle J placement, the other is far enough to the right that it does
not feed the centre during `t=159..188`. Example: `k=47`, leftmost
`-7`, live `{-7,-4,-1,0,2,4,6,11}` union the same motif shifted by 66.
The run is still `t=159..188`, `L=29` at `tcap=872` and at `1744`.

Two distant copies do not add. Padding zeros between them does not
lengthen the burst past the single-copy `L`.

## Repeat the 8-one motif

The `4369552` motif (live at `-7,-4,-1,0,2,4,6,11` relative to a local
origin) is repeated at `n=2,3,4,5` copies and spacings `d=1..64`, plus
`n=6,8` at a few large `d`. All placements through the origin.
`n=29668` rows.

`L_run=24`. Repeating the motif *destroys* the length-29 burst. At
spacing 64, `L` versus `n` is `15,17,16,19,19,21` for `n=2..8`: a slow
rise that stays well below 29. No spacing has `L` growing like
`20+d/2`.

The same experiment on the `7503` motif (`n=2,3,4`, `d=1..64`,
`n=15360`) reaches `L=27` at four copies, spacing 12 (true radius 41).
That beats the single-copy `L=24` and still holds after doubling
`tcap`, but it is a finite bump, not an unbounded family, and it is
below 29.

## Random Hamming-weight masks

For each `w=12..16` and each Hamming weight `8..16`, `2^18` samples,
`tcap=8w+256`. Total `11 796 480` rows.

| `w` | `tcap` | `n` | `L_run` | `n≥29` | `n≥30` |
|----:|-------:|----:|--------:|-------:|-------:|
| 12 | 352 | 2359296 | 29 | 3 | 0 |
| 13 | 360 | 2359296 | 29 | 2 | 0 |
| 14 | 368 | 2359296 | **30** | 2 | 1 |
| 15 | 376 | 2359296 | 29 | 3 | 0 |
| 16 | 384 | 2359296 | 29 | 5 | 0 |

The length-30 row is `w=14`, weight 8, mask `403448386`, live at
`-13,-8,-5,-1,4,5,13,14` (span 28). Run of 30 from `t=219` to `t=249`,
stable at `tcap=736`. At Cycle J’s cap `8·14+128=240` the same run is
still going (`L=21`, suffix 21): another cap truncation, the same
kind Cycle J saw on mask `1082165`.

No sampled row has `L≥40`.

## Single-interval supports of length `≤20`

Exact convex support of length `ℓ` (first and last cells live), every
placement inside radius 20, `tcap=416`. `12 058 623` rows. Zero
padding to `w=20` does not change the centre trace; the family cap is
at least `8w+256` of every smaller true radius.

| `ℓ` | `L_run` | `n≥29` | `n≥30` |
|----:|--------:|-------:|-------:|
| 1–6 | 16 | 0 | 0 |
| 7 | 19 | 0 | 0 |
| 8 | 23 | 0 | 0 |
| 9–12 | 21 | 0 | 0 |
| 13 | 24 | 0 | 0 |
| 14–15 | 25 | 0 | 0 |
| 16 | 26 | 0 | 0 |
| 17 | 28 | 0 | 0 |
| 18 | 29 | 1 | 0 |
| **19** | **31** | 4 | 1 |
| 20 | 31 | 8 | 1 |

Max `L` among span-`ℓ` rows rose through `ℓ=19` and matched at `ℓ=20`.
Least squares on this window is `L≈0.85ℓ+14`. That is an enumeration
maximum, not a constructive iterate, and it is not the bound
`L≥20+ℓ/2` (only 4 of 20 lengths hit that comparison). A plateau at 31
for `ℓ=19` and `ℓ=20` is compatible with slow growth of `L_run` with
span; it is not a proof that `L` tends to infinity.

## Witness, `L=31`

Least true-radius row among the length-31 interval supports:

- true radius 17, mask `281769`
- packed row (bit 0 = spatial `-17`): `10010101001100100010000000000000000`
- live at `-17,-14,-12,-10,-7,-6,-3,1` (8 ones, span 19)
- run of 31 from `t=320` to `t=351` (exclusive end), bits
  `0101010101010101010101010101010`
- bits immediately before and after are both `0`
- `tcap=392` (`8·17+256`) and `tcap=784` give the same
  `(L,start,end)=(31,320,351)`

Packed, fast loop, and naive live-cell spacetime agree
(`witness_check.ok`, `verify_ok`). The same physical row scanned at
`w=20` (zeros on the right) is mask `2254152`, same run.

Cycle J’s cap `8w+128=264` **misses the burst entirely** and reports
`L=6` (a short interior run at `t=173..179`). The length-31 factor
starts at `t=320>264`. So `8w+128` is not a cap-free statement of
`L_run(17)` for this row.

The length-20 maximizer is the same live set plus a 1 at `+2`
(mask `806057` at `w=17`). Same window `t=320..351`, still `L=31`.

These are finite bursts, not eventual period 2. After `t=351` the
centre is no longer alternating.

## What is proved, what is not

Proved (machine-checked in this run):

- Mask `4369552` at `w=11` still has `L=29`. Zero-padding it does not
  lengthen the burst.
- Concatenating two copies of that support (or of `7503`, or of
  `4842768`) with `k=0..64` zeros, all placements, never produces
  `L≥30`. The single-copy burst is the ceiling of that family.
- Repeating the 8-one motif at `n=2..8` and spacings `1..64` never
  produces `L≥29`. Four copies of `7503` reach 27, not 30.
- A finite row of true radius 17, mask `281769`, has a period-2
  centre run of length 31 that is unchanged by doubling `tcap`.
- A radius-14 weight-8 row has a run of length 30, truncated to 21
  at `tcap=8w+128`.
- Self-checks as above.

Not proved:

- Any family with `L(param)→∞`. The prescribed constructions do not
  grow. The span-`ℓ` envelope rose through 19 and flattened at 31;
  that is a 20-point table, not an unbounded construction.
- `L≥40`. Absent in `2.4×10^7` family/random/interval rows.
- A uniform bound `L_run(w)≤C`. The constant 29 is false. Whether
  `L_run` is bounded in `w` remains open.
- Eventual period 2 of any finite seed. A bounded burst of length 31
  is compatible with every centre eventually leaving period 2.

## Verdict

`L_GE_30`, wall time 630.5s.

- Kill of a uniform bound by a growing family: **no**. Concat and
  motif-repeat do not make `L` grow with the spacing (in particular
  none satisfies `L≥20+k/2`). Two copies recover at most the
  single-copy burst.
- Kill of the constructive-unbounded search as specified: the
  concat/repeat constructions are dead as a route to unbounded `L`.
  That is not a proof of a bound, and it is not ideas10’s “no
  `L≥30`” kill — a row with `L=31` exists.
- `L≥40`: no.
- Survive / uniform proof: no.

The Cycle J constant 29 is false in the same sense 24 was: a finite
nonzero row, here radius 17, has a longer interior burst that survives
doubling the family cap. The burst sits past `8w+128`, so that cap is
too tight to see it.

## Files

- `research/period2_lrun_family.md` (this note)
- `research/period2_lrun_family.py` (`--certify` runs the checks,
  concat, motif repeats, random Hamming-weight samples, interval
  supports, true-radius rescans, and cap comparisons)
- `research/period2_lrun_family.json` (dump)
