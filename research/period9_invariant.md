# q=8: local invariant excluding the vacuum quotient I

**Status.** q=8 is not excluded. No local invariant \(K\) of the form
Astra asked for was found. This is not a prize claim.

Helper: `research/period9_invariant.py`. Dump: `research/period9_invariant.json`.
Does not modify `strip_graph.py`, `strip_extend.py`, or `period9_sigma.py`.

Notation as in `period9_sigma.md`. Reconstruction is the one-sided CA

\[
S_{k+1}(n)=H(S_k(n),S_k(n+1)),
\]

with \(S_k(n)=(W_{k-1}(n),W_k(n))\) an 18-bit symbol and
\(S_1(n)=(011111111,\sigma_n00000001)\). The vacuum quotient \(I\) is
the 512-state set of symbols whose wrap-bit stream in the depth
direction is eventually the all-zero wrap of an \(L_0\) tail.

Target: a set \(K\) given by relations on 2–3 neighboring symbols with
all initial streams in \(K\), \(H(K)\subseteq K\), and \(K\cap I=\emptyset\).

## What the machine check shows

- Both initial symbols lie outside \(I\). All four initial 2-blocks
  are legal.
- Observed consistent symbols through the collected depths never meet
  \(I\) (rank stays small; same computational fact as
  `period9_sigma.md`).
- **1-site:** the full 2-shift on the union of observed symbols
  *does* enter \(I\). A 1-site invariant on those symbols cannot exist.
- **2-site / 3-site H-closure** of the observed union stays \(I\)-free
  through the allotted rounds (2-site: 92 pairs / 46 symbols after 14
  extra rounds; 3-site still growing at round 20) and **does not
  stabilize**. That is not an invariant.
- Pairwise local filters do not forbid \(I\) as a symbol
  (`pairwise_forbids_I_as_symbol: false`).
- Complement of \(I\) is not 1-site invariant: 512 non-\(I\) states
  have a wrap into \(I\).

Any \(K\) that contains all initial streams and is \(H\)-invariant must
contain every consistent block at every depth, hence the observed
finite union. A 1-site language on that union already meets \(I\).
A 2- or 3-site language might still avoid \(I\), but the smallest
invariant extensions we closed did not settle: they neither hit \(I\)
nor closed. Extending the depth table is exactly the obstruction Astra
named. No initialization-and-preservation proof was obtained.

## Strongest honest statement

q=8 is not excluded. The wrap-coordinate \(I\) is a genuine \(L_0\)
obstruction in the depth direction, but no finite-block invariant
separating consistent \(\sigma\)-streams from \(I\) was found. The
1-site full shift on observed symbols enters \(I\); 2- and 3-site
closures of the observed union neither enter \(I\) nor stabilize.
Large onset \(T\) remains open, as in `period9_sigma.md`.
