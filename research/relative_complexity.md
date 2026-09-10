# Relative symbolic complexity of the pair \((\ell,c)\)

**Status.** The criterion \(\sup_m R_m=\infty\) is a sufficient condition for
prize problem 1 that is strictly stronger than aperiodicity of the pair and is
not the rejected rigidity implication \(A_p\Rightarrow B_p\). It is **not
proved**. The only exact values on the single-cell seed are \(R_1=2\) and
\(R_2=3\). A seed-valid return-word construction that would produce arbitrarily
large fibres dies: the inductive amplification step requires independently
choosing a right-neighbour bit or a further-left bit. This is not a prize
claim.

Helper: `research/relative_complexity.py`. Dump:
`research/relative_complexity.json`. Does not modify `strip_graph.py`,
`strip_extend.py`, or `experiment.py`.

Convention:

\[
x(t+1,j)=x(t,j-1)\oplus(x(t,j)\lor x(t,j+1)),
\qquad
x(0,j)=\mathbf{1}_{j=0},
\]
\[
\ell_t=x(t,-1),\qquad c_t=x(t,0),\qquad r_t=x(t,1).
\]

For \(m\ge 1\) and a left word \(a\in\{0,1\}^m\), write \(F(a)\) for the set of
center words \(b\in\{0,1\}^m\) such that \((a,b)\) occurs as a consecutive
length-\(m\) block of the pair \((\ell,c)\) on this one orbit. Then

\[
R_m=\max_a\,|F(a)|.
\]

Measured values below are lower bounds coming from a finite prefix: the
true \(R_m\) is at least as large.

## 1. Why unbounded \(R_m\) would kill every eventual period

If \(c\) is eventually period \(p\) after onset \(T\), then \(c\) has at most
\(T+p\) distinct length-\(m\) factors (the \(T\) prefix starts, plus at most
\(p\) eventual phases). Therefore \(R_m\le T+p\) for every \(m\), and

\[
\sup_m R_m=\infty
\quad\Longrightarrow\quad
\text{\(c\) is not eventually periodic}.
\]

This is stronger than aperiodicity of the *pair*. Jen/Kopra already give that
\((\ell,c)\) is not eventually periodic. If \(c=\ell\), the pair can be
aperiodic with \(R_m=1\) for all \(m\). Unbounded fibres mean the center
carries information not determined by left \(m\)-blocks.

It is not the rigidity implication of `rigidity_ep.md`. That asked
\(e_p(t,0)=0\) eventually \(\Rightarrow\) \(e_p(t,-1)=0\) eventually, which
given Jen/Kopra is equivalent to \(\neg A_p\). Here the target is a growth
statement about factor fibres of one orbit, with no period \(p\) in the
hypothesis.

## 2. Exact branching

The center update is

\[
c_{t+1}=\ell_t\oplus(c_t\lor r_t).
\]

**Lemma (lock / branch).** If \(c_t=1\), then \(c_{t+1}=1-\ell_t\), independently
of \(r_t\). If \(c_t=0\), then \(c_{t+1}=\ell_t\oplus r_t\), so the next center
bit branches on the right neighbour.

Checked on the packed seed for \(t<12000\): zero failures of the update, zero
failures of the lock, and both values of \(r_t\) occur at center zeros.

A pair \((a,b)\) of length \(m\) is *locally compatible* if there exists some
right word realizing the update, equivalently: for every \(i<m-1\) with
\(b_i=1\), one has \(b_{i+1}=1\oplus a_i\). Write \(C(a)\) for the number of
such \(b\). Then \(F(a)\subseteq\{\text{locally compatible }b\}\), so
\(R_m\le\max_a C(a)\).

\(C(a)\) is independent of any orbit. It is minimized by \(a=0^m\), where a
center \(1\) must be followed by \(1\), hence the compatible words are exactly
\(0^k1^{m-k}\) and \(C(0^m)=m+1\). It is maximized by \(a=1^m\), where a
center \(1\) must be followed by \(0\), hence the compatible words are the
length-\(m\) strings with no two consecutive \(1\)s and
\(C(1^m)=F_{m+2}\) (Fibonacci, \(F_1=F_2=1\)). Every observed seed pair of
length \(16\) in the length-\(12000\) prefix is locally compatible.

**Lemma (left-zero run).** Along any run of zeros in \(\ell\), the center is
nondecreasing: if \(\ell_t=0\) then \(c_{t+1}=c_t\lor r_t\). Consequently every
center companion of \(0^m\) is of the form \(0^k1^{m-k}\).

Continuation of the left-zero run is a *left*-exterior constraint: with
\(\ell_t=0\),

\[
\ell_{t+1}=x(t,-2)\oplus c_t,
\]

so \(\ell_{t+1}=0\) if and only if \(x(t,-2)=c_t\). The flip time inside the
run is a *right*-exterior constraint: the first \(r_t=1\) while \(c\) is still
\(0\).

## 3. Exact small values on the seed

### \(R_1=2\)

Times \(t=1\) and \(t=2\): \(\ell\) is \(1\) with centers \(1\) and \(0\).
Times \(t=0\) and \(t=6\): \(\ell\) is \(0\) with centers \(1\) and \(0\).
Local maximum is \(2\), so \(R_1=2\) on the infinite orbit.

### \(R_2=3\)

Local maximum is \(C(a)=3\) for every length-\(2\) left word (the forbidden
center pair is the one that would violate the lock). The seed realizes all
three companions of each of the four left words:

| \(a\) | companions \(b\) | first times |
|------:|------------------|-------------|
| \(00\) | \(11,00,01\) | \(3,17,21\) |
| \(01\) | \(11,00,01\) | \(0,6,12\) |
| \(10\) | \(01,10,00\) | \(2,5,11\) |
| \(11\) | \(10,00,01\) | \(1,10,25\) |

Thus \(R_2=3\) on the infinite orbit. In particular \(c\) is not purely
period \(2\) from time \(0\) (that would force \(R_2\le 2\)), which is already
visible from the prefix \(c=110\ldots\), and is the only eventual-period
exclusion these exact values give: \(T+p\ge 3\).

For \(m=3\), every left word has seed fibre \(4\) in the length-\(12000\)
prefix, with explicit first hits in the dump. Words with \(C(a)=4\) are
saturated; words with \(C(a)=5\) are missing one locally legal companion.
So \(R_3\ge 4\), and the local maximum \(5\) is not realized in this window.

## 4. Attempted return-word construction

The assignment asked for a seed-valid family: for every \(r\), one left word
together with actual occurrence times at which at least \(r\) distinct center
words appear, with spacetime certificates that extend inductively.

### Nested lineage \(1,10,100,\ldots,10^{m-1}\)

Start from the \(R_1=2\) cylinder \(\ell_t=1\). The greedy right extension
that preserves the largest fibre on the seed is the nested family

\[
\alpha_m=10^{m-1}.
\]

Occurrence counts in a prefix of length \(12000\) roughly halve at each
length (\(5984,2963,1515,757,375,194,100,56,\ldots\)). Fibre along this
lineage is

\[
2,3,4,5,6,7,8
\]

through \(m=7\), strictly below \(C(\alpha_m)=2m-1\) once \(m\ge 3\). Each
increase \(m\mapsto m+1\) for \(m\le 7\) is a genuine seed \(r\)-split: two
visits to \(\alpha_{m+1}\) share a center prefix ending in \(0\) and take
both values of \(r\) at that \(0\)-phase. After \(m=8\) the nested fibre
falls, because the longer word simply does not repeat often enough in the
window.

There is no inductive production of the next occurrence time. A certificate
that \(\alpha_m\) occurs at time \(t\) is the seed triangle through row
\(t+m\). The next visit \(t'>t\) is a different light cone. Nothing in the
Rule 30 stencil, the left lightlike \(x(s,-s)=1\), or the left-zero tail at
time \(0\) maps one visit to the next.

### The word \(0^m\)

This is the combinatorially cheapest family: \(C(0^m)=m+1\), and lemma 2
says the only possible companions are \(0^k1^{m-k}\). If every offset \(k\)
occurred, one would have \(R_m\ge m+1\) and the criterion would be proved.

On the seed, \(0^6\) *does* realize all \(7\) locally legal companions (first
hits at times \(61,125,126,156,191,1038,5808\) in the length-\(40000\)
prefix). Already \(0^7\) drops to fibre \(6<8\), \(0^8\) to \(6<9\),
\(0^{12}\) to \(3<13\), \(0^{14}\) to \(3<15\). The missing companions are
the late offsets: long left-zero runs that keep \(c=0\) for most of the run,
i.e. long simultaneous \(00\) blocks of the width-\(2\) trace. Jen/Kopra
forbid an infinite such block and say nothing about unbounded finite length.

To extend a left-zero run of length \(m\) starting at \(t\) to length \(m+1\),
the new cell \(x(t+m-1,-2)\) must equal \(c_{t+m-1}\). That cell lies strictly
left of the left word being amplified. It is not determined by \((\ell,c)\)
on the existing block; sideways reconstruction of column \(-2\) needs a
*future* bit of \((\ell,c)\). Forward in time it is an independent left
boundary bit. Prescribing the flip offset additionally requires a chosen
value of \(r\) at the \(0\)-phase.

So the inductive step for this family has the form: “keep \(\ell=0\) by
setting column \(-2\) equal to \(c\), and optionally flip \(c\) by setting
\(r=1\).” Both bits are exterior to the pair-block. On the seed they happen
to take whatever values the triangle gives; they are not produced from
shorter certificates.

### Overlapping returns of a short word

Every length-\(4\) left word repeats in the sample, and every one of them
sees both values of \(r\) at some internal \(0\)-phase (\(16/16\)). The same
holds for all \(256\) length-\(8\) left words in a prefix of length \(12000\).
Repeating a short word with many center companions does not yield a *long*
left word with a large fibre: the left extensions at distinct visits
generally differ, splitting one large short fibre into many singleton long
fibres. Nested extensions of a maximizer therefore cannot be pumped by
returns alone. A new maximizer at length \(m+1\) is a different word, not an
inductive extension of the length-\(m\) certificate.

## 5. Measured \(R_m\)

Packed evolution of \(F^t\delta_0\). Encoding matches `experiment.py` /
`rigidity_ep.py` (bit \(k\) of the row is spatial coordinate \(k-t\)) and was
checked against a spatial dictionary through \(t<80\).

Prefix \(N=12000\), all binary left and center words occur through \(m=10\)
(\(p_\ell(m)=p_c(m)=2^m\)):

| \(m\) | \(R_m\) | \(p_\ell\) | \(p_{\ell,c}\) | mean fibre | local \(\max C\) |
|------:|--------:|-----------:|---------------:|-----------:|-----------------:|
| 1 | 2 | 2 | 4 | 2.00 | 2 |
| 2 | 3 | 4 | 12 | 3.00 | 3 |
| 3 | 4 | 8 | 32 | 4.00 | 5 |
| 4 | 5 | 16 | 80 | 5.00 | 8 |
| 5 | 7 | 32 | 200 | 6.25 | 13 |
| 6 | 9 | 64 | 496 | 7.75 | 21 |
| 8 | 15 | 256 | 2545 | 9.94 | 55 |
| 10 | 14 | 1024 | 7125 | 6.96 | 144 |
| 12 | 8 | 3871 | 10484 | 2.71 | 377 |
| 16 | 4 | 10959 | 11903 | 1.09 | 2584 |

The drop for \(m\ge 12\) is a finite-window artefact: \(N-m+1\) overlapping
blocks cannot repeat a typical \(m\)-word often enough to grow a fibre.
At \(m=32\) every left word in the prefix is unique, so the measured value
is \(1\) regardless of the infinite orbit.

Longer prefixes, same \(m\), show which values have saturated and which are
still accumulating:

| \(N\) | \(R_4\) | \(R_6\) | \(R_8\) | \(R_{10}\) | \(R_{12}\) | \(R_{16}\) |
|------:|--------:|--------:|--------:|-----------:|-----------:|-----------:|
| 12000 | 5 | 9 | 15 | 14 | 8 | 4 |
| 20000 | 5 | 9 | 15 | 15 | 12 | 4 |
| 30000 | 5 | 9 | 15 | 18 | 13 | 5 |
| 40000 | 5 | 9 | 15 | 19 | 14 | 6 |

So \(R_4=5\), \(R_6=9\), and \(R_8=15\) are stable from \(N=12000\) to
\(N=40000\) (for \(m=4\), already from \(N=2000\)), while remaining strictly
below the free-boundary counts \(8\), \(21\), and \(55\). These are still
only lower bounds on the infinite-orbit values, but they are the right scale:
a true \(R_8=15\) would give only \(T+p\ge 15\), a finite onset constraint of
the same kind already obtained by SAT in `period2_left_edge.md`, not
\(\sup R_m=\infty\).

A top-\(k\) nested search (not just the greedy \(10^{m-1}\) path) reaches
measured fibre \(14\) at \(m=8\) then falls for the same window reason.
Other odd finite seeds \(3,5,7\) at \(N=4000\) show the same small-\(m\)
pattern (\(R_4=5\), \(R_8\) in the low teens) and do not supply a better
inductive family.

## 6. Free right boundary versus the seed

The locally compatible count \(C(a)\) is exactly the fibre in a strip with a
freely chosen right neighbour. On the seed it is a large overapproximation:

| \(m\) | seed \(R_m\) (\(N=12000\)) | maximizer’s \(C(a)\) | sample-mean \(C(a)\) |
|------:|---------------------------:|---------------------:|---------------------:|
| 4 | 5 | 7–8 | 6.8 |
| 8 | 15 | 33–37 | 33.7 |
| 12 | 8 | 127–163 | 163 |
| 16 | 4 | 743–1055 | 786 |

Using an independently chosen exterior right bit therefore counts many
center words that never occur with that left word on \(F^t\delta_0\). This is
the same free-boundary obstruction recorded for residual strip SCCs in
`strip_graph.py` / `strip_extend.py` and in `rigidity_ep.md` §3: locally
admissible branches need not appear on the prescribed orbit.

## 7. Kill

The only local mechanism that increases a nested fibre is a \(0\)-phase of
\(c\) at which two visits to the same left word take both values of \(r\).
The only cheap infinite family of left words whose compatible companions are
completely classified is \(0^m\), and extending those runs requires
\(x(\,\cdot\,,-2)=c\) at the new time.

Both steps ask for an exterior bit that is not a function of the pair-block
already constructed:

- \(r_t\) is the right half of the triangle;
- \(x(t,-2)\) is the next column to the left.

On the seed those bits are fixed; they are not available as construction
parameters. Treating them as free recovers the large \(C(a)\) numbers above
and is exactly “independently choosing an exterior boundary.” Changing the
initial seed (\(3,5,7\)) does not produce an inductive certificate either.
There is no remaining seed-valid pumping step.

Establishing that some left \(m\)-word recurs with more and more center
companions as \(m\) grows is a recurrence/normality-strength statement about
one orbit. It is not implied by Jen/Kopra, by infinitely many \(0\)s and
\(1\)s in \(c\) (`constant_tails.md`), or by the lock identity.

## Strongest honest statement

On every Rule 30 orbit, \(c_{t+1}=\ell_t\oplus(c_t\lor r_t)\): \(1\)-phases of
the center lock the next bit, \(0\)-phases branch on \(r\), and along a run
of left zeros the center is nondecreasing. Locally \(R_m\le F_{m+2}\). If
\(c\) is eventually period \(p\) after \(T\), then \(R_m\le T+p\) for all
\(m\), so unbounded \(R_m\) would solve problem 1. On the single-cell seed,
\(R_1=2\) and \(R_2=3\) by explicit times, matching the local maxima. Measured
lower bounds grow through \(R_8\ge 15\) and then cannot be tracked without
\(N\gg 2^m\). No seed-valid return-word family with inductively extending
spacetime certificates produces arbitrarily large fibres: amplification
requires a free right neighbour or a free column \(-2\). Problem 1 is not
closer. The criterion remains a sufficient condition with two exact small
values and a finite table of lower bounds.

## Reproduction

```
python3 research/relative_complexity.py
```

Asserts the packed/spatial encoding through \(t<80\), the update and lock
identities on the length-\(12000\) prefix, local Fibonacci counts for
\(0^m\) and \(1^m\), and \(R_2=3\) by saturating every length-\(2\) left
word. Writes the fibre tables, nested lineage, return-word splits, and the
seed-versus-free comparison.
