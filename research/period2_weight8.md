# Period-2 `L_run`: weight-8 span-24 census

This note extends Cycle K (`research/period2_lrun_family.md`). It does
**not** exclude eventual period 2 for every finite row, and it does
not claim a prize result. It is a finite census of Hamming weight
`≤8` and span `≤24`, not a uniform-in-`w` bound.

Helper: `research/period2_weight8.py --certify`. Dump:
`research/period2_weight8.json`. Packed evolution is imported from
`research/period2_fiber.py` and that file is not modified.

## Attack

Cycle K found `L=31` on a weight-8 row of span `maxlive-minlive=18`
(inclusive length 19), true radius 17, mask `281769`, a run from
`t=320` to `t=351`. Cycle J’s cap `8w+128=264` misses that burst
entirely. Both known maximizers (masks `4369552` and `281769`) have
eight 1s. ideas11 item 1 asks for a complete-up-to-translation census
of every finite row of Hamming weight `1..8` and
`span = maxlive-minlive ≤ 24`, with the long cap `tcap=32w+512`.

**Kill:** a weight-`≤8` row with a period-2 centre run of length
`≥40` after doubling `tcap`, or max `L` strictly increasing with
span through 24.

**Finite theorem (this class only):** every scanned row has `L≤31`.

**Survive / uniform proof:** not claimed; the census is finite.

Packed Rule 30 is the Cycle I engine:

```
new = (row << 2) ^ ((row << 1) | row)
```

with the centre bit at time `t` equal to `(row >> (w+t)) & 1`. Bit 0
is the leftmost cell of the current support (spatial `-w` at `t=0`).

Each combinatorial support is placed in canonical form on `[0,s]`
and scored at every translation for which some live cell lies in
`[-s,s]` (origin in or within one span of the live block). That is
`3s+1` centres, not `2^{2w+1}` masks. `tcap=32w+512` of the true
radius of that placement. Any `L≥30` row is re-evolved at `2·tcap`.

## Self-checks

- `w=11` mask `4369552`, `tcap=8·11+128=216`: `L=29` from
  `t=159` to `t=188`. Live cells
  `-7, -4, -1, 0, 2, 4, 6, 11`. Weight 8, span 18.
- `w=17` mask `281769`, `tcap=8·17+256=392`:
  `L=31` from `t=320` to `t=351`.
  Cycle J’s `8w+128` reports `L=6` (misses the burst).
  Census cap `32·17+512=1056` still has
  `L=31` from `t=320`.
- Inlined inner loop agrees with `period2_fiber.scan_mask_runs`.
- Packed traces match the independent live-cell spacetime on the prize
  seed, on mask `4369552`, and on mask `281769`.
- Multi-centre extraction of a canonical support agrees with the packed
  engine on both maximizers and on random off-hull placements.
- `checks.all_ok=True`.

## Census

`536,155` combinatorial supports, `35,324,440` origin-near placements, `tcap=32w+512`, `4` processes, 1563.4s.

Span here is `maxlive-minlive`. Cycle K’s “span 19” is inclusive
length `max-min+1`, i.e. this span 18.

| `wt` | types | placements | `L_run` | `n≥30` | `n≥31` | best | `w` | span |
|-----:|------:|-----------:|--------:|-------:|-------:|-----:|----:|-----:|
| 1 | 1 | 1 | **7** | 0 | 0 | 1 | 0 | 0 |
| 2 | 24 | 924 | **19** | 0 | 0 | 33 | 3 | 5 |
| 3 | 276 | 14,076 | **26** | 0 | 0 | 8,388,673 | 38 | 23 |
| 4 | 2,024 | 115,874 | **31** | 1 | 1 | 2,113,601 | 30 | 21 |
| 5 | 10,626 | 648,186 | **32** | 3 | 3 | `20,22,27,39,43` | 43 | 23 |
| 6 | 42,504 | 2,699,004 | **32** | 5 | 5 | `20,22,27,39,43,44` | 44 | 24 |
| 7 | 134,596 | 8,787,196 | **32** | 8 | 7 | `7,10,13,14,22,26,30` | 30 | 23 |
| 8 | 346,104 | 23,059,179 | **35** | 24 | 15 | 17,057,305 | 38 | 24 |

| span | types | placements | `L_run` | `n≥30` | `n≥31` | best | `w` |
|-----:|------:|-----------:|--------:|-------:|-------:|-----:|----:|
| 0 | 1 | 1 | **7** | 0 | 0 | 1 | 0 |
| 1 | 1 | 4 | **10** | 0 | 0 | 3 | 1 |
| 2 | 2 | 14 | **11** | 0 | 0 | 112 | 3 |
| 3 | 4 | 40 | **13** | 0 | 0 | 15 | 4 |
| 4 | 8 | 104 | **15** | 0 | 0 | 25 | 7 |
| 5 | 16 | 256 | **19** | 0 | 0 | 33 | 3 |
| 6 | 32 | 608 | **19** | 0 | 0 | 97 | 3 |
| 7 | 64 | 1,408 | **19** | 0 | 0 | 231 | 4 |
| 8 | 127 | 3,175 | **21** | 0 | 0 | 277 | 7 |
| 9 | 247 | 6,916 | **21** | 0 | 0 | 1,058 | 5 |
| 10 | 466 | 14,446 | **23** | 0 | 0 | 1,991 | 13 |
| 11 | 848 | 28,832 | **23** | 0 | 0 | 18,216 | 7 |
| 12 | 1,486 | 54,982 | **24** | 0 | 0 | `12,13,14,15,17,21,22,24` | 24 |
| 13 | 2,510 | 100,400 | **29** | 0 | 0 | 4,733,796,352 | 16 |
| 14 | 4,096 | 176,128 | **29** | 0 | 0 | 26,647,461,888 | 17 |
| 15 | 6,476 | 297,896 | **29** | 0 | 0 | 87,654,662,144 | 18 |
| 16 | 9,949 | 487,501 | **29** | 0 | 0 | 450,187,231,232 | 19 |
| 17 | 14,893 | 774,436 | **30** | 1 | 0 | `16,18,19,23,27,28,33` | 33 |
| 18 | 21,778 | 1,197,790 | **31** | 4 | 2 | 281,769 | 17 |
| 19 | 31,180 | 1,808,440 | **31** | 3 | 1 | `12,20,23,27,30,31` | 31 |
| 20 | 43,796 | 2,671,556 | **31** | 2 | 1 | `12,20,23,27,30,32` | 32 |
| 21 | 60,460 | 3,869,440 | **31** | 3 | 3 | 2,294,017 | 17 |
| 22 | 82,160 | 5,504,720 | **31** | 6 | 6 | 6,488,321 | 17 |
| 23 | 110,056 | 7,703,920 | **33** | 9 | 8 | 8,532,417 | 27 |
| 24 | 145,499 | 10,621,427 | **35** | 13 | 10 | 17,057,305 | 38 |

Max `L` versus span: 0:7, 1:10, 2:11, 3:13, 4:15, 5:19, 6:19, 7:19, 8:21, 9:21, 10:23, 11:23, 12:24, 13:29, 14:29, 15:29, 16:29, 17:30, 18:31, 19:31, 20:31, 21:31, 22:31, 23:33, 24:35.

Max `L` does **not** strictly increase with span through 24 (ties at several lengths; global max 35).

After a plateau `L=31` on spans `18..22`, the envelope rises again: `L=33` at span 23 and `L=35` at span 24. That is not the specified kill (every consecutive span would have to go up), but span 24 is not a plateau of `L` either.


Every recorded `L≥32` row has the origin **outside** the live convex hull (all 1s strictly left, or all strictly right, of cell 0). Among dumped `L≥30` rows, origin-in-hull max is `31`; off-hull max is `35`. Cycle K’s `L=31` maximizer has origin in the hull; the new `L=32,33,35` bursts do not.

## Witness

Least true-radius maximizer of the census:

- true radius `38`, mask `17057305`
- packed row (bit 0 = spatial `-38`): `10011000011000100010000010000000000000000000000000000000000000000000000000000`
- live at `-38, -35, -34, -29, -28, -24, -20, -14` (8 ones, span 24)
- origin in the live hull: `False` (this maximizer is entirely to the left of cell 0; the rightmost 1 is at `-14`, which still lies in `[-24,24]`)
- run of 35 from `t=159` to `t=194` (exclusive end)
- run bits `01010101010101010101010101010101010`
- bits immediately before and after: `0`, `0`
- `tcap=1728` and doubled `tcap=3456` both give `(L,start,end)=(35,159,194)`
- packed, fast loop, and naive spacetime agree (`witness_check.ok=True`)

Cycle J cap `8w+128=432` reports `L=35`.
Cycle K cap `8w+256=560` reports `L=35`. Census `32w+512=1728` reports `L=35`.

Known maximizers, rescored inside this census class:

- mask `4369552`: w=11 L=29 (expected ≥29), span 18, ok=True
- mask `281769`: w=17 L=31 (expected ≥31), span 18, ok=True

`L≥32` rows (unique `(w,mask)`): 8. All have origin off-hull.

| `L` | `w` | mask | span | live min..max | start | end | doubled L |
|----:|----:|-----:|-----:|--------------:|------:|----:|----------:|
| 35 | 38 | 17057305 | 24 | -38..-14 | 159 | 194 | 35 |
| 33 | 26 | 16945191 | 24 | -26..-2 | 496 | 529 | 33 |
| 33 | 27 | 8532417 | 23 | -27..-4 | 1184 | 1217 | 33 |
| 32 | 30 | 1229510323501793280 | 23 | 7..30 | 964 | 996 | 32 |
| 32 | 31 | 7070706665430974464 | 24 | 7..31 | 964 | 996 | 32 |
| 32 | 38 | 19268619 | 24 | -38..-14 | 584 | 616 | 32 |
| 32 | 43 | 82208182442275685565202432 | 23 | 20..43 | 607 | 639 | 32 |
| 32 | 44 | 473901374705896439855185920 | 24 | 20..44 | 607 | 639 | 32 |

These are finite bursts, not eventual period 2: none of the
recorded `L≥30` rows reaches the cap after doubling.

## What is proved, what is not

Proved (machine-checked in this run):

- The Cycle I packed engine, on every finite row of Hamming weight
  `1..8` and span `≤24` with the origin in/near the live
  span (`3s+1` translations), produces a longest period-2 centre
  run of length `L_run=35` inside `tcap=32w+512`.
- Self-checks as above, including `w=11` mask `4369552` `L=29` and
  `w=17` mask `281769` `L=31` at `tcap=8·17+256`.
- Every `L≥30` candidate was re-evolved at `2·tcap`; none grew,
  none reached `L≥40`, none reached the cap.
- Among those `L≥30` rows, origin-in-hull supports still have
  `L≤31`; every `L≥32` row is off-hull.

Not proved:

- A bound for weight `>8` or span `>24`.
- A bound `L≤31` for origin-in-hull rows: it holds on the dumped
  `L≥30` slice, but that is not a separately enumerated hull-only
  census.
- Eventual period 2 of any finite seed. A bounded burst is
  compatible with every centre eventually leaving period 2.
- A uniform-in-`w` theorem.

## Verdict

`L_GT_31`, wall time 1564.0s.

- Reason: best L on the census is 35 (in 32..39). No L>=40, and max L does not strictly increase with span through 24. The L<=31 finite theorem is false on this class; a larger constant is not claimed.
- `L≥40`: no.
- Span strictly increasing through 24: no.
- Finite theorem `L≤31` on this census: no.
- Survive / uniform proof: no.

## Files

- `research/period2_weight8.md` (this note)
- `research/period2_weight8.py` (`--certify` runs the checks and the
  weight-8 span-24 census)
- `research/period2_weight8.json` (dump)

