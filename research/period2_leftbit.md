# Period-2 `L_run`: left-bit-1 (prize-seed left edge)

This note extends Cycle I (`research/period2_fiber.md`). It does
**not** exclude eventual period 2 for every finite row, and it does
not claim a prize result. It is a finite census of radius-`w≤10`
rows whose leftmost 1 sits at spatial `-w`, not a uniform-in-`w`
bound.

Helper: `research/period2_leftbit.py --certify`. Dump:
`research/period2_leftbit.json`. Packed evolution is imported from
`research/period2_fiber.py` and that file is not modified.

## Attack

The prize seed is a single 1 at the origin. Its light-cone left edge
satisfies `x(t,-t)=1` for every `t`. Finite-row `L_run` scans allow
arbitrary supports: packed bit 0 may be 0, so the window has vacuum
to the left of the true support (a dying / padded left). Cycle I’s
`w=7` maximizer is exactly the `w=6` row `7503` shifted by one left
vacuum.

For any finite row whose leftmost 1 is at `L`, vacuum to the left,
Rule 30 sends that edge left at speed 1 and keeps it 1:

```
x(t+1, L-1-t) = 0 XOR (0 OR 1) = 1
```

so `x(t, L-t)=1` is automatic — not a new constraint. Packed Rule 30
has the same identity: `(new & 1) == (old & 1)`. The prize-specific
extra is that the leftmost 1 *starts at 0*, so a later slice at time
`T` is a radius-`T` row with leftmost 1 at `-T`.

**Scan:** every radius-`w` packed row with bit 0 (spatial `-w`) equal
to 1. That is `2^{2w}` states, exhaustive through `w=10`
(`2^{20}` at the top radius). Two caps: Cycle I `tcap=8w+128` and
the ideas11 long cap `tcap=32w+512`, from a single evolution.

**Kill:** `L_run` on this class still grows with `w`, or matches the
unrestricted Cycle I table (left-edge-on does not cut the burst).

**Finite theorem (this class only):** left-edge-on forces a strictly
smaller cap than unrestricted, with a plateau at the scan edge.

**Survive / uniform proof:** not claimed; the census is finite.

Packed Rule 30 is the Cycle I engine:

```
new = (row << 2) ^ ((row << 1) | row)
```

with the centre bit at time `t` equal to `(row >> (w+t)) & 1`. Bit 0
is the leftmost cell of the current support (spatial `-w` at `t=0`).

Secondary filters, scored in the same loop: origin in the live hull
(`rightmost ≥ 0`), origin live, and both packed edges live (true
support bounding box exactly `[-w,w]`).

## Self-checks

- Prize seed `w=0` mask `1`, `tcap=128`: `L_run=7`
  from `t=35` (factor `1010101`).
- `w=6` mask `7503`, row `1111001010111`, `tcap=176`: `L=24` from `t=94` to `t=118`. Bit 0 is `1` (in the left-bit class). Origin in hull, both edges live.
- Inlined two-cap loop agrees with `period2_fiber.scan_mask_runs`.
- Packed traces match the independent live-cell spacetime on the prize
  seed and on mask `7503`.
- Packed bit-0 identity: `(new & 1) == (old & 1)` on sampled rows.
- Left edge `x(t,-w-t)=1` holds on packed bit 0 and on the naive
  spacetime for sampled left-bit-1 rows.
- Cycle I `w=2` maximizer mask `2` has bit 0 = `0` (excluded; true leftmost `-1`).
- Cycle I `w=7` maximizer is `7503 << 1` (yes), bit 0 = `0`.
- Of 11 Cycle I maximizers (`w=0..10`), 5 already have bit 0 = 1 and 6 are left-padded / dying-left.
- `checks.all_ok=True`.

## Exhaustive left-bit-1 rows, `w≤10`

`2^{2w}` states per radius (bit 0 fixed), `4` processes on the large radii, scan wall 152.0s (total process 152.1s).

| `w` | states | Cycle I `L_run` | bit0 of CI max | `tcap=8w+128` | `L_left` | `L_hull` | `L_both` | `tcap=32w+512` | `L_long` | short best | long best |
|----:|-------:|----------------:|---------------:|--------------:|---------:|---------:|---------:|---------------:|---------:|-----------:|----------:|
| 0 | 1 | 7 | 1 | 128 | **7** | 7 | 7 | 512 | **7** | 1 | 1 |
| 1 | 4 | 8 | 1 | 136 | **8** | 8 | 8 | 544 | **10** | 1 | 1 |
| 2 | 16 | 10 | 0 | 144 | **10** | 10 | 10 | 576 | **11** | 7 | 9 |
| 3 | 64 | 13 | 0 | 152 | **12** | 12 | 12 | 608 | **19** | 31 | 33 |
| 4 | 256 | 15 | 1 | 160 | **15** | 15 | 15 | 640 | **19** | 261 | 231 |
| 5 | 1,024 | 15 | 0 | 168 | **15** | 15 | 15 | 672 | **19** | 1,819 | 627 |
| 6 | 4,096 | 24 | 1 | 176 | **24** | 24 | 24 | 704 | **24** | 7,503 | 7,503 |
| 7 | 16,384 | 24 | 0 | 184 | **24** | 24 | 24 | 736 | **24** | 19,171 | 19,171 |
| 8 | 65,536 | 24 | 1 | 192 | **24** | 24 | 24 | 768 | **24** | 8,647 | 8,647 |
| 9 | 262,144 | 24 | 0 | 200 | **24** | 24 | 24 | 800 | **25** | 58,579 | 131,589 |
| 10 | 1,048,576 | 24 | 0 | 208 | **24** | 24 | 24 | 832 | **27** | 58,233 | 75,565 |

Max `L` versus `w` (short / long / Cycle I): 0:7/7/7, 1:8/10/8, 2:10/11/10, 3:12/19/13, 4:15/19/15, 5:15/19/15, 6:24/24/24, 7:24/24/24, 8:24/24/24, 9:24/25/24, 10:24/27/24.

Short-cap match with Cycle I at `w=[0, 1, 2, 4, 5, 6, 7, 8, 9, 10]`. Strictly below at `w=[3]`. Long cap exceeds short cap at `w=[1, 2, 3, 4, 5, 9, 10]`.

### Cycle I maximizers versus the left-bit class

| `w` | CI mask | bit 0 | in class | CI `L_run` | `L_left` |
|----:|--------:|------:|---------:|-----------:|---------:|
| 0 | 1 | 1 | yes | 7 | 7 |
| 1 | 1 | 1 | yes | 8 | 8 |
| 2 | 2 | 0 | no | 10 | 10 |
| 3 | 122 | 0 | no | 13 | 12 |
| 4 | 261 | 1 | yes | 15 | 15 |
| 5 | 522 | 0 | no | 15 | 15 |
| 6 | 7,503 | 1 | yes | 24 | 24 |
| 7 | 15,006 | 0 | no | 24 | 24 |
| 8 | 8,647 | 1 | yes | 24 | 24 |
| 9 | 17,294 | 0 | no | 24 | 24 |
| 10 | 34,588 | 0 | no | 24 | 24 |

### Prefixes, hull, both edges

| `w` | `L_prefix` short | `L_prefix` long | `n` hull | `n` origin-live | `n` both-edges | `L_hull` long | `L_both` long |
|----:|-----------------:|----------------:|---------:|----------------:|---------------:|--------------:|--------------:|
| 0 | 1 | 1 | 1 | 1 | 1 | 7 | 7 |
| 1 | 7 | 7 | 3 | 2 | 2 | 10 | 10 |
| 2 | 6 | 6 | 14 | 8 | 8 | 11 | 11 |
| 3 | 6 | 6 | 60 | 32 | 32 | 19 | 19 |
| 4 | 5 | 5 | 248 | 128 | 128 | 19 | 19 |
| 5 | 9 | 9 | 1,008 | 512 | 512 | 19 | 19 |
| 6 | 10 | 10 | 4,064 | 2,048 | 2,048 | 24 | 24 |
| 7 | 10 | 10 | 16,320 | 8,192 | 8,192 | 24 | 24 |
| 8 | 15 | 15 | 65,408 | 32,768 | 32,768 | 24 | 24 |
| 9 | 16 | 16 | 261,888 | 131,072 | 131,072 | 25 | 25 |
| 10 | 15 | 15 | 1,048,064 | 524,288 | 524,288 | 27 | 27 |

No maximizer is eventual in either cap: the longest bursts are
interior. Each maximizer was re-evolved at `2·tcap`; none lengthened.
No scanned row has `L > 4w+16`.

### Long cap versus Cycle I

Cycle I’s `tcap=8w+128` plateaus at `L_run=24` for `6≤w≤10`. On
left-bit-1 rows the same plateau holds *inside that cap*. The long
cap `32w+512` finds later bursts that Cycle I never saw:

- `w=9`, mask `131589`, row `1010000001000000010`, live `[-9, -7, 0, 8]` (weight 4, origin live, hull contains 0, right edge off). Run of length `25` from `t=405` to `t=430` inside `tcap=800`. Cycle I’s cap is `200`, which ends before the burst starts. Doubled `L=25`.
- `w=10`, mask `75565`, row `101101001110010010000`, live `[-10, -8, -7, -5, -2, -1, 0, 3, 6]` (weight 9, origin live, hull contains 0, right edge off). Run of length `27` from `t=699` to `t=726` inside `tcap=832`. Cycle I’s cap is `208`. Doubled `L=27`.
  Both-edges (bounding box exactly `[-10,10]`) still reaches `L=27` on mask `1386285`, same run window.

So `L_run` on this class still grows with `w` once the cap is long
enough to see the burst: 24, 25, 27 at `w=8,9,10`. Hull-contains-0
and both-edges-live agree with the class max at every scanned radius.

`w=3` is the only short-cap radius strictly below Cycle I (`12` vs
`13`). That is a one-step dip, not a smaller plateau: `w=4` already
matches again at 15, and `w=6` matches the unrestricted 24.

### Witness that the class attains Cycle I

Radius 6, mask `7503`, row `1111001010111`, live `[-6, -5, -4, -3, 0, 2, 4, 5, 6]`. Weight 9, span 12, origin in hull yes, both edges yes. Period-2 run of length `24` from `t=94` to `t=118` inside `tcap=176`. Doubled cap `L=24`.

This is the Cycle I maximizer. Restricting to left-bit-1 rows does
not remove it, and neither does requiring the origin in the hull or
both light-cone edges live.

Least squares over the short-cap table: `L_left ≈ 2.04 w + 6.82`. Summary of the small-`w` ramp plus whatever plateau is present, not a growth conjecture.

## Verdict

**KILL.** left-edge-on (packed bit 0 = 1) attains the unrestricted Cycle I L_run at w=[1, 2, 4, 5, 6, 7, 8, 9, 10]. The w=6 maximizer mask 7503 already has leftmost 1 at -6, origin in the hull, and both packed edges live, with a period-2 centre run of length 24 inside tcap=8w+128; the long cap 32w+512 raises the class max to 27. Left-edge-on does not force a smaller cap than unrestricted. The runs are interior bursts, not an eventual regime. This does not exclude eventual period 2, and it is not a uniform-in-w theorem.

What this does not show:

- A uniform bound `L_run(w)≤C` on this class for all `w`.
- That the prize seed itself has a long period-2 centre run. The
  prize seed is one left-bit-1 row (`w=0`, `L_run=7`); later prize
  slices are one specific mask per radius, not the maximizer.
- Exclusion of eventual period 2. Every scanned burst is finite
  inside the cap.

## Files

- `research/period2_leftbit.py` — this scan
- `research/period2_leftbit.json` — dump
- `research/period2_fiber.py` — packed engine, not modified

