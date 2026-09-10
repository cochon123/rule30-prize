# Finite ancestry through the inverse row transducer

**Status.** No periodic center is excluded for the actual seed. There is
no depth-independent invariant. This note does not claim a prize result.

Helper: `research/ancestry_transducer.py`. Dump:
`research/ancestry_transducer.json`. Does not modify `strip_graph.py`,
`strip_extend.py`, or `experiment.py`.

The integer encoding and unique 2-adic inverse are those of
`twoadic.md`:

\[
z=f(y)=y\oplus((y\ll 1)\lor(y\ll 2)),
\qquad
y_k=z_k\oplus(y_{k-1}\lor y_{k-2}),
\quad y_{-1}=y_{-2}=0.
\]

Bit \(k\) of a row is the cell \(k\) steps left of the right edge. The
prize center at time \(t\) is bit \(t\) of \(f^t(1)\). Strips omit both
the infinite zero tail *and* membership in this single-seed orbit. The
transducer supplies the missing tail test. It does not supply seed
membership as a local constraint.

As in `period9_sigma.md`: a periodic *label in the depth direction*
(here: return of the transducer to state `00` at the left endpoint) is
not periodicity of the center in time, and is not a construction of the
seed orbit.

## The 4-state transducer

State \((y_{k-1},y_{k-2})\), packed `y_{k-1} | (y_{k-2}<<1)`:

| state | on input \(z_k\) | output \(y_k\) | next |
|------:|:-----------------|---------------:|:-----|
| `00` | \(y_k=z_k\) | \(z_k\) | `00` if \(z_k=0\), `10` if \(z_k=1\) |
| `01` | \(y_k=\overline{z_k}\) | \(\overline{z_k}\) | `10` if \(z_k=0\), `00` if \(z_k=1\) |
| `10` | \(y_k=\overline{z_k}\) | \(\overline{z_k}\) | `11` if \(z_k=0\), `01` if \(z_k=1\) |
| `11` | \(y_k=\overline{z_k}\) | \(\overline{z_k}\) | `11` if \(z_k=0\), `01` if \(z_k=1\) |

Start at `00`. After a finite word, trailing input is `0`.

**Lemma (finite predecessor).** A nonnegative integer has a finite
predecessor iff the transducer ends in `00` after its bits. From `00`,
input `0` stays in `00` and writes `0`. From `01`, input `0` goes
`01 → 10 → 11 → 11 → ⋯` and writes `0111⋯`. From `10` or `11`, input `0`
writes an infinite `1`-tail. No non-`00` tail state ever returns to `00`
on zeros.

**Lemma (3-state fold).** `10` and `11` have identical transitions, so
the machine quotients to three states `{00, 01, 1*}`. The `OR` of the
two previous predecessor bits is already `1` whenever the last bit is
`1`.

**Lemma (bitlength and exact depth).** For \(y>0\),
\(\mathrm{bitlength}(f(y))=\mathrm{bitlength}(y)+2\). Hence a positive
finite integer admits at most \((\mathrm{bitlength}-1)/2\) successive
finite predecessors. The seed `1` is a kernel (no finite predecessor).
Exact ancestry depth of \(f^t(1)\) is \(t\). Checked for \(t\le 12\);
the bitlength identity is for every positive integer.

`f` is bijective on \(\mathbb Z_2\), so every 2-adic integer has a
unique predecessor. Finiteness is a *tail* condition, not a window
condition. That is the source of everything below.

## Automata for \(d=1,2,4\) successive finite predecessors

Let \(L_d\) be the language of finite LSB-first words whose integer
value has \(d\) successive finite predecessors. Feed the input through
a cascade of \(d\) copies of the transducer; accept iff every layer is
`00`. Raw state space \(4^d\). Endpoints and a marked center are
regular annotations of the same DFA: the first bit, the last bit, and
(with a marked alphabet) a unique marked position. Equality of left and
right half-lengths is *not* regular; imposing it together with exact
depth \(d\) and kernel `1` collapses the language to the singleton
\(\{f^d(1)\}\).

Machine-checked through \(d=6\):

| \(d\) | raw \(4^d\) | reachable | minimized live | max shortest reset |
|------:|------------:|----------:|---------------:|-------------------:|
| 1 | 4 | 4 | 3 | 2 |
| 2 | 16 | 10 | 7 | 4 |
| 3 | 64 | 22 | 16 | 6 |
| 4 | 256 | 50 | 35 | 8 |
| 5 | 1024 | 104 | 71 | 10 |
| 6 | 4096 | 208 | 141 | 12 |

Every one of the \(4^d\) cascade states is co-reachable to accept. The
live language has a **full binary prefix language** (every live state
has live `0` and `1` successors). Consequently every finite word is a
prefix of some word in \(L_d\), and every finite word is a factor.
Marking a center bit and recording both endpoints cannot create a
forbidden local pattern: there is none.

The shortest word from a live state back to all-`00` has length at most
\(2d\), with the bound attained. That is a well-founded rank *on a
fixed cascade*, not a rank that is uniform in ancestry depth.

## No inductive automaton containing the seed

Three candidate limits fail in different ways.

1. \(\bigcap_d L_d\cap\mathbb Z_{\ge 0}=\{0\}\), because bitlength
   drops by 2 at each inverse. This language does not contain `1`.
2. \(\bigcup_d L_d\) is every finite word. Too coarse to constrain a
   center.
3. The minimized live DFAs are strictly increasing
   \(3,7,16,35,71,141\). No finite quotient of the cascade stabilizes.
   Adding a layer (the inductive step from depth \(d\) to \(d+1\))
   roughly doubles the live automaton.

Any regular overapproximation closed under \(f\) and containing `1`
must therefore accept many non-orbit rows. The smallest natural one,
\(L_1\) (one finite predecessor), already has a full prefix language.

Retaining the geometric middle (odd length \(2t+1\), mark at bit \(t\))
together with `inv^t(z)=1` is exact seed membership. It is a singleton
at each \(t\), not an inductive automaton.

## Period monitor and ranking

The prize column of generation \(n-j\) sits at bit \(n-j\) of
\(\mathrm{inv}^j(z)\), not at a fixed bit of the cascade. A correct
period monitor samples *diagonally*. On the singleton
\(z=f^n(1)\) this readout is exactly the true center history, reversed.
No new exclusion: it reproduces `experiment.py`.

On the overapproximation (any kernel, not just `1`), a ranking on the
4-state at the center fails in two independent ways.

**Along the seed.** The projection
\((\text{state before bit }t,\; t\bmod p,\; c_t)\) is not functional
for \(p=2,\ldots,8\): the same key has several observed successors
(11 of 16 keys are already ambiguous for \(p=2\) on the first 64
times). There is no rank on this finite set that decreases along every
periodic-center step, because the observed steps are not a function of
the set.

**Across finite seeds.** At each of \(t=8,12,16\), every one of the
four transducer states occurs with *both* center bits among odd
\(y<2^8\). The 4-state at the prize column does not determine the
center, even at a fixed time.

The shortest-reset distance on the \(d\)-fold cascade is well-founded
going *backward* (depth drops, bound \(2d\) drops). Going forward,
depth grows, so the bound grows. That ranking only restates “a finite
row has a last finite predecessor”, which is the bitlength lemma. It
does not mention the center.

## The obstruction, in numbers

Write \(c_t(y)=(f^t(y)\gg t)\mathbin{\&}1\). For \(y=1\) this is the
prize sequence. For a general odd finite \(y\) it is the fixed spatial
column that began at the right edge of that seed.

Union over odd \(y<2^{10}\) of the length-6 factors of
\((c_t(y))_{t<64}\) is the **full 2-shift** (64/64). The same 64 words
already occur among kernels. The seed itself, in the same window, has
only 36 of 64 factors. From onset \(T=1\) through \(T=32\), every
length-6 slice across those \(y\) has at least 63 of the 64 words
(almost always 64). Length 8, odd \(y<2^8\), 96 steps: all 256 words;
the seed has 75.

So every local center pattern, including every local periodic word, has
finite-seed realizations at many ancestry depths. The automata of \(L_d\)
cannot forbid a periodic *stretch*. They also cannot force a kernel to
be `1` without collapsing to the singleton orbit.

A finite scan is not an eventual-periodicity theorem for other seeds.
At 256 steps, no odd \(y<2^8\) has a tail of length \(\ge 4p\) for any
period \(p=2,\ldots,12\). Constant-tail exclusion
(`constant_tails.md`) already kills period 1 for every nonzero finite
seed, via Jen/Kopra. That is the only period this ancestry analysis
excludes, and it does not use the transducer.

## What this does not do

It does not exclude period 2, periods 3–7, or \(q=8\). It does not
produce a ranking certificate with checkable initialization and
preservation that would block infinite periodic-center continuation of
the seed. A table of DFA sizes indexed by \(d\) is exactly the object
the assignment forbids as a substitute for an invariant; the table is
recorded only as evidence that the construction does not stabilize.

Pinning the kernel to `1` reduces to the original sequence. Relaxing
the kernel to any finite seed makes the local center language the full
shift. There is no intermediate regular invariant in this transducer.

## Strongest honest statement

The inverse row map is a 3-state transducer; finite predecessors are
exactly the words that end in `00`. The \(d\)-fold languages \(L_d\)
are regular, have a full prefix language, and have minimized live DFAs
whose sizes strictly increase through \(d=6\) (reset rank \(2d\)).
Every length-6 (resp. 8) center factor is realized by some odd finite
seed, already at many times. The 4-state at the prize column does not
determine the center bit. Therefore finite ancestry, with endpoints and
a marked center, yields no depth-independent invariant that excludes a
nonconstant eventual period for \(f^t(1)\). Period 1 remains excluded
by the constant-tail argument, not by this construction.

## Reproduction

```
python3 research/ancestry_transducer.py
```

The script inverts `f` on `1..199`, checks the tail classification and
the 3-state fold, asserts the DFA-size table, full prefix languages,
reset bound \(2d\), full length-6/8 finite-seed factor languages, and
that every transducer state realizes both center bits at \(t=8,12,16\).
