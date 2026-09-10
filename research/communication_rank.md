# Communication rank of the Rule 30 apex

Attack on prize problem 3, as specified in [_astra_ideas6.md](_astra_ideas6.md)
item 1. Exact \(\mathrm{GF}(2)\) ranks of the three spatial splits of \(f_h\)
were computed for \(h=2,\ldots,10\). The prototype envelope \(r_h\le 8h\)
fails on a required neighbouring split at \(h=9\) and \(h=10\). This is not
a prize claim.

Certifier: `research/communication_rank.py`. Dump:
`research/communication_rank.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

The historical lead is Goles, Meunier, Rapaport, Theyssier,
*Communications in cellular automata*,
[arXiv:0906.3284](https://arxiv.org/abs/0906.3284) §4.4. They recorded
Rule 30 as an experimental candidate for high one-round communication
complexity together with low matrix rank (suggesting cheap multi-round
protocols). That was not a theorem. The present measurement is the
\(\mathrm{GF}(2)\) rank needed for an XOR-of-products factorisation, on
the central split they used and on its two neighbours.

## Apex and splits

Rule 30 is \(x_{t+1,j}=x_{t,j-1}\oplus(x_{t,j}\lor x_{t,j+1})\). For an
arbitrary bottom word of length \(2h+1\), the apex \(f_h\) is the leftover
bit after \(h\) shrinking steps: each step maps a word
\(x_0\ldots x_{n-1}\) to the length-\(n-2\) word with

\[
y_i=x_i\oplus(x_{i+1}\lor x_{i+2}).
\]

The \(2h+1\) cells are the full neighbourhood of the apex, so the local
rule never reads outside the word. Vacuum padding of extra zeros gives
the same centre bit; extra live cells are not introduced.

Write \(f_h(uv)\) for the concatenation of a left block \(u\) and a right
block \(v\). The Boolean communication matrix is \(M_h(u,v)=f_h(uv)\).
Three splits are required, all with both sides nonempty for \(h\ge 2\):

- centre: \((|u|,|v|)=(h,h+1)\),
- left of centre: \((h-1,h+2)\),
- right of centre: \((h+1,h)\).

Bits are packed with the LSB equal to the leftmost cell of that half.
Ranks are exact, by Gaussian elimination on bitset rows over
\(\mathrm{GF}(2)\). The field is \(\mathrm{GF}(2)\) because a rank-\(r\)
factorisation is an identity

\[
f_h(uv)=\bigoplus_{i=1}^{r}A_{h,i}(u)\,B_{h,i}(v).
\]

A row-space basis supplies such \(A,B\). Self-checks: packed single-seed
evolution `row = (row<<2)^((row<<1)|row)` and `experiment.center_bits`
agree with \(f_h\) on the seed triangle word for \(h=1,\ldots,12\);
tuple shrinking matches the packed map exhaustively through \(h=4\);
zero-padding the window agrees with shrinking; each central
factorisation reconstructs its matrix.

## Ranks versus \(8h\)

| \(h\) | \(8h\) | rank \((h-1,h+2)\) | rank \((h,h+1)\) | rank \((h+1,h)\) |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 16 | 2 | 3 | 2 |
| 3 | 24 | 3 | 4 | 4 |
| 4 | 32 | 4 | 7 | 5 |
| 5 | 40 | 7 | 10 | 9 |
| 6 | 48 | 12 | 19 | 12 |
| 7 | 56 | 23 | 26 | 19 |
| 8 | 64 | 44 | 39 | 26 |
| 9 | 72 | **79** | 53 | 39 |
| 10 | 80 | **104** | 79 | 53 |

Boldface exceeds \(8h\). The central split stays just under the envelope
at \(h=10\) (\(79\le 80\)). The left-of-centre split does not:
\(\mathrm{rk}(M_9^{(8,11)})=79>72\) and
\(\mathrm{rk}(M_{10}^{(9,12)})=104>80\). One-round cost
\(\mathbf{cc}_1=\lceil\log_2 d\rceil\), with \(d\) the minimum of the
numbers of distinct rows and distinct columns (Goles et al., Fact 1),
remains \(6\) or \(7\) on every \(h=10\) split. Rank is not \(O(\log d)\).

On the central split the number of distinct rows is \(2^h\) through
\(h=8\), then \(506\) of \(512\) at \(h=9\) and \(1010\) of \(1024\) at
\(h=10\). Alice’s rows are essentially all different. The cheap one-round
direction is Bob’s, whose column types grow as \(3,4,9,11,20,26,42,54,85\).

Algebraic degree of \(f_h\) itself is \(2h-1\) on \(2h+1\) inputs
(\(10,30,122,1360,23094,79192,324572\) ANF terms at
\(h=2,3,4,6,8,9,10\)).

## Factorisation at \(h=2\)

Smallest \(h\) in the range; central rank \(r=3\). The \(4\times 8\)
matrix, rows indexed by \(u=u_0u_1\in\{0,1\}^2\) and columns by
\(v=v_0v_1v_2\in\{0,1\}^3\), LSB leftmost, is

\[
\begin{pmatrix}
0&0&1&0&1&0&1&0\\
1&1&0&1&0&1&0&1\\
0&0&0&1&0&1&0&1\\
1&1&1&0&1&0&1&0
\end{pmatrix}.
\]

Row \(11\) is the \(\mathrm{GF}(2)\)-sum of the other three. A basis of
rows \(\{01,00,10\}\) gives

\begin{align*}
A_0(u)&=u_0,\\
A_1(u)&=1+u_0+u_1,\\
A_2(u)&=u_1,
\end{align*}

and cubic \(B_i(v)\),

\begin{align*}
B_0&=1+v_1+v_0v_1+v_2+v_0v_2+v_1v_2+v_0v_1v_2,\\
B_1&=v_1+v_0v_1+v_2+v_0v_2+v_1v_2+v_0v_1v_2,\\
B_2&=v_0v_1+v_0v_2+v_0v_1v_2.
\end{align*}

The identity \(f_2(uv)=\bigoplus_{i=0}^{2}A_i(u)B_i(v)\) holds on all
\(32\) words. Already at \(h=2\) the \(B_i\) are full-degree truth tables
on the right half, not a recursive local rule.

Central factorisations were extracted and checked for every \(h\le 10\).
The feature ANFs do not stay affine: at \(h=10\) the maps \(A_i\) have
degree \(7\)–\(8\) (up to \(224\) terms) and the maps \(B_i\) have degree
\(6\)–\(11\) (up to \(1714\) terms). Evaluation is a \(2^{\Theta(h)}\)
table, or else the original cone.

## Why it died

The assignment froze the prototype at \(r_h\le 8h\) on every required
split. That envelope is false at \(h=9\) and \(h=10\) for
\((|u|,|v|)=(h-1,h+2)\).

The surviving central and right-of-centre ranks do not yield recursively
computable features. Joining two time blocks of height \(h\) to make
height \(2h\) still produces a middle word of length \(2h+1\), which is
the shrinking evolution of the bottom cone. Using that middle word as the
input to the height-\(h\) factorisation is exactly “simulate the cone”.
The extracted \(A,B\) are coordinates in a row-space basis: they are
indexed by the \(2^h\) (resp. \(2^{h+1}\)) half-words. Composition was
not a separate survival test, because the rank envelope had already
failed; those feature spaces would have failed the remaining kill
criteria in any case.

Low \(\mathbf{cc}_1\) in Bob’s direction with rank \(\Theta(h)\) to
\(\omega(h)\) is not a cheap predictor of the seed apex. Rank above
\(8h\) on a required split kills the prototype. Not a prize claim.
