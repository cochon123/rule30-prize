# Period-6 and period-7 centres: finite-row analog of the radius-10 theorem

This note is a checked finite scan. It does **not** exclude eventual
period 6 or 7 for every finite row, and it does not claim a prize result.
It is ideas11 item 3: the period-4/5 exhaustive of
`research/period45_fiber.py`, repeated for exact periods 6 and 7.

Helper: `research/period67_fiber.py --certify`. Dump:
`research/period67_fiber.json`.

## Attack

Prove or kill: no nonzero finite-support configuration has an
eventually period-6 or period-7 central trace. Broader than the prize
seed. Not the strip-graph residual-SCC test (residual components
remain for every primitive period-6 and period-7 word; see
`period_scan_6.json` / `period_scan_7.json`), not onset SAT,
not `F_T` ideal certificates, and not the unique-left fiber
reconstruction of `period2_fiber.py`.

Kill: `L6(w)` or `L7(w)` is still strictly larger at the max scanned
`w` than at every smaller scanned radius (growing, no plateau), or a
finite row whose centre stays period-p through the cap and still does
not break when the cap is extended. Survive a finite theorem if `L_p`
plateaus at a constant on at least three scanned radii, like Cycle I’s
period-2 `L_run=24` for `6≤w≤10`. A two-radius edge plateau is not a
finite theorem (period 3 looked the same at `w=6..7` before `L3(8)=22`).

## Engine

Every nonzero initial word of support radius `w=0..6`
(`2^{2w+1}-1` states; `w=6` is `8191`) is evolved in a
quiescent background up to `tcap = 8w+128`. Packed Rule 30
`new = (row<<2) ^ ((row<<1)|row)`, bit 0 leftmost, centre bit
`(row>>(w+t))&1`, copied from `research/period45_fiber.py` and matching
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

## Period 6

The primitive necklaces of period 6 are `000001`, `000011`, `000101`, `000111`, `001011`, `001101`, `001111`, `010111`, `011111`. All
54 rotations, and therefore every starting phase, are scored
as global alignments

```
000001, 000010, 000100, 001000, 010000, 100000, 000011, 000110, 001100, 011000, 110000, 100001, 000101, 001010, 010100, 101000, 010001, 100010, 000111, 001110, 011100, 111000, 110001, 100011, 001011, 010110, 101100, 011001, 110010, 100101, 001101, 011010, 110100, 101001, 010011, 100110, 001111, 011110, 111100, 111001, 110011, 100111, 010111, 101110, 011101, 111010, 110101, 101011, 011111, 111110, 111101, 111011, 110111, 101111
```

A centre factor is exact period 6 when it is a contiguous run of one of those 54 infinite words.
The five non-primitive length-6 necklaces `000000`, `111111`,
`010101`, `001001`, and `011011` are excluded (periods 1, 2, 3).
A period-2 alternating factor matches a 5-bit window of `000101`
and then breaks, so it does not inflate `L6`.

| `w` | mode | scanned | states | `tcap` | `L6` | `L_prefix` | `L_suffix` | `L>4w+16` | maximizer | pattern | start |
|----:|------|--------:|-------:|-------:|-----:|-----------:|-----------:|----------:|-----------|---------|------:|
| 0 | exhaustive | 1 | 1 | 128 | 13 | 6 | 9 | 0 | `1` | `110001` | 96 |
| 1 | exhaustive | 7 | 7 | 136 | 13 | 8 | 10 | 0 | `010` | `110001` | 96 |
| 2 | exhaustive | 31 | 31 | 144 | 14 | 10 | 8 | 0 | `10000` | `000111` | 75 |
| 3 | exhaustive | 127 | 127 | 152 | 17 | 14 | 16 | 0 | `0101001` | `001010` | 99 |
| 4 | exhaustive | 511 | 511 | 160 | 20 | 14 | 15 | 0 | `111111110` | `111011` | 31 |
| 5 | exhaustive | 2047 | 2047 | 168 | 20 | 14 | 15 | 0 | `10000000000` | `110111` | 30 |
| 6 | exhaustive | 8191 | 8191 | 176 | 21 | 16 | 16 | 0 | `1000110000010` | `000110` | 42 |

Per-necklace maxima `L_neck(w)`:

| necklace | w=0 | w=1 | w=2 | w=3 | w=4 | w=5 | w=6 |
|----------|----:|----:|----:|----:|----:|----:|----:|
| `000001` | 9 | 9 | 9 | 12 | 18 | 18 | 18 |
| `000011` | 11 | 11 | 12 | 16 | 19 | 19 | 21 |
| `000101` | 8 | 9 | 10 | 17 | 18 | 18 | 19 |
| `000111` | 13 | 13 | 14 | 14 | 17 | 20 | 20 |
| `001011` | 10 | 10 | 11 | 12 | 16 | 16 | 19 |
| `001101` | 7 | 11 | 11 | 13 | 14 | 19 | 19 |
| `001111` | 8 | 10 | 12 | 13 | 16 | 16 | 18 |
| `010111` | 11 | 12 | 12 | 15 | 15 | 19 | 20 |
| `011111` | 7 | 10 | 13 | 15 | 20 | 20 | 20 |

The prize seed (`w=0`) has `L6=13`, the factor `1100011100011` of pattern `110001` starting at time 96.
`L_prefix(0)=6`.

Radius-1 maximizer: row `010` (mask=2), pattern `110001` (necklace `000111`), run of 13 from `t=96` to `t=109` (3 masks attain `L6`). Extending that evolution to 544 steps finds a later finite burst `ext_L=14` of pattern `110010` at `t=306..320` (the tcap-window maximizer is not eventual).
`L_prefix` maximizer at this radius: row `001` (mask=4), pattern `011001`, prefix `01100101` of length 8.

Radius-2 maximizer: row `10000` (mask=1), pattern `000111` (necklace `000111`), run of 14 from `t=75` to `t=89` (6 masks attain `L6`). Extending that evolution to 576 steps finds a later finite burst `ext_L=16` of pattern `110100` at `t=359..375` (the tcap-window maximizer is not eventual).
`L_prefix` maximizer at this radius: row `11111` (mask=31), pattern `100101`, prefix `1001011001` of length 10.

Radius-3 maximizer: row `0101001` (mask=74), pattern `001010` (necklace `000101`), run of 17 from `t=99` to `t=116` (1 mask attains `L6`). Extending that evolution to 608 steps does not lengthen the run (`ext_L=17`).
`L_prefix` maximizer at this radius: row `0010111` (mask=116), pattern `000101`, prefix `00010100010100` of length 14.

Radius-4 maximizer: row `111111110` (mask=255), pattern `111011` (necklace `011111`), run of 20 from `t=31` to `t=51` (2 masks attain `L6`). Extending that evolution to 640 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `000101110` (mask=232), pattern `000101`, prefix `00010100010100` of length 14.

Radius-5 maximizer: row `10000000000` (mask=1), pattern `110111` (necklace `011111`), run of 20 from `t=30` to `t=50` (21 masks attain `L6`). Extending that evolution to 672 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `00001011100` (mask=464), pattern `000101`, prefix `00010100010100` of length 14.

Radius-6 maximizer: row `1000110000010` (mask=2097), pattern `000110` (necklace `000011`), run of 21 from `t=42` to `t=63` (2 masks attain `L6`). Extending that evolution to 704 steps does not lengthen the run (`ext_L=21`).
`L_prefix` maximizer at this radius: row `1010001000111` (mask=7237), pattern `110100`, prefix `1101001101001101` of length 16.

### Plateau / growth

- `L6` table: `[13, 13, 14, 17, 20, 20, 21]`
- maximum `21` attained at `w=[6]`
- still growing at `w_max`: `True`
- strictly larger at `w_max` than every smaller `w`: `True`
- plateau at the global max: `False`
- real plateau (≥3 consecutive radii): `False`
- two-radius edge only: `False`
- final constant block: `L=21` on `w=6..6`

Least squares over the whole table (a summary only, not a conjecture):

- `L6 ≈ 1.571*w + 12.143`
- `L_prefix ≈ 1.643*w + 6.786`

### Eventual witnesses

No scanned row is eventual in the cap: a genuine eventual regime would produce a period-6 suffix of length `tcap-O(w)`. Every maximizer’s run is a finite burst strictly inside the window (or a short suffix that is not a light-cone transient).

### Verdict (L6)

`KILL`.

- Kill: yes.
- Reason: L6(w) is still strictly larger at w=6 than at every smaller scanned radius (table [13, 13, 14, 17, 20, 20, 21])

## Period 7

The primitive necklaces of period 7 are `0000001`, `0000011`, `0000101`, `0000111`, `0001001`, `0001011`, `0001101`, `0001111`, `0010011`, `0010101`, `0010111`, `0011011`, `0011101`, `0011111`, `0101011`, `0101111`, `0110111`, `0111111`. All
126 rotations, and therefore every starting phase, are scored
as global alignments

```
0000001, 0000010, 0000100, 0001000, 0010000, 0100000, 1000000, 0000011, 0000110, 0001100, 0011000, 0110000, 1100000, 1000001, 0000101, 0001010, 0010100, 0101000, 1010000, 0100001, 1000010, 0000111, 0001110, 0011100, 0111000, 1110000, 1100001, 1000011, 0001001, 0010010, 0100100, 1001000, 0010001, 0100010, 1000100, 0001011, 0010110, 0101100, 1011000, 0110001, 1100010, 1000101, 0001101, 0011010, 0110100, 1101000, 1010001, 0100011, 1000110, 0001111, 0011110, 0111100, 1111000, 1110001, 1100011, 1000111, 0010011, 0100110, 1001100, 0011001, 0110010, 1100100, 1001001, 0010101, 0101010, 1010100, 0101001, 1010010, 0100101, 1001010, 0010111, 0101110, 1011100, 0111001, 1110010, 1100101, 1001011, 0011011, 0110110, 1101100, 1011001, 0110011, 1100110, 1001101, 0011101, 0111010, 1110100, 1101001, 1010011, 0100111, 1001110, 0011111, 0111110, 1111100, 1111001, 1110011, 1100111, 1001111, 0101011, 1010110, 0101101, 1011010, 0110101, 1101010, 1010101, 0101111, 1011110, 0111101, 1111010, 1110101, 1101011, 1010111, 0110111, 1101110, 1011101, 0111011, 1110110, 1101101, 1011011, 0111111, 1111110, 1111101, 1111011, 1110111, 1101111, 1011111
```

A centre factor is exact period 7 when it is a contiguous run of one of those 126 infinite words.
Length 7 is prime, so the only excluded necklaces are the
constants `0000000` and `1111111` (20 binary necklaces minus
those two). A period-2 alternating factor matches a 7-bit window
of a primitive necklace (7 is odd) and then breaks, so it does
not inflate `L7`.

| `w` | mode | scanned | states | `tcap` | `L7` | `L_prefix` | `L_suffix` | `L>4w+16` | maximizer | pattern | start |
|----:|------|--------:|-------:|-------:|-----:|-----------:|-----------:|----------:|-----------|---------|------:|
| 0 | exhaustive | 1 | 1 | 128 | 14 | 7 | 10 | 0 | `1` | `1010101` | 50 |
| 1 | exhaustive | 7 | 7 | 136 | 14 | 11 | 9 | 0 | `100` | `0010011` | 51 |
| 2 | exhaustive | 31 | 31 | 144 | 18 | 11 | 12 | 0 | `11110` | `1101000` | 41 |
| 3 | exhaustive | 127 | 127 | 152 | 18 | 11 | 12 | 0 | `0111100` | `1101000` | 41 |
| 4 | exhaustive | 511 | 511 | 160 | 20 | 16 | 14 | 0 | `101100010` | `1011100` | 43 |
| 5 | exhaustive | 2047 | 2047 | 168 | 22 | 16 | 16 | 0 | `10000101110` | `0101011` | 27 |
| 6 | exhaustive | 8191 | 8191 | 176 | 23 | 16 | 21 | 0 | `1110011011100` | `0011001` | 61 |

Per-necklace maxima `L_neck(w)`:

| necklace | w=0 | w=1 | w=2 | w=3 | w=4 | w=5 | w=6 |
|----------|----:|----:|----:|----:|----:|----:|----:|
| `0000001` | 10 | 10 | 13 | 15 | 16 | 17 | 18 |
| `0000011` | 8 | 9 | 13 | 16 | 16 | 16 | 19 |
| `0000101` | 7 | 9 | 12 | 12 | 17 | 18 | 19 |
| `0000111` | 10 | 13 | 13 | 15 | 15 | 22 | 22 |
| `0001001` | 8 | 10 | 10 | 11 | 20 | 20 | 20 |
| `0001011` | 12 | 12 | 12 | 14 | 15 | 17 | 19 |
| `0001101` | 8 | 10 | 18 | 18 | 19 | 19 | 22 |
| `0001111` | 11 | 11 | 11 | 13 | 16 | 21 | 21 |
| `0010011` | 10 | 14 | 14 | 14 | 15 | 18 | 23 |
| `0010101` | 8 | 11 | 12 | 15 | 17 | 18 | 21 |
| `0010111` | 9 | 9 | 15 | 15 | 20 | 20 | 20 |
| `0011011` | 8 | 11 | 13 | 16 | 19 | 19 | 22 |
| `0011101` | 10 | 10 | 12 | 15 | 17 | 17 | 22 |
| `0011111` | 8 | 12 | 12 | 13 | 15 | 16 | 18 |
| `0101011` | 14 | 14 | 14 | 16 | 16 | 22 | 22 |
| `0101111` | 9 | 9 | 13 | 13 | 15 | 17 | 21 |
| `0110111` | 8 | 10 | 11 | 13 | 16 | 18 | 22 |
| `0111111` | 9 | 9 | 15 | 15 | 17 | 17 | 18 |

The prize seed (`w=0`) has `L7=14`, the factor `01010110101011` of pattern `1010101` starting at time 50.
`L_prefix(0)=7`.

Radius-1 maximizer: row `100` (mask=1), pattern `0010011` (necklace `0010011`), run of 14 from `t=51` to `t=65` (6 masks attain `L7`). Extending that evolution to 544 steps does not lengthen the run (`ext_L=14`).
`L_prefix` maximizer at this radius: row `100` (mask=1), pattern `0101010`, prefix `01010100101` of length 11.

Radius-2 maximizer: row `11110` (mask=15), pattern `1101000` (necklace `0001101`), run of 18 from `t=41` to `t=59` (2 masks attain `L7`). Extending that evolution to 576 steps does not lengthen the run (`ext_L=18`).
`L_prefix` maximizer at this radius: row `01000` (mask=2), pattern `0101010`, prefix `01010100101` of length 11.

Radius-3 maximizer: row `0111100` (mask=30), pattern `1101000` (necklace `0001101`), run of 18 from `t=41` to `t=59` (5 masks attain `L7`). Extending that evolution to 608 steps does not lengthen the run (`ext_L=18`).
`L_prefix` maximizer at this radius: row `0010000` (mask=4), pattern `0101010`, prefix `01010100101` of length 11.

Radius-4 maximizer: row `101100010` (mask=141), pattern `1011100` (necklace `0010111`), run of 20 from `t=43` to `t=63` (4 masks attain `L7`). Extending that evolution to 640 steps does not lengthen the run (`ext_L=20`).
`L_prefix` maximizer at this radius: row `100101111` (mask=489), pattern `0001101`, prefix `0001101000110100` of length 16.

Radius-5 maximizer: row `10000101110` (mask=929), pattern `0101011` (necklace `0101011`), run of 22 from `t=27` to `t=49` (3 masks attain `L7`). Extending that evolution to 672 steps does not lengthen the run (`ext_L=22`).
`L_prefix` maximizer at this radius: row `01001011110` (mask=978), pattern `0001101`, prefix `0001101000110100` of length 16.

Radius-6 maximizer: row `1110011011100` (mask=1895), pattern `0011001` (necklace `0010011`), run of 23 from `t=61` to `t=84` (3 masks attain `L7`). Extending that evolution to 704 steps does not lengthen the run (`ext_L=23`).
`L_prefix` maximizer at this radius: row `0010010111100` (mask=1956), pattern `0001101`, prefix `0001101000110100` of length 16.

### Plateau / growth

- `L7` table: `[14, 14, 18, 18, 20, 22, 23]`
- maximum `23` attained at `w=[6]`
- still growing at `w_max`: `True`
- strictly larger at `w_max` than every smaller `w`: `True`
- plateau at the global max: `False`
- real plateau (≥3 consecutive radii): `False`
- two-radius edge only: `False`
- final constant block: `L=23` on `w=6..6`

Least squares over the whole table (a summary only, not a conjecture):

- `L7 ≈ 1.607*w + 13.607`
- `L_prefix ≈ 1.500*w + 8.071`

### Eventual witnesses

No scanned row is eventual in the cap: a genuine eventual regime would produce a period-7 suffix of length `tcap-O(w)`. Every maximizer’s run is a finite burst strictly inside the window (or a short suffix that is not a light-cone transient).

### Verdict (L7)

`KILL`.

- Kill: yes.
- Reason: L7(w) is still strictly larger at w=6 than at every smaller scanned radius (table [14, 14, 18, 18, 20, 22, 23])

## What is proved, what is not

Proved (and machine-checked):

- Packed evolution agrees with `experiment.center_bits` on 256
  prize-seed bits and with an independent live-cell spacetime on
  sampled radius-`w` rows.
- The streaming scorer agrees with a stored-trace scorer for both
  catalogs, including the combined one-evolution path.
- Synthetic primitive words score as claimed; period-2, period-3,
  period-4, period-5, and constant traces are not long exact
  period-6 or period-7 runs.
- `010101` / `001001` / `011011` are not period-6 necklaces;
  `0000000` / `1111111` are not period-7 necklaces.
- The exclusion tables inside `tcap=8w+128` for `w≤6`: `L6=[13, 13, 14, 17, 20, 20, 21]`, `L7=[14, 14, 18, 18, 20, 22, 23]`.
- **No plateau (L6).** Unlike period 2 (`L_run=24` for `6≤w≤10`), `L6(w)` is still strictly larger at `w=6` than at every smaller scanned radius (`L6(6)=21`). That kills this route as a Condrey-style finite theorem at these radii.
- **No plateau (L7).** Unlike period 2 (`L_run=24` for `6≤w≤10`), `L7(w)` is still strictly larger at `w=6` than at every smaller scanned radius (`L7(6)=23`). That kills this route as a Condrey-style finite theorem at these radii.

Not proved:

- A uniform-in-`w` bound on `L6(w)` or `L7(w)`. The tables are only
  for radius `≤6`.
- Existence of an eventually period-6 or period-7 finite row. Growth
  of `L_p(w)` is compatible with either a slow unbounded family or a
  later plateau; it is not a witness.
- Eventual period 6 or 7 of the prize seed. The seed is the `w=0`
  line (`L6=13`, `L7=14`).
- Anything about residual strip-graph SCCs for these necklaces.

## Verdict

`KILL`, wall time 7.8s.

- Kill: yes.
- Survive: no.
- Witness: none (no eventual-in-cap row) unless listed above.
- Reason: L6: L6(w) is still strictly larger at w=6 than at every smaller scanned radius (table [13, 13, 14, 17, 20, 20, 21]); L7: L7(w) is still strictly larger at w=6 than at every smaller scanned radius (table [14, 14, 18, 18, 20, 22, 23])
- Exclusion tables: `L6(w)` and `L7(w)` as above, `tcap=8w+128`, radius `≤6`.

## Files

- `research/period67_fiber.md` (this note)
- `research/period67_fiber.py` (`--certify` runs the checks and the
  radius-`w` exhaustive)
- `research/period67_fiber.json` (dump)

