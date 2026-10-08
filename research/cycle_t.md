# Cycle T: isolated-one strips, packed \(D\) current, kernel \(\varphi_k\)

Three attacks. All three hit their kill criteria. Square 2-kernel
columns remain distinct through \(k=9\) (same finite bound as Cycle R).
Not a prize claim.

Helper: `python3 research/cycle_t.py --certify`. Dump:
`research/cycle_t.json`. Calls `strip_graph.analyze` without modifying
that file. Packed centre matches `experiment.center_bits` on 20 bits.

## 1. Isolated-one words \(10^q\)

The dual of isolated zeros: centre word \(1\) then \(q\) zeros. At
radius 6, **every** \(q=1,\ldots,17\) has a residual recurrent SCC
(no forced periodic neighbor). Residual sizes grow (84 at \(q=1\),
724 at \(q=17\)). Period 2 is \(q=1\); \(q=2,3\) are the period-3/4
necklaces \(100\) and \(1000\) already open in
`research/small_periods.md`. There is no Jen tail for large \(q\).
**Killed.**

## 2. Packed current for \(D(N)\)

Over \(\mathbb Z\), \(e_t=1_{11}(t)-1_{00}(t)=c_t+c_{t+1}-1\). Summing
recovers Cycle R: \(D(N)=N_{11}-N_{00}+c_{N-1}\). Certified on a
length-20 prefix and on \(N=2^{12}\) (`e_sum_identity`).

This is a restatement of Problem 2, not a current. On \(N=2^{12}\):

- \(\mathrm{corr}(D,\mathrm{excess\ popcount\ of\ row})=-0.005\)
- \(D=\mathrm{excess}\) on 28 of 4096 times
- \(|D|=40\), so no bounded local \(J\) with \(e=\Delta J\)

A packed popcount Boolean does not carry \(D\). **Killed.**

## 3. \(\varphi_k\) injectivity template

Let \(\varphi_k(r)=\min\{i:c_{i 2^k}\ne c_{r+i 2^k}\}\) for
\(1\le r<2^k\). If \(\varphi_k\) is injective then the \(2^k\) kernel
columns are pairwise distinct (each first-disagrees with residue 0 at a
unique index, hence they disagree with each other). The template dies
at \(k=3\): only 3 distinct \(\varphi\)-values among 7 residues.
Square columns of length \(2^k\) are nevertheless distinct through
\(k=9\) on \(N=2^{18}\) (need \(2^{20}\) for \(k=10\), not run). A
finite distinct-column table is not an infinite kernel. **Template
killed**; the square census is unchanged.

## Verdict

`KILLED` (all three), wall time 5.2s. Prize unsolved.

## Files

- `research/cycle_t.md` (this note)
- `research/cycle_t.py`
- `research/cycle_t.json`
