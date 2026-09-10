# Period 9, isolated zero \(q=8\): \(011111111\)

**Status.** Not excluded. Jen/Kopra still do not fire for an eventual
center \(01^8\). This note does not claim a prize result.

Helper: `research/period9_q8.py`. Dump: `research/period9_q8.json`.
Uses `strip_graph.graph` / `components` / `analyze` and `strip_extend`
without modifying those files.

## What is proved (finite, machine-checked)

Write \(\sigma\) for the left-neighbor bit on the isolated \(0\) (phase
\(0\)). On the eight \(1\)s the left neighbor is locally forced:
\(0^7 1\). Algebraically \(\sigma=1\oplus r_0=1\oplus\) (bit \(4\) of
the last-\(1\) row at radius \(6\)). So:

- \(\sigma=1\) iff last-\(1\) bit \(4=0\), prefix `110001101`
  (the “good” wrap of `isolated_zero_uniform.md`);
- \(\sigma=0\) iff last-\(1\) bit \(4=1\), prefix `000111100`
  (the extra branch).

On any path that uses the forced \(1\)-run left bits, column \(-2\) is
a function of \(\sigma\) alone:

| \(\sigma\) | column \(-1\) | column \(-2\) |
|---:|:---:|:---:|
| \(1\) | `100000001` | `111111100` |
| \(0\) | `000000001` | `011111101` |

**Lemma (constant \(\sigma\) is Jen-excluded).** A recurrent path on
which \(\sigma\) is constant has columns \(-1\) and \(0\) both
eventually period \(9\). Kopra/Jen forbid that for every nonzero finite
seed. The only residual case is a path that *mixes* the two values of
\(\sigma\).

At radius \(6\) this mixing is not an artifact of two weakly linked
pieces. The unique residual SCC has \(186\) vertices (size \(14q+74\),
same formula as \(q\ge 9\)). Its phase-\(0\) slice has \(20\) rows,
six with \(\sigma=0\) and fourteen with \(\sigma=1\). The \(9\)-step
map on those \(20\) vertices is a single recurrent component containing
both labels, and the directed distance from a \(\sigma=0\) vertex to a
\(\sigma=1\) vertex is **one** period. Extra last-\(1\) rows and good
last-\(1\) rows reach each other inside the SCC.

All nine rotations of `011111111` give isomorphic radius-\(6\) graphs
(one residual SCC of size \(186\)). Time-shifting the center word does
not change the obstruction.

## What is only computational (sound over-approximations)

A genuine eventual \(01^8\) tail of a finite seed must occupy a
recurrent SCC of every finite-strip graph with free outer bits. If
every such SCC forced a periodic neighbor, Jen/Kopra would exclude the
word. They do not.

Independent `strip_graph.analyze` (unique residual SCC, graph period
\(9\), both values of \(\sigma\)):

| radius | residual size | elapsed |
|------:|--------------:|--------:|
| \(6\) | \(186\) | \(0.2\)s |
| \(7\) | \(328\) | \(1.0\)s |
| \(8\) | \(586\) | \(4.2\)s |
| \(9\) | \(916\) | \(204\)s |

Jen-pruned `strip_extend` through radius \(18\) (cap not hit): one
component, graph period \(9\), \(\sigma\in\{0,1\}\) at every radius,
last-\(1\) column \(-2\) still takes both bits. Sizes grow by a factor
about \(1.6\) per radius (\(91762\) states at radius \(18\)). No
collapse, no split, no forced neighbor.

**Left-only extension** from the radius-\(6\) residual (add left bits,
keep right radius \(6\), further-left still free). This is still a
sound over-approximation. Residual size stays \(186\) through left
radius \(10\), then grows slowly to \(461\) at left radius \(26\).
Both values of \(\sigma\) survive the whole way. Deepening the extra
prefix does not kill it once the further-left bit is free.

Left-deep prefix automata (width \(P=9,\ldots,15\), center at \(P-3\),
so right radius \(2\)) likewise keep a unique residual SCC with both
\(\sigma\) bits. Sizes \(51\) through \(78\).

## Constrained graphs that are *not* seed-applicable

These freeze an outer incoming bit to \(0\) for all time. That is
strictly stronger than a light-cone zero, which moves. Emptying them
does **not** exclude a finite seed.

- **Left \(0\)-wall.** Incoming further-left bit \(0\). Then the
  leftmost cell satisfies \(x_{t+1}=x_t\lor x_t^{\mathrm{next}}\), so
  it is nondecreasing and cannot lie on a cycle unless it is already
  constant. Checked widths \((L,R)\in\{(6,6),(8,6),(10,4),(10,6),(12,4)\}\):
  **no recurrent component at all**.
- **Right \(0\)-wall.** Incoming further-right bit \(0\). Widths
  \((6,6)\) and \((8,6)\): unique recurrent SCC with \(\sigma=1\) only
  (extra dies), neighbor forced, Jen-pruned. Width \((6,8)\): both
  \(\sigma\) bits still appear, but the right neighbor of the center is
  forced periodic, so the component is still Jen-pruned.

A moving light-cone search (`small_period_cert.light_cone_search`) for
onset \(T\le 11\) finds no unbounded period match (best finite match
\(19\) steps at \(T=11\)). That is a finite-onset check, not an
exclusion.

## Extra-only subgraph

Dropping every radius-\(6\) residual vertex with \(\sigma=1\) at
phase \(0\) or good last-\(1\) prefix still leaves a \(20\)-vertex
recurrent SCC. Those cycles have constant \(\sigma=0\), hence are
Jen-excluded by the lemma above. They are not the obstruction. The
obstruction is the mixed SCC, which uses both branches in one strongly
connected component.

## Strongest honest statement

For every integer radius \(6\le r\le 9\), and along the incremental
free-boundary extension through radius \(18\), and along left-only
deepening through \(26\) left bits at right radius \(6\): the strip
graph of \(01^8\) has a unique residual recurrent SCC of graph period
\(9\) in which the left neighbor of the isolated \(0\) takes both
values. Therefore this family of certificates does **not** exclude an
eventual center \(011111111\) for a nonzero finite seed.

The \(q=8\) exception at radius \(6\) is not an artifact of a small
width. It is mixing of two last-\(1\) prefixes that remain compatible
with free outer bits at every larger width checked. Fixed \(0\)-walls
kill the mixing, but they constrain the spacetime more strongly than a
finite seed allows.

## What this does not do

It does not exclude \(q\in\{1,2,3,4,5,6,8\}\). It does not force a
`00` or `11` in an eventual period. Isolated ones \(0^q 1\) remain a
separate family; \(q=8\) is also exceptional there.
