# Cycle Y: spine reduction, Rule 150 ⊕ AND, sibling indices

One lemma that reduces an infinite 2-kernel to the dyadic centre bits;
one exact packed identity; the ideas22 index templates die. Not a prize
claim: \((c_{2^k})\) is still not proved to be non-eventually-constant.

Helper: `python3 research/cycle_y.py --certify`. Dump:
`research/cycle_y.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Green reconstruction of the centre from AND-injections
matches the packed generator on \(t<80\).

## 1. Lemma: spine reduction

Write \(v_k[n]=c_{n 2^k}\) and \(b_k=c_{2^k}=v_k[1]\). If \(v_k=v_{k+1}\)
as sequences, then \(v_k[n]=v_k[2n]\) for every \(n\), hence

\[
b_{k+j}=v_k[2^j]=v_k[1]=b_k\qquad(j\ge 0).
\]

So \(v_k=v_{k+1}\) forces \((b_j)_{j\ge k}\) to be constant. Conversely,
if \((b_k)\) is not eventually constant then \(v_k\ne v_{k+1}\) for every
\(k\). If moreover \((b_k)\) is not eventually periodic, it has
infinitely many distinct suffixes, and the suffix from index \(k\) is
\((v_k[2^j])_{j\ge 0}\), so \(\{v_k:k\ge 0\}\) is infinite. An infinite
2-kernel implies that \(c\) is not eventually periodic.

This is stronger than Cycle W’s observation that aperiodicity of
\((b_k)\) already implies aperiodicity of \(c\) (because \(2^k\bmod p\)
is eventually periodic). Here the same hypothesis yields an infinite
kernel, not merely aperiodicity. Certified: \(n_*=1\) iff
\(b_k\ne b_{k+1}\) on the scanned prefix; no \(v_k=v_{k+1}\) collision
through \(k=15\). On that prefix \(b_k\) takes both values (last 0 at
\(k=14\), last 1 at \(k=15\)). **Eventual constancy of \((b_k)\) remains
open.**

## 2. Lemma: packed Rule 30 is Rule 150 XOR adjacent AND

The packed step is
`row' = (row<<2) ^ ((row<<1)|row)`. Over \(\mathrm{GF}(2)\),
\(A\lor B=A\oplus B\oplus(A\land B)\), so

\[
\texttt{row}'=\texttt{r150(row)}\oplus\bigl((\texttt{row}{\ll}1)\land\texttt{row}\bigr),
\]

where \(\texttt{r150(row)}=(\texttt{row}{\ll}2)\oplus(\texttt{row}{\ll}1)\oplus\texttt{row}\)
is packed Rule 150 (\(x'=L\oplus C\oplus R\)). Checked on 30 steps from
the seed.

Rule 150 from a single 1 at the origin is spatially palindromic
(\(x(t,j)=x(t,-j)\) by induction). Hence \(\ell=r\) about the origin and
\(c'=\ell\oplus c\oplus r=c\). The centre is identically \(1\). Checked
on \(t<64\) (packed centre, naive spacetime, and palindrome).

Every centre 0 of Rule 30 is therefore a net odd contribution of the
AND injections, evolved linearly by Rule 150. Explicitly, writing
injections as the bits of \((\mathrm{row}_s{\ll}1)\land\mathrm{row}_s\)
placed at time \(s+1\),

\[
c_t=[x^t](1+x+x^2)^t\oplus\bigoplus_{(s,p)}\,[x^{t-p}](1+x+x^2)^{t-s},
\]

the first term being 1. Certified against `rule30_step` for \(t<80\).
This is a rewrite of \(c_t\), not a closed form for \(b_k\).

## 3. Sibling split indices (ideas22)

For sibling kernel columns at depth \(k\) (residues \(r\) and
\(r+2^k\)), the first disagreement \(n_*\) has worst value
\(1,3,6,5,7,4,6,8,9,11\) for \(k=1,\ldots,10\) (order \(k\), not a
proof of existence). None of the predicted indices
\(k,k-1,k+1\), Rowland’s right-diagonal period of index \(r\),
\(v_2(r+1)\), \(\mathrm{popcount}(r)\) splits every sibling pair.
The 4-point identity “\(c_r=c_{r+2^k}\) implies a split at \(n=1\)”
fails from \(k=2\) (2 failures, 73 at \(k=8\)). **Killed** as a
universal index.

## Verdict

`LEMMA` (spine reduction; Rule 150 centre; packed XOR-AND). `KILLED`
(sibling index templates, 4-point). `OPEN` (\((b_k)\) not eventually
constant). Wall time 0.24s. Prize unsolved.

## Files

- `research/cycle_y.md` (this note)
- `research/cycle_y.py`
- `research/cycle_y.json`
