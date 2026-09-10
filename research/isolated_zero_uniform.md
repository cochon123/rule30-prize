# Uniform radius-6 certificate for isolated zeros \(01^q\)

## Theorem

Let \(G_q\) be the radius-6 strip graph of `strip_graph.graph` for the
imposed center word \(01^q\) (width 13, arbitrary outer bits). Write
columns \(-6,\ldots,+6\) of a row as a 13-bit string, bit \(0\) on the
left. The left neighbor of the center is bit \(5\).

**Theorem.** For every integer \(q=7\) and every \(q\ge 9\):

1. \(G_q\) has a unique recurrent strongly connected component \(U_q\);
2. \(U_q\) meets every phase and has graph period \(q+1\);
3. every vertex of \(U_q\) at phase \(0\) (the isolated \(0\)) has left
   neighbor \(1\);
4. on the \(1\)-run the left neighbor is the locally forced word
   \(0^{q-1}1\).

Jen/Kopra therefore exclude an eventual \(01^q\) tail of the finite
nonzero seed: columns \(-1\) and \(0\) would both be eventually
periodic.

The case \(q=8\) (period \(9\)) is a genuine exception at this radius:
the unique recurrent component still admits both left-neighbor bits at
phase \(0\).

**Status.** All \(q\ge 9\) are proved, not merely enumerated up to \(30\).
The infinite tail \(q\ge 17\) is a uniform finite-gadget argument. The
eight values \(9\le q\le 16\) are finite graphs, checked by the same
code as \(q=7\). Helper: `research/isolated_zero_uniform.py`.

## Notation

Rule 30 on the strip: interior bits of the next row are
\(x_{t+1,j}=x_{t,j-1}\oplus(x_{t,j}\lor x_{t,j+1})\) for
\(j\in\{-5,\ldots,+5\}\). The two outer bits of the next row are free
in \(G_q\). Center bits are imposed by the phase.

A \(1\to 1\) transition requires left neighbor \(0\). A \(1\to 0\)
transition requires left neighbor \(1\). On a \(0\to 1\) transition the
phase-\(0\) left bit equals \(1\oplus r_t\), equivalently
\(\mathrm{NOT}\) of bit \(4\) of the preceding last-\(1\) row.

Write \(C\) for the \(14\)-row **cruise** and \(Z\), \(L\) for the
phase-\(0\) and last-\(1\) layers of the large-\(q\) component. Each is
a single \(9\)-bit prefix times the fourteen \(4\)-bit suffixes that
omit `1100` and `1101`.

## The \(14\)-state cruise

Prefix `101010101` (columns \(-6,\ldots,+2\)). Left neighbor \(0\),
center \(1\). Rightmost four bits omit `1100` and `1101`:

```
1010101010000
1010101011000
1010101010100
1010101010010
1010101011010
1010101010110
1010101011110
1010101010001
1010101011001
1010101010101
1010101010011
1010101011011
1010101010111
1010101011111
```

Unconstrained \(1\to 1\) successors of \(C\) split by the free left
outer bit:

- left outer \(1\): **stay**, image exactly \(C\);
- left outer \(0\): **exit**, image the \(14\)-row layer with prefix
  `001010101`.

Among all \(512\) possible \(9\)-bit prefixes, `101010101` is the
**unique** \(1\to 1\) self-loop. That is why extra \(1\)s, once the
component has entered \(C\), can only insert copies of this same
\(14\)-set.

On stay (and on every other \(14\)-state layer with the same omitted
suffixes) the right \(4\) bits evolve by the same out-degree-\(2\) map,
independent of the prefix:

```
0000 -> 1000, 1001
1000 -> 0100, 0101
0100 -> 0110, 0111
0010 -> 1110, 1111
1010 -> 0010, 0011
0110 -> 0100, 0101
1110 -> 0000, 0001
0001 -> 1010, 1011
1001 -> 0110, 0111
0101 -> 0100, 0101
0011 -> 1110, 1111
1011 -> 0010, 0011
0111 -> 0100, 0101
1111 -> 0000, 0001
```

## Wrap-through-zero gadget

For every \(q\ge 17\) the unique recurrent component is the circular
composition

\[
Z=G_0 \to G_1 \to \cdots \to G_{10} \to
\underbrace{C\to\cdots\to C}_{q-16\text{ copies}} \to
E_1\to E_2\to E_3\to E_4\to E_5\to L \to Z.
\]

Each arrow is a subset of the radius-\(6\) strip relation, with every
vertex of out-degree exactly \(2\) and image equal to the next layer.
Size \(|U_q|=14q+74\).

### Post-zero layers \(G_0,\ldots,G_{10}\) (independent of \(q\ge 16\))

Phase \(0\) is \(Z\), prefix `101011001`, left neighbor \(1\):

```
1010110010000
1010110011000
1010110010100
1010110010010
1010110011010
1010110010110
1010110011110
1010110010001
1010110011001
1010110010101
1010110010011
1010110011011
1010110010111
1010110011111
```

Then (prefixes; full row lists in `isolated_zero_uniform.json`):

| phase | n | left | prefixes |
|------:|--:|:----:|----------|
| 0 | 14 | 1 | `101011001` |
| 1 | 14 | 0 | `101010111` |
| 2 | 14 | 0 | `101010100` |
| 3 | 18 | 0 | `101010110`, `101010111` |
| 4 | 20 | 0 | `101010100`, `101010101` |
| 5 | 28 | 0 | `101010101`, `101010110`, `101010111` |
| 6 | 24 | 0 | `101010100`, `101010101` |
| 7 | 26 | 0 | `101010101`, `101010110`, `101010111` |
| 8 | 20 | 0 | `101010100`, `101010101` |
| 9 | 20 | 0 | `101010101`, `101010110` |
| 10 | 16 | 0 | `101010101` (all 16 suffixes) |

Phase \(1\), prefix `101010111`, omit `1100`,`1101`:

```
1010101110000
1010101111000
1010101110100
1010101110010
1010101111010
1010101110110
1010101111110
1010101110001
1010101111001
1010101110101
1010101110011
1010101111011
1010101110111
1010101111111
```

Phase \(2\), prefix `101010100`, omit `1100`,`1101`:

```
1010101000000
1010101001000
1010101000100
1010101000010
1010101001010
1010101000110
1010101001110
1010101000001
1010101001001
1010101000101
1010101000011
1010101001011
1010101000111
1010101001111
```

The bump at phases \(3\)–\(10\) is where bit \(8\) of the prefix is
\(0\), so the right-hand bits leak into the left \(9\). After phase
\(10\) the prefix has locked onto the cruise self-loop and the extra
suffixes of \(G_{10}\) are dropped: \(G_{10}\to C\).

### Pre-wrap \(E_1,\ldots,E_5,L\) (last six \(1\)s, independent of \(q\ge 16\))

Exit from \(C\) (left outer \(0\)) starts a deterministic \(9\)-bit
countdown. Each layer is \(14\) rows, omit `1100`,`1101`:

```
E1  001010101   (phase q-5)
E2  011010101   (phase q-4)
E3  010010101   (phase q-3)
E4  111110101   (phase q-2)
E5  100000101   (phase q-1)
L   110001101   (phase q, left neighbor 1)
```

Explicit rows of \(L\):

```
1100011010000
1100011011000
1100011010100
1100011010010
1100011011010
1100011010110
1100011011110
1100011010001
1100011011001
1100011010101
1100011010011
1100011011011
1100011010111
1100011011111
```

\(L\) has bit \(4=0\), so every \(1\to 0\) successor has left neighbor
\(1\). Unconstrained those successors occupy two prefixes
`001011001` and `101011001`; the recurrent component keeps only \(Z\).

The other five exit layers are the same \(14\) suffixes under the
prefixes above (dumped in the JSON under q=18 phases \(13\)–\(17\)).

## Proof for \(q\ge 17\)

**Lemma A (unique cruise).** The only \(9\)-bit prefix \(P\) that is a
\(1\to 1\) self-loop is `101010101`. Checked by enumerating all \(512\)
prefixes. Thus a long \(1\)-run in a recurrent component can occupy a
constant left-\(9\) block for many consecutive phases only by sitting
in \(C\).

**Lemma B (exit tree).** From \(C\), each unconstrained \(1\to 1\) step
has two next prefixes (the free left outer bit). Staying chooses
`101010101`; exiting chooses `001010101`. After exactly six
non-self-loop steps every reachable prefix has the form
`*****1101` with bit \(5=1\) (legal \(1\to 0\)), and there are
\(32\) such prefixes. None of them admits a further \(1\to 1\)
successor. So a path that has entered \(C\) can wrap through the
isolated \(0\) only by taking some \(6\)-step exit after any number of
stays.

**Lemma C (unique living wrap).** For each of those \(32\) prefixes,
form all \(1\to 0\) successors, then one \(0\to 1\) and ten further
\(1\to 1\) steps (enough to reach phase \(11\), where \(C\) lives).
**Only** prefix `110001101` \(=L\) has nonempty image, and that image
meets \(C\). The other \(31\), including every prefix with bit \(4=1\)
(which would put left neighbor \(0\) on the isolated \(0\)), die: no
legal continuation through eleven imposed center bits. This check is
independent of \(q\).

**Lemma D (countdown is forced).** Therefore any infinite path in
\(G_q\) that occupies \(C\) and completes a period of length \(q+1\ge 18\)
must, after the last stay in \(C\), follow the unique \(6\)-step exit
that lands on \(L\), wrap into \(Z\), and return. The left outer bits
along that exit are exactly the pre-wrap prefixes \(E_1,\ldots,E_5,L\).
In particular the phase-\(0\) left neighbor is constantly \(1\).

**Lemma E (assembly of \(U_q\)).** Let \(V_q\) be the vertex set of the
circular composition displayed above, with \(q-16\) copies of \(C\).
The post-zero layers \(G_0,\ldots,G_{10}\) and the pre-wrap are the
phase slices of the unique recurrent component of \(G_{18}\), hence are
closed under the \(q\)-independent relations \(0\to 1\), \(1\to 1\),
and \(1\to 0\). Stay on \(C\) is an onto self-map; exit \(C\to E_1\)
is onto. So \(V_q\) is forward-closed in the induced subgraph, every
vertex has out-degree \(2\), and the image of each layer is the next
layer. It is strongly connected: the gadget through \(Z\) mixes the
fourteen suffixes once per period (already one SCC at \(q=17\)), and
inserting extra onto self-maps of \(C\) cannot split that mixing.

**Lemma F (nothing else is recurrent).** A recurrent path must wrap, so
its last-\(1\) row has bit \(5=1\). After the post-zero gadget it must
occupy a \(1\to 1\) self-loop in order to fill the \(q-16\) intermediate
phases; by Lemma A that loop is \(C\). Lemma D then forces the rest of
the path to lie in \(V_q\). Hence \(U_q=V_q\).

**Induction on extra cruise layers.** The step \(q\mapsto q+1\) inserts
one more stay \(C\to C\) between \(G_{10}\) and the pre-wrap. It does
not change \(Z\) or \(L\). By Lemma C no new living wrap appears, so
the phase-\(0\) left bit cannot un-freeze. This is the requested
induction: adding one \(1\to 1\) cruise layer cannot un-force the left
bit.

## Finite range \(9\le q\le 16\), and \(q=7\)

These are eight plus one finite directed graphs, each with
\((q+1)2^{13}\) vertices. Full Tarjan SCC plus the forced-column test
of `strip_graph.analyze` gives a unique recurrent component, graph
period \(q+1\), and left neighbor \(1\) at phase \(0\). The same run
shows \(|U_q|=14q+74\) already for \(q\ge 9\), with the bump still
migrating toward the wrap and \(C\) not yet occupying a positive-length
stay block (the first \(14\)-state copy of prefix `101010101` appears
at \(q=17\), phase \(11\)).

Independently re-checked in this work: \(q=7,9,10,11,17,18,31,40\).
At \(q=31\) and \(q=40\) the enumerated component equals the predicted
\(V_q\) exactly (sizes \(508\) and \(634\)).

## The \(q=8\) exception

Period \(9\) is too short to enter \(C\). The unique recurrent
component of \(G_8\) still has a last-\(1\) branch that the
length-\(6\) exit tree from \(C\) never uses:

```
0001111000000
0001111000010
0001111000001
0001111000011
```

These four rows have bit \(4=1\), so they \(1\to 0\) to phase-\(0\)
rows with left neighbor \(0\) and prefix `101100010`:

```
1011000100000
1011000100010
1011000100110
1011000100001
1011000100011
1011000100111
```

The same component also contains the “good” last-\(1\) prefix
`110001101` and the corresponding phase-\(0\) rows of \(Z\) (left
neighbor \(1\)). Both left bits therefore survive at phase \(0\).

That extra last-\(1\) prefix is **not** a \(1\to 1\) successor of the
\(q=9\) last-\(1\) layer. One additional \(1\) kills it, and Lemmas
B–C prevent it from returning for any larger \(q\): from \(C\) it is
not a living wrap, and \(C\) is the only long-run self-loop.

Modular origin: wrapable prefixes reachable from the *post-zero*
prefix `101010111` include `000111100` at distance \(7\), with bit
\(4=1\). Period \(9\) is exactly long enough for that distance-\(7\)
branch to close through the isolated \(0\), and too short for the
cruise self-loop to filter it. That is a length obstruction, not an
artifact of a \(q\le 30\) cutoff.

## What this does not do

It does not exclude \(q\in\{1,2,3,4,5,6,8\}\). It does not force a
`00` or `11` in an eventual period. Isolated ones \(0^q 1\) remain a
separate family.

## Reproduction

```
python3 research/isolated_zero_uniform.py
```

Uses `strip_graph.graph` / `components` / `analyze` and does not
modify `strip_graph.py`. Dumps: `research/isolated_zero_uniform.json`.
