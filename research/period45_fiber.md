# Period-4 and period-5 centres: finite-row analog of the radius-10 theorem

This note is a checked finite scan. It does **not** exclude eventual
period 4 or 5 for every finite row, and it does not claim a prize result.
It is ideas10 item 3: the period-3 exhaustive of
`research/period3_fiber.py`, repeated for exact periods 4 and 5.

Helper: `research/period45_fiber.py --certify`. Dump:
`research/period45_fiber.json`.

## Attack

Prove or kill: no nonzero finite-support configuration has an
eventually period-4 or period-5 central trace. Broader than the prize
seed. Not the strip-graph residual-SCC test (residual components
remain for every primitive period-4 and period-5 word), not onset SAT,
not `F_T` ideal certificates, and not the unique-left fiber
reconstruction of `period2_fiber.py`.

Kill: `L4(w)` or `L5(w)` is still strictly larger at `w=7` than at
every smaller scanned radius (growing, no plateau), or a finite row
whose centre stays period-p through the cap and still does not break
when the cap is extended. Survive a finite theorem if `L_p` plateaus
at a constant on the scanned radii, like Cycle I’s period-2
`L_run=24` for `6≤w≤10`.

## Engine

Every nonzero initial word of support radius `w=0..7`
(`2^{2w+1}-1` states; `w=7` is `2^{15}-1`) is evolved in a
quiescent background up to `tcap = 8w+128`. Packed Rule 30
`new = (row<<2) ^ ((row<<1)|row)`, bit 0 leftmost, centre bit
`(row>>(w+t))&1`, copied from `research/period3_fiber.py` and matching
`experiment.center_bits` on the prize seed prefix of length 256
(`1101110011000101…`) and an independent live-cell
implementation on sampled small rows. The streaming scorer matches a
stored-trace scorer on those rows. One packed evolution scores both
periods.

`L_run(w) = L_p(w)` is the longest such run anywhere in `[0, tcap)`.
`L_prefix(w)` is the longest exact period-p prefix from time 0.
Per-necklace maxima are recorded. No row is “eventual in the cap”
(last break inside the light cone `2w+8`, suffix at least 16) unless
listed below.

## Period 4

The primitive necklaces of period 4 are `0001`, `0011`, `0111`. All
12 rotations, and therefore every starting phase, are scored
as global alignments

```
0001, 0010, 0100, 1000, 0011, 0110, 1100, 1001, 0111, 1110, 1101, 1011
```

A centre factor is exact period 4 when it is a contiguous run of one of those 12 infinite words.
The period-2 necklace `0101` and the constants `0000` / `1111`
are excluded. A period-2 alternating factor matches a 3-bit
window of `0100` and then breaks, so it does not inflate `L4`.

| `w` | states | `tcap` | `L4` | `L_prefix` | `L_suffix` | `L_0001` | `L_0011` | `L_0111` | `L>4w+16` | maximizer | pattern | start |
|----:|-------:|-------:|-----:|-----------:|-----------:|--------:|--------:|--------:|----------:|-----------|---------|------:|
| 0 | 1 | 128 | 8 | 7 | 7 | 7 | 8 | 7 | 0 | `1` | `1100` | 4 |
| 1 | 7 | 136 | 9 | 7 | 7 | 8 | 9 | 8 | 0 | `100` | `0011` | 50 |
| 2 | 31 | 144 | 12 | 7 | 10 | 11 | 11 | 12 | 0 | `01111` | `1101` | 108 |
| 3 | 127 | 152 | 15 | 8 | 9 | 15 | 12 | 12 | 0 | `0010010` | `0001` | 134 |
| 4 | 511 | 160 | 20 | 11 | 10 | 16 | 13 | 20 | 0 | `101111110` | `0111` | 102 |
| 5 | 2047 | 168 | 20 | 13 | 13 | 17 | 15 | 20 | 0 | `01011111100` | `0111` | 102 |
| 6 | 8191 | 176 | 22 | 14 | 16 | 17 | 22 | 20 | 0 | `1001100110010` | `1001` | 123 |
| 7 | 32767 | 184 | 22 | 14 | 22 | 22 | 22 | 21 | 0 | `010011001100100` | `1001` | 123 |

The prize seed (`w=0`) has `L4=8`, the factor `11001100` of pattern `1100` starting at time 4.
`L_prefix(0)=7`.

Radius-1 maximizer: row `100` (mask=1), pattern `0011` (necklace `0011`), run of 9 from `t=50` to `t=59` (3 masks attain `L4`). Extending that evolution to 544 steps does not lengthen the run (`ext_L=9`).
`L_prefix` maximizer at this radius: row `010` (mask=2), pattern `1101`, prefix `1101110` of length 7.

Radius-2 maximizer: row `01111` (mask=30), pattern `1101` (necklace `0111`), run of 12 from `t=108` to `t=120` (1 mask attains `L4`). Extending that evolution to 576 steps finds a later finite burst `ext_L=18` of pattern `1100` at `t=394..412` (the tcap-window maximizer is not eventual).
`L_prefix` maximizer at this radius: row `00100` (mask=4), pattern `1101`, prefix `1101110` of length 7.

Radius-3 maximizer: row `0010010` (mask=36), pattern `0001` (necklace `0001`), run of 15 from `t=134` to `t=149` (3 masks attain `L4`). Extending that evolution to 608 steps does not lengthen the run (`ext_L=15`).
`L_prefix` maximizer at this radius: row `0001001` (mask=72), pattern `1101`, prefix `11011101` of length 8.

Radius-4 maximizer: row `101111110` (mask=253), pattern `0111` (necklace `0111`), run of 20 from `t=102` to `t=122` (2 masks attain `L4`). Extending that evolution to 640 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `100000010` (mask=129), pattern `0001`, prefix `00010001000` of length 11.

Radius-5 maximizer: row `01011111100` (mask=506), pattern `0111` (necklace `0111`), run of 20 from `t=102` to `t=122` (5 masks attain `L4`). Extending that evolution to 672 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `11110000010` (mask=527), pattern `0010`, prefix `0010001000100` of length 13.

Radius-6 maximizer: row `1001100110010` (mask=2457), pattern `1001` (necklace `0011`), run of 22 from `t=123` to `t=145` (2 masks attain `L4`). Extending that evolution to 704 steps does not lengthen the run (`ext_L=22`).
`L_prefix` maximizer at this radius: row `1010100111111` (mask=8085), pattern `0100`, prefix `01000100010001` of length 14.

Radius-7 maximizer: row `010011001100100` (mask=4914), pattern `1001` (necklace `0011`), run of 22 from `t=123` to `t=145` (6 masks attain `L4`). Extending that evolution to 736 steps does not lengthen the run (`ext_L=22`).
`L_prefix` maximizer at this radius: row `100000010000000` (mask=129), pattern `1101`, prefix `11011101110111` of length 14.

### Plateau / growth

- `L4` table: `[8, 9, 12, 15, 20, 20, 22, 22]`
- maximum `22` attained at `w=[6, 7]`
- still growing at `w_max`: `False`
- strictly larger at `w_max` than every smaller `w`: `False`
- plateau at the global max: `True`
- final constant block: `L=22` on `w=6..7`
- caveat: this is only two radii at the scan edge, not Cycle I’s five-radius period-2 plateau (`L_run=24` on `6≤w≤10`). Period 3 looked the same at `w=6..7` (`L3=20`) before `L3(8)=22`.

Least squares over the whole table (a summary only, not a conjecture):

- `L4 ≈ 2.286*w + 8.000`
- `L_prefix ≈ 1.250*w + 5.750`

### Eventual witnesses

No scanned row is eventual in the cap: a genuine eventual regime would produce a period-4 suffix of length `tcap-O(w)`. Every maximizer’s run is a finite burst strictly inside the window (or a short suffix that is not a light-cone transient).

Some rows have a period-p burst that happens to end at `tcap` (window-edge, not light-cone eventual). Extending those evolutions does not produce an eventual regime:
- w=7 mask=30388 L_at_tcap=22 suffix=22 last_break=162; extended to 736: L_ext=22, suffix_ext=4, reaches_ext=False

### Verdict (L4)

`FINITE_THEOREM`.

- Kill: no.
- Reason: no genuine eventual witness; L4(w) plateaus at 22 on w=6..7 of the scanned radii; every radius-w row breaks every exact period-4 centre run by time 8w+128, and no period-4 run exceeds L4(w)

## Period 5

The primitive necklaces of period 5 are `00001`, `00011`, `00101`, `00111`, `01011`, `01111`. All
30 rotations, and therefore every starting phase, are scored
as global alignments

```
00001, 00010, 00100, 01000, 10000, 00011, 00110, 01100, 11000, 10001, 00101, 01010, 10100, 01001, 10010, 00111, 01110, 11100, 11001, 10011, 01011, 10110, 01101, 11010, 10101, 01111, 11110, 11101, 11011, 10111
```

A centre factor is exact period 5 when it is a contiguous run of one of those 30 infinite words.
Constants `00000` and `11111` are excluded (they have period 1);
those two extra length-5 necklaces are why some notes say “8
necklaces”. A period-2 alternating factor matches a 5-bit window
of `01010` or `10101` and then breaks, so it does not inflate `L5`.

| `w` | states | `tcap` | `L5` | `L_prefix` | `L_suffix` | `L_00001` | `L_00011` | `L_00101` | `L_00111` | `L_01011` | `L_01111` | `L>4w+16` | maximizer | pattern | start |
|----:|-------:|-------:|-----:|-----------:|-----------:|--------:|--------:|--------:|--------:|--------:|--------:|----------:|-----------|---------|------:|
| 0 | 1 | 128 | 10 | 6 | 8 | 8 | 8 | 7 | 10 | 10 | 6 | 0 | `1` | `10011` | 27 |
| 1 | 7 | 136 | 11 | 11 | 8 | 9 | 10 | 11 | 10 | 10 | 9 | 0 | `110` | `10010` | 0 |
| 2 | 31 | 144 | 16 | 11 | 9 | 9 | 16 | 11 | 11 | 11 | 12 | 0 | `10010` | `01100` | 62 |
| 3 | 127 | 152 | 17 | 11 | 12 | 14 | 16 | 14 | 14 | 17 | 12 | 0 | `1000100` | `11010` | 128 |
| 4 | 511 | 160 | 18 | 11 | 15 | 14 | 16 | 17 | 18 | 17 | 15 | 0 | `100010000` | `10011` | 84 |
| 5 | 2047 | 168 | 20 | 13 | 16 | 17 | 17 | 20 | 20 | 17 | 17 | 0 | `10101011110` | `10010` | 76 |
| 6 | 8191 | 176 | 20 | 13 | 15 | 19 | 19 | 20 | 20 | 17 | 20 | 0 | `0101010111100` | `10010` | 76 |
| 7 | 32767 | 184 | 22 | 14 | 18 | 22 | 21 | 20 | 20 | 20 | 20 | 0 | `101000111100100` | `01000` | 119 |

The prize seed (`w=0`) has `L5=10`, the factor `0111001110` of pattern `10011` starting at time 27.
`L_prefix(0)=6`.

Radius-1 maximizer: row `110` (mask=3), pattern `10010` (necklace `00101`), run of 11 from `t=0` to `t=11` (1 mask attains `L5`). Extending that evolution to 544 steps finds a later finite burst `ext_L=19` of pattern `10101` at `t=266..285` (the tcap-window maximizer is not eventual).
`L_prefix` maximizer at this radius: row `110` (mask=3), pattern `10010`, prefix `10010100101` of length 11.

Radius-2 maximizer: row `10010` (mask=9), pattern `01100` (necklace `00011`), run of 16 from `t=62` to `t=78` (2 masks attain `L5`). Extending that evolution to 576 steps does not lengthen the run (`ext_L=16`).
`L_prefix` maximizer at this radius: row `01100` (mask=6), pattern `10010`, prefix `10010100101` of length 11.

Radius-3 maximizer: row `1000100` (mask=17), pattern `11010` (necklace `01011`), run of 17 from `t=128` to `t=145` (3 masks attain `L5`). Extending that evolution to 608 steps finds a later finite burst `ext_L=20` of pattern `10000` at `t=221..241` (the tcap-window maximizer is not eventual).
`L_prefix` maximizer at this radius: row `0011000` (mask=12), pattern `10010`, prefix `10010100101` of length 11.

Radius-4 maximizer: row `100010000` (mask=17), pattern `10011` (necklace `00111`), run of 18 from `t=84` to `t=102` (5 masks attain `L5`). Extending that evolution to 640 steps does not lengthen the run (`ext_L=18`).
`L_prefix` maximizer at this radius: row `000110000` (mask=24), pattern `10010`, prefix `10010100101` of length 11.

Radius-5 maximizer: row `10101011110` (mask=981), pattern `10010` (necklace `00101`), run of 20 from `t=76` to `t=96` (4 masks attain `L5`). Extending that evolution to 672 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `10110000000` (mask=13), pattern `00100`, prefix `0010000100001` of length 13.

Radius-6 maximizer: row `0101010111100` (mask=1962), pattern `10010` (necklace `00101`), run of 20 from `t=76` to `t=96` (13 masks attain `L5`). Extending that evolution to 704 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `0101100000000` (mask=26), pattern `00100`, prefix `0010000100001` of length 13.

Radius-7 maximizer: row `101000111100100` (mask=5061), pattern `01000` (necklace `00001`), run of 22 from `t=119` to `t=141` (5 masks attain `L5`). Extending that evolution to 736 steps does not lengthen the run (`ext_L=22`).
`L_prefix` maximizer at this radius: row `100101111100000` (mask=1001), pattern `10011`, prefix `10011100111001` of length 14.

### Plateau / growth

- `L5` table: `[10, 11, 16, 17, 18, 20, 20, 22]`
- maximum `22` attained at `w=[7]`
- still growing at `w_max`: `True`
- strictly larger at `w_max` than every smaller `w`: `True`
- plateau at the global max: `False`
- final constant block: `L=22` on `w=7..7`

Least squares over the whole table (a summary only, not a conjecture):

- `L5 ≈ 1.690*w + 10.833`
- `L_prefix ≈ 0.857*w + 8.250`

### Eventual witnesses

No scanned row is eventual in the cap: a genuine eventual regime would produce a period-5 suffix of length `tcap-O(w)`. Every maximizer’s run is a finite burst strictly inside the window (or a short suffix that is not a light-cone transient).

Some rows have a period-p burst that happens to end at `tcap` (window-edge, not light-cone eventual). Extending those evolutions does not produce an eventual regime:
- w=7 mask=242 L_at_tcap=18 suffix=18 last_break=166; extended to 736: L_ext=18, suffix_ext=6, reaches_ext=False
- w=7 mask=370 L_at_tcap=18 suffix=18 last_break=166; extended to 736: L_ext=18, suffix_ext=6, reaches_ext=False
- w=7 mask=882 L_at_tcap=18 suffix=18 last_break=166; extended to 736: L_ext=18, suffix_ext=6, reaches_ext=False
- w=7 mask=1394 L_at_tcap=18 suffix=18 last_break=166; extended to 736: L_ext=18, suffix_ext=6, reaches_ext=False

### Verdict (L5)

`KILL`.

- Kill: yes.
- Reason: L5(w) is still strictly larger at w=7 than at every smaller scanned radius (table [10, 11, 16, 17, 18, 20, 20, 22])

## What is proved, what is not

Proved (and machine-checked):

- Packed evolution agrees with `experiment.center_bits` on 256
  prize-seed bits and with an independent live-cell spacetime on
  sampled radius-`w` rows.
- The streaming scorer agrees with a stored-trace scorer for both
  catalogs, including the combined one-evolution path.
- Synthetic primitive words score as claimed; period-2, period-3,
  and constant traces are not long exact period-4 or period-5 runs.
- `0101` is not a period-4 necklace; `00000` / `11111` are not
  period-5 necklaces.
- The exclusion tables inside `tcap=8w+128` for `w≤7`: `L4=[8, 9, 12, 15, 20, 20, 22, 22]`, `L5=[10, 11, 16, 17, 18, 20, 20, 22]`.
- **Finite theorem (L4).** Every nonzero row of support radius `w≤7` has every exact period-4 centre run of length at most `L4(w)`, hence at most 22, inside `tcap=8w+128`. The constant block is only two radii at the scan edge, weaker than Cycle I’s period-2 plateau on `6≤w≤10`; it is a checked bound `L4(w)≤22` for `w≤7`, not a uniform-in-`w` theorem.
- **No plateau (L5).** Unlike period 2 (`L_run=24` for `6≤w≤10`), `L5(w)` is still strictly larger at `w=7` than at every smaller scanned radius (`L5(7)=22`). That kills this route as a Condrey-style finite theorem at these radii.

Not proved:

- A uniform-in-`w` bound on `L4(w)` or `L5(w)`. The tables are only
  for radius `≤7`.
- Existence of an eventually period-4 or period-5 finite row. Growth
  of `L_p(w)` is compatible with either a slow unbounded family or a
  later plateau; it is not a witness.
- Eventual period 4 or 5 of the prize seed. The seed is the `w=0`
  line (`L4=8`, `L5=10`).
- Anything about residual strip-graph SCCs for these necklaces.

## Verdict

`KILL`, wall time 31.2s.

- Kill: yes.
- Survive: no.
- Witness: none (no eventual-in-cap row) unless listed above.
- Reason: L5: L5(w) is still strictly larger at w=7 than at every smaller scanned radius (table [10, 11, 16, 17, 18, 20, 20, 22]) (L4: no genuine eventual witness; L4(w) plateaus at 22 on w=6..7 of the scanned radii; every radius-w row breaks every exact period-4 centre run by time 8w+128, and no period-4 run exceeds L4(w))
- Exclusion tables: `L4(w)` and `L5(w)` as above, `tcap=8w+128`, radius `≤7`.

## Files

- `research/period45_fiber.md` (this note)
- `research/period45_fiber.py` (`--certify` runs the checks and the
  radius-`w` exhaustive)
- `research/period45_fiber.json` (dump)

