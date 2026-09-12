# Defect recurrence: local Boolean fits

This note is ideas13 item 2 (leftover ideas11 item 5 / ideas12 item 3; prize Problem 2). It does **not** prove `D(N)=o(N)`, and it does not claim a prize result.

Helper: `research/defect_recurrence.py --certify`. Dump:
`research/defect_recurrence.json`. Packed evolution is the same
engine as `experiment.center_bits`; that file is not modified.

## Attack

Cycle K wrote `D(N) = sum_{t<N} (2 c_t - 1)` as the signed sum of
the centre at **defect** times `t` with `c_t = c_{t-1}`, plus an
`O(1)` endpoint from the alternating positions:

```
D_alt(N) = (σ_0 + σ_{N-1}) / 2  ∈  {-1, 0, +1},
D(N)     = D_defects(N) + D_alt(N).
```

On the length-`4096` centre prefix that identity holds with `D=-40`, `D_defects=-41`, `D_alt=1` (same `D(4096)=-40` as [xor_transform.md](xor_transform.md)). The defect sequence still has Berlekamp–Massey `L(4096)=2048` so `L/n=0.5000 ~ 1/2`, matching `L(c)=2049` on the same length (`L/n=0.5002`).

A *local* recurrence for `d_t = 1_{c_t=c_{t-1}}` would still be a
Problem 2 handle if it closed on a bounded window (a cellular
automaton or finite-memory shift on `d`, or on `(c,l,r)` without
growing the spatial slice). Then the signed sum of `d` would be a
function of a finite state, and one could hope to bound `D(N)`.

**Kill:** every defect window `w=1..8` mismatches on the prize seed
through `t=4096` (so `d` is not a low-order CA), or the only
Boolean fits from `c_{t-w..t}` plus leftover neighbour bits secretly
need the light cone.

## Local algebra

Rule 30 is `x(t+1,j) = x(t,j-1) XOR (x(t,j) OR x(t,j+1))`. Write
`l_t = x(t,-1)`, `c_t = x(t,0)`, `r_t = x(t,1)`. Then

\[
c_{t+1}=l_t\oplus(c_t\lor r_t),\qquad
d_{t+1}=1_{c_{t+1}=c_t}.
\]

The eight triples:

| `c` | `l` | `r` | `c_{t+1}` | `d_{t+1}` |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 |

Closed form: if `c_t=1` then `d_{t+1} = NOT l_t` (right neighbour
drops out); if `c_t=0` then `d_{t+1} = 1_{l_t=r_t}`. So `d_{t+1}`
**is** a Boolean of the radius-1 slice. The leftover pair does not
close:

\[
l_{t+1}=x(t,-2)\oplus(l_t\lor c_t),\qquad
r_{t+1}=c_t\oplus(r_t\lor x(t,2)).
\]

Next leftovers need `x(t,±2)`. A bounded history of `(l,c,r)` is a
bounded spacetime diamond; the missing bits sit on the light cone.
Radius `k` at time `t` determines `d_{t+1},…,d_{t+k}` and fails at
`d_{t+k+1}` — the original CA window.

## Engine

Packing is `experiment.py`: `z_0=1`, `z=(z<<2)^((z<<1)|z)`,
`x(t,j)=(z>>(j+t))&1`. The centre is bit `t`; leftovers sit at
indices `t-1` and `t+1`. Centre bits match `experiment.center_bits`
through `4097`, including the known 20-bit word
`11011100110001011001`. An independent live-cell spacetime agrees
on `c`, `l`, `r`, `x(t,±2)` for `t=0..64`. The three-bit formula
matches `c_{t+1}` and `d_{t+1}` for `t=1..4096`. The prefix-16
defects are the seven times `1,4,5,7,9,11,12` recorded in
[period2_defects.md](period2_defects.md). Synthetic `01` has a
width-1 rule `d_{t+1}=0`; constant `1` has `d_{t+1}=1`; a
period-2 defect stream has `d_{t+1}=NOT d_t`. A forced collision
is detected. Copied Berlekamp–Massey agrees with
`experiment.linear_complexity` on a 40-bit sample.

A Boolean fit on a finite prefix is a **witnessed function** only
if some key is reused and every reuse agrees. Unique keys are not
evidence (birthday / injective fingerprint of the triangle).

## Defect windows `w=1..8`

Predict `d_{t+1}` from `(d_t,…,d_{t-w+1})` at `t=w..4096` on the
prize seed. iid fair bits (seed `20260911`) are a noise control.

| w | keys | reused | colliding | consistent | witnessed | maj acc | first mismatch | iid mismatch |
|---:|---:|---:|---:|---|---|---:|---|---|
| 1 | 2 | 2 | 2 | no | no | 0.5090 | t=3 | t=3 |
| 2 | 4 | 4 | 4 | no | no | 0.5096 | t=6 | t=3 |
| 3 | 8 | 8 | 8 | no | no | 0.5134 | t=11 | t=11 |
| 4 | 16 | 16 | 16 | no | no | 0.5177 | t=11 | t=14 |
| 5 | 32 | 32 | 32 | no | no | 0.5327 | t=11 | t=14 |
| 6 | 64 | 64 | 64 | no | no | 0.5493 | t=27 | t=21 |
| 7 | 128 | 128 | 128 | no | no | 0.5675 | t=27 | t=26 |
| 8 | 256 | 256 | 256 | no | no | 0.5975 | t=27 | t=26 |

Every prize-seed window collides, with reuse (so the collision is real) and first mismatch at small `t`. Majority-vote accuracy stays near `1/2`, as on iid defects. Width 8 has `2^8=256` keys and thousands of samples; it is not an undersampled lookup. The defect sequence is not a cellular automaton of memory `≤8`.

## Centre window plus leftover neighbours

Predict `d_{t+1}` from `c_{t-w..t}` and leftover neighbour bits
(cells adjacent to the centre, not already in the centre column).
Every row is listed; witnessed functions are those with reuse and
no colliding keys.

| w | leftover | key bits | reused | colliding | witnessed | maj acc | first mismatch | cone |
|---:|---|---:|---:|---:|---|---:|---|---|
| 0 | `none` | 1 | 2 | 2 | no | 0.5090 | t=3 | no |
| 0 | `l_t` | 2 | 4 | 2 | no | 0.7546 | t=10 | yes |
| 0 | `r_t` | 2 | 4 | 4 | no | 0.5134 | t=3 | yes |
| 0 | `l_t,r_t` | 3 | 8 | 0 | yes | 1.0000 | — | yes |
| 0 | `l_t,r_t,l_{t-1},r_{t-1}` | 5 | 24 | 0 | yes | 1.0000 | — | yes |
| 1 | `none` | 2 | 4 | 4 | no | 0.5146 | t=4 | no |
| 1 | `l_t` | 3 | 8 | 4 | no | 0.8696 | t=10 | yes |
| 1 | `r_t` | 3 | 8 | 8 | no | 0.5149 | t=6 | yes |
| 1 | `l_t,r_t` | 4 | 16 | 0 | yes | 1.0000 | — | yes |
| 1 | `l_t,r_t,l_{t-1},r_{t-1}` | 6 | 24 | 0 | yes | 1.0000 | — | yes |
| 2 | `none` | 3 | 8 | 8 | no | 0.5155 | t=6 | no |
| 2 | `l_t` | 4 | 16 | 8 | no | 0.8696 | t=10 | yes |
| 2 | `r_t` | 4 | 16 | 16 | no | 0.5226 | t=6 | yes |
| 2 | `l_t,r_t` | 5 | 32 | 0 | yes | 1.0000 | — | yes |
| 2 | `l_t,r_t,l_{t-1},r_{t-1}` | 7 | 48 | 0 | yes | 1.0000 | — | yes |
| 3 | `none` | 4 | 16 | 16 | no | 0.5213 | t=11 | no |
| 3 | `l_t` | 5 | 32 | 16 | no | 0.8908 | t=11 | yes |
| 3 | `r_t` | 5 | 32 | 32 | no | 0.5320 | t=16 | yes |
| 3 | `l_t,r_t` | 6 | 64 | 0 | yes | 1.0000 | — | yes |
| 3 | `l_t,r_t,l_{t-1},r_{t-1}` | 8 | 96 | 0 | yes | 1.0000 | — | yes |
| 4 | `none` | 5 | 32 | 32 | no | 0.5275 | t=18 | no |
| 4 | `l_t` | 6 | 64 | 31 | no | 0.8915 | t=69 | yes |
| 4 | `r_t` | 6 | 64 | 63 | no | 0.5373 | t=18 | yes |
| 4 | `l_t,r_t` | 7 | 127 | 0 | yes | 1.0000 | — | yes |
| 4 | `l_t,r_t,l_{t-1},r_{t-1}` | 9 | 188 | 0 | yes | 1.0000 | — | yes |
| 5 | `none` | 6 | 64 | 64 | no | 0.5442 | t=34 | no |
| 5 | `l_t` | 7 | 128 | 61 | no | 0.8981 | t=87 | yes |
| 5 | `r_t` | 7 | 124 | 120 | no | 0.5591 | t=34 | yes |
| 5 | `l_t,r_t` | 8 | 232 | 0 | yes | 1.0000 | — | yes |
| 5 | `l_t,r_t,l_{t-1},r_{t-1}` | 10 | 327 | 0 | yes | 1.0000 | — | yes |
| 6 | `none` | 7 | 128 | 128 | no | 0.5644 | t=34 | no |
| 6 | `l_t` | 8 | 256 | 109 | no | 0.9012 | t=87 | yes |
| 6 | `r_t` | 8 | 224 | 214 | no | 0.5857 | t=34 | yes |
| 6 | `l_t,r_t` | 9 | 410 | 0 | yes | 1.0000 | — | yes |
| 6 | `l_t,r_t,l_{t-1},r_{t-1}` | 11 | 542 | 0 | yes | 1.0000 | — | yes |
| 7 | `none` | 8 | 256 | 256 | no | 0.5917 | t=34 | no |
| 7 | `l_t` | 9 | 512 | 171 | no | 0.9105 | t=87 | yes |
| 7 | `r_t` | 9 | 407 | 378 | no | 0.6164 | t=34 | yes |
| 7 | `l_t,r_t` | 10 | 694 | 0 | yes | 1.0000 | — | yes |
| 7 | `l_t,r_t,l_{t-1},r_{t-1}` | 12 | 820 | 0 | yes | 1.0000 | — | yes |
| 8 | `none` | 9 | 512 | 505 | no | 0.6349 | t=34 | no |
| 8 | `l_t` | 10 | 940 | 235 | no | 0.9200 | t=87 | yes |
| 8 | `r_t` | 10 | 703 | 614 | no | 0.6681 | t=34 | yes |
| 8 | `l_t,r_t` | 11 | 1027 | 0 | yes | 1.0000 | — | yes |
| 8 | `l_t,r_t,l_{t-1},r_{t-1}` | 13 | 1062 | 0 | yes | 1.0000 | — | yes |

Centre-only windows (`leftover=none`) all mismatch. Adding only
`l_t` or only `r_t` still mismatches: algebra needs `r` when
`c=0` and needs `l` when `c=1`. Adding the current pair
`(l_t, r_t)` is a witnessed function for every `w` — that is the
radius-1 slice, i.e. the original local rule, not a closed
recurrence on the centre column. A one-step history of leftovers
`l_t,r_t,l_{t-1},r_{t-1}` also works, because it contains the
current pair; it does not remove the cone.

Windows of leftovers without the centre column:

| w | leftover | target | key bits | reused | colliding | witnessed | maj acc | first mismatch |
|---:|---|---|---:|---:|---:|---|---:|---|
| 1 | `l_t..l_{t-w+1}` | `d_{t+1}` | 1 | 2 | 2 | no | 0.7468 | t=10 |
| 1 | `r_t..r_{t-w+1}` | `d_{t+1}` | 1 | 2 | 2 | no | 0.5090 | t=3 |
| 1 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 2 | 4 | 2 | no | 0.7529 | t=10 |
| 1 | `(l,r) window reconstructs c_t` | `c_t` | 2 | 4 | 4 | no | 0.5134 | t=6 |
| 2 | `l_t..l_{t-w+1}` | `d_{t+1}` | 2 | 4 | 4 | no | 0.7468 | t=10 |
| 2 | `r_t..r_{t-w+1}` | `d_{t+1}` | 2 | 4 | 4 | no | 0.5104 | t=4 |
| 2 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 4 | 16 | 4 | no | 0.8774 | t=27 |
| 2 | `(l,r) window reconstructs c_t` | `c_t` | 4 | 16 | 8 | no | 0.7680 | t=16 |
| 3 | `l_t..l_{t-w+1}` | `d_{t+1}` | 3 | 8 | 8 | no | 0.7467 | t=12 |
| 3 | `r_t..r_{t-w+1}` | `d_{t+1}` | 3 | 8 | 8 | no | 0.5144 | t=5 |
| 3 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 6 | 56 | 4 | no | 0.9717 | t=83 |
| 3 | `(l,r) window reconstructs c_t` | `c_t` | 6 | 56 | 8 | no | 0.9399 | t=83 |
| 4 | `l_t..l_{t-w+1}` | `d_{t+1}` | 4 | 16 | 16 | no | 0.7637 | t=14 |
| 4 | `r_t..r_{t-w+1}` | `d_{t+1}` | 4 | 16 | 16 | no | 0.5187 | t=10 |
| 4 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 8 | 152 | 4 | no | 0.9936 | t=393 |
| 4 | `(l,r) window reconstructs c_t` | `c_t` | 8 | 152 | 8 | no | 0.9839 | t=107 |
| 5 | `l_t..l_{t-w+1}` | `d_{t+1}` | 5 | 32 | 32 | no | 0.7674 | t=44 |
| 5 | `r_t..r_{t-w+1}` | `d_{t+1}` | 5 | 32 | 32 | no | 0.5301 | t=27 |
| 5 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 10 | 385 | 3 | no | 0.9985 | t=2015 |
| 5 | `(l,r) window reconstructs c_t` | `c_t` | 10 | 385 | 7 | no | 0.9951 | t=446 |
| 6 | `l_t..l_{t-w+1}` | `d_{t+1}` | 6 | 64 | 61 | no | 0.7722 | t=57 |
| 6 | `r_t..r_{t-w+1}` | `d_{t+1}` | 6 | 64 | 64 | no | 0.5473 | t=27 |
| 6 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 12 | 768 | 2 | no | 0.9993 | t=2015 |
| 6 | `(l,r) window reconstructs c_t` | `c_t` | 12 | 768 | 4 | no | 0.9980 | t=447 |
| 7 | `l_t..l_{t-w+1}` | `d_{t+1}` | 7 | 128 | 112 | no | 0.7778 | t=80 |
| 7 | `r_t..r_{t-w+1}` | `d_{t+1}` | 7 | 128 | 128 | no | 0.5721 | t=39 |
| 7 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 14 | 1038 | 1 | no | 0.9998 | t=2184 |
| 7 | `(l,r) window reconstructs c_t` | `c_t` | 14 | 1038 | 2 | no | 0.9995 | t=2184 |
| 8 | `l_t..l_{t-w+1}` | `d_{t+1}` | 8 | 256 | 201 | no | 0.7897 | t=80 |
| 8 | `r_t..r_{t-w+1}` | `d_{t+1}` | 8 | 256 | 256 | no | 0.6016 | t=39 |
| 8 | `(l,r)_t..(l,r)_{t-w+1}` | `d_{t+1}` | 16 | 956 | 0 | yes | 1.0000 | — |
| 8 | `(l,r) window reconstructs c_t` | `c_t` | 16 | 956 | 0 | yes | 1.0000 | — |

A single leftover pair `(l_t,r_t)` does not determine `d_{t+1}` (the truth table already splits on `c`). Width-`7` leftover pair histories still collide (first mismatch `t=2184`). Width `8` of `(l,r)` is consistent on this prefix (`956` reused keys): that is `16` light-cone bits, and the required memory grew through the smaller widths. The same leftover window reconstructs `c_t` at width `8` (witnessed). That is reading the centre back out of the cone, not a closed defect rule. Algebra still needs `c_t`; a growing leftover history is the original triangle.

## Light cone and closing of leftovers

Spatial slice `x(t,-k)..x(t,k)` at times `t=8..` versus `d_{t+j}`
and versus the next leftover pair. Algebra: radius `k` determines
`d_{t+1}..d_{t+k}` and the next leftovers iff `k≥2`.

| radius | target | key bits | colliding | witnessed | algebra |
|---:|---|---:|---:|---|---|
| 0 | `d_{t+1}` | 1 | 2 | no | no |
| 0 | `d_{t+2}` | 1 | 2 | no | no |
| 1 | `d_{t+1}` | 3 | 0 | yes | yes |
| 1 | `d_{t+2}` | 3 | 8 | no | no |
| 1 | `d_{t+3}` | 3 | 8 | no | no |
| 2 | `d_{t+1}` | 5 | 0 | yes | yes |
| 2 | `d_{t+2}` | 5 | 0 | yes | yes |
| 2 | `d_{t+3}` | 5 | 32 | no | no |
| 2 | `d_{t+4}` | 5 | 32 | no | no |
| 3 | `d_{t+1}` | 7 | 0 | yes | yes |
| 3 | `d_{t+2}` | 7 | 0 | yes | yes |
| 3 | `d_{t+3}` | 7 | 0 | yes | yes |
| 3 | `d_{t+4}` | 7 | 128 | no | no |
| 3 | `d_{t+5}` | 7 | 128 | no | no |
| 4 | `d_{t+1}` | 9 | 0 | yes | yes |
| 4 | `d_{t+2}` | 9 | 0 | yes | yes |
| 4 | `d_{t+3}` | 9 | 0 | yes | yes |
| 4 | `d_{t+4}` | 9 | 0 | yes | yes |
| 4 | `d_{t+5}` | 9 | 497 | no | no |
| 4 | `d_{t+6}` | 9 | 492 | no | no |

Next leftovers from a radius-`k` slice:

| radius | target | colliding | witnessed | algebra closes |
|---:|---|---:|---|---|
| 0 | `l_{t+1}` | 2 | no | no |
| 0 | `r_{t+1}` | 2 | no | no |
| 0 | `(l_{t+1},r_{t+1})` | 2 | no | no |
| 1 | `l_{t+1}` | 8 | no | no |
| 1 | `r_{t+1}` | 4 | no | no |
| 1 | `(l_{t+1},r_{t+1})` | 8 | no | no |
| 2 | `l_{t+1}` | 0 | yes | yes |
| 2 | `r_{t+1}` | 0 | yes | yes |
| 2 | `(l_{t+1},r_{t+1})` | 0 | yes | yes |
| 3 | `l_{t+1}` | 0 | yes | yes |
| 3 | `r_{t+1}` | 0 | yes | yes |
| 3 | `(l_{t+1},r_{t+1})` | 0 | yes | yes |
| 4 | `l_{t+1}` | 0 | yes | yes |
| 4 | `r_{t+1}` | 0 | yes | yes |
| 4 | `(l_{t+1},r_{t+1})` | 0 | yes | yes |

Bounded history of the triple `(l_t,c_t,r_t)`:

| w | target | key bits | colliding | witnessed | algebra closes |
|---:|---|---:|---:|---|---|
| 1 | `d_{t+1}` | 3 | 0 | yes | yes |
| 1 | `c_{t+1}` | 3 | 0 | yes | yes |
| 1 | `l_{t+1}` | 3 | 8 | no | no |
| 1 | `r_{t+1}` | 3 | 4 | no | no |
| 2 | `d_{t+1}` | 6 | 0 | yes | yes |
| 2 | `c_{t+1}` | 6 | 0 | yes | yes |
| 2 | `l_{t+1}` | 6 | 24 | no | no |
| 2 | `r_{t+1}` | 6 | 8 | no | no |
| 3 | `d_{t+1}` | 9 | 0 | yes | yes |
| 3 | `c_{t+1}` | 9 | 0 | yes | yes |
| 3 | `l_{t+1}` | 9 | 64 | no | no |
| 3 | `r_{t+1}` | 9 | 16 | no | no |
| 4 | `d_{t+1}` | 12 | 0 | yes | yes |
| 4 | `c_{t+1}` | 12 | 0 | yes | yes |
| 4 | `l_{t+1}` | 12 | 159 | no | no |
| 4 | `r_{t+1}` | 12 | 40 | no | no |
| 5 | `d_{t+1}` | 15 | 0 | yes | yes |
| 5 | `c_{t+1}` | 15 | 0 | yes | yes |
| 5 | `l_{t+1}` | 15 | 371 | no | no |
| 5 | `r_{t+1}` | 15 | 89 | no | no |
| 6 | `d_{t+1}` | 18 | 0 | yes | yes |
| 6 | `c_{t+1}` | 18 | 0 | yes | yes |
| 6 | `l_{t+1}` | 18 | 629 | no | no |
| 6 | `r_{t+1}` | 18 | 148 | no | no |
| 7 | `d_{t+1}` | 21 | 0 | yes | yes |
| 7 | `c_{t+1}` | 21 | 0 | yes | yes |
| 7 | `l_{t+1}` | 21 | 735 | no | no |
| 7 | `r_{t+1}` | 21 | 156 | no | no |
| 8 | `d_{t+1}` | 24 | 0 | yes | yes |
| 8 | `c_{t+1}` | 24 | 0 | yes | yes |
| 8 | `l_{t+1}` | 24 | 565 | no | no |
| 8 | `r_{t+1}` | 24 | 110 | no | no |

Radius 0 (the centre bit) does not determine `d_{t+1}`. Radius 1
does, and fails for `d_{t+2}`. Radius 1 does not determine
`(l_{t+1},r_{t+1})`; radius 2 does. A history of `w≤8` triples
determines `d_{t+1}` and `c_{t+1}` (they sit in the last triple)
and never determines the next leftovers. The state `(l,c,r)` is
not closed. Extending the horizon grows the spatial window: that
is the Rule 30 light cone, not a defect CA.

## Why it died

Preregistered kill: every window w=1..8 of previous defects has a mismatch (the defect sequence is not itself a low-order CA / shift of finite memory), or fitting d_{t+1} from (c_{t-w..t}, leftover neighbour bits) secretly needs the light cone. Both fired. Every defect window w=1..8 mismatches on the prize seed through t=4096 (w=1 at t=3, w=2 at t=6, w=3 at t=11, w=4 at t=11, w=5 at t=11, w=6 at t=27, w=7 at t=27, w=8 at t=27); d is not a width-<=8 CA / finite-memory shift. D_{t+1} is a witnessed Boolean of the radius-1 slice (c_t,l_t,r_t) but not of any centre-only window; the leftover pair (l,r) does not close on a bounded history of triples (next leftovers need x(t,±2), the original light cone). Radius 1 determines d_{t+1} and fails for d_{t+2}, so any longer horizon secretly grows the spatial window. Not a prize claim.

Cycle K already killed density / linear-complexity shortcuts.
This freeze kills the remaining local-recurrence hope: `d` is not
a width-`≤8` Boolean CA, and the only exact local rule for
`d_{t+1}` is the original three-bit slice, whose leftovers do not
close. Finite evidence on the prize prefix through `t=4096`. Not
a prize claim.

## Verdict

`KILL`, wall time 0.84s.

- Kill: yes.
- Survive: no.
- Reason: Every defect window w=1..8 mismatches on the prize seed through t=4096 (w=1 at t=3, w=2 at t=6, w=3 at t=11, w=4 at t=11, w=5 at t=11, w=6 at t=27, w=7 at t=27, w=8 at t=27); d is not a width-<=8 CA / finite-memory shift. D_{t+1} is a witnessed Boolean of the radius-1 slice (c_t,l_t,r_t) but not of any centre-only window; the leftover pair (l,r) does not close on a bounded history of triples (next leftovers need x(t,±2), the original light cone). Radius 1 determines d_{t+1} and fails for d_{t+2}, so any longer horizon secretly grows the spatial window. Not a prize claim.

## Files

- `research/defect_recurrence.md` (this note)
- `research/defect_recurrence.py` (`--certify` runs the checks and the freeze)
- `research/defect_recurrence.json` (dump)

Self-check: packed centre agrees with `experiment.center_bits` on 256 bits and on `0..4097`; `checks.all_ok=True`.

