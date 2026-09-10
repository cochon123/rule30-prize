# Period-2 bursts: defect density and signed discrepancy

This note is ideas10 item 4 (prize Problem 2). It does **not**
prove `D(N)=o(N)`, and it does not claim a prize result.

Helper: `research/period2_defects.py --certify`. Dump:
`research/period2_defects.json`. Packed evolution is the same
engine as `experiment.center_bits`; that file is not modified.

## Attack

Write `D(N) = sum_{t<N} (2 c_t - 1)`. Split the centre into
maximal alternating (period-2) runs: a new run starts at every
time `t >= 1` with `c_t == c_{t-1}`. Call those times **defects**.
Each defect is a global phase flip between the two period-2
alignments `01` and `10`. An *isolated* phase flip is a defect
sitting between two genuine alternating bursts (neither neighbour
pair is a defect).

A period-2 burst of even length contributes **0** to `D`: the
bits pair as `01` or `10`. An odd-length burst contributes `±1`
(one leftover unpaired bit). Length-1 runs are leftover defect
bits that never seed a burst. Hence

```
D(N) = (signed leftovers of odd-length runs),
|D(N)| <= (# odd runs) <= (# runs) = (# defects) + 1.
```

A tighter pairing holds on *positions*: writing `σ_t = 2 c_t - 1`,
the signed sum over alternating times (`t=0` and every `t` with
`c_t != c_{t-1}`) telescopes to an endpoint,

```
D_alt(N) = (σ_0 + σ_{N-1}) / 2  ∈  {-1, 0, +1},
D(N)     = D_defects(N) + D_alt(N).
```

So even-length interior bursts, and in fact every alternating
position, contribute only `O(1)` to `D`. The whole discrepancy
is the signed sum of the defect bits plus a boundary. If defect
density were `o(1)`, that sum would be `o(N)` and Problem 2 would
follow.

**Kill:** density stays `>= 1/4` on the prize seed at `N=10^5`,
or the defect sequence has Berlekamp–Massey `L(N) ~ N/2` like
`c` itself.

iid fair bits have expected defect density `1/2` and mean
alternating-run length `2`. Isolated phase flips have expected
density `1/8`.

## Engine

Packed Rule 30

```
new = (row << 2) ^ ((row << 1) | row)
```

with the centre bit at time `t` equal to `(row >> (w+t)) & 1`.
The prize seed is `w=0`, mask `1`, which is
`experiment.center_bits`. The packed prefix of length 256 matches
that function (`1101110011000101…`). An independent
live-cell spacetime agrees on the prize seed and on a sampled
radius-3 row. The streaming defect scorer agrees with the
stored-trace analyzer. `D_alt = (σ_0 + σ_{N-1})/2` holds on the
prize prefixes and on the synthetic words. Even-length synthetic
`01` has density 0 and `D=0`; a single inserted repeat is an
isolated phase flip whose two even bursts still sum to `D=0`.

## Prize seed through `N=10^5`

| N | ones | D(N) | density | mean run | max run | even | odd ≥2 | len-1 | D even | D odd ≥2 | D len-1 | D defects | D alt | isolated |
|--:|-----:|-----:|--------:|---------:|--------:|-----:|-------:|------:|-------:|---------:|--------:|----------:|------:|---------:|
| 10 | 7 | 4 | 0.555556 | 1.6667 | 3 | 2 | 1 | 3 | 0 | 1 | 3 | 3 | 1 | 3 |
| 100 | 52 | 4 | 0.464646 | 2.1277 | 7 | 19 | 6 | 22 | 0 | 2 | 2 | 4 | 0 | 14 |
| 1000 | 481 | -38 | 0.527528 | 1.8939 | 10 | 168 | 80 | 280 | 0 | -6 | -32 | -39 | 1 | 117 |
| 10000 | 5032 | 64 | 0.501550 | 1.9936 | 13 | 1656 | 839 | 2521 | 0 | 19 | 45 | 63 | 1 | 1266 |
| 100000 | 50098 | 196 | 0.499675 | 2.0013 | 17 | 16644 | 8304 | 25020 | 0 | 34 | 162 | 195 | 1 | 12524 |

At `N=10^5`, defect density is `0.499675` (iid expects `1/2`), mean alternating-run length is `2.0013` (iid expects `2`), and `D(10^5)=196`. Every even-length burst contributes `0` to `D`. The signed sum is the leftover of odd-length runs (`34` from bursts of length ≥3, `162` from length-1 bits), 33324 odd runs in all. The bound `|D| <= 33324` is true and useless: those leftovers cancel down to 196, the same order as a random walk of that many ±1 steps, not a structured pairing.

The position split is the sharp statement. Alternating positions contribute `D_alt=1` (equal to `(σ_0 + σ_{N-1})/2`; the prize seed starts with 1 and the last bit is 1). Defect positions contribute `195`, which *is* `D` up to that endpoint. Pairing succeeds; sparsity does not.

Isolated phase flips are `12524` of the `49967` defects (density `0.125241`; iid expects `1/8 = 0.125`). The rest are clustered.

Run-length histogram at `N=10^5`:

| length | 1 | 2 | 3–4 | 5–8 | 9–16 | 17+ |
|:-------|--:|--:|----:|----:|-----:|----:|
| count | 25020 | 12456 | 9384 | 2891 | 216 | 1 |

The mass sits on lengths 1 and 2, as for iid bits
(`P(L=k)=1/2^k`: among 49968 runs one expects about 24984 of length 1 and 12492 of length 2;
the table has 25020 and 12456). Long period-2
bursts exist (Cycle I’s `L_run(0)=7` inside `tcap=128`; here
max run is 17 through `N=10^5`), but
they are rare and even the long even ones still contribute 0
only locally.

## Comparison to iid fair bits

| source | N | defect density | mean run | isolated density | `L(d)/n` |
|--------|--:|---------------:|---------:|-----------------:|---------:|
| iid expectation | — | 0.500000 | 2.0000 | 0.125000 | ~1/2 |
| iid PRNG (seed 20260910) | 100000 | 0.500015 | 1.9999 | 0.124621 | 0.500050 |
| prize centre | 100000 | 0.499675 | 2.0013 | 0.125241 | 0.499950 |

The prize centre is statistically indistinguishable from fair
bits on this screen: density stays near `1/2` at every
checkpoint from `N=10` through `N=10^5`, never dropping to the
kill threshold `1/4`.

## Berlekamp–Massey of the defect sequence

Defect bits `d_{t-1} = 1_{c_t == c_{t-1}}` for `t = 1, …, N`.
Training lengths match `experiment.py`’s centre BM checkpoints,
plus 4096. Copied BM agrees with `experiment.linear_complexity`
on a 64-bit prefix.

| train | `L(c)` | `L(c)/n` | `L(d)` | `L(d)/n` |
|------:|-------:|---------:|-------:|---------:|
| 100 | 48 | 0.480000 | 51 | 0.510000 |
| 1000 | 500 | 0.500000 | 500 | 0.500000 |
| 4096 | 2049 | 0.500244 | 2048 | 0.500000 |
| 10000 | 5001 | 0.500100 | 5001 | 0.500100 |
| 20000 | 10000 | 0.500000 | 9999 | 0.499950 |

At 20000 bits, `L(d)/n=0.499950` and `L(c)/n=0.500000`. Defects are as
irregular as `c`: a linear recurrence of order `o(N)` is not
hiding in the break sequence. (The same `L ~ N/2` profile is why
residue-class subsamples died in
`research/residue_discrepancy.md`.)

## Exhaustive small-`w` rows

Every nonzero initial word of support radius `w=0..6`
(`2^{2w+1}-1` states; `w=6` is 8191) evolved in a quiescent
background up to `tcap=8w+128`. Defect density of the centre
trace, as a check that finite rows are similar to the prize seed.

| w | states | tcap | mean density | median | min | max | mean of mean-run | max L_run | frac ≥ 1/4 |
|--:|-------:|-----:|-------------:|-------:|----:|----:|-----------------:|----------:|-----------:|
| 0 | 1 | 128 | 0.488189 | 0.488189 | 0.488189 | 0.488189 | 2.0317 | 7 | 1.0000 |
| 1 | 7 | 136 | 0.501587 | 0.496296 | 0.466667 | 0.525926 | 1.9817 | 8 | 1.0000 |
| 2 | 31 | 144 | 0.510264 | 0.510490 | 0.433566 | 0.566434 | 1.9546 | 10 | 1.0000 |
| 3 | 127 | 152 | 0.498775 | 0.496689 | 0.384106 | 0.589404 | 2.0046 | 13 | 1.0000 |
| 4 | 511 | 160 | 0.494738 | 0.496855 | 0.371069 | 0.591195 | 2.0212 | 15 | 1.0000 |
| 5 | 2047 | 168 | 0.495827 | 0.497006 | 0.365269 | 0.592814 | 2.0158 | 15 | 1.0000 |
| 6 | 8191 | 176 | 0.497806 | 0.497143 | 0.354286 | 0.622857 | 2.0082 | 24 | 1.0000 |

Mean densities sit in a tight band around `1/2`. The `w=0` line
is the prize seed at `tcap=128` (density already well above
`1/4`). Every scanned radius-`w` row has density `>= 1/4` (at
`w=6` the sparsest centre still has density `0.354`). No
finite-row exception makes the prize seed look atypical. The
Cycle I `L_run(6)=24` maximizer is a long *local* burst, not a
low-density trace: long even bursts still contribute 0 only on
their own support, and the rest of the centre is defect-rich.
The `max L_run` column reproduces the Cycle I table through
`w=6`.

## Why it died

Preregistered kill: density stays `>= 1/4` at `N=10^5`, or
defects have `L(N) ~ N/2` like `c`. Both fired. Period-2 pairing
does reduce `D` to the defect positions plus an `O(1)` endpoint,
but defect density is `Θ(1)`, of order `1/2`, so the `o(N)`
counting argument never starts. The defect sequence is not
simpler than `c`.

Not a prize claim. Eventual period 2 of the prize seed is a
different question (a single unbounded run, not a density); this
screen does not address it.

## Verdict

`KILL`, wall time 1.71s.

- Kill: yes.
- Survive: no.
- Reason: prize-seed defect density at N=10^5 is 0.499675 >= 1/4 (stays >= 1/4 at every checkpoint, min 0.464646); Berlekamp-Massey of the defect sequence at 20000 bits has L=9999 so L/n=0.5000 ~ 1/2, matching L(c)/n=0.5000. Even-length period-2 bursts contribute 0 to D, but they are not the bulk of the trace. Defects are as irregular as c. Not a prize claim.

## Files

- `research/period2_defects.md` (this note)
- `research/period2_defects.py` (`--certify` runs the checks, the
  prize-seed screen through `N=10^5`, and exhaustive `w<=6`)
- `research/period2_defects.json` (dump)

