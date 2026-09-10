# CFG parse-parity of \(\mathrm{bin}(n)\)

Attack on prize problem 3, as specified in [_astra_ideas7.md](_astra_ideas7.md)
item 4. No Chomsky grammar in the frozen family realises the Rule 30
centre as the GF(2) parse count of canonical binary indices. This is
not a prize claim.

Certifier: `research/cfg_parse_parity.py`. Dump:
`research/cfg_parse_parity.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Family

Four nonterminals, start symbol \(0\), at most eight binary productions
\(X\to YZ\), and terminal productions \(X\to 0\) and/or \(X\to 1\).
Empty and unit productions are forbidden, so every word has finitely
many parses. The target is
\[
c_n=\#\{\text{parses of }\operatorname{bin}(n)\}\pmod 2,
\]
with \(\operatorname{bin}(n)\) written without leading zeros. \(n=0\) is
omitted: \(\varepsilon\) is forbidden and \(\operatorname{bin}(0)=0\) is
a special one-bit word. Constraints run on \(n=1,\ldots,1023\), then
any survivor would be tested through \(2^{16}-1\).

Centre bits match `experiment.center_bits` on a prefix of length 256.
A scalar CYK agrees with a naive parse counter on a 2-nonterminal
test grammar. An independent Python enumeration of every 2-nonterminal
grammar finds no fit on \(n=1,\ldots,31\).

## Search

Z3 on a direct CYK encoding stalls by length 5. The certifier instead
enumerates every binary-production subset of size \(\le 8\) and, for
each subset, evaluates all \(2^{2r}\) terminal assignments at once by
bit-sliced CYK over \(\mathrm{GF}(2)\). OpenMP splits the combination
tree on the first production index. Synthesis is capped at two hours.

## Outcome

| nonterminals | max binary prods | subsets checked | \(n=1..1023\) | wall |
| ---: | ---: | ---: | --- | ---: |
| 2 | 8 | 256 | unsat | 0.09 s |
| 3 | 6 | 397{,}594 | unsat | 0.11 s |
| 3 | 8 | 3{,}505{,}699 | unsat | 0.56 s |
| 4 | 6 | 83{,}278{,}001 | unsat | 7.1 s |
| **4** | **8** | **5{,}130{,}659{,}561** | **unsat** | **644 s** |

The declared kill family is the last row. Nested smaller freezes (3
nonterminals and/or 6 productions, and the 2-nonterminal screen) are
unsat as well. No grammar reached the hold-out. Total wall time 652 s.

## Why it died

Preregistered kill: unsatisfiable bounded grammar constraints, any
held-out mismatch, or no candidate in the cap. The first clause fires:
there is no 4-nonterminal, \(\le 8\)-binary-production grammar whose
parse parity on canonical \(\operatorname{bin}(n)\) equals \(c_n\) for
all \(n=1,\ldots,1023\). Productions indexed by \(n\) or imported rows
were never in the family. Not a prize claim.
