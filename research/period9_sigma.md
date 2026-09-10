# Period 9 / \(q=8\): reconstruction quotient and \(\sigma\)

**Status.** Not excluded. This note does not claim a prize result.

Helper: `research/period9_sigma.py`. Dump: `research/period9_sigma.json`.
Uses `strip_graph.graph` / `components` without modifying `strip_graph.py`
or `strip_extend.py`.

Notation as in `period9_q8.md`. The center is \(01^8\), period \(9\).
Write \(\sigma_n=x(9n,-1)\) for the left neighbor of the isolated \(0\),
and
\[
C_{k,a}(n)=x(9n+a,-k),\qquad 0\le a<9.
\]
Phase \(9\) is phase \(0\) at \(n+1\). Reconstruction is Rule 30 inverted:
\[
C_{k+1,a}(n)=C_{k,a+1}(n)\oplus\bigl(C_{k,a}(n)\lor C_{k-1,a}(n)\bigr).
\]
Initialize \(C_0=011111111\) and \(C_1=\sigma_n00000001\) (the \(1\)-run
left bits are locally forced). The wrap at phase \(8\) reads
\(C_{k,0}(n+1)\).

An \(L_0\) onset at the first isolated-zero time is \(C_{T,0}(0)=1\) and
\(C_{k,0}(0)=0\) for all \(k>T\). Every finite seed has some finite \(T\)
at the onset of a hypothetical periodic-center regime.

## What is proved (algebraic)

**Lemma (every eventually periodic \(\sigma\) is Jen-excluded).** If
\(\sigma\) is eventually period \(m\), column \(-1\) is eventually period
\(9m\): \(\sigma\) on the isolated \(0\), and the forced word \(0^7 1\)
on the \(1\)-run. Column \(0\) is period \(9\). Kopra/Jen forbid that
adjacent pair for every nonzero finite seed. This includes constant
\(\sigma\) *and* periodic mixing such as \(0101\ldots\). Forcing constant
\(\sigma\) is unnecessarily strong.

**Lemma (\(C_2\) with a possibly mixing wrap).** Checked on all four
pairs \((\sigma_n,\sigma_{n+1})\):
\[
C_2(n)=\sigma_n\,111111\,0\,\overline{\sigma}_{n+1}.
\]
The constant-\(\sigma\) specializations recover the table in
`period9_q8.md`: \(111111100\) (\(\sigma=1\)) and \(011111101\)
(\(\sigma=0\)).

**Lemma (vacuum propagation).** If \(C_{k,0}(0)=0\) for every \(k>T\),
then \(C_{k,a}(0)=0\) for \(a=0,\ldots,8\) and \(k>T+a\), and
\(C_{k,0}(1)=0\) for \(k>T+8\). Iterating, \(C_{k,0}(n)=0\) for
\(k>T+9n\). A phase-\(0\) vacuum tail at \(n=0\) is therefore a moving
left vacuum of speed at most \(1\).

Proof: \(C_{k+1,0}(0)=C_{k,1}(0)\oplus(C_{k,0}(0)\lor C_{k-1,0}(0))\).
Once the two phase-\(0\) inputs vanish, the next phase-\(0\) bit equals
phase \(1\), and so on through phase \(8\). The phase-\(8\) wrap then
forces \(C_{k,0}(1)=0\).

## The \(20\)-state automaton is a full \(2\)-shift

The radius-\(6\) residual SCC has a \(20\)-state phase-\(0\) return
graph, six vertices with \(\sigma=0\) and fourteen with \(\sigma=1\),
one strongly connected \(9\)-step component, mix distance one
(`period9_q8.md`).

**Lemma (sigma language).** The labeled sofic shift is the full
\(2\)-shift. After a \(0\) the follower set is exactly the six
\(\sigma=0\) vertices; after a \(1\), exactly the fourteen
\(\sigma=1\) vertices; each of those two subsets has successors of both
labels, landing back on the same two subsets. Out-degree on the
\(20\)-state graph is \(6\)–\(14\).

So the radius-\(6\) return graph does **not** constrain \(\sigma\) as a
sequence. Internal states remain mixed and nondeterministic. Free-boundary
mixing at larger left radius (`period9_q8.md`, depth \(26\)) is the same
phenomenon and is **not** a construction of a seed orbit.

Any exclusion of an aperiodic \(\sigma\) has to come from reconstruction
together with finite left support, not from the strip label language.

## Reconstruction quotient (machine-checked, \(2^{18}\) states)

Pack \(S_k=(W_{k-1}(0),W_k(0))\in\{0,1\}^{18}\), where \(W_k(n)\) is the
\(9\)-bit word \((C_{k,0}(n),\ldots,C_{k,8}(n))\). One depth step is
\[
W_{k+1}(0)=\mathrm{pair\_step}\bigl(W_{k-1}(0),W_k(0),w_k\bigr),
\]
with wrap \(w_k=C_{k,0}(1)\). Wrap is a \(1\)-bit control. Let
\(Z^{(0)}=\{S:\text{bit }0\text{ of }W_k=0\}\) and
\[
Z^{(j+1)}=\{S\in Z^{(j)}:\exists\,w,\ \mathrm{succ}_w(S)\in Z^{(j)}\}.
\]
Sizes \(2^{17},2^{16},\ldots,2^{9}\). The sequence stabilizes at
\(j=8\): \(I:=Z^{(8)}\) has \(512\) states. Membership in every
\(Z^{(j)}\), including \(I\), is wrap-independent (both wraps remain in
\(Z^{(j-1)}\) whenever \(S\in Z^{(j)}\)).

Closed identities, checked by enumerating all \(2^{18}\) pairs:

| layer | extra constraint |
|------:|:---|
| \(Z^{(0)}\) | \(c_0=0\) |
| \(Z^{(1)}\) | \(c_1=p_0\) |
| \(Z^{(2)}\) | \(c_2=c_1\lor p_1\) |
| \(Z^{(3)}\) | \(c_3=c_1\oplus(c_2\lor p_2)\) |
| \(Z^{(4)}\) | \(c_4=c_2\oplus(c_3\lor p_3)\) |

Here \(p\) is the previous \(9\)-bit word and \(c\) the current one.
Inductively \(c_{a+1}=c_{a-1}\oplus(c_a\lor p_a)\) along the word, with
\(c_0=0\). A pair lies in \(Z^{(t)}\) iff it can keep phase \(0\) equal
to \(0\) for (at least) \(t\) further depth steps under *some* wrap
sequence. In particular a window of five consecutive phase-\(0\) zeros
starting at depth \(k\) places \(S_k\) in \(Z^{(4)}\); eight further
zeros place it in \(I\).

**Lemma (unique wrap on \(I\)).** Every state of \(I\) has exactly one
wrap that remains in \(I\) (\(293\) force wrap \(0\), \(219\) force wrap
\(1\)). The directed graph on \(I\) with that unique wrap is a functional
graph. It has a unique recurrent component: the vacuum pair
\((0^9,0^9)\) with wrap \(0\). Every other state of \(I\) reaches vacuum
in at most \(9\) steps. The current word is a function of the previous
word (\(512\) distinct previous words).

**Corollary (periodic labels on a vacuum tail).** Any wrap sequence that
keeps \(C_{k,0}(0)=0\) for all large \(k\) must enter \(I\), hence is
eventually \(0\), and \(W_k(0)\) is eventually \(0^9\). This is a
quotient of reconstruction whose only surviving recurrent component
forces a periodic *label* sequence (the wrap bits), even though the
ambient \(20\)-state strip automaton is nondeterministic on \(\sigma\).

The wrap \(w_k=C_{k,0}(1)\) is a sequence in the depth index \(k\), not
the mixing bit \(\sigma_n\) in the period index \(n\). Eventual
periodicity of wrap is **not** eventual periodicity of \(\sigma\).

## Consistent wrap does not enter \(I\) at checked depths

On a genuine spacetime the wrap is not a free control: \(w_k=C_{k,0}(1)\)
is the same reconstruction started at \(n=1\). Call a pair
*consistent* if it arises as \((W_{k-1}(0),W_k(0))\) from some binary
\(\sigma\).

**Checked through depth \(16\) (all \(2^{16}\) prefixes).** Every
consistent pair has controlled rank at most \(3\). None lie in \(I\).
The unique rank-\(3\) witness is the prefix \(0100000000\). Consequently
there is no window of five consecutive phase-\(0\) zeros in
\(C_{k,0}(0)\) for \(k\le 16\).

**Onset scan, all binary \(\sigma\).** For each \(T=1,\ldots,12\), the
system \(C_{T,0}(0)=1\) and \(C_{T+1,0}(0)=\cdots=C_{T+R,0}(0)=0\) is
unsatisfiable at some \(R\le 5\). The longest survivor is \(T=9\), killed
at \(R=5\).

These two tables are the same obstruction: rank \(\le 3\) forbids five
consecutive zeros, so an infinite \(L_0\) tail is impossible *inside the
checked depth*. They are not a \(T\)-independent proof. Free wrap *can*
enter \(I\) in \(9\) steps (the wrap delay across one period); the
correlation \(w_k=C_{k,0}(1)\) is what appears to block it. Rank
\(\le 3\) is not preserved under an arbitrary wrap, so the bound does not
close by a one-site induction.

## Constant \(\sigma\), read on the left

When \(\sigma\) is constant, wrap equals the phase-\(0\) bit of the same
site and the pair \((W_{k-1},W_k)\) is independent of \(n\). Both
\(\sigma=0\) and \(\sigma=1\) enter a spatial cycle of length \(135\)
(preperiods \(11\) and \(8\)) on which the phase-\(0\) bit is not
identically zero (\(64\) and \(65\) ones per cycle). So a constant
\(\sigma\) has no last \(1\) in \(C_{k,0}(0)\). Jen already excludes
this case; the left edge says the same thing.

## What this does not do

It does not exclude \(q=8\). It does not prove the target implication
\(L_0\Rightarrow\sigma\) eventually periodic. A proof of that implication
would exclude \(q=8\) for a finite seed, because every eventually
periodic \(\sigma\) is already Jen-killed. The reconstruction quotient
gives the implication only for the *wrap* sequence in the depth
direction. Lifting wrap-periodicity to \(\sigma\)-periodicity in \(n\)
fails as soon as the vacuum boundary is allowed to move.

If consistent pairs never enter \(I\) at any depth, then \(L_0\) is
impossible for every \(\sigma\) (no five consecutive phase-\(0\) zeros,
a fortiori no last \(1\) with an infinite vacuum tail). That would
exclude \(q=8\) without passing through periodicity of \(\sigma\). The
certificate stops at depth \(16\).

Left-only strip extension through depth \(26\) still mixes when the outer
bit is free. That over-approximation omits the infinite zero tail, which
is exactly the constraint encoded by \(I\). It is not a seed orbit.

## Strongest honest statement

For an eventual center \(011111111\), every eventually periodic mixing
bit \(\sigma\) is Jen/Kopra-excluded. The radius-\(6\) return graph does
not restrict \(\sigma\) at all. Finite left support at \(n=0\) forces,
in the \(18\)-bit reconstruction FSM, entry into a \(512\)-state
quotient on which the wrap label is eventually the constant \(0\) and
the \(9\)-bit word at \(n=0\) dies. Consistent \(\sigma\)-streams do not
enter that quotient through depth \(16\), and every onset width
\(T\le 12\) dies after at most five further zeros. None of this excludes
a finite seed with a large left-edge distance at onset.

## Reproduction

```
python3 research/period9_sigma.py
```
