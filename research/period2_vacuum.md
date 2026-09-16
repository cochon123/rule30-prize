# Period-2 L_0: eventual vacuum and sound onset

This note is a checked lemma plus a finite scan. It does not exclude
eventual period 2, and it does not claim a prize result.

Helper: `research/period2_vacuum.py --certify`. Dump:
`research/period2_vacuum.json`. Notation as in
`research/period2_left_edge.md`: after a time origin the center is
`c_{2n}=0`, `c_{2n+1}=1`, and `F_k(u_n,u_{n+1},\ldots)=x(2n,-k)` on
Fibonacci `u` (no consecutive 1s).

## Variable bound

By induction on the recurrences

```
F_k = G_{k-1} XOR (F_{k-1} OR F_{k-2}),
G_k = F_{k-1}(u_{n+1},\ldots) XOR (G_{k-1} OR G_{k-2}),
```

one has `max_index(F_k) <= floor((k-1)/2)` and
`max_index(G_k) <= floor(k/2)`. So `F_0,\ldots,F_K` are determined by
the `nvars(K) = floor((K-1)/2)+1` bits `u_0,\ldots,u_{nvars(K)-1}`.
Padding extra zeros past that index does not change those values.
For \(K\ge 3\), \(u_0\) is in fact absent (`research/period2_silent.md`).
For \(K\ge 8\), \(u_1\) is absent from every \(G_K\)
(`research/period2_gsilent.md`); in \(F_K\) it appears only as a
factor of \(u_1 u_3\) (`research/period2_u1u3.md`).

## Vacuum and the fold machine

The all-zero suffix of `u` produces

```
F_k = k mod 2,     G_0 = 1,     G_k = k mod 2 for k >= 1.
```

Call this pair *vacuum*. Folding a `0` onto vacuum yields vacuum.
Folding a bit `u_n` only writes `F_1 = 1 XOR u_n`; for `k >= 2` the
column recurrences do not mention `u_n` again. In the region where the
*suffix* `F` is already vacuum, the next window’s tail is a 16-state
machine on the 4-tuple `(F_{k-1}, F_{k-2}, G_{k-1}, G_{k-2})`. Every
state, at every parity of `k`, reaches the vacuum 4-tuple in at most 9
steps and stays there (`certify_fsm`). Therefore every fold, `0` or
`1`, preserves eventual vacuum, and the last disagreement with vacuum
increases by at most 11 columns.

## Lemma (eventually-zero `u`)

If `u` is eventually `0`, then `F_k` is eventually equal to `k mod 2`.
In particular `F_k = 1` for every large odd `k`, so `(F_k)` has no last
`1`. An `L_0` onset — `F_T = 1` and `F_k = 0` for all `k > T` — is
impossible.

Proof: a finite Fibonacci word is a finite sequence of folds applied to
vacuum. Each fold preserves eventual vacuum.

Jen/Kopra already forbid an eventually-zero even right neighbor for a
period-2 center (column `-1` becomes eventually constant). The lemma is
the same exclusion read on the left edge instead of on `u`.

The spatial identity `G_k = F_{k+1} XOR (F_k OR F_{k-1})` for `k >= 1`
is Rule 30 one step to the left; it is checked on Fibonacci strings in
the same certificate.

## What remains: infinitely many isolated 1s

If `u` has infinitely many 1s, the fold chain never starts at vacuum.
`L_0` is still a well-defined infinite system of polynomial equations
in the bits of `u`. A *sound* enumeration uses exactly `nvars(T+R)`
Fibonacci strings and asks whether `F_T=1` and `F_{T+1}=\cdots=F_{T+R}=0`.
That is a complete check for infinite `u`, because later bits do not
appear.

Every `T = 1,\ldots,28` dies at a finite `R` (longest survivor is
`T=20` with `R=16`, killed by `F_{37}` in the bounded-`nvars` scan).
`T=4` is identically `0`. The unbounded \(Q\)-forced continuation of
those six words 11-clips at \(n=18\) (`research/period2_qshift.md`);
`F_{37}` is the padding-zero artifact of refusing the clip. There is
no uniform-in-`T` bound in this table, so a period-2 regime that
starts only after a huge left-edge distance is not excluded. The
tail past `nvars(T)` is nevertheless unique:
`research/period2_lead.md` gives \(F_{2n+1}=u_n\oplus Q_n\).

If such a bound existed — a number `R_0` with no `T` and no Fibonacci
`u` satisfying `F_T=1` and `R_0` further zeros — then period 2 would
be impossible for every finite seed: at the first even time of the
regime the true spacetime is `L_0` with some finite `T`.
