# 2-kernel / k-automaticity of the Rule 30 centre

Attack on prize problem 1 via the 2-kernel of the centre sequence \(c\),
the unused “Cobham morphism at \(n\) and \(2n+1\)” item. This is not
linear complexity \(L(N)\), not substitution tilings, not time-digit
matrices, and not the bivariate Cartier attack on \(U(z,w)\) in
[cartier_kernel.md](cartier_kernel.md). No infinite kernel is proved.
This is not a prize claim.

Certifier: `research/two_kernel.py`. Dump: `research/two_kernel.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

Packed generator: `row=1`; `row=(row<<2)^((row<<1)|row)`; bit \(t\) is
`(row>>t)&1`. Centre bits match `experiment.center_bits` on a prefix of
length 256, and match the known 20-bit word
`11011100110001011001`.

## Kill criterion (predeclared)

- If the number of distinct length-128 prefixes saturates at some
  \(K_0\le 64\) for all larger \(k\) that the data supports, the
  finite-kernel hypothesis survives the screen (then try to identify a
  2-DFA; if you cannot, still report saturation). A finite kernel does
  **not** prove periodicity (Thue–Morse), so that is **not** a prize
  claim; it kills this route as a nonperiodicity proof unless you can
  still prove that the identified automatic sequence is not eventually
  periodic **and** equals \(c\), which is a much stronger claim — do
  not claim it without a proof.
- If distinct prefixes grow like \(2^k\) (full kernel) through \(k=12\),
  the screen does not kill automaticity of a possibly large finite
  kernel, and also does **not** prove an infinite kernel. Optionally try
  a structural lemma (a family \(r_k\) where kernel words disagree at a
  predicted index using the CA). If no lemma, kill the
  “proof via automaticity” route.

## Target

An eventually periodic sequence is \(k\)-automatic for every \(k\),
hence has a finite 2-kernel. The 2-kernel of \(c\) is

\[
\bigl\{\,(c_{2^k n+r})_{n\ge 0}:k\ge 0,\; 0\le r<2^k\,\bigr\}.
\]

A sequence over a finite alphabet is 2-automatic iff its 2-kernel is
finite (Christol; Allouche–Shallit). Equivalently, \(c\) is the coding
of a fixed point of a 2-uniform morphism (Cobham). The even/odd
sampling

\[
n\;\longmapsto\;(c_{2n},\,c_{2n+1})
\]

is then a length-2 morphism on the hidden alphabet, whose letters are
the kernel states. If the kernel is infinite, \(c\) is not 2-automatic,
hence not eventually periodic.

A finite kernel does not prove periodicity: Thue–Morse has kernel size
2 and is not eventually periodic. An infinite kernel on a finite prefix
table is also not proved by counting: automatic sequences may have
arbitrarily large finite kernels.

This experiment is a 1-D kernel screen of \(c\) itself. It does not
use Cartier operators on the bivariate series \(U(z,w)\), mixed
diagonals \(x(t,\pm 1)\), or the \(R\)-hierarchy.

## Experiment

\(N=2^{19}=524288\) centre bits. For each \(k\) with \(2^k L\le N\),
the length-\(L\) prefix of every kernel sequence \(c[2^k n+r]\) is
packed as an integer. Distinct prefixes are counted at \(L=64\) and
\(L=128\). New prefixes versus the \((k-1)\)-kernel (and versus the
union of all shallower kernels) measure decimation consistency.
Closure: the even/odd decimation of \((k,r)\) equals \((k+1,r)\) and
\((k+1,r+2^k)\). The same screen is run for the 3-kernel.

Controls, run on the same counter: Thue–Morse saturates at 2 distinct
length-128 prefixes for every \(k\ge 1\); the purely periodic word
`01` saturates at 2 from \(k=1\).

Wall time: **21.4 s** total (18.0 s generating the packed row; kernel
counts, closures, and morphism windows under 4 s). Stdlib only.

## Distinct 2-kernel prefixes

Every supported depth is a full kernel: \(\#=\ 2^k\) distinct prefixes,
and all of them are new relative to depth \(k-1\) and to the union of
shallower depths. Birthday expectation at \(k=12\), \(L=128\) is
\(4096^2/2^{129}\sim 10^{-32}\). No saturation at any \(K_0\le 64\).

| \(k\) | residues \(2^k\) | distinct \(L=64\) | new vs \(k-1\) | distinct \(L=128\) | new vs \(k-1\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 2 | 2 | 2 | 2 | 2 |
| 2 | 4 | 4 | 4 | 4 | 4 |
| 3 | 8 | 8 | 8 | 8 | 8 |
| 4 | 16 | 16 | 16 | 16 | 16 |
| 5 | 32 | 32 | 32 | 32 | 32 |
| 6 | 64 | 64 | 64 | 64 | 64 |
| 7 | 128 | 128 | 128 | 128 | 128 |
| 8 | 256 | 256 | 256 | 256 | 256 |
| 9 | 512 | 512 | 512 | 512 | 512 |
| 10 | 1024 | 1024 | 1024 | 1024 | 1024 |
| 11 | 2048 | 2048 | 2048 | 2048 | 2048 |
| 12 | 4096 | 4096 | 4096 | 4096 | 4096 |
| 13 | 8192 | 8192 | 8192 | — | — |

\(L=128\) is supported through \(k=12\) (\(128\cdot 2^{12}=N\)); \(L=64\)
through \(k=13\). Union of all observed \(L=128\) prefixes:
\(2^{13}-1=8191\). Union at \(L=64\): \(2^{14}-1=16383\).

2-kernel closure holds at every supported parent depth (0 mismatches).
No 2-DFA is identified: any 2-automaton consistent with these prefixes
needs at least 4096 states.

## Cobham morphism at \(n\) and \(2n+1\)

If \(c\) were a 2-uniform morphic sequence on the visible bits, the
pair \((c_{2n},c_{2n+1})\) would be a function of a finite window of
\(c\) about \(n\). That fails at radius 0 on the second sample:
\(c_0=1\) gives \((c_0,c_1)=(1,1)\), while \(c_1=1\) gives
\((c_2,c_3)=(0,1)\). The same map remains inconsistent for every
window radius \(0\le r\le 8\) (111{,}858 conflicts at radius 8 among
262{,}136 samples). Restricting the output to \(c_{2n+1}\) alone is
inconsistent at every such radius (first conflict at \(n=3\) for
radius 0).

A hidden alphabet of size \(q\) could still generate \(c\). The kernel
count forces \(q\ge 4096\) on this prefix. That breaks every small
Cobham morphism. It does not break automaticity.

## 3-kernel (optional)

Same full-kernel pattern: distinct length-128 prefixes equal \(3^k\)
through \(k=7\) (\(3^7=2187\)), and length-64 prefixes through \(k=8\)
(\(3^8=6561\)). All new versus the previous depth. 3-kernel closure
holds (child residue \(r+d\cdot 3^k\)). Cobham’s theorem on
multiplicatively independent bases is not available: neither kernel is
shown finite.

## Structural lemma screen

The even-decimation chain \(v_k=(c_{2^k n})_{n\ge 0}\) is pairwise
distinct on the computed range, but the first disagreement index
between \(v_k\) and \(v_{k+1}\) is not constant:

\[
n_*=1,1,3,2,1,1,3,2,1,1,1,1,2,1,1,2,1,1
\quad(k=0,\ldots,17).
\]

The candidate \(n=1\) (i.e. \(c(2^k)\ne c(2^{k+1})\)) already fails
at \(k=2\) (\(c(4)=c(8)=1\)). The same holds for \(n=3,5,7\). The
all-ones residues \(r=2^k-1\) and the sibling pair
\((k,0)\) vs \((k,2^{k-1})\) likewise have no uniform disagreement
index. No CA identity was found that predicts a witness index for
every \(k\). A finite table of first disagreements is not a lemma.

## Why this route died

The second predeclared bullet fires. Distinct length-128 prefixes grow
like \(2^k\) through \(k=12\) (and like \(2^k\) through \(k=13\) at
\(L=64\)). Saturation at \(K_0\le 64\) did not occur, so a 2-kernel of
size \(\le 64\) is incompatible with these prefixes — but that is a
finite lower bound \(|K|\ge 4096\), not an infinite family. Automatic
sequences may have arbitrarily large finite kernels. No structural
lemma supplies a predicted disagreement for a one-parameter family
\(r_k\).

Kill the proof-via-automaticity route. Nonautomaticity is not proved.
Eventual periodicity of \(c\) remains open. Not a prize claim.

## What was obtained

- Birthday-safe full 2-kernel on length-128 prefixes through depth 12
  (\(N=2^{19}\)), and on length-64 prefixes through depth 13.
- Matching full 3-kernel through depth 7 (\(L=128\)) / 8 (\(L=64\)).
- Verified 2-kernel and 3-kernel closure, and a broken visible-bit
  Cobham map \(n\mapsto(c_{2n},c_{2n+1})\) at every radius \(\le 8\).
- No 2-DFA, no uniform witness index, no lemma.
