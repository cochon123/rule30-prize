**Do not rerun \(d(k)\)-injectivity, seed-locked `fiber_left` of the prize
row, or adjacent \(1\)-run/\(0\)-run pairing.** Cycle R killed those.
The gap-4 SFT still contains the \(T=20\), \(R=16\) onset. These are
proposals.

1. **Injective square 2-kernel columns — Problem 1**

   Cycle R: for every \(k\le 9\), the \(2^k\) sequences
   \((c_{r+i 2^k})_{i=0}^{2^k-1}\) are pairwise distinct, and the
   shortest distinguishing prefix has length \(\min L(k)\in[k,2k+3]\).
   If this holds for all \(k\), the 2-kernel is infinite and \(c\) is
   not eventually periodic. The length-\(2^k\) matrix is *not* always
   full rank over \(\mathrm{GF}(2)\) (ranks \(3/4\), \(31/32\),
   \(127/128\) at \(k=2,5,7\)), so invertibility is the wrong target;
   distinct columns are enough. Kill if some \(k\) has a collision at
   length \(2^k\), or if no CA identity distinguishes two residues
   inside a bound depending only on \(k\). Survive only with a proof
   for all \(k\), not another prefix table.

2. **Long-range pairing of \(11\) with \(00\) — Problem 2**

   Cycle R: \(D(N)=N_{11}-N_{00}+c_{N-1}\). Local \(L_i=M_i\) is
   false. Seek a bijection (or \(o(N)\) unmatched) between \(11\)-pairs
   and \(00\)-pairs using the spacetime, not the 1-D run sequence:
   for example a matching along light-cone diagonals, or a sign on
   each defect from \(\ell_t\) versus \(r_t\). Kill if every window
   of radius \(\le 8\) about a \(11\) (resp. \(00\)) realises both
   signs of the next unmatched \(00\) (resp. \(11\)) with comparable
   frequency. Survive only with \(N_{11}-N_{00}=o(N)\).

3. **Odd-time zeros of column \(-1\) via a production gadget — Problem 1**

   Phase `01` forces \(x(2n+1,-1)=1\) eventually. Empirically that
   column is \(0\) on half of all odd times through \(2^{16}\). A
   finite spacetime gadget that, whenever it occurs at the right or
   left edge (both constantly \(1\)), produces a later odd-time
   \(11\) in the centre, would exclude period 2 for this seed. Kill
   if the gadget can be placed so that the centre \(11\) lands on
   even time, or if it does not recur from the single-1 edges.
   Distinct from screening unforced \(r_{2n}\) for membership in \(X\).

4. **Stop after (1)–(3) unless a \(T\)-uniform or \(k\)-uniform identity
   appears.** Another finite onset table, another hull census, and
   another driven-\(\sigma\) scan are not new mechanisms.
