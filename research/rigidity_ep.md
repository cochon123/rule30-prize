# Seed-specific rigidity of time-shifted orbits

**Status.** The implication below is **not proved** for the single-cell
seed. It is **false** as a statement about arbitrary bi-infinite Rule 30
orbits. Given Jen/Kopra’s width-2 theorem it is logically equivalent to
prize problem 1, so a proof would be prize-level; none is obtained.
This is not a prize claim.

Helper: `research/rigidity_ep.py`. Dump: `research/rigidity_ep.json`.
Does not modify `strip_graph.py`, `strip_extend.py`, or `experiment.py`.

Convention:

\[
x(t+1,j)=x(t,j-1)\oplus(x(t,j)\lor x(t,j+1)),
\qquad
x(0,j)=\mathbf 1_{j=0},
\qquad
c_t=x(t,0).
\]

For \(p>0\) define the time-shifted disagreement

\[
e_p(t,j)=x(t+p,j)\oplus x(t,j).
\]

The proposed rigidity theorem is

\[
e_p(t,0)=0\text{ eventually}
\quad\Longrightarrow\quad
e_p(t,-1)=0\text{ eventually}.
\]

Call the antecedent \(A_p\) and the consequent \(B_p\). If \(A_p\Rightarrow B_p\)
held on the seed, then a hypothetical eventually period-\(p\) centre
would make columns \(-1\) and \(0\) both eventually period \(p\),
contradicting Kopra 2023, Corollary 3.7 (Jen’s width-2 theorem) for every
nonzero finite seed. That would solve problem 1.

## 1. Exact update

Write \(a_j=x(t+p,j)\), \(b_j=x(t,j)\), \(e_j=e_p(t,j)\), and

\[
h_j=(a_j\lor a_{j+1})\oplus(b_j\lor b_{j+1}).
\]

The Rule 30 images satisfy

\[
e_p(t+1,j)=e_p(t,j-1)\oplus h_j.
\]

Over \(\mathrm{GF}(2)\), with \(a=b+e\) and \(\lor\) expanded as
\(u\lor v=u+v+uv\),

\[
h_j=e_j+e_{j+1}+b_j e_{j+1}+b_{j+1}e_j+e_j e_{j+1}.
\]

Equivalently (as in `block_energy.md`)

\[
e'_j=e_{j-1}+(1+b_{j+1})e_j+(1+b_j)e_{j+1}+e_je_{j+1}.
\]

Disagreement is therefore not an autonomous linear light-cone rule: the
background \(b=F^t\delta_0\) (or the shifted background \(a\)) enters
through bilinear terms, and those terms can cancel a mismatch. Checked
against the packed seed orbit for \(p\in\{1,2,3,4,8,9\}\) and
\(t<80\), every spatial index in the light cone: no mismatch.

Rearranged at the origin, the same identity is

\[
e_p(t+1,0)=e_p(t,-1)\oplus h_0.
\]

### Erasure at a periodic centre

If \(e_p(t,0)=e_p(t+1,0)=0\), then \(e_p(t,-1)=h_0\). In that case
\(a_0=b_0=c_t\), so

\[
h_0=(c_t\lor x(t+p,1))\oplus(c_t\lor x(t,1))
=(1+c_t)\,e_p(t,1).
\]

**Lemma (erasure).** Whenever two consecutive centre bits of \(e_p\)
vanish,

\[
e_p(t,-1)=(1+c_t)\,e_p(t,1).
\]

In particular: on every 1-phase of the centre, left disagreement is
forced to \(0\) independently of the right; on every 0-phase, left
disagreement equals right disagreement. The identity is the same
relation recorded in `disagreement.md` for \(p=2\). It is checked on
every consecutive centre-agreement of the seed for \(t<16000\) and
\(p=1,\ldots,9\) (zero failures; several thousand hits per \(p\)).

Constant tails (`constant_tails.md`) are the \(p=1\) special cases.
If \(c_t=1\) eventually then the erasure formula gives \(B_1\) at once,
and Jen kills the resulting width-2 pair. If \(c_t=0\) eventually then
\(e_1(t,-1)=e_1(t,1)\) at every large \(t\), and the right-neighbour
update forces that common neighbour to be eventually constant, again
Jen. So \(A_1\) is already false on the seed, and \(A_1\Rightarrow B_1\)
holds vacuously. The interesting case is nonconstant \(p>1\).

## 2. Why local causality cannot prove the implication

Assume \(A_p\), and shift time so that \(e_p(t,0)=0\) for all \(t\ge 0\).
Erasure then holds at every time:

\[
e_p(t,-1)=(1+c_t)\,e_p(t,1),\qquad t\ge 0.
\]

The centre has infinitely many 0s (`constant_tails.md`), so \(1+c_t=1\)
infinitely often. Thus \(B_p\) holds if and only if \(e_p(t,1)=0\) at
every sufficiently late 0-phase of \(c\). That is a constraint on the
*right* neighbour, not a consequence of a finite left-of-centre window.

Any argument that uses only the local Rule 30 stencil around column \(0\)
is therefore consistent with \(A_p\wedge\neg B_p\): put \(c_t=0\) and
\(e_p(t,1)=1\) at a 0-phase, and erasure copies the mismatch to column
\(-1\). The spatially periodic counterexample below realises this
globally.

## 3. Local / infinite-row counterexamples

### The period-7 orbit (`disagreement.md`)

The bi-infinite spatially 7-periodic configuration with one period
`0100110` (index 0 at the first displayed 0) has temporal period 4:

```
t  b          F^2(b)     e = b XOR F^2(b)   e(t,0)  e(t,-1)
0  0100110    0000001    0100111              0        1
1  1111101    1000011    0111110              0        0
2  0000001    0100110    0100111              0        1
3  1000011    1111101    0111110              0        0
```

The centre of \(b\) is exactly period 2, so \(A_2\) holds identically,
while \(e_2(t,-1)\) is the period-2 sequence \(1010\ldots\), so \(B_2\)
fails. Reproduced by `period_7_audit`. Periodic boundary here is only a
compact display of a bi-infinite configuration; it is a valid Rule 30
orbit.

Jen/Kopra do not apply: the configuration is not left-asymptotic to
\(0^{\mathbb Z}\).

### Cyclic census

Every cyclic configuration of spatial width \(n\le 14\) was evolved to
its temporal cycle, and every spatial origin was tested
(`cyclic_census`). A *target-\(p\) hit* is a column that is purely
\(p\)-periodic whose left neighbour is not.

| \(p\) | hits (\(n\le 14\)) |
|------:|-------------------:|
| 2 | 419 |
| 3 | 0 |
| 4 | 0 |
| 8 | 0 |
| 9 | 0 |

All 419 hits are of the same arithmetic type as the period-7 orbit:
min-period of the chosen column is 2, min-period of its left neighbour
is 4 (so \(A_2\) holds and \(B_2\) fails; \(A_4\) and \(B_4\) both hold).
No cyclic realisation of \(A_p\wedge\neg B_p\) was found for
\(p\in\{3,4,8,9\}\) at these widths. That is not a theorem, and it does
not restore a local proof: the erasure identity already supplies a
finite-window obstruction for every nonconstant period.

### Free-boundary strips

The radius-\(\ge 6\) residual SCCs of `strip_graph.py` /
`strip_extend.py` for the alternating word `01` and for the primitive
words of periods 3–7 (`small_periods.md`) are overapproximations with
free outer bits. They are not seed orbits, but they are exactly the
local objects one would retain if \(A_p\) did not force a periodic left
neighbour. Nonempty residual components are therefore the same
obstruction, now in the language of bounded strips.

## 4. The single-cell seed, small \(p\)

Packed evolution of \(F^t\delta_0\) through \(t<16000\), columns
\(-2,-1,0,1,2\). Both lightlike bits of the seed are identically 1:
\(x(t,-t)=x(t,t)=1\). The left front of disagreement is the left
lightlike of the shifted orbit,

\[
e_p(t,-(t+p))=x(t+p,-(t+p))=1
\]

for every \(t,p\). Checked.

| \(p\) | last \(e_p(\cdot,0)=1\) | last \(e_p(\cdot,-1)=1\) | freq \(e_0\) | freq \(e_{-1}\) | longest \(e_0=0\) run | \(e_{-1}\) ones in that run | consecutive centre agreements | of which \(e_{-1}=1\) |
|------:|------------------------:|--------------------------:|-------------:|----------------:|----------------------:|----------------------------:|------------------------------:|----------------------:|
| 1 | 15999 | 15998 | 0.504 | 0.493 | 13 | 2 | 3933 | 462 |
| 2 | 15999 | 15999 | 0.501 | 0.509 | 12 | 2 | 4018 | 1004 |
| 3 | 15998 | 15999 | 0.498 | 0.493 | 15 | 3 | 4039 | 962 |
| 4 | 15999 | 15996 | 0.495 | 0.496 | 12 | 3 | 4146 | 1022 |
| 8 | 15999 | 15999 | 0.500 | 0.503 | 10 | 2 | 3936 | 958 |
| 9 | 15998 | 15992 | 0.505 | 0.498 | 12 | 3 | 3967 | 965 |

Neither \(A_p\) nor \(B_p\) is visible in this window for any listed
\(p\): both columns of \(e_p\) keep producing 1s at the end of the
sample, at frequency \(\approx 1/2\). During the longest finite zero
run of the centre of \(e_p\), column \(-1\) of \(e_p\) is still 1
several times. Almost every zero run of length \(\ge 6\) in \(e_p(\cdot,0)\)
still contains a 1 in \(e_p(\cdot,-1)\) (for \(p=2\): 133 of 136 such
runs).

The last two columns are the finite-time local test: times \(t\) with
\(e_p(t,0)=e_p(t+1,0)=0\) but \(e_p(t,-1)=1\). They occur in the
hundreds to thousands for every listed \(p\), as the erasure lemma
predicts (0-phases of \(c\) that meet a right disagreement). They do
**not** decide the eventual implication, because the seed’s centre is
not eventually periodic in this range. They do show that the seed
itself does not obey a one-step rigidity rule.

The same last-mismatch picture holds for the other odd finite seeds
\(y\in\{1,3,5,7,9,11\}\) through 2500 steps: last 1s of both
\(e_p(\cdot,0)\) and \(e_p(\cdot,-1)\) sit at the end of the sample.

If the prize claim is true, then \(A_p\) is false, so the implication
holds vacuously and column \(-1\) of \(e_p\) is not constrained by it.
Empirically, for these \(p\), column \(-1\) of \(e_p\) is 1 infinitely
often in the same sense that the centre is: last mismatch late, density
near \(1/2\). That is consistent with the prize and with Jen, and it is
not a proof of either.

## 5. Attempted global arguments (all fail to give \(A_p\Rightarrow B_p\))

### Left lightlike

Let \(v(t,k)=x(t,-t+k)\). Then \(v(t,0)=1\) for all \(t\), and
\(v(t,1)=1\) for all \(t\ge 1\). The left-edge recurrence is

\[
v(t+1,k)=v(t,k-2)\oplus(v(t,k-1)\lor v(t,k))
\]

with \(v(t,m)=0\) for \(m<0\). Checked for \(k<12\), \(t<400\).

Consequently the leftmost bit of \(e_p(\cdot,t)\) is always 1, at
spatial index \(-(t+p)\). A 1 is born on the far left at every time,
distance \(t+p\) from the origin. Because \(e'_j\) depends on
\(e_{j-1},e_j,e_{j+1}\) and on the background, that 1 may travel right,
be cancelled, or remain on the expanding left front. There is no
forced visit of the moving 1 to the *fixed* column \(-1\): new
disagreement is created further left at every step, so a front-speed
argument does not drag a mismatch through the origin. The period-7
orbit is the extreme case with no left vacuum at all; the seed has a
vacuum to the left of \(-t\), but the relevant left data of \(e_p\)
live in the length-\(p\) strip between \(-(t+p)\) and \(-t\), which is
exactly the left edge of \(x(t+p,\cdot)\) and is not a finite
automaton independent of \(p\) and \(t\).

### Right lightlike

\(x(t,t)=1\) likewise, and \(e_p(t,t+p)=1\). Right-edge diagonals
\(u(t,k)=x(t,t-k)\) are eventually periodic of period dividing \(2^k\)
(Rowland; `twoadic.md`). The centre is the diagonal \(u(n,n)\), whose
offset grows. Periodicity of a fixed-offset right diagonal does not
constrain \(e_p(t,-1)\). The erasure identity relates column \(-1\) of
\(e_p\) to column \(+1\), not to the right lightlike.

### Finite ancestry / inverse transducer

The 4-state (3-state folded) inverse row transducer of
`ancestry_transducer.md` decides whether a finite row has a finite
predecessor. Exact ancestry depth of \(F^t(1)\) is \(t\), and pinning
the kernel to \(1\) together with odd width \(2t+1\) collapses to the
singleton seed orbit. That is a restatement of the original spacetime
triangle, not an invariant that could force \(e_p(t,-1)=0\) from
\(e_p(t,0)=0\).

On any regular overapproximation (some finite kernel, not necessarily
`1`), every local centre factor occurs, including every local periodic
word (`ancestry_transducer.md`). The 4-state at the prize column does
not determine the centre bit. There is therefore no depth-independent
transducer relation that converts centre agreement of \(F^t(1)\) and
\(F^{t+p}(1)\) into agreement at column \(-1\).

### Period 2, via the even right neighbour

If one *assumes* \(A_2\) on the seed, `period2_neighbor.md` already
gives: the even right neighbour \(u_n=x(2n,1)\) has no two consecutive
1s, has infinitely many isolated 1s (else Jen), and cannot be
eventually periodic (else left reconstruction in `alternating.md` makes
column \(-1\) periodic and Jen applies). Then

\[
e_2(2n,-1)=u_n\oplus u_{n+1},
\]

which equals 1 at every isolated 1 of \(u\). So \(A_2\Rightarrow\neg B_2\)
on the seed. Combined with the desired \(A_2\Rightarrow B_2\), this is
exactly \(\neg A_2\). The period-2 case of rigidity is not a weaker
lemma; it is the period-2 case of the prize.

### Logical status for every \(p\)

Kopra’s Corollary 3.7 says that on the seed, columns \(-1\) and \(0\)
are never both eventually period \(p\). That is \(\neg(A_p\wedge B_p)\),
or \(A_p\Rightarrow\neg B_p\). Therefore, *given Jen/Kopra*,

\[
(A_p\Rightarrow B_p)\quad\Longleftrightarrow\quad \neg A_p.
\]

Proving seed-specific rigidity is proving that the centre is not
eventually period \(p\). The reduction is honest, but it is not a
reduction in difficulty. The only \(p\) for which \(\neg A_p\) is
already known is \(p=1\).

## 6. Stop

The assignment asked for a global boundary or ancestry proof, and to
stop if only local counterexamples or another free-boundary obstruction
appeared.

- The erasure identity is the exact local update at a periodic centre,
  and it permits \(A_p\wedge\neg B_p\) whenever the periodic word has a
  0.
- That possibility is realised by a bi-infinite spatially periodic
  orbit for \(p=2\), and by 419 cyclic column-pairs of spatial width
  \(\le 14\).
- Bounded-strip residual SCCs are the same obstruction with free outer
  bits.
- Left/right lightlike bits, finite ancestry, and the inverse
  transducer do not force \(B_p\) from \(A_p\) on the seed; they either
  reconstruct the original triangle or ignore the background-dependent
  cancellation.
- On the seed, for \(p=2,3,4,8,9\), one does not even see \(A_p\) in
  \(10^4\) steps, while local (finite-run) failures of rigidity occur
  throughout the sample.

The implication is therefore **false in the infinite-row category** and
**unproved for the seed**. For the seed it is equivalent to problem 1
and remains open for every \(p>1\).

## Strongest honest statement

On every Rule 30 orbit, \(e_p(t+1,j)=e_p(t,j-1)\oplus h_j\) with the
background polynomial \(h_j\) of §1, and two consecutive centre zeros
give the erasure rule \(e_p(t,-1)=(1+c_t)e_p(t,1)\). That rule does
not imply \(B_p\) from \(A_p\). A spatially 7-periodic orbit has \(A_2\)
and \(\neg B_2\). For the single-cell seed, Jen/Kopra make
\(A_p\Rightarrow B_p\) equivalent to nonperiodicity of the centre; no
boundary, ancestry, or transducer argument proved the implication, and
finite samples for \(p=2,3,4,8,9\) show persistent 1s in both
\(e_p(\cdot,0)\) and \(e_p(\cdot,-1)\). Problem 1 is untouched.

## Reproduction

```
python3 research/rigidity_ep.py
```

Asserts the packed/spatial encoding, the update and erasure identities,
the period-7 table, both seed lightlike bits, the left-diagonal
recurrence, and zero erasure failures on the length-16000 sample.
