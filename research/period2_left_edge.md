# Period-2 left edge: identities, SAT, remaining gap

Shift so a hypothetical period-2 center has `c_{2n}=0`, `c_{2n+1}=1`.
The even right neighbor is `u_n=x(2n,1)`, with no consecutive 1s
(`research/period2_neighbor.md`). Odd right bits `v_n` do not appear in
any left column: brute-forced through width 10 against all Fibonacci
`u`-strings of length 6 (`verify_v_independence`). The inverse also
round-trips on the real seed (`verify_against_forward`). ANFs match
direct reconstruction (`poly_vs_recon`).

WLOG this phase: any period-2 tail can be shifted by at most one step
so the first even time has center 0. That shift increases the left-edge
distance `T` by at most 1.

## Column polynomials

Write `F_k` for `x(2n,-k)` and `G_k` for `x(2n+1,-k)` as ANFs in
`u_n,u_{n+1},...`, reduced modulo `u_i u_{i+1}=0`.

```
k   F_k                         G_k
0   0                           1
1   1+u0                        1
2   u0                          u1
3   1+u1                        1+u1
4   0                           u2
5   1+u1+u2                     1+u1
6   u2                          u1+u2+u3
```

Unreduced, `F_4=u_0 u_1`. On every legal `u` this vanishes.

**Lemma.** For every `n` large enough that the period-2 regime has
begun, `x(2n,-4)=0`.

Proof: `F_4=u_n u_{n+1}=0`.

## Immediate onset exclusions

At the start of the regime the leftmost 1 is at column `-T`, with zeros
strictly to its left. Need `x(0,-T)=1`.

* `T=4`: `F_4=0`, so the onset bit is identically 0. Impossible.
* `T=2`: `F_2=u_0` forces `u_0=1`, while `x(0,-3)=F_3=1+u_1=0` forces
  `u_1=1`, contradicting no consecutive 1s. Continuation through even
  time `s=2` also asks for column `-4` as the moving edge (`T+s=4`)
  and hits the same identity.
* `T=0` is not an `L_0` onset in this phase: the “edge” is the center,
  which is 0.

On-demand SAT (assign `u` bits only as the inverse reads them; no
length cap) for the stronger `L_0` chain
`x(s,-(T+s))=1` and `x(s,-(T+s)-1)=0` for `s=0,1,...,tmax`:

| T | max `tmax` |
|--:|----------:|
| 1 | 2 |
| 2 | impossible |
| 3 | 0 |
| 4 | impossible |
| 5 | 1 |
| 6 | 1 |
| 7 | 0 |
| 8 | 4 |
| 9 | 2 |
| 10–12 | 0 |
| 13–14 | 1 |
| 15 | 0 |
| 16 | 1 |

The longest survivor is `T=8` for five times (`s=0..4`), then the edge
fails at `s=5`. Independent Fibonacci enumeration with 18-bit prefixes
agrees through `T=12`.

## What is proved, what is not

Proved: the `F_4` identity; `v`-independence of left reconstruction;
impossibility of onsets `T=2` and `T=4`; machine-checked finite lifetime
of every `L_0` chain for `1 <= T <= 16`.

**Eventual vacuum** (`research/period2_vacuum.md`): if `u` is eventually
`0`, then `F_k` returns to `k mod 2` after a finite disagreement (every
4-bit tail state absorbs in `<= 9` columns). So `F` has infinitely many
`1`s and cannot be `L_0`. This is the left-edge form of the already-known
Jen exclusion of eventually-zero `u`.

**Sound onset scan** (exactly `nvars(T+R)` Fibonacci strings, valid for
infinite `u`): every `1 <= T <= 28` has a finite extra `R` that makes
`F_T=1` and `F_{T+1..T+R}=0` unsatisfiable. Longest is `T=20` with
`R=16`, killed by `F_{37}`.

Not proved: a uniform bound for all `T`. Eventual period 2 on the prize
seed would have large `T` (the left edge is already at `-T`). A lifetime
that stayed `O(1)` for all `T` would finish period 2; the table is
consistent with that but is not a proof.

Helper: `research/period2_left_edge.py`. Vacuum/onset certificate:
`research/period2_vacuum.py`.
