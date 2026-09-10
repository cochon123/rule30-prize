# Automaton sections along the query ray

Attack on prize problem 3: treat the integer row map as a 3-state
automaton group and try to evaluate one diagonal bit by compressed
wreath arithmetic along a single input ray. No O(n) or O(n log n)
algorithm was obtained. Failure of this representation to compress is
not a lower bound for arbitrary algorithms, and is not a prize claim.

Certifier: `research/automaton_sections.py`.
It does not modify `strip_graph.py`, `strip_extend.py`, or
`experiment.py`.

The wreath-recursion language is that of automaton groups (e.g. the
GAP package AutomGrp). The 3-state machine is the same local rule as
the forward direction of the inverse transducer in
[ancestry_transducer.md](ancestry_transducer.md), not a retread of
that DFA cascade, and not the Mahler DAG of
[mahler_dependency.md](mahler_dependency.md).

## Machine model

Same two models as [mahler_dependency.md](mahler_dependency.md). An
O(n) claim would have to live in model 1.

1. **Bit / multi-tape TM / transdichotomous RAM with word size Θ(log n).**
   Rewriting one generator letter costs O(1). A wreath section of a
   word of length L costs Θ(L). Packed iteration of
   `z ↦ z XOR ((z<<1) OR (z<<2))` is Θ(n) bit operations per row and
   Θ(n) rows, i.e. Θ(n²). This is the model in which an O(n) bound
   would refute the displayed prize predicate.
2. **Unit-cost RAM on O(n)-bit words.** Already makes the packed
   recurrence n operations, hence O(n). Not used below.

O(n log n) in model 1 would be progress, not a solution. None was
found. Exponent arithmetic on O(log n)-bit integers is counted; it is
not the bottleneck.

## The 3-state wreath recursion

Bits are read least-significant first. The three states remember
whether the previous two input bits are `00`, `01`, or `1*`:

```
A = (A, C)
B = (A, C)σ
C = (B, C)σ
```

with A = f the row map, and σ the transposition of the current bit.
Composition is `(gh)(x) = g(h(x))`, so

```
(gh)|_x = g|_{x ⊕ ε(h)} · h|_x,     ε(gh) = ε(g) ⊕ ε(h),
```

where ε is the root permutation (activity): ε(A)=0, ε(B)=ε(C)=1.
Generator sections are length 1:

```
A|_0=A,  A|_1=C,     B|_0=A,  B|_1=C,     C|_0=B,  C|_1=C.
```

The machine is invertible and noncontracting: `A^m|_0 = A^m` for every
m, and A has infinite order (if `A^k = id` then `A|_0 = A` forces
`A = id`). Any useful compression must therefore concern the actual
query ray, not a finite nucleus.

## The query

For n ≥ 1 the prize bit is bit n of `f^n(1)`. The seed 1 is the ray
`10^∞`. Because A does not flip the first bit,

```
A^n|_1 = C^n.
```

The remaining input is n−1 zeros, and the next output bit on input 0
is the activity of the remaining section:

```
c_n = ε(A^n | 10^{n-1}) = ε(C^n | 0^{n-1}).
```

Checked against packed Rule 30 through n=48. Also `A^n` acts as `f^n`
on integers (checked through n=19 on a window wide enough for the
light cone).

## Proved section identities (arbitrary m)

Write products left-to-right with the rightmost generator applied
first. All identities are the wreath formula for powers, proved by
induction on m from the 3-state tables. The certifier expands
`X^m` as a word and checks equality of sections through m=16, and
checks the compressed Periodic form against that expansion through
n=24.

**Powers of generators.**

```
A^m |_0 = A^m
A^m |_1 = C^m

B^m |_0 = (CA)^{m/2}                 if m even
        = A (CA)^{(m-1)/2}           if m odd
B^m |_1 = (AC)^{m/2}                 if m even
        = C (AC)^{(m-1)/2}           if m odd

C^m |_0 = (CB)^{m/2}                 if m even
        = B (CB)^{(m-1)/2}           if m odd
C^m |_1 = (BC)^{m/2}                 if m even
        = C (BC)^{(m-1)/2}           if m odd
```

Equivalently: `C^m|_0` (resp. `C^m|_1`) is the unique length-m
alternating word in {B,C} that ends in B (resp. C). Same for B^m in
{A,C}, ending in A (resp. C).

**Two-letter powers.**

```
(BC)^m |_0 = (CB)^m
(BC)^m |_1 = (AC)^m

(CB)^m |_0 = (CA)^m
(CB)^m |_1 = (BC)^m
```

These follow because ε(BC)=ε(CB)=0, so `w^m|_x = (w|_x)^m`, together
with `(BC)|_0 = CB`, `(BC)|_1 = AC`, `(CB)|_0 = CA`, `(CB)|_1 = BC`.

**General power.** For an arbitrary block w, writing e for the
exponent:

```
if ε(w)=0:   w^e |_x = (w|_x)^e
if ε(w)=1, e even:   w^e |_x = (w|_{x⊕1} · w|_x)^{e/2}
if ε(w)=1, e odd:    w^e |_x = (w|_x) · (w|_{x⊕1} · w|_x)^{(e-1)/2}
```

(the odd case written so the rightmost factor is `w|_x`). In
particular, a 1-activity block **doubles its period** and halves its
exponent. That is the only rewrite used below.

The next two-letter family that appears on the ray has ε(CA)=1 and

```
(CA)|_0 = BA,     (CA)|_1 = C^2,
```

hence for even k

```
(CA)^k |_0 = (C^2 BA)^{k/2} = (CCBA)^{k/2}.
```

Checked as an instance of the general power formula through m=11,
together with (AC)^m, (BA)^m, (AB)^m.

## Attempted grammar

A candidate compressed form is `prefix · block^e · suffix` in the
semigroup {A,B,C}*, closed under the power-section rewrite above.
Squaring is cheap: `C^{2m}` has wreath

```
C^{2m} = ((CB)^m, (BC)^m)
```

(ε=0). Binary exponentiation therefore gives an SLP of size Θ(log n)
for `C^n`, **before** walking the ray.

Walking n−1 zeros is not cheap. For the family n=2^m the compressed
forms begin

```
k=0:  C^n
k=1:  (CB)^{n/2}
k=2:  (CA)^{n/2}
k=3:  (CCBA)^{n/4}
```

and then the 1-activity substitution `w ↦ w|_1 w|_0` (or the
length-preserving recoding `w ↦ w|_0` when ε(w)=0) produces blocks

```
C,  CB,  CA,  CCBA,  CBCCBCAA,  CACBCBAA,  CCBCBCCCBACACAAA,  …
```

of lengths 1,2,2,4,8,8,16,… . After Θ(log n) steps the exponent is 1
and the block has length n. The remaining n−Θ(log n) zeros recode a
length-n word, one generator per site per step.

An SLP product construction (each node sectioned at both letters)
does not save this. For n=16 the SLP sizes along the ray start
`5,7,7,16,33,33,66,127,…` and finish at 209, already larger than the
expanded word; the sum of SLP sizes is 1831 against expanded cost
n²=256.

There is no finite family of block types closed under `|0` on this
ray: the substitution iterates have unbounded length, and CCBA is not
equal to any word of length ≤3 (nor to any other length-4 word) as an
automorphism.

## Why the rewrite is Ω(n²) on an explicit family

**Lemma (length-preserving sections).** For every word
w ∈ {A,B,C}* and every letter x, the wreath section `w|_x` is a word
of the same length. Proof: each of A,B,C sections to a single
generator.

**Corollary.** For every n≥1 and every 0≤k≤n−1, the word produced by
the rewrite for `C^n|_{0^k}` has length exactly n. The query asks for
the activity after n−1 zeros, i.e. n successive words (k=0 through
k=n−1). Charging Θ(1) per generator rewrite, the total expansion
along the ray is exactly n².

This holds for **every** n, including the two dyadic families

```
n = 2^m,     n = 2^m − 1.
```

The certifier checks `sum of expanded lengths = n²` on those families
through n=128 and n=63 respectively, and that every snapshot has
expanded length n.

The compressed description size (letters stored in
`prefix/block/suffix`, not expanded) only postpones the bill. On
n=2^m it is O(1) for the first O(log n) steps and then n. The sum of
description sizes is n²−O(n log n): 14953 vs n²=16384 at n=128. Still
Ω(n²).

No length-reducing relation absorbs this. Distinct words of length
≤6 are pairwise distinct already as maps on `{0,1}^8` (hence as tree
automorphisms). For n≤8, no word `C^n|_{0^k}` equals any strictly
shorter word even on 8-bit prefixes. In particular the semigroup
does not identify the length-n ray words with a sublinear generator
word for those n, and the first 4-letter block CCBA is reduced.

## Cost of what was actually constructed

- Construction of `C^n` by squaring: Θ(log n) group multiplications,
  with exponents of bit length O(log n). Fine.
- Evaluation of `ε(C^n|_{0^{n-1}})` by the proved section rules: Θ(n²)
  generator rewrites in model 1, on every n, with explicit constants
  `sum_exp = n²` on the dyadic families.
- The same walk also emits bits 1..n of `f^n(1)` (the activities
  along the zero ray). Computing one bit by this method computes the
  whole upper row of length n, at quadratic bit-cost.

This is the original CA in a different alphabet: the length-n word in
{A,B,C} evolving under the right-to-left 2-state section transducer
is a recoding of the triangular dependency, not a shortcut around it.

## Why the attack died

The kill criterion was: retire if the proved rewrite rules require
Ω(n²) total expansion along an explicit infinite family of query
rays.

They do. The family is n=2^m (also n=2^m−1). The rewrite is
length-preserving on {A,B,C}* and starts from C^n, so n letters are
rewritten at each of n depths. Block-doubling under 1-activity powers
reaches a linear-size block after O(log n) zeros and then stays
linear. Short relations that would cut the word length do not exist
through length 6, and do not exist for the actual ray words through
n=8.

This is not a lower bound on arbitrary algorithms. A different
encoding (Hashlife on the spacetime, a closed form for the diagonal,
a contracting conjugacy that the 2-adic audit in
[twoadic.md](twoadic.md) did not find) could still be O(n) or o(n) in
model 1. Nothing here rules that out. Nothing here produces it
either.

## What was obtained

- Exact wreath presentation A=(A,C), B=(A,C)σ, C=(B,C)σ, with
  `c_n = ε(C^n|_{0^{n-1}})` and `A^n|_1 = C^n`.
- Closed section formulae for A^m, B^m, C^m, (BC)^m, (CB)^m, and the
  general power-section rule (including the 4-letter identity
  `(CA)^k|_0 = (CCBA)^{k/2}` for even k).
- A length-preserving lemma that forces n² expansion of those rules
  on every query ray, checked on the dyadic families.
- No O(n) algorithm, and no O(n log n) algorithm, from this attack.

## Reproduction

```
python3 research/automaton_sections.py
```
