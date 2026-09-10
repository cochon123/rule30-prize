# Adaptive Boolean certificates for \(c_n\)

Attack on prize problem 3 via data-dependent short-circuit certificates
of the spacetime circuit, as specified in
[_astra_ideas5.md](_astra_ideas5.md) item 3. No subquadratic evaluator
was obtained. This is not a prize claim, and the finite cutoff below is
not a general complexity lower bound.

Helper: `python3 research/adaptive_certificate.py`. Dump:
`research/adaptive_certificate.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`. Packed evolution is checked
against the local rule on every evolved cell with \(t\le n\), and every
evaluator is checked against the packed centre bit.

## Model

\[
x(t+1,j)=x(t,j-1)\oplus\bigl(x(t,j)\lor x(t,j+1)\bigr),
\qquad
x(0,j)=\mathbf{1}_{j=0},\qquad
c_n=x(n,0).
\]

Each evolved cell \((t,j)\) with \(t\ge 1\) and \(|j|\le t\) is one
internal gate. Seed cells and vacuum \(|j|>t\) are free. Evaluating
\(a\oplus(b\lor c)\) always requires \(a\). The OR is certified by a
single input equal to \(1\); OR \(=0\) requires both inputs. Shared
subcalculations are charged once.

\(C(n)\) is the minimum number of internal gates in such a certificate
for \(c_n\) on this seed. Independently generated rows are used only as
an oracle for the diagnostic. A small certificate whose witness choices
require the whole triangle is not a fast algorithm.

The light cone of \(c_n\) contains \(\sum_t\bigl(2\min(t,n-t)+1\bigr)
= n(n+2)/2\) internal cells for even \(n\) (e.g. \(33024\) at \(n=256\)).
The full width-\(t\) triangle is larger; the kill threshold is stated
against \(n^2\) as preregistered.

## Binary optimisation

Let \(y_{t,j}\in\{0,1\}\) indicate that gate \((t,j)\) is selected.
Write \(a=(t-1,j-1)\), \(b=(t-1,j)\), \(c=(t-1,j+1)\), and write \(y=0\)
for free cells.

\[
\min\sum y_{t,j}
\qquad\text{s.t.}\qquad
y_{n,0}=1,
\]
and, for every selected gate, the predecessor constraints determined by
the oracle values:

- \(y_a\ge y_{t,j}\) always;
- if \(b=c=0\), then \(y_b\ge y_{t,j}\) and \(y_c\ge y_{t,j}\);
- if exactly one of \(b,c\) is \(1\), that witness is required;
- if \(b=c=1\), then \(y_b+y_c\ge y_{t,j}\).

This is the exact integer programme for \(C(n)\). A certified lower
bound is available without solving the IP: the AND-forced closure \(F\)
of the output (unique predecessors, no 11-choices) is contained in every
certificate, and the unresolved 11-pairs inside \(F\) form a bipartite
graph of adjacent cells on the previous row. A maximum matching in that
graph is a set of extra internal vertices that cannot share, so

\[
C(n)\ge |F|+\nu(G).
\]

Branch-and-bound on the remaining 11-witnesses, pruning by this bound,
gives exact \(C(n)\) when it exhausts.

## Numbers

Tiny exact checks (search exhausted; bounds sandwich \(C\)):

| \(n\) | \(C(n)\) | LB | executable left | \(n^2\) |
| ---: | ---: | ---: | ---: | ---: |
| 4 | 9 | 6 | 10 | 16 |
| 8 | 37 | 37 | 40 | 64 |
| 12 | 71 | 62 | 72 | 144 |
| 16 | 107 | 107 | 107 | 256 |

Main table. “LB” is \(|F|+\nu(G)\). “UB” is the best circuit certificate
among oracle-greedy 11-policies and the executable evaluators (edge
identities \(x(t,\pm t)=1\) are **not** used as free gates in \(C(n)\)).
Exact search closed \(n=32\). It timed out at \(n=64,128,256\); the
reported intervals remain certified.

| \(n\) | \(n^2\) | \(0.1n^2\) | cone | LB | \(C(n)\) | UB | LB\(/n^2\) | exec left |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 32 | 1024 | 102.4 | 544 | 419 | **474** | 474 | 0.409 | 478 |
| 64 | 4096 | 409.6 | 2112 | 1635 | \([1635,1824]\) | 1824 | 0.399 | 1827 |
| 128 | 16384 | 1638.4 | 8320 | 6438 | \([6438,6580]\) | 6580 | 0.393 | 6587 |
| 256 | 65536 | 6553.6 | 33024 | 27139 | \([27139,27490]\) | 27490 | 0.414 | 27501 |

Update-check failures: 0 at every \(n\). Centre-bit failures: 0.

OR-kind histogram on the light cone is essentially balanced
(\(\approx 1/4\) each of `both0`, unique-\(b\), unique-\(c\), `either`).
Inside the forced closure the unresolved 11-pairs are rare: 3, 4, 9, 18
at \(n=32,64,128,256\). Almost all of the quadratic mass is AND-forced.

## Executable evaluator

The uniform machine receives only \(n\) and the seed. It evaluates
\(a\) always, then short-circuits the OR, with memoisation so each
gate is charged at most once.

- Left-first (try \(b=x(t-1,j)\) then maybe \(c\)): 478, 1827, 6587, 27501
  gates. Matches the packed centre bit.
- Right-first (try \(c\) then maybe \(b\)): the entire light cone
  (544, 2112, 8317, 33024). Preferring the right OR-input saves nothing
  after sharing.
- Spatial left-edge / right-edge order: identical to left-first /
  right-first on this neighbourhood.
- Optional extra: use the inductive identities \(x(t,\pm t)=1\) as base
  cases. That skips edge gates and drops to 450, 1771, 6486, 27287.
  Still \(\Theta(n^2)\), and it is not a circuit certificate for \(C(n)\).

Oracle-greedy 11-policies, which may inspect the whole triangle, beat
left-first by 4, 3, 7, 11 gates at \(n=32,64,128,256\). The gap is not
a complexity-class gap. Apparent savings relative to the cone are
real charged skips (cells reachable only as a right OR-input behind a
centre input already equal to 1). They are a constant-factor slice:
left-first still occupies \(0.88,0.87,0.79,0.83\) of the cone.

There is **no** executable subquadratic evaluator in this model.

## Why it died

Preregistered kill: retire if certified lower bounds already exceed
\(0.1n^2\) at **both** \(n=128\) and \(n=256\).

\[
C(128)\ge 6438>1638.4=0.1\cdot 128^2,
\qquad
C(256)\ge 27139>6553.6=0.1\cdot 256^2.
\]

Both fire. The AND-forced closure alone is already \(\approx 0.39n^2\)
and \(\approx 0.77\)–\(0.82\) of the light cone. Short-circuit choices
do not open a hole of size \(0.9n^2\).

The second preregistered kill (savings that exist only as uncharged
oracle values) did not need to fire: the oracle optimum and the
left-first evaluator differ by \(O(1)\) gates on these \(n\), and both
sit at \(\approx 0.4n^2\). The finite cutoff rejects this prototype. It
is not a lower bound for arbitrary algorithms, and it is not a prize
claim.
