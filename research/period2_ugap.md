# Period-2 even neighbor: no five consecutive zeros

Checked lemma on the even right neighbor of a period-2 centre, phase
`01`. It restricts the Fibonacci subshift that `L_0` quantifies over. It
does **not** exclude eventual period 2: three of the six Fibonacci
`T=20`, `R=16` last-sat words are ugap-legal and remain last-sat
(`research/period2_ugap_sat.md`). Not a prize claim.

Helper: `python3 research/period2_ugap.py --certify`. Dump:
`research/period2_ugap.json`. Uses `forced_right_traces` from
`research/period2_fiber.py` and the 2-step identities of
`research/period2_neighbor.md`.

## Lemma

Assume `c_{2n}=0`, `c_{2n+1}=1` for all `n` in the regime. Write
`u_n=x(2n,1)`, `e_n=x(2n,2)`, `f_n=x(2n,3)`, `g_n=x(2n,4)`,
`h_n=x(2n,5)`. Then `u` has no five consecutive zeros.

Proof. The two-step update with forced centre is left-permutive of lag 2
at the origin, but on columns `1,2,3` it closes after reading `g,h`. The
complete 16-row table with `u=c=0` at an even time is:

| `(e,f)` | `g,h` | `u'` | `(e',f')` |
| --- | --- | --- | --- |
| `00` | any | `1` | (vacuum identity) |
| `01` | any | `0` | `10` |
| `10` | any | `0` | `00` |
| `11` | `00` | `0` | `00` |
| `11` | not `00` | `0` | `01` |

While `u` stays 0, `(e,f)` therefore walks on the acyclic graph

```
11 → 01 → 10 → 00  (exit: next u is 1),
11 → 00  (exit next).
```

No self-loop, and `11` has no predecessor in this graph. The unique
longest path has four vertices, hence four consecutive even times with
`u=0`. The fifth bit is 1. Neighborhood radius 2 over two steps reaches
only through column 5, so extra right-hand bits cannot add an edge.

Together with “no consecutive 1s” (`research/period2_neighbor.md`) every
even-right sequence compatible with a period-2 centre — finite or
infinite right — lies in the subshift of finite type forbidding
`{11, 00000}`. Infinitely many 1s still follow from Jen (an eventually
zero `u` makes column `-1` eventually constant).

## What this does not do

The `T=20` last-sat `L_0` words of `research/period2_certificate.md`
share the period-3 tail `00010010010001` (max zero run 3), but three of
the six prefixes contain a leading zero-run of length 5, 6, or 7 and
are illegal in this SFT. The other three remain last-sat at `R=16`.
Restricting onset search to ugap therefore does not kill `R=16` and
does not supply a uniform `R(T)` (`research/period2_ugap_sat.md`).
Random words in the SFT have `F`-zero runs of length at most 12 in a
short sample; that is not a bound.

`F^2` is left-permutive of lag 2 (flipping `x_{-2}` always flips the
even-time centre) but not of lag 1 (4 of 16 neighborhoods keep `G_0`
when `x_{-1}` flips). Kopra width 1 for `F^2` is false, so even-time
constancy of the prize centre is not Kopra-forbidden by that route.

## Finite-right check

Every nonzero-or-empty right of width `≤8` evolved with a forced
phase-`01` centre through time 240 has `u`-zero-run `≤4`, and  the
bound is attained (vacuum hits 4). This is a corollary of the table,
not an independent census.

## Verdict

`LEMMA`, wall time <1s.

- Kill of period 2: no.
- New uniform constraint on `u`: yes, max zero run 4.
- `F^2` width 1: killed.

## Files

- `research/period2_ugap.md` (this note)
- `research/period2_ugap.py`
- `research/period2_ugap.json`
- `research/period2_ugap_sat.md` (onset table inside this SFT)
