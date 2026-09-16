# Period-2 L_0: shift germs, identities, no descent

Attack on the uniform-in-`T` bound for left-edge onsets. Cycle D already
had the two-zero lemma and the observation that `S` sends a long `L_0`
to a length-2 bump. This note records the complete `R≥4` identity, checks
that neither Hamming weight nor last-1 is a rank on that bump, and
extends the sound onset table by two widths. It does **not** exclude
eventual period 2, and it is not a prize claim.

Helper: `python3 research/period2_germ.py --certify`. Dump:
`research/period2_germ.json`. Notation as in
`research/period2_vacuum.md` and `research/period2_certificate.md`.

## Target

An `L_0` onset of width `T` is a Fibonacci even-right-neighbor `u` with
`F_T(u)=1` and `F_k(u)=0` for all `k>T`. Compactness gives a finite
killing `R(T)` once that infinite tail is unsatisfiable. A uniform
`R(T)≤R_0` would exclude every onset, hence (with the eventual-vacuum
lemma) period 2 for every finite seed. Through `T=32` the worst is still
`T=20`, `R=16`. The hope was that the bump produced by `S` decreases a
rank until it hits the identically zero column `F_4`.

## Identities (algebraic)

Work on any `u` for which the spatial identity
`G_k=F_{k+1}⊕(F_k∨F_{k-1})` (`k≥1`) and the fold
`G_k(u)=F_{k-1}(Su)⊕(G_{k-1}∨G_{k-2})` hold; both are already certified
on the Fibonacci variety.

**Lemma (L_0 to 011-bump).** Suppose `F_T=1` and
`F_{T+1}=F_{T+2}=F_{T+3}=F_{T+4}=0` (so `R≥4` and `T≠4`). Then

```
G_T = G_{T+1} = 1,     G_{T+2} = G_{T+3} = 0,
F_T(Su) = 0,           F_{T+1}(Su) = F_{T+2}(Su) = 1.
```

If also `F_{T+5}=0`, then `F_{T+3}(Su)=0`.

Proof. Spatial reconstruction gives
`G_T=0⊕(1∨F_{T-1})=1`,
`G_{T+1}=0⊕(0∨1)=1`,
`G_{T+2}=0⊕(0∨0)=0`,
`G_{T+3}=0`.
Fold at `k=T+1`: `1=F_T(Su)⊕(1∨G_{T-1})`, hence `F_T(Su)=0`.
At `k=T+2`: `0=F_{T+1}(Su)⊕(1∨1)`, hence `F_{T+1}(Su)=1`.
At `k=T+3`: `0=F_{T+2}(Su)⊕(0∨1)`, hence `F_{T+2}(Su)=1`.
At `k=T+4` with one more zero: `G_{T+4}=F_{T+3}(Su)` and
`G_{T+4}=F_{T+5}⊕(F_{T+4}∨F_{T+3})=0`.

So a long `L_0` at `T` becomes, after one shift, a length-2 bump
`011` at the *same* columns `T,T+1,T+2`, followed by zeros. The column
index does not decrease. The bump overlaps the identically zero `F_4`
only for `T∈{2,3}`, which are already excluded.

Checked on every Fibonacci string of length `nvars(T+6)` for
`5≤T≤14`, `T≠4`: 20 `L_0` germs with at least four zeros, 0 failures
(`identities.n_fail=0`).

## No rank

On every last-sat model of `(T,R)∈{(8,9),(16,9),(20,16),(22,12)}`:

- ones in the window `[T,T+R]` never decrease under `S` (they increase
  on all 18 models);
- last 1 of `F(Su)` decreases on the four `T=16` models, stays on the
  six `T=20` models, and increases on `T=8` and `T=22`.

The `T=20` chain is typical: `L_0` → `not1` (`11…`) → `B0` → `B0` →
short `L_0` tail → `B0`, with the 1s spreading right, not draining.
Cycle D’s obstruction stands: a zero run of length `R` does not
transfer to `Su` with a loss that can reach vacuum in
`nvars(T+R)≈(T+R)/2` shifts.

The tail itself is unique given the onset prefix:
`research/period2_lead.md` proves \(F_{2n+1}=u_n\oplus Q_n\), so
\(F_k=0\) for \(k>T\) forces \(u_n=Q_n\) for all
\(n>\lfloor(T-1)/2\rfloor\). The \(T=20\) models already follow that
continuation. On the same tail, `research/period2_qshift.md` gives
the one-step identity \(Q_n(u)=Q_{n-1}(Su)\) whenever \(2n-3>T\);
it does not iterate under \(S\) because \(Su\) is the bump above,
not a smaller \(L_0\). The bump itself is \(B_0\) of run \(R-4\), and
`research/period2_b0.md` records that \(S\) then sends \(B_0(S,R)\) to
\(B_0(S+2,R-4)\) with \(G_S=0\). Finite extra zeros descend; an
infinite tail does not.

## Onset table

Sound enumeration, exact variable bound. New rows:

| `T` | `maxR` | `n` at max | killed by |
|----:|-------:|-----------:|----------:|
| 33 | 14 | 5 | `F_48` |
| 34 | 12 | 5 | `F_47` |

Together with Cycle D’s table through `T=32`, every onset width
`1≤T≤34` dies at finite extra `R`, and `maxR≤16` still, uniquely at
`T=20`. This is not a proof that `R≤16` for all `T`. Widths `≥35` were
not enumerated: `nvars(T+16)` is already 26 at `T=35` (`F_27` Fibonacci
strings).

## Vacuum `u` is not eventually period 7

`research/period2_fiber.md` previously stated that the driven vacuum
right, phase `01`, has `u=01` then `(0001010)^∞` from index 2. That
attractor is only a transient. Gaps of 1s in vacuum `u` are `4,2` then
`(5,2)` repeating until even-time index `n=152` (`T=400` is enough to
see the break; the first non-`(5,2)` gap is 3). After that the gap
language is `{3,5}` and Berlekamp–Massey length of the spatial left
stays `~T/2`. The unique left of the vacuum fiber is empirically
infinite (`last1=T-O(1)` through `T=512`); there is still no closed
form. Periodic `u` is already Jen-excluded, so a broken period-7
attractor would not have given a prize lemma in any case.

## What is proved, what is not

Proved: the `R≥4` identity above; no ones-window or last-1 rank on the
listed last-sat models; sound `L_0` death at `T=33,34` with `maxR≤14`.

Not proved: a uniform `R(T)`; well-founded reduction of `L_0` under
`S`; unique-left infinitude for every finite right; eventual period 2
of the prize seed.

The unique-left-is-infinite statement for a prescribed period-2 centre
and a finite right is the same `L_0` problem read at time 0
(`L_k=F_k(u)` for the driven even-right `u`). Vacuum is one realizable
`u`, not a bypass.

## Verdict

`NO_DESCENT`, wall time 30s for the identity/rank/T=33–34 certificate.

- Kill of the bump-rank route: yes.
- Survive of a uniform `R≤16`: no.
- Witness: none.
- Worst onset remains `T=20`, `R=16`.

## Files

- `research/period2_germ.md` (this note)
- `research/period2_germ.py`
- `research/period2_germ.json`
