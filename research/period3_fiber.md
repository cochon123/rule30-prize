# Period-3 centre: finite-row analog of the radius-10 theorem

This note is a checked finite scan. It does **not** exclude eventual
period 3 for every finite row, and it does not claim a prize result.
It is ideas9 item 2: the period-2 exhaustive of
`research/period2_fiber.py`, repeated for exact period 3.

Helper: `research/period3_fiber.py --certify`. Dump:
`research/period3_fiber.json`.

## Attack

Prove or kill: no nonzero finite-support configuration has an
eventually period-3 central trace. Broader than the prize seed.
Not the strip-graph residual-SCC test (which still has residual
components for `001` and `011` at radius 8), not onset SAT, not
`F_T` ideal certificates, and not the unique-left fiber
reconstruction of `period2_fiber.py`.

The primitive necklaces of period 3 are `001` and `011`. All three
rotations, and therefore both families of starting phases, are
scored as global alignments

```
001, 010, 100     (necklace 001)
011, 110, 101     (necklace 011)
```

A centre factor is exact period 3 when it is a contiguous run of
one of those six infinite words. Constants `000` and `111` are
excluded (they have period 1). A period-2 alternating factor
matches a 3-bit window of `010` or `101` and then breaks, so it
does not inflate `L3`.

Kill: `L3(w)` keeps growing through `w=8` with no plateau, or a
finite row whose centre stays period 3 through the cap and still
does not break when the cap is extended. Survive a finite theorem
if `L3` plateaus at a constant on the scanned radii.

## Engine

Every nonzero initial word of support radius `w=0..8`
(`2^{2w+1}-1` states; `w=8` is `2^{17}-1`) is evolved in a
quiescent background up to `tcap = 8w+128`. Packed Rule 30
`new = (row<<2) ^ ((row<<1)|row)`, bit 0 leftmost, centre bit
`(row>>(w+t))&1`, matches `experiment.center_bits` on the prize
seed prefix of length 256 (`1101110011000101…`) and an
independent live-cell implementation on sampled small rows. The
streaming six-phase scorer matches a stored-trace scorer on those
rows.

`L_run(w) = L3(w)` is the longest such run anywhere in `[0, tcap)`.
`L_prefix(w)` is the longest exact period-3 prefix from time 0.
`L_001` / `L_011` are the same maximum restricted to one necklace.
No row is “eventual in the cap” (last break inside the light cone
`2w+8`, suffix at least 16) unless listed below.

## Exhaustive finite rows

| `w` | states | `tcap` | `L3` | `L_prefix` | `L_suffix` | `L_001` | `L_011` | `L>4w+16` | maximizer | pattern | start |
|----:|-------:|-------:|-----:|-----------:|-----------:|--------:|--------:|----------:|-----------|---------|------:|
| 0 | 1 | 128 | 11 | 5 | 2 | 7 | 11 | 0 | `1` | `101` | 106 |
| 1 | 7 | 136 | 11 | 5 | 5 | 7 | 11 | 0 | `010` | `101` | 106 |
| 2 | 31 | 144 | 12 | 6 | 5 | 12 | 12 | 0 | `10001` | `100` | 108 |
| 3 | 127 | 152 | 12 | 10 | 11 | 12 | 12 | 0 | `0100010` | `100` | 108 |
| 4 | 511 | 160 | 17 | 10 | 14 | 14 | 17 | 0 | `101001000` | `110` | 94 |
| 5 | 2047 | 168 | 18 | 10 | 12 | 16 | 18 | 0 | `11110011110` | `011` | 121 |
| 6 | 8191 | 176 | 20 | 14 | 14 | 17 | 20 | 0 | `1110100000001` | `101` | 124 |
| 7 | 32767 | 184 | 20 | 14 | 18 | 19 | 20 | 0 | `011101000000010` | `101` | 124 |
| 8 | 131071 | 192 | 22 | 17 | 19 | 21 | 22 | 0 | `10110110000111100` | `110` | 25 |

The prize seed (`w=0`) has `L3=11`, the factor `01101101101` of pattern `101` starting at time 106.
`L_prefix(0)=5` (the opening `11011` of `110110…`).

Radius-1 maximizer: row `010` (mask=2), pattern `101` (necklace `011`), run of 11 from `t=106` to `t=117` (3 masks attain `L3`). Extending that evolution to 544 steps does not lengthen the run (`ext_L=11`).
`L_prefix` maximizer at this radius: row `010` (mask=2), pattern `110`, prefix `11011` of length 5.

Radius-2 maximizer: row `10001` (mask=17), pattern `100` (necklace `001`), run of 12 from `t=108` to `t=120` (2 masks attain `L3`). Extending that evolution to 576 steps finds a later finite burst `ext_L=14` of pattern `011` at `t=148..162` (the tcap-window maximizer is not eventual).
`L_prefix` maximizer at this radius: row `01001` (mask=18), pattern `010`, prefix `010010` of length 6.

Radius-3 maximizer: row `0100010` (mask=34), pattern `100` (necklace `001`), run of 12 from `t=108` to `t=120` (9 masks attain `L3`). Extending that evolution to 608 steps finds a later finite burst `ext_L=14` of pattern `011` at `t=148..162` (the tcap-window maximizer is not eventual).
`L_prefix` maximizer at this radius: row `0100111` (mask=114), pattern `010`, prefix `0100100100` of length 10.

Radius-4 maximizer: row `101001000` (mask=37), pattern `110` (necklace `011`), run of 17 from `t=94` to `t=111` (4 masks attain `L3`). Extending that evolution to 640 steps does not lengthen the run (`ext_L=17`).
`L_prefix` maximizer at this radius: row `001001110` (mask=228), pattern `010`, prefix `0100100100` of length 10.

Radius-5 maximizer: row `11110011110` (mask=975), pattern `011` (necklace `011`), run of 18 from `t=121` to `t=139` (2 masks attain `L3`). Extending that evolution to 672 steps does not lengthen the run (`ext_L=18`).
`L_prefix` maximizer at this radius: row `10011111000` (mask=249), pattern `100`, prefix `1001001001` of length 10.

Radius-6 maximizer: row `1110100000001` (mask=4119), pattern `101` (necklace `011`), run of 20 from `t=124` to `t=144` (1 mask attains `L3`). Extending that evolution to 704 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `1000010010000` (mask=289), pattern `010`, prefix `01001001001001` of length 14.

Radius-7 maximizer: row `011101000000010` (mask=8238), pattern `101` (necklace `011`), run of 20 from `t=124` to `t=144` (4 masks attain `L3`). Extending that evolution to 736 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `010000100100000` (mask=578), pattern `010`, prefix `01001001001001` of length 14.

Radius-8 maximizer: row `10110110000111100` (mask=30829), pattern `110` (necklace `011`), run of 22 from `t=25` to `t=47` (3 masks attain `L3`). Extending that evolution to 768 steps does not lengthen the run (`ext_L=22`).
`L_prefix` maximizer at this radius: row `10011111000011100` (mask=28921), pattern `011`, prefix `01101101101101101` of length 17.

## Plateau / growth

- `L3` table: `[11, 11, 12, 12, 17, 18, 20, 20, 22]`
- maximum `22` attained at `w=[8]`
- still growing at `w_max`: `True`
- plateau at the global max: `False`
- final constant block: `L=22` on `w=8..8`

Least squares over the whole table (a summary only, not a conjecture):

- `L3 ≈ 1.550*w + 9.689`
- `L_prefix ≈ 1.517*w + 4.044`

`L_prefix` is the period-3 analogue of Condrey’s horizon `H(p,w)≥w`:
a prescribed period-3 centre of length `w` is always realised by
some radius-`w` row (left permutivity), so `L_prefix` can grow like
`w`. The scanned prefixes stay well below `tcap`.

## Eventual witnesses

No scanned row is eventual in the cap: a genuine eventual regime would produce a period-3 suffix of length `tcap-O(w)`. Every maximizer’s run is a finite burst strictly inside the window (or a short suffix that is not a light-cone transient).

## What is proved, what is not

Proved (and machine-checked):

- Packed evolution agrees with `experiment.center_bits` on 256
  prize-seed bits and with an independent live-cell spacetime on
  sampled radius-`w` rows.
- The six-phase streaming scorer agrees with a stored-trace scorer.
- Synthetic `(001)^∞` / `(011)^∞` / `(010)^∞` score as claimed;
  period-2 and constant traces are not long exact period-3 runs.
- The exclusion table `L3(w)` for `w≤8` inside `tcap=8w+128`: [11, 11, 12, 12, 17, 18, 20, 20, 22]. No scanned row is eventual in that window (`n_genuine_eventual=0`).
- **No plateau.** Unlike period 2 (`L_run=24` for `6≤w≤10`), `L3(w)` is still strictly larger at `w=8` than at every smaller scanned radius (`L3(8)=22`). That kills this route as a Condrey-style finite theorem at these radii.

Not proved:

- A uniform-in-`w` bound on `L3(w)`. The table is only for radius `≤8`.
- Existence of an eventually period-3 finite row. Growth of
  `L3(w)` through radius 8 is compatible with either a slow
  unbounded family or a later plateau; it is not a witness.
- Eventual period 3 of the prize seed. The seed is the `w=0` line
  (`L3=11`, `L_prefix=5`).
- Anything about residual strip-graph SCCs for `001` / `011`.

## Verdict

`KILL`, wall time 9.4s.

- Kill: yes.
- Survive: no.
- Witness: none (no eventual-in-cap row).
- Reason: L3(w) keeps growing through w=8 with no plateau (table [11, 11, 12, 12, 17, 18, 20, 20, 22])
- Exclusion table: `L3(w)` as above, `tcap=8w+128`, `L3(w)≤22` for `w≤8`; the table does not plateau.

## Files

- `research/period3_fiber.md` (this note)
- `research/period3_fiber.py` (`--certify` runs the checks and the
  radius-`w` exhaustive)
- `research/period3_fiber.json` (dump)

