# Period-2 `L_run`: origin-in-hull weight-9/10 span-20 census

This note extends Cycle M (`research/period2_hull.md`). It does
**not** exclude eventual period 2 for every finite row, and it does
not claim a prize result. It is a finite census of Hamming weights
`9` and `10` and span `≤20` with the origin in the live convex hull,
not a uniform-in-`w` bound.

Helper: `research/period2_hull910.py --certify`. Dump:
`research/period2_hull910.json`. Packed evolution is imported from
`research/period2_fiber.py` and that file is not modified.
`research/period2_hull.py` is not modified.

## Attack

Cycle M proved `L≤31` for every in-hull weight-`≤8` span-`≤24` row
at `tcap=32w+512`. The prize seed’s later rows have larger weight.
ideas13 item 1 asks for the same origin-in-hull census at weights
`9` and `10`, span `≤20` (state space comparable to Cycle M), with

```
min(live) <= 0 <= max(live)
```

Each combinatorial support still sits on `[0,s]` with live endpoints.
In-hull is then `C ∈ [0,s]` (`s+1` centres), not Cycle L’s window
`C ∈ [-s, 2s]` (`3s+1` centres). Cap `tcap=32w+512` of the true
radius of that placement. Any `L≥30` row is re-evolved at `2·tcap`.

**Kill:** an in-hull weight-`9` or `10` span-`≤20` row with a
period-2 centre run of length `≥32` after doubling `tcap`.

**Finite theorem (this class only):** every in-hull weight-`9` or
`10` span-`≤20` row has `L≤31`.

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
  Not in this census (weight 8).
- `w=17` mask `281769`, `tcap=8·17+256=392`:
  `L=31` from `t=320` to `t=351`.
  Live `-17, -14, -12, -10, -7, -6, -3, 1`. In-hull
  (`min=-17 ≤ 0 ≤ 1`). Census cap
  `32·17+512=1056` still has `L=31`.
  Weight 8, span 18: **not** in this wt=9/10 census. The packed
  engine is unchanged.
- `w=38` mask `17057305`: live
  `-38, -35, -34, -29, -28, -24, -20, -14`. All live `< 0`,
  origin off-hull, `C=38` not in `[0, 24]`.
  Packed engine still gives `L=35` at `tcap=32·38+512`;
  excluded here by weight 8 and by the hull filter.
- Full-ones weight-9 span-8 and weight-10 span-9 supports match the
  packed engine at an in-hull centre.
- Inlined inner loop agrees with `period2_fiber.scan_mask_runs`.
- Packed traces match the independent live-cell spacetime on the prize
  seed, on mask `4369552`, and on mask `281769`.
- Multi-centre extraction of a canonical support agrees with the packed
  engine on the Cycle M in-hull maximizers. Hull scan `nC=s+1` does
  not contain the off-hull centre of mask `17057305`.
- Random in-hull centres of weight 9/10 (`C in [0,s]`) satisfy
  `min≤0≤max` and match the packed engine; random `C` outside `[0,s]`
  are off-hull.
- `checks.all_ok=True`.

## Census

`293,930` combinatorial supports, `5,819,814` in-hull placements (`C in [0,s]`), `tcap=32w+512`, `4` processes, 155.0s.

Span here is `maxlive-minlive`. Cycle L’s off-hull window used
`3s+1` translations; this census uses `s+1`.

| `wt` | types | placements | `L_run` | `n≥30` | `n≥31` | `n≥32` | best | `w` | span |
|-----:|------:|-----------:|--------:|-------:|-------:|-------:|-----:|----:|-----:|
| 9 | 125,970 | 2,477,410 | **31** | 3 | 2 | 0 | 806,057 | 17 | 19 |
| 10 | 167,960 | 3,342,404 | **30** | 2 | 0 | 0 | 1,592,244 | 10 | 18 |

| span | types | placements | `L_run` | `n≥30` | `n≥31` | `n≥32` | best | `w` |
|-----:|------:|-----------:|--------:|-------:|-------:|-------:|-----:|----:|
| 0 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 1 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 2 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 3 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 4 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 5 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 6 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 7 | 0 | 0 | **0** | 0 | 0 | 0 | — | — |
| 8 | 1 | 9 | **12** | 0 | 0 | 0 | 511 | 6 |
| 9 | 9 | 90 | **15** | 0 | 0 | 0 | 895 | 7 |
| 10 | 45 | 495 | **16** | 0 | 0 | 0 | 1,775 | 7 |
| 11 | 165 | 1,980 | **21** | 0 | 0 | 0 | 7,406 | 6 |
| 12 | 495 | 6,435 | **24** | 0 | 0 | 0 | 7,503 | 6 |
| 13 | 1,287 | 18,018 | **24** | 0 | 0 | 0 | 23,198 | 7 |
| 14 | 3,003 | 45,045 | **24** | 0 | 0 | 0 | 111,932 | 8 |
| 15 | 6,435 | 102,960 | **26** | 0 | 0 | 0 | 34,771 | 11 |
| 16 | 12,870 | 218,790 | **27** | 0 | 0 | 0 | 75,565 | 10 |
| 17 | 24,310 | 437,580 | **30** | 1 | 0 | 0 | 271,834 | 9 |
| 18 | 43,758 | 831,402 | **30** | 1 | 0 | 0 | 1,592,244 | 10 |
| 19 | 75,582 | 1,511,640 | **31** | 2 | 1 | 0 | 806,057 | 17 |
| 20 | 125,970 | 2,645,370 | **31** | 1 | 1 | 0 | 1,330,345 | 17 |

Max `L` versus span: 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:12, 9:15, 10:16, 11:21, 12:24, 13:24, 14:24, 15:26, 16:27, 17:30, 18:30, 19:31, 20:31.

Off-hull placements scored: `0` (must be 0; every scanned centre is `C in [0,s]`).

## Witness

Least true-radius maximizer of the in-hull census:

- true radius `17`, mask `806057`
- packed row (bit 0 = spatial `-17`): `10010101001100100011000000000000000`
- live at `-17, -14, -12, -10, -7, -6, -3, 1, 2` (9 ones, span 19)
- origin in the live hull: `True` (min=-17, max=2)
- run of 31 from `t=320` to `t=351` (exclusive end)
- run bits `0101010101010101010101010101010`
- bits immediately before and after: `0`, `0`
- `tcap=1056` and doubled `tcap=2112` both give `(L,start,end)=(31,320,351)`
- packed, fast loop, and naive spacetime agree (`witness_check.ok=True`)

Cycle J cap `8w+128=264` reports `L=6` (truncated).
Cycle K cap `8w+256=392` reports `L=31`. Census `32w+512=1056` reports `L=31`; doubled `2112` reports `L=31`.

Known Cycle M rows. All have weight 8, so none enter this census:

- mask `4369552`: w=11 L=29 (expected ≥29), span 18, wt=8, in-hull=True, excluded, ok=True
- mask `281769`: w=17 L=31 (engine expected 31), span 18, wt=8, in-hull=True, excluded from this census, ok=True
- mask `17057305`: in-hull=False, `C=38` not in `[0,s]`, wt=8, excluded, ok=True
- census_excludes_281769=True

`L≥31` in-hull rows (unique `(w,mask)`): 2. None reach `L≥32`.

| `L` | `w` | mask | span | live min..max | start | end | doubled L |
|----:|----:|-----:|-----:|--------------:|------:|----:|----------:|
| 31 | 17 | 806057 | 19 | -17..2 | 320 | 351 | 31 |
| 31 | 17 | 1330345 | 20 | -17..3 | 320 | 351 | 31 |

These are finite bursts, not eventual period 2: none of the
recorded `L≥30` rows reaches the cap after doubling.

## What is proved, what is not

Proved (machine-checked in this run):

- The Cycle I packed engine, on every finite row of Hamming weight
  `9` or `10` and span `≤20` with the origin in the live
  convex hull (`min(live)≤0≤max(live)`, `s+1` translations),
  produces a longest period-2 centre run of length
  `L_run=31` inside `tcap=32w+512`.
- Self-checks as above, including engine `L=31` on in-hull `w=17`
  mask `281769` (weight 8, **not** in this census), and exclusion
  of off-hull `w=38` mask `17057305` (`L=35`, all live `< 0`).
- Every `L≥30` candidate was re-evolved at `2·tcap`.
- Every such in-hull row has `L≤31` at `tcap` and after doubling.

Not proved:

- A bound for weight `>10` or span `>20`.
- A bound for off-hull placements (Cycle L already found `L=35`).
- Eventual period 2 of any finite seed. A bounded burst is
  compatible with every centre eventually leaving period 2.
- A uniform-in-`w` theorem.

## Verdict

`FINITE_THEOREM`, wall time 155.3s.

- Reason: every finite row of Hamming weight 9 or 10 and span (maxlive-minlive)<=20 with the origin in the live convex hull (min(live)<=0<=max(live); C in [0,s]), has a longest period-2 centre run of length L<=31 inside tcap=32w+512. Any L>=30 row still has L>=30 and L<32 after doubling tcap. Mask 281769 (w=17, wt=8, span=18) is in-hull with engine L=31 but is not in this census. This is a finite theorem for those supports only, not a uniform-in-w bound, and not an exclusion of eventual period 2.
- `L≥32` after doubling: no.
- Finite theorem `L≤31` on in-hull weight 9–10 span≤20: yes.
- Survive / uniform proof: no.

## Files

- `research/period2_hull910.md` (this note)
- `research/period2_hull910.py` (`--certify` runs the checks and the
  in-hull weight-9/10 span-20 census)
- `research/period2_hull910.json` (dump)

