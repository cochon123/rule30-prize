# Time-digit linear representations of \(c_n\)

Attack on prize problem 3, as specified in [_astra_ideas7.md](_astra_ideas7.md)
item 2. Concatenation matrices over \(\mathbb F_3\) have rank above 16
from \(\ell=5\) onward. No 16-dimensional digit representation exists
in this family. This is not a prize claim.

Certifier: `research/time_digit_matrices.py`. Dump:
`research/time_digit_matrices.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Family

MSB-first binary digits \(b_1\cdots b_m=\mathrm{bin}(n)\). A linear
representation of dimension \(r\) over \(\mathbb F_3\) is
\(c_n=\lambda^\top M_{b_1}\cdots M_{b_m}\rho\) with the output always
in \(\{0,1\}\). Concatenation then factors as
\(H(u,v)=(\lambda^\top M_u)(M_v\rho)\), so
\(\mathrm{rk}\,H\le r\). The assignment froze \(r\le 16\). Leading zeros
are included as extra left factors of length \(<\ell\).

This is a representation of the **time index**, not of a spatial cut of
the apex \(f_h\). Centre bits through \(2^{14}\) suffice for \(\ell\le 7\).
They match `experiment.center_bits` on a prefix of length 256.

## Ranks over \(\mathbb F_3\)

| \(\ell\) | rank \(H_\ell\) \(2^\ell\times 2^\ell\) | rank split \((\ell-1,\ell+1)\) | rank with leading-zero rows | cap 16 |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 3 | 2 | 3 | yes |
| 3 | 7 | 4 | 7 | yes |
| 4 | 15 | 8 | 15 | yes |
| 5 | **32** | 16 | **32** | no |
| 6 | **64** | **32** | **64** | no |
| 7 | **128** | **64** | **128** | no |

From \(\ell=5\) the square block is full rank \(2^\ell\). Leading zeros
do not collapse rows. The neighbour split already exceeds 16 at
\(\ell=6\).

## Why it died

Preregistered kill: any rank above 16 excludes the family. First
violation is \(\ell=5\), rank 32. There is nothing to reconstruct and no
induction to Rule 30. An \(O(\log n)\) evaluator in this dimension bound
does not exist. Not a prize claim.
