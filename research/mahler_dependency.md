# Backward dependency of a diagonal Mahler query

Attack on prize problem 3 via the exact support recurrence of
[support_exact.md](support_exact.md) and [support_fast.md](support_fast.md).
No O(n) algorithm was obtained. Failure of this representation to compress
is not a lower bound for arbitrary algorithms, and is not a prize claim.

Experiment: [mahler_dependency.py](mahler_dependency.py).
It does not modify `support_exact.py`, `support_fast.py`, `strip_graph.py`,
`strip_extend.py`, or `experiment.py`.

## Machine model

The prize predicate (detailed announcement) asks whether some exact finite
machine satisfies `limsup T(n)/n < infinity`. The announcement allows a
Turing machine with binary input, CA cell updates, or CPU time, and does
not fix a word-RAM cost. The counts below are therefore stated in two
models; an O(n) claim would need both construction and evaluation in one
of them.

1. **Bit / multi-tape TM / transdichotomous RAM with word size Θ(log n).**
   A GF(2) operation on a bit costs O(1); an XOR of two N-bit strings
   costs Θ(N). Packed row updates of width Θ(n) cost Θ(n) bit operations
   each. This is the model in which an O(n) bound would actually refute
   the displayed predicate, and in which the naive spacetime simulation
   is Θ(n²).
2. **Unit-cost RAM on O(n)-bit words.** Here the packed recurrence
   `z ↦ z XOR ((z<<1) OR (z<<2))` is already n operations, hence O(n).
   That model is **not** used below: it would make the existing simulation
   a linear-time algorithm and would contradict the CA-cell-update reading
   (the light cone has Θ(n²) cells). [complexity.md](../complexity.md)
   already flags growing-integer Python operations as non-constant.

All circuit sizes are bit-gates over GF(2). O(n log n) in model 1 would be
progress but not a solution. An O(n) bound in model 1 for this sequence
would solve problem 3 in the negative (there is linear effort); none was
found, and none is announced.

## Recurrence and sound truncation

Write `a_{k,j} = [j ∈ S_k]`. The exact identity of `support_exact.md`, for
`j ≥ 1`, is

```
a_{k,j} = a_{k-1,j-1} + a_{k-2,j-1} + sum_{r OR s = j-1} a_{k-1,r} a_{k-2,s}
```

over GF(2), with `a_{k,j}=0` for `k<0`, `S_0={0}`, and `a_{k,0}=0` for
`k≥1`. The center bit is the subset zeta / Mahler evaluation

```
c_n = XOR_{j ⊆ n} a_{n,j} = Z_n(n),
```

where `Z_k(s) = XOR_{j ⊆ s} a_{k,j}`.

Two truncations are identically sound, not merely “for some queries”:

- **Min-support.** `min S_k ≥ ceil(k/2)` ([support_fast.md](support_fast.md)).
  Coefficients with `j < ceil(k/2)` are zero and may be dropped from the
  DAG. Verified on the untruncated supports through `k=24`: no contributing
  Mahler index at layer `n` falls below `ceil(n/2)`.
- **Cap.** `Inc` and bitwise OR never decrease an index, so indices `j>n`
  cannot feed a term `j ⊆ n`. They may be dropped when the query is `c_n`.

The contributing final indices are exactly the submasks of `n` that contain
the high bit `H = 2^{⌊log₂ n⌋}`: a submask omitting `H` is at most `H-1 < n/2`.
Thus `|Need[n]| = 2^{popcount(n)-1}` for `n>0`. At `n=2^m` this is 1 (the
test `2^m ∈ S_{2^m}` of `support_exact.md`). At `n=2^m-1` it is `2^{m-1}`.

The coefficient recurrence, the Mahler identity, and both truncations are
checked in `mahler_dependency.py` against packed Rule-30 evolution.

## Backward coefficient DAG

Start from `Need[n] = {j ⊆ n : j ≥ ceil(n/2)}`. For each `a_{k,j}` in the
closure, the linear terms request `j-1` at layers `k-1` and `k-2`, and the
OR-convolution at `m=j-1` requests every `r ⊆ m` that survives min-support
(taking `s=m` always gives a legal partner). This is an over-approximation
only in that some operands might cancel in a special identity for this
seed; it is exact as a *formal* circuit. Shared convolution is counted
separately below.

### First-step explosion

`H` is always in `Need[n]`. Decrementing it yields `H-1 = 2^m-1`, whose
submask lattice is `{0,…,H-1}`. After min-support, layer `n-1` already
contains every `r ∈ [ceil((n-1)/2), H-1]`.

- For `n=2^m`: that interval is the high half `{2^{m-1},…,2^m-1}`, size
  `n/2`.
- For `n=2^m-1`: `Need[n]` itself already has size `n/2`.
- For general `n`: `|Need[n]|` can be small when `n` is sparse, but the
  high-bit decrement still injects Θ(`H`) = Θ(`n`) operands at layer
  `n-1` once the other final submasks are included. Empirically
  `|Need[n-1]| ∈ [n/2, n/2+1]` on every sample with `n≤128`.

So every query, including the “sparse” power-of-two query, materializes
Ω(`n`) coefficients within one backward step. Sparse binary `n` does not
have sparse ancestry.

### Growth through `n=128`

`need_sum = Σ_k |Need[k]|` is the coefficient-DAG size. `possible_sum`
counts truncated slots `ceil(k/2) ≤ j ≤ n`. `fill = need_sum / possible_sum`.
`zeta_shared_sum` is the bit-gate count if each layer evaluates all
requested OR-convolutions by one subset-zeta on the covering cube.

| n | family | Need[n] | Need[n-1] | need_sum | fill | need_sum / n² | zeta_shared_sum |
|---:|---|---:|---:|---:|---:|---:|---:|
| 8 | pow2 | 1 | 4 | 37 | 0.607 | 0.578 | 176 |
| 10 | general | 2 | 5 | 57 | 0.626 | 0.570 | 360 |
| 15 | all-ones | 8 | 8 | 128 | 0.667 | 0.569 | 880 |
| 16 | pow2 | 1 | 8 | 137 | 0.631 | 0.535 | 984 |
| 31 | all-ones | 16 | 16 | 512 | 0.667 | 0.533 | 4768 |
| 32 | pow2 | 1 | 16 | 529 | 0.647 | 0.517 | 5024 |
| 63 | all-ones | 32 | 32 | 2048 | 0.667 | 0.516 | 23744 |
| 64 | pow2 | 1 | 32 | 2081 | 0.657 | 0.508 | 24352 |
| 100 | general | 4 | 50 | 5054 | 0.661 | 0.505 | 74752 |
| 127 | all-ones | 64 | 64 | 8192 | 0.667 | 0.508 | 112768 |
| 128 | pow2 | 1 | 64 | 8257 | 0.662 | 0.504 | 114176 |

Closed forms, matching the script on every sampled power of two `n≥2` and
every all-ones index:

```
n = 2^m (m≥1):   need_sum = n²/2 + n/2 + 1
n = 2^m - 1:     need_sum = (n+1)²/2
```

For `n=2^m`, layers `k < n` alternate in size between `n/2` and `n/2+1`;
only the query layer is a singleton. For `n=2^m-1`, every layer has size
exactly `(n+1)/2`. General `n` interpolates: `Need[n] = 2^{popcount(n)-1}`,
then the remaining layers fill consecutive intervals of length ~`n/2`.
The fill ratio approaches `2/3` of the truncated `(k,j)` rectangle, i.e.
construction is `~ n²/2` nodes, not `O(n)` or `O(n log n)`.

Unshared expansion of each convolution as `3^{popcount(m)}` AND–XOR pairs
is strictly worse (superlinear per layer at `m=n-1`). Sharing the
OR-convolution via subset zeta costs `Θ(q 2^q)` per layer with `2^q ~ n`,
total `Θ(n² log n)` bit operations — the same as, and no better than,
the forward truncated-zeta algorithm of `support_fast.py`, and worse than
packed CA simulation in model 1.

## Exact XOR cancellations: zeta queries collapse to `u(t,k)`

The value `Z_k(s)` does not need every coefficient in `Need[k]` if linear
combinations cancel. Over GF(2),

```
Z_k(s) = XOR_{t} M(s,t) Z_C(t),
```

where `C = a_{k-1} + a_{k-2} + (a_{k-1} ★_OR a_{k-2})`,
`Z_C(t) = Z_{k-1}(t) + Z_{k-2}(t) + Z_{k-1}(t) Z_{k-2}(t)`, and

```
M(s,t) = #{j ⊆ s : j≥1 and t ⊆ (j-1)}  (mod 2).
```

**Lemma.** For every `s≥1`, `M(s,t)=1` if and only if `0 ≤ t < s`.

Proof by induction on `s`. Write `s = 2^m + s'` with `s' < 2^m`. Submasks
split into those of `s'` and those `2^m+r` for `r ⊆ s'`. The XOR of Boolean
down-sets `↓(j-1)` over `j ⊆ s'`, `j≥1`, is `{0,…,s'-1}` by induction.
The term `j=2^m` contributes `↓(2^m-1) = {0,…,2^m-1}`. For `r ⊆ s'`,
`r≥1`, one has `↓(2^m+r-1) = ↓(r-1) ∪ (2^m + ↓(r-1))`, so those terms
XOR to `{0,…,s'-1}` XOR `{2^m,…,2^m+s'-1}`. The two copies of
`{0,…,s'-1}` cancel, leaving `{0,…,2^m-1} XOR {2^m,…,s-1} = {0,…,s-1}`.
Base `s=1` is `{0}`. □

Checked for every sampled `n≤128`: the Hamming weight of `M(n,·)` is
exactly `n`. There is **no** cancellation in the zeta expansion of the
query `Z_n(n)`: it depends on every `Z_C(t)` for `t < n`.

Consequently, for `k≥1` and `s≥1`,

```
Z_k(s) = XOR_{t=0}^{s-1} Z_C(t)
       = Z_k(s-1) + Z_{k-1}(s-1) + Z_{k-2}(s-1)
         + Z_{k-1}(s-1) Z_{k-2}(s-1),
```

with `Z_k(0)=0` (`k≥1`) and `Z_0(s)=1`. This is the original right-edge
rule

```
u(s,k) = u(s-1,k) XOR (u(s-1,k-1) OR u(s-1,k-2)),
```

because the Mahler formula is `u(t,k) = XOR_j a_{k,j} [j ⊆ t] = Z_k(t)`.
The script checks `Z_k(s)=u(s,k)` against the 2-adic row map of
[twoadic.md](twoadic.md), and checks that the `Z`-triangle reproduces
`c_n`, through `n=24`.

So preserving XOR cancellations and sharing the OR-convolution does not
produce a new compressed circuit. The exact zeta-query DAG **is** the
`u(t,k)` spacetime triangle. Min-support truncation is the statement
that `u(t,k)=0` for `k` too large relative to `t` in the coefficient
picture; it cuts about one third of the `(k,j)` rectangle and leaves a
half-triangle of Θ(n²) cells. Evaluating `c_n = Z_n(n)` still requires
the two previous `Z`-rows on `{0,…,n-1}` at every layer, i.e. Θ(n)
bits of state per layer and Θ(n) layers.

The prefix form `c_n = XOR_{t<n} (Z_{n-1}(t) OR Z_{n-2}(t))` is exact
and still bilinear: the pointwise products are not a function of the
two row-parities, so they do not collapse to O(1) state.

## Comparison of families

- **`n=2^m`.** The query is a single coefficient `a_{n,n}`. One decrement
  exposes the full `m`-bit cube. DAG size `n²/2 + n/2 + 1`. This is the
  combinatorially sparsest final layer and still quadratic overall.
- **`n=2^m-1`.** The query already asks for every index in `[2^{m-1}, 2^m-1]`.
  Every layer is saturated at size `2^{m-1}`. DAG size `(n+1)²/2`, the
  densest of the three families.
- **General `n`.** Final layer `2^{popcount(n)-1}`; within one step the
  occupancy joins the same `~ n/2` band. Ratio `need_sum/n² → 1/2` from
  above through `n=128`.

No family admits a uniform O(n) construction+evaluation bound in this
representation. Zeta-query occupancy is *larger* than coefficient Need
(the zeta argument is not min-support truncated), e.g. `zneed_sum=785`
versus `need_sum=529` at `n=32`.

## Why the attack died

The opportunity was to evaluate one parity without building every
truncated support. The obstruction is arithmetic increment vs the Boolean
lattice: `Inc` on the high-bit singleton produces an all-ones index, whose
OR-convolution is the full cube of width `⌊log₂ n⌋`. Exact GF(2)
cancellation in zeta space does not thin that cube; it rewrites the DAG
as the original CA. The only uniform saving is the already-known
min-support cut, which leaves `Θ(n²)` gates.

This is not a lower bound. A different encoding (Hashlife-style blocks,
a closed form for `S_n`, a small automaton for the diagonal, a conjugacy
that the 2-adic audit in [twoadic.md](twoadic.md) did not find, …) could
still be O(n) or o(n) in model 1. Nothing here rules that out. Nothing
here produces it either.

## What was obtained

- Sound truncated backward closure for `c_n`, with exact first-layer
  cardinalities and closed DAG sizes on the two dyadic families.
- Proof that `M(s,·)` is the numerical interval `{0,…,s-1}`, hence that
  the zeta-shared circuit is the `u(t,k)` triangle.
- Quadratic growth data through `n=128` in a stated bit-cost model.
- No O(n) algorithm, and no O(n log n) algorithm, from this attack.
