# Period-9 isolated zero: exhaustive finite rows

This note is a finite scan in the style of `research/period2_fiber.md`
experiment 1. It does **not** exclude an eventual centre \(01^8\) for a
nonzero finite seed, and it does not claim a prize result. Residual
strip SCCs for \(q=8\) remain as in `research/period9_q8.md`.

Helper: `research/period9_fiber.py`. Dump: `research/period9_fiber.json`.
Stdlib only. Does not modify `experiment.py`, `strip_graph.py`,
`strip_extend.py`, `period2_fiber.*`, or `period3_fiber.*`.

## Attack

Prove or kill the period-2 analog for the isolated-zero exception
`011111111` (period 9, \(q=8\)): every nonzero finite row of support
radius \(w\) has every exact period-9 isolated-zero centre run of length
at most some small constant, inside `tcap=8w+128`.

**Kill (eventual).** A finite nonzero row whose centre stays on a
rotation of \(01^8\) through the cap, or whose isolated-zero suffix
looks eventual (last break inside the light cone \(2w+8\), suffix at
least two periods).

**Kill (no analog).** \(L_{\mathrm{iso}}(w)\) grows through the scanned
radii with no terminal plateau. That kills the hope that \(q=8\)
behaves like period 2, where \(L_{\mathrm{run}}(w)=24\) for
\(6\le w\le 10\).

**Finite theorem.** \(L_{\mathrm{iso}}(w)\) plateaus at a small constant
and no row looks eventual.

Also record \(L_{\mathrm{any}}(w)\): longest exact period-9 centre run
whose repeating block is *any* primitive 9-bit necklace (504 such
words; 56 necklaces).

An exact period-9 run of length \(L\ge 9\) is a consecutive centre
factor whose repeating 9-block \(B\) has \(\min\)-period 9, and
\(c_{t}=B_{(t-s)\bmod 9}\) for \(t\in[s,s+L)\). Isolated-zero runs
restrict \(B\) to a rotation of `011111111`. A single 9-window counts;
confirming repetitions make \(L>9\).

## Packed Rule 30

Bit 0 is the leftmost cell. One step:

```
new = (row << 2) ^ ((row << 1) | row)
```

The centre at time \(t\) of a radius-\(w\) row is `(row >> (w+t)) & 1`.
This matches `experiment.center_bits` on a prefix of length 64, matches
the known 20-bit prize word `11011100110001011001`, and matches an
independent live-cell spacetime on the prize seed and on sampled small
rows. Window-scan run lengths match a brute-force scan on those traces
and on synthetic \(01^8\) factors.

## Exhaustive finite rows

Every nonzero initial word of support radius \(w=0..7\)
(\(2^{2w+1}-1\) states; \(w=7\) is \(2^{15}-1=32767\)) is evolved in a
quiescent background up to `tcap=8w+128`. No row is eventual in the cap
(isolated-zero suffix \(\ge 18\) with last break \(\le\max(2w+8,18)\)),
so none is a genuine eventual witness. A few late bursts *touch* tcap
with suffix 19–23; doubling the cap does not extend them.

| `w` | states | `tcap` | `L_iso` | `L_any` | `L_prefix_iso` | `L_suffix_iso` | `L_iso>4w+16` |
|----:|-------:|-------:|--------:|--------:|---------------:|---------------:|--------------:|
| 0 | 1 | 128 | 0 | 13 | 0 | 0 | 0 |
| 1 | 7 | 136 | 10 | 15 | 0 | 9 | 0 |
| 2 | 31 | 144 | 11 | 18 | 0 | 0 | 0 |
| 3 | 127 | 152 | 14 | 19 | 0 | 0 | 0 |
| 4 | 511 | 160 | 17 | 23 | 0 | 16 | 0 |
| 5 | 2047 | 168 | 17 | 25 | 9 | 12 | 0 |
| 6 | 8191 | 176 | 19 | 25 | 11 | 19 | 0 |
| 7 | 32767 | 184 | 23 | 27 | 16 | 23 | 0 |

The prize seed (`w=0`) has `L_iso=0` inside `tcap=128`: it contains no
9-bit rotation of `011111111` in that window. Its longest any-necklace
period-9 run has length 13, block `010101101`, starting at time 50.
(Past the declared cap, the prize seed’s first isolated-zero 9-window
is at \(t=128\), and through time 512 the longest isolated-zero run is
still only 10.)

Isolated-zero maximizers, LSB = spatial \(-w\):

| `w` | row | `L_iso` | start | block |
|----:|-----|--------:|------:|-------|
| 1 | `100` | 10 | 115 | `110111111` |
| 2 | `11110` | 11 | 124 | `111111011` |
| 3 | `1000000` | 14 | 117 | `101111111` |
| 4 | `100110010` | 17 | 141 | `111011111` |
| 5 | `01001100100` | 17 | 141 | `111011111` |
| 6 | `1010100010000` | 19 | 155 | `101111111` |
| 7 | `000000100110001` | 23 | 161 | `111111110` |

The \(w=5\) maximizer is the \(w=4\) row padded by a 0 on each side, so
the apparent stall \(L_{\mathrm{iso}}(4)=L_{\mathrm{iso}}(5)=17\) is
zero-padding, not a plateau. Radius 6 and 7 produce strictly longer
runs. Doubling tcap on each maximizer does not lengthen the run.

Rows with an isolated-zero factor of length \(\ge 18\) (at least two
periods): none for \(w\le 5\), then 23 at \(w=6\) and 120 at \(w=7\).
Prefixes of \(01^8\) from time 0 are 0 through radius 4, then 9, 11, 16.
No scanned row has an isolated-zero run longer than \(4w+16\).

Least squares over the table gives \(L_{\mathrm{iso}}\approx 2.70\,w+4.42\)
and \(L_{\mathrm{any}}\approx 2.06\,w+13.4\). Those are summaries of a
still-rising table, not a bound.

## Verdict

`KILL` of the period-2 analog, wall time 2.36s.

- Eventual isolated-zero witness: **no**.
- Finite theorem / plateau: **no.** \(L_{\mathrm{iso}}(w)\) is
  \(0,10,11,14,17,17,19,23\) with a new record at \(w=7\).
- Survive: no.
- This does **not** exclude \(q=8\) for a finite seed. A growing
  finite-row table without an eventual witness leaves the residual
  mixing-\(\sigma\) SCC of `period9_q8.md` untouched.

Period 2 had a plateau \(L_{\mathrm{run}}=24\) on five consecutive
radii. Isolated-zero period 9 does not, at any radius in \(0..7\).
The same exhaustive method therefore does not give a finite theorem
for \(q=8\).

## What this does not do

It does not exclude an eventual centre `011111111` for any finite seed.
It does not bound \(L_{\mathrm{iso}}(w)\) independently of \(w\). A
radius-8 row with a much longer isolated-zero burst is not excluded; the
growth already visible at \(w=7\) is the point. It does not touch
periods 3–7, isolated ones, or the unique-left fiber of Condrey. It is
not a strip-graph argument.

## Files

- `research/period9_fiber.md` (this note)
- `research/period9_fiber.py` (checks and the radius-`w` exhaustive)
- `research/period9_fiber.json` (dump)
