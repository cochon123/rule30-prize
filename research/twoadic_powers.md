# Power-of-two iterate experiment

I computed the row map modulo (2^{512}),

```
f(z) = z XOR ((z << 1) OR (z << 2)),
```
and sampled (f^t(1)\mathbin{\operatorname{XOR}}1) at (t=2^a). The 512-bit modulus is sufficient for the listed valuations (all are below 512), so these are exact 2-adic low-bit valuations.

```
t          1  2  4  8  16 32 64 128 256 512 1024 2048 4096 8192
v2(f^t(1) XOR 1)
           1  3  4  6   7  9 15  16  24  25   27   29   34   36

t          16384 32768 65536 131072 262144 524288 1048576
v2(...)        37    39    41     43      48      49      51
```

The growth is irregular and does not follow the linear valuation law expected from a literal translation (z\mapsto z+c) (or a simple affine map). In particular, at the first steps (f(1)=7) gives valuation 1, while (f^2(1)=25) gives valuation 3. This is only negative evidence: a nonlinear 2-adic coordinate change could in principle conjugate a map with irregular valuations to another map, and the independent finite-quotient cycle failure already rules out an adding-machine conjugacy for the natural residue filtration.

For the Rule 30 target, the center bit at time (t) is bit position (t) of (f^t(1)). Therefore the sampled valuations probe only the low bits of the same iterate; they do not determine the diagonal bit. A fast-doubling strategy would need a compact description of (f^{2^a}) valid at bit position (2^a). The local rule has dependency radius 2, so (f^{2^a}) has radius (2^{a+1}). No bounded-size composition invariant appeared in these calculations; the valuation data does not establish a formal representation lower bound either.

The computation was an exact integer recurrence reduced modulo (2^{512}) after each step, requiring (2^{20}) iterations. It is a diagnostic for possible 2-adic translation structure, not a solution or lower-bound proof.
