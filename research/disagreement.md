# Disagreement/front audit for a hypothetical period-2 center

Write the Rule 30 update as

```
F(x)_j = x_(j-1) XOR (x_j OR x_(j+1)).
```

For two configurations `a,b`, let `e_j=a_j XOR b_j` and define
`h_j=(a_j OR a_(j+1)) XOR (b_j OR b_(j+1))`. Then the disagreement update is

```
e'_j = e_(j-1) XOR h_j.
```

Over GF(2), with `a=b+e`, the nonlinear term is explicitly

```
h_j = e_j + e_(j+1) + b_j e_(j+1) + b_(j+1)e_j + e_j e_(j+1).
```

Therefore disagreement does not obey an autonomous linear light-cone rule; its propagation depends on the reference configuration `b` and can cancel.

If `a=F^2(b)` and the center sequence of `b` has period 2, then `e(t,0)=0` at every time. The inverse/left-permutive relation quoted in the main analysis,

```
e(t,-1) = (1 + c_t)e(t,1),
```

is consistent with erasure rather than contradiction: on phases with `c_t=1`, it forces the left neighbor disagreement to zero regardless of the right disagreement. A leftmost mismatch can consequently move through the cone while the center channel remains zero.

## Explicit counterexample to a purely causal contradiction

Take the bi-infinite spatially periodic configuration with period 7,

```
...0100110 0100110 0100110...
```

using index 0 at the first displayed 0. Exact evolution on one period gives:

```
t   b_t       F^2(b_t)  e= b_t XOR F^2(b_t)   center
0   0100110   0000001   0100111                 0
1   1111101   1000011   0111110                 1
2   0000001   0100110   0100111                 0
3   1000011   1111101   0111110                 1
```

The center is exactly period 2, so `e(t,0)=0` for all `t`, yet `e(t,·)` is nonzero at every phase. This is a valid Rule 30 orbit (periodic boundary is only a compact way to display a bi-infinite configuration), and it disproves any argument that center period-2 agreement alone forces `F^2(b)=b` by finite-speed propagation.

The counterexample does not settle the prize instance, whose initial configuration is one finite seed. It shows that a successful front proof must use special one-seed boundary/left-edge information in an essential way. Causality and the center constraint alone are insufficient; the nonlinear cancellation terms permit persistent off-center disagreement.
