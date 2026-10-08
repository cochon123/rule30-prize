# Period-2 `L_run`: origin-in-hull weight-8 span-24 census

This note extends Cycle L (`research/period2_weight8.md`). It does
**not** exclude eventual period 2 for every finite row, and it does
not claim a prize result. It is a finite census of Hamming weight
`≤8` and span `≤24` with the origin in the live convex hull, not a
uniform-in-`w` bound.

Helper: `research/period2_hull.py --certify`. Dump:
`research/period2_hull.json`. Packed evolution is imported from
`research/period2_fiber.py` and that file is not modified.
`research/period2_weight8.py` is not modified.

## Attack

Cycle L’s weight-8 span-24 census at `tcap=32w+512` reached `L=35`
on mask `17057305` (true radius 38), but every `L≥32` placement had
the origin **outside** the live convex hull: all 1s strictly left of
cell 0, or all strictly right. The prize seed has a 1 at the origin,
so those off-hull bursts are not prize-shaped. ideas12 item 1 asks
for the same census restricted to placements with

```
min(live) <= 0 <= max(live)
```

Each combinatorial support still sits on `[0,s]` with live endpoints.
In-hull is then `C ∈ [0,s]` (`s+1` centres), not Cycle L’s window
`C ∈ [-s, 2s]` (`3s+1` centres). Cap `tcap=32w+512` of the true
radius of that placement. Any `L≥30` row is re-evolved at `2·tcap`.

**Kill:** an in-hull weight-`≤8` span-`≤24` row with a period-2
centre run of length `≥32` after doubling `tcap`.

**Finite theorem (this class only):** every in-hull weight-`≤8`
span-`≤24` row has `L≤31`.

**Survive / uniform proof:** not claimed; the census is finite.

Packed Rule 30 is the Cycle I engine:

```
new = (row << 2) ^ ((row << 1) | row)
```

with the centre bit at time `t` equal to `(row >> (w+t)) & 1`. Bit 0
is the leftmost cell of the current support (spatial `-w` at `t=0`).

## Self-checks

- `w=11` mask `4369552`, `tcap=8·11+128=216`: `L=29` from
  `t=159` to `t=188`. Live cells
  `-7, -4, -1, 0, 2, 4, 6, 11`. Weight 8, span 18,
  origin in hull (`min=-7`, `max=11`).
- `w=17` mask `281769`, `tcap=8·17+256=392`:
  `L=31` from `t=320` to `t=351`.
  Live `-17, -14, -12, -10, -7, -6, -3, 1`. In-hull
  (`min=-17 ≤ 0 ≤ 1`). Census cap
  `32·17+512=1056` still has `L=31`.
- `w=38` mask `17057305`: live
  `-38, -35, -34, -29, -28, -24, -20, -14`. All live `< 0`,
  origin off-hull, `C=38` not in `[0, 24]`.
  Packed engine still gives `L=35` at `tcap=32·38+512`;
  the hull census excludes this row.
- Inlined inner loop agrees with `period2_fiber.scan_mask_runs`.
- Packed traces match the independent live-cell spacetime on the prize
  seed, on mask `4369552`, and on mask `281769`.
- Multi-centre extraction of a canonical support agrees with the packed
  engine on both in-hull maximizers. Hull scan `nC=s+1` does not
  contain the off-hull centre of mask `17057305`.
- Random in-hull centres (`C in [0,s]`) satisfy `min≤0≤max` and match
  the packed engine; random `C` outside `[0,s]` are off-hull.
- `checks.all_ok=True`.

## Census

`536,155` combinatorial supports, `12,132,250` in-hull placements (`C in [0,s]`), `tcap=32w+512`, `4` processes, 401.8s.

Span here is `maxlive-minlive`. Cycle L’s off-hull window used
`3s+1` translations; this census uses `s+1`.

| `wt` | types | placements | `L_run` | `n≥30` | `n≥31` | `n≥32` | best | `w` | span |
|-----:|------:|-----------:|--------:|-------:|-------:|-------:|-----:|----:|-----:|
| 1 | 1 | 1 | **7** | 0 | 0 | 0 | 1 | 0 | 0 |
| 2 | 24 | 324 | **19** | 0 | 0 | 0 | 33 | 3 | 5 |
| 3 | 276 | 4,876 | **23** | 0 | 0 | 0 | 65,672 | 8 | 13 |
| 4 | 2,024 | 39,974 | **25** | 0 | 0 | 0 | 131,589 | 9 | 17 |
| 5 | 10,626 | 223,146 | **31** | 1 | 1 | 0 | 2,294,017 | 17 | 21 |
| 6 | 42,504 | 928,004 | **31** | 2 | 2 | 0 | 6,488,321 | 17 | 22 |
| 7 | 134,596 | 3,018,796 | **31** | 2 | 2 | 0 | 27,459,841 | 17 | 24 |
| 8 | 346,104 | 7,917,129 | **31** | 4 | 3 | 0 | 281,769 | 17 | 18 |

| span | types | placements | `L_run` | `n≥30` | `n≥31` | `n≥32` | best | `w` |
|-----:|------:|-----------:|--------:|-------:|-------:|-------:|-----:|----:|
| 0 | 1 | 1 | **7** | 0 | 0 | 0 | 1 | 0 |
| 1 | 1 | 2 | **10** | 0 | 0 | 0 | 3 | 1 |
| 2 | 2 | 6 | **10** | 0 | 0 | 0 | 5 | 1 |
| 3 | 4 | 16 | **11** | 0 | 0 | 0 | 9 | 2 |
| 4 | 8 | 40 | **13** | 0 | 0 | 0 | 23 | 4 |
| 5 | 16 | 96 | **19** | 0 | 0 | 0 | 33 | 3 |
| 6 | 32 | 224 | **19** | 0 | 0 | 0 | 97 | 3 |
| 7 | 64 | 512 | **19** | 0 | 0 | 0 | 231 | 4 |
| 8 | 127 | 1,143 | **21** | 0 | 0 | 0 | 277 | 7 |
| 9 | 247 | 2,470 | **21** | 0 | 0 | 0 | 1,058 | 5 |
| 10 | 466 | 5,126 | **21** | 0 | 0 | 0 | 6,212 | 6 |
| 11 | 848 | 10,176 | **23** | 0 | 0 | 0 | 18,216 | 7 |
| 12 | 1,486 | 19,318 | **23** | 0 | 0 | 0 | 101,968 | 8 |
| 13 | 2,510 | 35,140 | **24** | 0 | 0 | 0 | 8,647 | 8 |
| 14 | 4,096 | 61,440 | **24** | 0 | 0 | 0 | 19,171 | 7 |
| 15 | 6,476 | 103,616 | **26** | 0 | 0 | 0 | 78,878 | 8 |
| 16 | 9,949 | 169,133 | **28** | 0 | 0 | 0 | 1,129,552 | 10 |
| 17 | 14,893 | 268,074 | **26** | 0 | 0 | 0 | 250,145 | 13 |
| 18 | 21,778 | 413,782 | **31** | 1 | 1 | 0 | 281,769 | 17 |
| 19 | 31,180 | 623,600 | **28** | 0 | 0 | 0 | 302,030,336 | 14 |
| 20 | 43,796 | 919,716 | **29** | 0 | 0 | 0 | 1,868,069 | 12 |
| 21 | 60,460 | 1,330,120 | **31** | 1 | 1 | 0 | 2,294,017 | 17 |
| 22 | 82,160 | 1,889,680 | **31** | 2 | 2 | 0 | 6,488,321 | 17 |
| 23 | 110,056 | 2,641,344 | **31** | 2 | 2 | 0 | 10,682,625 | 17 |
| 24 | 145,499 | 3,637,475 | **31** | 3 | 2 | 0 | 27,459,841 | 17 |

Max `L` versus span: 0:7, 1:10, 2:10, 3:11, 4:13, 5:19, 6:19, 7:19, 8:21, 9:21, 10:21, 11:23, 12:23, 13:24, 14:24, 15:26, 16:28, 17:26, 18:31, 19:28, 20:29, 21:31, 22:31, 23:31, 24:31.

Off-hull placements scored: `0` (must be 0; every scanned centre is `C in [0,s]`).

## Witness

Least true-radius maximizer of the in-hull census:

- true radius `17`, mask `281769`
- packed row (bit 0 = spatial `-17`): `10010101001100100010000000000000000`
- live at `-17, -14, -12, -10, -7, -6, -3, 1` (8 ones, span 18)
- origin in the live hull: `True` (min=-17, max=1)
- run of 31 from `t=320` to `t=351` (exclusive end)
- run bits `0101010101010101010101010101010`
- bits immediately before and after: `0`, `0`
- `tcap=1056` and doubled `tcap=2112` both give `(L,start,end)=(31,320,351)`
- packed, fast loop, and naive spacetime agree (`witness_check.ok=True`)

Cycle J cap `8w+128=264` reports `L=6` (truncated).
Cycle K cap `8w+256=392` reports `L=31`. Census `32w+512=1056` reports `L=31`; doubled `2112` reports `L=31`.

Known rows, scored inside this in-hull class:

- mask `4369552`: w=11 L=29 (expected ≥29), span 18, in-hull=True, ok=True
- mask `281769`: w=17 L=31 (expected ≥31), span 18, in-hull=True, ok=True
- mask `17057305`: in-hull=False, `C=38` not in `[0,s]`, excluded, ok=True

`L≥31` in-hull rows (unique `(w,mask)`): 8. None reach `L≥32`.

| `L` | `w` | mask | span | live min..max | start | end | doubled L |
|----:|----:|-----:|-----:|--------------:|------:|----:|----------:|
| 31 | 17 | 281769 | 18 | -17..1 | 320 | 351 | 31 |
| 31 | 17 | 2294017 | 21 | -17..4 | 110 | 141 | 31 |
| 31 | 17 | 6488321 | 22 | -17..5 | 110 | 141 | 31 |
| 31 | 17 | 10682625 | 23 | -17..6 | 110 | 141 | 31 |
| 31 | 17 | 27459841 | 24 | -17..7 | 110 | 141 | 31 |
| 31 | 19 | 4735619 | 22 | -19..3 | 318 | 349 | 31 |
| 31 | 19 | 13124227 | 23 | -19..4 | 318 | 349 | 31 |
| 31 | 19 | 21512835 | 24 | -19..5 | 318 | 349 | 31 |

These are finite bursts, not eventual period 2: none of the
recorded `L≥30` rows reaches the cap after doubling.

## What is proved, what is not

Proved (machine-checked in this run):

- The Cycle I packed engine, on every finite row of Hamming weight
  `1..8` and span `≤24` with the origin in the live convex
  hull (`min(live)≤0≤max(live)`, `s+1` translations), produces a
  longest period-2 centre run of length
  `L_run=31` inside `tcap=32w+512`.
- Self-checks as above, including in-hull `w=17` mask `281769`
  `L=31`, and exclusion of off-hull `w=38` mask `17057305` (`L=35`,
  all live `< 0`).
- Every `L≥30` candidate was re-evolved at `2·tcap`.
- Every such in-hull row has `L≤31` at `tcap` and after doubling.

Not proved:

- A bound for weight `>8` or span `>24`.
- A bound for off-hull placements (Cycle L already found `L=35`).
- Eventual period 2 of any finite seed. A bounded burst is
  compatible with every centre eventually leaving period 2.
- A uniform-in-`w` theorem.

## Verdict

`FINITE_THEOREM`, wall time 402.0s.

- Reason: every finite row of Hamming weight 1..8 and span (maxlive-minlive)<=24 with the origin in the live convex hull (min(live)<=0<=max(live); C in [0,s]), has a longest period-2 centre run of length L<=31 inside tcap=32w+512. Any L>=30 row still has L>=30 and L<32 after doubling tcap. Mask 281769 (w=17) is in-hull with L=31; mask 17057305 (w=38) is off-hull (all live < 0) and is excluded. This is a finite theorem for those supports only, not a uniform-in-w bound, and not an exclusion of eventual period 2.
- `L≥32` after doubling: no.
- Finite theorem `L≤31` on in-hull weight≤8 span≤24: yes.
- Survive / uniform proof: no.

## Files

- `research/period2_hull.md` (this note)
- `research/period2_hull.py` (`--certify` runs the checks and the
  in-hull weight-8 span-24 census)
- `research/period2_hull.json` (dump)

