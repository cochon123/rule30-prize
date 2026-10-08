# Trace of a short matrix product over \(\mathbb F_2\) and \(\mathbb F_3\)

Attack on prize problem 3, as specified in [_astra_ideas9.md](_astra_ideas9.md)
item 3. **UNSAT** in 26.031 s. The kill fired: no pair fitted the training set t=1,...,255. This is not a prize claim.

Certifier: `research/trace_product.py`. Dump:
`research/trace_product.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Family

For \(t\ge 1\) write \(b_1\cdots b_m=\operatorname{bin}(t)\) without
leading zeros, most significant bit first. The product is
\(M(t)=A_{b_1}\cdots A_{b_m}\). Sought readouts, over \(\mathbb F_2\) and
\(\mathbb F_3\), with \(d\in\{2,3\}\):

- \(c_t=\operatorname{Tr}(M(t))\);
- \(c_t=\operatorname{Tr}(M(t))+k\) for a field constant \(k\);
- \(c_t=M(t)_{11}\) (and, in the same pass, every other fixed entry);
- the affine shift of a fixed entry;
- for \(d=2\) only, \(c_t=\lambda^\top M(t)\rho\), and the same with \(+k\).

This is a representation of the **time index** of the single-cell seed,
not a Lax pair and not a spatial communication matrix of an apex \(f_h\).
It is also not the killed concatenation-rank freeze of dimension 16
over \(\mathbb F_3\) in [time_digit_matrices.md](time_digit_matrices.md):
that test asked whether some \(r\le 16\) linear representation exists, and
died at \(\ell=5\). The present freeze is the tiny explicit catalogue
\(d\le 3\), including the trace readout (which is not a length-\(d\)
linear representation) and the dimension-2 bilinear readout (which that
rank argument does not by itself enumerate).

Training times are \(t=1,\ldots,255\). Hold-out is \(t=256,\ldots,4095\).
Centre bits match `experiment.center_bits` on a prefix of length 256.
The product recurrence \(M(t)=M(\lfloor t/2\rfloor)A_{t\bmod 2}\) with
\(M(1)=A_1\) is MSB-first and is checked against an independent bit-loop
multiply on every recorded witness.

## Search

All \(p^{2d^2}\) matrix pairs are enumerated for
\((p,d)\in\{(2,2),(2,3),(3,2)\}\) in Python, using a full multiply table.
The \(\mathbb F_3\) \(3\times 3\) catalogue is \(3^{18}=387{,}420{,}489\)
pairs and is enumerated in C with OpenMP, aborting a pair as soon as
every readout family has failed. Affine constants are fixed at \(t=1\).
Dimension-2 linear representations enumerate \(\lambda,\rho\) (and \(k\))
on top of the \(2\times 2\) pairs. Cap two hours.

A planted \(\operatorname{Tr}\) model over \(\mathbb F_2\) on a fake
prefix is recovered by the same enumerator.

## Outcome

**Status: UNSAT. Wall time 26.031 s. Kill fired.**

Status `unsat` means no pair fitted \(t=1..255\). Hold-out was never reached.
`sat` would have been a hold-out survivor (still not a prize
claim without an induction to Rule 30).

| field \(p\) | \(d\) | pairs | readout | status | train SAT | hold-out SAT | wall |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: |
| 2 | 2 | 256 | `tr` | unsat | 0 | 0 | 0.001 s |
| 2 | 2 | 256 | `tr_affine` | unsat | 0 | 0 | 0.001 s |
| 2 | 2 | 256 | `entry11` | unsat | 0 | 0 | 0.001 s |
| 2 | 2 | 256 | `entry11_affine` | unsat | 0 | 0 | 0.001 s |
| 2 | 3 | 262{,}144 | `tr` | unsat | 0 | 0 | 2.917 s |
| 2 | 3 | 262{,}144 | `tr_affine` | unsat | 0 | 0 | 2.917 s |
| 2 | 3 | 262{,}144 | `entry11` | unsat | 0 | 0 | 2.917 s |
| 2 | 3 | 262{,}144 | `entry11_affine` | unsat | 0 | 0 | 2.917 s |
| 3 | 2 | 6{,}561 | `tr` | unsat | 0 | 0 | 0.026 s |
| 3 | 2 | 6{,}561 | `tr_affine` | unsat | 0 | 0 | 0.026 s |
| 3 | 2 | 6{,}561 | `entry11` | unsat | 0 | 0 | 0.026 s |
| 3 | 2 | 6{,}561 | `entry11_affine` | unsat | 0 | 0 | 0.026 s |
| 3 | 3 | 387{,}420{,}489 | `tr` | unsat | 0 | 0 | 21.741 s |
| 3 | 3 | 387{,}420{,}489 | `tr_affine` | unsat | 0 | 0 | 21.741 s |
| 3 | 3 | 387{,}420{,}489 | `entry11` | unsat | 0 | 0 | 21.741 s |
| 3 | 3 | 387{,}420{,}489 | `entry11_affine` | unsat | 0 | 0 | 21.741 s |

Every other fixed entry \(M(t)_{ij}\) (exact and affine) was screened in
the same pair enumeration: 44 of 44 auxiliary entry
families are unsat on training. Extra hold-out survivors: none.

### Dimension-2 linear representations \(\lambda^\top M\rho\)

| field \(p\) | readout | candidates | status | train SAT | hold-out SAT | wall |
| ---: | --- | ---: | --- | ---: | ---: | ---: |
| 2 | exact | 4{,}096 | unsat | 0 | 0 | 0.003 s |
| 2 | affine | 8{,}192 | unsat | 0 | 0 | 0.007 s |
| 3 | exact | 531{,}441 | unsat | 0 | 0 | 0.195 s |
| 3 | affine | 1{,}594{,}323 | unsat | 0 | 0 | 0.218 s |

Self-checks: centre prefix matches `experiment.center_bits` on 256
bits; multiply and MSB product recurrence agree on a hand example; a
planted \(\mathbb F_2\) trace model on a fake prefix is recovered and
holds out (planted_train_sat=True, holdout_ok=True).

Total wall time 26.031 s, inside the two-hour cap.

## Why it died

Preregistered kill: no pair fits the training set, or a fit fails
hold-out. No pair \(A_0,A_1\) of \(d\le 3\) matrices over \(\mathbb F_2\)
or \(\mathbb F_3\) realises \(c_t\) as \(\operatorname{Tr}\) of the
MSB-first \(\operatorname{bin}(t)\) product, as that trace plus a
constant, as a fixed matrix entry (including \((1,1)\)) plus an
optional constant, or as a dimension-2 linear representation
\(\lambda^\top M\rho\) (exact or affine), on the training times
\(t=1,\ldots,255\).

A survivor would still have needed an induction from the matrices to
Rule 30. Fitting alone is not a prize claim. Not a prize claim.

