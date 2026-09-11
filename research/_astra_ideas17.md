**Do not rerun \(F^2\) Condrey iteration, radius-\(\le 8\) spatial pairing
of \(11\) with \(00\), or a width-8 half-time right-edge gadget.** Cycle S
killed those. The lag-2 inverse of \(F^2\) is \(F_2=u\) on phase `01`.
These are proposals.

1. **Injective square 2-kernel columns — Problem 1**

   Still the only listed route to an infinite kernel. Cycle R: distinct
   length-\(2^k\) prefixes through \(k=9\); first disagreement is not
   a function of \(r\oplus s\). Survive only with a proof for all \(k\).
   Kill on a single collision at length \(2^k\).

2. **Generating function of \(N_{11}-N_{00}\) from the packed row — Problem 2**

   Cycle R: \(D(N)=N_{11}-N_{00}+c_{N-1}\). Cycle S: no radius-8 spatial
   pairing. Write \(d_t=c_t\oplus c_{t+1}\) (a \(00\) or \(11\) is
   \(d_t=0\)) and \(s_t=2c_t-1\), so a \(11\) contributes \(+s_t\) wait
   no: a \(11\) is \(c_t=1,d_t=0\). Seek an identity that expresses
   \(N_{11}-N_{00}\) as a boundary term of the packed integer \(z_t\)
   (popcount of a simple Boolean of \(z_t,z_t{\ll}1\)), with an error
   \(o(t)\) after summing. Kill if every local Boolean of
   \((c,\ell,r,d)\) that matches \(1_{11}-1_{00}\) on a prefix fails
   at a later \(t\le 2^{14}\). Survive only with \(D(N)=o(N)\).

3. **Stop after (1)–(2) unless a \(k\)-uniform or summed-boundary identity
   appears.** Another finite onset table, another hull census, and
   another driven-\(\sigma\) scan are not new mechanisms.
