# Cycle R: kernel disagreement, seed-locked fiber, pair discrepancy

Three attacks. Two hit their kill criteria. The third is an exact
rewrite of Problem 2, not a solution. Not a prize claim.

Helper: `python3 research/cycle_r.py --certify`. Dump:
`research/cycle_r.json`. Packed centre matches `experiment.center_bits`.
Uses `fiber_left` from `research/period2_fiber.py` without modifying
that file.

## 1. First disagreement of \(v_k=(c_{2^k n})\) against \(v_0\)

Let \(d(k)=\min\{n\ge 1:c_n\ne c_{n\cdot 2^k}\}\). If \(d\) were
injective, the even-decimation chain would be pairwise distinct, the
2-kernel would be infinite, and \(c\) would not be eventually
periodic. Predeclared kill: \(d\) not injective on the computed range,
and no closed form among \(d(k)\in\{1,k,k+1,2^k,2^k-1\}\) or
strict increase of \(d\) / of the odd-restricted \(d\).

On \(N=2^{18}\) bits, \(k=1,\ldots,14\):

```
d(k) = 1,2,2,5,1,2,2,3,1,5,1,2,3,1
```

Repeats \(d=1\) five times (exactly the \(k\) with \(c_{2^k}=0\), since
\(c_1=1\)). Not injective. The power-of-two centre bits themselves mix:

```
c_{2^k} = 1,0,1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,0   (k=0..17)
```

Same obstruction as `research/two_kernel.md`: \(n_*=1\) already fails
at \(k=2\) (\(c_4=c_8=1\)). No replacement family with a uniform
predicted index. **Killed** as an infinite-kernel proof.

What remains of the kernel screen, and is not a lemma: the \(2^k\)
residues at depth \(k\) have distinct length-\(L\) prefixes with

| \(k\) | \(\min L\) | length-\(2^k\) columns distinct |
| ---: | ---: | :---: |
| 0 | 1 | yes |
| 1 | 2 | yes |
| 2 | 4 | yes |
| 3 | 4 | yes |
| 4 | 7 | yes |
| 5 | 9 | yes |
| 6 | 13 | yes |
| 7 | 17 | yes |
| 8 | 18 | yes |
| 9 | 17 | yes |

So \(\min L\) is not \(k\), and is not bounded. Distinct square
columns through \(k=9\) (512 residues, length-512 prefixes, \(N\)
exactly supports the last index \(2^{18}-1\)) is a period lower
bound \(p\ge 512\) under eventual periodicity, weaker than the
already-recorded \(|K|\ge 4096\) at depth 12. It is not an infinite
family.

## 2. Prize-seed left edge versus `fiber_left`

At time \(T\) the prize row has left edge \(x(T,-T)=1\). The unique
left compatible with the actual right half and a period-2 centre
starting at \(c_T\) is `fiber_left`. If the predicted bit at spatial
\(-T\) were \(0\) for every \(T\ge 1\), no onset could occur.

Through \(T=192\): predicted edge is \(0\) for 92 onsets and \(1\) for
100. The only full left-match is the trivial \(T=1\) (one reconstructed
bit). First disagreement indices:

| index (spatial) | count |
| ---: | ---: |
| 0 (\(-1\)) | 102 |
| 1 (\(-2\)) | 50 |
| 2 | 17 |
| 3 | 10 |
| 4 | 6 |
| 5 | 4 |
| 6 | 2 |

Disagreement at column \(-1\) is exactly \(c_{T+1}\) failing to
continue period 2, a one-step restatement of the centre sequence.
No fixed column and no light-cone identity. **Killed.**

Column \(x(t,-1)\) itself has 16425 zeros on odd times and 16350 on
even times through \(t<2^{16}\), last odd zero at \(t=65535\). Phase
`01` would require the odd-time left neighbor eventually \(1\). This
is finite evidence, not a production lemma. Do not claim infinitely
many odd zeros of column \(-1\).

## 3. Pair discrepancy (Problem 2 rewrite)

**Lemma.** Let \(D(N)=\sum_{t<N}(2c_t-1)=2\cdot\#\{t<N:c_t=1\}-N\),
and write \(N_{11}\) (resp. \(N_{00}\)) for the number of consecutive
pairs \(11\) (resp. \(00\)) among \((c_t,c_{t+1})_{t<N-1}\). Then

\[
D(N)=N_{11}-N_{00}+c_{N-1}.
\]

Proof. Among the \(N-1\) pairs, \(N_{11}+N_{10}=\#\{t<N-1:c_t=1\}=
\#1s-c_{N-1}\) and \(N_{00}+N_{01}=\#0s-(1-c_{N-1})\). Also
\(N_{01}-N_{10}=c_{N-1}-c_0\). Subtracting and using \(c_0=1\) gives
the identity. Certified on a length-256 prefix against
`experiment.center_bits` and on \(N=2^{18}\) (`pairs.identity_ok`).

Thus Problem 2 is exactly \(N_{11}-N_{00}=o(N)\). Cycle K showed that
*unsigned* defect density stays \(\approx 1/2\), which kills “few
defects \(\Rightarrow D=o(N)\)” but does **not** kill signed
cancellation of \(11\) against \(00\).

A local pairing that identified the \(i\)-th \(1\)-run length \(L_i\)
with the following \(0\)-run length \(M_i\) fails: only \(33.5\%\) of
adjacent pairs have \(L_i=M_i\) at \(N=2^{18}\), and the conditional
law of \(M_i\) given \(L_i\) is still geometric (independent-looking).
**Killed** as a local run-length pairing. A long-range matching of
\(11\)-blocks with \(00\)-blocks remains open and would finish
Problem 2.

At \(N=2^{18}\), \(D=634\), \(N_{11}=65797\), \(N_{00}=65163\). Both
factors persist to the end of the window (`last11=262138`,
`last00=262142`). Finite evidence of infinitely many \(00\) and
\(11\), which would exclude period 2, is not a proof.

## Verdict

`KILLED` (kernel injectivity, seed-locked edge, local run pairing),
wall time 4.1s. Exact \(D(N)\) identity survives as a rewrite.
Prize unsolved.

## Files

- `research/cycle_r.md` (this note)
- `research/cycle_r.py`
- `research/cycle_r.json`
