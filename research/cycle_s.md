# Cycle S: \(F^2\) lag-2 Condrey iteration, and \(11\)/\(00\) windows

Three attacks from [_astra_ideas16.md](_astra_ideas16.md). All three hit
their kill criteria. Not a prize claim.

Helper: `python3 research/cycle_s.py --certify`. Dump:
`research/cycle_s.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Uses `forced_right_traces` from
`research/period2_fiber.py` without modifying that file.

## 1. Lag-2 inverse of \(F^2\)

On every 32-cell neighborhood, the two-step centre is

\[
G_0=x_{-2}\oplus\bigl((x_{-1}\,\mathrm{XNOR}\,x_0)\land(x_1\lor x_2)\bigr).
\]

Flipping \(x_{-1}\) keeps \(G_0\) on 8 of 32 neighborhoods (lag 1 is
not permutive). Holding the even centre at \(0\) therefore determines
only column \(-2\), not the whole left. Choosing \(x_{-1}=1\) makes
the predicted \(x_{-2}\) identically \(0\), so there is no Condrey
horizon: a finite right can sit next to an even-time left neighbor
\(1\) and never force a 1 at lag 2.

On phase `01` the one determined bit is already in the vacuum fold.
For every finite right of width \(\le 6\) and \(T=64\),
\(x(2n,-2)=u_n=x(2n,1)\) (`n_fail=0` on 127 rights), and
`F_of_u` gives \(F_2=u_0\). That is `fold_bit`’s
`Fn[2]=un`, not a new closed form for \(F_4,F_6,\ldots\). Iterating
the lag-2 inverse is the existing \(F_k\) recurrence. **Killed.**

## 2. Spatial windows about \(11\) and \(10\)

Problem 2 is \(N_{11}-N_{00}=o(N)\). At each \(11\) pair, pack the
spatial window of radius \(r\le 8\) about the centre and ask whether
it determines the displacement to the next \(00\). At each \(10\)
transition, ask whether the same window determines the next \(0\)-run
length.

On \(N=2^{14}\) centre bits:

| \(r\) | windows at \(11\) | multi disp | windows at \(10\) | multi \(M\) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 2 | 2 | 2 |
| 2 | 8 | 8 | 8 | 4 |
| 4 | 128 | 80 | 128 | 17 |
| 8 | 3881 | 44 | 3869 | 1 |

Radius 8 still has collisions for both maps. A local spacetime rule
of radius \(\le 8\) does not pair \(11\) with \(00\). **Killed.**

Odd-time \(11\)s persist to the end of the window (`n_odd11=2095`,
`last_odd11=16345`). Finite evidence, not a production lemma.

## 3. Half-time right-edge gadget

A width-8 right-edge word at time \(\lfloor t/2\rfloor\) is inside the
light cone of \(c_t\). All 32 such words occur both with and without
an odd-time \(11\) at \(t\). Contemporaneous left-edge bits cannot
reach the centre (distance \(t\)). **Killed.**

## Verdict

`KILLED` (all three), wall time 0.13s. Prize unsolved.

## Files

- `research/cycle_s.md` (this note)
- `research/cycle_s.py`
- `research/cycle_s.json`
