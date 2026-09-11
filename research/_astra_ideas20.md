**Do not rerun \(F^p\) Kopra width, never-in-\(X\) for short prize-\(u\)
windows, or a longer de Bruijn prefix as a prize proof.** Cycle V: every
iterate \(F^p\) has width \(2p\). Prize \(u\) has length-8 factors in
\(X\). These are proposals.

1. **Infinitely many \(11\) in prize \(u_n=x(2n,1)\) — period 2 for this seed**

   A \(11\) in \(u\) is forbidden in \(X\). Cycle V sees 32738 of them in
   \(2^{17}\) even samples, last at the end of the prefix, max gap 46.
   Survive only with a CA production of infinitely many such pairs
   (e.g. a forced width-3 pattern at even times). Kill if some residue
   of even times is eventually \(11\)-free for a structural reason, or if
   the argument cannot reach other periods. This would exclude period 2
   for the prize seed only; periods 3–7 and \(q=8\) remain.

2. **Closed witness \(n_*\in\{1,2,3\}\) for \(v_k\) vs \(v_{k+1}\) — Problem 1**

   Empirically true through \(k=15\). The \(n_*=3\) case is three
   consecutive equal \(c_{2^k}\) saved by the length-3 sample. Survive
   only with a proof that those five bits cannot all match, for every
   \(k\). Then still need \(v_k\neq v_{k+m}\) for \(m\ge 2\) (period-2
   chain). Kill on one \(k\) with \(n_*>3\).

3. **Stop unless (1) or (2) becomes a proof.** Length-64 emptiness of
   \(X\) in one prefix, lag-disagreement bounds, and all-15-mer hunts
   are not new mechanisms. Problem 2 is still \(D(N)=o(N)\). Problem 3
   is still the official TM predicate.
