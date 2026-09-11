# Rule 30 prize research

Sustained attempt at the [Rule 30 prizes](https://rule30prize.org/).
**No prize problem is solved.** Do not submit or contact the committee
from this repo.

## Continue on another machine

```sh
git clone git@github.com:cochon123/rule30-prize.git
cd rule30-prize
python3 experiment.py --bits 1000
```

Read in this order:

1. [REPORT.md](REPORT.md) — checked conclusions and cycle summaries
2. [research/LOG.md](research/LOG.md) — what was tried and what died
3. The notes those files cite under `research/`

Last completed cycle is **AP**. Mersenne targets satisfy
\(G(m,2^a-1)=1\) iff \(2^a\mid(m+1)\); \(5\cdot 2^k-1\) has four
residues. Those laws give four unique-Green bits on the 3-fold
annulus. The prize is still open.

Do not overwrite `experiment.py`, `research/strip_graph.py`, or
`research/strip_extend.py`.

## Constraints that still hold

- Official site still open; width-1 center periodicity is the gap after
  Jen/Kopra (width-2 aperiodicity). Every iterate \(F^p\) has Kopra
  width \(2p\) (Cycle V), so the gap is not closed by passing to a
  power. An infinite 2-kernel would close it: \(v_k=v_{k+1}\) already
  forces \((c_{2^j})_{j\ge k}\) constant (Cycle Y). One doubling is
  \(c_{2^k}=c_{2^{k-1}}\oplus I_k\) with \(I_k\) the AND-Green remainder
  (Cycle Z). Every \(c_t\land r_t\) on that annulus hits \(I_k\)
  (Cycle AA); the off-centre remainder is the palindrome-defect
  parity \(\bigoplus(\ell\oplus r)\) and cannot be eventually the zero
  sequence (Cycle AB). Every left-diagonal \(x(t,-t+j)\) is eventually
  periodic; the centre is the onset \(e_t(t)\), not the tail
  (Cycle AC). Centre `00` is the triple `000` or `101`. Agreeing
  nonzero left-diagonals force a white stripe; \(e_7\equiv 0\) and
  \(e_{28}\equiv 0\) (Cycle AD). A finite family of left-diagonals
  meets the centred 5-window only finitely often, so nested left is
  not a `00` production. Right-diagonals are pure integrators with no
  white stripes; nested right is likewise not a `00` production
  (Cycle AE). The two-step Green identity for \(c_{s+2}\) has an older
  remainder \(O_s\) that is not identically 0, so local ANDs at a
  1-run ending do not force `00` (Cycle AF). On the prize orbit
  \(O_s\) is a local 5-window Boolean, equal to \(a\oplus e\) at
  1-run endings, so it is not a bulk `00` handle (Cycle AG). The same
  Freshman factorisation at times \(q\cdot 2^k\) gives
  \(c_{2qU}=c_{qU}\oplus\Delta^{(q)}\oplus J^{(q)}\); for \(q=1\) this
  is Cycle Z, and \(\Delta,J\) are not closed forms for
  \(q\in\{3,5,7,9\}\). Eventual period \(2^m r\) with \(r\) odd forces
  \((b_k)\) eventually periodic of period dividing \(\mathrm{ord}_r(2)\);
  \(r=1\) forces eventual constancy (Cycle AH). The one-step Green
  remainder is local, so it is not a bulk `00` or \(I_k\) handle.
  From any time \(t\), a power-of-2 step is
  \(c_{t+2^k}=c_t\oplus x(t,\pm 2^k)\oplus J_{t,k}\) with \(J\) causal
  of width \(2^{k+1}+1\) (Cycle AI); palindrome graphs at distance
  \(2\) and \(4\) have mixing SCCs, so they do not extend Cycle AB.
  The 3-fold remainder \(\theta_k=c_{3\cdot 2^k}\oplus c_{2^k}\)
  vanishes under eventual period \(2^m\); the leftmost 11 always hits
  it, so \(\theta_k=1\oplus S_k\) (Cycle AJ). The same remainder
  exists for every Fermat-odd \(q=2^a+1\), and the leftmost-11 hit
  parity is odd for the whole family (Cycle AK). The identity is not
  special to Fermat-odd \(q\): for every integer \(q\ge 1\) the
  Freshman edges cancel, so \(\varphi^{(q)}_k=J\), and the leftmost-11
  hit parity is \(1\oplus\mathrm{popcount}(q)\) (Cycle AL). Nested-left
  ANDs at packed bit 4 contribute 1 to every \(I_k\); bit 6 cancels
  it. With the period-4 forms of \(e_8\) and \(e_{10}\),
  \(I_k=1\oplus B_k^{\ge 10}\) for \(k\ge 5\) (Cycle AM). The
  generating function of \(W\) makes \(W(2^a,D)\) an interval of
  length \(2^a\); Mersenne and Fermat \(G\) have closed forms, and
  \(I_k\) splits by that interval into packed-index halves
  (Cycle AN). The time-\(T\) Mersenne slice is not a formula for
  \(I_k\). \(G(m,3\cdot 2^k-1)\) lives on two residue classes
  modulo \(2^{k+2}\), so the leftmost-11 hit for \(\theta_k\) is
  unique and occurs at time \(2^k\); \(N(q)\) is independent of
  \(k\) (Cycle AO). Mersenne targets obey
  \(G(m,2^a-1)=1\) iff \(2^a\mid(m+1)\), and \(5\cdot 2^k-1\) has a
  four-residue law; together they produce four unique-Green packed
  bits on the 3-fold annulus, of which only \(p=1\) always fires
  (Cycle AP).
- Infinitely many 0s and 1s in the center are proved.
- Isolated-zero periods `01^q` are excluded except `q ∈ {1,2,3,4,5,6,8}`.
- Period 2 has no uniform-in-onset bound (`maxR=16` at `T=20` is still
  the worst through `T=34`). The even right neighbor of a period-2
  centre has no five consecutive zeros, in addition to no consecutive
  1s. Origin-in-hull rows of weight `≤10` and span `≤20` (weight `≤8`
  through span 24) have `L_run≤31`. Off-hull weight-8 reaches 35.
  Periods 3–7 and `q=8` remain.
- Density and linear-time computation are untouched by a proof.
  Problem 2 is exactly \(N_{11}-N_{00}=o(N)\) via
  \(D(N)=N_{11}-N_{00}+c_{N-1}\). There is no finite-window coboundary
  or small-range bond flux for \(2c_t-1\) (Cycle X).

Helper scripts live in `research/`. Dumps are the matching `.json` files.
Astra briefs and idea lists are `research/_astra_brief*.md` and
`research/_astra_ideas*.md`.
