# Period-2 centre: Condrey-style unique left fiber

This note is a checked lemma plus a finite scan. It does **not** exclude
eventual period 2 for every finite row, and it does not claim a prize
result. It does **not** re-prove the constant-trace case (Condrey 2026,
arXiv:2609.09431; the single-cell centre already has infinitely many 0s
and 1s by `research/constant_tails.md`).

Helper: `research/period2_fiber.py --certify`. Dump:
`research/period2_fiber.json`. Identities from
`research/period2_neighbor.md` (`u` has no consecutive 1s;
`u_{n+1}=1` iff a width-3 right vacuum) are reused as machine checks
and are not modified.

## Attack

Prove or kill: no nonzero finite-support configuration has an eventually
period-2 central trace. Broader than the prize seed, and broader than
the `L_0` left edge of that seed. Not the strip-graph residual-SCC
test, not onset SAT, not `F_T` ideal certificates.

Rule 30 is left permutive. Condrey’s Lemma 1 (triangular uniqueness)
therefore still applies: a right half together with a prescribed central
trace determines the left half uniquely, via

```
x(t, j-1) = x(t+1, j) XOR (x(t, j) OR x(t, j+1)),
```

hence

```
l_t = c_{t+1} XOR (c_t OR r_t).
```

For a constant trace Condrey computes that unique left in closed form
(an alternating tail selected by the leading right-hand 1, or a single
checkerboard) and observes that every nonzero member is infinite, so
the only finite constant-trace row is zero. The same mechanism at
period 2 has two phases, `01` repeating and `10` repeating. Phase `10`
is phase `01` of `F(x)`, and `F` preserves finite support, so it is
enough to understand phase `01` plus the scan of both.

WLOG phase `01`: `c_{2n}=0`, `c_{2n+1}=1`. Then as in
`research/alternating.md` and `research/period2_neighbor.md`,

```
l_{2n} = 1 XOR u_n,     l_{2n+1} = 1,
u_{n+1} = 1  iff  (u_n, e_n, f_n) = (0,0,0),
```

and `u` has no consecutive 1s. Both identities hold on every forced
period-2 right half in the scan (`u_no_consecutive_ones_phase01`,
`u_vacuum_triple_identity_phase01`).

Survive, in Condrey’s sense, would be a closed-form unique left that is
always infinite on nonzero finite rights. Kill would be a single finite
nonzero row whose centre stays period 2 for a time cap and still does
not break when the cap is extended.

## Exhaustive finite rows (experiment 1)

Every nonzero initial word of support radius `w=0..10` (`2^{2w+1}-1`
states; `w=10` is `2^{21}-1`) is evolved in a quiescent background up
to `tcap = 8w+128`. Packed Rule 30 (`new = (row<<2) ^ ((row<<1)|row)`,
bit 0 leftmost) matches an independent live-cell implementation on the
prize seed (`1101110011000101…`) and on sampled small rows.

An alternating run is a period-2 centre factor of either phase. `L_run(w)`
is the longest such run anywhere in `[0, tcap)`. `L_prefix(w)` is the
longest alternating prefix from time 0. No row is “eventual in the cap”
(last break inside the light cone `2w+8`, suffix at least 16), so none
was a candidate for cap extension.

| `w` | states | `tcap` | `L_run` | `L_prefix` | `L_suffix` | `L>4w+16` |
|----:|-------:|-------:|--------:|-----------:|-----------:|----------:|
| 0 | 1 | 128 | 7 | 1 | 1 | 0 |
| 1 | 7 | 136 | 8 | 7 | 8 | 0 |
| 2 | 31 | 144 | 10 | 7 | 4 | 0 |
| 3 | 127 | 152 | 13 | 7 | 10 | 0 |
| 4 | 511 | 160 | 15 | 7 | 8 | 0 |
| 5 | 2047 | 168 | 15 | 9 | 10 | 0 |
| 6 | 8191 | 176 | 24 | 10 | 16 | 0 |
| 7 | 32767 | 184 | 24 | 10 | 13 | 0 |
| 8 | 131071 | 192 | 24 | 15 | 16 | 0 |
| 9 | 524287 | 200 | 24 | 17 | 16 | 0 |
| 10 | 2097151 | 208 | 24 | 17 | 22 | 0 |

The prize seed (`w=0`) has `L_run=7`, the factor `1010101` starting at
time 35. The first radius-6 maximizer is the row `1111001010111`
(`mask=7503`), a run of 24 from `t=94` to `t=118`; extending that
evolution to 800 steps does not lengthen the run.

**Finite theorem (radius ≤ 10).** Every nonzero row of support radius
`w≤10` has every period-2 centre run of length at most `L_run(w)`,
hence at most 24, inside `tcap=8w+128`. In particular no such row has
an eventually period-2 centre visible in that window: a genuine
eventual regime would produce a suffix of length `tcap-O(w)`.

`L_run(w)=24` for every `6≤w≤10` is a plateau, not a superlinear
escape. Least squares over the whole table gives `L_run ≈ 2.02 w + 7`,
which is a summary of the small-`w` ramp plus the plateau, not a
conjecture that runs grow. Condrey already notes that left permutivity
forces `H(2,w)≥w` for *prefixes*; the scanned `L_prefix` is
`1,7,7,7,7,9,10,10,15,17,17`, compatible with that lower bound and
well below `4w+16`. No scanned row has a period-2 run longer than
`4w+16`.

This is a finite theorem for those `w`, not a uniform proof. A
radius-`11` row with a length-25 burst is not excluded.

## Unique left fiber (experiment 2)

For every finite right of width `w=0..10` (bits `1..w`, zeros beyond)
and both phases, the right half is evolved with the centre *forced*
period 2, then the left initial row `L_k=x(0,-k)` is reconstructed
for `T=8w+128` steps. Reconstruction of a genuine (unforced) spacetime
recovers the true left. The constant-trace formulas of Condrey
Theorems 2 and 3 are recovered as a sanity check, not a re-proof.

Facts on that fiber:

- **Uniqueness.** Condrey’s triangular uniqueness, only permutivity.
  The period-2 left is well-defined: prefixes of the reconstructed
  `L_k` are stable as `T` grows.
- **Never finite in the scan.** For every one of the `2(2^{11}-1)`
  rights, `min last1` is `T-O(1)` (e.g. 199 of 208 at `w=10` phase
  `01`). Trailing zeros are at most 10. No right has a zero tail of
  length 24 with last 1 bounded away from `T`. So no finite
  bimaterial period-2 fiber member was found, and the `>4w+16`
  bimaterial search is empty.
- **Not a function of the leading 1.** Unlike Condrey’s classes
  `C_m`, bits past the first right-hand 1 change the left. At width 8
  phase `01`, the 128 rights with leading 1 already produce 49
  distinct 40-bit left prefixes; at width 10 that count is 129.
- **No closed-form tail.** Generic lefts have Berlekamp–Massey length
  growing with the prefix (`max_bm80` reaches 52 at `w=10`). They are
  not eventually periodic, not `k mod 2`, and not Condrey’s
  checkerboard. Max gaps grow slowly with `w` (5 at vacuum, 16 by
  `w=6`) so even a uniform gap bound is not visible.
- **One sparse family.** The single 1 at position 6, phase `01`, has
  left head `1000000100000010000001…` (period 7, BM 7, infinitely
  many 1s). This is a special kernel, not the generic fiber.
- **Even-neighbor `u`.** On phase `01` the vacuum-triple identity
  never fails and `u` never has two consecutive 1s. Some rights have
  an eventually periodic `u` (period 5 pattern `00100` and period 7
  `0001010` are the most common attractors in the finite window).
  Most do not: 1341 of the phase-`01` rights in the cumulative scan
  have no 6-period suffix in the window. No scanned `u` is eventually
  zero, so the eventual-vacuum lemma of `research/period2_vacuum.md`
  does not hand us `F_k → k mod 2` on this family. For vacuum right,
  phase `01`, `u` tracks `(0001010)` after a short prefix only until
  even-time index `n=152`; the first later gap is 3, not 2 or 5
  (`research/period2_germ.md`). The spatial left still has BM `~T/2`.
  Periodic `u` is already Jen-excluded and does not force a periodic
  left in any case, because `F_k` is a nonlinear function of a growing
  prefix of `u`.

Truncating the unique left at depth `w` and evolving the resulting
radius-`w` row produces period-2 prefixes of length
`7,7,7,7,9,10,10,15` for `w=1..8`. That is the light cone of the first
missing 1 past the truncation — Condrey’s horizon argument with an
irregular gap sequence in place of “every odd depth”. It realises
`H(2,w)≥w` and dies at `O(w)`, as expected. It is not an eventual
witness.

## What is proved, what is not

Proved (and machine-checked):

- Left permutivity plus a prescribed centre uniquely determines the
  left; the period-2 inverse is `l_t = c_{t+1} XOR (c_t OR r_t)`.
- On every forced period-2 phase-`01` right half of width `≤10`, `u`
  has no consecutive 1s and `u_{n+1}=1` iff a width-3 right vacuum.
- The odd-time left neighbor is identically 1 on phase `01`.
- Packed evolution, reconstruction, and Condrey’s two constant fibers
  agree with independent implementations.
- **Finite theorem.** Every nonzero row of radius `w≤10` breaks every
  period-2 centre run by length `L_run(w)≤24` inside `tcap=8w+128`.
  `f(w)=L_run(w)` is the table above.

Not proved:

- A closed-form unique left for period 2, infinite on every nonzero
  finite right. The left is unique and empirically infinite, but
  generic members are high linear-complexity sequences, not an
  alternating or checkerboard tail.
- A uniform-in-`w` bound `L_run(w)≤24`. The plateau through radius 10
  is consistent with a bound and is not a theorem for radius 11.
- Eventual period 2 of the prize seed. The seed is the `w=0` line of
  the table (`L_run=7`); that is the same finite observation as the
  rest of the scan.

## Why the attack does not survive as a Condrey lemma

Condrey’s constant case works because the unique left is an explicit
Boolean of the right (prefix-OR, or one checkerboard), visibly
infinite. Period 2 keeps uniqueness and, in the scan, infinitude of
the left, but drops the closed form: the right half under a forced
period-2 boundary injects a chaotic wake, `u` is not classified by
the leading 1, and `F_k(u)` is a nonlinear sliding function of a
growing prefix. A finite list of `u`-attractors does not cover width
10. Without that formula there is no `T`-independent identification
of a 1 at an odd depth past any radius, so there is no sharp horizon
`w+2` and no uniform exclusion of all finite rows.

The complementary kill — a finite fiber member, or a row whose centre
stays period 2 through an extended cap — did not fire.

## Verdict

`FINITE_THEOREM`, wall time 95.0s.

- Kill: no.
- Survive: no.
- Witness: none.
- Exclusion table: `L_run(w)` as above, `tcap=8w+128`,
  `L_run(w)≤24` for `w≤10`.

## Files

- `research/period2_fiber.md` (this note)
- `research/period2_fiber.py` (`--certify` runs the checks, the
  radius-`w` exhaustive, and the fiber reconstruction)
- `research/period2_fiber.json` (dump)
